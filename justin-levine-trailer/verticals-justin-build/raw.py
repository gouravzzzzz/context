import sys, os
sys.path.insert(0, os.path.expanduser("~/verticals-justin-build"))
import wav, numpy as np
tr, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
T = wav.track(tr); i0, i1 = int(a / wav.HOP), int(b / wav.HOP)
bb, hf = T['bb'][i0:i1], T['hf'][i0:i1]
pk = np.percentile(T['bb'][int((a-20)/wav.HOP):int((b+20)/wav.HOP)], 97)
ch = ' .:-=+*#%@'
row = ''.join(ch[int(np.clip((v - (pk - 40)) / 4, 0, 9))] for v in bb.reshape(-1, 2).max(1))
hrow = ''.join(ch[int(np.clip((v - (pk - 50)) / 4, 0, 9))] for v in hf.reshape(-1, 2).max(1))
print(f"pk {pk:.1f}  (bb: 4 dB/step from pk-40; 10 ms/char)")
print(f"{a:.2f} bb|{row}|"); print(f"{a:.2f} hf|{hrow}|")
