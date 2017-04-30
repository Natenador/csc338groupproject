import threading
import socket
import queue
import logging
import time

TOO_MANY_CONNECTIONS_ERROR = "/e:-1"

CONNECTION_MADE_MESSAGE = "Connected!"


MAX_MESSAGE_SIZE = 2048

#Date time formats
MMDDYYYY_HHMMSS = "MM/DD/YYYY HH:MM:SS"
TIME = "HH:MM:SS"
DAY = "MM/DD/YYYY"
LOG_NAME = "MMDDYYYY.HHMMSS"
LOG = MMDDYYYY_HHMMSS

def now(date_format):
    today = time.localtime(time.time())

    #by default, mmddyyyy_hhmmss
    month = str(today[1])
    day = str(today[2])
    year = str(today[0])
    hour = str(today[3])
    minute = str(today[4])
    second = str(today[5])
    if int(month) < 10:
        month = "0" + month
    if int(day) < 10:
        day = "0" + day
    if int(hour) < 10:
        hour = "0" + hour
    if int(minute) < 10:
        minute = "0" + minute
    if int(second) < 10:
        second = "0" + second

    date = month + "/" + day + "/" + year
    timez = hour + ":" + minute + ":" + second
    now = date + " " + timez
    if date_format == TIME:
        now = timez

    if date_format == DAY:
        now = date

    if date_format == LOG_NAME:
        now = year + day + month + "." + hour + minute + second

    return now
 

class ClientThread(threading.Thread):

        
        def __init__(self, id, username, conn_socket, ip, port, clients):
                threading.Thread.__init__(self)
                self.id = id
                self.username = username
                self.running = True
                self.port = port
                self.ip = ip
                self.conn_socket = conn_socket
                self.other_connections = clients

        def run(self):
                while self.running:
                        try:
                            message = self.conn_socket.recv(MAX_MESSAGE_SIZE).decode("utf-8")
                            if message == "exit":
                                self.running = False
                                logging.info("%s: %s has disconnected...", now(LOG), self.username)
                            else:
                                logging.info ("%s: Server recieved data: %s", now(LOG), message)
                                id_message = self.username + ": " + message
                                self.broadcast(id_message)
                        except socket.error as se:
                            logging.warn("%s: %s has disconnected. May be a normal log off : %s", now(LOG), self.username, se)
                            self.running = False
                            self.conn_socket.close()


        def sendMessage(self, message):
                self.conn_socket.send(message.encode("utf-8"))

        def disconnect(self):
                self.running = False

        def connect(self):
                self.running = True

        def broadcast(self, message):
                logging.info("%s: %s is sending '%s' to all clients", now(LOG), self.username, message)
                for client in self.other_connections:
                        if client.id != self.id and client.running:
                                client.sendMessage(message)



class Server:
    
    TCP_IP = "0.0.0.0"
    CURRENT_CONNECTION_ID = 0
    SERVER_LISTEN_PORT = 13000
    BUFFER_SIZE = 1024
    MAX_CLIENT_COUNT = 20

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((Server.TCP_IP, Server.SERVER_LISTEN_PORT))
        self.clients = []
        self.running = True

        #Logging setup
        logging.basicConfig(filename="../logging/serverlogs/server." + now(LOG_NAME) + ".log", level=logging.DEBUG)

    def start(self):
        logging.info("%s: Starting server...", now(LOG))
        while self.running:
            self.server.listen(4)
            logging.info ("%s: Waiting for a connection...", now(LOG))
            (conn, (ip, port)) = self.server.accept()
            username = conn.recv(MAX_MESSAGE_SIZE).decode("utf-8").split(':')[1]
            logging.info ("%s: Made a connection with %s at %s on port %d", now(LOG), username, ip, port)
            if len(self.clients) + 1 > Server.MAX_CLIENT_COUNT:
                conn.send(TOO_MANY_CONNECTIONS_ERROR.encode("utf-8"))
            else:
                conn.send(CONNECTION_MADE_MESSAGE.encode("utf-8"))
                newthread = ClientThread(Server.CURRENT_CONNECTION_ID, username, conn, ip, port, self.clients)
                newthread.start()
                self.clients.append(newthread)
                Server.CURRENT_CONNECTION_ID += 1

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
