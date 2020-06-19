#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Copyright (C) 2019, 2020 Brandon M. Pace
#
# This file is part of logcontrol
#
# logcontrol is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# logcontrol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with logcontrol.
# If not, see <https://www.gnu.org/licenses/>.

"""module for validation functions"""


import logging
import os


def validate_file_path(filepath: str):
    """Internal function to validate that a provided path is good for logging"""
    if os.path.isdir(filepath):
        raise ValueError(f"Provided filepath is a directory and not a file. Path: '{filepath}'")

    directory, filename = os.path.split(filepath)
    if not os.path.isdir(directory):
        raise ValueError(f"Provided filepath does not contain a valid directory. Path: '{filepath}'")
    elif not filename:  # should be caught by the first isdir above, but just in case..
        raise ValueError(f"Provided filepath does not have any filename part. Path: '{filepath}'")


def validate_group_name(name: str):
    """Internal function to make sure any new group names are valid"""
    if isinstance(name, str):
        if not name:
            raise ValueError(f"Group name must not be empty string")
    else:
        raise TypeError(f"Group name must be str, got: '{type(name)}'")


def validate_handler_object(handler: logging.Handler):
    if not isinstance(handler, logging.Handler):
        raise TypeError(f"Expected logging.Handler, got: '{type(handler)}'")


def validate_logger_object(logger: logging.Logger):
    if not isinstance(logger, logging.Logger):
        raise TypeError(f"Expected logging.Logger, got: '{type(logger)}'")
