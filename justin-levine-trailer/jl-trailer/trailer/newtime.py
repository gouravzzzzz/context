"""Trailer v2 timing (tight recut). OLD = the v1 cut timeline (timeline.json / words_cut.json / mix.wav, 102.6 s).
NEW = the v2 timeline (timeline_new.json / words_new.json / audio/mix2.wav). 24 fps, all cuts frame-aligned.
  M(t_old) -> t_new        (a time inside a removed pause lands on its cut point)
  A(t_new) -> t_old        (for lip-synced speaker footage: cut_frame(round(A(t)*FPS)) is in sync with mix2.wav)"""
import json, os
_H = os.path.dirname(os.path.abspath(__file__)) + '/'
REG = [(r[0], r[1]) for r in json.load(open(_H + 'newtime.json'))['regions']]
FPS = 24
def M(t):
    d = 0.0
    for r0, r1 in REG:
        if t >= r1: d += r1 - r0
        elif t > r0: return r0 - d
        else: break
    return t - d
def A(t):
    d = 0.0
    for r0, r1 in REG:
        if t + d >= r0 - 1e-9: d += r1 - r0
        else: break
    return t + d
def n_old(n_new): return int(round(A(n_new / FPS + 1e-4) * FPS))   # +eps: at a cut point show the first KEPT frame after the pause
WORDS = json.load(open(_H + 'words_new.json'))          # [t0, t1, word, speaker, ...] on the NEW timeline
TL = json.load(open(_H + 'timeline_new.json'))
