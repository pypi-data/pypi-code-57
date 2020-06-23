import os
import platform
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
        #["installer","-pkg",os.path.dirname(__file__)+"/driver/ch34x_install.pkg","-target","/"])
    elif sys=="Windows":
        subprocess.call([os.path.dirname(__file__)+"/driver/ch34x_install.exe"])
    return