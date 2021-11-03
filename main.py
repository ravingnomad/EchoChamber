from userInfoInterface import *
from clientInterface import *
from echoChamberClient import *
from echoChamberServer import *
  
  
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
    main()
