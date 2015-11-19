#!/usr/bin/python
'''
Created on 2011-2-10

@author: michael
'''

import  time, sys, os, datetime
import lib.commonutils as cutils
import lib.recon as recon;
import lib.trade_db as tdb;
import ConfigParser;


# Generic Variables
program = 'reconciliation2'
log_name = '/tmp/' + program + time.strftime("%Y%m%d.%H%M%S")

# Global variables for this script only.
db_file = '/srv/recon/trade_sqlite.db'
mfg_db_file = '/srv/recon/mfg.db'
log_dir = '/srv/recon/log'
config_file = '/home/epoch/scripts/recon2.conf'

report_name = 'recon_report_%s.csv' % time.strftime("%Y%m%d");


def generate_report(match_list):
    report = [];
    header = '%-10s%-100s%-100s' % (' ','[MFG Records]', '[EPOCH Records]');
    report.append(header);
    header = '%-10s%-10s%-10s%-10s%-10s%-10s%-15s%-10s%-10s%-10s' % ('STATUS', 'exchange', 'account', 'product', 'buy_qty', 'sell_qty','Gross P/L','COM','GST','Net P/L')
    header1 = '%-10s%-10s%-10s%-10s%-10s%-15s%-10s%-10s%-10s' % ('exchange', 'account', 'product', 'buy_qty', 'sell_qty','Gross P/L','COM','GST','Net P/L')
    header = header + header1;
    report.append(header);
    for entry in match_list:
        (flag, mfg_item, epoch_item) = entry;
        status = '%-10s' % flag;
        if(mfg_item is not None):
            mfg = '%-10s%-10s%-10s%-10s%-10s%-15s%-10s%-10s%-10s' % (mfg_item.exchange, mfg_item.account, mfg_item.product, mfg_item.buy_qty, mfg_item.sell_qty, mfg_item.profit, mfg_item.commission, mfg_item.gst, mfg_item.profit - mfg_item.commission- mfg_item.gst);
        else:
            mfg = '%-10s%-10s%-10s%-10s%-10s%-15s%-10s%-10s%-10s' % (' ',' ',' ',' ',' ',' ',' ',' ',' ');
            
        if(epoch_item is not None):
            epoch = '%-10s%-10s%-10s%-10s%-10s%-15s%-10s%-10s%-10s' % (epoch_item.exchange, epoch_item.account, epoch_item.product, epoch_item.buy_qty, epoch_item.sell_qty,epoch_item.profit, epoch_item.commission, epoch_item.gst, epoch_item.profit - epoch_item.commission - epoch_item.gst);
        else:
            epoch = '%-10s%-10s%-10s%-10s%-10s%-15s%-10s%-10s%-10s' % (' ',' ',' ',' ',' ',' ',' ',' ',' ');
            
        line = status + mfg + epoch
        report.append(line);
    return report;        
            
def write_report_to_file(report, file_path):
    file = open(file_path, 'w');
    for line in report:
        file.write(line);
        file.write('\n')
    file.close();

def get_timestamp(datestamp, offset):
    ''' 
    the format of the offset is like:
    -1/18:00   # 18:00 of previous working day of datestamp
    0/18:00    # 18:00 of the datestamp
    1/18:00    # next day of the datestamp
    '''
    (d, t) = offset.split('/');
    tm = time.strptime(datestamp + ' ' + t, '%Y%m%d %H:%M');
    sec = time.mktime(tm);
    
    d = int(d);
    # if it is Monday, then point to Friday
    if(d < 0 and tm.tm_wday == 0):
        sec = sec - 60 * 60 * 24 * 3
    else:
        sec = sec + d * 60 * 60 * 24;
        
    return sec;

def get_datetime_obj(datestamp, offset):
    ''' 
    the format of the offset is like:
    -1/18:00   # 18:00 of previous working day of datestamp
    0/18:00    # 18:00 of the datestamp
    1/18:00    # next day of the datestamp
    '''
    (d, t) = offset.split('/');
    dt_obj = datetime.datetime.strptime(datestamp + ' ' + t, '%Y%m%d %H:%M');
    
    d = int(d);
    # if it is Monday, then point to Friday
    if(d < 0 and dt_obj.weekday() == 0):
        dt_obj = dt_obj - datetime.timedelta(days=3);
    else:
        dt_obj = dt_obj + datetime.timedelta(days=d);
    
    return dt_obj;    

#def get_recent_file_log(db, datestamp):
#    days = 3;
#    d = time.mktime(time.strptime(datestamp, '%Y%m%d'));
#    start = d - 24*60*60*days;
#    end = d + 24*60*60*days;
#    
#    files = db.getFileLog(start,end);
#    
#    report = [];
#    report.append('-------------------------------------------------');
#    report.append('RECENT LOG FILES FOR %s: '%datestamp);
#    report.append('-------------------------------------------------');
#    report.extend(files);
#    report.append('\n\n');
#    return report;
    

if __name__ == '__main__':
    # store report in this array
    report = [];
    
    logger = cutils.Logger()
    logger.openLog(log_name)
    logger.log("=====================Start running %s=====================================" % program)
    
    
    if(len(sys.argv) > 1):
        datestamp = sys.argv[1];
        logger.log('using specified datestamp %s' % datestamp);
    else:
        now = int(time.time());
        yesterday = now - 60 * 60 * 24;
        tm = time.localtime(yesterday);
        datestamp = time.strftime('%Y%m%d', tm);
        logger.log('using yesterday datestamp %s' % datestamp);
    
    report_name = 'recon_report_%s.csv' % datestamp;
    
    
    # check MFG existence
#    mfg_file = None;
#    files = os.listdir(log_dir);
#    mfg_pattern = 'EPOCH_%s.xls$' % datestamp;
#    logger.log('looking for MFG cash file %s' % mfg_pattern);
#    for file in files:
#        if(re.match(mfg_pattern, file)):
#            mfg_file = file;
#            logger.log('found MFG file %s in local directory %s' % (file, log_dir));
#            break;
#    
#    if(mfg_file is None):
#        logger.log('cannot find MFG source file.');
#        logger.closeLog();
#        error_str = 'Cannot find the MFG source file, please contact administrator.'
#        report.append(error_str);
#        write_report_to_file(report, os.path.join(log_dir, report_name));
#        sys.exit(1);
#
#    # get MFG records and covert to account/product summary
#    mfg_acc_prod_records = []
#    logger.log('processing MFG source file %s' % file);
#    logger.log('extracting records from MFG source file %s' % file);
#    path = os.path.join(log_dir, mfg_file);
#    raw_records = tu.get_mfg_trade_records(path);
#    logger.log('sorting MFG trading records.')
#    sorted_records = tu.sort_trade_records(raw_records);
#    logger.log('generating account/product trade summary')
#    sum_list = tu.make_account_product_summary(sorted_records, MFG=True);   
#    logger.log('retrieving open positions');
#    open_positions = tu.get_open_positions(path)
#    mfg_acc_prod_records = tu.merge_with_open_positions(sum_list, open_positions);
#    print "MFG number: %d" % len(mfg_acc_prod_records);
    
    
    ###################################################################
    # read from database for MFG data
    ###################################################################
    logger.log('opening MFG database')
    mfgDB = tdb.MFGTradeDB(mfg_db_file);
    mfgDB.openDB();
    
    logger.log('retrieving MFG data records for date %s'%datestamp);
    mfg_records = mfgDB.getMFGRecords(start_date=datestamp, end_date=datestamp);
    
    ###################################################################
    # retrieving open positions
    ###################################################################
    logger.log('retrieving MFG open position for date %s'%datestamp);
    p_date = cutils.last_work_day(datestamp);
    ops = mfgDB.getOpenPosition(date=datestamp);
    logger.log('retrieving MFG open position for date %s'%p_date);
    p_ops = mfgDB.getOpenPosition(date=p_date);
    logger.log('closing MFG database');
    mfgDB.closeDB(); 
    
    
    ###################################################################
    # read from database for epoch data
    ###################################################################
    config = ConfigParser.ConfigParser()
    config.read(config_file);
    
    exchanges = config.get('config', 'exchange_list');
    exchange_list = exchanges.strip().split(',');
    database = tdb.TradeDB(db_file);
    
    # getting data from RTS/TT/ASAP
    epoch_records = [];
    acc_prod_summary = [];
    log_files = [];
    database.openDB();
    for exchange in exchange_list:
        start = config.get(exchange, 'start');
        end = config.get(exchange, 'end');
        
        start_time = get_datetime_obj(datestamp, start);
        end_time = get_datetime_obj(datestamp, end);
        # build filter and query for records.
        filter = tdb.Filter();
        filter.exchange = exchange;
        filter.start_time = start_time;
        filter.end_time = end_time;
        
        logger.log('retrieving epoch trading records from exchange %s'%exchange);
        records = database.getRecords(filter);
        epoch_records.extend(records);
        
        logger.log('retrieving source file name...')
        fnames = database.getSRCFileNames(filter);
        for fname in fnames:
            fn = os.path.basename(fname);
            if(fn not in log_files):
                log_files.append(fn);
    
    logger.log('SOURCE FILES:')
    for line in log_files:
        logger.log(line);
           
    runner = recon.Recon();
    runner.epochRecords = epoch_records;
    runner.mfgRecords = mfg_records;
    runner.startPositions = p_ops;
    runner.endPositions = ops;
    
    logger.log('running reconciliation process...');
    for line in log_files:
        logger.log(line);
    
    results = runner.reconcile();
    output = generate_report(results);
    for line in output:
        logger.log(line);
    
     
     
    report.append('SOURCE FILES:')
    for file in log_files:
        report.append(file);
    
    
    logger.log('generating CSV report format');
    main = runner.generate_csvreport(results);
    report.extend(main);
    
    database.closeDB();
    write_report_to_file(report,os.path.join(log_dir,report_name));
    logger.log("=======================End running %s=====================================" % program)
    logger.closeLog()
    sys.exit(0)
    
