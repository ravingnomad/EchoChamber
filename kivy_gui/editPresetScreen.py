import kivy
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.clock import Clock
from kivy.graphics import Color


import echoChamberWindow

class EditScreenLayout(Screen):
    preset_widget = ObjectProperty(None)
    preset_name = ObjectProperty(None)
    sms = ObjectProperty(None)
    phone_widget = ObjectProperty(None)
    phone = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    
    def __init__(self, *args, **kwargs):
        super(EditScreenLayout, self).__init__(**kwargs)
        self.loadedPresetName = None
        self.presetNameViolation = False
        self.phoneViolation = False 
        self.emailViolation = False 
        self.passwordViolation = False
        self.validPasswordChars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        self.allPresetNames = {}
      
      
    def on_enter(self):
        self.loadedPresetName = self.preset_name.text
        self.allPresetNames = self.parent.presetScreen.samplePresetData.keys()
        
        
    def exitButton(self):
        self.manager.transition = SlideTransition(direction = "right")
        self.manager.current = 'loadPresetScreen'
        
        
    def saveButton(self):
        if self.hasFieldViolation() == False:
            if self._presetNameChanged():
                del self.parent.presetScreen.samplePresetData[self.loadedPresetName]
                newPresetName = self.preset_name.text
                self.parent.presetScreen.samplePresetData[newPresetName] = {}
            self._saveEntries()
            self.manager.transition = SlideTransition(direction = "right")
            self.manager.current = 'loadPresetScreen'
            
    
    def _saveEntries(self):
        toSaveDict = self.parent.presetScreen.samplePresetData[self.preset_name.text]
        toSaveDict['sms'] = self.sms.spinner_dropdown.text
        toSaveDict['phone'] = self.phone.text
        toSaveDict['email'] = self.email.text
        toSaveDict['password'] = self.password.text
        self.parent.presetScreen.samplePresetData[self.preset_name.text] = toSaveDict


    def checkPresetNameField(self, text):
        if text.strip() != self.loadedPresetName and text.strip() in self.allPresetNames:
            self.presetNameViolation = True
            self.preset_widget.requirement_text.color = [1, 0, 0, 1]
        else:
            self.presetNameViolation = False
            self.preset_widget.requirement_text.color = [0, 0, 0, 1]

        
    def checkPhoneNumberField(self, text):
        if len(text) != 10 or text.isdigit() == False:
            self.phoneViolation = True
            self.phone_widget.requirement_text.color = [1, 0, 0, 1]
        else:
            self.phoneViolation = False
            self.preset_widget.requirement_text.color = [0, 0, 0, 1]
    
    
    def checkEmailField(self, text):
        splitText = text.split('@')
        if len(splitText) != 2 or splitText[-1] != 'gmail.com':
            self.emailViolation = True
            self.email_widget.requirement_text.color = [1, 0, 0, 1]
        else:
            self.emailViolation = False
            self.email_widget.requirement_text.color = [0, 0, 0, 1]
    
    
    def checkPasswordField(self, text):
        if self._validPassword(text) == False:
            self.passwordViolation = True
            self.password_widget.requirement_text.color = [1, 0, 0, 1]
        else:
            self.passwordViolation = False
            self.password_widget.requirement_text.color = [0, 0, 0, 1]
            
    
    def _validPassword(self, pswd):
        for char in pswd:
            if char not in self.validPasswordChars:
                return False
        return True

        
    def hasFieldViolation(self):
        return self.presetNameViolation or self.phoneViolation or self.emailViolation or self.passwordViolation


    def _presetNameChanged(self):
        return self.loadedPresetName != self.preset_name.text

        