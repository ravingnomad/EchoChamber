import pickle


class PickleFileHandler():
    
    def __init__(self):
        self._toBeSavedInfo = {}
        self._pickleFileName = None
        
        
    def getInfo(self):
        return self._toBeSavedInfo
        
    
    def setNewInfo(self, newInfo: dict):
        '''Completely replaces old info with an entirely new one.'''
        self._toBeSavedInfo = newInfo
        
        
    def add(self, key, entry) -> None:
        self._toBeSavedInfo[key] = entry
        
        
    def delete(self, key) -> None:
        try: 
            del self._toBeSavedInfo[key]    
        except KeyError:
            print(f"ERROR: key '{key}' does not exist")
                
 
    def clear(self) -> None:
        '''Completely clear all info from handler that would have been saved into a pickle file'''
        self._toBeSavedInfo.clear()
        
        
    def save(self) -> None:
        with open(self._pickleFileName, 'wb') as pickleFile:
            pickle.dump(self._toBeSavedInfo, pickleFile)
        
        
    def loadFile(self, pickleFileName: str, overwrite = True) -> None:
        '''Load a pickle file's data into the current handler and saves data into toBeSavedInfo; will overwrite or add to existing data depending
        on optional flag'''
        try:
            with open(pickleFileName, 'rb') as pickleFile:
                pickleFileData = pickle.load(pickleFile)
                if overwrite:
                    self._toBeSavedInfo = pickleFileData
                else:
                    self._toBeSavedInfo.update(pickleFileData)
        except FileNotFoundError:
            print(f"ERROR: file '{pickleFileName}' does not exist. Creating a new empty file.")
            with open(pickleFileName, 'wb') as newPickleFile:
                pass
        finally:
           self._pickleFileName = pickleFileName 
        
        
    def view(self) -> None:
        print("KEY               VALUE")
        for key, value in self._toBeSavedInfo.items():
            print(f"{key}     :     {value}")
         
        
        
        
    