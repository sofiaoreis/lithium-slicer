import os, sys, json, logging, time
from shutil import copy, rmtree
from subprocess import STDOUT, CalledProcessError, check_output, call
from shlex import split
from utils import parse_comments, get_locs, get_relative_path, checkout_and_compile

line = sys.argv[1]
lithium_tmp = sys.argv[2]
project_dir = sys.argv[3]
backup_dir = sys.argv[4]

project = line.split(" ")[0]
bug_number = line.split(" ")[1] + "b" # buggy version
testcase = line.split(" ")[2]
expected = line[line.index("*")+1:] # TODO: check for better pattern
classes = [os.path.join(project_dir, x) for x in line.split(" ")[3].split(",")]

testcase_name = testcase.replace("::", "_").split(".")[-1]

# if remove_comments == True, the comments/javadoc in original file are removed (otimization)
#! FIX THIS: if true, the function (utils.get_loc) does not works as expected (empty array)
remove_comments = False 

data = {"slicer":[]}

# create debug-testcase directory
debug_testcase_dir = os.path.join(backup_dir, testcase_name)
os.makedirs(debug_testcase_dir, exist_ok=True)

# log settings
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_filename = "lithium-slicer-{}.log".format(time.asctime())
log_path = os.path.join(backup_dir, log_filename)
handler = logging.FileHandler(log_path)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info("Started Lithium-Slicer")
logger.info("Running {}-{}".format(project, bug_number))
for java_file in classes:
    logger.info("Trying to reduce {} file".format(java_file))
    
    # checkout and compile project
    checkout_and_compile(project, bug_number, project_dir)

    # create tmp directories if necessary
    os.makedirs(lithium_tmp, exist_ok=True)
    os.makedirs(project_dir, exist_ok=True)

    # saves original file in backup_dir
    origin_filename = os.path.basename(java_file)
    origin_path = os.path.join(debug_testcase_dir, origin_filename)
    copy(java_file, origin_path)
    
    # remove comments in original file
    if remove_comments:
        uncomment_path = os.path.join(debug_testcase_dir, "uncomment_" + origin_filename)
        parse_comments(java_file, uncomment_path)
        copy(uncomment_path, java_file) # overwrite original java class

    # run lithium
    cmd_line = "python3 -m lithium --tempdir={TEMPDIR} compile_run {PROJECTDIR} {TESTCASE} '{EXPECTED}' {FILE}".format(TEMPDIR=lithium_tmp, PROJECTDIR=project_dir, TESTCASE=testcase, FILE=java_file, EXPECTED=expected)
    call(split(cmd_line), stderr=STDOUT)
    
    # copy minimized file
    minimized_filename = "lithium_" + os.path.basename(java_file)
    minimized_path = os.path.join(debug_testcase_dir, minimized_filename)
    copy(java_file, minimized_path)

    # append obj to data
    obj = {}
    obj["class"] = get_relative_path(project, java_file)
    obj["loc"] = get_locs(origin_path, minimized_path)
    data["slicer"].append(obj)

    # remove tmp directories
    rmtree(lithium_tmp, ignore_errors=True)
    rmtree(project_dir, ignore_errors=True)

# generate slicer-testcase.json
testcase_fmt = testcase.split("::")[-1]
slicer_name = "slicer-{}.json".format(testcase_fmt)
json_filename = os.path.join(debug_testcase_dir, slicer_name)
with open(json_filename, 'w') as doc:
    json.dump(data, doc, indent=4)
