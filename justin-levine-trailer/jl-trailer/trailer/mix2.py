"""Justin Levine (Shepherd) trailer audio, per the script's edit map (v4). Only the SFX in the map.
voice  = the A-roll cut (Verticals_Justin_Levine_Trailer_Cut_v1 mix), high-pass + light denoise, -14 LUFS
track A = arpmedia 'Energetic Energy' (F, 79 bpm): its 4-bar pulse intro looped x3 (bar-exact) so the drop lands on "15%";
          music in on "Today we're", pre-drop mid (-39 LUFS), full after the drop (-35), HARD STOP on "I used to work"
track B = tatamusic 'Energetic Upbeat' (F, 118 bpm, faster + brighter): in on "inception", cuts out after Luke's question,
          swells back on "underestimated", stops dead before "We actually" (-37 LUFS)
-> audio/mix.wav   (python mix.py)"""
import subprocess, json, re, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); A = HERE + '/audio/'
FF = '/Users/gourav/ks-ron-build/reel1/ff'; SR = 48000
T = json.load(open(HERE + '/timeline_new.json'))
import sys; sys.path.insert(0, HERE); from newtime import M
END = T['END']; N = int(round(END * SR))
D, S1, S2, S3 = '/Users/gourav/Downloads/', '/Users/gourav/SFX/SFX/', '/Users/gourav/SFX/Sound Effects/', '/Users/gourav/SFX/DIME motion SFX/'
CW = S3 + 'CINEMA WAVE/REMCOSounds_X_ChristianMuniz_SFXPack_V4 (1)/'


def load(f, ss=0, t=None, mono=False):
    a = [FF, '-v', 'error', '-ss', str(ss)] + (['-t', str(t)] if t else []) + ['-i', f, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(a, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()


def lufs(x):
    p = A + '_m.raw'; open(p, 'wb').write(x.astype(np.float32).tobytes())
    o = subprocess.run([FF, '-hide_banner', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', p, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    os.remove(p); return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', o)[-1])


def fade(x, fi=0.0, fo=0.0):
    x = x.copy()
    if fi > 0: n = min(len(x), int(fi * SR)); x[:n] *= np.linspace(0, 1, n)[:, None]
    if fo > 0: n = min(len(x), int(fo * SR)); x[-n:] *= np.linspace(1, 0, n)[:, None]
    return x


def place(buf, x, t):
    i = int(round(t * SR)); j = max(0, -i); i = max(0, i); n = min(len(x) - j, N - i)
    if n > 0: buf[i:i + n] += x[j:j + n]


W = {w[2]: w for w in []}
words = json.load(open(HERE + '/words_new.json'))
def wt(txt, after=0.0):
    return next(w for w in words if w[2] == txt and w[0] >= after - 1e-6)

# ---------------------------------------------------------------- voice
voice = load(A + 'adobe/JL_trailer_v2_voice-esv2-speech-50p.wav')   # Adobe Podcast Enhance Speech v2 (same timing)
voice = np.pad(voice, ((0, max(0, N - len(voice))), (0, 0)))[:N]
vend = T['VOICE_END']                                     # last word fully finished, then fade out before the black
e0 = int(vend * SR); e1 = int((vend + 0.12) * SR); voice[e0:e1] *= np.linspace(1, 0, e1 - e0)[:, None]; voice[e1:] = 0
voice *= 10 ** ((-14 - lufs(voice)) / 20)

# ---------------------------------------------------------------- music
mus = np.zeros((N, 2), np.float32)
t_today, t_15, t_used = wt("Today,")[0], wt('15', M(40))[0], wt('I', M(55))[0]
arp = load(D + 'arpmedia-energetic-energy-569427.mp3')
BEAT_A = 0.7596; L = 16 * BEAT_A                          # 4 bars
# refine the drop onset near 12.14 s on the onset envelope
mono = arp.mean(1); hop = 256
fl = np.array([np.abs(mono[i:i + 1024]).mean() for i in range(int(11.6 * SR), int(12.6 * SR), hop)])
TD = 11.6 + (np.argmax(np.diff(fl)) + 1) * hop / SR
intro = arp[int((TD - L) * SR):int(TD * SR)] if TD - L >= 0 else np.pad(arp[:int(TD * SR)], ((int((L - TD) * SR), 0), (0, 0)))
xf = int(0.025 * SR)
pre = intro.copy()
for _ in range(2):                                        # bar-exact loop with 25 ms crossfades at the seams
    a, b = pre[-xf:], intro[:xf]; r = np.linspace(0, 1, xf)[:, None]
    pre = np.concatenate([pre[:-xf], a * (1 - r) + b * r, intro[xf:]])
pre = pre[-int(round((t_15 - t_today) * SR)):]                       # v2: tighter cut -> trim the loop from its start, drop stays on '15%'
full = arp[int(TD * SR):int((TD + (t_used - 0.06 - t_15) + 1) * SR)]
tA0 = t_15 - len(pre) / SR
pre = fade(pre, fi=0.12); pre *= 10 ** ((-39 - lufs(pre)) / 20)
full_n = int((t_used - 0.06 - t_15) * SR); full = full[:full_n]
full *= 10 ** ((-35 - lufs(full)) / 20); full = fade(full, fo=0.03)          # HARD STOP on "I used to work"
place(mus, pre, tA0); place(mus, full, t_15)
print(f'track A: in {tA0:.3f} (Today {t_today:.2f}), drop {t_15:.3f} (TD {TD:.3f} in the track), stop {t_used - 0.06:.2f}')

tata = load(D + 'tatamusic-energetic-upbeat-background-music-377668.mp3')
t_inc = wt('inception')[0]; t_bub_end = wt('bubble?')[1]; t_under = wt('underestimated')[0]; t_we = wt('we', M(93.5))[0]
B0 = 0.49                                                 # first downbeat in the track
def b_at(t0, t1):
    return tata[int((B0 + t0 - t_inc) * SR):int((B0 + t1 - t_inc) * SR)]
gB = None
seg1 = b_at(t_inc, t_bub_end + 0.12); seg2 = b_at(t_under - 0.30, t_we - 0.12)
gB = 10 ** ((-37 - lufs(np.concatenate([seg1, seg2]))) / 20)
place(mus, fade(seg1 * gB, fi=0.02, fo=0.04), t_inc)                       # cuts out after Luke's question
place(mus, fade(seg2 * gB, fi=0.65, fo=0.012), t_under - 0.30)            # swells back, stops dead before "We actually"
print(f'track B: in {t_inc:.2f}, out {t_bub_end + 0.12:.2f}, swell {t_under - 0.30:.2f}, dead stop {t_we - 0.12:.2f}')

# ---------------------------------------------------------------- SFX (only the ones in the edit map)
sfx = np.zeros((N, 2), np.float32)
_C = {}
def sx(f, t, db, ss=0, dur=None, peak_at=False, fi=0.0, fo=0.03):
    k = (f, ss, dur)
    if k not in _C:
        x = load(f, ss, dur); x = x / max(1e-6, np.abs(x).max()); _C[k] = fade(x, fi, fo)
    x = _C[k] * 10 ** (db / 20)
    if peak_at:
        env = np.convolve(np.abs(x).mean(1), np.ones(480) / 480, 'same'); t -= np.argmax(env) / SR
    place(sfx, x, t)
t_writing, t_orch = wt('writing')[0], wt('orchestrating,')[0]
# 1: soft keyboard clicks under "writing code", gone by "orchestrating"
kb = load(S1 + 'KEYBOARD TYPING-20250523T150224Z-1-001/KEYBOARD TYPING/TYPING 1.wav', 2.0, t_orch - 0.35 - (t_writing - 0.15))
kb = fade(kb / max(1e-6, np.abs(kb).max()), 0.15, 0.6) * 10 ** (-30 / 20); place(sfx, kb, t_writing - 0.15)
# a low sub drone fades in under "orchestrating" and hands over to track A
dr = load(CW + 'Deep/Deep_Drone 2.wav'); dr = dr / np.abs(dr).max()
dn = int((tA0 + 1.8 - (t_orch - 0.2)) * SR); dr = dr[:dn]
env = np.clip(np.linspace(0, (dn / SR) / 1.6, dn), 0, 1) * np.clip(np.linspace((dn / SR) / 1.6, 0, dn), 0, 1)
# v3 (Krish): removed -- its pulses read as a hit at ~6 s
# place(sfx, dr * env[:, None] * 10 ** (-24 / 20), t_orch - 0.2)
# 2: a soft impact on each logo (4 hits): Autodesk, Procore, Greenlight Re, Intact
# [v4 Krish: no hits/risers] for w, a in (('Autodesk.', 0), ('Procore', 0), ('Greenlight', 0), ('intact', 0)):
# [v4 Krish: no hits/risers]     sx(S1 + 'Cinematic Boom Soft.wav', wt(w)[0] - 0.02, -21, peak_at=True)
# riser in the last 2 s of scene 2, keeps climbing through scene 3, peaks on "right?"
t_right = wt('right?')[0]
# [v4 Krish: no hits/risers] sx(CW + 'Risers/Riser 10.wav', t_right + 0.15, -22, peak_at=True, fi=0.8, fo=0.25)
# 4: big hit on "15%" (the beat drop)
# [v4 Krish: no hits/risers] sx(S1 + 'cinematic-impact-hit-352702.mp3', t_15, -11, peak_at=True)
# [v4 Krish: no hits/risers] sx(S2 + 'Bass Drop, Deep Sub, 55Hz.mp3', t_15, -16, peak_at=True)
# 5: counter ticks as "50" climbs to "THOUSANDS"
t50, tth = wt('50')[0], wt('thousands.')[0]
sx(S2 + 'Game Counter or Digital Data Readout Sound Pack 1.mp3', t50 - 0.02, -27, ss=0.0, dur=tth - t50 + 0.25, fo=0.15)
# 6: one low boom on "manufactured"
# [v4 Krish: no hits/risers] sx(S1 + 'deep-cinematic-boom-404695.mp3', wt('manufactured')[0], -12, peak_at=True)
# 7: page-flip ticks under the calendar (one per page, accelerating)
for tf in T['CAL_FLIPS']:
    sx(S2 + 'PaperTurn_AP1.1264 (SFX).mp3', tf, -22, peak_at=True)
# 9: long riser from beat 9, builds, peaks on Nic's question and STOPS DEAD before "We actually"
t_r0 = wt('And', M(83))[0] - 0.1; t_stop = t_we - 0.12
rz = load(S3 + 'Dystopia SFX/Dystopia SFX/Assets/Riser/DarkCinematicRiser1.wav'); rz = rz / np.abs(rz).max()
need = int((t_stop - t_r0) * SR); env = np.convolve(np.abs(rz).mean(1), np.ones(4800) / 4800, 'same'); pk = int(np.argmax(env))
rz = rz[max(0, pk - need):pk]; rz = fade(rz, fi=1.5, fo=0.012) * 10 ** (-21 / 20)
# [v4 Krish: no hits/risers] place(sfx, rz, t_stop - len(rz) / SR)
# 10: news sting on "Breaking news"; final impact on the cut to black
# [v4 Krish: no hits/risers] sx(S3 + 'OCULAR SFX/CLIMAX/Stingers/DSGNStngr_STINGER-Station B_Ocular_Climax Vol 1.wav', wt('Breaking')[0] - 0.05, -17, fo=0.4)
# [v4 Krish: no hits/risers] sx(CW + 'Impact/Impact 1.wav', T['BLACK'], -9, peak_at=True, fo=1.2)

mix = voice + mus + sfx
fin = np.linspace(1, 0, int(1.0 * SR)) ** 2; mix[-len(fin):] *= fin[:, None]
p = A + '_mix.f32'; open(p, 'wb').write(mix.astype(np.float32).tobytes())
pre_ = [FF, '-hide_banner', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', p]
o = subprocess.run(pre_ + ['-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
m = json.loads(o[o.rindex('{'):o.rindex('}') + 1])
af = ('loudnorm=I=-14:TP=-1.5:LRA=11:linear=true:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s'
      % (m['input_i'], m['input_tp'], m['input_lra'], m['input_thresh'], m['target_offset']))
subprocess.run(pre_ + ['-af', af + ',alimiter=limit=0.84:level=false', '-ar', str(SR), '-c:a', 'pcm_s16le', '-y', A + 'mix2.wav'], capture_output=True)
os.remove(p)
out = load(A + 'mix2.wav')
print('voice', round(lufs(voice), 1), 'music', round(lufs(mus), 1), 'final', round(lufs(out), 1), f'len {len(out) / SR:.3f}s (END {END})')
