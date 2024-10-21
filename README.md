# The Tandem-FL

Tandem-FL is a program slicer prototype based on the [Mozilla lithium tool]((https://github.com/MozillaSecurity/lithium)), a test minimization tool to help developers create small test inputs (i.e., code snippets) in their bug reports. 

By default, Mozilla Lithium uses a clever algorithm that's efficient at reducing most large testcases. For a testcase with 2048 lines, it will try removing each chunk of size 1024, permanently removing it if it is still 'interesting'. It then does the same for each chunk of size 512, then 256, all the way down to chunks of size 1. It then does as many additional rounds at chunk size 1 as necessary until it completes a round without removing anything, at which point the file is 1-minimal (removing any single line from the file makes it 'uninteresting'). Mozilla Lithium can attempt to reduce entire codebases or specifiic files.

Tandem-FL attempts to minimize a set of classes that are determined as the most likely to include the faulty statement by Spectrum-based Fault Localization (SFL) techniques. However, the tool can also be run without any input from SFL. Just look at the example at the end of the file where we try to minimize only the class where the bug was found.

## Oracle Comparison

Tandem-FL removes as much code as possible such that the new test execution produces the same message. Tandem-FL uses lithium to minimize and store the slicing output into a temporary diretory. The tool runs `compile` and `test` commands with `defects4j` to compile and test the new test case stored inside the temp directory. If the message generated is the same as the original/expected one, then the file is considered "interesting" and the chunk is officially removed. Otherwise, the file is considered "uninteresting" and the tool keeps trying other chunks. Tandem-FL does NOT compare the entire oracle. The oracle is truncated to the first lines of the oracle message until the line where the test fails, considering `class.java:line_number` (heuristic 1, more conservative, published at IJCAI) or without considering the `line_number`, i.e., `class.java:` (heuristic 2).

e.g., Chart 24 (heuristic 1).

```
java.lang.IllegalArgumentException: Color parameter outside of expected range: Red Green Blue
	at java.awt.Color.testColorValueRange(Color.java:310)
	at java.awt.Color.<init>(Color.java:395)
	at java.awt.Color.<init>(Color.java:369)
	at org.jfree.chart.renderer.GrayPaintScale.getPaint(GrayPaintScale.java:128)
	at org.jfree.chart.renderer.junit.GrayPaintScaleTests.testGetPaint(GrayPaintScaleTests.java:107)
```

One of the major issues of heuristic 1 is that it can't reduce the beginning of the faulty class until the line where the issue is found (e.g., `GrayPaintScale.java:128`). It is only capable to reduce the rest of the file and other classes that may be suspicious. Heuristic 2 can reduce the top of the file and achieve better results for Chart 24.

e.g., Chart 24 (heuristic 2).

```
java.lang.IllegalArgumentException: Color parameter outside of expected range: Red Green Blue
	at java.awt.Color.testColorValueRange(Color.java:)
	at java.awt.Color.<init>(Color.java:)
	at java.awt.Color.<init>(Color.java:)
	at org.jfree.chart.renderer.GrayPaintScale.getPaint(GrayPaintScale.java:)
	at org.jfree.chart.renderer.junit.GrayPaintScaleTests.testGetPaint(GrayPaintScaleTests.java:)
```

For both heuristics, in addition to message comparison, we ensure that the new test cases fail in the line and test class as in the original test. 

Result for heuristic 1: [GrayPaintScale.java](./example/lithium_h1_GrayPaintScale.java)
Result for heuristic 2: [GrayPaintScale.java](./example/lithium_h2_GrayPaintScale.java)
Original class for reference: [GrayPaintScale.java](./example/GrayPaintScale.java)


## Lithium Default Configuration
* `--testcase` and `--tempdir` are defined by our tool
* `--strategy` = `minimize` (default), there are other strategies available
* `--max`; default (half of the file)
* `--min`; default (1)

## Dependencies 
- Python 3.0+
- [Defects4J (D4J)](https://github.com/rjust/defects4j) v2.1.0
- Java 1.8

## Installation with virtualenv
(if you don't have `virtualenv` installed, run `pip3 install virtualenv`).

Create the virtual environment.
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```


## Example Run

The script `run_lithium` is currently instantiated to the [Defects4J](https://github.com/rjust/defects4j) (D4J) dataset (v2.1.0). The inputs to `run_lithium.py` are as follows:
 - The D4J project name
 - The D4J bug number
 - A test to use for minimization
 - A comma-separated list of input files to minimize
 - A path to a file with the failing test message

### Get the failing test message

```
defects4j checkout -p {project_name} -v {bug_number}b -w {tmp_path}
defects4j compile -w {tmp_path} 
defects4j test -w {tmp_path} 
cp {tmp_path}/failing_tests {filename}
```

e.g., for Chart 24 run the following commands.  

```
defects4j checkout -p Chart -v 24b -w /tmp/chart_24_buggy/
defects4j compile -w /tmp/chart_24_buggy/ 
defects4j test -w /tmp/chart_24_buggy/ 
cp /tmp/chart_24_buggy/failing_tests chart_24_message
```

These will store a file with the test expected message in your current repo, called `chart_24_message`. This file needs to be passed to lithium.

### Run lithium

The following command will minimize the file `GrayPaintScale.java` with respect to the test `testGetPaint` from D4J project `Chart`, bug number `24`. We ran the test in isolation once to find the error message.

```bash
$> python3 run_lithium.py --project Chart --bug_number 24 \
 --test_case org.jfree.chart.renderer.junit.GrayPaintScaleTests::testGetPaint \
 --classes source/org/jfree/chart/renderer/GrayPaintScale.java \ 
 --expected_msg_path chart_24_message
 --top 1
 --horacle 1
```

## References

[[1]](https://www.ijcai.org/Proceedings/2019/0661.pdf) Sofia Reis, Rui Abreu and Marcelo D’Amorim. **2019**. _Demystifying the Combination of Dynamic Slicing and Spectrum-based Fault Localization_. International Joint Conference on Artificial Intelligence (IJCAI) · Conference Paper 
