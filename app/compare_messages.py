#! /usr/bin/python3
import sys, os, logging
from utils import check_obj_comparison, is_object_comparison, get_testname_expected_msg, truncate_message
import re
from difflib import unified_diff

def apply_oracle_heuristic(horacle, msg):
    return '\n'.join(msg).strip() if horacle == 1 \
        else re.sub(r'\d+', '','\n'.join(msg).strip())
            
expected_msg_path = sys.argv[1] # "message expected" file path
output_filepath = sys.argv[2] # "failing_test" file that contains the test output after run d4j-test
testname = sys.argv[3] # test name
horacle = int(sys.argv[4]) # heuristic (1 or 2)

print(f"\n[🔎] Comparing messages...")

print(f"[🔎] 🔸 Path for Expected Test Message: {expected_msg_path}")
# get expected/original test case message
if os.path.isfile(expected_msg_path):
    with open(expected_msg_path) as fout:
        expected_test_message = get_testname_expected_msg(testname, fout.readlines())[1::]
        expected_message_truncated, _ = truncate_message(expected_test_message, testname)
        expected_message_truncated_str = apply_oracle_heuristic(horacle, expected_message_truncated)
    print(f'[🔎] 🔸 Test Expected message ⬇️\n{expected_message_truncated_str}\n')


print(f"[🔎] 🔹 Path for Lithium Test Message: {output_filepath}")
# get message from running lithium
if os.path.isfile(output_filepath):
    lithium_result = ''
    with open(output_filepath) as fout:
        lithium_test_message = get_testname_expected_msg(testname, fout.readlines())[1::]
        if len(lithium_test_message) > 0:
            lithium_test_message_truncated, testcase_line = truncate_message(lithium_test_message, testname)
            lithium_test_message_truncated_str = apply_oracle_heuristic(horacle, lithium_test_message_truncated)
            lithium_result = f'[🔎] 🔹 Lithium Test message  ⬇️\n{lithium_test_message_truncated_str}\n'
        else:
            lithium_result = f'[🔎] 🔹 Empty Test Message (after Lithium minimization)'
    print(lithium_result)      
            
    diff = list(unified_diff(expected_message_truncated, lithium_test_message_truncated, lineterm=''))
    if diff: 
        diff_str = '\n'.join(diff)
        print(f"Diff\n{diff_str}")
    else: print('[🔎] 🔻 No difference found between the messages.\n')
    
    try:
        # should print this line to check if there is the same testcase line
        print(f"\n[🔎] 🐞 LITHIUM TEST FAIL CASE LINE [BS]{testcase_line}[BE]")
    except:
        pass
    
    message_cmp_success = f"[🔎] ✅ Expected and Lithium messages are equal. Minimization is GOOD."
    message_cmp_unsuccess = f"[🔎] ❌ Expected and Lithium messages are different. Minimization is BAD."

    # removes the "project_path/failing_tests" file
    os.remove(output_filepath)
    
    print("\n[🔎] Does the expected message include objects to compare? " + str(is_object_comparison(expected_message_truncated_str)))
    # if lithium generates a failing test message
    if lithium_test_message_truncated_str:
        # if the test message includes objects
        if is_object_comparison(expected_message_truncated_str):
            print(message_cmp_success if check_obj_comparison(expected_message_truncated_str, lithium_test_message_truncated_str) else message_cmp_unsuccess)
        else:
            print(message_cmp_success if (expected_message_truncated_str == lithium_test_message_truncated_str) else message_cmp_unsuccess)
    else:
        print(message_cmp_unsuccess)
    
    
