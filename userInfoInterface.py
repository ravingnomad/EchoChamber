import pickle

class userInfoInterface():
    
    def __init__(self):
        self.userInfo = {}
        self.pickleFile = {}
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
    
    
    def printAllUserInfo(self) -> None:
        for name in self.userInfo.keys():
            print(name)
            print(self._userInfoPrintString(name))
    
    
    def addUserInfo(self) -> None:
        username = self._promptUsername()
        phoneNumber = self._promptPhoneNumber()
        phoneCarrier = self._promptPhoneCarrier()
        emailAddr = self._promptEmailAddr()
        emailPwd = self._promptEmailPwd()
        self.userInfo[username] = {}
        self.userInfo[username]['SMS'] = self._formatSMS(phoneNumber, phoneCarrier)
        self.userInfo[username]['Email Address'] = emailAddr
        self.userInfo[username]['Email Password'] = emailPwd
        
        
    def _promptUsername(self) -> str:
        name = self._promptUserForAnswer('promptUsername')
        while name in self.userInfo.keys():
            overwriteOriginal = input("WARNING: username '" + name + "' already exists. " \
                                      "Continuing will overwrite original entry for username '" + name + "'. " \
                                      "Continue? (y / n)\n" \
                                      "->")
            if overwriteOriginal == 'y':
                break;
            elif overwriteOriginal == 'n':
                name = self._promptUserForAnswer('promptUsername')
            else:
                print("ERROR: Incorrect response\n")
        return name
    
    
    def _promptPhoneNumber(self) -> str:
        phoneNumber = self._promptUserForAnswer('promptPhoneNumber')
        while len(phoneNumber) != 10 or sum(1 for x in phoneNumber if str.isdigit(x)) != 10:
            print("ERROR: Incorrect response\n")
            phoneNumber = self._promptUserForAnswer('promptPhoneNumber')
        return phoneNumber
        
        
    def _promptPhoneCarrier(self) -> str:
        phoneCarrier = self._promptUserForAnswer('promptPhoneCarrier')
        while phoneCarrier not in self.supportedCarrierSMS.keys():
            print("ERROR: Incorrect response\n")
            phoneCarrier = self._promptUserForAnswer('promptPhoneCarrier')
        return phoneCarrier
    
    
    def _promptEmailAddr(self) -> str:
        emailAddress = input("\nEnter email address to use\n"\
                         "->")
        return emailAddress
        
        
    def _promptEmailPwd(self) -> str:
        emailPassword = input("\nEnter password for above email address\n"\
                         "->")
        return emailPassword
        
        
    def _formatSMS(self, phoneNumber: str, carrier: str) -> str:
        return phoneNumber + self.supportedCarrierSMS[carrier]
    
        
    def _supportedCarriersPrintString(self) -> str:
        returnStr = ""
        for carrier in self.supportedCarrierSMS.keys():
            returnStr += str(carrier) + "\n"
        return returnStr
        
        
    def editUserInfo(self) -> None:
        answer = self._promptUserForAnswer('editUserInfo')
        while answer != 'q' and answer not in self.userInfo.keys():
            if answer == 'ls':
                self.printAllUserInfo()
            else:
                print("ERROR: User does not exist\n")
            answer = self._promptUserForAnswer('editUserInfo')
        if answer == 'q':
            return
        else:
            self._editUserInfoChangeField(answer)
            
    
    def _promptUserForAnswer(self, functionName, *args) -> str:
        functionNamesDict = {
            'promptUsername': "\nEnter new username\n"\
                              "->",
            
            'promptPhoneNumber': "\nEnter phone number (no dashes or spaces)\n" \
                                 "->",
            
            'promptPhoneCarrier': "\nChoose from supported phone carriers: \n" \
                                  + self._supportedCarriersPrintString() + \
                                  "->",
                                  
            'editUserInfo': "\nEnter username to edit\n" \
                            "Enter 'ls' to see all users\n" \
                            "Enter 'q' to quit\n" \
                            "->"
            }
        #assigns this print statement to functionNamesDict['userInfoChangeField' at runtime because self._userInfoPrintString()
        #does not know what 'args' is at compile time
        if functionName == 'userInfoChangeField':
            functionNamesDict[functionName] = "\nChange one of the fields below by entering '[field name] : [new info]'\n" \
                                              + self._userInfoPrintString(args[0]) + \
                                              "'q' to quit\n"\
                                              "->"
        printStatement = functionNamesDict[functionName]
        userAnswer = input(printStatement)
        return userAnswer
        
        
    def _editUserInfoChangeField(self, username: str) -> None:
        action = self._promptUserForAnswer('userInfoChangeField', username)
        while action != 'q':
            if len(action.split(" : ")) == 2:
                key, value = action.split(" : ")
                if key in self.userInfo[username].keys():
                    self.userInfo[username][key] = value
            else:
                print("ERROR: Incorrect response\n")
            action = self._promptUserForAnswer('userInfoChangeField', username)
        
        
    def _userInfoPrintString(self, username: str) -> str:
        returnStr = ""
        for fieldName in self.userInfo[username].keys():
            returnStr += str(fieldName) + " : " + self.userInfo[username][fieldName] + "\n"
        return returnStr
    
        