#!/usr/bin/python
'''
Created on 2011-2-1

@author: michael
'''

import os, time, sys, re
import lib.commonutils as cutils
from lib.mailagent import MailReader

# Generic Variables
program = 'fetch_tt_mail_attachment'
log_name = '/tmp/' + program + time.strftime("%Y%m%d.%H%M%S")
ver = '0.1'

# Global variables for this script only.
mail_username = "python";
mail_password = "zaq12wsx";
mail_server = "10.10.10.5";
mail_filter = '(UNSEEN)'
mail_box = "TT";

base_dir = '/srv/recon';
local_dir = os.path.join(base_dir,time.strftime("%Y%m%d"));
#save_as_name = 'EPOCH_%s.xls'%time.strftime("%Y%m%d");
db_dir = '/srv/recon/log';




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
        
    logger.log("searching mail account for new TT mails")
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
            
            date_pattern = '\d{2}/\d{2}/\d{4}';
            date_str = re.findall(date_pattern,subject);
#            if(len(date_str) != 0):
#                secs = time.strptime(date_str[0], '%d/%m/%Y');
#                date_dir = time.strftime('%Y%m%d',secs)
#                local_dir = os.path.join(base_dir,date_dir);
#                if(os.path.exists(local_dir)):
#                    logger.log("found local diretory %s"%local_dir)
#                else:
#                    logger.log("creating local directory %s"%local_dir);
#                    os.mkdir(local_dir);
            
            files = mail_rd.saveMailAttachments(mail_id, db_dir);
            for file in files:
                logger.log("attachment saved to file %s"%os.path.join(db_dir,file));
                
#                #copy to another directory for db
#                db_dir = '/srv/recon/log';
#                shutil.copy2(file, db_dir);
#                logger.log('%s also copied to db directory %s'%(file,db_dir));
                
    logger.log("logging out account %s"%mail_username);
    mail_rd.logout();
    logger.log("=======================End running %s====================================="%program)
    logger.closeLog()
    sys.exit(0)