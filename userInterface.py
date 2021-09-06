import pickle

class userInterface():
    
    def __init__(self):
        self.userInfo = {}
        self.pickleFile = {}
        self.isClient = False
        self.serverAddress = ""
        self.userRecentCommand = ""
        
    def getUserInfo(self) -> dict:
        return self.userInfo
        
    def getIsClient(self) -> bool:
        return self.isClient
        
    def getServerAddress(self) -> str:
        return self.serverAddress
        
    def getRecentCommand(self) -> str:
        temp = self.userRecentCommand
        self.userRecentCommand = "" #reset so subsequent calls don't use old commands
        return temp
    
    def promptIsClient(self) -> None:
        None
    
    def promptServerAddress(self) -> None:
        None
    
    def promptUserInfo(self) -> None:
        None
        
    def promptClientCommand(self) -> None:
        None
        
    def _loadPickleFile(self) -> None:
        None
        
    
    