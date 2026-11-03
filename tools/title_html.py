# -*- coding: utf-8 -*-
"""上下篇共用的自訂標題畫面（Larch customInterfaces.title）。版型同一套，配色與導語各自。
從 ~/.claude/skills/larch-vn/title-template.html 改：書名與按鈕在左、人物在右，動態 AVIF 疊在靜態封面上。
  python3 tools/title_html.py preview <資料夾>  → 本機預覽頁（素材用本機檔案、書名先填好），印出檔案位置
  from title_html import html; html('handoff', loop_id)  → 寫進 Larch 的那份
"""
import os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WORKS = {
    'start': dict(eyebrow='上篇', mpos='84%', line='槍響之前，有些事早就決定了。', accent='#e0432a', accent2='#ff7a5e', ink='#f4f6fb', shade='10,17,34'),
    'handoff': dict(eyebrow='下篇', mpos='90%', line='信寫到一半，她停下筆，抬頭看了一眼。', accent='#e8a04a', accent2='#ffc983', ink='#fbf6ee', shade='28,20,30'),
}

TEMPLATE = '''<style>
:root { color-scheme: dark; }
* { box-sizing: border-box; }
html, body { margin: 0; height: 100%; background: rgb({{shade}}); }
.cover { position: relative; min-height: 100dvh; overflow: hidden; color: {{ink}};
  font-family: "Noto Serif TC", "Songti TC", "PMingLiU", serif; }
.art, .loop { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 62% 50%; pointer-events: none; }
.loop { opacity: 0; transition: opacity 1.2s ease; }
.loop.is-playing { opacity: 1; }
.shade { position: absolute; inset: 0; pointer-events: none;
  background: linear-gradient(90deg, rgba({{shade}},.82) 0%, rgba({{shade}},.5) 30%, rgba({{shade}},0) 52%),
              linear-gradient(0deg, rgba({{shade}},.35), rgba({{shade}},0) 30%); }
.content { position: absolute; left: 6vw; top: 50%; transform: translateY(-50%); max-width: 44vw; }
.eyebrow { margin: 0 0 14px; font-size: clamp(13px, 1.05vw, 17px); letter-spacing: .5em; color: {{accent2}}; }
h1 { margin: 0; font-weight: 700; font-size: clamp(32px, 5vw, 82px); line-height: 1.15; letter-spacing: .08em; white-space: nowrap;
  text-shadow: 0 2px 18px rgba(0,0,0,.55); }
.line { margin: 18px 0 0; font-size: clamp(15px, 1.35vw, 21px); line-height: 1.7; letter-spacing: .06em; opacity: .92;
  text-shadow: 0 1px 10px rgba(0,0,0,.6); }
.lane { display: flex; gap: 6px; margin: 26px 0 30px; }
.lane i { height: 3px; border-radius: 2px; background: {{accent}}; }
.lane i:nth-child(1) { width: 120px; } .lane i:nth-child(2) { width: 26px; } .lane i:nth-child(3) { width: 26px; opacity: .5; }
nav { display: flex; flex-direction: column; align-items: flex-start; gap: 12px; }
button { font: inherit; font-size: clamp(16px, 1.3vw, 20px); letter-spacing: .3em; min-width: 11em; padding: 12px 26px 12px 22px; text-align: left;
  color: {{ink}}; background: rgba({{shade}},.55); border: 1px solid rgba(255,255,255,.45); border-radius: 2px; cursor: pointer;
  transition: background .2s, border-color .2s, transform .2s; }
button:hover, button:focus-visible { background: {{accent}}; border-color: {{accent2}}; transform: translateX(4px); outline: none; color: #fff; }
button:focus-visible { box-shadow: 0 0 0 2px {{accent2}}; }
button:active { transform: translateX(4px) scale(.97); }
button:disabled { color: rgba(255,255,255,.55); border-color: rgba(255,255,255,.25); background: rgba({{shade}},.4); transform: none; cursor: default; }
button[hidden] { display: none; }
@media (max-width: 720px), (orientation: portrait) {
  .art, .loop { object-position: {{mpos}} 50%; }
  .line { font-size: clamp(12px, 3.6vw, 15px); letter-spacing: 0; white-space: nowrap; }
  .shade { background: linear-gradient(0deg, rgba({{shade}},.92) 0%, rgba({{shade}},.6) 40%, rgba({{shade}},0) 65%); }
  .content { left: 50%; top: auto; bottom: 6vh; transform: translateX(-50%); max-width: 90vw; text-align: center; }
  h1 { font-size: clamp(30px, 9vw, 52px); }
  .lane { justify-content: center; margin: 18px 0 22px; }
  nav { align-items: center; }
  button { min-width: 13em; text-align: center; }
}
@media (prefers-reduced-motion: reduce) {
  .loop { display: none; }
  button, button:hover, button:focus-visible, button:active { transition: none; transform: none; }
}
</style>
<main class="cover">
  <img class="art" data-larch-slot="cover" alt=""{{cover_src}}>
  <img class="loop" data-larch-asset="{{loop}}" alt="" aria-hidden="true"{{loop_src}}>
  <div class="shade"></div>
  <div class="content">
    <p class="eyebrow">{{eyebrow}}</p>
    <h1 data-larch-slot="title">{{title}}</h1>
    <p class="line">{{line}}</p>
    <div class="lane" aria-hidden="true"><i></i><i></i><i></i></div>
    <nav aria-label="遊戲選單">
      <button data-larch-action="start">開始閱讀</button>
      <button data-larch-action="continue">繼續閱讀</button>
      <button data-larch-action="gallery">CG 收藏</button>
    </nav>
  </div>
</main>
<script>
(function () {
  var v = document.querySelector('.loop');
  function shown() { if (v.complete && v.naturalWidth) v.classList.add('is-playing'); }
  v.addEventListener('load', shown);
  shown();
})();
</script>'''


def html(work, loop_id, cover_src='', loop_src='', title=''):
    w = dict(WORKS[work], loop=loop_id, title=title,
             cover_src=f' src="{cover_src}"' if cover_src else '', loop_src=f' src="{loop_src}"' if loop_src else '')
    out = TEMPLATE
    for k, v in w.items(): out = out.replace('{{' + k + '}}', v)
    return out


if __name__ == '__main__' and sys.argv[1:2] == ['preview']:
    d = sys.argv[2]; os.makedirs(d, exist_ok=True)   # 預覽頁放在 repo 外，不進公開站
    srcs = {'start': ('start/cover.webp', 'start/title_loop.avif', '起跑總在開始前'),
            'handoff': ('handoff/COVER_v1.webp', 'handoff/title_loop.avif', '交棒總在終點後')}
    for k, (c, l, t) in srcs.items():
        open(os.path.join(d, k + '.html'), 'w').write('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                                                     '<title>' + t + '</title>' + html(k, 'preview', c, l, t))
    print(d)
