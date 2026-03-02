from socket import *
import threading

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

with open("passwords.txt", "r") as file:
    passwordList = file.read().splitlines()

with open("webster-dictionary.txt", "r") as file:
    WordList = file.read().splitlines()

chunkSize = 10000
WordList =[WordList[i:i + chunkSize] for i in range(0, len(WordList), chunkSize)]

currentChunk = 0

def handleClient(connectionSocket):
    while True:
        message = connectionSocket.recv(1024).decode()
        
        match message:
            case "ready":
                continue
            case "chunk":
                sentence = WordList[currentChunk]
                currentChunk = (currentChunk + 1) % len(WordList)
            case "password":
                sentence = passwordList
            case _:
                continue
        connectionSocket.send(sentence.upper().encode())

while True:
    connectionSocket, addr = serverSocket.accept()
    threading.Thread(target=handleClient, args=(connectionSocket,)).start()