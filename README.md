# Lithium-Slicer
This is a program slicer based on the [Mozilla lithium tool]((https://github.com/MozillaSecurity/lithium)). The goal of the slicer is to remove as much lines from your code as possible. A successful step (i.e., line removal) occurs when running the test on the--mutated--file produces an output that matches the string provided on input.

The input to the main script (`run_lithium.py`) are:
 - The project name
 - The bug number
 - A test to use for minimization
 - A list of input files to minimize (separated by comma)
 - A string message to use as oracle

To get all these data, our infrastructure obtains dinamically the data from output_sfl (the JSON files) and run the lithium-slicer for each of them, just using the project name and the bug number.

The bash script `runner.sh` uses `run_lithium.py` to run the minimization.

## Dependencies
- Python 3.0+
- [Defects4J (D4J)](https://github.com/rjust/defects4j)
- [Lithium](https://github.com/MozillaSecurity/lithium)

## Installation
- `$> pip3 install -r requirements.txt`

## Data directory
Copy the output_sfl content to data directory. For example, the JSON files in `Chart` should maintain the files in structure data/Chart/*.json.

## Generate seeds (data for run_lithium.py)
The script `generate_seeds.py` will get the first five files (by default) in ranking list for each bug number in data/ProjectName/*.json and save the data a seed_file. This file will be read by the script that will run the main program.

## Running
- Running bug 1 for Chart project `$> ./runner.sh Chart 1`
- Running bug 1 and 2 for Chart project `$> ./runner.sh Chart 1,2`
- Running all bugs for Chart project `$> ./runner.sh Chart 0`

## Structure
- `runner.sh` - main script
- `generate_seed.py` - script to generate a seed file that contains informations extracted from output_sfl json
- `run_lithium.py`  - script to checkout, compile and minimize a file
- `compile_run.py` - script used by lithium to check if the file is interesting to reduce 
- `compare_messages.py` - script used to check if expected message is equal to the output message after reduce a file
- `runtest` - script used in interesting function (compile_run.py)
- `utils` - utilities methods
