import json, sys
tr, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
print(' '.join(f"{w[2]}[{w[0]:.2f}-{w[1]:.2f}]" for w in json.load(open(f'tx/{tr}.json')) if a <= w[0] <= b))
