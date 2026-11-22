"""v2 seg 15 = NEW frames 1689-1846 (08c_cloud "...underestimated how big AI is." + 09_lloyds "And so I think underwriting
is another profession that is moving in that direction.").

Krish: the floating AI photo collage ARRANGES itself into the Pinterest carousel (pin.it/3jAdv9fF3, refs_cloud2/ref.mp4) and
cross-fades (opacity) into the underwriting B-roll, then the carousel moves exactly like the ref; captions on top.

Ref, read frame by frame (720x480, 60 fps):
  * billboard cards (aspect 0.74, round corners) on a vertical cylinder seen from D = 3R: theta = (k - p) * 60 deg,
    scale = 2 / (3 - cos theta), x = R sin theta * scale, R = 0.82 front-card widths, all on one centre line.
    -> front card 1.0, sides at theta 60 (scale 0.80, offset 0.57 W0), a new card emerges from behind at theta 90
       (scale 0.67), the leaving one slides behind the left card. z-order swaps at the fastest moment.
  * one step every 1.25 s (75 ref frames), cards travel LEFT, never park. Measured step curve = 22 % constant drift
    + 20 % short EU burst (u 0.40, 0.10 long) + 58 % long EU (u 0.10, 0.85 long) -- Krish's graph, fitted (max err 0.6 %).
  python scene15.py stills 1700 1740 ... | python scene15.py speed | python scene15.py render
"""
import sys, os, math, json, bisect, subprocess
import numpy as np, cv2
cv2.setNumThreads(1)
from PIL import Image
from scipy.special import erfc
sys.path.insert(0, '/Users/gourav/jl-trailer/trailer')
import engine
engine.PATCH_MAP.clear()
from engine import *
import shots as SH
from newtime import WORDS as WN
J = L.J

HERE = '/Users/gourav/jl-trailer/trailer/v2segs/seg15/'
FF = '/Users/gourav/ks-ron-build/reel1/ff'
OUT = '/Users/gourav/jl-trailer/trailer/v2segs/15_cloud_lloyds.mp4'
N0, N1 = 1689, 1846
def fr(n): return n / FPS
PURPLE = ((70, 185, 255), (165, 92, 255))                      # = render_v2.PURPLE (v3: Krish, "some captions a bit purple")
def wn(txt, near):
    return next(w[0] for w in WN if w[2] == txt and abs(w[0] * FPS - near) < 8)


# ================================================================ the ref's carousel
P_FIT = json.load(open(HERE + 'refcurve.json'))['p']            # a, b, u1, d1, u2, d2 (fitref.py)
def STEP(u):
    a, b, u1, d1, u2, d2 = P_FIT                                # v5: no linear drift, only Krish's graph (EU) steps
    b2 = b / (1 - a)
    return b2 * EU(cl((u - u1) / d1)) + (1 - b2) * EU(cl((u - u2) / d2))
_uu = np.linspace(0, 1, 2001); _vv = np.gradient([STEP(x) for x in _uu], _uu); U_PEAK = float(_uu[_vv.argmax()])
PERIOD = 1.25                                                   # ref: 75 frames @ 60 fps
STEP0 = fr(1759) - U_PEAK * PERIOD                              # swaps (fastest) on 1759 "And", 1789 "underwriting", 1819 "that"
def ring_p(t):
    u = (t - STEP0) / PERIOD
    if u < 0: return 0.0                                        # v5: no linear drift before the first step
    k = math.floor(u); return k + STEP(u - k)


W0, H0 = 533.0, 720.0                                           # front card (ref aspect 0.74; 67 % of frame height)
CYR = 488.0                                                     # carousel centre line (captions sit under it, on top)
RR = 0.82 * W0
def ring_rect(theta):
    th = math.radians(theta); s = 2.0 / (3.0 - math.cos(th))
    return CX + RR * math.sin(th) * s, CYR, W0 * s, H0 * s, (math.cos(th) + 1) / 2


# ================================================================ content
AI = {os.path.basename(c[0]).split('.')[0]: c for c in S.AI_CARDS}
_MIP = {}
def mips_of(key, loader):
    if key not in _MIP:
        im = loader(); m = [im]
        for _ in range(3): m.append(cv2.pyrDown(m[-1]))
        if len(_MIP) > 40: _MIP.pop(next(iter(_MIP)))
        _MIP[key] = m
    return _MIP[key]


def ai_layer(name):
    f, fx, fy, asp, z = AI[name]
    def load():
        im = L.grade(L.load(f)); s_ = 1600 / max(im.shape[:2])
        return cv2.resize(im, (int(im.shape[1] * s_), int(im.shape[0] * s_)), interpolation=cv2.INTER_AREA) if s_ < 1 else im
    return lambda tf: (mips_of(('ai', name), load), fx, fy, z)


UQ = json.load(open(HERE + 'unique.json'))
_RD = {}
def read_frame(clip, i):
    """EXACT frame i: sequential decode only (POS_FRAMES seeks land on wrong frames in these mp4s). Going back = reopen
    and read forward from 0. 1440x810 (cards never need more than 0.9x of it)."""
    st = _RD.get(clip)
    if st is None or i < st[1]:
        if st is not None: st[0].release()
        st = _RD[clip] = [cv2.VideoCapture(BRV + clip + '.mp4'), -1, None]
    c = st[0]
    if i == st[1] and st[2] is not None: return st[2]
    f = None
    while st[1] < i:
        ok, f = c.read()
        if not ok: break
        st[1] += 1
    if f is None: return st[2]
    st[2] = cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2RGB), (1440, 810), interpolation=cv2.INTER_AREA).astype(np.float32)
    return st[2]
def broll_layer(clip, n_start, fx, fy, z=1.0, i0=0):
    """normal speed from NEW frame n_start (held on its first frame before), unique source frames only"""
    keep = UQ[clip]['keep']
    def get(tf):
        u = max(0.0, tf - fr(n_start)); i = int(math.floor(u * 30 + 1e-6)) + i0
        idx = keep[max(0, bisect.bisect_right(keep, i) - 1)]
        return mips_of((clip, idx), lambda: L.grade(read_frame(clip, idx))), fx, fy, z
    return get


# ring members k = -2..3 come out of the collage as AI photos and cross-fade into the B-roll 09 needs
RING_AI = {-2: 'ceo_altman2019', -1: 'pichai_4', 0: 'zuck_1', 1: 'huang_0', 2: 'bmwr_15', 3: 'jl_msft_70p5'}
EXTRA_AI = ['amodei_1', 'ceo_murati', 'lisasu_ces', 'bmwr_28', 'axios_openai_70b', 'jl_oracle_44']
BROLL = {-3: broll_layer('c_osha_56', 1749, 0.42, 0.50),
         -2: broll_layer('c_osha_56', 1749, 0.42, 0.50),
         -1: broll_layer('c_osha_56', 1750, 0.42, 0.50),       # man on the phone over paperwork at his desk
         0: broll_layer('c_osha_166', 1752, 0.30, 0.50),       # pen on the forms
         1: broll_layer('c_intact_139', 1754, 0.49, 0.40, 1.12),   # Intact (insurer) exec -> Intact logo
         2: broll_layer('c_lloyds_97', 1756, 0.42, 0.55),      # the underwriting room -- front on "underwriting"
         3: broll_layer('c_bctt_15', 1784, 0.20, 0.50),        # "Now with detailed risk profiles" -- front on "that is moving"
         4: broll_layer('c_prog99_60', 1800, 0.45, 0.50),      # Progressive online
         5: broll_layer('c_intact_142', 1790, 0.55, 0.42, 1.12, i0=66),
         6: broll_layer('c_lloyds_97', 1800, 0.60, 0.55)}
XF0, XF_ST, XF_D = fr(1749), 2 / FPS, 0.42                      # opacity cross-fade AI -> B-roll, staggered by slot
def xfade(k, t): return EIO(cl((t - XF0 - XF_ST * (k + 2)) / XF_D))


# ================================================================ the collage (v1 08c_cloud wave 1, unchanged) + arrangement
T_IN = 70.3583                                                 # v1 08c_cloud start on the NEW timeline (cards leave the stream)
CL = SH.cluster(12, 12, 300, 140, 150, 300)                    # v1 wave 1: same seed, same places and sizes
CAM = chain(T_IN, 73.2933, 0.08, dur=3.0)                      # v1 shot camera (overlapped EU push) on the collage
def zc(t): return math.exp(sum(m.at(t)[0] for m in CAM))

_mem = sorted(range(len(CL)), key=lambda i: CL[i]['depth'])[-6:]           # the 6 nearest cards become the carousel
_mem = sorted(_mem, key=lambda i: CL[i]['x'] + CL[i]['w'] / 2)
CARDS = []
for k, i in zip(range(-2, 4), _mem): CARDS.append(dict(CL[i], k=k, ai=RING_AI[k], ring=True))
for j, i in enumerate([i for i in range(len(CL)) if i not in _mem]): CARDS.append(dict(CL[i], k=None, ai=EXTRA_AI[j], ring=False))
for c in CARDS: c['vk'] = CL.index(next(x for x in CL if x['x'] == c['x'] and x['y'] == c['y']))   # v1 stagger index
AR0, AR_ST, AR_D = fr(1716), 0.045, 1.45                       # arrange: EU flights, overlapped (next starts ~3 % in)
_order = sorted(CARDS, key=lambda c: (not c['ring'], abs(c['k']) if c['ring'] else c['depth']))
for j, c in enumerate(_order): c['ar0'] = AR0 + AR_ST * j


def collage_state(c, t):
    """v1 card_state: emerges from its stream slot (small, on the centre line) and flies to its place (G1)"""
    e = G1(cl((t - (T_IN + 0.035 * c['vk'])) / 0.65))
    w = 40 + (c['w'] - 40) * e; h = 30 + (c['h'] - 30) * e
    x = c['sx'] + (c['x'] + c['w'] / 2 - c['sx']) * e; y = CY + (c['y'] + c['h'] / 2 - CY) * e
    z = zc(t)
    return e, CX + (x - CX) * z, CY + (y - CY) * z, w * z, h * z


def layout(t):
    """every card at time t: (depth, cx, cy, w, h, op, layers=[(get, weight)], key)"""
    p = ring_p(t); out = []
    for c in CARDS:
        e0, x0, y0, w0, h0 = collage_state(c, t)
        if e0 <= 0.01: continue
        a = EU(cl((t - c['ar0']) / AR_D))
        if c['ring']:
            th = (c['k'] - p) * 60
            if a >= 0.999 and abs(th) > 165: continue              # gone round the back: never wrap onto a later card's slot
            x1, y1, w1, h1, d1 = ring_rect(th)
            op = 1.0
        else:
            x1, y1, w1, h1, _ = ring_rect(180); d1 = -0.2
            op = 1 - EIO(cl((a - 0.25) / 0.6))
        if op <= 0.003: continue
        x, y, w, h = x0 + (x1 - x0) * a, y0 + (y1 - y0) * a, w0 + (w1 - w0) * a, h0 + (h1 - h0) * a
        dep = c['depth'] * (1 - a) + d1 * a
        xf = xfade(c['k'], t) if c['ring'] else 0.0
        lay = [(ai_layer(c['ai']), 1 - xf)] + ([(BROLL[c['k']], xf)] if xf > 0.001 else [])
        out.append((dep, x, y, w, h, op, lay, ('c', c['ai'])))
    for k in (4, 5, 6):                                        # pure carousel cards (enter from behind later)
        th = (k - p) * 60
        if abs(th) > 165: continue
        x, y, w, h, d = ring_rect(th)
        out.append((d, x, y, w, h, 1.0, [(BROLL[k], 1.0)], ('r', k)))
    return sorted(out, key=lambda r: r[0])


# ================================================================ drawing
def sdf_rr(xs, ys, cx, cy, hw, hh, r):
    qx = np.abs(xs - cx)[None, :] - (hw - r); qy = np.abs(ys - cy)[:, None] - (hh - r)
    return np.hypot(np.maximum(qx, 0), np.maximum(qy, 0)) + np.minimum(np.maximum(qx, qy), 0) - r


def fitwarp(mips, fx, fy, z, x, y, w, h, size):
    lvl = 0; img = mips[0]; ih, iw = img.shape[:2]; s = max(w / iw, h / ih) * z
    while s < 0.5 and lvl + 1 < len(mips):
        lvl += 1; img = mips[lvl]; ih, iw = img.shape[:2]; s = max(w / iw, h / ih) * z
    cw, ch = w / s, h / s
    sx0 = min(max(fx * iw - cw / 2, 0), iw - cw); sy0 = min(max(fy * ih - ch / 2, 0), ih - ch)
    M = np.float32([[s, 0, x - sx0 * s], [0, s, y - sy0 * s]])
    return cv2.warpAffine(img, M, size, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def draw_card(dst, tf, cx, cy, w, h, op, layers):
    x, y = cx - w / 2, cy - h / 2
    sig = max(3.0, h * 0.07); ox, oy = max(2.0, h * 0.03), max(3.0, h * 0.05); r = max(2.0, 0.028 * w)
    X0, Y0 = max(0, int(x - 3 * sig)), max(0, int(y - 3 * sig))
    X1, Y1 = min(W, int(x + w + ox + 3 * sig) + 2), min(H, int(y + h + oy + 3 * sig) + 2)
    if X1 <= X0 or Y1 <= Y0: return
    xs = np.arange(X0, X1, dtype=np.float32) + 0.5; ys = np.arange(Y0, Y1, dtype=np.float32) + 0.5
    q = 4.0                                                         # soft shadow: solved on a 1/4 grid, upsampled
    xq = X0 + (np.arange(int(math.ceil((X1 - X0) / q)), dtype=np.float32) + 0.5) * q
    yq = Y0 + (np.arange(int(math.ceil((Y1 - Y0) / q)), dtype=np.float32) + 0.5) * q
    shq = (0.55 * 0.5 * erfc(sdf_rr(xq, yq, cx + ox, cy + oy, w / 2, h / 2, r) / (sig * 1.4142))).astype(np.float32)
    sh = cv2.resize(shq, (len(xq) * 4, len(yq) * 4), interpolation=cv2.INTER_LINEAR)[:Y1 - Y0, :X1 - X0]
    roi = dst[Y0:Y1, X0:X1]; roi *= (1 - op * sh)[..., None]
    bx0, by0 = max(0, int(math.floor(x)) - 1), max(0, int(math.floor(y)) - 1)
    bx1, by1 = min(W, int(math.ceil(x + w)) + 1), min(H, int(math.ceil(y + h)) + 1)
    if bx1 <= bx0 or by1 <= by0: return
    a = np.clip(0.5 - sdf_rr(xs[bx0 - X0:bx1 - X0], ys[by0 - Y0:by1 - Y0], cx, cy, w / 2, h / 2, r), 0, 1).astype(np.float32) * op
    patch = None
    for get, wt_ in layers:
        if wt_ <= 0.001: continue
        mips, fx, fy, z = get(tf)
        pc = fitwarp(mips, fx, fy, z, x - bx0, y - by0, w, h, (bx1 - bx0, by1 - by0)) * wt_
        patch = pc if patch is None else patch + pc
    reg = dst[by0:by1, bx0:bx1]; a3 = a[..., None]
    reg[:] = reg * (1 - a3) + patch * a3


_TH = {}
def stream(d, t, op):
    """v1: the thin stream of tiny thumbnails sliding left on the centre line (fades as the cards arrange)"""
    if op <= 0.003: return
    off = (t - T_IN) * 140.0; pitch = 49; k0 = int(off // pitch)
    for j in range(-1, W // pitch + 2):
        x = j * pitch - (off - k0 * pitch) + 30
        if x < 20 or x > W - 60: continue
        idx = ((j + k0) * 7) % len(S.AI_CARDS)
        if idx not in _TH:
            f, fx, fy, asp, z = S.AI_CARDS[idx]; _TH[idx] = L.fit(SH.cimg(f), 40, 30, fx, fy, z) * 0.82
        xi = int(round(x)); reg = d[CY - 15:CY + 15, xi:xi + 40]
        reg[:] = reg * (1 - op) + _TH[idx] * op
def stream_op(t): return 1 - EIO(cl((t - fr(1716)) / 0.75))


def cards_at(d, ts, tf):
    stream(d, ts, stream_op(ts))
    for dep, x, y, w, h, op, lay, key in layout(ts): draw_card(d, tf, x, y, w, h, op, lay)


def disp(t0, t1):
    A = {r[7]: r for r in layout(t0)}; B = {r[7]: r for r in layout(t1)}; m = 0.0
    for k in A.keys() & B.keys():
        a, b = A[k], B[k]
        m = max(m, abs(a[1] - b[1]) + abs(a[3] - b[3]) / 2, abs(a[2] - b[2]) + abs(a[4] - b[4]) / 2)
    return m


# ================================================================ captions (screen space, on top): per word, hero words typed
FIN = 3.5 / FPS
def rise_anim(t_on): return lambda t: round(cl((t - t_on) / FIN) * 8) / 8


def word_items(words, px, x, y, align='center', t_off=None, faces=None, glow=0.18):
    faces = faces or {}; sp = J3.font(px).getlength(' ') * 0.95; xx = 0.0; lay = []
    for tw, w in words:
        rg, asc = J3.text_rgba(w, px, face=faces.get(w, 'reg'), hs=1.0); lay.append((tw, rg, asc, xx)); xx += rg.shape[1] + sp
    lw = xx - sp; x0 = x if align == 'left' else (x - lw if align == 'right' else x - lw / 2)
    its = []
    for tw, rg, asc, xo in lay:
        def draw(d, a, rg=rg, asc=asc, xo=xo):
            e = EIO(a); J3._put_word(d, rg, asc, x0 + xo, y + 13 * (1 - e), (1.0, 8 * (1 - e), 0, 0), True, glow)
        its.append(Item(tw - LEAD, draw, t_off=t_off, fin=FIN, fout=0.17, anim=rise_anim(tw - LEAD)))
    return its


def lay_line(parts, px, x, align='center'):
    """[(word, kind)] -> x of each word, laid once on the final line width"""
    sp = J3.font(px).getlength(' ') * 0.95; xx = 0.0; xs = []
    for w, kind in parts:
        rg, asc = J3.text_rgba(w, px, hs=1.0); xs.append(xx); xx += rg.shape[1] + sp
    lw = xx - sp; x0 = x if align == 'left' else (x - lw if align == 'right' else x - lw / 2)
    return [x0 + v for v in xs]


def typed_anim(t_on, n, rate):
    return lambda t: (int(min(n, max(0, math.floor((t - t_on) * FPS / rate) + 1))), round(cl((t - t_on) / FIN) * 8) / 8)


def box_word(t_on, word, px, x0, by, rate, t_off=None, box=None):
    """key word on the blue gradient box (Trailer-1 type), letters typed on inside it; box=(c0, c1) -> left-to-right gradient"""
    rgf, _ = J3.text_rgba(word, px, hs=1.0)
    bx0, bx1 = int(x0 - px * 0.10), int(x0 + rgf.shape[1] + px * 0.10); by0, by1 = int(by - px * 0.80), int(by + px * 0.24)
    GB = L.gbox(bx1 - bx0, by1 - by0) if box is None else J3.grad(bx1 - bx0, by1 - by0, box[0], box[1], diag=False)
    def draw(d, a):
        n, q = a; dy = int(round(13 * (1 - EIO(q))))
        bs = np.zeros((by1 - by0, bx1 - bx0, 4), np.float32); bs[..., 3] = 1
        J3.drop_shadow(d, bs, bx0, by0 + dy, 1.0, strength=0.45)
        J3.glow_screen(d, GB, 16, 0.16, bx0, by0 + dy)
        d[by0 + dy:by1 + dy, bx0:bx1] = GB
        if n > 0:
            rg, asc = J3.text_rgba(word[:n], px, hs=1.0); J3._put_word(d, rg, asc, x0, by + dy, (1.0, 0, 0, 0), True, 0.10)
    return Item(t_on, draw, t_off=t_off, fin=FIN, fout=0.17, anim=typed_anim(t_on, len(word), rate))


def grad_word(t_on, word, px, xc, by, rate, t_off=None, c0=(70, 255, 236), c1=(40, 120, 255)):
    """hero word: gradient fill (cyan -> blue default), typed on letter by letter, gradient fixed to the full word"""
    rgf, asc = J3.text_rgba(word, px, hs=1.0); x0 = xc - rgf.shape[1] / 2
    G = J.grad(rgf.shape[1], rgf.shape[0], c0, c1) / 255
    def draw(d, a):
        n, q = a
        if n <= 0: return
        dy = 13 * (1 - EIO(q)); rg, asc2 = J3.text_rgba(word[:n], px, hs=1.0)
        lay = rg.copy(); lay[..., :3] = G[:rg.shape[0], :rg.shape[1]] * rg[..., 3:4]
        yy = by + dy - asc2
        J3.drop_shadow(d, lay, x0, yy, 1.0, strength=0.75)
        J3.glow_screen(d, lay[..., :3] * 255, 18, 0.30, x0, yy)
        J3.over(d, lay, x0, yy)
    return Item(t_on, draw, t_off=t_off, fin=FIN, fout=0.17, anim=typed_anim(t_on, len(word), rate))


def captions():
    its = []
    # 08c: "underestimated" (boxed, typed) -> "how big AI is." (AI boxed, typed) -- v1 type, centred under the cards
    BY, PX = 965, 104
    tu = wn('underestimated', 1690)
    x0 = lay_line([('underestimated', 'k')], PX, CX)[0]
    its.append(box_word(tu - LEAD, 'underestimated', PX, x0, BY, 1.15, t_off=fr(1723), box=PURPLE))   # v3: blue -> purple box
    xs = lay_line([('how', ''), ('big', ''), ('AI', 'k'), ('is.', '')], PX, CX)
    toff = fr(1756)
    for (w, n), x in zip([('how', 1729), ('big', 1734), ('is.', 1754)], [xs[0], xs[1], xs[3]]):
        its += word_items([(wn(w, n), w)], PX, x, BY, align='left', t_off=toff)
    its.append(box_word(wn('AI', 1740) - LEAD, 'AI', PX, xs[2], BY, 1.5, t_off=toff))
    # 09: "And so I think" -> "underwriting" (hero, typed) over "is another profession" -> "moving in that direction."
    its += word_items([(wn(w, n), w) for w, n in [('And', 1764), ('so', 1767), ('I', 1772), ('think', 1774)]], 66, CX, 958,
                      t_off=fr(1784))
    its.append(grad_word(wn('underwriting', 1788) - LEAD, 'underwriting', 116, CX, 925, 0.72))
    its += word_items([(wn(w, n), w) for w, n in [('is', 1798), ('another', 1801), ('profession', 1806)]], 60, CX, 1005,
                      t_off=fr(1817), faces={'profession': 'it'})
    its += word_items([(wn(w, n), w) for w, n in [('moving', 1823), ('in', 1829), ('that', 1831), ('direction.', 1834)]], 60, CX, 1005)
    return its
CAPS = captions()


# ================================================================ frame
def raw(n):
    t = n / FPS; J3.RNG_T[0] = t
    bg = tech(37, t, 0.55)
    h = 0.25 / FPS
    ns = int(np.clip(math.ceil(disp(t - h, t + h) / 2.0), 1, 12))
    if stream_op(t) > 0.01: ns = max(ns, 3)
    acc = None
    for k in range(ns):
        ts = t + ((k / (ns - 1) - 0.5) * 0.5 / FPS if ns > 1 else 0.0)        # 180-degree shutter
        d = bg.copy(); cards_at(d, ts, t)
        acc = d if acc is None else acc + d
    out = acc / ns
    for it in CAPS:
        op = it.op(t)
        if op > 0.002: apply_item(out, it.mc(it.anim(t) if it.anim else None), op)
    return out


def finished(n):
    out = raw(n)
    return fin16.finish(np.clip(J3.grain(out, 4.5, seed=n), 0, 255), vig=0.60, tex=0.35, rb=0.50)


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'stills':
        os.makedirs(HERE + 'stills', exist_ok=True)
        for a in sys.argv[2:]:
            n = int(a); Image.fromarray(finished(n)).save(HERE + f'stills/s_{n}.jpg', quality=90); print(n, flush=True)
    elif mode == 'speed':
        prev = None
        for n in range(N0, N1):
            d = disp(fr(n), fr(n + 1)); print(n, round(d, 1), round(ring_p(fr(n)), 3))
    elif mode == 'render':
        tmp = HERE + 'tmp15.mp4'
        p = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', '24', OUT], stdin=subprocess.PIPE)
        import multiprocessing as mp
        with mp.get_context('fork').Pool(int(os.environ.get('NW', 3))) as pool:
            for i, img in enumerate(pool.imap(finished, range(N0, N1), chunksize=2)):
                p.stdin.write(np.ascontiguousarray(img).tobytes())
                if i % 10 == 0: print('frame', N0 + i, flush=True)
        p.stdin.close(); p.wait()
        dur = (N1 - N0) / FPS
        subprocess.run([FF, '-v', 'error', '-y', '-i', OUT, '-ss', f'{N0 / FPS:.6f}', '-t', f'{dur:.6f}', '-i',
                        '/Users/gourav/jl-trailer/trailer/audio/mix2.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac',
                        '-b:a', '320k', '-t', f'{dur:.6f}', OUT.replace('.mp4', '_check.mp4')], check=True)
        print('done', OUT, N1 - N0, 'frames')
