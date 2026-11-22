"""v6b: person mattes for Luke's full-screen 'Breaking news' frames (split_luke.mp4 frames 380-470) -> matte/luke_<n>.png
(rembg isnet-general-use, same as mattes.py) so the BREAKING NEWS box can sit BEHIND him (Krish)."""
import os, cv2
from PIL import Image
from rembg import new_session, remove
S = new_session('isnet-general-use')
OUT = '/Users/gourav/jl-trailer/trailer/matte/'
c = cv2.VideoCapture('/Users/gourav/jl-trailer/trailer/broll/split_luke.mp4'); n = 0
while n <= 470:
    ok, f = c.read()
    if not ok: break
    if n >= 380 and not os.path.exists(OUT + f'luke_{n:05d}.png'):
        m = remove(Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)), session=S, only_mask=True, post_process_mask=False)
        m.save(OUT + f'luke_{n:05d}.png'); print('luke', n, flush=True)
    n += 1
print('done')
