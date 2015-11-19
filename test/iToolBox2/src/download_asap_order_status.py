#!/usr/bin/python
'''
Created on 2011-5-5

@author: michael
'''
import time, os, re, sys, paramiko
import lib.commonutils as cutils;
import lib.mailagent as ma;




# Generic Variables
program = 'download_asap_order_db'
log_name = '/tmp/' + program + time.strftime("%Y%m%d.%H%M%S")
ver = '0.1'


host = '10.10.10.17'
user = 'Administrator'
password = '3p0chadmin'

remote_dir = '/cygdrive/c/Program Files/Epoch Capital/ASAP Admin Tools/python_output'
local_dir = '/srv/asap_orders'


mail_from = 'python@epochcapital.com.au'
mail_to = ['traders.sydney@epochcapital.com.au','michael.tao@epochcapital.com.au']
mail_server = '10.10.10.5'
mail_subject = 'ASAP Order Status Have been saved to share drive'





if __name__ == '__main__':
    logger = cutils.Logger()
    logger.openLog(log_name)
    logger.log("=====================Start running %s=====================================" % program);
    
    
    # if do not specify the date, use yesterday as date stamp
    if(len(sys.argv) > 1):
        datestamp = sys.argv[1];
        logger.log('using specified datestamp %s' % datestamp);
    else:
        datestamp = time.strftime('%Y%m%d');
        logger.log('using today datestamp %s' % datestamp);
        
       
    file_pattern = 'asap_order_%s\d*\.csv' % datestamp;
    
    local_files = os.listdir(local_dir);
       
    target_files = [];   
    # Log on to SFTP server and check for files
    logger.log('log on to ASAP staging server %s:%s to check order status files' % (host, user));
    t = paramiko.Transport((host, 22));
    t.connect(username=user, password=password);
    sftp = paramiko.SFTPClient.from_transport(t);
    logger.log('sftp connected to server %s as %s' % (host, user))
    files = sftp.listdir(remote_dir);
    
    mail_flag = False;
    download_files = [];
    for f in files:
        if(re.match(file_pattern, f)):
            
            local_path = os.path.join(local_dir, f); 
            if(os.path.exists(local_path)):
                logger.log('file %s already exists on %s' % (f, local_dir));
            else:
                logger.log('downloading file %s to local directory %s' % (f, local_dir));
                sftp.get(os.path.join(remote_dir, f), local_path);
                download_files.append(f);
                mail_flag = True;
    
    t.close();
    logger.log('sftp disconneced.')
    
    if(mail_flag == True):
        mail_agent = ma.MailSender();
        mail_agent.smtp_server = mail_server;
        mail_text = 'Following new order files are downloaded to share drive \\\\10.10.10.7\\asap_orders:\n'
        for file in download_files:
            mail_text += '%s\n'%file;
        
        logger.log('sending out notification mail')
        mail_agent.send_mail(mail_from, mail_to, mail_subject, mail_text, [])
    
    logger.log("=======================End running %s=====================================" % program)
    logger.closeLog()
    sys.exit(0)
