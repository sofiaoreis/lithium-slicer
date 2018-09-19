#!/bin/bash

FILEDIR="some_project/src/main/java/example"
TESTCASE="example.BinarySearchTreeTest#deleteExisting"
FILE="BinarySearchTree.java"

# make sure lithium is installed
pip install lithium-reducer timeout_decorator

# compile the codebase
(cd some_project;
 mvn compile
 # save classpath in a file for running test cases outside maven (for speed)
 mvn dependency:build-classpath -Dmdep.outputFile=../cp.txt
)

# compile extra (e.g., single test runner)
CP=$(cat cp.txt)
(cd extra;
 javac -cp $CP *.java
)

# debug
#echo ${FILEDIR} ${TESTCASE} ${FILE} 

# backup original file
(cd ${FILEDIR};
 cp $FILE $FILE.orig
)

# copy file to slice
cp ${FILEDIR}/${FILE} .

## run lithium
python -m lithium compileandrun ${FILEDIR} ${TESTCASE} ${FILE} # file needs to be the last (lithium requirement)

# recover original file
(cd ${FILEDIR};
 mv $FILE.orig $FILE
)

# cleaning
rm -rf tmp*
rm cp.txt
