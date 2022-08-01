import loadPresetScreen
import editPresetScreen
#import deletePresetScreen
import kivy
from kivy.lang import Builder 
from kivy.app import App 
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.textinput import TextInput



#use buttons in other modules to call a function in this module to switch the screens?
class EchoChamberWindow(ScreenManager):
    presetScreen = ObjectProperty(None)
    editScreen = ObjectProperty(None)
    #deletePresetScreen = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(EchoChamberWindow, self).__init__()

    def loadInfoToEditScreen(self, presetName: str, presetData: dict, *args):
        self.editScreen.preset_name.text = presetName
        print(self.editScreen.preset_name.text)
        #editPresetScreen.EditScreenLayout(presetName = presetName)

        

        
class echoChamberApp(App):
    def build(self):
        Builder.load_file("echo_chamber_window.kv")
        Builder.load_file("load_preset_screen.kv")
        Builder.load_file("edit_preset_screen.kv")
        #Builder.load_file("delete_preset_screen.kv")
        manager = EchoChamberWindow()
        return manager
        
#TO DO field text correction for password (want only alphanumeric and ascii)

if __name__ == "__main__":

    echoChamberApp().run()