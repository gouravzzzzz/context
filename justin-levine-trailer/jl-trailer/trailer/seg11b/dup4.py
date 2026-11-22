import cv2, numpy as np, glob, os
from PIL import Image, ImageDraw
tiles = []
for p in sorted(glob.glob('/Users/gourav/jl-trailer/trailer/broll/c_*.mp4')):
    name = os.path.basename(p)[:-4]
    if name.startswith('c_shep'): continue
    c = cv2.VideoCapture(p); prev = None; keep = 0; i = 0; mid = None
    while True:
        ok, f = c.read()
        if not ok: break
        g = cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (480, 270), interpolation=cv2.INTER_AREA).astype(np.float32)
        if prev is None or np.percentile(np.abs(g - prev), 99.5) > 6: keep += 1
        prev = g; i += 1
        if i == 20: mid = f
    print(f'{name:14s} {i:3d}f {i / 30:.2f}s unique {keep:3d} dup {(1 - keep / i) * 100:3.0f}%')
    im = Image.fromarray(cv2.cvtColor(cv2.resize(mid, (320, 180)), cv2.COLOR_BGR2RGB)); ImageDraw.Draw(im).text((6, 6), name, fill=(255, 0, 0)); tiles.append(im)
s = Image.new('RGB', (320 * 6, 180 * ((len(tiles) + 5) // 6)))
for k, im in enumerate(tiles): s.paste(im, ((k % 6) * 320, (k // 6) * 180))
s.save('allbroll.jpg', quality=80)
