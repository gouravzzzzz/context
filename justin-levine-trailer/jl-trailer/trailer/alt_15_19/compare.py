import sys; sys.path.insert(0, '/Users/gourav/jl-trailer/trailer/alt_15_19')
from PIL import Image, ImageDraw, ImageFont
import scene
R = '/Users/gourav/jl-trailer/refs/pin_15_19/'
fnt = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 22)
rows = []
for t, lab, rt in scene.STILLS:
    ref = Image.open(R + f'f_{int(round(rt * 30)) + 1:04d}.jpg').resize((203, 360))
    me = Image.open(scene.A + f'stills/s_{t:05.2f}.png').resize((640, 360))
    row = Image.new('RGB', (203 + 640 + 12, 400), (24, 24, 26)); row.paste(ref, (0, 40)); row.paste(me, (215, 40))
    d = ImageDraw.Draw(row); d.text((6, 8), f'ref {rt:.2f}s', fill=(255, 120, 120), font=fnt); d.text((221, 8), f'{t:.2f}s  {lab}', fill=(230, 230, 230), font=fnt)
    rows.append(row)
cw, ch = rows[0].size; sheet = Image.new('RGB', (cw * 2 + 10, ch * 5), (12, 12, 14))
for i, r in enumerate(rows): sheet.paste(r, ((i // 5) * (cw + 10), (i % 5) * ch))
sheet.save(scene.A + 'stills/compare.jpg', quality=88); print(sheet.size)
