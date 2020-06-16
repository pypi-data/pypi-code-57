from __future__ import annotations  # forward reference of classmethod returning cls
from typing import Optional
import numpy as np
from itertools import filterfalse

class QAPInstance:
    """
    Instance of the Quadratic Assignment Problem.
    """
    def __init__(self, nsize: int, name: str=None, /):
        self.nsize = nsize
        self.name = name
        self.weights = np.zeros(shape=(nsize, nsize))
        self.distances = np.zeros(shape=(nsize, nsize))


    @classmethod
    def read_qaplib(cls, path: str, /) -> Optional[QAPInstance]:
        with open(path) as fh:
            lines = fh.read(1024*1024*1024).splitlines()

        try:
            nsize = int(lines[0])
        except (ValueError, IndexError):
            print(f'Can not parse size field of file {path}') # TODO logger
            return None
        qap_instance = QAPInstance(nsize)

        file_iter = filterfalse(_empty_or_whitespace, lines[1:])
        for row, line in enumerate(file_iter):
            for col, elem in enumerate(line.split()):
                qap_instance.weights[row, col] = elem
            if row == nsize-1:
                break
        for row, line in enumerate(file_iter):
            for col, elem in enumerate(line.split()):
                qap_instance.distances[row, col] = elem
            if row == nsize-1:
                break

def _empty_or_whitespace(line: str) -> bool:
    return len(line) == 0 or line.isspace()

if __name__ == '__main__':
    QAPInstance.read_qaplib('./data/qap/chr12a.dat')
    #QAPInstance.read_qaplib('./data/qap/empty.dat')
