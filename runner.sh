#!/bin/bash

PROJECT=$1 # project arg (e.g. Lang or Chart or Mockito...)
BUG=$2 # run these bugs (e.g. 1 or 1,2,5,9 else will run all bugs)
BASEPATH=$(pwd) # workdir
SEEDS="seed_${PROJECT}_${BUG}" # seed filename
TMPFOLDER="/tmp/lithium-slicer" # tmp directory
LITHIUM_DIR="tmp_lithium_${PROJECT}_${BUG}" # local directory to save the lithium outputs

LOG_DIR="logs/${PROJECT}_${BUG}" # log directory
LOG_NAME="$LOG_DIR/$(date).txt" # log filename
DEBUG_DIR="$LOG_DIR/debug"

# create initial directories if necessary
mkdir -p $TMPFOLDER
mkdir -p $LITHIUM_DIR
mkdir -p $DEBUG_DIR

# generates a doc that contains info to run the projects
python3 gen_seed.py --project "$PROJECT" --output "$SEEDS" --bugnumber "$BUG"

while read line; do
    BUGNUMBER=$(echo $line | cut -f2 -d " ")
    TESTCASE=$(echo $line | cut -f3 -d " ")

    #! todo python logging (extra)
    echo "$(date) - running $PROJECT $BUG" >> "$LOG_NAME"
    echo "$(date) - running $TESTCASE" >> "$LOG_NAME"

    # update project dir name
    TMP_PROJECT="$TMPFOLDER/$PROJECT"
    TMP_PROJECT+="_"
    TMP_PROJECT+="$BUGNUMBER"
    
    # run defects4j and lithium
    python3 run_lithium.py "$line" $LITHIUM_DIR $TMP_PROJECT $DEBUG_DIR

    rm -rf $LITHIUM_DIR
    rm -rf $TMP_PROJECT
done < "$BASEPATH/$SEEDS"