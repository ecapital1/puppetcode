#!/usr/bin/python
'''
Created on 2011-8-19

@author: michael
'''

import sys, xmlrpclib, re, time

def get_timestamp(input):
    timestamp = None;
    if(re.match('^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',input)):
        ts = re.findall('^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',input);
        timestamp = time.strftime('%Y%m%d%H%M%S',time.strptime(ts[0], '%Y-%m-%d %H:%M:%S'));
    elif(re.match('^(\d{2}:\d{1,2}:\d{1,2})',input)):
        ts = re.findall('^(\d{1,2}:\d{1,2}:\d{1,2})',input);
        d = time.strftime('%Y%m%d');
        t = time.strftime('%H%M%S',time.strptime(ts[0],'%H:%M:%S'));
        timestamp = '%s%s'%(d,t);
    elif(re.match('^(\d{1,2}:\d{1,2})',input)):
        ts = re.findall('^(\d{1,2}:\d{1,2})',input);
        d = time.strftime('%Y%m%d');
        t = time.strftime('%H%M%S',time.strptime(ts[0], '%H:%M'));
        timestamp = '%s%s'%(d,t);
    
    return timestamp


def main():
    
    tango_server = '192.168.2.55'
    tango_port = 38580
    
    print "Please input the tango server IP: [Default is %s]"%tango_server;
    input = sys.stdin.readline();
    if(input != '\n'):
        tango_server = input
    tango_server = tango_server.strip();
    print "Tango Server: %s"%tango_server;
    
    s_time = None
    while(s_time is None):
        print "Please input Start Time: [Format: 2011-08-23 08:00:00 OR 9:04:20 OR 6:20 if it is today]"
        input = sys.stdin.readline();
        s_time = get_timestamp(input);
        if(s_time is not None):
            break;
        print "Cannot parse the input time"   
    print "Start timestamp: %s"%s_time;
    
    
    e_time = None;
    while(e_time is None):
        print "Please input End Time: [Format: 2011-08-23 08:00:00 OR 9:04:20 OR 6:20 if it is today]"
        input = sys.stdin.readline();
        e_time = get_timestamp(input);
        if(e_time is not None):
            break;
        print "Cannot pare the input time"
    print "End timestamp: %s"%e_time;
    
    
    output_file = 'tango.log';
    print "Please input the output file, [Default is %s]"%output_file;
    input = sys.stdin.readline();
    if(input != '\n'):
        output_file = input.rstrip();
    print "Output file is %s"%output_file;
    
    tango_server_url = "http://%s:%d"%(tango_server,tango_port);
    print "Connecting to Tango Server %s"%tango_server_url;
    server = xmlrpclib.ServerProxy(tango_server_url);
    print "Fetching logs..."
    result = server.latest_tango_log(s_time,e_time);
    
    print "saving to %s..."%output_file;
    f = open(output_file,'w');
    for line in result:
        f.write(line);
    f.close();
    
    print "DONE!";
    
    
    
    
    
    
    pass
    

if __name__ == '__main__':
    main();
