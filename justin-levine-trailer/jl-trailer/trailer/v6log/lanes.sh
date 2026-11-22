#!/bin/zsh
P=~/ks-ron-build/venv/bin/python
T=/Users/gourav/jl-trailer/trailer
export NW=4
run() { name=$1; shift; echo "$(date +%T) START $name" >> $T/v6log/status.txt; (cd $T && "$@") > $T/v6log/$name.log 2>&1; echo "$(date +%T) END $name rc=$?" >> $T/v6log/status.txt; }
laneA() { run 01_name3d_v6 $P render_v2.py s1014 206 317 v2segs/01_name3d_v6.mp4; run 02_founded_v6 $P render_v2.py v1 317 353 v2segs/02_founded_v6.mp4; }
laneB() { run 16_split_end_v6 $P render_v2.py v1 1846 2175 v2segs/16_split_end_v6.mp4; }
laneA & laneB & wait
echo "$(date +%T) ALL DONE" >> $T/v6log/status.txt
