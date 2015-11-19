#!/usr/bin/python

import time, sys, subprocess, os

'''
Created on 2011-5-5

@author: michael
'''

if __name__ == '__main__':
    
    exchange = 'SFE';
    asap_host = '203.27.17.200';
    date = time.strftime('%Y%m%d');
    py_output_dir = 'python_output'
    
    
    if(len(sys.argv)>1):
        date = sys.argv[1];
        
     
    out_file = 'asap_%s.csv'%date
    out_path = os.path.join(py_output_dir,out_file);
     
       
    cmd = 'FillExporter -e %s -d %s -o %s %s'%(exchange,date,out_path,asap_host);
    print 'running command: %s'%cmd;
    
    retval = subprocess.call(cmd,shell=True);
    
    if(retval != 0):
        print "failed to run FillExporter Command";
        sys.exit(1);
    else:
        print "Done";