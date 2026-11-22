"""Join the v2 segments (frame-exact, NEW timeline) + audio/mix2.wav -> ~/Downloads/Verticals_Justin_Levine_Trailer_v2.mp4
  python assemble_v2.py            (checks every segment's frame count first)"""
import subprocess, sys, os, json
FF = '/Users/gourav/ks-ron-build/reel1/ff'
D = '/Users/gourav/jl-trailer/trailer/v2segs/'
SEGS = [('00_open_fx', 0, 206), ('01_name3d_fx', 206, 317), ('02_founded', 317, 353), ('04_showcase', 353, 434),
        ('05_autodesk_fx', 434, 485), ('06_nic_fx', 485, 692), ('07_procore', 692, 850), ('09_dollar15', 850, 971),
        ('10_tv_counter', 971, 1189), ('11_risk_osha', 1189, 1343), ('12_manufactured', 1343, 1392),
        ('13_calendar_no_fx', 1392, 1689), ('15_cloud_lloyds', 1689, 1846), ('16_split_end_fx', 1846, 2175)]
OUT = sys.argv[1] if len(sys.argv) > 1 else '/Users/gourav/Downloads/Verticals_Justin_Levine_Trailer_v2.mp4'


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
subprocess.run([FF, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-i', '/Users/gourav/jl-trailer/trailer/audio/mix2.wav',
                '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', '-r', '24',
                '-c:a', 'aac', '-b:a', '320k', '-t', f'{dur:.4f}', '-movflags', '+faststart', OUT], check=True)
print('done', OUT, total, 'frames', dur, 's')
