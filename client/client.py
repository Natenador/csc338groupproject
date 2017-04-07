import socket
import login_client as login

host = socket.gethostname() 
port = 13000
BUFFER_SIZE = 1024
MESSAGE = ''
data = ''

tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpClient.connect((host, port))
 
data = tcpClient.recv(BUFFER_SIZE)

while MESSAGE != 'exit':

	if (data.decode('utf-8') == 'AUTH'):
		userData = login.signIn()
		name, pword = userData.split(':')
		tcpClient.send(userData.encode('utf-8'))
		data = tcpClient.recv(BUFFER_SIZE)
		if data.decode('utf-8') == 'AUTH_PASS':
			print("\nSigned in as: ", name)

	elif (data.decode('utf-8') == 'AUTH2'):
		print("\nIncorrect password.")
		data = 'AUTH'.encode('utf-8')

	else:
		MESSAGE = input("tcpClient: Enter message to continue/ Enter exit:")
		tcpClient.send(MESSAGE.encode("utf-8"))
		data = tcpClient.recv(BUFFER_SIZE)
		print("Client2 received data:", data.decode('utf-8'))  #TWM added decode call to decode the incoming encoded message

tcpClient.close()
