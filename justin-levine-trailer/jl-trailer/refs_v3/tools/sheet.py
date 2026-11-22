import sys
from PIL import Image, ImageDraw
d, a, b, step, cols, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
W = int(sys.argv[7]) if len(sys.argv) > 7 else 320
ids = list(range(a, b + 1, step))
im0 = Image.open(f'{d}/{a+1:04d}.jpg'); h = int(im0.height * W / im0.width)
rows = (len(ids) + cols - 1) // cols
S = Image.new('RGB', (cols * W, rows * h), 'black'); dr = ImageDraw.Draw(S)
for k, i in enumerate(ids):
    im = Image.open(f'{d}/{i+1:04d}.jpg').resize((W, h))
    x, y = (k % cols) * W, (k // cols) * h
    S.paste(im, (x, y)); dr.rectangle([x, y, x + 34, y + 14], fill='black'); dr.text((x + 2, y + 1), str(i), fill='yellow')
S.save(out, quality=88)
