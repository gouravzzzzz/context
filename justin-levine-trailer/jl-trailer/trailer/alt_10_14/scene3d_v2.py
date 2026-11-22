"""10-14 s 3D scene, v2 (Krish's notes on v1):
  * footage was laggy: our screen recording of the Shepherd film had only 38 real frames in 78. Now the ORIGINAL film
    (Vimeo 1157667900, 23.98 fps) is used frame-for-frame on the 24 fps timeline: film/f<n>.jpg, native mattes matte_film/.
  * Justin centred (face at frame centre x, lower in frame); 'Justin / Levine' big (170 / 230 px), right beside him,
    in front of his outline like the Dime ref's 'Restaurant'; the landing headline bigger too.
  * NO zoom-through in or out. The Dime ref's own transitions (study_dmA S2->S3): the previous shot (Nic) WHIPS LEFT with an
    ease-in + heavy horizontal motion blur; Justin RISES from below while scaling 1.20 -> 1.00 with a 62 px left drift
    (ease-out ~0.83 s); the photo card enters with a left-anchored horizontal WIPE (0.3 s ease-out, blurred leading edge);
    the parallax truck; HARD CUT out.
  python scene3d_v2.py stills t ...  |  python scene3d_v2.py render out.mp4
"""
import sys, os, math, subprocess
import numpy as np, cv2
from PIL import Image
HERE = '/Users/gourav/jl-trailer/trailer/alt_10_14/'
sys.path.insert(0, HERE)
import scene3d as S3
from engine import *
HERE = '/Users/gourav/jl-trailer/trailer/alt_10_14/'          # (engine's * import also defines HERE)
FF = '/Users/gourav/ks-ron-build/reel1/ff'
S3.ZIN = 1.0                                           # no incoming zoom any more: layout = screen
T0, T1, CUT_IN = S3.T0, S3.T1, S3.CUT_IN
EO3 = lambda u: G1(cl(u))                              # v5: Krish's graph 1 (was a cubic ease-out)

# ---------------------------------------------------------------- native film frames
_FC = {}
def film(i):
    if i not in _FC:
        if len(_FC) > 8: _FC.pop(next(iter(_FC)))
        _FC[i] = cv2.cvtColor(cv2.imread(HERE + f'film/f{i:05d}.jpg'), cv2.COLOR_BGR2RGB).astype(np.float32)
    return _FC[i]
def film_matte(i):
    return np.asarray(Image.open(HERE + f'matte_film/f{i:05d}.png')).astype(np.float32) / 255

N_CUT = int(round(CUT_IN * FPS))
def justin_idx(t):
    n = int(round(t * FPS))
    return int(np.clip(20 + (n - 226), 10, 89)) if n < N_CUT else int(np.clip(446 + (n - N_CUT), 440, 501))

def justin_src(t):
    i = justin_idx(t)
    return film(i), film_matte(i), (None if i < 100 else S3.A20)

S3.justin_src = justin_src
S3.Justin.key = lambda s, t: ('f', justin_idx(t))

# Justin centred, lower: face at x = 960, face centre ~ y 515
S3.Justin.DX = CX - S3.SH1_FACE[0] * S3.Justin.SC
S3.Justin.DY = S3.Justin.DY + 120

# rise-in (ref f100-f125): from below the frame, scale 1.20 -> 1.00 about his base, 62 px drift left, cubic ease-out
RISE0, RISE_D = T0 - 0.10, 0.83
def rise_e(t): return EO3((t - RISE0) / RISE_D)
def rise_M(t):
    e = rise_e(t); s = 1.20 - 0.20 * e; dy = 820 * (1 - e); dx = 62 * (1 - e)
    return np.float32([[s, 0, CX * (1 - s) + dx], [0, s, H * (1 - s) + dy], [0, 0, 1]])

_H0 = S3.Layer.H
def H2(s, p):
    Hm, zr = _H0(s, p)
    if s.name == 'justin' and p['t'] < RISE0 + RISE_D + 0.05: Hm = rise_M(p['t']) @ Hm
    return Hm, zr
S3.Layer.H = H2

# ---------------------------------------------------------------- the photo card: sign shot (28 f) -> Shepherd end card
CARD_T = T0 + 0.10                                     # wipe starts 3 frames after Justin (ref f103)
WIPE_D = 0.30
def card_idx(t):
    n = int(round(t * FPS)); k = n - int(round(CARD_T * FPS))
    return 526 + int(np.clip(k, 0, 27))                  # the sign shot, real time; the card whips out as it ends
def wipe_e(t): return EO3((t - CARD_T) / WIPE_D)

def sign_key(s, t): return (card_idx(t), round(wipe_e(t), 3))
def sign_tex(s, t):
    img = L.grade(film(min(4143, card_idx(t))))
    ox, oy = s.cx0 - s.rect[0], s.cy0 - s.rect[1]
    e = wipe_e(t)
    def fn(d): L.card(d, img, ox, oy, s.cw, s.ch, fx=0.20, fy=0.50, zoom=1.0, shadow=True)
    M, C = S3.mc_draw(s.tw, s.th, fn)
    if e < 0.999:                                       # left-anchored wipe; the leading edge smears with its speed
        edge = ox + s.cw * e; v = s.cw * (wipe_e(t + 0.5 / FPS) - wipe_e(t - 0.5 / FPS))
        ramp = max(4.0, v * 1.2)
        xr = np.arange(s.tw, dtype=np.float32)
        m = np.clip((edge - xr) / ramp + 0.5, 0, 1)[None, :, None]
        M = 1 - m * (1 - M); C = C * m
    return M, C
S3.SignCard.key = sign_key
S3.SignCard.tex = sign_tex
CARD_OUT, CARD_OUT_D = CARD_T + 28 / FPS - 0.30, 0.30      # whip LEFT out (ease-in, graph 2) as its 28 real frames end
S3.LAYER_MOVES['card'] = [S3.M3(CARD_OUT, CARD_OUT_D, ease=G2, X=-2300)]


# ---------------------------------------------------------------- captions: big, right beside him, in front of his outline
class Caption2(S3.Layer):
    """'Justin' (fade 3 f + 12 px rise) / 'Levine' (gradient key word, 2 f pop-fade) -- big, left of Justin, tail over his arm"""
    PXJ, PXL = 170, 236
    def __init__(s):
        super().__init__('caption', 1590.0, (40, 520, 1060, 1012), S3.P_REF0, ss=1.0)
        s.tj, s.tl = S3.WORDS_['Justin'] - LEAD, S3.WORDS_['Levine.'] - LEAD
        wl = L.text_rgba('Levine', s.PXL, 'reg', (255, 255, 255), 1.0)[0].shape[1]
        s.x = min(150, 800 - wl)                       # block ends just over his left arm, clear of his face
    def st(s, t):
        return round(EIO(cl((t - s.tj) / (3 / FPS))) * 6) / 6, round(EIO(cl((t - s.tl) / (2 / FPS))) * 4) / 4
    def key(s, t): return s.st(t)
    def tex(s, t):
        a, b = s.st(t); ox, oy = s.rect[0], s.rect[1]
        def fn(d):
            if a > 0: L.put_text(d, 'Justin', s.PXJ, s.x + 8 - ox, 772 + 12 * (1 - a) - oy, glow=0.22, op=a)
            if b > 0:
                lay = d.copy(); L.grad_text(lay, 'Levine', s.PXL, s.x - ox, 978 - oy, glow=0.34)
                d[:] = d * (1 - b) + lay * b
        return S3.mc_draw(s.tw, s.th, fn)


class Headline2(S3.Headline):
    """same type-on as v1, bigger: 'co-founder and CEO of' 84 px over 'Shepherd.' 264 px"""
    def __init__(s):
        s.R, s.yS = 1790, 372; s.yB = 640; s.pxS, s.pxB = 84, 264
        S3.Layer.__init__(s, 'headline', 2850.0, (720, 200, 1840, 760), S3.P_LAND, ss=1.2)
        ss = s.ss
        s.small = ''.join(v for _, v in s.SMALL); s.big = 'Shepherd.'
        s.wS = J3.text_rgba(s.small, int(s.pxS * ss), hs=1.0)[0].shape[1]; s.wB = J3.text_rgba(s.big, int(s.pxB * ss), hs=1.0)[0].shape[1]
        s.xS = (s.R - s.rect[0]) * ss - s.wS; s.xB = (s.R - s.rect[0]) * ss - s.wB
        s.eS = [s.xS + J3.text_rgba(s.small[:i], int(s.pxS * ss), hs=1.0)[0].shape[1] if i else s.xS for i in range(len(s.small) + 1)]
        s.eB = [s.xB + J3.text_rgba(s.big[:i], int(s.pxB * ss), hs=1.0)[0].shape[1] if i else s.xB for i in range(len(s.big) + 1)]
        s.tS = []
        for key, txt in s.SMALL:
            t0 = S3.WORDS_[key] - LEAD; nl = len(txt); dt = min(2.0, max(0.8, 6.0 / nl)) / FPS
            s.tS += [t0 + i * dt for i in range(nl)]
        t0 = S3.WORDS_['Shepherd.'] - LEAD; s.tB = [t0 + i * 1.1 / FPS for i in range(len(s.big))]
        s.full = None


def layers2():
    if S3.LAYERS is None: S3.LAYERS = [S3.Ground(), Headline2(), S3.SignCard(), S3.Justin(), Caption2()]   # far -> near
    return S3.LAYERS
S3.layers = layers2
S3.screen_X = lambda t: (np.float32([[1, 0, 0], [0, 1, 0]]), 1.0)        # no zoom in / out at all; hard cut out

_PS = S3.probe_speed
def probe2(t):
    h = 0.25 / FPS
    v = _PS(t)
    v += 800 * abs(rise_e(t + h) - rise_e(t - h))                              # Justin's rise
    v += 700 * abs(wipe_e(t + h) - wipe_e(t - h)) * 0.5                        # card wipe edge
    v += 1800 * abs(G2(cl((t + h - CARD_OUT) / CARD_OUT_D)) - G2(cl((t - h - CARD_OUT) / CARD_OUT_D)))   # card whip out
    return v
S3.probe_speed = probe2


# ---------------------------------------------------------------- neighbours: Nic whips LEFT out (ref S2 exit), hard cut into 02d
WHIP0, WHIP_D = T0 - 0.50, 0.50
_R = None
def v1():
    global _R
    if _R is None:
        R = S3.v1()
        for s_ in R.SHOTS:
            if s_.name == '02a_nic': s_.tout = 'cut'
            if s_.name in ('02b_name', '02d_founded'): s_.tin = 'cut'
        _R = R
    return _R


def whip_x(t): return -1.08 * W * G2(cl((t - WHIP0) / WHIP_D))


def nic_layer(t):
    R = v1(); i = [k for k, s_ in enumerate(R.SHOTS) if s_.name == '02a_nic'][0]
    return R.shot_frame(i, min(t, T0 - 1e-3))


def scene_frame(t):
    """the 3D scene, plus Nic whipping off over it before T0"""
    J3.RNG_T[0] = t
    if t < WHIP0 + WHIP_D:
        nsub = 16; acc = None; nic = nic_layer(t)
        for k in range(nsub):
            ts = t + (k / (nsub - 1) - 0.5) * 0.5 / FPS
            base = S3.sub_render(ts, t) if ts >= RISE0 - 0.2 else S3.sub_render(RISE0 - 0.2, t)
            dx = whip_x(ts)
            if dx > -W:
                M = np.float32([[1, 0, dx], [0, 1, 0]])
                nw = cv2.warpAffine(nic, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
                msk = cv2.warpAffine(np.ones((H, W), np.float32), M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)[..., None]
                v = abs(whip_x(ts + 0.25 / FPS / nsub) - whip_x(ts - 0.25 / FPS / nsub))
                if v >= 3: nw = cv2.blur(nw, (int(v), 1)); msk = cv2.blur(msk, (int(v), 1))[..., None] if msk.ndim == 3 else msk
                f = base * (1 - msk) + nw * msk
            else: f = base
            acc = f if acc is None else acc + f
        return acc / nsub
    return S3.frame(t)[0]


def finished(n):
    t = n / FPS
    if t < WHIP0 or t >= T1: return v1().frame(n)
    out = scene_frame(t)
    return fin16.finish(np.clip(J3.grain(out, 4.0, seed=n), 0, 255), vig=0.60, tex=0.30, rb=0.35)


A0, A1 = 8.6, 14.6
if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        os.makedirs(HERE + 'stills_v2', exist_ok=True)
        for a in sys.argv[2:]:
            n = int(round(float(a) * FPS)); Image.fromarray(finished(n)).save(HERE + f'stills_v2/s_{float(a):05.2f}.jpg', quality=92); print(a, flush=True)
    if sys.argv[1] == 'render':
        out = sys.argv[2]; n0, n1 = int(round(A0 * FPS)), int(round(A1 * FPS)); tmp = HERE + 'tmp_v2.mp4'
        p = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                              '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', '-r', '24', tmp], stdin=subprocess.PIPE)
        import multiprocessing as mp
        with mp.get_context('fork').Pool(int(os.environ.get('NW', 8))) as pool:
            for img in pool.imap(finished, range(n0, n1), chunksize=3): p.stdin.write(np.ascontiguousarray(img).tobytes())
        p.stdin.close(); p.wait(); dur = (n1 - n0) / FPS
        subprocess.run([FF, '-v', 'error', '-y', '-i', tmp, '-ss', f'{A0:.4f}', '-t', f'{dur:.4f}', '-i', '/Users/gourav/jl-trailer/trailer/audio/mix.wav',
                        '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '320k', '-t', f'{dur:.4f}', '-movflags', '+faststart', out], check=True)
        os.remove(tmp); print('done', out, n1 - n0, 'frames', dur, 's')
