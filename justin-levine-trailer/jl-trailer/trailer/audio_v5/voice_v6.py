"""Trailer v6 voice = v5 + (Krish: "abrupt mute between think and we will (1:17) -- no abrupt mutes anywhere"):
  * Nic's source track LOSES 265 ms mid-word (speech -> digital zero -> speech, 3069.93 s): the word fades out into it (35 ms),
    back in (22 ms), and the gap is filled with his room tone -> a natural short pause; lip sync untouched
  * v5's room tone sat ~20 dB under each speaker's real background -> every pause / speaker change dropped to near-silence.
    Now a continuous BED follows each speaker's own background level (10th pct of 10 ms blocks, +-5 s), glides between
    speakers over ~0.3 s, and only fills where the voice is quieter than it (power complement) -> no dead air anywhere
  * a span that is still loud when it hands over to the bed fades out over 50 ms instead of 20 ms
Trailer v5 voice (Krish: "it sounds weird at some places, some words aren't said properly").
Rebuilt from the ORIGINAL per-speaker tracks (no Adobe Enhance), with the SAME timing as the v4 voice, so lip sync is untouched:
  * every A-roll span keeps its exact position (output time -> source time map unchanged)
  * v1 joined spans by fading each one to digital zero (8-20 ms dips) right on the aligner's word boundary -> chopped word
    onsets/ends + a dropout at every mid-sentence cut. Now every joint is moved to the QUIETEST point near it (the span
    audio simply continues in its own source track around the joint) and the two sides are equal-power crossfaded
  * room tone under the added air is crossfaded in/out (no dips), looped with crossfades
  * the v2 tight recut (newtime.json regions, all in quiet runs) is applied with 10 ms crossfades instead of fades to zero
  * light clean-up only: high-pass 75 Hz, very soft 1.6:1 levelling (no denoise / de-ess = no warble); loudness in mix3.py
  -> audio_v5/voice_v5_cut.wav (old cut timeline, 99.46 s) and audio_v5/voice_v5.wav (NEW timeline, = voice_new.wav length)
  python audio_v5/voice_v5.py"""
import json, wave, os, sys, subprocess
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
B = '/Users/gourav/verticals-justin-build/'
HERE = '/Users/gourav/jl-trailer/trailer/'
OUT = HERE + 'audio_v5/'
FF = '/Users/gourav/ks-ron-build/reel1/ff'
SR, FPS = 48000, 24
sys.path.insert(0, B)
import wav as WV

S = json.load(open(B + 'cut/spans.json'))
A = {}
for tr in ('justin', 'nic', 'luke'):
    with wave.open(B + f'work/{tr}48.wav') as w:
        A[tr] = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
HP = butter(2, 80, 'highpass', fs=SR, output='sos')
AH = {tr: sosfilt(HP, x).astype(np.float32) for tr, x in A.items()}      # for the energy search only

# speaker level match (same rule as the A-roll cut: loudest 60 % of 50 ms blocks of the kept words -> -20 dBFS)
gain = {}
for tr in A:
    xs = np.concatenate([A[tr][int(s['onset'] * SR):int(s['offset'] * SR)] for s in S if s['spk'] == tr])
    bl = xs[:len(xs) // 2400 * 2400].reshape(-1, 2400); e = np.sort(np.mean(bl ** 2, 1))[::-1]
    gain[tr] = 10 ** ((-20 - 10 * np.log10(np.mean(e[:int(len(e) * 0.6)]) + 1e-12)) / 20)

# span positions on the old cut timeline: exactly as the A-roll render concatenated them
pos, cur = [], 0
for s in S:
    a_i, e_i = int(s['a'] * SR), int(s['e'] * SR); air = int(s.get('air', 0.0) * SR)
    pos.append(dict(start=cur, a_i=a_i, n=e_i - a_i, air=air)); cur += (e_i - a_i) + air
NTOT = int(round(round(cur / SR * FPS) / FPS * SR))


def src_idx(k, i):  return pos[k]['a_i'] + (i - pos[k]['start'])          # output sample i -> source sample of span k
def rms(tr, j, w=480):
    j = int(j); x = AH[tr][max(0, j - w // 2):j + w // 2]; return float(np.sqrt(np.mean(x * x) + 1e-12))


def best(k_out, k_in, J, lo, hi, lam=0.0025):
    """quietest output sample near J: sum of the outgoing / incoming tracks' 10 ms RMS (gain applied) + distance penalty"""
    cands = range(J + int(lo * SR), J + int(hi * SR) + 1, 48)
    def cost(i):
        c = 0.0
        if k_out is not None: c += rms(S[k_out]['spk'], src_idx(k_out, i)) * gain[S[k_out]['spk']]
        if k_in is not None: c += rms(S[k_in]['spk'], src_idx(k_in, i)) * gain[S[k_in]['spk']]
        return c + lam * abs(i - J) / (0.01 * SR)
    return min(cands, key=cost)


_RT = {}
def roomtone(tr, t, n):
    """n samples of the speaker's room tone. The tracks are noise-GATED (digital zeros between words), so a real 'quiet'
    stretch still carries breath / faint words -> SYNTHETIC room tone instead: noise with the average spectrum and level of the
    speaker's quietest un-gated 10 ms blocks (phase-randomised: stationary, can never sound like a word)."""
    if tr not in _RT:
        x = A[tr]; bl = int(0.01 * SR); nb = len(x) // bl
        be = np.mean(x[:nb * bl].astype(np.float64).reshape(nb, bl) ** 2, 1)
        ok = np.flatnonzero(be > 10 ** (-72 / 10))
        q = ok[np.argsort(be[ok])[:max(50, len(ok) // 50)]]               # quietest 2 % of the un-gated blocks
        L_ = 2048; acc = np.zeros(L_ // 2 + 1); win = np.hanning(L_)
        for b in q[:400]:
            seg = x[b * bl:b * bl + L_]
            if len(seg) == L_: acc += np.abs(np.fft.rfft(seg * win)) ** 2
        lvl = float(np.sqrt(np.median(be[q])))
        rng = np.random.default_rng(7); N_ = 20 * SR
        spec = np.fft.rfft(rng.standard_normal(N_)) * np.interp(np.linspace(0, 1, N_ // 2 + 1), np.linspace(0, 1, L_ // 2 + 1), np.sqrt(acc))
        y = np.fft.irfft(spec, N_).astype(np.float32); y *= lvl / (np.sqrt(np.mean(y * y)) + 1e-12)
        _RT[tr] = y
    y = _RT[tr]; o = int(t * 997) % (len(y) - SR)
    return np.tile(y, n // len(y) + 2)[o:o + n].copy()


def unit_tone(tr, t, n):
    y = roomtone(tr, t, n); return y / (np.sqrt(np.mean(y * y)) + 1e-12)


def local_floor(tr, i, span=5.0):
    """the speaker's real background level around source sample i: 10th percentile of the un-gated 10 ms block RMS"""
    x = A[tr]; a = max(0, int(i) - int(span * SR)); b = min(len(x), int(i) + int(span * SR)); seg = x[a:b]; nb = len(seg) // 480
    be = np.sqrt(np.mean(seg[:nb * 480].astype(np.float64).reshape(nb, 480) ** 2, 1)); be = be[be > 1e-6]
    return float(np.percentile(be, 10))


# ---- v6: source dropouts (digital-zero runs inside used spans) -> fade out / in + local room tone (a natural short pause)
DROPS = []
for s in S:
    tr = s['spk']; x = A[tr]; a_i, e_i = int(s['a'] * SR), int(s['e'] * SR)
    z = (x[a_i:e_i] == 0).astype(np.int8); dz = np.diff(np.r_[0, z, 0])
    for r0, r1 in zip(np.flatnonzero(dz == 1), np.flatnonzero(dz == -1)):
        if r1 - r0 >= int(0.004 * SR): DROPS.append((tr, a_i + int(r0), a_i + int(r1)))
for tr, z0, z1 in DROPS:
    x = A[tr]; nf, ni = int(0.060 * SR), int(0.006 * SR)
    x[z0 - nf:z0] *= np.cos(np.linspace(0, np.pi / 2, nf)).astype(np.float32)
    x[z1:z1 + ni] *= np.sin(np.linspace(0, np.pi / 2, ni)).astype(np.float32)
    n = (z1 + ni) - (z0 - nf); env = np.ones(n, np.float32)
    env[:nf] = np.sin(np.linspace(0, np.pi / 2, nf)); env[-ni:] = np.cos(np.linspace(0, np.pi / 2, ni))
    x[z0 - nf:z1 + ni] += unit_tone(tr, z0 / SR, n) * local_floor(tr, z0) * env
    print(f'dropout repaired: {tr} {z0 / SR:.3f}-{z1 / SR:.3f} s ({(z1 - z0) / SR * 1000:.0f} ms)')
AH = {tr: sosfilt(HP, x).astype(np.float32) for tr, x in A.items()}


# ---- per-span layers with their own envelopes; joints decided first
XF_D, XF_R = int(0.012 * SR), int(0.020 * SR)     # crossfade length: direct joint / to-from room tone
cuts = []                                         # (k, i_in, i_out): span k plays on output samples [i_in, i_out)
lay_in = [None] * len(S); lay_out = [None] * len(S); xin = [0] * len(S); xout = [0] * len(S)
report = []
LONG = set()                                      # v6: fades into the bed that decay linearly in dB (natural word end)
for k, s in enumerate(S):
    p = pos[k]; j0, j1 = p['start'], p['start'] + p['n']
    if k == 0: lay_in[k], xin[k] = j0, 0
    if p['air'] > 0 or k == len(S) - 1:            # span -> room tone (or the end)
        if k == len(S) - 1: lay_out[k], xout[k] = j1, 0
        else:
            i = best(k, None, j1, -0.06, 0.03 if not s['c_out'] else 0.005)
            loud = rms(s['spk'], src_idx(k, i)) > 3.0 * local_floor(s['spk'], src_idx(k, i))     # still sounding -> longer fade
            lay_out[k], xout[k] = i, (int(0.050 * SR) if loud else XF_R)
            if loud: LONG.add(k)
            report.append((k, 'out->room', (i - j1) / SR))
        if k + 1 < len(S):                         # room tone -> next span
            J = j1 + p['air']; i = best(None, k + 1, J, -0.04 if not S[k + 1]['c_in'] else -0.01, 0.04 if not S[k + 1]['c_in'] else 0.005); lay_in[k + 1], xin[k + 1] = i, XF_R
            report.append((k + 1, 'room->in', (i - J) / SR))
    else:                                          # direct joint
        # a word that runs right up to the cut is never shortened: coarticulated outgoing end -> the joint may only move later,
        # coarticulated incoming onset -> only earlier (restores what the aligner's boundary chopped); both -> stays, longer fade
        co, ci = s['c_out'], S[k + 1]['c_in']
        lo, hi = (-0.005, 0.005) if (co or ci) else (-0.05, 0.05)       # coarticulated: later = leaks the cut filler, earlier = chops
        i = best(k, k + 1, j1, lo, hi); xf = XF_D if not (co and ci) else int(0.018 * SR)
        lay_out[k], xout[k] = i, xf; lay_in[k + 1], xin[k + 1] = i, xf
        so, si = src_idx(k, i), src_idx(k + 1, i)
        if rms(s['spk'], so) > 3.0 * local_floor(s['spk'], so) and rms(S[k + 1]['spk'], si) < 2.0 * local_floor(S[k + 1]['spk'], si):
            lay_out[k], xout[k] = i - int(0.020 * SR), int(0.045 * SR)      # v6: still sounding -> 45 ms fade that ends at the joint
            LONG.add(k)
            report.append((k, 'long-fade', 0.0))
        report.append((k + 1, 'direct', (i - j1) / SR))

out = np.zeros(NTOT + SR, np.float32)
room = np.zeros(NTOT + SR, np.float32)
for k, s in enumerate(S):
    tr = s['spk']; g = gain[tr]
    i0, i1 = lay_in[k] - xin[k] // 2, lay_out[k] + xout[k] // 2
    i0 = max(0, i0); idx = np.arange(i0, i1)
    sidx = pos[k]['a_i'] + (idx - pos[k]['start'])
    x = A[tr][np.clip(sidx, 0, len(A[tr]) - 1)] * g
    env = np.ones(len(x), np.float32)
    if xin[k]: r = np.linspace(0, 1, xin[k], dtype=np.float32); env[:xin[k]] = np.sqrt(r)
    if xout[k]:
        r = np.linspace(1, 0, xout[k], dtype=np.float32)
        env[-xout[k]:] = (10 ** (-2.4 * (1 - r)) - 10 ** -2.4) / (1 - 10 ** -2.4) if k in LONG else np.sqrt(r)
    if k == len(S) - 1: n4 = int(0.4 * SR); env[-n4:] *= np.linspace(1, 0, n4, dtype=np.float32) ** 2
    out[i0:i1] += x * env
    if pos[k]['air'] > 0 and k + 1 < len(S):     # room tone bridging the air, crossfaded with both neighbours
        fo, fi_ = xout[k], xin[k + 1]
        r0 = lay_out[k] - fo // 2; r1 = lay_in[k + 1] + fi_ // 2
        rt = unit_tone(tr, s['e'], r1 - r0) * local_floor(tr, int(s['e'] * SR)) * g      # v6: at his REAL background level
        env = np.ones(r1 - r0, np.float32)
        env[:fo] = np.sqrt(np.linspace(0, 1, fo, dtype=np.float32)); env[-fi_:] = np.sqrt(np.linspace(1, 0, fi_, dtype=np.float32))
        room[r0:r1] += rt * env
vcut = (out + room)[:NTOT]

# ---- v6: background-level map per speaker (old cut timeline); the BED itself is added after the recut (no chopped glides)
FLOOR_MIN = 10 ** (-58 / 20)                       # never below a real room: Nic's noise-suppressed pauses sit at -80..-90
Lt_raw = np.zeros(NTOT, np.float32); spk_w = {tr: np.zeros(NTOT, np.float32) for tr in A}
for k, s in enumerate(S):
    i0 = max(0, lay_in[k] - xin[k] // 2) if k else 0
    i1 = NTOT if k == len(S) - 1 else max(0, lay_in[k + 1] - xin[k + 1] // 2)
    tr = s['spk']; fl = max(FLOOR_MIN, local_floor(tr, int((s['a'] + s['e']) / 2 * SR)) * gain[tr])
    Lt_raw[i0:i1] = fl; spk_w[tr][i0:i1] = 1.0
END_I = lay_out[len(S) - 1]
Lt_raw[END_I:] = 1e-6
# ---- de-click: single-sample jumps far above the local level (gate edges / mouth clicks) -> cubic bridge over 1.5 ms
d = np.abs(np.diff(vcut)); loc = np.convolve(np.abs(vcut), np.ones(480) / 480, 'same')[1:]
for c in np.flatnonzero(d > np.maximum(6 * loc, 0.01)):
    a0, a1 = c - 36, c + 36
    if a0 < 4 or a1 > len(vcut) - 4: continue
    xs = np.r_[a0 - 3:a0 + 1, a1:a1 + 4]; cf = np.polyfit(xs, vcut[xs], 3); vcut[a0:a1] = np.polyval(cf, np.arange(a0, a1))

# ---- clean-up: high-pass, gentle de-ess, soft levelling (no spectral denoise -> no warble)
p = OUT + '_v.f32'; open(p, 'wb').write(vcut.astype(np.float32).tobytes())
subprocess.run([FF, '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', p,
                '-af', 'highpass=f=75:poles=2,acompressor=threshold=0.125:ratio=1.6:attack=15:release=200:makeup=1:knee=4',
                '-c:a', 'pcm_f32le', OUT + 'voice_v6_cut.wav'], check=True)
os.remove(p)
raw = subprocess.run([FF, '-v', 'error', '-i', OUT + 'voice_v6_cut.wav', '-f', 'f32le', '-'], capture_output=True).stdout
vcut = np.frombuffer(raw, np.float32).copy()

# ---- the v2 tight recut on top (same regions as newcut.py -> same NEW timeline), 10 ms crossfades at the joins
REG = [(r[0], r[1]) for r in json.load(open(HERE + 'newtime.json'))['regions']]
xf = int(0.010 * SR); h = xf // 2; parts = []; prev = 0
for r0, r1 in REG:
    parts.append((prev, int(round(r0 * SR)))); prev = int(round(r1 * SR))
parts.append((prev, len(vcut)))
res = [vcut[parts[0][0]:parts[0][1] - h]]
r = np.linspace(0, 1, 2 * h, dtype=np.float32)
for (pa, pb), (a, b) in zip(parts[:-1], parts[1:]):
    # equal-power crossfade centred on the joint: outgoing runs h past its cut, incoming starts h before its cut (both quiet)
    res.append(vcut[pb - h:pb + h] * np.sqrt(1 - r) + vcut[a - h:a + h] * np.sqrt(r))
    res.append(vcut[a + h:b - h] if (a, b) != parts[-1] else vcut[a + h:b])
v_new = np.concatenate(res)


def recut(arr):
    out_ = [arr[parts[0][0]:parts[0][1] - h]]
    for (pa, pb), (a, b) in zip(parts[:-1], parts[1:]):
        out_.append(arr[pb - h:pb + h]); out_.append(arr[a + h:b - h] if (a, b) != parts[-1] else arr[a + h:b])
    return np.concatenate(out_)
Lt = recut(np.pad(Lt_raw, (0, max(0, len(vcut) - NTOT)), constant_values=1e-6)[:len(vcut)])
gl = int(0.30 * SR); ker = np.hanning(gl).astype(np.float32); ker /= ker.sum()
Lt = (10 ** (fftconvolve(20 * np.log10(Lt + 1e-9), ker, 'same') / 20)).astype(np.float32)      # glide in dB (0.3 s)
bed = np.zeros(len(v_new), np.float32)
for tr in A:
    w_ = recut(np.pad(spk_w[tr], (0, max(0, len(vcut) - NTOT)))[:len(vcut)])
    w_ = fftconvolve(w_, ker, 'same').astype(np.float32)
    if w_.max() > 0: bed += unit_tone(tr, 3.0, len(v_new)) * w_
bed /= np.sqrt(np.clip(fftconvolve(bed * bed, np.ones(4800) / 4800, 'same'), 1e-12, None))
lv2 = np.clip(fftconvolve(v_new * v_new, np.ones(480) / 480, 'same'), 0, None)
fill = np.sqrt(np.clip(1 - lv2 / (Lt * Lt + 1e-12), 0, 1))
fill = fftconvolve(fill, np.ones(960) / 960, 'same').astype(np.float32)
v_new = (v_new + bed * Lt * np.clip(fill, 0, 1)).astype(np.float32)
want = int(round(87.5 * SR))
want = (os.path.getsize(HERE + 'audio/voice_new.wav') - 92) // 8               # stereo float32 wav, same length as v2-v4's voice
v_new = np.pad(v_new, (0, max(0, want - len(v_new))))[:want]
p = OUT + '_n.f32'; open(p, 'wb').write(v_new.astype(np.float32).tobytes())
subprocess.run([FF, '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', p, '-c:a', 'pcm_f32le', OUT + 'voice_v6.wav'], check=True)
os.remove(p)
print('gains dB', {k: round(20 * np.log10(v), 1) for k, v in gain.items()}, 'cut len', NTOT / SR, 'new len', len(v_new) / SR)
for k, kind, d in report:
    s = S[k]; print(f"  span {k:2d} {s['spk']:6s} {s['join']:5s} {kind:9s} moved {d * 1000:+6.1f} ms   << {s['w0']}")
