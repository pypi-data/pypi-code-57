#!python


import shutil
import os
import mfa_problem
from pathlib import Path

if __name__ == '__main__':
    doc_file = os.path.join(os.path.dirname(mfa_problem.__file__), 'data')
    home = str(Path.home())
    new_dir = os.path.join(home, 'mfa_problem_notebook')
    if os.path.exists(new_dir):
        os.rmdir(new_dir)
    shutil.copytree(doc_file, new_dir)
