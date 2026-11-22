"""Justin Levine (Shepherd) trailer: storyboard stills, 16:9, Jennifer look + Twiml/Dime motion language.
  python jl_stills.py            -> every scene
  python jl_stills.py s01 s05    -> only those scenes
Sources: ep/spk/<who>_<episode sec>.jpg (Riverside tracks), broll/frames/jl_*.jpg (YouTube / Shepherd video grabs),
assets/logos/*_dk.png, assets/tv/kv20_cut_clean.png, ep/matte/*_a.png (rembg person mattes for text-behind shots).
"""
import sys, os, json
import numpy as np, cv2
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jl_look as L
from jl_look import W, H, CX, CY, J, J3

FACES = json.load(open(L.ROOT + '/ep/faces.json'))
SPK = L.ROOT + '/ep/spk/'
BR = L.ROOT + '/broll/frames/'
LG = L.ROOT + '/assets/logos/'


def spk(name):
    return L.grade(L.load(SPK + name + '.jpg'))


def face(name):
    x, y, w, h = FACES[name + '.jpg'][:4]
    return x + w / 2, y + h / 2, w, h


def push(img, name, z):
    """camera push of z anchored on the speaker's face (talking heads only ever zoom in, face-anchored)"""
    fx, fy, _, _ = face(name)
    return L.zoom_on(img, z, fx, fy)


# ================================================================ S01  cold claim, Justin tight, no B-roll
def s01():
    # 01a: first frame. Hook on screen. Tight on Justin (face-anchored 1.32 push), left side shade for the hook.
    n = 'j_259.4'; d = push(spk(n), n, 1.32)
    L.side_shade(d, 'left', 0.36, 0.30)
    L.t1_lines(d, ['UNDERWRITERS', 'ARE NEXT'], 120, 470, px=104, key=('NEXT',))
    L.save(d, '01a_hook')
    # 01b: "Our engineering team spends zero time writing code" -- caption beside the head (Twiml TH stack, Jennifer type)
    n = 'j_261.6'; d = push(spk(n), n, 1.32)
    L.side_shade(d, 'left', 0.36, 0.30)
    L.put_text(d, 'Our engineering team spends', 50, 120, 440)
    L.grad_text(d, 'zero time', 150, 112, 580)
    L.put_text(d, 'writing code', 58, 120, 668)
    L.save(d, '01b_zero_time')


def s01c():
    # 01c: "and 100% of their time orchestrating how the code is written." -- 100% sits BEHIND Justin (Dime), gradient
    n = 'j_263.0'; plate = push(spk(n), n, 1.32)
    a = L.zoom_on(np.dstack([L.matte(n)] * 3), 1.32, *face(n)[:2])[..., 0]
    d = plate.copy()
    def draw(o):
        L.grad_text(o, '100%', 330, 800, 860, align='right', glow=0.35)
    L.text_behind(d, plate, a, draw)
    L.side_shade(d, 'right', 0.30, 0.42)
    L.put_text(d, 'of their time', 52, 1800, 820, align='right', face='it')
    L.t1_lines(d, ['orchestrating'], 1800, 935, px=96, align='right', key=('orchestrating',))
    L.save(d, '01c_100_orchestrating')


# ================================================================ S02  who he is (authority stack)
def logo(name):
    return L.load_rgba(LG + name)


def cutout(img, alpha, outline=18, col=(214, 236, 250)):
    """Dime roto cut-out with the ice-blue sticker outline: premultiplied RGBA of the person + a soft outline ring"""
    a = alpha.astype(np.float32)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * outline + 1, 2 * outline + 1))
    ring = cv2.GaussianBlur(cv2.dilate((a > 0.5).astype(np.float32), k), (0, 0), 2.0)
    lay = np.zeros(img.shape[:2] + (4,), np.float32)
    lay[..., :3] = np.array(col, np.float32) / 255 * ring[..., None]
    lay[..., 3] = ring
    lay[..., :3] = img / 255 * a[..., None] + lay[..., :3] * (1 - a[..., None])
    lay[..., 3] = a + ring * (1 - a)
    return lay


def badge(d, lg, cx, cy, w=430, h=520, r=46, fill=(10, 12, 16), stroke=(236, 240, 244), logo_w=330):
    """Dime logo badge card (rounded portrait card, white stroke) in the Jennifer palette: near-black glass + soft blue glow"""
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    m = np.zeros((h, w), np.uint8)
    cv2.rectangle(m, (r, 0), (w - r, h), 255, -1); cv2.rectangle(m, (0, r), (w, h - r), 255, -1)
    for px_, py_ in ((r, r), (w - r, r), (r, h - r), (w - r, h - r)): cv2.circle(m, (px_, py_), r, 255, -1, cv2.LINE_AA)
    a = m.astype(np.float32) / 255
    inner = cv2.erode(m, np.ones((11, 11), np.uint8), borderType=cv2.BORDER_CONSTANT, borderValue=0).astype(np.float32) / 255
    lay = np.zeros((h, w, 4), np.float32)
    lay[..., :3] = (np.array(fill, np.float32) / 255) * inner[..., None] + (np.array(stroke, np.float32) / 255) * (a - inner)[..., None]
    lay[..., 3] = a
    J3.drop_shadow(d, lay, x0, y0, 1.0, strength=0.6)
    J3.glow_screen(d, np.dstack([a * 20, a * 70, a * 200]), 30, 0.55, x0, y0)
    J3.over(d, lay, x0, y0)
    L.place_rgba(d, lg, cx, cy, w=logo_w, shadow=False)


def s02():
    # 02a: whip to Nic on "Today we're" -- caption left of his head, left side shade
    n = 'n_4.6'; d = push(spk(n), n, 1.08)
    L.side_shade(d, 'left', 0.40, 0.34)
    L.put_text(d, "Today we're super excited", 54, 140, 610)
    L.put_text(d, 'to bring on', 54, 140, 680)
    L.save(d, '02a_nic_today')

    # 02b: NAME CARD on Shepherd's own film of Justin (wide, he sits right of centre). Dime roto sandwich: the name is the one
    # hero element BEHIND him (his arm covers the end of 'Levine'); the title line stays in front, left-aligned
    plate = L.grade(L.load(BR + 'jl_shep_1.jpg'))
    L.side_shade(plate, 'left', 0.46, 0.34)
    a = L.matte('jl_shep_1')
    d = plate.copy()
    def nm(o):
        L.put_text(o, 'Justin', 300, 110, 420, glow=0.22)
        L.grad_text(o, 'Levine', 300, 110, 690, glow=0.30)
    L.text_behind(d, plate, a, nm)
    L.put_text(d, 'COFOUNDER AND CEO, SHEPHERD', 42, 122, 800)
    L.save(d, '02b_name_card')

    # 02c: "...CEO of Shepherd." Shepherd's office sign (their film, 0:22) shrinks from full frame into a card on the
    # tech ground, 3x3 hairline grid off its edges (Twiml S07), the words in the outer cells
    d = L.tech(23)
    x0, y0, cw, ch = 548, 300, 824, 464
    L.hairline_grid(d, x0, y0, x0 + cw, y0 + ch)
    L.card(d, L.load(BR + 'jl_shep_22.3.jpg'), x0, y0, cw, ch, fx=0.40, fy=0.5, zoom=1.05)
    L.put_text(d, 'co-founder', 60, 300, y0 - 14, align='center', face='it')
    L.put_text(d, 'and CEO', 56, 300, y0 + ch - 14, align='center')
    L.put_text(d, 'of', 56, 1650, y0 - 14, align='center', face='it')
    L.grad_text(d, 'Shepherd.', 86, 1650, y0 + ch - 14, align='center')
    L.save(d, '02c_shepherd_card')

    # 02d: "I had founded a construction..." -- Dime S3: Justin as a roto cut-out with the ice-blue sticker outline, rising
    # from below in front of a literal photo card (rebar cage on a live job site, LumiCon film 0:28) on the tech ground
    n = 'j_163.0'
    d = L.tech(36, amount=0.7)
    L.card(d, L.grade(L.load(BR + 'jl_lumi_28.jpg')), 780, 120, 1044, 800, fx=0.30, fy=0.45)
    co = cutout(spk(n), L.matte(n))
    fx, fy = face(n)[:2]
    s = 0.86
    co = cv2.resize(co, (int(W * s), int(H * s)), interpolation=cv2.INTER_AREA)
    ox, oy = 1330 - fx * s, H - co.shape[0] + 10
    J3.drop_shadow(d, co, ox, oy, 1.0, strength=0.6)
    J3.over(d, co, ox, oy)
    L.put_text(d, 'I had founded a', 58, 120, 470)
    L.grad_text(d, 'construction', 120, 112, 610)
    L.save(d, '02d_founded')

    # 02e: "construction software business." -- TradeTapp's real product (BuildingConnected film, 0:15) in a centred
    # card, Twiml layout: text right-aligned to the card's left edge, left-aligned to its right edge
    d = L.tech(24)
    x0, y0, cw, ch = 610, 250, 700, 580
    L.hairline_grid(d, x0, y0, x0 + cw, y0 + ch)
    L.card(d, L.load(BR + 'jl_bctt_15.jpg'), x0, y0, cw, ch, fx=0.62, fy=0.45, zoom=1.0)
    L.put_text(d, 'software', 70, x0 - 48, 560, align='right', face='it')
    L.grad_text(d, 'business.', 90, x0 + cw + 48, 560)
    L.save(d, '02e_tradetapp')

    # 02f: "We sold our business to Building Connected" -- hard cut INSIDE the same card to BuildingConnected's own film
    d = L.tech(24)
    L.hairline_grid(d, x0, y0, x0 + cw, y0 + ch)
    lg = L.load(BR + 'jl_bctt_1p5.jpg')
    d[y0:y0 + ch, x0:x0 + cw] = lg[8:40, 8:40].reshape(-1, 3).mean(0)          # the film's own blue fills the card
    lh = int(cw * lg.shape[0] / lg.shape[1]); ly = y0 + (ch - lh) // 2
    d[ly:ly + lh, x0:x0 + cw] = cv2.resize(lg, (cw, lh), interpolation=cv2.INTER_AREA)
    L.put_text(d, 'We sold', 64, x0 - 48, 520, align='right')
    L.put_text(d, 'our business', 64, x0 - 48, 595, align='right', face='it')
    L.grad_text(d, 'to', 96, x0 + cw + 48, 575)
    L.save(d, '02f_buildingconnected')

    # 02g: "and then, together, to Autodesk." -- hit 1/4 is FOOTAGE, not a logo card: Autodesk's own film of the Autodesk
    # Gallery (San Francisco), AUTODESK on the big screen, full frame with a slow push on the screen; lead line on the dark ceiling
    d = L.grade(L.load(BR + 'jl_adsk_2.jpg'))
    d = L.zoom_on(d, 1.06, 975, 560, CX, 590)
    L.put_text(d, 'and then, together, to', 56, CX, 175, align='center', face='it')
    L.save(d, '02g_autodesk')

    # 02h: Nic -- "You guys strike me as top one percent of companies"
    n = 'n_1847.0'; d = push(spk(n), n, 1.08)
    L.side_shade(d, 'left', 0.42, 0.32)
    L.put_text(d, 'You guys strike me as', 54, 150, 560)
    L.t1_lines(d, ['top 1%'], 140, 700, px=150, key=('1%',))
    L.put_text(d, 'of companies', 54, 150, 790)
    L.save(d, '02h_top_one_percent')

    # 02i-k: "Procore and Greenlight Re from the beginning, Intact later on." -- one logo per word (hits 2-4), accelerating cuts
    n = 'n_1858.4'
    plate = push(spk(n), n, 1.04)
    a = L.zoom_on(np.dstack([L.matte(n)] * 3), 1.04, *face(n)[:2])[..., 0]
    for k, nm in enumerate(('02i_procore', '02j_greenlight')):
        d = plate.copy()
        def cards(o):
            badge(o, logo('procore_dk.png'), 420, 470, logo_w=340)
            if k: badge(o, logo('greenlightre_dk.png'), 1500, 470, logo_w=320)
        L.text_behind(d, plate, a, cards)
        if k: L.put_text(d, 'from the beginning', 50, CX, 150, align='center', face='it')
        L.save(d, nm)
    # 02k: "...Intact later on." -- hit 4/4 is FOOTAGE: Intact's own film 'Becoming Intact Insurance' (2:22, f142.3), the Intact letters
    # on their office wall with a rack focus. The film has burned-in subtitles at the bottom, cropped out by a 1.12 push from the top.
    d = L.grade(L.fit(L.load(BR + 'jl_intact_142.jpg'), W, H, 0.5, 0.0, zoom=1.10))
    L.t1_lines(d, ['later on.'], 1000, 160, px=92, align='center', key=('later', 'on.'))
    L.save(d, '02k_intact')


# ================================================================ S03  Nic pushes: job site, sensor on steel, Nic
def s03():
    # 03a: hard cut to a job site (Brickeye/LumiCon film 0:05, aerial)
    d = L.grade(L.load(BR + 'jl_lumi_5.jpg'))
    L.side_shade(d, 'left', 0.42, 0.32)
    L.put_text(d, 'Maybe you put a', 58, 130, 520)
    L.save(d, '03a_jobsite')
    # 03a2: fast sensor montage (Dime S16-23: full-frame cuts every 6-10 f, the caption survives the cuts at the same anchor):
    # the LumiNode sensor and its connector, close (Brickeye 'LumiSense Installation and Connection' 0:46, bug cropped)
    d = L.grade(L.fit(L.load(BR + 'jl_lss_46.jpg'), W, H, 0.42, 0.40, zoom=1.10))
    L.side_shade(d, 'left', 0.42, 0.32)
    L.put_text(d, 'Maybe you put a', 58, 130, 520)
    L.save(d, '03a2_luminode')
    # 03b: a sensor going onto steel formwork (LumiCon 0:14). Hard cut INSIDE the frame: the clip fills the centre cell of a
    # full-frame hairline grid (Twiml S5), the words sit in the flanking cells on the row centre line
    d, (x0, y0, x1, y1) = L.cell_scene(L.grade(L.load(BR + 'jl_lumi_14p5.jpg')), 640, 480, fx=0.62, fy=0.42, zoom=1.15, seed=34)
    L.grad_text(d, 'sensor', 120, x0 - 40, CY + 36, align='right')
    L.put_text(d, 'on site', 70, x1 + 40, CY + 22, face='it')
    L.save(d, '03b_sensor')
    # 03b2 / 03b3: hard cuts INSIDE the same cell (Twiml persistent card), the words hold:
    # a sensor on a column's rebar cage on site (Brickeye 'LumiCon - Mass Concrete…' 0:31, render), then a phone reading the
    # sensor on a live pour (Brickeye 'LumiCon Concrete Sensors' 0:57)
    for nm, f, fx, fy, z in (('03b2_sensor_cage', 'jl_lcm_31p5.jpg', 0.49, 0.40, 1.20), ('03b3_sensor_phone', 'jl_lcs_57p5.jpg', 0.56, 0.45, 1.05)):
        d, (x0, y0, x1, y1) = L.cell_scene(L.grade(L.load(BR + f)), 640, 480, fx=fx, fy=fy, zoom=z, seed=34)
        L.grad_text(d, 'sensor', 120, x0 - 40, CY + 36, align='right')
        L.put_text(d, 'on site', 70, x1 + 40, CY + 22, face='it')
        L.save(d, nm)
    # 03c: back to Nic -- "and we'll give you better rates, right?"
    n = 'n_1116.8'; d = push(spk(n), n, 1.08)
    L.side_shade(d, 'left', 0.42, 0.32)
    L.put_text(d, "and we'll give you", 54, 150, 600)
    L.t1_lines(d, ['better rates,'], 150, 730, px=128, key=('rates,',))
    L.put_text(d, 'right?', 64, 150, 830, face='it')
    L.save(d, '03c_better_rates')


# ================================================================ S04  flash frame into Justin, 15% slams in on the drop
def behind(n, z):
    """face-anchored push of speaker frame n and its person matte"""
    fx, fy = face(n)[:2]
    plate = L.zoom_on(spk(n), z, fx, fy)
    a = L.zoom_on(np.dstack([L.matte(n)] * 3), z, fx, fy)[..., 0]
    return plate, a


def s04():
    n = 'j_1227.0'
    plate, a = behind(n, 1.12)
    f = 255 - plate                                  # Twiml one-frame colour negative of the incoming shot
    L.save(f, '04a_flash_frame', vig=0.0, grain=0)
    d = plate.copy()
    L.text_behind(d, plate, a, lambda o: L.grad_text(o, '15%', 430, 1830, 800, align='right', glow=0.35))
    L.side_shade(d, 'left', 0.34, 0.40)
    L.put_text(d, 'Worth your while is', 54, 130, 470)
    L.put_text(d, 'difference on price.', 54, 1820, 880, align='right')
    L.save(d, '04b_fifteen_percent')


# ================================================================ S05  Progressive, 50 -> THOUSANDS, commercial
def tv(d, screen_img, cx, cy, w):
    """the real Sony Trinitron (Commons) with the archive ad playing in its glass"""
    tvc = L.load_rgba('assets/tv/kv20_cut_clean.png'); sx, sy, sw, sh = np.load(L.ROOT + '/assets/tv/kv20_screen.npy')
    m = np.asarray(Image.open(L.ROOT + '/assets/tv/kv20_screenmask.png')).astype(np.float32) / 255
    th, tw = tvc.shape[:2]
    scr = L.fit(screen_img, sw, sh)
    scr = scr * 0.92 + 8                              # CRT: lifted blacks
    scr[::3] *= 0.86                                  # scanlines
    lay = tvc.copy()
    reg = lay[sy:sy + sh, sx:sx + sw]; mm = m[sy:sy + sh, sx:sx + sw][..., None]
    reg[..., :3] = reg[..., :3] * (1 - mm) + scr / 255 * mm
    s = w / tw
    lay = cv2.resize(lay, (int(tw * s), int(th * s)), interpolation=cv2.INTER_AREA)
    x, y = cx - lay.shape[1] / 2, cy - lay.shape[0] / 2
    J3.drop_shadow(d, lay, x, y, 1.0, strength=0.6)
    J3.over(d, lay, x, y)


def dots(d, x0, y0, cols, rows, pitch, lit, r=4):
    """graph-paper grid of data points (Twiml graph grid, Jennifer colours): `lit` points glow cyan, the rest faint"""
    lay = np.zeros((rows * pitch + 40, cols * pitch + 40, 3), np.float32)
    k = 0
    for j in range(rows):
        for i in range(cols):
            c = (int(20 + i * pitch), int(20 + j * pitch))
            col = (60, 230, 245) if k < lit else (60, 70, 80)
            cv2.circle(lay, c, r, col, -1, cv2.LINE_AA); k += 1
    for i in range(cols + 1): cv2.line(lay, (20 + i * pitch - pitch // 2, 0), (20 + i * pitch - pitch // 2, lay.shape[0]), (40, 46, 54), 1)
    for j in range(rows + 1): cv2.line(lay, (0, 20 + j * pitch - pitch // 2), (lay.shape[1], 20 + j * pitch - pitch // 2), (40, 46, 54), 1)
    J3.glow_screen(d, lay * (lay.max(2, keepdims=True) > 100), 6, 0.9, x0 - 20, y0 - 20)
    J.screen(d, lay, int(x0 - 20), int(y0 - 20))


def s05():
    # 05a: Progressive's archive TV ad (late-1990s spot, YouTube ZymdJ-SAWwQ 0:28) in a real CRT on the tech ground (Dime retro TV)
    # Dime CRT composite (dmB f1126-1171): the TV fills the left of frame and lands on a fast zoom-out; the spot hard-cuts
    # INSIDE the screen (logo card -> the 1999 laptop spot); the caption stacks on the right, right-aligned
    for nm, src_f in (('05a_progressive_tv', 'jl_prog90s_28p5.jpg'), ('05a2_progressive_tv', 'jl_prog99_60.jpg')):
        d = L.tech(27)
        tv(d, L.load(BR + src_f), 700, 545, 1180)
        L.grad_text(d, 'Progressive', 116, 1810, 470, align='right')
        L.put_text(d, 'was the one', 56, 1810, 560, align='right', face='it')
        L.put_text(d, 'that started', 56, 1810, 626, align='right')
        L.save(d, nm)
    # 05b: "...go from 50 data points per underwriting submission" -- counter + 50 lit points on the graph grid
    d = L.tech(28)
    L.grad_text(d, '50', 300, 470, 640, align='center')
    L.put_text(d, 'data points', 56, 470, 730, align='center')
    L.put_text(d, 'per underwriting submission', 40, 470, 790, align='center', face='it')
    dots(d, 900, 230, 22, 14, 40, 50)
    L.save(d, '05b_fifty')
    # 05c: "...to thousands." -- counter has climbed, every point lit, the grid is dense
    d = L.tech(28)
    dots(d, 120, 110, 88, 44, 20, 99999, r=3)
    d[:] = d * 0.55
    L.put_text(d, '50 to', 70, CX, 470, align='center', face='it')
    L.t1_lines(d, ['THOUSANDS'], CX, 640, px=170, align='center', key=('THOUSANDS',))
    L.save(d, '05c_thousands')
    # 05d: "And I just think we can do the same thing in commercial." -- Dime fast B-roll montage (S16-23): five real commercial
    # builds, a hard cut every ~0.4 s, the sentence builds across the cuts and every phrase takes a new anchor; lands on the
    # Oracle aerial with 'commercial.' boxed. Bugs / counters cropped out of every clip.
    def top_shade(d, depth=380, edge=0.45):
        y = np.arange(H, dtype=np.float32); u = np.clip((depth - y) / depth, 0, 1); u = u * u * (3 - 2 * u)
        d *= (1 - (1 - edge) * u)[:, None, None]
    # CyrusOne data hall going up (CyrusOne's own timelapse 0:33) -- lower-left
    d = L.grade(L.fit(L.load(BR + 'jl_cyrus_33.jpg'), W, H, 0.30, 0.62, zoom=1.30))
    L.bottom_shade(d, 420, 0.42)
    L.put_text(d, 'And I just think', 84, 120, 950)
    L.save(d, '05d1_cyrusone')
    # Intel Ohio One fab, red crawler cranes (aerial 1:06) -- upper-left
    d = L.grade(L.fit(L.load(BR + 'jl_intel_66.jpg'), W, H, 0.45, 0.55, zoom=1.06))
    top_shade(d, 480, 0.30)
    L.put_text(d, 'we can do', 108, 120, 220, face='it')
    L.save(d, '05d2_intel')
    # Aligned Data Centers NEO-01, a crane setting modules against the data hall (Aligned's own film 0:31) -- upper-right
    d = L.grade(L.fit(L.load(BR + 'jl_aligned_31.jpg'), W, H, 0.40, 0.60, zoom=1.15))
    top_shade(d, 480, 0.38)
    L.put_text(d, 'the same thing', 108, 1800, 220, align='right')
    L.save(d, '05d3_aligned')
    # Microsoft Fairwater AI datacenter, the steel roof deck from the air (aerial 1:10) -- centre
    d = L.grade(L.load(BR + 'jl_msft_70p5.jpg'))
    L.put_text(d, 'in', 190, 700, 780, align='center', face='it', glow=0.3)
    L.save(d, '05d4_microsoft')
    # Oracle / Stargate, Abilene TX (aerial 0:44) -- the hero word
    d = L.grade(L.load(BR + 'jl_oracle_44.jpg'))
    L.bottom_shade(d, 460, 0.40)
    L.t1_lines(d, ['commercial.'], CX, 960, px=150, align='center', key=('commercial.',))
    L.save(d, '05d_commercial')


# ================================================================ S06  the confession: music stops
def s06():
    # 06a: slow push on Justin (music hard stop). Caption block stays left of the head with a clear margin.
    n = 'j_1619.0'; d = push(spk(n), n, 1.18)
    L.side_shade(d, 'left', 0.38, 0.30)
    L.put_text(d, 'I used to work at', 50, 120, 440)
    L.put_text(d, 'a construction company', 50, 120, 500)
    L.put_text(d, 'as a', 50, 120, 590, face='it')
    L.grad_text(d, 'risk', 120, 120, 710)
    L.grad_text(d, 'manager', 120, 120, 820)
    L.save(d, '06a_risk_manager')
    # 06b: "I knew when the insurance company was coming to inspect the job site" -- the inspector with the clipboard on a
    # spotless site (OSHA's own film 'The OSHA Inspection Process', 3:46). Twiml 'card beside text': card right of centre,
    # 2-line block on the left; nothing sits on the people.
    # More shots from the SAME OSHA film hard-cut inside the same card (Twiml persistent card) while the line builds beside it:
    # the inspector arriving at reception (0:56) -> the clipboard on the spotless site (3:46) -> hands on the inspection
    # checklist (2:46) -> the walk-round (3:50). OSHA bug cropped by the 1.14 push.
    x0, y0, cw, ch = 802, 290, 925, 521
    shots = (('06b1_arrives', 'jl_osha_56p5.jpg', 0.50, 0.40, 3), ('06b_inspector', 'jl_osha_226.jpg', 0.40, 0.40, 4),
             ('06b2_checklist', 'jl_osha_166p5.jpg', 0.42, 0.40, 4), ('06b3_walkround', 'jl_osha_230p5.jpg', 0.42, 0.40, 5))
    for nm, f, fx, fy, nlines in shots:
        d = L.tech(29, amount=0.75)
        L.card(d, L.grade(L.load(BR + f)), x0, y0, cw, ch, fx=fx, fy=fy, zoom=1.14)
        L.put_text(d, 'I knew when the', 46, 760, 420, align='right')
        L.put_text(d, 'insurance company', 46, 760, 476, align='right')
        L.put_text(d, 'was coming to', 46, 760, 532, align='right')
        if nlines >= 4: L.grad_text(d, 'inspect', 124, 760, 660, align='right')
        if nlines >= 5: L.put_text(d, 'the job site', 56, 760, 730, align='right', face='it')
        L.save(d, nm)
    # 06c: "It's somewhat manufactured." -- the 'perfect' inspection as a three-card collage (Twiml S09). The big word is
    # split by a track matte: white over the photo, gradient over the ground. It only crosses the empty-yard card. One low boom.
    d = L.tech(29, amount=0.6)
    cards = [('jl_osha_14.jpg', 430, 190, 500, 300, 0.55, 0.40, 1.18), ('jl_osha_192.jpg', 990, 210, 500, 300, 0.55, 0.40, 1.18),
             ('jl_osha_96.jpg', 700, 560, 520, 310, 0.62, 0.32, 1.40)]
    mask = np.zeros((H, W), np.float32)
    for f, x0, y0, cw, ch, fx, fy, z in cards:
        L.card(d, L.grade(L.load(BR + f)), x0, y0, cw, ch, fx=fx, fy=fy, zoom=z)
        mask[y0:y0 + ch, x0:x0 + cw] = 1
    grd = d.copy(); L.grad_text(grd, 'manufactured.', 176, CX, 800, align='center', face='it')
    wht = d.copy(); L.put_text(wht, 'manufactured.', 176, CX, 800, align='center', face='it')
    m = mask[..., None]; d[:] = wht * m + grd * (1 - m)
    L.put_text(d, "It's somewhat", 54, CX, 130, align='center')
    L.save(d, '06c_manufactured')


# ================================================================ S07  the proof: 11 months
_TEX = {}
def calendar_page(num, w=380, h=440, seed=0):
    """a tear-off calendar page on real paper (Texturelabs Paper 316L): blue binding, 'MONTH' label, big serif numeral"""
    if 'p' not in _TEX: _TEX['p'] = L.load('/Users/gourav/textures/Texturelabs_Paper_316L.jpg')
    p = L.fit(_TEX['p'], w, h, 0.25 + 0.12 * (seed % 5), 0.5)
    p = np.ascontiguousarray(p * 0.20 + 236 * 0.80)
    cv2.rectangle(p, (0, 0), (w - 1, 30), (26, 92, 220), -1)
    for hx in range(40, w - 30, 46): cv2.circle(p, (hx, 15), 6, (12, 14, 18), -1, cv2.LINE_AA)
    lab, _ = J3.text_rgba('MONTH', 30, fill=(90, 96, 108), hs=1.0, track=0.25)
    J3.over(p, lab, (w - lab.shape[1]) / 2, 58)
    rg, asc = J3.text_rgba(str(num), 250, fill=(24, 26, 32), hs=1.0)
    J3.over(p, rg, (w - rg.shape[1]) / 2, 110)
    lay = np.zeros((h, w, 4), np.float32); lay[..., :3] = p / 255; lay[..., 3] = 1
    return lay


def s07():
    # 07a: hard cut back to Justin -- "From inception of the company to our first insurance products being offered in market"
    n = 'j_2395.5'; d = push(spk(n), n, 1.10)
    L.side_shade(d, 'right', 0.38, 0.30)
    L.put_text(d, 'From', 54, 1810, 430, align='right')
    L.grad_text(d, 'inception', 130, 1810, 560, align='right')
    L.put_text(d, 'to our first insurance products', 44, 1810, 636, align='right')
    L.put_text(d, 'being offered in market', 44, 1810, 694, align='right', face='it')
    L.save(d, '07a_inception')
    # 07b: calendar flipping (page-flip ticks under it): month pages tear away 1 -> 11; page 10 mid-flip, 11 underneath
    d = L.tech(30)
    px0, py0 = CX - 165, 330
    for k in range(4):
        pg = calendar_page(11, w=330, h=380, seed=k)
        J3.drop_shadow(d, pg, px0 + (3 - k) * 4, py0 + (3 - k) * 5, 1.0, strength=0.45)
        J3.over(d, pg, px0 + (3 - k) * 4, py0 + (3 - k) * 5)
    flip = calendar_page(10, w=330, h=380, seed=7)
    fw, _ = J3.persp(flip, 0, -62)
    ys, xs = np.where(fw[..., 3] > 0.01); fw = fw[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    J3.drop_shadow(d, fw, CX - fw.shape[1] / 2, py0 - fw.shape[0] + 26, 1.0, strength=0.5)
    J3.over(d, fw, CX - fw.shape[1] / 2, py0 - fw.shape[0] + 26)
    L.put_text(d, 'was about', 48, CX, 790, align='center', face='it')
    L.neon(d, '11 MONTHS', CX, 900, px=84)
    L.save(d, '07b_calendar_11_months')
    # 07c: "which was like record pace."
    n = 'j_2398.3'; d = push(spk(n), n, 1.14)
    L.side_shade(d, 'left', 0.36, 0.30)
    L.put_text(d, 'which was like', 54, 120, 520)
    L.t1_lines(d, ['record pace.'], 120, 660, px=120, key=('pace.',))
    L.save(d, '07c_record_pace')



# ---- 08c photo cloud (Pinterest motion ref): real AI imagery
AI = L.ROOT + '/assets/ai/'
AI_CARDS = [  # (file, focus x, focus y, aspect w/h, zoom)
    (AI + 'huang_0.jpg', 0.45, 0.30, 0.75, 1.0), (AI + 'amodei_1.jpg', 0.48, 0.32, 1.33, 1.0),
    (AI + 'ceo_altman2019.jpg', 0.33, 0.40, 0.75, 1.0), (AI + 'ceo_murati.png', 0.58, 0.42, 1.33, 1.0),
    (AI + 'pichai_4.jpg', 0.74, 0.36, 0.75, 1.0), (AI + 'zuck_1.jpg', 0.60, 0.40, 0.75, 1.0),
    (AI + 'lisasu_ces.png', 0.55, 0.50, 1.33, 1.0), (AI + 'bmwr_15.png', 0.55, 0.45, 1.78, 1.0),
    (AI + 'bmwr_28.png', 0.60, 0.45, 1.33, 1.0), (AI + 'axios_openai_70b.jpg', 0.50, 0.08, 1.33, 1.0),
    (BR + 'jl_msft_70p5.jpg', 0.45, 0.50, 1.78, 1.0), (BR + 'jl_oracle_44.jpg', 0.55, 0.55, 1.33, 1.0),
    (BR + 'jl_aligned_31.jpg', 0.40, 0.60, 1.33, 1.15), (BR + 'jl_cyrus_33.jpg', 0.30, 0.62, 1.78, 1.30),
    (BR + 'jl_intel_66.jpg', 0.45, 0.55, 1.78, 1.06),
]
_AIIMG = {}


def _ai(f):
    if f not in _AIIMG: _AIIMG[f] = L.grade(L.load(f))
    return _AIIMG[f]


def ai_cloud(d, seed, n, sx, sy, smin, smax):
    rng = np.random.default_rng(seed)
    # the stream: tiny thumbnails edge to edge on the centre line (dimmed), cycling through the same real images
    tw, th, gap, x = 40, 30, 9, 30
    k = 0
    while x + tw < W - 30:
        f, fx, fy, asp, z = AI_CARDS[(k * 7 + seed) % len(AI_CARDS)]
        t = L.fit(_ai(f), tw, th, fx, fy, z) * 0.82
        d[CY - th // 2:CY - th // 2 + th, x:x + tw] = t
        x += tw + gap; k += 1
    # the burst: cards in depth, back to front, straight (no tilt), ~1/3 with a white border, soft shadow
    order = rng.permutation(len(AI_CARDS))
    cards = []
    for i in range(n):
        f, fx, fy, asp, z = AI_CARDS[order[i % len(order)]]
        depth = rng.random()
        w = int(smin + (smax - smin) * depth); h = int(w / asp)
        cx = CX + rng.normal(0, sx); cy = CY + rng.normal(0, sy)
        x0 = int(np.clip(cx - w / 2, 110, W - 110 - w)); y0 = int(np.clip(cy - h / 2, 150, 870 - h))
        cards.append((depth, f, fx, fy, z, x0, y0, w, h, rng.random() < 0.35))
    for depth, f, fx, fy, z, x0, y0, w, h, border in sorted(cards):
        L.card(d, _ai(f), x0, y0, w, h, fx=fx, fy=fy, zoom=z, shadow=True, border=6 if border else 0)

# ================================================================ S08  the viewer's own question
def s08():
    # 08a: Luke asks -- centred bottom subtitle (Twiml S15) with the key words in gradient, bottom shade
    n = 'l_3015.9'; d = push(spk(n), n, 1.06)
    bx0, by0, bx1, by1 = 110, 330, 620, 690                              # Jennifer v2: 50 % black caption box beside the head
    d[by0:by1, bx0:bx1] *= 0.5
    L.put_text(d, 'Do you think', 54, 150, 420)
    L.put_text(d, "we're in an", 54, 150, 490, face='it')
    L.grad_text(d, 'AI bubble?', 110, 140, 630)
    L.save(d, '08a_ai_bubble')
    # 08b: hard cut to Justin, "No." plays dry -- one huge word BEHIND him (Dime)
    n = 'j_3019.8'
    plate, a = behind(n, 1.10)
    d = plate.copy()
    L.text_behind(d, plate, a, lambda o: L.put_text(o, 'No.', 460, 1300, 760, align='left', glow=0.25))
    L.save(d, '08b_no')
    # 08c: "I just think that we have consistently underestimated how big AI is." (track B swells on 'underestimated')
    n = 'j_3034.5'; d = push(spk(n), n, 1.10)
    L.side_shade(d, 'left', 0.38, 0.30)
    L.put_text(d, 'I just think that we have', 52, 130, 470)
    L.grad_text(d, 'consistently', 124, 122, 610)
    L.save(d, '08c_underestimated')
    # 08c2 / 08c3: the user's Pinterest ref (pin.it/byqxYwpKP, 'Motion design video'): a thin stream of tiny thumbnails runs
    # across the middle of a black frame and clusters of photo cards burst out of it in depth, reshuffling every ~0.5 s.
    # Built on the Jennifer tech ground with REAL AI imagery only; the cluster grows between the two reshuffles ('how big').
    for nm, seed, ncard, sx, sy, smin, smax, line, key in (
            ('08c2_ai_cloud', 81, 12, 300, 140, 150, 300, 'underestimated', ('underestimated',)),
            ('08c3_ai_cloud_big', 82, 15, 470, 190, 190, 400, 'how big AI is.', ('AI',))):
        d = L.tech(37, amount=0.55)
        ai_cloud(d, seed, ncard, sx, sy, smin, smax)
        L.t1_lines(d, [line], CX, 990, px=100, align='center', key=key)
        L.save(d, nm)


# ================================================================ S09  stakes: underwriters at desks, slow push
def s09():
    # underwriters at their desks (Lloyd's of London underwriting room, PropertyCasualty360 'Inside Lloyd's', 1:37). The clip
    # fills the centre cell of a full-frame hairline grid (Twiml S5) and the whole layer slow-pushes; the words sit in the
    # flanking cells on the row centre line, so nothing is written over the people.
    d, (x0, y0, x1, y1) = L.cell_scene(L.grade(L.load(BR + 'jl_lloydsin_97p5.jpg')), 760, 520, fx=0.40, fy=0.62, zoom=1.25, seed=35)
    L.put_text(d, 'And so I think', 48, CX, y0 - 30, align='center')
    L.grad_text(d, 'underwriting', 104, x0 - 36, CY + 30, align='right')
    L.put_text(d, 'is another', 52, x1 + 36, CY - 10)
    L.put_text(d, 'profession', 52, x1 + 36, CY + 52, face='it')
    L.put_text(d, 'moving in that direction.', 48, CX, y1 + 70, align='center')
    L.save(d, '09_underwriters')


# ================================================================ S10  the biggest payoff, left open
def split3(active=None, bar=150):
    """three-way split of Nic, Justin and Luke (edit map, beat 10): faces centred in 632 px columns on the same eye line,
    hairline dividers; the speaker who talks is lit, the other two drop to 42 %; Twiml final-shot letterbox"""
    d = np.zeros((H, W, 3), np.float32)
    cols = [('n_3069.0', 0, 1.34), ('j_3082.35', 1, 1.05), ('l_3085.0', 2, 1.05)]
    for n, k, z in cols:
        fx, fy, fw, fh = face(n)
        img = L.zoom_on(spk(n), z, fx, fy, CX, 520)
        p = img[:, CX - 316:CX + 316]
        if active is not None and k != active: p = p * 0.42
        d[:, k * 644:k * 644 + 632] = p
    for xx in (638, 1282): d[:, xx - 6:xx + 6] = (10, 11, 13); d[:, xx - 1:xx + 1] = (120, 130, 140)
    if bar: L.letterbox(d, bar)
    return d


def s10():
    d = split3(active=0)
    lw = J3.text_rgba('When do you think we will see the first ', 44, hs=1.0)[0].shape[1]
    kw = J3.text_rgba('fully AI underwritten commercial policy?', 50, hs=1.0)[0].shape[1]
    xs = CX - (lw + kw) / 2
    L.put_text(d, 'When do you think we will see the first', 44, xs, 1000)
    L.grad_text(d, 'fully AI underwritten commercial policy?', 50, xs + lw, 1000, glow=0.2)
    L.save(d, '10a_split_question')
    d = split3(active=1)
    L.t1_lines(d, ['We actually, like, we did this.'], CX, 1004, px=62, align='center', key=('this.',))
    L.save(d, '10b_we_did_this')
    d = split3(active=2)
    L.neon(d, 'BREAKING NEWS', 1604, 984, px=42)
    L.save(d, '10c_breaking_news')
    L.save(np.zeros((H, W, 3), np.float32), '10d_cut_to_black', vig=0, grain=0)
    # title card: the show's own wordmark (keyed from the Verticals cover art) + guest line
    d = L.tech(31, amount=0.7)
    L.place_rgba(d, L.load_rgba(LG + 'verticals_wordmark.png'), CX, 440, w=880, glow=0.2)
    L.neon(d, 'JUSTIN LEVINE, SHEPHERD', CX, 760, px=60)
    L.save(d, '10e_title_card')


SCENES = {'s01': [s01, s01c], 's02': [s02], 's03': [s03], 's04': [s04], 's05': [s05], 's06': [s06],
          's07': [s07], 's08': [s08], 's09': [s09], 's10': [s10]}

if __name__ == '__main__':
    want = sys.argv[1:] or list(SCENES)
    for k in want:
        for fn in SCENES[k]: fn()
