import threading
import socket
import queue
import logging
import time
import login_server as login

TOO_MANY_CONNECTIONS_ERROR = "/e:-1"
LIST_OF_NAMES_MESSAGE = "/names:"

CONNECTION_MADE_MESSAGE = "Connected!"

AUTHORIZATION_REQUIRED = "AUTH_REQ"
AUTHORIZATION_PASS = "AUTH_PASS"
AUTHORIZATION_FAIL = "AUTH_FAIL"

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

#Goes through every client and appends each client name to a string, separated by a ':'
def getClientNames(clients):
    names = ""
    for client in range(len(clients)):
        names += clients[client].userData[0]
        if client != len(clients) - 1:
            names += ":"
    return names 

class ClientThread(threading.Thread):        
        def __init__(self, id, conn_socket, ip, port, clients):
                threading.Thread.__init__(self)
                self.id = id
                self.running = True
                self.port = port
                self.ip = ip
                self.conn_socket = conn_socket
                self.other_connections = clients

                #TWM - Login variables
                self.authorized = False
                self.userData = ['',''] #userData[0] == username | userData[1] == password

        def run(self):
                self.signIn()
                self.other_connections.append(self)
                self.broadcastToAll(LIST_OF_NAMES_MESSAGE + getClientNames(self.other_connections)) 
                logging.debug("%s: Adding %s to the list of connected clients", now(LOG), self.userData[0])
                logging.debug("%s: FROM CLIENT -- There are now %d connections to this server", now(LOG), len(self.other_connections))
                while self.running:
                        try:
                            message = self.conn_socket.recv(MAX_MESSAGE_SIZE).decode("utf-8")
                            if message == "exit":
                                self.conn_socket.send(message.encode('utf-8'))
                                self.running = False
                                logging.info("%s: %s has disconnected...", now(LOG), self.userData[0])
                            elif message != '':
                                logging.info ("%s: Server recieved data: %s", now(LOG), message)
                                id_message = self.userData[0] + ": " + message
                                self.broadcast(id_message)
                        except socket.error as se:
                            logging.warn("%s: %s has disconnected. May be a normal log off : %s", now(LOG), self.userData[0], se)
                            self.running = False
                            self.conn_socket.close()
                #if not running, remove from the list
                self.other_connections.remove(self)
                self.broadcastToAll(LIST_OF_NAMES_MESSAGE + getClientNames(self.other_connections)) 
                logging.debug("%s: %s has been removed from the list of clients", now(LOG), self.userData[0])


        def sendMessage(self, message):
                self.conn_socket.send(message.encode("utf-8"))

        def disconnect(self):
                self.running = False

        def connect(self):
                self.running = True

        def broadcast(self, message):
                logging.info("%s: %s is sending '%s' to all clients but itself", now(LOG), self.userData[0], message)
                for client in self.other_connections:
                        if client.id != self.id and client.running:
                                client.sendMessage(message)
        def broadcastToAll(self, message):
            logging.info("%s: %s is sending '%s' to all clients including itself", now(LOG), self.userData[0], message)
            for client in self.other_connections:
                client.sendMessage(message)

        #TWM - signIn functionality for login
        #Requests user credentials from client - sets userData equal to these credentials
        #Checks data file to see if they match
        #Sign in if match | Request new credentials if no match | create new user if no match is found
        def signIn(self):
            #Send authorization code to client
            logging.debug("%s: Authorization required for user %s", now(LOG), self.userData[0])
            self.conn_socket.send(AUTHORIZATION_REQUIRED.encode('utf-8'))
            #While NOT authorized
            while(self.authorized == False):
                #Receive username and password from client
                self.userData = self.conn_socket.recv(2048)
                self.userData = self.userData.decode('utf-8')
                #split userData string into name & password, then put them into a list.
                name, pword = self.userData.split(':')
                self.userData = [name, pword]
                logging.debug("%s: Credentials sent from %s -- {username: %s, password: %s}", now(LOG), self.ip, name, pword)
                #Check if the authorization passes
                authFlag = login.checkCreds(self.userData)
                if authFlag == 0: #username and password match
                    logging.info("%s: User signed in: %s", now(LOG), self.userData[0])
                    self.conn_socket.send(AUTHORIZATION_PASS.encode('utf-8')) #send authorization pass to client
                    self.authorized = True
                elif authFlag == 1: #incorrect password
                    self.conn_socket.send(AUTHORIZATION_FAIL.encode('utf-8')) #send authorization fail to client
                    logging.info("%s: User failed password attempt: %s", now(LOG), self.userData[0])
                else: #User created
                    logging.info("%s: User created: %s", now(LOG), self.userData[0])
                    self.conn_socket.send(AUTHORIZATION_PASS.encode('utf-8')) #send authorization pass to client
                    self.authorized = True



class Server:
    
    TCP_IP = "0.0.0.0"
    CURRENT_CONNECTION_ID = 0
    SERVER_LISTEN_PORT = 13000
    BUFFER_SIZE = 1024
    MAX_CLIENT_COUNT = 2

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

            try:
                self.server.listen(4)
                logging.info ("%s: Waiting for a connection...", now(LOG))
                (conn, (ip, port)) = self.server.accept()
                logging.info ("%s: Incoming connection attempt at %s on port %d", now(LOG), ip, port)
                if len(self.clients) + 1 > Server.MAX_CLIENT_COUNT:
                    logging.info("%s: Too many connections, not allowing connections from %s", now(LOG), ip)
                    conn.send(TOO_MANY_CONNECTIONS_ERROR.encode("utf-8"))
                else:
                    conn.send(CONNECTION_MADE_MESSAGE.encode("utf-8"))
                    newthread = ClientThread(Server.CURRENT_CONNECTION_ID, conn, ip, port, self.clients)
                    Server.CURRENT_CONNECTION_ID += 1
                    newthread.start()
                    logging.debug("%s: FROM SERVER -- After starting the new client, there are now %d clients connected", now(LOG), len(self.clients))
            except socket.error as se:
                logging.error("%s: Something went wrong while waiting for a connection: %s", now(LOG), se)

            for client in self.clients:
                client.other_connections = self.clients

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
