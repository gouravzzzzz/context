"""10-14 s scene v5 = v2 (Krish's smooth 3D camera: overlapped creep + 2.5 s eased truck, Nic whips left, Justin rises in)
with the photo card done the way Krish asked (2026-11-22):
  - the card sits behind Justin on his right (screen left) and ends HALFWAY THROUGH HIM (right edge on his centre line)
  - it is revealed by a FEATHERED WIPE travelling RIGHT -> LEFT, out from behind him (Krish's graph, ~0.4 s, ref f101-f111)
  - a still photo like the ref's card; no whip-out -- it leaves with its caption on the truck (ref f140-f150)
  python scene_v5.py stills t ... | python scene_v5.py render out.mp4"""
import sys, os, subprocess
import numpy as np, cv2
from PIL import Image
sys.path.insert(0, '/Users/gourav/jl-trailer/trailer/alt_10_14/')
import scene3d_v2 as V
S3 = V.S3
from engine import *
HERE = '/Users/gourav/jl-trailer/trailer/alt_10_14/'
FF = '/Users/gourav/ks-ron-build/reel1/ff'

CARD_X0, CARD_Y0, CARD_H = 92, 84, 896
CARD_W = int(round(CX - CARD_X0))                  # right edge on Justin's centre line (face centred at CX)
FEATHER = 110.0                                    # soft wipe edge (ref ~60-75 px at 720p-equivalent -> ours)
# the ref's wipe, measured frame by frame (f101..f112, edge travel in ref px): accelerates to f107-f108, then settles
from scipy.interpolate import PchipInterpolator
_WP = np.float32([0, 8, 20, 40, 60, 90, 130, 185, 215, 245, 260, 262]) / 262.0
_WI = PchipInterpolator(np.arange(len(_WP)), _WP)
CARD_T = V.RISE0 + 0.05                            # 1.5 ref frames after Justin starts rising (ref f99.5 -> f101)
WIPE_D = (len(_WP) - 1) / 30.0                     # 0.367 s, the ref's duration


def sc_init(s):
    s.cx0, s.cy0, s.cw, s.ch = CARD_X0, CARD_Y0, CARD_W, CARD_H
    S3.Layer.__init__(s, 'card', 2050.0, (32, 24, CARD_X0 + CARD_W + 60, CARD_Y0 + CARD_H + 70), S3.P_REF0)
S3.SignCard.__init__ = sc_init


def wipe_e(t):
    u = (t - CARD_T) / WIPE_D
    return 0.0 if u <= 0 else (1.0 if u >= 1 else float(np.clip(_WI(u * (len(_WP) - 1)), 0, 1)))
V.CARD_T = CARD_T
V.wipe_e = wipe_e
V.CARD_OUT = 1e9                                   # no whip-out (the v2 card exit is gone)
S3.LAYER_MOVES['card'] = [S3.M3(S3.TR0, S3.TR_DUR, X=-720)]   # card leaves with the caption on the truck, like the ref

_IMG = None
def card_img():
    global _IMG
    if _IMG is None: _IMG = L.grade(V.film(540))   # the clearest frame of Shepherd's sign shot, held like the ref's photo
    return _IMG


def sign_tex(s, t):
    ox, oy = s.cx0 - s.rect[0], s.cy0 - s.rect[1]
    def fn(d): L.card(d, card_img(), ox, oy, s.cw, s.ch, fx=0.20, fy=0.50, zoom=1.0, shadow=True)
    M, C = S3.mc_draw(s.tw, s.th, fn)
    return wipe_mask(M, C, s.rect[0], s.ss, t)


def wipe_mask(M, C, rx0, ss, t):
    """right-anchored feathered wipe in layout-screen x: the soft edge travels right -> left, out from behind Justin"""
    e = wipe_e(t)
    if e >= 0.999: return M, C
    right = CARD_X0 + CARD_W + 60 + FEATHER; span = CARD_W + 60 + 2 * FEATHER + 70
    edge = right - span * e
    v = span * (wipe_e(t + 0.5 / FPS) - wipe_e(t - 0.5 / FPS))
    ramp = max(FEATHER, v * 1.2)
    xs = rx0 + np.arange(M.shape[1], dtype=np.float32) / ss
    u = np.clip((xs - edge) / ramp + 0.5, 0, 1)
    m = (u * u * (3 - 2 * u))[None, :, None]
    return 1 - m * (1 - M), C * m
S3.SignCard.key = lambda s, t: round(wipe_e(t), 3)
S3.SignCard.tex = sign_tex

# ---------------------------------------------------------------- Krish: black boxes behind 'Justin' / 'Levine', block moved up to the middle
BOX_OP, PADX, PADY, GAP = 0.86, 28, 18, 12
MID_Y = CY                                           # the two-line block is centred on the frame's middle


def _ink(draw):
    P = np.zeros((H, W, 3), np.float32); draw(P)
    ys, xs = np.where(P.max(2) > 60)
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def cap_init(s):
    s.tj, s.tl = S3.WORDS_['Justin'] - LEAD, S3.WORDS_['Levine.'] - LEAD
    wl = L.text_rgba('Levine', s.PXL, 'reg', (255, 255, 255), 1.0)[0].shape[1]
    s.x = min(150, 800 - wl)
    j = _ink(lambda d: L.put_text(d, 'Justin', s.PXJ, s.x + 8, 1000, glow=0.0))          # ink relative to a test baseline
    l = _ink(lambda d: L.grad_text(d, 'Levine', s.PXL, s.x, 1000, glow=0.0))
    hj, hl = (j[3] - j[1]) + 2 * PADY, (l[3] - l[1]) + 2 * PADY
    top = MID_Y - (hj + GAP + hl) / 2
    s.bj_base = top + PADY + (1000 - j[1])                    # baselines so the ink sits PADY inside each box
    s.bl_base = top + hj + GAP + PADY + (1000 - l[1])
    bx0 = min(j[0], l[0]) - PADX
    s.boxJ = (bx0, top, j[2] + PADX, top + hj)
    s.boxL = (bx0, top + hj + GAP, l[2] + PADX, top + hj + GAP + hl)
    S3.Layer.__init__(s, 'caption', 1590.0, (40, int(top) - 40, 1060, int(top + hj + GAP + hl) + 50), S3.P_REF0, ss=1.0)
V.Caption2.__init__ = cap_init


def cap_tex_boxes(s, t):
    a, b = s.st(t); ox, oy = s.rect[0], s.rect[1]
    def box(d, r, op):
        x0, y0, x1, y1 = [int(round(v)) for v in (r[0] - ox, r[1] - oy, r[2] - ox, r[3] - oy)]
        d[max(0, y0):y1, max(0, x0):x1] *= (1 - BOX_OP * op)
    def fn(d):
        if a > 0:
            box(d, s.boxJ, a)
            L.put_text(d, 'Justin', s.PXJ, s.x + 8 - ox, s.bj_base + 12 * (1 - a) - oy, glow=0.22, op=a)
        if b > 0:
            lay = d.copy(); box(lay, s.boxL, 1.0); L.grad_text(lay, 'Levine', s.PXL, s.x - ox, s.bl_base - oy, glow=0.34)
            d[:] = d * (1 - b) + lay * b
    return S3.mc_draw(s.tw, s.th, fn)
V.Caption2.tex = cap_tex_boxes

_cap_key, _cap_tex = V.Caption2.key, V.Caption2.tex      # the caption rides on the card: revealed by the same wipe
V.Caption2.key = lambda s, t: (_cap_key(s, t), round(wipe_e(t), 3))
def cap_tex(s, t):
    M, C = _cap_tex(s, t)
    return wipe_mask(M, C, s.rect[0], s.ss, t)
V.Caption2.tex = cap_tex

finished = V.finished
A0_, A1_ = 8.6, 14.6
if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        os.makedirs(HERE + 'stills_v5', exist_ok=True)
        for a in sys.argv[2:]:
            n = int(round(float(a) * FPS)); Image.fromarray(finished(n)).save(HERE + f'stills_v5/s_{float(a):05.2f}.jpg', quality=92); print(a, flush=True)
    if sys.argv[1] == 'render':
        out = sys.argv[2]; n0, n1 = int(round(A0_ * FPS)), int(round(A1_ * FPS)); tmp = HERE + 'tmp_v5.mp4'
        p = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                              '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', '-r', '24', tmp], stdin=subprocess.PIPE)
        import multiprocessing as mp
        with mp.get_context('fork').Pool(int(os.environ.get('NW', 8))) as pool:
            for img in pool.imap(finished, range(n0, n1), chunksize=3): p.stdin.write(np.ascontiguousarray(img).tobytes())
        p.stdin.close(); p.wait(); dur = (n1 - n0) / FPS
        subprocess.run([FF, '-v', 'error', '-y', '-i', tmp, '-ss', f'{A0_:.4f}', '-t', f'{dur:.4f}', '-i', '/Users/gourav/jl-trailer/trailer/audio/mix.wav',
                        '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '320k', '-t', f'{dur:.4f}', '-movflags', '+faststart', out], check=True)
        os.remove(tmp); print('done', out, n1 - n0, 'frames', dur, 's')
