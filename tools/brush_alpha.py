# -*- coding: utf-8 -*-
"""白紙上的水彩刷痕 → 透明底 PNG（白色轉透明、保留顏料濃淡，暈染邊緣不會被切掉）。
做法：每個像素的不透明度 = 跟白色差多少（取三色最暗的那一個），顏色再除回不透明度（反預乘），疊回白底時跟原圖一樣。
  python3 tools/brush_alpha.py <輸入> <輸出.png>
"""
import sys
import numpy as np
from PIL import Image

src = np.asarray(Image.open(sys.argv[1]).convert('RGB'), np.float32)
a = (255 - src.min(axis=2)) / 255
a = np.clip((a - .03) / .97, 0, 1)                      # 紙的底色帶一點灰，先扣掉
rgb = 255 - (255 - src) / np.maximum(a, 1e-3)[..., None]
out = np.dstack([np.clip(rgb, 0, 255), a * 255]).astype(np.uint8)
ys, xs = np.where(a > .04)
y0, y1, x0, x1 = max(ys.min() - 8, 0), ys.max() + 8, max(xs.min() - 8, 0), xs.max() + 8
img = Image.fromarray(out, 'RGBA').crop((x0, y0, x1, y1))
img.save(sys.argv[2], optimize=True)
assert img.getpixel((img.width // 2, img.height // 2))[3] > 200, '中間應該是不透明的顏料'
print(sys.argv[2], img.size)
