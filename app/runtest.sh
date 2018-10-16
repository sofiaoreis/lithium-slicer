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
EXPECTED=$3 #e.g. junit.... expected <0> but was <1>

####################
# run the test case
####################
defects4j compile -w ${PROJECTDIR} 2>/dev/null
defects4j test -t $TESTCASE -w ${PROJECTDIR} 2>/dev/null

# compare output message with expected message
python3 compare_messages.py "$EXPECTED" "${PROJECTDIR}/failing_tests"

# remove build directories
rm -rf ${PROJECTDIR}/build
rm -rf ${PROJECTDIR}/build-tests