import cv2, numpy as np, json, sys
out = {}
for name in ['s_osha_hs', 'c_osha_192', 'c_osha_96']:
    c = cv2.VideoCapture(f'/Users/gourav/jl-trailer/trailer/broll/{name}.mp4'); prev = None; ds = []; keep = []; i = 0
    while True:
        ok, f = c.read()
        if not ok: break
        g = cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (480, 270)).astype(np.float32)
        d = 999 if prev is None else float(np.abs(g - prev).mean())
        ds.append(round(d, 2))
        if d > 0.35: keep.append(i)
        prev = g; i += 1
    out[name] = keep
    print(name, i, len(keep), ds[:40])
    print(keep)
json.dump(out, open('unique.json', 'w'))
