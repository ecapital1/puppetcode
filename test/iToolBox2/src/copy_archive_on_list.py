#!/usr/bin/python
'''
Created on 2010-11-16

@author: michael tao
'''
import os, time, sys
from optparse import OptionParser
import lib.commonutils as utils
from lib.copyutils import copy_file
# Generic Variables
program = 'copy_archive_on_list'
log_name = program + time.strftime("%Y%m%d.%H%M%S")
ver = '0.1'

# Global variables for this script only.
local_list = 'local_list'
remote_list = None
local_dir = '.'
remote_dir = None
user = None
server = None

tmp_dir = '/tmp'
# Functions for this script only.

################################################################
# Parsing and checking parameters
################################################################
parser = OptionParser(description='copy files by comparing local and remote list',prog=program,version=ver)
parser.add_option('--local_list', metavar='local_list', dest='local_list', help='the local file list which records files that have been copied')
parser.add_option('--remote_list', metavar='remote_list',dest='remote_list', help='the remote list which  records files that should be copied')
parser.add_option('--local_dir', metavar='local_dir', dest='local_dir', help='the local directory for storing the copied file')
parser.add_option('--remote_dir', metavar='remote_dir',dest='remote_dir', help='the remote directory from which files that should be copied')
parser.add_option('-l','--log', metavar='log',dest='log', help='log file for this script')
parser.add_option('-u','--user', metavar='user',dest='user', help='remote server user')
parser.add_option('-s','--server', metavar='server',dest='server', help='remote server user')

(options, args) = parser.parse_args(sys.argv)

if(options.local_list):
    local_list = options.local_list
        
if(options.remote_list):
    remote_list = options.remote_list
    
if(options.local_dir):
    local_dir = options.local_dir
    
if(options.log):
    log_name = options.log
    
if(options.remote_dir):
    remote_dir = options.remote_dir
    
if(options.user):
    user = options.user
    
if(options.server):
    server = options.server
    
#if(remote_list is None or not os.path.exists(remote_list)):
#    print "Cannot locate the remote file list"
#    sys.exit(1)
    
if(not os.path.exists(local_dir)):
    print "Cannot locate local directory"
    sys.exit(1)

if(remote_dir is None):
    remote_dir = os.path.dirname(remote_list)

################################################################
# Main route starts from here
################################################################
logger = utils.Logger()
logger.openLog(log_name)
logger.log("=====================Start running %s====================================="%program)

# copying remote list to local tmp dir
logger.log('copying remote file list to local...')
remote_login = ""
if(user is not None):
    remote_login += '%s@' %user
if(server is not None):
    remote_login += '%s:' %server
    
retval = copy_file(remote_login+remote_list,tmp_dir)
logger.check_status_code(retval, "Failed to copy remote file list")

remote = utils.parse_properties_from_file(os.path.join(tmp_dir,os.path.basename(remote_list)))

local = None
if(not os.path.exists(local_list)):
    logger.log('cannot locate local list, will create a new one %s'%local_list)
    local = {}
else:
    logger.log('parsing local list %s'%local_list)
    local = utils.parse_properties_from_file(local_list)
    
for item in remote:
    if(item not in local):
        logger.log('copying %s '%remote[item])
        src = os.path.join(remote_dir,remote[item])
        dst = os.path.join(local_dir,remote[item])
        src = remote_login + src
        retval = copy_file(src, dst)
        logger.check_status_code(retval, "Failed to copy remote file list")
        local[item] = remote[item]
        
logger.log('saving local file list %s' %local_list)        
utils.save_properties_to_file(local, local_list)
    
    
logger.log("=======================End running %s====================================="%program)
logger.closeLog()
    
    
    
    






