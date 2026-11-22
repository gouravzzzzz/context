"""contact sheet: sheet.py framedir fps start_frame end_frame step cols tilew out.jpg  (frames are 1-based files)"""
import sys, os
from PIL import Image, ImageDraw, ImageFont
d, fps, a, b, step, cols, tw, out = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), sys.argv[8]
idx = list(range(a, b + 1, step))
im0 = Image.open(os.path.join(d, '%05d.jpg' % idx[0])); th = round(tw * im0.height / im0.width)
rows = (len(idx) + cols - 1) // cols
S = Image.new('RGB', (cols * tw, rows * (th + 16)), (40, 40, 40)); dr = ImageDraw.Draw(S)
try: font = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 12)
except Exception: font = None
for k, i in enumerate(idx):
    p = os.path.join(d, '%05d.jpg' % i)
    if not os.path.exists(p): continue
    x, y = (k % cols) * tw, (k // cols) * (th + 16)
    S.paste(Image.open(p).resize((tw, th)), (x, y + 16))
    dr.text((x + 3, y + 1), f'f{i-1} {(i-1)/fps:.2f}s', fill=(255, 220, 0), font=font)
S.save(out, quality=85)
