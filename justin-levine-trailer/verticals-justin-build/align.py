"""wav2vec2 CTC forced alignment of the transcript words around every span, so each cut boundary is bracketed
between the last letter of the kept word and the first letter of the next one. Writes cut/align.json."""
import json, os, re, sys, wave
import numpy as np, torch, torchaudio
B = os.path.expanduser('~/verticals-justin-build/')
sys.path.insert(0, B)
from edl import LINES
bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
model = bundle.get_model().eval()
LAB = bundle.get_labels(); IDX = {c: i for i, c in enumerate(LAB)}
NUM = {'15': 'FIFTEEN', '100': 'ONE HUNDRED', '50': 'FIFTY', '11': 'ELEVEN', '1': 'ONE', '%': 'PERCENT', 'AI': 'A I'}


def norm(w):
    w = w.strip()
    if w.strip('.,?!') in NUM: return NUM[w.strip('.,?!')]
    return re.sub(r"[^A-Z' ]", '', w.upper().replace('-', ' ')).strip()


def load(tr):
    with wave.open(B + f'work/{tr}16.wav') as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768


def align(x, words, a, b):
    """words: list of whisper words inside [a,b]. Returns [(start, end, text)] in recording seconds (CTC spike spans)."""
    seg = torch.from_numpy(x[int(a * 16000):int(b * 16000)].copy())[None]
    with torch.inference_mode():
        em, _ = model(seg)
    em = torch.log_softmax(em, -1)
    toks, owner = [], []
    for k, w in enumerate(words):
        s = norm(w[2])
        for ch in s.replace(' ', '|'):
            if ch in IDX: toks.append(IDX[ch]); owner.append(k)
    ali, scores = torchaudio.functional.forced_align(em, torch.tensor([toks], dtype=torch.int32), blank=0)
    spans = torchaudio.functional.merge_tokens(ali[0], scores[0].exp())
    ratio = (b - a) / em.shape[1]
    out = [[None, None, w[2]] for w in words]
    for sp, k in zip(spans, owner):
        if LAB[sp.token] == '|': continue
        t0, t1 = a + sp.start * ratio, a + sp.end * ratio
        if out[k][0] is None: out[k][0] = t0
        out[k][1] = t1
    return out


res, XC = {}, {}
for beat, spk, ss in LINES:
    x = XC.setdefault(spk, load(spk))
    W = sorted(json.load(open(B + f'tx/{spk}.json')), key=lambda w: w[0])
    idx = lambda t: min(range(len(W)), key=lambda k: abs(W[k][0] - t))
    groups = []                                   # spans that sit close together in the recording are aligned as one block
    for t0, t1, _ in ss:
        if groups and 0 <= t0 - groups[-1][-1][1] < 6: groups[-1].append((t0, t1))
        else: groups.append([(t0, t1)])
    for g in groups:
        i, j = idx(g[0][0]), idx(g[-1][1])
        i0, j1 = max(0, i - 3), min(len(W) - 1, j + 3)
        while i0 < i and W[i0 + 1][0] - W[i0][1] > 1.5: i0 += 1          # don't reach across a long silence / other window
        while j1 > j and W[j1][0] - W[j1 - 1][1] > 1.5: j1 -= 1
        a, b = W[i0][0] - 0.10, W[j1][1] + 0.3
        al = align(x, W[i0:j1 + 1], a, b)
        for t0, t1 in g:
            res[f'{spk}@{t0}'] = dict(words=al, first=idx(t0) - i0, last=idx(t1) - i0)
        print(f"{spk:6} {g[0][0]:8.2f}  " + ' '.join(f"{w[2]}[{w[0]:.2f}-{w[1]:.2f}]" for w in al if w[0] is not None), flush=True)
json.dump(res, open(B + 'cut/align.json', 'w'), indent=0)
