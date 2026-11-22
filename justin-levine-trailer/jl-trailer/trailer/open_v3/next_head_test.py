"""TEST ONLY (does not touch v2segs/01_name3d_fx.mp4): stills of the next segment's first frames (NEW 206+) with the v3
opening captions installed into its own v1 instance, to show the 205 -> 206 caption continuity fix to its owner.
  python next_head_test.py 206 209 212"""
import sys, os
sys.path.insert(0, '/Users/gourav/jl-trailer/trailer'); sys.path.insert(0, '/Users/gourav/jl-trailer/trailer/open_v3')
import render_v2 as RV
import scene
from PIL import Image
m = RV.src('s1014')
scene.install(m.V.v1())
os.makedirs(scene.HERE + 'stills', exist_ok=True)
for a in sys.argv[1:]:
    Image.fromarray(RV.frame('s1014', int(a))).save(scene.HERE + f'stills/next_{int(a):03d}.jpg', quality=90); print(a, flush=True)
