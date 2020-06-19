import os
import socket
import platform

OS = platform.system()

def shutdown(password):
    passw = password.strip()
    if OS == "Windows":
        os.system("shutdown /s")

    elif OS == "Darwin" or OS == "Linux":
        os.system(f"echo {passw} | sudo -S shutdown -h now")
	
def reboot(password):
	passw = password.strip()
	if OS == "Windows":
        os.system("shutdown /r")

    elif OS == "Darwin" or OS == "Linux":
        os.system(f"echo {passw} | sudo -S reboot")
        
def sleep(password):
	passw = password.strip()
	if OS == "Windows":
        os.system("shutdown /h")

    elif OS == "Darwin":
        os.system(f"echo {passw} | sudo -S shutdown -s now")

def ipAddress():
	if OS == "Windows":
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip.strip()

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
	
def enableSSH(password):
	passw = password.strip()
	os.system(f'echo {passw} | sudo -S systemsetup -setremotelogin on')
	
def disableSSH(password):
	passw = password.strip()
	os.system(f'echo {passw} | sudo -S systemsetup -setremotelogin off')
	
def getHostname():
	try:
        run = os.popen('whoami')
        output = run.read()
        return output.strip()
    except:
        try:
            run = os.popen('id -un')
            output = run.read()
            return output.strip()
        except:
            try:
                run = os.popen('logname')
                output = run.read()
                return output.strip()
            except:
                return 'No username found'
