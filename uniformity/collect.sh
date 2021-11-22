#!/bin/bash

res="REPLACE"

for val in {0..9..1}
do
    mkdir $val
    cd $val
    cp ../Master/* .
    sed -e "s/$res/$val/" _nanostars.py > nanostars.py
    qsub start.pbs
    cd ..
done
