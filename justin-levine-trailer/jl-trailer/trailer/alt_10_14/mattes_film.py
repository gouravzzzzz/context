"""rembg isnet mattes for the Shepherd film frames Justin uses (native 23.98 fps) -> matte_film/f<n>.png"""
import os
from PIL import Image
from rembg import new_session, remove
S = new_session('isnet-general-use'); D = '/Users/gourav/jl-trailer/trailer/alt_10_14/'
for n in list(range(10, 90)) + list(range(440, 502)):
    p = D + f'matte_film/f{n:05d}.png'
    if not os.path.exists(p): remove(Image.open(D + f'film/f{n:05d}.jpg').convert('RGB'), session=S, only_mask=True, post_process_mask=False).save(p)
print('done')
