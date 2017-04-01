import socket
 
host = socket.gethostname() 
port = 13000
BUFFER_SIZE = 1024
MESSAGE = input("tcpClient: Enter message/ Enter exit:") 
 
tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpClient.connect((host, port))
 
while MESSAGE != 'exit':
    tcpClient.send(MESSAGE.encode("utf-8"))     
    data = tcpClient.recv(BUFFER_SIZE)
    print("Client2 received data:", data.decode('utf-8'))  #TWM added decode call to decode the incoming encoded message
    MESSAGE = input("tcpClient: Enter message to continue/ Enter exit:")
 
tcpClient.close()
