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
PX0, PY0, PW, PH = 1040, 168, 700, 744            # photo card (right), ref aspect ~0.96 -> 0.94
PCX, PCY = PX0 + PW / 2, PY0 + PH / 2
SC = PW / 537.0                                     # ref -> ours scale (ref photo 537 px wide on 720)
AST_R = 50 * SC                                     # asterisk half-length (ref ~100 px across)
LW = max(3, int(round(5 * SC * 0.8)))               # stroke

# ---------------------------------------------------------------- timing (ref seconds, 30 -> 24 fps by time)
TA = T0 + 0.53                                      # asterisk hold ends (ref f0-f15)
TF_ = 0.20                                          # fold into -> <- (ref f16-f21)
TS = TA + TF_                                       # arrows start splitting (ref f22)
TP = TS + 0.08                                      # photo starts growing (ref f24)
TPD = 0.42                                          # dot -> full (ref f24-f36), graph 1 (fast -> settle)


def photo_u(t): return G1(cl((t - TP) / TPD))
def split_u(t): return EIO(cl((t - TS) / 0.10))


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
    z = 1.0 + 0.05 * EU(cl((t - TP) / 2.6))
    c = L.fit(im, max(2, w), max(2, h), 0.56, 0.30, 1.0 + 0.04 + z - 1.0)
    yy, xx = np.mgrid[0:c.shape[0], 0:c.shape[1]].astype(np.float32)
    r = np.sqrt(((xx / max(1, c.shape[1]) - 0.5) / 0.5) ** 2 + ((yy / max(1, c.shape[0]) - 0.5) / 0.5) ** 2)
    return c * (1 - 0.28 * np.clip(r - 0.55, 0, 1) ** 1.5)[..., None]


def strokes(t):
    """asterisk -> two arrows -> arrows on the photo corners; returns line segments [(x1,y1,x2,y2)] in screen px"""
    R = AST_R
    if t < TA:                                       # the asterisk
        segs = []
        for a in (0, 45, 90, 135):
            dx, dy = R * math.cos(math.radians(a)), R * math.sin(math.radians(a))
            segs.append((PCX - dx, PCY - dy, PCX + dx, PCY + dy))
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


def draw_strokes(d, segs):
    ss = 3; x0 = int(max(0, min(min(a, c) for a, b, c, e in segs) - 20)); y0 = int(max(0, min(min(b, e) for a, b, c, e in segs) - 20))
    x1 = int(min(W, max(max(a, c) for a, b, c, e in segs) + 20)); y1 = int(min(H, max(max(b, e) for a, b, c, e in segs) + 20))
    if x1 <= x0 or y1 <= y0: return
    m = np.zeros(((y1 - y0) * ss, (x1 - x0) * ss), np.uint8)
    for a, b, c, e in segs:
        cv2.line(m, (int((a - x0) * ss), int((b - y0) * ss)), (int((c - x0) * ss), int((e - y0) * ss)), 255, LW * ss, cv2.LINE_AA)
    m = cv2.resize(m, (x1 - x0, y1 - y0), interpolation=cv2.INTER_AREA).astype(np.float32)[..., None] / 255
    reg = d[y0:y1, x0:x1]
    J3.glow_screen(d, np.repeat(m, 3, 2) * 255, 10, 0.25, x0, y0)
    reg = d[y0:y1, x0:x1]; reg[:] = reg * (1 - m) + 250 * m


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
MOVES = chain(T0, T1, 0.05, dur=3.0)


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
    draw_strokes(d, strokes(t))
    return d


def sub(t, tf):
    X, top = xform(t); A = compose(X, cam(t))
    F = warp(plate(t, tf), A)
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
    return _R


def finished(n):
    t = n / FPS; R = v1()
    for s_ in R.SHOTS:                                                          # hard cuts both sides, no zoom
        if s_.name == '02ef_card': s_.tout = 'cut'
        if s_.name in ('02g_autodesk', '02h_nic'): s_.tin = 'cut'
    if t < T0 or t >= T1: return R.frame(n)                                     # neighbouring v1 shots
    out = frame_scene(t)
    return fin16.finish(np.clip(J3.grain(out, 4.5, seed=n), 0, 255), vig=0.60, tex=0.35, rb=0.50)


A0, A1 = 19.2, 22.2
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
