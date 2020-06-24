# Copyright (C) 2019 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher Oct 2019

import subprocess
import os
import numpy as np
import collections

from ekit.logger import vprint


def create_path(identity, out_folder=None, defined_parameters={},
                undefined_parameters=[], suffix=''):
    """
    Creates a standardised path for files. The meta data is encoded in the path
    and can be savely recovered using the get_parameters_from_path function.
    NOTE: Your variable names must not contain underscores or equal signs.

    :param identity: The prefix of the name.
    :param out_folder: The directory of the file.
    :param defined_parameters: A dictionary of key value pairs.
    :param undefined_parameters: A list of parameters that do not have a name
                                (be mindful about their order when
                                reading them from the name again!).
    :param suffix: What should go at the end of the name.
    :return: A string which is the created path.
    """
    if out_folder is None:
        outstring = identity
    else:
        outstring = "{}/{}".format(out_folder, identity)

    # order by keys to remove ambigous ordering
    defined_parameters = collections.OrderedDict(sorted(
                                                 defined_parameters.items()))

    # add the defined parameters
    for key in defined_parameters.keys():
        add = '_{}={}'.format(key, defined_parameters[key])
        outstring = outstring + add

    # add the undefined parameters
    for param in undefined_parameters:
        add = '_{}'.format(param)
        outstring = outstring + add

    # add suffix
    outstring += suffix

    return outstring


def get_parameters_from_path(paths, suffix=True, fmt=None):
    """
    Given a list of standardised paths, or a single path created with
    create_path() this function reads the parameters in the paths.

    :param paths: Either a single string or a list of strings. The strings
                  should be paths in the create_path() format.
    :param suffix: If True assumes that the given paths have suffixes and
                   exclues them from the parsing
    :return: Returns a dictionary which contains the defined parameters and
             a list containing the undefined parameters.
    """
    # convert to list if needed
    if not isinstance(paths, list):
        paths = [paths]

    # use first path to initialize the dictionary and list for output
    defined_names = []
    undefined_count = 0
    path = paths[0]

    path = _prepare_path(path, suffix=suffix)

    # loop over parameters in first path to initialize dictionary
    for c in path:
        if isinstance(c, list):
            c = c[0]
        if '=' in c:
            b = c.split('=')
            defined_names.append(b[0])
        else:
            undefined_count += 1

    # initialize
    undefined = np.zeros((len(paths), undefined_count), dtype=object)
    defined = {}
    for d in defined_names:
        defined[d] = np.zeros(len(paths), dtype=object)

    # loop over files and get parameters
    for ii, path in enumerate(paths):
        path = _prepare_path(path, suffix=suffix)
        count = 0
        for idx_c, c in enumerate(path):
            if isinstance(c, list):
                c = c[0]
            if '=' in c:
                b = c.split('=')
                to_add = _check_type(b[1], fmt, idx_c)
                defined[b[0]][ii] = to_add
            else:
                to_add = _check_type(c, fmt, idx_c)
                undefined[ii, count] = to_add
                count += 1
    return defined, undefined


def mkdir_on_demand(path, logger=None, verbose=False):
    """
    Creates a directory if it does not exist.

    :param path: The path to the directory.
    :param logger: A logging instance if needed.
    """
    if not os.path.exists(path):
        subprocess.call(["mkdir -p {}".format(path)], shell=True)
        vprint("Created directory-tree for {}".format(path), logger=logger,
               verbose=verbose)


def _check_type(in_, fmt, idx):
    if fmt is not None:
        try:
            format = fmt[idx]
        except IndexError:
            format = None
    else:
        format = None

    if format is None:
        if in_ == 'True':
            to_add = True
        elif in_ == 'False':
            to_add = False
        else:
            try:
                to_add = int(in_)
            except ValueError:
                try:
                    to_add = float(in_)
                except ValueError:
                    try:
                        to_add = str(in_)
                    except ValueError:
                        raise Exception(
                            "Did not understand parameter: "
                            "{}. Not a bool, integer, "
                            "float nor string".format(in_))
    return to_add


def _prepare_path(path, suffix=True):
    path = path.split('/')[-1]
    path = path.split('_')

    # do not consider identifier
    path = path[1:]

    # do not consider suffix
    if suffix:
        path[-1] = path[-1].split('.')[:-1]
    else:
        path[-1] = path[-1].split('.')
    path[-1] = '.'.join(path[-1])
    return path
