import os
import platform
from time import sleep
import subprocess
def exist():
    sys = platform.system()
    if sys=="Darwin":
        kexts = os.listdir("/Library/Extensions/")
        return "usbserial.kext" in kexts
    elif sys=="Windows":
        return False
    return True

def install():
    sys = platform.system()
    if sys=="Darwin":
        subprocess.call(["/usr/bin/open",os.path.dirname(__file__)+"/driver/ch34x_install.pkg"])
    elif sys=="Windows":
        subprocess.call([os.path.dirname(__file__)+"/driver/ch34x_install.exe"])
    while not exist():
        sleep(1)
    return