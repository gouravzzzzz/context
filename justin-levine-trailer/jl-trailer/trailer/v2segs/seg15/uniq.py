import cv2, numpy as np, json
out = {}
for name in ['c_lloyds_97', 'c_intact_142', 'c_intact_139', 'c_bctt_15', 'c_osha_166', 'c_osha_56', 'c_prog99_60', 'c_osha_14', 'c_lumi_14','c_shep_20']:
    c = cv2.VideoCapture(f'/Users/gourav/jl-trailer/trailer/broll/{name}.mp4'); prev = None; keep = []; i = 0; fps=c.get(cv2.CAP_PROP_FPS)
    while True:
        ok, f = c.read()
        if not ok: break
        g = cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (480, 270)).astype(np.float32)
        d = 999 if prev is None else float(np.abs(g - prev).mean())
        if d > 0.35: keep.append(i)
        prev = g; i += 1
    out[name] = dict(n=i, fps=fps, keep=keep)
    print(name, fps, i, 'unique', len(keep), 'dur', round(i/fps,2), 'rate', round(len(keep)/(i/fps),1))
json.dump(out, open('unique.json', 'w'))
