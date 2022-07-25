import loadPresetScreen
import editPresetScreen
import kivy
from kivy.lang import Builder 
from kivy.app import App 
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.properties import ObjectProperty




#use buttons in other modules to call a function in this module to switch the screens?
class EchoChamberWindow(ScreenManager):
    manager = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(EchoChamberWindow, self).__init__()
        print(f"Loaded screens: {self.screens}")
        print(f"Current Screen: {self.current}")

        
    def test(self):
        self.manager.current = 'editPresetScreen'
        
    def test2(self):
        self.manager.current = 'loadPresetScreen'

        
class echoChamberApp(App):
    def build(self):
        #sm = ScreenManager()
        #sm.add_widget(loadPresetScreen.PresetScreenLayout())
        #return sm
        Builder.load_file("echo_chamber_window.kv")
        Builder.load_file("load_preset_screen.kv")
        Builder.load_file("edit_preset_screen.kv")
        manager = EchoChamberWindow()
        return manager
        


if __name__ == "__main__":

    echoChamberApp().run()