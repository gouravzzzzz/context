import cv2, numpy as np, glob, os
for p in sorted(glob.glob('/Users/gourav/jl-trailer/trailer/broll/c_*.mp4')):
    name = os.path.basename(p)[:-4]
    if 'osha' in name or 'shep' in name: continue
    c = cv2.VideoCapture(p); prev = None; keep = 0; i = 0
    while True:
        ok, f = c.read()
        if not ok: break
        g = cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (240, 135)).astype(np.float32)
        if prev is None or np.abs(g - prev).mean() > 1.0: keep += 1
        prev = g; i += 1
    print(f'{name:14s} {i / 30:.2f}s dup {(1 - keep / i) * 100:3.0f}%')
