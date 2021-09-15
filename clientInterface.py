

class clientInterface():
    
    def __init__(self):
        self.serverAddress = ""
        self.userRecentCommand = ""
        self.validCommands = ['send', 'sendSMS', 'SMSLog', 'help', 'ls', 'q']
        
    
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
        while self._commandCorrectlyFormatted(userInput) == False:
            userInput = input("\nPlease enter a command for the client\n" \
                        "Enter 'help' for commands and formatting\n" \
                        "->")
        self.userRecentCommand = userInput
        
        
    def _commandCorrectlyFormatted(self, userInput: str) -> bool:
        splitUserInput = userInput.split(' ')
        command = splitUserInput[0]
        if command not in self.commands:
            self._printCommandNotExistError(command)
            return False

        if command == "send" and len(splitUserInput) not in (2, 3):
            self._printIncorrectlyFormattedError(command)
            return False
#             elif self._fileExists(command[1]) == False:
#                 print("ERROR: The file '{}' does not exist. Type 'ls' to see list of available files in directory.\n".format(command[1]))
#                 return True
            
        elif command == "sendSMS" and len(splitUserInput) != 3:
            self._printIncorrectlyFormattedError(command)
            return False
#             elif self._fileExists(command[-1]) == False:
#                 print("ERROR: The file '{}' does not exist. Type 'ls' to see list of available files in directory.\n".format(command[1]))
#                 return True
            
#             elif self._fileCorrectType(command[-1]) == False:
#                 extension = command[-1].split('.')[-1]
#                 print("ERROR: Cannot send files of type '{}'. Type 'help' to see supported file types.\n".format(extension))
#                 return True

        elif command == "ls" and len(splitUserInput) != 1:
            self._printIncorrectlyFormattedError(command)
            return False
#             if len(command) > 2 or (len(command) == 2 and command[1] != '-s'):
#                 print("ERROR: 'ls' command incorrectly formatted. Type 'help' to see correct format.\n")
#                 return True
                
                
        elif command == "SMSLog" and len(splitUserInput) != 1:
            self._printIncorrectlyFormattedError(command)
            return False
#             if len(command) > 1:
#                 print("ERROR: 'SMSLog' command incorrectly formatted. Type 'help' to see correct format.\n")
#                 return True
            
        elif command == "help" and len(splitUserInput) != 1:
            self._printIncorrectlyFormattedError(command)
            return False
#             print("ERROR: 'help' command incorrectly formatted. Type 'help' to see correct format.\n")
#             return False
        return True
    
    
    def _printCommandNotExistError(self, command: str) -> None:
        print(f"ERROR: Command '{command}' does not exist. Type 'help' to see available commands \n")
    
    
    def _printIncorrectlyFormattedError(self, command: str) -> None:
        print(f"ERROR: '{command}' incorrectly formatted. Type 'help' to see correct format \n")
    
    
    def promptServerAddress(self) -> None:
        self.serverAddress = input("Enter server ip address \n ->")
    
    
    def promptClientCommand(self) -> None:
        None