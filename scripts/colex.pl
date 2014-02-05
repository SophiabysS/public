#!/usr/bin/perl -w

#  colex.pl = barebones implementation of colex;  J Gray July 2004
# vertical option May 2008: default = tab-sep, -v = vertical, -s = space-sep

$line_cnt = $num_c = 0;
$vertical = "\t"; # output is transposed to be vertical (instead of default == tab-sep) for each input line

# which columns?
if (@ARGV) {
    while (@ARGV) {
	$a = shift @ARGV;
	if    ($a =~ /^\d+$/) {$col[$num_c++] = $a;} 
	elsif ($a =~ /^-v$/ ) {$vertical = "\n";}
	elsif ($a =~ /^-s$/ ) {$vertical = " ";}
	else {die "$0: unsupported argument \'$a\'\n";}
    }
}
else {die "$0: takes 1 or more integer column indices as arguments\n";}

# pull them out
while ($line = <>) {
    chomp $line;
    @f = split ' ',$line;
    $line_cnt++;
    foreach $i (0..$num_c-1) {
	unless (length $f[$col[$i]-1]) {
	    die "$0: empty field $col[$i], input line $line_cnt\n";
	}
    }
    $str = '';
    foreach $i (0..$num_c-1) { $str .= $f[$col[$i]-1].$vertical;}
    print "$str";
    if ($vertical !~ /\n/) {print "\n";}
}

exit 0;
