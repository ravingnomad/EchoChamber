import kivy
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.clock import Clock


import echoChamberWindow

class EditScreenLayout(Screen):
    preset_name = ObjectProperty(None)
    sms = ObjectProperty(None)
    phone = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    
    def __init__(self, *args, **kwargs):
        super(EditScreenLayout, self).__init__(**kwargs)
        #Clock.schedule_once(self.assignPresetName, .1)
        
    def exitButton(self):
        self.manager.transition = SlideTransition(direction = "right")
        self.manager.current = 'loadPresetScreen'
        

    