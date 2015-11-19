#!/usr/bin/python
'''
Created on 2011-5-16

@author: michael
'''

import time, sys, os, re, xlrd
import lib.commonutils as cutils
from optparse import OptionParser

# Generic Variables
program = 'merge_money_base'
log_name = '/tmp/' + program + time.strftime("%Y%m%d.%H%M%S")
ver = '0.1'

source_dir = '/srv/recon/log'

file_pattern = 'EPOCH_.*\.xls'

class MoneyBaseObject(object):
    def __init__(self):
        self.date = None;
        self.Class = None;
        self.Salesman = None;
        self.Account = None;
        self.Msname = None;
        self.baseBal = None;
        self.baseOTE = None;
        self.baseTE = None;
        self.baseIR = None;
        self.baseME = None;
        self.baseLov = None;
        self.BaseSov = None;
        self.BaseLQV = None;
        self.BaseCurr = None;

def get_money_base_record(xls_file, date, sheet_name='MoneyBase'):
    
    fields = ['Class', 'Salesman', 'Account', 'Msname', 'baseBal', 'baseOTE', 'baseTE', 'baseIR', 'baseME', 'baseLov', 'BaseSov', 'BaseLQV', 'BaseCurr'];
    workBook = xlrd.open_workbook(xls_file);
    spreadsheet = workBook.sheet_by_name(sheet_name);
    
    # build field index
    index_map = {};
    for field in fields:
        for col in range(spreadsheet.ncols):
            if(field.upper() == spreadsheet.cell_value(0, col).upper()):
                index_map[field.upper()] = col;
                break;
    
    # get records from xls file
    records = [];
    row = 1;
    while(row < spreadsheet.nrows):
        rec = MoneyBaseObject()
        rec.Class = str(spreadsheet.cell_value(row, index_map['CLASS']));
        rec.Salesman = str(spreadsheet.cell_value(row, index_map['SALESMAN']));
        rec.Account = str(spreadsheet.cell_value(row, index_map['ACCOUNT']));
        rec.Msname = str(spreadsheet.cell_value(row, index_map['MSNAME']));
        rec.baseBal = str(spreadsheet.cell_value(row, index_map['BASEBAL']));
        rec.baseOTE = str(spreadsheet.cell_value(row, index_map['BASEOTE']));
        rec.baseTE =str(spreadsheet.cell_value(row, index_map['BASETE']));
        rec.baseIR = str(spreadsheet.cell_value(row, index_map['BASEIR']));
        rec.baseME = str(spreadsheet.cell_value(row, index_map['BASEME']));
        rec.baseLov = str(spreadsheet.cell_value(row, index_map['BASELOV']));
        rec.BaseSov = str(spreadsheet.cell_value(row, index_map['BASESOV']));
        rec.BaseLQV = str(spreadsheet.cell_value(row, index_map['BASELQV']));
        rec.BaseCurr = str(spreadsheet.cell_value(row, index_map['BASECURR']));
        
        rec.date = date;
        records.append(rec);
        row = row + 1;
    return records;
    
    
    

if __name__ == '__main__':
    
    logger = cutils.Logger()
    logger.openLog(log_name)
    logger.log("=====================Start running %s=====================================" % program);
    
    parser = OptionParser(description='Merge Moeny Base',prog=program,version=ver)
    parser.add_option('-d','--directory', metavar='dir', dest='dir', help='MFG Cash File Directory')
    parser.add_option('-o','--out', metavar='outfile',dest='outfile', help='simple output file')
    (options, args) = parser.parse_args(sys.argv)
    
    
    if(options.dir):
        source_dir = options.dir;
        
    if(options.outfile):
        out_file = options.outfile;
        
        
    if(out_file is None):
        print "output file is not specified"
        sys.exit(1);
        
        
    
    logger.log('listing directory %s'%source_dir);
    files = os.listdir(source_dir);
    cash_files = [];
    for file in files:
        if(re.match(file_pattern,file)):
            logger.log('found cash file %s'%file)
            cash_files.append(file);
            
    cash_files = sorted(cash_files);
    
    
    records = [];
    for file in cash_files:
        datestamp = re.findall('EPOCH_(\d*)\.xls',file);
        if(len(datestamp) == 0):
            raise "Format not correct";
        
        path = os.path.join(source_dir,file);
        logger.log('retrieving money base records for %s'%datestamp[0])
        current_records = get_money_base_record(path,datestamp[0]);
        records.extend(current_records);
            
    
    logger.log('writing to CSV file %s'%out_file)
    f = open(out_file, 'w');
    logger.log('writing header');
    header = 'Date,Class,Salesman,Account,Msname,baseBal,BaseOTE,BaseTE,baseIR,baseME,baseLov,BaseSov,BaseLQV,BaseCurr\n';
    f.write(header);
    
    for rec in records:
        f.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(rec.date,rec.Class,rec.Salesman,rec.Account,rec.Msname,rec.baseBal,rec.baseOTE,rec.baseTE,rec.baseIR,rec.baseME,rec.baseLov,rec.BaseSov,rec.BaseLQV,rec.BaseCurr));
    f.close();
    logger.log('Done!');
    
    logger.log("=======================End running %s=====================================" % program)
    logger.closeLog()
    sys.exit(0)
    pass