"""10-14 s scene v3: every element moves exactly like the Dime ref S3 (refs/dime_s3, f85-f160, checked frame by frame).
  f88-103  previous shot drifts, then whips LEFT (ease-in, heavy blur)          -> Nic, 8.95-9.45
  f100-125 speaker cut-out rises from below, 1.2 -> 1.0, settles (cubic out)   -> Justin (native 23.98 fps film)
  f101-110 photo card SLIDES IN from the left edge (ease-out), then sits       -> Shepherd sign photo (a still, like the ref)
  f109-130 caption words fade in on the card, hero word pops                   -> 'Justin' / 'Levine' (ride with the card)
  f110-139 near-static hold (~1 s)
  f131-    small headline word types on at the far right edge, then the truck
  f133-154 TRUCK (22 f, speed 2..90..1 px/f): card + caption 540 px left, speaker 500 px + x1.4 + defocus,
           headline only 280 px (parallax)                                     -> 'co-founder and CEO of' / 'Shepherd.'
  f150-160 hold, hard cut out                                                  -> hard cut into 02d
2.5D: each element is its own flat layer with its own move (the ref's parallax), no zoom-through anywhere.
  python scene_v3.py stills t ... | python scene_v3.py render out.mp4"""
import sys, os, math, subprocess
import numpy as np, cv2
from PIL import Image
from scipy.interpolate import PchipInterpolator
sys.path.insert(0, '/Users/gourav/jl-trailer/trailer/alt_10_14/')
import scene3d_v2 as V
S3 = V.S3
from engine import *
HERE = '/Users/gourav/jl-trailer/trailer/alt_10_14/'
FF = '/Users/gourav/ks-ron-build/reel1/ff'
T0, T1 = S3.T0, S3.T1
EO3 = V.EO3

# ---------------------------------------------------------------- the ref's truck, measured speed per frame (30 fps, px/f)
PROF = [2, 3, 4, 5, 6, 8, 10, 12, 15, 19, 26, 37, 49, 80, 90, 46, 28, 18, 11, 8, 4, 1]
_cum = np.concatenate([[0.0], np.cumsum(PROF)]) / float(sum(PROF))
_P = PchipInterpolator(np.arange(len(_cum)), _cum)
TR_D = len(PROF) / 30.0
TS = 11.11                                   # truck starts (ref f133) 2 f after the headline starts typing; peak (ref f147) at 11.58
N_TAKE = 278                                 # Justin's take change sits on the truck's fastest frame (11.583 s), like the ref hides cuts
def justin_idx(t):
    n = int(round(t * FPS))
    return int(np.clip(20 + (n - 226), 10, 89)) if n < N_TAKE else int(np.clip(440 + (n - N_TAKE), 440, 501))
V.justin_idx = justin_idx
def P(t):
    u = (t - TS) / TR_D * len(PROF)
    return 0.0 if u <= 0 else (1.0 if u >= len(PROF) else float(_P(u)))

CARD_T, CARD_D = V.RISE0 + 1 / 30, 0.30      # card slides in one ref frame after the speaker starts rising (f101-f110)
def card_e(t): return EO3((t - CARD_T) / CARD_D)


# ---------------------------------------------------------------- layers (textures from v2, placed flat on screen)
def card_tex(s, t):
    img = L.grade(V.film(540))               # the ref's card is a still photo: the clearest frame of the sign shot
    ox, oy = s.cx0 - s.rect[0], s.cy0 - s.rect[1]
    def fn(d): L.card(d, img, ox, oy, s.cw, s.ch, fx=0.20, fy=0.50, zoom=1.0, shadow=False)
    return S3.mc_draw(s.tw, s.th, fn)
S3.SignCard.key = lambda s, t: 0
S3.SignCard.tex = card_tex

LAY = None
def layers():
    global LAY
    if LAY is None: LAY = [S3.Ground(), V.Headline2(), S3.SignCard(), S3.Justin(), V.Caption2()]   # back -> front
    return LAY


def A0(l):
    x0, y0 = l.rect[0], l.rect[1]
    return np.array([[1 / l.ss, 0, x0], [0, 1 / l.ss, y0], [0, 0, 1]], np.float64)


def tr(dx, dy=0.0): return np.array([[1, 0, dx], [0, 1, dy], [0, 0, 1]], np.float64)
def sc_about(s, x, y): return np.array([[s, 0, x * (1 - s)], [0, s, y * (1 - s)], [0, 0, 1]], np.float64)

FACE = (CX, S3.Justin.DY + S3.SH1_FACE[1] * S3.Justin.SC)        # Justin's face on screen after the rise
CREEP = chain(T0, T1, 0.022, dur=3.0)                              # barely-there drift so nothing ever parks (Krish's graph)
def creep(t):
    dz = sum(m.at(t)[0] for m in CREEP); return sc_about(math.exp(dz), CX, CY)


def T_layer(l, t):
    p = P(t)
    if l.name == 'ground': return tr(-150 * p)
    if l.name in ('card', 'caption'):
        slide = -(1302 + 60) * (1 - card_e(t))
        return tr(-540 * p + slide)
    if l.name == 'justin':
        rise = V.rise_M(t).astype(np.float64) if t < V.RISE0 + V.RISE_D + 0.05 else np.eye(3)
        truck = tr(-500 * p, 26 * p) @ sc_about(1 + 0.40 * p, FACE[0], FACE[1])
        return truck @ rise
    if l.name == 'headline': return tr(280 * (1 - p))
    return np.eye(3)


def sig(l, t):
    p = P(t)
    if l.name == 'justin': return 12.0 * p          # the speaker becomes a soft foreground (ref lens blur 10-15 px)
    if l.name in ('card', 'caption'): return 3.0 * p
    return 0.0


def sub(t, tf):
    G = creep(t); out = None
    for l in layers():
        A = (G @ T_layer(l, t) @ A0(l))[:2].astype(np.float32)
        r = l.get(tf); s_ = sig(l, t)
        if l.opaque:
            out = cv2.warpAffine(r, A, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT); continue
        M, C = r
        Mw = cv2.warpAffine(M, A, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(1, 1, 1))
        Cw = cv2.warpAffine(C, A, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
        if s_ > 0.4: Mw = cv2.GaussianBlur(Mw, (0, 0), s_); Cw = cv2.GaussianBlur(Cw, (0, 0), s_)
        out = out * Mw + Cw
    return out


def speed(t):
    h = 0.25 / FPS
    v = 900 * abs(P(t + h) - P(t - h))
    v += 820 * abs(V.rise_e(t + h) - V.rise_e(t - h))
    v += 1360 * abs(card_e(t + h) - card_e(t - h))
    return v


def scene(t):
    J3.RNG_T[0] = t
    whip = t < V.WHIP0 + V.WHIP_D
    n = 16 if whip else int(np.clip(math.ceil(speed(t) / 1.6), 1, 16))
    nic = V.nic_layer(t) if whip else None
    acc = None
    for k in range(n):
        ts = t if n == 1 else t + (k / (n - 1) - 0.5) * 0.5 / FPS
        f = sub(ts, t)
        if whip:
            dx = V.whip_x(ts)
            if dx > -W:
                M = np.float32([[1, 0, dx], [0, 1, 0]])
                nw = cv2.warpAffine(nic, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
                msk = cv2.warpAffine(np.ones((H, W), np.float32), M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
                v = abs(V.whip_x(ts + 0.25 / FPS / n) - V.whip_x(ts - 0.25 / FPS / n))
                if v >= 3: nw = cv2.blur(nw, (int(v), 1)); msk = cv2.blur(msk, (int(v), 1))
                f = f * (1 - msk[..., None]) + nw * msk[..., None]
        acc = f if acc is None else acc + f
    return acc / n


def finished(n):
    t = n / FPS
    if t < V.WHIP0 or t >= T1: return V.v1().frame(n)
    return fin16.finish(np.clip(J3.grain(scene(t), 4.0, seed=n), 0, 255), vig=0.60, tex=0.30, rb=0.35)


A0_, A1_ = 8.6, 14.6
if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        os.makedirs(HERE + 'stills_v3b', exist_ok=True)
        for a in sys.argv[2:]:
            n = int(round(float(a) * FPS)); Image.fromarray(finished(n)).save(HERE + f'stills_v3b/s_{float(a):05.2f}.jpg', quality=92); print(a, flush=True)
    if sys.argv[1] == 'render':
        out = sys.argv[2]; n0, n1 = int(round(A0_ * FPS)), int(round(A1_ * FPS)); tmp = HERE + 'tmp_v3.mp4'
        p = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                              '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', '-r', '24', tmp], stdin=subprocess.PIPE)
        import multiprocessing as mp
        with mp.get_context('fork').Pool(int(os.environ.get('NW', 8))) as pool:
            for img in pool.imap(finished, range(n0, n1), chunksize=3): p.stdin.write(np.ascontiguousarray(img).tobytes())
        p.stdin.close(); p.wait(); dur = (n1 - n0) / FPS
        subprocess.run([FF, '-v', 'error', '-y', '-i', tmp, '-ss', f'{A0_:.4f}', '-t', f'{dur:.4f}', '-i', '/Users/gourav/jl-trailer/trailer/audio/mix.wav',
                        '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '320k', '-t', f'{dur:.4f}', '-movflags', '+faststart', out], check=True)
        os.remove(tmp); print('done', out, n1 - n0, 'frames', dur, 's')
