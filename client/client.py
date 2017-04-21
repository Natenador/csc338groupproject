import socket
import login_client as login

host = socket.gethostname() 
port = 13000
BUFFER_SIZE = 1024
MESSAGE = ''
server_msg = ''

#User login info
userData =''

tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpClient.connect((host, port))
 
server_msg = tcpClient.recv(BUFFER_SIZE)

while MESSAGE != 'exit':
	#Check to see if user credentials are required by server
	if (server_msg.decode('utf-8') == 'AUTH'):
		userData = login.getCreds() #Prompts user for credentials
		name, pword = userData.split(':')
		tcpClient.send(userData.encode('utf-8')) #Sends those credentials to server
		userData = [name, pword]		
		server_msg = tcpClient.recv(BUFFER_SIZE)
		if server_msg.decode('utf-8') == 'AUTH_PASS': #If server accepts those credentials : sign in
			print("\nSigned in as: ", name)
	#Check if credentials fail
	elif (server_msg.decode('utf-8') == 'AUTH_FAIL'): #If server denies those credentials : request new credentials
		print("\nIncorrect password.")
		server_msg = 'AUTH'.encode('utf-8')

	else:
		MESSAGE = input("tcpClient: Enter message to continue/ Enter exit:")
		tcpClient.send(MESSAGE.encode("utf-8"))
		server_msg = tcpClient.recv(BUFFER_SIZE)
		print("%s received server_msg:", server_msg.decode('utf-8'))  #TWM added decode call to decode the incoming encoded message

tcpClient.close()
