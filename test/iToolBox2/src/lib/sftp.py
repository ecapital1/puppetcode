'''
Created on 2011-3-11

@author: michael
'''

import paramiko, stat, os

class SFTPException(Exception):
    pass


class SFTPAgent(object):
    '''
    classdocs
    '''
    def __init__(self, server, port=22):
        '''
        Constructor
        '''
        self.server = server
        self.port = port
        self.sftp = None
        self.transport = None
        
        
    def login(self,username=None,password=None):
        self.transport = paramiko.Transport((self.server,self.port));
        self.transport.connect(username=username, password=password);
        self.sftp = paramiko.SFTPClient.from_transport(self.transport);
        pass
    
    
    def logout(self): 
        self.sftp.close();
        self.transport.close();
        pass
    
    
    def download(self,remote_path, local_path):
        attr_remote = self.sftp.lstat(remote_path);
        r_dir = stat.S_ISDIR(attr_remote.st_mode);
        
        if(os.path.exists(local_path)):
            l_dir = os.path.isdir(local_path);
        else:
            l_dir = False;
        
        if(r_dir is False and l_dir is False):
            # both are not directory
            self.sftp.get(remote_path,local_path);
        elif(r_dir is False and l_dir is True):
            # remote is not directory but local is directory, download to this directory with the same name
            file_name = os.path.basename(remote_path);
            self.sftp.get(remote_path,os.path.join(local_path,file_name));
        elif(r_dir is True and l_dir is False):
            raise SFTPException('cannot download directory %s to a file'%remote_path)
        else:
            # both are directory, complicated
            paths = self.sftp.listdir(remote_path);
            # create the local sub directory.
            remote_dir_name = os.path.basename(remote_path);
            sub_dir_name = os.path.join(local_path,remote_dir_name);
            if(not os.path.exists(sub_dir_name)):
                os.mkdir(sub_dir_name);
            for path in paths:
                self.download(os.path.join(remote_path,path), sub_dir_name);
       
    def upload(self, local_path, remote_path):
        # detect local or remote path is directory or not
        l_dir = os.path.isdir(local_path);
        attr_remote = self.sftp.lstat(remote_path);
        r_dir = stat.S_ISDIR(attr_remote.st_mode);
        
        if(r_dir is False and l_dir is False):
            # both are not directory
            self.sftp.put(local_path,remote_path);
        elif(l_dir is False and r_dir is True):
            # local is a file and remote is a directory, copy to that directory with the same name
            file_name = os.path.basename(local_path);
            self.sftp.put(local_path,os.path.join(remote_path,file_name));
        elif(l_dir is True and r_dir is False):
            raise SFTPException('cannot upload directory %s to a file'%local_path);
        
        else:
            # both are directory, complicated
            paths = os.listdir(local_path);
            # create remote sub directory
            local_dir_name = os.path.basename(local_path);
            sub_dir_name = os.path.join(remote_path,local_dir_name);
            
            # check if this directory already exist
            r_paths = self.sftp.listdir(remote_path);
            if(local_dir_name not in r_paths):
                self.sftp.mkdir(sub_dir_name);
                
            for path in paths:
                self.upload(os.path.join(local_path,path), sub_dir_name);
                     
        pass  
