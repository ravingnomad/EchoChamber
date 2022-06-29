import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder 
from kivy.uix.boxlayout import BoxLayout

Builder.load_file("edit_screen.kv")

class EditScreenLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(EditScreenLayout, self).__init__(**kwargs)
        

class mainApp(App):
    def build(self):
        return EditScreenLayout()

if __name__ == "__main__":
    mainApp().run()