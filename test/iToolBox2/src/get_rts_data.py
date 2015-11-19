#!/usr/bin/python

'''
Created on 2011-2-11

@author: michael
'''

import paramiko, os, datetime, time, sys, re

prod_server = '192.168.2.60'
prod_user = 'rts'
prod_password = 'rtsadmin'
prod_dir = '/opt/rts/export'


#file_server = '10.10.10.7'
#file_user = 'epoch'
#file_password = '3p0chadmin'
#file_dir = '/srv/recon'

local_dir = '/media/recon'

def last_work_day(date_str):
    tm = time.strptime(date_str, '%Y%m%d');
    current = datetime.date(tm.tm_year,tm.tm_mon,tm.tm_mday);
    
    weekday = current.weekday();
    delta = 1;
    if(weekday == 0):
        delta = 3;
    elif(weekday == 6):
        delta = 2;
    else:
        delta = 1;
    last_working_day = current - datetime.timedelta(days=delta);
    return last_working_day.strftime('%Y%m%d');


if __name__ == '__main__':
    
    # download file to local server
    current_day = time.strftime('%Y%m%d');
    now = int(time.time());
    yesterday = now - 60*60*24;
    datestamp = time.strftime('%Y%m%d',time.localtime(yesterday));
    if(len(sys.argv) > 1):
        datestamp = sys.argv[1];
        
#    day2 = last_work_day(current_day);
#    day1 = last_work_day(day2);
#    
#    file_pattern_day2 = '.*rtdexport\.trade\.%s'%day2;
#    file_pattern_day1 = '.*rtdexport\.trade\.%s'%day1;
#    
#    pattern_list = [];
#    pattern_list.append(file_pattern_day2);
#    pattern_list.append(file_pattern_day1);
    
#    sys.stdout.write('looking for data for date %s and %s\n'%(day2,day1));
#    
#    # fix sat problem
#    day2_week_day = time.strftime('%w',time.strptime(day2,'%Y%m%d'));
#    # if it is Monday, then saturday data is also needed
#    if(day2_week_day == '1'):
#        sys.stdout.write('%s is Monday, so Saturday data is also needed\n'%day2);
#        tm = time.strptime(day2, '%Y%m%d');
#        current = datetime.date(tm.tm_year,tm.tm_mon,tm.tm_mday);
#        sat = current - datetime.timedelta(days=2);
#        day_sat = sat.strftime('%Y%m%d');
#        file_pattern_sat = '.*rtdexport\.trade\.%s'%day_sat;
#        pattern_list.append(file_pattern_sat);
#    

    catch_list = [];
    pattern_list = [];
    file_pattern = '.*rtdexport\.trade\.%s'%datestamp;
    sys.stdout.write('looking for file %s.\n'%file_pattern);
    pattern_list.append(file_pattern);
    
    
    # Download
    sys.stdout.write('Connecting to production server %s\n'%prod_server);
    t = paramiko.Transport((prod_server, 22));
    t.connect(username=prod_user,password=prod_password);
    sftp = paramiko.SFTPClient.from_transport(t);
    
    sys.stdout.write('listing directory %s\n'%prod_dir);
    files = sftp.listdir(prod_dir);
    for f in files:
#        if(re.match(file_pattern_day2,f)):
#            local_path = os.path.join(local_dir,f);
#            sftp.get(os.path.join(prod_dir,f),local_path);
#            catch_list.append(local_path);
#            sys.stdout.write('Catched file and downloaded to %s\n'%local_path);
#        if(re.match(file_pattern_day1,f)):
#            local_path = os.path.join(local_dir,f);
#            sftp.get(os.path.join(prod_dir,f),local_path);
#            catch_list.append(local_path);
#            sys.stdout.write('Catched file and downloaded to %s\n'%local_path);
        for pat in pattern_list:
            if(re.match(pat,f)):
                local_path = os.path.join(local_dir,f);
                sftp.get(os.path.join(prod_dir,f),local_path);
                catch_list.append(local_path);
                sys.stdout.write('Catched file and downloaded to %s\n'%local_path);
    
    t.close();
    
        
    # Upload
#    sys.stdout.write('Connecting to file server %s\n' %file_server);
#    t = paramiko.Transport((file_server, 22));
#    t.connect(username=file_user,password=file_password);
#    sftp = paramiko.SFTPClient.from_transport(t);
#    
#   
#    file_date_dir = os.path.join(file_dir,day2);
#    sys.stdout.write('Uploading files to %s\n'%file_date_dir);
#    for file in catch_list:
#        bname = os.path.basename(file);
#        sftp.put(file,os.path.join(file_date_dir,bname));
#        sys.stdout.write('File %s uploaded\n'%bname);
#    
#    
#    
#    t.close();