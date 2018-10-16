# List of scripts under directory app

## Basic Functionality (indentation reflects call chain)
- `interesting.py` - python wrapper to lithium that encapsulates the minimization process
    - `runtest.sh` - executes the test and returns if Good or Bad
        - `compare_messages.py` - checks if expected message is equal to the output message
- `utils.py` - utilities methods

## High-Level Functionality

- `run_lithium.py`  - basic lithium script to automate the minimization process
- `runner.sh` - adapter script for SFL
    - `generate_inputs.py` - script to generate the inputs extracted from SFL output


