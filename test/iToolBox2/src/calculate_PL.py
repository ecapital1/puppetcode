#!/usr/bin/python
'''
Created on 2011-3-25

@author: michael
'''

import os, time, sys
import lib.trade_db as tdb;
import lib.tradeutils as tu;
import lib.commonutils as cutils;
from optparse import OptionParser

# Generic Variables
program = 'calculate_PL_'
log_name = "/tmp/" + program +time.strftime("%Y%m%d.%H%M%S")
ver = '0.1'



def calculate_PL(records,start_positions,end_positions):
    sorted_records = tu.sort_trade_records(records);
    
    summary = tu.make_account_product_summary(sorted_records, MFG=True);
    summary = tu.merge_with_start_open_positions(summary, start_positions);
    summary = tu.merge_with_open_positions(summary, end_positions);
    return summary;


def calculate_PL_on_demand(db_file, start_date, end_date, account=None,product=None,):
    db = tdb.MFGTradeDB(db_file);
    db.openDB();
    records = db.getMFGRecords(account, product, start_date, end_date);
    op_start_date = cutils.last_work_day(start_date);
    start_ops = db.getOpenPosition(account, product, op_start_date);
    end_ops = db.getOpenPosition(account, product, end_date)
    summary = calculate_PL(records,start_ops,end_ops)
    db.closeDB();
    return summary;

def generate_report(summary):
    report = [];
    header = '%-10s%-10s%-10s%-10s%-10s%-15s%-10s%-10s%-10s' % ('exchange', 'account', 'product', 'buy_qty', 'sell_qty','Gross P/L','COM','GST','Net P/L')
    report.append(header);
    
    for mfg_item in summary:
        line = '%-10s%-10s%-10s%-10s%-10s%-15s%-10s%-10s%-10s' % (mfg_item.exchange, mfg_item.account, mfg_item.product, mfg_item.buy_qty, mfg_item.sell_qty, mfg_item.profit, mfg_item.commission, mfg_item.gst, mfg_item.profit - mfg_item.commission- mfg_item.gst);
        report.append(line);
        
    return report;

def generate_csvreport(summary):
    report = [];
    header = '%s,%s,%s,%s,%s,%s,%s,%s,%s' % ('exchange', 'account', 'product', 'buy_qty', 'sell_qty','Gross P/L','COM','GST','Net P/L')
    report.append(header);
    
    for mfg_item in summary:
        line = '%s,%s,%s,%s,%s,%s,%s,%s,%s' % (mfg_item.exchange, mfg_item.account, mfg_item.product, mfg_item.buy_qty, mfg_item.sell_qty, mfg_item.profit, mfg_item.commission, mfg_item.gst, mfg_item.profit - mfg_item.commission- mfg_item.gst);
        report.append(line);
        
    return report;

    

if __name__ == '__main__':
    
    
    db_file = '/srv/recon/mfg.db';
    account = None;
    product = None;
    start_date = None;
    end_date = None;
    out_file = None;
    detail = False;
    
    
    parser = OptionParser(description='Calculate PnL from MFG cash file',prog=program,version=ver)
    parser.add_option('-d','--db_file', metavar='db_file', dest='db_file', help='MFG database')
    parser.add_option('-a','--account', metavar='account',dest='account', help='account used in trading')
    parser.add_option('-p','--product', metavar='product',dest='product', help='product or contract or instrument')
    parser.add_option('-s','--start', metavar='start',dest='start', help='Start Date of PnL')
    parser.add_option('-e','--end', metavar='end',dest='end', help='End Date of PnL')
    parser.add_option('-o','--out', metavar='outfile',dest='outfile', help='simple output file')
    (options, args) = parser.parse_args(sys.argv)
    
    if(options.db_file):
        db_file = options.db_file;
        
    if(options.account):
        account = options.account;
        
    if(options.product):
        product = options.product
        
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
    
    
    
    logger = cutils.Logger()
    logger.openLog(log_name)
    logger.log("=====================Start running %s====================================="%program)
    # get the start day open position, should be the previous working day of the start day
#    logger.log('OPEN POSITION BASE DATE: %s'%start_date);
#    logger.log('OPEN POSITION END DATE: %s'%end_date);
    
    summary = calculate_PL_on_demand(db_file,start_date, end_date, account,product)
    report = generate_report(summary);
    
    
    for line in report:
        logger.log(line);
    
    if(out_file is not None):
        logger.log('generating out put file to %s'%out_file)    
        csvreport = generate_csvreport(summary);
        f = open(out_file,'w');
        for line in csvreport:
            f.write(line);
            f.write('\n');
        f.close();
    
    
    
    
    logger.log("=======================End running %s====================================="%program)
    logger.closeLog()
    sys.exit(0)