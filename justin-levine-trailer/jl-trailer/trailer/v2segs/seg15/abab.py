import cv2, numpy as np, sys
c = cv2.VideoCapture(sys.argv[1]); N0 = int(sys.argv[2]); F = []
while True:
    ok, f = c.read()
    if not ok: break
    F.append(cv2.resize(f, (384, 216), interpolation=cv2.INTER_AREA).astype(np.float32))
print('frames', len(F))
GX, GY = 12, 6; tw, th = 384 // GX, 216 // GY
def td(a, b): return np.abs(a - b).reshape(GY, th, GX, tw, 3).mean(axis=(1, 3, 4))
flags = []
for i in range(1, len(F) - 1):
    d1, d2, d02 = td(F[i - 1], F[i]), td(F[i], F[i + 1]), td(F[i - 1], F[i + 1])
    m = (d1 > 12) & (d2 > 12) & (d02 < 0.45 * np.minimum(d1, d2))
    if m.any(): flags.append((N0 + i, int(m.sum()), round(float(np.max(np.minimum(d1, d2)[m])), 1)))
print('A-B-A-B tiles flagged (frame, tiles, diff):', flags)
