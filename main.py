import pickle
from userInterface import *
  
  
def main() -> None:
    interface = userInterface()
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
    

if __name__ == "__main__":
    main()