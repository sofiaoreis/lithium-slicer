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
runtest_script = "./runtest {PROJECTDIR} {TESTCASE} '{EXPECTED}'"
timeout_seconds = 60
first_run = True
buggy_content = {"line_content": None, "function": None, "class": None}

def interesting(conditionArgs, prefix):
    global first_run
    global buggy_content

    project_dir = conditionArgs[0]
    testcase = conditionArgs[1]
    expected = conditionArgs[2]
    source_file = conditionArgs[3] # not used yet
    
    cmd_str = runtest_script.format(PROJECTDIR=project_dir, TESTCASE=testcase, EXPECTED=expected)

    output = call_cmd(cmd_str) # call shell script

    is_interesting = "GOOD" in output   
    if is_interesting:
        # copy the interesting file to this path
        name = os.path.basename(conditionArgs[-1])
        copy(conditionArgs[-1], name)
        print("### GOOD")

    return is_interesting

def get_buggy_content():
    """ line content + function + class """
    pass

@timeout(timeout_seconds) # 60s at most
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