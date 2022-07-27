import kivy
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.clock import Clock


import echoChamberWindow

class EditScreenLayout(Screen):
    preset_name = ObjectProperty(None)
    sms = ObjectProperty(None)
    phone = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    
    def __init__(self, *args, **kwargs):
        super(EditScreenLayout, self).__init__(**kwargs)
        self.loadedPresetName = None
        #Clock.schedule_once(self.assignPresetName, .1)
      
      
    def on_enter(self):
        self.loadedPresetName = self.preset_name.text
        print(f"Current phone value: {self.phone.text_input.text}")
        
    def exitButton(self):
        self.manager.transition = SlideTransition(direction = "right")
        self.manager.current = 'loadPresetScreen'
        
    def saveButton(self):
        if self._presetNameChanged():
            del self.parent.presetScreen.samplePresetData[self.loadedPresetName]
            newPresetName = self.preset_name.text
            self.parent.presetScreen.samplePresetData[newPresetName] = {}
        self._saveEntries()
        self.manager.transition = SlideTransition(direction = "right")
        self.manager.current = 'loadPresetScreen'


    def _presetNameChanged(self):
        return self.loadedPresetName != self.preset_name.text
    
#"preset10": {'sms': 'T-Mobile', 'phone': 000000000, 'email': 'example10@gmail.com', 'password': 'C@pi+an'}
    def _saveEntries(self):
        toSaveDict = self.parent.presetScreen.samplePresetData[self.preset_name.text]
        toSaveDict['sms'] = self.sms.spinner_dropdown.text
        toSaveDict['phone'] = self.phone.text_input.text
        toSaveDict['email'] = self.email.text_input.text
        toSaveDict['password'] = self.password.text_input.text
        self.parent.presetScreen.samplePresetData[self.preset_name.text] = toSaveDict
        