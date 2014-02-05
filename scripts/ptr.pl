#!/usr/bin/perl -w 

# (c) Jeremy R. Gray 2009, jrgray@gmail.com; distributed as part of graylab code under GPLv3

# ptr.pl $repeat $column 
# periodic-transpose $repeat elements from input column $coloumn
#   example: ... | dt t 1 t 5 d 8 | ptr 3 4
#            takes linear output in column 4 (of the dt output) and makes a matrix 3 items wide
# repeat of 0 means transpose into one line, regardless of how long 

# would be nice to reverse transpose, and to allow retention of labels

$period = shift @ARGV;
$col = -1 + shift @ARGV;

$i = $cnt = 0;

while ($line = <>) {
    chomp $line;
    @f = split ' ',$line;
    if (length $f[$col]) {print "$f[$col] ";}
    else {die "$0: blank column ".(1+$col).", at line $cnt\n";}
    $i++; $cnt++;
    if ($period != 0 and $i >= $period) {print "\n"; $i=0}
}

if ($period == 0 or $i != 0 and $i < $period) {print "\n";}

exit 0;

 
