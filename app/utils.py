import json, re, shlex, difflib, os
from subprocess import Popen, PIPE, STDOUT, call

def json_to_dict(json_path):
    """ 
        Converts a json data to dictionary structure
        @json_path: json absolute path
    """
    with open(json_path) as doc:
        _json = json.loads(doc.read())
    return _json

def checkout_project(project, bug_number, project_dir):
    """
        Checkout and Compile commands
    """
    cmd_line = "defects4j checkout -p {} -v {} -w {}".format(project, bug_number, project_dir)
    cmd = shlex.split(cmd_line)
    call(cmd, stderr=STDOUT)


def get_relative_path(project, class_name, bug_number):
    """ get the path inside the project directory """
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

    if project == 'Lang' and int(bug_number) < 36:
        project_path = paths[project+'2']
    elif project == 'Math' and int(bug_number) > 84:
        project_path = paths[project+'2']
    else:
        project_path = paths[project]
    path = "{}/".format(project_path)
    index = class_name.index(path) + len(path)
    class_name = class_name[index:]

    return class_name

def remove_comments(string):
    """ remove the comments in java file """
    #! TODO: need to use better pattern. This function affects the diff_parser function
    multiline, singleline = r"\/\*([\S\s]+?)\*\/", r"\/\/.+"
    output = re.sub(multiline, "", string)
    output = re.sub(singleline, "", output)
    return output

def parse_comments(origin_file, output_path):
    """ remove comments in file and save it """
    with open(origin_file) as doc:
        origin = doc.read()

    # where they remove comments
    output = remove_comments(origin)

    with open(output_path, "w") as doc:
        doc.write(output)

def diff_parser(origin_file, minimized_file):
    """ run the diff command (diff FILE FILE_MINIMIZED | grep -vE '<|>|\|') to obtain the lines in file """
    diff_args = shlex.split("diff {} {}".format(origin_file, minimized_file))
    grep_args = shlex.split("grep -vE '<|>|\|'")
    cut_args = shlex.split("cut -dd -f1")

    diff_ps = Popen(diff_args, stdout=PIPE, shell=False)
    grep_ps = Popen(grep_args, stdin=diff_ps.stdout, stdout=PIPE, shell=False)
    cut_ps = Popen(cut_args, stdin=grep_ps.stdout, stdout=PIPE, shell=False)
    
    diff_output = cut_ps.communicate()[0].decode('utf-8')
    return diff_output

def is_line_valid(string):
    """ check if the string contain a digit """
    return bool(re.search(r'\d', string))

def parser(diff_output):
    """
    returns a list with numbers of lines removed
    """
    out = shlex.split(diff_output)
    lines_removed = []
    for item in out:
        if not is_line_valid(item):
            # skip lines that does not contains digit
            continue

        if 'c' in item: # (e.g. 1,5c3)
            # removing 'c' char from item
            c_index = item.index('c')
            item = item[:c_index]

        elif 'd' in item:# (e.g. 1,5d0)
            # removing 'd' char from item
            d_index = item.index('d')
            item = item[:d_index]

        if ',' in item:
            _range = item.split(',') # range from N to M (e.g. 10,20)
            if len(_range)>2:
                _range = _range[:2]
                
            for line in range(int(_range[0]), int(_range[1]) + 1):
                lines_removed.append(line) # 1 to MAX_SIZE
        else: # single line number
            lines_removed.append(int(item))
    return lines_removed
    
def extract_locs(origin_file, lines_removed):
    origin_size = Popen('wc -l < {}'.format(origin_file), shell=True, stdout=PIPE)
    out = origin_size.communicate()[0].decode('utf-8')
    n_loc = int(out.split('\n')[0]) + 1
    loc = [index for index in range(1, n_loc) if index not in lines_removed]
    return loc

def get_locs(origin_file, minimized_file):
    diff_output = diff_parser(origin_file, minimized_file)
    lines_removed = parser(diff_output)
    locs = extract_locs(origin_file, lines_removed)

    return locs

def check_obj_comparison(expected_msg, output_msg):
    """ returns True if the messages compare the same object """
    # expected:<...ClassName@MemoryAddress...> but was:<...ClassName@MemoryAddress...>
    obj_comparison_pattern = r'.+(\<.+\@.+\>).+but was.+(\<.+\@.+\>)'
    search_expected = re.search(obj_comparison_pattern, expected_msg)
    search_output = re.search(obj_comparison_pattern, output_msg)
    if search_expected and search_output:
        expected = search_expected.group(1).split('@')[0], search_expected.group(2).split('@')[0]
        output = search_output.group(1).split('@')[0], search_output.group(2).split('@')[0]
        return (expected[0] == output[0]) and (expected[1] == output[1])  
    return False

def is_object_comparison(expected_msg):
    """ check if the message is an object comparison """
    obj_comparison_pattern = r'.+(\<.+\@.+\>).+but was.+(\<.+\@.+\>)'
    return re.search(obj_comparison_pattern, expected_msg) is not None

def create_json(filename, data):
    """ method to store the results in a json file """
    with open(filename, 'w') as doc:
        json.dump(data, doc, indent=4)
    
    return os.path.isfile(filename)


def get_testname_expected_msg(testname, expected):
    test_found = False; res = []
    for i in expected:
        if testname in i and test_found:
            test_found = False
        if testname in i:
            test_found = True
        if test_found:
            res.append(i)
    return res

def get_to_compare(stacktrace):
    lines = []; ov_acm = 0
    is_overflow = re.search(r'StackOverflowError', stacktrace[0])
    for i in range(len(stacktrace)):
        lines.append(stacktrace[i].strip())
        buggy_line = stacktrace[i].strip()
        if is_overflow:
            if stacktrace[i] == stacktrace[i+1]:
                ov_acm +=1
            if ov_acm > 5:
                break
        if re.search(r'Test(.*).java',stacktrace[i]): 
            break
    return lines, buggy_line
    
