import socket

TOO_MANY_CONNECTIONS_ERROR = "/e:-1"

#Takes the message from the server as an input
#If the message equals any error, print the error and stop the loop to end the program
#Otherwise print the message.
def isError(message):
    if message == TOO_MANY_CONNECTIONS_ERROR:
        print ("There are currently too many connections to this server, please try again later.")
        return True
    else:
        return False
    
host = socket.gethostname() 
port = 13000
BUFFER_SIZE = 1024
ERROR = False
MESSAGE = input("tcpClient: Enter message/ Enter exit:") 
 
tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpClient.connect((host, port))
 
while MESSAGE != 'exit' and not ERROR:
    tcpClient.send(MESSAGE.encode("utf-8"))     
    data = tcpClient.recv(BUFFER_SIZE)
    if isError(data.decode("utf-8")):
        ERROR = True
    else:
        print(data.decode())
        MESSAGE = input("tcpClient: Enter message to continue/ Enter exit:")
 
tcpClient.close()
