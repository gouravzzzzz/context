"""All shots of the Justin Levine (Shepherd) trailer, built from the storyboard stills (storyboard/jl_stills.py), in motion.
Times are on the A-roll cut (words_cut.json). tin = how the shot comes in: 'zt' zoom-through (G2 out / G1 in), 'whip',
'cut' (hard cut, camera keeps travelling in), 'flash' (one-frame negative), 'none' (first shot)."""
import math, numpy as np, cv2
from engine import *

LM, RMX = 135, 1785                     # text margins (inside the 90 % safe area with room for the camera drift)


class Shot:
    tin = 'zt'; kind = 'gfx'; TF = 1.0
    def __init__(s, name, t0, t1):
        s.name, s.t0, s.t1, s.items, s.moves = name, t0, t1, [], []
        s.z0, s.ax, s.ay, s.px, s.py = 1.0, CX, CY, CX, CY
        s.roto = None
    # ---- camera (without transitions)
    def anchor(s, ts): return s.ax, s.ay, s.px, s.py
    def cam(s, ts):
        dz = dx = dy = 0.0
        for m in s.moves:
            a, b, c = m.at(ts); dz += a; dx += b; dy += c
        ax, ay, px, py = s.anchor(ts)
        return mat(s.z0 * math.exp(dz), ax, ay, px + dx, py + dy)
    def text_T(s, ts):
        if s.TF == 0: return np.float32([[1, 0, 0], [0, 1, 0]])
        A = np.vstack([s.cam(ts), [0, 0, 1]]); R = np.vstack([s.cam(s.t0), [0, 0, 1]])
        Mrel = (A @ np.linalg.inv(R))[:2]
        return (np.float32([[1, 0, 0], [0, 1, 0]]) + s.TF * (Mrel - np.float32([[1, 0, 0], [0, 1, 0]]))).astype(np.float32)
    def shade(s, ts): return None
    def speed(s, ts): return 0.0
    def plate(s, ts, tf): raise NotImplementedError
    def matte(s, tf): return None
    def post(s, img, ts): pass
    def key(s, ts, tf): return None          # plate cache key when the plate does not change inside the frame


# ================================================================ speakers (the A-roll cut itself: always in sync)
class Spk(Shot):
    kind = 'spk'; TF = 0.4
    def __init__(s, name, t0, t1, z0, dz, dur=3.0, pans=None, shade=None, roto=False):
        super().__init__(name, t0, t1)
        s.n0, s.n1 = int(round(t0 * FPS)), int(round(t1 * FPS))
        s.fx, s.fy = face_track(s.n0 - 12, s.n1 + 12)
        # v5 (Krish): talking heads are STABLE -- no face-follow (the tracker made the frame wiggle) and no drifting
        # pan / push chain. One fixed framing per shot (zoom z0 about the shot's median face point); only transitions move.
        s.z0 = z0; s.moves = []
        s.fax, s.fay = float(np.median(s.fx[12:-12] if len(s.fx) > 30 else s.fx)), float(np.median(s.fy[12:-12] if len(s.fy) > 30 else s.fy))
        s._shade = shade; s.roto = roto
    def nidx(s, tf): return int(min(s.n1 - 1, max(s.n0, round(tf * FPS))))
    def anchor(s, ts):
        return s.fax, s.fay, s.fax, s.fay
    def plate(s, ts, tf): return spk_frame(s.nidx(tf))
    def key(s, ts, tf): return s.nidx(tf)
    def matte(s, tf): return matte('cut', s.nidx(tf)) if s.roto else None
    def shade(s, ts): return s._shade(ts) if callable(s._shade) else s._shade


SH_L = side_shade_map('left', 0.38, 0.30)
SH_L2 = side_shade_map('left', 0.42, 0.32)
SH_R = side_shade_map('right', 0.34, 0.36)


def words_line(t_words, px, x, y, align='left', key=(), fin=0.12, t_off=None):
    """one caption line whose words pop on one by one at their own times, laid out once (never re-centres)"""
    lay = []; sp = J3.font(px).getlength(' ') * 0.95; xx = 0.0
    for tw, w in t_words:
        rg, asc = J3.text_rgba(w, px, hs=1.0); lay.append((tw, w, xx)); xx += rg.shape[1] + sp
    lw = xx - sp; x0 = x if align == 'left' else (x - lw if align == 'right' else x - lw / 2)
    return [Item(tw - LEAD, T_t1([w], px, x0 + xo, y, align='left', key=key), t_off=t_off, fin=fin) for tw, w, xo in lay]


# ---------------------------------------------------------------- S01 cold open, Justin tight
def s01():
    sh = Spk('01_justin', 0.0, 6.94, 1.32, 0.07, dur=3.0, pans=[(-10, 0), (6, -4), (10, 0), (-4, 4)], roto=True)
    sh.tin = 'none'
    def shade(ts):
        a = EIO(cl((ts - 3.15) / 0.45)); return SH_L * (1 - a) + SH_R * a
    sh._shade = shade
    sh.items = [Item(0.0, T_t1(['UNDERWRITERS', 'ARE NEXT'], 104, LM, 470, key=('NEXT',)), t_off=1.22, fin=0, fout=0.3),
                Item(1.30, T_put('Our engineering team spends', 50, LM, 440), t_off=3.25),
                Item(wt('zero') - LEAD, T_grad('zero time', 150, LM - 8, 580), t_off=3.25),
                Item(wt('writing') - LEAD, T_put('writing code', 58, LM, 668), t_off=3.25),
                Item(wt('100') - LEAD, T_grad('100%', 330, 800, 860, align='right', glow=0.35), behind=True, fin=0.2),
                Item(wt('of', 4) - LEAD, T_put('of their time', 52, RMX, 820, align='right', face='it')),
                Item(wt('orchestrating,') - LEAD, T_t1(['orchestrating'], 96, RMX, 935, align='right', key=('orchestrating',)))]
    return sh


# ---------------------------------------------------------------- S02 who he is
def s02a():
    sh = Spk('02a_nic', 6.94, 9.45, 1.08, 0.05, pans=[(-8, 0), (6, -3)], shade=side_shade_map('left', 0.40, 0.34))
    sh.tin = 'whip'
    sh.items = [Item(wt("Today,") - LEAD, T_put("Today we're super excited", 54, 140, 610)),
                Item(wt('to', 8) - LEAD, T_put('to bring on', 54, 140, 680))]
    return sh


class Foot(Shot):
    """full-frame B-roll: list of (t_from, clip, u0, fx, fy, zoom, fit) inside one continuous camera"""
    kind = 'foot'; TF = 0.6
    def __init__(s, name, t0, t1, parts, z0=1.0, dz=0.06, dur=3.0, pans=None, shades=None, anchor=None):
        super().__init__(name, t0, t1)
        s.parts = parts; s.z0 = z0; s.moves = chain(t0, t1, dz, dur, pans); s.shades = shades or {}
        if anchor: s.ax, s.ay, s.px, s.py = anchor
    def part(s, tf):
        return [p for p in s.parts if p[0] <= tf + 1e-6][-1] if tf >= s.parts[0][0] else s.parts[0]
    def plate(s, ts, tf):
        t_from, clip, u0, fx, fy, z = s.part(tf)[:6]
        v = vid(clip); f = v.at(u0 + tf - t_from)
        if (fx, fy, z) != (0.5, 0.5, 1.0) or f.shape[:2] != (H, W): f = L.fit(f, W, H, fx, fy, z)
        return L.grade(f)
    def key(s, ts, tf): return (s.part(tf)[1], int(round(tf * FPS)))
    def shade(s, ts):
        t_from = s.part(ts)[0]; return s.shades.get(t_from)


def s02b():
    """NAME CARD on Shepherd's own film of Justin; 'Justin Levine' BEHIND him (Dime roto sandwich), title line in front"""
    sh = Foot('02b_name', 9.45, 11.05, [(9.45, 'c_shep_1', 0.0, 0.5, 0.5, 1.0)], z0=1.04, dz=0.05, pans=[(-10, 0)])
    sh.roto = True
    sh.matte = lambda tf: matte('shep', int(round((tf - 9.45) * 30)))
    sh.shade = lambda ts: side_shade_map('left', 0.46, 0.34)
    sh.items = [Item(wt('Justin') - 0.06, T_put('Justin', 300, 140, 420, glow=0.22), behind=True, fin=0.22),
                Item(wt('Levine.') - 0.12, T_grad('Levine', 300, 140, 690, glow=0.30), behind=True, fin=0.22),
                Item(wt('He') - 0.15, T_put('COFOUNDER AND CEO, SHEPHERD', 42, 152, 800))]
    return sh


class Card(Shot):
    """tech ground + hairline 3x3 grid + a footage card (Twiml); content parts cut INSIDE the same card"""
    kind = 'gfx'
    def __init__(s, name, t0, t1, seed, rect, parts, dz=0.05, dur=3.0, pans=None, grid=True, amount=0.8, shadow=True):
        super().__init__(name, t0, t1)
        s.seed, s.rect, s.parts, s.grid, s.amount, s.shadow = seed, rect, parts, grid, amount, shadow
        s.moves = chain(t0, t1, dz, dur, pans)
    def part(s, tf): return [p for p in s.parts if p[0] <= tf + 1e-6][-1] if tf >= s.parts[0][0] else s.parts[0]
    def content(s, tf):
        t_from, clip, u0, fx, fy, z = s.part(tf)[:6]
        return L.grade(vid(clip).at(u0 + tf - t_from)), fx, fy, z
    def plate(s, ts, tf):
        d = tech(s.seed, tf, s.amount); x0, y0, cw, ch = s.rect
        if s.grid: L.hairline_grid(d, x0, y0, x0 + cw, y0 + ch)
        img, fx, fy, z = s.content(tf)
        L.card(d, img, x0, y0, cw, ch, fx=fx, fy=fy, zoom=z, shadow=s.shadow)
        return d
    def key(s, ts, tf): return int(round(tf * FPS))


class ShepCard(Card):
    """the Shepherd sign film shrinks from full frame into the card; the grid draws on round it"""
    def plate(s, ts, tf):
        d = tech(s.seed, tf, s.amount); x0, y0, cw, ch = s.rect
        e = EU(cl((ts - s.t0 + 0.10) / 1.25))
        img = L.grade(vid('s_shep_sign').at(tf - s.t0))
        X0, Y0 = x0 * e, y0 * e; Wc, Hc = W + (cw - W) * e, H + (ch - H) * e
        if e > 0.02:
            g = np.zeros_like(d); L.hairline_grid(g, x0, y0, x0 + cw, y0 + ch, col=(205, 215, 225), op=1.0)
            d[:] = d * (1 - 0.42 * EIO(cl((e - 0.55) / 0.45)) * (g[..., :1] / 205.0)) + g * 0.42 * EIO(cl((e - 0.55) / 0.45))
        c = L.fit(img, int(round(Wc)), int(round(Hc)), 0.40 + 0.10 * (1 - e), 0.5, 1.05 - 0.05 * (1 - e))
        if e > 0.01:
            sh_ = np.zeros((c.shape[0], c.shape[1], 4), np.float32); sh_[..., 3] = 1
            J3.drop_shadow(d, sh_, X0, Y0, 1.0, strength=0.55 * e)
        xi, yi = int(round(X0)), int(round(Y0))
        hh, ww = min(c.shape[0], H - yi), min(c.shape[1], W - xi)
        d[yi:yi + hh, xi:xi + ww] = c[:hh, :ww]
        return d
    def key(s, ts, tf): return None
    def speed(s, ts):
        u = (ts - s.t0 + 0.10) / 1.25
        return 0.0 if u > 1 or u < 0 else 900 * (EU(cl(u + 0.02)) - EU(cl(u - 0.02))) / (0.04 * 1.25) / FPS


def s02c():
    x0, y0, cw, ch = 548, 300, 824, 464
    sh = ShepCard('02c_shep_card', 11.05, 14.16, 23, (x0, y0, cw, ch), [], dz=0.045)
    sh.items = [Item(11.55, T_put('co-founder', 60, 300, y0 - 14, align='center', face='it')),
                Item(11.82, T_put('and CEO', 56, 300, y0 + ch - 14, align='center')),
                Item(wt('of', 12.5) - LEAD, T_put('of', 56, 1650, y0 - 14, align='center', face='it')),
                Item(wt('Shepherd.') - LEAD, T_grad('Shepherd.', 86, 1650, y0 + ch - 14, align='center'))]
    return sh


class Founded(Shot):
    """Dime S3: Justin as a roto cut-out with the ice-blue sticker outline rising in front of a literal photo card"""
    kind = 'gfx'
    def __init__(s):
        super().__init__('02d_founded', 14.16, 15.66)
        s.moves = chain(s.t0, s.t1, 0.045); s._co = {}
        s.n0 = int(round(s.t0 * FPS)); s.n1 = int(round(s.t1 * FPS)); s.fx, s.fy = face_track(s.n0 - 12, s.n1 + 12)
    def cut(s, n):
        if n not in s._co:
            co = S.cutout(cut_frame(n), matte('cut', n)); sc = 0.86
            co = cv2.resize(co, (int(W * sc), int(H * sc)), interpolation=cv2.INTER_AREA)
            if len(s._co) > 3: s._co.pop(next(iter(s._co)))
            s._co[n] = co
        return s._co[n]
    def plate(s, ts, tf):
        d = tech(36, tf, 0.7)
        e = EU(cl((ts - s.t0 + 0.05) / 0.9))
        L.card(d, L.grade(vid('c_lumi_28').at(tf - s.t0)), 780, 120, 1044, 800, fx=0.30, fy=0.45, zoom=1.0 + 0.04 * (1 - e))
        n = int(min(s.n1 - 1, max(s.n0, round(tf * FPS)))); co = s.cut(n)
        fx = float(np.median(s.fx))                                  # v5: fixed placement (no face-follow wiggle)
        rise = 340 * (1 - EU(cl((ts - s.t0 + 0.05) / 1.25)))
        ox, oy = 1330 - fx * 0.86, H - co.shape[0] + 10 + rise
        J3.drop_shadow(d, co, ox, oy, 1.0, strength=0.6); J3.over(d, co, ox, oy)
        return d
    def speed(s, ts):
        u = (ts - s.t0 + 0.05) / 1.25
        return 0.0 if u > 1 else 340 * (EU(cl(u + 0.02)) - EU(cl(u - 0.02))) / (0.04 * 1.25) / FPS


def s02d():
    sh = Founded()
    sh.items = [Item(14.17, T_put('I had founded a', 58, 140, 470)),
                Item(wt('construction', 14) - LEAD, T_grad('construction', 120, 140, 610))]
    return sh


class BCCard(Card):
    def content(s, tf):
        if tf < 17.31: return super().content(tf)
        lg = L.grade(vid('s_bc_logo').at(min(tf - 17.31, 42 / 30)))
        return lg, 0.5, 0.5, 1.0
    def plate(s, ts, tf):
        if tf < 17.31: return super().plate(ts, tf)
        d = tech(s.seed, tf, s.amount); x0, y0, cw, ch = s.rect
        L.hairline_grid(d, x0, y0, x0 + cw, y0 + ch)
        lg = s.content(tf)[0]
        sh_ = np.zeros((ch, cw, 4), np.float32); sh_[..., 3] = 1; J3.drop_shadow(d, sh_, x0, y0, 1.0, strength=0.55)
        d[y0:y0 + ch, x0:x0 + cw] = lg[8:40, 8:40].reshape(-1, 3).mean(0)
        lh = int(cw * lg.shape[0] / lg.shape[1]); ly = y0 + (ch - lh) // 2
        d[ly:ly + lh, x0:x0 + cw] = cv2.resize(lg, (cw, lh), interpolation=cv2.INTER_AREA)
        return d


def s02ef():
    x0, y0, cw, ch = 610, 250, 700, 580
    sh = BCCard('02ef_card', 15.66, 19.55, 24, (x0, y0, cw, ch), [(15.66, 'c_bctt_15', 0.0, 0.62, 0.45, 1.0)], dz=0.05)
    sh.items = [Item(15.66, T_put('software', 70, x0 - 48, 560, align='right', face='it'), t_off=17.27),
                Item(wt('business', 16) - LEAD, T_grad('business.', 90, x0 + cw + 48, 560), t_off=17.27),
                Item(wt('we', 17) - LEAD, T_put('We sold', 64, x0 - 48, 520, align='right')),
                Item(wt('our', 17.5) - LEAD, T_put('our business', 64, x0 - 48, 595, align='right', face='it')),
                Item(wt('to', 18.3) - LEAD, T_grad('to', 96, x0 + cw + 48, 575))]
    return sh


def s02g():
    sh = Foot('02g_autodesk', 19.55, 21.88, [(19.55, 's_adsk_screen', 0.0, 0.5, 0.5, 1.0)], z0=1.06, dz=0.08,
              anchor=(975, 560, CX, 590))
    sh.items = [Item(19.56, T_put('and then, together, to', 56, CX, 175, align='center', face='it'))]
    return sh


def s02h():
    sh = Spk('02h_nic', 21.88, 30.84, 1.08, 0.10, dur=3.0, pans=[(-12, -4), (8, 0), (12, 4), (-6, 0)], shade=SH_L2)
    sh.items = [Item(wt('you', 21.5) - LEAD, T_put('You guys strike me as', 54, 150, 560), t_off=25.36),
                Item(wt('top') - LEAD, T_t1(['top 1%'], 150, 140, 700, key=('1%',)), t_off=25.36),
                Item(wt('companies') - LEAD - 0.15, T_put('of companies', 54, 150, 790), t_off=25.36),
                Item(wt('in', 25.3) - LEAD, T_put('in terms of how', 54, 150, 520)),
                Item(wt('intelligently') - LEAD, T_grad('intelligently', 120, 145, 650)),
                Item(wt("you've") - LEAD, T_put("you've sequenced and", 54, 150, 740)),
                Item(wt('leveraged') - LEAD, T_put('leveraged', 54, 150, 820)),
                Item(wt('partnerships') - LEAD, T_grad('partnerships', 110, 145, 930))]
    return sh


def badge_item(t_on, logo_name, cx, cy, logo_w):
    lg = S.logo(logo_name)
    def draw(d, a):
        sc = 0.80 + 0.20 * a
        S.badge(d, lg, cx, cy, w=int(430 * sc), h=int(520 * sc), r=int(46 * sc), logo_w=int(logo_w * sc))
    q = lambda t: round(G1(cl((t - t_on) / 0.55)) * 14) / 14
    return Item(t_on, draw, behind=True, fin=0.14, anim=q)


def s02ij():
    sh = Spk('02ij_badges', 30.84, 34.55, 1.04, 0.06, roto=True)
    sh.items = [badge_item(wt('Procore') - 0.04, 'procore_dk.png', 420, 470, 340),
                badge_item(wt('Greenlight') - 0.04, 'greenlightre_dk.png', 1500, 470, 320),
                Item(wt('from', 33) - LEAD, T_put('from the beginning', 50, CX, 150, align='center', face='it'))]
    return sh


def s02k():
    sh = Foot('02k_intact', 34.55, 36.73, [(34.55, 's_intact', 0.0, 0.5, 0.0, 1.10)], z0=1.0, dz=0.06)
    sh.items = [Item(wt('later') - LEAD, T_t1(['later on.'], 92, 1000, 160, align='center', key=('later', 'on.')))]
    return sh


# ---------------------------------------------------------------- S03 sensor
def s03a():
    sh = Foot('03a_jobsite', 36.73, 37.95, [(36.73, 'c_lumi_5', 0.0, 0.5, 0.5, 1.0), (37.35, 'c_lss_46', 0.0, 0.42, 0.40, 1.10)],
              z0=1.04, dz=0.05)
    sh.tin = 'cut'; sh.shades = {36.73: SH_L2, 37.35: SH_L2}
    sh.items = [Item(36.70, T_put('Maybe you put a', 58, 140, 520), fin=0.10)]
    return sh


class Cell(Card):
    """Twiml S5: full-frame 3x3 hairline grid, the footage fills the centre cell, hard cuts inside it"""
    def plate(s, ts, tf):
        d = tech(s.seed, tf, s.amount); x0, y0, cw, ch = s.rect
        L.hairline_grid(d, x0, y0, x0 + cw, y0 + ch)
        img, fx, fy, z = s.content(tf)
        L.card(d, img, x0, y0, cw, ch, fx=fx, fy=fy, zoom=z, shadow=False)
        return d


def s03b():
    cw, ch = 640, 480; x0, y0 = int(CX - cw / 2), int(CY - ch / 2)
    sh = Cell('03b_sensor', 37.95, 39.05, 34, (x0, y0, cw, ch),
              [(37.95, 'c_lumi_14', 0.0, 0.62, 0.42, 1.15), (38.55, 'c_lcm_31', 0.0, 0.49, 0.40, 1.20), (38.85, 'c_lcs_57', 0.0, 0.56, 0.45, 1.05)],
              dz=0.05, amount=0.75)
    sh.tin = 'cut'
    sh.items = [Item(wt('sensor') - LEAD, T_grad('sensor', 120, x0 - 40, CY + 36, align='right')),
                Item(wt('on', 38.3) - LEAD, T_put('on site', 70, x0 + cw + 40, CY + 22, face='it'))]
    return sh


def s03c():
    sh = Spk('03c_nic', 39.05, 41.59, 1.08, 0.06, shade=SH_L2)
    sh.items = [Item(39.04, T_put("and we'll give you", 54, 150, 600)),
                Item(wt('better') - LEAD, T_t1(['better rates,'], 128, 150, 730, key=('rates,',))),
                Item(wt('right?') - LEAD, T_put('right?', 64, 150, 830, face='it'))]
    return sh


# ---------------------------------------------------------------- S04 the drop
def s04():
    sh = Spk('04_fifteen', 41.59, 45.49, 1.12, 0.06, roto=True, shade=side_shade_map('left', 0.34, 0.40))
    sh.tin = 'flash'
    t15 = wt('15', 40)
    sh.moves += [Move(t15 - 0.03, 0.22, dz=0.035, ease=G1), Move(t15 + 0.08, 1.5, dz=-0.035, ease=EU)]   # punch on the drop
    def slam(d, a):
        L.grad_text(d, '15%', int(430 * (1.20 - 0.20 * a)), 1800 + int(0 * a), 800 + int(40 * (1 - a)), align='right', glow=0.35)
    q = lambda t: round(G1(cl((t - t15 + 0.02) / 0.35)) * 16) / 16
    sh.items = [Item(wt('worth') - LEAD, T_put('Worth your while is', 54, 130, 470)),
                Item(t15 - 0.02, slam, behind=True, fin=0.06, anim=q),
                Item(wt('difference') - LEAD, T_put('difference on price.', 54, 1790, 880, align='right'))]
    sh.speed = lambda ts: 30.0 if 0 <= ts - t15 < 0.3 else 0.0
    return sh


# ---------------------------------------------------------------- S05 Progressive, 50 -> THOUSANDS, commercial
_TVA = {}
def tv_assets():
    if not _TVA:
        _TVA['tvc'] = L.load_rgba('assets/tv/kv20_cut_clean.png')
        _TVA['box'] = np.load(L.ROOT + '/assets/tv/kv20_screen.npy')
        _TVA['m'] = np.asarray(Image.open(L.ROOT + '/assets/tv/kv20_screenmask.png')).astype(np.float32) / 255
    return _TVA


def tv(d, screen_img, cx, cy, w):
    A = tv_assets(); tvc = A['tvc']; sx, sy, sw, sh = A['box']; m = A['m']
    th, tw = tvc.shape[:2]
    scr = L.fit(screen_img, sw, sh); scr = scr * 0.92 + 8; scr[::3] *= 0.86
    lay = tvc.copy(); reg = lay[sy:sy + sh, sx:sx + sw]; mm = m[sy:sy + sh, sx:sx + sw][..., None]
    reg[..., :3] = reg[..., :3] * (1 - mm) + scr / 255 * mm
    s = w / tw; lay = cv2.resize(lay, (int(tw * s), int(th * s)), interpolation=cv2.INTER_AREA)
    x, y = cx - lay.shape[1] / 2, cy - lay.shape[0] / 2
    J3.drop_shadow(d, lay, x, y, 1.0, strength=0.6); J3.over(d, lay, x, y)


class TV(Shot):
    kind = 'gfx'
    def __init__(s):
        super().__init__('05a_tv', 45.49, 48.62); s.moves = chain(s.t0, s.t1, 0.05)
    def plate(s, ts, tf):
        d = tech(27, tf)
        img = vid('c_prog90s_28').at(tf - s.t0) if tf < 47.55 else vid('c_prog99_60').at(tf - 47.55)
        tv(d, img, 700, 545, 1180)
        return d
    def key(s, ts, tf): return int(round(tf * FPS))


def s05a():
    sh = TV()
    sh.items = [Item(wt('Progressive') - LEAD, T_grad('Progressive', 116, RMX, 470, align='right')),
                Item(wt('was', 46) - LEAD, T_put('was the one', 56, RMX, 560, align='right', face='it')),
                Item(wt('that', 46.5) - LEAD, T_put('that started', 56, RMX, 626, align='right'))]
    return sh


_DOTS = {}
def dots_layer(kind, lit):
    k = (kind, lit)
    if k not in _DOTS:
        d = np.zeros((H, W, 3), np.float32)
        if kind == 'a': S.dots(d, 900, 230, 22, 14, 40, lit)
        else: S.dots(d, 120, 110, 88, 44, 20, 99999, r=3)
        if len(_DOTS) > 6: _DOTS.pop(next(iter(_DOTS)))
        _DOTS[k] = d
    return _DOTS[k]


class Counter(Shot):
    kind = 'gfx'
    def __init__(s):
        super().__init__('05bc_counter', 48.62, 52.21); s.moves = chain(s.t0, s.t1, 0.06)
        s.t50, s.tth = wt('50'), wt('thousands.')
    def lit(s, tf):
        if tf < s.t50 + 0.6: return int(50 * EU(cl((tf - s.t50 + 0.05) / 0.6)))
        if tf < s.tth - 0.95: return 50
        return int(50 + (308 - 50) * EU(cl((tf - (s.tth - 0.95)) / 0.7)))
    def plate(s, ts, tf):
        d = tech(28, tf)
        b = EIO(cl((tf - (s.tth - 0.25)) / 0.40))                     # sparse grid -> dense, everything lit
        if b < 1: d += dots_layer('a', s.lit(tf)) * (1 - b)
        if b > 0:
            z = 1.12 - 0.12 * EU(cl((tf - (s.tth - 0.25)) / 1.2))
            dd = cv2.warpAffine(dots_layer('b', 0), zoom_about(z), (W, H)); d += dd * b * 0.55
            d *= 1 - 0.45 * b * 0.0
        return np.minimum(d, 255)
    def key(s, ts, tf): return int(round(tf * FPS))


def counter_num(t, t0, t1):
    u = cl((t - t0) / (t1 - t0)); return int(round(50 * (4000 / 50) ** EU(u) / 10) * 10) if u > 0 else 50


def s05bc():
    sh = Counter(); t50, tth = sh.t50, sh.tth
    climb0, climb1 = tth - 0.95, tth - 0.15
    def num(d, a): L.grad_text(d, f'{a:,}', 300, 470, 640, align='center')
    sh.items = [Item(t50 - LEAD, num, t_off=tth - 0.20, fin=0.12, anim=lambda t: counter_num(t, climb0, climb1)),
                Item(wt('data') - LEAD, T_put('data points', 56, 470, 730, align='center'), t_off=tth - 0.20),
                Item(wt('per') - LEAD, T_put('per underwriting submission', 40, 470, 790, align='center', face='it'), t_off=tth - 0.20),
                Item(tth - 0.12, T_put('50 to', 70, CX, 470, align='center', face='it')),
                Item(tth - LEAD, T_t1(['THOUSANDS'], 170, CX, 640, align='center', key=('THOUSANDS',)))]
    return sh


def s05d():
    parts = [(52.21, 'c_cyrus_33', 0.03, 0.30, 0.62, 1.30), (52.92, 'c_intel_66', 0.0, 0.45, 0.55, 1.06),
             (53.40, 'c_aligned_31', 0.0, 0.40, 0.60, 1.15), (53.80, 'c_msft_70', 0.0, 0.5, 0.5, 1.0),
             (54.10, 'c_oracle_44', 0.0, 0.5, 0.5, 1.0)]
    sh = Foot('05d_commercial', 52.21, 55.45, parts, z0=1.0, dz=0.10, dur=3.0)
    sh.shades = {52.21: bottom_shade_map(420, 0.42), 52.92: top_shade_map(480, 0.30), 53.40: top_shade_map(480, 0.38),
                 54.10: bottom_shade_map(460, 0.40)}
    sh.items = [Item(wt('And', 52) - LEAD, T_put('And I just think', 84, 130, 950), t_off=52.92, fout=0.0, fin=0.08),
                Item(52.92, T_put('we can do', 108, 130, 220, face='it'), t_off=53.40, fout=0.0, fin=0.06),
                Item(53.40, T_put('the same thing', 108, 1790, 220, align='right'), t_off=53.80, fout=0.0, fin=0.06),
                Item(53.80, T_put('in', 190, 700, 780, align='center', face='it', glow=0.3), t_off=54.10, fout=0.0, fin=0.06),
                Item(54.10, T_t1(['commercial.'], 150, CX, 960, align='center', key=('commercial.',)), fin=0.06)]
    return sh


# ---------------------------------------------------------------- S06 the confession
def s06a():
    sh = Spk('06a_risk', 55.45, 58.20, 1.18, 0.07, dur=3.0, shade=SH_L)
    sh.tin = 'cut'
    sh.items = [Item(wt('I', 55) - LEAD, T_put('I used to work at', 50, 130, 440)),
                Item(wt('a', 56.3) - LEAD, T_put('a construction company', 50, 130, 500)),
                Item(wt('as', 57) - LEAD, T_put('as a', 50, 130, 590, face='it')),
                Item(wt('risk') - LEAD, T_grad('risk', 120, 125, 710)),
                Item(wt('manager.') - LEAD, T_grad('manager', 120, 125, 820))]
    return sh


def s06b():
    sh = Card('06b_osha', 58.20, 62.27, 29, (802, 290, 925, 521),
              [(58.20, 'c_osha_56', 0.0, 0.50, 0.40, 1.14), (59.30, 'c_osha_226', 0.0, 0.40, 0.40, 1.14),
               (60.40, 'c_osha_166', 0.0, 0.42, 0.40, 1.14), (61.35, 'c_osha_230', 0.0, 0.42, 0.40, 1.14)],
              dz=0.06, grid=False, amount=0.75)
    sh.items = [Item(wt('I', 58) - LEAD, T_put('I knew when the', 46, 760, 420, align='right')),
                Item(wt('insurance', 59) - LEAD, T_put('insurance company', 46, 760, 476, align='right')),
                Item(wt('was', 60) - LEAD, T_put('was coming to', 46, 760, 532, align='right')),
                Item(wt('inspect') - LEAD, T_grad('inspect', 124, 760, 660, align='right')),
                Item(wt('the', 61) - LEAD, T_put('the job site', 56, 760, 730, align='right', face='it'))]
    return sh


class Collage(Shot):
    """Twiml S09: three inspection shots fly in and settle as a collage; 'manufactured.' split by a track matte"""
    kind = 'gfx'
    CARDS = [('s_osha_hs', 3 / 30, 430, 190, 500, 300, 0.55, 0.40, 1.18), ('c_osha_192', 0.0, 990, 210, 500, 300, 0.55, 0.40, 1.18),
             ('c_osha_96', 0.0, 700, 560, 520, 310, 0.62, 0.32, 1.40)]
    def __init__(s):
        super().__init__('06c_collage', 62.27, 64.58); s.moves = chain(s.t0, s.t1, 0.05)
    def e(s, ts, i): return G1(cl((ts - (s.t0 + 0.02 + 0.16 * i)) / 0.75))
    def plate(s, ts, tf):
        d = tech(29, tf, 0.6)
        for i, (clip, u0, x0, y0, cw, ch, fx, fy, z) in enumerate(s.CARDS):
            e = s.e(ts, i)
            if e <= 0: continue
            img = L.grade(vid(clip).at(u0 + 0.8 * (tf - s.t0) if clip == 's_osha_hs' else u0 + tf - s.t0))
            sc = 0.90 + 0.10 * e; w, h = int(cw * sc), int(ch * sc)
            xx = int(x0 + (cw - w) / 2); yy = int(y0 + (ch - h) / 2 + 160 * (1 - e))
            lay = d.copy(); L.card(lay, img, xx, yy, w, h, fx=fx, fy=fy, zoom=z)
            a = cl(e * 1.6); d[:] = d * (1 - a) + lay * a
        return d
    def speed(s, ts):
        return max(160 * (s.e(ts + 0.02, i) - s.e(ts - 0.02, i)) / 0.04 / FPS for i in range(3))


def s06c():
    sh = Collage()
    mask = np.zeros((H, W), np.float32)
    for clip, u0, x0, y0, cw, ch, *_ in Collage.CARDS: mask[y0:y0 + ch, x0:x0 + cw] = 1
    m = mask[..., None]
    def split(d):
        grd = d.copy(); L.grad_text(grd, 'manufactured.', 176, CX, 800, align='center', face='it')
        wht = d.copy(); L.put_text(wht, 'manufactured.', 176, CX, 800, align='center', face='it')
        d[:] = wht * m + grd * (1 - m)
    sh.items = [Item(wt('somewhat') - 0.30, T_put("It's somewhat", 54, CX, 130, align='center')),
                Item(wt('manufactured') - LEAD, split)]
    return sh


# ---------------------------------------------------------------- S07 the proof: 11 months
def s07a():
    sh = Spk('07a_inception', 64.58, 67.50, 1.10, 0.06, shade=SH_R)
    sh.tin = 'cut'
    sh.items = [Item(wt('from', 64.5) - LEAD, T_put('From', 54, 1790, 430, align='right')),
                Item(wt('inception') - LEAD, T_grad('inception', 130, 1790, 560, align='right')),
                Item(wt('of', 66) - LEAD, T_put('of the company', 46, 1790, 640, align='right', face='it'))]
    return sh


CAL_T0 = 67.80
CAL_FLIPS = [round(CAL_T0 + 2.10 * (1 - (1 - k / 9) ** 1.7), 3) for k in range(10)]
FLIP_DUR = 0.34
_PAGES = {}
def page(num):
    if num not in _PAGES: _PAGES[num] = S.calendar_page(num, w=300, h=345, seed=num)
    return _PAGES[num]


def flip_warp(pg, theta, x, y):
    """the page turns about its top edge (binding) up and over, in perspective; returns (rgba, x, y)"""
    h, w = pg.shape[:2]; f = 1500.0; th = math.radians(theta)
    P = []
    for (u, v) in ((0, 0), (w, 0), (w, h), (0, h)):
        yy = v * math.cos(th); zz = -v * math.sin(th)
        X = (u - w / 2) * f / (f + zz); Y = yy * f / (f + zz)
        P.append((X + w / 2 + 300, Y + 300))
    Mx = cv2.getPerspectiveTransform(np.float32([[0, 0], [w, 0], [w, h], [0, h]]), np.float32(P))
    out = cv2.warpPerspective(pg, Mx, (w + 600, h + 600), flags=cv2.INTER_LINEAR)
    return out, x - 300, y - 300


class Calendar(Shot):
    kind = 'gfx'
    def __init__(s):
        super().__init__('07b_calendar', 67.50, 70.85); s.moves = chain(s.t0, s.t1, 0.05)
    def plate(s, ts, tf):
        d = tech(30, tf)
        px0, py0 = CX - 150, 318
        for k in range(3):                                               # the pad underneath
            pg = page(11)
            J3.drop_shadow(d, pg, px0 + (2 - k) * 4, py0 + (2 - k) * 5, 1.0, strength=0.45); J3.over(d, pg, px0 + (2 - k) * 4, py0 + (2 - k) * 5)
        done = sum(1 for tf_ in CAL_FLIPS if ts >= tf_ + FLIP_DUR)
        top = done + 1                                                     # month on top of the pad
        if top <= 10: J3.over(d, page(top + 1) if top + 1 <= 11 else page(11), px0, py0); J3.over(d, page(top), px0, py0)
        for k, t_f in enumerate(CAL_FLIPS):                                # pages in flight
            u = (ts - t_f) / FLIP_DUR
            if 0 <= u < 1:
                th = 112 * G2(u)
                fw, x, y = flip_warp(page(k + 1), th, px0, py0)
                a = 1 - cl((th - 80) / 32)
                J3.drop_shadow(d, fw, x, y, a, strength=0.4); J3.over(d, fw, x, y, a)
        return d
    def speed(s, ts):
        return 40.0 if any(0 <= ts - t_f < FLIP_DUR for t_f in CAL_FLIPS) else 0.0


def neon_item(t_on, word, cx, cy, px, dur=1.0, rate=1.2, h=None):
    def draw(d, a): J3.neon_box(d, t_on + a / FPS, t_on, word, cx, cy, px=px, h=h, dur=dur, type_rate=rate)
    return Item(t_on, draw, fin=0.0, anim=lambda t: int(min(60, max(0, round((t - t_on) * FPS)))))


def s07b():
    sh = Calendar()
    sh.items = [Item(wt('to', 67.4) - LEAD, T_put('to our first insurance products', 50, CX, 190, align='center')),
                Item(wt('being') - LEAD, T_put('being offered in market', 50, CX, 252, align='center', face='it')),
                Item(wt('was', 69.6) - LEAD, T_put('was about', 48, CX, 758, align='center', face='it')),
                neon_item(wt('11') - 0.08, '11 MONTHS', CX, 872, 80)]
    return sh


def s07c():
    sh = Spk('07c_record', 70.85, 73.42, 1.14, 0.06, shade=SH_L)
    sh.items = [Item(wt('which,') - LEAD, T_put('which was like', 54, 130, 520)),
                Item(wt('record') - LEAD, T_t1(['record pace.'], 120, 130, 660, key=('pace.',)))]
    return sh


# ---------------------------------------------------------------- S08 the viewer's own question
def s08a():
    sh = Spk('08a_luke', 73.42, 75.73, 1.06, 0.05)
    sh.tin = 'cut'
    def box(d): d[330:690, 110:620] *= 0.5
    sh.items = [Item(wt('do', 73) - 0.12, box, fin=0.14),
                Item(wt('do', 73) - LEAD, T_put('Do you think', 54, 150, 420)),
                Item(wt("we're", 73.9) - LEAD, T_put("we're in an", 54, 150, 490, face='it')),
                Item(wt('AI', 74) - LEAD, T_grad('AI bubble?', 110, 140, 630))]
    return sh


def s08b():
    sh = Spk('08b_no', 75.73, 77.21, 1.10, 0.05, roto=True)
    sh.tin = 'cut'
    tno = wt('No.')
    def no(d, a): L.put_text(d, 'No.', int(460 * (1.10 - 0.10 * a)), 1260, 760, align='left', glow=0.25)
    sh.items = [Item(tno - 0.04, no, behind=True, fin=0.08, anim=lambda t: round(G1(cl((t - tno + 0.04) / 0.32)) * 12) / 12)]
    return sh


def s08c():
    sh = Spk('08c_consistently', 77.21, 79.15, 1.10, 0.05, shade=SH_L)
    sh.items = [Item(wt('I', 77) - LEAD, T_put('I just think that we have', 52, 130, 470)),
                Item(wt('consistently') - LEAD, T_grad('consistently', 124, 125, 610))]
    return sh


# ---- photo cloud (Krish's Pinterest pin): a thin stream of thumbnails, clusters of real AI photos burst out of it
_CI = {}
def cimg(f):
    if f not in _CI:
        im = L.grade(L.load(f)); s_ = 640 / max(im.shape[:2]); _CI[f] = cv2.resize(im, (int(im.shape[1] * s_), int(im.shape[0] * s_)), interpolation=cv2.INTER_AREA)
    return _CI[f]


def cluster(seed, n, sx, sy, smin, smax):
    rng = np.random.default_rng(seed); order = rng.permutation(len(S.AI_CARDS)); out = []
    for i in range(n):
        f, fx, fy, asp, z = S.AI_CARDS[order[i % len(order)]]
        depth = rng.random(); w = int(smin + (smax - smin) * depth); h = int(w / asp)
        cx = CX + rng.normal(0, sx); cy = CY + rng.normal(0, sy)
        x0 = float(np.clip(cx - w / 2, 150, W - 150 - w)); y0 = float(np.clip(cy - h / 2, 150, 860 - h))
        out.append(dict(f=f, fx=fx, fy=fy, z=z, x=x0, y=y0, w=w, h=h, depth=depth, border=rng.random() < 0.35,
                        sx=float(np.clip(x0 + w / 2 + rng.normal(0, 260), 60, W - 60))))
    return sorted(out, key=lambda c: c['depth'])


class Cloud(Shot):
    kind = 'gfx'
    WAVES = [(79.15, 81, 12, 300, 140, 150, 300), (80.30, 83, 12, 330, 150, 160, 310), (81.35, 82, 15, 470, 190, 190, 400)]
    def __init__(s):
        super().__init__('08c_cloud', 79.15, 83.21); s.moves = chain(s.t0, s.t1, 0.08, dur=3.0)
        s.waves = [(t, cluster(sd, n, a, b, c, d_)) for t, sd, n, a, b, c, d_ in s.WAVES]
    def card_state(s, c, t_in, t_out, k, ts):
        """emerges from its stream slot (small, on the centre line) and flies to its place (G1); leaves back into the stream (G2)"""
        e_in = G1(cl((ts - (t_in + 0.035 * k)) / 0.65))
        e_out = G2(cl((ts - (t_out - 0.30 + 0.015 * k)) / 0.30)) if t_out else 0.0
        e = e_in * (1 - e_out)
        w = 40 + (c['w'] - 40) * e; h = 30 + (c['h'] - 30) * e
        x = c['sx'] - w / 2 + (c['x'] + c['w'] / 2 - c['sx']) * e; y = CY - h / 2 + (c['y'] + c['h'] / 2 - CY) * e
        return e, x, y, w, h
    def plate(s, ts, tf):
        d = tech(37, tf, 0.55)
        off = (ts - s.t0) * 140.0; pitch = 49; k0 = int(off // pitch)
        for j in range(-1, W // pitch + 2):                               # the stream: tiny thumbnails sliding left
            x = j * pitch - (off - k0 * pitch) + 30
            if x < 20 or x > W - 60: continue
            f, fx, fy, asp, z = S.AI_CARDS[((j + k0) * 7) % len(S.AI_CARDS)]
            t_ = L.fit(cimg(f), 40, 30, fx, fy, z) * 0.82; xi = int(round(x))
            d[CY - 15:CY + 15, xi:xi + 40] = t_
        for wi, (t_in, cards) in enumerate(s.waves):
            t_out = s.waves[wi + 1][0] if wi + 1 < len(s.waves) else None
            if ts < t_in or (t_out and ts > t_out + 0.2): continue
            for k, c in enumerate(cards):
                e, x, y, w, h = s.card_state(c, t_in, t_out, k, ts)
                if e <= 0.01: continue
                wi_, hi_ = max(8, int(round(w))), max(6, int(round(h)))
                L.card(d, cimg(c['f']), int(round(x)), int(round(y)), wi_, hi_, fx=c['fx'], fy=c['fy'], zoom=c['z'],
                       shadow=True, border=6 if (c['border'] and e > 0.6) else 0)
        return d
    def speed(s, ts):
        for t_in, _ in s.waves:
            if -0.35 < ts - t_in < 1.1: return 45.0
        return 0.0


def s08cloud():
    sh = Cloud()
    sh.items = [Item(wt('underestimated') - LEAD, T_t1(['underestimated'], 100, CX, 990, align='center', key=('underestimated',)), t_off=81.30),
                Item(wt('how', 81) - LEAD, T_t1(['how big AI is.'], 100, CX, 990, align='center', key=('AI',)))]
    return sh


# ---------------------------------------------------------------- S09 stakes
def s09():
    cw, ch = 760, 520; x0, y0 = int(CX - cw / 2), int(CY - ch / 2); x1, y1 = x0 + cw, y0 + ch
    sh = Cell('09_lloyds', 83.21, 87.09, 35, (x0, y0, cw, ch), [(83.21, 'c_lloyds_97', 0.0, 0.40, 0.62, 1.25)], dz=0.08, dur=3.0, amount=0.75)
    sh.items = [Item(wt('And', 83) - LEAD, T_put('And so I think', 48, CX, y0 - 30, align='center')),
                Item(wt('underwriting', 84) - LEAD, T_grad('underwriting', 92, x0 - 36, CY + 28, align='right')),
                Item(wt('is', 85) - LEAD, T_put('is another', 52, x1 + 36, CY - 10)),
                Item(wt('profession') - LEAD, T_put('profession', 52, x1 + 36, CY + 52, face='it')),
                Item(wt('moving') - LEAD, T_put('moving in that direction.', 48, CX, y1 + 70, align='center'))]
    return sh


# ---------------------------------------------------------------- S10 the payoff, left open
SPLIT = json.load(open(HERE + 'split_win.json'))
SPL_FACE = {'nic': (792, 736, 1.34), 'justin': (1015, 386, 1.05), 'luke': (1132, 539, 1.05)}


class Split(Shot):
    kind = 'spk'; TF = 0.0
    def __init__(s):
        super().__init__('10_split', 87.09, 98.58); s.moves = []          # v5: talking heads stable (no push)
        s.segs = [g for g in SEGS if g['k'] >= 32]
        s.lit = [(87.09, 0), (wt('we', 93.5) - 0.42, 1), (wt('Breaking') - 0.38, 2)]
    def ep(s, tf):
        g = [g for g in s.segs if g['t0'] <= tf + 1e-6]; g = g[-1] if g else s.segs[0]
        return g['src0'] / 24 + min(tf - g['t0'], (g['n'] - 1) / 24)
    def act(s, ts):
        w = np.full(3, 0.42)
        for i, (t, k) in enumerate(s.lit):
            if ts >= t: w = np.full(3, 0.42); w[k] = 1.0; prev = s.lit[i - 1][1] if i else None
        # smooth hand-over of the light (0.3 s)
        for i, (t, k) in enumerate(s.lit[1:], 1):
            u = (ts - t) / 0.3
            if 0 <= u < 1:
                a = EIO(u); pk = s.lit[i - 1][1]; w = np.full(3, 0.42); w[pk] = 1 - 0.58 * a; w[k] = 0.42 + 0.58 * a
        return w
    def plate(s, ts, tf):
        d = np.zeros((H, W, 3), np.float32); e = s.ep(tf); fi = int(round((e - SPLIT['ep0']) * 24))
        w = s.act(ts)
        for k, who in enumerate(('nic', 'justin', 'luke')):
            fx, fy, z = SPL_FACE[who]
            img = L.grade(vid('split_' + who, 24.0).frame(fi))
            img = cv2.warpAffine(img, mat(z, fx, fy, CX, 520), (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
            d[:, k * 644:k * 644 + 632] = img[:, CX - 316:CX + 316] * w[k]
        for xx in (638, 1282): d[:, xx - 6:xx + 6] = (10, 11, 13); d[:, xx - 1:xx + 1] = (120, 130, 140)
        return d
    def post(s, img, ts):
        b = int(round(150 * EU(cl((ts - s.t0 - 0.05) / 1.4))))
        if b > 0: img[:b] = 0; img[H - b:] = 0


def s10():
    sh = Split()
    q1 = 'When do you think we will see the first'; q2 = 'fully AI underwritten commercial policy?'
    lw = J3.text_rgba(q1 + ' ', 44, hs=1.0)[0].shape[1]; kw = J3.text_rgba(q2, 50, hs=1.0)[0].shape[1]; xs = CX - (lw + kw) / 2
    t_we = wt('we', 93.5)
    sh.items = [Item(wt('When') - LEAD, T_put(q1, 44, xs, 1000), t_off=t_we - 0.45),
                Item(wt('fully') - LEAD, T_grad(q2, 50, xs + lw, 1000, glow=0.2), t_off=t_we - 0.45)]
    ws = [(wt('we', 93.5), 'We'), (wt('actually,'), 'actually,'), (wt('like,', 94.5), 'like,'), (wt('we', 95), 'we'),
          (wt('did'), 'did'), (wt('this.'), 'this.')]
    sh.items += words_line(ws, 62, CX, 1004, align='center', key=('this.',), t_off=wt('Breaking') - 0.40)
    sh.items += [neon_item(wt('Breaking') - 0.06, 'BREAKING NEWS', 1590, 976, 40, dur=0.8, rate=1.0, h=70)]
    return sh


class Black(Shot):
    kind = 'black'; tin = 'cut'
    def plate(s, ts, tf): return np.zeros((H, W, 3), np.float32)
    def key(s, ts, tf): return 0


class Title(Shot):
    kind = 'gfx'; tin = 'cut'
    def __init__(s, t0, t1):
        super().__init__('10e_title', t0, t1); s.moves = chain(t0, t1, 0.05, dur=3.0, lead=0.0)
    def plate(s, ts, tf): return tech(31, tf, 0.7)
    def key(s, ts, tf): return int(round(tf * FPS))


def title(t0, t1):
    sh = Title(t0, t1)
    wm = L.load_rgba(L.ROOT + '/assets/logos/verticals_wordmark.png')
    def mark(d, a):
        L.place_rgba(d, wm, CX, 440 + 30 * (1 - a), w=int(880 * (0.94 + 0.06 * a)), glow=0.2)
    sh.items = [Item(t0 + 0.15, mark, fin=0.5, anim=lambda t: round(G1(cl((t - t0 - 0.15) / 1.1)) * 24) / 24),
                neon_item(t0 + 0.50, 'JUSTIN LEVINE, SHEPHERD', CX, 760, 60, dur=0.8, rate=0.7)]
    sh.speed = lambda ts: 12.0 if 0 <= ts - t0 - 0.15 < 0.6 else 0.0
    return sh


def build(END, BLACK, TITLE):
    shots = [s01(), s02a(), s02b(), s02c(), s02d(), s02ef(), s02g(), s02h(), s02ij(), s02k(), s03a(), s03b(), s03c(), s04(),
             s05a(), s05bc(), s05d(), s06a(), s06b(), s06c(), s07a(), s07b(), s07c(), s08a(), s08b(), s08c(), s08cloud(), s09(), s10()]
    assert abs(shots[-1].t1 - BLACK) < 1e-6
    shots += [Black('10d_black', BLACK, TITLE), title(TITLE, END)]
    for a, b in zip(shots, shots[1:]):
        assert abs(a.t1 - b.t0) < 1e-6, (a.name, a.t1, b.name, b.t0)
        a.tout = b.tin
    shots[-1].tout = 'end'
    return shots
