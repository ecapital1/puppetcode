#!/usr/bin/python
'''
Created on 2011-3-25

@author: michael
'''

import os, time, sys, datetime
import lib.tradereport as tr
import lib.commonutils as cutils;
import lib.trade_db as tdb;
import lib.tradeutils as tu;
from optparse import OptionParser

# Generic Variables
program = 'epoch_PL_report'
log_name = "/tmp/" + program +time.strftime("%Y%m%d.%H%M%S")
ver = '0.1'
    

if __name__ == '__main__':
    
    
    db_file = '/srv/recon/mfg.db';
    epoch_db_file = '/srv/recon/trade_sqlite.db';
    account = None;
    product = None;
    start_date = None;
    end_date = None;
    out_file = None;
    detail = False;
    
    
    parser = OptionParser(description='Calculate PnL from MFG cash file',prog=program,version=ver)
    parser.add_option('-d','--db_file', metavar='db_file', dest='db_file', help='MFG database')
    parser.add_option('-s','--start', metavar='start',dest='start', help='Start Date of PnL')
    parser.add_option('-e','--end', metavar='end',dest='end', help='End Date of PnL')
    parser.add_option('-o','--out', metavar='outfile',dest='outfile', help='simple output file')
    (options, args) = parser.parse_args(sys.argv)
    
    if(options.db_file):
        db_file = options.db_file;
        
    if(options.start):
        start_date = options.start;
        
    if(options.end):
        end_date = options.end;
        
    if(options.outfile):
        out_file = options.outfile;
        
    if(not os.path.exists(db_file)):
        print "cannot locate MFG Database file."
        sys.exit(1);
        
    if(start_date is None):
        print "start date is not specified";
        sys.exit(1);
    if(end_date is  None):
        print "end date is not specified";
        sys.exit(1);
        
    if(out_file is None):
        print "out put file is not specified";
        sys.exit(1);
    
    
    
    logger = cutils.Logger()
    logger.openLog(log_name)
    logger.log("=====================Start running %s====================================="%program)
    ##################################
    # get open positions.
    ###################################
    mfg_db = tdb.MFGTradeDB(db_file);
    logger.log('Open MFG database')
    mfg_db.openDB();
    logger.log('retrieving open positions between %s and %s'%(start_date,end_date))
    p_date = cutils.last_work_day(start_date);   
    ops = mfg_db.getOpenPositions(start_date=p_date, end_date=end_date);
    mfg_db.closeDB();
    logger.log('Close MFG database')
    
    # get trading records.
    epoch_db = tdb.TradeDB(epoch_db_file);
    filter = tdb.Filter();
    
    s_date_obj = datetime.datetime.strptime(start_date,'%Y%m%d');
    e_date_obj = datetime.datetime.strptime(end_date,'%Y%m%d');
    s_date_obj = s_date_obj - datetime.timedelta(days=5);
    e_date_obj = e_date_obj + datetime.timedelta(days=2);
    logger.log('start time: %s'%s_date_obj.strftime('%Y%m%d'));
    logger.log('end time: %s'%e_date_obj.strftime('%Y%m%d'))
   
    filter.start_time = s_date_obj;
    filter.end_time = e_date_obj;
    
    logger.log('Open Epoch database');
    epoch_db.openDB();
    logger.log('retrieving epoch data records');
    init_epoch_records = epoch_db.getRecords(filter);
    epoch_records = [];
    
    logger.log('calculating MFG date for records')
    for record in init_epoch_records:
        ex = record.exchange;
        ts = record.datetime;
        mfgdate = tu.caculate_mfg_date(ex, ts);
        if(mfgdate >= start_date and mfgdate <= end_date):
            record.mfgdate = mfgdate;
            epoch_records.append(record);
    
    logger.log('Close Epoch database');
    epoch_db.closeDB();
    
    
    report = tr.PLReport(start_date,end_date,None);
    report.tradeRecords = epoch_records;
    report.ops= ops;
    
    
    logger.log('calculation PnL for all accounts and all products from %s to %s'%(start_date,end_date));
    
    
    logger.log('getting all accounts');
    accounts = report.getAllAccounts();
    
    csvreport = [];
    
    for account in accounts:
        logger.log('generating report for account %s'%account);
        (dates,products,table) = report.buildReportTable(account, MFG=False);
        logger.log('converting report into csv format for account %s'%account);
        r = report.generateCSVReport(account, dates, products, table)
        csvreport.extend(r);
        csvreport.append(' ');
        
    
    if(out_file is not None):
        logger.log('generating out put file to %s'%out_file)    
        
        f = open(out_file,'w');
        for line in csvreport:
            f.write(line);
            f.write('\n');
        f.close();
    
    
    
    
    logger.log("=======================End running %s====================================="%program)
    logger.closeLog()
    sys.exit(0)