import argparse, os
from utils import json_to_dict

main = argparse.ArgumentParser()
main.add_argument("--output", type=str, nargs=1, help="The output path to save the seed file")
main.add_argument("--project", type=str, nargs=1, help="Project name")
main.add_argument("--bugnumber", type=str, nargs=1, default="0", help="Number that represent a Bug in Project") # 0 corresponde to all
main.add_argument("--files_per_bug", type=str, nargs=1, default="5", help="Max quantity of files per bug")


args = main.parse_args()
project_name = args.project[0]
bugs = args.bugnumber[0]
output = args.output[0]

max_files_per_bug = int(args.files_per_bug[0])

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
        "Math": "src/main/java",
        "Mockito": "src",
        "Time": "src/main/java"
    }

    return paths[project_name]

def generate_seed(project, bugnumber, output):
    """ generates a file that contains json info to run d4j and lithium """
    global max_files_per_bug
    initial_projects = ["Chart", "Lang", "Closure", "Math", "Mockito", "Time"]
    if project not in initial_projects:
        raise Exception("Project {} invalid. Please select one of {}".format(project, initial_projects))

    project_path = os.path.join(os.getcwd(), "data", project)

    if not os.path.isdir(project_path):
        print("FAILED") # should print to stop the main script
        raise Exception("Project {} directory not found".format(project_path))
    
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
        for bug in bugnumbers:
            data = json_to_dict(os.path.join(project_path, bug))
            bug_number = bug.replace(".json", "")
            classes = []
            for item in data["rankings"]:
                java_file = os.path.join(source_path, item["class"])
                if java_file not in classes:
                    classes.append(java_file)
                    if len(classes) == max_files_per_bug:
                        break

            if len(classes) > 1:
                classes = ",".join(classes) # converts [classA, classB] to classA,classB
            else:
                classes = classes[0] # get only line

            for fail in data["failing"]: # list of tests failing
                testcase = fail["test"]
                expected_msg = fail["error"]
                if len(expected_msg) > 1:
                    join_lines = ','.join([line.strip() for line in expected_msg])
                    expected_msg = "*" + join_lines
                else:
                    # TODO: add better pattern
                    # pattern to show the expected message begin(*)
                    # (e.g. *junit.framework.AssertionFailedError: expected:<1> but was:<0>)
                    expected_msg = "*" + expected_msg[0].strip()

                seed_file.write(
                    "{} {} {} {} {}\n".format(project, bug_number, testcase, classes, expected_msg)
                )

generate_seed(project_name, bugs, output)