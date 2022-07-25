import kivy
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, SlideTransition


import echoChamberWindow

class EditScreenLayout(Screen):
    preset_name_input = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(EditScreenLayout, self).__init__(**kwargs)
        
    def testButton(self):
        self.manager.transition = SlideTransition(direction = "right")
        self.manager.current = 'loadPresetScreen'
#class mainApp(App):
#    def build(self):
#        return EditScreenLayout()

#if __name__ == "__main__":
#    mainApp().run()