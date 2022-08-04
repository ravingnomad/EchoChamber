import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder 
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

import os 

Builder.load_file("main_screen.kv")

class MainScreenLayout(BoxLayout):
    computer_screen = ObjectProperty(None)
    phone_screen = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(MainScreenLayout, self).__init__(**kwargs)
        parentDirectory = os.path.join(os.getcwd(), os.pardir)
        self.computer_screen.file_list.path = parentDirectory
        
    def transferFile(self):
        files = self.computer_screen.file_list.selection
        if files:
            self.phone_screen.transferred_files.test_text.text = files[0] 
        else:
            self.phone_screen.transferred_files.test_text.text = "None"
    

class mainApp(App):
    def build(self):
        return MainScreenLayout()

if __name__ == "__main__":
    mainApp().run()