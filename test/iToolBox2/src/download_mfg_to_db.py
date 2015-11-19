#!/usr/bin/python
'''
Created on 2011-3-25

@author: michael
'''

import os, time, sys, re
import lib.commonutils as cutils
import lib.trade_db as tdb;
import lib.tradeutils as tu;

# Generic Variables
program = 'download_mfg_to_db'
log_name = '/tmp/' + program + time.strftime("%Y%m%d.%H%M%S")
ver = '0.1'


db_file = '/srv/recon/mfg.db'
log_dir = '/srv/recon/log'

if __name__ == '__main__':
    
    
    logger = cutils.Logger()
    logger.openLog(log_name)
    logger.log("=====================Start running %s=====================================" % program)
    logger = cutils.Logger()
    logger.openLog(log_name)
    logger.log("=====================Start running %s=====================================" % program)
    
    # if do not specify the date, use last working day as date stamp
    if(len(sys.argv) > 1):
        datestamp = sys.argv[1];
        logger.log('using specified datestamp %s' % datestamp);
    else:
        now = int(time.time());
        weekday = time.strftime('%w');
        if(weekday == '1'):
            yesterday = now - 60 * 60 * 72;
        else:
            yesterday = now - 60 * 60 * 24;
        tm = time.localtime(yesterday);
        datestamp = time.strftime('%Y%m%d', tm);
        logger.log('using last working day %s' % datestamp);
    
    
    
    # check if the log file is already downloaded.
    mfg_pattern = 'EPOCH_%s.xls' % datestamp
    logger.log('looking for file like %s' % mfg_pattern);
    
    files = os.listdir(log_dir);
    mfg_files = [];
    for file in files:
        if(re.match(mfg_pattern, file)):
            mfg_files.append(file);
            logger.log('found TT log file %s in local directory %s' % (file, log_dir));
            
    
    
    # load into data base.
    if(len(mfg_files) != 0):
        logger.log('loading trading records from log files into database file %s' % db_file);
        database = tdb.MFGTradeDB(db_file)
        database.openDB();
        
        for file in mfg_files:
            path = os.path.join(log_dir, file);
            logger.log('loading trading log file %s' % path);
            records = tu.get_mfg_trade_records(path);
            ops = tu.get_open_positions(path);
            logger.log('found %d open positions'%len(ops));
            database.loadRecordsToDB(records, ops, file)
            logger.log('Done!')
        database.closeDB();
    else:
        logger.log('cannot find any trading log files, no data is loaded to database');
    
    
    
    
    
    logger.log("=======================End running %s=====================================" % program)
    logger.closeLog()
    sys.exit(0)
