#!/usr/bin/python
'''
Created on 2011-3-25

@author: michael
'''

import os, time, sys, re
import lib.tradereport as tr
import lib.commonutils as cutils;
from optparse import OptionParser

import xlwt;

def add_csv_to_xls_sheet(csvlines,sheet_name,work_book):
    sheet = work_book.add_sheet(sheet_name);
    
    num_pattern = re.compile('^[+-]?\d*\.?\d*$');
    for i in range(len(csvlines)):
        cells = csvlines[i].split(',');
        for j in range(len(cells)):
            data = cells[j];
            if(data is None or data == ''):
                pass;
            elif(data.isdigit()):
                data = int(data);
            elif(num_pattern.match(data)):
                data = float(data);
            else:
                pass
            sheet.write(i,j,data);

# Generic Variables
program = 'generate_PL_report'
log_name = "/tmp/" + program +time.strftime("%Y%m%d.%H%M%S")
ver = '0.1'
    

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
   
   
    report = tr.PLReport(start_date,end_date,db_file);
    logger.log('calculation PnL for all accounts and all products from %s to %s'%(start_date,end_date));
    logger.log('loading trade records from database')
    report.loadTradeRecordsFromDB();
    logger.log('getting all accounts');
    accounts = report.getAllAccounts();
    
    summarycsvreport = [];
    csvreport = [];
    
    acc_pl_summary = [];
    for account in accounts:
        logger.log('generating report for account %s'%account);
        (dates,products,table) = report.buildReportTable(account);
        logger.log('converting report into csv format for account %s'%account);
        r = report.generateCSVReport(account, dates, products, table)
        csvreport.extend(r);
        csvreport.append(' ');
        
        acc_summary = report.summarisePLPerAccount(table);
        summarycsvreport.extend(report.generatePLPerAccountCSV(account, products, acc_summary));
        summarycsvreport.append(" ");
        
    
    
    currency_pl_report = [];
    logger.log('generating Currency P/L report')
    (dates, header, table) = report.buildCurrencyReportTable();
    currency_pl_report = report.generateCurrencyCSVReport(dates, header, table);
    currency_summary_report = report.summarisePLPerCurrency(header, table);    
    summarycsvreport.extend(report.generatePLPerCurrencyCSV(currency_summary_report));
    summarycsvreport.append(" ");
    
    
    currency_fee_report = [];
    logger.log('generating Currency Fee report')
    (dates, header, table) = report.buildCurrencyReportTable(type='fee');
    currency_fee_report = report.generateCurrencyCSVReport(dates, header, table);
    fee_summary_report = report.summarisePLPerCurrency(header, table);    
    summarycsvreport.extend(report.generatePLPerCurrencyCSV(fee_summary_report,PnL=False));
    summarycsvreport.append(" ");
    
    
    product_pl_report = [];
    logger.log('generating Product P/L report')
    (dates, header, table) = report.buildProductReportTable();
    product_pl_report = report.generateProductCSVReport(dates, header, table)
    
    product_summary = report.buildProductPL_FeeSummary()
    summarycsvreport.extend(report.generatePLPerProductSummaryCSV(header, product_summary));
    summarycsvreport.append(" ");
    
    lot_exchange_report = [];
    logger.log('generating Lot Per Exchange report')
    (dates, header, table) = report.buildLotPerExchangeReport();
    lot_exchange_report = report.generateLotPerExchangeCSVReport(dates, header, table)
    
    lot_summary = report.summariseLotsPerExchange(table);
    summarycsvreport.extend(report.generateLotsSummaryCSV(header, lot_summary));
    summarycsvreport.append(" ");
    
        
    
    if(out_file is not None):
        
        work_book = xlwt.Workbook()
        
        logger.log('writing smmary report to spreadsheet');
        add_csv_to_xls_sheet(summarycsvreport,'SUMMARY',work_book);
        
        logger.log('writing account product P/L report to spreadsheet...')
        add_csv_to_xls_sheet(csvreport,'ACCOUNT_PRODUCT_PL',work_book);
        
        logger.log('writing currency PL report to spreadsheet...')
        add_csv_to_xls_sheet(currency_pl_report,'CURRENCY_PL',work_book);
        
        logger.log('writing currency fee report to spreadsheet...')
        add_csv_to_xls_sheet(currency_fee_report,'CURRENCY_FEE',work_book);
        
        logger.log('writing product PL report to spreadsheet...')
        add_csv_to_xls_sheet(product_pl_report,'PRODUCT_PL',work_book);
        
        logger.log('writing lot per exchange report to spreadsheet...')
        add_csv_to_xls_sheet(lot_exchange_report,'LOT_PER_EXCHANGE',work_book);
        
        
        logger.log('saving spread sheet');
        work_book.save(out_file);
#        PL_file = '%s_acc_prod.csv'% out_file;
#        logger.log('generating out put file to %s'%PL_file)    
#        f = open(PL_file,'w');
#        for line in csvreport:
#            f.write(line);
#            f.write('\n');
#        f.close();
#        
#        curr_pl_flie = '%s_currency_pl.csv'% out_file;
#        logger.log('generating out put file to %s'%curr_pl_flie)    
#        f = open(curr_pl_flie,'w');
#        for line in currency_pl_report:
#            f.write(line);
#            f.write('\n');
#        f.close();
#        
#        curr_fee_flie = '%s_currency_fee.csv'% out_file;
#        logger.log('generating out put file to %s'%curr_fee_flie)    
#        f = open(curr_fee_flie,'w');
#        for line in currency_fee_report:
#            f.write(line);
#            f.write('\n');
#        f.close();
    
    logger.log("=======================End running %s====================================="%program)
    logger.closeLog()
    sys.exit(0)