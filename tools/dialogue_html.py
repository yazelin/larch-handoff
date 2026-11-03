# -*- coding: utf-8 -*-
"""自訂對話框（Larch customInterfaces.dialogue），不擋 CG：
  下篇 handoff：右下角一張半透明的小信紙卡（整部是一封信）。
  上篇 start：貼底的窄字幕帶，只在字後面壓一點淡漸層。
兩種都有「只看圖」鈕：按下收成一個小標籤，再按一次回來（播放器的存讀檔工具列不歸這裡管）。
介面契約見 ~/.claude/skills/larch-vn/interface-skills.md：框照內容長高、從底部往上長，所以只把框做窄，不撐高。
"""

COMMON_JS = '''<script>
(function () {
  var root = document.querySelector('.dlg'), hide = document.querySelector('.hide'), show = document.querySelector('.show');
  function set(h) { root.classList.toggle('is-hidden', h); show.hidden = !h; }
  hide.addEventListener('click', function (e) { e.stopPropagation(); set(true); });
  show.addEventListener('click', function (e) { e.stopPropagation(); set(false); });
  window.addEventListener('larch:state', function () { set(false); });   // 換句就回來，免得玩家以為卡住
})();
</script>'''

EYE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5C6.5 5 2.7 9.4 1.5 12c1.2 2.6 5 7 10.5 7s9.3-4.4 10.5-7C21.3 9.4 17.5 5 12 5zm0 11.5a4.5 4.5 0 1 1 0-9 4.5 4.5 0 0 1 0 9z"/></svg>'

HANDOFF = '''<style>
@import url("https://fonts.googleapis.com/css2?family=LXGW+WenKai+TC:wght@400;700&display=swap");
html { --larch-project-font: "LXGW WenKai TC", "Noto Serif TC", serif !important; }
* { box-sizing: border-box; }
body { margin: 0; background: transparent; }
.dlg { display: flex; justify-content: flex-end; padding: 0 3vw 2vh; }
.card { position: relative; width: min(40vw, 640px); padding: 18px 22px 14px 24px; color: #3a2e28;
  background: rgba(251,246,236,.86); border-radius: 3px; box-shadow: 0 10px 30px -12px rgba(30,20,10,.55), 0 0 0 1px rgba(120,95,70,.18);
  transition: opacity .35s, transform .35s; }
.card::before { content: ""; position: absolute; top: -9px; left: 24px; width: 64px; height: 18px; background: rgba(232,160,74,.55); rotate: -3deg; }
.name { margin: 0 0 4px; font-size: .82em; letter-spacing: .2em; color: #a0622a; }
.name:empty { display: none; }
.text { margin: 0; font-size: var(--larch-text-size, 22px); line-height: 1.9; letter-spacing: .03em; min-height: 1.9em; }
.bar { display: flex; justify-content: flex-end; gap: 8px; margin-top: 6px; }
button { font: inherit; border: 0; cursor: pointer; display: inline-grid; place-items: center; width: 34px; height: 34px; border-radius: 50%;
  color: #6b4a33; background: rgba(160,98,42,.12); transition: background .2s, transform .2s; }
button svg { width: 18px; height: 18px; fill: currentColor; }
button:hover, button:focus-visible { background: rgba(160,98,42,.28); outline: none; }
button:focus-visible { box-shadow: 0 0 0 2px #a0622a; }
button:active { transform: scale(.92); }
.show { position: absolute; right: 3vw; bottom: 2vh; width: auto; padding: 0 14px; border-radius: 99px; font-size: 14px; letter-spacing: .1em;
  background: rgba(251,246,236,.8); box-shadow: 0 4px 14px -6px rgba(0,0,0,.4); }
.show[hidden] { display: none; }
.is-hidden .card { opacity: 0; transform: translateY(12px); pointer-events: none; }
@media (max-width: 720px), (orientation: portrait) {
  .dlg { padding: 0 3vw 1.5vh; }
  .card { width: 100%; padding: 14px 16px 10px 18px; }
  .text { font-size: min(var(--larch-text-size, 22px), 17px); }
}
@media (prefers-reduced-motion: reduce) { .card, button { transition: none; } }
</style>
<div class="dlg">
  <div class="card">
    <p class="name" data-larch-slot="speaker"></p>
    <p class="text" data-larch-slot="text"></p>
    <div class="bar">
      <button class="hide" aria-label="只看圖" title="只看圖">''' + EYE + '''</button>
      <button data-larch-action="advance" aria-label="下一句" title="下一句"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8.6 5.4 15.2 12l-6.6 6.6-1.4-1.4L12.4 12 7.2 6.8z"/></svg></button>
    </div>
  </div>
  <button class="show" hidden aria-label="顯示文字">顯示文字</button>
</div>
''' + COMMON_JS

START = '''<style>
* { box-sizing: border-box; }
body { margin: 0; background: transparent; }
.dlg { position: relative; padding: 4.5em 6vw 2.2vh;
  background: linear-gradient(0deg, rgba(6,10,22,.62) 0%, rgba(6,10,22,.34) 55%, rgba(6,10,22,0) 100%); transition: opacity .35s;
  -webkit-mask-image: linear-gradient(90deg, transparent 0, #000 12%, #000 88%, transparent 100%);
          mask-image: linear-gradient(90deg, transparent 0, #000 12%, #000 88%, transparent 100%); }
.row { display: flex; align-items: flex-end; gap: 14px; max-width: 1200px; margin: 0 auto; }
.body { flex: 1; min-width: 0; color: #f4f6fb; text-shadow: 0 1px 3px rgba(0,0,0,.85), 0 0 14px rgba(0,0,0,.45); }
.name { margin: 0 0 2px; font-size: .8em; letter-spacing: .22em; color: #ff9a82; }
.name:empty { display: none; }
.text { margin: 0; font-size: var(--larch-text-size, 22px); line-height: 1.65; letter-spacing: .03em; min-height: 1.65em; }
button { font: inherit; border: 0; cursor: pointer; display: inline-grid; place-items: center; width: 34px; height: 34px; border-radius: 50%;
  color: #f4f6fb; background: rgba(255,255,255,.14); transition: background .2s, transform .2s; flex: none; }
button svg { width: 18px; height: 18px; fill: currentColor; }
button:hover, button:focus-visible { background: #e0432a; outline: none; }
button:focus-visible { box-shadow: 0 0 0 2px #ff7a5e; }
button:active { transform: scale(.92); }
.show { position: absolute; right: 6vw; bottom: 2.2vh; width: auto; padding: 0 14px; border-radius: 99px; font-size: 14px; letter-spacing: .1em;
  background: rgba(6,10,22,.6); }
.show[hidden] { display: none; }
.is-hidden { background: none; }
.is-hidden .row { opacity: 0; pointer-events: none; }
@media (max-width: 720px), (orientation: portrait) {
  .dlg { padding: 3.5em 4vw 1.5vh; }
  .text { font-size: min(var(--larch-text-size, 22px), 17px); }
}
@media (prefers-reduced-motion: reduce) { .dlg, button { transition: none; } }
</style>
<div class="dlg">
  <div class="row">
    <div class="body">
      <p class="name" data-larch-slot="speaker"></p>
      <p class="text" data-larch-slot="text"></p>
    </div>
    <button class="hide" aria-label="只看圖" title="只看圖">''' + EYE + '''</button>
    <button data-larch-action="advance" aria-label="下一句" title="下一句"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8.6 5.4 15.2 12l-6.6 6.6-1.4-1.4L12.4 12 7.2 6.8z"/></svg></button>
  </div>
  <button class="show" hidden aria-label="顯示文字">顯示文字</button>
</div>
''' + COMMON_JS

PAGES = {'handoff': HANDOFF, 'start': START}
