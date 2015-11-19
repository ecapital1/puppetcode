#!/usr/bin/python
'''
Created on 2011-8-18

@author: michael
'''
from optparse import OptionParser
import lib.commonutils as cutils
import sys, datetime, time, xmlrpclib

# Generic Variables
program = 'tango_log_client_sample'
log_name = '/tmp/' + program + time.strftime("%Y%m%d.%H%M%S")
ver = '0.1'


def main():
    
    logger = cutils.Logger()
    logger.openLog(log_name)
    logger.log("=====================Start running %s====================================="%program)
    
    parser = OptionParser();
    parser.add_option('-H','--host', dest='host',help='Tango Server');
    parser.add_option('-p','--port', dest='port',help='Tango Log Server port');
    parser.add_option('-s','--start',dest='start', help='start time stamp, such as 20111220080900');
    parser.add_option('-e','--end',dest='end', help='end time stamp, such 20110812145523');
    parser.add_option('-o','--output', dest='output',help='output file');
    
    options, args = parser.parse_args(sys.argv);
    print args;
    
    if(options.host):
        server_ip = options.host;
        logger.log("Server: %s"%server_ip);
    else:
        logger.log("Tango Log server not spedified")
        sys.exit(1);
    
    if(options.port):
        server_port = options.port;
    else:
        server_port = 38580;
    logger.log("Tango Log server port %d"%server_port);
        
    if(options.start):
        start_time = options.start
        logger.log("Start Time: %s"%start_time);
    else:
        logger.log('no start time specified!');
        sys.exit(1);
    
    if(options.end):
        end_time = options.end
    else:
        logger.log('End Time not specified, use NOW instead.');
        end_time = datetime.datetime.now();
    logger.log("End Time: %s"%end_time);
    
    sp = xmlrpclib.ServerProxy('http://%s:%s'%(server_ip,server_port));
    result = sp.latest_tango_log(start_time,end_time);
    for line in result:
        print line;
    
    
    logger.log("=======================End running %s====================================="%program)
    logger.closeLog()
    sys.exit(0)

if __name__ == '__main__':    
    main();

