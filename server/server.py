import threading
import socket
import queue

class Client(threading.Thread):

	def __init__(self, conn_socket, ip, port):
		Thread.__init__(self)
		self.running = True;
		self.port = port
		self.ip = ip
		self.conn_socket = conn_socket

	def run(self):
		while self.running:
			data = self.conn_socket.recv(2048)
			print ("Server recieved data: ", data)
			self.conn_socket.send("Message recieved")

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
			if self.threads.len() + 1 > Server.MAX_CLIENT_COUNT:
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
