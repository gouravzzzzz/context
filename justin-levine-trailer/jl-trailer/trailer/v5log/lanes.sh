#!/bin/zsh
P=~/ks-ron-build/venv/bin/python
T=/Users/gourav/jl-trailer/trailer
export NW=3
run() { name=$1; shift; echo "$(date +%T) START $name" >> $T/v5log/status.txt; (cd $T/$1 && shift && "$@") > $T/v5log/$name.log 2>&1; echo "$(date +%T) END $name rc=$?" >> $T/v5log/status.txt; }
laneA() {
  run 00_open_v3 . $P open_v3/scene.py render v2segs/00_open_v3.mp4
  run 05_06_v3 v3_20grid $P grid_trans.py seg
  run 11a_risk_v3 . $P render_v2.py v1 1189 1255 v2segs/11a_risk_v3.mp4
  run 15_cloud_lloyds_v3 v2segs/seg15 $P scene15_v3.py final
}
laneB() {
  run 16_split_end_fx . $P render_v2.py v1 1846 2175 v2segs/16_split_end_fx.mp4
  run 13_v3 . $P render_v2.py v1 1410 1660 v2segs/13_v3.mp4
  run 02_founded_v3 . $P render_v2.py v1 317 353 v2segs/02_founded_v3.mp4
  run 09_dollar15 v2seg09 $P scene.py render
}
laneC() {
  run 01_name3d_v3 . $P render_v2.py s1014 206 317 v2segs/01_name3d_v3.mp4
  run 04_showcase alt_15_19 $P scene4.py render
  run 07_procore v2_07 $P seg07_procore.py patch 692 850
  run 10_tv_counter v2segs $P seg10_tv_counter.py render
  run 11b_manu_v3 seg11b $P scene11b.py render
}
laneA & laneB & laneC & wait
echo "$(date +%T) ALL DONE" >> $T/v5log/status.txt
