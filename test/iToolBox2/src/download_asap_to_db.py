#!/usr/bin/python


import paramiko, os, time, sys, re
import lib.commonutils as cutils
import lib.trade_db as tdb;

# Generic Variables
program = 'download_asap_to_db'
log_name = '/tmp/' + program + time.strftime("%Y%m%d.%H%M%S")
ver = '0.1'


asap_server = '10.10.10.17'
asap_dir = '/cygdrive/c/Program Files/Epoch Capital/ASAP Admin Tools/python_output'
asap_user = 'Administrator';
asap_password = '3p0chadmin'

db_file = '/srv/recon/trade_sqlite.db'
log_dir = '/srv/recon/log'





if __name__ == '__main__':
    
    logger = cutils.Logger()
    logger.openLog(log_name)
    logger.log("=====================Start running %s====================================="%program)
    
    # if do not specify the date, use yesterday as date stamp
    if(len(sys.argv) > 1):
        datestamp = sys.argv[1];
        logger.log('using specified datestamp %s'%datestamp);
    else:
        now = int(time.time());
        yesterday = now - 60 * 60 * 24;
        tm = time.localtime(yesterday);
        datestamp = time.strftime('%Y%m%d',tm);
        logger.log('using yesterday datestamp %s'%datestamp);
        
    
    
    # check if the log file is already downloaded.
    download_flag = True;
    asap_pattern = 'asap_%s\.csv$'%datestamp
    files = os.listdir(log_dir);
    asap_files = [];
    for file in files:
        if(re.match(asap_pattern,file)):
            download_flag = False;
            asap_files.append(file);
            logger.log('found asap log file %s in local directory %s'%(file,log_dir));
            
    
    if(download_flag is True):
        logger.log('need to download ASAP log from ASAP server %s:%s'%(asap_server,asap_dir));
        # download stuff
        t = paramiko.Transport((asap_server, 22));
        t.connect(username=asap_user,password=asap_password);
        sftp = paramiko.SFTPClient.from_transport(t);
        logger.log('sftp connected to server %s as %s'%(asap_server,asap_user))
        files = sftp.listdir(asap_dir);
        for f in files:
            if(re.match(asap_pattern,f)):
                local_path = os.path.join(log_dir,f);
                sftp.get(os.path.join(asap_dir,f),local_path);
                logger.log('downloaded ASAP log file %s to %s'%(f,log_dir));
                asap_files.append(f);
        t.close();
    
    
    # load into data base.
    if(len(asap_files)!=0):
        logger.log('loading trading records from log files into database file %s'%db_file);
        database = tdb.TradeDB(db_file);
        database.openDB();
        
        for file in asap_files:
            path = os.path.join(log_dir,file);
            logger.log('loading trading log file %s'%path);
            database.loadASAPRecords(path);
            logger.log('Done!')
        database.closeDB();
    else:
        logger.log('cannot find any trading log files, no data is loaded to database');
    
    
    logger.log("=======================End running %s====================================="%program)
    logger.closeLog()
    sys.exit(0)
    
    
    
