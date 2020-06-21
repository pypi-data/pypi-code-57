#!/usr/bin/env python3
"""line integral convolution algorithms
"""

import logging
from typing import Tuple, Sequence, Union
import numpy as np  # type: ignore

logging.basicConfig(format='%(asctime)s | %(levelname)-8s | %(message)s', level=logging.DEBUG)
plt_logger = logging.getLogger('matplotlib')
plt_logger.setLevel(level=logging.WARNING)

logging.debug(f'numpy version {np.__version__}')

_eps = 1e-6


def _load_npy_data(file_x: str, file_y: str) -> Tuple[np.array, np.array]:
    try:
        data_x = np.load(file_x)
        data_y = np.load(file_y)
    except FileNotFoundError as e:
        logging.error('Could not read one of the input files')
        raise e

    return data_x, data_y


def _load_pluto_single_file_data(file_data: str, var='B', dim='12') -> Tuple[np.array, np.array]:  # pragma: no cover
    logging.warning('Only 2d PLUTO dbl single files are supported at the moment.')
    try:
        data = np.fromfile(file_data)
    except FileNotFoundError as e:
        logging.error('Could not read one of the input files')
        raise e

    print(data.shape)
    data = data.reshape((7, 400, 160))
    print(data.shape)
    for i in range(7):
        print(data[i, 0:10, 0:10])
    if var == 'B':
        data_x = data[2 + int(dim[1]), :, :]
        data_y = data[2 + int(dim[0]), :, :]
    elif var == 'v':
        data_x = data[int(dim[0]), :, :]
        data_y = data[int(dim[1]), :, :]
    else:
        raise NotImplementedError('in _load_pluto_single_file_data: var has to be one of "v" or "B"')
    return data_x, data_y


def _check_data(data_x: np.array, data_y: np.array) -> bool:
    if len(data_x.shape) != 2:
        logging.error(f'data has to be 2d. data_x is {len(data_x.shape)}d.')
    if len(data_y.shape) != 2:
        logging.error(f'data has to be 2d. data_y is {len(data_y.shape)}d.')
    if len(data_x.shape) != 2 or len(data_y.shape) != 2:
        return False

    if (data_x.shape[0] != data_y.shape[0] or data_x.shape[1] != data_y.shape[1]):
        logging.error(f'data shapes do not match: x {data_x.shape}, y {data_y.shape}.')
        return False

    return True


def lic(data_x: np.array,
        data_y: np.array,
        length: int = 10,
        kernel: Sequence = None) -> np.array:
    """Generate a line integral convolution representation of the input data."""

    assert length > 0
    assert len(data_x.shape) == 2
    assert len(data_y.shape) == 2
    assert data_x.shape[0] == data_y.shape[0] and data_x.shape[1] == data_y.shape[1]

    if kernel is None:
        kernel = np.ones(length)
    else:
        logging.info(f'lic: overwriting parameter length with {len(kernel)}')
        length = len(kernel)
        kernel = np.array(kernel) / np.mean(kernel)

    # TODO: make it possible to pass seed images or generate parameterized seeds
    seed = np.random.random(data_x.shape)
    seed[0, :] = seed[:, 0] = seed[-1, :] = seed[:, -1] = 0.5
    result = np.empty_like(seed)
    it = np.nditer(result, flags=['multi_index'], op_flags=['writeonly'])
    for res in it:
        x, y = it.multi_index
        fx = fy = 0.5
        line = []
        for k in range(length):
            tx = ty = np.inf
            if data_x[x, y] > _eps:
                tx = (1 - fx) / data_x[x, y]
            elif data_x[x, y] < -_eps:
                tx = -fx / data_x[x, y]
            if data_y[x, y] > _eps:
                ty = (1 - fy) / data_y[x, y]
            elif data_y[x, y] < -_eps:
                ty = -fy / data_y[x, y]
            if tx < ty:
                if data_x[x, y] > 0:
                    x += 1
                    fx = 0.
                else:
                    x -= 1
                    fx = 1.
                x = min(max(x, 0), data_x.shape[0] - 1)
                fy += data_y[x, y] * tx

            else:
                if data_y[x, y] > 0:
                    y += 1
                    fy = 0.
                else:
                    y -= 1
                    fy = 1.
                y = min(max(y, 0), data_x.shape[1] - 1)
                fx += data_x[x, y] * ty

            line.append(seed[x, y])

        res[...] = np.mean(np.array(line) * kernel)

    return result


def _contrast(x: Union[np.array, float]) -> Union[np.array, float]:  # pragma: no cover
    return .5 * (1. - np.cos(np.pi * x))


if __name__ == '__main__':
    import argparse
    import matplotlib.pyplot as plt  # type: ignore
    logging.debug(f'matplotlib version {np.__version__}')

    parser = argparse.ArgumentParser(description='Line integral convolution Algorithms.')
    parser.add_argument('data_x_file', type=argparse.FileType('rb'))
    parser.add_argument('data_y_file', type=argparse.FileType('rb'), nargs='?')
    parser.add_argument('-l', '--linelength', type=int, default=20)
    parser.add_argument('-ps', '--pluto-single-file', action='store_true')
    args = parser.parse_args()

    logging.debug(args)

    if args.pluto_single_file is True:
        data_x, data_y = _load_pluto_single_file_data(args.data_x_file, 'B', '12')
    else:
        data_x, data_y = _load_npy_data(args.data_x_file, args.data_y_file)

    if _check_data(data_x, data_y) is False:
        exit(1)

    print(data_x[0:10, 0:10])
    print(data_y[0:10, 0:10])

    lic_result = lic(data_x, data_y, args.linelength, kernel=list(range(40)))

    plt.imshow(lic_result, cmap=plt.get_cmap('binary'), origin='lower')
    # plt.show()
    sane_x = args.data_x_file.name.split('/')[-1].replace('.', '_')
    if args.data_y_file is not None:
        sane_y = args.data_y_file.name.split('/')[-1].replace('.', '_')
    else:
        sane_y = ''
    plt.savefig(f'out_{sane_x}_{sane_y}_{args.linelength}.png')
