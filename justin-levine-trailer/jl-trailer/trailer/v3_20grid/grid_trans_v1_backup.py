"""v3 20 s transition: Autodesk (05) -> Nic (06) with the IG reel DfztsmVIC6x opening (study: refs_v3/ig_reel/study.md).
Hard cut at NEW 485 onto Nic built in a 3x3 tile grid: opening white wash, white tiles flashing in a clockwise spiral every
2 frames (pop, hold 2, fade on G1), mosaic cells until their tile passes, whole picture + grid settling 0.914 -> 1.0 on G1
over 36 frames, grid lines leave at j = 33 (the ref's cut). No blur anywhere (no defocus / zoom-blur), sub-frame motion blur only.
  python grid_trans.py still j ...            -> stills/j_XX.jpg
  python grid_trans.py seg                    -> v2segs/05_06_v3.mp4 (NEW 434-692)
  python grid_trans.py preview                -> ~/Downloads/Verticals_JL_v3_preview_A_20s_transition.mp4 (17.5-23.5 s)"""
import sys, os, math, subprocess
import numpy as np, cv2
sys.path.insert(0, '/Users/gourav/jl-trailer/trailer')
import render_v2 as RV
import engine
from newtime import n_old

FF = '/Users/gourav/ks-ron-build/reel1/ff'
HERE = '/Users/gourav/jl-trailer/trailer/v3_20grid/'
SEGD = '/Users/gourav/jl-trailer/trailer/v2segs/'
W, H, CX, CY = engine.W, engine.H, engine.CX, engine.CY
N0, NC, N1 = 434, 485, 692          # segment start, the cut, segment end
J_END = 33                          # grid lines + effect end here (the ref cuts away at f33)
ZDUR = 36.0                         # zoom settle length in frames (G1)
Z0 = 0.914
GK = 1.112                          # centre cell = GK x thirds x zoom
LINE_W, LINE_A, LINE_C = 4.0, 0.95, np.float32([6, 7, 9])
WHITE = np.float32([238, 241, 245])
WASH = [0.45, 0.28, 0.14]
# cells: (row, col); spiral order TL TM TR MR BR BM BL ML MM, one pop every 2 frames
ORDER = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0), (1, 1)]
MOSAIC = {(1, 0), (1, 1), (1, 2), (2, 1), (2, 2)}
BLOCK = 20


def G1(u):
    """Krish's graph 1, cubic-bezier(0,0,0,1): x = s^3, y = 3s^2 - 2s^3"""
    u = min(max(u, 0.0), 1.0); s = u ** (1 / 3); return 3 * s * s - 2 * s ** 3


def tile_alpha(jp):
    if jp < 0: return 0.0
    if jp < 2: return 1.0
    return 0.8 * (1 - G1((jp - 2) / 5.0))


def Z(j): return Z0 + (1 - Z0) * G1(j / ZDUR)


def grid(z):
    hw, hh = GK * z * W / 6, GK * z * H / 6
    return [0.0, CX - hw, CX + hw, float(W)], [0.0, CY - hh, CY + hh, float(H)]


def band(n, c, w):
    """anti-aliased 1-D coverage of a band of width w centred at c over pixels 0..n-1"""
    x = np.arange(n, dtype=np.float32) + 0.5
    return np.clip(np.minimum(x - (c - w / 2), (c + w / 2) - x) + 0.5, 0, 1)


def line_mask(z):
    xs, ys = grid(z); w = LINE_W * z
    mx = np.maximum(band(W, xs[1], w), band(W, xs[2], w))[None, :]
    my = np.maximum(band(H, ys[1], w), band(H, ys[2], w))[:, None]
    return np.maximum(mx, my)


def cell_mask(z, r, c):
    xs, ys = grid(z)
    x = np.arange(W, dtype=np.float32) + 0.5; y = np.arange(H, dtype=np.float32) + 0.5
    mx = np.clip(np.minimum(x - xs[c], xs[c + 1] - x) + 0.5, 0, 1); my = np.clip(np.minimum(y - ys[r], ys[r + 1] - y) + 0.5, 0, 1)
    return my[:, None] * mx[None, :]


def mosaic_cell(img, z, r, c):
    xs, ys = grid(z)
    x0, x1, y0, y1 = int(round(xs[c])), int(round(xs[c + 1])), int(round(ys[r])), int(round(ys[r + 1]))
    reg = img[y0:y1, x0:x1]; h, w = reg.shape[:2]; b = max(4, int(round(BLOCK * z)))
    # blocks anchored on the cell's inner corner (towards the frame centre) so edge blocks are the partial ones
    ax = 0 if c == 2 else (w % b if c == 0 else 0); ay = 0 if r == 2 else (h % b if r == 0 else 0)
    pw, ph = ((w + ax + b - 1) // b) * b, ((h + ay + b - 1) // b) * b
    pad = cv2.copyMakeBorder(reg, (b - ay) % b if ay else 0, 0, (b - ax) % b if ax else 0, 0, cv2.BORDER_REFLECT)
    ph2, pw2 = pad.shape[:2]; PH, PW = ((ph2 + b - 1) // b) * b, ((pw2 + b - 1) // b) * b
    pad = cv2.copyMakeBorder(pad, 0, PH - ph2, 0, PW - pw2, cv2.BORDER_REFLECT)
    sm = cv2.resize(pad, (PW // b, PH // b), interpolation=cv2.INTER_AREA)
    big = cv2.resize(sm, (PW, PH), interpolation=cv2.INTER_NEAREST)
    oy, ox = ph2 - h, pw2 - w
    img[y0:y1, x0:x1] = big[oy:oy + h, ox:ox + w]


_R = None
def nic():
    global _R
    if _R is None:
        R = RV.v1()
        i = [k for k, s in enumerate(R.SHOTS) if s.name == '02h_nic'][0]
        _R = (R, i, R.SHOTS[i])
    return _R


def zmin(A):
    """smallest extra screen zoom about the centre that still keeps the plate covering the frame"""
    lo, hi = 0.85, 1.0
    for _ in range(30):
        m = (lo + hi) / 2
        A2 = engine.compose(engine.zoom_about(m), A)
        pts = np.float32([[0, 0], [1920, 0], [0, 1080], [1920, 1080]]) @ A2[:, :2].T + A2[:, 2]
        ok = pts[:, 0].min() <= 0 and pts[:, 0].max() >= W and pts[:, 1].min() <= 0 and pts[:, 1].max() >= H
        if ok: hi = m
        else: lo = m
    return hi


def trans_frame(n):
    """NEW frame n in [NC, NC + J_END): Nic in the tile grid, unfinished float -> finished uint8"""
    R, i, sh = nic()
    j = n - NC; no = n_old(n); t = no / engine.FPS
    R.J3.RNG_T[0] = t
    # sub-frame count from the zoom speed (edge displacement over the half-frame shutter) and the v1 camera
    nv, _ = R.n_sub(sh, t)
    dz = abs(Z(j + 0.25) - Z(max(0.0, j - 0.25)))
    ns = int(np.clip(max(nv, math.ceil(dz * 1100 / 1.6)), 1, 16))
    acc = None; lm = np.zeros((H, W), np.float32); pc = {}
    cmask = {}
    for k in range(ns):
        d = (k / (ns - 1) - 0.5) * 0.5 if ns > 1 else 0.0           # frames, 180-degree shutter
        js = max(0.0, j + d); ts = t + d / engine.FPS
        A, AT, top = R.full_cam(sh, ts)
        z = max(Z(js), zmin(A))
        A2 = engine.compose(engine.zoom_about(z), A)
        key = sh.key(ts, t)
        if key not in pc: pc.clear(); pc[key] = np.ascontiguousarray(sh.plate(ts, t), dtype=np.float32)
        F = cv2.warpAffine(pc[key], A2, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        shd = sh.shade(ts)
        if shd is not None: F *= shd
        acc = F if acc is None else acc + F
        lm += line_mask(Z(js))
        for q, (r, c) in enumerate(ORDER):
            a = tile_alpha(js - 2 * q)
            if a > 0.002: cmask[(r, c)] = cmask.get((r, c), 0) + a * cell_mask(Z(js), r, c)
    out = acc / ns; lm /= ns
    zj = Z(j)
    for q, (r, c) in enumerate(ORDER):                          # mosaic until the cell's own white tile has popped
        if (r, c) in MOSAIC and j < 2 * q: mosaic_cell(out, zj, r, c)
    for rc, m in cmask.items():                                 # white tiles (pop, hold, fade on G1)
        m = (m / ns)[..., None]; out = out * (1 - m) + WHITE * m
    if j < len(WASH): out = out * (1 - WASH[j]) + WHITE * WASH[j]
    la = (lm * LINE_A)[..., None]; out = out * (1 - la) + LINE_C * la
    # captions on top, exactly as v1 draws them (screen space, unaffected by the grid zoom)
    A, AT, top = R.full_cam(sh, t)
    for it in sh.items:
        op = it.op(t) * top
        if op > 0.002: engine.apply_item(out, it.mc(it.anim(t) if it.anim else None), op, AT)
    return R.fin16.finish(np.clip(R.J3.grain(out, 2.2, seed=no), 0, 255), vig=0.60, tex=0.0, rb=0.35)


def frame(n):
    if n < NC: return RV.frame('adsk', n)
    if n < NC + J_END: return trans_frame(n)
    return RV.frame('v1', n)


def job(n): return np.ascontiguousarray(frame(n))


def encode(frames_iter, out, n):
    p = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', '24', out], stdin=subprocess.PIPE)
    k = 0
    for img in frames_iter: p.stdin.write(np.ascontiguousarray(img).tobytes()); k += 1
    p.stdin.close(); p.wait(); assert k == n, (k, n)


def read_all(f):
    raw = subprocess.run([FF, '-v', 'error', '-i', f, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'still':
        from PIL import Image
        os.makedirs(HERE + 'stills', exist_ok=True)
        for a in sys.argv[2:]:
            n = NC + int(a); Image.fromarray(frame(n)).save(HERE + f'stills/j_{int(a):03d}.jpg', quality=90); print(a, flush=True)
    elif mode == 'seg':
        import multiprocessing as mp
        out = SEGD + '05_06_v3.mp4'
        with mp.get_context('fork').Pool(int(os.environ.get('NW', 3))) as pool:
            encode(pool.imap(job, range(N0, N1), chunksize=2), out, N1 - N0)
        print('done', out, N1 - N0)
    elif mode == 'preview':
        a0, a1 = 420, 564                                           # 17.5 - 23.5 s
        seg = read_all(SEGD + '05_06_v3.mp4'); assert len(seg) == N1 - N0, len(seg)
        s04 = read_all(SEGD + '04_showcase.mp4')                    # NEW 353-434 (what the trailer shows before 434)
        fr = [s04[n - 353] for n in range(a0, N0)] + [seg[n - N0] for n in range(N0, a1)]
        tmp = HERE + '_prev_v.mp4'
        encode(iter(fr), tmp, a1 - a0)
        out = os.path.expanduser('~/Downloads/Verticals_JL_v3_preview_A_20s_transition.mp4')
        subprocess.run([FF, '-v', 'error', '-y', '-i', tmp, '-ss', f'{a0 / 24:.6f}', '-t', f'{(a1 - a0) / 24:.6f}',
                        '-i', '/Users/gourav/jl-trailer/trailer/audio/mix2.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                        '-c:a', 'aac', '-b:a', '256k', '-shortest', out], check=True)
        print('done', out, a1 - a0)
