#!/usr/bin/python
'''
Created on 2011-5-5

@author: michael
'''
import time, sys, subprocess, os

if __name__ == '__main__':
    
    asap_host = '203.27.17.200';
    date = time.strftime('%Y%m%d%H%M%S');
    py_output_dir = 'python_output'
        
     
    out_file = 'asap_order_%s.csv'%date
    out_path = os.path.join(py_output_dir,out_file);
     
       
    cmd = 'OrderExporter -o %s %s'%(out_path, asap_host);
    print 'running command: %s'%cmd;
    
    retval = subprocess.call(cmd,shell=True);
    
    if(retval != 0):
        print "failed to run OrderExporter Command";
        sys.exit(1);
    else:
        print "Done";