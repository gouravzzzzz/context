"""Justin Levine (Shepherd) trailer storyboard: shared look helpers.
LOOK = Jennifer style (the KSS trailer engine: jstyle2/jstyle3 via jen_stills_h -> 1920x1080):
  black '01' tech ground, Instrument Serif (white), cyan-blue -> blue gradient key-word boxes / gradient words,
  neon boxes, Trailer-1 big serif speaker captions, shadows + glow on all text, vignette + grain.
MOTION / LAYOUT = mix of the two refs (Twiml AI trailer + Dime 'Sports Bra' trailer), see refs/study_*.md:
  hairline 3x3 grids hung off a centred card, words in the outer cells, card collapse, text behind the speaker (roto),
  retro TV, captions beside the head on the empty side with a side shade.
All text sits inside the 90 % title-safe area (x 96-1824, y 54-1026).
"""
import os, sys
import numpy as np, cv2
from PIL import Image
sys.path.insert(0, '/Users/gourav/ks-kristina-build/storyboard')
import jen_stills_h as SH                      # sets the Jennifer engine to 1920x1080
B, J, J3 = SH.B, SH.J, SH.J3
W, H, CX, CY = 1920, 1080, 960, 540
SAFE = (96, 54, 1824, 1026)
ROOT = '/Users/gourav/jl-trailer'
OUT = ROOT + '/storyboard/stills'
GB0, GB1 = (14, 150, 232), (20, 52, 232)       # key-word box gradient (cyan-blue -> blue), same as the KSS trailer
WHITE = (246, 246, 244)
T = 99.0                                        # stills: every animation finished


def load(p):
    if not p.startswith('/'): p = ROOT + '/' + p
    return np.asarray(Image.open(p).convert('RGB')).astype(np.float32)


def load_rgba(p):
    if not p.startswith('/'): p = ROOT + '/' + p
    a = np.asarray(Image.open(p).convert('RGBA')).astype(np.float32) / 255
    a[..., :3] *= a[..., 3:4]
    return a                                    # premultiplied


def matte(name):
    return np.asarray(Image.open(f'{ROOT}/ep/matte/{name}_a.png').convert('L')).astype(np.float32) / 255


def grade(img):
    return B.grade(img)


def fit(img, w, h, fx=0.5, fy=0.5, zoom=1.0):
    """cover-crop img to w x h around (fx, fy)"""
    ih, iw = img.shape[:2]
    s = max(w / iw, h / ih) * zoom
    cw, ch = w / s, h / s
    x0 = min(max(fx * iw - cw / 2, 0), iw - cw); y0 = min(max(fy * ih - ch / 2, 0), ih - ch)
    M = np.float32([[s, 0, -x0 * s], [0, s, -y0 * s]])
    return cv2.warpAffine(img, M, (int(w), int(h)), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)


def zoom_on(img, z, ax, ay, px=None, py=None):
    """camera: zoom z about source point (ax, ay), placed at screen (px, py) (default: same point)"""
    px = ax if px is None else px; py = ay if py is None else py
    M = np.float32([[z, 0, px - ax * z], [0, z, py - ay * z]])
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)


def tech(seed=21, t=0.0, amount=0.9):
    d = J3.TechBG(seed=seed).render(t, amount=amount)
    J3.number_row(d, t, H - 30, x0=40, x1=W - 40, px=20, seed=seed)
    return d


def side_shade(d, side='left', frac=0.30, edge=0.37):
    """Twiml legibility gradient on the caption side: 1.0 at (1-frac) of the width -> `edge` at the frame edge"""
    x = np.arange(W, dtype=np.float32) / W
    u = np.clip((x - (1 - frac)) / frac, 0, 1) if side == 'right' else np.clip(((frac) - x) / frac, 0, 1)
    u = u * u * (3 - 2 * u)
    d *= (1 - (1 - edge) * u)[None, :, None]


def bottom_shade(d, depth=380, edge=0.45):
    y = np.arange(H, dtype=np.float32)
    u = np.clip((y - (H - depth)) / depth, 0, 1); u = u * u * (3 - 2 * u)
    d *= (1 - (1 - edge) * u)[:, None, None]


def finish(img, vig=0.42, grain=4.0, seed=0):
    img = J.grain(img, grain, seed)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W * 0.60)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
    img = img * (1 - vig * np.clip(r - 0.38, 0, 1) ** 1.3)[..., None]
    return np.clip(img, 0, 255).astype(np.uint8)


def save(img, name, vig=0.42, grain=4.0):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name + '.png')
    Image.fromarray(finish(img, vig, grain)).save(p)
    print('rendered', p, flush=True)
    return p


# ---------------------------------------------------------------- type
def text_rgba(txt, px, face='reg', fill=WHITE, hs=1.0):
    return J3.text_rgba(txt, px, face=face, fill=fill, hs=hs)


def put_text(d, txt, px, x, base_y, align='left', face='reg', fill=WHITE, glow=0.18, hs=1.0, op=1.0):
    """one serif line with the caption shadow + glow, aligned to x by side"""
    rg, asc = text_rgba(txt, px, face, fill, hs)
    x0 = x if align == 'left' else (x - rg.shape[1] if align == 'right' else x - rg.shape[1] / 2)
    J3._put_word(d, rg, asc, x0, base_y, (op, 0, 0, 0), True, glow)
    return x0, x0 + rg.shape[1]


def grad_text(d, txt, px, x, base_y, align='left', c0=(70, 255, 236), c1=(40, 120, 255), face='reg', hs=1.0, glow=0.30):
    """big word filled with the teal -> blue gradient, shadow + soft glow (Jennifer gradient word)"""
    rg, asc = text_rgba(txt, px, face, (255, 255, 255), hs)
    g = J.grad(rg.shape[1], rg.shape[0], c0, c1) / 255
    lay = rg.copy(); lay[..., :3] = g * rg[..., 3:4]
    x0 = x if align == 'left' else (x - rg.shape[1] if align == 'right' else x - rg.shape[1] / 2)
    J3.drop_shadow(d, lay, x0, base_y - asc, 1.0, strength=0.75)
    if glow: J3.glow_screen(d, lay[..., :3] * 255, 18, glow, x0, base_y - asc)
    J3.over(d, lay, x0, base_y - asc)
    return x0, x0 + rg.shape[1], base_y - asc, base_y - asc + rg.shape[0]


_GB = {}
def gbox(w, h):
    if (w, h) not in _GB: _GB[(w, h)] = J.grad(w, h, GB0, GB1)
    return _GB[(w, h)]


def t1_lines(d, lines, x, base_y, px=120, align='left', key=(), leading=0.94):
    """Trailer-1 type (KSS trailer v2+): big natural-width Instrument Serif, tight leading, the key word(s) on a solid
    cyan-blue -> blue gradient box, soft shadows. lines = ['word word', ...]; key = words that get the box"""
    for li, line in enumerate(lines):
        words = line.split(); sp = J3.font(px).getlength(' ') * 0.95
        lay, xx = [], 0.0
        for w in words:
            rg, asc = J3.text_rgba(w, px, hs=1.0); lay.append((w, rg, asc, xx)); xx += rg.shape[1] + sp
        lw = xx - sp; by = base_y + li * px * leading
        x0 = x if align == 'left' else (x - lw if align == 'right' else x - lw / 2)
        run = [e for e in lay if e[0] in key]
        if run:
            bx0 = int(x0 + run[0][3] - px * 0.10); bx1 = int(x0 + run[-1][3] + run[-1][1].shape[1] + px * 0.10)
            by0, by1 = int(by - px * 0.80), int(by + px * 0.24)
            sh = np.zeros((by1 - by0, bx1 - bx0, 4), np.float32); sh[..., 3] = 1
            J3.drop_shadow(d, sh, bx0, by0, 1.0, strength=0.45)
            d[by0:by1, bx0:bx1] = gbox(bx1 - bx0, by1 - by0)
        for w, rg, asc, xx in lay:
            J3._put_word(d, rg, asc, x0 + xx, by, (1.0, 0, 0, 0), True, 0.10)


def neon(d, word, cx, cy, px=84, lead='', lead_px=54, gap=58):
    """straight Jennifer neon box with the key word (fully typed), optional centred lead line above"""
    full, _ = J.text_rgba(word, px)
    SH.put3d(d, SH.neon_layer(word, px), cx, cy, glow=0)
    if lead: put_text(d, lead, lead_px, cx, cy - px * 0.875 - gap, align='center')


def text_behind(d, plate, alpha, draw):
    """Dime technique: type sits BEHIND the speaker. draw(d) paints text onto the plate, then the person (alpha) goes back on top"""
    out = plate.copy(); draw(out)
    a = alpha[..., None]
    d[:] = out * (1 - a) + plate * a


# ---------------------------------------------------------------- cards / grid
def hairline_grid(d, x0, y0, x1, y1, col=(205, 215, 225), op=0.42, th=2):
    """Twiml 3x3 hairline grid hung off the card edges, running to the frame edges (on the Jennifer black ground)"""
    lay = np.zeros((H, W), np.float32)
    for x in (x0, x1): cv2.line(lay, (int(x), 0), (int(x), H - 1), 1.0, th, cv2.LINE_AA)
    for y in (y0, y1): cv2.line(lay, (0, int(y)), (W - 1, int(y)), 1.0, th, cv2.LINE_AA)
    a = lay[..., None] * op
    d[:] = d * (1 - a) + np.array(col, np.float32) * a


def card(d, img, x0, y0, w, h, fx=0.5, fy=0.5, zoom=1.0, shadow=True, border=0):
    c = fit(img, w, h, fx, fy, zoom)
    if shadow:
        sh = np.zeros((h, w, 4), np.float32); sh[..., 3] = 1
        J3.drop_shadow(d, sh, x0, y0, 1.0, strength=0.55)
    if border:
        d[y0 - border:y0 + h + border, x0 - border:x0 + w + border] = (235, 235, 230)
    d[y0:y0 + h, x0:x0 + w] = c
    return c


def place_rgba(d, rgba, cx, cy, h=None, w=None, shadow=True, glow=0.0):
    """premultiplied RGBA scaled to height h (or width w), centred on (cx, cy)"""
    ih, iw = rgba.shape[:2]
    s = (h / ih) if h else (w / iw)
    r = cv2.resize(rgba, (max(1, int(iw * s)), max(1, int(ih * s))), interpolation=cv2.INTER_AREA)
    x, y = cx - r.shape[1] / 2, cy - r.shape[0] / 2
    if shadow: J3.drop_shadow(d, r, x, y, 1.0, strength=0.5)
    if glow: J3.glow_screen(d, r[..., :3] * 255, 22, glow, x, y)
    J3.over(d, r, x, y)
    return x, y, r.shape[1], r.shape[0]


def cell_scene(img, cw=620, ch=520, cy=CY, fx=0.5, fy=0.5, zoom=1.0, seed=33, amount=0.75):
    """Twiml S5: full-frame 3x3 hairline grid on the ground, the footage exactly fills the centre cell.
    Returns (frame, cell box) so words can be set into the flanking cells on the row centre line."""
    d = tech(seed, amount=amount)
    x0, y0 = int(CX - cw / 2), int(cy - ch / 2)
    hairline_grid(d, x0, y0, x0 + cw, y0 + ch)
    card(d, img, x0, y0, cw, ch, fx=fx, fy=fy, zoom=zoom, shadow=False)
    return d, (x0, y0, x0 + cw, y0 + ch)


def letterbox(d, bar=150):
    """Twiml final-shot letterbox (bars slide 0 -> 150 px)"""
    d[:bar] = 0; d[H - bar:] = 0


def invert_block(d, x0, y0, x1, y1):
    """Twiml one-frame colour-negative block"""
    d[y0:y1, x0:x1] = 255 - d[y0:y1, x0:x1]
