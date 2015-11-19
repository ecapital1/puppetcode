'''
Created on 2010-11-29

@author: michael
'''
import commonutils as cutils

import smtplib, imaplib, email, os
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.Utils import COMMASPACE, formatdate
from email import Encoders

class MailException(Exception):
    pass;

class MailSender(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.username = None
        self.password = None
        self.smtp_server = None
        self.smtp_port = 25
        self.smtps_port = 465
        self.from_addr = None
        self.use_tls = True;
     
    def loadUserSetting(self,propFile):
        props = cutils.parse_properties_from_file(propFile)
        if('username' in props):
            self.username = props['username']
        if('password' in props):
            self.password = props['password']
        if('from_addr' in props):
            self.from_addr = props['from_addr']
        if('smtp_server' in props):
            self.smtp_server = props['smtp_server']
        if('smtp_port' in props):
            self.smtp_port = props['smtp_port']
        if('smtps_port' in props):
            self.smtps_port = props['smtps_port']    
                   
        
    def sendTextMailWithSMTPS(self,to_addr,subject,body, from_addr=None, SMTPAuth=True):
        msg = MIMEText(body)
        msg['Subject'] = subject
        if(from_addr is None):
            msg['From'] = self.from_addr
        else:
            msg['From'] = from_addr
            
        msg['To'] = ";".join(to_addr)
        s = smtplib.SMTP()
        s.set_debuglevel(1)
        s.connect(self.smtp_server,self.smtps_port)
        s.starttls()
        if(SMTPAuth is True):
            s.login(self.username,self.password)
        s.sendmail(from_addr, to_addr, msg.as_string())
        s.close()

        
    
    def sendTextMailWithSMTP(self,from_addr,to_addr,subject,body,SMTPAuth=False):
        msg = MIMEText(body)
        msg['Subject'] = subject
        if(from_addr is None):
            msg['From'] = self.from_addr
        else:
            msg['From'] = from_addr
        msg['To'] = ";".join(to_addr)
        s = smtplib.SMTP()
        s.set_debuglevel(1)
        s.connect(self.smtp_server,self.smtp_port)
        if(SMTPAuth is True):
            s.login(self.username,self.password)
        
        s.sendmail(from_addr, to_addr, msg.as_string())
        s.close()
    
    def send_mail(self,send_from, send_to, subject, text, files=[]):
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
    
        smtp = smtplib.SMTP(self.smtp_server)
        if(self.use_tls is True):
            smtp.starttls()
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()
    


class MailReader(object):
    def __init__(self):
        self.username = None;
        self.password = None;
        self.server = None;
        self.imap = None;
        
        
    def loadUserSetting(self,propFile):
        props = cutils.parse_properties_from_file(propFile);
        if('username' in props):
            self.username = props['username'];
        if('password' in props):
            self.password = props['password'];
        if('server' in props):
            self.server = props['server']
            
    def login(self,directory='INBOX'):
        self.imap = imaplib.IMAP4_SSL(self.server);
        self.imap.login(self.username, self.password);
        self.imap.select(directory);
    
    def logout(self):
        if(self.imap is not None):
            self.imap.logout();
    
    
    def getAllMailIDs(self,directory='INBOX'):
        return self.searchMailIDs('(ALL)', directory);
    
    def getUnseenMailIDs(self,directory='INBOX'):
        return self.searchMailIDs('(UNSEEN)', directory);
    
    def getMailIDsBySender(self,sender,directory='INBOX'):
        return self.searchMailIDs('(FROM "%s")'%sender, directory)
     
    def searchMailIDs(self,filter,directory='INBOX'):
        self.imap.select(directory);
        retval, list = self.imap.search(None,filter);
        if(retval == "OK"):
            return list;
        else:
            raise MailException('IMAP Error: %s'%retval);
        
    def getMailSubject(self,mailID):
        retval, data = self.imap.fetch(mailID, "(RFC822)");
        if(retval == "OK"):
            mail = email.message_from_string(data[0][1]);   
        return mail['SUBJECT'];
    
    def getMailSender(self,mailID):
        retval, data = self.imap.fetch(mailID, "(RFC822)");
        if(retval == "OK"):
            mail = email.message_from_string(data[0][1]);   
        return mail['FROM'];
    
    def saveMailAttachments(self,mailID,saveDir):
        saved_files = [];
        retval, data = self.imap.fetch(mailID, "(RFC822)");
        if(retval == "OK"):
            mail = email.message_from_string(data[0][1]);
            if(mail.get_content_maintype() == 'multipart'):
                for part in mail.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue;
                    if part.get('Content-Disposition') is None:
                        continue;
                    filename = part.get_filename();
                    counter = 1;
                    if not filename:
                        filename = 'part-%03d%s' % (counter, 'bin'); 
                        counter += 1;
                    att_path = os.path.join(saveDir, filename);
                    if not os.path.isfile(att_path) :
                        fp = open(att_path, 'wb');
                        fp.write(part.get_payload(decode=True));
                        fp.close();
                        saved_files.append(att_path);
            elif(mail.get_content_maintype() == 'application'):
                filename = mail.get_filename();
                att_path = os.path.join(saveDir, filename);
                if not os.path.isfile(att_path) :
                    fp = open(att_path, 'wb');
                    fp.write(mail.get_payload(decode=True));
                    fp.close();
                    saved_files.append(att_path);
        return saved_files;
    


        
        
        
    
        