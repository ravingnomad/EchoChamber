import socket
import struct
import sys
import os
from connection import *

class echoChamberClient(Connection):

    def __init__(self, serverName, port):
        Connection.__init__(self, None)
        self.server = serverName
        self.port = port
        self.commands = ['send', 'sendSMS', 'SMSLog', 'help', 'ls', 'q']
        self.smsSupportedFileTypes = ["jpg", "img", "png", "gif", "txt", "webm", "mp4"]
        self.serverAskedToCompress = False


    def getServerAskedToCompress(self) -> bool:
        return self.serverAskedToCompress
    
    
    def connectToServer(self) -> None:
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server, self.port))
            print("Successfully connected to {}\n".format(self.server))
        except Exception as e:
            print(e)
            print("ERROR: Could not establish connection.\n")
        
    
    def _closeConnection(self) -> None:
        self._sendData('q')
        self.socket.close()
        print("Closed connection with server\n")
    
    
    def processCommands(self, userInput: str) -> None:
        command, *args = userInput.split(' ')
        if command == "send":
            self._requestServerSendFile(userInput)
        elif command == "sendSMS":
            self._requestServerSendSMSFile(userInput)
        elif command == "SMSLog":
            self._requestSMSLog(userInput)
        elif command == "ls":
            self._requestDisplayFiles(userInput)
        elif command == "help":
            print("Commands:\n")
            print("\t\"send\" [file name with extension] [optional: new file name with same extension as requested file]:  "\
                  "requests a file from server with specified file name. Server will send it, and client will save it "\
                  "with new name if specified. Otherwise, saves it as specified file name.\n")
            
            print("\t\"sendSMS\" [file name with extension] [name of recipient]: "\
                  "requests a specified file from the server to be sent to the recipient's phone via SMS. "\
                  "Limited to TXT, PNG, IMG, GIF, JPG, WEBM, and MP4 files.\n")
            
            print("\t\"SMSLog\": "\
                  "receive usernames from server of what phone contacts are available for use.\n")
            
            print("\t\"ls\" : "\
                  "lists the files that are currently in the server directory.\n")
            
            print("\t\"q\": "\
                  "terminates connection with server and shuts down server.\n\n")
        if command == 'q':
            self._closeConnection()      


    def _requestServerSendFile(self, userInput: str) -> None:
        self._sendData(userInput)
        if self._fileExistsOnServer(userInput) == True:
            unused, *fileNames = userInput.split(' ')
            self._receiveFileFromServer(fileNames)
                
    
    def _receiveFileFromServer(self, possibleFileNames: list) -> None:
        fileName = None
        if len(possibleFileNames) == 1:
            fileName = possibleFileNames[0]
        elif len(possibleFileNames) == 2: #length of 2 means that the third optional field of the 'send' command is filled
            fileName = possibleFileNames[1]
        self._sendData("Ready to receive file")
        with open(fileName, 'wb') as receivedFile:
            dataFromServer = self._recvData()
            receivedFile.write(dataFromServer)
        print(f"Saved file received from server as '{fileName}'\n")
        
        
    def _requestServerSendSMSFile(self, userInput: str) -> None:
        self._sendData(userInput)
        if self._fileExistsOnServer(userInput) == True and self._recipientExists(userInput) == True:
            print("Server sending file to recipient by SMS...\n")
            compressQuery = self._recvStrData()
            if compressQuery == "Would you like to compress":
                self.serverAskedToCompress = True
            else:
                self.continueSendingSMS()

   
    def sendCompressQueryAnswer(self, answer: str) -> None:
       self._sendData(answer)
       
    
    def continueSendingSMS(self) -> None:
        #Mainly used to continue sending SMS text after querying client/user on whether they want to compress the file
        serverDoneSending = self._recvStrData() #stops client from entering anything else while server sends SMS
        while serverDoneSending != "Sent SMS to recipient successfully\n":
            serverDoneSending = self._recvStrData()
        print(serverDoneSending)
        self.serverAskedToCompress = False
   
   
    def _fileExistsOnServer(self, userInput: str) -> bool:
        serverResponse = self._recvStrData()
        unused, *args = userInput.split(' ')
        fileName = args[0]
        if serverResponse == "File not found":
            print(f"ERROR: File '{fileName}' does not exist\n")
            return False
        return True
    
    
    def _recipientExists(self, userInput: str) -> bool:
        serverResponse = self._recvStrData()
        unused, *args = userInput.split(' ')
        recipientName = args[1]
        if serverResponse == "Recipient not found":
            print(f"ERROR: User '{recipientName}' does not exist\n")
            return False
        return True
    
    
    def _requestSMSLog(self, userInput: str) -> None:
        self._sendData(userInput)
        info = self._recvStrData()
        print(info)


    def _requestDisplayFiles(self, userInput: str) -> None:
        self._sendData(userInput)
        fileInfo = self._recvStrData()
        print(fileInfo)


    
    
