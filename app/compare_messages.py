import sys, os

expected = sys.argv[1] # message expected got from JSON
output_filepath = sys.argv[2] # file that contains the log of test after run d4j

with open(output_filepath) as out:
    output = [line.strip() for line in out.readlines() if not line.startswith('---') and not line.startswith('\t')]

# remove "project_path/failing_tests" file
os.remove(output_filepath)

# uncomment these lines to check que output if necessary
# print("=== [debug] ===")
# print("expected:", expected.split(','))
# print("got:", output)

# should print GOOD or BAD in console
print("GOOD" if (expected.split(',') == output) else "BAD")
