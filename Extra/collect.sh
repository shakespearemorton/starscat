#!/bin/bash
#!/bin/bash

res="REPLACER"

for val in {1..20..1}
do
    mkdir $val
    cd $val
    cp ../* .
    sed -e "s/$res/$val/" _nanostars.py > nanostars1.py
    qsub start.pbs
    cd ..
done
