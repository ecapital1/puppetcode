'''
Created on 2011-8-19

@author: michael
'''
import datetime,time,re, os

def get_latest_tango_log():
    
    base_dir = '/opt/rts/tango/tmp'
    
    items = os.listdir(base_dir);
    
    list = [];
    for item in items:
        dir = os.path.join(base_dir,item);
        if(os.path.isdir(dir) and re.match('\d{8}',item)):
            list.append(item);
            
    list = sorted(list,reverse=True);
    target = list[0];
    return os.path.join(base_dir,target,'tango.log');


def search_tango_log(log_file,start_time,end_time=None,filters=None):
    
    if(end_time is None):
        end_time = datetime.datetime.now();
    
    assert type(start_time) == datetime.datetime;
    assert type(end_time) == datetime.datetime;
    assert start_time < end_time;
    
    s_date = start_time.strftime('%Y%m%d');
    s_time = start_time.strftime('%H:%M:%S');
    e_date = end_time.strftime('%Y%m%d');
    e_time = end_time.strftime('%H:%M:%S');
    
    date_pattern = re.compile('Date is (\d{4}-\w{3}-\d{2})');
    time_pattern = re.compile('^\d\d:\d\d:\d\d');
    
    results = [];
    start_date_flag = False;
    start_time_flag = False;
    end_date_flag = False;
    end_time_flag = False
    
    f = open(log_file,'r');
    
    line = 'START';
    while(line != ''):
        # read one line first
        line = f.readline();
        
        # look for the start date
        if(start_date_flag is False):
            # check for start date
            ds = date_pattern.findall(line);
            if(len(ds)!=0):
                ds = ds[0];
                datestamp = time.strftime('%Y%m%d',time.strptime(ds,'%Y-%b-%d'));
                if(datestamp >= s_date):
                    start_date_flag = True;
                else:
                    continue;
            else:
                continue;
         
        # look for the end date
        if(end_date_flag is False):
            # check for start date
            ds = date_pattern.findall(line);
            if(len(ds)!=0):
                ds = ds[0];
                datestamp = time.strftime('%Y%m%d',time.strptime(ds,'%Y-%b-%d'));
                if(datestamp >= e_date):
                    end_date_flag = True;
        
        
        # look for start time
        if(start_time_flag is False):
            # check for start time
            ts = time_pattern.findall(line);
            if(len(ts)!=0):
                timestamp = ts[0];
                if(timestamp >= s_time):
                    start_time_flag = True;
                else:
                    continue;
            else:
                continue;
                    
        
        # look for end time
        if(end_date_flag is True and end_time_flag is False):
            ts = time_pattern.findall(line);
            if(len(ts)!=0):
                timestamp = ts[0];
                if(timestamp >= e_time):
                    end_time_flag = True;
         
        # check whether it is finished.
        if(end_date_flag is True and end_time_flag is True):
            break;
         
         
        # if the code finally comes here, start_date_flag and start_time_flag must be True now
        # and end flags must not be true at the same time, so we can copy lines here. 
        # even we can apply further filters.
        results.append(line);
    
    
    # close the file
    f.close();
    return results;


def search_tango_log2(log_file,start_time,end_time=None,filters=None):
    
    if(end_time is None):
        end_time = datetime.datetime.now();
    
    assert type(start_time) == datetime.datetime;
    assert type(end_time) == datetime.datetime;
    assert start_time < end_time;
    
    ts_pattern = re.compile('^(\d{4}-\d{2}-\d{2} \d\d:\d\d:\d\d)');
    
    results = [];
    
    f = open(log_file,'r');
    line = 'start';
    start_tag = False;
    while(line != ''):
        line = f.readline();
        ts = ts_pattern.findall(line)
        if(len(ts)!=0):
            ts = ts[0];
            ts = datetime.datetime.strptime(ts,'%Y-%m-%d %H:%M:%S');
            if(ts < start_time):
                continue
            elif(ts >= start_time and ts <= end_time):
                results.append(line);
                start_tag = True;
            else:
                break;
        else:
            if(start_tag == True):
                results.append(line)
            
    f.close();
    return results;


if __name__ == '__main__':
    pass