#!/usr/bin/python
'''
Created on 2010-12-7

@author: michael
'''
import os, time, sys
from optparse import OptionParser
from lib.hostdb import HostXMLDB
import lib.commonutils as cutils

# Generic Variables
program = 'scan_host'
log_name = program + time.strftime("%Y%m%d.%H%M%S")
ver = '0.1'

host_xml_db = None
scan_file = None
scan_network = None

# Functions for this script only.

def dumpHosts(db,logger):
    logger.log("Dumping all hosts information from XML file")
    hosts = db.getAllHosts()
    logger.log("%-15s%-20s%-20s%-20s%-20s"%('NAME','MAC','IP','LAST_CHECK','DESCRIPTION'))
    for host in hosts:
        date_fmt = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(host['last_check'])))
        logger.log("%-15s%-20s%-20s%-20s%-20s"%(host['name'],host['MAC'],host['IP'], date_fmt, host['description']))
    return True


################################################################
# Main route starts from here
################################################################
if __name__ == "__main__":
    ################################################################
    # Parsing and checking parameters
    ################################################################
    parser = OptionParser(description='invoke',prog=program,version=ver)
    parser.add_option('-l','--log', metavar='log',dest='log', help='log file for this script')
    parser.add_option('-d','--database', metavar='db',dest='db', help='XML database for hosts information')
    parser.add_option('-s','--scan_file', metavar='scan_file', dest='scan_file', help='nmap scan result file')
    parser.add_option('-n','--network', metavar='network', dest='network', help='network for nmap to scan')
    parser.add_option('--dump', action="store_true", dest='dump', help='just print out hosts information', default=False)
    
    (options, args) = parser.parse_args(sys.argv)
    
    if(options.log):
        log_name = options.log
        
    if(options.db):
        host_xml_db = options.db
        
    if(options.network):
        scan_network = options.network
        
    if(options.scan_file):
        scan_file = options.scan_file
        if(not os.path.exists(scan_file)):
            print "Cannot locate nmap scan file"
            sys.exit(1)
            
    if(host_xml_db is None):
        print "hosts database file not specified."
        sys.exit(1)
    
    logger = cutils.Logger()
    logger.openLog(log_name)
    logger.log("=====================Start running %s====================================="%program)
    
    db = HostXMLDB()
    logger.log("opening Host XML database file %s" %host_xml_db)
    retval = db.loadHostDBfromFile(host_xml_db)
    if(retval is True):
        logger.log("Hosts data have been loaded.")
    else:
        logger.log("Host XML file does not exist, new empty xml file %s is created" %host_xml_db)
    
    if(options.dump):
        dumpHosts(db,logger)
        
     
    if(scan_file is not None):
        logger.log('updating XML database with nmap scan result file %s'%scan_file)
        db.updateFromNmapFile(scan_file)
        db.saveHostDBtoFile()
        logger.log('XML database %s has been updated'%host_xml_db)
    
    if(scan_network is not None):
        logger.log("preparing for scanning network %s"%scan_network)
        logger.log("checking whether nmap is installed")
        retval = cutils.run_cmd_get_code("which nmap")
        logger.check_status_code(retval, "nmap program is not installed")
        cmd = "sudo nmap -sP %s" %scan_network
        logger.log('Issuing cmd %s' %cmd)
        logger.log('waiting for nmap scan finishing...')
        (out, err) = cutils.run_cmd_get_output(cmd)
        if(err != ''):
            logger.log('Nmap Error: %s' %err)
            sys.exit(1)
        logger.log('nmap output: \n %s' %out)
        logger.log("updating XML database according to nmap ouput")
        db.updateFromNmapString(out.split('\n'))
        db.saveHostDBtoFile()
        logger.log('XML database %s has been updated'%host_xml_db)
        
    logger.log("=======================End running %s====================================="%program)
    logger.closeLog()
    sys.exit(0)
    
    
        
    
    