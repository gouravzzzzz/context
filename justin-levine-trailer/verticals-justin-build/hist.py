import sys, os
sys.path.insert(0, os.path.expanduser("~/verticals-justin-build"))
import wav, numpy as np
for tr, t in [('nic', 5), ('nic', 1850), ('nic', 3070), ('justin', 263), ('justin', 1620), ('justin', 3030), ('luke', 3015), ('luke', 3085)]:
    T = wav.track(tr); i0, i1 = max(0,int((t-20)/wav.HOP)), int((t+20)/wav.HOP); v = T['bb'][i0:i1]
    print(tr, t, ' '.join(f"{p}:{np.percentile(v, p):.0f}" for p in [1, 5, 10, 20, 30, 50, 70, 90, 99]))
