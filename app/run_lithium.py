#! /usr/bin/python3
import os, logging, time, argparse, tempfile, sys
import subprocess
import platform
import threading

from subprocess import STDOUT, CalledProcessError, check_output, call
from shlex import split
from shutil import copy, rmtree
from colors import prGreen, prPurple, prLightPurple, prYellow
from utils import parse_comments, get_locs, get_relative_path, checkout_project, create_json
from interesting import call_cmd

def log_output(pipe):
    for line in iter(pipe.readline, b''):
        print(line.decode().rstrip())
    pipe.close()

def cut_classes(classes):
    # edge cases:
    # classes=[1, 2, 3, 4], top=3
    # classes=[1], top=3
    # classes=[1, 2, 3], top=3 
    return classes if len(classes) <= top else classes[0:top]

# args
main = argparse.ArgumentParser()
main.add_argument("--project", nargs=1, type=str)
main.add_argument("--bug_number", nargs=1, type=str)
main.add_argument("--test_case", nargs=1, type=str)
main.add_argument("--classes", nargs=1, type=str)
main.add_argument("--expected_msg_path", nargs=1, type=str)
main.add_argument("--top", nargs=1, type=str)
main.add_argument("--horacle", nargs=1, type=int)

args = main.parse_args()
project = args.project[0]
bug_number = args.bug_number[0]
test_case = args.test_case[0]
classes = args.classes[0]
expected_msg_path = args.expected_msg_path[0]
top = int(args.top[0])
horacle = args.horacle[0]

prGreen(f"Analyzing {project} {bug_number}\ntest_case={test_case}\nclasses={classes}\ntop: {top}\nexpected test message stored in {expected_msg_path}\nhoracle={horacle}")

# temporary directories
base_path = os.getcwd()
log_dir = os.path.join(base_path, 'logs_{}'.format(top), '{}_{}'.format(project, bug_number), '{}'.format(bug_number))
# this 'b' char corresponds to buggy version
bug_number += "b" 
# converts "classes" argument to a list of classes
classes = cut_classes(classes.split(","))
# renaming test case
testcase_name = test_case.split(".")[-1].replace("::", ".")


# if remove_comments == True, the comments/javadoc 
# in original file are removed (optimization)
# BUG @TODO: if true, the function (utils.get_loc) 
# does not work as expected (empty array) 
remove_comments, uncomment_path = True, None

# create log_testcase directory
log_testcase_dir = os.path.join(log_dir, testcase_name)
os.makedirs(log_testcase_dir, exist_ok=True)

# logging settings
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_filename = "log_{project}_{bug}_{time}.log".format(project=project, bug=bug_number, time=time.asctime().replace(' ', '_'))
log_path = os.path.join(log_dir, log_filename)
prGreen(f"log_path={log_path}\n")

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
    global project, bug_number, test_case, expected_msg_path, log_path
    
    output_lithium = {} # structute to store the output of lithium
    
    # /tmp directories
    project_dir = tempfile.mkdtemp(prefix="lithium-slicer_")
    lithium_tmp = tempfile.mkdtemp(prefix="lithium-interesting_")

    # checkout the project 
    prYellow(f"[⬇️ ] Checking out program {project} {bug_number}...")
    checkout_project(project, bug_number, project_dir)
    prYellow(f"[⬇️ ] Finished checking out program {project} {bug_number}!")

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
        if platform.system() == 'Darwin':
            bash_cmd = '/usr/libexec/java_home -v 1.8 --exec java -cp utils/java-parser-comments-remover-1.0-SNAPSHOT-jar-with-dependencies.jar com.tqrg.cleaner.Cleaner ' + java_file + ' ' + uncomment_path
        elif platform.system() == 'Linux':
            bash_cmd = '/usr/lib/jvm/java-8-oracle/bin/java -cp utils/java-parser-comments-remover-1.0-SNAPSHOT-jar-with-dependencies.jar com.tqrg.cleaner.Cleaner ' + java_file + ' ' + uncomment_path
        process = subprocess.Popen(bash_cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            print(error)
        copy(uncomment_path, java_file)
        logger.info(f"[🧹 task] Removed comments from {filename}. Cleaned class was copied to {uncomment_path}.")
        prYellow(f"[🧹] Removed comments from {filename}")


    # run lithium
    try:
        start_lithium = time.time()
        prYellow(f"\n[🔪] Starting Lithium...")
        logger.info(f"[🔪] Running lithium for {filename}...")
        logger.info(f"[🔪][config] --tempdir={lithium_tmp} interesting {project_dir} {test_case} {expected_msg_path} {log_path} {horacle} {java_file}")
        # --testcase and --tempdir are defined by our tool
        # --strategy = minimize (default), there are other strategies available
        # --max; default (half of the file)
        # --min; default (1)
        cmd_line = f"python3 -m lithium --tempdir={lithium_tmp} --testcase={java_file} interesting {project_dir} {test_case} {expected_msg_path} {log_path} {horacle} {java_file}"
        subprocess.run(cmd_line.split(' '), stdout=sys.stdout, stderr=sys.stderr)
        
        logger.info(f"[🔪] Lithium finished for {filename}")
        prYellow(f"[🔪] Finished running Lithium...")

        # copy minimized file
        print(f"\n[💬] Copying minimized file to {log_dir}...")
        minimized_filename = "lithium_" + filename
        minimized_path = os.path.join(log_testcase_dir, minimized_filename)
        copy(java_file, minimized_path)

        # update 
        output_lithium["class"] = get_relative_path(project, java_file, args.bug_number[0])
        output_lithium["loc"] = get_locs(origin_path, minimized_path) if not remove_comments else get_locs(uncomment_path, minimized_path)

        est_time = int((time.time() - start_lithium)/60.0)
        print("\n[🔪] The file {filename} was minimized in {time} minutes".format(filename=filename, time=est_time))

    except Exception as e:
        raise Exception("Something happened {}".format(e.message))
    finally:
        # remove tmp directories
        rmtree(lithium_tmp, ignore_errors=True)
        rmtree(project_dir, ignore_errors=True)

    return output_lithium


for _class in classes:
    try:
        prLightPurple(f"\nAttempting to minimize {_class}")
        result = minimize_file(_class)
        data["slicer"].append(result)
        prLightPurple(f"\nMinimization ended to {_class}")
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
logger.info("[✅ ] The testcase {test_case} was finished in {time} minutes".format(test_case=testcase_name, time=total_time))