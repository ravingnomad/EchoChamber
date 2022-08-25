from kivy.properties import StringProperty
from kivy.lang import Builder 
from kivy.uix.popup import Popup
from kivy.app import App


class EmailPasswordVerifyScreen(Popup):
    screenMessage = StringProperty()
    
    def __init__(self, msg):
        super(EmailPasswordVerifyScreen, self).__init__()
        self.msg = msg 
        
    
    def on_open(self):
        self.screenMessage = self.msg