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

def interesting(conditionArgs, prefix):    
    project_dir = conditionArgs[0]
    testcase = conditionArgs[1]
    expected = conditionArgs[2]
    
    cmd_str = runtest_script.format(PROJECTDIR=project_dir, TESTCASE=testcase, EXPECTED=expected)

    str = call_cmd(cmd_str) # call shell script
    if "BUILD FAILED" in str:
        print("BUILD FAILED")
    elif 'GOOD' in str:
        # copy the interesting file to this path
        # to check the last interesting file
        name = os.path.basename(conditionArgs[-1])
        copy(conditionArgs[-1], name)
    
    return 'GOOD' in str

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