#!/usr/bin/env python

import sys, os

"""
if filename <> '':
    try:
        file = open(filename)
    except:
        print this_script, "cannot open file:", filename
        sys.exit(1)
else:
    file = sys.stdin
"""

try:
    file1 = open(sys.argv[1],"r")
    file2 = open(sys.argv[2],"r")
except:
    sys.exit(os.path.basename(sys.argv[0]), "failed to open input files (two required):", arg1, arg2)    
    
for line1 in file1: 
    line2 = file2.readline()
    print line1[:-1], '\t', line2[:-1]
    
file1.close()
file2.close()