from kivy.lang import Builder
from kivy_gui import echoChamberWindow  # @UnresolvedImport
from mylib import pickleFileHandler

import os, sys


def main() -> None:
    pickleHandler = pickleFileHandler.PickleFileHandler()
    pickleHandler.loadFile("users.pkl")
    
    userInfo = pickleHandler.getInfo()
    gui = echoChamberWindow.EchoChamberApp(userInfo).run()
    pickleHandler.setNewInfo(userInfo)
    pickleHandler.save()


#anything >=8MB can't be sent
if __name__ == "__main__":
    main()
    

    
    
    #main()
