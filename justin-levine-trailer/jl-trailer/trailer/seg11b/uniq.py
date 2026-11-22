"""unique-frame lists (real duplicates = only compression noise vs the previous frame) for every source sequence used"""
import cv2, numpy as np, json
BR = '/Users/gourav/jl-trailer/trailer/broll/'
SEQS = {  # name: ([(clip, f0, f1)], crop x0,y0,x1,y1 or None)
    'hs':   ([('c_osha_11', 91, 107), ('c_osha_14', 8, 10)], None),   # after the source's fade-in, before its title dim
    'chk':  ([('c_osha_166', 0, 45)], None),
    'i226': ([('c_osha_226', 0, 54)], None),                     # Krish's tank-site inspection shot (grey fleece + tablet)
    'i230': ([('c_osha_230', 1, 42)], None),
    'lumi14': ([('c_lumi_14', 0, 47)], None),
    'intel': ([('c_intel_66', 0, 40)], None),
    'lumi5': ([('c_lumi_5', 13, 55)], None),                    # after its frozen head
    'exc':  ([('c_osha_11', 20, 76)], (0, 0, 760, 428)),
    'wh':   ([('c_osha_96', 0, 84)], None),
    'tank': ([('c_osha_11', 9, 76)], (962, 700, 1632, 1077)),
    'harn': ([('c_osha_11', 19, 76)], (1130, 0, 1830, 394)),
}
cache = {}
def frames(clip):
    if clip not in cache:
        c = cv2.VideoCapture(BR + clip + '.mp4'); fs = []
        while True:
            ok, f = c.read()
            if not ok: break
            fs.append(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY))
        cache[clip] = fs
    return cache[clip]
out = {}
for name, (parts, crop) in SEQS.items():
    seq = [(c, i) for c, a, b in parts for i in range(a, b + 1)]
    prev = None; keep = []; ds = []
    for k, (c, i) in enumerate(seq):
        g = frames(c)[i].astype(np.float32)
        if crop: g = g[crop[1]:crop[3], crop[0]:crop[2]]
        g = cv2.resize(g, (480, int(480 * g.shape[0] / g.shape[1])), interpolation=cv2.INTER_AREA)
        if prev is None: keep.append(k); prev = g; ds.append(99); continue
        d = np.abs(g - prev); p = float(np.percentile(d, 99.5))
        ds.append(round(p, 1))
        if p > 6.0: keep.append(k)
        prev = g
    out[name] = dict(seq=seq, crop=crop, uniq=keep)
    print(name, len(seq), 'unique', len(keep), 'p99.5 diffs:', ds)
json.dump(out, open('sources.json', 'w'))
