# Copyright (C) 2019 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher Oct 2019

import os
import yaml
from pydoc import locate
from ekit.logger import vprint


def setup_context(ctx_in=None, allowed=[], types=[],
                  defaults=[], remove_unknowns=False,
                  logger=None, verbose=False):
    """
    Sets up a context in the form a dictionary.

    :param ctx_in: If it is a directory containing keys corresponding to
                   parameter names defined in allowed they will be used.
                   If it is a valid path the file is assumed to be in YAML
                   format and the parameters are read from it.
    :param allowed: A list of the parameter names that are allowed
                    in the context.
    :param types: A list of the data types required for the parameters.
    :param defaults: A list of the default values of the parameters
                     (used if no other values found).
    :param verbose: If True returns some messages about what it is doing.
    :param remove_unknowns: If True then parameters that are in ctx_in but not
                            in allowed are not in the returned context.
    :return: A directory containing all the parameter names
             and their assigned values.
    """

    ctx = {}

    # first set all parameters to their defaults
    for ii, parameter in enumerate(allowed):
        ctx[parameter] = defaults[ii]

    # check if config file path is given
    if isinstance(ctx_in, str):
        if os.path.isfile(ctx_in):
            vprint("Received configuration file.",
                   logger=logger, verbose=verbose)
            with open(ctx_in, 'r') as f:
                CONF = yaml.load(f, yaml.FullLoader)
            for key in CONF.keys():
                if key in allowed:
                    if isinstance(CONF[key],
                                  locate(str(types[allowed.index(key)]))):
                        ctx[key] = CONF[key]
                    else:
                        raise Exception("Parameter {} is not \
                                         instance of type {}".format(
                            key, locate(str(types[allowed.index(key)]))))
                else:
                    if remove_unknowns:
                        vprint("Parameter {} is not kown. Ignoring".format(
                            key), logger=logger, verbose=verbose)
                    else:
                        ctx[key] = ctx_in[key]
        else:
            raise Exception("Path {} is not valid".format(ctx_in))
    # if parameters given directly as arguments overwrite
    elif ctx_in is not None:
        for key in ctx_in.keys():
            if key in allowed:
                if isinstance(ctx_in[key],
                              locate(str(types[allowed.index(key)]))):
                    vprint("Setting parameter {} to value {}".format(
                        key, ctx_in[key]), logger=logger, verbose=verbose)
                    ctx[key] = ctx_in[key]
                else:
                    raise Exception("Parameter {} is not "
                                    "instance of type {}. Value is: {}".format(
                                        key, locate(
                                            str(types[allowed.index(key)])),
                                        ctx_in[key]))
            else:
                if remove_unknowns:
                    vprint("Parameter {} is not kown. Ignoring".format(
                        key), logger=logger, verbose=verbose)
                else:
                    ctx[key] = ctx_in[key]

    vprint("Set context to:", logger=logger, verbose=verbose)
    vprint(
        '######################################',
        logger=logger, verbose=verbose)
    for parameter in allowed:
        vprint("{} : {}".format(
            parameter, ctx[parameter]), logger=logger, verbose=verbose)
    vprint(
        '######################################',
        logger=logger, verbose=verbose)

    return ctx
