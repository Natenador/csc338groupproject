import threading
import socket
import queue
import login_server as login

class Client(threading.Thread):

	def __init__(self, conn_socket, ip, port):
		threading.Thread.__init__(self)
		self.running = True
		self.port = port
		self.ip = ip
		self.conn_socket = conn_socket

		#Login variables
		self.authorized = False
		self.userData = []

	def run(self):
		userList = login.readUserList()
		#Send authorization code to client
		self.conn_socket.send('AUTH'.encode('utf-8'))
		userData = ''
		#While NOT authorized
		while(self.authorized == False):
			#Receive username and password from client
			userData = self.conn_socket.recv(2048)
			userData = userData.decode('utf-8')
			#split userData string into name & password, then put them into a list.
			name, pword = userData.split(':')
			userData = [name, pword]
			#Check if the authorization passes
			authFlag = login.signIn(userData, userList)
			if authFlag == 0: #username and password match
				print("\nUser signed in: ", userData[0])
				self.conn_socket.send('AUTH_PASS'.encode('utf-8')) #send authorization pass to client
				self.userData = userData
				self.authorized = True
			elif authFlag == 1: #incorrect password
				self.conn_socket.send('AUTH_FAIL'.encode('utf-8')) #send authorization fail to client
				print("\nUser failed password attempt: ", userData[0])
			else: #User created
				print("\nUser created: ", userData[0])
				self.conn_socket.send('AUTH_PASS'.encode('utf-8')) #send authorization pass to client
				self.userData = userData
				self.authorized = True



		while self.running:
			data = self.conn_socket.recv(2048)
			print ("Server recieved data: %s -> %s" % (userData[0], data.decode('utf-8'))) #TWM added a decode call to decode the encoded message
			self.conn_socket.send("Message recieved".encode('utf-8'))
			print('Server sent notification')

	def sendMessage(self, message):
		self.conn_socket.send(message)

	def disconnect(self):
		self.running = False

	def connect(self):
		self.running = True

class Server:
	
	TCP_IP = "0.0.0.0"
	SERVER_LISTEN_PORT = 13000
	BUFFER_SIZE = 1024
	MAX_CLIENT_COUNT = 20

	def __init__(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((Server.TCP_IP, Server.SERVER_LISTEN_PORT))
		self.threads = []
		self.message_queue = queue.Queue()
		self.running = True

	def start(self):
		print ("Starting server...")
		while self.running:
			self.server.listen(4)
			print ("Waiting for a connection...")
			(conn, (ip, port)) = self.server.accept()
			newthread = Client(conn, ip, port)
			newthread.start()
			if len(self.threads) + 1 > Server.MAX_CLIENT_COUNT:	#TWM fixed len(self.threads)
				newthread.sendMessage("I'm sorry, there are too many connections to the server at the moment. Please try again later.")
				newthread.disconnect()
			else:
				self.threads.append(newthread)

		for t in self.threads:
			t.join()

	def disconnect(self):
		self.running = False

	def connect(self):
		self.running = True

		
def main():

	server = Server()
	server.start()
	
if __name__ == "__main__":
	main()
