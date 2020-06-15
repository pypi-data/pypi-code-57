import subprocess
from halo import Halo
from devyzer.utils.cli import bcolors


# execute the command and print out the result
def run_command(command):
    with Halo(text=f'Executing : {command}', spinner='dots') as sp:
        try:
            output = subprocess.getoutput(command)
            print(output)
            sp.succeed("Done .")
            return True
        except Exception as e:
            sp.fail(str(e), bcolors.FAIL)
        return False

