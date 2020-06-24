import os
import platform
from time import sleep
import subprocess
def exist():
    sys = platform.system()
    if sys=="Darwin":
        kexts = "_".join(os.listdir("/Library/Extensions/"))
        return "usbserial.kext" in kexts
    elif sys=="Windows":
        return "ch341ser.inf" in "_".join(os.listdir("C:\Windows\System32\DriverStore\FileRepository"))
    return True

def install():
    if exist():
        return True
    sys = platform.system()
    if sys=="Darwin":
        subprocess.call(["/usr/bin/open",os.path.dirname(__file__)+"/driver/ch34x_install.pkg"])
    elif sys=="Windows":
        os.chdir(os.path.dirname(__file__)+"/driver/")
        subprocess.call([os.path.dirname(__file__)+"/driver/ch34x_install.exe","/sw","/se"])
    while not exist():
        sleep(1)
    return True