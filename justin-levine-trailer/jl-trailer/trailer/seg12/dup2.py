import cv2, numpy as np, glob, os, json
res = {}
for p in sorted(glob.glob('/Users/gourav/jl-trailer/trailer/broll/*osha*.mp4')):
    name = os.path.basename(p)[:-4]
    c = cv2.VideoCapture(p); prev = None; keep = []; i = 0
    while True:
        ok, f = c.read()
        if not ok: break
        g = cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (480, 270)).astype(np.float32)
        if prev is None or np.abs(g - prev).mean() > 1.5: keep.append(i)
        prev = g; i += 1
    # real-time mapping over 2.05 s: max hold in output frames
    holds = []; last = None; run = 0
    for n in range(49):
        u = n / 24 * 30; k = max(j for j in keep if j <= u + 1e-6) if keep[0] <= u else keep[0]
        if k == last: run += 1
        else: holds.append(run); run = 1
        last = k
    holds.append(run)
    res[name] = keep
    print(f'{name:12s} frames {i:3d} unique {len(keep):3d} dup {(1 - len(keep) / i) * 100:4.0f}%  dur {i / 30:.2f}s  max hold (2.05 s) {max(holds)}')
json.dump(res, open('unique_osha.json', 'w'))
