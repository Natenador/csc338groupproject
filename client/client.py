import socket
import login_client as login

host = socket.gethostname() 
port = 13000
BUFFER_SIZE = 1024
MESSAGE = ''
server_msg = ''
userData =''

tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpClient.connect((host, port))
 
server_msg = tcpClient.recv(BUFFER_SIZE)

while MESSAGE != 'exit':
	#Check to see if user credentials are required by server
	if (server_msg.decode('utf-8') == 'AUTH'):
		userData = login.signIn()
		name, pword = userData.split(':')
		tcpClient.send(userData.encode('utf-8'))
		userData = [name, pword]		
		server_msg = tcpClient.recv(BUFFER_SIZE)
		if server_msg.decode('utf-8') == 'AUTH_PASS':
			print("\nSigned in as: ", name)
	#Check if credentials fail
	elif (server_msg.decode('utf-8') == 'AUTH_FAIL'):
		print("\nIncorrect password.")
		server_msg = 'AUTH'.encode('utf-8')

	else:
		MESSAGE = input("tcpClient: Enter message to continue/ Enter exit:")
		tcpClient.send(MESSAGE.encode("utf-8"))
		server_msg = tcpClient.recv(BUFFER_SIZE)
		message_recv = server_msg #Received message tied to userId of sender
		print("%s received server_msg:", server_msg.decode('utf-8'))  #TWM added decode call to decode the incoming encoded message

tcpClient.close()
