#!/usr/bin/python
'''
Created on 2011-3-2

@author: michael
'''
# this script should not be used.


import time, sys, subprocess, os, shutil

if __name__ == '__main__':
    
    exchange = 'SFE';
    asap_host = '203.27.17.200';
    asap_port = 33001;
    date = time.strftime('%Y%m%d');
    exp_output_dir = 'Logs'
    py_output_dir = 'python_output'
    
    
    
    if(len(sys.argv)>1):
        date = sys.argv[1];
        
    cmd = 'FillExporter --hostname %s -p %s -e %s -d %s'%(asap_host,asap_port,exchange,date);
    
    retval = subprocess.call(cmd,shell=True);
    
    if(retval != 0):
        print "failed to run FillExporter Command";
        sys.exit(1);
    
    dirs = os.listdir(exp_output_dir);
    
    if(len(dirs)!=1):
        print "cannot locate output directories as there are %d sub-directories"%len(dirs);
        sys.exit(1);
    else:
        print "found directory %s"%dirs[0];
        
    dir = os.path.join(exp_output_dir,dirs[0]);
    files = os.listdir(dir);
    
    target = None;
    for file in files:
        if(file.startswith('trades')):
            print "found trade file %s"%file
            target = os.path.join(dir,file);
            break;
        
    if(target is None):
        print "Failed to find trade log."
        sys.exit(1);
    
    dst_file = "asap_%s.csv"%date; 
    dst = os.path.join(py_output_dir,dst_file);
    print "copy %s to %s"%(target,dst);   
    shutil.copy2(target, dst);
    
    print "delete %s"%dir
    for file in files:
        path = os.path.join(dir,file);
        print path;
        os.remove(path);
    os.rmdir(dir);
    
    
    
    pass