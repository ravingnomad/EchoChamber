from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup



#Builder.load_file("delete_preset_screen.kv")

class DeletePresetScreen(Popup):
    text_prompt = ObjectProperty(None)
    currentPresetName = None
    currentPresetScreen = None
    
    def on_open(self):
        self.text_prompt.text = f"Are you sure you want to delete the preset '{self.currentPresetName}'?\nAll info in this preset will be lost."
    
    def deleteButtonPressed(self):
        self.currentPresetScreen._deletePreset(self.currentPresetName)
        self.dismiss()
        
        
        
        
#class MyApp(App):
#    def build(self):
#       return DeletePresetScreen()
    
    
    
#if __name__ == "__main__":
#    MyApp().run()