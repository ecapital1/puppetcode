#!/usr/bin/python
'''
Created on 2011-3-4

@author: michael
'''

import paramiko, os, time, sys, re
import lib.commonutils as cutils
import lib.trade_db as tdb;

from optparse import OptionParser;

# Generic Variables
program = 'download_rts_to_db'
log_name = '/tmp/' + program + time.strftime("%Y%m%d.%H%M%S")
ver = '0.1'


#rts_server = '10.10.10.50'
#rts_dir = '/media/recon'
rts_server = 'abnau-srv-001.epochcapital.com.au'
rts_dir = '/opt/rts/export'
rts_user = 'rtslog';
rts_password = 'm0n3y!@#'

db_file = '/srv/recon/trade_sqlite.db'
log_dir = '/srv/recon/log'





if __name__ == '__main__':
    
    
    parser = OptionParser(description='Download RTS export file from server',prog=program,version=ver)
    parser.add_option('-s','--server',metavar='server', dest='server', help='server address')
    
    (options, args) = parser.parse_args(sys.argv);
    
    if(options.server):
        rts_server = options.server;
    
    logger = cutils.Logger()
    logger.openLog(log_name)
    logger.log("=====================Start running %s====================================="%program)
    
    # if do not specify the date, use yesterday as date stamp
    if(len(args) > 1):
        datestamp = args[1];
        logger.log('using specified datestamp %s'%datestamp);
    else:
        now = int(time.time());
        yesterday = now - 60 * 60 * 24;
        tm = time.localtime(yesterday);
        datestamp = time.strftime('%Y%m%d',tm);
        logger.log('using yesterday datestamp %s'%datestamp);
        
    
    
    # check if the log file is already downloaded.
    download_flag = True;
    rts_pattern = '.*rtdexport\.trade\.%s$'%datestamp
    rts_files = [];
#    files = os.listdir(log_dir);
#    rts_files = [];
#    for file in files:
#        if(re.match(rts_pattern,file)):
#            download_flag = False;
#            rts_files.append(file);
#            logger.log('found rts log file %s in local directory %s'%(file,log_dir));
            
    
    if(download_flag is True):
        logger.log('need to download rts log from RTS server %s:%s'%(rts_server,rts_dir));
        # download stuff
        t = paramiko.Transport((rts_server, 22));
        t.connect(username=rts_user,password=rts_password);
        sftp = paramiko.SFTPClient.from_transport(t);
        logger.log('sftp connected to server %s as %s'%(rts_server,rts_user))
        files = sftp.listdir(rts_dir);
        for f in files:
            if(re.match(rts_pattern,f)):
                local_path = os.path.join(log_dir,f);
                if(not os.path.exists(local_path)):
                    sftp.get(os.path.join(rts_dir,f),local_path);
                    logger.log('downloaded RTS log file %s to %s'%(f,log_dir));
                else:
                    logger.log('%s already exists, no need to download'%local_path);
                rts_files.append(f);
        t.close();
    
    
    # load into data base.
    if(len(rts_files)!=0):
        logger.log('loading trading records from log files into database file %s'%db_file);
        database = tdb.TradeDB(db_file);
        database.openDB();
        
        for file in rts_files:
            path = os.path.join(log_dir,file);
            logger.log('loading trading log file %s'%path);
            database.loadRTSRecords(path);
            logger.log('Done!')
        database.closeDB();
    else:
        logger.log('cannot find any trading log files, no data is loaded to database');
    
    
    logger.log("=======================End running %s====================================="%program)
    logger.closeLog()
    sys.exit(0)
    
    
    
