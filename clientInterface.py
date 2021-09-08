

class clientInterface():
    
    def __init__(self):
        self.serverAddress = ""
        self.userRecentCommand = ""
        
    
    def getServerAddress(self) -> str:
        return self.serverAddress
        
        
    def getRecentCommand(self) -> str:
        temp = self.userRecentCommand
        self.userRecentCommand = "" #reset so subsequent calls don't use old commands
        return temp
    
    
    def promptServerAddress(self) -> None:
        self.serverAddress = input("Enter server ip address \n ->")
    
    
    def promptClientCommand(self) -> None:
        None