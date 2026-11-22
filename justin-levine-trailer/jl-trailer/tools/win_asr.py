"""transcribe windows of a track: win_asr.py track.wav out.json a1-b1 a2-b2 ... (seconds)"""
import sys, json, numpy as np, soundfile as sf
from faster_whisper import WhisperModel
wav, out = sys.argv[1], sys.argv[2]
x, sr = sf.read(wav, dtype='float32')
m = WhisperModel('small.en', device='cpu', compute_type='int8')
res = {}
for w in sys.argv[3:]:
    a, b = map(float, w.split('-'))
    seg = x[int(a * sr):int(b * sr)]
    segs, _ = m.transcribe(seg, word_timestamps=True, vad_filter=True, language='en')
    words = []
    for s in segs:
        words += [{'w': t.word.strip(), 's': round(a + t.start, 2), 'e': round(a + t.end, 2)} for t in s.words]
    res[w] = words
    print(f'== {w}'); line = []; 
    for t in words: line.append(f"{t['w']}@{t['s']:.1f}")
    print(' '.join(line), flush=True)
json.dump(res, open(out, 'w'))
