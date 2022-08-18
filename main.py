from kivy.lang import Builder
from kivy_gui import echoChamberWindow
from mylib import pickleFileHandler

import os


test = {"preset1": {'sms': 'Sprint', 'phone': '1111111111', 'email': 'example1@gmail.com', 'password': 'alonzo'},
                         "preset2": {'sms': 'Verizon', 'phone': '2222222222', 'email': 'example2@gmail.com', 'password': 'buttercup'},
                         "preset3": {'sms': 'Sprint', 'phone': '3333333333', 'email': 'example3@gmail.com', 'password': 'jazmina11'},
                         "preset4": {'sms': 'T-Mobile', 'phone': '4444444444', 'email': 'example4@gmail.com', 'password': 'Kinetic'},
                         "preset5": {'sms': 'AT&T', 'phone': '5555555555', 'email': 'example5@gmail.com', 'password': '@dam5App113'},
                         "preset6": {'sms': 'AT&T', 'phone': '6666666666', 'email': 'example6@gmail.com', 'password': 'Futurio'},
                         "preset7": {'sms': 'Verizon', 'phone': '7777777777', 'email': 'example7@gmail.com', 'password': 'Kam3R@'},
                         "preset8": {'sms': 'Sprint', 'phone': '8888888888', 'email': 'example8@gmail.com', 'password': '1adf78@'},
                         "preset9": {'sms': 'T-Mobile', 'phone': '9999999999', 'email': 'example9@gmail.com', 'password': '80085boobs'},
                         "preset10": {'sms': 'T-Mobile', 'phone': '0000000000', 'email': 'example10@gmail.com', 'password': 'C@pi+an'}
                         }

def main() -> None:
    pickleHandler = pickleFileHandler.PickleFileHandler()
    pickleHandler.loadPickle("users")
    
    pickleHandler.viewPickle()
    info = pickleHandler._toBeSavedInfo
    gui = echoChamberWindow.EchoChamberApp(info).run()
    pickleHandler._toBeSavedInfo = info
    pickleHandler.savePickle("users")

#anything >=8MB can't be sent

if __name__ == "__main__":
    main()


    
    
    #main()
