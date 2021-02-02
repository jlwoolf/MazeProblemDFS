#Maze Problem solved using DFS
Implementation of Depth First Search to solve maze problem outlined in the problem pdf. Input file provided is the same as problem.pdf but any file can
be provided following this input format:

* Line 1 contains two integers, n and m.
* Line 2 contains n−1 characters where the ith character represents the color of the ith vertex.
The vertex with index n is the goal and has no color.
* Line 3 contains two integers s1 and s2, representing the index of the starting vertices of
Captain Rocket and Lieutenant Lucky, respectively.
* Each of the next m lines contains two integers a and b and one character c, in that order,
representing a corridor with color c from a to b. Note that a, b ∈ [1, n].

The input in input.txt corresponds to problem.pdf where 1 is A, 2 is B, . . ., 27 is AA and
28 is the Goal vertex. The four colors are R (red), G (green), Y (yellow) and B (blue).

The output is printed to the console and saved in a file called output.txt by default but can be changed as
the contents of the second argument.