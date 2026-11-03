# -*- coding: utf-8 -*-
"""標題畫面與專案縮圖用的微動循環 → 動態 AVIF（做法同《仙泉．香布纏．續》xu/讀本/build_loop.py）。
雲帶飄、陽光光暈呼吸、浮塵飄過；人物那一側遮掉不動。所有運動週期恰為 T 秒，最後一格接回第一格，不用淡入接縫。
自架的影片模型只吃文字、不能由靜圖生影片，所以逐像素的動態要靠遮罩與位移自己做。
  python3 tools/title_loop.py handoff   → assets/art/cover/title_loop.avif
  python3 tools/title_loop.py start     → ~/larch-start-line/assets/art/cover/title_loop.avif
  加 --frames 只輸出第 0、1/4、1/2 格的 PNG 檢查用
"""
import os, sys, subprocess, tempfile, shutil
import numpy as np
from PIL import Image

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS, T = 1280, 720, 12, 6
N = FPS * T
# 每部的設定：來源封面、輸出、人物所在的 x 範圍（遮掉不動）、天空帶的高度、太陽位置
PRESETS = {
    'handoff': dict(src=os.path.join(R, 'assets/art/cg/COVER_v1.webp'), out=os.path.join(R, 'assets/art/cover/title_loop.avif'),
                    still_x=.47, sky_y=.20, sky_h=.24, sun=(.15, .10), sun_rgb=(255, 214, 150)),
    'start': dict(src=os.path.expanduser('~/larch-start-line/assets/art/cover/cover.webp'),
                  out=os.path.expanduser('~/larch-start-line/assets/art/cover/title_loop.avif'),
                  still_x=.55, sky_y=.20, sky_h=.26, sun=(.62, .30), sun_rgb=(255, 236, 190)),
}


def build(p):
    src = np.asarray(Image.open(p['src']).convert('RGB').resize((W, H), Image.LANCZOS), np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    keep = np.clip((p['still_x'] - xx / W) / .06, 0, 1)                          # 人物那一側＝0（不動）
    sky = np.clip(1 - np.abs(yy / H - p['sky_y']) / p['sky_h'], 0, 1) ** 1.5 * keep
    sx, sy = p['sun']
    glow = np.exp(-(((xx / W - sx) / .28) ** 2 + ((yy / H - sy) / .30) ** 2))[..., None] * np.array(p['sun_rgb'], np.float32)
    rng = np.random.default_rng(7)
    dust = [(rng.uniform(0, p['still_x']), rng.uniform(.15, .9), rng.uniform(1.2, 2.6), rng.integers(1, 3), rng.uniform(0, 2 * np.pi))
            for _ in range(46)]                                                   # (x, y, 半徑 px, 繞幾圈, 相位)

    def frame(k):
        ph = 2 * np.pi * k / N
        dx = 9 * np.sin(ph)                                                       # 雲帶左右飄（像素）
        sh = np.clip(xx - dx, 0, W - 1)
        x0 = np.floor(sh).astype(np.int32); x1 = np.minimum(x0 + 1, W - 1); f = (sh - x0)[..., None]
        yi = yy.astype(np.int32)
        moved = src[yi, x0] * (1 - f) + src[yi, x1] * f
        img = src * (1 - sky[..., None]) + moved * sky[..., None]
        img = img + glow * (.035 + .025 * np.sin(ph - 1.0))                         # 光暈呼吸
        for (x, y, r, n, a) in dust:                                               # 浮塵：繞小圈、一明一暗
            cx = (x + .012 * np.sin(n * ph + a)) * W; cy = (y + .02 * np.cos(n * ph + a)) * H
            al = (.35 + .35 * np.sin(n * ph + a * 2)) * keep[int(min(cy, H - 1)), int(min(cx, W - 1))]
            x_lo, x_hi, y_lo, y_hi = int(cx - 6), int(cx + 7), int(cy - 6), int(cy + 7)
            if x_lo < 0 or y_lo < 0 or x_hi >= W or y_hi >= H: continue
            d = np.exp(-(((xx[y_lo:y_hi, x_lo:x_hi] - cx) ** 2 + (yy[y_lo:y_hi, x_lo:x_hi] - cy) ** 2) / (r * r)))
            img[y_lo:y_hi, x_lo:x_hi] += (d * al * 110)[..., None] * np.array([1, .95, .8], np.float32)
        return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    return frame


if __name__ == '__main__':
    p = PRESETS[sys.argv[1]]
    frame = build(p)
    if '--frames' in sys.argv:
        for k in (0, N // 4, N // 2): frame(k).save(p['out'].replace('.avif', f'_f{k}.png'))
        sys.exit()
    os.makedirs(os.path.dirname(p['out']), exist_ok=True)
    tmp = tempfile.mkdtemp()
    try:
        for k in range(N): frame(k).save(os.path.join(tmp, 'f%03d.png' % k))
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(tmp, 'f%03d.png'),
                        '-vf', 'format=yuv420p', '-c:v', 'libsvtav1', '-crf', os.environ.get('CRF', '42'), '-preset', '6', '-an', '-f', 'avif', p['out']], check=True)
    finally:
        shutil.rmtree(tmp)
    print(p['out'], round(os.path.getsize(p['out']) / 1024), 'KB')
