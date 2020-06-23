#!/usr/bin/env python3
"""p2n reads data from pluto files and writes it to npy files"""

import logging
import sys
import numpy as np

logging_format = 'p2n | %(asctime)s | %(levelname)-8s | %(message)s'
logging.basicConfig(format=logging_format, level=logging.WARNING)


def load_pluto_file(filename: str, shape: tuple, n_vars: int) -> np.ndarray:
    logging.debug(filename)
    data_arr = np.fromfile(filename)
    x1_dim, x2_dim = shape
    data_arr = data_arr.reshape((n_vars, x2_dim, x1_dim))

    return data_arr


def save_npy_files(filename: str, data: np.ndarray, vars: tuple):
    for i, v in enumerate(vars):
        outfilename = filename + '_' + v + '.npy'
        logging.debug(outfilename)
        np.save(outfilename, data[i])


def run(argv: list = None):
    vars = ('rho', 'vx1', 'vx2', 'prs')
    filename = argv[1]
    logging.debug(filename)
    shape = (900, 300)
    data = load_pluto_file(filename, shape, len(vars))
    save_npy_files(filename, data, vars)


if __name__ == '__main__':
    run(sys.argv)
