"""v3 (Krish on v2): (1) the opening move runs on his graph cubic-bezier(0,1,1,1) from the scene's first frame (fastest at the
cut, long settle onto Justin's card); the Justin->TT and TT->BC moves and their overlap are unchanged. (2) a thin, very glowing
purple line draws from TradeTapp to BuildingConnected like pin.it/2AbnLjOI5 (path + two-surge draw-on measured from the ref,
refs/pin_line), attached to the logos' 3D plane, drawing on while the camera travels so the camera follows its head.

15.66-19.55 s alt scene, v2 (Krish's notes on v1: camera far too fast and not smooth, too few elements, moves between
logos looked flat 2D). Reference: pin.it/2boBV7c90, measured frame by frame (refs/pin_15_19/motion.json).
  * the ref's big moves last 1.25-2.0 s with the speed peaking ~30-35 % in and a long tail (= EASE_USER). v1 squeezed them
    into 0.4 s. v2 uses only two big moves at the ref's real length (2.0 s / 1.95 s), overlapped, plus one continuous drift chain.
  * real 3D camera: look-at target + distance + orbit (yaw/pitch), true perspective projection of every layer (cards
    foreshorten), each move pulls back and swings round then pushes in; depth of field follows the target plane.
  * 17 elements at 8 depths (far tech ground + hairline grid, far UI/site cards, Justin's card, tiles, logos, chips).
  * captions sit on their logo's plane, so they move in 3D with it; Dime-style per-word reveal (3 f fade, 16 px rise,
    blur clearing; hero words type on letter by letter).
  * B-roll tiles play only their unique frames, one per output frame (native cadence); UI frames are stills; A-roll 1:1.
  python scene2.py stills | speed | render out.mp4
"""
import sys, os, math, json, subprocess
sys.path.insert(0, '/Users/gourav/jl-trailer/trailer')
import numpy as np, cv2
from PIL import Image
from engine import *            # W, H, CX, CY, J3, L, EU, G1, G2, EIO, cl, spk_frame, vid, tech, fin16, wt, FPS

A = '/Users/gourav/jl-trailer/trailer/alt_15_19/'
AS = A + 'assets/'
FF = '/Users/gourav/ks-ron-build/reel1/ff'
T0, T1 = 15.66, 19.55
N0, N1 = int(round(T0 * FPS)), int(round(T1 * FPS))
F = 1000.0
BLUE0, BLUE1 = (70, 255, 236), (40, 120, 255)
KEY0, KEY1 = (40, 132, 255), (16, 56, 214)
UNQ = json.load(open(AS + 'unique_frames.json'))
LEAD = 0.05


# ---------------------------------------------------------------- small image helpers (straight RGBA, 0..255)
def rgba(p): return np.asarray(Image.open(p).convert('RGBA')).astype(np.float32)


def rrect_mask(w, h, r):
    m = np.zeros((h, w), np.uint8); r = int(max(1, min(r, h // 2, w // 2)))
    cv2.rectangle(m, (r, 0), (w - 1 - r, h - 1), 255, -1); cv2.rectangle(m, (0, r), (w - 1, h - 1 - r), 255, -1)
    for cx_, cy_ in ((r, r), (w - 1 - r, r), (r, h - 1 - r), (w - 1 - r, h - 1 - r)): cv2.circle(m, (cx_, cy_), r, 255, -1, cv2.LINE_AA)
    return m.astype(np.float32)


def border(img, m, col=(255, 255, 255), a=0.14, th=2):
    e = cv2.morphologyEx((m > 127).astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((th * 2 + 1, th * 2 + 1), np.uint8)).astype(np.float32)
    e = cv2.GaussianBlur(e, (0, 0), 0.8) * (m / 255)
    img[..., :3] = img[..., :3] * (1 - a * e[..., None]) + np.array(col, np.float32) * a * e[..., None]


def paste(dst, src, x, y):
    h, w = src.shape[:2]; x, y = int(round(x)), int(round(y))
    xa, ya, xb, yb = max(0, x), max(0, y), min(dst.shape[1], x + w), min(dst.shape[0], y + h)
    if xb <= xa or yb <= ya: return
    s = src[ya - y:yb - y, xa - x:xb - x]; a = s[..., 3:4] / 255
    d = dst[ya:yb, xa:xb]; d[..., :3] = d[..., :3] * (1 - a) + s[..., :3] * a; d[..., 3:4] = d[..., 3:4] * (1 - a) + 255 * a


def text_img(txt, px, face='reg', fill=(255, 255, 255)):
    rg, asc = J3.text_rgba(txt, px, face, fill, 1.0)
    a = rg[..., 3:4]; rgb = np.where(a > 1e-4, rg[..., :3] / np.maximum(a, 1e-4), 0)
    return np.concatenate([rgb * 255, a * 255], 2).astype(np.float32), asc


def logo_w(p, w):
    im = rgba(p); s = w / im.shape[1]
    return cv2.resize(im, (int(w), max(1, int(im.shape[0] * s))), interpolation=cv2.INTER_AREA)


def logo_h(p, h):
    im = rgba(p); s = h / im.shape[0]
    return cv2.resize(im, (max(1, int(im.shape[1] * s)), int(h)), interpolation=cv2.INTER_AREA)


def grad_img(w, h, c0, c1):
    u = np.linspace(0, 1, w, dtype=np.float32)[None, :, None]
    return np.broadcast_to(np.array(c0, np.float32) * (1 - u) + np.array(c1, np.float32) * u, (h, w, 3)).copy()


def chip_img(pw, ph, txt, px, rs, grad_border=True, fill=(16, 17, 20)):
    img = np.zeros((ph, pw, 4), np.float32); m = rrect_mask(pw, ph, ph / 2); img[..., :3] = fill; img[..., 3] = m
    if grad_border:
        g = grad_img(pw, ph, BLUE0, BLUE1); e = cv2.morphologyEx((m > 127).astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((5, 5), np.uint8)).astype(np.float32)[..., None]
        img[..., :3] = img[..., :3] * (1 - e) + g * e
    else: border(img, m, a=0.22)
    t, _ = text_img(txt, int(px * rs), fill=(236, 240, 246)); paste(img, t, (pw - t.shape[1]) / 2, (ph - t.shape[0]) / 2 + 1)
    return img


# ---------------------------------------------------------------- footage
_RD = {}
def clip_frame(name, idx):
    """frame idx of a B-roll clip, read once (intra-coded, seek is exact)"""
    k = (name, idx)
    if k in _RD: return _RD[k]
    c = cv2.VideoCapture(f'/Users/gourav/jl-trailer/trailer/broll/{name}.mp4'); c.set(cv2.CAP_PROP_POS_FRAMES, idx); ok, f = c.read(); c.release()
    f = L.grade(cv2.cvtColor(f, cv2.COLOR_BGR2RGB).astype(np.float32))
    if len(_RD) > 24: _RD.pop(next(iter(_RD)))
    _RD[k] = f
    return f


def unique_at(name, n, n_start):
    """the clip's own unique frames, one per output frame from n_start (native cadence, never resampled), held at the ends"""
    u = UNQ[name]; k = int(np.clip(n - n_start, 0, len(u) - 1))
    return clip_frame(name, u[k])


def still_of(name, t):
    c = cv2.VideoCapture(f'/Users/gourav/jl-trailer/trailer/broll/{name}.mp4'); c.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, f = c.read(); c.release()
    return L.grade(cv2.cvtColor(f, cv2.COLOR_BGR2RGB).astype(np.float32))


# ---------------------------------------------------------------- the set: (cx, cy, w, h) as seen by the reference camera (front, D=1000), depth z
# z > 0 is behind Justin's card, z < 0 in front of it. RS = render px per world unit.
EL = [
    ('bg',      960, 540, 1920, 1080,  700, 1.0),
    ('grid',    960, 540, 2600, 1500,  450, 0.7),
    ('site',    300, 330,  400,  250,  260, 1.3),     # c_lumi_5 aerial (plays)
    ('bcui',   1610, 255,  430,  250,  260, 1.3),     # TradeTapp risk list (BuildingConnected film, still)
    ('main',    960, 500,  960,  540,    0, 2.0),     # Justin's A-roll in the hero card
    ('label',   960, 190,  360,   40,    0, 2.2),
    ('sold',   1452, 420,  124,   46,  -40, 2.6),
    ('dots',   1500, 690,   64,   18,  -60, 2.6),
    ('adsk',    980, 1105, 210,  126,  -80, 2.8),   # v3: lowered so the line passes clear above it
    ('tt',      470, 765,  220,  280, -120, 3.0),
    ('bc',     1400, 830,  480,  108, -120, 2.9),
    ('risk',    250, 930,  180,   42, -150, 3.0),
    ('bid',    1585, 738,  214,   42, -150, 3.0),
    ('sensor', 1440, 215,  190,  130, -160, 3.0),    # c_lumi_14 (plays)
    ('ttui',    245, 565,  220,  150, -180, 3.0),    # TradeTapp company UI (still)
    ('bcblue', 1665, 968,  210,  118, -180, 3.0),    # BuildingConnected logo frame (still)
    ('lss',    1650, 560,  220,  150, -200, 3.0),    # c_lss_46 LumiNode (plays)
    ('photo',   415, 245,  190,  190, -240, 3.2),    # c_lumi_28 ironworker (plays)
]
ELD = {e[0]: e for e in EL}


def wrect(name):
    _, cx, cy, w, h, z, rs = ELD[name]; k = (1000 + z) / 1000
    return 960 + (cx - 960) * k - w * k / 2, 540 + (cy - 540) * k - h * k / 2, w * k, h * k, z


# ---------------------------------------------------------------- camera
def cam_basis(c):
    yaw, pit = math.radians(c['yaw']), math.radians(c['pitch']); D = math.exp(c['lD'])
    T = np.array([c['tx'], c['ty'], c['tz']])
    P = T + D * np.array([math.sin(yaw) * math.cos(pit), -math.sin(pit), -math.cos(yaw) * math.cos(pit)])
    Fw = (T - P) / np.linalg.norm(T - P)
    R = np.cross(np.array([0, 1.0, 0]), Fw); R /= np.linalg.norm(R); Dn = np.cross(Fw, R)
    return P, R, Dn, Fw, D


def project(basis, pts):
    P, R, Dn, Fw, D = basis; v = pts - P
    x, y, z = v @ R, v @ Dn, v @ Fw
    return np.stack([960 + F * x / z, 540 + F * y / z], 1), z


def target_for(name, sx, sy, screen_h=None, screen_w=None):
    X, Y, w, h, z = wrect(name)
    D = F * (h / screen_h if screen_h else w / screen_w)
    return dict(tx=X + w / 2 + (960 - sx) * D / F, ty=Y + h / 2 + (540 - sy) * D / F, tz=z, lD=math.log(D))


KJ = dict(tx=960.0, ty=505.0, tz=0.0, lD=math.log(1000 / 1.32), yaw=0.0, pitch=0.0, dof=0.55)
KT = dict(target_for('tt', 560, 505, screen_h=540), yaw=0.0, pitch=0.0, dof=1.0)
KB = dict(target_for('bc', 1190, 525, screen_w=960), yaw=0.0, pitch=0.0, dof=1.0)
CHN = ('tx', 'ty', 'tz', 'lD', 'yaw', 'pitch', 'dof')
# two big moves (ref length or longer), the second starting 57 % into the first (keyframe overlapping). Target, distance
# and focus travel on Krish's EASE_USER; through each move the camera pulls back and orbits out and home again (a sine hill
# on EASE_IO), so it reads as a 3D move through z-space. Screen-flow speed: one hill per move, peak 91 px/f, max change 20 px/f.
MOVES = [(15.60, 2.50, KJ, KT, dict(lD=0.50, yaw=-10.0, pitch=4.0)), (17.45, 2.10, KT, KB, dict(lD=0.60, yaw=11.0, pitch=-3.0))]
DRIFT_DUR, DRIFT_STEP = 3.0, 0.2
DRIFT_N = int(math.ceil((T1 + 0.9 - (T0 - 1.5) - DRIFT_DUR) / (DRIFT_DUR * DRIFT_STEP))) + 1


# v3 opening move on Krish's graph cubic-bezier(0,1,1,1): starts ON the scene's first frame, so its fastest part (the
# curve is steepest at x=0) is seen as the scene opens, then it decelerates over a long settle onto Justin's card. It
# runs the same way as the Justin->TT move that picks up under it (camera panning left/down, orbiting to straight-on,
# pushing in), so the speeds hand over without a park.
BZ_OPEN = J3.bez(0, 1, 1, 1)
T_OPEN, D_OPEN = N0 / FPS, 1.45
OPEN_OFF = dict(tx=142.0, ty=-55.0, lD=0.24, yaw=8.5, pitch=-3.0)


def cam_at(t):
    c = dict(KJ)
    o = 1.0 - BZ_OPEN(cl((t - T_OPEN) / D_OPEN))
    for k, v in OPEN_OFF.items(): c[k] += v * o
    for t0, d, a, b, sw in MOVES:
        u = cl((t - t0) / d); e = EU(u); hill = math.sin(math.pi * EIO(u))
        for k in CHN: c[k] += (b[k] - a[k]) * e
        for k, v in sw.items(): c[k] += v * hill
    for i in range(DRIFT_N):                                       # one slow continuous push + sway, 20 % overlap chain
        t0 = T0 - 1.5 + i * DRIFT_DUR * DRIFT_STEP; e = EU(cl((t - t0) / DRIFT_DUR))
        c['lD'] -= 0.075 / DRIFT_N * e
    return c


def sigma_for(basis, zc):
    D = basis[4]; return abs(F / zc - F / D)


# ---------------------------------------------------------------- art
_ART = {}
def art(name, n):
    _, cx, cy, w, h, z, rs = ELD[name]; X, Y, ww, hh, _ = wrect(name)
    pw, ph = int(round(ww * rs)), int(round(hh * rs))
    play = {'site': ('c_lumi_5', N0 - 10), 'sensor': ('c_lumi_14', N0 - 4), 'lss': ('c_lss_46', N1 - 43), 'photo': ('c_lumi_28', N0)}
    if name in play:
        clip, ns = play[name]; f = unique_at(clip, n, ns)
        key = (name, UNQ[clip][int(np.clip(n - ns, 0, len(UNQ[clip]) - 1))])
        if key in _ART: return _ART[key]
        fx, fy, zz = {'site': (0.5, 0.5, 1.0), 'sensor': (0.5, 0.5, 1.1), 'lss': (0.42, 0.40, 1.1), 'photo': (0.30, 0.42, 1.10)}[name]
        img = np.zeros((ph, pw, 4), np.float32); m = rrect_mask(pw, ph, 10 * rs); img[..., :3] = L.fit(f, pw, ph, fx, fy, zz); img[..., 3] = m
        border(img, m, a=0.18)
        if len(_ART) > 80: _ART.pop(next(iter(_ART)))
        _ART[key] = img
        return img
    if name in _ART: return _ART[name]
    img = np.zeros((ph, pw, 4), np.float32)
    if name == 'bg':
        img = None                                                  # drawn per frame (animated numbers)
    elif name == 'grid':
        step = 200 * rs; col = (150, 172, 196)
        for x in np.arange(0, pw, step): cv2.line(img, (int(x), 0), (int(x), ph - 1), (*col, 30), 2, cv2.LINE_AA)
        for y in np.arange(0, ph, step): cv2.line(img, (0, int(y)), (pw - 1, int(y)), (*col, 30), 2, cv2.LINE_AA)
    elif name == 'bcui':
        f = still_of('c_bctt_15', 2.2); c = L.fit(f[:, int(f.shape[1] * 0.47):], pw, ph, 0.5, 0.2, 1.0)
        m = rrect_mask(pw, ph, 10 * rs); img[..., :3] = c; img[..., 3] = m; border(img, m, a=0.2)
    elif name == 'ttui':
        f = still_of('c_bctt_15', 0.5); c = L.fit(f[:, int(f.shape[1] * 0.44):], pw, ph, 0.5, 0.1, 1.0)
        m = rrect_mask(pw, ph, 10 * rs); img[..., :3] = c; img[..., 3] = m; border(img, m, a=0.2)
    elif name == 'bcblue':
        f = still_of('s_bc_logo', 1.0); c = L.fit(f, pw, ph, 0.5, 0.5, 1.25)
        m = rrect_mask(pw, ph, 10 * rs); img[..., :3] = c; img[..., 3] = m; border(img, m, a=0.2)
    elif name == 'label':
        m = rrect_mask(pw, ph, ph / 2); img[..., :3] = (20, 21, 25); img[..., 3] = m; border(img, m, a=0.22)
        t, _ = text_img('Verticals  ·  a weekly biz show', int(16 * rs), fill=(222, 226, 232)); paste(img, t, (pw - t.shape[1]) / 2, (ph - t.shape[0]) / 2 + 1)
    elif name == 'sold': img = chip_img(pw, ph, 'SOLD', 19, rs)
    elif name == 'risk': img = chip_img(pw, ph, 'Risk profiles', 16, rs, grad_border=False)
    elif name == 'bid': img = chip_img(pw, ph, 'Bid management', 16, rs, grad_border=False)
    elif name == 'dots':
        for i, c in enumerate((BLUE0, BLUE1)): cv2.circle(img, (int(ph / 2 + i * (pw - ph)), int(ph / 2)), int(ph / 2 - 1), (*c, 255), -1, cv2.LINE_AA)
    elif name == 'adsk':
        m = rrect_mask(pw, ph, 10 * rs); img[..., :3] = (18, 19, 23); img[..., 3] = m; border(img, m, a=0.16)
        lg = logo_w(L.ROOT + '/assets/logos/Autodesk_Logo_2021_dk.png', pw * 0.66); paste(img, lg, (pw - lg.shape[1]) / 2, (ph - lg.shape[0]) / 2)
    elif name == 'bc':
        m = rrect_mask(pw, ph, ph / 2); img[..., :3] = grad_img(pw, ph, KEY0, KEY1); img[..., 3] = m
        sh = np.zeros_like(img[..., 0]); sh[: ph // 2] = 1; img[..., :3] += 18 * cv2.GaussianBlur(sh, (0, 0), ph / 5)[..., None] * (m[..., None] / 255)
        border(img, m, a=0.28)
        lg = logo_w(AS + 'bc_logo_white.png', pw * 0.74); paste(img, lg, (pw - lg.shape[1]) / 2, (ph - lg.shape[0]) / 2)
    _ART[name] = img
    return img


def art_tt(m_, rs=3.0):
    k = ('tt', round(m_, 3))
    if k in _ART: return _ART[k]
    X, Y, w, h, _ = wrect('tt'); pw, ph = int(round(w * rs)), int(round(h * rs))
    img = np.zeros((ph, pw, 4), np.float32); m = rrect_mask(pw, ph, 12 * rs); img[..., :3] = (17, 18, 22); img[..., 3] = m; border(img, m, a=0.16)
    pad = 13 * rs
    wd = logo_h(AS + 'tt_word.png', 10.5 * rs); paste(img, wd, pad, pad)
    t, _ = text_img('Construction software', int(9.5 * rs), fill=(150, 156, 166)); paste(img, t, pad, pad + wd.shape[0] + 5 * rs)
    tg = np.zeros((int(17 * rs), int(30 * rs), 4), np.float32); tm = rrect_mask(tg.shape[1], tg.shape[0], tg.shape[0] / 2)
    tg[..., :3] = (44, 47, 54); tg[..., 3] = tm; tt_, _ = text_img('01', int(9.5 * rs), fill=(210, 214, 220))
    paste(tg, tt_, (tg.shape[1] - tt_.shape[1]) / 2, (tg.shape[0] - tt_.shape[0]) / 2 + 1); paste(img, tg, pw - pad - tg.shape[1], pad - 2 * rs)
    mk = logo_w(AS + 'tt_mark.png', pw * 0.62)
    sy = (1 - 0.9 * EIO(cl(2 * m_))) if m_ < 0.5 else (0.1 + 0.9 * EIO(cl(2 * m_ - 1)))
    if m_ >= 0.5: mk = mk.copy(); mk[..., :3] = grad_img(mk.shape[1], mk.shape[0], BLUE0, BLUE1)
    mh = max(2, int(mk.shape[0] * sy)); mk = cv2.resize(mk, (mk.shape[1], mh), interpolation=cv2.INTER_AREA)
    paste(img, mk, (pw - mk.shape[1]) / 2, ph - 20 * rs - mh)
    if len(_ART) > 80: _ART.pop(next(iter(_ART)))
    _ART[k] = img
    return img


def art_main(n, rs=2.0):
    X, Y, w, h, _ = wrect('main'); pw, ph = int(round(w * rs)), int(round(h * rs))
    f = cv2.resize(spk_frame(n), (pw, ph), interpolation=cv2.INTER_AREA)            # A-roll: native 24 fps, frame n = output frame n
    y = np.linspace(0, 1, ph, dtype=np.float32)[:, None, None]; xg = np.linspace(0, 1, pw, dtype=np.float32)[None, :, None]
    f = f * (1 - 0.62 * np.clip((y - 0.55) / 0.45, 0, 1) ** 1.4) * (1 - 0.35 * np.clip((0.16 - y) / 0.16, 0, 1))
    ux = np.clip((0.40 - xg) / 0.26, 0, 1); uy = np.clip((0.72 - y) / 0.30, 0, 1)
    f = f * (1 - 0.80 * (ux * ux * (3 - 2 * ux)) * (uy * uy * (3 - 2 * uy)))       # hero shade behind the headline
    img = np.zeros((ph, pw, 4), np.float32); m = rrect_mask(pw, ph, 16 * rs); img[..., :3] = f; img[..., 3] = m
    pad = 24 * rs
    if 'shep' not in _ART: _ART['shep'] = logo_h(L.ROOT + '/assets/logos/shepherd_dk.png', 17 * rs)
    paste(img, _ART['shep'], 0.06 * pw, pad)
    xx = pw - pad
    for lab in ('Construction', 'Insurance'):
        t, _ = text_img(lab, int(12 * rs), fill=(208, 212, 218)); xx -= t.shape[1]; paste(img, t, xx, pad + 2 * rs); xx -= 26 * rs
    border(img, m, a=0.18)
    return img


# ---------------------------------------------------------------- captions: Dime reveal, laid out once, on their logo's plane
RSC = 2.4
def word_layer(txt, wpx, kind):
    face = 'it' if kind == 'it' else 'reg'
    t, asc = text_img(txt, int(wpx * RSC), face=face)
    if kind == 'grad': t[..., :3] = grad_img(t.shape[1], t.shape[0], BLUE0, BLUE1)
    return t, asc


def caption_lines():
    Xm, Ym, wm, hm, zm = wrect('main'); Xt, Yt, wt_, ht, zt = wrect('tt'); Xb, Yb, wb, hb, zb = wrect('bc')
    # (plane z, x, baseline y, align, [(t_word, word, world px, kind)], t_off)
    return [
        (zm, Xm + 0.06 * wm, Ym + 0.29 * hm, 'left', [(T0 - 0.02, 'construction', 46, 'put')], 16.95),
        (zm, Xm + 0.06 * wm, Ym + 0.29 * hm + 54, 'left', [(wt('software', 15), 'software', 46, 'put')], 16.95),
        (zm, Xm + 0.055 * wm, Ym + 0.29 * hm + 142, 'left', [(wt('business', 16), 'business.', 88, 'grad')], 16.95),
        (zt, Xt + wt_ + 22, Yt + ht * 0.5 + 18, 'left', [(wt('we', 17), 'We', 54, 'grad'), (wt('sold'), 'sold', 54, 'grad')], 18.30),
        (zt, Xt + wt_ + 24, Yt + ht * 0.5 + 66, 'left', [(17.62, 'our', 32, 'it'), (17.68, 'business', 32, 'it')], 18.30),
        (zb, Xb - 22, Yb + hb / 2 + 17, 'right', [(wt('to', 18.3), 'to', 52, 'it')], None)]


CAPL = None


def caption_canvas(line, t):
    """RGBA canvas for one caption line at time t; returns (img, X0, Ytop) in world units on the line's plane"""
    z, X, Yb, align, words, t_off = line
    lay = []; xx = 0.0
    for tw, w, px, kind in words:
        img, asc = word_layer(w, px, kind); sp = J3.font(int(px * RSC)).getlength(' ') * 0.95
        lay.append((tw, img, asc, xx, kind)); xx += img.shape[1] + sp
    lw = xx - sp; asc_max = max(a for _, _, a, _, _ in lay); hmax = max(i.shape[0] for _, i, _, _, _ in lay)
    padc = int(40 * RSC / 2.4) + 30
    cw, chh = int(lw + 2 * padc), int(hmax + 2 * padc + 20)
    can = np.zeros((chh, cw, 4), np.float32)
    off = 1.0 if t_off is None else 1 - EIO(cl((t - t_off) / 0.25))
    for tw, img, asc, x0, kind in lay:
        t_on = tw - LEAD
        if t < t_on: continue
        if kind == 'grad':                                          # hero word: letters type on, one per frame, each fading in over 2 f
            wtxt, pxx = [(w2, p2) for (tw2, w2, p2, k2) in words if tw2 == tw][0]
            fnt = J3.font(int(pxx * RSC)); full = fnt.getlength(wtxt); sc = img.shape[1] / max(1.0, full)
            colA = np.zeros(img.shape[1], np.float32)
            for i in range(len(wtxt)):
                a_i = cl(((t - t_on) * FPS - i * 1.0) / 2.0)
                xa = int(fnt.getlength(wtxt[:i]) * sc); xb = img.shape[1] if i == len(wtxt) - 1 else int(fnt.getlength(wtxt[:i + 1]) * sc)
                colA[xa:xb] = a_i
            w_img = img.copy(); w_img[..., 3] *= colA[None, :]
            a = EIO(cl((t - t_on) / (3 / FPS)))
        else:
            a = EIO(cl((t - t_on) / (3 / FPS))); w_img = img.copy(); w_img[..., 3] *= a
        rise = 16 * (1 - a) * RSC / 2.4; bl = 5.0 * (1 - a)
        if bl > 0.4: w_img = cv2.GaussianBlur(w_img, (0, 0), bl)
        w_img[..., 3] *= off
        y0 = padc + (asc_max - asc) + rise
        # shadow + glow, then the word
        shd = np.zeros_like(w_img); shd[..., 3] = cv2.GaussianBlur(w_img[..., 3], (0, 0), 6) * 0.55
        paste(can, shd, padc + x0 + 2, y0 + 5)
        if kind == 'grad':
            gl = w_img.copy(); gl[..., 3] = cv2.GaussianBlur(w_img[..., 3], (0, 0), 14) * 0.35; paste(can, gl, padc + x0, y0)
        paste(can, w_img, padc + x0, y0)
    X0 = (X - padc / RSC) if align == 'left' else (X - (lw + padc) / RSC)
    return can, X0, Yb - (asc_max + padc) / RSC, z


# ---------------------------------------------------------------- compositing
def warp_layer(out, basis, img, X0, Y0, ww, hh, z, op=1.0, shadow=False, dim_blur=False):
    if img is None or op <= 0.002: return
    corners = np.array([[X0, Y0, z], [X0 + ww, Y0, z], [X0 + ww, Y0 + hh, z], [X0, Y0 + hh, z]], np.float64)
    q, zc = project(basis, corners)
    if (zc < 20).any(): return
    pad_s = 0
    sg = 0.0
    if dim_blur is not None:                                        # focus is a depth plane (the target's), as in the ref
        D = basis[4]; sg = abs(F / (D + (z - DOFK[1])) - F / D) * DOFK[0] if D + (z - DOFK[1]) > 20 else 40.0
    pad_s = int(3 * sg) + 6
    xa, ya = int(max(0, math.floor(q[:, 0].min()) - pad_s)), int(max(0, math.floor(q[:, 1].min()) - pad_s))
    xb, yb = int(min(W, math.ceil(q[:, 0].max()) + pad_s)), int(min(H, math.ceil(q[:, 1].max()) + pad_s))
    if xb <= xa or yb <= ya: return
    ih, iw = img.shape[:2]
    ratio = (np.linalg.norm(q[1] - q[0]) / iw + np.linalg.norm(q[3] - q[0]) / ih) / 2
    src = img if ratio > 0.6 else cv2.GaussianBlur(img, (0, 0), 0.45 / max(ratio, 0.05))
    pm = src.copy(); pm[..., :3] *= pm[..., 3:4] / 255
    Hm = cv2.getPerspectiveTransform(np.float32([[0, 0], [iw, 0], [iw, ih], [0, ih]]), np.float32(q - [xa, ya]))
    lay = cv2.warpPerspective(pm, Hm, (xb - xa, yb - ya), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    if sg > 0.6: lay = cv2.GaussianBlur(lay, (0, 0), sg)
    if dim_blur and sg > 0.6: lay[..., :3] *= 1 - 0.28 * min(1.0, sg / 18)
    a = lay[..., 3:4] / 255 * op
    d = out[ya:yb, xa:xb]
    if shadow:
        sh = cv2.GaussianBlur(lay[..., 3], (0, 0), 10 + sg) / 255 * 0.5 * op
        M = np.float32([[1, 0, 4], [0, 1, 12]]); sh = cv2.warpAffine(sh, M, (sh.shape[1], sh.shape[0]))
        d *= (1 - sh[..., None])
    d[:] = d * (1 - a) + lay[..., :3] * op


DOFK = [55.0, 0.0]


def tt_morph(t): return cl((t - 17.80) / 0.50)


# ---------------------------------------------------------------- v3: glowing line TradeTapp -> BuildingConnected
# Path = the ref's own stroke (pin.it/2AbnLjOI5, frames 7-53: a dip, a U-bend, then an S), mirrored and fitted from the
# bottom of the TradeTapp card to the bottom-left of the BuildingConnected pill on their shared 3D plane (z -120), so it
# parallaxes and foreshortens with the camera. Draw-on = the ref's measured head progress (two surges: whip out, slow,
# whip again, long settle), time-scaled to fit the TT->BC camera travel so the camera chases the head.
LREF = json.load(open(AS + 'line_ref.json'))
LZ = -120.0
LP0, LP1, LEX = (0.62, 1.0), (70.0, 1.0), 0.56              # start (TT frac w, frac h), end (BC x offset, frac h), excursion
L_T0, L_DUR = 17.60, 1.00                                    # draw-on window (ref 1.64 s -> 1.00 s), fully drawn at 18.60
LW = 2.6                                                      # core width, screen px
CORE_C, GLOW_C = np.array([235, 215, 255], np.float32), np.array([150, 70, 255], np.float32)
GLOWS = ((6.0, 1.10), (18.0, 0.75), (45.0, 0.50))            # (sigma px, strength) stacked purple glows, additive


def _line_path():
    rp = np.array(LREF['path']); Xt, Yt, wt_, ht, _ = wrect('tt'); Xb, Yb, wb, hb, _ = wrect('bc')
    P0 = np.array([Xt + wt_ * LP0[0], Yt + ht * LP0[1]]); P1 = np.array([Xb + LP1[0], Yb + hb * LP1[1]])
    a, b = rp[0], rp[-1]; q = (rp - a) * [-1, 1]; v = (b - a) * [-1, 1]; w = P1 - P0
    ang = math.atan2(w[1], w[0]) - math.atan2(v[1], v[0]); sc = np.hypot(*w) / np.hypot(*v)
    Rm = np.array([[math.cos(ang), -math.sin(ang)], [math.sin(ang), math.cos(ang)]]); p = P0 + (q @ Rm.T) * sc
    u = w / np.hypot(*w); nr = np.array([-u[1], u[0]]); rel = p - P0
    p = P0 + np.outer(rel @ u, u) + np.outer((rel @ nr) * LEX, nr)
    s = np.r_[0, np.cumsum(np.hypot(*np.diff(p, axis=0).T))]
    return p, s / s[-1]


LPATH, LARC = _line_path()
LEASE = np.array(LREF['ease'])


def line_prog(t):
    return float(np.interp(cl((t - L_T0) / L_DUR) * (len(LEASE) - 1), np.arange(len(LEASE)), LEASE))


def line_pts(t):
    pr = line_prog(t)
    if pr <= 1e-4: return None, pr
    k = int(np.searchsorted(LARC, pr)); k = max(1, min(k, len(LARC) - 1))
    f = (pr - LARC[k - 1]) / max(1e-9, LARC[k] - LARC[k - 1]); hd = LPATH[k - 1] + (LPATH[k] - LPATH[k - 1]) * f
    pts = np.vstack([LPATH[:k], hd[None]]); return np.c_[pts, np.full(len(pts), LZ)], pr


def line_head_screen(t):
    pts, pr = line_pts(t)
    if pts is None: return None
    q, zc = project(cam_basis(cam_at(t)), pts[-1:]); return q[0]


def _gblur(m, sg):
    k = 1 if sg < 10 else (2 if sg < 30 else 4)                 # big glows blurred at reduced size (same result, faster)
    if k == 1: return cv2.GaussianBlur(m, (0, 0), sg)
    h, w = m.shape; sm = cv2.resize(m, (max(1, w // k), max(1, h // k)), interpolation=cv2.INTER_AREA)
    return cv2.resize(cv2.GaussianBlur(sm, (0, 0), sg / k), (w, h), interpolation=cv2.INTER_LINEAR)


def draw_line(out, basis, t):
    pts, pr = line_pts(t)
    if pts is None: return
    q, zc = project(basis, pts)
    if (zc < 20).any(): return
    D = basis[4]; sg = abs(F / (D + (LZ - DOFK[1])) - F / D) * DOFK[0] if D + (LZ - DOFK[1]) > 20 else 40.0
    m = 150; xa, ya = int(max(0, q[:, 0].min() - m)), int(max(0, q[:, 1].min() - m))
    xb, yb = int(min(W, q[:, 0].max() + m)), int(min(H, q[:, 1].max() + m))
    if xb <= xa or yb <= ya: return
    SS = 4; mk = np.zeros(((yb - ya) * SS, (xb - xa) * SS), np.uint8)
    cv2.polylines(mk, [np.round((q - [xa, ya]) * SS * 16).astype(np.int32)], False, 255, int(round(LW * SS)), cv2.LINE_AA, 4)
    core = cv2.resize(mk.astype(np.float32) / 255, (xb - xa, yb - ya), interpolation=cv2.INTER_AREA)
    if sg > 0.6: core = cv2.GaussianBlur(core, (0, 0), sg)
    # head hot-spot: brighter, bigger bloom while drawing, fades once the line has landed
    hx, hy = q[-1, 0] - xa, q[-1, 1] - ya; ha = 1.0 - EIO(cl((t - (L_T0 + L_DUR)) / 0.35))
    yy, xx = np.mgrid[0:yb - ya, 0:xb - xa].astype(np.float32); r2 = (xx - hx) ** 2 + (yy - hy) ** 2
    glow = np.zeros_like(core)
    for sgl, amp in GLOWS:
        glow += _gblur(core, sgl) * (amp * math.sqrt(2 * math.pi) * sgl / LW)   # normalised: a straight line peaks at amp
    if ha > 0.01:
        glow += ha * (0.9 * np.exp(-r2 / (2 * 14.0 ** 2)) + 0.45 * np.exp(-r2 / (2 * 42.0 ** 2)))
        core = np.maximum(core, ha * np.exp(-r2 / (2 * 3.2 ** 2)))
    d = out[ya:yb, xa:xb]
    d += glow[..., None] * GLOW_C                                  # additive purple glow
    d[:] = d * (1 - core[..., None]) + core[..., None] * CORE_C * 1.0 + core[..., None] * 40.0   # near-white lavender core, hot


def sub_frame(t, n):
    global CAPL
    if CAPL is None: CAPL = caption_lines()
    c = cam_at(t); basis = cam_basis(c); DOFK[0] = 55.0 * c['dof']; DOFK[1] = c['tz']
    out = np.zeros((H, W, 3), np.float32)
    X, Y, ww, hh, z = wrect('bg'); bgi = tech(26, n / FPS, 0.6); bga = np.concatenate([bgi, np.full((H, W, 1), 255, np.float32)], 2)
    warp_layer(out, basis, bga, X, Y, ww, hh, z, dim_blur=None)
    order = ['grid', 'site', 'bcui', 'main', 'label', 'sold', 'dots', 'adsk', 'tt', 'bc', 'risk', 'bid', 'sensor', 'ttui', 'bcblue', 'lss', 'photo']
    caps_by_z = {}
    for ln in CAPL: caps_by_z.setdefault(ln[0], []).append(ln)
    done_caps = set()
    for name in order:
        X, Y, ww, hh, z = wrect(name)
        if name == 'main': img = art_main(n)
        elif name == 'tt': img = art_tt(round(tt_morph(t) * 40) / 40)
        else: img = art(name, n)
        op = 1.0
        if name == 'sold':
            e = G1(cl((t - (wt('sold') - 0.05)) / 0.45)); op = cl(e * 1.5)
            if op <= 0: continue
        warp_layer(out, basis, img, X, Y, ww, hh, z, op=op, shadow=z < 0, dim_blur=(name == 'main'))
        # captions on this layer's plane go right after it (TT/BC captions after both logos are down)
        if name in ('main', 'bc'):
            for zz in ([0] if name == 'main' else [-120]):
                for ln in caps_by_z.get(zz, []):
                    can, cX0, cY0, cz = caption_canvas(ln, t)
                    warp_layer(out, basis, can, cX0, cY0, can.shape[1] / RSC, can.shape[0] / RSC, cz)
            if name == 'bc': draw_line(out, basis, t)                # same plane as the logos; nearer layers still cover it
    return out


def probes(t):
    basis = cam_basis(cam_at(t)); pts = []
    for name in ('main', 'tt', 'bc', 'photo', 'bg'):
        X, Y, ww, hh, z = wrect(name); pts += [[X, Y, z], [X + ww, Y + hh, z]]
    q, _ = project(basis, np.array(pts, np.float64)); return q


def n_subs(t):
    d = max(flow(t - 0.25 / FPS, 0.5 / FPS), float(np.abs(probes(t + 0.25 / FPS) - probes(t - 0.25 / FPS)).max()) * 0.5)
    h0, h1 = line_head_screen(t - 0.25 / FPS), line_head_screen(t + 0.25 / FPS)
    if h0 is not None and h1 is not None: d = max(d, float(np.hypot(*(h1 - h0))))   # the line's head blurs too
    return int(np.clip(math.ceil(d / 1.6), 1, 16)), d


def frame(n):
    t = n / FPS; J3.RNG_T[0] = t; ns, d = n_subs(t)
    if ns == 1: out = sub_frame(t, n)
    else:
        out = None
        for k in range(ns):
            f = sub_frame(t + (k / (ns - 1) - 0.5) * 0.5 / FPS, n); out = f if out is None else out + f
        out /= ns
    return fin16.finish(np.clip(J3.grain(out, 4.5, seed=n), 0, 255), vig=0.60, tex=0.35, rb=0.50)


SCR = np.array([[960, 540], [360, 240], [1560, 240], [360, 840], [1560, 840]], float)


def flow(t, dt=1 / 24):
    c = cam_at(t); b = cam_basis(c); b2 = cam_basis(cam_at(t + dt)); best = 0.0
    P, R, Dn, Fw, D = b
    for zp in (c['tz'], 0.0):
        Wp = []
        for x, y in SCR:
            d = Fw + R * (x - 960) / F + Dn * (y - 540) / F; s_ = (zp - P[2]) / d[2]; Wp.append(P + s_ * d)
        q, _ = project(b2, np.array(Wp)); best = max(best, float(np.hypot(*(q - SCR).T).max()))
    return best


def speed():
    rows = []
    for n in range(N0, N1):
        c = cam_at(n / FPS); rows.append((n, n / FPS, flow(n / FPS), c['yaw'], c['pitch'], F / math.exp(c['lD'])))
    vs = np.array([r[2] for r in rows]); acc = np.abs(np.diff(vs))
    spikes = [rows[k] for k in range(1, len(rows) - 1) if vs[k] > 1.35 * max(vs[k - 1], vs[k + 1]) + 1.0]
    for r in rows: print('%d %.3f  speed %6.1f px/f  yaw %+6.2f  pitch %+5.2f  zoom %.3f' % r)
    print('max speed %.1f px/f, max frame-to-frame change %.1f px/f, parked frames (<0.3 px/f) %d, spikes %d'
          % (vs.max(), acc.max(), int((vs < 0.3).sum()), len(spikes)), [(r[0], round(r[2], 1)) for r in spikes])


STILLS = [(15.70, 'Justin card, "construction software"', 1.30), (16.20, '"business." types on, pulling back', 2.00),
          (16.60, 'pull back + orbit toward TradeTapp', 2.95), (16.95, 'swinging in (3D)', 3.15),
          (17.45, 'TradeTapp, "We sold"', 3.55), (17.80, 'TradeTapp mark morph, "our business"', 4.10),
          (18.25, 'leaving TradeTapp, pull back + orbit', 5.10), (18.60, 'swinging onto BuildingConnected', 5.40),
          (19.00, 'BuildingConnected, "to"', 6.20), (19.45, 'end (cut to Autodesk)', 6.60)]


def stills():
    os.makedirs(A + 'stills_v3', exist_ok=True)
    for t, lab, rt in STILLS:
        Image.fromarray(frame(int(round(t * FPS)))).save(A + f'stills_v3/s_{t:05.2f}.png'); print('still', t, lab, flush=True)


def _chunk(args):
    i, a, b = args
    tmp = A + f'_chunks/c{i:02d}.mp4'
    p = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                          '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-pix_fmt', 'yuv420p', '-r', '24', tmp], stdin=subprocess.PIPE)
    for n in range(a, b): p.stdin.write(np.ascontiguousarray(frame(n)).tobytes())
    p.stdin.close(); p.wait(); return i


def render(out):
    import multiprocessing as mp
    os.makedirs(A + '_chunks', exist_ok=True)
    for f in os.listdir(A + '_chunks'): os.remove(A + '_chunks/' + f)
    nw = 8; cuts = [N0 + (N1 - N0) * i // nw for i in range(nw + 1)]
    with mp.get_context('fork').Pool(nw) as pool: pool.map(_chunk, [(i, cuts[i], cuts[i + 1]) for i in range(nw)])
    open(A + '_chunks/list.txt', 'w').write(''.join(f"file 'c{i:02d}.mp4'\n" for i in range(nw)))
    vo = A + '_chunks/video.mp4'
    subprocess.run([FF, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', A + '_chunks/list.txt', '-c', 'copy', vo], check=True)
    dur = (N1 - N0) / FPS
    subprocess.run([FF, '-v', 'error', '-y', '-i', vo, '-ss', f'{N0 / FPS:.4f}', '-t', f'{dur:.4f}', '-i', A + '../audio/mix.wav',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '320k', '-t', f'{dur:.4f}', '-movflags', '+faststart', out], check=True)
    print('done', out, N1 - N0, 'frames', dur, 's')


if __name__ == '__main__':
    m = sys.argv[1]
    if m == 'stills': stills()
    elif m == 'speed': speed()
    elif m == 'render': render(sys.argv[2])
    elif m == 'test':
        os.makedirs(A + 'stills_v3', exist_ok=True)
        for a in sys.argv[2:]:
            t = float(a); Image.fromarray(frame(int(round(t * FPS)))).save(A + f'stills_v3/t_{t:05.2f}.jpg', quality=90); print('t', t, flush=True)
