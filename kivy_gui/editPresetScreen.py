from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, SlideTransition

import echoChamberWindow




class EditScreenLayout(Screen):
    preset_widget = ObjectProperty(None)
    preset_name = ObjectProperty(None)
    sms = ObjectProperty(None)
    phone_widget = ObjectProperty(None)
    phone = ObjectProperty(None)
    email_widget = ObjectProperty(None)
    email = ObjectProperty(None)
    password_widget = ObjectProperty(None)
    password = ObjectProperty(None)
    
    def __init__(self, *args, **kwargs):
        super(EditScreenLayout, self).__init__(**kwargs)
        self.loadedPresetName = None
        self.presetNameViolation = False
        self.phoneViolation = False 
        self.emailViolation = False 
        self.passwordViolation = False
        self.emptyFieldViolation = False
        self.validPasswordChars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        self.allPresetNames = {}
      
      
    def on_pre_enter(self):
        if self.loadedPresetName != None:
            print(self.loadedPresetName)
            self.preset_name.text = self.loadedPresetName
        self.allPresetNames = self.parent.presetScreen.samplePresetData.keys()
        self._checkEmptyFields()

        
    def on_leave(self):
        self._clearFields()
        
        
    def _clearFields(self):
        self.preset_name.text = ""
        self.loadedPresetName = None
        self.sms.spinner_dropdown.text = "Click to choose SMS"
        self.phone.text = ""
        self.email.text = ""
        self.password.text = ""
        
        
    def _checkEmptyFields(self):
        if self.preset_name.text == "":
            self.preset_widget.requirement_text.color = [1, 0, 0, 1]
            self.emptyFieldViolation = True
        if self.phone.text == "":
            self.phone_widget.requirement_text.color = [1, 0, 0, 1]
            self.emptyFieldViolation = True
        if self.email.text == "":
            self.email_widget.requirement_text.color = [1, 0, 0, 1]
            self.emptyFieldViolation = True 
        if self.password.text == "":
            self.password_widget.requirement_text.color = [1, 0, 0, 1]
            self.emptyFieldViolation = True
        else:
            self.emptyFieldViolation = False
        
        
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
        toSaveDict = {}
        if self.preset_name.text in self.parent.presetScreen.samplePresetData.keys():
            toSaveDict = self.parent.presetScreen.samplePresetData[self.preset_name.text]
        toSaveDict['sms'] = self.sms.spinner_dropdown.text
        toSaveDict['phone'] = self.phone.text
        toSaveDict['email'] = self.email.text
        toSaveDict['password'] = self.password.text
        self.parent.presetScreen.samplePresetData[self.preset_name.text] = toSaveDict


    def checkPresetNameField(self, text):
        if (text.strip() != self.loadedPresetName and text.strip() in self.allPresetNames) or text.strip() == "":
            self.presetNameViolation = True
            self._changeFieldColor(self.preset_widget.requirement_text, 'red')
        else:
            self.presetNameViolation = False
            self._changeFieldColor(self.preset_widget.requirement_text, 'black')

        
    def checkPhoneNumberField(self, text):
        if len(text) != 10 or text.isdigit() == False or text.strip() == "":
            self.phoneViolation = True
            self._changeFieldColor(self.phone_widget.requirement_text, 'red')
        else:
            self.phoneViolation = False
            self._changeFieldColor(self.phone_widget.requirement_text, 'black')
    
    
    def checkEmailField(self, text):
        splitText = text.split('@')
        if len(splitText) != 2 or splitText[0] == "" or splitText[-1] != 'gmail.com' or text.strip() == "":
            self.emailViolation = True
            self._changeFieldColor(self.email_widget.requirement_text, 'red')
        else:
            self.emailViolation = False
            self._changeFieldColor(self.email_widget.requirement_text, 'black')
    
    
    def checkPasswordField(self, text):
        if self._validPassword(text) == False or text.strip() == "":
            self.passwordViolation = True
            self._changeFieldColor(self.password_widget.requirement_text, 'red')
        else:
            self.passwordViolation = False
            self._changeFieldColor(self.password_widget.requirement_text, 'black')
            
            
    def _changeFieldColor(self, field, color):
        if color.lower() == 'black':
            field.color = [0, 0, 0, 1]
        if color.lower() == 'red':
            field.color = [1, 0, 0, 1]
            
            
    def hasSMSViolation(self):
        return self.sms.spinner_dropdown.text == "Click to choose SMS"
        
            
    def _validPassword(self, pswd):
        for char in pswd:
            if char not in self.validPasswordChars:
                return False
        return True

        
    def hasFieldViolation(self):
        self._checkEmptyFields()
        return self.presetNameViolation or self.phoneViolation or self.emailViolation or self.passwordViolation or\
             self.emptyFieldViolation or self.hasSMSViolation()


    def _presetNameChanged(self):
        return self.loadedPresetName != None and self.loadedPresetName != self.preset_name.text

        