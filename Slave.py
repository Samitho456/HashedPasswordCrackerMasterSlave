import hashlib
import base64
from socket import *
import json

# Client setup
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

chunk = [] # Current chunk of words received from server
passwordDictionary = {} # Dictionary of username and password pairs received from server

def crackPassword(password: str) -> str:
    global chunk
    for word in chunk:
        print("Trying password: " + word)
        lowerWord = word.lower()
        hashedWord = get_sha1_base64(lowerWord)
        if(password == hashedWord):
            print("Password found: " + lowerWord)
            return lowerWord
            
        upperWord = word.upper()
        hashedWord = get_sha1_base64(upperWord)
        if(password == hashedWord):
            print("Password found: " + upperWord)
            return upperWord
            
        capitalizedWord = word.capitalize()
        hashedWord = get_sha1_base64(capitalizedWord)
        if(password == hashedWord):
            print("Password found: " + capitalizedWord)
            return capitalizedWord
            
        reverseWord = reverse(word)
        hashedWord = get_sha1_base64(reverseWord)
        if(password == hashedWord):
            print("Password found: " + reverseWord)
            return reverseWord
        
        for i in range(100):
            str(i) + word
            hashedWord = get_sha1_base64(str(i) + word) 
            if(password == hashedWord):
                print("Password found: " + str(i) + word)
                return str(i) + word
        
        for i in range(100):
            numberword = word + str(i)
            hashedWord = get_sha1_base64(numberword) 
            if(password == hashedWord):
                print("Password found: " + numberword)
                return numberword
            
        for i in range(10):
            for j in range(10):
                str(j) + word + str(i)
                hashedWord = get_sha1_base64(str(j) + word + str(i)) 
                if(password == hashedWord):
                    print("Password found: " + str(j) + word + str(i))
                    return str(j) + word + str(i)
    return None

def get_sha1_base64(input_string: str) -> str:
    """Takes an input string, computes its SHA-1 hash, and returns the hash encoded in Base64."""
    
    data = input_string.encode('utf-8')
    
    sha1_bytes = hashlib.sha1(data).digest()
    
    base64_hash = base64.b64encode(sha1_bytes).decode('utf-8')
    
    return base64_hash

def reverse(sentence: str) -> str:
    """Takes a string as input and returns the string reversed."""
    return sentence[::-1]

# Get password dictionary first
print("Requesting password dictionary from server...")
clientSocket.send("password".encode())
print("Receiving password dictionary from server...")
passwordDictData = clientSocket.recv(100000).decode()
print("Password dictionary received from server: " + passwordDictData)

passwordDictionary = json.loads(passwordDictData)
print("Password dictionary ready for cracking: " + str(list(passwordDictionary.keys())))


while True:
    print("Requesting chunk from server...")
    clientSocket.send("chunk".encode())
    recievedChunk = clientSocket.recv(100000).decode()
    
    if recievedChunk == "NO_MORE_CHUNKS":
        print("No more chunks available. Finishing.")
        clientSocket.send("done".encode())
        break
    
    try:
        chunk = json.loads(recievedChunk)
    except Exception as e:
        print(f"Error parsing chunk: {e}")
        continue
    
    # Try cracking passwords with the current chunk of words
    for username in list(passwordDictionary.keys()):
        crackedpassword = crackPassword(passwordDictionary[username])
        if crackedpassword:
            print("Password cracked for user " + username + ": " + crackedpassword)
            clientSocket.send(json.dumps(["found", username, crackedpassword]).encode())
            del passwordDictionary[username] # Remove cracked password from dictionary
            break
    
    # Clear chunk
    chunk = []

clientSocket.close()
