#!/bin/bash

command -v defects4j >/dev/null 2>&1 || { echo >&2 "defects4j not found.  Aborting."; exit 1; }

if [ -z "$1" ];then
    echo "The project name is empty. [Chart, Lang, Time, Mockito, Closure, Math]"
    exit 1;
elif [ -z "$2" ];then
    echo "The bug number is empty. Use 0 to run all bugs, use a number (e.g. 5) to minimize the bug 5 or use a list of numbers (e.g. 1,3,5,10)"
    exit 1;
fi

PROJECT=$1 # project arg (e.g. Lang or Chart or Mockito...)
BUG=$2 # run these bugs (e.g. 1 or 1,2,5,9 else will run all bugs)
BASEPATH=$(pwd) # workdir
SEEDS="seed_${PROJECT}_${BUG}" # seed filename
TMPFOLDER="/tmp/lithium-slicer" # tmp directory
LITHIUM_DIR="tmp_lithium_${PROJECT}_${BUG}" # local directory to save the lithium outputs

LOG_DIR="logs/${PROJECT}_${BUG}" # log directory
LOG_NAME="$LOG_DIR/$(date).txt" # log filename
DEBUG_DIR="$LOG_DIR"

# create initial directories if necessary
mkdir -p $TMPFOLDER
mkdir -p $LITHIUM_DIR
mkdir -p $DEBUG_DIR

# generates a doc that contains info to run the projects
gen_data=$(python3 generate_seed.py --project "$PROJECT" --output "$SEEDS" --bugnumber "$BUG" --files_per_bug 5)
if [[ $gen_data == *"FAILED"* ]]; then
    exit
fi

while read line; do
    BUGNUMBER=$(echo $line | cut -f2 -d " ")
    TESTCASE=$(echo $line | cut -f3 -d " ")

    RESULTS_DIR="$DEBUG_DIR/$BUGNUMBER"
    mkdir -p $RESULTS_DIR

    # update project dir name
    TMP_PROJECT="$TMPFOLDER/$PROJECT"
    TMP_PROJECT+="_"
    TMP_PROJECT+="$BUGNUMBER"
    
    # run defects4j and lithium
    python3 run_lithium.py "$line" $LITHIUM_DIR $TMP_PROJECT $RESULTS_DIR

    rm -rf $LITHIUM_DIR
    rm -rf $TMP_PROJECT
done < "$BASEPATH/$SEEDS"

rm $BASEPATH/$SEEDS