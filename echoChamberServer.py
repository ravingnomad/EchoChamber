import socket, struct, sys, os, smtplib, ffmpy
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from connection import *
from test.test_string_literals import byte

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
        print("Closed connection with client\n")
                    

    def _waitForCommands(self) -> None:
        userInput = self._recvStrData()
        command, *args = userInput.split(" ")
        if command == "send":
            self._sendFileToClient(args[0])
        elif command == "sendSMS":
            self._sendSMSFile(args)
        elif command == "SMSLog":
            self._sendSMSInfo()
        elif command == "ls":
            self._sendFileInfo()
        elif command == "q":
            self.endConnection = True

    
    def _sendFileToClient(self, fileName: str) -> None:
        print(f"\nClient wants file '{fileName}'\n")
        if self._fileExists(fileName) == True:
            with open(fileName, 'rb') as file:
                self._sendData("File found")
                fileBuffer = file.read()
                clientResponse = self._recvStrData()
                if clientResponse == "Ready to receive file":
                    self._sendData(fileBuffer)
            print(f"Successfully sent '{fileName}' to client\n")
        else:
            print("ERROR: File {} does not exist.\n".format(fileName))
            self._sendData("File not found")
            

    def _sendSMSFile(self, commandArgs: list) -> None:
        print("\nClient wants to text a file to a valid recipient\n")
        fileName, recipientName = commandArgs
        if self._fileExists(fileName) == True:
            self._sendData("File found")
            if self._smsRecipientValid(recipientName) == True:
                self._sendData("Recipient found")
                self._textFile(recipientName, fileName)
                print("Sent SMS to recipient successfully\n")
            else:
                print("ERROR: recipient not valid\n")
                self._sendData("Recipient not found")
        else:
            print("ERROR: file does not exist\n")
            self._sendData("File not found") 
            
    
    def _fileExists(self, fileName: str) -> bool:
        return fileName in os.listdir()
        
        
    def _smsRecipientValid(self, recipientName: str) -> bool:
        return recipientName in self.validUsers.keys()


    def _textFile(self, recipient: str, fileName: str) -> None:
        """SMS limits sent file sizes to be around 1.8MB, so will check the size of the file and compress
        using FFmpeg. CURRENT COMPRESSION ONLY SUPPORTS MP4 AND WEBM. If file is still too large,
        will still attempt to send the file. There are no guarantees that delivery will be
        successful as entirely dependent on rules imposed by client's mobile plan. After file is sent,
        if compression used, must delete resulting compressed file after reading its info as errors will 
        arise if another compression occurs and saves with the same file name as the compressed file."""
        
        fileData = self._smsReadDataFromFile(fileName) 
        mimeMsg = self._createMIME(fileData, fileName)
        server = smtplib.SMTP("smtp.gmail.com", 587, None, 30)
        server.starttls()
        server.login(self.validUsers[recipient]['Email Address'], self.validUsers[recipient]['Email Password'])
        server.sendmail('computer', self.validUsers[recipient]['SMS'], mimeMsg.as_string())
        server.close()
    
    
    def _smsReadDataFromFile(self, fileName: str) -> byte:
        fileExtension = fileName.split('.')[-1].lower()
        fileData = None
        if self._fileTooBig(fileName) and fileExtension in ('webm', 'mp4'):
            self._compress(fileName, fileExtension)
            with open(f'compressedFile.{fileExtension}', 'rb') as compressedFile:
                fileData = compressedFile.read()
            os.remove(f'compressedFile.{fileExtension}')
        else:
            with open(fileName, 'rb') as file:
                fileData = file.read()
        return fileData
    
    
    def _createMIME(self, fileData: byte, fileName: str) -> MIMEMultipart:
        fileExtension = fileName.split('.')[-1].lower()
        msg = MIMEMultipart()
        msg['Subject'] = 'Echo Chamber SMS'
        msg['From'] = 'Server'
        msg['To'] = 'Phone'
        if fileExtension in ('webm', 'mp4'):
            data = MIMEBase('video', 'mp4')
            data.set_payload(fileData)
            encoders.encode_base64(data)
            data.add_header('Content-Disposition', 'attachment', filename = fileName)
            msg.attach(data)
            text = MIMEText("Video File")
            msg.attach(text)
        elif fileExtension == 'txt':
            text = MIMEText(fileData, _charset = "UTF-8")
            msg.attach(text)
        else:
            text = MIMEText("Image File")
            msg.attach(text)
            image = MIMEImage(fileData)
            msg.attach(image)
        return msg
        
        
    #attempts to compress files > 1.8MB; sizes above this are tricky to send; CURRENT COMPRESSION ONLY SUPPORTS MP4 AND WEBM
    def _compress(self, fileName: str, extension: str) -> None:
        encoder = None
        crf = 0
        outputFileName = 'compressedFile.' + extension
        result = "File compressed. Sending to recipient."
        if extension.lower() == 'mp4':
            crf = 30
            encoder = 'libx264'
        elif extension.lower() == 'webm':
            crf = 63
            encoder = 'libvpx-vp9'
        inD = {fileName: None}
        outD = {outputFileName: '-c:v {} -crf {}'.format(encoder, crf)}
        ff = ffmpy.FFmpeg(executable = 'C:\\ffmpeg\\bin\\ffmpeg.exe', inputs = inD, outputs = outD)
        print("Running FFmpeg command: " + ff.cmd)
        ff.run()


    def _sendSMSInfo(self) -> None:
        log = ""
        for user in self.validUsers.keys():
            log += user
            log += "\n"
        self._sendData(log)
        
        
    def _copyFile(self, fileName: str) -> None:
        with open(fileName, 'wb') as file:
            self._sendData("Ready to receive file.")
            data = self._recvData()
            print("Receiving File")
            file.write(data)
        print("Finished copying file\n")


    def _fileTooBig(self, fileName: str) -> None:
        fileStats = os.stat(fileName)
        size = fileStats.st_size
        return size >= 1800000


    def _sendFileInfo(self) -> None:
        fileInfo = ""
        for fileName in os.listdir():
            statinfo = os.stat(fileName)
            size = statinfo.st_size / 1000000
            fileInfo += fileName + '\t' + str(round((size), 2)) + " MB\n"
        self._sendData(fileInfo)
