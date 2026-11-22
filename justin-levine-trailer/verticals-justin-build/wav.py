"""Waveform helpers: per-track energy envelopes (broadband + fricative band) and silence-gap finding between two words."""
import json, wave, os, numpy as np
from scipy import signal as ss
B = os.path.expanduser('~/verticals-justin-build/')
SR, HOP, WIN = 16000, 0.005, 0.020          # 5 ms hop, 20 ms window
_cache = {}


def track(tr):
    if tr in _cache: return _cache[tr]
    with wave.open(B + f'work/{tr}16.wav') as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    bb = ss.sosfiltfilt(ss.butter(4, 90, 'highpass', fs=SR, output='sos'), x)
    hf = ss.sosfiltfilt(ss.butter(4, [2500, 7000], 'bandpass', fs=SR, output='sos'), x)
    h, n = int(HOP * SR), int(WIN * SR)

    def env(y):
        p = np.convolve(y * y, np.ones(n) / n, 'same')[::h]
        return 10 * np.log10(p + 1e-12)
    words = [w for w in json.load(open(B + f'tx/{tr}.json'))]
    words.sort(key=lambda w: w[0])
    _cache[tr] = dict(bb=env(bb), hf=env(hf), words=words)
    return _cache[tr]


def floors(tr, t):
    """Local activity thresholds (bb, hf) from the +-20 s around t."""
    T = track(tr); i0, i1 = max(0, int((t - 20) / HOP)), int((t + 20) / HOP)
    bb, hf = T['bb'][i0:i1], T['hf'][i0:i1]
    # gated tracks (Nic) sit at -80 dB between turns, so also cap the threshold at 30 dB under the speech peaks
    return max(np.percentile(bb, 10) + 11, np.percentile(bb, 97) - 30), max(np.percentile(hf, 10) + 9, np.percentile(hf, 97) - 32)


def active(tr, a, b):
    T = track(tr); fb, fh = floors(tr, (a + b) / 2)
    i0, i1 = int(a / HOP), int(b / HOP)
    return (T['bb'][i0:i1] > fb) | (T['hf'][i0:i1] > fh), i0


def word(tr, t):
    """Word whose start is nearest t; returns (index, word)."""
    W = track(tr)['words']; i = int(np.argmin([abs(w[0] - t) for w in W]))
    assert abs(W[i][0] - t) < 0.03, (tr, t, W[i])
    return i, W[i]


def gap(tr, a_end, b_start):
    """Silence between a word ending ~a_end and the next starting ~b_start.
    Returns (g0, g1, coart): speech offset of the first, onset of the second; coart=True if no real silence."""
    lo, hi = a_end - 0.12, b_start + 0.12
    if hi - lo < 0.05: hi = lo + 0.05
    act, i0 = active(tr, lo, hi)
    runs, s = [], None
    for k, v in enumerate(np.append(act, True)):
        if not v and s is None: s = k
        if v and s is not None: runs.append((s, k)); s = None
    runs = [r for r in runs if (r[1] - r[0]) * HOP >= 0.03]
    if runs:
        r = max(runs, key=lambda r: r[1] - r[0])
        return (i0 + r[0]) * HOP, (i0 + r[1]) * HOP, False
    T = track(tr); j0, j1 = int((a_end - 0.06) / HOP), int((b_start + 0.06) / HOP)
    if j1 <= j0: j1 = j0 + 1
    m = (j0 + int(np.argmin(T['bb'][j0:j1]))) * HOP
    return m, m, True


def bounds(tr, t_first, t_last):
    """Speech onset of word t_first and offset of word t_last, plus the silence available around them."""
    T = track(tr); W = T['words']
    i, wf = word(tr, t_first); j, wl = word(tr, t_last)
    pv = W[i - 1] if i > 0 else [wf[0] - 2, wf[0] - 2]
    nx = W[j + 1] if j + 1 < len(W) else [wl[1] + 2, wl[1] + 2]
    if wf[0] - pv[1] > 1.5: pv = [wf[0] - 1.5, wf[0] - 1.5]      # far / other window: treat as silence
    if nx[0] - wl[1] > 1.5: nx = [wl[1] + 1.5, wl[1] + 1.5]
    p0, onset, c_in = gap(tr, pv[1], wf[0])
    offset, n1, c_out = gap(tr, wl[1], nx[0])
    return dict(onset=onset, prev_end=p0, c_in=c_in, offset=offset, next_start=n1, c_out=c_out,
                prev_word=pv[2] if len(pv) > 2 else '', next_word=nx[2] if len(nx) > 2 else '')


def score(tr, a, b):
    """Per-frame 'speechiness' over [a,b): dB above the activity thresholds (max of both bands)."""
    T = track(tr); fb, fh = floors(tr, (a + b) / 2)
    i0, i1 = int(a / HOP), max(int(b / HOP), int(a / HOP) + 1)
    return np.maximum(T['bb'][i0:i1] - fb, T['hf'][i0:i1] - fh), i0


def silence_runs(tr, a, b, min_len=0.03):
    s, i0 = score(tr, a, b)
    runs, st = [], None
    for k, v in enumerate(np.append(s > 0, True)):
        if not v and st is None: st = k
        if v and st is not None:
            if (k - st) * HOP >= min_len: runs.append(((i0 + st) * HOP, (i0 + k) * HOP))
            st = None
    return runs


def boundary(tr, a, b):
    """Boundary between two aligned words: a = last letter of the first word, b = first letter of the next.
    Returns (end_of_first, start_of_next, coarticulated)."""
    lo, hi = a, b + 0.03
    if hi - lo < 0.04: lo, hi = (a + b) / 2 - 0.03, (a + b) / 2 + 0.03
    R = silence_runs(tr, lo, hi)
    if R:
        g0, g1 = R[0][0], R[-1][1]
        if g0 <= lo + 0.006:                      # aligner marked the word end late: walk back to the real end
            s, i0 = score(tr, lo - 0.3, lo); k = len(s)
            while k > 0 and s[k - 1] <= 0: k -= 1
            g0 = (i0 + k) * HOP
        if g1 >= hi - 0.006:                      # next word starts later than its first letter spike
            s, i0 = score(tr, hi, hi + 0.3); k = 0
            while k < len(s) and s[k] <= 0: k += 1
            g1 = (i0 + k) * HOP
        return g0, g1, False
    s, i0 = score(tr, lo, hi)
    m = (i0 + int(np.argmin(s))) * HOP
    return m, m, True


def span_bounds(tr, al, first, last):
    """al: aligned words around a span (CTC spikes). Speech onset/offset of the span and the room around it."""
    W = al
    W = [w if not (w[2].startswith('Thank') or (w[2] == 'you.' and k and W[k-1][2].startswith('Thank'))) or k in (first, last)
         else [None, None, w[2]] for k, w in enumerate(W)]           # drop whisper's 'Thank you.' hallucinations
    F, L = W[first], W[last]
    P = W[first - 1] if first > 0 and W[first - 1][1] is not None else [F[0] - 1.5, F[0] - 1.5]
    N = W[last + 1] if last + 1 < len(W) and W[last + 1][0] is not None else [L[1] + 1.5, L[1] + 1.5]
    if F[0] - P[1] > 1.5: P = [F[0] - 1.5, F[0] - 1.5]
    if N[0] - L[1] > 1.5: N = [L[1] + 1.5, L[1] + 1.5]
    prev_end, onset, c_in = boundary(tr, P[1], F[0])
    offset, next_start, c_out = boundary(tr, L[1], N[0])
    return dict(onset=onset, prev_end=prev_end, c_in=c_in, offset=offset, next_start=next_start, c_out=c_out,
                prev_word=P[2] if len(P) > 2 else '', next_word=N[2] if len(N) > 2 else '')
