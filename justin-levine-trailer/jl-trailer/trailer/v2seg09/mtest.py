import cv2, numpy as np
from PIL import Image
from rembg import new_session, remove
CUT = '/Users/gourav/Downloads/Verticals_Justin_Levine_Trailer_Cut_v1.mp4'
c = cv2.VideoCapture(CUT); c.set(cv2.CAP_PROP_POS_FRAMES, 971); ok, f = c.read()
im = Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))
outs = [im.resize((480, 270))]
for name in ['u2net_human_seg', 'u2net']:
    S = new_session(name)
    m = remove(im, session=S, only_mask=True, post_process_mask=False)
    outs.append(m.convert('RGB').resize((480, 270)))
Sh = Image.new('RGB', (1440, 270))
for i, o in enumerate(outs): Sh.paste(o, (480 * i, 0))
Sh.save('mtest.jpg')
