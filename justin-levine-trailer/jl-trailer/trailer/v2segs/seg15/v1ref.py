import sys, os; sys.path.insert(0, '/Users/gourav/jl-trailer/trailer')
import numpy as np, engine, importlib.util
engine.PATCH_MAP.clear()
sp = importlib.util.spec_from_file_location('jl_render', '/Users/gourav/jl-trailer/trailer/render.py')
R = importlib.util.module_from_spec(sp); sp.loader.exec_module(R)
from newtime import n_old
from PIL import Image
for s in R.SHOTS:
    if s.tin == 'zt': s.tin = 'cut'
    if s.tout == 'zt': s.tout = 'cut'
os.makedirs('v1', exist_ok=True)
for n in map(int, sys.argv[1:]):
    no = n_old(n); f = R.frame(no); Image.fromarray(f).save(f'v1/v1_{n}.jpg', quality=88); print(n, no, flush=True)
