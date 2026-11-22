#!/bin/zsh
P=~/ks-ron-build/venv/bin/python
T=/Users/gourav/jl-trailer/trailer
export NW=3
run() { name=$1; shift; echo "$(date +%T) START $name" >> $T/v5log/status.txt; (cd $T/$1 && shift && "$@") > $T/v5log/$name.log 2>&1; echo "$(date +%T) END $name rc=$?" >> $T/v5log/status.txt; }
laneD() { run 10_tv_counter v2segs $P seg10_tv_counter.py render; }
laneE() { run 11b_manu_v3 seg11b $P scene11b.py render; run 07_procore v2_07 $P seg07_procore.py patch 692 850; }
laneD & laneE & wait
echo "$(date +%T) LANES2 DONE" >> $T/v5log/status.txt
