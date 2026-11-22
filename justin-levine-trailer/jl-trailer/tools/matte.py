"""person mattes with rembg (isnet-general-use): matte.py out_dir img1 img2 ... -> <name>_a.png (8-bit alpha)"""
import sys, os, numpy as np
from PIL import Image
from rembg import new_session, remove
out = sys.argv[1]; S = new_session('isnet-general-use')
for p in sys.argv[2:]:
    im = Image.open(p).convert('RGB')
    m = remove(im, session=S, only_mask=True, post_process_mask=True)
    m.save(os.path.join(out, os.path.basename(p).rsplit('.', 1)[0] + '_a.png')); print('ok', p, flush=True)
