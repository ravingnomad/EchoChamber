import pickle
from userInfoInterface import *
from clientInterface import *
from echoChamberClient import *
from echoChamberServer import *
  
  
def setupServer() -> None:
    server = echoChamberServer()
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
    server._mainLoop()
    
  
  
def setupClient() -> None:
    client = echoChamberClient()
    client.mainLoop()
    
  
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
    main()