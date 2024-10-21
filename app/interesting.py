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
timeout_seconds = 120
buggy_line = None
debug = True # True to check output in console

def interesting(conditionArgs, prefix):
    """ This function check if the file is interesting to reduce """
    global buggy_line
    global debug
    project_dir, testcase, expected, logfile_path, horacle, source_file = conditionArgs
    
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler(logfile_path, mode='a')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)    
    logger.info(f"[🧪] Starting interesting check to access if the file is interesting to reduce...")

    file_basename = os.path.basename(source_file).replace('.java', '')
    runtest_script = f"./runtest.sh {project_dir} {testcase} {expected} {file_basename} {horacle}"
    logger.info(f"[🧪] Running {runtest_script}...")
    output = call_cmd(runtest_script) # call shell script
    # class is interesting to minimize if 
    # Expected and Lithium messages are equal
    is_interesting = "GOOD" in output

    logger.info(f"[🧪] Running new test case result: \n{output}")
    
    # if class is interesting to minimize
    # we want to get the buggy line in 
    # the new sliced test case 
    if is_interesting:
        testcase_line = get_testcase_line(output)
        logger.info(f"[🧪] Found buggy line [{testcase_line}]")            
    
    # double check comparison with testcase_line and expected/output message
    if debug:
        logger.info(f'[🧪] Class is interesting to minimize and original buggy line is on the new test case: {is_interesting and (testcase_line in output)}\n')
    
    # the minimization step is only accepted if 
    # the file is interested and the test case line
    # in the new test case is the same as in the 
    # original test case
    return is_interesting and (testcase_line in output)

def get_testcase_line(output):
    """ get test line in test file """
    # in first iteration, update test line with the line that fail in the original test
    start, end = output.index('[BS]'), output.index('[BE]')
    # get text between [BS] and [BE] labels
    return output[start+4:end].strip() 

@timeout(timeout_seconds) # 60s at most (compile and run test)
def call_cmd(cmd_line):
    cmd, msg = split(cmd_line), ''
    try:
        msg = check_output(cmd, stderr=STDOUT).decode('utf-8')
    except TimeoutError as e:
        msg = 'Error: TIMEOUT'
    except CalledProcessError as errorExc:
        msg = errorExc.output.decode('utf-8')
    return msg