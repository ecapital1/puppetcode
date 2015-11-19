#!/usr/bin/python
'''
Created on 2011-3-11

@author: michael
'''
from lib.sftp import SFTPAgent
from lib.commonutils import Logger
import time, os, sys, re, ConfigParser
from optparse import OptionParser


# Generic Variables
program = 'upload_build'
ver = '0.1'
log_name = '/tmp/' + program + time.strftime("%Y%m%d.%H%M%S")


if __name__ == '__main__':
    
    config_dir = os.path.dirname(sys.argv[0])
    config_file = os.path.join(config_dir, 'upload_build.conf');
    build_level = None;
    
    logger = Logger()
    logger.openLog(log_name)
    logger.log("=====================Start running %s=====================================" % program)
    
    parser = OptionParser(description='copy files by comparing local and remote list', prog=program, version=ver)
    parser.add_option('-c', '--config', metavar='config_file', dest='config_file', help='the configuration file used for uplaoding build');
    
    (options, args) = parser.parse_args(sys.argv)
    
    if(options.config_file):
        config_file = options.config_file;
        
    if(len(args) > 1):
        build_level = args[1];
        
        
    if(not os.path.exists(config_file)):
        logger.log('cannot find config file %s' % config_file);
        logger.closeLog();
        sys.exit(1);
        
    
    config = ConfigParser.ConfigParser();
    config.read(config_file);
    
    local_dir = config.get('config', 'local dir');
    pattern = config.get('config', 'pattern');
    build_parser = config.get('config', 'parser');
    
    server = config.get('config', 'server');
    port = config.getint('config', 'port');
    username = config.get('config', 'username');
    password = config.get('config', 'password');
    server_dir = config.get('config', 'server dir');
    
    latest_stamp = config.getint('config', 'latest timestamp');
    latest_file = config.get('config', 'latest file');
    if(latest_stamp == ''):
        latest_stamp = 0;
    
    
    logger.log('Local Directory: %s' % local_dir);
    logger.log('Build Pattern: %s' % pattern);
    logger.log('Date Parser: %s' % build_parser);
    logger.log('Upload Server: %s' % server);
    logger.log('Upload Server Port:%d' % port);
    logger.log('Username: %s' % username);
    logger.log('Password: ******');
    logger.log('Server Directory: %s' % server_dir);
    logger.log('Latest File:%s' % latest_file);
    logger.log('Latest stamp: %d' % latest_stamp);
    
    
    target_build = None;
    if(build_level is not None):
        target_build = build_level;
        logger.log('using specified build level: %s' % build_level);
    else:
        candidate_ts = 0;
        candidate = None
        paths = os.listdir(local_dir);
        for path in paths:
            result = re.findall(pattern, path)
            if(len(result) != 0):
                ts = time.mktime(time.strptime(result[0], build_parser));
                ts = int(ts);
                if(ts > candidate_ts):
                    candidate_ts = ts;
                    candidate = path;
                           
        # after iterate all build. compare with the latest one
        if(candidate_ts > latest_stamp):
            target_build = candidate
            latest_stamp = candidate_ts;
            logger.log('using latest build level: %s'%target_build);
            
            
            
    if(target_build is not None):
        # do upload stuff
        logger.log('about to upload latest build %s'%target_build);
        sftp = SFTPAgent(server,port);
        logger.log('connecting to remote server %s'%server);
        try:
            logger.log('log in as account %s'%username);
            sftp.login(username, password);
            local_path = os.path.join(local_dir,target_build);
            logger.log('uploading build %s to %s:%s'%(local_path,server,server_dir));
            sftp.upload(local_path, server_dir);
            logger.log('Done');
        except:
            logger.log('error found while uploading build to remote server');
            logger.closeLog();
        finally:
            logger.log('log out');
            sftp.logout();
    else:
        logger.log('no latest build found');
    
    
    
    # update config file
    
    config.set('config','latest file',target_build);
    config.set('config','latest timestamp',latest_stamp);
    config.write(open(config_file, 'wb'));
    
    logger.log("=======================End running %s=====================================" % program)
    logger.closeLog()
    sys.exit(0)
