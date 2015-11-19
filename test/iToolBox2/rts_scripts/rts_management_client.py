#!/usr/bin/python

from twisted.internet import reactor, protocol
from twisted.protocols import basic
import sys, time

class menu:

	def options(self):

		print "\nPlease Choice An Option from the list below:\n"
		print "\t(1) Logout Tango User\n"
		print "\t(2) Getting Tango Log\n"

		self.choice = sys.stdin.readline().strip()
		l = log()

		op = [logoutCommand, log]

		return op[int(self.choice) - 1]()
			
class command(basic.LineOnlyReceiver):

        def lineReceived(self, data):
                print "\nServer said: ", data
					

        def connectionLost(self, reason):
                print "\nconnection closed"

class logoutCommand(command):	
	
	def __init__(self):
		
		print ("\nPlease enter a user to log out: \n")
		self.username = sys.stdin.readline().strip()

		print ("\nAre you sure you want to logout " + self.username + " from \n")
		print ("Y/N: \n")
		self.confirmation = sys.stdin.readline().strip().lower()

		if self.confirmation == 'y':
			
			return

		elif self.confirmation == 'n':
        		sys.exit()

		else:
        		print("\nYou entered a incorrect character please try again")
        		time.sleep(5)
       			sys.exit()

	def connectionMade(self):
		self.sendLine("logout")
                self.sendLine(self.username)
		self.sendLine("")
	
	def lineReceived(self, line):
		if line == "EOF":
			self.transport.loseConnection()
		else:
			print line

class log(command):

	def connectionMade(self):
                self.sendLine("log")
                self.sendLine("")
		
	def dataReceived(self, data):
                if data == "EOF":
                	self.transport.loseConnection()
                else:
                        f = open("/tmp/log.txt","w")
			f.write(data)
			f.close()

class EchoFactory(protocol.ClientFactory):

	def __init__(self, command):
		self.command = command

	def buildProtocol(self, addr):
		return self.command

        def clientConnectionFailed(self, connector, reason):
                print "\nConnection failed - goodbye!"
                reactor.stop()

        def clientConnectionLost(self, connector, reason):
                print "\nConnection closed - goodbye!"
                reactor.stop()
                time.sleep(5)


def main():

	print "\nWelcome to the RTS Management Script\n This Script Will add you to control multiple aspects of RTS/Tango\n"
	print ("Please enter the RTS Server IP you want: \n")
        serverip = sys.stdin.readline().strip()
	m = menu()
	o = m.options()
	f = EchoFactory(o)
	reactor.connectTCP(serverip, 8000, f)
	reactor.run()

if __name__ == '__main__':
	main()
