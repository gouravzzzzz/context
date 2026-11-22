"""v2 segment 09 '$$$ -> 15%' : NEW frames 850-971 (121 f).
03c_nic  (850-898): v1 shot (camera, captions) + a big glowing, blinking cyan->blue '$$$' BEHIND Nic's head (rembg matte),
                    on from 'better' (OLD 40 s); in the last 0.25 s it shoots UP off screen (graph G2, sub-frame blur).
04_fifteen (898-971): Justin, own camera (slow push + G1 punch hiding the jump cut at 928). '15%' centred below his face,
                    enters from below at the cut (G1, fastest at the cut = the $$$ whoosh continuing), counts 1% -> 15%,
                    lands on '15' (931). 'worth your while is' / 'difference on price.' centred, Dime word build.
  python scene.py stills n1 n2 ...   |   python scene.py render   |   python scene.py speed"""
import sys, os, math, subprocess, importlib.util
import numpy as np, cv2
from PIL import Image
sys.path.insert(0, '/Users/gourav/jl-trailer/trailer')
from engine import *
import engine
engine.PATCH_MAP.clear()
from newtime import A as A_new2old, WORDS as WN
HERE = '/Users/gourav/jl-trailer/trailer/v2seg09/'
FF = '/Users/gourav/ks-ron-build/reel1/ff'
N0, NC, N1 = 850, 898, 971                       # segment start, the Nic -> Justin cut, segment end (exclusive)
TC = NC / FPS

_sp = importlib.util.spec_from_file_location('jl_shots', '/Users/gourav/jl-trailer/trailer/shots.py')
SH = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(SH)


def nold(n):
    """lip-synced OLD cut frame for NEW frame n (cut points map past the removed pause)"""
    return int(round(A_new2old(n / FPS + 1e-4) * FPS))


def wn(txt, after=0.0):
    return next(w[0] for w in WN if w[2] == txt and w[0] >= after - 1e-6)


I2 = np.float32([[1, 0, 0], [0, 1, 0]])
def tr(dx, dy): return np.float32([[1, 0, dx], [0, 1, dy]])


def layer_mc(draw):
    """affine (x0, y0, M, C) crop of a draw op: out = frame * M + C"""
    P0 = np.zeros((H, W, 3), np.float32); P1 = np.full((H, W, 3), 200.0, np.float32)
    draw(P0); draw(P1)
    M = (P1 - P0) / 200.0; C = P0
    act = (np.abs(M - 1).max(2) > 2e-3) | (C.max(2) > 0.3); ys, xs = np.where(act)
    if len(ys) == 0: return None
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    return (x0, y0, np.ascontiguousarray(M[y0:y1, x0:x1]), np.ascontiguousarray(C[y0:y1, x0:x1]))


def blur_layer(r, Ts):
    """real motion blur of a layer: the average of the layer under several sub-frame transforms (union box, clipped)"""
    if r is None: return None
    if len(Ts) == 1 and np.allclose(Ts[0], I2, atol=1e-4): return r
    x0, y0, M, C = r; h, w = M.shape[:2]
    pts = np.float32([[x0, y0], [x0 + w, y0], [x0, y0 + h], [x0 + w, y0 + h]])
    q = np.concatenate([pts @ T[:, :2].T + T[:, 2] for T in Ts])
    cx0, cy0 = int(max(0, math.floor(q[:, 0].min()) - 2)), int(max(0, math.floor(q[:, 1].min()) - 2))
    cx1, cy1 = int(min(W, math.ceil(q[:, 0].max()) + 2)), int(min(H, math.ceil(q[:, 1].max()) + 2))
    if cx1 <= cx0 or cy1 <= cy0: return None
    Ma = np.zeros((cy1 - cy0, cx1 - cx0, 3), np.float32); Ca = np.zeros_like(Ma)
    for T in Ts:
        Tl = compose(tr(-cx0, -cy0), compose(T, tr(x0, y0)))
        Ma += cv2.warpAffine(M, Tl, (cx1 - cx0, cy1 - cy0), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(1, 1, 1))
        Ca += cv2.warpAffine(C, Tl, (cx1 - cx0, cy1 - cy0), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
    return (cx0, cy0, Ma / len(Ts), Ca / len(Ts))


def subs(t, n):
    return [t] if n <= 1 else [t + (k / (n - 1) - 0.5) * 0.5 / FPS for k in range(n)]      # 180-degree shutter


# ================================================================ 03c_nic: v1 shot + '$$$' behind his head
NIC = SH.s03c(); NIC.tin = 'cut'; NIC.tout = 'cut'; NIC.roto = True
DOL_PX, DOL_CX, DOL_BASE = 560, 965, 565             # '$$$' size / centre x / baseline (head top ~390 on screen)
T_DOL = wn('better', 36.0) - 0.05                    # Krish: 'at 40 to 41 s' (OLD) = from 'better rates'
EXIT_D, EXIT_DIST = 0.25, 1400.0                     # last 0.25 s: shoots up, graph G2 (accelerating out)
T_EXIT = TC - EXIT_D
GRAD0, GRAD1 = (70, 255, 236), (40, 120, 255)        # the trailer's cyan -> blue
# blink + glow per frame from the 'better' frame (neon flicker-on, glow surges, two blinks on the beats)
BLINK = [(.55, .6), (.12, .15), (1, 1), (.35, .3), (1, .95), (1, .8), (1, .7), (1, .65), (1, .75), (.4, .35), (.22, .2),
         (1, 1), (1, .85), (1, .72), (1, .66), (.42, .32), (1, 1), (1, .86), (1, .78)]


def dol_state(t):
    k = int(math.floor((t - T_DOL) * FPS + 1e-6))
    if k < 0: return 0.0, 0.0
    b, g = BLINK[min(k, len(BLINK) - 1)]
    return float(b), round(float(g) * 20) / 20


_DOL = {}
def dol_mc(g):
    if g not in _DOL:
        def draw(d):
            rg, asc = J3.text_rgba('$$$', DOL_PX, 'reg', (255, 255, 255), 1.0)
            gr = J.grad(rg.shape[1], rg.shape[0], GRAD0, GRAD1) / 255
            lay = rg.copy(); lay[..., :3] = gr * rg[..., 3:4]
            x0 = DOL_CX - rg.shape[1] / 2; y0 = DOL_BASE - asc
            J3.glow_screen(d, lay[..., :3] * 255, 60, 0.55 * g, x0, y0)          # wide neon bloom (pulses)
            J3.drop_shadow(d, lay, x0, y0, 1.0, strength=0.55)
            J3.glow_screen(d, lay[..., :3] * 255, 20, 0.30 + 0.45 * g, x0, y0)   # tight glow
            J3.over(d, lay, x0, y0)
        _DOL[g] = layer_mc(draw)
    return _DOL[g]


def dol_dy(t): return -EXIT_DIST * G2(cl((t - T_EXIT) / EXIT_D)) if t > T_EXIT else 0.0


def nic_speed(t):
    h = 0.25 / FPS
    return abs(dol_dy(t + h) - dol_dy(t - h)) * 2


def nic_frame(n):
    t = n / FPS; no = nold(n); to = no / FPS                     # contiguous: OLD time drives the v1 camera / captions
    P = spk_frame(no)
    h = 0.25 / FPS
    d = float(np.abs(NIC.cam(to + h) - NIC.cam(to - h))[:, 2].max()) * 2
    ns = int(np.clip(math.ceil(d / 1.6), 1, 8))
    F = sum(warp(P, NIC.cam(s)) for s in subs(to, ns)) / ns
    shd = NIC.shade(to)
    if shd is not None: F = F * shd
    AT = NIC.text_T(to)
    # '$$$' behind the head
    b, g = dol_state(t)
    if b > 0.002:
        F0 = F.copy()
        ss = subs(t, int(np.clip(math.ceil(nic_speed(t) / 6.0), 1, 48)))
        r = blur_layer(dol_mc(g), [compose(tr(0, dol_dy(s)), AT) for s in ss])
        apply_item(F, r, b)
        m = matte('cut', no)
        a = cv2.warpAffine(m, NIC.cam(to), (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)[..., None]
        F = F * (1 - a) + F0 * a
    for it in NIC.items:                                         # v1 captions as they were
        op = it.op(to)
        if op > 0.002: apply_item(F, it.mc(it.anim(to) if it.anim else None), op, AT)
    return F


# ================================================================ 04_fifteen: Justin, '15%' counter, centred captions
J_OLD = [nold(n) for n in range(NC, N1)]
_fx = [FACES[o][0] + FACES[o][2] / 2 for o in J_OLD if FACES[o]]; _fy = [FACES[o][1] + FACES[o][3] * 0.45 for o in J_OLD if FACES[o]]
JAX, JAY = float(np.median(_fx)), float(np.median(_fy))
T_JC = next(NC + i for i in range(1, len(J_OLD)) if J_OLD[i] - J_OLD[i - 1] > 1) / FPS     # jump cut inside Justin (928)
J_MOVES = [Move(T_JC - 0.5 / FPS, 0.30, dz=0.035, ease=G1)]       # v5: stable talking head; only the G1 punch hiding the jump cut


def jcam(t):
    dz = sum(m.at(t)[0] for m in J_MOVES)
    return mat(math.exp(dz), JAX, JAY, JAX, JAY)


T15 = wn('15', 38.0)                                  # '15' -> the counter lands on 15 % here (frame 931)
N15 = int(math.ceil(T15 * FPS - 1e-6))
PX15, CX15 = 212, CX
Y15_LO, Y15_HI = 978, 910                            # baseline: below line A, then up under the face for line B
IN_D, IN_DIST = 0.45, 450.0                           # enters from below the frame, graph G1 (fastest at the cut)
T_IN = TC - 2.0 / FPS
T_GL, GL_D = (N15 + 6) / FPS, 0.45                    # glides up once 15 % has landed and line A has gone
LA_PX, LA_Y = 80, 785
LB_PX, LB_Y = 80, 986
T_A_OFF = (N15 + 5) / FPS


def count(t):
    u = cl((t - TC) / (N15 / FPS - TC))
    return 15 if u >= 1 else 1 + int(math.floor(14 * (1 - (1 - u) ** 1.4)))


_F15 = J3.font(PX15, 'reg')
_XPCT = CX15 - _F15.getlength('15%') / 2 + _F15.getlength('15')     # the '%' never moves; digits right-aligned to it
_CNT = {}
def cnt_mc(v, flash):
    k = (v, flash)
    if k not in _CNT:
        s = f'{v}%'; x = _XPCT - _F15.getlength(str(v))
        def draw(d):
            rg, asc = J3.text_rgba(s, PX15, 'reg', (255, 255, 255), 1.0)
            if flash > 0:
                gr = J.grad(rg.shape[1], rg.shape[0], GRAD0, GRAD1)
                J3.glow_screen(d, gr * rg[..., 3:4], 40, 0.7 * flash, x, Y15_LO - asc)
            L.grad_text(d, s, PX15, x, Y15_LO, glow=0.40)
        _CNT[k] = layer_mc(draw)
    return _CNT[k]


def c15_dy(t):
    dy = IN_DIST * (1 - G1(cl((t - T_IN) / IN_D))) if t < T_IN + IN_D else 0.0
    return dy - (Y15_LO - Y15_HI) * EU(cl((t - T_GL) / GL_D))


def flash(t):
    u = (t - N15 / FPS) / 0.40
    return 0.0 if u < 0 or u > 1 else round((1 - u) ** 2 * 10) / 10


class WordItem(Item):
    """Dime word build: fades in over 3 f while rising 14 px and its blur clears (laid out in place)"""
    def __init__(s, t_on, draw_at, t_off=None, fout=0.17):
        super().__init__(t_on - 0.06, None, t_off=t_off, fin=3 / FPS, fout=fout,
                         anim=lambda t, t_on=t_on: round(cl((t - (t_on - 0.06)) / (4 / FPS)) * 8) / 8)
        s.draw_at = draw_at
    def mc(s, a=None):
        if a in s.cache: return s.cache[a]
        e = G1(a); dy = 14 * (1 - e); sig = 3.5 * (1 - e)
        r = layer_mc(lambda d: s.draw_at(d, dy))
        if r is not None and sig > 0.4:
            x0, y0, M, C = r; p = int(sig * 3) + 2
            M = cv2.GaussianBlur(np.pad(M, ((p, p), (p, p), (0, 0)), constant_values=1), (0, 0), sig)
            C = cv2.GaussianBlur(np.pad(C, ((p, p), (p, p), (0, 0))), (0, 0), sig)
            r = (x0 - p, y0 - p, M, C)
        s.cache[a] = r
        return r


def line_items(words, px, base_y, t_off=None):
    """one centred line, each word on at its own (NEW) time"""
    sp = J3.font(px).getlength(' ') * 0.95; lay = []; xx = 0.0
    for tw, w in words:
        rg, asc = J3.text_rgba(w, px, hs=1.0); lay.append((tw, w, xx)); xx += rg.shape[1] + sp
    x0 = CX - (xx - sp) / 2
    return [WordItem(tw, lambda d, dy, w=w, x=x0 + xo: L.put_text(d, w, px, x, base_y + dy, glow=0.24), t_off=t_off)
            for tw, w, xo in lay]


J_ITEMS = line_items([(wn('worth', 37), 'worth'), (wn('your', 37), 'your'), (wn('while', 37), 'while'), (wn('is', 38), 'is')],
                     LA_PX, LA_Y, t_off=T_A_OFF) + \
          line_items([(wn('difference', 39), 'difference'), (wn('on', 39.8), 'on'), (wn('price.', 39.9), 'price.')], LB_PX, LB_Y)
J_SHADE = bottom_shade_map(420, 0.72)


def j_speed(t):
    h = 0.25 / FPS
    return abs(c15_dy(t + h) - c15_dy(t - h)) * 2


def cam_disp(Afn, t):
    h = 0.25 / FPS
    pts = np.float32([[0, 0], [W, 0], [0, H], [W, H]])
    a, b = Afn(t - h), Afn(t + h)
    return float(np.abs((pts @ a[:, :2].T + a[:, 2]) - (pts @ b[:, :2].T + b[:, 2])).max()) * 2


def justin_frame(n):
    t = n / FPS; no = J_OLD[n - NC]
    P = spk_frame(no)
    ns = int(np.clip(math.ceil(cam_disp(jcam, t) / 1.6), 1, 12))
    F = sum(warp(P, jcam(s)) for s in subs(t, ns)) / ns
    F = F * J_SHADE
    for it in J_ITEMS:
        op = it.op(t)
        if op > 0.002: apply_item(F, it.mc(it.anim(t)), op)
    ss = subs(t, int(np.clip(math.ceil(j_speed(t) / 5.0), 1, 40)))
    apply_item(F, blur_layer(cnt_mc(count(t), flash(t)), [tr(0, c15_dy(s)) for s in ss]), 1.0)
    return F


# ================================================================ frame / finish
def frame(n):
    t = n / FPS; J3.RNG_T[0] = t
    out = nic_frame(n) if n < NC else justin_frame(n)
    return fin16.finish(np.clip(J3.grain(out, 2.2, seed=n), 0, 255), vig=0.60, tex=0.0, rb=0.35)


def speed_report():
    rows = []
    prev = None
    for n in range(N0, N1):
        t = n / FPS
        if n < NC:
            to = nold(n) / FPS; c = NIC.cam(to); ov = dol_dy(t)
        else:
            c = jcam(t); ov = c15_dy(t)
        pts = np.float32([[0, 0], [W, 0], [0, H], [W, H]]); p = pts @ c[:, :2].T + c[:, 2]
        v = None if prev is None or (n == NC) else float(np.abs(p - prev[0]).max())
        ovv = None if prev is None or (n == NC) else abs(ov - prev[1])
        rows.append((n, nold(n), None if v is None else round(v, 2), None if ovv is None else round(ovv, 1), count(t) if n >= NC else '-'))
        prev = (p, ov)
    for r in rows: print(*r)


if __name__ == '__main__':
    os.makedirs(HERE + 'stills', exist_ok=True)
    if sys.argv[1] == 'stills':
        for a in sys.argv[2:]:
            Image.fromarray(frame(int(a))).save(HERE + f'stills/f_{int(a)}.jpg', quality=90); print(a, flush=True)
    elif sys.argv[1] == 'speed':
        speed_report()
    elif sys.argv[1] == 'render':
        out = '/Users/gourav/jl-trailer/trailer/v2segs/09_dollar15.mp4'
        chk = '/Users/gourav/jl-trailer/trailer/v2segs/09_dollar15_check.mp4'
        p = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', '24', out], stdin=subprocess.PIPE)
        import multiprocessing as mp
        with mp.get_context('fork').Pool(int(os.environ.get('NW', 3))) as pool:
            for k, img in enumerate(pool.imap(frame, range(N0, N1), chunksize=2)):
                p.stdin.write(np.ascontiguousarray(img).tobytes())
                if k % 20 == 0: print('frame', N0 + k, flush=True)
        p.stdin.close(); p.wait(); dur = (N1 - N0) / FPS
        subprocess.run([FF, '-v', 'error', '-y', '-i', out, '-ss', f'{N0 / FPS:.6f}', '-t', f'{dur:.6f}', '-i',
                        '/Users/gourav/jl-trailer/trailer/audio/mix2.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac',
                        '-b:a', '320k', '-t', f'{dur:.6f}', chk], check=True)
        print('done', out, N1 - N0, 'frames')
