import sys, os
from utils import check_obj_comparison, is_object_comparison

expected = sys.argv[1] # message expected got from JSON
output_filepath = sys.argv[2] # "failing_test" file that contains the test output after run d4j-test

debug = False # true to check expected and output messages in console (need to set debug=True in compile_run as well)

if os.path.isfile(output_filepath):
    output = None
    with open(output_filepath) as out:
        failing_tests = out.readlines()
        # print buggy_line in TestName.java
        buggy_line = [line for line in failing_tests if 'Tests.java' in line]
        try:
            # should print this line to check if there is the same buggy line
            print("[Buggy_START]{}[Buggy_END]".format(buggy_line[0].strip()))
        except:
            pass
        output = [line.strip() for line in failing_tests if not line.startswith('---') and not line.startswith('\t')]
        output = ''.join(output)

    # removes the "project_path/failing_tests" file
    os.remove(output_filepath)

    if debug:
        print("expected:", expected)
        print("got:", output)
    
    if is_object_comparison(expected):
        print("GOOD" if check_obj_comparison(expected, output) else "BAD")
    else:
        # should print GOOD or BAD in console
        print("GOOD" if (expected == output) else "BAD")
