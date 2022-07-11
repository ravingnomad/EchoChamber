import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder 
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

Builder.load_file("edit_screen.kv")

class EditScreenLayout(BoxLayout):
    preset_name_input = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(EditScreenLayout, self).__init__(**kwargs)
        
        print(self.preset_name_input.text_input.text)
    

class mainApp(App):
    def build(self):
        return EditScreenLayout()

if __name__ == "__main__":
    mainApp().run()