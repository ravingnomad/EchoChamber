from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.clock import Clock 
from kivy.lang import Builder

import echoChamberWindow
import deletePresetScreen


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
        self.buttonCallbackBindings = {"Load": self.loadPresetButton,
                    "Edit": self.editPresetButton,
                    "Delete": self.deletePresetButton,
                    "+Add New Preset": self.addNewPresetButton,
                    "Exit": self.exitButton
                    }
        self.presetData = {}
        
        
    def on_enter(self):
        self.refreshScreen()
        
        
    def refreshScreen(self):
        Clock.schedule_once(self._clearTopScreen, .1)
        Clock.schedule_once(self._loadPresetData, .1)
        
        
    def _clearTopScreen(self, *args):
        tempList = self.top_screen.children.copy()
        for child in tempList:
            self.top_screen.remove_widget(child)
            
            
    def _loadPresetData(self, *args):
        for preset in self.presetData.keys():
            row = BoxLayout(size = self.top_screen.size)
            presetNameWidget = PresetName()
            loadButtonWidget = LoadButton()
            editButtonWidget = EditButton()
            deleteButtonWidget = DeleteButton()
    
            presetNameLabel = self._copyButtonWidget(presetNameWidget)
            loadButton = self._copyButtonWidget(loadButtonWidget)
            editButton = self._copyButtonWidget(editButtonWidget)
            deleteButton = self._copyButtonWidget(deleteButtonWidget)
            
            presetNameLabel.text = f"{preset}"
            
            row.add_widget(presetNameLabel)
            row.add_widget(loadButton)
            row.add_widget(editButton)
            row.add_widget(deleteButton)
            
            row.size_hint_x = 1
            self.top_screen.add_widget(widget = row)
            

        
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
        if newButton.text in self.buttonCallbackBindings.keys():
            newButton.bind(on_release = self.buttonCallbackBindings[newButton.text])
        return newButton
    
    
    def loadPresetButton(self, event) -> None:
        presetName = self._getPresetName(event.parent)
        self.parent.mainScreen.preset_name = presetName
        self.parent.mainScreen.presetInfo = self.presetData[presetName]
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = "echoChamberMainScreen"
        
        
    def editPresetButton(self, event) -> None:
        presetName = self._getPresetName(event.parent)
        self.parent.editScreen.loadedPresetName = presetName
        self.parent.editScreen.loadedPresetInfo = self.presetData[presetName]
        self.parent.editScreen.screenEnteredFrom = "loadPresetScreen"
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'editPresetScreen'
    
    
    def deletePresetButton(self, event) -> None:
        presetName = self._getPresetName(event.parent) 
        popupObject = deletePresetScreen.DeletePresetScreen()
        popupObject.currentPresetName = presetName
        popupObject.currentPresetScreen = self
        popupObject.open()
        
        
    def _deletePreset(self, presetName):
        del self.presetData[presetName]
        self.refreshScreen()
        
        
    def addNewPresetButton(self) -> None:
        self.parent.editScreen.screenEnteredFrom = "loadPresetScreen"
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'editPresetScreen'
        
    
    def exitButton(self) -> None:
        Window.close()
        
        
    def _getPresetName(self, widget):
        for grandchild in widget.children:
            if grandchild.text not in ["Load", "Edit", "Delete"]:
                return grandchild.text
    



