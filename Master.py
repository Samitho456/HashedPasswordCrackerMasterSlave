from socket import *
import threading

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

crackedPasswords = []

# Get the hashed passwords
with open("passwords.txt", "r") as file:
    passwordList = file.read().splitlines()

# Get the dictionary words
with open("webster-dictionary.txt", "r") as file:
    WordList = file.read().splitlines()

chunkSize = 1000 # Number of words in each chunk

# Split the word list into chunks
WordList =[WordList[i:i + chunkSize] for i in range(0, len(WordList), chunkSize)]


chuckAmount = len(WordList) # Number of chunks to distribute among clients
currentChunk = 0 # Index of the current chunk being distributed to clients

def handleClient(connectionSocket):
    global currentChunk
    print("Client connected: " + str(connectionSocket.getpeername()))
    while True:
        message = connectionSocket.recv(1024).decode()
        match message:
            case "ready":
                continue
            case "chunk":
                currentChunk = (currentChunk + 1) % len(WordList) # Gets next chunk index
                connectionSocket.send(str(WordList[currentChunk]).encode())
            case "password":
                connectionSocket.send(str(passwordList).encode())
            case "done":
                print("Client has finished cracking passwords.")
                break
            case _:
                # Check if the message indicates a found password
                if message.startswith("found:"):
                    password = message.split("found:")[1]
                    print("Client found password: " + password)
                    crackedPasswords.append(password)
                
                # If all chunks have been distributed, print the cracked passwords
                if currentChunk == chuckAmount - 1:
                    print(crackedPasswords)
                continue


while True:
    connectionSocket, addr = serverSocket.accept()
    threading.Thread(target=handleClient, args=(connectionSocket,)).start()