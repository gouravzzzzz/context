"""Justin Levine (Shepherd) trailer -- frame loop: shots + transitions + real motion blur + finish.
  python render.py timeline            -> timeline.json (for mix.py)
  python render.py safe                -> every caption's box vs the 90 % title safe
  python render.py speed               -> camera speed per frame + spike / stuck check
  python render.py test t1 t2 ...      -> test/f_<t>.jpg
  python render.py full out.mp4 [aud]  -> chunked render, concat, mux (video length == audio length checked)
"""
import sys, os, json, math, subprocess
import numpy as np, cv2
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import *
import shots as SH

FF = '/Users/gourav/ks-ron-build/reel1/ff'
VOICE_END, BLACK, TITLE, END = 98.50, 98.58, 99.25, 102.60
SHOTS = SH.build(END, BLACK, TITLE)
NF = int(round(END * FPS))

ZT_OUT, ZT_AMT = 0.32, 0.24          # outgoing half of a zoom-through: graph 2 (slow -> fastest at the cut)
ZT_IN, ZT_IN_AMT = 0.85, 0.07        # incoming half: keeps zooming IN, graph 1 (fastest at the cut -> long settle)
WH_OUT, WH_IN = 0.26, 0.42           # whip pan halves
DISS = 3                             # frames of dissolve hiding a zoom-through / whip cut
I2 = np.float32([[1, 0, 0], [0, 1, 0]])


def idx_at(t):
    for i, s in enumerate(SHOTS):
        if s.t0 - 1e-9 <= t < s.t1 - 1e-9: return i
    return len(SHOTS) - 1


# ---------------------------------------------------------------- transition transforms (screen space, after the camera)
def xform(sh, ts):
    """returns (X for the picture, X for the text, text opacity)"""
    X = I2.copy(); XT = I2.copy(); top = 1.0
    if sh.tout == 'zt':
        u = cl((ts - (sh.t1 - ZT_OUT)) / ZT_OUT)
        if u > 0:
            z = zoom_about(1 + ZT_AMT * G2(u)); X = compose(z, X); XT = compose(z, XT); top *= 1 - EIO(u)
    elif sh.tout == 'whip':
        u = cl((ts - (sh.t1 - WH_OUT)) / WH_OUT)
        if u > 0:
            m = np.float32([[1, 0, -0.55 * W * G2(u)], [0, 1, 0]]); X = compose(m, X); XT = compose(m, XT); top *= 1 - EIO(u)
    if sh.tin == 'zt':
        v = cl((ts - sh.t0) / ZT_IN)
        X = compose(X, zoom_about(1 + ZT_IN_AMT * G1(v)))
    elif sh.tin == 'whip':
        v = cl((ts - sh.t0) / WH_IN)
        m = np.float32([[1, 0, 0.55 * W * (1 - G1(v))], [0, 1, 0]]); X = compose(m, X); XT = compose(m, XT)
    return X, XT, top


def full_cam(sh, ts):
    X, XT, top = xform(sh, ts)
    return compose(X, sh.cam(ts)), compose(XT, sh.text_T(ts)), top


def disp(A, B):
    pts = np.float32([[0, 0], [W, 0], [0, H], [W, H], [CX, CY]])
    pa = pts @ A[:, :2].T + A[:, 2]; pb = pts @ B[:, :2].T + B[:, 2]
    return float(np.abs(pa - pb).max())


def n_sub(sh, t):
    h = 0.25 / FPS
    d = disp(full_cam(sh, t - h)[0], full_cam(sh, t + h)[0]) + sh.speed(t) * 0.5
    n = int(np.clip(math.ceil(d / 1.6), 1, 16))
    if sh.key(t, t) is None and sh.kind == 'gfx': n = min(n, 10)
    return n, d


# ---------------------------------------------------------------- one shot at one sub-frame time
def draw(sh, ts, tf, plate_cache):
    k = sh.key(ts, tf)
    if k is not None and k in plate_cache: P = plate_cache[k]
    else:
        P = np.ascontiguousarray(sh.plate(ts, tf), dtype=np.float32)
        if k is not None: plate_cache.clear(); plate_cache[k] = P
    A, AT, top = full_cam(sh, ts)
    F = warp(P, A)
    if F is P: F = P.copy()
    shd = sh.shade(ts)
    if shd is not None: F *= shd
    sh.post(F, ts)
    beh = [it for it in sh.items if it.behind]
    if beh:
        m = sh.matte(tf)
        F0 = F.copy() if m is not None else None
        for it in beh:
            op = it.op(ts) * top
            if op > 0.002: apply_item(F, it.mc(it.anim(ts) if it.anim else None), op, AT)
        if m is not None:
            a = cv2.warpAffine(m, A, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)[..., None]
            F = F * (1 - a) + F0 * a
    for it in sh.items:
        if it.behind: continue
        op = it.op(ts) * top
        if op > 0.002: apply_item(F, it.mc(it.anim(ts) if it.anim else None), op, AT)
    return F


def whip_blur(img, sh, ts, n):
    """residual horizontal smear between sub-frames of a whip"""
    h = 0.25 / FPS / max(1, n)
    dx = abs(full_cam(sh, ts + h)[0][0, 2] - full_cam(sh, ts - h)[0][0, 2])
    k = int(dx)
    return cv2.blur(img, (k, 1)) if k >= 3 else img


_PC = {}
def shot_frame(i, t):
    sh = SHOTS[i]; n, d = n_sub(sh, t)
    pc = _PC.setdefault(i, {})
    if n == 1: return draw(sh, t, t, pc)
    acc = None
    for k in range(n):
        ts = t + (k / (n - 1) - 0.5) * 0.5 / FPS                  # 180-degree shutter
        f = draw(sh, ts, t, pc)
        if 'whip' in (sh.tin, sh.tout): f = whip_blur(f, sh, ts, n)
        acc = f if acc is None else acc + f
    return acc / n


def frame(n):
    t = n / FPS; J3.RNG_T[0] = t
    i = idx_at(t); sh = SHOTS[i]
    out = shot_frame(i, t)
    # dissolve hiding the cut of a zoom-through / whip (3 frames, centred on the cut)
    for j in (i, i + 1):
        if j <= 0 or j >= len(SHOTS): continue
        b = SHOTS[j]
        if b.tin not in ('zt', 'whip'): continue
        tc = b.t0; w = (t - (tc - DISS / 2 / FPS)) / (DISS / FPS)
        if 0 < w < 1:
            w = EIO(w)
            if j == i: out = shot_frame(j - 1, t) * (1 - w) + out * w
            else: out = out * (1 - w) + shot_frame(j, t) * w
    if sh.tin == 'flash' and n == int(math.ceil(sh.t0 * FPS - 1e-6)):
        out = 255 - np.clip(out, 0, 255)
    kind = sh.kind
    if sh.name == '10e_title':
        e = EIO(cl((t - sh.t0) / 0.6)) * (1 - EIO(cl((t - (END - 0.8)) / 0.8)))
        out = out * e
    if kind == 'black': return np.zeros((H, W, 3), np.uint8)
    if kind == 'spk': return fin16.finish(np.clip(J3.grain(out, 2.2, seed=n), 0, 255), vig=0.60, tex=0.0, rb=0.35)
    if kind == 'foot': return fin16.finish(np.clip(J3.grain(out, 3.0, seed=n), 0, 255), vig=0.60, tex=0.18, rb=0.40)
    return fin16.finish(np.clip(J3.grain(out, 4.5, seed=n), 0, 255), vig=0.60, tex=0.35, rb=0.50)


# ---------------------------------------------------------------- modes
def timeline():
    T = dict(END=END, VOICE_END=VOICE_END, BLACK=BLACK, TITLE=TITLE, CAL_FLIPS=SH.CAL_FLIPS,
             shots=[[s.name, round(s.t0, 3), round(s.t1, 3), s.tin] for s in SHOTS])
    json.dump(T, open(HERE + 'timeline.json', 'w'), indent=1); print('timeline.json', len(SHOTS), 'shots, END', END)


def safe():
    x0s, y0s, x1s, y1s = SAFE; bad = 0
    for s in SHOTS:
        for it in s.items:
            states = [None] if it.anim is None else sorted({it.anim(tt) for tt in np.arange(s.t0, s.t1, 1 / FPS)})[-1:]
            for a in states:
                r = it.mc(a)
                if r is None: continue
                x0, y0, M, C = r
                vis = (M.min(2) < 0.75) | (C.max(2) > 60)
                ys, xs = np.where(vis)
                if len(ys) == 0: continue
                bb = (x0 + xs.min(), y0 + ys.min(), x0 + xs.max() + 1, y0 + ys.max() + 1)
                ok = bb[0] >= x0s and bb[1] >= y0s and bb[2] <= x1s and bb[3] <= y1s
                if not ok and not it.behind: bad += 1; print('OUT ', s.name, bb)
    print('safe check done,', bad, 'outside')


def speed():
    prev = None; rows = []
    for n in range(NF):
        t = n / FPS; i = idx_at(t); sh = SHOTS[i]
        A = full_cam(sh, t)[0]; ns, d = n_sub(sh, t)
        v = disp(A, prev[1]) if prev is not None and prev[0] == i else None
        rows.append((n, sh.name, v, ns)); prev = (i, A)
    spikes = []
    def in_trans(t):
        for s in SHOTS:
            if s.tin in ('zt', 'whip') and s.t0 - ZT_OUT - 0.05 <= t <= s.t0 + 0.12: return True
            if s.name == '04_fifteen' and 0 <= t - SH.wt('15', 40) < 0.35: return True
        return False
    for k in range(2, len(rows)):
        if in_trans(rows[k][0] / FPS): continue
        a, b, c = rows[k - 2][2], rows[k - 1][2], rows[k][2]
        if None in (a, b, c): continue
        if c > 2.2 * max(a, b) + 1.0 and c > 3: spikes.append(rows[k])
    vs = [r[2] for r in rows if r[2] is not None]
    print('frames', len(rows), 'median cam speed %.2f px/f, p95 %.2f, max %.2f' % (np.median(vs), np.percentile(vs, 95), max(vs)))
    print('sub-frames: total', sum(r[3] for r in rows), 'frames with blur', sum(1 for r in rows if r[3] > 1))
    still = [r for r in rows if r[2] is not None and r[2] < 0.02]
    print('camera parked frames (<0.02 px/f):', len(still), [r[:2] for r in still[:10]])
    print('spikes (non-cut):', [(r[0], r[1], round(r[2], 1)) for r in spikes[:40]])


CH = HERE + 'chunks/'
def render_chunk(args):
    c, a, b = args
    p = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                          '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', '-r', '24', CH + f'c{c:03d}.mp4'],
                         stdin=subprocess.PIPE)
    for n in range(a, b):
        p.stdin.write(np.ascontiguousarray(frame(n)).tobytes())
    p.stdin.close(); p.wait()
    print(f'chunk {c} done ({a}-{b})', flush=True)
    return c


def nframes(p):
    o = subprocess.run([FF, '-i', p, '-map', '0:v:0', '-c', 'copy', '-f', 'null', '-'], capture_output=True, text=True).stderr
    import re
    return int(re.findall(r'frame=\s*(\d+)', o)[-1])


def main():
    mode = sys.argv[1]
    if mode == 'timeline': return timeline()
    if mode == 'safe': return safe()
    if mode == 'speed': return speed()
    if mode == 'test':
        out = HERE + 'test/'; os.makedirs(out, exist_ok=True)
        for a in sys.argv[2:]:
            n = int(round(float(a) * FPS)); Image.fromarray(frame(n)).save(out + f'f_{float(a):06.2f}.jpg', quality=90); print('frame', a, flush=True)
        return
    if mode in ('full', 'seg'):
        if mode == 'full': n0, n1, out = 0, NF, sys.argv[2]; aud = sys.argv[3] if len(sys.argv) > 3 else None
        else: n0, n1, out = int(round(float(sys.argv[2]) * FPS)), int(round(float(sys.argv[3]) * FPS)), sys.argv[4]; aud = None
        os.makedirs(CH, exist_ok=True)
        for f in os.listdir(CH): os.remove(CH + f)
        step = 48; jobs = [(c, a, min(n1, a + step)) for c, a in enumerate(range(n0, n1, step))]
        import multiprocessing as mp
        nw = int(os.environ.get('NW', 8))
        with mp.get_context('fork').Pool(nw, maxtasksperchild=6) as pool:
            for c in pool.imap_unordered(render_chunk, jobs): pass
        open(CH + 'list.txt', 'w').write(''.join(f"file 'c{c:03d}.mp4'\n" for c, _, _ in jobs))
        vid_only = CH + 'video.mp4'
        subprocess.run([FF, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', CH + 'list.txt', '-c', 'copy', vid_only], check=True)
        nv = nframes(vid_only); print('video frames', nv, 'expected', n1 - n0, '=', nv / FPS, 's')
        assert nv == n1 - n0, 'frame count mismatch'
        cmd = [FF, '-v', 'error', '-y', '-i', vid_only]
        if aud: cmd += ['-i', aud, '-map', '0:v', '-map', '1:a', '-c:a', 'aac', '-b:a', '320k', '-t', f'{nv / FPS:.4f}']
        subprocess.run(cmd + ['-c:v', 'copy', '-movflags', '+faststart', out], check=True)
        print('done', out)


if __name__ == '__main__':
    main()
