import sys, os

expected = sys.argv[1]
output_filepath = sys.argv[2]

with open(output_filepath) as out:
    output = [line.strip() for line in out.readlines() if not line.startswith('---') and not line.startswith('\t')]

# remove temporary output
os.remove(output_filepath)

# uncomment these lines to check que output
# print(expected.split(','))
# print(output)

# should print GOOD or BAD in console
print("GOOD" if (expected.split(',') == output) else "BAD")


def NPE_check():
    # TODO
    pass