from kivy.lang import Builder 
from kivy.app import App 
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty


import loadPresetScreen
import editPresetScreen



class EchoChamberWindow(ScreenManager):
    presetScreen = ObjectProperty(None)
    editScreen = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(EchoChamberWindow, self).__init__() 

        
class echoChamberApp(App):
    def build(self):
        Builder.load_file("echo_chamber_window.kv")
        Builder.load_file("load_preset_screen.kv")
        Builder.load_file("edit_preset_screen.kv")
        manager = EchoChamberWindow()
        return manager


if __name__ == "__main__":

    echoChamberApp().run()