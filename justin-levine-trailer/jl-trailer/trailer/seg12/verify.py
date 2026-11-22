import cv2, numpy as np, sys
c = cv2.VideoCapture(sys.argv[1]); prev = None; i = 0; ds = []
while True:
    ok, f = c.read()
    if not ok: break
    g = cv2.resize(f, (480, 270)).astype(np.float32)
    if prev is not None: ds.append(float(np.abs(g - prev).mean()))
    prev = g; i += 1
print('frames', i)
for k, d in enumerate(ds): print(k + 1, '%5.2f' % d, '#' * int(d * 4))
print('stuck (<0.3):', [k + 1 for k, d in enumerate(ds) if d < 0.3])
