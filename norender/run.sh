#!/bin/bash
gens=100
for i in $(seq 1 $gens);
do
    python2 Map.py #>> data.txt
    echo "Generation $i / $gens"
    
done