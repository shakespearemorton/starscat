#!/bin/bash

res="REPLACE"

cd Master
python _nanostars.py
cd ..
cd test
cp ../Master/* .
qsub start.pbs
