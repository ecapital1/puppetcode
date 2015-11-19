#!/usr/bin/python

'''
Created on 2011-8-16

@author: michael
'''

import time, sys, datetime
from optparse import OptionParser

import lib.commonutils as cutils;
from lib.tango import search_tango_log, get_latest_tango_log

# Generic Variables
program = 'filter_tango_log'
log_name = '/tmp/' + program + time.strftime("%Y%m%d.%H%M%S")
ver = '0.1'

def write_output(result,outfile=None):
    if(outfile is None):
        for line in result:
            line = line.strip();
            print line;
    else:
        f = open(outfile,'w');
        for line in result:
            f.write(line);
        f.close();
        

    
def main():
    logger = cutils.Logger()
    logger.openLog(log_name)
    logger.log("=====================Start running %s====================================="%program)
    
    parser = OptionParser();
    parser.add_option('-f','--file', dest='file',help='Tango log file');
    parser.add_option('-s','--start',dest='start', help='start time stamp, such as 20111220080900');
    parser.add_option('-e','--end',dest='end', help='end time stamp, such 20110812145523');
    parser.add_option('-o','--output', dest='output',help='output file');
    
    
    options, args = parser.parse_args(sys.argv);
    print args;
    
    if(options.file):
        tango_log = options.file;
    else:
        logger.log('Tango Log not specified, latest tango file will be used');
        tango_log = get_latest_tango_log();
        logger.log('Tango Log file %s'%tango_log);
        
    
    if(options.start):
        # because python 2.4.3 does not support
        # start_time = datetime.datetime.strptime(options.start,'%Y%m%d%H%M%S');
        start_time = datetime.datetime.fromtimestamp(time.mktime(time.strptime(options.start,'%Y%m%d%H%M%S')));
        logger.log("Start Time: %s"%start_time.strftime('%Y-%m-%d %H:%M:%S'));
    else:
        logger.log('no start time specified!');
        sys.exit(1);
        
    
    if(options.end):
        # because python 2.4.3 does not support it
        # end_time = datetime.datetime.strptime(options.end,'%Y%m%d%H%M%S');
        end_time = datetime.datetime.fromtimestamp(time.mktime(time.strptime(options.end,'%Y%m%d%H%M%S')));
    else:
        logger.log('End Time not specified, use NOW instead.');
        end_time = datetime.datetime.now();
    logger.log("End Time: %s"%end_time.strftime('%Y-%m-%d %H:%M:%S'));
        
    
    if(options.output):
        outfile = options.output;
        logger.log("Output File: %s"%outfile);
    else:
        outfile = None;
        logger.log("Output File not specified, will print to screen");
    
    logger.log('Filtering Tango log %s...'%tango_log);
    result = search_tango_log(tango_log,start_time,end_time);
    
    logger.log('Writing to output...')
    write_output(result,outfile);
    
    logger.log("=======================End running %s====================================="%program)
    logger.closeLog()
    sys.exit(0)
               
if __name__ == '__main__':
    main();
    
