import subprocess
import os
import sys
from comtypes import client


def getlw(syspath="c:\\windows"):
    try:
        lw = client.CreateObject("lw.lwsoft3")
    except:
        print('here')
        if os.path.exists(os.path.join(syspath, 'SysWOW64')):
            cmd = os.path.join(syspath, 'SysWOW64', 'regsvr32.exe') + \
                " /s " + os.path.join(os.path.abspath('.'), 'lw.dll')
        else:
            cmd = "regsvr32 /s " + os.path.join(os.path.abspath('.'), 'lw.dll')
        ret = subprocess.run(cmd, capture_output=True)
        try:
            lw = client.CreateObject("lw.lwsoft3")
        except Exception:
            raise Exception(
                "lw com reg failed!Try change config.py set your system path!")
    return lw
