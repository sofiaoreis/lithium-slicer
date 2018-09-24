import argparse, shlex, json, os
from subprocess import Popen, PIPE

parser = argparse.ArgumentParser(description='TODO')

parser.add_argument('--origin', type=str, nargs=1, help='Original filepath')
parser.add_argument('--minimized', type=str, nargs=1, help='Minimized filepath')
parser.add_argument('--output', type=str, nargs=1, help='Output filepath')

args = parser.parse_args()

origin_file = args.origin[0]
minimized_file = args.minimized[0]
output_file = args.output[0]

diff_args = shlex.split("diff {} {}".format(origin_file, minimized_file))
grep_args = shlex.split("grep -vE '<|>|\|'")
cut_args = shlex.split("cut -dd -f1")

diff_ps = Popen(diff_args, stdout=PIPE, shell=False)
grep_ps = Popen(grep_args, stdin=diff_ps.stdout, stdout=PIPE, shell=False)
cut_ps = Popen(cut_args, stdin=grep_ps.stdout, stdout=PIPE, shell=False)

diff_output = cut_ps.communicate()[0].decode('utf-8')

def parser(diff_output):
    """
    TODO
    returns a list of lines removed
    """
    out = shlex.split(diff_output)
    lines_removed = []
    for item in out:
        if ',' in item: # range 10,20
            _range = item.split(',')
            _range = [int(x) for x in _range]
            for line in range(_range[0], _range[1] + 1):
                lines_removed.append(line - 1) # 0 to MAX_SIZE -1
        else: # single line number
            lines_removed.append(int(item) - 1)
    return lines_removed
    

def get_kept_loc(lines_removed):
    origin_size = Popen('wc -l < {}'.format(origin_file), shell=True, stdout=PIPE)
    out = origin_size.communicate()[0].decode('utf-8')
    n_loc = int(out.split('\n')[0])
    loc = [x for x in range(n_loc) if x not in lines_removed]
    return loc

def data_to_json(filename):
    data = {}
    r = parser(diff_output)
    with open('{}.json'.format(filename), 'w') as doc:
        data['class'] = filename
        data['loc'] = str(get_kept_loc(r))
        json.dump(data, doc, indent=4)

data_to_json(os.path.basename(origin_file))
