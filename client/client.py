import socket
import threading
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

TOO_MANY_CONNECTIONS_ERROR = "/e:-1"

AUTHORIZATION_REQUIRED = "AUTH_REQ"
AUTHORIZATION_PASS = "AUTH_PASS"
AUTHORIZATION_FAIL = "AUTH_FAIL"

CONNECTION_MADE_MESSAGE = "Connected!"

tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

USERNAME = ''
THREAD_RUNNING = False

class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.inc_mssg =  ''
        self.username = QtWidgets.QLineEdit(self)
        self.userLabel = QtWidgets.QLabel('Username: ', self)
        self.password = QtWidgets.QLineEdit(self)
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

#GUI Class
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
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
        self.sendButton.setMaximumSize(QtCore.QSize(200, 200))
        self.sendButton.setStyleSheet("QPushButton {background: rgb(165,67,67); font-size: 12px; font-family:Arial, Helvetica, sans-serif; font-weight: bold}")
        self.sendButton.setObjectName("sendButton")
        self.messageArea = QtWidgets.QLineEdit(self.centralwidget)
        self.messageArea.setGeometry(QtCore.QRect(30, 540, 591, 31))
        self.messageArea.setStyleSheet("QLineEdit {background: rgb(108,108,108); color: white;font-size: 12px; font-family:Arial, Helvetica, sans-serif}")
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
        self.chatArea.setStyleSheet("QTextBrowser {background: rgb(108,108,108); color: white; font-size: 12px; font-family:Arial, Helvetica, sans-serif}")
        self.chatArea.setObjectName("chatArea")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.userArea = QtWidgets.QTextBrowser(self.centralwidget)
        self.userArea.setGeometry(QtCore.QRect(630, 10, 141, 521))
        self.userArea.setStyleSheet("QTextBrowser {background: rgb(108,108,108); color: white; font-size: 12px; font-family:Arial, Helvetica, sans-serif}")
        self.userArea.setObjectName("userArea")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 31))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.sendButton.clicked.connect(self.sendMessage)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle('Chat Client')
        self.sendButton.setText('Send')

    def sendMessage(self):
        mssg = self.messageArea.text()
        self.messageArea.clear()
        try:
            self.chatArea.append(USERNAME + ":" + " " + mssg)
            tcpClient.send(mssg.encode("utf-8"))
        except socket.error as se:
            self.chatArea.append("Error sending message:" + mssg)

    def closeEvent(self, evnt):
        THREAD_RUNNING = False
        print('Thread stopping...')

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


def listen_for_messages(conn, ui):
    ERROR = False
    while not ERROR and THREAD_RUNNING == True:
        try:
            message = conn.recv(BUFFER_SIZE)
            if isError(message.decode("utf-8")):
                ERROR = True
            else:
                message = message.decode('utf-8')
                ui.chatArea.append(message)
        except socket.error as se:
            ui.chatArea.append("Error receiving message! Socket may have closed.")
            ERROR = True

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

def main(): 

    tcpClient.connect((host, port))
    connection_response = tcpClient.recv(BUFFER_SIZE).decode("utf-8")
    connected = connection_response == CONNECTION_MADE_MESSAGE

    print(connection_response)

    app = QtWidgets.QApplication(sys.argv)
    login = Login()
    if login.exec_() == QtWidgets.QDialog.Accepted:
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()

        if connected:            
            listen_thread = threading.Thread(target = listen_for_messages, args = [tcpClient, ui])
            THREAD_RUNNING = True
            listen_thread.start()
            sys.exit(app.exec_())  

if __name__ == "__main__":    
    main()    