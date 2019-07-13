#! /usr/bin/python3
import argparse, os
from utils import json_to_dict, get_testname_expected_msg, call_cmd

main = argparse.ArgumentParser()
main.add_argument("--output", type=str, nargs=1, help="The output path to save the seed file")
main.add_argument("--project", type=str, nargs=1, help="Project name")
main.add_argument("--bugnumber", type=str, nargs=1, default="0", help="Number that represent a Bug in Project") # 0 means all bugs
main.add_argument("--statements", type=str, nargs=1, default="10", help="Max quantity of statements per bug")

args = main.parse_args()
project_name = args.project[0]
bugs = args.bugnumber[0]
output = args.output[0]
statements = int(args.statements[0])

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

def generate_seed(project, bugnumber, output):
    """ generates a file that contains json info to run d4j and lithium """
    global statements
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
    
    with open(output, "w") as seed_file:
        # for each bug
        for bug in bugnumbers:
            data = json_to_dict(os.path.join(project_path, bug))
            bug_number = bug.replace(".json", "")
            classes = []
            # get rankings from morpho's report
            for item in data["rankings"][0:statements]:
                java_file = os.path.join(source_path, item["class"])
                if java_file not in classes:
                    classes.append(java_file)
                    
            # get the top-k classes
            if len(classes) > 1:
                classes = ",".join(classes) # converts [classA, classB] to classA,classB
            else:
                classes = classes[0] # get only line

            expected_dir = 'oracle/'+project_name+'/'
            expected_msg_path = expected_dir+bug_number

            i = 0; f = 0; c = 0;
            with open(expected_msg_path) as f:
                failing = f.readlines()
                for l in failing:
                    if '---' in l:
                        testcase = l.strip().split(' ')[1]
                        seed_file.write(
                                "{} {} {} {} {}\n".format(project, bug_number, testcase, classes, expected_msg_path)
                            )
                    
generate_seed(project_name, bugs, output)

