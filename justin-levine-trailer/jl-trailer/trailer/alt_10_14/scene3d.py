"""ALT 9.45-14.16 (replaces 02b name card + 02c Shepherd card) -- a real 3D z-space shot copying the Dime 'Sports Bra' trailer
4-5 s (S3, f120-150): settled layout (photo card left + speaker cut-out with sticker outline + 2-line caption bottom-left),
words fading in, hero words typing on letter by letter at the right edge, then a 2.5D/3D TRUCK RIGHT + PUSH FORWARD past the
speaker, who becomes a big defocused foreground while the headline lands on the right.
Here every layer is a plane at its own depth in ONE pinhole camera; the camera dollies along z (+ trucks x, small yaw), so
text and footage parallax for real. All moves on Krish's graph (EASE_USER), overlapped; out on G2, in on G1.
  python scene3d.py stills t1 t2 ...   -> stills/s_<t>.png + sheet.jpg
"""
import sys, os, math, json
import numpy as np, cv2
from PIL import Image
sys.path.insert(0, '/Users/gourav/jl-trailer/trailer')
from engine import *                              # W, H, CX, CY, L, S, J3, EU, G1, G2, EIO, cl, vid, matte, tech, fin16 ...
HERE = '/Users/gourav/jl-trailer/trailer/alt_10_14/'
T0, T1 = 9.45, 14.16
F = 1600.0                                        # focal length (px): a plane at z = F renders 1:1
WORDS_ = {w[2]: w[0] for w in WORDS if 9.4 < w[0] < 14.3}


# ---------------------------------------------------------------- camera: stacked moves (keyframe overlapping)
class M3:
    def __init__(s, t0, dur, ease=EU, **d): s.t0, s.dur, s.e, s.d = t0, dur, ease, d
    def at(s, t): e = s.e(cl((t - s.t0) / s.dur)); return {k: v * e for k, v in s.d.items()}


TR0, TR_DUR = 10.80, 2.5                          # the truck: slow in, fastest ~11.75, long settle (EU), lands ~13.1
MOVES = []
for i in range(8):                                # pre-truck creep: 3 s moves every 0.6 s (next starts 20 % in) -> never parks
    MOVES.append(M3(8.05 + 0.6 * i, 3.0, Z=22, X=6))
MOVES += [M3(TR0, TR_DUR, X=500, Z=390, Y=-12),   # truck right + push forward past Justin
          M3(TR0 + 0.2, 1.8, yaw=2.6), M3(TR0 + 1.1, 2.4, yaw=-2.6)]   # yaw swings in with the truck, back to 0 from 50 % (text lands straight)
for i in range(7):                                # post-landing drift, starts 40 % into the truck, keeps moving into the cut
    MOVES.append(M3(TR0 + 1.0 + 0.6 * i, 3.0, Z=16, X=7))


LAYER_MOVES = {'card': [M3(TR0, TR_DUR, X=-720)], 'caption': [M3(TR0, TR_DUR, X=-720)]}


def pose(t):
    p = dict(X=0.0, Y=0.0, Z=0.0, yaw=0.0, t=t)
    for m in MOVES:
        for k, v in m.at(t).items(): p[k] += v
    return p


P_REF0 = pose(T0)                                  # layout pose for the opening layers
P_LAND = pose(13.45)                               # layout pose for the landing headline


def project(pts, p):
    """world (N,3) -> screen (N,2) for camera pose p (yaw in degrees, positive = turn right)"""
    th = math.radians(p['yaw']); c, s_ = math.cos(th), math.sin(th)
    x = pts[:, 0] - p['X']; y = pts[:, 1] - p['Y']; z = pts[:, 2] - p['Z']
    xr = c * x - s_ * z; zr = s_ * x + c * z
    return np.stack([CX + F * xr / zr, CY + F * y / zr], 1).astype(np.float32), zr


def unproject_rect(x0, y0, x1, y1, Z, p):
    """screen rect seen at pose p (yaw 0 assumed for layout) -> world corners on the plane z = Z"""
    zr = Z - p['Z']
    return np.float32([[p['X'] + (u - CX) * zr / F, p['Y'] + (v - CY) * zr / F, Z] for u, v in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))])


# ---------------------------------------------------------------- layers: (M, C) textures on world planes
class Layer:
    """texture drawn with the affine trick (M = multiplier, C = add), mapped onto a world quad; per-layer defocus."""
    def __init__(s, name, Z, rect, ref_pose, ss=1.0, opaque=False):
        s.name, s.Z, s.ss, s.opaque = name, Z, ss, opaque
        s.rect = rect; s.quad = unproject_rect(*rect, Z, ref_pose)
        s.tw, s.th = int(round((rect[2] - rect[0]) * ss)), int(round((rect[3] - rect[1]) * ss))
        s.cache = {}
    def tex(s, t): raise NotImplementedError       # -> (M, C) at texture size, or RGB if opaque
    def key(s, t): return None
    def get(s, t):
        k = s.key(t)
        if k is not None and k in s.cache: return s.cache[k]
        r = s.tex(t)
        if k is not None:
            if len(s.cache) > 30: s.cache.pop(next(iter(s.cache)))
            s.cache[k] = r
        return r
    def H(s, p):
        q = s.quad
        if s.name in LAYER_MOVES:                   # the card (with its caption) also slides out left on the truck's curve
            off = sum(m.at(p['t'])['X'] for m in LAYER_MOVES[s.name]); q = q + np.float32([off, 0, 0])
        scr, zr = project(q, p)
        src = np.float32([[0, 0], [s.tw, 0], [s.tw, s.th], [0, s.th]])
        return cv2.getPerspectiveTransform(src, scr), float(zr.mean())


ZIN = 1.07                                         # the zoom-through's incoming G1 zoom, fully on after 0.85 s
def pre(x, y):
    """final screen position (after the incoming zoom) -> layout position"""
    return CX + (x - CX) / ZIN, CY + (y - CY) / ZIN


def mc_draw(w, h, fn):
    P0 = np.zeros((h, w, 3), np.float32); P1 = np.full((h, w, 3), 200.0, np.float32)
    fn(P0); fn(P1)
    return (P1 - P0) / 200.0, P0


class Ground(Layer):
    def __init__(s):
        super().__init__('ground', 4300.0, (-420, -200, 2420, 1300), P_REF0, opaque=True)
    def key(s, t): return int(round(t * FPS))
    def tex(s, t):
        g = tech(23, t, 0.8)
        pad = cv2.copyMakeBorder(g, 200, 220, 420, 500, cv2.BORDER_REFLECT)
        return cv2.resize(pad, (s.tw, s.th), interpolation=cv2.INTER_LINEAR)


class SignCard(Layer):
    """Shepherd's own sign film as the photo card on the left (the ref's restaurant card); square corners, soft shadow"""
    def __init__(s):
        s.cx0, s.cy0, s.cw, s.ch = 92, 84, 1150, 896
        super().__init__('card', 2050.0, (32, 24, 92 + 1150 + 60, 84 + 896 + 70), P_REF0)
    def key(s, t): return int(round(t * FPS))
    def tex(s, t):
        img = L.grade(vid('s_shep_sign').at(min(2.95, (t - T0) * 0.62)))
        ox, oy = s.cx0 - s.rect[0], s.cy0 - s.rect[1]
        def fn(d): L.card(d, img, ox, oy, s.cw, s.ch, fx=0.20, fy=0.50, zoom=1.0, shadow=True)
        return mc_draw(s.tw, s.th, fn)


class Caption(Layer):
    """'Justin' (fades in 3 f with a 12 px rise) / 'Levine' (cyan->blue key word, 2 f pop-fade) -- bottom-left of the card"""
    def __init__(s):
        super().__init__('caption', 1960.0, (96, 640, 900, 1026), P_REF0, ss=1.25)
        s.tj, s.tl = WORDS_['Justin'] - LEAD, WORDS_['Levine.'] - LEAD
    def st(s, t):
        a = round(EIO(cl((t - s.tj) / (3 / FPS))) * 6) / 6; b = round(EIO(cl((t - s.tl) / (2 / FPS))) * 4) / 4
        return a, b
    def key(s, t): return s.st(t)
    def tex(s, t):
        a, b = s.st(t); ss = s.ss / ZIN; ox, oy = s.rect[0], s.rect[1]
        (xj, yj), (xl, yl) = pre(168, 778), pre(160, 940)
        def fn(d):
            if a > 0: L.put_text(d, 'Justin', int(104 * ss), (xj - ox) * s.ss, (yj + 12 * (1 - a) - oy) * s.ss, glow=0.18, op=a)
            if b > 0:
                lay = d.copy(); L.grad_text(lay, 'Levine', int(184 * ss), (xl - ox) * s.ss, (yl - oy) * s.ss, glow=0.30)
                d[:] = d * (1 - b) + lay * b
        return mc_draw(s.tw, s.th, fn)


SH1_FACE = (987.9 + 232.0 / 2, 118.9 + 344.2 / 2)     # c_shep_1 f73 face centre (YuNet)
SH20_FACE = (1004.4 + 201.4 / 2, 122.6 + 298.9 / 2)   # c_shep_20 f0
K20 = 232.0 / 201.4
A20 = np.float32([[K20, 0, SH1_FACE[0] - K20 * SH20_FACE[0]], [0, K20, SH1_FACE[1] - K20 * SH20_FACE[1]]])
CUT_IN = 11.92                                         # take change hidden in the fastest, most blurred part of the truck


def justin_src(t):
    """Justin's own footage: Shepherd film c_shep_1 real time, then c_shep_20 (same set, face-matched) slowed to fill"""
    if t < CUT_IN:
        n = int(min(77, max(0, round((t - T0) * 30)))); return vid('c_shep_1').frame(n), matte('shep', n), None
    n = int(min(40, max(0, round((t - CUT_IN) / (T1 + 0.3 - CUT_IN) * 40))))
    m = np.asarray(Image.open(HERE + f'matte/s20_{n:05d}.png')).astype(np.float32) / 255
    return vid('c_shep_20').frame(n), m, A20


class Justin(Layer):
    SC = 0.90                                          # headroom like Jenny in the ref (hair ~150 px from the top)
    DX = 1250 - SH1_FACE[0] * SC; DY = H + 24 - H * SC # face right of centre; body runs off the bottom
    def __init__(s):
        super().__init__('justin', 1600.0, (s.DX, s.DY, s.DX + W * s.SC, s.DY + H * s.SC), P_REF0, ss=1 / s.SC)
    def key(s, t):
        return ('a', int(round((t - T0) * 30))) if t < CUT_IN else ('b', int(round((t - CUT_IN) / (T1 + 0.3 - CUT_IN) * 40)))
    def tex(s, t):
        img, a, A = justin_src(t)
        img = L.grade(img)
        if A is not None:
            img = cv2.warpAffine(img, A, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
            a = cv2.warpAffine(a, A, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        a[-4:] = a[-5:-4]                               # body runs off the bottom of frame: no outline along the crop
        co = S.cutout(img, a)
        def fn(d): J3.drop_shadow(d, co, 0, 0, 1.0, strength=0.55); J3.over(d, co, 0, 0)
        return mc_draw(s.tw, s.th, fn)


def type_mask(w, edges, n_full, frac):
    """letters 0..n_full-1 fully on, letter n_full at opacity frac (the newest letter fades in), the rest off"""
    m = np.zeros(w, np.float32)
    m[:int(edges[n_full])] = 1.0
    if n_full < len(edges) - 1: m[int(edges[n_full]):int(edges[n_full + 1])] = frac
    return m


class Headline(Layer):
    """lands on the right: small line 'co-founder and CEO of' over the hero 'Shepherd.' (cyan->blue) -- both TYPE ON letter
    by letter in place at the voice (Dime 'that's / Insane'), while the camera is still trucking towards them."""
    SMALL = [('co', 'co'), ('-founder', '-founder'), ('and', ' and'), ('CEO', ' CEO'), ('of', ' of')]
    def __init__(s):
        s.R, s.yS = pre(1786, 400); s.yB = pre(0, 612)[1]; s.pxS, s.pxB = 60 / ZIN, 236 / ZIN
        super().__init__('headline', 2850.0, (880, 250, 1824, 700), P_LAND, ss=1.2)
        ss = s.ss
        s.small = ''.join(v for _, v in s.SMALL); s.big = 'Shepherd.'
        fS = J3.font(int(s.pxS * ss)); fB = J3.font(int(s.pxB * ss))
        s.wS = J3.text_rgba(s.small, int(s.pxS * ss), hs=1.0)[0].shape[1]; s.wB = J3.text_rgba(s.big, int(s.pxB * ss), hs=1.0)[0].shape[1]
        s.xS = (s.R - s.rect[0]) * ss - s.wS; s.xB = (s.R - s.rect[0]) * ss - s.wB
        s.eS = [s.xS + J3.text_rgba(s.small[:i], int(s.pxS * ss), hs=1.0)[0].shape[1] if i else s.xS for i in range(len(s.small) + 1)]
        s.eB = [s.xB + J3.text_rgba(s.big[:i], int(s.pxB * ss), hs=1.0)[0].shape[1] if i else s.xB for i in range(len(s.big) + 1)]
        # letter times
        s.tS = []
        for key, txt in s.SMALL:
            t0 = WORDS_[key] - LEAD; nl = len(txt); dt = min(2.0, max(0.8, 6.0 / nl)) / FPS
            s.tS += [t0 + i * dt for i in range(nl)]
        t0 = WORDS_['Shepherd.'] - LEAD; s.tB = [t0 + i * 1.1 / FPS for i in range(len(s.big))]
        s.full = None
    def st(s, t):
        def one(ts):
            n = sum(1 for x in ts if t >= x + 1.0 / FPS); f = 0.0
            if n < len(ts) and t >= ts[n]: f = round(cl((t - ts[n]) * FPS) * 2) / 2
            return n, f
        return one(s.tS), one(s.tB)
    def key(s, t): return s.st(t)
    def tex(s, t):
        if s.full is None:
            ss = s.ss
            def fS(d): L.put_text(d, s.small, int(s.pxS * ss), (s.R - s.rect[0]) * ss, (s.yS - s.rect[1]) * ss, align='right', face='it', glow=0.18)
            def fB(d): L.grad_text(d, s.big, int(s.pxB * ss), (s.R - s.rect[0]) * ss, (s.yB - s.rect[1]) * ss, align='right', glow=0.32)
            s.full = (mc_draw(s.tw, s.th, fS), mc_draw(s.tw, s.th, fB))
        (nS, fS_), (nB, fB_) = s.st(t)
        M = np.ones((s.th, s.tw, 3), np.float32); C = np.zeros((s.th, s.tw, 3), np.float32)
        for (Mi, Ci), n, f, e in ((s.full[0], nS, fS_, s.eS), (s.full[1], nB, fB_, s.eB)):
            if n == 0 and f == 0: continue
            m = type_mask(s.tw, e, n, f)[None, :, None]
            M = M * (1 - m * (1 - Mi)); C = C * (1 - m * (1 - Mi)) + Ci * m
        return M, C


LAYERS = None
def layers():
    global LAYERS
    if LAYERS is None: LAYERS = [Ground(), Headline(), SignCard(), Caption(), Justin()]   # far -> near
    return LAYERS


def defocus(t):
    """focus pulls from Justin to the headline during the truck; aperture opens with it (ref: foreground lens blur ~10-15 px)"""
    e = EU(cl((t - TR0) / TR_DUR)); p = pose(t)
    zj, zh = 1600 - p['Z'], 2850 - p['Z']
    return 11.0 * e, zj + (zh - zj) * e


# ---------------------------------------------------------------- frame
ZT_OUT, ZT_AMT, ZT_IN, ZT_IN_AMT = 0.32, 0.24, 0.85, 0.07
def screen_X(t):
    z = 1.0
    u = cl((t - (T1 - ZT_OUT)) / ZT_OUT)
    if u > 0: z *= 1 + ZT_AMT * G2(u)
    z *= 1 + ZT_IN_AMT * G1(cl((t - T0) / ZT_IN))
    return zoom_about(z), (1 - EIO(u))


def sub_render(t, tf):
    p = pose(t); A, fstop = defocus(t); X, top = screen_X(t)
    out = None
    for ly in layers():
        Hm, zr = ly.H(p); Hm = np.vstack([X, [0, 0, 1]]) @ Hm
        r = ly.get(tf)
        sig = A * abs(1 - fstop / zr) if A > 0 else 0.0
        if ly.opaque:
            out = cv2.warpPerspective(r, Hm, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
            if sig > 0.4: out = cv2.GaussianBlur(out, (0, 0), sig)
            continue
        M, C = r
        if ly.name in ('caption', 'headline') and top < 1: M = 1 - top * (1 - M); C = C * top
        Mw = cv2.warpPerspective(M, Hm, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(1, 1, 1))
        Cw = cv2.warpPerspective(C, Hm, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
        if sig > 0.4: Mw = cv2.GaussianBlur(Mw, (0, 0), sig); Cw = cv2.GaussianBlur(Cw, (0, 0), sig)
        out = out * Mw + Cw
    return out


def probe_speed(t):
    h = 0.25 / FPS; ly = layers()
    pts = []
    for tt in (t - h, t + h):
        p = pose(tt); X, _ = screen_X(tt); q = []
        for l_ in (ly[1], ly[4], ly[2]):
            Hm, _ = l_.H(p); Hm = np.vstack([X, [0, 0, 1]]) @ Hm
            c = np.float32([[[0, 0]], [[l_.tw, l_.th]]]); q.append(cv2.perspectiveTransform(c, Hm).reshape(-1, 2))
        pts.append(np.concatenate(q))
    return float(np.abs(pts[0] - pts[1]).max())


def frame(t):
    J3.RNG_T[0] = t
    d = probe_speed(t); n = int(np.clip(math.ceil(d / 1.6), 1, 14))
    if n == 1: out = sub_render(t, t)
    else: out = sum(sub_render(t + (k / (n - 1) - 0.5) * 0.5 / FPS, t) for k in range(n)) / n
    return out, n, d


_R = None
def v1():
    """the trailer's own render.py (by path: the Kristina build on sys.path also has a render.py)"""
    global _R
    if _R is None:
        import importlib.util
        sp = importlib.util.spec_from_file_location('jl_render', '/Users/gourav/jl-trailer/trailer/render.py')
        _R = importlib.util.module_from_spec(sp); sp.loader.exec_module(_R)
    return _R


def hand_off(t, out):
    """3-frame dissolve with the neighbouring v1 shots at the two cuts (02a Nic before, 02d founded after)"""
    R = v1()
    for tc, other in ((T0, '02a_nic'), (T1, '02d_founded')):
        w = (t - (tc - 1.5 / FPS)) / (3 / FPS)
        if 0 < w < 1:
            i = [k for k, s_ in enumerate(R.SHOTS) if s_.name == other][0]
            o = R.shot_frame(i, t); w = EIO(w)
            out = o * (1 - w) + out * w if other == '02a_nic' else out * (1 - w) + o * w
    return out


def finished(t):
    if t >= T1 + 1.5 / FPS:                      # after the cut: the v1 02d shot itself
        return v1().frame(int(round(t * FPS))), 0, 0
    out, n, d = frame(t); out = hand_off(t, out)
    return fin16.finish(np.clip(J3.grain(out, 4.0, seed=int(t * FPS)), 0, 255), vig=0.60, tex=0.30, rb=0.35), n, d


if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        os.makedirs(HERE + 'stills', exist_ok=True)
        for a in sys.argv[2:]:
            t = float(a); img, n, d = finished(t)
            Image.fromarray(img).save(HERE + f'stills/s_{t:05.2f}.png'); print(f'{t:.2f}  sub-frames {n}  speed {d:.1f}px', flush=True)
    if sys.argv[1] == 'speed':
        prev = None
        for k in range(int(T0 * FPS), int(T1 * FPS)):
            t = k / FPS; d = probe_speed(t); print(f'{t:.3f} {d:7.2f}', '#' * int(d / 3))


def face_screen(t):
    """where Justin's face centre is on screen at t (for the layout check)"""
    ly = layers()[4]; p = pose(t); Hm, _ = ly.H(p); X, _ = screen_X(t); Hm = np.vstack([X, [0, 0, 1]]) @ Hm
    return cv2.perspectiveTransform(np.float32([[[SH1_FACE[0] * ly.ss * Justin.SC, SH1_FACE[1] * ly.ss * Justin.SC]]]), Hm).ravel()
