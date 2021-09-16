import socket, struct, sys, os, smtplib, ffmpy
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from connection import *

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
            self._sendFile(args[0])
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
        elif command == "q":
            self.endConn = True

    
    def _sendFile(self, fileName: str) -> None:
        print("\nClient wants to send a file\n")
        noErrors = self._recvData().decode()
        if (noErrors == "File Exists"):
            self._copyFile(fileName)
        elif (noErrors == "Error found"):
            print("\nClient found error(s) when trying to open file. Stopping command execution\n")


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
        print("\nClient wants to see information about SMS contacts\n")
        log = None
        with open("SMSLog.txt", 'r', encoding = 'latin-1') as file:
            log = file.read()
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
        """Copies the client's specified file onto the computer"""
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

# if __name__ == "__main__":
#     
#     test._mainLoop()

    #anything greater than 1.5 needs to be compressed. Upper limit exists at around 4MB as compression
    #only takes it down to 1.8


                

