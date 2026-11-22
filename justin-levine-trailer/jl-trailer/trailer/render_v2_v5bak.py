"""Trailer v2: my segments on the NEW (tight-cut) timeline. Each NEW frame n shows the OLD frame n_old(n) (whole-frame shift
per kept stretch, jump cuts in the removed pauses), with:
  - no zoom-through anywhere (every 'zt' -> hard cut), no slow-motion hold patches (real frames only)
  - 10-14 s = alt_10_14/scene_v5 (feathered wipe, v2 camera, black name boxes), 20 s = alt_20/scene_adsk (to -> star)
  - 07b_calendar block centred vertically, 08b 'No.' moved to his left (screen left) in the gradient colour
  python render_v2.py SEG n0 n1 out.mp4   (SEG: v1 | s1014 | adsk)      python render_v2.py still SEG n ..."""
import sys, os, subprocess, importlib.util
import numpy as np, cv2
sys.path.insert(0, '/Users/gourav/jl-trailer/trailer')
import engine
from newtime import n_old, A
FPS = 24
engine.PATCH_MAP.clear()
FF = '/Users/gourav/ks-ron-build/reel1/ff'
HERE = '/Users/gourav/jl-trailer/trailer/'


def fix_v1(R):
    """applied to every render.py instance: hard cuts instead of zoom-throughs + Krish's layout notes (v2 + v3 rounds)"""
    L, J3 = engine.L, engine.J3
    by = {sh.name: sh for sh in R.SHOTS}
    for sh in R.SHOTS:
        if sh.tin == 'zt': sh.tin = 'cut'
        if sh.tout == 'zt': sh.tout = 'cut'
        if getattr(sh, '_v3', False): continue
        sh._v3 = True
        purple_items(sh, L)
        if sh.name == '07b_calendar': fix_calendar(sh, L, J3)
    s8b, s8c = by.get('08b_no'), by.get('08c_consistently')
    if s8b is not None and not getattr(s8b, '_v3b', False):
        s8b._v3b = True; fix_no(s8b, s8c, L)


# ---------------------------------------------------------------- v3: some key words in a blue -> purple gradient (Krish)
PURPLE = ((70, 185, 255), (165, 92, 255))
PURPLE_WORDS = {'02d_founded': ['construction'], '02h_nic': ['partnerships'], '06a_risk': ['manager'],
                '07a_inception': ['inception'], '08a_luke': ['AI bubble?']}


def purple_items(sh, L):
    for it in sh.items:
        f = it.draw
        if not getattr(f, '__closure__', None): continue
        env = dict(zip(f.__code__.co_freevars, [c.cell_contents for c in f.__closure__]))
        if env.get('txt') in PURPLE_WORDS.get(sh.name, []) and {'px', 'x', 'y', 'align', 'face', 'glow'} <= set(env):
            it.draw = (lambda d, e=env: L.grad_text(d, e['txt'], e['px'], e['x'], e['y'], align=e['align'], face=e['face'],
                                                     glow=e['glow'], c0=PURPLE[0], c1=PURPLE[1]))
            it.cache.clear()


# ---------------------------------------------------------------- v3: 'No.' on his left in purple; 08b -> 08c is ONE take (Krish: "abrupt cut at 1:09")
NO_X = 740           # right edge of 'No.' just left of his face


def fix_no(s8b, s8c, L):
    it = s8b.items[0]
    def no(d, a): L.grad_text(d, 'No.', int(460 * (1.10 - 0.10 * a)), NO_X, 580, align='right', glow=0.34, c0=PURPLE[0], c1=PURPLE[1])
    it.draw = no; it.cache.clear()
    if s8c is None: return
    t0 = s8c.t0
    mv = []                                                          # v5: talking head stable (no push) across both
    s8b.moves = mv; s8c.moves = mv; s8c.z0 = s8b.z0
    s8c.tin = 'cut'
    s8c.items.insert(0, engine.Item(t0 - 1e-3, lambda d: no(d, 1.0), t_off=t0, fin=0.0, fout=0.22))   # 'No.' fades out
    for k in (1, 2): s8c.items[k].t_on = max(s8c.items[k].t_on, t0 + 0.09)                          # captions after it
    SH = s8c._shade
    s8c._shade = lambda ts, SH=SH: 1.0 - (1.0 - SH) * engine.EIO(engine.cl((ts - t0) / 0.40))         # shade fades in


# ---------------------------------------------------------------- v3: calendar block centred in BOTH states (glides up as the
# lower lines arrive) + the '11 MONTHS' box in the trailer's solid blue key-box style
CAL = {}


def fix_calendar(sh, L, J3):
    M = sys.modules[type(sh).__module__]
    wt = M.wt; LEAD = engine.LEAD
    t11 = wt('11') - 0.08
    BOX_CY, PXB, TXT = 868, 84, '11 MONTHS'
    rg, asc = L.text_rgba(TXT, PXB)
    bw, bh = rg.shape[1] + 2 * 30, int(PXB * 1.10)
    def box(d, a):
        x0, y0 = int(engine.CX - bw / 2), int(BOX_CY - bh / 2)
        shd = np.zeros((bh, bw, 4), np.float32); shd[..., 3] = 1
        J3.drop_shadow(d, shd, x0, y0, 1.0, strength=0.45)
        d[y0:y0 + bh, x0:x0 + bw] = L.gbox(bw, bh)
        if a > 0: L.put_text(d, TXT[:a], PXB, x0 + 30, int(BOX_CY + PXB * 0.33), glow=0.12)
    sh.items[3] = engine.Item(t11, box, fin=0.10, anim=lambda t: int(np.clip(round((t - t11 - 0.05) * 15), 0, len(TXT))))
    def pad(d, ts):                                              # the v1 pad + flips, without the tech ground
        px0, py0 = engine.CX - 150, 318
        for k in range(3):
            pg = M.page(11)
            J3.drop_shadow(d, pg, px0 + (2 - k) * 4, py0 + (2 - k) * 5, 1.0, strength=0.45); J3.over(d, pg, px0 + (2 - k) * 4, py0 + (2 - k) * 5)
        done = sum(1 for tf_ in M.CAL_FLIPS if ts >= tf_ + M.FLIP_DUR)
        top = done + 1
        if top <= 10: J3.over(d, M.page(top + 1) if top + 1 <= 11 else M.page(11), px0, py0); J3.over(d, M.page(top), px0, py0)
        for k, t_f in enumerate(M.CAL_FLIPS):
            u = (ts - t_f) / M.FLIP_DUR
            if 0 <= u < 1:
                th = 112 * M.G2(u)
                fw, x, y = M.flip_warp(M.page(k + 1), th, px0, py0)
                a = 1 - engine.cl((th - 80) / 32)
                J3.drop_shadow(d, fw, x, y, a, strength=0.4); J3.over(d, fw, x, y, a)
    CAL.update(sh=sh, pad=pad, M=M)
    T_G, G_D = wt('was', 69.6) - LEAD - 0.22, 0.80
    def DY(ts): return CAL_DY_E + (CAL_DY_L - CAL_DY_E) * engine.EU(engine.cl((ts - T_G) / G_D))
    def plate(ts, tf):
        d = engine.tech(30, tf)
        P0 = np.zeros_like(d); P1 = np.full_like(d, 200.0); pad(P0, ts); pad(P1, ts)
        Mx, C = (P1 - P0) / 200.0, P0
        T = np.float32([[1, 0, 0], [0, 1, DY(ts)]])
        Mx = cv2.warpAffine(Mx, T, (engine.W, engine.H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(1, 1, 1))
        C = cv2.warpAffine(C, T, (engine.W, engine.H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
        return d * Mx + C
    sh.plate = plate
    tT = sh.text_T
    def text_T(ts, tT=tT):
        T = np.array(tT(ts), np.float32); T[1, 2] += DY(ts); return T
    sh.text_T = text_T
    sp = sh.speed
    sh.speed = lambda ts, sp=sp: sp(ts) + 2.0 * abs(DY(ts + 0.5 / FPS) - DY(ts - 0.5 / FPS))


CAL_DY_E, CAL_DY_L = 122, 2          # measured: early block (texts + pad) centre 412.5, full block centre 533 -> both on 535


_R = None
def v1():
    global _R
    if _R is None:
        sp = importlib.util.spec_from_file_location('jl_render_v2', HERE + 'render.py')
        _R = importlib.util.module_from_spec(sp); sp.loader.exec_module(_R); fix_v1(_R)
    return _R


_S = {}
def src(seg):
    if seg in _S: return _S[seg]
    if seg == 's1014':
        sys.path.insert(0, HERE + 'alt_10_14/'); import scene_v5 as m
        fix_v1(m.V.v1())
        sp = importlib.util.spec_from_file_location('open_v3_scene', HERE + 'open_v3/scene.py')   # v3 opening captions carry over
        OS = importlib.util.module_from_spec(sp); sp.loader.exec_module(OS); OS.install(m.V.v1())
    elif seg == 'adsk':
        sys.path.insert(0, HERE + 'alt_20/'); import scene_adsk as m
        R = m.v1(); fix_v1(R)
        for sh in R.SHOTS:
            if sh.name == '02ef_card':
                for it in sh.items[2:4]: it.t_on = 1e9                   # 'We sold / our business' never shown (v2 showcase lands here)
    else: m = None
    _S[seg] = m
    return m


OVR = {1392: 1557, 1846: 2104, 1847: 2105, 1848: 2106}   # 10_split: start on the silent frames just before the 87.2-87.8 cut -> continuous into 1849   # shot heads that a removed pause / rounding put one old frame early (would flash the previous v1 shot)


def frame(seg, n):
    no = OVR.get(n, n_old(n)) if seg == 'v1' else n_old(n)
    m = src(seg)
    if m is None: return v1().frame(no)
    return m.finished(no)


_SEG = None
def job(n): return np.ascontiguousarray(frame(_SEG, n))


if __name__ == '__main__':
    if sys.argv[1] == 'still':
        from PIL import Image
        os.makedirs(HERE + 'stills_v2b', exist_ok=True)
        for a in sys.argv[3:]:
            Image.fromarray(frame(sys.argv[2], int(a))).save(HERE + f'stills_v2b/{sys.argv[2]}_{int(a):05d}.jpg', quality=90); print(a, flush=True)
    else:
        seg, n0, n1, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        W, H = engine.W, engine.H
        p = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', '24', out], stdin=subprocess.PIPE)
        import multiprocessing as mp
        _SEG = seg
        with mp.get_context('fork').Pool(int(os.environ.get('NW', 3))) as pool:
            for img in pool.imap(job, range(n0, n1), chunksize=2): p.stdin.write(img.tobytes())
        p.stdin.close(); p.wait(); print('done', out, n1 - n0)
