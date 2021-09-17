import socket, struct, sys, os, smtplib, ffmpy
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from connection import *
from pickle import NONE

class echoChamberServer(Connection):

    def __init__(self, name, port):
        Connection.__init__(self, None)
        self.name = name
        self.port = port
        self.clientConn = None
        self.clientAddr = None
        self.endConnection = False
        self.validUsers = {}


    def loadUserInfo(self, userInfo: dict) -> None:
        self.validUsers = userInfo
    

    def waitForClient(self) -> None:
        print("\nWaiting to connect with client...\n")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.name, self.port))
            s.listen()
            self.socket, self.clientAddr = s.accept()
            print("Connected to client at {}".format(self.clientAddr))


    def start(self) -> None:
        with self.socket:
            while self.endConnection == False:
                self._waitForCommands()
                    

    def _waitForCommands(self):
        data = self._recvData()
        command, *args = data.decode().split(" ")
        if command == "send":
            self._sendFileToClient(args[0])
        elif command == "sendSMS":
            recipient = args[0]
            fileName = args[1]
            if self._smsRecipientValid(recipient) == True:
                noErrors = self._recvData().decode()
                if (noErrors == "File Exists"):
                    self._copyFile(fileName)
                    self._textFile(recipient, fileName)
                elif (noErrors == "Error found"):
                    print("\nClient found error(s) when trying to open file. Stopping command execution\n")
        elif command == "SMSLog":
            self._sendSMSInfo()
        elif command == "ls":
            self._sendFileInfo()
        elif command == "q":
            self.endConn = True

    
    def _sendFileToClient(self, fileName: str) -> None:
        print(f"\nClient wants file '{fileName}'\n")
        try:
            with open(fileName, 'rb') as file:
                self._sendData("File found")
                fileBuffer = file.read()
                clientResponse = self._recvData()
                if clientResponse == "Ready to receive file":
                    self._sendData(fileBuffer)
        except FileNotFoundError:
            print("ERROR: File {} does not exist.\n".format(fileName))
            self._sendData("File not found")
            
    # def _sendFile(self, fileName):
    #     """Sends a file over to the server to be saved. Will print a message once it is
    #     done sending the file."""
    #     try:
    #         with open(fileName, 'rb') as file:
    #             self._sendData("File Exists")
    #             buffer = file.read()
    #             readyToSend = self._recvData()
    #             if readyToSend.decode() == "Ready to receive file.":
    #                 print("Sending File to Server\n")
    #                 self._sendData(buffer)
    #     except FileNotFoundError:
    #         print("ERROR: File {} does not exist.\n".format(fileName))
    #         self._sendData("Error found")

    def _smsRecipientValid(self, recipientName: str) -> bool:
        print("\nClient wants to text a file to a valid recipient\n")
        if recipientName not in self.validUsers.keys():
            print("ERROR: recipient not valid\n")
            self._sendData("ERROR: not a valid recipient.")
            return False
        else:
            self._sendData("Recipient Found")
            return True
            
            
    def _sendSMSInfo(self):
        log = ""
        for user in self.validUsers.keys():
            log += user
            log += "\n"
        self._sendData(log)


    def _textFile(self, recipient, fileName):
        """Given a valid recipient name, server will send a text message to the recipient that
        contains the specified file. Since current SMS limits sent file sizes to be around 1.8MB,
        will check the size of the file and if it is greater than 1.8MB, will attempt to compress
        using FFmpeg. CURRENT COMPRESSION ONLY SUPPORTS MP4 AND WEBM. If file is still too large,
        will attempt to send the file, but will send client a message stating that file is too big
        and likely it will not be able to be sent. There are no guarantees that delivery will be
        successful as entirely dependent on rules imposed by client's mobile plan. After file is sent,
        if it was compressed, the compressed file will be deleted. If compression used, must delete
        resulting compressed file after reading its info as errors will arise if another compression
        occurs and saves with the same file name as the compressed file."""

        file = None
        compressed = False
        extension = fileName.split('.')[-1]
        clientMsg = 'Texting file to recipient'

        if self._fileTooBig(fileName):
            if extension.lower() in ('webm', 'mp4'):
                clientMsg = self._compress(fileName, extension)
                compressed = True
            else:
                clientMsg = 'WARNING: File larger than 1.8MB and does not support compression. Highly probable that file will not reach recipient.'
        self._sendData(clientMsg)
        
        if compressed == True:
            with open('output.{}'.format(extension), 'rb') as file:
                file = file.read()
            os.remove('output.{}'.format(extension))

        elif file == None and extension.lower() != 'txt':
            with open(fileName, 'rb') as file:
                file = file.read()
        else:
            with open(fileName, 'r', encoding = 'latin-1') as file:
                file = file.read()
                
        msg = MIMEMultipart()
        if extension.lower() in ('webm', 'mp4'):
            data = MIMEBase('video', 'mp4')
            data.set_payload(file)
            encoders.encode_base64(data)
            data.add_header('Content-Disposition', 'attachment', filename = fileName)
            msg.attach(data)
            msg['Subject'] = 'subject'
            msg['From'] = 'us'
            msg['To'] = 'us'
            text = MIMEText("test")
            msg.attach(text)

        elif extension.lower() == 'txt':
            text = MIMEText(file, _charset = "UTF-8")
            msg.attach(text)

        else:
            msg['Subject'] = 'subject'
            msg['From'] = 'us'
            msg['To'] = 'us'
            text = MIMEText("test")
            msg.attach(text)
            image = MIMEImage(file)
            msg.attach(image)
            
            
        server = smtplib.SMTP("smtp.gmail.com", 587, None, 30)
        server.starttls()
        server.login(self.validUsers[recipient]['Email Address'], self.validUsers[recipient]['Email Password'])
        server.sendmail('computer', self.validUsers[recipient]['SMS'], msg.as_string())
        server.close()
        


    def _compress(self, fileName, extension):
        """Given a filename, will compress the file using ffmpeg in order for it to be deliverable
        to a recipient's cellphone. If the compressed file is still >= 1.8MB, will return an error
        statement stating so. For now, can only compress webm and mp4 files."""
        encoder = None
        crf = 0
        output = 'output.' + extension
        result = "File compressed. Sending to recipient."
        if extension.lower() == 'mp4':
            crf = 30
            encoder = 'libx264'
        elif extension.lower() == 'webm':
            crf = 63
            encoder = 'libvpx-vp9'
   
        inD = {fileName: None}
        outD = {output: '-c:v {} -crf {}'.format(encoder, crf)}
        ff = ffmpy.FFmpeg(executable = 'C:\\ffmpeg\\bin\\ffmpeg.exe', inputs = inD, outputs = outD)
        print("Running FFmpeg command: " + ff.cmd)
        ff.run()

        if self._fileTooBig(output):
            result = 'WARNING: File larger than 1.8MB. Highly probable that file will not reach recipient.'
        return result


    def _copyFile(self, fileName):
        with open(fileName, 'wb') as file:
            self._sendData("Ready to receive file.")
            data = self._recvData()
            print("Receiving File")
            file.write(data)
        print("Finished copying file\n")


    def _fileTooBig(self, fileName):
        fileStats = os.stat(fileName)
        size = fileStats.st_size
        if size >= 1800000:
            return True
        return False


    def _sendFileInfo(self):
        fileInfo = ""
        for fileName in os.listdir():
            statinfo = os.stat(fileName)
            size = statinfo.st_size / 1000000
            fileInfo += fileName + '\t' + str(round((size), 2)) + " MB\n"
        self._sendData(fileInfo)


    def _fileExists(self, fileName) -> bool:
        return fileName in os.listdir()




                
# def _commandHasErrors(self, command) -> bool:
#         """Takes a command, split by its white spaces, and sees if it is formatted correctly. If it is,
#         return 'False' as in there are no errors. Otherwise, return 'True'
#         as in there is an error."""
#         if command[0] not in self.commands:
#             print("ERROR: Command '{}' does not exist. Type 'help' to see available commands.\n".format(command[0]))
#             return True
#
#         check = command[0]
#         if check == "send":
#             if len(command) < 2 or len(command) > 3:
#                 print("ERROR: 'send' command incorrectly formatted. Type 'help' to see correct format.\n")
#                 return True
#             elif self._fileExists(command[1]) == False:
#                 print("ERROR: The file '{}' does not exist. Type 'ls' to see list of available files in directory.\n".format(command[1]))
#                 return True
#
#         elif check == "sendSMS":
#             if len(command) < 3 or len(command) > 3:
#                 print("ERROR: 'sendSMS' command incorrectly formatted. Type 'help' to see correct format.\n")
#                 return True
#
#             elif self._fileExists(command[-1]) == False:
#                 print("ERROR: The file '{}' does not exist. Type 'ls' to see list of available files in directory.\n".format(command[1]))
#                 return True
#
#             elif self._fileCorrectType(command[-1]) == False:
#                 extension = command[-1].split('.')[-1]
#                 print("ERROR: Cannot send files of type '{}'. Type 'help' to see supported file types.\n".format(extension))
#                 return True
#
#         elif check == "ls":
#             if len(command) > 2 or (len(command) == 2 and command[1] != '-s'):
#                 print("ERROR: 'ls' command incorrectly formatted. Type 'help' to see correct format.\n")
#                 return True
#
#         elif check == "SMSLog":
#             if len(command) > 1:
#                 print("ERROR: 'SMSLog' command incorrectly formatted. Type 'help' to see correct format.\n")
#                 return True
#
#         elif check == "help" and len(command) > 1:
#             print("ERROR: 'help' command incorrectly formatted. Type 'help' to see correct format.\n")
#             return True
#
#         elif check == "q" and len(command) > 1:
#             print("ERROR: 'q' command incorrectly formatted. Type 'help' to see correct format.\n")
#             return True
#
#         return False
