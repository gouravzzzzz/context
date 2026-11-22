"""v7: 16 re-rendered (BREAKING NEWS box behind Luke via rembg matte) + audio/mix5.wav (voice through Adobe Podcast Enhance, no background). v6: 01/02/16 re-rendered (headline G2 exit, cut-out G1 rise, Luke full screen + 2 zoom cuts + grade, no black) + audio/mix5.wav. v5: same segments re-rendered (stable talking heads, only Krish's 3 graphs) + audio/mix4.wav (no music, rebuilt voice).
Join the v2 segments (frame-exact, NEW timeline) + audio/mix2.wav -> ~/Downloads/Verticals_Justin_Levine_Trailer_v2.mp4
  python assemble_v2.py            (checks every segment's frame count first)"""
import subprocess, sys, os, json
FF = '/Users/gourav/ks-ron-build/reel1/ff'
D = '/Users/gourav/jl-trailer/trailer/v2segs/'
SEGS = [('00_open_v3', 0, 206), ('01_name3d_v6', 206, 317), ('02_founded_v6', 317, 353), ('04_showcase', 353, 434),
        ('05_06_v3', 434, 692), ('07_procore', 692, 850), ('09_dollar15', 850, 971),
        ('10_tv_counter', 971, 1189), ('11a_risk_v3', 1189, 1255), ('11b_manu_v3', 1255, 1410),
        ('13_v3', 1410, 1660), ('15_cloud_lloyds_v3', 1660, 1846), ('16_split_end_v6b', 1846, 2175)]
OUT = sys.argv[1] if len(sys.argv) > 1 else '/Users/gourav/Downloads/Verticals_Justin_Levine_Trailer_v7.mp4'


def nframes(f):
    o = subprocess.run([FF, '-v', 'error', '-i', f, '-map', '0:v', '-c', 'copy', '-f', 'null', '-'], capture_output=True, text=True)
    o2 = subprocess.run([FF, '-i', f, '-map', '0:v', '-c', 'copy', '-f', 'null', '-'], capture_output=True, text=True).stderr
    import re
    m = re.findall(r'frame=\s*(\d+)', o2)
    return int(m[-1]) if m else -1


bad = []
prev = 0
for name, n0, n1 in SEGS:
    f = D + name + '.mp4'
    assert n0 == prev, f'gap before {name}'; prev = n1
    if not os.path.exists(f): bad.append(f'{name}: MISSING'); continue
    k = nframes(f)
    print(f'{name:18s} {n0:5d}-{n1:5d}  want {n1 - n0:4d}  have {k:4d}', '' if k == n1 - n0 else '  <-- MISMATCH')
    if k != n1 - n0: bad.append(f'{name}: {k} != {n1 - n0}')
if bad:
    print('NOT READY:', bad); sys.exit(1)
lst = D + '_concat.txt'
open(lst, 'w').write(''.join(f"file '{D}{n}.mp4'\n" for n, _, _ in SEGS))
total = prev; dur = total / 24
subprocess.run([FF, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-i', '/Users/gourav/jl-trailer/trailer/audio/mix5.wav',
                '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', '-r', '24',
                '-c:a', 'aac', '-b:a', '320k', '-t', f'{dur:.4f}', '-movflags', '+faststart', OUT], check=True)
print('done', OUT, total, 'frames', dur, 's')
