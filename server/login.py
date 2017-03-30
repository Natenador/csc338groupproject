#loginFunctions

#Global data file name
USER_DATA_FILE = 'users.dat'


#Takes a list of user data and writes it to the file
#data format: ["name", "ip", "password"]
def createUser(data):
    with open(USER_DATA_FILE, "r+") as file:
        len(file.readlines())
        file.write("%s:%s:%s\n" % (data[0], data[1], data[2]))

#Reads all users from user data file and returns them into a list
def readUserList():
    with open(USER_DATA_FILE, "r") as file:
        userList = file.readlines()
        userList = [line.strip('\n') for line in userList]
        return userList

#Returns true/false depending on if the user exists in the user data file
#userList is a list of all the users
#data format: ["name", "ip", "password"]
def checkExists(userList, data):
    userData = "%s:%s:%s" % (data[0], data[1], data[2])
    for user in userList:
        if user == userData:
            return True
    return False


