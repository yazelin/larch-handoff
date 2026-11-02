"""推到 Larch（私人專案，不發佈）：圖走 jsDelivr 孤兒 tag → 換網址 → 整包 PUT → 讀回比對。

    python3 tools/push.py "這次改了什麼"

專案 id 記在 larch.json（第一次跑會建專案）。金鑰只從 ~/.config/larch/key 讀，不進 repo。
"""
import json, os, re, subprocess, sys, hashlib, pathlib, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
STATE = ROOT / 'larch.json'
KEY = open(os.path.expanduser('~/.config/larch/key')).read().strip()
API = 'https://larch.ink/api/agent/projects'
REPO = 'yazelin/larch-handoff'


def req(method, url, body=None, etag=None):
    h = {'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json'}
    if etag: h['If-Match'] = etag
    data = json.dumps(body, ensure_ascii=False).encode() if body is not None else None
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data, h, method=method), timeout=180) as r:
            return r.headers.get('ETag'), json.loads(r.read() or b'{}')
    except urllib.error.HTTPError as e:
        raise SystemExit(f'{method} {url} → {e.code} {e.read()[:300]}')


def git(*a):
    return subprocess.run(['git', '-C', str(ROOT), *a], check=True, capture_output=True, text=True).stdout.strip()


def jsd_tag(paths):
    """只放用到的檔案的孤兒 commit，打 tag（同一組檔案同一個 tag）。"""
    env = dict(os.environ, GIT_INDEX_FILE=str(ROOT / '.git/push-index'))
    ls = subprocess.run(['git', '-C', str(ROOT), 'ls-tree', '-r', '-z', 'HEAD', '--', *paths], check=True, capture_output=True, env=env).stdout
    if ls.count(b'\0') != len(paths): raise SystemExit('有用到的檔案還沒 commit')
    subprocess.run(['git', '-C', str(ROOT), 'read-tree', '--empty'], check=True, env=env)
    subprocess.run(['git', '-C', str(ROOT), 'update-index', '-z', '--index-info'], input=ls, check=True, env=env)
    tree = subprocess.run(['git', '-C', str(ROOT), 'write-tree'], check=True, capture_output=True, text=True, env=env).stdout.strip()
    os.remove(env['GIT_INDEX_FILE'])
    tag = 'assets-' + tree[:10]
    if not git('tag', '-l', tag):
        git('tag', tag, git('commit-tree', tree, '-m', 'jsDelivr：交棒總在終點後'))
        git('push', 'origin', tag)
    return tag


def main(summary):
    text = (ROOT / 'project.json').read_text()
    paths = sorted(set(re.findall(r'"(assets/[^"]+)"', text)))
    tag = jsd_tag(paths)
    cdn = f'https://cdn.jsdelivr.net/gh/{REPO}@{tag}/'
    for p in paths:
        try:
            urllib.request.urlopen(urllib.request.Request(cdn + p, method='HEAD'), timeout=60)
        except urllib.error.HTTPError as e:
            raise SystemExit(f'jsDelivr 拿不到 {p}：{e.code}')
    built = json.loads(re.sub(r'"(assets/[^"]+)"', lambda m: f'"{cdn}{m.group(1)}"', text))

    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    if 'project_id' not in state:
        _, j = req('POST', API, {'name': built['name']})
        state['project_id'] = j.get('project', j)['id']
        STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1) + '\n')
        print('建了新專案', state['project_id'])
    url = f"{API}/{state['project_id']}"

    etag, cur = req('GET', url)
    project = dict(cur.get('project', cur))
    project['name'] = built['name']
    project['boards'] = built['boards']
    project['activeBoardId'] = built['boards'][0]['id']
    project.pop('nodes', None); project.pop('edges', None)
    req('PUT', url, {'project': project, 'summary': summary}, etag)

    _, back = req('GET', url)
    back = back.get('project', back)
    for b, w in zip(back['boards'], built['boards']):
        if (len(b['nodes']), len(b['edges'])) != (len(w['nodes']), len(w['edges'])):
            raise SystemExit(f"讀回比對失敗：{b['id']} {len(b['nodes'])}/{len(b['edges'])} ≠ {len(w['nodes'])}/{len(w['edges'])}")
    print(f'推送完成：{len(paths)} 個素材（{tag}），讀回比對通過')
    _, prev = req('GET', url + '/preview?boardId=main&hours=24')
    print('預覽', prev.get('url') or prev.get('playUrl') or prev)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '更新')
