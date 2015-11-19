#!/usr/bin/python
'''
Created on 2010-12-21

@author: michael
'''

import os, time, sys
from optparse import OptionParser
import lib.commonutils as cutils
import tarfile

# Generic Variables
program = 'archive_files'
log_name = program + time.strftime("%Y%m%d.%H%M%S")
ver = '0.1'
cmd_err = False


# Global variables
file_list = None
output_file = None
fmt = 'gz'

# Functions for this script only.
def archive_on_list(file_list,output_file,logger,fmt='gz'):
    tgz = tarfile.open(output_file,"w:%s"%fmt)
    for file in file_list:
        tgz.add(file)     
        logger.log("%s is added to the archive" %file)  
    tgz.close()
    logger.log("%s is generated" %output_file)



################################################################
# Main route starts from here
################################################################
if __name__ == '__main__':
    ################################################################
    # Parsing and checking parameters
    ################################################################
    parser = OptionParser(description='invoke',prog=program,version=ver)
    parser.add_option('-l','--log', metavar='log',dest='log', help='log file for this script')
    parser.add_option('-f','--file_list', metavar='file_list',dest='file_list', help='file list which contains the files to be archived')
    parser.add_option('-o','--output_file', metavar='output_file',dest='output_file', help='target archive file that would be created')
    parser.add_option('--fmt',action='store', type='choice', choices=['bz2','tgz'], metavar='fmt', dest='fmt', help='Compression format for the target file')
    
    (options, args) = parser.parse_args(sys.argv)
    
    if(options.log):
        log_name = options.log
    
    if(options.file_list):
        file_list = options.file_list
        
    if(options.output_file):
        output_file = options.output_file
        
    if(options.fmt):
        fmt = options.fmt
        
    if(file_list is None or not os.path.exists(file_list)):
        print "file list not specified or does not exist."
        cmd_err = True
        
    if(output_file is None):
        print "output file is not specified"
        cmd_err = True
        
    if(cmd_err is True):
        sys.exit(1)
    
    logger = cutils.Logger()
    logger.openLog(log_name)
    logger.log("=====================Start running %s====================================="%program)
    
    # open config file and get file list
    logger.log('reading file list from %s' %file_list)
    f = open(file_list,'r')
    list = []
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if(not line.startswith('#') and not line==''):
            list.append(line)
    f.close()

    # create the archive file
    logger.log("Following files would be archived:")
    for path in list:
        logger.log("%s"%path)
    logger.log('creating archive file %s'%output_file)
    archive_on_list(list,output_file,logger,fmt)
    logger.log("=======================End running %s====================================="%program)
    logger.closeLog()
    sys.exit(0)
    
    