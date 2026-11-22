"""v2 segment 07: NEW frames 692-850 (28.833-35.417 s) 'Procore and Greenlight Re from the beginning, Intact later on,
you put a sensor on site'.
Part 1 (692-805) copies Krish's pin https://pin.it/3LMPHfWnT (~/jl-trailer/refs_v2/pin_procore, 'PAC NYC'), measured
frame by frame:
  0.00-0.93  small square between two words, growing slowly        -> blue gradient square, 'Procore' types on (left)
  0.93-1.10  square snaps open into a photo box (0.07H -> 0.675H)   -> Procore HQ (Carpinteria) aerial in the box
  1.10-2.08  box keeps growing (0.675H -> 0.92H, accelerating), words pushed out by its edges
             -> cut inside the box to Greenlight Re's lobby on 'Greenlight', 'Greenlight Re' types on (right)
  2.08-2.30  box bursts to full frame (fast, long settle), words pushed off
  2.10-3.90  full-frame rapid cuts 0.4/0.3/0.3/0.3 s -> Procore CEO, Greenlight Re reception, Procore AI on site,
             Greenlight Re boardroom, then Intact's logo wall (footage) on 'Intact'
  3.92-4.48  the last shot contracts back to a small box, the words ride back in with its edges -> 'Intact' | 'later on.'
Part 2 (805-850): simple full-frame B-roll (jobsite aerial, sensor install), big centred captions built word by word.
Look = trailer (black '01' tech ground, Instrument Serif, gradient key words, shadows + glow, grain + vignette).
  python seg07_procore.py stills n1 n2 ...   |   python seg07_procore.py render
"""
import sys, os, math, subprocess
import numpy as np, cv2
from PIL import Image
sys.path.insert(0, '/Users/gourav/jl-trailer/trailer')
from engine import *
import newtime as NT
import fin16

HERE = '/Users/gourav/jl-trailer/trailer/v2_07/'
AS = '/Users/gourav/jl-trailer/assets/v2_31_39/'
OUTD = '/Users/gourav/jl-trailer/trailer/v2segs/'
FF = '/Users/gourav/ks-ron-build/reel1/ff'
N0, N1, NB = 692, 850, 805


def wn(txt, after=0.0):
    return next(w[0] for w in NT.WORDS if w[2] == txt and w[0] >= after - 1e-6)


# ---------------------------------------------------------------- timing (NEW seconds)
SQ0 = N0 / FPS                      # square phase starts at the hard cut
TSN = 29.10                         # snap (ref 0.933 s) -- 'Procore' is being said
TACC = 30.65                        # box growth starts accelerating (ref 1.65 s)
TEX = 746 / FPS                     # burst to full frame (ref 2.083 s) -- right after 'Re'
TC0 = 32.527                        # contraction starts (ref 3.917 s); lands small at 'later' (ref 4.15 -> 32.76)
RS = 28.61                          # ref -> NEW shift for the contraction keyframes
CUTS = [(0, 'hq'), (728, 'gl_lobby'), (746, 'p_ceo'), (755, 'gl_rec'), (762, 'p_ai'), (769, 'gl_board'),
        (775, 'in_wall'), (796, 'in_sign')]       # content by output frame ('Greenlight' 30.35, 'intact' 32.29, 'on,' 33.16)
GAP = 30


def box_wh(t):
    """box size (w, h) in px -- ref measurements (720x480, in units of H or W) mapped to 1920x1080"""
    if t < TSN:
        u = cl((t - SQ0) / (TSN - SQ0)); s = (0.050 + 0.020 * u * u) * H; return s, s
    r = t - TSN
    if r < 0.167:
        s = np.interp(r, [0, 0.034, 0.05, 0.067, 0.117, 0.167], [0.07, 0.42, 0.55, 0.59, 0.645, 0.675]) * H; return s, s
    if t < TACC:
        s = (0.675 + 0.065 * (t - TSN - 0.167) / (TACC - TSN - 0.167)) * H; return s, s
    if t < TEX:
        s = np.interp(t - TACC, [0, 0.167, 0.30, 0.367, 0.40, 0.433], [0.74, 0.76, 0.80, 0.84, 0.87, 0.92]) * H; return s, s
    if t < TC0:
        k = [0, 0.034, 0.067, 0.10, 0.134, 0.167, 0.20, TC0 - TEX]
        w = np.interp(t - TEX, k, [0.92 * H, 0.763 * W, 0.889 * W, 0.920 * W, 0.940 * W, 0.955 * W, 0.965 * W, 0.99 * W])
        h = np.interp(t - TEX, k, [0.92 * H, H, H, H, H, H, H, H]); return w, h
    rt = t - RS
    kt = [3.917, 3.95, 3.983, 4.017, 4.05, 4.083, 4.117, 4.15, 4.183, 4.217, 4.25, 4.283, 4.317, 4.35, 4.383, 4.417, 4.45, 4.483, 4.95]
    kw = [0.99 * W, 0.981 * W, 0.965 * W, 0.951 * W, 0.925 * W, 0.887 * W, 0.817 * W] + \
         [s * H for s in (0.663, 0.556, 0.502, 0.467, 0.444, 0.423, 0.413, 0.40, 0.394, 0.390, 0.385, 0.374)]
    kh = [H] * 7 + kw[7:]
    return float(np.interp(rt, kt, kw)), float(np.interp(rt, kt, kh))


# ---------------------------------------------------------------- content
_IM = {}
def still(name, fname):
    if name not in _IM:
        im = np.asarray(Image.open(AS + fname).convert('RGB')).astype(np.float32)
        _IM[name] = L.grade(im)
    return _IM[name]


STILLS = {  # name: (file, fx, fy, zoom at start, push per second)
    'hq': ('procore_hq_aerial.jpg', 0.50, 0.46, 1.00, 0.030),
    'gl_lobby': ('greenlightre_lobby.jpg', 0.50, 0.40, 1.00, 0.030),
    'p_ceo': ('procore_ceo_groundbreak.jpg', 0.60, 0.40, 1.02, 0.050),
    'gl_rec': ('greenlightre_reception.jpg', 0.50, 0.45, 1.02, 0.050),
    'p_ai': ('procore_ai_jobsite.jpg', 0.55, 0.45, 1.02, 0.050),
    'gl_board': ('greenlightre_boardroom.jpg', 0.50, 0.50, 1.00, 0.050),
    'in_sign': ('intact_hq_sign.jpg', 0.66, 0.77, 1.90, 0.030),
}


_UQ = {}
def uniq_frames(name):
    """indices of the unique frames of a screen-recorded clip (duplicates dropped)"""
    if name not in _UQ:
        c = cv2.VideoCapture(BRV + name + '.mp4'); prev = None; keep = []; i = 0
        while True:
            ok, x = c.read()
            if not ok: break
            s = cv2.resize(x, (240, 135)).astype(np.float32)
            if prev is None or np.abs(s - prev).mean() > 0.6: keep.append(i)
            prev = s; i += 1
        _UQ[name] = keep
    return _UQ[name]


_FT = {}
def intact_wall(n):
    """Intact logo wall footage (s_intact), unique frames at normal speed, burnt-in subtitle cropped off"""
    k = n - 775
    if k not in _FT:
        u = uniq_frames('s_intact'); f = vid('s_intact', 30.0).frame(u[min(k, len(u) - 1)])
        if len(_FT) > 4: _FT.pop(next(iter(_FT)))
        _FT[k] = L.grade(np.ascontiguousarray(f[:int(H * 0.86)]))
    return _FT[k]


def shot_at(n):
    name, st = CUTS[0][1], CUTS[0][0]
    for a, b in CUTS:
        if n >= a: name, st = b, a
    return name, st


def content(n, ts, w, h):
    """the box picture at size w x h (cover fit, slow inner push like the ref's moving footage)"""
    name, st = shot_at(n)
    if name == 'in_wall':
        return L.fit(intact_wall(n), w, h, 0.60, 0.45, 1.0)
    f, fx, fy, z0, pz = STILLS[name]
    z = z0 + pz * max(0.0, ts - st / FPS)
    return L.fit(still(name, f), w, h, fx, fy, z)


def photo_vig(c):
    hh, ww = c.shape[:2]
    yy, xx = np.ogrid[0:hh, 0:ww]
    r = np.sqrt(((xx / max(1, ww) - 0.5) / 0.5) ** 2 + ((yy / max(1, hh) - 0.5) / 0.5) ** 2)
    return c * (1 - 0.25 * np.clip(r - 0.6, 0, 1) ** 1.5)[..., None]


# ---------------------------------------------------------------- text items (Dime word build / type-on, with shadow + glow)
class WordItem(Item):
    """one word: fades in over 3 frames while rising 14 px and its blur clears"""
    def __init__(s, t_on, draw_at, t_off=None, fout=0.0):
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
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        r = (x0, y0, np.ascontiguousarray(M[y0:y1, x0:x1]), np.ascontiguousarray(C[y0:y1, x0:x1]))
        s.cache[a] = r
        return r


class TypeItem(Item):
    """hero word typed on letter by letter (1 letter / frame, soft edge), gradient key word"""
    def __init__(s, t_on, word, px, x, base_y, t_off=None, fout=0.0, face='reg'):
        s.word, s.px, s.x, s.base_y, s.face = word, px, x, base_y, face
        fnt = J3.font(px, face)
        s.edges = [x + fnt.getlength(word[:k]) for k in range(len(word) + 1)]
        nl = len(word)
        super().__init__(t_on - 0.04, None, t_off=t_off, fin=0.0, fout=fout,
                         anim=lambda t: round(cl((t - (t_on - 0.04)) * FPS / nl) * nl * 2) / 2)
        s.full = None
    def mc(s, a=None):
        if a in s.cache: return s.cache[a]
        if s.full is None:
            P0 = np.zeros((H, W, 3), np.float32); P1 = np.full((H, W, 3), 200.0, np.float32)
            for P in (P0, P1): L.grad_text(P, s.word, s.px, s.x, s.base_y, face=s.face, glow=0.32)
            s.full = ((P1 - P0) / 200.0, P0)
        M, C = s.full
        k = int(a); fr = a - k
        xr = np.arange(W, dtype=np.float32)
        e0 = s.edges[min(k, len(s.word))]; e1 = s.edges[min(k + 1, len(s.word))]
        mask = np.where(xr < e0, 1.0, np.where(xr < e1, fr, 0.0)).astype(np.float32)
        if k >= len(s.word): mask[:] = 1.0
        else: mask = cv2.GaussianBlur(mask[None, :], (0, 0), 6)[0]
        m3 = mask[None, :, None]
        Mm = 1 - m3 * (1 - M); Cm = C * m3
        act = (np.abs(Mm - 1).max(2) > 2e-3) | (Cm.max(2) > 0.3); ys, xs = np.where(act)
        if len(ys) == 0: r = None
        else:
            y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
            r = (x0, y0, np.ascontiguousarray(Mm[y0:y1, x0:x1]), np.ascontiguousarray(Cm[y0:y1, x0:x1]))
        s.cache[a] = r
        return r


def tw(txt, px, face='reg'): return J3.font(px, face).getlength(txt)


XL, XR = 760.0, 1160.0              # anchors the side words are laid out at (then ride with the box edges)
P1PX, P3PX = 96, 128
BY1 = CY + int(0.30 * P1PX); BY3 = CY + int(0.30 * P3PX)
# phase 1: 'Procore' (left, typed) | 'Greenlight Re' (right, typed); gone once the burst has pushed them off
T_P1OFF = TEX + 0.25
LEFT1 = [TypeItem(wn('Procore') - 0.02, 'Procore', P1PX, XL - tw('Procore', P1PX), BY1, t_off=T_P1OFF)]
RIGHT1 = [TypeItem(wn('Greenlight') - 0.02, 'Greenlight Re', P1PX, XR, BY1, t_off=T_P1OFF)]
# phase 3: 'Intact' (left) | 'later on.' (right), riding back in with the contraction
_wl = tw('later', P3PX, 'reg') + J3.font(P3PX).getlength(' ') * 0.95
LEFT3 = [Item(wn('intact'), lambda d: L.grad_text(d, 'Intact', P3PX, XL, BY3, align='right', glow=0.32), fin=0.0)]
RIGHT3 = [WordItem(wn('later'), lambda d, dy: L.put_text(d, 'later', P3PX, XR, BY3 + dy, glow=0.22)),
          WordItem(wn('on,', 33), lambda d, dy: L.put_text(d, 'on.', P3PX, XR + _wl, BY3 + dy, face='it', glow=0.22))]


def ground(tf):
    return tech(52, tf, 0.8)


def plate1(ts, tf, n):
    d = ground(tf)
    w, h = box_wh(ts)
    wi, hi = max(2, int(round(w))), max(2, int(round(h)))
    x0, y0 = int(round(CX - w / 2)), int(round(CY - h / 2))
    if wi < W - 2 or hi < H - 2:
        shd = np.zeros((hi, wi, 4), np.float32); shd[..., 3] = 1
        J3.drop_shadow(d, shd, x0, y0, 1.0, strength=0.55)
    if ts < TSN + 0.045:                                    # the square (ref: black on cream -> trailer blue gradient)
        c = L.gbox(wi, hi).astype(np.float32)
    else:
        c = photo_vig(content(n, ts, wi, hi))
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + wi), min(H, y0 + hi)
    d[ya:yb, xa:xb] = c[ya - y0:yb - y0, xa - x0:xb - x0]
    # side words ride the box edges
    tl = np.float32([[1, 0, (CX - w / 2 - GAP) - XL], [0, 1, 0]])
    tr = np.float32([[1, 0, (CX + w / 2 + GAP) - XR], [0, 1, 0]])
    for grp, T in ((LEFT1, tl), (RIGHT1, tr), (LEFT3, tl), (RIGHT3, tr)):
        for it in grp:
            op = it.op(ts)
            if op > 0.002: apply_item(d, it.mc(it.anim(ts) if it.anim else None), op, T)
    return d


def speed1(t):
    h = 0.25 / FPS
    wa, ha = box_wh(t - h); wb, hb = box_wh(t + h)
    return abs(wb - wa) / 2 + abs(hb - ha) / 2 + 2.0


# ---------------------------------------------------------------- part 2: simple B-roll + centred captions
P2 = [(805, 'c_lumi_28', 0.50, 0.50), (825, 'c_lumi_14', 0.50, 0.42)]     # rebar + sensor spots, cut on 'sensor' (f825)
MOV2 = chain(NB / FPS, N1 / FPS, 0.05, dur=3.0)
L1PX, L2PX, L3PX = 112, 236, 112
BYL1, BYL2, BYL3 = 400, 640, 790


def centred_words(words, px, by, face='reg'):
    sp = J3.font(px, face).getlength(' ') * 0.95
    ws = [tw(w, px, face) for _, w in words]
    x = CX - (sum(ws) + sp * (len(ws) - 1)) / 2; out = []
    for (t, w), wd in zip(words, ws):
        out.append(WordItem(t, lambda d, dy, w=w, x=x: L.put_text(d, w, px, x, by + dy, face=face, glow=0.22)))
        x += wd + sp
    return out


CAP2 = centred_words([(wn('you', 33.5), 'you'), (wn('put', 33.5), 'put'), (wn('a', 34.2), 'a')], L1PX, BYL1) + \
    [TypeItem(wn('sensor', 34), 'sensor', L2PX, CX - tw('sensor', L2PX) / 2, BYL2)] + \
    centred_words([(wn('on', 34.8), 'on'), (wn('site', 34.8), 'site')], L3PX, BYL3, face='it')


def foot2(n):
    st, name, fx, fy = P2[0]
    for a in P2:
        if n >= a[0]: st, name, fx, fy = a
    v = vid(name, 30.0)
    if name == 'c_lumi_28':                             # screen-recorded: unique frames only (~24/s = normal speed)
        u = uniq_frames(name)[1:]; return L.grade(v.frame(u[min(n - st, len(u) - 1)])), fx, fy   # [0] is the previous shot
    return L.grade(v.frame(int(round((n - st) / FPS * 30)))), fx, fy


def cam2(t):
    dz = sum(m.at(t)[0] for m in MOV2)
    return zoom_about(math.exp(dz))


def sub2(ts, n, fr):
    img, fx, fy = fr
    F = warp(img, cam2(ts)) * 0.74
    for it in CAP2:
        op = it.op(ts)
        if op > 0.002: apply_item(F, it.mc(it.anim(ts) if it.anim else None), op)
    return F


def speed2(t):
    h = 0.25 / FPS
    a, b = cam2(t - h), cam2(t + h)
    pts = np.float32([[0, 0], [W, 0], [0, H], [W, H]])
    return float(np.abs((pts @ a[:, :2].T + a[:, 2]) - (pts @ b[:, :2].T + b[:, 2])).max())


# ---------------------------------------------------------------- frame
def nsub(d): return int(np.clip(math.ceil(d / 1.6), 1, 16))


def frame(n):
    t = n / FPS; J3.RNG_T[0] = t
    if n < NB:
        k = nsub(speed1(t))
        offs = [0.0] if k == 1 else [(i / (k - 1) - 0.5) * 0.5 / FPS for i in range(k)]
        out = sum(plate1(t + o, t, n) for o in offs) / len(offs)
        return fin16.finish(np.clip(J3.grain(out, 4.5, seed=n), 0, 255), vig=0.60, tex=0.35, rb=0.50)
    fr = foot2(n); k = nsub(speed2(t))
    offs = [0.0] if k == 1 else [(i / (k - 1) - 0.5) * 0.5 / FPS for i in range(k)]
    out = sum(sub2(t + o, n, fr) for o in offs) / len(offs)
    return fin16.finish(np.clip(J3.grain(out, 3.0, seed=n), 0, 255), vig=0.60, tex=0.18, rb=0.40)


def nframes(p):
    import re
    o = subprocess.run([FF, '-i', p, '-map', '0:v:0', '-c', 'copy', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return int(re.findall(r'frame=\s*(\d+)', o)[-1])


def render_tail():
    """re-render part 2 only; part 1 frames are taken from the existing render"""
    out = OUTD + '07_procore.mp4'; old = HERE + 'part1_old.mp4'; os.replace(out, old)
    dec = subprocess.Popen([FF, '-v', 'error', '-i', old, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    p = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', '24', out], stdin=subprocess.PIPE)
    for _ in range(NB - N0): p.stdin.write(dec.stdout.read(W * H * 3))
    dec.stdout.close(); dec.wait()
    import multiprocessing as mp
    with mp.get_context('fork').Pool(int(os.environ.get('NW', 3))) as pool:
        for img in pool.imap(frame, range(NB, N1), chunksize=2): p.stdin.write(np.ascontiguousarray(img).tobytes())
    p.stdin.close(); p.wait()
    return out


def render_patch(a, b):
    """re-render frames [a, b) only, the rest copied from the current render"""
    out = OUTD + '07_procore.mp4'; old = HERE + 'prev_render.mp4'; os.replace(out, old)
    dec = subprocess.Popen([FF, '-v', 'error', '-i', old, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    p = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', '24', out], stdin=subprocess.PIPE)
    import multiprocessing as mp
    with mp.get_context('fork').Pool(int(os.environ.get('NW', 3))) as pool:
        new = list(pool.imap(frame, range(a, b), chunksize=2))
    for n in range(N0, N1):
        buf = dec.stdout.read(W * H * 3)
        p.stdin.write(np.ascontiguousarray(new[n - a]).tobytes() if a <= n < b else buf)
    dec.stdout.close(); dec.wait(); p.stdin.close(); p.wait()
    return out


if __name__ == '__main__':
    if sys.argv[1] == 'patch':
        out = render_patch(int(sys.argv[2]), int(sys.argv[3])); chk = OUTD + '07_procore_check.mp4'
        nv = nframes(out); print('frames', nv, 'expected', N1 - N0)
        subprocess.run([FF, '-v', 'error', '-y', '-i', out, '-ss', f'{N0 / FPS:.4f}', '-t', f'{(N1 - N0) / FPS:.4f}',
                        '-i', '/Users/gourav/jl-trailer/trailer/audio/mix2.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                        '-c:a', 'aac', '-b:a', '320k', '-t', f'{(N1 - N0) / FPS:.4f}', '-movflags', '+faststart', chk], check=True)
        print('done', out, chk)
    if sys.argv[1] == 'tail':
        out = render_tail(); chk = OUTD + '07_procore_check.mp4'
        nv = nframes(out); print('frames', nv, 'expected', N1 - N0)
        subprocess.run([FF, '-v', 'error', '-y', '-i', out, '-ss', f'{N0 / FPS:.4f}', '-t', f'{(N1 - N0) / FPS:.4f}',
                        '-i', '/Users/gourav/jl-trailer/trailer/audio/mix2.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                        '-c:a', 'aac', '-b:a', '320k', '-t', f'{(N1 - N0) / FPS:.4f}', '-movflags', '+faststart', chk], check=True)
        print('done', out, chk)
    if sys.argv[1] == 'stills':
        for a in sys.argv[2:]:
            n = int(a); Image.fromarray(frame(n)).save(HERE + f'stills/f{n}.jpg', quality=90); print(n, flush=True)
    if sys.argv[1] == 'render':
        out = OUTD + '07_procore.mp4'; chk = OUTD + '07_procore_check.mp4'
        p = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', '24', out], stdin=subprocess.PIPE)
        import multiprocessing as mp
        with mp.get_context('fork').Pool(int(os.environ.get('NW', 3))) as pool:
            for img in pool.imap(frame, range(N0, N1), chunksize=2): p.stdin.write(np.ascontiguousarray(img).tobytes())
        p.stdin.close(); p.wait()
        nv = nframes(out); print('frames', nv, 'expected', N1 - N0)
        subprocess.run([FF, '-v', 'error', '-y', '-i', out, '-ss', f'{N0 / FPS:.4f}', '-t', f'{(N1 - N0) / FPS:.4f}',
                        '-i', '/Users/gourav/jl-trailer/trailer/audio/mix2.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                        '-c:a', 'aac', '-b:a', '320k', '-t', f'{(N1 - N0) / FPS:.4f}', '-movflags', '+faststart', chk], check=True)
        print('done', out, chk)
