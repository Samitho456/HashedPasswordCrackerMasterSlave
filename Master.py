from socket import *
import threading
import json

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)

crackedPasswords = []
chunkLock = threading.Lock() # Lock to synchronize access to currentChunk and crackedPasswords 

def CreatePasswordDict(passwordList: list) -> dict:
    """Creates a dictionary from a list of 'username:hash' entries."""
    passwordDict = {}
    for entry in passwordList:
        parts = entry.split(":")
        if len(parts) == 2:
            passwordDict[parts[0]] = parts[1]
    return passwordDict

# Get the hashed passwords
with open("passwords.txt", "r") as file:
    passwordList = file.read().splitlines()

# Create password dictionary from list
passwordDict = CreatePasswordDict(passwordList)

# Get the dictionary words
with open("webster-dictionary.txt", "r") as file:
    WordList = file.read().splitlines()

chunkSize = 1000 # Number of words in each chunk

# Split the word list into chunks
WordList =[WordList[i:i + chunkSize] for i in range(0, len(WordList), chunkSize)]


chuckAmount = len(WordList) # Number of chunks to distribute among clients
currentChunk = 0 # Index of the current chunk being distributed to clients

def handleClient(connectionSocket: socket):
    """Handles communication with a connected client."""
    global currentChunk
    print("Client connected: " + str(connectionSocket.getpeername()))
    while True:
        message = connectionSocket.recv(1024).decode()
        if not message:
            break
        match message:
            case "ready":
                continue
            case "chunk":
                with chunkLock:
                    if currentChunk >= len(WordList):
                        connectionSocket.send("NO_MORE_CHUNKS".encode())
                    else:
                        connectionSocket.send(json.dumps(WordList[currentChunk]).encode())
                        currentChunk += 1
                        print(f"Sent chunk {currentChunk}/{len(WordList)} to {connectionSocket.getpeername()}")
            case "password":
                connectionSocket.send(json.dumps(passwordDict).encode())
            case "done":
                print(f"Client {connectionSocket.getpeername()} has finished cracking passwords.")
                with chunkLock:
                    if currentChunk >= len(WordList):
                        print("\n=== All chunks distributed ===")
                        print("Cracked passwords:")
                        for pwd in crackedPasswords:
                            print(f"  {pwd}")
                break
            case _:
                # Parse JSON list payloads from slave, e.g. ["found", "user", "password"]
                try:
                    payload = json.loads(message)
                except json.JSONDecodeError:
                    payload = None

                if isinstance(payload, list) and len(payload) == 3 and payload[0] == "found":
                    password = f"{payload[1]}:{payload[2]}"
                    print("Client found password: " + password)
                    with chunkLock:
                        crackedPasswords.append(password)
                continue

def createPasswordDictionary() -> dict:
    passwordDictionary = {}
    for i in range(len(passwordList)):
        passwordDictionary[passwordList[i].split(":")[0]] = passwordList[i].split(":")[1]
    return passwordDictionary

passwordDictionary = createPasswordDictionary()

while True:
    connectionSocket, addr = serverSocket.accept()
    threading.Thread(target=handleClient, args=(connectionSocket,)).start()