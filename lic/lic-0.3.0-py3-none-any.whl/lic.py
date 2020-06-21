#!/usr/bin/env python3
# coding: utf-8

"""line integral convolution for numpy arrays
"""

__version__ = '0.3.0'

import argparse
import logging
import sys
from typing import List, Sequence, Tuple, Union
import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore

_LIC_DEBUG_MODE = False

logging_format = 'lic | %(asctime)s | %(levelname)-8s | %(message)s'
logging.basicConfig(format=logging_format, level=logging.WARNING)
plt_logger = logging.getLogger('matplotlib')
plt_logger.setLevel(level=logging.WARNING)

logging.debug(f'matplotlib version {np.__version__}')
logging.debug(f'numpy version {np.__version__}')

_eps = 1e-6


def _load_npy_data(file_x: str, file_y: str) -> Tuple[np.ndarray, np.ndarray]:
    logging.info(f'loading data files: {file_x} and {file_y}')
    try:
        data_x = np.load(file_x)
        data_y = np.load(file_y)
    except FileNotFoundError as e:
        logging.error('Could not read one of the input files')
        raise e

    logging.info(f'successfully opened the data files: {file_x} and {file_y}')
    logging.debug(f'shape of data_x: {data_x.shape}')
    logging.debug(f'shape of data_y: {data_y.shape}')

    return data_x, data_y


def _load_seed(seed_file: str) -> np.ndarray:
    logging.info(f'loading seed file: {seed_file}')
    try:
        seed = np.load(seed_file)
    except FileNotFoundError as e:  # pragma: no cover
        logging.error('Could not read the seed file')
        raise e

    logging.info(f'successfully opened the seed file: {seed_file}')
    logging.debug(f'shape of seed: {seed.shape}')

    return seed


def _load_pluto_single_file_data(file_data: str,
                                 var='B',
                                 dim='12') -> Tuple[np.ndarray, np.ndarray]:  # pragma: no cover
    logging.warning('only 2d PLUTO dbl single files are supported at the moment')
    try:
        data = np.fromfile(file_data)
    except FileNotFoundError as e:
        logging.error('could not read one of the input files')
        raise e

    data = data.reshape((7, 400, 160))
    if var == 'B':
        data_x = data[2 + int(dim[1]), :, :]
        data_y = data[2 + int(dim[0]), :, :]
    elif var == 'v':
        data_x = data[int(dim[0]), :, :]
        data_y = data[int(dim[1]), :, :]
    else:
        raise NotImplementedError('in _load_pluto_single_file_data: var has to be one of "v" or "B"')
    return data_x, data_y


def _check_data(data_x: np.ndarray, data_y: np.ndarray) -> bool:
    logging.info('checking the data')
    if len(data_x.shape) != 2:
        logging.error(f'data has to be 2d. data_x is {len(data_x.shape)}d.')
    if len(data_y.shape) != 2:
        logging.error(f'data has to be 2d. data_y is {len(data_y.shape)}d.')
    if len(data_x.shape) != 2 or len(data_y.shape) != 2:
        return False

    if (data_x.shape[0] != data_y.shape[0] or data_x.shape[1] != data_y.shape[1]):
        logging.error(f'data shapes do not match: x {data_x.shape}, y {data_y.shape}.')
        return False
    logging.info('data is valid')

    return True


def gen_seed(shape: Tuple[int, int],
             noise='white',
             points_every: Union[Tuple[int, int], int] = None,
             points_size: int = 0,
             points_alternate: bool = True,
             combine: str = 'multiply') -> np.ndarray:
    """Generate a 2d seed for the lic algorithm. The seed array can be generated using a random
    noise of values between 0.0 and 1.0 with different power spectrum and additional "points"
    spread evenly across the array. The distance between the points and their size can be adjusted.

    :param shape: the shape of the resulting seed, should be equal to the data dimensions
    :type shape: Tuple[int, int]
    :param noise: the power spectrum of the generated noise, defaults to 'white',
        future options are going to be 'white', 'pink' and 'blue'
    :type noise: str, optional
    :param points_every: add a regoin of values 1.0 every n points, defaults to None, which means nothing is added.
        If a tuple of two ints is given, the values are applied to the x and y direction seperately.
    :type points_every: tuple of ints or int, optional
    :param points_size: size of the added points, defaults to 0, which means a single pixel
    :type points_size: int, optional
    :param points_alternate: whether to alternate the placement of the points, defaults to True
    :type points_alternate: bool, optional
    :param combine: how to add the points to the random background, defaults to 'multiply', possible values are
        'multiply', 'sum', 'replace'
    :type combine: str, optional

    :raises NotImplementedError: in case of selecting options which have not been implementeds yet

    :return: the generated 2d seed array
    :rtype: numpy.ndarray
    """
    logging.info('generate the seed')
    if noise == 'white':
        np.random.seed(28032005)
        seed = np.random.random(shape)
    else:
        raise NotImplementedError('lic.gen_seed: parameter noise must be one of ["white"]')

    if points_size != 0:
        raise NotImplementedError('lic.gen_seed: point size is limited to 0 (i.e., one pixel) as of now.')

    if points_every is not None:
        # generate point pattern
        points = np.zeros_like(seed)
        if isinstance(points_every, int):
            _points_every = points_every, points_every
        else:
            _points_every = points_every

        if points_alternate is True:
            points[1::_points_every[0] * 2, 1::_points_every[1]] = 1.0
            points[1 + _points_every[0]::_points_every[0] * 2, 1 + int(_points_every[1] / 2)::_points_every[1]] = 1.0
        else:
            points[1::_points_every[0], 1::_points_every[1]] = 1.0

        # combine with seed
        if combine == 'multiply':
            seed *= points
        elif combine == 'sum':
            seed += points
        elif combine == 'replace':
            seed = np.where(points == 1.0, points, seed)
        else:
            raise ValueError(f'lic.gen_seed: {combine} is not a valid value for parameter combine.')  # pragma: no cover

    seed[0, :] = seed[:, 0] = seed[-1, :] = seed[:, -1] = 0.5
    logging.info('generated the seed')
    return seed


def lic(data_x: np.ndarray,
        data_y: np.ndarray,
        length: int = 10,
        kernel: Sequence = None,
        seed: np.ndarray = None,
        contrast: bool = False) -> np.ndarray:
    """Generate a line integral convolution representation of the input data.

    :param data_x: a 2d numpy.ndarray with the x component of the vector field
    :type data_x: numpy.ndarray
    :param data_y: a 2d numpy.ndarray with the y component of the vector field
    :type data_y: numpy.ndarray
    :param length: the length of the line of the lic
    :type length: int, optional
    :param kernel: the convolution kernel of the lic
    :type kernel: a sequence (e.g., list or numpy.ndarray), optional
    :param seed: a 2d numpy.ndarray containing the seed of the lic. If no seed array is passed,
        a random seed is generated.
    :type seed: numpy.ndarray, optional
    :param contrast: whether to enhance the contrast of the resulting lic image
    :type contrast: bool, optional

    :return: The generated 2d lic array
    :rtype: numpy.ndarray
    """

    assert length > 0
    assert len(data_x.shape) == 2
    assert len(data_y.shape) == 2
    assert data_x.shape[0] == data_y.shape[0] and data_x.shape[1] == data_y.shape[1]

    logging.info('starting lic')

    # adjust and/or generate kernel and length
    if kernel is None:
        kernel = np.ones(length)
    else:
        logging.warning(f'lic.lic: overwriting parameter length with {len(kernel)}')
        length = len(kernel)
        kernel = np.array(kernel) / np.mean(kernel)

    # generate seed if necessary or check validity of the provided seed
    if seed is None:
        seed = gen_seed(data_x.shape)
    else:
        assert isinstance(seed, np.ndarray), 'lic.lic: parameter seed must be of type numpy.ndarray.'
        assert len(seed.shape) == 2, 'lic.lic: parameter seed must be 2d.'
        assert seed.shape[0] == data_x.shape[0] and seed.shape[1] == data_x.shape[1],\
            'lic.lic: parameter seed must have the same dimensions as the data.'

    if _LIC_DEBUG_MODE:
        plt.imshow(seed, cmap=plt.get_cmap('binary'), origin='lower')
        plt.show()

    # generate result
    result = np.empty_like(seed)
    it = np.nditer(result, flags=['multi_index'], op_flags=['writeonly'])
    for res in it:
        line = _get_flow_line(data_x, data_y, it.multi_index, length)
        res[...] = np.mean(np.array([seed[idx] for idx in line]) * kernel)

    # normalize and enhance contrast
    result = _normalize(result)
    if contrast is True:
        result = _contrast(result)

    logging.info('lic created')
    return result


def _get_flow_line(data_x: np.ndarray,
                   data_y: np.ndarray,
                   idx: Tuple[int, int],
                   length: int = 10) -> List[Tuple[int, int]]:
    """Get the flow line coordinates starting from one point in the data."""
    fx = fy = 0.5
    line = []
    for _ in range(length):
        t = (np.inf, np.inf)
        if data_x[idx] > _eps:
            t = ((1 - fx) / data_x[idx], t[1])
        elif data_x[idx] < -_eps:
            t = (-fx / data_x[idx], t[1])
        if data_y[idx] > _eps:
            t = (t[0], (1 - fy) / data_y[idx])
        elif data_y[idx] < -_eps:
            t = (t[0], -fy / data_y[idx])
        if t[0] < t[1]:
            if data_x[idx] > 0:
                idx = (idx[0] + 1, idx[1])
                fx = 0.
            else:
                idx = (idx[0] - 1, idx[1])
                fx = 1.
            idx = (min(max(idx[0], 0), data_x.shape[0] - 1), idx[1])
            fy += data_y[idx] * t[0]

        else:
            if data_y[idx] > 0:
                idx = (idx[0], idx[1] + 1)
                fy = 0.
            else:
                idx = (idx[0], idx[1] - 1)
                fy = 1.
            idx = (idx[0], min(max(idx[1], 0), data_x.shape[1] - 1))
            fx += data_x[idx] * t[1]

        line.append(idx)
    return line


def _contrast(v: Union[np.ndarray, float]) -> Union[np.ndarray, float]:  # pragma: no cover
    return .5 * (1. - np.cos(np.pi * v))


def _normalize(arr: np.ndarray) -> np.ndarray:
    """scale the input array to the interval [0, 1]

    >>> _normalize(np.array([2, 3, 4]))
    array([0. , 0.5, 1. ])
    """
    return (arr - arr.min()) / (arr - arr.min()).max()


def _set_logging_level(quiet: bool, verbose: bool, debug: bool) -> None:  # pragma: no cover
    if debug is True:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.info('debug mode engaged')
    if verbose is True:
        logging.getLogger().setLevel(logging.INFO)
    if quiet is True:
        logging.getLogger().setLevel(logging.ERROR)


def run(argv: list = None):
    """the command line tool. Please use the ``--help`` option to get help."""

    # parse the command line options
    parser = argparse.ArgumentParser(description='Line integral convolution (lic) algorithm. '
                                     'Please have a look at the documentation (https://pypi.org/project/lic/) '
                                     'for further information on how tho use this software.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('data_x_file', type=argparse.FileType('rb'),
                        help='an npy file containing a 2d numpy.ndarray with the x component '
                        'of the vector field')
    parser.add_argument('data_y_file', type=argparse.FileType('rb'),
                        help='an npy file containing a 2d numpy.ndarray with the y component '
                        'of the vector field')
    parser.add_argument('-s', '--seed-file', type=argparse.FileType('rb'),
                        help='an npy file containing a 2d numpy.ndarray with the seed image')
    parser.add_argument('-l', '--line-length', type=int, default=20, metavar='LENGTH',
                        help='the length of the line of the lic')
    parser.add_argument('-o', '--output-file', type=str, metavar='FILE',
                        help='the name of the output file, If it is not set, a name will be generated from '
                        'the names of the input data files.')
    parser.add_argument('-c', '--enhance-contrast', action='store_true',
                        help='enhance the contrast of the resulting lic image')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='switch off text output except for error messages. This will overwrite -v.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='more verbose text output')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='switch on debug mode. This will show intermediate results and plots, as well as '
                        'log a lot of debugging information.')
    parser.add_argument('-ps', '--pluto-single-file', action='store_true',
                        help=argparse.SUPPRESS)
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}',
                        help='show the version of this software')
    args = parser.parse_args(argv)

    # print the logo and version
    if args.quiet is False:  # pragma: no cover
        print(f'⎣⫯🤇  v{__version__}')

    # set debug mode
    _LIC_DEBUG_MODE = args.debug

    # set verbosity level
    _set_logging_level(args.quiet, args.verbose, args.debug)

    logging.debug(args)

    if args.pluto_single_file is True:  # pragma: no cover
        x, y = _load_pluto_single_file_data(args.data_x_file.name, 'B', '12')
    else:
        x, y = _load_npy_data(args.data_x_file.name, args.data_y_file.name)

    if _check_data(x, y) is False:  # pragma: no cover
        sys.exit(1)

    if args.seed_file is None:
        seed_data = gen_seed(x.shape,
                             noise='white',
                             points_every=1,
                             points_size=0,
                             points_alternate=True,
                             combine='multiply')
    else:
        seed_data = _load_seed(args.seed_file.name)

    lic_result = lic(x, y, length=args.line_length, contrast=args.enhance_contrast, seed=seed_data)

    if _LIC_DEBUG_MODE:
        plt.hist(lic_result.flatten(), 100)
        plt.show()

    # generate plot
    plt.imshow(lic_result, cmap=plt.get_cmap('binary'), origin='lower')

    # generate sane output file name
    if args.output_file is None:
        sane_x = args.data_x_file.name.split('/')[-1].replace('.', '_')
        if args.data_y_file is not None:
            sane_y = args.data_y_file.name.split('/')[-1].replace('.', '_')
        else:  # pragma: no cover
            sane_y = ''
        output_filename = f'out_{sane_x}_{sane_y}_{args.line_length}.png'
    else:  # pragma: no cover
        output_filename = args.output_file

    # save plot to file
    logging.info(f'saving lic plot to {output_filename}')
    plt.savefig(output_filename)
    if _LIC_DEBUG_MODE:
        plt.show()
    logging.info('all done.')


if __name__ == '__main__':
    run()
