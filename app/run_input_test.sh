#!/bin/bash
#####################################################################
# This script will:
#
# (1) run the failing test case 
# (2) check if the output matches the contents of file expected.txt
#####################################################################

# PARAMS
PROJECTDIR=$1 #e.g. /tmp/Lang_1b/
PROJECT=$2 #e.g. Lang
BUG=$3 #e.g. 1b

####################
# run the test case
####################
defects4j compile -w ${PROJECTDIR} 2>/dev/null
defects4j test -w ${PROJECTDIR} 2>/dev/null 
