#! /usr/bin/python3
import argparse, os, tempfile
from utils import json_to_dict, get_testname_expected_msg, call_cmd
from shutil import rmtree


main = argparse.ArgumentParser()
main.add_argument("--project", type=str, nargs=1, help="Project name", required=True)
main.add_argument("--bugnumber", type=str, nargs=1, default="0", help="Number that represent a Bug in Project") # 0 corresponde to all
main.add_argument("--debug", action='store_true', help='print debug messages')

args = main.parse_args()
project_name = args.project[0]
bugs = args.bugnumber[0]

def is_input_number_valid(bug_numbers, project_data_path):
    """ check if a bug number exists in Project data directory """
    if "0" not in bug_numbers:
        json_files = os.listdir(project_data_path)
        for bug in bug_numbers:
            if "{}.json".format(bug) not in json_files:
                return False
    return True

def get_source_path(project_name):
    """ each project contains differents java_path """
    paths = {
        "Chart": "source",
        "Closure": "src",
        "Lang": "src/java",
        "Lang2": "src/main/java",
        "Math": "src/main/java",
        "Math2": "src/java",
        "Mockito": "src",
        "Time": "src/main/java"
    }

    return paths[project_name]

def generate_seed(project, bugnumber, debug):
    """ generates a file that contains json info to run d4j and lithium """
    initial_projects = ["Chart", "Lang", "Closure", "Math", "Mockito", "Time"]
    if project not in initial_projects:
        raise Exception("Project {} invalid. Please select one of {}".format(project, initial_projects))

    project_path = os.path.join(os.getcwd(), "data", project)

    if not os.path.isdir(project_path):
        print("FAILED") # should print to stop the main script
        raise Exception("Project {} directory not found".format(project_path))
    
    # Solves the issue of different source paths for the same project
    if project == 'Lang' and int(bugnumber) < 36:
        source_path = get_source_path(project+'2')
    elif project == 'Math' and int(bugnumber) > 84:
        source_path = get_source_path(project+'2')
    else:
        source_path = get_source_path(project)

    # get only bugs choosen by user
    bugnumber = bugnumber.split(",")
    
    if not is_input_number_valid(bugnumber, project_path):
        print("FAILED") # should print to stop the main script
        raise Exception("one or more json files({}) are not found in path {}".format(bugnumber, project_path))

    bugnumbers = ['{}.json'.format(bug) for bug in bugnumber]
    
    if '0' in bugnumber: # 0 similar to "all" bugs
        bugnumbers = os.listdir(project_path)
    else:
        bugnumbers = [doc for doc in os.listdir(project_path) if doc in bugnumbers]
    print(bugnumbers)
    # for each bug
    for bug in bugnumbers:
            data = json_to_dict(os.path.join(project_path, bug))
            bug_number = bug.replace(".json", "")

            # getting the expected message
            expected_dir = 'oracle/'+project_name+'/'
            if not os.path.exists(expected_dir):
                os.makedirs(expected_dir)
            
            expected_msg_path = expected_dir+bug_number
            project_dir = tempfile.mkdtemp(prefix="lithium-slicer_")
            output_filepath = project_dir+'/failing_tests'
            
            runtest_script = "bash run_input_test.sh {PROJECTDIR} {PROJECT} {BUG}"
            cmd_str = runtest_script.format(PROJECTDIR=project_dir, PROJECT=project_name, BUG=bug_number+'b')
            if debug: print(f"running {cmd_str}...")
            output = call_cmd(cmd_str) # call shell script
            if debug: print(output)
            
            if os.path.isfile(output_filepath):
                    with open(output_filepath) as out_fail:
                        failing = out_fail.readlines()
            if debug: print(f"test case message:\n{''.join(failing)}")

            with open(expected_msg_path,"w+") as expected:
                expected.write(
                    f"{''.join(failing)}"
                )
                
            # removing temporary folder
            if debug: print(f"removing {project_dir}...")
            rmtree(project_dir, ignore_errors=True)
            print(f"Test case expected message stored at {expected_msg_path}")

generate_seed(project_name, bugs, args.debug)

