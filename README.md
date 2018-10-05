This is a program slicer based on the Mozilla lithium tool (*). The
goal of the slicer is to remove as much lines from your code as
possible. The input to the slicer are:

 - The input file to minimize
 - A test to use for minimization
 - A string message to use as oracle

A successful step (i.e., line removal) occurs when running the test on
the--mutated--file produces an output that matches the string provided
on input.

Example:

Run the script "s" to minimize the file "BinarySearchTree" located in
the project "some_project".

Instructions:

...TODO...



* https://github.com/MozillaSecurity/lithium