#!/usr/bin/python
'''
Created on 2011-8-16

@author: michael
'''
import time, sys
import lib.commonutils as cutils;


# Generic Variables
program = 'run_dummy_script'
log_name = '/tmp/' + program + time.strftime("%Y%m%d.%H%M%S")
ver = '0.1'

if __name__ == '__main__':
    logger = cutils.Logger()
    logger.openLog(log_name)
    logger.log("=====================Start running %s====================================="%program)
    
    
    logger.log("=======================End running %s====================================="%program)
    logger.closeLog()
    sys.exit(0)