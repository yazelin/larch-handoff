# -*- coding: utf-8 -*-
"""公開站的查證紀錄頁：canon/查證紀錄.md → docs/sources/index.html。只認這份檔案用到的寫法（#、##、###、兩層清單、網址）。
  python3 tools/build_site.py
"""
import html, os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return re.sub(r'(https?://[^\s<）]+)', lambda m: f'<a href="{m.group(1)}" target="_blank" rel="noopener">{html.unescape(m.group(1))[:72]}</a>', s)


def md(src):
    out, depth = [], 0
    def close(to):
        nonlocal depth
        while depth > to: out.append('</li></ul>'); depth -= 1
    for line in src.splitlines():
        m = re.match(r'( *)- (.*)', line)
        if m:
            d = len(m.group(1)) // 2 + 1
            if d > depth: out.append('<ul><li>'); depth += 1
            else: close(d); out.append('</li><li>')
            out.append(inline(m.group(2))); continue
        close(0)
        if line.startswith('### '): out.append(f'<h3>{inline(line[4:])}</h3>')
        elif line.startswith('## '): out.append(f'<h2>{inline(line[3:])}</h2>')
        elif line.startswith('# '): continue
        elif line.strip(): out.append(f'<p>{inline(line)}</p>')
    close(0)
    return '\n'.join(out)


PAGE = '''<!doctype html>
<html lang="zh-Hant" data-skin="cheng">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>查證紀錄 · 交棒總在終點後</title>
<meta name="description" content="《交棒總在終點後》寫信時查過的事實與來源：懷孕與生產、憂鬱症住院、跨性別醫療與法規、田徑規則。">
<link rel="canonical" href="https://yazelin.github.io/larch-handoff/sources/">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=LXGW+WenKai+TC:wght@400;700&family=Noto+Serif+TC:wght@400;600&family=Noto+Sans+TC:wght@400;500;700&display=swap">
<link rel="stylesheet" href="../assets-site/site.css">
<link rel="stylesheet" href="../assets-site/skins.css">
<style>
body{background:var(--paper)}
.doc{max-width:46em;margin:0 auto;padding:96px 16px 64px;font-size:16px;line-height:1.9}
.doc h1{font-family:var(--f-display);font-weight:400;font-size:clamp(28px,5vw,42px);margin:0 0 8px}
.doc h2{font-family:var(--f-display);font-weight:400;font-size:26px;margin:56px 0 12px;padding-top:12px;border-top:1px solid var(--line)}
.doc h3{font-size:18px;margin:32px 0 6px}
.doc ul{margin:0;padding-left:1.3em}
.doc a{color:var(--accent);word-break:break-all}
.doc .lead{color:var(--ink-2)}
</style>
</head>
<body>
<header class="top" data-solid>
  <div class="wrap in">
    <a class="brand" href="../"><i aria-hidden="true"></i><span>交棒總在終點後</span></a>
    <a class="home" href="../" style="margin-left:auto">← 回首頁</a>
  </div>
</header>
<main class="doc">
<h1>查證紀錄</h1>
<p class="lead">寫這封信時查過的事實。每一項寫結論、用在哪一句、來源；查不到的另外列出，維持一般經驗的寫法。</p>
%s
</main>
<script src="../assets-site/site.js"></script>
</body>
</html>
'''

def gallery():
    """圖庫資料：CG 清單的每一段 → docs/assets-site/gallery.js（用遊戲裡實際選定的那一版）。"""
    import json, sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from cg_jobs import latest
    up = {"C04": "art/cg/upstream/cg-vending.webp", "F04": "art/cg/upstream/cg-gaze.webp"}
    secs, cur = [], None
    for line in open(os.path.join(R, 'canon', 'CG清單.md'), encoding='utf-8'):
        m = re.match(r'## (.+)', line)
        if m:
            name = m.group(1).split('（')[0].strip()
            cur = None if name in ('年紀時間線', '合計') else {'name': name, 'items': []}
            if cur: secs.append(cur)
            continue
        m = re.match(r'\| ([A-Z]+[0-9]+[ab]?) \| ([^|]+) \|', line)
        if cur and m:
            cid, title = m.group(1), m.group(2).strip()
            path = up.get(cid) or (latest('assets/art/cg', cid) and os.path.relpath(latest('assets/art/cg', cid), os.path.join(R, 'assets')))
            if path and cid not in ('C06', 'C11'): cur['items'].append([path, title])
    open(os.path.join(R, 'docs', 'assets-site', 'gallery.js'), 'w', encoding='utf-8').write(
        '/* 由 tools/build_site.py 從 canon/CG清單.md 產生，路徑相對於 assets/ */\nwindow.GALLERY = ' + json.dumps(secs, ensure_ascii=False, indent=1) + ';\n')
    return sum(len(s['items']) for s in secs)


if __name__ == '__main__':
    print('圖庫', gallery(), '張')
    src = open(os.path.join(R, 'canon', '查證紀錄.md'), encoding='utf-8').read()
    src = src.split('\n', 3)[3] if src.startswith('# ') else src   # 跳過標題與內部說明那段
    os.makedirs(os.path.join(R, 'docs', 'sources'), exist_ok=True)
    open(os.path.join(R, 'docs', 'sources', 'index.html'), 'w', encoding='utf-8').write(PAGE % md(src))
    print('docs/sources/index.html')
    if '--tag' in __import__('sys').argv:   # 公開站用到的素材照 push.py 同一套分組打 tag，網址寫進 docs/site.json
        import json, sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from push import all_paths, cdn_map
        everything, _, paths = all_paths()
        urls = cdn_map(everything)   # 跟遊戲同一套 tag
        sj = os.path.join(R, 'docs', 'site.json'); j = json.load(open(sj))
        j.pop('assetBase', None)
        j['assets'] = {p[len('assets/'):]: urls[p] for p in paths}
        open(sj, 'w').write(json.dumps(j, ensure_ascii=False, indent=1) + '\n')
        print(len(paths), '個素材寫進 docs/site.json')
