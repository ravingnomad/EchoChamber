import pickle

class userInterface():
    
    def __init__(self):
        self.userInfo = {}
        self.pickleFile = {}
        self.isClient = False
        self.serverAddress = ""
        self.userRecentCommand = ""
        self.supportedCarrierSMS = {"at&t": "@txt.att.net",
                                    "tmobile": "@tmomail.net"
                                    }
        
    def loadUserInfo(self) -> None:
        try:
            with open("users.pickle", "rb") as pickleFile:
                self.userInfo = pickle.load(pickleFile)
                print("Loaded user pickle file\n")
        except FileNotFoundError:
            print("No user file found. Using default empty dict\n")
        
        
    def saveUserInfo(self) -> None:
        with open("users.pickle", "wb") as pickleFile:
            pickle.dump(self.userInfo, pickleFile)
        print("\nSaved userinfo in pickle file\n")
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
        userResponse = input("Is this machine a client? (y/n) \n ->")
        while userResponse not in ('y', 'n'):
            self._incorrectResponse()
            userResponse = input("Is this machine a client? (y/n) \n ->")
        self.isClient = userResponse == "y"
    
    
    def promptServerAddress(self) -> None:
        self.serverAddress = input("Enter server ip address \n ->")
    
    
    def promptClientCommand(self) -> None:
        None
            
        
    def addUserInfo(self) -> None:
        username = self._promptUsername()
        phoneNumber = self._promptPhoneNumber()
        phoneCarrier = self._promptPhoneCarrier()
        self.userInfo[username] = {}
        self.userInfo[username]['SMS'] = self._formatSMS(phoneNumber, phoneCarrier)
        
        
    def _promptUsername(self) -> str:
        name = input("\nEnter new username\n"\
                         "->")
        while name in self.userInfo.keys():
            overwriteOriginal = input("WARNING: username '" + name + "' already exists. " \
                                      "Continuing will overwrite original entry for username '" + name + "'. " \
                                      "Continue? (y / n)\n" \
                                      "->")
            if overwriteOriginal == 'y':
                break;
            elif overwriteOriginal == 'n':
                name = input("\nEnter new username\n" \
                             "->")
            else:
                self._incorrectResponse()
        return name
    
    
    def _promptPhoneNumber(self) -> str:
        phoneNumber = input("\nEnter phone number (no dashes or spaces)\n" \
                            "->")
        while len(phoneNumber) != 10 or sum(1 for x in phoneNumber if str.isdigit(x)) != 10:
            self._incorrectResponse()
            phoneNumber = input("\nEnter phone number (no dashes or spaces)\n" \
                                "->")
        return phoneNumber
        
        
    def _promptPhoneCarrier(self) -> str:
        phoneCarrier = input("\nChoose from supported phone carriers: \n" \
                             + self._supportedCarriersPrintString() + \
                             "->")
        while phoneCarrier not in self.supportedCarrierSMS.keys():
            self._incorrectResponse()
            phoneCarrier = input("\nChoose from supported phone carriers: \n"\
                     + self._supportedCarriersPrintString() + \
                     "->")
        return phoneCarrier
        
        
    def _formatSMS(self, phoneNumber: str, carrier: str) -> str:
        return phoneNumber + self.supportedCarrierSMS[carrier]
    
        
    def _supportedCarriersPrintString(self) -> str:
        returnStr = ""
        for carrier in self.supportedCarrierSMS.keys():
            returnStr += str(carrier) + "\n"
        return returnStr
        
        
    def editUserInfo(self) -> None:
        answer = input("\nEnter username to edit\n" \
                       "Enter 'ls' to see all users\n" \
                       "Enter 'q' to quit\n" \
                       "->")
        while answer != 'q' and answer not in self.userInfo.keys():
            if answer == 'ls':
                print(self.getUserInfo())
            else:
                print("ERROR: User does not exist\n")
            answer = input("\nEnter username to edit\n" \
                           "Enter 'ls' to see all users\n" \
                           "Enter 'q' to quit \n" \
                           "->")
        if answer == 'q':
            return
        else:
            self._editUserInfoHelper(answer)
        
        
        
    def _editUserInfoHelper(self, username: str) -> None:
        action = input("\nChange one of the fields below by entering '[field name] : [new info]'\n" \
                       + self._userInfoPrintString(username) + \
                       "'q' to quit\n"
                       "->")
        while action != 'q':
            if len(action.split(" : ")) == 2:
                key, value = action.split(" : ")
                if key in self.userInfo[username].keys():
                    self.userInfo[username][key] = value
            else:
                self._incorrectResponse()
            action = input("\nChange one of the fields below by entering '[field name] : [new info]\n" \
               + self._userInfoPrintString(username) + \
               "'q' to quit\n"
               "->")
        
        
    def _userInfoPrintString(self, username: str) -> str:
        returnStr = ""
        for fieldName in self.userInfo[username].keys():
            returnStr += str(fieldName) + " : " + self.userInfo[username][fieldName] + "\n"
        return returnStr
    
    
    def _incorrectResponse(self) -> None:
        print("ERROR: Incorrect response\n")
        
    
    