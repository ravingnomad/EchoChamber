import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.weakproxy import WeakProxy
from kivy.uix.screenmanager import Screen, SlideTransition, NoTransition
from kivy.clock import Clock 
from functools import partial
import echoChamberWindow
#Set app size, and min window size
#windowStartSize = (700, 700)
#Window.size = windowStartSize
#Window.minimum_width, Window.minimum_height = windowStartSize



#Builder.load_file('load_preset_screen.kv')

class PresetName(Button):
    def __init__(self, **kwargs):
        super(PresetName, self).__init__(**kwargs)
        

class LoadButton(Button):
    def __init__(self, **kwargs):
        super(LoadButton, self).__init__(**kwargs)
        
        
class EditButton(Button):
    def __init__(self, **kwargs):
        super(EditButton, self).__init__(**kwargs)
        
        
class DeleteButton(Button):
    def __init__(self, **kwargs):
        super(DeleteButton, self).__init__(**kwargs)
        

class PresetScreenLayout(Screen):
    main_screen = ObjectProperty(None)
    top_screen = ObjectProperty(None)
    bottom_screen = ObjectProperty(None)
    new_preset_button = ObjectProperty(None) 
    exit_button = ObjectProperty(None) 
    
    def __init__(self, **kwargs):
        super(PresetScreenLayout, self).__init__(**kwargs)
        self.callbackBindings = {"Load": self.loadPresetButton,
                    "Edit": self.editPresetButton,
                    "Delete": self.deletePresetButton,
                    "+Add New Preset": self.addNewPresetButton,
                    "Exit": self.exitButton
                    } 
        self.samplePresetData = {"preset1": {'sms': 'Sprint', 'phone': '1111111111', 'email': 'example1@gmail.com', 'password': 'alonzo'},
                                 "preset2": {'sms': 'Verizon', 'phone': '2222222222', 'email': 'example2@gmail.com', 'password': 'buttercup'},
                                 "preset3": {'sms': 'Sprint', 'phone': '3333333333', 'email': 'example3@gmail.com', 'password': 'jazmina11'},
                                 "preset4": {'sms': 'T-Mobile', 'phone': '4444444444', 'email': 'example4@gmail.com', 'password': 'Kinetic'},
                                 "preset5": {'sms': 'AT&T', 'phone': '5555555555', 'email': 'example5@gmail.com', 'password': '@dam5App113'},
                                 "preset6": {'sms': 'AT&T', 'phone': '6666666666', 'email': 'example6@gmail.com', 'password': 'Futurio'},
                                 "preset7": {'sms': 'Verizon', 'phone': '7777777777', 'email': 'example7@gmail.com', 'password': 'Kam3R@'},
                                 "preset8": {'sms': 'Sprint', 'phone': '8888888888', 'email': 'example8@gmail.com', 'password': '1adf78@'},
                                 "preset9": {'sms': 'T-Mobile', 'phone': '9999999999', 'email': 'example9@gmail.com', 'password': '80085boobs'},
                                 "preset10": {'sms': 'T-Mobile', 'phone': '000000000', 'email': 'example10@gmail.com', 'password': 'C@pi+an'}
                                 }
        #this is used to make sure that the kv file is loaded
        #before the method gets called; else, properties will be
        #NoneType
        #Clock.schedule_once(self._testData, .1)
        
        
    def _testData(self, *args):
        #self.top_screen.remove_widget()
        for preset in self.samplePresetData.keys():
            test = BoxLayout(size = self.top_screen.size)
            presetNameWidget = PresetName()
            loadButtonWidget = LoadButton()
            editButtonWidget = EditButton()
            deleteButtonWidget = DeleteButton()
    
            presetNameLabel = self._copyButtonWidget(presetNameWidget)
            loadButton = self._copyButtonWidget(loadButtonWidget)
            editButton = self._copyButtonWidget(editButtonWidget)
            deleteButton = self._copyButtonWidget(deleteButtonWidget)
            
            presetNameLabel.text = f"{preset}"
            
            test.add_widget(presetNameLabel)
            test.add_widget(loadButton)
            test.add_widget(editButton)
            test.add_widget(deleteButton)
            
            self.top_screen.add_widget(widget = test)
            test.size_hint_x = 1

        
    def _copyButtonWidget(self, mainWidget) -> None:
        kwargs = {}
        
        #extracts id of Button() widget from the kivy rule
        buttonID = list(mainWidget.ids.keys())[0]
        oldButton = mainWidget.ids[buttonID]
        for attr in dir(oldButton):
            if not callable(getattr(oldButton, attr)) \
            and not attr.startswith('_') \
            and attr not in ('proxy_ref', 'refs', 'uid', 'parent', 'canvas'):
                kwargs[attr] = getattr(oldButton, attr)   
        newButton = Button(**kwargs)
        if newButton.text in self.callbackBindings.keys():
            newButton.bind(on_release = self.callbackBindings[newButton.text])
        return newButton
    
    
    #when a row is created, can check presetname of row by accessing button's parent, and checking the 'text' field of each of its 'children'
    def loadPresetButton(self, event) -> None:
        print("You clicked the 'Load' Button!")
        presetName = None 
        for child in event.parent.children:
            if child.text not in ["Load", "Edit", "Delete"]:
                presetName = child.text
        print(f"The preset name is called: {presetName}\n")
        
        
    def editPresetButton(self, event) -> None:
        presetName = None 
        for child in event.parent.children:
            if child.text not in ["Load", "Edit", "Delete"]:
                presetName = child.text
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'editPresetScreen'
        self.parent.editScreen.preset_name.text = presetName
        self.parent.editScreen.sms.spinner_dropdown.text = self.samplePresetData[presetName]['sms']
        self.parent.editScreen.phone.text = self.samplePresetData[presetName]['phone']
        self.parent.editScreen.email.text = self.samplePresetData[presetName]['email']
        self.parent.editScreen.password.text = self.samplePresetData[presetName]['password']
    
    
    def deletePresetButton(self, event) -> None:
        print("You clicked the 'Delete' Button!")
        presetName = None 
        for child in event.parent.children:
            if child.text not in ["Load", "Edit", "Delete"]:
                presetName = child.text
        print(f"The preset name is called: {presetName}\n")
        from subprocess import Popen, PIPE 
        process = Popen(['python3', 'deletePresetScreen.py'], stdout=PIPE, stderr=PIPE)
        
        
    def addNewPresetButton(self) -> None:
        print("You clicked the 'Add New Preset' Button!")
        
    
    def exitButton(self) -> None:
        print("You clicked the 'Exit' Button!")
        
        
    def on_enter(self):
        Clock.schedule_once(self._clearTopScreen, .1)
        Clock.schedule_once(self._testData, .1)
        
        
    def _clearTopScreen(self, *args):
        tempList = self.top_screen.children.copy()
        for child in tempList:
            self.top_screen.remove_widget(child)
            
    
    def _getPresetName(self, widget):
        for grandchild in widget.children:
            if grandchild.text not in ["Load", "Edit", "Delete"]:
                return grandchild.text
    
    def _printAllWidgets(self, *args):
        print("List of all widgets in top screen: ")
        for child in self.top_screen.children:
            grandchildrenText = []
            for grandchild in child.children:
                grandchildrenText.append(grandchild.text)
            print(grandchildrenText)
        #print(f"The current sample data: {self.samplePresetData}")






#class AwesomeApp(App):
#    def build(self):
 #       return PresetScreenLayout()
    

    
    
#if __name__ == "__main__":
#    AwesomeApp().run()
