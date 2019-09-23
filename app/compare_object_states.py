#! /usr/bin/python3
import sys, os, logging
from utils import check_obj_comparison, is_object_comparison, get_testname_expected_msg, get_to_compare
import re
import os
from os import listdir
from os.path import isfile, join
from lxml import etree
from xmldiff import main, formatting
from shutil import copyfile
from lxml import etree


states_path = sys.argv[1] # "message expected" file path
project_dir = sys.argv[2] # "message expected" file path
testname = sys.argv[3] # "message expected" file path


debug = True # true to check expected and output messages in console (need to set debug=True in interesting.py as well)

logger = logging.getLogger(__name__)


print('Comparing objects...')
oracles_path = project_dir+'/oracles/'
if os.path.isdir(oracles_path):
    files_slicer = [f for f in listdir(oracles_path) if isfile(join(project_dir+'/oracles/', f)) if 'slicer' in f and '.DS_Store' not in f]
    files = [f for f in listdir(oracles_path) if isfile(join(project_dir+'/oracles/', f)) if 'slicer' not in f and '.DS_Store' not in f]

print('files_slicer=', files_slicer)
print('files=', files)

inspected = False
if len(files_slicer) == len(files):
    inspected = True
    print('All object were inspected')
else:
    print('Some objects were not inspected')
    
failed = False
if os.path.isfile(project_dir+'/failing_tests'):
    with open(project_dir+'/failing_tests') as f:
        data = f.readlines()
        # if the passed test is not the testname
        if len(data) > 0:
            print(''.join(data[1:4]))
            # print("Failing Test: {}, testname: {}".format(string, testname))
            # if testname in string:
            print('Test failed')
            failed = True
            # else:
            #     print('Test passed: GOOD')
        else:
            print('Test passed')

print("Number of expected objects: {}, Number of inspected objects: {}".format(len(files), len(files_slicer)))

os.remove(project_dir+'/failing_tests')
for f in files_slicer:
    os.remove(oracles_path+f)

if not failed and inspected:
    print('Result: GOOD')
else:
    print('Result: BAD')



# buggy_line = False
# if len(files_slicer) == len(files):
#     # find for each file a slicer
#     different = False; count = 0
#     for f in files:
#         file_s = f.replace('.xml','_slicer.xml')
#         fil = f
#         copyfile(oracles_path+f, '/Users/miniontroublemaker/Documents/wip_papers/obs_state_slicing/lithium-slicer/app/results/'+f)
#         copyfile(oracles_path+file_s, '/Users/miniontroublemaker/Documents/wip_papers/obs_state_slicing/lithium-slicer/app/results/'+file_s)
#         diff = main.diff_files(oracles_path+f, oracles_path+file_s)
#         if len(diff) > 0:
#             different = True
#             break
#         else:
#             count+=1
#     if os.path.isfile(project_dir+'/failing_tests'):
#         with open(project_dir+'/failing_tests') as f:
#             data = f.readlines()
#             for i in data:
#                 if 'org.jfree.chart.imagemap.junit.StandardToolTipTagFragmentGeneratorTests.testGenerateURLFragment(StandardToolTipTagFragmentGeneratorTests.java:115)' in i.strip():
#                     buggy_line = True
# else:
#     print('Different Length, Result: BAD')
#
# try:
#     print("Size of the expected: {}, Size of the slicer: {}, Null Diffs: {}".format(len(files), len(files_slicer), count))
#     print("Diff Length Between {} vs {}: {}".format(fil, file_s, len(diff)))
#     print('buggy_line=', buggy_line)
# except:
#     pass
#
# if not different and buggy_line:
#     print('Result: GOOD')
# else:
#     print('Result: BAD')


