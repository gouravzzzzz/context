"""v2 seg 10 -- NEW frames 971-1189: 05a_tv ('Progressive was the one that started...'), 05bc_counter ('50 data points per
underwriting submission to, thousands.'), 05d_commercial ('And I just think we can do the same thing in commercial.').
Hard cut in at 971, hard cuts between the three shots (no zoom-through), hard cut out at 1189.
Krish v1 notes:
  05a  -> new clean cut-out: front-on Sony Trinitron KV-27 photo, perspective-rectified, geometric rounded-rect matte,
          the Progressive spots composited inside the measured glass (bulge, scanlines, glass sheen). Smooth camera only.
  05bc -> '50 to THOUSANDS' frame dropped; the '4,000 data points / per underwriting submission' + glowing dot grid holds the
          whole shot, the number counts live 50 -> 4,000 (eased, log scale), landing as 'thousands.' lands.
  05d  -> every caption centred (x and y), big, one phrase at a time; 'commercial.' types on in the blue key box.
  python seg10_tv_counter.py stills n1 n2 ...  |  render  |  check
"""
import sys, os, math, json, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw
sys.path.insert(0, '/Users/gourav/jl-trailer/trailer')
from engine import *
from newtime import WORDS as WN

E_PATCH = None
N0, N1 = 971, 1189
OUTD = HERE + 'v2segs/'
NAME = '10_tv_counter'
FFX = '/Users/gourav/ks-ron-build/reel1/ff'
ASSET = '/Users/gourav/jl-trailer/assets/tv2/'
RMX = 1785
I2 = np.float32([[1, 0, 0], [0, 1, 0]])


def wn(txt, after=0.0):
    return next(w[0] for w in WN if w[2] == txt and w[0] >= after - 1e-6)


TA0, TA1 = N0 / FPS, 1040 / FPS
TB0, TB1 = 1040 / FPS, 1121 / FPS
TC0, TC1 = 1121 / FPS, N1 / FPS


# ---------------------------------------------------------------- footage: unique frames only (screen-recorded B-roll has dups)
_UQ = {}
DUPT = {'c_cyrus_33': 1.2, 'c_aligned_31': 1.2, 'c_oracle_44': 1.2}   # these repeat frames with codec noise (0.4-1.1 diff)
def uniq(name):
    if name not in _UQ:
        c = cv2.VideoCapture(BRV + name + '.mp4'); prev = None; keep = []; i = 0
        while True:
            ok, f = c.read()
            if not ok: break
            g = cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (320, 180)).astype(np.float32)
            if prev is None or np.abs(g - prev).mean() >= DUPT.get(name, 0.3): keep.append(i)
            prev = g; i += 1
        _UQ[name] = keep
    return _UQ[name]


def clip_at(name, u):
    """frame of clip at clip-time u (s), stepping through its unique frames at the source rate"""
    k = uniq(name); j = int(round(u * 30.0))
    return vid(name).frame(k[min(len(k) - 1, max(0, j))])


# ---------------------------------------------------------------- words (Dime word build) -- from alt_20/scene_adsk.py
class WordItem(Item):
    """one word: fades in over ~3 frames while rising 14 px and its blur clears, laid out in place"""
    def __init__(s, t_on, draw_at, t_off, fout=0.10):
        super().__init__(t_on - 0.06, None, t_off=t_off, fin=3 / FPS, fout=fout,
                         anim=lambda t, t_on=t_on: round(cl((t - (t_on - 0.06)) / (4 / FPS)) * 8) / 8)
        s.draw_at = draw_at
    def mc(s, a=None):
        if a in s.cache: return s.cache[a]
        e = G1(a); dy = 14 * (1 - e); sig = 3.5 * (1 - e)
        P0 = np.zeros((H, W, 3), np.float32); P1 = np.full((H, W, 3), 200.0, np.float32)
        s.draw_at(P0, dy); s.draw_at(P1, dy)
        M = (P1 - P0) / 200.0; C = P0
        if sig > 0.4: M = cv2.GaussianBlur(M, (0, 0), sig); C = cv2.GaussianBlur(C, (0, 0), sig)
        act = (np.abs(M - 1).max(2) > 2e-3) | (C.max(2) > 0.3); ys, xs = np.where(act)
        r = None if len(ys) == 0 else (xs.min(), ys.min(), np.ascontiguousarray(M[ys.min():ys.max() + 1, xs.min():xs.max() + 1]),
                                         np.ascontiguousarray(C[ys.min():ys.max() + 1, xs.min():xs.max() + 1]))
        s.cache[a] = r
        return r


class TypeItem(Item):
    """hero word typed on letter by letter (1 letter / frame, soft leading edge); draw(d) paints the finished word,
    edges = x of each letter boundary on screen"""
    def __init__(s, t_on, draw, edges, t_off=None, fout=0.10):
        s.edges = edges; nl = len(edges) - 1; s.fullmc = None; s.wdraw = draw
        super().__init__(t_on - 0.04, None, t_off=t_off, fin=0.0, fout=fout,
                         anim=lambda t: round(cl((t - (t_on - 0.04)) * FPS / nl) * nl * 2) / 2)
    def mc(s, a=None):
        if a in s.cache: return s.cache[a]
        if s.fullmc is None:
            P0 = np.zeros((H, W, 3), np.float32); P1 = np.full((H, W, 3), 200.0, np.float32)
            s.wdraw(P0); s.wdraw(P1); s.fullmc = ((P1 - P0) / 200.0, P0)
        M, C = s.fullmc; nl = len(s.edges) - 1
        k = int(a); fr = a - k
        if k >= nl: Mm, Cm = M, C
        else:
            xr = np.arange(W, dtype=np.float32); e0 = s.edges[k]; e1 = s.edges[k + 1]
            mask = np.where(xr < e0, 1.0, np.where(xr < e1, fr, 0.0)).astype(np.float32)
            mask = cv2.GaussianBlur(mask[None, :], (0, 0), 6)[0]
            m3 = mask[None, :, None]; Mm = 1 - m3 * (1 - M); Cm = C * m3
        act = (np.abs(Mm - 1).max(2) > 2e-3) | (Cm.max(2) > 0.3); ys, xs = np.where(act)
        r = None if len(ys) == 0 else (xs.min(), ys.min(), np.ascontiguousarray(Mm[ys.min():ys.max() + 1, xs.min():xs.max() + 1]),
                                         np.ascontiguousarray(Cm[ys.min():ys.max() + 1, xs.min():xs.max() + 1]))
        s.cache[a] = r
        return r


def line_words(words, px, x, by, align, face='reg', glow=0.20, t_off=None, fout=0.10):
    """caption line: each word lands at its own time, laid out once for the whole line (aligned by side)"""
    sp = J3.font(px, face).getlength(' ') * 0.95; lay = []; xx = 0.0
    for tw, w in words:
        rg = J3.text_rgba(w, px, face, hs=1.0)[0]; lay.append((tw, w, xx)); xx += rg.shape[1] + sp
    lw = xx - sp; x0 = x if align == 'left' else (x - lw if align == 'right' else x - lw / 2)
    return [WordItem(tw, lambda d, dy, w=w, wx=x0 + xo: L.put_text(d, w, px, wx, by + dy, face=face, glow=glow), t_off, fout)
            for tw, w, xo in lay]


def text_edges(word, px, x0, face='reg'):
    f = J3.font(px, face); return [x0 + f.getlength(word[:k]) for k in range(len(word) + 1)]


# ---------------------------------------------------------------- shots (NEW time)
class Sh:
    TF = 1.0
    def __init__(s, name, t0, t1, kind, dz, dur=3.0, pans=None, z0=1.0):
        s.name, s.t0, s.t1, s.kind, s.z0 = name, t0, t1, kind, z0
        s.moves = chain(t0, t1, dz, dur, pans); s.items = []
    def cam(s, ts):
        dz = dx = dy = 0.0
        for m in s.moves:
            a, b, c = m.at(ts); dz += a; dx += b; dy += c
        return mat(s.z0 * math.exp(dz), CX, CY, CX + dx, CY + dy)
    def text_T(s, ts):
        A = np.vstack([s.cam(ts), [0, 0, 1]]); R = np.vstack([s.cam(s.t0), [0, 0, 1]])
        Mrel = (A @ np.linalg.inv(R))[:2]
        return (I2 + s.TF * (Mrel - I2)).astype(np.float32)
    def shade(s, ts): return None
    def plate(s, tf): raise NotImplementedError


# ================================================================ 05a TV
TVG = json.load(open(ASSET + 'kv27_front.json'))
TVW = 1090                                    # on-plate width; text column on the right (right-aligned at RMX)
TVCX, TVCY = 676, 540
_TV = {}
def tv_assets():
    if not _TV:
        body = L.load_rgba(ASSET + 'kv27_front_cut.png')            # premultiplied
        bw, bh = TVG['size']; s = TVW / bw; th = int(round(bh * s))
        body = cv2.resize(body, (TVW, th), interpolation=cv2.INTER_AREA)
        gx, gy, gw, gh = [v * s for v in TVG['glass']]
        x0, y0, x1, y1 = int(round(gx)), int(round(gy)), int(round(gx + gw)), int(round(gy + gh))
        sw, sh_ = x1 - x0, y1 - y0
        # rounded glass mask (AA, 4x), radius from the photo
        S4 = 4; rr = int(TVG['radius'] * s * S4); mk = np.zeros((sh_ * S4, sw * S4), np.uint8)
        cv2.rectangle(mk, (rr, 0), (sw * S4 - rr, sh_ * S4), 255, -1); cv2.rectangle(mk, (0, rr), (sw * S4, sh_ * S4 - rr), 255, -1)
        for cx, cy in [(rr, rr), (sw * S4 - rr, rr), (rr, sh_ * S4 - rr), (sw * S4 - rr, sh_ * S4 - rr)]:
            cv2.circle(mk, (cx, cy), rr, 255, -1, cv2.LINE_AA)
        m = cv2.resize(mk.astype(np.float32) / 255, (sw, sh_), interpolation=cv2.INTER_AREA)
        # CRT bulge map (centre magnified ~5 %, corners pinned), edge falloff, glass sheen
        yy, xx = np.mgrid[0:sh_, 0:sw].astype(np.float32)
        nx = (xx + 0.5) / sw * 2 - 1; ny = (yy + 0.5) / sh_ * 2 - 1; r2 = nx * nx + ny * ny
        k = 0.95 + 0.05 * r2 / 2
        mapx = ((nx * k + 1) / 2 * sw - 0.5).astype(np.float32); mapy = ((ny * k + 1) / 2 * sh_ - 0.5).astype(np.float32)
        ex = np.minimum(xx, sw - 1 - xx) / sw; ey = np.minimum(yy, sh_ - 1 - yy) / sh_
        edge = np.clip(np.minimum(ex / 0.06, ey / 0.08), 0, 1); edge = edge * edge * (3 - 2 * edge)
        vig = (0.62 + 0.38 * edge) * (1 - 0.10 * r2 / 2)
        scan = np.ones((sh_, 1), np.float32); scan[::3] = 0.88
        refl = np.asarray(Image.open(ASSET + 'kv27_glass_refl.png')).astype(np.float32) / 255
        refl = cv2.resize(refl, (sw, sh_), interpolation=cv2.INTER_AREA)
        sheen = np.clip(1.0 - (xx / sw * 0.9 + yy / sh_ * 1.1), 0, 1) ** 2.2 * 0.10          # soft top-left highlight
        _TV.update(body=body, box=(x0, y0, sw, sh_), m=m, mapx=mapx, mapy=mapy, vig=(vig * scan)[..., None],
                   glass=(refl * 0.10 + sheen)[..., None] * 255)
    return _TV


def tv_draw(d, content):
    A = tv_assets(); x0, y0, sw, sh_ = A['box']
    scr = L.fit(content, sw, sh_)
    scr = cv2.remap(scr, A['mapx'], A['mapy'], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    scr = cv2.GaussianBlur(scr, (0, 0), 0.6)
    scr = np.clip(scr * 0.94 + 6, 0, 255) * A['vig']
    scr = 255 - (255 - scr) * (255 - A['glass']) / 255                             # glass reflection (screen blend)
    lay = A['body'].copy(); m = A['m'][..., None]
    reg = lay[y0:y0 + sh_, x0:x0 + sw]
    reg[..., :3] = reg[..., :3] * (1 - m) + scr / 255 * m
    th, tw = lay.shape[:2]; X, Y = TVCX - tw / 2, TVCY - th / 2
    J3.drop_shadow(d, lay, X, Y, 1.0, strength=0.65)
    J3.glow_screen(d, scr * 0.5, 34, 0.16, X + x0, Y + y0)                          # faint CRT light spill on the ground
    J3.over(d, lay, X, Y)


T_SPOT2 = 42.258                              # v1's cut inside the screen (old 47.55) on the NEW timeline
class TV(Sh):
    def plate(s, tf):
        d = tech(27, tf)
        img = clip_at('c_prog90s_28', 0.50 + tf - s.t0) if tf < T_SPOT2 else clip_at('c_prog99_60', 0.30 + tf - T_SPOT2)
        tv_draw(d, img)
        return d


def s05a():
    sh = TV('05a_tv', TA0, TA1, 'gfx', 0.05)
    tp = wn('Progressive'); px = 120
    x0 = RMX - J3.font(px).getlength('Progressive')
    sh.items = [TypeItem(tp, lambda d: L.grad_text(d, 'Progressive', px, x0, 470, glow=0.32), text_edges('Progressive', px, x0))]
    sh.items += line_words([(wn('was', 41), 'was'), (wn('the', 41.1), 'the'), (wn('one', 41.3), 'one')], 62, RMX, 562, 'right', 'it')
    sh.items += line_words([(wn('that', 41.5), 'that'), (wn('started', 41.7), 'started')], 62, RMX, 634, 'right')
    return sh


# ================================================================ 05bc counter: 4,000 + dot grid, counting live
T50, TTH = wn('50'), wn('thousands.')
TTH1 = next(w[1] for w in WN if w[2] == 'thousands.')
CA0, CA1 = T50 + 0.25, 45.75                  # slow creep while he says '50 data points per underwriting submission'
CB0, CB1 = 45.22, TTH1 - 0.02                 # the climb on 'to, thousands' (overlapped, Krish's graph), lands on the word
PA = 0.22
def pcount(t): return PA * EU(cl((t - CA0) / (CA1 - CA0))) + (1 - PA) * EU(cl((t - CB0) / (CB1 - CB0)))
def num_at(t):
    p = pcount(t)
    if p >= 0.99999: return 4000
    v = 50 * 80 ** p
    return int(v) if v < 1000 else min(3990, int(v // 10) * 10)
def lit_at(t):
    a = EU(cl((t - (T50 - 0.06)) / 0.55))                       # 0 -> 50 points light as '50' lands
    return 50 * a * (308 / 50) ** pcount(t)

NPX, NCX, NBY = 300, 470, 640
SLOT = 124.0                                                    # tabular digits (Instrument Serif digits are proportional)
def n_adv(ch): return SLOT if ch.isdigit() else J3.font(NPX).getlength(ch)
def n_width(sv): return sum(n_adv(c) for c in sv)
# smooth centring: the block width eases between digit counts instead of jumping
_WEV = []
def _wevents():
    if not _WEV:
        prev = n_width(f'{num_at(TB0):,}')
        for tt in np.arange(TB0, TB1 + 0.01, 1 / (FPS * 8)):
            w = n_width(f'{num_at(tt):,}')
            if w != prev: _WEV.append((tt, prev, w)); prev = w
    return _WEV
def width_s(t):
    ev = _wevents()
    w = ev[0][1] if ev else n_width('50')
    for tc, a, b in ev: w += (b - a) * EIO(cl((t - tc) / 0.22))
    return w


def num_draw(d, a):
    sv, xl = a
    f = J3.font(NPX); asc, desc = f.getmetrics(); pad = 40
    wid = int(n_width(sv)) + 2 * pad; im = Image.new('L', (wid, asc + desc + 20), 0); dr = ImageDraw.Draw(im); x = pad
    for c in sv:
        dr.text((x + (n_adv(c) - f.getlength(c)) / 2, asc), c, font=f, fill=255, anchor='ls'); x += n_adv(c)
    al = np.asarray(im).astype(np.float32) / 255
    g = J.grad(al.shape[1], al.shape[0], (70, 255, 236), (40, 120, 255)) / 255
    lay = np.zeros(al.shape + (4,), np.float32); lay[..., :3] = g * al[..., None]; lay[..., 3] = al
    X, Y = xl - pad, NBY - asc
    J3.drop_shadow(d, lay, X, Y, 1.0, strength=0.75)
    J3.glow_screen(d, lay[..., :3] * 255, 18, 0.30, X, Y)
    J3.over(d, lay, X, Y)


class NumItem(Item):
    def __init__(s):
        super().__init__(T50 - 0.06, num_draw, fin=4 / FPS, anim=lambda t: (f'{num_at(t):,}', round((NCX - width_s(t) / 2) * 2) / 2))
    def mc(s, a=None):
        r = super().mc(a)
        if len(s.cache) > 6: s.cache.pop(next(iter(s.cache)))
        return r


_DL = {}
def dot_layers():
    if not _DL:
        cols, rows, pitch, r = 22, 14, 40, 4
        h, w = rows * pitch + 40, cols * pitch + 40
        off = np.zeros((h, w, 3), np.float32); on = np.zeros((h, w, 3), np.float32); idx = np.full((h, w), -1, np.int32)
        k = 0
        for j in range(rows):
            for i in range(cols):
                c = (int(20 + i * pitch), int(20 + j * pitch))
                cv2.circle(off, c, r, (60, 70, 80), -1, cv2.LINE_AA); cv2.circle(on, c, r, (60, 230, 245), -1, cv2.LINE_AA)
                cv2.circle(idx, c, r + 2, k, -1); k += 1
        grid = np.zeros((h, w, 3), np.float32)
        for i in range(cols + 1): cv2.line(grid, (20 + i * pitch - pitch // 2, 0), (20 + i * pitch - pitch // 2, h), (40, 46, 54), 1)
        for j in range(rows + 1): cv2.line(grid, (0, 20 + j * pitch - pitch // 2), (w, 20 + j * pitch - pitch // 2), (40, 46, 54), 1)
        _DL.update(off=off, on=on, idx=idx, grid=grid, n=k)
    return _DL


def dots_draw(d, lit):
    D = dot_layers(); wk = np.clip(lit - np.arange(D['n'], dtype=np.float32), 0, 1)
    wm = np.where(D['idx'] >= 0, wk[np.maximum(D['idx'], 0)], 0.0)[..., None]
    onl = D['on'] * wm; lay = np.maximum(D['off'] * (1 - wm) + onl, D['grid'])
    J3.glow_screen(d, onl, 6, 0.9, 900 - 20, 230 - 20)
    J.screen(d, lay, 900 - 20, 230 - 20)


class Counter(Sh):
    def plate(s, tf):
        d = tech(28, tf); dots_draw(d, lit_at(tf)); return np.minimum(d, 255)


def s05bc():
    sh = Counter('05bc_counter', TB0, TB1, 'gfx', 0.06)
    sh.items = [NumItem()]
    sh.items += line_words([(wn('data', 43.6), 'data'), (wn('points', 43.9), 'points')], 62, NCX, 736, 'center')
    sh.items += line_words([(wn('per', 44.2), 'per'), (wn('underwriting', 44.4), 'underwriting'), (wn('submission', 45.0), 'submission')],
                           46, NCX, 800, 'center', 'it')
    return sh


# ================================================================ 05d commercial: B-roll, captions in the very centre
PARTS = [(TC0, 'c_cyrus_33', 0.03, 0.30, 0.62, 1.30), (47.295, 'c_intel_66', 0.30, 0.45, 0.55, 1.06),
         (47.775, 'c_aligned_31', 0.0, 0.40, 0.60, 1.15), (48.175, 'c_msft_70', 0.0, 0.5, 0.5, 1.0),
         (48.475, 'c_oracle_44', 0.0, 0.5, 0.5, 1.0)]
def centre_shade(k):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    g = np.exp(-(((xx - CX) / 760) ** 2 + ((yy - CY) / 250) ** 2))
    return np.repeat((1 - k * g)[..., None], 3, 2).astype(np.float32)
_CS = {}
def cshade(k):
    if k not in _CS: _CS[k] = centre_shade(k)
    return _CS[k]


class Foot(Sh):
    TF = 0.6
    def part(s, tf): return [p for p in PARTS if p[0] <= tf + 1e-6][-1] if tf >= PARTS[0][0] else PARTS[0]
    def plate(s, tf):
        t_from, clip, u0, fx, fy, z = s.part(tf)
        f = clip_at(clip, u0 + tf - t_from)
        if (fx, fy, z) != (0.5, 0.5, 1.0): f = L.fit(f, W, H, fx, fy, z)
        return L.grade(f)
    def shade(s, ts):
        return cshade({'c_aligned_31': 0.58, 'c_intel_66': 0.50}.get(s.part(ts)[1], 0.46))


def s05d():
    sh = Foot('05d_commercial', TC0, TC1, 'foot', 0.10)
    tw = wn('we', 47.3); tt = wn('the', 47.8); ti = wn('in', 48.3)
    P1 = [(wn('And', 46.7), 'And'), (wn('I', 46.9), 'I'), (wn('just', 47.0), 'just'), (wn('think', 47.2), 'think')]
    P2 = [(tw, 'we'), (wn('can', 47.5), 'can'), (wn('do', 47.7), 'do')]
    P3 = [(tt, 'the'), (wn('same', 47.9), 'same'), (wn('thing', 48.1), 'thing')]
    it = []
    it += line_words(P1, 116, CX, CY + 38, 'center', t_off=tw - 0.10, fout=0.10)
    it += line_words(P2, 136, CX, CY + 45, 'center', 'it', t_off=tt - 0.10, fout=0.10)
    it += line_words(P3, 136, CX, CY + 45, 'center', t_off=ti - 0.10, fout=0.10)
    # 'in' (italic) over the key word 'commercial.' typed on in the blue key box -- one centred group
    it += line_words([(ti, 'in')], 96, CX, CY - 62, 'center', 'it', glow=0.22)
    tc = wn('commercial.'); px = 160; by = CY + 112
    wv = J3.font(px).getlength('commercial.'); x0 = CX - wv / 2
    bx0, bx1 = int(x0 - px * 0.12), int(x0 + wv + px * 0.12); by0, by1 = int(by - px * 0.80), int(by + px * 0.24)
    def box(d, dy):
        sh_ = np.zeros((by1 - by0, bx1 - bx0, 4), np.float32); sh_[..., 3] = 1
        J3.drop_shadow(d, sh_, bx0, by0 + dy, 1.0, strength=0.45)
        d[int(by0 + dy):int(by1 + dy), bx0:bx1] = L.gbox(bx1 - bx0, by1 - by0)
    it.append(WordItem(tc - 0.04, box, None))
    rg, asc = J3.text_rgba('commercial.', px, hs=1.0)
    it.append(TypeItem(tc + 0.02, lambda d: J3._put_word(d, rg, asc, x0, by, (1.0, 0, 0, 0), True, 0.12), text_edges('commercial.', px, x0)))
    sh.items = it
    return sh


SHOTS = [s05a(), s05bc(), s05d()]


# ---------------------------------------------------------------- frame loop: camera + sub-frame motion blur + finish
def shot_at(t):
    for s in SHOTS:
        if s.t0 - 1e-9 <= t < s.t1 - 1e-9: return s
    return SHOTS[-1]


def disp(A, B):
    pts = np.float32([[0, 0], [W, 0], [0, H], [W, H], [CX, CY]])
    return float(np.abs((pts @ A[:, :2].T + A[:, 2]) - (pts @ B[:, :2].T + B[:, 2])).max())


def draw(sh, ts, tf, P):
    F = warp(P, sh.cam(ts))
    if F is P: F = P.copy()
    shd = sh.shade(ts)
    if shd is not None: F *= shd
    AT = sh.text_T(ts)
    for it in sh.items:
        op = it.op(ts)
        if op > 0.002: apply_item(F, it.mc(it.anim(ts) if it.anim else None), op, AT)
    return F


def frame(n):
    t = n / FPS; J3.RNG_T[0] = t; sh = shot_at(t)
    P = np.ascontiguousarray(sh.plate(t), dtype=np.float32)
    h = 0.25 / FPS; d = disp(sh.cam(t - h), sh.cam(t + h))
    ns = int(np.clip(math.ceil(d / 1.6), 1, 10))
    if ns == 1: out = draw(sh, t, t, P)
    else: out = sum(draw(sh, t + (k / (ns - 1) - 0.5) * 0.5 / FPS, t, P) for k in range(ns)) / ns
    if sh.kind == 'foot': return fin16.finish(np.clip(J3.grain(out, 3.0, seed=n), 0, 255), vig=0.60, tex=0.18, rb=0.40)
    return fin16.finish(np.clip(J3.grain(out, 4.5, seed=n), 0, 255), vig=0.60, tex=0.35, rb=0.50)


def nframes(p):
    o = subprocess.run([FFX, '-i', p, '-map', '0:v:0', '-c', 'copy', '-f', 'null', '-'], capture_output=True, text=True).stderr
    import re
    return int(re.findall(r'frame=\s*(\d+)', o)[-1])


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'stills':
        os.makedirs(OUTD + 'stills10', exist_ok=True)
        for a in sys.argv[2:]:
            n = int(a); Image.fromarray(frame(n)).save(OUTD + f'stills10/f_{n}.jpg', quality=90); print(n, flush=True)
    if mode == 'render':
        out = OUTD + NAME + '.mp4'
        p = subprocess.Popen([FFX, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', '24', out], stdin=subprocess.PIPE)
        import multiprocessing as mp
        with mp.get_context('fork').Pool(int(os.environ.get('NW', 3))) as pool:
            for k, img in enumerate(pool.imap(frame, range(N0, N1), chunksize=2)):
                p.stdin.write(np.ascontiguousarray(img).tobytes())
                if k % 24 == 0: print('frame', N0 + k, flush=True)
        p.stdin.close(); p.wait()
        nv = nframes(out); print('frames', nv, 'expected', N1 - N0); assert nv == N1 - N0
        chk = OUTD + NAME + '_check.mp4'
        subprocess.run([FFX, '-v', 'error', '-y', '-i', out, '-ss', f'{N0 / FPS:.5f}', '-t', f'{(N1 - N0) / FPS:.5f}', '-i', HERE + 'audio/mix2.wav',
                        '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '320k', '-t', f'{(N1 - N0) / FPS:.5f}',
                        '-movflags', '+faststart', chk], check=True)
        print('done', out, chk)
