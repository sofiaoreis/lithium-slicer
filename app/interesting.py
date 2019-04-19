#! /usr/bin/python3
import os, signal, time, logging
from shutil import copy

from subprocess import STDOUT, CalledProcessError, check_output
from shlex import split
from timeout_decorator import timeout, TimeoutError

'''
Lithium requires a module that defines an interesting function, which
returns true if the input is interesting and false if not
interesting. The script that does that for us is compile-and-run
(note the .sh extension), which just compiles the code and re-runs the
test.
'''
runtest_script = "./runtest.sh {PROJECTDIR} {TESTCASE} {EXPECTED} {SOURCE}"
timeout_seconds = 120
buggy_line = None
debug = True # True to check output in console

def interesting(conditionArgs, prefix):
    """ This function check if the file is interesting to reduce """
    global buggy_line
    global debug

    project_dir = conditionArgs[0]
    testcase = conditionArgs[1]
    expected = conditionArgs[2]
    source_file = conditionArgs[3]
    
    print('Running test...')
    file_basename = os.path.basename(source_file).replace('.java', '')
    cmd_str = runtest_script.format(PROJECTDIR=project_dir, TESTCASE=testcase, EXPECTED=expected, SOURCE=file_basename)
    output = call_cmd(cmd_str) # call shell script
    
    if debug:
        print('Output of calling runtest.sh', output)

    is_interesting = "GOOD" in output

    if debug:
        print('is_interesting=', is_interesting)
    
    if (buggy_line is None) and is_interesting:
        buggy_line = get_buggy_line(output)
    
    # double check comparison with buggy_line and expected/output message
    if debug:
        print('double_check outcome ', is_interesting and (buggy_line in output))
    return is_interesting and (buggy_line in output)

def get_buggy_line(output):
    """ get buggy line in test file """
    # in first iteration, update buggy_line with the line that fail in original test
    start, end = output.index('[Buggy_START]'), output.index('[Buggy_END]')
    buggy_line = output[start+13:end].strip() # get text between [Buggy_START] and [Buggy_END] labels
    return buggy_line

@timeout(timeout_seconds) # 60s at most (compile and run test)
def call_cmd(cmd_line):
    cmd = split(cmd_line)
    msg = ''
    try:
        msg = check_output(cmd, stderr=STDOUT).decode('utf-8')
    except TimeoutError as e:
        msg = 'Error: TIMEOUT'
    except CalledProcessError as errorExc:
        msg = errorExc.output.decode('utf-8')
    return msg