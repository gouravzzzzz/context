"""v3 OPENING, NEW frames 0-206 (0-8.58 s): v1 01_justin + whip + 02a_nic (camera, shade, whip, lip-sync untouched),
every v1 caption removed ('UNDERWRITERS ARE NEXT' gone), new captions animated like Krish's ref
'/Users/gourav/Krish works/Trailer 1.mp4' 11-16 s (study: open_v3/STUDY.txt):
  - each word CUTS ON whole on the frame it is spoken (no fade / rise / blur / scale), no exit animation
  - single words replace each other in one column; a key phrase BUILDS in place into a 2-3 line left-aligned block
    (words appended on their line, the next line starts under it), the key word on a solid box; the whole block
    CUTS OFF on the frame the next word cuts on
  - text rides the shot's camera (scene-locked, the v1 partial text tracking), it never animates on its own
  - Instrument Serif 112 px at 1080p ('h' 83 px tall), baseline step 126 px, block vertically centred, box -0.90/+0.29 em,
    0.107 em side pad, ONE left column (singles + blocks share the left edge here: alignment by side)
The captions are engine Items inside the v1 shots, so they get the same sub-frame motion blur, whip and finish.
  python scene.py still n ...         python scene.py plate n ...        python scene.py render out.mp4
"""
import sys, os, math, subprocess
import numpy as np
sys.path.insert(0, '/Users/gourav/jl-trailer/trailer')
import render_v2 as RV
import engine
from engine import Item, J3, L, W, H
from newtime import n_old, WORDS
FF = '/Users/gourav/ks-ron-build/reel1/ff'
HERE = '/Users/gourav/jl-trailer/trailer/open_v3/'
N0, N1 = 0, 206
FPS = 24
LEAD = 0.05                    # text lands a touch before the word (trailer rule)
PX = 112                       # ref: 'the' is 83 px from the h top to the baseline -> 112 px Instrument Serif
STEP = 126 / 112               # ref baseline step 126 px
YC = 579                       # ref single-word baseline (x-height centred on the frame centre)
FIRST_NIC = 158                # first NEW frame of 02a_nic


def wnew(word, after=0.0):
    return next(w[0] for w in WORDS if w[2] == word and w[0] >= after - 1e-6)


def nframe(word, after=0.0, lo=0):
    return max(lo, int(math.floor((wnew(word, after) - LEAD) * FPS + 0.5)))


def t_old(N):
    """OLD time at which a hard cut must sit so it lands exactly on NEW frame N (shutter samples +-0.25 f never straddle)"""
    return (n_old(N) - 0.5) / FPS


# ---------------------------------------------------------------- drawing (trailer look: white serif, gradient box, shadow + glow)
def word_lay(words, px):
    sp = J3.font(px).getlength(' ') * 0.95; xx = 0.0; out = []
    for w in words:
        rg, asc = J3.text_rgba(w, px, hs=1.0); out.append((w, rg, asc, xx)); xx += rg.shape[1] + sp
    return out, xx - sp


def draw_word(d, w, x, by, px, style):
    rg, asc = J3.text_rgba(w, px, hs=1.0)
    if style == 'box':
        bx0, bx1 = int(x - px * 0.107), int(x + rg.shape[1] + px * 0.107)          # ref 'Twitter' box: 12 px pad,
        by0, by1 = int(by - px * 0.90), int(by + px * 0.29)                        # 101 px above / 32 below the baseline
        sh = np.zeros((by1 - by0, bx1 - bx0, 4), np.float32); sh[..., 3] = 1
        J3.drop_shadow(d, sh, bx0, by0, 1.0, strength=0.45)
        J3.glow_screen(d, L.gbox(bx1 - bx0, by1 - by0) * 0.55, 16, 0.22, bx0, by0)
        d[by0:by1, bx0:bx1] = L.gbox(bx1 - bx0, by1 - by0)
        J3._put_word(d, rg, asc, x, by, (1.0, 0, 0, 0), True, 0.10)
    elif style == 'purple':                                                         # Krish v3: some key words blue -> purple
        L.grad_text(d, w, px, x, by, glow=0.30, c0=RV.PURPLE[0], c1=RV.PURPLE[1])
    elif style == 'grad':
        L.grad_text(d, w, px, x, by, glow=0.30)
    else:
        J3._put_word(d, rg, asc, x, by, (1.0, 0, 0, 0), True, 0.18)


def block_items(lines, x, align, t_end, yc=YC, px=PX, keys=(), grads=(), purples=()):
    """lines = [[(N_new, word), ...], ...]: each word its own hard-cut Item, laid out ONCE in its final place.
    align 'left': every line starts at x; 'right': every line ends at x (alignment by side). Vertically centred on yc."""
    k = len(lines); its = []
    for li, line in enumerate(lines):
        by = yc + (li - (k - 1) / 2) * px * STEP
        lay, lw = word_lay([w for _, w in line], px)
        x0 = x if align == 'left' else x - lw
        for (N, w), (_, rg, asc, xo) in zip(line, lay):
            st = 'box' if w in keys else ('purple' if w in purples else ('grad' if w in grads else 'plain'))
            its.append(Item(t_old(N), (lambda d, w=w, xx=x0 + xo, by=by, st=st: draw_word(d, w, xx, by, px, st)),
                            t_off=t_end, fin=0, fout=0))
    return its


def captions():
    """returns {shot name: [Items]} -- times are OLD (the v1 shot clock), cut points are NEW frames"""
    nf = nframe
    # ---- Justin: ONE LEFT column like the ref (left of his face, on the v1 left shade, kept for the whole shot), left-aligned
    XL = 150                                            # ref left edge 246 px; our speaker sits centred -> further left, clear of his face
    a_our, a_eng, a_team = nf('our'), nf('engineering'), nf('team')
    a_sp, a_zero, a_time, a_wr, a_code = nf('spends'), nf('zero'), nf('time,'), nf('writing'), nf('code')
    b_and, b_100, b_of, b_their, b_time = nf('and', 3.3), nf('100'), nf('of', 4.0), nf('their', 4.0), nf('time,', 4.2)
    c_orch = nf('orchestrating,')
    c_how, c_the, c_code, c_is, c_wr = nf('how', 5.4), nf('the', 5.6), nf('code', 5.7), nf('is', 5.9), nf('written.')
    END_J = 1e9                                         # last Justin block rides out with the v1 whip (its own fade)
    J = []
    J += block_items([[(a_our, 'Our')]], XL, 'left', t_old(a_eng))
    J += block_items([[(a_eng, 'engineering')]], XL, 'left', t_old(a_team))
    J += block_items([[(a_team, 'team')]], XL, 'left', t_old(a_sp))
    J += block_items([[(a_sp, 'spends')], [(a_zero, 'zero'), (a_time, 'time,')], [(a_wr, 'writing'), (a_code, 'code')]],
                     XL, 'left', t_old(b_and), keys=('zero',))
    J += block_items([[(b_and, 'and'), (b_100, '100%')], [(b_of, 'of'), (b_their, 'their'), (b_time, 'time,')]],
                     XL, 'left', t_old(c_orch), purples=('100%',))
    J += block_items([[(c_orch, 'orchestrating')]], XL, 'left', t_old(c_how), purples=('orchestrating',))
    J += block_items([[(c_how, 'how'), (c_the, 'the'), (c_code, 'code')], [(c_is, 'is'), (c_wr, 'written.')]],
                     XL, 'left', END_J)
    # ---- Nic: LEFT column (v1 left shade), left-aligned
    XN = 150
    d_today = nf('Today,', lo=FIRST_NIC)
    d_we, d_sup, d_exc, d_to, d_br = nf("we're"), nf('super'), nf('excited'), nf('to', 8.1), nf('bring')
    d_on = nf('on', 8.6)                                # NEW 209: after this segment; only shows if the next one installs these
    Nn = []
    Nn += block_items([[(d_today, 'Today,')]], XN, 'left', t_old(d_we))
    Nn += block_items([[(d_we, "we're"), (d_sup, 'super')], [(d_exc, 'excited')], [(d_to, 'to'), (d_br, 'bring'), (d_on, 'on')]],
                      XN, 'left', 1e9, keys=('excited',))
    return {'01_justin': J, '02a_nic': Nn}


def install(R, clean=False):
    """replace the v1 caption items of 01_justin / 02a_nic in a render.py instance (also usable for the next segment)"""
    caps = captions()
    for sh in R.SHOTS:
        if sh.name in caps:
            sh.items = [] if clean else caps[sh.name]
            if sh.name == '01_justin':                              # text stays on his left -> keep a left shade (the ref's
                sh._shade = engine.side_shade_map('left', 0.48, 0.24)   # left side is dark too) instead of v1's switch to the right
    R._PC.clear() if hasattr(R, '_PC') else None


def frame(n):
    return RV.frame('v1', n)


def job(n): return np.ascontiguousarray(frame(n))


if __name__ == '__main__':
    mode = sys.argv[1]
    install(RV.v1(), clean=(mode == 'plate'))
    if mode in ('still', 'plate'):
        from PIL import Image
        os.makedirs(HERE + 'stills', exist_ok=True)
        for a in sys.argv[2:]:
            Image.fromarray(frame(int(a))).save(HERE + f'stills/{mode}_{int(a):03d}.jpg', quality=90); print(a, flush=True)
    elif mode == 'times':
        for k, v in captions().items():
            for it in v: print(k, round(it.t_on, 3), it.t_off)
    else:
        out = sys.argv[2]
        p = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', '24', out],
                             stdin=subprocess.PIPE)
        import multiprocessing as mp
        with mp.get_context('fork').Pool(int(os.environ.get('NW', 3))) as pool:
            for img in pool.imap(job, range(N0, N1), chunksize=2): p.stdin.write(img.tobytes())
        p.stdin.close(); p.wait(); print('done', out, N1 - N0)
