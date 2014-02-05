        IAT in PsychoPy: Creative-Practical x Good-Bad

Copyright (C) Jeremy R. Gray, 2014. Released under the terms of the GPLv3.
Contact jrgray@gmail.com

Task modeled after that reported by JS Mueller, et al.,‎2011, Psych Science.

To score the output .csv files, from within the directory:
% python ./scoreIAT.py data/data_file_name.csv
data_file_name.csv 0.080750882075

Uses scoring procedure outlined in Nosek et al. (2007), developed by Greenwald Nosek & Banaji (2003)

Checks for following exclusionary criteria:
 - 25% of responses too fast in any one of the critical blocks
 - going too fast (<300 ms) on more than 10% of responses across all critical blocks
 - 35% too fast in any one of the practice blocks
 - making more than 30% erroneous responses across the critical blocks
 - 40% errors in any one of the critical blocks
 - 40% errors across all of the practice blocks
 - 50% errors in any one of the practice blocks
