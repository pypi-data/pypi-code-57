# Additional modules
import os
import socket
import platform

OS = platform.system()

# Shutdown computer
def shutdown():
    if OS == "Windows":
        os.system("shutdown /s")

    elif OS == "Darwin" or OS == "Linux":
        os.system("sudo shutdown -h now")

# Reboot computer
def reboot():
    if OS == "Windows":
        os.system("shutdown /r")

    elif OS == "Darwin" or OS == "Linux":
        os.system("sudo shutdown -r now")

# Put computer to sleep
def sleep():
    if OS == "Windows":
        os.system("shutdown /h")

    elif OS == "Darwin" or OS == "Linux":
        os.system("sudo shutdown -s now")

#Logout of computer
def logout():
    if OS == "Windows":
        os.system("shutdown /l")

    elif OS == "Darwin" or OS == "Linux":
        os.system("sudo -s")

# Get IP Address of computer
def ip_address():
    if OS == "Windows":
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip

    elif OS == "Linux":
        run = os.popen("hostname -I")
        output = run.read()
        ip = ""
        for i in output:
            if i != " ":
                ip += i
            elif i == " ":
                break
        return ip.strip()

    elif OS == "Darwin":
        run = os.popen("ipconfig getifaddr en1")
        output = run.read()
        return output.strip()