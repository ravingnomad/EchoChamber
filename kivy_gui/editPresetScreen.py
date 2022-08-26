from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, SlideTransition

import smtplib
import enum
import echoChamberWindow
import emailPasswordVerifyScreen


#used to check for field violations; these act as indices in a list in EditScreenLayout; if any
#element in the list is a 1, means there is a violation; a lot more legible and less cumbersome than
#having a disinct bool for every field to check for violations
class ViolationEnum(enum.Enum):
    presetViolation = 0
    carrierViolation = 1
    phoneViolation = 2
    emailViolation = 3
    passwordViolation = 4
    emptyFieldViolation = 5
    



class EditScreenLayout(Screen):
    preset_widget = ObjectProperty(None)
    carrier_widget = ObjectProperty(None)
    phone_widget = ObjectProperty(None)
    email_widget = ObjectProperty(None)
    password_widget = ObjectProperty(None)
    save_button = ObjectProperty(None)
    
    
    def __init__(self, *args, **kwargs):
        super(EditScreenLayout, self).__init__(**kwargs)
        self.loadedPresetName = None
        self.loadedPresetInfo = None
        self.fieldViolations = [0 for i in range(len(ViolationEnum))]
        self.validPasswordChars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        self.allPresetNames = []
        self.screenEnteredFrom = None
      
    
    def setText(self, field, text):
        if field == self.carrier_widget:
            field.spinner_dropdown.text = text 
        else:
            field.text_input.text = text
    
    
    def getText(self, field):
        if field == self.carrier_widget:
            return field.spinner_dropdown.text
        return field.text_input.text
    
    
    def _changeFieldColor(self, field, color):
        if color.lower() == 'black':
            field.requirement_text.color = [0, 0, 0, 1]
        if color.lower() == 'red':
            field.requirement_text.color = [1, 0, 0, 1]
      
      
    def on_pre_enter(self):
        if self.loadedPresetName != None:
            self.setText(self.preset_widget, self.loadedPresetName)
        if self.loadedPresetInfo != None:
            self.setText(self.carrier_widget, self.loadedPresetInfo['carrier'])
            self.setText(self.phone_widget, self.loadedPresetInfo['phone'])
            self.setText(self.email_widget, self.loadedPresetInfo['email'])
            self.setText(self.password_widget, self.loadedPresetInfo['password'])
        self.allPresetNames = self.parent.presetScreen.presetData.keys()
        self._checkEmptyFields()
        self.checkCarrierViolation()
        #disable ability to edit fields if entered from echo chamber main screen
        if self.screenEnteredFrom == "echoChamberMainScreen":
            self._disableWidgets()

        
    def _disableWidgets(self):
        self.preset_widget.text_input.disabled = True
        self.phone_widget.text_input.disabled = True
        self.email_widget.text_input.disabled = True
        self.password_widget.text_input.disabled = True
        self.carrier_widget.spinner_dropdown.disabled = True
        self.save_button.disabled = True
        
        
    def _enableWidgets(self):
        self.preset_widget.text_input.disabled = False
        self.phone_widget.text_input.disabled = False
        self.email_widget.text_input.disabled = False
        self.password_widget.text_input.disabled = False
        self.carrier_widget.spinner_dropdown.disabled = False
        self.save_button.disabled = False
        
        
    def on_leave(self):
        self._clearFields()
        self._enableWidgets()
        
        
    def _clearFields(self):
        self.setText(self.preset_widget, "")
        self.loadedPresetName = None
        self.loadedPresetInfo = None
        self.setText(self.carrier_widget, "Click to choose carrier")
        self.setText(self.phone_widget, "")
        self.setText(self.email_widget, "")
        self.setText(self.password_widget, "")
        
        
    def hasFieldViolation(self):
        return any(self.fieldViolations)
        
        
    def _checkEmptyFields(self):
        emptyFields = []
        if self.getText(self.preset_widget) == "":
            emptyFields.append(self.preset_widget)
        if self.getText(self.phone_widget) == "":
            emptyFields.append(self.phone_widget)
        if self.getText(self.email_widget) == "":
            emptyFields.append(self.email_widget)
        if self.getText(self.password_widget) == "":
            emptyFields.append(self.password_widget)
            
        if emptyFields != []:
            self.fieldViolations[ViolationEnum.emptyFieldViolation.value] = 1
            self._turnRedEmptyFields(emptyFields)
        else:
            self.fieldViolations[ViolationEnum.emptyFieldViolation.value] = 0
            
            
    def _turnRedEmptyFields(self, fields):
        for field in fields:
            self._changeFieldColor(field, 'red')
            
            
    def checkCarrierViolation(self):
        if self.getText(self.carrier_widget) == "Click to choose carrier":
            self.fieldViolations[ViolationEnum.carrierViolation.value] = 1
        else:
            self.fieldViolations[ViolationEnum.carrierViolation.value] = 0
            
            
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
        if len(splitText) != 2 or splitText[0] == "" or splitText[-1] != 'yahoo.com' or text.strip() == "":
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
    
    
    #check to see if email and email password can be used to login to email;
    #checks by logging into email through smtplib; if success, no exceptions are raised; otherwise
    #SMTPServerDisconnected is raised if password invalid; TypeError is raised if 
    #email is empty
    def verifyPwdEmail(self):
        msgString = "Valid email and password."
        try:
            email = self.getText(self.email_widget)
            password = self.getText(self.password_widget)
            server = smtplib.SMTP("smtp.mail.yahoo.com", 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(email, password)
            server.quit()
        except smtplib.SMTPServerDisconnected:
            msgString = "ERROR: Email and/or password are incorrect and cannot be used\n to login to the specified email. Please check." 
        except TypeError:
            msgString = "ERROR: Email and/or password must not be empty."
        finally:
            popUpObject = emailPasswordVerifyScreen.EmailPasswordVerifyScreen(msgString)
            popUpObject.open()
            
            


    def exitButton(self):
        self.manager.transition = SlideTransition(direction = "right")
        self.manager.current = self.screenEnteredFrom
        
        
    def saveButton(self):
        #have to check for empty fields and reset empty field violation flag; there is no trigger event/callback
        #that allows for resetting of the empty fields violation flag when all
        #fields are non-empty, unless a check is made after each entry of each field
        #if don't check, when adding new preset, this empty fields violation will still have its flag raised 
        self._checkEmptyFields()
        if self.hasFieldViolation() == False:
            if self._presetNameChanged():
                del self.parent.presetScreen.presetData[self.loadedPresetName]
                newPresetName = self.getText(self.preset_widget)
                self.parent.presetScreen.presetData[newPresetName] = {}
            self._saveEntries()
            self.manager.transition = SlideTransition(direction = "right")
            self.manager.current = 'loadPresetScreen'
            
            
    def _presetNameChanged(self):
        return self.loadedPresetName != None and self.loadedPresetName != self.getText(self.preset_widget)
            
    
    def _saveEntries(self):
        toSaveDict = {}
        currentPresetName = self.getText(self.preset_widget)
        if currentPresetName in self.allPresetNames:
            toSaveDict = self.parent.presetScreen.presetData[currentPresetName]
        toSaveDict['carrier'] = self.getText(self.carrier_widget)
        toSaveDict['phone'] = self.getText(self.phone_widget)
        toSaveDict['email'] = self.getText(self.email_widget)
        toSaveDict['password'] = self.getText(self.password_widget)
        self.parent.presetScreen.presetData[currentPresetName] = toSaveDict

        