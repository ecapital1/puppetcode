#!/usr/bin/python

'''
Created on 2011-3-8

@author: michael
'''
import smtplib, ConfigParser
import os, sys, time, re
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

log_dir = 'c:\\tt\\Prof Serv\\Fill Recapper\\Export';
send_to = ['michael.tao@epochcapital.com.au','admin@epochcapital.com.au']
send_from = 'michael.tao@epochcapital.com.au';
alert_to = 'michael.tao@epochcapital.com.au';
account = send_from;
server = '203.45.112.151'
config_file = 'mail_tt_file.conf'

def send_mail(send_from, send_to, subject, text, files=[], server="localhost"):
    assert type(send_to) == list
    assert type(files) == list

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(f, "rb").read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.starttls()
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()



if __name__ == '__main__':
    
    cmd_path = sys.argv[0];
    config_dir = os.path.dirname(cmd_path);
    config_path = os.path.join(config_dir,config_file);
    
    if(not os.path.exists(config_path)):
        print("cannot find the config file %s"%config_path);
        sys.exit(1);
    
    if(len(sys.argv) > 1):
        datestamp = sys.argv[1];
        print('using specified datestamp %s' % datestamp);
    else:
        now = int(time.time());
        tm = time.localtime(now);
        datestamp = time.strftime('%Y%m%d', tm);
        print('using today datestamp %s' % datestamp);
    
    
    config = ConfigParser.ConfigParser();
    config.read(config_path);
    
    defaults = config.defaults();
    
    if('log_dir' in defaults):
        log_dir = defaults['log_dir'];
    
    if('server' in defaults):
        server = defaults['server'];
        
    if('send_from' in defaults):
        send_from = defaults['send_from'];
        
    if('send_to' in defaults):
        send_to = defaults['send_to'].split(';');
        
    if('account' in defaults):
        account = defaults['account'];
        
    if('alert_to' in defaults):
        alert_to = defaults['alert_to'].split(';');
    
    
    subject = 'TT Trade Log for %s from %s' %(datestamp,account);
    text = subject;
    
    d = time.strftime('%Y_%m_%d', time.strptime(datestamp, '%Y%m%d'));
    pattern = '.*Export_%s_\d{6}_Details.csv' % d
    
    file_list = [];
    files = os.listdir(log_dir);
    print "looking for file %s"%pattern
    for file in files:
        if(re.match(pattern, file)):
            print "find TT log file %s" % file
            path = os.path.join(log_dir, file);
            file_list.append(path);
     
    
    if(len(file_list) == 0):
        print "sending reminder mail";
        subject = 'Please check whehter TT recapper has generated the log file and contact system admin';
        text = subject;
        send_mail(send_from, alert_to, subject, text, files=[], server=server);
        print "done"
    else:
        for file in file_list:
            f = open(file,'r');
            lines = f.readlines();
            f.close();
            warning = True;
            for line in lines:
                if(line.find(account)!=-1):
                    warning = False;
                    break;
            if(warning is True):
                log = "log file %s does not contain any information about %s"%(file,account);
                print log;
                text += "\n%s"%log;
                subject = subject + " with WARNING";
                send_to.extend(alert_to);   
         
        print "sending mail...";       
        send_mail(send_from, send_to, subject, text, files=file_list, server=server);
        print "done";
            
            
    
    
    
        
    
