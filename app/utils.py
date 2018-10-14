import json, re, shlex, difflib
from subprocess import Popen, PIPE, STDOUT, call

def json_to_dict(json_path):
    """ 
        Converts a json data to dictionary structure
        @json_path: json absolute path
    """
    with open(json_path) as doc:
        _json = json.loads(doc.read())
    return _json

def checkout_and_compile(project, bug_number, project_dir):
    """
        Checkout and Compile commands
    """
    cmd_line = "defects4j checkout -p {} -v {} -w {}".format(project, bug_number, project_dir)
    cmd = shlex.split(cmd_line)
    call(cmd, stderr=STDOUT)

    cmd_line = "defects4j compile -w {}".format(project_dir)
    cmd = shlex.split(cmd_line)
    call(cmd, stderr=STDOUT)

def get_relative_path(project, class_name):
    paths = {
        "Chart": "source",
        "Closure": "src",
        "Lang": "src/java",
        "Math": "src/main/java",
        "Mockito": "src",
        "Time": "src/main/java"
    }

    project_path = paths[project]
    path = "{}/".format(project_path)
    index = class_name.index(path) + len(path)
    
    class_name = class_name[index:]

    return class_name

def remove_comments(string):
    multiline, singleline = r"\/\*([\S\s]+?)\*\/", r"\/\/.+"
    output = re.sub(multiline, "", string)
    output = re.sub(singleline, "", output)
    return output

def parse_comments(origin_file, output_path):
    with open(origin_file) as doc:
        origin = doc.read()

    output = remove_comments(origin)

    with open(output_path, "w") as doc:
        doc.write(output)

def diff_parser(origin_file, minimized_file):
    diff_args = shlex.split("diff {} {}".format(origin_file, minimized_file))
    grep_args = shlex.split("grep -vE '<|>|\|'")
    cut_args = shlex.split("cut -dd -f1")

    diff_ps = Popen(diff_args, stdout=PIPE, shell=False)
    grep_ps = Popen(grep_args, stdin=diff_ps.stdout, stdout=PIPE, shell=False)
    cut_ps = Popen(cut_args, stdin=grep_ps.stdout, stdout=PIPE, shell=False)

    diff_output = cut_ps.communicate()[0].decode('utf-8')
    return diff_output

def is_line_valid(string):
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
        elif ',' in item: # range 10,20
            _range = item.split(',')
            if len(_range)>2:
                _range = _range[:2]
                
            if 'c' in _range[1]: # ignores 'c' char between range numbers
                _range[1] = _range[1][:_range[1].index('c')]

            for line in range(int(_range[0]), int(_range[1]) + 1):
                lines_removed.append(line) # 1 to MAX_SIZE
        else: # single line number
            if 'c' in item and ',' not in item:
                item = item.split('c')[0]
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
    obj_comparison_pattern = r'.+(\<.+\@.+\>).+but was.+(\<.+\@.+\>)'
    return re.search(obj_comparison_pattern, expected_msg) is not None

