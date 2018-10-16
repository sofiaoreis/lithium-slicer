# Running LithiumSlicer with SFL output

To get all these data, our infrastructure obtains dinamically the data from output_sfl (the JSON files) and run the lithium-slicer for each of them, just using the project name and the bug number.

The script `generate_seeds.py` will get the first five files (by default) in ranking list for each bug number in data/ProjectName/*.json and save the data a seed_file. This file will be read by the script that will run the main program.

The bash script `runner.sh` uses `run_lithium.py` to run the minimization.

## Setup

Copy the output_sfl content to data directory. For example, the JSON files in `Chart` should maintain the files in structure data/Chart/*.json.


## Examples 
- Running bug 1 for Chart project `$> ./runner.sh Chart 1`  
- Running bug 1 and 2 for Chart project `$> ./runner.sh Chart 1,2`
- Running all bugs for Chart project `$> ./runner.sh Chart 0`

