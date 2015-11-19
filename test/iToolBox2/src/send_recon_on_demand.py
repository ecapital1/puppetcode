#!/usr/bin/python
'''
Created on 2011-2-14

@author: michael
'''

import os, time, sys, re
import lib.commonutils as cutils
import lib.mailagent as ma;
import ConfigParser


# Generic Variables
program = 'send_recon_on_demand'
log_name = '/tmp/' + program + time.strftime("%Y%m%d.%H%M%S")


date_pattern = '(\d{2}/\d{2}/\d{4})';



if __name__ == '__main__':
    
    config_file = 'mail_recon_report.conf';
    date_dir = time.strftime('%Y%m%d');
    report_file = 'recon_report_%s.txt' % date_dir
    
    if(len(sys.argv) > 1):
        config_file = sys.argv[1];
    config = ConfigParser.ConfigParser();
    config.read(config_file);
    mail_server = config.get('mail', 'mail_server');
    mail_smtps_port = config.getint('mail', 'mail_smtps_port');
    mail_from = config.get('mail', 'mail_from');
    mail_to = config.get('mail', 'mail_to');
    mail_subject = config.get('mail', 'mail_subject');
    recon_dir = config.get('recon', 'base_dir');
    
    
    mail_username = config.get('mail', 'mail_username');
    mail_password = config.get('mail', 'mail_password');
    mail_box = config.get('mail', 'mail_box');
    mail_filter = config.get('mail', 'mail_filter');
    mail_valid_users = config.get('mail', 'valid_user');
    
    
    #Get mail request
    mail_rd = ma.MailReader();
    mail_rd.username = mail_username;
    mail_rd.password = mail_password;
    mail_rd.server = mail_server;
    
    mail_rd.login(mail_box);
    ids = mail_rd.searchMailIDs(mail_filter, mail_box);
    
    # If there is no request, then script end here.
    if(ids == ['']):
        mail_rd.logout();
        sys.exit(0);
        
    
    ids = ids[0].split();    
    
    
    # Log start from here
    logger = cutils.Logger()
    logger.openLog(log_name)
    logger.log("=====================Start running %s=====================================" % program)
    
    valid_users = mail_valid_users.split(';');
    for mail_id in ids:
        sender = mail_rd.getMailSender(mail_id);
        logger.log('received recon request from %s' % sender);
        
        slist = re.findall('<(.*@.*)>',sender);
        if(len(slist) != 0):
            sender = slist[0];
        
        if(sender not in valid_users):
            logger.log('%s is not in the valid user list, no recon would be sent out for this user' % sender);
            continue;
        
        messages = [];
        report_path = None;
        subject = mail_rd.getMailSubject(mail_id);
        logger.log('receiving recon request: %s' % subject);
        date_stamp = re.findall(date_pattern, subject);
        
        if(len(date_stamp) == 0):
            messages.append('SUBJECT Format Error: cannot parse the date from subject: %s' % subject);
            logger.log('SUBJECT Format Error: cannot parse the date from subject: %s' % subject);
        else:
            tm = time.strptime(date_stamp[0], '%d/%m/%Y');
            date_dir = time.strftime('%Y%m%d', tm);
            report_file = 'recon_report_%s.txt' % date_dir;
            report_path = os.path.join(recon_dir, report_file);
            logger.log('looking for report file %s' % report_path);
            if(not os.path.exists(report_path)):
                logger.log('cannot find the recon report')
                messages.append('cannot find the recon report');
            
        # Now start to send out mail
        mail_sender = ma.MailSender();
        mail_sender.smtp_server = mail_server;
        mail_sender.smtps_port = mail_smtps_port;
        mail_sender.from_addr = mail_from;
        mail_body = '';
        mail_subject = mail_subject.replace('{0}', date_dir)
        
        logger.log('sending recon report for date %s'%date_dir)
        if(len(messages) != 0):
            mail_body = '\n'.join(messages);
        else:
            file = open(report_path, 'r');
            mail_body = file.read();
            file.close();
        sender = [sender];
        mail_sender.sendTextMailWithSMTPS(sender, mail_subject, mail_body, SMTPAuth=False)
        logger.log('recon report has been send to %s'%sender);
    mail_rd.logout();
    logger.log('logging off mail account %s'%mail_rd.username);
    logger.log("=======================End running %s=====================================" % program)
    logger.closeLog()
    sys.exit(0)
