import json, sys
def fmt(t): return f"{int(t//60):02d}:{t%60:05.2f}"
tr, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
W = [w for w in json.load(open(f'tx/{tr}.json')) if a <= w[0] <= b]
line, st = [], None
for i, w in enumerate(W):
    if line and w[0] - W[i-1][1] > 0.5:
        print(f"[{fmt(st)}] " + ' '.join(line)); line = []
    if not line: st = w[0]
    line.append(f"{w[2]}")
if line: print(f"[{fmt(st)}] " + ' '.join(line))
