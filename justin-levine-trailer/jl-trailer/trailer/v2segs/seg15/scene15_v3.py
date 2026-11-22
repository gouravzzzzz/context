"""v3 of seg 15: NEW 1660-1846 (186 frames). Krish: "to transition from previous scene to this one lets slide this photo line
from right to left then fade the background into this one then continue with our animation".
  1660-1661  plain v1 08c_consistently (render_v2.frame('v1', n)) -- hard cut in
  1661->     the photo line (v1 stream) slides in from the RIGHT edge, right->left, on G1 (fast, then settles), real motion blur;
             it rides low on Justin's shirt (off his face) and is in place by "consistently" (1675)
  1683-1696  the line glides up to the centre line on Krish's EU while the background fades Justin -> black "01" ground
             (1682-1694, his captions go with his shot); the cards burst out of the line on "underestimated" as before
  from ~1695 the v2 animation unchanged (collage -> carousel -> B-roll, captions)
  python scene15_v3.py stills n ... | render (PNG cache, then preview + final)"""
import sys, os, math, subprocess
import numpy as np, cv2
cv2.setNumThreads(1)
from PIL import Image
sys.path.insert(0, '/Users/gourav/jl-trailer/trailer/v2segs/seg15')
import scene15 as B
from scene15 import *
import importlib.util
_sp = importlib.util.spec_from_file_location('jl_render_v2_mod', '/Users/gourav/jl-trailer/trailer/render_v2.py')
RV = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(RV)     # by path: 'render_v2' resolves to the Kristina build
from newtime import n_old

HERE3 = '/Users/gourav/jl-trailer/trailer/v2segs/seg15/'
CACHE = HERE3 + 'v3png/'
OUT3 = '/Users/gourav/jl-trailer/trailer/v2segs/15_cloud_lloyds_v3.mp4'
PREV = '/Users/gourav/Downloads/Verticals_JL_v3_preview_C_collage.mp4'
MIX = '/Users/gourav/jl-trailer/trailer/audio/mix2.wav'
P0, P1 = 1640, 1781            # preview NEW 1640-1780
V0, V1 = 1660, 1846            # v3 deliverable

SL0, SL_D = fr(1679), 0.45   # v3b (Krish): line slides in at the END of his shot, on the centre line
Y_LOW = float(CY)   # v3b (Krish): line slides in at the END of his shot, on the centre line
UP0, UP_D = fr(1683), 0.55     # glide up to the centre line on EU (lands 1696), mostly after his face has faded
BF0, BF_D = fr(1688), 0.33   # v3b (Krish): line slides in at the END of his shot, on the centre line
STRIP_FIRST = 1680   # v3b (Krish): line slides in at the END of his shot, on the centre line


def slide_x(t):
    """offset of the whole line from its resting place (G1: fastest at the entry, long settle)"""
    return (W - 10.0) * (1 - G1(cl((t - SL0) / SL_D)))
def strip_y(t): return Y_LOW + (CY - Y_LOW) * EU(cl((t - UP0) / UP_D))
def bg_fade(t): return EIO(cl((t - BF0) / BF_D))


def strip_layer(t, op):
    """the v1 line as an RGBA layer (premultiplied) at time t: rigid slide + its own 140 px/s scroll"""
    lay = np.zeros((H, W, 4), np.float32)
    if op <= 0.003: return lay, 0
    X = slide_x(t); yc = strip_y(t); y0 = int(round(yc)) - 15
    off = (t - B.T_IN) * 140.0; pitch = 49; k0 = int(off // pitch)
    for j in range(-1, W // pitch + 2):
        x = j * pitch - (off - k0 * pitch) + 30
        if x < 20 or x > W - 60: continue
        x += X
        if x > W: continue
        idx = ((j + k0) * 7) % len(S.AI_CARDS)
        if idx not in B._TH:
            f, fx, fy, asp, z = S.AI_CARDS[idx]; B._TH[idx] = L.fit(SH.cimg(f), 40, 30, fx, fy, z) * 0.82
        xi = int(round(x)); x1 = min(W, xi + 40)
        if x1 <= xi: continue
        lay[y0:y0 + 30, xi:x1, :3] = B._TH[idx][:, :x1 - xi] / 255.0; lay[y0:y0 + 30, xi:x1, 3] = 1.0
    return lay, y0


def put_strip(d, t, op):
    """composite the line with real motion blur (box along its motion over the 180-degree shutter)"""
    if op <= 0.003: return
    lay, y0 = strip_layer(t, op)
    h = 0.25 / FPS
    dx = abs(slide_x(t + h) - slide_x(t - h)) + 140.0 * 0.5 / FPS
    dy = abs(strip_y(t + h) - strip_y(t - h))
    kx, ky = max(1, int(round(dx))), max(1, int(round(dy)))
    pad = ky // 2 + 2; a0, a1 = max(0, y0 - pad), min(H, y0 + 30 + pad)
    band = lay[a0:a1]
    if kx > 1 or ky > 1: band = cv2.blur(band, (kx, ky), borderType=cv2.BORDER_CONSTANT)
    a = band[..., 3:4] * op
    reg = d[a0:a1]; reg[:] = reg * (1 - a) + band[..., :3] * 255.0 * op


# the cards burst out of the line wherever it is (it lands on the centre line at 1691, as in v2 from then on)
def collage_state(c, t):
    e = G1(cl((t - (B.T_IN + 0.035 * c['vk'])) / 0.65))
    w = 40 + (c['w'] - 40) * e; h = 30 + (c['h'] - 30) * e
    ys = strip_y(t)
    x = c['sx'] + (c['x'] + c['w'] / 2 - c['sx']) * e; y = ys + (c['y'] + c['h'] / 2 - ys) * e
    z = B.zc(t)
    return e, CX + (x - CX) * z, CY + (y - CY) * z, w * z, h * z
B.collage_state = collage_state


# ---- Justin's shot (08c_consistently, v1 with all v2 fixes), carried on past the old cut so it can fade
_JI = None
def justin_raw(n):
    global _JI
    R = RV.v1()
    if _JI is None:
        _JI = [k for k, s in enumerate(R.SHOTS) if s.name == '08c_consistently'][0]
        sh = R.SHOTS[_JI]; sh.n1 = 1912; sh.t1 = 1912 / FPS          # real footage keeps running (lip-synced), no hold
    to = n_old(n) / FPS; J3.RNG_T[0] = to
    return R.shot_frame(_JI, to)


def raw3(n):
    t = n / FPS; f = bg_fade(t)
    base = justin_raw(n) if f < 0.999 else None
    J3.RNG_T[0] = t
    if f > 0.001:
        bg = tech(37, t, 0.55)
        base = bg if base is None else base * (1 - f) + bg * f
    put_strip(base, t, B.stream_op(t))
    h = 0.25 / FPS
    ns = int(np.clip(math.ceil(B.disp(t - h, t + h) / 2.0), 1, 12))
    acc = None
    for k in range(ns):
        ts = t + ((k / (ns - 1) - 0.5) * 0.5 / FPS if ns > 1 else 0.0)
        d = base.copy()
        for dep, x, y, w, hh, op, lay, key in B.layout(ts): B.draw_card(d, t, x, y, w, hh, op, lay)
        acc = d if acc is None else acc + d
    out = acc / ns
    for it in B.CAPS:
        op = it.op(t)
        if op > 0.002: apply_item(out, it.mc(it.anim(t) if it.anim else None), op)
    return out, f


def finished3(n):
    if n < STRIP_FIRST: return RV.frame('v1', n)
    out, f = raw3(n)
    gfx = lambda: fin16.finish(np.clip(J3.grain(out, 4.5, seed=n), 0, 255), vig=0.60, tex=0.35, rb=0.50)
    spk = lambda: fin16.finish(np.clip(J3.grain(out, 2.2, seed=n_old(n)), 0, 255), vig=0.60, tex=0.0, rb=0.35)
    if f >= 0.999: return gfx()
    if f <= 0.001: return spk()
    return np.clip(spk().astype(np.float32) * (1 - f) + gfx().astype(np.float32) * f + 0.5, 0, 255).astype(np.uint8)


def job(n):
    p = CACHE + f'{n}.png'
    if not os.path.exists(p):
        Image.fromarray(np.ascontiguousarray(finished3(n))).save(p + '.tmp.png', compress_level=1); os.replace(p + '.tmp.png', p)
    return n


def encode(n0, n1, out, audio):
    cmd = [FF, '-v', 'error', '-y', '-framerate', '24', '-start_number', str(n0), '-i', CACHE + '%d.png']
    if audio: cmd += ['-ss', f'{n0 / FPS:.6f}', '-t', f'{(n1 - n0) / FPS:.6f}', '-i', MIX, '-map', '0:v', '-map', '1:a', '-c:a', 'aac', '-b:a', '320k']
    cmd += ['-frames:v', str(n1 - n0), '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', '24']
    if audio: cmd += ['-t', f'{(n1 - n0) / FPS:.6f}']
    subprocess.run(cmd + [out], check=True)


if __name__ == '__main__':
    os.makedirs(CACHE, exist_ok=True)
    if sys.argv[1] == 'stills':
        os.makedirs(HERE3 + 'stills3', exist_ok=True)
        for a in sys.argv[2:]:
            n = int(a); Image.fromarray(finished3(n)).save(HERE3 + f'stills3/s_{n}.jpg', quality=90); print(n, flush=True)
    elif sys.argv[1] == 'final':                   # deliverable only (preview rebuilt by the coordinator)
        import multiprocessing as mp
        with mp.get_context('fork').Pool(int(os.environ.get('NW', 3))) as pool:
            for i, n in enumerate(pool.imap(job, list(range(V0, V1)), chunksize=1)):
                if i % 10 == 0: print('frame', n, flush=True)
        encode(V0, V1, OUT3, False)
        encode(V0, V1, OUT3.replace('.mp4', '_check.mp4'), True)
        print('done', OUT3, V1 - V0, 'frames', flush=True)
    elif sys.argv[1] == 'render':
        import multiprocessing as mp
        todo = list(range(P0, V1))
        with mp.get_context('fork').Pool(int(os.environ.get('NW', 3))) as pool:
            for i, n in enumerate(pool.imap(job, todo, chunksize=1)):
                if n == P1 - 1:
                    encode(P0, P1, PREV, True); print('preview done', PREV, flush=True)
                if i % 10 == 0: print('frame', n, flush=True)
        encode(V0, V1, OUT3, False)
        encode(V0, V1, OUT3.replace('.mp4', '_check.mp4'), True)
        print('done', OUT3, V1 - V0, 'frames', flush=True)
