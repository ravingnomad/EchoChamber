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

    def start(self):
        """Starts the connection between server and client. Will tell user if connection
        is established or if there was an issue with connecting to the server. Once
        connected, will start the main loop."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.socket:
            #try:
            self.socket.connect((self.server, self.port))
            print("Successfully connected to {}\n".format(self.server))
            self.mainLoop()
            #except:
            print("ERROR: Could not establish connection.\n")
        

        
    def mainLoop(self):
        """The main loop where the interaction between client and server takes place."""
        while True:
            message = input("->")
            abort = self._commands(message)
            if abort:
                break
    
    
    def _commands(self, command):
        """Takes a command that the user inputs and determines whether it is valid or not.
        If valid, calls the appropriate function. If not, tells the user the command is
        invalid. Additionally, constantly returns a bool that states whether or not the
        client wants to terminate the connection."""
        check = command.split(' ')
        if self._commandErrors(check) == False:
            
            if check[0] == 'q':
                self._sendData('q')
                return True

            elif check[0] == "sendSMS":
                self._sendData(command)
                checkError = self._recvData().decode()
                if checkError == "Recipient Found":
                    fileName = check[-1]
                    self._sendFile(fileName)
                    serverMsg = self._recvData().decode()
                    print(serverMsg + '\n')
                else:
                    print(checkError + '\n')
            
            elif check[0] == "send":
                fileName = check[1]
                self._sendData(command)
                self._sendFile(fileName)

            elif check[0] == "SMSLog":
                '''Get message from server detailing the logged sms info'''
                self._sendData(command)
                self._requestSMSLog()
                
            elif check[0] == "ls":
                self._displayFiles(check)

            elif check[0] == "help":
                print("Commands:\n")
                print("\t\"send\" [file name with extension] [optional: new file name]:  makes a copy of specified file and sends it to receiving server. Will save file on server-side with new name if specified.\n")
                print("\t\"sendSMS\" [name of recipient] [file name with extension]: sends a file and recipient name to the server so that file can be converted to email and texted to recipient's phone. Limited to text, PNG, IMG, GIF, and WEBM files.\n")
                print("\t\"SMSLog\": receive information from server describing what phone contacts are available for use along with a small description of who\what they are\n")
                print("\t\"q\": terminates connection with server-side. In current condition, also shuts down server.\n")
                print("\t\"ls\" [optional: '-s']: lists the files that are currently in the directory. If '-s' included, also displays file size in megabytes, rounded to 2 decimal places.\n\n")        
        return False

    
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


            

    def _commandErrors(self, command) -> bool:
        """Takes a command, split by its white spaces, and sees if it is formatted correctly. If it is,
        return 'False' as in there are no errors. Otherwise, return 'True'
        as in there is an error."""
        if command[0] not in self.commands:
            print("ERROR: Command '{}' does not exist. Type 'help' to see available commands.\n".format(command[0]))
            return True

        check = command[0]
        if check == "send":
            if len(command) < 2 or len(command) > 3:
                print("ERROR: 'send' command incorrectly formatted. Type 'help' to see correct format.\n")
                return True
            elif self._fileExists(command[1]) == False:
                print("ERROR: The file '{}' does not exist. Type 'ls' to see list of available files in directory.\n".format(command[1]))
                return True
            
        elif check == "sendSMS":
            if len(command) < 3 or len(command) > 3:
                print("ERROR: 'sendSMS' command incorrectly formatted. Type 'help' to see correct format.\n")
                return True
            
            elif self._fileExists(command[-1]) == False:
                print("ERROR: The file '{}' does not exist. Type 'ls' to see list of available files in directory.\n".format(command[1]))
                return True
            
            elif self._fileCorrectType(command[-1]) == False:
                extension = command[-1].split('.')[-1]
                print("ERROR: Cannot send files of type '{}'. Type 'help' to see supported file types.\n".format(extension))
                return True

        elif check == "ls":
            if len(command) > 2 or (len(command) == 2 and command[1] != '-s'):
                print("ERROR: 'ls' command incorrectly formatted. Type 'help' to see correct format.\n")
                return True
                
        elif check == "SMSLog":
            if len(command) > 1:
                print("ERROR: 'SMSLog' command incorrectly formatted. Type 'help' to see correct format.\n")
                return True
            
        elif check == "help" and len(command) > 1:
            print("ERROR: 'help' command incorrectly formatted. Type 'help' to see correct format.\n")
            return True

        elif check == "q" and len(command) > 1:
            print("ERROR: 'q' command incorrectly formatted. Type 'help' to see correct format.\n")
            return True

        return False





    
    
