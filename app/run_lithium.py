import os, sys, json, logging
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

data = {"slicer":[]}

# create debug-testcase directory
debug_testcase_dir = os.path.join(backup_dir, testcase_name)
os.makedirs(debug_testcase_dir, exist_ok=True)

for java_file in classes:
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
    uncomment_path = os.path.join(debug_testcase_dir, "uncomment_" + origin_filename)
    parse_comments(java_file, uncomment_path)
    copy(uncomment_path, java_file) # overwrite java_file

    # run lithium
    cmd_line = "python -m lithium --tempdir={TEMPDIR} compile_run {PROJECTDIR} {TESTCASE} '{EXPECTED}' {FILE}".format(TEMPDIR=lithium_tmp, PROJECTDIR=project_dir, TESTCASE=testcase, FILE=java_file, EXPECTED=expected)
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
testcase_fmt = testcase.format(testcase.split("::")[-1])
slicer_name = "slicer-{}.json".format(testcase_fmt)
with open(os.path.join(debug_testcase_dir, slicer_name)) as doc:
    json.dump(data, doc, indent=4)
