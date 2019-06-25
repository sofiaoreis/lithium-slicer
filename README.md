# The LithiumSlicer (IJCAI VERSION)
LithiumSlicer is a program slicer based on the [Mozilla lithium tool]((https://github.com/MozillaSecurity/lithium)), a test minimization tool to help developers create small test inputs (i.e., code snippets) in their bug reports. 

The goal of LithiumSlicer is to minimize the program with respect to a certain criteria defined by the user. The user needs to provide an oracle that indicates what constitutes a good/bad minimization step. Although, the user can implement whatever oracle function she likes, in most cases the oracle checks if the output of the program is as expected. For the typical scenario, the oracle would check if the execution output of the minimized program matches with test message produced by the original test, e.g., "Expect 10 but seen 5". LithiumSlicer would remove as much code as possible such that test execution would still produce that same message.

## Dependencies 
- Python 3.0+
- [Defects4J (D4J)](https://github.com/rjust/defects4j)

## Installation
- Install dependencies above 
- `$> pip3 install -r requirements.txt`

## Example Run

The script `run_lithium` is currently instantiated to the [Defects4J](https://github.com/rjust/defects4j) (D4J) dataset. (Please send us a message if you need to generalize it.) The inputs to `run_lithium.py` are as follows:
 - The D4J project name
 - The D4J bug number
 - A test to use for minimization
 - A comma-separated list of input files to minimize
 - A string message to use as oracle

For example, the following command will minimize the file `GrayPaintScale.java` with respect to the test `testGetPaint` from D4J project `Chart`, bug number `24`. We ran the test in isolation once to find the error message.

```bash
$> python3 run_lithium.py --project Chart --bug_number 24 \
 --test_case org.jfree.chart.renderer.junit.GrayPaintScaleTests::testGetPaint \
 --classes source/org/jfree/chart/renderer/GrayPaintScale.java \ 
 --expected_message "java.lang.IllegalArgumentException: Color parameter outside of expected range: Red Green Blue"
```
