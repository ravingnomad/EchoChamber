from kivy.lang import Builder 
from kivy.app import App 
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty

import editPresetScreen
import mainScreen
import loadPresetScreen
import os



class EchoChamberWindow(ScreenManager):
    presetScreen = ObjectProperty(None)
    editScreen = ObjectProperty(None)
    def __init__(self, userInfo: {}):
        super(EchoChamberWindow, self).__init__()
        self.presetScreen.samplePresetData = userInfo
        

        
class EchoChamberApp(App):
    
    def __init__(self, testInfo: {}):
        super(EchoChamberApp, self).__init__()
        self.testInfo = testInfo
    
    def build(self):
        currFilePath = os.path.abspath(__file__)
        kivyGUIDirPath = os.path.abspath(os.path.join(currFilePath, os.pardir))
        cwd = os.getcwd()
        if kivyGUIDirPath == cwd:
            Builder.load_file("echo_chamber_window.kv")
            Builder.load_file("load_preset_screen.kv")
            Builder.load_file("edit_preset_screen.kv")
            Builder.load_file("delete_preset_screen.kv")
            Builder.load_file("main_screen.kv")
        else:
            Builder.load_file(".\kivy_gui\echo_chamber_window.kv")
            Builder.load_file(".\kivy_gui\load_preset_screen.kv")
            Builder.load_file(".\kivy_gui\edit_preset_screen.kv")
            Builder.load_file(".\kivy_gui\delete_preset_screen.kv")
            Builder.load_file(".\kivy_gui\main_screen.kv")
            pass
        manager = EchoChamberWindow(self.testInfo)
        return manager
    

if __name__ == "__main__":

    EchoChamberApp().run()