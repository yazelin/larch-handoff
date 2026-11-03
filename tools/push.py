"""推到 Larch（私人專案，不發佈）：素材照類型與路線分組，各打一個 jsDelivr 孤兒 tag → 換網址 → 整包 PUT → 讀回比對。

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


GROUP_MB = 40   # 一組上限（jsDelivr 一個版本 50 MB 就 403，留空間補檔）


def group_of(p):
    """素材分組：配樂兩組、圖照路線分四組。遊戲與公開站共用同一套分組，改一張圖只重打那一組。"""
    name = os.path.basename(p)
    if p.startswith('assets/audio/full/'): return 'ost'
    if p.startswith('assets/audio/'): return 'bgm'
    return {'N': 'img-living', 'T': 'img-photo', 'F': 'img-mirror'}.get(name[0], 'img-common')


def cdn_map(paths):
    """每一組打一個孤兒 tag，回傳 {路徑: jsDelivr 網址}，並逐一 HEAD 確認拿得到。"""
    groups = {}
    for p in paths: groups.setdefault(group_of(p), []).append(p)
    out = {}
    for g, ps in sorted(groups.items()):
        mb = sum(os.path.getsize(ROOT / p) for p in ps) / 1e6
        if mb > GROUP_MB: raise SystemExit(f'{g} 有 {mb:.1f} MB，超過 {GROUP_MB} MB，要再拆')
        tag = jsd_tag(sorted(ps), g)
        for p in ps: out[p] = f'https://cdn.jsdelivr.net/gh/{REPO}@{tag}/{p}'
        print(f'  {g}：{len(ps)} 個、{mb:.1f} MB → {tag}', flush=True)
    for p, u in out.items():
        try: urllib.request.urlopen(urllib.request.Request(u, method='HEAD'), timeout=60)
        except urllib.error.HTTPError as e: raise SystemExit(f'jsDelivr 拿不到 {p}：{e.code}')
    return out


def all_paths():
    """遊戲（project.json＋封面）與公開站用到的全部素材。兩邊都用這一份分組，同一組只會有一個 tag。"""
    sys.path.insert(0, str(ROOT / 'tools'))
    from cg_jobs import latest
    cover = os.path.relpath(latest('assets/art/cg', 'COVER'), ROOT)
    game = set(re.findall(r'"(assets/[^"]+)"', (ROOT / 'project.json').read_text())) | {cover}
    site = ''.join((ROOT / 'docs' / f).read_text() for f in ('index.html', 'assets-site/tracks.js', 'music/index.html'))
    site = {'assets/' + p for p in re.findall(r'"((?:art|audio)/[^"]+\.(?:webp|mp3))"', site)}
    return sorted(game | site), cover, sorted(site)


def jsd_tag(paths, prefix):
    """只放這組檔案的孤兒 commit，打 tag（同一組檔案同一個 tag；tag 名不用 v＋數字開頭）。"""
    env = dict(os.environ, GIT_INDEX_FILE=str(ROOT / '.git/push-index'))
    ls = subprocess.run(['git', '-C', str(ROOT), 'ls-tree', '-r', '-z', 'HEAD', '--', *paths], check=True, capture_output=True, env=env).stdout
    if ls.count(b'\0') != len(paths): raise SystemExit('有用到的檔案還沒 commit')
    subprocess.run(['git', '-C', str(ROOT), 'read-tree', '--empty'], check=True, env=env)
    subprocess.run(['git', '-C', str(ROOT), 'update-index', '-z', '--index-info'], input=ls, check=True, env=env)
    tree = subprocess.run(['git', '-C', str(ROOT), 'write-tree'], check=True, capture_output=True, text=True, env=env).stdout.strip()
    os.remove(env['GIT_INDEX_FILE'])
    tag = f'{prefix}-{tree[:10]}'
    if not git('tag', '-l', tag):
        git('tag', tag, git('commit-tree', tree, '-m', 'jsDelivr：交棒總在終點後'))
        git('push', 'origin', tag)
    return tag


def main(summary):
    paths, cover, _ = all_paths()   # cover：標題畫面底圖與專案縮圖
    text = (ROOT / 'project.json').read_text()
    urls = cdn_map(paths)
    built = json.loads(re.sub(r'"(assets/[^"]+)"', lambda m: f'"{urls[m.group(1)]}"', text))

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
    settings = dict(project.get('settings') or {})
    settings['titleCoverImage'] = settings['projectThumbnail'] = urls[cover]
    project['settings'] = settings
    req('PUT', url, {'project': project, 'summary': summary}, etag)

    _, back = req('GET', url)
    back = back.get('project', back)
    for b, w in zip(back['boards'], built['boards']):
        if (len(b['nodes']), len(b['edges'])) != (len(w['nodes']), len(w['edges'])):
            raise SystemExit(f"讀回比對失敗：{b['id']} {len(b['nodes'])}/{len(b['edges'])} ≠ {len(w['nodes'])}/{len(w['edges'])}")
    if back.get('settings', {}).get('projectThumbnail') != urls[cover]: raise SystemExit('讀回比對失敗：封面沒寫進去')
    print(f'推送完成：{len(paths)} 個素材，讀回比對通過')
    _, prev = req('GET', url + '/preview?boardId=main&hours=24')
    print('預覽', prev.get('url') or prev.get('playUrl') or prev)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '更新')
