#!C:\Users\mbhas\pylabnet\venv\dev\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'PyQt5','console_scripts','pyuic5'
__requires__ = 'PyQt5'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('PyQt5', 'console_scripts', 'pyuic5')()
    )
