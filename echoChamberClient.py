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
        self.supportedTypes = ["png", "PNG", "GIF", "gif", "TXT", "txt", "WEBM", "webm", "MP4", "mp4"]


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
        print("Closed client connection\n")
    
    
    def processCommands(self, userInput: str) -> None:
        command, *args = userInput.split(' ')
        if command == "send":
            self._requestServerSendFile(userInput)
        elif command == "sendSMS":
            self._sendData(command)
            checkError = self._recvData().decode()
            if checkError == "Recipient Found":
                fileName = check[-1]
                self._sendFile(fileName)
                serverMsg = self._recvData().decode()
                print(serverMsg + '\n')
            else:
                print(checkError + '\n')
        elif command == "SMSLog":
            self._requestSMSLog(userInput)
        elif command == "ls":
            self._requestDisplayFiles(userInput)
        elif command == "help":
            print("Commands:\n")
            print("\t\"send\" [file name with extension] [optional: new file name with extension]:  "\
                  "requests a file from server with specified file name. Server will send it, and client will save it "\
                  "with new name if specified. Otherwise, saves it as specified file name.\n")
            
            print("\t\"sendSMS\" [name of recipient] [file name with extension]: "\
                  "requests a specified file from the server to be sent to the recipient's phone via SMS. "\
                  "Limited to TXT, PNG, IMG, GIF, WEBM, and MP4 files.\n")
            
            print("\t\"SMSLog\": "\
                  "receive usernames from server of what phone contacts are available for use.\n")
            
            print("\t\"ls\" : "\
                  "lists the files that are currently in the directory.\n")
            
            print("\t\"q\": "\
                  "terminates connection with server and shuts down server.\n\n")
        if command == 'q':
            self._closeConnection()      


    def _requestServerSendFile(self, userInput: str) -> None:
            self._sendData(userInput)
            serverResponse = self._recvData()
            temp, *args = userInput.split(' ')
            fileName = args[0]
            if serverResponse == "File not found":
                print(f"ERROR: File '{fileName}' does not exist\n")
            else:
                self._receiveFileFromServer(args)
                
    
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
        
    
    def _requestSMSLog(self, userInput: str) -> None:
        self._sendData(userInput)
        info = self._recvData()
        print(info.decode('ascii'))


    def _requestDisplayFiles(self, userInput: str) -> None:
        self._sendData(userInput)
        fileInfo = self._recvData()
        print(fileInfo.decode('ascii'))


    
    
