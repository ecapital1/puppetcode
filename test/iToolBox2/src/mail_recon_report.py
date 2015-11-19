#!/usr/bin/python
'''
Created on 2011-2-11

@author: michael
'''

import os, time, sys, re
import lib.commonutils as cutils
import lib.mailagent as ma;
import ConfigParser


# Generic Variables
program = 'mail_recon_report'
log_name = '/tmp/' + program + time.strftime("%Y%m%d.%H%M%S")

# Global variables for this script only.

if __name__ == '__main__':
    
    logger = cutils.Logger()
    logger.openLog(log_name)
    logger.log("=====================Start running %s====================================="%program)
    
    config_file = 'mail_recon_report.conf';
    date_dir = time.strftime('%Y%m%d');
    csv_file = 'recon_report_%s.csv'%date_dir;
    pl_file = 'PL_%s.*\.xls'%date_dir;
    
    # config file processing
    if(len(sys.argv) > 1):
        config_file = sys.argv[1];
    config = ConfigParser.ConfigParser();
    config.read(config_file);
    mail_server = config.get('mail', 'mail_server');
    mail_smtps_port = config.getint('mail', 'mail_smtps_port');
    mail_from = config.get('mail','mail_from');
    mail_to = config.get('mail','mail_to');
    mail_subject = config.get('mail','mail_subject');
    recon_dir = config.get('recon','base_dir')
    
    
    # date directory selection
    if(len(sys.argv) > 2):
        date_dir = sys.argv[2];
#        report_file = 'recon_report_%s.txt'%date_dir
        csv_file = 'recon_report_%s.csv'%date_dir
        pl_file = 'PL_%s.*\.xls'%date_dir;
        
    mail_subject = mail_subject.replace('{0}',date_dir)
#    report_path = os.path.join(recon_dir, report_file);
    csv_path = os.path.join(recon_dir, csv_file);
    
    attach_list = [csv_path];
    files = os.listdir(recon_dir);
    for file in files:
        if(re.match(pl_file,file)):
            path = os.path.join(recon_dir,file);
            logger.log('found PL log file %s'%path);
            attach_list.append(path);
        
     
    logger.log("%-15s%-10s"%('MAIL SERVER:',mail_server));
    logger.log("%-15s%-10s"%('MAIL PORT:',mail_smtps_port));
    logger.log("%-15s%-10s"%('MAIL FROM:',mail_from));
    logger.log("%-15s%-10s"%('MAIL TO:',mail_to));
    logger.log("%-15s%-10s"%('MAIL SUBJECT:',mail_subject));
    
    body = 'Please kindly find report in the attachment.';
    
    
    mail_agent = ma.MailSender();
    mail_agent.smtp_server = mail_server;
    mail_agent.smtps_port = mail_smtps_port;
    mail_agent.from_addr = mail_from;
#    mail_agent.sendTextMailWithSMTPS(mail_to.split(';'), mail_subject, body, SMTPAuth=False);

    mail_agent.send_mail(mail_from, mail_to.split(';'), mail_subject, body, files=attach_list)
        
    logger.log("=======================End running %s====================================="%program)
    logger.closeLog()
    sys.exit(0)