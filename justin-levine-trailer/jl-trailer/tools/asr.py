import sys, json
from faster_whisper import WhisperModel
m = WhisperModel('small.en', device='cpu', compute_type='int8')
for wav in sys.argv[1:]:
    segs, _ = m.transcribe(wav, word_timestamps=True, vad_filter=False)
    words = []; lines = []
    for s in segs:
        lines.append(f'[{s.start:6.2f}-{s.end:6.2f}] {s.text.strip()}')
        words += [{'w': w.word.strip(), 's': round(w.start, 2), 'e': round(w.end, 2)} for w in s.words]
    json.dump(words, open(wav.replace('.wav', '_words.json'), 'w'))
    open(wav.replace('.wav', '_lines.txt'), 'w').write('\n'.join(lines))
    print(wav, len(words))
