#!/usr/bin/perl -w

##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with check_bacula.pl.  If not, see <http://www.gnu.org/licenses/>.

# Submitted:
# Julian Hein                   NETWAYS GmbH
# Managing Director             Deutschherrnstr. 47a
# Fon.0911/92885-0              D-90429 Nürnberg
# Fax.0911/92885-31                                        
# jhein@netways.de              www.netways.de     

# 18/07/2014: Modified by Zoltan Glozik based on check_bacula.pl
# Report an error if there are jobs in the given time period that did not
# terminate normally

# Modified:
# Silver Salonen <silver@ultrasoft.ee>

# version 0.0.3 (07.May.2007)
# * fix typo 'successfull' -> 'successful'
# * add $sqlUsername and $sqlDB variables

# version 0.0.2 (05.May.2006)
# * implement print_usage()
# * implement print_help()
# * add variable $sqlPassword for setting MySQL-password
# * add variable $progVers for showing it in case of -V


# *** Change made by Patrick Roughan at 05:10 13 June 2012: Line 68 added sql password


use strict;
use POSIX;
use File::Basename;
use DBI;
use Getopt::Long;
use vars qw(
       $opt_help
           $opt_hours
           $opt_min_jobs
           $opt_usage
           $opt_version
           $out
           $sql
           $date_start
           $date_stop
           $state
           $count
           $count_err
           );
           
sub print_help();
sub print_usage();
sub get_now();
sub get_date;

my $progname = basename($0);
my $progVers = "0.0.3";
my $sqlDB = "bacula";
my $sqlUsername = "bacula";
my $sqlPassword = "3p0chadmin";

my %ERRORS = (  'UNKNOWN'       =>      '-1',
                'OK'            =>      '0',
                'WARNING'       =>      '1',
                'CRITICAL'      =>      '2');

Getopt::Long::Configure('bundling');
GetOptions
        (
        "H=s"   =>      \$opt_hours,    "hours=s"       =>      \$opt_hours,
        "J=s"   =>      \$opt_min_jobs, "min_jobs=s"    =>      \$opt_min_jobs,
        "h"     =>      \$opt_help,     "help"          =>      \$opt_help,
                                        "usage"         =>      \$opt_usage,
        "V"     =>      \$opt_version,  "version"       =>      \$opt_version
        ) || die "Try '$progname --help' for more information.\n";

sub print_help() {
 print "\n";
 print "If Bacula holds its MySQL-data behind password, you have to manually enter the password into the script as variable \$sqlPassword.\n";
 print "And be sure to prevent everybody from reading it!\n";
 print "\n";
 print "Options:\n";
 print "H	check jobs with errors within <hours> period\n";
 print "J	minimum number of total jobs within <hours> period\n";
 print "h	show this help\n";
 print "V	print script version\n";
}

sub print_usage() {
 print "Usage: $progname -H <hours> -J <min_jobs> [ -h ] [ -V ]\n";
}

sub get_now() {
 my $now  = defined $_[0] ? $_[0] : time;
 my $out = strftime("%Y-%m-%d %X", localtime($now));
 return($out);
}

sub get_date {
 my $day = shift;
 my $now  = defined $_[0] ? $_[0] : time;
 my $new = $now - ((60*60*1) * $day);
 my $out = strftime("%Y-%m-%d %X", localtime($new));
 return ($out);
}

if ($opt_help) {
 print_usage();
 print_help();
 exit $ERRORS{'UNKNOWN'};
}

if ($opt_usage) {
 print_usage();
 exit $ERRORS{'UNKNOWN'};
}

if ($opt_version) {
 print "$progname $progVers\n";
 exit $ERRORS{'UNKNOWN'};
}

my $dsn = "DBI:mysql:database=$sqlDB;host=localhost";
my $dbh = DBI->connect( $dsn,$sqlUsername,$sqlPassword ) or die "Error connecting to: '$dsn': $DBI::errstr\n";
 
if ($opt_hours) {
  $date_stop = get_date($opt_hours);
} else {
  $date_stop = '1970-01-01 01:00:00';
}
$opt_min_jobs = 1 if !$opt_min_jobs;
 
$date_start = get_now();
 
# count number of jobs completed and also number of errors
$sql = "SELECT count(*) as 'count', sum(if(JobStatus != 'T', 1, 0)) as 'count_err' from Job where EndTime <> '' and EndTime <= '$date_start' and EndTime >= '$date_stop';";

my $sth = $dbh->prepare($sql) or die "Error preparing statemment",$dbh->errstr;
$sth->execute;
 
while (my @row = $sth->fetchrow_array()) {
  ($count, $count_err) = @row;
}
$dbh->disconnect();
$count_err = 0 if $count == 0;

$state = $count >= $opt_min_jobs && $count_err == 0 ? 'OK' : 'CRITICAL';

print "Bacula $state: Found $count jobs, $count_err errors\n";
exit $ERRORS{$state};
