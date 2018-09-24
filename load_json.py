import json, sys
from os.path import basename, splitext, dirname

def get_data(json_path):
    with open(json_path) as doc:
        _json = json.loads(doc.read())
    return _json
    
def write(filename, data, configuration):
    fails = data['failing']
    bug_number = splitext(basename(filename))[0]
    javafiles = []
    for item in data['rankings']:
        if item['class'] not in javafiles:
            javafiles.append(item['class'])

    with open(configuration, 'w') as doc:
        for fail in fails:
            for javafile in javafiles:
                fail = fail.replace('::', '#')
                javafile_dir = dirname(javafile)
                javafile = basename(javafile)
                doc.write('{} {} {} {}\n'.format(bug_number, fail, javafile_dir, javafile))

configuration = 'config.txt'
json_path = sys.argv[1]
data = get_data(json_path)
write(json_path, data, configuration)
