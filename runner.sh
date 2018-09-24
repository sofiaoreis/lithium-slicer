#!/bin/bash

PROJECTS="projects"
JSONFILES="json_files"
RESULTS="experiments"
BASEPATH=$(pwd)
FILENAME="config.txt"
TMPFOLDER="/tmp/slicer"
CP="cp.txt"

mkdir -p $RESULTS
mkdir -p $TMPFOLDER

for project in $(ls ${JSONFILES}); do
    tests=($(find $(pwd)/$JSONFILES/$project -path "*.json"))
    for test in ${tests[*]};do
        # generates a configuration file that includes
        # number of bug, test class/name and java file
        python load_json.py $test
        while read line; do
            bugnumber=$(echo $line | cut -f1 -d " ") # get bugnumber
            TESTCASE=$(echo $line | cut -f2 -d " ")
            FILEDIR=$(echo $line | cut -f3 -d " ")
            FILE=$(echo $line | cut -f4 -d " ")

            bugnumber+="b" # buggy version
            projectdir="$TMPFOLDER/$project"
            projectdir+="_"
            projectdir+="$bugnumber"
                        
            # compilation step TODO
            # defects4j checkout -p $project -v $bugnumber -w $projectdir
            # cd $projectdir && defects4j compile

            # backup original file
            JAVA_DIRPATH=$projectdir/"src/java"/${FILEDIR}
            (cd $JAVA_DIRPATH;
                cp $FILE $FILE.orig
            )

            # copy file to slice
            cp $JAVA_DIRPATH/${FILE} .

            # run lithium
            python -m lithium compileandrun ${JAVA_DIRPATH} ${TESTCASE} ${projectdir} ${FILE} # file needs to be the last (lithium requirement)

            # recover original file
            (cd $JAVA_DIRPATH;
                cp $FILE $FILE.lithium
                mv $FILE.orig $FILE
            )

            python3 diff_parser.py --origin ${FILEDIR}/${FILE} --minimized ${FILEDIR}/${FILE}.lithium --output ${FILE}.json

        done < $BASEPATH/$FILENAME
    done
done

rm -rf tmp*