"""Trailer v3 segment 11b -- NEW 1255-1410 (155 frames): 06b rebuilt with clean real-speed footage -> hand-off into the pin
animation (pin.it/RyU5xmNfN, first second) starting FROM 06b's footage box -> pixel overlay into Justin (07a) at 1392.
  * 1255-1342  06b (v1 code: tech ground, box (802,290,925,521), v1 camera + captions); footage = clean OSHA, real time
  * 1343-1391  pin first second: the box is the pin's main card; footage cross-fades (opacity, 6 f) to the next shot, the 06b
               captions fade out (3 f) as the camera starts. Camera = the pin's measured zoom-out (main-card width curve f3-f25,
               then the same velocity decaying, tau 0.3 s) + its camera roll (pitch lines rotate with the card) + its small drift
               down; satellite cards slide in at the pin's frames (top-left from above at f19, bottom-right from below at f21, G1)
               to the pin's positions relative to the main card. "It's somewhat" / "manufactured." are children of the main
               card (same transform), per-word fade+rise+blur / type-on, re-timed to the NEW words.
  * 1385-1398  pixel overlay (jennifer render3 pixel_overlay, 14 f centred on the 1392 cut), then Justin v1 plates.
  python scene11b.py stills n ..  |  speed  |  render
"""
import sys, os, math, json, subprocess
import numpy as np, cv2
from PIL import Image
sys.path.insert(0, '/Users/gourav/jl-trailer/trailer')
import render_v2 as RV
from engine import *                                   # W, H, CX, CY, L, J3, EU, G1, G2, EIO, cl, vid, tech, fin16, LEAD, FPS, compose, apply_item
from newtime import WORDS as WN

HERE = '/Users/gourav/jl-trailer/trailer/seg11b/'
OUTD = '/Users/gourav/jl-trailer/trailer/v2segs/'
FF = '/Users/gourav/ks-ron-build/reel1/ff'
N0, NH, NC, N1 = 1255, 1343, 1392, 1410               # segment, hand-off, 07a cut, end
TH = NH / FPS
PURPLE = RV.PURPLE
R = RV.v1()
I6B = [i for i, s in enumerate(R.SHOTS) if s.name == '06b_osha'][0]
SH = R.SHOTS[I6B]
BOX = (802, 290, 925, 521)                             # v1 06b footage box (x0, y0, w, h)
SRC = json.load(open(HERE + 'sources.json'))


def wn(w, a=0.0): return next(x[0] for x in WN if x[2] == w and x[0] >= a)


# ---------------------------------------------------------------- footage: real time, unique frames only
class Foot:
    """a source sequence (clip, frame) list at 30 fps; at elapsed e shows the unique frame whose original timestamp is the
    latest <= e (real speed: no speed-up, no slow-down, no interpolation)"""
    def __init__(s, name, n_start, fx=0.5, fy=0.5, zoom=1.0):
        d = SRC[name]; s.seq, s.crop, s.uniq = d['seq'], d['crop'], d['uniq']; s.n_start = n_start
        s.fx, s.fy, s.zoom = fx, fy, zoom
    def index(s, n):
        """unique frame j plays at its own content time j / fps_c (fps_c = 30 for dup-free sources, 25 for the 25 fps tile
        inside the 30 fps capture): real speed, never a repeated frame"""
        fps_c = 25.0 if len(s.uniq) < 0.9 * len(s.seq) else 30.0
        e = max(0.0, (n - s.n_start) / FPS); j = int(math.floor(e * fps_c + 1e-6))
        return s.uniq[min(len(s.uniq) - 1, j)]
    def img(s, n):
        c, i = s.seq[min(len(s.seq) - 1, s.index(n))]
        f = vid(c).frame(i)
        if s.crop: x0, y0, x1, y1 = s.crop; f = np.ascontiguousarray(f[y0:y1, x0:x1])
        return L.grade(f)


# 06b box parts (NEW frames): handshake -> checklist -> excavator on the job site; the main card after the hand-off = c_osha_96
F_HS = Foot('hs', N0, 0.42, 0.40, 1.20)                 # 'And I knew when' (one clean clip before the inspection)
F_226 = Foot('i226', 1271, 0.42, 0.40, 1.20)            # Krish's footage: tank-site inspection (grey fleece + tablet, valve)
F_230 = Foot('i230', 1315, 0.42, 0.40, 1.20)            # same shot later, from 'inspect' through the hand-off (becomes the pin card)
F_EXC = F_230                                           # the footage in the box when it becomes the pin card
F_WH = Foot('wh', NH, 0.62, 0.32, 1.40)
CUT_A, CUT_B = 1271, 1315                               # 'when' | 'the insurance company was coming to' | 'inspect the job site'
XF = 6                                                  # footage cross-fade frames at the hand-off


def box_foot(n):
    if n < CUT_A: return F_HS
    if n < CUT_B: return F_226
    return F_230


# ---------------------------------------------------------------- 06b (v1 code, footage swapped)
_CUR = [N0]
def _content(tf):
    f = box_foot(_CUR[0]); return f.img(_CUR[0]), f.fx, f.fy, f.zoom
SH.content = _content


def frame_06b(n):
    _CUR[0] = n
    return RV.frame('v1', n).astype(np.float32)


# ---------------------------------------------------------------- the pin's measured motion (736x414 @ 25 fps)
# hand-off = pin f13: the pin's card has just finished unrolling and fills 51 % of the frame width = our 06b box (51 %)
PIN_W = [375.4, 368.2, 360.0, 352.0, 344.8, 336.0, 327.7, 319.5, 311.3, 302.9, 295.0, 287.0, 279.6]   # main card width f13..f25
PIN_A = [-0.81, -0.54, -0.17, 0.0, 0.39, 0.64, 0.87, 1.10, 1.37, 1.46, 1.66, 1.74, 1.91]              # its angle = camera roll
_fp = np.arange(len(PIN_W)) / 25.0
_PW = np.polyfit(_fp, np.array(PIN_W) / PIN_W[0], 2)                                 # smooth fits (measurement noise out)
_PA = np.polyfit(_fp, np.array(PIN_A) - PIN_A[0], 2)
T25 = _fp[-1]; TAU_S, TAU_A = 0.25, 0.10                # after f25 the same velocity decays ...
CREEP = 0.045                                           # ... into a slow creep (camera never parks)
ROLL_K = 1.91 / 2.72                                    # roll ends at the pin's own end angle (+1.9 deg); we start straight
def _tail(p, t, tau):
    v = np.polyval(np.polyder(p), T25); return np.polyval(p, T25) + v * tau * (1 - math.exp(-(t - T25) / tau))
ZK = 1.38                                               # Krish v3b: 'zoom out more' -> the pin's curve shape, amount x1.38
def S_pin(t):
    e = t - TH
    if e <= 0: return 1.0
    s0 = float(np.polyval(_PW, e)) if e <= T25 else float(_tail(_PW, e, TAU_S)) - CREEP * (e - T25)
    return 1 - ZK * (1 - s0)
# v5 (Krish: only his graphs): the same zoom-out, same end size at the 07a cut, on graph 1 (fast start, long settle),
# still creeping 0.25 s past the cut so the camera never parks
_SD = (NC - NH) / FPS + 0.25
_SA = (1 - S_pin(NC / FPS)) / G1(((NC - NH) / FPS) / _SD)
def S_(t):
    e = t - TH
    if e <= 0: return 1.0
    return 1 - _SA * G1(cl(e / _SD))
def roll_(t):
    e = t - TH
    if e <= 0: return 0.0
    return 0.0                                          # Krish v3c: 'get this straight' -> no roll / tilt at all
def dy_(t): return DYK * (1 - S_(t))                  # pin: main card drifts down (+2.9 % of H by f25) -> wall centred
DYK = 40.0


def t_old(t): return SH.t1 + (t - 55.9783)             # v1 06b camera keeps running past its end (linear in time)


def v1cam(t): return R.full_cam(SH, t_old(t))[0]
def v1txt(t): return R.full_cam(SH, t_old(t))[1]


T_CENTRE = 1360 / FPS                                   # main card (and its text) reaches x = 960 here, smoothly
def pan_f(t):
    """1 at the hand-off (box where 06b left it) -> 0 at T_CENTRE, on the zoom's own curve, squared = no velocity kink"""
    S, Sc = S_(t), S_(T_CENTRE)
    return 1.0 if t <= TH else (max(0.0, (S - Sc) / (1 - Sc)) ** 2)


def zcam(t):
    """pin camera on top of the v1 camera: zoom-out about the frame centre + drift; pan that centres the main card"""
    s = S_(t); V = v1cam(t)
    xm = V[0, 0] * (x0 + cw / 2) + V[0, 2]                 # main card centre after the v1 camera
    dx = -(1 - pan_f(t)) * s * (xm - CX)
    return np.float32([[s, 0, CX - s * CX + dx], [0, s, CY - s * CY + dy_(t)]])


def cam(t): return compose(zcam(t), v1cam(t))


def apply_pt(M, x, y): return M[0, 0] * x + M[0, 1] * y + M[0, 2], M[1, 0] * x + M[1, 1] * y + M[1, 2]


# ---------------------------------------------------------------- world layout (06b plate coordinates)
x0, y0, cw, ch = BOX
MAIN = (x0, y0, cw, ch)
GAP = 0.04 * cw
TLC = (x0 - GAP - cw, y0 - 1.03 * ch, cw, ch)           # pin f29-32: top-left card's bottom = main top - 3 %, right = main left - 4 %
BRC = (x0 + cw / 2, y0 + 0.78 * ch, cw, ch)             # pin: bottom-right card's left = main centre, slides up over its lower ~22 %
def rect(X, Y, k): return (X, Y, cw * k, ch * k)
# the wall (world = 06b plate coords). name, rect, source, entry (s after the hand-off), slide (s), from ('up' above / 'dn' below)
#   pin: TL card from above at f19, BR card from below at f21 (G1); the extra cards stagger in over the first ~0.6 s the same way
WALL = [('exc',    rect(x0 - 0.06 * cw - 0.90 * cw, y0 + 0.30 * ch, 0.90), 'exc',    0.16, 0.80, 'dn'),   # excavator, left of main
        ('tl',     TLC,                                                      'harn',   0.24, 0.70, 'up'),   # pin TL card
        ('br',     BRC,                                                      'tank',   0.32, 0.90, 'dn'),   # pin BR card
        ('lumi14', rect(x0 + cw + 0.06 * cw, y0 - 0.45 * ch, 0.85),       'lumi14', 0.44, 0.80, 'up'),   # right of main, high
        ('chk',    rect(TLC[0] - 0.06 * cw - 0.85 * cw, TLC[1] - 0.25 * ch, 0.85), 'chk', 0.50, 0.80, 'up'),   # far left, high
        ('lumi5',  rect(BRC[0] + cw + 0.06 * cw, BRC[1] + 0.40 * ch, 0.95), 'lumi5',  0.66, 0.80, 'dn'),   # far right, low
        ('i226b',  rect(x0 - 0.06 * cw - 1.85 * cw, y0 + 1.30 * ch, 1.0), 'i226',  0.40, 0.80, 'dn'),   # bottom-left: tank inspection
        ('intel',  rect(x0 + cw + 0.45 * cw, y0 - 0.45 * ch - 1.10 * ch, 0.95), 'intel', 0.70, 0.80, 'up')]   # top-right: jobsite aerial   # far right, low
FOOTS = {}
FOOT_FIT = {'exc': (0.5, 0.5, 1.0), 'harn': (0.5, 0.5, 1.0), 'tank': (0.5, 0.5, 1.0), 'lumi14': (0.5, 0.45, 1.12),
            'chk': (0.42, 0.40, 1.20), 'lumi5': (0.5, 0.45, 1.12), 'i226': (0.42, 0.40, 1.20), 'intel': (0.5, 0.45, 1.10)}


def sat_off(t, name):
    """screen-space slide in from beyond the frame edge (G1: fastest at entry, long settle)"""
    nm, (X, Y, w, h), src, e_in, dur, side = next(r for r in WALL if r[0] == name)
    t_in = TH + e_in
    if t < t_in: return None
    u = G1(cl((t - t_in) / dur)); M = cam(t_in)
    if side == 'up':
        yb = max(apply_pt(M, X, Y + h)[1], apply_pt(M, X + w, Y + h)[1]); return -(max(yb, 0) + 8) * (1 - u)
    yt = min(apply_pt(M, X, Y)[1], apply_pt(M, X + w, Y)[1]); return (H - min(yt, H) + 8) * (1 - u)


# ---------------------------------------------------------------- textures (M, C) at world scale
MG = 60
def mc_draw(w, h, fn):
    P0 = np.zeros((h, w, 3), np.float32); P1 = np.full((h, w, 3), 200.0, np.float32)
    fn(P0); fn(P1)
    return (P1 - P0) / 200.0, P0


def card_tex(img, w, h, fx, fy, zoom):
    tw, th = int(w) + 2 * MG, int(h) + 2 * MG
    return mc_draw(tw, th, lambda d: L.card(d, img, MG, MG, int(w), int(h), fx=fx, fy=fy, zoom=zoom))


_GROUND = {}
GP = (700, 1100)                                        # ground pad (y, x)
def ground(n):
    if n not in _GROUND:
        g = tech(29, t_old(n / FPS), 0.75)                 # same ground clock as v1 06b (old time): no pop at the hand-off
        _GROUND.clear(); _GROUND[n] = cv2.copyMakeBorder(g, GP[0], GP[0], GP[1], GP[1], cv2.BORDER_REFLECT)
    return _GROUND[n]


# text (children of the main card)
SOME = "It's somewhat"; PX_S = 150
XC_S, YB_S = x0 + cw / 2, y0 - 34                      # centred above 'manufactured.' on the main card's axis
T_ITS, T_SOME = wn('somewhat', 56) - 0.30, wn('somewhat', 56) - LEAD
MAN = 'manufactured.'; PX_M = 380; DT_M = 0.75          # hero: types on letter by letter
XC_M, YB_M = x0 + cw / 2, y0 + 0.70 * ch                # on the main card, above the bottom-right card's top
T_MAN = wn('manufactured', 56) - LEAD


def cap_text(d, txt, px, xc, base_y, face, grad, shadow=0.75, glow=0.25, op=1.0, x_left=None):
    """the trailer caption: soft drop shadow (J3.drop_shadow, down-right, as L.grad_text) + soft glow + the type
    (white, or the blue -> purple gradient); centred on xc (or from x_left)"""
    rg, asc = J3.text_rgba(txt, px, face=face, fill=(255, 255, 255))
    lay = rg.copy()
    if grad is not None:
        g = J.grad(rg.shape[1], rg.shape[0], grad[0], grad[1]) / 255; lay[..., :3] = g * rg[..., 3:4]
    if op < 1: lay = lay * op
    x0_ = x_left if x_left is not None else xc - rg.shape[1] / 2; y0_ = base_y - asc
    J3.drop_shadow(d, lay, x0_, y0_, 1.0, strength=shadow)
    if glow: J3.glow_screen(d, lay[..., :3] * 255, 18, glow, x0_, y0_)
    J3.over(d, lay, x0_, y0_)


class TextTex:
    def __init__(s):
        fS = J3.text_rgba(SOME, PX_S); s.wS = fS[0].shape[1]; w2 = J3.text_rgba('somewhat', PX_S)[0].shape[1]
        s.xS1 = XC_S - s.wS / 2; s.xS2 = s.xS1 + s.wS - w2
        s.rS = (int(s.xS1 - 70), int(YB_S - PX_S - 60), int(s.xS1 + s.wS + 70), int(YB_S + 70))
        rg, asc = J3.text_rgba(MAN, PX_M, face='it'); s.wM = rg.shape[1]
        xm0 = XC_M - s.wM / 2
        s.rM = (int(xm0 - 80), int(YB_M - asc - 70), int(xm0 + s.wM + 80), int(YB_M - asc + rg.shape[0] + 70))
        w, h = s.rM[2] - s.rM[0], s.rM[3] - s.rM[1]; ox, oy = s.rM[0], s.rM[1]
        s.white = mc_draw(w, h, lambda d: cap_text(d, MAN, PX_M, XC_M - ox, YB_M - oy, 'it', None, shadow=0.95, glow=0.22))
        s.grad = mc_draw(w, h, lambda d: cap_text(d, MAN, PX_M, XC_M - ox, YB_M - oy, 'it', PURPLE, shadow=0.75, glow=0.30))
        s.edges = [xm0 - ox + (J3.text_rgba(MAN[:i], PX_M, face='it')[0].shape[1] if i else 0) for i in range(len(MAN) + 1)]
        s.edges[-1] = w
        s.tl = [T_MAN + i * DT_M / FPS for i in range(len(MAN))]
        s.cS = {}
    def some(s, t):
        st = tuple(round(EIO(cl((t - tw) / (3 / FPS))) * 6) / 6 for tw in (T_ITS, T_SOME))
        if st == (0, 0): return None
        if st in s.cS: return s.cS[st]
        w, h = s.rS[2] - s.rS[0], s.rS[3] - s.rS[1]; ox, oy = s.rS[0], s.rS[1]
        M = np.ones((h, w, 3), np.float32); C = np.zeros((h, w, 3), np.float32)
        for word, x, a in (("It's", s.xS1, st[0]), ('somewhat', s.xS2, st[1])):
            if a <= 0: continue
            Mi, Ci = mc_draw(w, h, lambda d: cap_text(d, word, PX_S, None, YB_S + 14 * (1 - a) - oy, 'reg', None, shadow=0.85, glow=0.20, op=a, x_left=x - ox))
            sg = 5.0 * (1 - a)
            if sg > 0.3: Mi = cv2.GaussianBlur(Mi, (0, 0), sg); Ci = cv2.GaussianBlur(Ci, (0, 0), sg)
            M = M * Mi; C = C * Mi + Ci
        if len(s.cS) > 8: s.cS.clear()
        s.cS[st] = (M, C); return M, C
    def man(s, t):
        k = sum(1 for x in s.tl if t >= x + 1.0 / FPS); f = 0.0
        if k < len(s.tl) and t >= s.tl[k]: f = round(cl((t - s.tl[k]) * FPS) * 2) / 2
        if k == 0 and f == 0: return None
        m = np.zeros(s.white[0].shape[1], np.float32); m[:int(s.edges[k])] = 1
        if k < len(s.edges) - 1: m[int(s.edges[k]):int(s.edges[k + 1])] = f
        m = m[None, :, None]
        return [(1 - m * (1 - Mi), Ci * m) for Mi, Ci in (s.white, s.grad)]


TT = None


def warp_mc(M, C, A, border_m=1.0):
    Mw = cv2.warpAffine(M, A, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(border_m,) * 3)
    Cw = cv2.warpAffine(C, A, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
    return Mw, Cw


def tex_to_screen(Mcam, ox, oy, s=1.0):
    """affine for a texture whose pixel (u, v) is world (ox + u / s, oy + v / s)"""
    return compose(Mcam, np.float32([[1 / s, 0, ox], [0, 1 / s, oy]]))


def shrink(tex, s):
    if s >= 0.98: return tex, 1.0
    return tuple(cv2.resize(a, None, fx=s, fy=s, interpolation=cv2.INTER_AREA) for a in tex), s


# ---------------------------------------------------------------- 06c frame (pin animation)
def cards_tex(n, sf):
    """per output frame: (name, rect, tex at scale sf, body mask)"""
    out = []
    w_ = EIO(cl((n - NH) / XF))
    a = F_EXC.img(n); b = F_WH.img(n)
    ta = card_tex(a, cw, ch, F_EXC.fx, F_EXC.fy, F_EXC.zoom)
    tb = card_tex(b, cw, ch, F_WH.fx, F_WH.fy, F_WH.zoom)
    tm = (ta[0], ta[1] * (1 - w_) + tb[1] * w_) if w_ < 1 else tb          # footage changes with opacity (box itself stays)
    out.append(('main', MAIN, shrink(tm, sf)))
    for nm, rc, src, e_in, dur, side in WALL:
        if n / FPS + 0.5 / FPS < TH + e_in: continue
        f = FOOTS[nm]; fx, fy, z = FOOT_FIT[src]
        out.append((nm, rc, shrink(card_tex(f.img(n), rc[2], rc[3], fx, fy, z), sf)))
    return out


def sub06c(ts, n, ct, gr):
    Mc = cam(ts)
    sf_g = gr[1]
    out = cv2.warpAffine(gr[0], tex_to_screen(Mc, -GP[1], -GP[0], sf_g), (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    cov = np.zeros((H, W), np.float32)
    for nm, (X, Y, w, h), (tex, sf) in ct:
        A = Mc
        if nm != 'main':
            off = sat_off(ts, nm)
            if off is None: continue
            A = compose(np.float32([[1, 0, 0], [0, 1, off]]), Mc)
        T = tex_to_screen(A, X - MG, Y - MG, sf)
        Mw, Cw = warp_mc(tex[0], tex[1], T)
        out = out * Mw + Cw
        body = cv2.warpAffine(np.ones((int(h), int(w)), np.float32), compose(A, np.float32([[1, 0, X], [0, 1, Y]])), (W, H),
                              flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        cov = np.maximum(cov, body)
    # 06b captions disappear as the animation starts (3 f), moving with the camera
    fo = 1 - EIO(cl((ts - TH) / (3 / FPS)))
    if fo > 0.002:
        XT = compose(zcam(ts), v1txt(ts))
        for it in SH.items:
            if it.op(t_old(ts)) > 0: apply_item(out, it.mc(None), fo, XT)
    # captions on the main card (same transform as the footage)
    r = TT.some(ts)
    if r is not None:
        Mw, Cw = warp_mc(r[0], r[1], tex_to_screen(Mc, TT.rS[0], TT.rS[1])); out = out * Mw + Cw
    r = TT.man(ts)
    if r is not None:
        T = tex_to_screen(Mc, TT.rM[0], TT.rM[1])
        (Mw1, Cw1), (Mw2, Cw2) = warp_mc(*r[0], T), warp_mc(*r[1], T)
        c = cov[..., None]
        out = out * (c * Mw1 + (1 - c) * Mw2) + (c * Cw1 + (1 - c) * Cw2)
    return out


def probe(t):
    h = 0.25 / FPS; q = []
    for tt in (t - h, t + h):
        Mc = cam(tt); pts = []
        for nm, (X, Y, w, h_) in [('main', MAIN)] + [(r[0], r[1]) for r in WALL]:
            off = 0.0
            if nm != 'main':
                o = sat_off(tt, nm); off = 0.0 if o is None else o
            for px, py in ((X, Y), (X + w, Y + h_)):
                x, y = apply_pt(Mc, px, py); pts.append((x, y + off))
        q.append(np.float32(pts))
    return float(np.abs(q[0] - q[1]).max())


def frame_06c(n):
    global TT
    if TT is None: TT = TextTex()
    t = n / FPS; J3.RNG_T[0] = t
    d = probe(t); ns = int(np.clip(math.ceil(d / 1.6), 1, 12))
    sf = min(1.0, S_(t) * 1.08)
    ct = cards_tex(n, sf)
    gr = shrink((ground(n),), sf); gr = (gr[0][0], gr[1])
    if ns == 1: out = sub06c(t, n, ct, gr)
    else: out = sum(sub06c(t + (k / (ns - 1) - 0.5) * 0.5 / FPS, n, ct, gr) for k in range(ns)) / ns
    return fin16.finish(np.clip(J3.grain(out, 4.5, seed=n), 0, 255), vig=0.60, tex=0.35, rb=0.50).astype(np.float32), ns, d


# ---------------------------------------------------------------- pixel overlay (jennifer render3.pixel_overlay, 16:9)
PX_DUR_F = 14
_PXF = None
PX_RAMP = np.array([[0, 0, 0], [5, 40, 167], [18, 86, 255], [40, 250, 242], [236, 255, 255]], np.float32)
def px_frames():
    global _PXF
    if _PXF is None:
        c = cv2.VideoCapture('/Users/gourav/Downloads/(Footage)/pixel transition 2.mov'); fr = []
        while True:
            ok, f = c.read()
            if not ok: break
            Lm = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
            Lm = cv2.resize(Lm, (W, H), interpolation=cv2.INTER_NEAREST)
            x = np.clip(Lm, 0, 1) * (len(PX_RAMP) - 1); i0 = np.floor(x).astype(int).clip(0, len(PX_RAMP) - 2); u = (x - i0)[..., None]
            fr.append((PX_RAMP[i0] * (1 - u) + PX_RAMP[i0 + 1] * u, Lm))
        _PXF = fr
    return _PXF
def pixel_overlay(a, b, k):
    fr = px_frames(); rgb, Lm = fr[min(len(fr) - 1, int(k * len(fr)))]
    base = a if k < 0.5 else b
    cover = np.clip(Lm * 2.2, 0, 1)[..., None]
    blocks = cv2.resize(cv2.resize(base, (48, 27), interpolation=cv2.INTER_AREA), (W, H), interpolation=cv2.INTER_NEAREST)
    base = base * (1 - cover) + blocks * cover
    return 255 - (255 - base) * (255 - rgb) / 255


# ---------------------------------------------------------------- the segment
def frame(n):
    k = (n - (NC - PX_DUR_F / 2)) / PX_DUR_F
    if n < NH: out, ns, d = frame_06b(n), 0, 0
    elif n < NC: out, ns, d = frame_06c(n)
    else: out, ns, d = RV.frame('v1', n).astype(np.float32), 0, 0
    if 0 <= k < 1: out = pixel_overlay(out, out, k)          # base switches at the cut itself (k = 0.5 at 1392)
    return np.clip(out, 0, 255).astype(np.uint8), ns, d


def init():
    for nm, rc, src, e_in, dur, side in WALL:                  # each card's own footage from its first visible frame, real speed
        FOOTS[nm] = Foot(src, int(math.ceil((TH + e_in) * FPS)))
init()


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
    elif mode == 'curves':
        for n in range(NH, NC + 1, 3): print(n, 'S %.3f roll %.2f dy %.1f' % (S_(n / FPS), roll_(n / FPS), dy_(n / FPS)), 'probe %.1f' % probe(n / FPS))
    elif mode == 'render':
        import multiprocessing as mp
        os.makedirs(HERE + 'chunks', exist_ok=True)
        cuts = [N0, 1298, 1343, 1368, N1]
        jobs = [(cuts[i], cuts[i + 1], HERE + f'chunks/c{i}.mp4') for i in range(len(cuts) - 1)]
        with mp.get_context('fork').Pool(3) as pool: paths = pool.map(render_range, jobs)
        open(HERE + 'chunks/list.txt', 'w').write(''.join(f"file '{q}'\n" for q in paths))
        out = OUTD + '11b_manu_v3.mp4'
        subprocess.run([FF, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', HERE + 'chunks/list.txt', '-c', 'copy', out], check=True)
        print('done', out)
