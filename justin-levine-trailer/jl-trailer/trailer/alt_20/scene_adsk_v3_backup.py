"""ALT 19.55-21.88 'and then, together, to Autodesk.' -- copies the opening (first second) of Krish's pin
https://pin.it/27MYc2UDA (refs/pin_adsk): a thin white asterisk holds at the centre, folds into two arrows facing each other
(-> <-), the arrows split diagonally and a photo grows out between them (dot -> full in ~0.4 s, fast then settling), the
arrows riding its top-left / bottom-right corners.  Here: the photo is a real Autodesk office (Toronto, Wikimedia Commons),
on the RIGHT; big captions on the LEFT, built word by word like the Dime ref (fade + rise + blur clearing, 3 f; the hero
word types on letter by letter).  Footage plays normally; only camera moves are eased (Krish's graph, overlapped).
  python scene_adsk.py stills t1 t2 ...  |  python scene_adsk.py render out.mp4
"""
import sys, os, math, subprocess
import numpy as np, cv2
from PIL import Image
sys.path.insert(0, '/Users/gourav/jl-trailer/trailer')
from engine import *
HERE = '/Users/gourav/jl-trailer/trailer/alt_20/'
T0, T1 = 19.55, 21.88
FF = '/Users/gourav/ks-ron-build/reel1/ff'

# ---------------------------------------------------------------- layout
# the bridge (Krish): 02ef_card's blue 'to' carries over the cut, slides slightly right and becomes the white star
TO_V1 = (1408.0, 543.5)                             # 'to' centre on screen in the last 02ef_card frame (measured, n=469)
TO_MINE = (1390.0, 543.5)                           # centre of L.grad_text('to', 96, 1358, 575) unscaled
TO_S0 = 62.0 / 60.0                                 # v1 camera scale on it at the cut (62 px wide vs 60)
SLIDE = 50.0                                        # 'slightly towards the right'
PW, PH = 700, 744                                   # photo card (right), ref aspect ~0.96 -> 0.94
PCX, PCY = TO_V1[0] + SLIDE, TO_V1[1]               # the star (and the photo it reveals) end where the 'to' lands
PX0, PY0 = PCX - PW / 2, PCY - PH / 2
SC = PW / 537.0                                     # ref -> ours scale (ref photo 537 px wide on 720)
AST_R = 50 * SC                                     # asterisk half-length (ref ~100 px across)
LW = max(3, int(round(5 * SC * 0.8)))               # stroke

# ---------------------------------------------------------------- timing (ref seconds, 30 -> 24 fps by time)
SL_D = 0.50                                         # the 'to' slide (Krish's graph)
TM0 = T0 + 0.10                                     # the 'to' collapses into its centre while the star's spokes grow out
TA = T0 + 0.62                                      # star formed by ~T0+0.45, short hold, then the ref's fold (ref f16)
TF_ = 0.20                                          # fold into -> <- (ref f16-f21)
TS = TA + TF_                                       # arrows start splitting (ref f22)
TP = TS + 0.0                                       # photo starts growing as the arrows split (soft start)
TPD = 1.60                                          # Krish: smoother reveal, its keyframes stretched past the scene end
RV = J3.bez(0.30, 0.0, 0.02, 1.0)                   # half size at ~0.43 s, 70 % at 0.6 s, still easing out at the cut


def photo_u(t): return RV(cl((t - TP) / TPD))
def split_u(t): return EIO(cl((t - TS) / 0.10))
def slide_e(t): return EU(cl((t - T0) / SL_D))
def star_g(t): return 1 - (1 - cl((t - (TM0 + 0.06)) / 0.32)) ** 3          # spokes grow out of the 'to' (cubic out)
def to_k(t): return EIO(cl((t - TM0) / 0.26))                               # 'to' collapse 0 -> 1
def to_op(t): return 1 - EIO(cl((t - (TM0 + 0.08)) / 0.20))
TO_COL = np.float32([55, 185, 250])                                         # the 'to' gradient's middle


_IMG = None
def adsk_img():
    global _IMG
    if _IMG is None:
        im = np.asarray(Image.open('/Users/gourav/jl-trailer/assets/adsk/adsk_toronto.jpg').convert('RGB')).astype(np.float32)
        c = im[300:2400, 1250:3250]                     # logo in the upper third, windows + canopy below
        c = cv2.resize(c, (PW * 2, int(PW * 2 * c.shape[0] / c.shape[1])), interpolation=cv2.INTER_AREA)
        _IMG = L.grade(c)
    return _IMG


def photo_tex(t, w, h):
    """the Autodesk photo at card size w x h, slow inner push (eased), soft photo vignette"""
    im = adsk_img()
    c = L.fit(im, max(2, w), max(2, h), 0.56, 0.30, 1.04)       # no inner zoom: the picture sits still in its frame
    yy, xx = np.mgrid[0:c.shape[0], 0:c.shape[1]].astype(np.float32)
    r = np.sqrt(((xx / max(1, c.shape[1]) - 0.5) / 0.5) ** 2 + ((yy / max(1, c.shape[0]) - 0.5) / 0.5) ** 2)
    return c * (1 - 0.28 * np.clip(r - 0.55, 0, 1) ** 1.5)[..., None]


def strokes(t):
    """asterisk -> two arrows -> arrows on the photo corners; returns line segments [(x1,y1,x2,y2)] in screen px"""
    R = AST_R
    if t < TA:                                       # the asterisk, grown out of the sliding 'to'
        g = star_g(t); r = R * g
        if r < 0.5: return []
        cx = TO_V1[0] + SLIDE * slide_e(t); cy = TO_V1[1]; rot = 90 * (1 - g)
        segs = []
        for a in (0, 45, 90, 135):
            dx, dy = r * math.cos(math.radians(a + rot)), r * math.sin(math.radians(a + rot))
            segs.append((cx - dx, cy - dy, cx + dx, cy + dy))
        return segs
    u = EIO(cl((t - TA) / TF_))                     # fold
    s = split_u(t); pu = photo_u(t)
    # arrow tips: from the centre (gap opening) -> out to the photo's top-left / bottom-right corners
    gap = 6 * SC * u
    hw, hh = PW / 2 * pu, PH / 2 * pu
    pre = 14 * SC * s * (1 - pu)                     # the arrows lead the photo a little before it shows
    tl = (PCX - gap - hw - pre - 6 * SC * pu, PCY - hh - pre * 0.9)
    br = (PCX + gap + hw + pre + 6 * SC * pu, PCY + hh + pre * 0.9)
    shaft = R * (1.0 - 0.10 * u)                     # horizontal spoke halves become the shafts
    barb = R * (1.0 - 0.58 * u); ang = math.radians(45 - 5 * u)
    segs = [(tl[0] - shaft, tl[1], tl[0], tl[1]),                                  # ->  (tip at tl)
            (tl[0], tl[1], tl[0] - barb * math.cos(ang), tl[1] - barb * math.sin(ang)),
            (tl[0], tl[1], tl[0] - barb * math.cos(ang), tl[1] + barb * math.sin(ang)),
            (br[0] + shaft, br[1], br[0], br[1]),                                  # <-  (tip at br)
            (br[0], br[1], br[0] + barb * math.cos(ang), br[1] - barb * math.sin(ang)),
            (br[0], br[1], br[0] + barb * math.cos(ang), br[1] + barb * math.sin(ang))]
    rv = R * (1 - u)                                  # the vertical spoke shrinks away
    if rv > 0.5: segs.append((PCX, PCY - rv, PCX, PCY + rv))
    return segs


def draw_strokes(d, segs, col=250.0):
    if not segs: return
    ss = 3; x0 = int(max(0, min(min(a, c) for a, b, c, e in segs) - 20)); y0 = int(max(0, min(min(b, e) for a, b, c, e in segs) - 20))
    x1 = int(min(W, max(max(a, c) for a, b, c, e in segs) + 20)); y1 = int(min(H, max(max(b, e) for a, b, c, e in segs) + 20))
    if x1 <= x0 or y1 <= y0: return
    m = np.zeros(((y1 - y0) * ss, (x1 - x0) * ss), np.uint8)
    for a, b, c, e in segs:
        cv2.line(m, (int((a - x0) * ss), int((b - y0) * ss)), (int((c - x0) * ss), int((e - y0) * ss)), 255, LW * ss, cv2.LINE_AA)
    m = cv2.resize(m, (x1 - x0, y1 - y0), interpolation=cv2.INTER_AREA).astype(np.float32)[..., None] / 255
    reg = d[y0:y1, x0:x1]
    J3.glow_screen(d, np.repeat(m, 3, 2) * 255, 10, 0.25, x0, y0)
    reg = d[y0:y1, x0:x1]; reg[:] = reg * (1 - m) + np.asarray(col, np.float32) * m


# ---------------------------------------------------------------- captions (left, big): Dime word build
CAP_X = 180
LINES = [  # (words with their cut-timeline times, px, baseline, face, kind)
    ([(wt('and', 19.5), 'and'), (wt('then,', 19.6), 'then,')], 128, 400, 'reg', 'white'),
    ([(wt('together', 19.9), 'together,'), (wt('to', 20.3), 'to')], 128, 556, 'it', 'white'),
]
HERO = (wt('Autodesk.', 20.5), 'Autodesk.', 236, 800)


class WordItem(Item):
    """one word: fades 0->1 over 3 frames while rising 14 px and its blur clears (Dime word build), laid out in place"""
    def __init__(s, t_on, draw_at, t_off):
        super().__init__(t_on - 0.06, None, t_off=t_off, fin=3 / FPS, fout=0.22,
                         anim=lambda t, t_on=t_on: round(cl((t - (t_on - 0.06)) / (4 / FPS)) * 8) / 8)
        s.draw_at = draw_at
    def mc(s, a=None):
        if a in s.cache: return s.cache[a]
        e = G1(a); dy = 14 * (1 - e); sig = 3.5 * (1 - e)
        s.draw = lambda d, _a=None: s.draw_at(d, dy)
        P0 = np.zeros((H, W, 3), np.float32); P1 = np.full((H, W, 3), 200.0, np.float32)
        s.draw(P0); s.draw(P1)
        M = (P1 - P0) / 200.0; C = P0
        if sig > 0.4: M = cv2.GaussianBlur(M, (0, 0), sig); C = cv2.GaussianBlur(C, (0, 0), sig)
        act = (np.abs(M - 1).max(2) > 2e-3) | (C.max(2) > 0.3); ys, xs = np.where(act)
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        r = (x0, y0, np.ascontiguousarray(M[y0:y1, x0:x1]), np.ascontiguousarray(C[y0:y1, x0:x1]))
        s.cache[a] = r
        return r


class TypeItem(Item):
    """hero word typed on letter by letter (1 letter / frame, each letter fading over 2 f), gradient key word"""
    def __init__(s, t_on, word, px, x, base_y, t_off):
        s.word, s.px, s.x, s.base_y = word, px, x, base_y
        fnt = J3.font(px, 'reg')
        s.edges = [x + fnt.getlength(word[:k]) for k in range(len(word) + 1)]
        rate = 1.0 / FPS
        super().__init__(t_on - 0.04, None, t_off=t_off, fin=0.0, fout=0.22,
                         anim=lambda t: round(cl((t - (t_on - 0.04)) / rate / len(word)) * len(word) * 2) / 2)
        s.full = None
    def mc(s, a=None):
        if a in s.cache: return s.cache[a]
        if s.full is None:
            P0 = np.zeros((H, W, 3), np.float32); P1 = np.full((H, W, 3), 200.0, np.float32)
            for P in (P0, P1): L.grad_text(P, s.word, s.px, s.x, s.base_y, glow=0.32)
            s.full = ((P1 - P0) / 200.0, P0)
        M, C = s.full
        k = int(a); fr = a - k
        xr = np.arange(W, dtype=np.float32)
        e0 = s.edges[min(k, len(s.word))]; e1 = s.edges[min(k + 1, len(s.word))]
        mask = np.where(xr < e0, 1.0, np.where(xr < e1, fr, 0.0)).astype(np.float32)
        if k >= len(s.word): mask[:] = 1.0
        mask = cv2.GaussianBlur(mask[None, :], (0, 0), 6)[0] if k < len(s.word) else mask
        m3 = mask[None, :, None]
        Mm = 1 - m3 * (1 - M); Cm = C * m3
        act = (np.abs(Mm - 1).max(2) > 2e-3) | (Cm.max(2) > 0.3); ys, xs = np.where(act)
        if len(ys) == 0: r = None
        else:
            y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
            r = (x0, y0, np.ascontiguousarray(Mm[y0:y1, x0:x1]), np.ascontiguousarray(Cm[y0:y1, x0:x1]))
        s.cache[a] = r
        return r


def build_items():
    items = []
    for words, px, by, face, kind in LINES:
        xx = CAP_X; sp = J3.font(px, face).getlength(' ')
        for tw, w in words:
            wx = xx
            items.append(WordItem(tw, lambda d, dy, w=w, wx=wx, px=px, by=by, face=face: L.put_text(d, w, px, wx, by + dy, face=face, glow=0.22), None))
            xx += L.text_rgba(w, px, face, (255, 255, 255), 1.0)[0].shape[1] + sp
    th, word, px, by = HERO
    items.append(TypeItem(th, word, px, CAP_X - 6, by, None))
    return items


ITEMS = build_items()
MOVES = []                                          # Krish: no zoom after the reveal, everything sits still


_TO = None
def to_layer():
    """the 02ef_card 'to' (same T_grad: 96 px gradient, glow .30) as an (x0, y0, M, C) crop"""
    global _TO
    if _TO is None:
        P0 = np.zeros((H, W, 3), np.float32); P1 = np.full((H, W, 3), 200.0, np.float32)
        for P in (P0, P1): L.grad_text(P, 'to', 96, 1358, 575, glow=0.30)
        M = (P1 - P0) / 200.0; C = P0
        act = (np.abs(M - 1).max(2) > 2e-3) | (C.max(2) > 0.3); ys, xs = np.where(act)
        y0, y1, x0, x1 = max(0, ys.min() - 30), ys.max() + 31, max(0, xs.min() - 30), xs.max() + 31
        _TO = (x0, y0, np.ascontiguousarray(M[y0:y1, x0:x1]), np.ascontiguousarray(C[y0:y1, x0:x1]))
    return _TO


def draw_to(F, t):
    op = to_op(t)
    if op < 0.003: return
    x0, y0, M, C = to_layer(); k = to_k(t)
    s = TO_S0 * (1 - 0.72 * k)                                         # collapses into the star's centre
    cx, cy = TO_V1[0] + SLIDE * slide_e(t), TO_V1[1]
    A = np.float32([[s, 0, cx - s * (TO_MINE[0] - x0)], [0, s, cy - s * (TO_MINE[1] - y0)]])
    Mw = cv2.warpAffine(M, A, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(1, 1, 1))
    Cw = cv2.warpAffine(C, A, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
    sg = 4.0 * k
    if sg > 0.4: Mw = cv2.GaussianBlur(Mw, (0, 0), sg); Cw = cv2.GaussianBlur(Cw, (0, 0), sg)
    F[:] = F * (1 - op * (1 - Mw)) + op * Cw


def cam(t):
    dz = sum(m.at(t)[0] for m in MOVES)
    return zoom_about(math.exp(dz))


def xform(t):
    """no zoom-through (Krish): the scene opens on the ref's asterisk after a hard cut, and hard-cuts out"""
    return np.float32([[1, 0, 0], [0, 1, 0]]), 1.0


def plate(t, tf):
    d = tech(25, tf, 0.6)
    pu = photo_u(t)
    if pu > 0.004:
        w, h = max(2, int(round(PW * pu))), max(2, int(round(PH * pu)))
        x0, y0 = int(round(PCX - w / 2)), int(round(PCY - h / 2))
        c = photo_tex(t, w, h)
        sh = np.zeros((h, w, 4), np.float32); sh[..., 3] = 1
        J3.drop_shadow(d, sh, x0, y0, 1.0, strength=0.6 * pu)
        d[y0:y0 + h, x0:x0 + w] = c
    g = star_g(t) if t < TA else 1.0
    draw_strokes(d, strokes(t), TO_COL + (250.0 - TO_COL) * g)      # blue like the 'to' -> white as it becomes the star
    return d


def sub(t, tf):
    X, top = xform(t); A = compose(X, cam(t))
    F = warp(plate(t, tf), A)
    draw_to(F, t)
    for it in ITEMS:
        op = it.op(t) * top
        if op > 0.002: apply_item(F, it.mc(it.anim(t)), op, A)
    return F


def speed(t):
    h = 0.25 / FPS
    a = compose(xform(t - h)[0], cam(t - h)); b = compose(xform(t + h)[0], cam(t + h))
    pts = np.float32([[0, 0], [W, 0], [0, H], [W, H]])
    d = float(np.abs((pts @ a[:, :2].T + a[:, 2]) - (pts @ b[:, :2].T + b[:, 2])).max())
    grow = PW * abs(photo_u(t + h) - photo_u(t - h)) / 2 + 60 * abs(split_u(t + h) - split_u(t - h))
    grow += SLIDE * abs(slide_e(t + h) - slide_e(t - h)) + AST_R * abs(star_g(t + h) - star_g(t - h)) \
        + 30 * abs(to_k(t + h) - to_k(t - h))
    return d + grow


def frame_scene(t):
    J3.RNG_T[0] = t
    n = int(np.clip(math.ceil(speed(t) / 1.6), 1, 16))
    if n == 1: out = sub(t, t)
    else: out = sum(sub(t + (k / (n - 1) - 0.5) * 0.5 / FPS, t) for k in range(n)) / n
    return out


_R = None
def v1():
    global _R
    if _R is None:
        import importlib.util
        sp = importlib.util.spec_from_file_location('jl_render', '/Users/gourav/jl-trailer/trailer/render.py')
        _R = importlib.util.module_from_spec(sp); sp.loader.exec_module(_R)
        for sh in _R.SHOTS:
            if sh.name == '02ef_card': patch_bc(sh)
    return _R


# ---------------------------------------------------------------- 02ef_card end (Krish): the 4-line square closes back to the
# centre the way it opened (the card shrinks with it), the lines meet in a cross and disappear, then the cut ('to' carries over)
CL0, CL_D = 18.95, 0.45                             # close on Krish's graph
LF0, LF_D = 19.33, 0.18                             # the lines fade once they have met


def aa_grid(d, x0, y0, x1, y1, op, col=(205, 215, 225), th=2):
    lay = np.zeros((H, W), np.float32); S = 16
    for x in (x0, x1): cv2.line(lay, (int(round(x * S)), 0), (int(round(x * S)), (H - 1) * S), 1.0, th, cv2.LINE_AA, 4)
    for y in (y0, y1): cv2.line(lay, (0, int(round(y * S))), ((W - 1) * S, int(round(y * S))), 1.0, th, cv2.LINE_AA, 4)
    a = np.minimum(lay, 1.0)[..., None] * op
    d[:] = d * (1 - a) + np.array(col, np.float32) * a


def patch_bc(sh):
    plate0, key0 = sh.plate, sh.key
    full = {}
    def card_full(tf):
        if 'c' not in full:
            x0, y0, cw, ch = sh.rect
            lg = sh.content(tf)[0]
            c = np.empty((ch, cw, 3), np.float32); c[:] = lg[8:40, 8:40].reshape(-1, 3).mean(0)
            lh = int(cw * lg.shape[0] / lg.shape[1]); ly = (ch - lh) // 2
            c[ly:ly + lh] = cv2.resize(lg, (cw, lh), interpolation=cv2.INTER_AREA)
            full['c'] = c
        return full['c']
    def plate(ts, tf):
        e = EU(cl((ts - CL0) / CL_D))
        if e <= 0: return plate0(ts, tf)
        d = tech(sh.seed, tf, sh.amount); x0, y0, cw, ch = sh.rect
        cx, cy = x0 + cw / 2, y0 + ch / 2; k = 1 - e
        fade = 1 - EIO(cl((ts - LF0) / LF_D))
        if fade > 0.002: aa_grid(d, cx - cw * k / 2, cy - ch * k / 2, cx + cw * k / 2, cy + ch * k / 2, 0.42 * fade)
        if k > 0.004:
            w_, h_ = max(2, int(round(cw * k))), max(2, int(round(ch * k)))
            shd = np.zeros((h_, w_, 4), np.float32); shd[..., 3] = 1
            J3.drop_shadow(d, shd, cx - w_ / 2, cy - h_ / 2, 1.0, strength=0.55 * k)
            A = np.float32([[k, 0, cx - k * cw / 2], [0, k, cy - k * ch / 2]])
            c = cv2.warpAffine(card_full(tf), A, (W, H), flags=cv2.INTER_AREA if k < 0.5 else cv2.INTER_LINEAR)
            m = cv2.warpAffine(np.ones((ch, cw), np.float32), A, (W, H), flags=cv2.INTER_LINEAR)[..., None]
            d[:] = d * (1 - m) + c * m
        return d
    def key(ts, tf): return None if ts >= CL0 - 0.05 else key0(ts, tf)
    def speed(ts):
        u = (ts - CL0) / CL_D
        return 0.0 if u > 1.05 or u < -0.05 else 400 * (EU(cl(u + 0.02)) - EU(cl(u - 0.02))) / (0.04 * CL_D) / FPS
    sh.plate, sh.key, sh.speed = plate, key, speed


def finished(n):
    t = n / FPS; R = v1()
    for s_ in R.SHOTS:                                                          # hard cuts both sides, no zoom
        if s_.name == '02ef_card': s_.tout = 'cut'
        if s_.name in ('02g_autodesk', '02h_nic'): s_.tin = 'cut'
    if t < T0 or t >= T1: return R.frame(n)                                     # neighbouring v1 shots
    out = frame_scene(t)
    return fin16.finish(np.clip(J3.grain(out, 4.5, seed=n), 0, 255), vig=0.60, tex=0.35, rb=0.50)


A0, A1 = 18.6, 22.2
if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        os.makedirs(HERE + 'stills', exist_ok=True)
        for a in sys.argv[2:]:
            n = int(round(float(a) * FPS)); Image.fromarray(finished(n)).save(HERE + f'stills/s_{float(a):05.2f}.jpg', quality=92); print(a, flush=True)
    if sys.argv[1] == 'render':
        out = sys.argv[2]; n0, n1 = int(round(A0 * FPS)), int(round(A1 * FPS)); tmp = HERE + 'tmp.mp4'
        p = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                              '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', '-r', '24', tmp], stdin=subprocess.PIPE)
        import multiprocessing as mp
        with mp.get_context('fork').Pool(int(os.environ.get('NW', 8))) as pool:
            for img in pool.imap(finished, range(n0, n1), chunksize=3): p.stdin.write(np.ascontiguousarray(img).tobytes())
        p.stdin.close(); p.wait(); dur = (n1 - n0) / FPS
        subprocess.run([FF, '-v', 'error', '-y', '-i', tmp, '-ss', f'{A0:.4f}', '-t', f'{dur:.4f}', '-i', '/Users/gourav/jl-trailer/trailer/audio/mix.wav',
                        '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '320k', '-t', f'{dur:.4f}', '-movflags', '+faststart', out], check=True)
        os.remove(tmp); print('done', out, n1 - n0, 'frames', dur, 's')
