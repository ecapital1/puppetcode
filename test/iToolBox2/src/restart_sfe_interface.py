#!/usr/bin/python
'''
Created on 2011-9-30

@author: michael
'''

import sys, xmlrpclib

if __name__ == '__main__':
    
    rts_server = '10.128.1.12'
    control_port = 38580
    
    
    if(len(sys.argv) > 1):
        rts_server = sys.argv[1];
    else:
        print "Please input the RTS server IP: [Default is %s]"%rts_server;
        input = sys.stdin.readline();
        if(input != '\n'):
            rts_server = input
    
    rts_server = rts_server.strip();
    print "RTS Server: %s"%rts_server;
    
    print "WARNING, YOU ARE ABOUT TO RESTART SFE INTERFACE %s, CONTINUE[Y/N]?"%rts_server;
    input = sys.stdin.readline();
    
    flag = False;
    if(input.startswith('Y') or input.startswith('y')):
        rts_server_url = "http://%s:%d"%(rts_server,control_port);
        print "Connecting to RTS Server %s"%rts_server_url;
        server = xmlrpclib.ServerProxy(rts_server_url);
        print "Running SFE interface restarting scripts..."
        output = server.restart_sfe_interface();
        print output;
    else:
        print "No Action performed";