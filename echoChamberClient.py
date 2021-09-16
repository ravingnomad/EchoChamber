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
        self.abort = False


    def connectToServer(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.socket:
            try:
                self.socket.connect((self.server, self.port))
                print("Successfully connected to {}\n".format(self.server))
                self.mainLoop()
            except Exception as e:
                print(e)
                print("ERROR: Could not establish connection.\n")
        

    def start(self) -> None:
        print("\nEnter a command. Type 'help' for commands and formatting\n")
        while self.abort == False:
            message = input("->")
            self._processCommands(message)

    
    def _processCommands(self, userInput: str) -> None:
        command, *args = userInput.split(' ')
        if command == 'q':
            self._sendData('q')
            self.abort = True
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
        
        elif command == "send":
            fileName = check[1]
            self._sendData(command)
            self._sendFile(fileName)

        elif command == "SMSLog":
            '''Get message from server detailing the logged sms info'''
            self._sendData(command)
            self._requestSMSLog()
            
        elif command == "ls":
            self._displayFiles()

        elif command == "help":
            print("Commands:\n")
            print("\t\"send\" [file name with extension] [optional: new file name]:  makes a copy of specified file and sends it to receiving server. Will save file on server-side with new name if specified.\n")
            print("\t\"sendSMS\" [name of recipient] [file name with extension]: sends a file and recipient name to the server so that file can be converted to email and texted to recipient's phone. Limited to text, PNG, IMG, GIF, and WEBM files.\n")
            print("\t\"SMSLog\": receive information from server describing what phone contacts are available for use along with a small description of who\what they are\n")
            print("\t\"ls\" : lists the files that are currently in the directory.\n\n")
            print("\t\"q\": terminates connection with server-side. In current condition, also shuts down server.\n")        

    
    
    
    def _requestSMSLog(self):
        """Requests a text log from the server that details the phone/contact info
        of individuals that server has stored in order to send text messages. Does not
        reveal info about individual's carrier nor phone number"""
        info = self._recvData()
        info = info.decode("ascii").split("\n\n")
        for line in info:
            if line != "END":
                print(line)
        print('\n')


    def _displayFiles(self):
        for file in os.listdir():
            print(file)
        print('\n')



    
    
