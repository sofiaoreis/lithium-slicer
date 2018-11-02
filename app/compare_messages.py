import sys, os, logging
from utils import check_obj_comparison, is_object_comparison, get_testname_expected_msg, get_to_compare
import re

expected_msg_path = sys.argv[1] # "message expected" file path
output_filepath = sys.argv[2] # "failing_test" file that contains the test output after run d4j-test
testname = sys.argv[3] # test name

debug = False # true to check expected and output messages in console (need to set debug=True in interesting.py as well)
logger = logging.getLogger(__name__)

if os.path.isfile(expected_msg_path):
    with open(expected_msg_path) as out_exp:
        expected = out_exp.readlines()
        expected_tests = get_testname_expected_msg(testname, expected)[1::]
        expected_to_cmp, _ = get_to_compare(expected_tests)
        expected_to_cmp = ' '.join(expected_to_cmp)

if os.path.isfile(output_filepath):
    output_to_cmp = None
    with open(output_filepath) as out_fail:
        failing = out_fail.readlines()
        failing_tests = get_testname_expected_msg(testname, failing)[1::]
        if len(failing_tests) > 0:
            output_to_cmp, buggy_line = get_to_compare(failing_tests)
            output_to_cmp = ' '.join(output_to_cmp)

    try:
        # should print this line to check if there is the same buggy line
        print("[Buggy_START]{}[Buggy_END]".format(buggy_line))
    except:
        pass

    # removes the "project_path/failing_tests" file
    os.remove(output_filepath)

    if debug:
        logger.debug("expected: {}\ngot: {}".format(expected_to_cmp, output_to_cmp))

    if is_object_comparison(expected_to_cmp):
        print("GOOD" if check_obj_comparison(expected_to_cmp, output_to_cmp) else "BAD")
    else:
        # should print GOOD or BAD in console
        #print("expected: ", expected_to_cmp, "got: ", output_to_cmp)
        print("GOOD" if (expected_to_cmp == output_to_cmp) else "BAD")
