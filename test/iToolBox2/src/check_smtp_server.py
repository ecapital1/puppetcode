#!/usr/bin/python

'''
Created on 2011-9-5

@author: michael
'''



import time, sys
import lib.commonutils as cutils;
from lib.mailagent import MailSender;


# Generic Variables
program = 'check_smtp_server'
log_name = '/tmp/' + program + time.strftime("%Y%m%d.%H%M%S")
ver = '0.1'


smtp_server = 'mail1.agama.com.au';
mail_from = 'noreply@epochcapital.com.au';
mail_to = 'support@epochcapital.com.au';

subject = 'Test Mail for SMTP server %s'%smtp_server;
content = '''
Test Mail Only
Please do not reply.
'''


if __name__ == '__main__':
    logger = cutils.Logger()
    logger.openLog(log_name)
    logger.log("=====================Start running %s====================================="%program)
    
    s = MailSender();
    s.smtp_server = smtp_server;
    s.use_tls = False;
    logger.log('sending test mail...')
    s.send_mail(mail_from, [mail_to], subject, content);
    logger.log('Done, please check email box for %s'%mail_to);
    logger.log("=======================End running %s====================================="%program)
    logger.closeLog()
    sys.exit(0)