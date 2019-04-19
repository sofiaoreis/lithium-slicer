#!/bin/bash

# check if defects4j is installed
command -v defects4j >/dev/null 2>&1 || { echo >&2 "defects4j not found.  Aborting."; exit 1; }

if [ -z "$1" ];then
    echo "The project name is empty. [Chart, Lang, Time, Mockito, Closure, Math]"
    exit 1;
elif [ -z "$2" ];then
    echo "The bug number is empty. Use 0 to run all bugs, use a number (e.g. 5) to minimize the bug 5 or use a list of numbers (e.g. 1,3,5,10)"
    exit 1;
fi

PROJECT=$1 # project name
BUGS=$2 # bugs
BASEPATH=$(pwd)

for BUG in $(seq 1 $BUGS); do
    gen_inputs=$(python3 generate_expected_msg.py --project "$PROJECT" --bugnumber "$BUG")
    if [[ $gen_inputs == *"FAILED"* ]]; then
        exit 1;
    fi
    echo "Bug $BUG - $PROJECT. Process finished."
done

