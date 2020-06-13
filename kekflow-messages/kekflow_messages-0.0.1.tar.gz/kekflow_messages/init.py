import sys
import pathlib

from os import listdir
from os.path import isfile, join

curr_path = pathlib.Path(__file__).parent.absolute()
[sys.path.append(f) for f in listdir(curr_path) if isfile(join(curr_path, f))]
