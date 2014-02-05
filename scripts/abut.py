#!/usr/bin/env python

"""abut, python implementation
(c) Jeremy R. Gray 2009, jrgray@gmail.com; distributed under GPLv3
"""

import sys, os

try:
    file1 = open(sys.argv[1], "rU")
    file2 = open(sys.argv[2], "rU")
except IOError:
    sys.exit(os.path.basename(sys.argv[0]), "failed to open input files (two required):", arg1, arg2)

for line1 in file1:
    line2 = file2.readline()
    print line1[:-1], '\t', line2[:-1]

file1.close()
file2.close()
