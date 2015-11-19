'''
Created on 2010-11-17

@author: michael
'''

import re, subprocess, shutil
import commonutils as cu

def copy_file(src, dst, key=None, passwd=None, tool='scp'):
    copy_type = 0
    remote_pattern = '([\w\-]*):.*'
    
    if(re.search(remote_pattern,src) and re.search(remote_pattern,dst)):
        raise IOError
    
    if(re.search(remote_pattern,src) or re.search(remote_pattern,dst)):
        copy_type = 1

    if(copy_type == 0):
        shutil.copy2(src, dst)
        return 0
    else:
        cmd = '%s '%tool
        if(key is not None):
            cmd += "-i %s "%key
        cmd += '%s %s'%(src,dst)
        print cmd
        return subprocess.call(cmd,shell=True)    


def scp(src, dst, options=''):
    cmd = 'scp %s %s %s'%(src,options,dst)
    return cu.run_cmd_get_code(cmd)    
                

def rsync(src, dst, options=''):
    cmd = 'rsync %s %s %s'%(src,options,dst)
    return cu.run_cmd_get_code(cmd)           
            
           
    
       
        
    
