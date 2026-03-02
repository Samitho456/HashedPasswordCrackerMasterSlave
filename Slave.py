import hashlib
import base64
from socket import *
import ast

# Client setup
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

chunk = []
passwordDictionary = {}


def crackPassword(password):
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

def get_sha1_base64(input_string):
    # 1. Convert string to bytes
    data = input_string.encode('utf-8')
    
    # 2. Get the SHA-1 hash (raw bytes, not hex)
    sha1_bytes = hashlib.sha1(data).digest()
    
    # 3. Encode those bytes to Base64
    base64_hash = base64.b64encode(sha1_bytes).decode('utf-8')
    
    return base64_hash

def reverse(sentence):
    return sentence[::-1]

first = True


# input and send data
while True:
    # receive and print modified data
    if(chunk == []):
        print("Requesting chunk from server...")
        clientSocket.send("chunk".encode())
        print("Receiving chunk from server...")
        recievedChunk = clientSocket.recv(100000).decode()
        try:
            chunk = ast.literal_eval(recievedChunk)
        except Exception as e:
            print(f"Error parsing chunk: {e}")
            continue
        continue
    
    elif(passwordDictionary == {}):
        print("Requesting password list from server...")
        clientSocket.send("password".encode())
        print("Receiving password list from server...")
        passwordList = clientSocket.recv(100000).decode()
        print("Password list received from server: " + passwordList)
        
        passwordList = ast.literal_eval(passwordList)
        print("Password list converted to list: " + str(passwordList))
        for i in range(len(passwordList)):
            passwordDictionary[passwordList[i].split(":")[0]] = passwordList[i].split(":")[1]
            passwordList[i] = passwordList[i].split(":")[1]
        continue
        
    if(chunk != [] and passwordDictionary != {}):
        print("Cracking password...")
        for username in passwordDictionary:
            crackedpassword = crackPassword(passwordDictionary[username])
            if crackedpassword:
                print("Password cracked for user " + username + ": " + crackedpassword)
                clientSocket.send(("found:" + username + ":" + crackedpassword).encode())
        clientSocket.send("done".encode())
        break
