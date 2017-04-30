import socket
import threading

TOO_MANY_CONNECTIONS_ERROR = "/e:-1"

CONNECTION_MADE_MESSAGE = "Connected!"

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


def listen_for_messages(conn):
    ERROR = False
    while not ERROR:
        try:
            message = conn.recv(BUFFER_SIZE)
            if isError(message.decode("utf-8")):
                ERROR = True
            else:
                print(message.decode())
        except socket.error as se:
            print ("Error receiving message! Socket may have closed.")
            ERROR = True


def main():
    username = input("Enter your username: ")
 
    tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    tcpClient.connect((host, port))
    MESSAGE = "/u:" + username
    tcpClient.send(MESSAGE.encode("utf-8"))
    connection_response = tcpClient.recv(BUFFER_SIZE).decode("utf-8")
    connected = connection_response == CONNECTION_MADE_MESSAGE

    print(connection_response)

    if connected:
        
        listen_thread = threading.Thread(target = listen_for_messages, args = [tcpClient])
        listen_thread.start()
        while MESSAGE != 'exit':
            try:
                MESSAGE = input(username + ":>> ")
                print(username + ":" + " " + MESSAGE)
                tcpClient.send(MESSAGE.encode("utf-8"))
            except socket.error as se:
                print("Error sending message", MESSAGE)
     
        tcpClient.close()
        print("Program ended!")


if __name__ == "__main__":
    main()
