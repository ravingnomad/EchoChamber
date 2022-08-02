from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, SlideTransition

import enum
import echoChamberWindow



class ViolationEnum(enum.Enum):
    presetViolation = 0
    smsViolation = 1
    phoneViolation = 2
    emailViolation = 3
    passwordViolation = 4
    emptyFieldViolation = 5
    
    
    
    


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
        self.fieldViolations = [0 for i in range(len(ViolationEnum))]
        self.validPasswordChars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        self.allPresetNames = {}
      
      
    def on_pre_enter(self):
        if self.loadedPresetName != None:
            self.preset_name.text = self.loadedPresetName
        self.allPresetNames = self.parent.presetScreen.samplePresetData.keys()
        self._checkEmptyFields()
        self.checkSMSViolation()

        
    def on_leave(self):
        self._clearFields()
        
        
    def _clearFields(self):
        self.preset_name.text = ""
        self.loadedPresetName = None
        self.sms.spinner_dropdown.text = "Click to choose SMS"
        self.phone.text = ""
        self.email.text = ""
        self.password.text = ""
        
        
    def hasFieldViolation(self):
        return any(self.fieldViolations)
        
        
    def _checkEmptyFields(self):
        emptyFields = []
        if self.preset_name.text == "":
            emptyFields.append(self.preset_widget)
        if self.phone.text == "":
            emptyFields.append(self.phone_widget)
        if self.email.text == "":
            emptyFields.append(self.email_widget)
        if self.password.text == "":
            emptyFields.append(self.password_widget)
            
        if emptyFields != []:
            self.fieldViolations[ViolationEnum.emptyFieldViolation.value] = 1
            self._turnRedEmptyFields(emptyFields)
        else:
            self.fieldViolations[ViolationEnum.emptyFieldViolation.value] = 0
            
            
    def _turnRedEmptyFields(self, fields):
        for field in fields:
            self._changeFieldColor(field, 'red')
            
            
    def checkSMSViolation(self):
        if self.sms.spinner_dropdown.text == "Click to choose SMS":
            self.fieldViolations[ViolationEnum.smsViolation.value] = 1
        else:
            self.fieldViolations[ViolationEnum.smsViolation.value] = 0
            
            
    def checkPresetNameField(self, text):
        if (text.strip() != self.loadedPresetName and text.strip() in self.allPresetNames) or text.strip() == "":
            self.fieldViolations[ViolationEnum.presetViolation.value] = 1
            self._changeFieldColor(self.preset_widget, 'red')
        else:
            self.fieldViolations[ViolationEnum.presetViolation.value] = 0
            self._changeFieldColor(self.preset_widget, 'black')

        
    def checkPhoneNumberField(self, text):
        if len(text) != 10 or text.isdigit() == False or text.strip() == "":
            self.fieldViolations[ViolationEnum.phoneViolation.value] = 1
            self._changeFieldColor(self.phone_widget, 'red')
        else:
            self.fieldViolations[ViolationEnum.phoneViolation.value] = 0
            self._changeFieldColor(self.phone_widget, 'black')
    
    
    def checkEmailField(self, text):
        splitText = text.split('@')
        if len(splitText) != 2 or splitText[0] == "" or splitText[-1] != 'gmail.com' or text.strip() == "":
            self.fieldViolations[ViolationEnum.emailViolation.value] = 1
            self._changeFieldColor(self.email_widget, 'red')
        else:
            self.fieldViolations[ViolationEnum.emailViolation.value] = 0
            self._changeFieldColor(self.email_widget, 'black')
    
    
    def checkPasswordField(self, text):
        if self._validPassword(text) == False or text.strip() == "":
            self.fieldViolations[ViolationEnum.passwordViolation.value] = 1
            self._changeFieldColor(self.password_widget, 'red')
        else:
            self.fieldViolations[ViolationEnum.passwordViolation.value] = 0
            self._changeFieldColor(self.password_widget, 'black')
            
            
    def _validPassword(self, pswd):
        for char in pswd:
            if char not in self.validPasswordChars:
                return False
        return True
            
            
    def _changeFieldColor(self, field, color):
        if color.lower() == 'black':
            field.requirement_text.color = [0, 0, 0, 1]
        if color.lower() == 'red':
            field.requirement_text.color = [1, 0, 0, 1]
            
        

    def exitButton(self):
        self.manager.transition = SlideTransition(direction = "right")
        self.manager.current = 'loadPresetScreen'
        
        
    def saveButton(self):
        #have to check; no trigger event that can trigger a check for all fields only once; if don't check, when adding new preset, 
        #this field violation will still have its flag raised
        self._checkEmptyFields()
        print(self.fieldViolations)
        if self.hasFieldViolation() == False:
            if self._presetNameChanged():
                del self.parent.presetScreen.samplePresetData[self.loadedPresetName]
                newPresetName = self.preset_name.text
                self.parent.presetScreen.samplePresetData[newPresetName] = {}
            self._saveEntries()
            self.manager.transition = SlideTransition(direction = "right")
            self.manager.current = 'loadPresetScreen'
            
            
    def _presetNameChanged(self):
        return self.loadedPresetName != None and self.loadedPresetName != self.preset_name.text
            
    
    def _saveEntries(self):
        toSaveDict = {}
        if self.preset_name.text in self.parent.presetScreen.samplePresetData.keys():
            toSaveDict = self.parent.presetScreen.samplePresetData[self.preset_name.text]
        toSaveDict['sms'] = self.sms.spinner_dropdown.text
        toSaveDict['phone'] = self.phone.text
        toSaveDict['email'] = self.email.text
        toSaveDict['password'] = self.password.text
        self.parent.presetScreen.samplePresetData[self.preset_name.text] = toSaveDict

        