# FlexiRPG -- directory paths.
#
# Copyright (C) 2010-2011 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
import sys
import os
import errno
import pkg_resources

dir_struct = {}

#-------------------------------------------------------
# void load_paths( dir_struct_reference )
# moved structure loading from dirpath.py by Snowdog 3-8-05
#-------------------------------------------------------
def load_paths(dir_struct):
    root_dir = pkg_resources.resource_filename(__name__, "images")

    dir_struct["icon"] = pkg_resources.resource_filename(__name__, "images") + os.sep
    dir_struct["template"] = pkg_resources.resource_filename(__name__, "templates") + os.sep

    #
    # Path to user files.
    #
    # Windows:
    #    %APPDATA%\OpenRPG\ = X:\Documents\<user>\Application Data\FlexiRPG\
    #
    # Linux:
    #   $HOME/.flexirpg/ = /home/<user>/.flexirpg/
    #
    if 'HOME' in os.environ:
        _user_dir = os.environ['HOME'] + os.sep + ".flexirpg" + os.sep
    elif 'APPDATA' in os.environ:
        _user_dir = os.environ['APPDATA'] + os.sep + "FlexiRPG" + os.sep
    else:
        # Neither Windows nor Linux?
        _user_dir = os.path.dirname(__file__) + "myfiles"

    for d in (_user_dir, _user_dir + "runlogs", _user_dir + "logs"):
        try:
            os.makedirs(d)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    dir_struct["user"] = _user_dir
    dir_struct["logs"] = dir_struct["user"] + "logs" + os.sep

load_paths(dir_struct)
