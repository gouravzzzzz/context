"""Justin Levine (Shepherd) trailer -- render engine (16:9, 1920x1080, 24 fps, Jennifer look, Twiml + Dime motion).

SMOOTHNESS RULES (Krish):
  * every move inside a shot runs on Krish's graph  EASE_USER = cubic-bezier(0.68, 0, 0.03, 1), 2-3 s long
  * keyframe overlapping: moves are stacked like nulls -- each next move starts at 50 % of the previous one, so the camera
    never parks between keys (chain()). The first move of a shot starts BEFORE the shot, so it is already travelling at the cut.
  * transitions: outgoing half on graph 2 cubic-bezier(1,0,1,1), incoming half on graph 1 cubic-bezier(0,0,0,1), fastest at
    the cut, hidden by a 3-frame dissolve; the camera keeps zooming IN across every cut (zoom-direction continuity)
  * real motion blur: each output frame averages sub-frames over a 180 deg shutter, the count follows the screen speed
TEXT: drawn in screen space (Trailer-1 / Jennifer type, shadows + glow), partially tracked to the camera, inside 90 % title safe.
Every draw op (over / screen / shadow) is affine per pixel, so each text item is cached as (M, C): out = frame * M + C.
"""
import sys, os, json, math
import numpy as np, cv2
from PIL import Image
sys.path.insert(0, '/Users/gourav/jl-trailer/storyboard'); sys.path.insert(0, '/Users/gourav/ks-kristina-build/trailer')
import jl_look as L
import jl_stills as S
import fin16
from jl_look import W, H, CX, CY, J, J3
J3.FPS = 24
FPS = 24
HERE = '/Users/gourav/jl-trailer/trailer/'
BRV = HERE + 'broll/'
EU, G1, G2, EIO = J3.EASE_USER, J3.EASE_G1_OUT, J3.EASE_G2_IN, J3.EASE_IO
cl = J3.clamp01

# v5 (Krish 2026-11-22): ONLY his three graphs for EVERY movement / fade / transition:
#   EU = cubic-bezier(0.68,0,0.03,1) S-curve,  G1 = cubic-bezier(0,0,0,1) fast start,  G2 = cubic-bezier(1,0,1,1) fast end.
# Any other curve a scene asks for (J3.bez(...), EASE_IO, cubic ease-outs) is mapped onto the graph with the same character.
_bez_raw = J3.bez
def _krish_bez(p1x, p1y, p2x, p2y):
    k = tuple(round(float(v), 3) for v in (p1x, p1y, p2x, p2y))
    if k == (0.68, 0.0, 0.03, 1.0): return EU
    if k == (0.0, 0.0, 0.0, 1.0): return G1
    if k == (1.0, 0.0, 1.0, 1.0): return G2
    f = _bez_raw(p1x, p1y, p2x, p2y)
    d0, d1 = f(0.03) / 0.03, (1 - f(0.97)) / 0.03          # start / end slope
    if d0 > 1.5 and d1 < 1.0: return G1                     # fast start, slow landing
    if d1 > 1.5 and d0 < 1.0: return G2                     # slow start, fast end
    return EU                                               # slow in, slow out
J3.bez = _krish_bez
J3.EASE_IO = EU
J3.EASE_OUT = G1
J3.EASE_OUT3 = G1
EIO = EU

SAFE = (96, 54, 1824, 1026)
CUT = '/Users/gourav/Downloads/Verticals_Justin_Levine_Trailer_Cut_v1.mp4'
WORDS = json.load(open(HERE + 'words_cut.json'))
SEGS = json.load(open(HERE + 'segs_cut.json'))
FACES = json.load(open(HERE + 'faces_cut.json'))
LEAD = 0.05                        # text lands a touch before the word


def wt(txt, after=0.0):
    return next(w[0] for w in WORDS if w[2] == txt and w[0] >= after - 1e-6)


# ---------------------------------------------------------------- footage readers
class Vid:
    def __init__(s, path, fps=30.0):
        s.path, s.fps, s.c, s.i, s.cache = path, fps, None, -1, {}
        c = cv2.VideoCapture(path); s.n = int(c.get(cv2.CAP_PROP_FRAME_COUNT)); c.release()
    def frame(s, i):
        i = int(max(0, min(s.n - 1, i)))
        if i in s.cache: return s.cache[i]
        if s.c is None: s.c = cv2.VideoCapture(s.path)
        if i != s.i + 1: s.c.set(cv2.CAP_PROP_POS_FRAMES, i)
        ok, f = s.c.read(); s.i = i
        if not ok: return s.cache.get(i - 1, np.zeros((H, W, 3), np.float32))
        f = cv2.cvtColor(f, cv2.COLOR_BGR2RGB).astype(np.float32)
        if f.shape[1] != W: f = cv2.resize(f, (W, H), interpolation=cv2.INTER_LANCZOS4)
        if len(s.cache) > 6: s.cache.pop(next(iter(s.cache)))
        s.cache[i] = f
        return f
    def at(s, u):
        return s.frame(int(round(u * s.fps)))


_V = {}
def vid(name, fps=30.0):
    if name not in _V: _V[name] = Vid(BRV + name + '.mp4', fps)
    return _V[name]


_CUTV = None
_GR = {}
def cut_frame(n, grade=True):
    """A-roll cut frame n (24 fps), exposed holds replaced by their slow-motion patch; graded and memoised"""
    global _CUTV
    k = (n, grade)
    if k in _GR: return _GR[k]
    p = HERE + f'patch/cut_{n:05d}.jpg'
    if os.path.exists(p): f = cv2.cvtColor(cv2.imread(p), cv2.COLOR_BGR2RGB).astype(np.float32)
    else:
        if _CUTV is None: _CUTV = Vid(CUT, 24.0)
        f = _CUTV.frame(n)
    f = L.grade(f) if grade else f
    if len(_GR) > 8: _GR.pop(next(iter(_GR)))
    _GR[k] = f
    return f


def seg_of(n):
    for g in SEGS:
        if round(g['t0'] * FPS) <= n < round(g['t0'] * FPS) + g['n'] + g['hold']: return g
    return SEGS[-1]


def spk_frame(n):
    """speaker frame with a 3-frame soft dissolve over jump cuts inside the same speaker (morph-cut feel)"""
    f = cut_frame(n)
    g = seg_of(n); n0 = round(g['t0'] * FPS)
    if g['k'] > 0 and SEGS[g['k'] - 1]['spk'] == g['spk'] and n - n0 < 3 and n0 - 1 >= 0:
        a = EIO((n - n0 + 1) / 4.0)
        f = cut_frame(n0 - 1) * (1 - a) + f * a
    return f


PATCH_MAP = {}                      # patched hold frame -> the real cut frame its slow-motion picture comes from
for _k in (4, 16, 26):
    _g = SEGS[_k]; _a = round(_g['t0'] * FPS) + _g['n'] - 8; _tot = 8 + _g['hold']
    for _j in range(_tot): PATCH_MAP[_a + _j] = _a + int(round(_j * 7 / (_tot - 1)))


_MT = {}
def matte(prefix, n):
    """person matte (plate space), temporally smoothed 1-2-1"""
    if prefix == 'cut': n = PATCH_MAP.get(n, n)
    k = (prefix, n)
    if k in _MT: return _MT[k]
    def one(i):
        p = HERE + f'matte/{prefix}_{i:05d}.png'
        return np.asarray(Image.open(p)).astype(np.float32) / 255 if os.path.exists(p) else None
    c = one(n)
    if c is None:
        for d in range(1, 40):
            c = one(n - d)
            if c is None: c = one(n + d)
            if c is not None: break
    a, b = one(n - 1), one(n + 1)
    if a is not None and b is not None: c = 0.5 * c + 0.25 * (a + b)
    if len(_MT) > 6: _MT.pop(next(iter(_MT)))
    _MT[k] = c
    return c


def face_track(n0, n1, sigma=10):
    """smoothed face centre per cut frame over [n0, n1)"""
    xs, ys = [], []
    for n in range(n0, n1):
        f = FACES[min(n, len(FACES) - 1)]
        if f is None: xs.append(np.nan); ys.append(np.nan)
        else: xs.append(f[0] + f[2] / 2); ys.append(f[1] + f[3] * 0.45)
    xs, ys = np.array(xs), np.array(ys)
    for a in (xs, ys):
        ok = ~np.isnan(a)
        a[~ok] = np.interp(np.flatnonzero(~ok), np.flatnonzero(ok), a[ok]) if ok.any() else CX
    from scipy.ndimage import median_filter, gaussian_filter1d
    xs = gaussian_filter1d(median_filter(xs, 9, mode='nearest'), sigma, mode='nearest')
    ys = gaussian_filter1d(median_filter(ys, 9, mode='nearest'), sigma, mode='nearest')
    return xs, ys


# ---------------------------------------------------------------- camera: overlapped eased moves (stacked nulls)
class Move:
    def __init__(s, t0, dur, dz=0.0, dx=0.0, dy=0.0, ease=EU):
        s.t0, s.dur, s.dz, s.dx, s.dy, s.e = t0, dur, dz, dx, dy, ease
    def at(s, t):
        e = s.e(cl((t - s.t0) / s.dur))
        return s.dz * e, s.dx * e, s.dy * e


def chain(t0, t1, dz, dur=3.0, pans=None, lead=0.5, step=0.2):
    """continuous push from t0 to t1, built from overlapped moves on Krish's graph (keyframe overlapping / stacked nulls).
    Each move lasts `dur`; the next one starts `step` (20 %) into the previous one -- with this steep S-curve a 50 % start
    makes the speed surge 7x every 1.4 s, 20 % keeps it within ~2x, so the push reads as one long glide.
    The first move starts lead*dur before t0 (already moving at the cut); the last ones are still travelling at t1."""
    st = dur * step; start = t0 - lead * dur
    n = max(1, int(math.ceil((t1 + 0.3 * dur - start - dur) / st)) + 1)
    pans = pans or [(0, 0)]
    k = step / 0.5                                            # pans were written per 50 %-overlap move
    return [Move(start + i * st, dur, dz / n, pans[i % len(pans)][0] * k, pans[i % len(pans)][1] * k) for i in range(n)]


def mat(z, ax, ay, px, py):
    return np.float32([[z, 0, px - ax * z], [0, z, py - ay * z]])


def compose(A, B):
    """A after B (2x3 affines)"""
    A3 = np.vstack([A, [0, 0, 1]]); B3 = np.vstack([B, [0, 0, 1]])
    return (A3 @ B3)[:2].astype(np.float32)


def zoom_about(z, cx=CX, cy=CY, dx=0.0, dy=0.0):
    return mat(z, cx, cy, cx + dx, cy + dy)


def warp(img, M, border=cv2.BORDER_REFLECT, flags=cv2.INTER_LINEAR):
    if np.allclose(M, [[1, 0, 0], [0, 1, 0]], atol=1e-4): return img
    return cv2.warpAffine(img, M, (W, H), flags=flags, borderMode=border)


# ---------------------------------------------------------------- layers: cached affine (M, C) items
class Item:
    """one drawable (text line, box, badge...). draw(d) paints it at full opacity onto a plate.
    t_on: fades in over fin; t_off: fades out over fout. anim(t)->quantised state for animated items (draw(d, a))."""
    def __init__(s, t_on, draw, t_off=None, fin=0.17, fout=0.22, behind=False, anim=None, track=None):
        s.t_on, s.draw, s.t_off, s.fin, s.fout, s.behind, s.anim, s.track = t_on, draw, t_off, fin, fout, behind, anim, track
        s.cache = {}
    def op(s, t):
        if t < s.t_on: return 0.0
        o = 1.0 if s.fin <= 0 else EIO(cl((t - s.t_on) / s.fin))
        if s.t_off is not None: o *= (1 - EIO(cl((t - s.t_off) / s.fout))) if s.fout > 0 else float(t < s.t_off)
        return o
    def mc(s, a=None):
        if a in s.cache: return s.cache[a]
        P0 = np.zeros((H, W, 3), np.float32); P1 = np.full((H, W, 3), 200.0, np.float32)
        if s.anim is None: s.draw(P0); s.draw(P1)
        else: s.draw(P0, a); s.draw(P1, a)
        M = (P1 - P0) / 200.0; C = P0
        act = (np.abs(M - 1).max(2) > 2e-3) | (C.max(2) > 0.3)
        ys, xs = np.where(act)
        if len(ys) == 0: r = None
        else:
            y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
            r = (x0, y0, np.ascontiguousarray(M[y0:y1, x0:x1]), np.ascontiguousarray(C[y0:y1, x0:x1]))
        if len(s.cache) > 40: s.cache.pop(next(iter(s.cache)))
        s.cache[a] = r
        return r
    def bbox(s, a=None):
        r = s.mc(a)
        if r is None: return None
        x0, y0, M, C = r
        return x0, y0, x0 + M.shape[1], y0 + M.shape[0]


def apply_item(out, r, op, T=None):
    """out = out * M' + C' with opacity op, through screen transform T (2x3) if given"""
    if r is None or op <= 0.002: return
    x0, y0, M, C = r
    if op < 0.999: M = 1 - op * (1 - M); C = C * op
    if T is None or np.allclose(T, [[1, 0, 0], [0, 1, 0]], atol=1e-4):
        h, w = M.shape[:2]
        xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
        if xb <= xa or yb <= ya: return
        sl = out[ya:yb, xa:xb]
        sl *= M[ya - y0:yb - y0, xa - x0:xb - x0]; sl += C[ya - y0:yb - y0, xa - x0:xb - x0]
        return
    h, w = M.shape[:2]
    pts = np.float32([[x0, y0], [x0 + w, y0], [x0, y0 + h], [x0 + w, y0 + h]])
    q = pts @ T[:, :2].T + T[:, 2]
    xa, ya = int(max(0, math.floor(q[:, 0].min()) - 2)), int(max(0, math.floor(q[:, 1].min()) - 2))
    xb, yb = int(min(W, math.ceil(q[:, 0].max()) + 2)), int(min(H, math.ceil(q[:, 1].max()) + 2))
    if xb <= xa or yb <= ya: return
    Tl = compose(np.float32([[1, 0, -xa], [0, 1, -ya]]), compose(T, np.float32([[1, 0, x0], [0, 1, y0]])))
    Mw = cv2.warpAffine(M, Tl, (xb - xa, yb - ya), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(1, 1, 1))
    Cw = cv2.warpAffine(C, Tl, (xb - xa, yb - ya), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
    sl = out[ya:yb, xa:xb]; sl *= Mw; sl += Cw


# ---------------------------------------------------------------- text helpers (Jennifer / Trailer-1 type)
def T_put(txt, px, x, y, align='left', face='reg', glow=0.18):
    return lambda d: L.put_text(d, txt, px, x, y, align=align, face=face, glow=glow)
def T_grad(txt, px, x, y, align='left', face='reg', glow=0.30):
    return lambda d: L.grad_text(d, txt, px, x, y, align=align, face=face, glow=glow)
def T_t1(lines, px, x, y, align='left', key=()):
    return lambda d: L.t1_lines(d, lines, x, y, px=px, align=align, key=key)


def side_shade_map(side, frac, edge):
    m = np.ones((H, W, 3), np.float32); L.side_shade(m, side, frac, edge); return m[:1]   # (1, W, 3)
def bottom_shade_map(depth, edge):
    m = np.ones((H, 1, 3), np.float32)
    y = np.arange(H, dtype=np.float32); u = np.clip((y - (H - depth)) / depth, 0, 1); u = u * u * (3 - 2 * u)
    m[:, 0, :] = (1 - (1 - edge) * u)[:, None]; return m
def top_shade_map(depth, edge):
    m = np.ones((H, 1, 3), np.float32)
    y = np.arange(H, dtype=np.float32); u = np.clip((depth - y) / depth, 0, 1); u = u * u * (3 - 2 * u)
    m[:, 0, :] = (1 - (1 - edge) * u)[:, None]; return m


_TECH, _TBG = {}, {}
def tech(seed, t, amount=0.8):
    """Jennifer black '01' tech ground (TechBG cached per seed) + the readout number row, per output frame"""
    n = int(round(t * FPS)); k = (seed, n, round(amount, 2))
    if k not in _TECH:
        if seed not in _TBG: _TBG[seed] = J3.TechBG(seed=seed)
        J3.RNG_T[0] = n / FPS
        d = _TBG[seed].render(n / FPS, amount=amount)
        J3.number_row(d, n / FPS, H - 30, x0=40, x1=W - 40, px=20, seed=seed)
        if len(_TECH) > 4: _TECH.pop(next(iter(_TECH)))
        _TECH[k] = d
    return _TECH[k].copy()
