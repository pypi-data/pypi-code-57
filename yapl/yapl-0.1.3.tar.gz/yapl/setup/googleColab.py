import os
import subprocess
import time

def changeDir(folder_name):
    os.chdir("/content/{}".format(folder_name))

def changePer(folder_name):
    os.system("chmod 777 runcolab.sh")
    os.system("chmod 777 train.sh")

def makerunFile(folder_name):
    runcolabfile = "/content/{}/runcolab.sh".format(folder_name)
    with open(runcolabfile, 'w') as runfile:
        runfile.write("pip install -r requirements.txt\n".format(folder_name))
        runfile.write("sh ./train.sh")

def setupColab(githubLink):
    """
        example:
            setupColab("https://github.com/orionpax00/yapl.git")
            !./runcolab.sh

    """
    os.system("git clone {}".format(githubLink))

    folder_name = githubLink.split("/")[-1].split('.')[0]
    makerunFile(folder_name)
    changeDir(folder_name)
    changePer(folder_name)

def setupTensorboard():
    os.system("wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip")
    os.system("unzip ngrok-stable-linux-amd64.zip")
    print("Starting ngrok")
    os.system("./ngrok http 6006 &")
    print("Starting tensorboard")
    os.system("tensorboard --logdir log --host 0.0.0.0 --port 6006 &")
    
    time.sleep(5)

    
    output = subprocess.check_output("curl -s http://localhost:4040/api/tunnels", shell=True)
    url_ = json.loads(output)['tunnels'][0]['public_url']
    
    print("---------------------\nIF:")
    print("Make sure that a web service is running on localhost:6006 and that it is a valid address.")
    print("TRY TO RUN TENSORBOARD MANUALLY")
    return url_


