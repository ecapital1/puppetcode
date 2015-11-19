#!/usr/bin/python
'''
Created on 2011-7-4

@author: michael
'''
import time, os, sys
import lib.commonutils as cutils;
from ConfigParser import ConfigParser

# Generic Variables
program = 'schedule_nagios_downtime'
log_name = '/tmp/' + program + time.strftime("%Y%m%d.%H%M%S")
ver = '0.1'


config_file = 'nagios_downtime.config'
nagios_cmd_file = '/var/lib/nagios3/rw/nagios.cmd';

def schedule_svc_downtime(host,service,start_time,end_time=None,fixed='false',trigger_id=0,duration=0,author='nagiosadmin',comment=''):
    
    ts = int(time.time());
    date_str = time.strftime("%Y%m%d");
    
    s_time = time.strptime("%s %s"%(date_str,start_time), "%Y%m%d %H:%M:%S");
    start_stamp = int(time.mktime(s_time));
    
    if(end_time is None):
        end_stamp = int(start_stamp + 3600);
    else:
        e_time = time.strptime("%s %s"%(date_str,end_time), "%Y%m%d %H:%M:%S");
        end_stamp = int(time.mktime(e_time));
        
    if(fixed == 'false'):
        fixed = 0;
    else:
        fixed = 1;
        
    cmd = '[%s] SCHEDULE_SVC_DOWNTIME;%s;%s;%s;%s;%s;%s;%s;%s;%s\n'%(ts,host,service,start_stamp,end_stamp,fixed,trigger_id,duration,author,comment);
    print 'COMMAND IS: %s'%cmd;
    
    
    f = open(nagios_cmd_file,'w');
    f.write(cmd);
    f.close();
    return 0;


if __name__ == '__main__':
    
    
    if(len(sys.argv)>1):
        config_file = sys.argv[1];
    
    
    if(not os.path.exists(config_file)):
        print "cannot find config file %s"%config_file;
        sys.exit(1);
    
    logger = cutils.Logger()
    logger.openLog(log_name)
    
    logger.log("=====================Start running %s=====================================" % program);
    
    logger.log("loading config file");
    config = ConfigParser();
    config.read(config_file);
    
    defaults= config.defaults();
    nagios_cmd_file = defaults['command_file'];
    logger.log("Nagios command file is %s"%nagios_cmd_file);
    
    
    for sec in config.sections():
        logger.log('reading section %s'%sec);
        type = config.get(sec, 'type');
        if(type == 'service'):
            server = config.get(sec,'server');
            svc= config.get(sec,'service');
            start_time = config.get(sec,'start_time');
            end_time = config.get(sec,'end_time');
            fixed = config.get(sec,'fixed');
            trigger_id = config.get(sec,'trigger_id');
            duration = config.get(sec,'duration');
            author = config.get(sec,'author');
            comment = config.get(sec,'comment');
            
            
            logger.log("server:%s"%server);
            logger.log("service:%s"%svc);
            logger.log("start time: %s"%start_time);
            logger.log("end time: %s"%end_time);
            logger.log("fixed: %s" %fixed);
            logger.log("trigger_id: %s" %trigger_id);
            logger.log("duration: %s" %duration);
            logger.log("author: %s" %author);
            logger.log("comment: %s" %comment);
            
            logger.log("scheduling downtime service in nagios")
            retval = schedule_svc_downtime(host=server,service=svc,start_time=start_time,end_time=end_time,fixed=fixed,trigger_id=trigger_id,duration=duration,author=author,comment=comment);
            logger.log("nagios return code: %d"%retval);
    
    
    
    logger.log("=======================End running %s=====================================" % program)
    logger.closeLog()
    sys.exit(0)