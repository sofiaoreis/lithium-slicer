#!/bin/bash
#####################################################################
# This script will:
#
# (1) run the failing test case 
# (2) check if the output matches the contents of file expected.txt
#####################################################################

# PARAMS
PROJECTDIR=$1 #e.g. /tmp/Lang_1b/
TESTCASE=$2 #e.g. org.jfree......Tests::test9999
PROJECT=$3 #e.g. Lang
BUG=$4 #e.g. 1b

####################
# run the test case
####################
defects4j checkout -p $PROJECT -v $BUG -w ${PROJECTDIR}
defects4j compile -w ${PROJECTDIR} 2>/dev/null
defects4j test -t $TESTCASE -w ${PROJECTDIR} 2>/dev/null
