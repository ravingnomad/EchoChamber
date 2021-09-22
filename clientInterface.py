from pickle import NONE


class clientInterface():
    
    def __init__(self):
        self.serverAddress = ""
        self.userRecentCommand = ""
        self.validCommands = ['send', 'sendSMS', 'SMSLog', 'help', 'ls', 'q']
        self.smsSupportedFileTypes = ["jpg", "img", "png", "gif", "txt", "webm", "mp4"]

        
    def promptServerAddress(self) -> None:
        self.serverAddress = input("Enter server ip address \n ->")
        
        
    def getServerAddress(self) -> str:
        return self.serverAddress
        
        
    def getRecentCommand(self) -> str:
        #mainly used for echoClient
        temp = self.userRecentCommand
        self.userRecentCommand = "" #reset so subsequent calls don't use old commands
        return temp
    
    
    def promptCommands(self) -> None:
        userInput = input("\nPlease enter a command for the client\n" \
                        "Enter 'help' for commands and formatting\n" \
                        "->")
        while self._commandCorrectlyFormatted(userInput) == False or self._isSupportedSMSFileType(userInput) == False:
            userInput = input("\nPlease enter a command for the client\n" \
                        "Enter 'help' for commands and formatting\n" \
                        "->")
        self.userRecentCommand = userInput
        
        
    def _commandCorrectlyFormatted(self, userInput: str) -> bool:
        command, *args = userInput.split(' ')
        noFormatError = True
        if command == "send":
            noFormatError = len(args) in (1, 2)
        elif command == "sendSMS":
            noFormatError = len(args) == 2
        elif command in ("ls", "SMSLog", "help", "q"):
            noFormatError = len(args) == 0
        else:
            self._printCommandNotExistError(command)
            return False
        if noFormatError == False:
            self._printIncorrectlyFormattedError(command)
        return noFormatError
    
    
    def _isSupportedSMSFileType(self, userInput: str) -> bool:
        splitCommand = userInput.split(' ')
        if splitCommand[0] != 'sendSMS': #only sendSMS command needs to check for file type
            return True
        fileName = splitCommand[1]
        extension = fileName.split('.')[-1].lower()
        if extension not in self.smsSupportedFileTypes:
            self._printIncorrectFileTypeError(fileName, extension)
            return False
        return True
        
    
    def _printCommandNotExistError(self, command: str) -> None:
        print(f"ERROR: Command '{command}' does not exist. Type 'help' to see available commands \n")
    
    
    def _printIncorrectlyFormattedError(self, command: str) -> None:
        print(f"ERROR: '{command}' incorrectly formatted. Type 'help' to see correct format \n")
        
        
    def _printIncorrectFileTypeError(self, fileName: str, fileExtension: str) -> None:
        print(f"ERROR: File '{fileName}' with extension '{fileExtension}' is not a supported file type for use with SMS \n")