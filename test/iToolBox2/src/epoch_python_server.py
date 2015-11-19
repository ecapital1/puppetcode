#!/usr/bin/python
'''
Created on 2011-8-18

@author: michael
'''


import SimpleXMLRPCServer
from lib.tango import search_tango_log2, get_latest_tango_log
from lib.commonutils import run_cmd_get_code;
import ConfigParser, datetime, time, sys


def restart_rts():
    log_file = '/tmp/rts_restart.%s'%time.strftime("%y%m%d%H%M%S");
    cmd = '/srv/ittools/python/shell/rts_restart >%s 2>&1'%log_file
    # run the shell script and save the output to the log file
    run_cmd_get_code(cmd);
    
    # read the result and present to client
    f = open(log_file,'r');
    result = f.read();
    f.close();
    return result;
    
    

def restart_sfe_interface():
    log_file = '/tmp/interface_restart.%s'%time.strftime("%y%m%d%H%M%S");
    cmd = '/srv/ittools/python/shell/interface_restart >%s 2>&1'%log_file
    # run the shell script and save the output to the log file
    run_cmd_get_code(cmd);
    
    # read the result and present to client
    f = open(log_file,'r');
    result = f.read();
    f.close();
    return result;

def force_log_out_rtd():
    log_file = '/tmp/force_log_out_rtd.%s'%time.strftime("%y%m%d%H%M%S");
    cmd = '/srv/ittools/python/shell/force_log_out_rtd >%s 2>&1'%log_file;
    # run the shell script and save the output to the log file
    run_cmd_get_code(cmd);
    
    # read the result and present to client
    f = open(log_file,'r');
    result = f.read();
    f.close();
    return result;
    

def latest_tango_log(start_ts,end_ts):
    tango_log = get_latest_tango_log();
    print "Latest tango log: %s"%tango_log;
    start = datetime.datetime.fromtimestamp(time.mktime(time.strptime(start_ts,'%Y%m%d%H%M%S')));
    end = datetime.datetime.fromtimestamp(time.mktime(time.strptime(end_ts,'%Y%m%d%H%M%S')));
    return search_tango_log2(tango_log, start, end);

def main():    
    config = ConfigParser.ConfigParser();
    config.read(sys.argv[1]);
    
    setting = config.defaults();
    bind_ip = setting['bind_ip'];
    bind_port = setting['bind_port'];
    
    server = SimpleXMLRPCServer.SimpleXMLRPCServer((bind_ip,int(bind_port)));
    server.register_function(latest_tango_log);
    server.register_function(force_log_out_rtd);
    server.register_function(restart_sfe_interface);
    server.register_function(restart_rts);
    server.serve_forever();

if __name__ == '__main__':
    main();
    
