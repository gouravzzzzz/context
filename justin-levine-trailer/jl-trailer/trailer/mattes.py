"""per-frame person mattes (rembg isnet-general-use) for the text-behind / cut-out shots.
cut frames (24 fps, the A-roll cut) -> matte/cut_<n>.png ; Shepherd film c_shep_1 (30 fps) -> matte/shep_<n>.png"""
import os, sys, cv2, numpy as np
from PIL import Image
from rembg import new_session, remove
S = new_session('isnet-general-use')
CUT = '/Users/gourav/Downloads/Verticals_Justin_Levine_Trailer_Cut_v1.mp4'
OUT = '/Users/gourav/jl-trailer/trailer/matte/'
RANGES = [(79, 168), (338, 378), (750, 831), (997, 1093), (1816, 1855)]
def run(path, frames, prefix):
    c = cv2.VideoCapture(path); want = set(frames); n = 0; last = max(frames)
    while n <= last:
        ok, f = c.read()
        if not ok: break
        if n in want and not os.path.exists(OUT + f'{prefix}_{n:05d}.png'):
            m = remove(Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)), session=S, only_mask=True, post_process_mask=False)
            m.save(OUT + f'{prefix}_{n:05d}.png'); print(prefix, n, flush=True)
        n += 1
run('/Users/gourav/jl-trailer/trailer/broll/c_shep_1.mp4', list(range(0, 78)), 'shep')
run(CUT, [n for a, b in RANGES for n in range(a, b + 1)], 'cut')
print('done')
