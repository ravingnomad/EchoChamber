from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.core.window import Window

import os 



class MainScreenLayout(Screen):
    computer_screen = ObjectProperty(None)
    phone_screen = ObjectProperty(None)
    preset_name = StringProperty()
    formattedSMS = StringProperty()
        
        
    def __init__(self, **kwargs):
        super(MainScreenLayout, self).__init__(**kwargs)
        self.presetInfo = {}
        
        
    def on_pre_enter(self):
        parentDirectory = os.path.join(os.getcwd(), os.pardir)
        self.computer_screen.file_list.path = parentDirectory
        self.formattedSMS = "PHONENUMBER@SMS"
        print(f"This is the preset info: {self.presetInfo}")
        
        
    def transferFile(self):
        files = self.computer_screen.file_list.selection
        if files:
            self.phone_screen.transferred_files.test_text.text = files[0] 
        else:
            self.phone_screen.transferred_files.test_text.text = "None"
            
            
    def changePresetButton(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = "loadPresetScreen"
        
        
    def viewPresetButton(self):
        self.parent.editScreen.screenEnteredFrom = "echoChamberMainScreen"
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = "editPresetScreen"

        
        
    def exitButton(self):
        Window.close()
