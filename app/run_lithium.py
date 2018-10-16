import os, json, logging, time, argparse, tempfile
from shutil import copy, rmtree
from subprocess import STDOUT, CalledProcessError, check_output, call
from shlex import split
from utils import parse_comments, get_locs, get_relative_path, checkout_project

# args
main = argparse.ArgumentParser()
main.add_argument("--project", nargs=1, type=str)
main.add_argument("--bug_number", nargs=1, type=str)
main.add_argument("--test_case", nargs=1, type=str)
main.add_argument("--classes", nargs=1, type=str)
main.add_argument("--expected_message", nargs='+', type=str)

args = main.parse_args()

project = args.project[0]
bug_number = args.bug_number[0]
test_case = args.test_case[0]
classes = args.classes[0]
expected_arg = args.expected_message[0:]

# temporary directories
base_path = os.getcwd()
log_dir = os.path.join(base_path, 'logs', '{}_{}'.format(project, bug_number), '{}'.format(bug_number))

# directories in /tmp
project_dir = tempfile.mkdtemp(prefix="lithium-slicer_") # remove it later
lithium_tmp = tempfile.mkdtemp(prefix="lithium-interesting_") # remove it later

# this 'b' char corresponds to buggy version
bug_number += "b" 
# converts "classes" argument to a list of classes
classes = [os.path.join(project_dir, x) for x in classes.split(",")]
# converts expected_arg list to string
expected_message = ' '.join(expected_arg)
# renaming test case
testcase_name = test_case.replace("::", "_").split(".")[-1]

# if remove_comments == True, the comments/javadoc in original file are removed (otimization)
#! FIX THIS: if true, the function (utils.get_loc) does not works as expected (empty array)
remove_comments = False 

# create log_testcase directory
log_testcase_dir = os.path.join(log_dir, testcase_name)
os.makedirs(log_testcase_dir, exist_ok=True)

# logging settings
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_filename = "lithium-slicer-{}.log".format(time.asctime())
log_path = os.path.join(log_dir, log_filename)
handler = logging.FileHandler(log_path)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# starting lithium-slicer
logger.info("Started Lithium-Slicer")
logger.info("Running testcase {} from {}-{}b".format(project, bug_number, testcase_name))

init_time = time.time()
data = {"slicer":[]}
for java_file in classes:
    logger.info("Trying to reduce {} file".format(java_file))
    
    # checkout and compile project
    checkout_project(project, bug_number, project_dir)

    # create tmp directories if necessary
    os.makedirs(lithium_tmp, exist_ok=True)
    os.makedirs(project_dir, exist_ok=True)

    # saves original file in log_dir
    origin_filename = os.path.basename(java_file)
    origin_path = os.path.join(log_testcase_dir, origin_filename)
    copy(java_file, origin_path)
    
    # remove comments in original file
    if remove_comments:
        uncomment_path = os.path.join(log_testcase_dir, "uncomment_" + origin_filename)
        parse_comments(java_file, uncomment_path)
        copy(uncomment_path, java_file) # overwrite original java class

    # run lithium
    start_lithium = time.time()
    cmd_line = "python3 -m lithium --tempdir={TEMPDIR} interesting {PROJECTDIR} {TESTCASE} '{EXPECTED}' {FILE}"
    cmd_line = cmd_line.format(TEMPDIR=lithium_tmp, PROJECTDIR=project_dir, TESTCASE=test_case, FILE=java_file, EXPECTED=expected_message)
    call(split(cmd_line), stderr=STDOUT)
    
    # copy minimized file
    minimized_filename = "lithium_" + os.path.basename(java_file)
    minimized_path = os.path.join(log_testcase_dir, minimized_filename)
    copy(java_file, minimized_path)

    # append obj to data
    obj = {}
    obj["class"] = get_relative_path(project, java_file)
    obj["loc"] = get_locs(origin_path, minimized_path)
    data["slicer"].append(obj)

    est_time = int((time.time() - start_lithium)/60.0)
    logger.info("The file {} was minimized in {} minutes".format(java_file, est_time))

    # remove tmp directories
    rmtree(lithium_tmp, ignore_errors=True)
    rmtree(project_dir, ignore_errors=True)

# generate slicer-testcase.json
testcase_fmt = test_case.split("::")[-1]
slicer_name = "slicer-{}.json".format(testcase_fmt)
json_filename = os.path.join(log_testcase_dir, slicer_name)
with open(json_filename, 'w') as doc:
    json.dump(data, doc, indent=4)

total_time = int((time.time() - init_time)/60.0)
logger.info("The testcase {} was finished in {} minutes".format(testcase_name, total_time))