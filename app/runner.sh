#!/bin/bash

# check if defects4j is installed
command -v defects4j >/dev/null 2>&1 || { echo >&2 "defects4j not found.  Aborting."; exit 1; }

if [ -z "$1" ];then
    echo "The project name is empty. [Chart, Lang, Time, Mockito, Closure, Math]"
    exit 1;
elif [ -z "$2" ];then
    echo "The bug number is empty. Use 0 to run all bugs, use a number (e.g. 5) to minimize the bug 5 or use a list of numbers (e.g. 1,3,5,10)"
    exit 1;
elif [ -z "$3" ];then
    echo "The top-number is empty. Use an integer."
    exit 1;
fi

PROJECT=$1 # project name
BUG=$2 # bugs
TOP=$3 # k from top-k
TESTS=$4
BASEPATH=$(pwd)

INPUTS="inputs-${PROJECT}_${BUG}_${TOP}" # data filename

# generates a document that contains the inputs to run the minimizer
gen_inputs=$(python3 generate_inputs.py --project "$PROJECT" --output "$INPUTS" --bugnumber "$BUG" --files_per_bug "$TOP" --tests "$TESTS")
if [[ $gen_inputs == *"FAILED"* ]]; then
    echo 'failed'
    exit 1;
fi

TESTNAME=$(grep "^---"  source/${PROJECT}_${BUG}/run_tests | cut -f2 -d' ')

# this while can be deleted I think
while read line; do
    BUGNUMBER=$(echo $line | cut -f2 -d " ")
    CLASSES=$(echo $line | cut -f3 -d " ")
    STATES_PATH=$(echo $line | cut -f4 -d " ")

    #run defects4j and lithium
    python3 run_lithium.py --project $PROJECT \
    --bug_number $BUGNUMBER \
	--testname $TESTNAME \
    --classes $CLASSES \
    --states_path $STATES_PATH \
    --top $TOP

done < "$BASEPATH/$INPUTS"

rm $BASEPATH/$INPUTS

echo "Bug $BUG from $PROJECT minimized. Process finished."