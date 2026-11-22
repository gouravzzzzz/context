"""15.66-19.55 s alt scene (Justin Levine trailer): Krish's Pinterest ref pin.it/2boBV7c90 ("Showcase (09)") in our look.
Justin's A-roll plays where the white-horse hero sits, inside a website-style card. Around it, at different depths:
photo tile, TradeTapp card, BuildingConnected pill, Autodesk tile, SOLD chip, dots, show-label pill.
Real 3D: every layer sits at depth o (fraction of the camera distance). One pinhole camera (centre C, main-plane scale S)
dollies in on Justin, travels to the TradeTapp card, whips to the BuildingConnected pill, then pulls back out, as in the ref.
Depth of field follows the camera focus. Captions are attached to their logo's layer, so they move with the camera.
Moves use Krish's graph EASE_USER with keyframe overlapping. Real motion blur (sub-frames) on the fast moves.
  python scene.py stills            -> stills/*.png + sheet
  python scene.py render out.mp4    -> the scene clip with the trailer mix (15.66-19.55)
"""
import sys, os, math, subprocess
sys.path.insert(0, '/Users/gourav/jl-trailer/trailer')
import numpy as np, cv2
from PIL import Image
from engine import *            # W, H, CX, CY, J3, L, EU, G1, G2, EIO, cl, spk_frame, vid, tech, fin16, wt, FPS

A = '/Users/gourav/jl-trailer/trailer/alt_15_19/'
AS = A + 'assets/'
FF = '/Users/gourav/ks-ron-build/reel1/ff'
T0, T1 = 15.66, 19.55
BLUE0, BLUE1 = (70, 255, 236), (40, 120, 255)          # trailer gradient (teal -> blue)
KEY0, KEY1 = (40, 132, 255), (16, 56, 214)             # key-box blues


def rgba(p):
    a = np.asarray(Image.open(p).convert('RGBA')).astype(np.float32)
    return a


# ---------------------------------------------------------------- layout (designed in the WIDE frame, screen px), depth o
# name: (o, cx, cy, w, h)
_L0 = {'main': (0.00, 960, 520, 900, 506), 'label': (0.00, 960, 236, 330, 38), 'chip': (0.04, 1418, 452, 118, 44),
       'dots': (0.06, 1462, 606, 60, 18), 'adsk': (0.08, 960, 915, 190, 118), 'tt': (0.12, 505, 745, 190, 240),
       'bc': (0.12, 1360, 800, 430, 96), 'photo': (0.24, 470, 245, 172, 172)}
GROW = 1.12                                            # the ref's wide fills ~90 % of the frame
LAY = {k: (o, 960 + (x - 960) * GROW, 540 + (y - 540) * GROW, w * GROW, h * GROW) for k, (o, x, y, w, h) in _L0.items()}


def world(name):
    """wide-frame design -> world rect (X0, Y0, w, h) on the layer's own depth (camera at S=1 looks at (960, 540))"""
    o, cx, cy, w, h = LAY[name]; s0 = 1 / (1 - o)
    X = 960 + (cx - 960) / s0; Y = 540 + (cy - 540) / s0
    return X - w / s0 / 2, Y - h / s0 / 2, w / s0, h / s0


def lscale(S, o): return 1.0 / (1.0 / S - o)


def to_screen(cam, o, X, Y):
    S, Cx, Cy = cam['S'], cam['cx'], cam['cy']; s = lscale(S, o)
    return 960 + s * (X - Cx), 540 + s * (Y - Cy), s


# ---------------------------------------------------------------- camera: keyframes + overlapped moves
def key_on(name, sx, sy, S):
    """camera centre that puts layer `name`'s centre at screen (sx, sy) at main-plane scale S"""
    X0, Y0, w, h = world(name); o = LAY[name][0]; s = lscale(S, o)
    return dict(lS=math.log(S), cx=X0 + w / 2 - (sx - 960) / s, cy=Y0 + h / 2 - (sy - 540) / s)


K0 = dict(lS=0.0, cx=960.0, cy=540.0, of=0.0, dof=0.05)
K1 = dict(lS=math.log(1.5), cx=960.0, cy=500.0, of=0.0, dof=1.0)                       # dolly in on Justin's card
K2 = dict(key_on('tt', 560, 500, 2.0), of=0.12, dof=1.0)                               # TradeTapp card + caption
K3 = dict(key_on('bc', 1180, 520, 2.0), of=0.12, dof=1.0)                              # BuildingConnected pill + caption
K4 = dict(lS=-0.10, cx=960.0, cy=544.0, of=0.0, dof=0.05)                              # back out to the wide (drifts add ~+0.12)
CH = ('lS', 'cx', 'cy', 'of', 'dof')
# (start, dur, delta dict, ease): travels are word-synced; the slow drifts start 20 % into the move before them
TRAV = [(15.92, 0.42, K0, K1), (17.02, 0.48, K1, K2), (18.38, 0.38, K2, K3), (19.12, 0.43, K3, K4)]
DRIFT = [(15.20, 1.40, dict(lS=0.030, cx=-6)), (16.00, 1.30, dict(lS=0.035, cx=8, cy=-4)), (17.12, 1.40, dict(lS=0.035, cx=-8)),
         (18.46, 1.00, dict(lS=0.025, cx=6))]


def cam_at(t):
    c = dict(K0)
    for t0, d, a, b in TRAV:
        e = EU(cl((t - t0) / d))
        for k in CH: c[k] += (b[k] - a[k]) * e
    for t0, d, dl in DRIFT:
        e = EU(cl((t - t0) / d))
        for k, v in dl.items(): c[k] += v * e
    c['S'] = math.exp(c['lS'])
    return c


def sigma(cam, o): return cam['dof'] * 75.0 * abs(o - cam['of']) * cam['S']


# ---------------------------------------------------------------- layer art (RGBA float, straight alpha 0..255, rendered at RS px / world unit)
def rrect_mask(w, h, r):
    m = np.zeros((h, w), np.uint8); r = int(r)
    cv2.rectangle(m, (r, 0), (w - 1 - r, h - 1), 255, -1); cv2.rectangle(m, (0, r), (w - 1, h - 1 - r), 255, -1)
    for cx_, cy_ in ((r, r), (w - 1 - r, r), (r, h - 1 - r), (w - 1 - r, h - 1 - r)): cv2.circle(m, (cx_, cy_), r, 255, -1, cv2.LINE_AA)
    return m.astype(np.float32)


def border(img, m, col=(255, 255, 255), a=0.14, th=2):
    e = cv2.morphologyEx((m > 127).astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((th * 2 + 1, th * 2 + 1), np.uint8)).astype(np.float32)
    e = cv2.GaussianBlur(e, (0, 0), 0.8) * (m / 255)
    img[..., :3] = img[..., :3] * (1 - a * e[..., None]) + np.array(col, np.float32) * a * e[..., None]


def paste(dst, src, x, y):
    """alpha-over a straight-alpha RGBA src onto an RGBA dst at (x, y)"""
    h, w = src.shape[:2]; x, y = int(round(x)), int(round(y))
    xa, ya, xb, yb = max(0, x), max(0, y), min(dst.shape[1], x + w), min(dst.shape[0], y + h)
    if xb <= xa or yb <= ya: return
    s = src[ya - y:yb - y, xa - x:xb - x]; a = s[..., 3:4] / 255
    d = dst[ya:yb, xa:xb]; d[..., :3] = d[..., :3] * (1 - a) + s[..., :3] * a; d[..., 3:4] = d[..., 3:4] * (1 - a) + 255 * a


def text_img(txt, px, face='reg', fill=(255, 255, 255)):
    rg, asc = J3.text_rgba(txt, px, face, fill, 1.0)                  # premultiplied 0..1
    a = rg[..., 3:4]; rgb = np.where(a > 1e-4, rg[..., :3] / np.maximum(a, 1e-4), 0)
    return np.concatenate([rgb * 255, a * 255], 2).astype(np.float32), asc


def logo_h(p, h):
    im = rgba(p); s = h / im.shape[0]
    return cv2.resize(im, (max(1, int(im.shape[1] * s)), int(h)), interpolation=cv2.INTER_AREA)


def logo_w(p, w):
    im = rgba(p); s = w / im.shape[1]
    return cv2.resize(im, (int(w), max(1, int(im.shape[0] * s))), interpolation=cv2.INTER_AREA)


def grad_img(w, h, c0, c1):
    u = np.linspace(0, 1, w, dtype=np.float32)[None, :, None]
    return np.broadcast_to(np.array(c0, np.float32) * (1 - u) + np.array(c1, np.float32) * u, (h, w, 3)).copy()


_ART = {}
RS = {'main': 2.2, 'label': 2.2, 'chip': 2.6, 'dots': 2.6, 'adsk': 2.8, 'tt': 3.0, 'bc': 2.9, 'photo': 4.6}


def art_static(name):
    if name in _ART: return _ART[name]
    X0, Y0, w, h = world(name); rs = RS[name]; pw, ph = int(round(w * rs)), int(round(h * rs))
    img = np.zeros((ph, pw, 4), np.float32)
    if name == 'label':
        m = rrect_mask(pw, ph, ph / 2); img[..., :3] = (20, 21, 25); img[..., 3] = m; border(img, m, a=0.22)
        t, asc = text_img('Verticals  ·  a weekly biz show', int(15.5 * rs), fill=(222, 226, 232))
        paste(img, t, (pw - t.shape[1]) / 2, (ph - t.shape[0]) / 2 + 1)
    elif name == 'chip':
        m = rrect_mask(pw, ph, ph / 2); img[..., :3] = (16, 17, 20); img[..., 3] = m
        g = grad_img(pw, ph, BLUE0, BLUE1); e = cv2.morphologyEx((m > 127).astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((5, 5), np.uint8)).astype(np.float32)[..., None]
        img[..., :3] = img[..., :3] * (1 - e) + g * e
        t, asc = text_img('SOLD', int(19 * rs), fill=(240, 244, 248)); paste(img, t, (pw - t.shape[1]) / 2, (ph - t.shape[0]) / 2 + 1)
    elif name == 'dots':
        for i, c in enumerate((BLUE0, BLUE1)):
            cv2.circle(img, (int(ph / 2 + i * (pw - ph)), int(ph / 2)), int(ph / 2 - 1), (*c, 255), -1, cv2.LINE_AA)
    elif name == 'adsk':
        m = rrect_mask(pw, ph, 10 * rs); img[..., :3] = (18, 19, 23); img[..., 3] = m; border(img, m, a=0.16)
        lg = logo_w(L.ROOT + '/assets/logos/Autodesk_Logo_2021_dk.png', pw * 0.66); paste(img, lg, (pw - lg.shape[1]) / 2, (ph - lg.shape[0]) / 2)
    elif name == 'bc':
        m = rrect_mask(pw, ph, ph / 2); img[..., :3] = grad_img(pw, ph, KEY0, KEY1); img[..., 3] = m
        sh = np.zeros_like(img[..., 0]); sh[: ph // 2] = 1; img[..., :3] += 18 * cv2.GaussianBlur(sh, (0, 0), ph / 5)[..., None] * (m[..., None] / 255)
        border(img, m, a=0.28, th=2)
        lg = logo_w(AS + 'bc_logo_white.png', pw * 0.74); paste(img, lg, (pw - lg.shape[1]) / 2, (ph - lg.shape[0]) / 2)
    elif name == 'photo':
        f = L.grade(vid('c_lumi_28').at(1.2)); c = L.fit(f, pw, ph, 0.30, 0.42, 1.10)
        m = rrect_mask(pw, ph, 10 * rs); img[..., :3] = c; img[..., 3] = m; border(img, m, a=0.18)
    _ART[name] = img
    return img


def art_tt(m_):
    """TradeTapp card; m_ in [0, 1] = the mark's morph (squash to the baseline, swap white -> gradient, grow back)"""
    k = ('tt', round(m_, 3))
    if k in _ART: return _ART[k]
    X0, Y0, w, h = world('tt'); rs = RS['tt']; pw, ph = int(round(w * rs)), int(round(h * rs))
    img = np.zeros((ph, pw, 4), np.float32); m = rrect_mask(pw, ph, 12 * rs); img[..., :3] = (17, 18, 22); img[..., 3] = m
    border(img, m, a=0.16)
    pad = 13 * rs
    wd = logo_h(AS + 'tt_word.png', 10.5 * rs); paste(img, wd, pad, pad)
    t, asc = text_img('Construction software', int(9.5 * rs), fill=(150, 156, 166)); paste(img, t, pad, pad + wd.shape[0] + 5 * rs)
    tg = np.zeros((int(17 * rs), int(30 * rs), 4), np.float32); tm = rrect_mask(tg.shape[1], tg.shape[0], tg.shape[0] / 2)
    tg[..., :3] = (44, 47, 54); tg[..., 3] = tm; tt_, _ = text_img('01', int(9.5 * rs), fill=(210, 214, 220))
    paste(tg, tt_, (tg.shape[1] - tt_.shape[1]) / 2, (tg.shape[0] - tt_.shape[0]) / 2 + 1); paste(img, tg, pw - pad - tg.shape[1], pad - 2 * rs)
    # the big mark (the ref's "Aa"), baseline-anchored
    mk = logo_w(AS + 'tt_mark.png', pw * 0.62)
    sy = (1 - 0.9 * EIO(cl(2 * m_))) if m_ < 0.5 else (0.1 + 0.9 * EIO(cl(2 * m_ - 1)))
    if m_ >= 0.5:
        g = grad_img(mk.shape[1], mk.shape[0], BLUE0, BLUE1); mk = mk.copy(); mk[..., :3] = g
    mh = max(2, int(mk.shape[0] * sy)); mk = cv2.resize(mk, (mk.shape[1], mh), interpolation=cv2.INTER_AREA)
    base = ph - 20 * rs
    paste(img, mk, (pw - mk.shape[1]) / 2, base - mh)
    if len(_ART) > 60: _ART.pop(next(iter(_ART)))
    _ART[k] = img
    return img


def art_main(n):
    """the website hero card with Justin's A-roll in place of the white horse"""
    X0, Y0, w, h = world('main'); rs = RS['main']; pw, ph = int(round(w * rs)), int(round(h * rs))
    f = cv2.resize(spk_frame(n), (pw, ph), interpolation=cv2.INTER_AREA)
    y = np.linspace(0, 1, ph, dtype=np.float32)[:, None, None]
    xg = np.linspace(0, 1, pw, dtype=np.float32)[None, :, None]
    f = f * (1 - 0.62 * np.clip((y - 0.55) / 0.45, 0, 1) ** 1.4) * (1 - 0.35 * np.clip((0.16 - y) / 0.16, 0, 1))
    ux = np.clip((0.58 - xg) / 0.32, 0, 1); uy = np.clip((0.66 - y) / 0.28, 0, 1)
    sh_ = (ux * ux * (3 - 2 * ux)) * (uy * uy * (3 - 2 * uy))
    f = f * (1 - 0.70 * sh_)                                                                    # headline side
    img = np.zeros((ph, pw, 4), np.float32); m = rrect_mask(pw, ph, 16 * rs); img[..., :3] = f; img[..., 3] = m
    pad = 24 * rs
    if 'shep' not in _ART: _ART['shep'] = logo_h(L.ROOT + '/assets/logos/shepherd_dk.png', 17 * rs)
    paste(img, _ART['shep'], 0.075 * pw, pad)
    xx = pw - pad
    for lab in ('Construction', 'Insurance'):
        t, _ = text_img(lab, int(12 * rs), fill=(208, 212, 218)); xx -= t.shape[1]; paste(img, t, xx, pad + 2 * rs); xx -= 26 * rs
    border(img, m, a=0.18)
    return img


# ---------------------------------------------------------------- text items attached to layers (world anchor on the layer's depth)
# (layer, dx, dy (world, from the layer's left/right edge or centre), world px, txt, kind, align, t_on, t_off)
def caps():
    Xm, Ym, wm, hm = world('main'); Xt, Yt, wt_, ht = world('tt'); Xb, Yb, wb, hb = world('bc')
    return [
        ('main', Xm + 0.075 * wm, Ym + 0.285 * hm, 30, 'construction software', 'put', 'left', T0 - 0.04, 17.00),
        ('main', Xm + 0.072 * wm, Ym + 0.285 * hm + 64, 60, 'business.', 'grad', 'left', wt('business', 16) - 0.05, 17.00),
        ('tt', Xt + wt_ + 20, Yt + ht * 0.5 + 40, 44, 'We sold', 'grad', 'left', wt('we', 17) - 0.05, 18.36),
        ('tt', Xt + wt_ + 22, Yt + ht * 0.5 + 78, 27, 'our business', 'it', 'left', wt('our', 17.5) - 0.05, 18.36),
        ('bc', Xb - 20, Yb + hb / 2 + 15, 42, 'to', 'it', 'right', wt('to', 18.3) - 0.05, None)]


CAPS = None


def cap_op(t_on, t_off, t):
    o = EIO(cl((t - t_on) / 0.17))
    if t_off is not None: o *= 1 - EIO(cl((t - t_off) / 0.22))
    return o


def draw_caption(out, cam, c, t):
    layer, X, Y, wpx, txt, kind, align, t_on, t_off = c
    op = cap_op(t_on, t_off, t)
    if op <= 0.003: return
    o = LAY[layer][0]; x, y, s = to_screen(cam, o, X, Y); px = max(6, int(round(wpx * s)))
    if x < -2000 or x > 4000: return
    P0 = np.zeros_like(out); P1 = np.full_like(out, 200.0)
    for P in (P0, P1):
        if kind == 'grad': L.grad_text(P, txt, px, x, y, align=align, glow=0.30)
        else: L.put_text(P, txt, px, x, y, align=align, face='it' if kind == 'it' else 'reg', glow=0.18)
    M = (P1 - P0) / 200.0; C = P0; sg = sigma(cam, o)
    if sg > 0.6: M = 1 - cv2.GaussianBlur(1 - M, (0, 0), sg); C = cv2.GaussianBlur(C, (0, 0), sg)
    M = 1 - op * (1 - M); C = C * op
    out *= M; out += C


# ---------------------------------------------------------------- compose one sub-frame
def comp_layer(out, cam, name, img, op=1.0, pop=1.0):
    X0, Y0, w, h = world(name); o = LAY[name][0]; rs = img.shape[1] / w
    S = cam['S']; s = lscale(S, o) * pop
    cxw, cyw = X0 + w / 2, Y0 + h / 2
    k = s / rs
    xs, ys, _ = to_screen(cam, o, cxw, cyw)
    M = np.float32([[k, 0, xs - k * img.shape[1] / 2], [0, k, ys - k * img.shape[0] / 2]])
    src = img
    if k < 0.6: src = cv2.GaussianBlur(img, (0, 0), 0.45 / k)                      # pre-filter big downscales
    pm = src.copy(); pm[..., :3] *= pm[..., 3:4] / 255
    q = np.float32([[0, 0], [img.shape[1], 0], [0, img.shape[0]], [img.shape[1], img.shape[0]]]) @ M[:, :2].T + M[:, 2]
    sg = sigma(cam, o); pad = int(3 * sg) + 4
    xa, ya = int(max(0, q[:, 0].min() - pad)), int(max(0, q[:, 1].min() - pad))
    xb, yb = int(min(W, q[:, 0].max() + pad)), int(min(H, q[:, 1].max() + pad))
    if xb <= xa or yb <= ya: return
    Ml = M.copy(); Ml[0, 2] -= xa; Ml[1, 2] -= ya
    lay = cv2.warpAffine(pm, Ml, (xb - xa, yb - ya), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    if sg > 0.6: lay = cv2.GaussianBlur(lay, (0, 0), sg)
    a = lay[..., 3:4] / 255 * op
    if name == 'main' and sg > 0.6: lay[..., :3] *= 1 - 0.28 * min(1.0, sg / 18)             # out-of-focus card falls back
    # soft contact shadow under every floating layer
    if o > 0:
        sh = cv2.GaussianBlur(lay[..., 3], (0, 0), 10 + sg) / 255 * 0.55 * op
        d = out[ya:yb, xa:xb]; d *= (1 - sh[..., None])
    d = out[ya:yb, xa:xb]; d[:] = d * (1 - a) + lay[..., :3] * op


def tt_morph(t):
    return cl((t - 17.72) / 0.50)


def sub_frame(t, tf, n):
    """t = camera/animation time of this sub-frame, tf = footage time (the frame's)"""
    global CAPS
    if CAPS is None: CAPS = caps()
    cam = cam_at(t)
    # background: far tech ground, slow parallax
    bg = tech(26, tf, 0.62); kz = 1 + 0.22 * (cam['S'] - 1)
    bx, by = 960 + 0.22 * (cam['cx'] - 960), 540 + 0.22 * (cam['cy'] - 540)
    out = cv2.warpAffine(bg, mat(kz, bx, by, 960, 540), (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    comp_layer(out, cam, 'main', art_main(int(round(tf * FPS))))
    comp_layer(out, cam, 'label', art_static('label'))
    for c in CAPS:
        if c[0] == 'main': draw_caption(out, cam, c, t)
    chip_e = G1(cl((t - (wt('sold') - 0.05)) / 0.40))
    if chip_e > 0: comp_layer(out, cam, 'chip', art_static('chip'), op=cl(chip_e * 1.5), pop=0.8 + 0.2 * chip_e)
    comp_layer(out, cam, 'dots', art_static('dots'))
    comp_layer(out, cam, 'adsk', art_static('adsk'))
    comp_layer(out, cam, 'tt', art_tt(round(tt_morph(t) * 40) / 40))
    comp_layer(out, cam, 'bc', art_static('bc'))
    for c in CAPS:
        if c[0] in ('tt', 'bc'): draw_caption(out, cam, c, t)
    comp_layer(out, cam, 'photo', art_static('photo'))
    return out


def n_subs(t):
    h = 0.25 / FPS; a, b = cam_at(t - h), cam_at(t + h); d = 0.0
    for name in ('main', 'tt', 'photo'):
        X0, Y0, w, hh = world(name); o = LAY[name][0]
        for (X, Y) in ((X0, Y0), (X0 + w, Y0 + hh)):
            xa, ya, _ = to_screen(a, o, X, Y); xb, yb, _ = to_screen(b, o, X, Y); d = max(d, abs(xa - xb), abs(ya - yb))
    return int(np.clip(math.ceil(d / 2.0), 1, 16)), d


def frame(n):
    t = n / FPS; J3.RNG_T[0] = t; ns, d = n_subs(t)
    if ns == 1: out = sub_frame(t, t, n)
    else:
        out = None
        for k in range(ns):
            ts = t + (k / (ns - 1) - 0.5) * 0.5 / FPS
            f = sub_frame(ts, t, n); out = f if out is None else out + f
        out /= ns
    return fin16.finish(np.clip(J3.grain(out, 4.5, seed=n), 0, 255), vig=0.60, tex=0.35, rb=0.50)


STILLS = [(15.70, 'wide, "software"', 0.10), (16.10, 'dolly in on Justin (mid-move)', 1.05),
          (16.55, 'Justin card, "business."', 2.00), (17.26, 'travel to TradeTapp (mid-move)', 3.00),
          (17.62, 'TradeTapp, "We sold"', 3.50), (17.97, 'TradeTapp mark morph', 4.00), (18.30, '"our business"', 4.80),
          (18.56, 'whip to BuildingConnected (mid-move)', 5.25), (19.02, 'BuildingConnected, "to"', 6.20),
          (19.42, 'pull back out (hand-off to 02g)', 7.75)]


def stills():
    os.makedirs(A + 'stills', exist_ok=True)
    for t, lab, rt in STILLS:
        n = int(round(t * FPS)); img = frame(n)
        Image.fromarray(img).save(A + f'stills/s_{t:05.2f}.png'); print('still', t, lab, flush=True)


def render(out):
    n0, n1 = int(round(T0 * FPS)), int(round(T1 * FPS))
    tmp = A + '_video.mp4'
    p = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                          '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for n in range(n0, n1):
        p.stdin.write(np.ascontiguousarray(frame(n)).tobytes())
        if (n - n0) % 12 == 0: print('frame', n - n0, '/', n1 - n0, flush=True)
    p.stdin.close(); p.wait()
    dur = (n1 - n0) / FPS
    subprocess.run([FF, '-v', 'error', '-y', '-i', tmp, '-ss', f'{n0 / FPS:.4f}', '-t', f'{dur:.4f}', '-i', A + '../audio/mix.wav',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '320k', '-t', f'{dur:.4f}', '-movflags', '+faststart', out], check=True)
    os.remove(tmp); print('done', out, n1 - n0, 'frames', dur, 's')


if __name__ == '__main__':
    if sys.argv[1] == 'stills': stills()
    elif sys.argv[1] == 'render': render(sys.argv[2])
    elif sys.argv[1] == 'test':
        for a in sys.argv[2:]:
            t = float(a); Image.fromarray(frame(int(round(t * FPS)))).save(A + f'stills/t_{t:05.2f}.jpg', quality=90); print('t', t)
