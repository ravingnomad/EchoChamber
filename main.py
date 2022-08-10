from userInfoInterface import *
from clientInterface import *
from echoChamberClient import *
from echoChamberServer import *
  
from kivy.lang import Builder
from kivy_gui import echoChamberWindow

import os

def setupServer() -> None:
    server = echoChamberServer(serverIPAddress, 65000)
    infoInterface = userInfoInterface()
    infoInterface.loadUserInfo()
    while True:
        action = input("\nWould you like to add or edit userinfo (add/edit)\n" \
               "'ls' to see userinfo\n" \
               "'q' to quit and start server\n"
               "->")
        if action == "add":
            infoInterface.addUserInfo()
        elif action == "edit":
            infoInterface.editUserInfo()
        elif action == "ls":
            print(infoInterface.getUserInfo())
        elif action == "q":
            break
        else:
            print("Incorrect command\n")
    infoInterface.saveUserInfo()
    server.loadUserInfo(infoInterface.getUserInfo())
    server.waitForClient()
    server.start()
    
  
def setupClient() -> None:
    client = echoChamberClient(serverIPAddress, 65000)
    interface = clientInterface()
    client.connectToServer()
    while True:
        interface.promptCommands()
        recentCommand = interface.getRecentCommand()
        client.processCommands(recentCommand)
        if client.getServerAskedToCompress() == True:
            userAnswer = interface.promptCompressQuery()
            client.sendCompressQueryAnswer(userAnswer)
            client.continueSendingSMS()
        if recentCommand == 'q':
            break
        
  
def main() -> None:
    isClient = input("Is this machine the client machine? (y/n)\n ->")
    while isClient not in ('y', 'n'):
        print("ERROR: Incorrect response\n")
        isClient = input("Is this machine the client machine? (y/n)\n ->")
    if isClient == 'y':
        setupClient()
    if isClient == 'n':
        setupServer()


if __name__ == "__main__":
    serverIPAddress = ''

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
    gui = echoChamberWindow.EchoChamberApp(test).run()
    #main()
