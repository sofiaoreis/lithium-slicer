#! /usr/bin/python3
import os, logging, time, argparse, tempfile, sys
from shutil import copy, rmtree
import subprocess
from subprocess import STDOUT, CalledProcessError, check_output, call
from shlex import split
from utils import parse_comments, get_locs, get_relative_path, checkout_project, create_json
import platform
from distutils.dir_util import copy_tree

# args
main = argparse.ArgumentParser()
main.add_argument("--project", nargs=1, type=str)
main.add_argument("--bug_number", nargs=1, type=str)
main.add_argument("--test_case", nargs=1, type=str)
main.add_argument("--classes", nargs=1, type=str)
main.add_argument("--expected_msg_path", nargs=1, type=str)
main.add_argument("--top", nargs=1, type=str)
main.add_argument("--objectname", nargs=1, type=str)
main.add_argument("--statement", nargs=1, type=str)
main.add_argument("--objects", nargs=1, type=str)

args = main.parse_args()

project = args.project[0]
bug_number = args.bug_number[0]
test_case = args.test_case[0]
classes = args.classes[0]
expected_msg_path = args.expected_msg_path[0]
top = args.top[0]
objectname = args.objectname[0]
statement = args.statement[0]
objects = args.objects[0]

# temporary directories
base_path = os.getcwd()
log_dir = os.path.join(base_path, 'logs_{}'.format(top),'{}_{}'.format(project, bug_number), '{}_{}'.format(statement, objects))

# this 'b' char corresponds to buggy version
bug_number += "b" 
# converts "classes" argument to a list of classes
classes = classes.split(",")
# renaming test case
testcase_name = test_case.split(".")[-1].replace("::", ".")

# if remove_comments == True, the comments/javadoc in original file are removed (otimization)
# BUG @TODO: if true, the function (utils.get_loc) does not works as expected (empty array)
remove_comments = True 
uncomment_path = None

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
    global project, bug_number, test_case, expected_msg_path, statement, objectname
    output_lithium = {} # structute to store the output of lithium
    
    # /tmp directories
    project_dir = tempfile.mkdtemp(prefix="lithium-slicer_")
    lithium_tmp = tempfile.mkdtemp(prefix="lithium-interesting_")

    # checkout the project - @TODO: not necessary anymore
    # checkout_project(project, bug_number, project_dir)
    copy_tree('/Users/fifaz/Documents/submissions/icse_20/source/{}_{}_{}_{}/'.format(project, bug_number.replace('b',''), statement, objects), project_dir)

    # update filepath path
    java_file = os.path.join(project_dir, filepath)
    filename = os.path.basename(java_file)

    logger.info("Minimizing {filename}".format(filename=filename))

    # saves original file in log_dir
    origin_filename = os.path.basename(java_file)
    origin_path = os.path.join(log_testcase_dir, origin_filename)
    copy(java_file, origin_path)
    
    object_path = os.path.join(project_dir,'oracles','{}.xml'.format(objectname))
    print(object_path)
    

    # remove comments in original file
    if remove_comments:
        logger.info("Removing comments for {filename}".format(filename=filename))
        uncomment_path = os.path.join(log_testcase_dir, "uncomment_" + origin_filename)
        if platform.system() == 'Darwin':
            bash_cmd = '/usr/libexec/java_home -v 1.8 --exec java -cp java-parser-comments-remover-1.0-SNAPSHOT-jar-with-dependencies.jar com.tqrg.cleaner.Cleaner ' + java_file + ' ' + uncomment_path
        elif platform.system() == 'Linux':
            bash_cmd = '/usr/lib/jvm/java-8-oracle/bin/java -cp java-parser-comments-remover-1.0-SNAPSHOT-jar-with-dependencies.jar com.tqrg.cleaner.Cleaner ' + java_file + ' ' + uncomment_path
        process = subprocess.Popen(bash_cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        copy(uncomment_path, java_file)
        logger.info("Removing comments was finished for {filename}".format(filename=filename))
    

    # run lithium
    try:
        start_lithium = time.time()
        cmd_line = "python3 -m lithium --tempdir={TEMPDIR} interesting {PROJECTDIR} {TESTCASE} {EXPECTED_MSG_PATH} {OBJECTPATH} {FILE}"
        
        cmd_line = cmd_line.format(TEMPDIR=lithium_tmp, PROJECTDIR=project_dir, TESTCASE=test_case, FILE=java_file, EXPECTED_MSG_PATH=expected_msg_path, OBJECTPATH=object_path)
        logger.info("Running lithium for {filename}".format(filename=filename))
        call(split(cmd_line), stderr=STDOUT)
        logger.info("Lithium was finished for {filename}".format(filename=filename))

        # copy minimized file
        logger.info("Copying minimized file to {log_dir}".format(log_dir=log_dir))
        minimized_filename = "lithium_" + filename
        minimized_path = os.path.join(log_testcase_dir, minimized_filename)
        copy(java_file, minimized_path)

        # update 
        output_lithium["class"] = get_relative_path(project, java_file, args.bug_number[0])
        output_lithium["loc"] = get_locs(origin_path, minimized_path) if not remove_comments else get_locs(uncomment_path, minimized_path)

        est_time = int((time.time() - start_lithium)/60.0)
        logger.info("The file {filename} was minimized in {time} minutes".format(filename=filename, time=est_time))
    except Exception as e:
        raise Exception("Something happens {}".format(e.message))
    finally:
        # remove tmp directories
        rmtree(lithium_tmp, ignore_errors=True)
        rmtree(project_dir, ignore_errors=True)

    return output_lithium


for _class in classes:
    try:
        result = minimize_file(_class)
        data["slicer"].append(result)
    except Exception as e:
        logger.error("{}".format(e))
        raise Exception("Minimization was failed. \n{}".format(e))

# generate slicer-testcase.json
testcase_fmt = test_case.split("::")[-1]
slicer_name = "slicer-{}.json".format(testcase_fmt)
json_path = os.path.join(log_testcase_dir, slicer_name)

# export data to a JSON file 
create_json(json_path, data)

total_time = int((time.time() - init_time)/60.0)
logger.info("The testcase {test_case} was finished in {time} minutes".format(test_case=testcase_name, time=total_time))