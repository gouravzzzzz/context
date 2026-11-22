"""SFX pass for the AE project (Krish/Gourav 2026-11-22): pick clicks / taps / whooshes / risers / hits from ~/SFX for every
visual event of Verticals_Justin_Levine_Trailer_v7, measure each file (onset, peak, loudness) and place it so that
  whoosh  -> its loudest point sits ON the cut / motion peak
  hit/tap -> its attack sits on the frame the thing appears
  riser   -> its peak lands on the cut it builds into
Levels: target short-term level per kind, under the -14 LUFS voice. Writes cues.json (read by add_sfx.jsx) and a
preview mix (preview_mix.wav = mix5 + all SFX) for a level / clipping check.
  python sfx_ae/build_cues.py"""
import json, os, subprocess, numpy as np
FF = '/Users/gourav/ks-ron-build/reel1/ff'
R = '/Users/gourav/SFX/'
OC = R + 'DIME motion SFX/OCULAR SFX/'
WS, WM, IM, SW = OC + 'MOMENTUM/Whooshes - Short/', OC + 'MOMENTUM/Whooshes - Medium/', OC + 'MOMENTUM/Impact/', OC + 'MOMENTUM/Sweeteners/'
QH, QI, QW, QG = OC + 'QUANTUM/Hits/', OC + 'QUANTUM/Impacts/', OC + 'QUANTUM/Simple Whoosh/', OC + 'QUANTUM/Gestures/'
UI = R + 'Ui SFX - DragerStudio/ui sfx(Copy)/'
CAM = R + 'DIME motion SFX/CAMERA/'
MP = R + 'DIME motion SFX/MotionPulse_BlackBox_24-Bit_Wav/'
AR = R + 'DIME motion SFX/ARCHETYPE SFX/Archetype SFX - MP3/'
BR = OC + 'CLIMAX/Braams/'
OUT = '/Users/gourav/jl-trailer/trailer/sfx_ae/'
SR = 48000

def whsh(n): return WS + f'DSGNWhsh_WHOOSH SHORT-{n}_Ocular_Momentum.wav'
def whm(n): return WM + f'DSGNWhsh_WHOOSH MEDIUM-{n}_Ocular_Momentum.wav'
def tw(i): return QW + f'DSGNWhsh_SIMPLE WHOOSH-Transition Whoosh {i:02d}_Ocular_Quantum.wav'
def qh(n): return QH + f'SCIImpt_HITS-{n}_Ocular_Quantum.wav'

# kind -> (label colour index in AE, target short-term dBFS of the loudest 300 ms)
KIND = {'whoosh': (8, -25.0), 'hit': (1, -22.0), 'tap': (11, -29.0), 'riser': (14, -26.0), 'braam': (1, -19.0),
        'glitch': (13, -28.0), 'shutter': (3, -26.0), 'shine': (2, -30.0), 'type': (6, -32.0), 'digital': (13, -30.0)}
# (time on the trailer, kind, file, align, what it is, extra dB)
C = [
    (0.000, 'hit', IM + 'DSGNWhsh_IMPACT-The Horizon_Ocular_Momentum.wav', 'onset', 'Opening low hit', -4),
    (1.760, 'tap', UI + 'ui-click-menu-modern-interface-select-small-01-230473.mp3', 'onset', '"zero" box', 0),
    (3.465, 'tap', UI + 'soft-subtle-ui-pop-sfx-348820 (1).mp3', 'onset', '"100%" gradient word', 0),
    (4.745, 'shine', UI + 'shine-3-268903.mp3', 'onset', '"orchestrating" gradient word', 0),
    (6.458, 'whoosh', tw(5), 'peak', 'Cut Justin -> Nic', 0),
    (7.796, 'tap', UI + 'ui-click-menu-modern-interface-select-small-01-230473 (2).mp3', 'onset', '"excited" box', 0),
    (8.958, 'whoosh', whsh('Swing'), 'peak', 'Nic whips out left', 2),
    (9.070, 'hit', IM + 'DSGNWhsh_IMPACT-Micro Meteor_Ocular_Momentum.wav', 'onset', 'Justin rises in', -2),
    (9.158, 'tap', UI + 'ui-pop-sound-316482.mp3', 'onset', '"Justin"', 0),
    (9.860, 'tap', UI + 'ui-pop-up-2-197887.mp3', 'onset', '"Levine"', 0),
    (11.417, 'whoosh', whm('Subtle Sweep'), 'peak', '3D truck past Justin', -2),
    (10.720, 'type', UI + 'interface-digital-de-texto-text-digital-interface-218128.mp3', 'onset', '"co-founder and CEO of" types on', 0),
    (12.600, 'type', UI + 'ui-tuping-391160.mp3', 'onset', '"Shepherd." types on', 0),
    (13.200, 'whoosh', whsh('The Reverse'), 'peak', 'Headline flies UP into the cut (graph 2)', 0),
    (13.208, 'whoosh', whsh('High Pass'), 'onset', 'Cut-out comes up from the bottom (graph 1)', 0),
    (13.620, 'hit', SW + 'DSGNWhsh_SWEETENERS-Set_Ocular_Momentum.wav', 'onset', 'Cut-out settles', -3),
    (14.125, 'tap', UI + 'soft-subtle-ui-pop-sfx-348820 (1).mp3', 'onset', '"construction" gradient word', 0),
    (14.700, 'whoosh', whm('Air Spirit'), 'onset', 'Showcase: camera pulls out', 0),
    (16.200, 'shine', UI + 'magical-whoosh-148459.mp3', 'onset', 'Purple line draws TradeTapp -> BuildingConnected', 0),
    (18.120, 'tap', UI + 'ui-interface-sound-10-299032.mp3', 'onset', 'Card closes to centre', 0),
    (18.450, 'shine', UI + 'short-punchy-sine-wave-ding-4-d-211755.mp3', 'onset', '"to" becomes the star', -2),
    (19.243, 'hit', qh('Blink'), 'onset', '"Autodesk." + photo reveal', 0),
    (19.250, 'whoosh', whm('Fly By'), 'onset', 'Autodesk photo slides in', -3),
    (20.150, 'digital', UI + 'digital_data_up_down_17.wav', 'onset', 'Grid uncovers into Nic', 0),
    (22.185, 'tap', UI + 'ui-click-menu-modern-interface-select-small-01-230473 (3).mp3', 'onset', '"top 1%" box', 0),
    (24.749, 'shine', UI + 'shine-12-268905.mp3', 'onset', '"intelligently" gradient word', -1),
    (28.062, 'tap', UI + 'soft-subtle-ui-pop-sfx-348820 (1).mp3', 'onset', '"partnerships" gradient word', 0),
    (28.830, 'whoosh', tw(8), 'peak', 'Cut to Procore', 0),
    (29.167, 'shutter', CAM + 'photo camera shutter 2.wav', 'onset', 'Procore photo', 0),
    (30.349, 'whoosh', whsh('Arrow Release'), 'peak', 'Greenlight photo slides in', -2),
    (31.083, 'shutter', CAM + 'Vintage Film Camera Shutter v1.wav', 'onset', 'Montage: Greenlight speaker', 0),
    (31.458, 'shutter', CAM + 'Vintage Film Camera Shutter v2.wav', 'onset', 'Montage: Greenlight logo', 0),
    (31.750, 'shutter', CAM + 'Vintage Film Camera Shutter v3.wav', 'onset', 'Montage: cut', 0),
    (32.042, 'shutter', CAM + 'antique camera shutter 2.wav', 'onset', 'Montage: "A different kind of reinsurer"', 0),
    (32.292, 'shutter', CAM + 'filmmaking-props---camera-shutter by ni-sound Artlist.wav', 'onset', 'Montage: intact logo', 0),
    (32.750, 'whoosh', whsh('Slicer'), 'peak', 'Intact card slides in', -2),
    (33.540, 'whoosh', tw(12), 'peak', 'Cut to job-site footage', -2),
    (33.650, 'digital', MP + 'SIGNAL/Beeps/Beep_Future_Computing_01.wav', 'onset', 'Sensor rings appear', 0),
    (34.377, 'tap', UI + 'click_digital_1.wav', 'onset', '"sensor"', 0),
    (35.420, 'whoosh', tw(3), 'peak', 'Cut to Nic', -3),
    (36.424, 'hit', qh('Relay'), 'onset', '"$$$" + "better rates"', -2),
    (37.417, 'shutter', CAM + 'cinematic-elements---hollywood-flash-impact- by tomas-herudek Artlist.wav', 'onset', 'Flash cut to Justin', 2),
    (37.600, 'digital', UI + 'digital_data_up_down_17.wav', 'onset', '4% -> 15% counts up', -2),
    (38.791, 'tap', UI + 'ui-pop-up-4-197890.mp3', 'onset', '"15%" lands', 0),
    (40.458, 'digital', QG + 'SCIMisc_GESTURES-Main Screen_Ocular_Quantum.wav', 'onset', 'TV switches on (Progressive)', 0),
    (42.292, 'glitch', R + 'Glitch, Flicker, Text  (1).wav', 'onset', 'TV picture changes', 0),
    (43.333, 'whoosh', tw(15), 'peak', 'Cut to data counter', -4),
    (46.708, 'whoosh', tw(18), 'peak', 'Cut to aerial job site', 0),
    (47.792, 'whoosh', whsh('Wing Friction'), 'peak', 'Aerial cut', -4),
    (48.526, 'hit', qh('Single Shot'), 'onset', '"commercial." box', 0),
    (49.540, 'whoosh', tw(20), 'peak', 'Cut to Justin', -3),
    (51.715, 'tap', UI + 'ui-click-menu-modern-interface-select-small-01-230473 (4).mp3', 'onset', '"risk manager"', 0),
    (52.292, 'whoosh', tw(22), 'peak', 'Inspection footage card', -2),
    (54.861, 'tap', UI + 'soft-subtle-ui-pop-sfx-348820 (1).mp3', 'onset', '"inspect"', 0),
    (55.960, 'glitch', AR + '04 - Glitches/Glitches - Silk/' , 'onset', 'Card wall bursts (pixel overlay)', 0),
    (56.000, 'whoosh', whsh('Blast'), 'peak', 'Card wall bursts', -2),
    (57.120, 'hit', IM + 'DSGNWhsh_IMPACT-Event_Ocular_Momentum.wav', 'onset', '"manufactured."', -1),
    (57.792, 'whoosh', tw(10), 'peak', 'Cut to Justin', -4),
    (58.398, 'shine', UI + 'shine-3-268903.mp3', 'onset', '"inception" gradient word', -1),
    (60.625, 'whoosh', tw(14), 'peak', 'Cut to calendar', -2),
    (63.121, 'hit', qh('Fuse'), 'onset', '"11 MONTHS" box', -1),
    (64.000, 'whoosh', tw(7), 'peak', 'Cut to Justin', -4),
    (64.988, 'tap', UI + 'ui-pop-up-2-197887.mp3', 'onset', '"record pace." box', 0),
    (65.875, 'whoosh', tw(16), 'peak', 'Cut to Luke', -2),
    (67.044, 'tap', UI + 'pop-up-351983.mp3', 'onset', '"AI bubble?"', 0),
    (67.888, 'hit', QI + 'DSGNDist_IMPACT-Clean_Ocular_Quantum.wav', 'onset', '"No."', 2),
    (69.786, 'shine', UI + 'shine-12-268905.mp3', 'onset', '"consistently" gradient word', -1),
    (70.358, 'whoosh', whm('Spirit Passby'), 'onset', 'Photo cloud: wave 1', -2),
    (70.428, 'hit', qh('Lock And Load'), 'onset', '"underestimated" box', -2),
    (71.458, 'whoosh', whsh('Surfer'), 'peak', 'Photo cloud: wave 2', -3),
    (71.975, 'whoosh', whsh('Bullet By'), 'peak', 'Photo cloud: wave 3', -3),
    (72.491, 'tap', UI + 'ui-click-menu-modern-interface-select-small-01-230473 (1).mp3', 'onset', '"AI" box', 0),
    (73.250, 'whoosh', tw(24), 'peak', 'Carousel starts', -2),
    (74.583, 'whoosh', WS + 'DSGNWhsh_WHOOSH SHORT-In Out_Ocular_Momentum_01.wav', 'peak', 'Carousel spins', -3),
    (75.667, 'whoosh', tw(26), 'peak', 'Collage -> Lloyd\'s', -2),
    (74.491, 'shine', UI + 'shine-3-268903.mp3', 'onset', '"underwriting" gradient word', -2),
    (76.923, 'hit', IM + 'DSGNWhsh_IMPACT-Transitor_Ocular_Momentum.wav', 'onset', 'Cut to 3-way split', -1),
    (84.249, 'tap', UI + 'ui-click-menu-modern-interface-select-small-01-230473 (2).mp3', 'onset', '"this." box', 0),
    (84.875, 'hit', MP + 'IMPACT/Trailer_Hits/', 'onset', 'BREAKING NEWS zoom cut 1', 0),
    (84.900, 'type', UI + 'ui-tuping-391160.mp3', 'onset', 'BREAKING NEWS box types on', 0),
    (85.833, 'hit', MP + 'IMPACT/Trailer_Hits/', 'onset', 'BREAKING NEWS zoom cut 2 (tighter)', 2),
    (87.292, 'riser', AR + '01 - Risers/Risers - Silk/', 'peak', 'Riser into the title', 0),
    (87.292, 'braam', BR + 'Arrival/DSGNBram_BRAAM AGGRESSIVE-Arrival A_Ocular_Climax Vol 1.wav', 'onset', 'VERTICALS title lands', 0),
    (87.792, 'type', UI + 'interface-digital-de-texto-text-digital-interface-218128.mp3', 'onset', '"JUSTIN LEVINE, SHEPHERD" types on', 0),
]


def load(f):
    raw = subprocess.run([FF, '-v', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def env_db(x, w=480):
    n = len(x) // w; e = np.sqrt(np.mean(x[:n * w].reshape(n, w) ** 2, 1)) + 1e-9
    return 20 * np.log10(e)


def measure(f):
    x = load(f); e = env_db(x)                    # 10 ms blocks
    pk = int(np.argmax(e)); on = int(np.argmax(e > e[pk] - 30))
    k = 30; loud = max(10 * np.log10(np.mean(10 ** (e[i:i + k] / 10))) for i in range(0, max(1, len(e) - k + 1)))
    return dict(dur=len(x) / SR, onset=on * 0.01, peak=pk * 0.01, loud=float(loud), x=x)


def pick_folder(d, want, used):
    """a folder given -> the file whose shape suits the cue (riser: long build with a late peak; hit: fast attack)"""
    fs = sorted(f for f in os.listdir(d) if f.lower().endswith(('.wav', '.mp3', '.m4a', '.aif', '.aiff')))
    best, bs = None, -1e9
    for f in fs:
        if d + f in used: continue
        m = measure(d + f)
        if want == 'riser': s = -abs(m['peak'] - 2.6) - (2 if m['peak'] > m['dur'] - 0.05 else 0)
        elif want == 'hit': s = -m['onset'] * 10 - abs(m['dur'] - 2.5) * 0.3
        else: s = -m['onset'] * 10 - abs(m['dur'] - 0.8)
        if s > bs: best, bs = d + f, s
    return best


PEAK_CAP = {'whoosh': -9, 'hit': -7, 'braam': -6, 'tap': -15, 'shutter': -13, 'shine': -15, 'type': -17, 'digital': -14,
            'glitch': -13, 'riser': -10}          # sample-peak ceiling per kind (dBFS): short hits / shutters are loud for their RMS


def load2(f):
    raw = subprocess.run([FF, '-v', 'error', '-i', f, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


used, cues = set(), []
for t, kind, f, align, what, extra in C:
    if f.endswith('/'): f = pick_folder(f, kind, used)
    used.add(f)
    m = measure(f)
    off = m['peak'] if align == 'peak' else m['onset']
    lbl, target = KIND[kind]
    pk_db = 20 * np.log10(np.abs(load2(f)).max() + 1e-9)
    lvl = float(np.clip(min(target + extra - m['loud'], PEAK_CAP[kind] - pk_db), -30, 12))
    cues.append(dict(t=round(t, 4), kind=kind, file=f, start=round(t - off, 4), align=align, off=round(off, 3), dur=round(m['dur'], 3),
                     level=round(lvl, 1), label=lbl, name=f"{kind.upper():7s} {t:6.2f}s  {what}"))
cues.sort(key=lambda c: c['t'])
for i, c in enumerate(cues): c['name'] = f"SFX {i + 1:02d} | " + c['name']

# headroom: mix5 (stereo) + every SFX layer must stay under -1 dBFS (AE sums layers with no limiter)
raw = subprocess.run([FF, '-v', 'error', '-i', '/Users/gourav/jl-trailer/trailer/audio/mix5.wav', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
mix = np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
X = {c['file']: load2(c['file']) for c in cues}
def render():
    sfx = np.zeros_like(mix)
    for c in cues:
        x = X[c['file']] * 10 ** (c['level'] / 20); i0 = int(round(c['start'] * SR))
        if i0 < 0: x = x[-i0:]; i0 = 0
        n = min(len(x), len(sfx) - i0); sfx[i0:i0 + n] += x[:n]
    return sfx
for it in range(40):
    sfx = render(); out = mix + sfx; pk = np.abs(out).max(1); i = int(np.argmax(pk)); over = 20 * np.log10(pk[i]) + 1.0
    if over <= 0: break
    t = i / SR
    for c in cues:
        if c['start'] <= t < c['start'] + c['dur']: c['level'] = round(float(c['level'] - over - 0.5), 1)
json.dump(cues, open(OUT + 'cues.json', 'w'), indent=1)
open(OUT + '_p.f32', 'wb').write(out.astype(np.float32).tobytes())
subprocess.run([FF, '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', OUT + '_p.f32', '-c:a', 'pcm_s16le', OUT + 'preview_mix.wav'])
os.remove(OUT + '_p.f32')
print(len(cues), 'cues;', len(set(c['file'] for c in cues)), 'files; peak mix+sfx %.2f dBFS (after %d headroom passes); sfx peak %.1f dBFS' %
      (20 * np.log10(np.abs(out).max()), it, 20 * np.log10(np.abs(sfx).max() + 1e-9)))
for c in cues: print(f"{c['name'][:70]:70s} start {c['start']:7.3f} lvl {c['level']:+5.1f}  {os.path.basename(c['file'])[:48]}")
