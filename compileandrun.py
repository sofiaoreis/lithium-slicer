import os, signal

from subprocess import STDOUT, check_output, CalledProcessError
from shlex import split
from os import linesep, path
from timeout_decorator import timeout, TimeoutError

''' 

Lithium requires a module that defines an interesting function, which
returns true if the input is interesting and false if not
interesting. The script that does that for us is compile-and-run
(note the .sh extension), which just compiles the code and re-runs the
test.
'''

runtest_script="./runtest {FILENAME} {FILEDIR} {TESTCASE}"
timeout_seconds=3
DEBUG=False

def interesting(conditionArgs, prefix):
    if DEBUG:
        print(conditionArgs)
    ## passed as param through the "s" script
    source_dir = conditionArgs[0]
    testcase = conditionArgs[1]
    source_file = conditionArgs[2]

    if (not path.isdir(source_dir)):
        raise Exception("cannot find this path!", source_dir)

    cmd_str = runtest_script.format(FILENAME=source_file, FILEDIR=source_dir, TESTCASE=testcase)
    str = call_cmd(cmd_str) # call shell script

    if DEBUG:
        print(str)
    
    return 'GOOD' in str


@timeout(timeout_seconds) # 1s at most
def call_cmd(cmd_line):

    if DEBUG:
        print(cmd_line)
    
    cmd = split(cmd_line)
    msg = ''
    try:
        msg = check_output(cmd, stderr=STDOUT).decode('utf-8')
    except TimeoutError as e:
        ## close java processes
        process = os.popen('ps -u') # | awk \'{print $2}\'
        msg = process.read()
        process.close()
        for str in msg.splitlines():
            if "java -cp" in str:
                pid = str.split()[1]
                os.kill(int(pid), signal.SIGKILL)
        msg = 'Error: TIMEOUT'        
    except CalledProcessError as errorExc:
        msg = errorExc.output.decode('utf-8')
    return msg

# please, be aware that this fragment's purpose is to assist debugging. 
# this script is to be called from lithium. the function interesting will
# be called from the lithium loop several times. so, run this as script
# only to understand what this script is doing. It compile a potentially 
# modified version of the original code (source_file) and runs a test to 
# check if this modified version is acceptable, i.e., it still satisfies
# the (general) oracle string passed as parameter
if __name__ == "__main__":
    str = interesting(None, None)
    print(str)
