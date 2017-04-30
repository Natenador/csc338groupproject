import socket
from threading import Thread, Lock
import time

def getCreds():
	name = input('Enter user name: ')
	password = input('Enter password: ')
	userData = name + ':' + password
	return userData

class Client:
	host = socket.gethostname() 
	port = 13000
	BUFFER_SIZE = 1024
	message_storage = []
	mutex = Lock()

	def __init__(self):
		self.running = True
		self.incoming_mssg = ''
		self.outgoing_mssg = ''
		#User login info
		self.userData = ''

	def recvMssgs(self, tcp):
		running = True
		try:
			tcpClient = tcp
			storage = []
			while self.running:
				storage.append(tcpClient.recv(Client.BUFFER_SIZE))
				if (len(storage) != 0):
					Client.mutex.acquire()
					while(len(storage) != 0):				
						Client.message_storage.append(storage.pop(0))
					Client.mutex.release()
		except:
			running = False
	def start(self):
		tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		tcpClient.connect((Client.host, Client.port))
		
		recvThread = Thread(target = Client.recvMssgs, name = 'mssg_thread', args = [self, tcpClient])
		recvThread.start()

		while(len(Client.message_storage) == 0):
			print("\nWaiting on a message")
		self.incoming_mssg = Client.message_storage.pop(0)

		while self.outgoing_mssg != 'exit':
			#Check to see if user credentials are required by server
			if (self.incoming_mssg.decode('utf-8') == 'AUTH'):
				self.userData = getCreds() #Prompts user for credentials
				name, pword = self.userData.split(':')
				tcpClient.send(self.userData.encode('utf-8')) #Sends those credentials to server
				self.userData = [name, pword]		
				#incoming_mssg.= tcpClient.recv(Client.BUFFER_SIZE)
				while len(Client.message_storage) == 0:
					print("\nWaiting on server authentication...")
				self.incoming_mssg = Client.message_storage.pop(0)

				if self.incoming_mssg.decode('utf-8') == 'AUTH_PASS': #If server accepts those credentials : sign in
					print(self.incoming_mssg.decode('utf-8'))
					print("\nSigned in as: ", name)
			#Check if credentials fail
			elif (self.incoming_mssg.decode('utf-8') == 'AUTH_FAIL'): #If server denies those credentials : request new credentials
				print("\nIncorrect password.")
				self.incoming_mssg = 'AUTH'.encode('utf-8')

			else:
				if (len(Client.message_storage) != 0):
					Client.mutex.acquire()
					while len(Client.message_storage) != 0:
						self.incoming_mssg = Client.message_storage.pop(0)
						print('\n', self.incoming_mssg)
					Client.mutex.release()
				self.outgoing_mssg = input("tcpClient: Enter message to continue/ Enter exit:")
				tcpClient.send(self.outgoing_mssg.encode("utf-8"))
		self.running = False
		tcpClient.close()

def main():
	client = Client()
	client.start()

if __name__ == "__main__":
	main()