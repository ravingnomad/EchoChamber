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
from kivy.properties import NumericProperty



#Set app size, and min window size
windowStartSize = (700, 700)
Window.size = windowStartSize
Window.minimum_width, Window.minimum_height = windowStartSize



Builder.load_file('load_preset_screen.kv')

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
        

class PresetScreenLayout(GridLayout):
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
        self._testScroll()

        
        
    def _testPlacement(self):
        topLayout = self.ids.top_screen
        
        presetNameWidget = PresetName()
        loadButtonWidget = LoadButton()
        editButtonWidget = EditButton()
        deleteButtonWidget = DeleteButton()

        presetNameLabel = self._copyButtonWidget(presetNameWidget)
        loadButton = self._copyButtonWidget(loadButtonWidget)
        editButton = self._copyButtonWidget(editButtonWidget)
        deleteButton = self._copyButtonWidget(deleteButtonWidget)
        
        topLayout.add_widget(presetNameLabel)
        topLayout.add_widget(loadButton)
        topLayout.add_widget(editButton)
        topLayout.add_widget(deleteButton)
        
        
    def _testScroll(self):
        for i in range(10):
            test = BoxLayout(size = self.top_screen.size)
            presetNameWidget = PresetName()
            loadButtonWidget = LoadButton()
            editButtonWidget = EditButton()
            deleteButtonWidget = DeleteButton()
    
            presetNameLabel = self._copyButtonWidget(presetNameWidget)
            loadButton = self._copyButtonWidget(loadButtonWidget)
            editButton = self._copyButtonWidget(editButtonWidget)
            deleteButton = self._copyButtonWidget(deleteButtonWidget)
            
            presetNameLabel.text = f"{presetNameLabel.text} #{i}"
            
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
            newButton.bind(on_press = self.callbackBindings[newButton.text])
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
        print("You clicked the 'Edit' Button!")
        presetName = None 
        for child in event.parent.children:
            if child.text not in ["Load", "Edit", "Delete"]:
                presetName = child.text
        print(f"The preset name is called: {presetName}\n")
    
    
    def deletePresetButton(self, event) -> None:
        print("You clicked the 'Delete' Button!")
        presetName = None 
        for child in event.parent.children:
            if child.text not in ["Load", "Edit", "Delete"]:
                presetName = child.text
        print(f"The preset name is called: {presetName}\n")
        
        
    def addNewPresetButton(self) -> None:
        print("You clicked the 'Add New Preset' Button!")
        
    
    def exitButton(self) -> None:
        print("You clicked the 'Exit' Button!")






class AwesomeApp(App):
    def build(self):
        return PresetScreenLayout()
    

    
    
if __name__ == "__main__":
    AwesomeApp().run()
