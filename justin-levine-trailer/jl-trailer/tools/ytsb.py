"""fetch YouTube storyboard sprites and build a labelled contact sheet: ytsb.py id 'spec' out.jpg"""
import sys, io, urllib.request, math
from PIL import Image, ImageDraw
vid, spec, out = sys.argv[1], sys.argv[2], sys.argv[3]
parts = spec.split('|'); base = parts[0]; levels = parts[1:]
L = len(levels) - 1
while L > 0 and int(levels[L].split('#')[0]) > 170: L -= 1      # biggest level with tiles <= 170 px
w, h, cnt, cols, rows, iv, name, sigh = levels[L].split('#')
w, h, cnt, cols, rows, iv = int(w), int(h), int(cnt), int(cols), int(rows), int(iv)
per = cols * rows; nsheets = math.ceil(cnt / per)
tiles = []
for s in range(nsheets):
    u = base.replace('$L', str(L)).replace('$N', name.replace('$M', str(s))) + '&sigh=' + sigh
    im = Image.open(io.BytesIO(urllib.request.urlopen(u).read())).convert('RGB')
    for k in range(per):
        if len(tiles) >= cnt: break
        x, y = (k % cols) * w, (k // cols) * h
        if y + h > im.height: break
        tiles.append(im.crop((x, y, x + w, y + h)))
C = 10; tw, th = 192, round(192 * h / w)
S = Image.new('RGB', (C * tw, math.ceil(len(tiles) / C) * (th + 14)), (30, 30, 30)); d = ImageDraw.Draw(S)
for i, t in enumerate(tiles):
    x, y = (i % C) * tw, (i // C) * (th + 14)
    S.paste(t.resize((tw, th)), (x, y + 14))
    sec = i * iv / 1000 if iv else i
    d.text((x + 3, y + 1), f'{int(sec)//60}:{sec%60:04.1f}', fill=(255, 220, 0))
S.save(out, quality=82); print(out, len(tiles), 'tiles, interval', iv)
