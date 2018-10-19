import os, logging, time, argparse, tempfile
from shutil import copy, rmtree
from subprocess import STDOUT, CalledProcessError, check_output, call
from shlex import split
from utils import parse_comments, get_locs, get_relative_path, checkout_project, create_json
from multiprocessing import Pool, cpu_count

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

# this 'b' char corresponds to buggy version
bug_number += "b" 
# converts "classes" argument to a list of classes
classes = classes.split(",")
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
log_filename = "log-{project}-{bug}-{time}.log".format(project=project, bug=bug_number, time=time.asctime())
log_path = os.path.join(log_dir, log_filename)
handler = logging.FileHandler(log_path)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# starting lithium-slicer
logger.info("Started Lithium-Slicer")
logger.info("Running testcase {test_case} from {project}-{bug}".format(test_case=testcase_name, project=project, bug=bug_number))
logger.info("Files to minimize: {classes}".format(classes=[os.path.basename(_class) for _class in classes]))

init_time = time.time()
data = {"slicer":[]}

def minimize_file(filepath):
    """ This method runs lithium on a java source code and returns an 
        object that contains the filepath and the similar loc in the original file

        obj = {
            "class": ".../ClassA.java",
            "loc": [1,50,52,54,...]
        }
    """    
    global project, bug_number, test_case, expected_message
    output_lithium = {} # structute to store the output of lithium
    
    # /tmp directories
    project_dir = tempfile.mkdtemp(prefix="lithium-slicer_")
    lithium_tmp = tempfile.mkdtemp(prefix="lithium-interesting_")

    # checkout the project
    checkout_project(project, bug_number, project_dir)

    # update filepath path
    java_file = os.path.join(project_dir, filepath)
    filename = os.path.basename(java_file)

    logger.info("Minimizing {filename}".format(filename=filename))

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
    try:
        start_lithium = time.time()
        cmd_line = "python3 -m lithium --tempdir={TEMPDIR} interesting {PROJECTDIR} {TESTCASE} '{EXPECTED}' {FILE}"
        cmd_line = cmd_line.format(TEMPDIR=lithium_tmp, PROJECTDIR=project_dir, TESTCASE=test_case, FILE=java_file, EXPECTED=expected_message)
        
        logger.info("Running lithium for {filename}".format(filename=filename))
        call(split(cmd_line), stderr=STDOUT)
        logger.info("Lithium was finished for {filename}".format(filename=filename))

        # copy minimized file
        logger.info("Copying minimized file to {log_dir}".format(log_dir=log_dir))
        minimized_filename = "lithium_" + filename
        minimized_path = os.path.join(log_testcase_dir, minimized_filename)
        copy(java_file, minimized_path)

        # update 
        output_lithium["class"] = get_relative_path(project, java_file)
        output_lithium["loc"] = get_locs(origin_path, minimized_path)

        est_time = int((time.time() - start_lithium)/60.0)
        logger.info("The file {filename} was minimized in {time} minutes".format(filename=filename, time=est_time))
    except Exception as e:
        raise Exception("Something happens {}".format(e))
    finally:
        # remove tmp directories
        rmtree(lithium_tmp, ignore_errors=True)
        rmtree(project_dir, ignore_errors=True)

    return output_lithium

with Pool(processes=cpu_count()) as pool:
    # minimize all java classes in parallel
    try:
        result = pool.map(minimize_file, classes)
    except Exception as e:
        logger.error("{}".format(e.message))
        raise Exception("Minimization was failed. \n{}".format(e))

# append each minimized file with their locs
for obj in result:
    data["slicer"].append(obj)

# generate slicer-testcase.json
testcase_fmt = test_case.split("::")[-1]
slicer_name = "slicer-{}.json".format(testcase_fmt)
json_path = os.path.join(log_testcase_dir, slicer_name)

# export data to a JSON file 
create_json(json_path, data)

total_time = int((time.time() - init_time)/60.0)
logger.info("The testcase {test_case} was finished in {time} minutes".format(test_case=testcase_name, time=total_time))