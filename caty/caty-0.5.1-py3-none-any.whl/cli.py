from pathlib import Path
from sys import argv

from caty.main import main


def cli():
    ''' Dump the file given as arg.
    '''
    path = Path(argv[1])
    ext = argv[2] if len(argv)==3 else path.suffix[1:]
    main(path, ext)

