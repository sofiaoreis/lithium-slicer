# Running LithiumSlicer with SFL output

To run lithium-slicer with the SFL it need add the SFL output in app/data directory. The bash script `runner.sh` encapsulates the `run_lithium.py` to run the minimization process.

The inputs to `runner.sh` are as follows:
- Project name
- Bug number(s)

## Setup
Copy the `output_sfl` content to `data` directory. The script `generate_inputs.py` need to read each json file in the data directory to extract the data for lithium-slicer.

For example, the json files related to `Chart` project should be in `lithium-slicer/app/data/Chart/*.json`.

## Examples 
- Running only one bug (e.g. Chart-1b)
    - `$> ./runner.sh Chart 1`
- Running one or more bugs (e.g. Time-5b,6b)
    - `$> ./runner.sh Time 5,6`
- Running all bugs from a project (e.g. Lang-1b,...,65b)
    - `$> ./runner.sh Lang 0`

