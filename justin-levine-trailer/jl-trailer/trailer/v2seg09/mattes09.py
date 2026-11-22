"""rembg mattes for Nic, OLD cut frames 930-990 (03c_nic in v2 segment 09)"""
import os, cv2
from PIL import Image
from rembg import new_session, remove
S = new_session('u2net_human_seg')
CUT = '/Users/gourav/Downloads/Verticals_Justin_Levine_Trailer_Cut_v1.mp4'
OUT = '/Users/gourav/jl-trailer/trailer/matte/'
c = cv2.VideoCapture(CUT); c.set(cv2.CAP_PROP_POS_FRAMES, 930); n = 930
while n <= 990:
    ok, f = c.read()
    if not ok: break
    p = OUT + f'cut_{n:05d}.png'
    if True:
        m = remove(Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)), session=S, only_mask=True, post_process_mask=False)
        m.save(p); print(n, flush=True)
    n += 1
print('done')
