
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup


Builder.load_file("delete_preset_screen.kv")

class DeletePresetScreen(Popup):
    delete_button = ObjectProperty(None)
    cancel_button = ObjectProperty(None) 

#class MyApp(App):
#    def build(self):
#       return DeletePresetScreen()
    
    
    
#if __name__ == "__main__":
#    MyApp().run()