import sys, os, importlib.util
sys.path.insert(0, '/Users/gourav/jl-trailer/trailer')
import numpy as np
from PIL import Image
import engine
engine.PATCH_MAP.clear()
sp = importlib.util.spec_from_file_location('jl_render', '/Users/gourav/jl-trailer/trailer/render.py')
R = importlib.util.module_from_spec(sp); sp.loader.exec_module(R)
from newtime import n_old
for s in R.SHOTS:
    if s.tin == 'zt': s.tin = 'cut'
    if getattr(s, 'tout', None) == 'zt': s.tout = 'cut'
for n in map(int, sys.argv[1:]):
    no = n_old(n)
    Image.fromarray(R.frame(no)).save(f'v1_{n}.jpg', quality=88); print(n, no, flush=True)
