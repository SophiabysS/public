#!/usr/bin/env python

"""dt, data tabulation; (c) Jeremy R. Gray 2009, jrgray@gmail.com; distributed under GPLv3

       descriptive stats within cells defined by labels-in-columns
       giving flexible control over data reduction
"""

import sys
import math  # only for log()

#import scipy, numpy  # nice, but I avoid them for portability

def MEAN_SD_SE(x):
    """return (mean, st.dev., std.err.) of list"""
    N = len(x)
    if N < 1:
        return ("_NA_", "_NA_", "_NA_")
    mean_x = float(x[0])
    if N < 2:
        return (mean_x, "_NA_", "_NA_")
    sum_sq_x = 0.
    for i in range(1, N):
        sweep = float(i) / (i + 1)
        delta_x = float(x[i]) - mean_x
        sum_sq_x += delta_x * delta_x * sweep
        mean_x += delta_x / (i + 1)
    sd = float(sum_sq_x / (N - 1)) ** 0.5
    return (mean_x, sd, sd / N ** 0.5)


def MEDIAN_MIN_MAX(x):
    """return (median, min, max) of list"""
    if len(x):
        x.sort(key=float)
        if len(x) % 2:
            med = float(x[len(x) // 2 ])
        else:
            med = (float(x[len(x) // 2]) + float(x[len(x) // 2 - 1])) / 2.
        return (med, float(x[0]), float(x[-1]))
    return ("_NA_", "_NA_", "_NA_")


def PEARSON(x, y):
    """return (correlation, Fisher_Z, seFisher_Z, abs(ratio)) of two lists"""
    N = len(x)
    if N <> len(y) or N < 3:
        return ("_NA_", "_NA_", "_NA_", "_NA_")
    sum_sq_x = 0.
    sum_sq_y = 0.
    sum_coproduct = 0.
    mean_x = float(x[0])
    mean_y = float(y[0])
    for i in range(1, N):
        sweep = float(i) / (i + 1)
        delta_x = float(x[i]) - mean_x
        delta_y = float(y[i]) - mean_y
        sum_sq_x += delta_x * delta_x * sweep
        sum_sq_y += delta_y * delta_y * sweep
        sum_coproduct += delta_x * delta_y * sweep
        mean_x += delta_x / (i + 1)
        mean_y += delta_y / (i + 1)
    pop_sd_x = (sum_sq_x / N) ** 0.5
    pop_sd_y = (sum_sq_y / N) ** 0.5
    if pop_sd_x and pop_sd_y:
        cov_x_y = sum_coproduct / N
        r = cov_x_y / (pop_sd_x * pop_sd_y)
        if r < 1 and r > -1:
            Zr = 0.5 * (math.log(1. + r) - math.log(1. - r))
        else:
            Zr = "_NA_"
        if N > 3:
            seZr = 1 / (N - 3) ** 0.5
        else:
            seZr = "_NA_"
        try:
            return r, Zr, seZr, abs(Zr / seZr)
        except:
            return r, Zr, seZr, "_NA_"
    return ("_NA_", "_NA_", "_NA_", "_NA_")


#### start of main script #### -----------------------------------------------

debug = 0  # or v for verbose
tcols = [ ]
do_factor = 0
filename = ''
hash_sep = ' '
concat_sep = '_'
add_notice = ''
x_col = -1
y_col = -1
d_col = 0  # 0 here allows default input of a single column of numbers
ignore_first_line = 0
add_amount = 0
do_threshold = 0
do_sum_only = 0
do_concat = 0
do_correlation = 0
do_diff = 0  # d = d_col - m_col
do_descriptive = 1  # default
precision = 4

# munch arguments
this_script = sys.argv.pop(0)
while sys.argv:
    arg = sys.argv.pop(0)
    if arg in ('d', 's', 'c', 'ct', 'r', 't', 'p', 'x', '+', 'm', '--file'): # expect another arg
        try:
            str_val = sys.argv.pop(0)
        except:
            print "%s: option %s requires a value (%s #)" % \
                  (this_script, arg, arg)
            sys.exit(1)

        if arg in ['d', 's', 'c', 'ct', 'r', 't', 'p', 'm']:  # expects an int()
            try:
                int_val = int(str_val)
            except:
                print "%s: option %s requires an integer (%s #):" % \
                    (this_script, arg, arg)
                sys.exit(1)
        if arg in ['x', '+']:  # expects a float()
            try:
                float_val = float(str_val)
            except:
                print "%s: option %s requires a float (%s #):" % \
                    (this_script, arg, arg)
                sys.exit(1)

    if arg == 't':
        tcols.append(int_val)
    elif arg in ['m']:
        m_col = int_val - 1
        do_diff = 1
    elif arg in ['d', 's', 'c', 'ct']:
        d_col = int_val - 1
        do_concat = 0
        do_sum_only = 0
        if arg in ('c', 'ct'):
            do_concat = 1
            if arg == 'ct': concat_sep = '\t'
        if arg == 's':
            do_sum_only = 1
    elif arg == 'r':
        if y_col > -1:
            print "%s: warning: more than two columns (r %d, r %d, r %d)" % \
                (this_script, x_col + 1, y_col + 1, int_val + 1)
        if x_col > -1:
            y_col = int_val - 1
        else:
            x_col = int_val - 1
        do_correlation = 1
    elif arg == '+':
        add_amount = float_val + 0  # helps with string formatting
        add_notice = "plus(%s)" % str(add_amount)
        if add_amount >= 0:
            add_notice = "plus(+%s)" % str(add_amount)
    elif arg == 'p': precision = int_val
    elif arg == '_': hash_sep = '_'
    elif arg == 'x':
        threshold_val = float_val
        do_threshold = 1
    elif arg == 'i': ignore_first_line = 1
    elif arg == 'v': debug = 1
    elif arg == '--factor': do_factor = 1
    elif arg == '--file': filename = str_val
    elif arg in ['h', '-h', '--help', '--usage']:
        print "\ndt [", this_script, "],   data tabulator, Jeremy R. Gray 2009\n"
        print """purpose:  data reduction within cells as defined by (multiple) text labels
input  :  text from stdin, pipe, or file
options:  all are optional, order is mostly irrelevant
 t #      - tabulate over labels in column #, multiple are fine (t # t # t # ...)
 d #      - descriptive stats for data in column # (mean SD SE median min max)
 s #      - like 'd', but give sum only
 c[t] #   - concatenate strings in col #, default = underscore sep.; ct is tab sep.
 + #      - add amount to each number; use (+ -#) to subtract
 p #      - output precision after decimal point (default 4)
 r # r #  - correlate two columns, report Pearson r, Fisher Z, SE Fisher Z, ratio
 x #      - exclude values below threshold #
 i        - ignore first line (e.g., header row of column labels)
 _        - [underscore] use _ to separate catagory labels (default = space)
 --factor - build up factor space from t_columns, report empty cells
 --file <filename>  - read from <filename> (default = stdin)

example:  dt t 3 t 1 d 5 p 8 i _ x 32 --file data.txt
bugs etc: - not specified which option takes priority (d, s, c, r), use only one
          - only partial validation of input
          - not tested with Big Numbers"""
        sys.exit(0)
    else:
        print this_script, "unknown argument '%s'. try --help" % arg
        sys.exit(1)

if x_col > -1 and y_col < 0:
    print this_script, ": correlation needs two r arguments (one given)"
    sys.exit(1)
if (do_concat or do_sum_only or do_correlation):
    do_descriptive = 0


#### get the data, build up a table #### -------------------------------------

# init dictionaries here, later link by common keys
values = {}  # holds d_col or x_col data
y_values = {}  # only for correlation
sum = {}
num_exclude = {}
count = {}
factor = {}
for t in tcols:
    factor[t] = []

if filename <> '':
    try:
        file = open(filename)
    except:
        print this_script, "cannot open file:", filename
        sys.exit(1)
else:
    file = sys.stdin

# one pass through all data
for line in file:  # read and process line-by-line
    if ignore_first_line:
        ignore_first_line = 0
        continue

    field = line.split()

    # hash-keys define categories; store unique labels for factor
    if len(tcols):
        str = []
        for t in tcols:
            str.append(field[int(t) - 1] + hash_sep)
            if do_factor and field[int(t) - 1] not in factor[t]:
                factor[t].append(field[int(t) - 1])  # unique label
        hash = ''.join(str)
        hash = hash[:len(hash) - len(hash_sep)]  # trim trailing, for display
    else:
        hash = "<all_lines>"

    if hash not in values.keys():
        values[hash] = []
        y_values[hash] = []
        sum[hash] = 0.
        count[hash] = 0
        num_exclude[hash] = 0

    if add_amount and field[d_col].isdigit():
        try:
            field[d_col] = float(field[d_col]) + add_amount
            str_tmp = "%.*f" % (precision, field[d_col])
            field[d_col] = str_tmp
        except:
            print "add to a string failed %s + %.*f" % (field[d_col], precision, add_amount)

    if do_diff:
        field[d_col] = float(field[d_col]) - float(field[m_col])

    if do_concat:
        if do_threshold and float(field[d_col]) < threshold_val:
            num_exclude[hash] += 1
            count[hash] -= 1
        else:
            values[hash].append(field[d_col] + concat_sep)
    elif do_descriptive or do_sum_only:
        if do_threshold and float(field[d_col]) < threshold_val:
            num_exclude[hash] += 1
            count[hash] -= 1
        else:
            values[hash].append(field[d_col])
            try:  # sum only needed for sum_only, but also effects a numeric check
                sum[hash] += float(field[d_col])
            except:
                print "%s: ? nonnumeric [%s]; try concat (c %d)" % \
                    (this_script, field[d_col], d_col + 1)
                num_exclude[hash] += 1
                count[hash] -= 1
                values[hash].pop()
    elif do_correlation:
        if do_threshold and (float(field[x_col]) < threshold_val or \
                             float(field[y_col]) < threshold_val):
            num_exclude[hash] += 1
            count[hash] -= 1
        else:
            values[hash].append(field[x_col])
            y_values[hash].append(field[y_col])
    else:
        print this_script, ": oops, unexpected state"

    count[hash] += 1

file.close()


#### do stats and report #### -------------------------------------------------

# which cells to report?
if do_factor and len(tcols): # then make keys for all factor crossings
    cells = factor[tcols[0]]
    new_cells = []
    if len(tcols) > 1:
        for i in range(1, len(tcols)):
            for j in range(len(cells)):
                for k in range(len(factor[tcols[i]])):
                    new_cells.append(cells[j] + hash_sep + factor[tcols[i]][k])
            cells = new_cells
            new_cells = []
    sortedKeys = cells
else:
    sortedKeys = values.keys()

sortedKeys.sort()

# do stats within-cell & report
for key in sortedKeys:
    print "%s\t" % key,
    if key not in values.keys():
        count[key] = 0
        num_exclude[key] = 0

    if do_concat:
        if count[key]:
            print "%s\tconcat" % ''.join(values[key])[: - len(concat_sep)],
        else:
            print "\"\"\tconcat_no_data",

    elif do_sum_only:
        if count[key]:
            print "%d\t%.*f\tcount_sum" % (count[key], precision, sum[key]),
        else:
            print "0\t_NA_\tcount_sum",

    elif do_descriptive:
        print "%d\t" % count[key],
        if count[key] == 0:
            print "_NA_\t" * 5,"_NA_",
        else:
            (mean, sd, se) = MEAN_SD_SE(values[key])
            try:
                print "%.*f" % (precision, mean),
            except:
                print "_NA_",
            try:
                print "%.*f\t%.*f" % (precision, sd, precision, se),
            except:
                print "_NA_\t_NA_",

            (median, min, max) = MEDIAN_MIN_MAX(values[key])
            try:
                print "%.*f %.*f %.*f" % \
                       (precision, median, precision, min, precision, max),
            except:
                print "_NA_ _NA_ _NA_",
        print "\tcount_mean_sd_se_median_min_max",

    elif do_correlation:
        print "%d\t" % count[key],
        if count[key]:
            (r, Zr, SEZr, zseRatio) = PEARSON(values[key], y_values[key])
            try:
                print "%.*f\t%.*f\t%.*f\t%.*f" % (precision, float(r), precision,
                      float(Zr), precision, float(SEZr), precision, zseRatio),
            except:
                print "_NA_\t_NA_\t_NA_\t_NA_",
        else:
            print "_NA_\t_NA_\t_NA_\t_NA_",
        print "\tcount_pearson_FisherZ_seFisherZ_zseRatio",
    else:
        print "<oops unexpected state in do_stats>",

    print add_notice,

    if num_exclude[key]:
        print "threshold(%d items" % num_exclude[key],
        if do_threshold:
            print "< %.*f)" % (precision, float(threshold_val)),
        else:
            print "excluded, ? non-numeric)",

    print
