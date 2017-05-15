import socket
import threading
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

TOO_MANY_CONNECTIONS_ERROR = "/e:-1"

AUTHORIZATION_REQUIRED = "AUTH_REQ"
AUTHORIZATION_PASS = "AUTH_PASS"
AUTHORIZATION_FAIL = "AUTH_FAIL"

LIST_OF_NAMES_MESSAGE = '/names:'

CONNECTION_MADE_MESSAGE = "Connected!"

USERNAME = ''
THREAD_RUNNING = False
connected = ''

tcpClient = ''

host = ''
PORT = 13000
BUFFER_SIZE = 1024

class IpWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(IpWindow, self).__init__(parent)
        self.ipAddress = QtWidgets.QLineEdit(self)
        self.ipLabel = QtWidgets.QLabel('IP Address: ', self)
        self.buttonIp = QtWidgets.QPushButton('Connect', self)
        self.buttonIp.clicked.connect(self.handleIp)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.ipLabel)
        layout.addWidget(self.ipAddress)
        layout.addWidget(self.buttonIp)
        self.resize(300,100)
        self.setWindowIcon(QtGui.QIcon('clientIcon.png'))
        self.setWindowTitle('IP Connection')
        self.setStyleSheet("QDialog {background: rgb(108,108,108); font-size: 12px; font-family:Arial, Helvetica, sans-serif} QLabel {font-size: 12px; font-family:Arial, Helvetica, sans-serif; color: white} QPushButton {background: rgb(165,67,67); font-size: 12px; font-family:Arial, Helvetica, sans-serif; font-weight: bold} ")

    def handleIp(self):
        global host
        global connected
        global tcpClient

        host = self.ipAddress.text()
        self.ipAddress.clear()
        try:
            tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpClient.connect((host, PORT))
            connection_response = tcpClient.recv(BUFFER_SIZE).decode("utf-8")
            connected = connection_response == CONNECTION_MADE_MESSAGE
            if connected:
                self.accept()
            else:
                tcpClient.close()
                QtWidgets.QMessageBox.warning(self, 'Error', 'There are too many connections to that server at this time.')
                connected = ''
        except socket.error as se:
            print(se)
            print(host)
            print("\nExcept block.")
            if connected != '':
                tcpClient.close()
                QtWidgets.QMessageBox.warning(self, 'Error', 'There are too many connections to that server at this time.')
            else:
                QtWidgets.QMessageBox.warning(self, 'Error', 'Invalid IP Address.')

#Login popup window
class Login(QtWidgets.QDialog):
    #Initialize Login GUI objects
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.inc_mssg =  ''
        self.username = QtWidgets.QLineEdit(self)
        self.userLabel = QtWidgets.QLabel('Username: ', self)
        self.password = QtWidgets.QLineEdit(self)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pwordLabel = QtWidgets.QLabel('Password: ', self)
        self.buttonLogin = QtWidgets.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.userLabel)
        layout.addWidget(self.username)
        layout.addWidget(self.pwordLabel)
        layout.addWidget(self.password)
        layout.addWidget(self.buttonLogin)
        self.resize(300,200)
        self.setWindowIcon(QtGui.QIcon('clientIcon.png'))
        self.setWindowTitle('User Login')
        self.setStyleSheet("QDialog {background: rgb(108,108,108); font-size: 12px; font-family:Arial, Helvetica, sans-serif} QLabel {font-size: 12px; font-family:Arial, Helvetica, sans-serif; color: white} QPushButton {background: rgb(165,67,67); font-size: 12px; font-family:Arial, Helvetica, sans-serif; font-weight: bold} ")

    #Handles I/O
    def handleLogin(self):
        global USERNAME
        if self.inc_mssg == '':
            self.inc_mssg = tcpClient.recv(BUFFER_SIZE)
            self.inc_mssg = self.inc_mssg.decode('utf-8')
        if (signIn(self.inc_mssg, self.username.text(), self.password.text()) == True):
            self.username = self.username.text()
            USERNAME = self.username
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Bad user or password')

#Handles authorization of username/password
def signIn(inc_mssg, username, pword):    
    while(inc_mssg == AUTHORIZATION_REQUIRED):
        if (inc_mssg == AUTHORIZATION_REQUIRED):
            userData = username + ':' + pword
            tcpClient.send(userData.encode('utf-8'))

            inc_mssg = tcpClient.recv(BUFFER_SIZE)
            inc_mssg = inc_mssg.decode('utf-8')
            if (inc_mssg == AUTHORIZATION_PASS):
                return True
            elif (inc_mssg == AUTHORIZATION_FAIL):
                inc_mssg = AUTHORIZATION_REQUIRED
                return False

#Worker thread class for receiving messages
class mssgThread(QtCore.QThread):
    new_mssg = QtCore.pyqtSignal(str)
    client_list = QtCore.pyqtSignal(str)

    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        ERROR = False
        THREAD_RUNNING = True
        while not ERROR and THREAD_RUNNING ==True:
            try:
                message = tcpClient.recv(BUFFER_SIZE)
                if isError(message.decode("utf-8")):
                    ERROR = True
                else:
                    message = message.decode('utf-8')
                    if message[:7] == LIST_OF_NAMES_MESSAGE:
                        self.client_list.emit(message)
                    else:
                        self.new_mssg.emit(message)
            except socket.error as se:
                message = "Error receiving message! Socket may have closed."
                ERROR = True
                self.new_mssg.emit(message)

#Main GUI Class
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        self.thread = mssgThread()
        self.thread.start()
        self.thread.new_mssg.connect(self.appendMssg)
        self.thread.client_list.connect(self.updateClientList)

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        MainWindow.setWindowIcon(QtGui.QIcon('clientIcon.png'))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(108, 108, 108))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(108, 108, 108))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(108, 108, 108))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(108, 108, 108))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        MainWindow.setPalette(palette)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.sendButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendButton.setGeometry(QtCore.QRect(630, 540, 141, 34))
        self.sendButton.setMinimumSize(QtCore.QSize(0, 0))
        self.sendButton.setMaximumSize(QtCore.QSize(300, 200))
        self.sendButton.setStyleSheet("QPushButton {background-color: transparent; background-repeat: none; border: none;}")
        self.sendButton.setIcon(QtGui.QIcon('button_send.png'))
        self.sendButton.setIconSize(QtCore.QSize(250,30))
        self.sendButton.setObjectName("sendButton")
        self.messageArea = QtWidgets.QLineEdit(self.centralwidget)
        self.messageArea.setGeometry(QtCore.QRect(30, 540, 591, 31))
        self.messageArea.setStyleSheet("QLineEdit {background: rgb(90,90,90); color: white;font-size: 12px; font-family:Arial, Helvetica, sans-serif}")
        self.messageArea.setObjectName("messageArea")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(30, 10, 591, 521))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 589, 519))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.chatArea = QtWidgets.QTextBrowser(self.scrollAreaWidgetContents_2)
        self.chatArea.setGeometry(QtCore.QRect(0, 0, 591, 521))
        self.chatArea.setStyleSheet("QTextBrowser {background: rgb(90,90,90); color: white; font-size: 12px; font-family:Arial, Helvetica, sans-serif}")
        self.chatArea.setObjectName("chatArea")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.userArea = QtWidgets.QTextBrowser(self.centralwidget)
        self.userArea.setGeometry(QtCore.QRect(630, 10, 141, 521))
        self.userArea.setStyleSheet("QTextBrowser {background: rgb(90,90,90); color: white; font-size: 12px; font-family:Arial, Helvetica, sans-serif}")
        self.userArea.setObjectName("userArea")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 31))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.messageArea.setFocus(True)

        self.messageArea.returnPressed.connect(self.sendMessage)
        self.sendButton.clicked.connect(self.sendMessage)

    #resets client positioning
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle('Chat Client')

    #sends message to server
    def sendMessage(self): #Sends messages and pushes the message to the chatArea
        mssg = self.messageArea.text()
        if mssg != '':
            self.messageArea.clear()
            try:
                self.chatArea.append(USERNAME + ":" + " " + mssg)
                tcpClient.send(mssg.encode("utf-8"))
            except socket.error as se:
                self.chatArea.append("Error sending message:" + mssg)
    #appends messages to the screen so the user can see them
    def appendMssg(self, mssg): #Appends incoming messages to the chatArea
        if mssg != '':
            self.chatArea.append(mssg)

    def updateClientList(self, mssg):
        nameList = mssg.split(':')
        self.userArea.clear()
        for name in range(1, len(nameList)):
            self.userArea.append(nameList[name])
    
    #Things to do when GUI closes (May not be working yet)            
    def closeEvent(self, event):
        THREAD_RUNNING = False
        mssg = 'exit'
        tcpClient.send(mssg.encode('utf-8'))

#Takes the message from the server as an input
#If the message equals any error, print the error and stop the loop to end the program
#Otherwise print the message.
def isError(message):
    if message == TOO_MANY_CONNECTIONS_ERROR:
        print ("There are currently too many connections to this server, please try again later.")
        return True
    else:
        return False    

def main():
    #Start the GUI 
    app = QtWidgets.QApplication(sys.argv)
    ip = IpWindow()
    ip.exec_()    
    #print(connection_response)
    #QtWidgets.QMessageBox.warning(self, 'Error', 'There are currently too many connections to this server, please try again later.')

    if connected:   
        login = Login()
        if login.exec_() == QtWidgets.QDialog.Accepted:
            MainWindow = QtWidgets.QMainWindow()
            ui = Ui_MainWindow()
            ui.setupUi(MainWindow)
            MainWindow.show()
            sys.exit(app.exec_()) 

if __name__ == "__main__":    
    main()    