import pickle
from userInfoInterface import *
from clientInterface import *
from echoChamberClient import *
from echoChamberServer import *
  
  
#client interface has to check file extensions also
  
def setupServer() -> None:
    server = echoChamberServer('192.168.1.184', 65000)
    interface = userInfoInterface()
    interface.loadUserInfo()
    while True:
        action = input("\nWould you like to add or edit userinfo (add/edit)\n" \
               "'ls' to see userinfo\n" \
               "'q' to quit\n"
               "->")
        if action == "add":
            interface.addUserInfo()
        elif action == "edit":
            interface.editUserInfo()
        elif action == "ls":
            print(interface.getUserInfo())
        elif action == "q":
            break
        else:
            print("Incorrect command\n")
    interface.saveUserInfo()
    server.loadUserInfo(interface.getUserInfo())
    server.waitForClient()
    server.start()
    #server._mainLoop()
    
  
  
def setupClient() -> None:
    client = echoChamberClient('192.168.1.184', 65000)
    interface = clientInterface()
    client.connectToServer()
    while True:
        interface.promptCommands()
        recentCommand = interface.getRecentCommand()
        client.processCommands(recentCommand)
        if recentCommand == 'q':
            break
        
  
def main() -> None:
    # interface = userInfoInterface()
    # interface.loadUserInfo()
    # while True:
    #     action = input("\nWould you like to add or edit userinfo (add/edit)\n" \
    #            "'ls' to see userinfo\n" \
    #            "'q' to quit\n"
    #            "->")
    #     if action == "add":
    #         interface.addUserInfo()
    #     elif action == "edit":
    #         interface.editUserInfo()
    #     elif action == "ls":
    #         interface.printAllUserInfo()
    #     elif action == "q":
    #         break
    #     else:
    #         print("Incorrect command\n")
    # interface.saveUserInfo()
    isClient = input("Is this machine the client machine? (y/n)\n ->")
    while isClient not in ('y', 'n'):
        print("ERROR: Incorrect response\n")
        isClient = input("Is this machine the client machine? (y/n)\n ->")
    
    if isClient == 'y':
        setupClient()
    if isClient == 'n':
        setupServer()




    

if __name__ == "__main__":
    main()