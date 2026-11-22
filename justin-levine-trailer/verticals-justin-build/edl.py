"""Script v4 edit list -> exact source in/out points (transcript words snapped to the waveform, with breathing room)."""
import json, os, sys
sys.path.insert(0, os.path.expanduser("~/verticals-justin-build"))
import wav
B = os.path.expanduser('~/verticals-justin-build/')

# One entry per script line: (beat, speaker, spans). A span = (first word start, last word start, join before it).
# join: 'line' = new script line, 'cut' = script [cut] inside a line, 'fill' = filler/repeat removed mid-sentence.
LINES = [
    (1, 'justin', [(259.16, 260.84, 'line'),          # our engineering team spends zero time,
                   (261.72, 261.94, 'fill'),          # [uh] writing code
                   (262.94, 263.86, 'fill'),          # [and, and,] and 100% of their time,
                   (265.02, 265.02, 'fill'),          # [um] orchestrating,
                   (265.98, 266.60, 'fill')]),        # [uh] how the code is written.
    (2, 'nic',    [(3.74, 9.60, 'line')]),            # Today we're super excited ... CEO of Shepherd.
    (2, 'justin', [(163.10, 164.86, 'line'),          # I had founded a construction software business.
                   (2703.48, 2703.60, 'cut'),         # We sold
                   (2703.98, 2705.96, 'fill'),        # [our,] our business to Building Connected and then,
                   (2706.70, 2707.16, 'fill')]),      # [you know,] together to Autodesk.
    (2, 'nic',    [(1840.34, 1840.78, 'line'),        # You guys
                   (1842.30, 1842.72, 'fill'),        # [have, have, you] strike me as,
                   (1844.46, 1851.32, 'fill'),        # [um, like,] top 1% ... leveraged partnerships
                   (1858.52, 1861.10, 'cut'),         # Procore and Greenlight Re from the beginning,
                   (1862.16, 1862.76, 'fill')]),      # [you know,] Intact later on.
    (3, 'nic',    [(1112.86, 1112.86, 'line'),        # Maybe
                   (1113.36, 1117.12, 'fill')]),      # [you have a,] you put a sensor ... better rates, right?
    (4, 'justin', [(1226.48, 1229.44, 'line')]),      # Worth your while is 15% difference on price.
    (5, 'justin', [(1408.44, 1413.62, 'line'),        # Progressive was the one ... submission to,
                   (1414.62, 1414.62, 'fill'),        # [you know,] thousands.
                   (1423.22, 1425.38, 'cut')]),       # And I just think we can do the same thing in commercial.
    (6, 'justin', [(1617.94, 1623.88, 'line'),        # I used to work ... inspect the job site.
                   (1633.96, 1635.12, 'cut')]),       # It's somewhat manufactured.
    (7, 'justin', [(2392.28, 2393.88, 'line'),        # From inception of the company
                   (2395.66, 2398.46, 'fill'),        # [functionally] to our first ... about 11 months,
                   (2399.84, 2399.84, 'fill'),        # [um,] which,
                   (2402.32, 2403.16, 'fill')]),      # [like, from what we understood at the time] was, like, record pace.
    (8, 'luke',   [(3014.98, 3016.50, 'line')]),      # Do you think we're in an AI bubble?
    (8, 'justin', [(3019.86, 3019.86, 'line'),        # No.
                   (3032.46, 3033.34, 'cut'),         # I just think that we
                   (3033.82, 3037.56, 'fill')]),      # [like] have consistently underestimated how big AI is.
    (9, 'justin', [(266.80, 270.14, 'line')]),        # And so I think underwriting is ... in that direction.
    (10, 'nic',   [(3068.64, 3073.98, 'line')]),      # When do you think we will see the first fully AI underwritten commercial policy?
    (10, 'justin', [(3080.68, 3082.64, 'line')]),     # We actually, like, we did this.
    (10, 'luke',  [(3083.56, 3085.52, 'line')]),      # Breaking news. Breaking news.
]
# breathing room (s): head before the first word / tail after the last word, by join type
HEAD = {'line': 0.40, 'cut': 0.30, 'fill': 0.12}
TAIL = {'line': 0.45, 'cut': 0.35, 'fill': 0.12}
SAFE = 0.05                    # never get closer than this to a sound that is cut out
OVERRIDE = {                    # (beat, speaker, span idx): (head, tail)
    (8, 'luke', 0): (0.40, 0.50),     # question, then 1 s of silence before "No."
    (8, 'justin', 0): (0.50, 0.45),
    (10, 'justin', 0): (0.30, 0.25),  # "we did this." -> "Breaking news" keeps the real 0.5 s gap
    (10, 'luke', 0): (0.25, 0.90),    # last word finishes, then held tail
}


PAUSE_MAX, PAUSE_TO = 0.90, 0.55   # a mid-sentence pause longer than PAUSE_MAX is shortened to PAUSE_TO


def build():
    global ALIGN
    ALIGN = json.load(open(B + 'cut/align.json'))
    spans = []
    for li, (beat, spk, ss) in enumerate(LINES):
        for k, (t0, t1, join) in enumerate(ss):
            nxt = ss[k + 1][2] if k + 1 < len(ss) else 'line'
            A = ALIGN[f'{spk}@{t0}']
            b = wav.span_bounds(spk, A['words'], A['first'], A['last'])
            head, tail = HEAD[join], TAIL[nxt]
            if (beat, spk, k) in OVERRIDE: head, tail = OVERRIDE[(beat, spk, k)]
            room_in = max(0.0, b['onset'] - b['prev_end'] - SAFE)
            room_out = max(0.0, b['next_start'] - b['offset'] - SAFE)
            a = b['onset'] - min(head, room_in)
            e = b['offset'] + min(tail, room_out)
            b['room_in'], b['room_out'] = room_in, room_out
            # long hesitations inside the kept words: shorten, keeping half of PAUSE_TO on each side
            parts, cur = [], a
            for r0, r1 in wav.silence_runs(spk, b['onset'] + 0.05, b['offset'] - 0.05, PAUSE_MAX):
                parts.append((cur, r0 + PAUSE_TO / 2)); cur = r1 - PAUSE_TO / 2
            parts.append((cur, e))
            for pi, (pa, pe) in enumerate(parts):
                spans.append(dict(beat=beat, spk=spk, line=li, join=join if pi == 0 else 'pause', a=round(pa, 3), e=round(pe, 3),
                                  **{k2: round(v, 3) if isinstance(v, float) else v for k2, v in b.items()}, w0=t0, w1=t1, part=pi, nparts=len(parts)))
    # spread the space at every join: wanted gap G, taken from whatever silence each side has; if the words run
    # straight into the next ones in the recording, the rest is added as room tone (picture holds) = 'air'
    G = {'line': 0.80, 'cut': 0.55, 'fill': 0.22, 'pause': 0.55}
    for i in range(len(spans) - 1):
        s0, s1 = spans[i], spans[i + 1]
        if s1['join'] == 'pause': s0['air'] = 0; continue
        g = G[s1['join']]
        key0, key1 = (s0['beat'], s0['spk'], 0), (s1['beat'], s1['spk'], 0)
        if key0 in OVERRIDE and s0['part'] == s0['nparts'] - 1 and s0['w1'] == LINES[s0['line']][2][-1][1]: g = OVERRIDE[key0][1] + (OVERRIDE.get(key1, (0.4, 0))[0])
        tail = min(s0['room_out'], g / 2); head = min(s1['room_in'], g - tail); tail = min(s0['room_out'], g - head)
        s0['e'] = round(s0['offset'] + tail, 3); s1['a'] = round(s1['onset'] - head, 3)
        s0['air'] = round(max(0.0, g - tail - head), 3) if s1['join'] != 'fill' else 0.0
    spans[0]['a'] = round(spans[0]['onset'] - min(0.4, spans[0]['room_in']), 3)
    spans[-1]['e'] = round(spans[-1]['offset'] + min(0.9, spans[-1]['room_out']), 3)
    spans[-1]['air'] = round(max(0.0, 0.9 - (spans[-1]['e'] - spans[-1]['offset'])), 3)
    return spans


if __name__ == '__main__':
    S = build()
    json.dump(S, open(B + 'cut/spans.json', 'w'), indent=1)
    tot = 0
    for s in S:
        d = s['e'] - s['a']; tot += d + s.get('air', 0)
        W = [w[2] for w in wav.track(s['spk'])['words'] if s['w0'] - 0.01 <= w[0] <= s['w1'] + 0.01] if s['part'] == 0 else ['  (pause shortened)']
        flag = ('C-in ' if s['c_in'] else '') + ('C-out' if s['c_out'] else '')
        print(f"{s['beat']:>2} {s['spk']:<6} {s['join']:<4} {s['a']:9.3f}-{s['e']:9.3f} ({d:5.2f}s)  on {s['onset']:.3f} [{s['onset']-s['a']:.2f}] off {s['offset']:.3f} [{s['e']-s['offset']:.2f}] "
              f"{flag:10} air {s.get('air',0):.2f} | {s['prev_word']!r:>12} << {' '.join(W)} >> {s['next_word']!r}")
    print(f'total {tot:.2f} s')
