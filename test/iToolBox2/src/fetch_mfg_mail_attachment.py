#!/usr/bin/python
'''
Created on 2011-2-1

@author: michael
'''

import os, time, sys, xlrd, shutil
import lib.commonutils as cutils
from lib.mailagent import MailReader

# Generic Variables
program = 'fetch_mfg_mail_attachment'
log_name = '/tmp/' + program + time.strftime("%Y%m%d.%H%M%S")
ver = '0.1'

# Global variables for this script only.
mail_username = "python";
mail_password = "zaq12wsx";
mail_server = "10.10.10.5";
mail_filter = '(UNSEEN SUBJECT "Open position files")'
mail_box = "INBOX";

#base_dir = '/srv/recon';
tmp_dir = '/srv/recon/tmp';
download_path = '/srv/recon/log';
#local_dir = os.path.join(base_dir,time.strftime("%Y%m%d"));

#save_as_name = 'EPOCH_%s.xls'%time.strftime("%Y%m%d");

def check_mfg_file_date(xls_file,sheet_name):
    fields = ['RunDate'];
    workBook = xlrd.open_workbook(xls_file);
    spreadsheet = workBook.sheet_by_name(sheet_name);
    
    # build field index
    index_map = {};
    for field in fields:
        for col in range(spreadsheet.ncols):
            if(field == spreadsheet.cell_value(0, col)):
                index_map[field] = col;
                break;
   
    row = 1;
    date_dir = spreadsheet.cell_value(row, index_map['RunDate'])
    return date_dir;
    
    


if __name__ == '__main__':
    logger = cutils.Logger()
    logger.openLog(log_name)
    logger.log("=====================Start running %s====================================="%program)
    
#    logger.log("preparing local reconciliation directory")
#    if(os.path.exists(local_dir)):
#        logger.log("found local diretory %s"%local_dir)
#    else:
#        logger.log("creating local directory %s"%local_dir);
#        os.mkdir(local_dir);
        
    logger.log("searching mail account for new MFG mails")
    mail_rd = MailReader();
    mail_rd.username = mail_username;
    mail_rd.password = mail_password;
    mail_rd.server = mail_server;
    logger.log("logging onto account %s"%mail_username);
    mail_rd.login();
    
    logger.log("searching mails in directory %s with filter string %s"%(mail_box,mail_filter));
    ids = mail_rd.searchMailIDs(mail_filter, mail_box)
    if(ids == ['']):
        logger.log("could not find any mails matching filter %s"%mail_filter);
    else:
        ids = ids[0].split();
        for mail_id in ids:
            logger.log("MAIL ID: %s"%mail_id);
            subject = mail_rd.getMailSubject(mail_id);
            logger.log("MAIL SUBJECT: %s"%subject);
            
            
#            date_pattern = '\d{2}/\d{2}/\d{4}';
#            date_str = re.findall(date_pattern,subject);
#            if(len(date_str) != 0):
#                secs = time.strptime(date_str[0], '%d/%m/%Y');
#                date_dir = time.strftime('%Y%m%d',secs)
#                local_dir = os.path.join(base_dir,date_dir);
#                if(os.path.exists(local_dir)):
#                    logger.log("found local diretory %s"%local_dir)
#                else:
#                    logger.log("creating local directory %s"%local_dir);
#                    os.mkdir(local_dir);            
            
            files = mail_rd.saveMailAttachments(mail_id, tmp_dir);
            print files;
            for file in files:
                logger.log("attachment saved to tmp file %s"%file);
                logger.log('checking running date of the MFG file %s'%file);
                run_date = check_mfg_file_date(file,'TradeActivity');
                logger.log('Run date of the MFG log is %s'%run_date);
                old_path = os.path.join(tmp_dir,file);
                new_path = os.path.join(download_path,'EPOCH_%s.xls'%run_date);
#                logger.log('Copying %s to %s'%(old_path,new_path));
#                shutil.copy2(old_path, new_path);
                
                #also copy to log directory:
                shutil.copy2(old_path,new_path);
                
                logger.log('removing the tmp file');
                os.remove(old_path);
                
                
    logger.log("logging out account %s"%mail_username);
    mail_rd.logout();
    logger.log("=======================End running %s====================================="%program)
    logger.closeLog()
    sys.exit(0)