#!/bin/bash
BASE="/etc/shinken"
OUTPUT="/tmp/shinken-conf.cfg"
DAEMONS="arbiter broker poller reactionner receiver scheduler"
EXCLUDEMODULES=sample.cfg

> $OUTPUT

cd $BASE

for e in $DAEMONS 
do 
    cd $e"s"
    for file in $(ls -1)
    do
        cat $file >> $OUTPUT
    done
    cd ..
done

echo "#===============================================================================" >> $OUTPUT
echo "# MODULES " >> $OUTPUT
echo "#===============================================================================" >> $OUTPUT


cd $BASE/modules

for file in $(ls -1 | grep -v "$EXCLUDEMODULES")
do
    cat $file >> $OUTPUT
done
    