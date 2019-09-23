#! /usr/bin/python3
import os, signal, time, logging
from shutil import copy

from subprocess import STDOUT, CalledProcessError, check_output
from shlex import split
from timeout_decorator import timeout, TimeoutError
from shutil import copytree


'''
Lithium requires a module that defines an interesting function, which
returns true if the input is interesting and false if not
interesting. The script that does that for us is compile-and-run
(note the .sh extension), which just compiles the code and re-runs the
test.
'''
runtest_script = "./runtest.sh {PROJECTDIR} {STATES} {TESTNAME} {SOURCE}"
timeout_seconds = 60
buggy_line = None
debug = True # True to check output in console

def interesting(conditionArgs, prefix):
    """ This function check if the file is interesting to reduce """
    global buggy_line
    global debug

    project_dir = conditionArgs[0]
    states_path = conditionArgs[1]
    testname = conditionArgs[2]
    source_file = conditionArgs[3]
    
    file_basename = os.path.basename(source_file).replace('.java', '')
    cmd_str = runtest_script.format(PROJECTDIR=project_dir, STATES=states_path, TESTNAME=testname, SOURCE=file_basename)
    output = call_cmd(cmd_str) # call shell script
        
    if debug:
        print('\n-----------------------------------')
        print('Output of calling runtest.sh:\n{}'.format(output))
    
    is_interesting = "BAD" not in output and "GOOD" in output

    if debug:
        print('is_interesting=', is_interesting)
        print('-----------------------------------')
    
        
    return is_interesting 

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