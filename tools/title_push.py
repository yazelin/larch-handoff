# -*- coding: utf-8 -*-
"""把自訂標題畫面寫進 Larch 專案（上下篇共用）：上傳動態 AVIF → 設定只改縮圖（與標題音樂）→ PUT /interface 寫標題 HTML → 讀回核對。
不整包 PUT 專案，所以不會動到版子。結果記在各自 repo（下篇 larch.json、上篇 assets/title.json），重推時沿用。
  python3 tools/title_push.py handoff|start
"""
import base64, json, os, sys, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from title_html import html

KEY = open(os.path.expanduser('~/.config/larch/key')).read().strip()
API = 'https://larch.ink/api/agent/projects'
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START = os.path.expanduser('~/larch-start-line')


def req(method, url, body=None, etag=None):
    h = {'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json'}
    if etag: h['If-Match'] = etag
    data = json.dumps(body, ensure_ascii=False).encode() if body is not None else None
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data, h, method=method), timeout=180) as r:
            return r.headers.get('ETag'), json.loads(r.read() or b'{}')
    except urllib.error.HTTPError as e:
        raise SystemExit(f'{method} {url} → {e.code} {e.read()[:400]}')


def main(work):
    if work == 'handoff':
        state_file = os.path.join(R, 'larch.json'); loop = os.path.join(R, 'assets/art/cover/title_loop.avif')
    else:
        state_file = os.path.join(START, 'assets/title.json'); loop = os.path.join(START, 'assets/art/cover/title_loop.avif')
    state = json.load(open(state_file)) if os.path.exists(state_file) else {}
    if work == 'start' and 'project_id' not in state:   # 上篇的專案 id 寫在 src/build.py
        import re
        state['project_id'] = re.search(r"PROJECT_ID\s*=\s*'([^']+)'", open(os.path.join(START, 'src/build.py')).read()).group(1)
    pid = state['project_id']
    url = f'{API}/{pid}'

    if not state.get('title_loop_url'):
        _, j = req('POST', url + '/media', {'name': f'{work}_title_loop.avif', 'mimeType': 'image/avif', 'category': 'scene',
                                             'base64': base64.b64encode(open(loop, 'rb').read()).decode()})
        state['title_loop_id'], state['title_loop_url'] = j['asset']['id'], j['asset']['url']
        json.dump(dict(state, project_id=pid), open(state_file, 'w'), ensure_ascii=False, indent=1)
        print('上傳', state['title_loop_url'])

    _, cur = req('GET', url)
    p = cur.get('project', cur); s = p.get('settings') or {}
    # 下篇的縮圖、標題音樂、簡介由 tools/push.py 寫

    old = ((s.get('customInterfaces') or {}).get('title') or {}).get('html') or ''
    page = html(work, 'media:' + state['title_loop_id'])
    req('PUT', url + '/interface', {'surface': 'title', 'html': page, 'enabled': True, 'expectedHtml': old,
                                    'summary': '自訂標題畫面：動態封面、上下篇同一套版型'})

    if work == 'start':   # 上篇：只改縮圖（設定端點若不收，交給上篇自己的推送程式）
        try:
            rev, sj = req('GET', url + '/settings')
            req('PATCH', url + '/settings', {'summary': '標題畫面：動態縮圖', 'changes': {'projectThumbnail': state['title_loop_url']}},
                f'"{sj.get("revision")}"' if sj.get('revision') is not None else rev)
        except SystemExit as e:
            print('縮圖沒改成（設定端點不收）：', e)
    _, back = req('GET', url)
    b = back.get('project', back)['settings']
    ok = (b.get('customInterfaces') or {}).get('title', {}).get('html') == page
    print('縮圖', '已換成動圖' if b.get('projectThumbnail') == state['title_loop_url'] else '還是舊的')
    print(work, '讀回核對', '通過' if ok else '失敗', '｜縮圖', b.get('projectThumbnail'), '｜封面', b.get('titleCoverImage'))
    if not ok: sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1])
