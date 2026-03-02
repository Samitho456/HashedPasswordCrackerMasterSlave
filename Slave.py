from socket import *

# Client setup
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

chunk = []
passwordList = []


def crackPassword(chunk, passwordList):
    for word in chunk:
        word = word.lower()
        word.hash = hash(word)
        for password in passwordList:
            if(password == word):
                print("Password found: " + password)
                return password
            
        word = word.upper()
        word.hash = hash(word)
        for password in passwordList:
            if(password == word):
                print("Password found: " + password)
                return password
            
        word = word.capitalize()
        word.hash = hash(word)
        for password in passwordList:
            if(password == word):
                print("Password found: " + password)
                return password
            
        word = reversed(word)
        word.hash = hash(word)
        for password in passwordList:
            if(password == word):
                print("Password found: " + password)
                return password


def reverse(sentence):
    return sentence[::-1]

# input and send data
while True:
    sentence = "ready"
    clientSocket.send(sentence.encode())
    # receive and print modified data
    if(chunk == []):
        clientSocket.send("chunk".encode())
        chunk = clientSocket.recv(1024).decode()
        continue
    
    elif(passwordList == []):
        clientSocket.send("password".encode())
        passwordList = clientSocket.recv(1024).decode()
        continue
        
    if(chunk != [] and passwordList != []):
        password = crackPassword(chunk, passwordList)
        clientSocket.send(password.encode())
