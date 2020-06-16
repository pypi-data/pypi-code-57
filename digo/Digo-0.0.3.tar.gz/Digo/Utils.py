import subprocess
import os

def getRequirements():
    proc = subprocess.Popen(
        ['pip', 'freeze'],
        stdout=subprocess.PIPE
    )

    out, err = proc.communicate()
    requirements = out.decode('utf-8')
    return requirements
