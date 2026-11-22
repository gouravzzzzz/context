"""Trailer v2 segment 12 -- NEW frames 1343-1392 (v1 06c_collage, "It's somewhat manufactured.") rebuilt in real 3D.
Same design/layout as v1 (two cards on top, one below, "It's somewhat" top centre, gradient italic "manufactured." over the
lower card, white where it crosses a card = track-matte split). Every card and text line is its own plane at its own depth
in one pinhole camera (F = 1600). Camera: continuous dolly in z + slight orbit (yaw about a pivot at z 1800) + small
pedestal, all built from stacked overlapping moves on Krish's EU graph (never parks). The camera passes through the v1
layout pose at T_L, so the settled frame is the v1 design. Cards fly in along z (from 900 deeper + 160 px low, with a
settling plane rotation) on G1 at the v1 times; text planes approach in z on G1 and land flat (no rotation).
B-roll at REAL speed: source frame = start + round(elapsed * 30) on dup-free OSHA footage (no speed-up, no holds).
  python scene12.py stills n1 n2 ...   -> stills/s_<n>.jpg
  python scene12.py speed              -> per-frame motion print
  python scene12.py render             -> ../v2segs/12_manufactured.mp4 (+ _check.mp4 with mix2.wav)
"""
import sys, os, math, json, subprocess
import numpy as np, cv2
from PIL import Image
sys.path.insert(0, '/Users/gourav/jl-trailer/trailer')
from engine import *                              # W, H, CX, CY, L, J3, EU, G1, G2, EIO, cl, vid, tech, fin16, LEAD, FPS
from newtime import WORDS as WN

HERE = '/Users/gourav/jl-trailer/trailer/seg12/'
OUTD = '/Users/gourav/jl-trailer/trailer/v2segs/'
FF = '/Users/gourav/ks-ron-build/reel1/ff'
N0, N1 = 1343, 1392
T0, T1 = N0 / FPS, N1 / FPS
TS0 = 55.9783                                     # v1 06c start on the NEW timeline
F = 1600.0
ZP = 1800.0                                       # orbit pivot depth (camera sits at Z 0 at the layout pose)


def wn(w): return next(x[0] for x in WN if x[2] == w and 56.0 < x[0] < 58.1)
T_ITS = wn('somewhat') - 0.30                     # v1: the line came in 0.30 s before 'somewhat'
T_SOME = wn('somewhat') - LEAD
T_MAN = wn('manufactured') - LEAD                 # v1: wt('manufactured') - LEAD
T_L = 57.50                                       # camera passes the v1 layout pose here (frame 1380)


# ---------------------------------------------------------------- camera: stacked overlapping EU moves (nulls)
def stacked(span, dur=2.0, step=0.10, w0=1.3, w1=0.7, at_L=0.0):
    """value(t): sum of overlapped EU moves (next starts 10 % into the previous: a smooth glide), weights fall w0 -> w1 (decelerating),
    scaled so value(T1) - value(T0) = span and offset so value(T_L) = at_L. Moves start before T0 and run past T1."""
    st = dur * step; start = T0 - 0.6 * dur
    n = int(math.ceil((T1 + 0.6 * dur - start) / st))
    ws = np.linspace(w0, w1, n)
    def raw(t): return sum(w * EU(cl((t - (start + i * st)) / dur)) for i, w in enumerate(ws))
    k = span / (raw(T1) - raw(T0)); off = at_L - k * raw(T_L)
    return lambda t: off + k * raw(t)


R_ = stacked(-280.0, at_L=1800.0)                 # dolly in: camera-to-pivot distance shrinks
A_ = stacked(-8.0, dur=2.4, w0=1.1, w1=0.9)       # orbit (deg): from the left side round to slightly right
Y_ = stacked(-28.0, dur=2.4, w0=1.0, w1=1.0)      # small pedestal up


def pose(t):
    a, r = A_(t), R_(t); th = math.radians(a)
    return dict(X=-r * math.sin(th), Y=Y_(t), Z=ZP - r * math.cos(th), yaw=a, t=t)


PL = dict(X=0.0, Y=0.0, Z=0.0, yaw=0.0)            # layout pose (= v1 screen layout)


def project(pts, p):
    th = math.radians(p['yaw']); c, s_ = math.cos(th), math.sin(th)
    x = pts[:, 0] - p['X']; y = pts[:, 1] - p['Y']; z = pts[:, 2] - p['Z']
    xr = c * x - s_ * z; zr = s_ * x + c * z
    return np.stack([CX + F * xr / zr, CY + F * y / zr], 1).astype(np.float32), zr


def unproject_rect(x0, y0, x1, y1, Z):
    return np.float32([[(u - CX) * Z / F, (v - CY) * Z / F, Z] for u, v in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))])


def mc_draw(w, h, fn):
    P0 = np.zeros((h, w, 3), np.float32); P1 = np.full((h, w, 3), 200.0, np.float32)
    fn(P0); fn(P1)
    return (P1 - P0) / 200.0, P0


# ---------------------------------------------------------------- layers
class Layer:
    opaque = False
    def __init__(s, name, Z, rect, ss=1.0):
        s.name, s.Z, s.rect, s.ss = name, Z, rect, ss
        s.quad = unproject_rect(*rect, Z)
        s.tw, s.th = int(round((rect[2] - rect[0]) * ss)), int(round((rect[3] - rect[1]) * ss))
        s.cache = {}
    def xf(s, t): return 0.0, 0.0, 0.0, 0.0, 0.0, 1.0      # dx, dy (screen px at layout), dz, rot_y, rot_x (deg), alpha
    def key(s, n, t): return None
    def get(s, n, t):
        k = s.key(n, t)
        if k is not None and k in s.cache: return s.cache[k]
        r = s.tex(n, t)
        if k is not None:
            if len(s.cache) > 8: s.cache.pop(next(iter(s.cache)))
            s.cache[k] = r
        return r
    def world(s, t):
        dx, dy, dz, ry, rx, a = s.xf(t)
        q = s.quad.copy(); c = q.mean(0)
        d = q - c
        if ry:
            th = math.radians(ry); x, z = d[:, 0].copy(), d[:, 2].copy()
            d[:, 0] = x * math.cos(th) - z * math.sin(th); d[:, 2] = x * math.sin(th) + z * math.cos(th)
        if rx:
            th = math.radians(rx); y, z = d[:, 1].copy(), d[:, 2].copy()
            d[:, 1] = y * math.cos(th) - z * math.sin(th); d[:, 2] = y * math.sin(th) + z * math.cos(th)
        k = s.Z / F
        return c + d + np.float32([dx * k, dy * k, dz]), a
    def H(s, p, t):
        q, a = s.world(t)
        scr, zr = project(q, p)
        src = np.float32([[0, 0], [s.tw, 0], [s.tw, s.th], [0, s.th]])
        return cv2.getPerspectiveTransform(src, scr), a


class Ground(Layer):
    opaque = True
    def __init__(s): super().__init__('ground', 4300.0, (-520, -320, 2440, 1400))
    def key(s, n, t): return n
    def tex(s, n, t):
        g = tech(29, n / FPS, 0.6)
        return cv2.copyMakeBorder(g, 320, 320, 520, 520, cv2.BORDER_REFLECT)


DUP = None
def uniq192():
    global DUP
    if DUP is None:
        c = cv2.VideoCapture('/Users/gourav/jl-trailer/trailer/broll/c_osha_192.mp4'); prev = None; DUP = []; i = 0
        while True:
            ok, f = c.read()
            if not ok: break
            g = cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (480, 270)).astype(np.float32)
            if prev is None or np.abs(g - prev).mean() > 1.5: DUP.append(i)
            prev = g; i += 1
    return DUP


# v1 Collage.CARDS layout (x0, y0, w, h) + depth + settle rotation (y, x). Footage at REAL speed (Krish): source frame =
# start + round(elapsed * 30), every real frame shown. v1's s_osha_hs (a slowed copy) and c_osha_192 (49 % duplicate frames:
# 3-frame holds at real time) are replaced by clean OSHA footage from c_osha_11 (0 dup in the tiles used, frames >= 15):
# its tank-site inspection tile and its harness-compliance tile (clean crops, logo excluded). c_osha_96 (0 dup) stays.
#        clip, start, crop (x0, y0, x1, y1) or None, x0, y0, w, h, fx, fy, zoom, depth, rot_y, rot_x
CARDS = [('c_osha_11', 15, (962, 678, 1632, 1080), 430, 190, 500, 300, 0.5, 0.5, 1.0, 2150.0, 18.0, 0.0),
         ('c_osha_11', 20, (1130, 0, 1830, 420), 990, 210, 500, 300, 0.5, 0.5, 1.0, 1900.0, -18.0, 0.0),
         ('c_osha_96', 0, None, 700, 560, 520, 310, 0.62, 0.32, 1.40, 1650.0, 0.0, 14.0)]
MG = 56


class Card(Layer):
    def __init__(s, i):
        s.i = i; (s.clip, s.u0, s.crop, x0, y0, s.cw, s.ch, s.fx, s.fy, s.zm, Z, s.ry0, s.rx0) = CARDS[i]
        s.t_in = TS0 - 0.04 + 0.16 * i                          # v1 stagger (first card already arriving at the hard cut)
        super().__init__('card%d' % i, Z, (x0 - MG, y0 - MG, x0 + s.cw + MG, y0 + s.ch + MG), ss=1.35)
        b = np.zeros((s.th, s.tw), np.float32)
        m = int(round(MG * s.ss)); b[m:m + int(round(s.ch * s.ss)), m:m + int(round(s.cw * s.ss))] = 1.0
        s.body = b
    def e(s, t): return G1(cl((t - s.t_in) / 0.75))
    def xf(s, t):
        e = s.e(t); u = 1 - e
        return 0.0, 160.0 * u, 900.0 * u, s.ry0 * u, s.rx0 * u, cl(e * 1.6)
    def src_index(s, n):
        """REAL time: start + round(elapsed * 30) at the output frame's time (dup-free sources: every real frame shown)"""
        return s.u0 + int(round(max(0.0, n / FPS - s.t_in) * 30.0))
    def key(s, n, t): return n
    def tex(s, n, t):
        img = L.grade(vid(s.clip).frame(s.src_index(n)))
        if s.crop: x0, y0, x1, y1 = s.crop; img = np.ascontiguousarray(img[y0:y1, x0:x1])
        ss = s.ss; m = int(round(MG * ss)); w, h = int(round(s.cw * ss)), int(round(s.ch * ss))
        def fn(d): L.card(d, img, m, m, w, h, fx=s.fx, fy=s.fy, zoom=s.zm)
        return mc_draw(s.tw, s.th, fn)


def blur_mc(M, C, sig):
    if sig < 0.3: return M, C
    return cv2.GaussianBlur(M, (0, 0), sig), cv2.GaussianBlur(C, (0, 0), sig)


class Line1(Layer):
    """"It's somewhat" (v1: 54 px, centred, baseline 130) -- per word: 3-frame fade, 12 px rise, blur clearing, in place"""
    PX, BASE = 54, 130
    def __init__(s):
        super().__init__('line1', 1500.0, (CX - 330, 40, CX + 330, 185), ss=1.5)
        full = J3.text_rgba("It's somewhat", s.PX)[0].shape[1]; w2 = J3.text_rgba('somewhat', s.PX)[0].shape[1]
        s.x1 = CX - full / 2; s.x2 = s.x1 + full - w2
        s.tw_ = [T_ITS, T_SOME]
    def xf(s, t): return 0.0, 0.0, 260.0 * (1 - G1(cl((t - T_ITS) / 0.8))), 0.0, 0.0, 1.0
    def st(s, t): return tuple(round(EIO(cl((t - tw) / (3 / FPS))) * 6) / 6 for tw in s.tw_)
    def key(s, n, t): return s.st(t)
    def tex(s, n, t):
        ss = s.ss; M = np.ones((s.th, s.tw, 3), np.float32); C = np.zeros((s.th, s.tw, 3), np.float32)
        for word, x, a in (("It's", s.x1, s.st(t)[0]), ('somewhat', s.x2, s.st(t)[1])):
            if a <= 0: continue
            def fn(d): L.put_text(d, word, int(s.PX * ss), (x - s.rect[0]) * ss, (s.BASE + 12 * (1 - a) - s.rect[1]) * ss, glow=0.18, op=a)
            Mi, Ci = blur_mc(*mc_draw(s.tw, s.th, fn), 4.0 * ss * (1 - a))
            M = M * Mi; C = C * Mi + Ci
        return M, C


def type_mask(w, edges, n_full, frac):
    m = np.zeros(w, np.float32)
    m[:int(edges[n_full])] = 1.0
    if n_full < len(edges) - 1: m[int(edges[n_full]):int(edges[n_full + 1])] = frac
    return m


class Hero(Layer):
    """"manufactured." (v1: 176 px italic, centred, baseline 800) -- types on letter by letter in place; gradient off the
    cards, white over them (the v1 track-matte split, done in screen space against the projected card bodies)"""
    PX, BASE, TXT, DT = 176, 800, 'manufactured.', 0.75
    def __init__(s):
        rg, asc = J3.text_rgba(s.TXT, s.PX, face='it')
        s.w = rg.shape[1]; s.asc = asc; x0 = CX - s.w / 2
        super().__init__('hero', 1250.0, (int(x0 - 70), int(s.BASE - asc - 60), int(x0 + s.w + 70), int(s.BASE - asc + rg.shape[0] + 60)), ss=1.3)
        ss = s.ss; xl = (x0 - s.rect[0]) * ss
        s.edges = [xl + (J3.text_rgba(s.TXT[:i], int(s.PX * ss), face='it')[0].shape[1] if i else 0) for i in range(len(s.TXT) + 1)]
        s.edges[-1] = s.tw
        s.tl = [T_MAN + i * s.DT / FPS for i in range(len(s.TXT))]
        bx, by = (CX - s.rect[0]) * ss, (s.BASE - s.rect[1]) * ss
        s.white = mc_draw(s.tw, s.th, lambda d: L.put_text(d, s.TXT, int(s.PX * ss), bx, by, align='center', face='it', glow=0.18))
        s.grad = mc_draw(s.tw, s.th, lambda d: L.grad_text(d, s.TXT, int(s.PX * ss), bx, by, align='center', face='it'))
    def xf(s, t): return 0.0, 0.0, 300.0 * (1 - G1(cl((t - T_MAN) / 0.85))), 0.0, 0.0, 1.0
    def st(s, t):
        n = sum(1 for x in s.tl if t >= x + 1.0 / FPS); f = 0.0
        if n < len(s.tl) and t >= s.tl[n]: f = round(cl((t - s.tl[n]) * FPS) * 2) / 2
        return n, f
    def key(s, n, t): return s.st(t)
    def tex(s, n, t):
        k, f = s.st(t)
        if k == 0 and f == 0: return None
        m = type_mask(s.tw, s.edges, k, f)[None, :, None]
        return [(1 - m * (1 - Mi), Ci * m) for Mi, Ci in (s.white, s.grad)]


LAYERS = None
def layers():
    global LAYERS
    if LAYERS is None: LAYERS = [Ground(), Card(0), Card(1), Card(2), Line1(), Hero()]
    return LAYERS


def warp_mc(M, C, Hm):
    Mw = cv2.warpPerspective(M, Hm, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(1, 1, 1))
    Cw = cv2.warpPerspective(C, Hm, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
    return Mw, Cw


def sub_render(ts, n, tf):
    p = pose(ts); out = None; cov = None
    for ly in layers():
        Hm, a = ly.H(p, ts)
        if ly.opaque:
            out = cv2.warpPerspective(ly.get(n, tf), Hm, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT); continue
        if a <= 0.002: continue
        r = ly.get(n, tf)
        if r is None: continue
        if isinstance(ly, Hero):
            (Mw1, Cw1), (Mw2, Cw2) = warp_mc(*r[0], Hm), warp_mc(*r[1], Hm)
            c = cov[..., None] if cov is not None else 0.0
            out = out * (c * Mw1 + (1 - c) * Mw2) + (c * Cw1 + (1 - c) * Cw2); continue
        M, C = r
        if a < 0.999: M = 1 - a * (1 - M); C = C * a
        Mw, Cw = warp_mc(M, C, Hm)
        out = out * Mw + Cw
        if isinstance(ly, Card):
            b = cv2.warpPerspective(ly.body, Hm, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0) * a
            cov = b if cov is None else np.maximum(cov, b)
    return out


def probe_speed(t):
    h = 0.25 / FPS; pts = []
    for tt in (t - h, t + h):
        p = pose(tt); q = []
        for ly in layers()[1:]:
            Hm, a = ly.H(p, tt)
            if a <= 0.002: q.append(np.zeros((2, 2), np.float32)); continue
            c = np.float32([[[0, 0]], [[ly.tw, ly.th]]]); q.append(cv2.perspectiveTransform(c, Hm).reshape(-1, 2))
        pts.append(np.concatenate(q))
    d = np.abs(pts[0] - pts[1]).max(1)
    return float(d.max())


def frame(n):
    t = n / FPS; J3.RNG_T[0] = t
    d = probe_speed(t); ns = int(np.clip(math.ceil(d / 1.6), 1, 12))
    if ns == 1: out = sub_render(t, n, t)
    else: out = sum(sub_render(t + (k / (ns - 1) - 0.5) * 0.5 / FPS, n, t) for k in range(ns)) / ns
    return fin16.finish(np.clip(J3.grain(out, 4.5, seed=n), 0, 255), vig=0.60, tex=0.35, rb=0.50), ns, d


def render_range(args):
    a, b, path = args
    p = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', '24', path], stdin=subprocess.PIPE)
    for n in range(a, b):
        img, ns, d = frame(n); p.stdin.write(np.ascontiguousarray(img).tobytes()); print(n, ns, round(d, 1), flush=True)
    p.stdin.close(); p.wait()
    return path


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'stills':
        os.makedirs(HERE + 'stills', exist_ok=True)
        for a in sys.argv[2:]:
            n = int(a); img, ns, d = frame(n)
            Image.fromarray(img).save(HERE + f'stills/s_{n}.jpg', quality=90); print(n, 'sub', ns, 'speed %.1f' % d, flush=True)
    elif mode == 'speed':
        prev = None
        for n in range(N0, N1):
            t = n / FPS; p = pose(t); q = []
            for ly in layers()[1:]:
                Hm, a = ly.H(p, t); c = np.float32([[[0, 0]], [[ly.tw, ly.th]]]); q.append(cv2.perspectiveTransform(c, Hm).reshape(-1, 2))
            cam = cv2.perspectiveTransform(np.float32([[[CX, CY]], [[200, 150]], [[1700, 900]]]), layers()[4].H(p, t)[0] @ np.linalg.inv(layers()[4].H(PL, 99)[0])).reshape(-1, 2)
            q = np.concatenate(q)
            if prev is not None:
                print(n, 'layers %6.2f' % np.abs(q - prev[0]).max(), ' cam(text plane) %5.2f' % np.abs(cam - prev[1]).max(), '#' * int(np.abs(cam - prev[1]).max() * 4))
            prev = (q, cam)
    elif mode == 'pose':
        for n in range(N0, N1 + 1, 4): print(n, {k: round(v, 2) for k, v in pose(n / FPS).items()})
    elif mode == 'render':
        import multiprocessing as mp
        os.makedirs(HERE + 'chunks', exist_ok=True)
        cuts = [N0, N0 + 17, N0 + 34, N1]
        jobs = [(cuts[i], cuts[i + 1], HERE + f'chunks/c{i}.mp4') for i in range(3)]
        with mp.get_context('fork').Pool(3) as pool: paths = pool.map(render_range, jobs)
        open(HERE + 'chunks/list.txt', 'w').write(''.join(f"file '{q}'\n" for q in paths))
        out = OUTD + '12_manufactured.mp4'
        subprocess.run([FF, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', HERE + 'chunks/list.txt', '-c', 'copy', out], check=True)
        subprocess.run([FF, '-v', 'error', '-y', '-i', out, '-ss', f'{N0 / FPS:.5f}', '-t', f'{(N1 - N0) / FPS:.5f}',
                        '-i', '/Users/gourav/jl-trailer/trailer/audio/mix2.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                        '-c:a', 'aac', '-b:a', '256k', '-shortest', OUTD + '12_manufactured_check.mp4'], check=True)
        print('done', out)
