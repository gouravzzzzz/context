import cv2, numpy as np, sys, subprocess
p = sys.argv[1]; N0 = int(sys.argv[2]) if len(sys.argv) > 2 else 1689
c = cv2.VideoCapture(p); prev = None; d = []; n = 0
while True:
    ok, f = c.read()
    if not ok: break
    g = cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (480, 270)).astype(np.float32)
    if prev is not None: d.append(float(np.abs(g - prev).mean()))
    prev = g; n += 1
print('frames', n)
print('stuck (diff<0.25):', [N0 + i + 1 for i, v in enumerate(d) if v < 0.25])
med = np.median(d)
sp = [(N0 + i + 1, round(v, 1)) for i, v in enumerate(d) if v > 2.5 * max(np.median(d[max(0, i - 3):i + 4]), 1e-3) and v > 6]
print('median diff', round(med, 2), 'spikes vs local median:', sp)
print(' '.join(f'{N0 + i + 1}:{v:.1f}' for i, v in enumerate(d)))
