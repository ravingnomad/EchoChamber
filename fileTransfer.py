import os, smtplib, ffmpeg

from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from moviepy.editor import VideoFileClip



class FileTransfer():


    def __init__(self):
        self.fileSizeLimit = 7000000 #7 MB
        self.targetSize = 7000 #7 MB before calc
        #have to be careful; this bit rate MUST allow for subsequent webm file 
        #to be under 7MB limit
        self._webmBitrate = "4500k"
        self._compressedFileNames = {'webm': "compressedFile.mp4",
                                     'mp4': "compressedFile.mp4",
                                     'gif': "compressedFile.webm"}
        self.compressionFuncs = {'webm': self._compress,
                                 'mp4': self._compress,
                                 'gif': self._convertGifToWebm}
        self.carrierAddresses = {"Verizon": {"sms": "@vtext.com", "mms": "@vzwpix.com"},
                   "AT&T": {"sms": "@txt.att.net", "mms": "@mms.att.net"},
                   "Sprint": {"sms": "@messaging.sprintpcs.com", "mms": "@pm.sprint.com"}, 
                   "T-Mobile": {"sms": "@tmomail.net", "mms": "@tmomail.net"}}


    def _textFile(self, carrier, phoneNumber, email, password, fileName):
        messageAddress = self.formatMsgAddr(fileName, carrier, phoneNumber)
        mimeMsg = self._createMIME(fileName, email, messageAddress)
        server = smtplib.SMTP("smtp.mail.yahoo.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(email, password)
        server.sendmail(email, [messageAddress], mimeMsg.as_string())
        server.quit()
        
        
    def formatMsgAddr(self, fileName, carrier, phoneNumber):
        extension = self._getFileExtension(fileName)
        address = phoneNumber
        if extension in ["mp4", "webm", "gif"]:
            address += self.carrierAddresses[carrier]['mms']
        else:
            address += self.carrierAddresses[carrier]['sms']
        return address
        
        
    def _createMIME(self, fileName: str, email, sms):
        fileExtension = self._getFileExtension(fileName)
        fileData = self._readDataFromFile(fileName)
        msg = MIMEMultipart()
        msg['Subject'] = 'Echo Chamber SMS'
        msg['From'] = email
        msg['To'] = sms
        msg['Date'] = formatdate(localtime = True)
        if fileExtension in ('webm', 'mp4', 'gif'):
            text = MIMEText("Video File")
            msg.attach(text)
            data = MIMEBase('video', 'webm')
            data.set_payload(fileData)
            encoders.encode_base64(data)
            data.add_header('Content-Disposition', 'attachment', filename = fileName)
            msg.attach(data)
        elif fileExtension == 'txt':
            text = MIMEText(fileData, _charset = "UTF-8")
            msg.attach(text)
        else:
            text = MIMEText("Image File")
            msg.attach(text)
            image = MIMEImage(fileData)
            msg.attach(image)
        return msg
    
    
    def _readDataFromFile(self, fileName):
        if self._fileTooBig(fileName):
            fileExtension = self._getFileExtension(fileName)
            #compress file based on its file extension
            self.compressionFuncs[fileExtension](fileName)
            compressedFileName = self._compressedFileNames[fileExtension]
            with open(compressedFileName, 'rb') as compressedFile:
                fileData = compressedFile.read()
        else:
            with open(fileName, 'rb') as file:
                fileData = file.read()
        return fileData
    
    
    def _fileTooBig(self, fileName):
        fileStats = os.stat(fileName)
        size = fileStats.st_size
        return size > self.fileSizeLimit
    
    
    #converting a gif to a webm allows for editing of its file size
    def _convertGifToWebm(self, fileName):
        compressedFileName = self._compressedFileNames['gif']
        gifClip = VideoFileClip(fileName) 
        gifClip.write_videofile(compressedFileName, bitrate = self._webmBitrate)
    

    def _compress(self, fileName):
        fileExtension = self._getFileExtension(fileName)
        min_audio_bitrate = 32000
        max_audio_bitrate = 256000
        outputFileName = self._compressedFileNames[fileExtension]
        probe = ffmpeg.probe(fileName)
        duration = float(probe['format']['duration'])
        audio_bitrate = min_audio_bitrate
        target_total_bitrate = (self.targetSize * 8192) / (1.073741824 * duration)
        video_bitrate = target_total_bitrate - audio_bitrate
        i = ffmpeg.input(fileName)
        try:
            ffmpeg.output(i, os.devnull,
                          **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
                          ).overwrite_output().run()
            ffmpeg.output(i, outputFileName,
                          **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
                          ).overwrite_output().run()
        except ffmpeg.Error as e:
            print(e)
        
        
    def _getFileExtension(self, fileName):
        return fileName.split('.')[-1].lower()
