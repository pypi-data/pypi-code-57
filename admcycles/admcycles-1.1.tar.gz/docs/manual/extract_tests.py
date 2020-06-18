#!/usr/bin/env python
# This script extract the doctests from the tex source main.tex and writes
# them in doctest.rst so that they can be parsed by the sage doctester.

outfile = open("doctests.rst", "w")
infile = open("admcycles_manual.tex")

outfile.write("admcycles manual doctest\n")
outfile.write("=========================\n\n")
outfile.write(".. linkall\n\n")
outfile.write("This file was automatically generated from main.tex, do not edit.\n\n")
outfile.write("TESTS:\n")

l = infile.readline()
n = 0

in_lstlistings = False
bad_doctest = False

while l:
    if in_lstlistings:
        if "\\end{lstlisting}" in l and not l.startswith("%"):
            assert in_lstlistings
            in_lstlistings = False

            if doctest:
                outfile.write("\nLines %d-%d::\n\n" %(n_start, n))
                outfile.write(doctest)
        else:
            if l.startswith("sage: "):
                if "?" in l:
                    bad_doctest = True
                else:
                    bad_doctest = False
            if not bad_doctest:
                l = l.strip()
                if l:
                    doctest += "    " + l
                else:
                    doctest += "    <BLANKLINE>"
                doctest += "\n"
    elif "\\begin{lstlisting}" in l and not l.startswith("%"):
        in_lstlistings = True
        doctest = ""
        n_start = n


    l = infile.readline()
    n += 1

outfile.close()
infile.close()
