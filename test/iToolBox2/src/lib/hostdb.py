'''
Created on 2010-12-6

@author: michael
'''

import time, os, re
import xml.dom.minidom as mdom

class HostXMLDB(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.xmlSourceFile = False
        self.doc = False
        self.top = False
     
    
    def initHostDB(self):
        impl = mdom.getDOMImplementation()
        self.doc = impl.createDocument(None, "inventory", None)
        self.top = self.doc.documentElement
        # create admin entry
        self.top.appendChild(self.doc.createElement("admin"))
        # create timestamps
        ts = self.doc.createElement("last_update")
        ts.setAttribute("timestamp", str(int(time.time())))
        self.top.appendChild(ts)
        # create host list
        self.top.appendChild(self.doc.createElement("hosts"))
        

        
    def loadHostDBfromFile(self, fileName):
        retval = False
        if(os.path.exists(fileName)):
            ds = open(fileName,'r')
            raw = ds.read()
            raw = raw.replace('\n','').replace('\t','')
            self.doc = mdom.parseString(raw)
            self.top = self.doc.documentElement
            ds.close()
            retval = True
        else:
            self.initHostDB()
            retval = False
        self.xmlSourceFile = fileName
        return retval
            
        

    def saveHostDBtoFile(self, fileName=None):
        if(fileName is not None):
            self.xmlSourceFile = fileName
        self.updateTimeStamp()
        f = open(self.xmlSourceFile,'w')
        f.write(self.doc.toprettyxml())
        f.close()
            
    
    def updateTimeStamp(self):
        tss = self.top.getElementsByTagName("last_update")
        # should has time stamp already, if not, add it
        if(len(tss) == 0):
            ts = self.doc.createElement("last_update")
            ts.setAttribute("timestamp", str(int(time.time())))
            self.top.appendChild(ts)
        else:
            tss[0].setAttribute("timestamp", str(int(time.time())))  
    
    
    def updateAdminInfo(self, name, email=None, phone=None):
        admins = self.top.getElementsByTagName("admin")
        # should has account already, if not, add it
        admin = None
        if(len(admins) == 0):
            admin = self.doc.createElement("admin")
            self.top.appendChild(admin)
        else:
            admin = admins[0]
        admin.setAttribute("name", name)
        if(email is not None):
            admin.setAttribute("email", email)
        if(phone is not None):
            admin.setAttribute("phone", phone)
        
    
    def updateHostInfo(self,hostMac, hostName=None, hostDesc=None,hostIP=None):
        host_list = self.top.getElementsByTagName("host")
        target = None
        for host in host_list:
            if(host.getAttribute("MAC") == hostMac):
                target = host
                break
        # add this host object if it does not exist
        if(target is None):
            target = self.doc.createElement("host")
            h = self.top.getElementsByTagName("hosts")
            if(len(h) == 0):
                hosts = self.doc.createElement("hosts")
                self.top.appendChild(hosts)
                # should have "hosts" tag now
                h = self.top.getElementsByTagName("hosts")
            #add it to the DOM tree
            h[0].appendChild(target)
        target.setAttribute("MAC",hostMac)
        if(hostName is not None):
            target.setAttribute("name", hostName)
        if(hostDesc is not None):
            target.setAttribute("description", hostDesc)
        if(hostIP is not None):
            target.setAttribute("IP", hostIP)
        target.setAttribute("last_check",str(int(time.time())))
    
                
    def removeHostInfo(self,hostMac):
        hosts_nodes = self.top.getElementsByTagName("hosts")
        if(len(hosts_nodes) != 0):
            hosts = hosts_nodes[0]
            host_nodes = hosts.getElementsByTagName("host")
            for host in host_nodes:
                if(host.getAttribute("MAC") == hostMac):
                    hosts.removeChild(host)
                    return host        
     
    def updateFromNmapFile(self,nmap_file):
        file = open(nmap_file,'r')
        lines = file.readlines()
        file.close()
        return self.updateFromNmapString(lines)
     
    
    def updateFromNmapString(self,nmap_lines):
        currentIP = None
        currentMac = None
        ip_pattern = re.compile('(\d+\.\d+\.\d+\.\d+)')
        mac_pattern = re.compile('([0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2})')
        for line in nmap_lines:
            if(line.startswith("Nmap scan report for")):
                currentIP = ip_pattern.findall(line)[0]
            elif(line.startswith("MAC Address")):
                currentMac = mac_pattern.findall(line)[0]
            else:
                continue
            if(currentIP is not None and currentMac is not None):
                self.updateHostInfo(hostMac=currentMac, hostIP=currentIP)
                currentIP = None
                currentMac = None
        return True       
     
               
    def getlastUpdate(self):
        nodes = self.top.getElementsByTagName("last_update")
        if(len(nodes) == 0):
            return None
        
        return nodes[0].getAttribute("timestamp")
        
    def getAllHosts(self):
        host_arr = []
        hosts = self.top.getElementsByTagName("host")
        for host in hosts:
            host_dict = {}
            host_dict['name'] = host.getAttribute("name")
            host_dict['MAC'] = host.getAttribute("MAC")
            host_dict['last_check'] = int(host.getAttribute("last_check"))
            host_dict['IP'] = host.getAttribute("IP")
            host_dict['description'] = host.getAttribute('description')
            host_arr.append(host_dict)
        return host_arr
               
    
        