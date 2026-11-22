"""rembg isnet mattes for c_shep_20 frames 0-40 (Justin wide) -> alt_10_14/matte/s20_<n>.png"""
import os, cv2
from PIL import Image
from rembg import new_session, remove
S = new_session('isnet-general-use'); OUT = '/Users/gourav/jl-trailer/trailer/alt_10_14/matte/'
c = cv2.VideoCapture('/Users/gourav/jl-trailer/trailer/broll/c_shep_20.mp4')
for n in range(41):
    ok, f = c.read()
    if not ok: break
    p = OUT + f's20_{n:05d}.png'
    if not os.path.exists(p):
        remove(Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)), session=S, only_mask=True, post_process_mask=False).save(p); print(n, flush=True)
print('done')
