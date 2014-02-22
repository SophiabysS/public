#!/usr/bin/env python2

"""periodic transpose (ptr): pull out a column and transpose it cyclically

converts a column vector of length n to n/period x period matric

label option preserves another column as a single label-per-line

% cat file | ptr period column [label's-col #]

for data reduction from behavioral output files, eg within-subject data plus subject number label

(c) Jeremy R. Gray 2014, jrgray@gmail.com; distributed as part of graylabcode under GPLv3
"""

import sys

period = int(sys.argv[1])
column = int(sys.argv[2])  # 1-indexed
if len(sys.argv) > 3:
    labcol = int(sys.argv[3])  # 1-indexed column for labels
else:
    labcol = 0
out = []
idx = 0  # where in the cycle
lab = []
warn = []

for count, line in enumerate(sys.stdin):
    line = line.strip()
    f = line.split()
    if ',' in sys.argv or len(f) == 1 and ',' in line:  # auto-detect .csv can fail, or use arg ','
        f = line.split(',')
    if labcol:
        lab.append(f[labcol-1])
    try:
        out.append(f[column-1])
    except IndexError:
        sys.exit("\n%s: bad column %d, at line %d\n" % (sys.arg[0], column, 1+count))
    idx += 1
    if period != 0 and idx >= period:
        if labcol and not set(lab) == set([lab[0]]):
            warn.append(str(1 + count))
        idx = 0
        lab = []
        if labcol:
            print ' '.join([f[labcol - 1]] + out)
        else:
            print ' '.join(out)
        out = []

if warn:
    print >> sys.stderr, 'WARNING: unequal labels line: %s' % ' '.join(warn)
