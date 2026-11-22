import sys, glob
from PIL import Image, ImageDraw
fs = []
for pat in sys.argv[2:]: fs += sorted(glob.glob('stills/' + pat))
S = Image.new('RGB', (3 * 640, ((len(fs) + 2) // 3) * 374), (30, 30, 30)); d = ImageDraw.Draw(S)
for k, f in enumerate(fs):
    x, y = (k % 3) * 640, (k // 3) * 374
    S.paste(Image.open(f).resize((640, 360)), (x, y + 14)); d.text((x + 4, y + 1), f.split('/')[-1], fill=(255, 220, 0))
S.save(sys.argv[1], quality=85)
