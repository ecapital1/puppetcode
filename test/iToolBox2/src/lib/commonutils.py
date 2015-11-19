'''
Created on 2010-11-4

@author: michael
'''

import time, sys, re, subprocess, datetime, os

def convert_time(src_time, tgt_tz, src_tz=None):
    assert type(src_time) == datetime.datetime
    
    # save old time zone
    tz_backup = None;
    if('TZ' in os.environ):
        tz_backup = os.environ['TZ'];
        
    tgt_time = None;
    try:
        if(src_tz is not None):
            os.environ['TZ'] = src_tz;
         
        # get the time stamp using source timezone info
        ts = time.mktime(src_time.timetuple())
        os.environ['TZ'] = tgt_tz;
        tgt_time = src_time.fromtimestamp(ts)
    finally:
        # restore the time zone
        if(tz_backup is not None):
            os.environ['TZ'] = tz_backup;
        else:
            del os.environ['TZ'];
            
    return tgt_time;

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

def next_work_day(date_str):
    tm = time.strptime(date_str, '%Y%m%d');
    current = datetime.date(tm.tm_year,tm.tm_mon,tm.tm_mday);
    
    weekday = current.weekday();
    delta = 1;
    if(weekday == 4):
        delta = 3;
    elif(weekday == 5):
        delta = 2;
    else:
        delta = 1;
    next_working_day = current + datetime.timedelta(days=delta);
    return next_working_day.strftime('%Y%m%d');
    

def run_cmd_get_code(cmd):
    return subprocess.call(cmd,shell=True)

def run_cmd_get_output(cmd):
    return subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()

def parse_properties_from_file(file_name):
    props = {}
    file = open(file_name,'r')
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        #ignore comments
        if(not line.startswith('#')):
            pair = line.split('=')
            if(len(pair) is 2):
                props[pair[0].strip()] = pair[1].strip()
                
    file.close()
    return props

def save_properties_to_file(props,file_name):
    file = open(file_name,'w')
    for key in props:
        file.write('%s=%s\n'%(key,props[key]))
    file.close()

def parse_config_file1(file_name):
    pattern = '^<(.*)>$'
    config = {}
    current_key= "unknown"
    config[current_key] = []
    file = open(file_name,'r')
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        #ignore comments
        if(not line.startswith('#') and not re.match('^$',line)):
            if(re.match(pattern,line)):
                current_key = re.findall(pattern,line)[0]
                config[current_key] = []
            else:
                arry = config[current_key]
                arry.append(line)
    file.close()
    return config


class Logger:
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.loglevel = 7
        self._logFile = None
        
        
    def openLog(self,logname):
        self._logFile = open(logname,'a',0)
        
    def closeLog(self):
        self._logFile.close()
        
    def log(self,log,level=3):
        ts = time.strftime("%Y%m%d.%H%M%S: ")
        str = ts+log
        if(level<=self.loglevel):
            print str;
            self._logFile.write(str+'\n');
            
    def printTable(self,dict):
        for key in dict:
            self.log("%s:%s"%(key,dict[key]))
            
    def check_status_code(self,retval,err_str):
        if(retval is not 0):
            self.log(err_str)
            self.closeLog()
            sys.exit(1)
    
        
        