import cv2, numpy as np, math
for name in ('c_osha_226', 'c_osha_230'):
    c = cv2.VideoCapture(f'/Users/gourav/jl-trailer/trailer/broll/{name}.mp4'); prev = None; keep = []; ds = []; i = 0
    while True:
        ok, f = c.read()
        if not ok: break
        g = cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (480, 270), interpolation=cv2.INTER_AREA).astype(np.float32)
        p = 99 if prev is None else float(np.percentile(np.abs(g - prev), 99.5)); ds.append(round(p, 1))
        if p > 6: keep.append(i)
        prev = g; i += 1
    print(name, i, 'unique', len(keep), keep)
    print(' diffs', ds)
    for nout in (34, 36, 44):
        best = None
        for off in range(0, 12):
            seq = []
            for n in range(nout):
                e = n / 24 * 30 + off; ks = [u for u in keep if u <= e + 1e-6]; seq.append(ks[-1] if ks else keep[0])
            if seq[-1] == keep[-1] and n / 24 * 30 + off > keep[-1] + 2: pass
            run = 1; mx = 1
            for a, b in zip(seq, seq[1:]):
                run = run + 1 if a == b else 1; mx = max(mx, run)
            over = (nout - 1) / 24 * 30 + off > i - 1
            if best is None or (mx, over) < best[:2]: best = (mx, over, off)
        print('  nout', nout, 'best maxhold', best[0], 'runs past end', best[1], 'offset', best[2])
