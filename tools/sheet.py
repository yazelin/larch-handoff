"""把幾張圖排成一列做檢查：python3 tools/sheet.py out.jpg a.webp b.webp ...（每張縮成高 600）"""
import sys
from PIL import Image
out, paths = sys.argv[1], sys.argv[2:]
ims = []
for p in paths:
    im = Image.open(p).convert("RGB"); im.thumbnail((900, 600)); ims.append(im)
W = sum(i.width for i in ims) + 10 * (len(ims) - 1); H = max(i.height for i in ims)
s = Image.new("RGB", (W, H), "white"); x = 0
for i in ims: s.paste(i, (x, 0)); x += i.width + 10
s.save(out, quality=88)
