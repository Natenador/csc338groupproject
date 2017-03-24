import threading
import socket
import queue

class Client(Thread):

    def __init__(self, conn_socket, ip, port):
        Thread.__init__(self)
        self.running = True;
        self.port = port
        self.ip = ip
        self.conn_socket = conn_socket

    def run(self):
        while self.running:
            data = self.conn_socket.recv(2048)
            print "Server recieved data: ", data
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

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((TCP_IP, SERVER_LISTEN_PORT))
        self.threads = []
        self.message_queue = queue.Queue()
        self.running = True

    def start(self):
        print "Starting server..."
        while self.running:
            self.server.listen(4)
            print "Waiting for a connection..."
            (conn, (ip, port)) = self.server.accept()
            newthread = Client(conn, ip, port)
            newthread.start()
            self.threads.append(newthread)

        for t in self.threads:
            t.join()

    def disconnect(self):
        self.running = False

    def connect(self):
        self.running = True
