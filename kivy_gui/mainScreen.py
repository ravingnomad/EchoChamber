from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.core.window import Window

import os
import fileTransfer
import emailPasswordVerifyScreen
import smtplib



class MainScreenLayout(Screen):
    computer_screen = ObjectProperty(None)
    phone_screen = ObjectProperty(None)
    supported_files_label = ObjectProperty(None)
    preset_name = StringProperty()
    formattedSMS = StringProperty()
    supportedFilesString = StringProperty()
        
        
    def __init__(self, **kwargs):
        super(MainScreenLayout, self).__init__(**kwargs)
        self.presetInfo = {}
        self.supportedFileExt = ["mp4", "webm", "gif", "jpeg", "jpg", "png", "img", "txt"]
        self.smsAddress = {"Verizon": "@vtext.com",
                           "AT&T": "@txt.att.net",
                           "Sprint": "@messaging.sprintpcs.com", 
                           "T-Mobile": "@tmomail.net"}
        
        
    def on_pre_enter(self):
        parentDirectory = os.path.join(os.getcwd(), os.pardir)
        self.computer_screen.file_list.path = parentDirectory
        self._formatSMSAddress()
        self._formatSupportedFiles()
        
        
    def transferFile(self):
        try:
            fileList = self.computer_screen.file_list.selection
            if fileList and self._validFile(fileList):
                self.supported_files_label.color = [0, 0, 0, 1]
                self.phone_screen.transferred_files.test_text.text = fileList[0]
                fileTransfer.FileTransfer()._textFile(self.formattedSMS, self.presetInfo['email'], self.presetInfo['password'], fileList[0])
            else:
                self._invalidFile()
        except smtplib.SMTPServerDisconnected:
            msgString = "ERROR: Failed to send file to target due to incorrect email and/or password.\n Please check." 
            popUpObject = emailPasswordVerifyScreen.EmailPasswordVerifyScreen(msgString)
            popUpObject.open()
            
    def _validFile(self, fileList):
        fileName = fileList[0].split('\\')[-1]
        fileExtension = fileName.split('.')[-1].lower()
        return fileExtension in self.supportedFileExt
    
    
    def _invalidFile(self):
        self.supported_files_label.color = [1, 0, 0, 1]
        
            
    def changePresetButton(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = "loadPresetScreen"
        
        
    def viewPresetButton(self):
        self.parent.editScreen.loadedPresetName = self.preset_name
        self.parent.editScreen.loadedPresetInfo = self.presetInfo
        self.parent.editScreen.screenEnteredFrom = "echoChamberMainScreen"
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = "editPresetScreen"

        
    def _formatSMSAddress(self):
        smsAddress = self.smsAddress[self.presetInfo['sms']]
        self.formattedSMS = self.presetInfo['phone'] + smsAddress
        
    
    def _formatSupportedFiles(self):
        self.supportedFilesString = ', '.join(self.supportedFileExt)

        
    def exitButton(self):
        Window.close()
        

