#!/usr/bin/python

'''
Created on 2010-11-4

@author: michael
'''

import time, sys, subprocess
from optparse import OptionParser
from lib.commonutils import Logger

# Generic Variables
program = 'rsync_backup'
log_name = "/tmp/" + program +time.strftime("%Y%m%d.%H%M%S")
ver = '0.1'
params = {}

# Global variables for this script only.
remote_backup = False


# Functions for this script only.



################################################################
# Parsing and checking parameters
################################################################
parser = OptionParser(description='backup specified directories to local or remote servers, seperated by space',prog=program,version=ver)
parser.add_option('-s','--src_list', metavar='src_list', dest='src_list', help='the srource directory list for backup')
parser.add_option('-d','--dst_dir', metavar='dst_dir', dest='dst_dir', help='the destination directory list for backup')
parser.add_option('-u','--user', metavar='user',dest='user', help='the user used for logging on to the remote server')
parser.add_option('-H','--host', metavar='host',dest='host', help='the backup remote server')
parser.add_option('-l','--log', metavar='log',dest='log', help='log file for this script')

(options, args) = parser.parse_args(sys.argv)

if(options.src_list):
    params['src_list'] = options.src_list.strip()
    
if(options.dst_dir):
    params['dst_dir'] = options.dst_dir.strip()
    
if(options.user):
    params['user'] = options.user
    
if(options.host):
    params['host'] = options.host
    
if(options.log):
    log_name = options.log
    
    
if('src_list' not in params.keys()):
    print "source directory is not specified or invalid"
    sys.exit(1)
    
if('dst_dir' not in params.keys()):
    print "destination directory is not specified or invalid"
    sys.exit(1)


if('user' not in params.keys() and 'host' not in params.keys()):
    print "backup %s to local directory %s"%(params['src_list'], params['dst_dir'])
else:
    if('user' not in params.keys()):
        print "user for logging onto remote server is not specified"
        sys.exit(1)
    if('host' not in params.keys()):
        print "remote server is not specified"
        sys.exit(1)
    remote_backup = True
    
    
################################################################
# Main route starts from here
################################################################
logger = Logger()
logger.openLog(log_name)
logger.log("=====================Start running %s====================================="%program)
logger.printTable(params)

cmd = None

if(remote_backup):
    cmd = "rsync -avz --timeout=999 %s %s@%s:%s" %(params['src_list'], params['user'], params['host'], params['dst_dir'])
else:
    cmd = "rsync -av --delete %s %s" %(params['src_list'], params['dst_dir'])
    
logger.log("Issuing command: %s"%cmd)
retval = subprocess.call(cmd,shell=True)
logger.check_status_code(retval,"command failed with return code %d. script is terminated." %retval)
logger.log("return code for %s: %d" %(program,retval))

logger.log("=======================End running %s====================================="%program)
logger.closeLog()
    
    
    
    






