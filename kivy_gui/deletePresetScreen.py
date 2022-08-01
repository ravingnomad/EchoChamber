from kivy.config import Config
Config.set('graphics', 'resizable', 0)

from kivy.core.window import Window
windowMinWidth = 500
windowMinHeight = 180
Window.minimum_width, Window.minimum_height = windowMinWidth, windowMinHeight
Window.size = (windowMinWidth, windowMinHeight)

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout


Builder.load_file("delete_preset_screen.kv")

class DeletePresetScreen(FloatLayout):
    pass 


#class MyApp(App):
#    def build(self):
#       return DeletePresetScreen()
    
    
    
#if __name__ == "__main__":
#    MyApp().run()