#!/bin/bash
#####################################################################
# This script will:
#
# (1) run the failing test case 
# (2) check if the output matches the contents of file expected.txt
#####################################################################

# PARAMS
PROJECT_DIR=$1 #e.g. /var/folders/.../T/lithium-slicer_...
TESTCASE=$2 #e.g. org.jfree.chart.renderer.junit.GrayPaintScaleTests::testGetPaint
EXPECTED_MSG_PATH=$3 #e.g. chart_24_message
SOURCE=$4 # e.g. GrayPaintScale (without the java extensin)
HORACLE=$5 # e.g. 1 or 2

####################
# run the test case
####################
defects4j compile -w ${PROJECT_DIR} 2>/dev/null
defects4j test -t $TESTCASE -w ${PROJECT_DIR} 2>/dev/null

# compare output message with expected message
python3 compare_messages.py "$EXPECTED_MSG_PATH" "${PROJECT_DIR}/failing_tests" $TESTCASE $HORACLE

# !! @OPTIMIZATION: remove only the SOURCE class (cost less on re-build)
BUG_CLASS="$(find ${PROJECT_DIR} -name $SOURCE.class)"
rm $BUG_CLASS 2>/dev/null