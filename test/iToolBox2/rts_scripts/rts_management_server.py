#!/usr/bin/python

# this is a network server that responds to tango requests

# author Patrick Roughan on 18/09/2012

import os
from twisted.internet import reactor, protocol
from twisted.protocols import basic

def logout(input, protocol):
        logged = os.popen('/opt/rts/tango/scripts/tangosrvutil info | grep '+ input[0] +' | wc -l').readline().strip()
        if logged == '1':
                result = "User Logged In\n logging user out now"
                os.popen('/opt/rts/tango/scripts/tangosrvutil logout ' + data)
        else:
                result = "User Not Logged In"

        protocol.sendLine(result)

def getLog(input, protocol):
	f = open('/home/patrick/repo/iToolBox2/rts_scripts/log.txt','r')
	while 1:
		line = f.readline()
		if not line:
			break
		protocol.sendLine(line)
	f.close()

handlers = dict([("logout", logout),("log", getLog)])

class command(basic.LineOnlyReceiver):

	def __init__(self):
		self.params = []	

	def lineReceived(self, line):
		if len(line) != 0:
			self.params.append(line)
		else:
			result = handlers[self.params[0]](self.params[1:], self)	
			self.params = []
			self.sendLine("EOF")

def main():
    """This runs the protocol on port 8000"""
    factory = protocol.ServerFactory()
    factory.protocol = command
    reactor.listenTCP(8000,factory)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()

