import pickle


class PickleFileHandler():
    
    def __init__(self):
        self._toBeSavedInfo = {}
        self._numberOfEntriesSoFar = 0
        
        
    def get(self, keyName: str) -> object:
        try:
            return self._toBeSavedInfo[keyName]
        except KeyError:
            print(f"ERROR: key '{keyName}' does not exist")
            return
        
        
    def add(self, entry, entryKey = None) -> None:
        key = f'Entry {self._numberOfEntriesSoFar + 1}'
        if entryKey != None:
            key = entryKey
        self._numberOfEntriesSoFar += 1
        self._toBeSavedInfo[key] = entry
        
        
    def delPickle(self, key) -> None:
        try: 
            del self._toBeSavedInfo[key]    
        except KeyError:
            print(f"ERROR: key '{key}' does not exist")
                
 
    def clearPickle(self) -> None:
        '''Completely clear all info from handler that would have been saved into a pickle file'''
        self._toBeSavedInfo.clear()
        
        
    def savePickle(self, pickleFileName: str) -> None:
        with open(f'{pickleFileName}.pkl', 'wb') as pickleFile:
            pickle.dump(self._toBeSavedInfo, pickleFile)
        
        
    def loadPickle(self, pickleFileName: str, overwrite = True) -> None:
        '''Load a pickle file's data into the current handler and saves data into toBeSavedInfo; will overwrite or add to existing data depending
        on optional flag'''
        try:
            with open(f'{pickleFileName}.pkl', 'rb') as pickleFile:
                pickleFileData = pickle.load(pickleFile)
                if overwrite:
                    self._toBeSavedInfo = pickleFileData
                else:
                    self._toBeSavedInfo.update(pickleFileData)
        except FileNotFoundError:
            print(f"ERROR: file '{pickleFileName}' does not exist") 
        
        
    def viewPickle(self) -> None:
        print("KEY               VALUE")
        for key, value in self._toBeSavedInfo.items():
            print(f"{key}     :     {value}")
         
        
        
        
    