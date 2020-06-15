# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import os

try:
    from collections import OrderedDict
except:
    from ordereddict import OrderedDict
from configobj import ConfigObj


class Config(object):
    """Reads and writes the config file `devyzer.rc`.

    Attributes:
        * TOKEN ; the token used to communitcate with devyzer bot
        * SHORTCUTS: A string that represents the start of shortcuts in
            the config file ~/.devyzer.rc.
        * MAIN: A string that represents the main set of configs in
            ~/.devyzer.rc.
        * THEME: A string that represents the config theme.
        * LOG_FILE: A string that represents the config log file location.
        * LOG_LEVEL: A string that represents the config default log
            file level.
        * COLOR: A string that represents the config color output mode.
        * FUZZY: A string that represents the config fuzzy matching mode.
        * SHORTCUT: A string that represents the config shortcut matching
             mode.
    """
    TOKEN = 'token'

    SHORTCUTS = 'shortcuts'
    MAIN = 'main'
    AUTH = 'auth'
    THEME = 'theme'
    LOG_FILE = 'log_file'
    LOG_LEVEL = 'log_level'
    COLOR = 'color_output'
    FUZZY = 'fuzzy_match'
    SHORTCUT = 'shortcut_match'

    # IS_COMMAND = 'is_command'

    def read_configuration(self, config_template=None, config_path=None):
        """Reads the config file if it exists, else reads the default config.

        Args:
            * config_template: A string representing the template file name.
            * config_path: A string representing the template file path.

        Returns:
            An instance of a ConfigObj.
        """
        if config_template is None:
            config_template = """
[main]

# Visual theme. Possible values: manni, igor, xcode, vim, autumn, vs, rrt,
# native, perldoc, borland, tango, emacs, friendly, monokai, paraiso-dark,
# colorful, murphy, bw, pastie, paraiso-light, trac, default, fruity
theme = vim

# Use color output mode.
color_output = True

# Use fuzzy matching mode for resources (default is to use simple substring match).
fuzzy_match = True

# Use shortcut matching mode
shortcut_match = True

# log_file location.
log_file = ~/.devyzer.log

# Default log level. Possible values: "CRITICAL", "ERROR", "WARNING", "INFO"
# and "DEBUG".
log_level = INFO

[auth]

token =  
            """
        if config_path is None:
            config_path = '~/.devyzer.rc'

        self._create_from_template(config_template, config_path)
        return self._read_configuration(config_path)

    def _read_configuration(self, usr_config, def_config=None):
        """Reads the config file if it exists, else reads the default config.

        Internal method, call read_configuration instead.

        Args:
            * usr_config: A string that specifies the config file name.
            * def_config: A string that specifies the config default file name.

        Returns:
            An instance of a ConfigObj.
        """
        usr_config_file = os.path.expanduser(usr_config)
        cfg = ConfigObj()
        cfg.filename = usr_config_file
        if def_config:
            cfg.merge(ConfigObj(def_config, interpolation=False))
        cfg.merge(ConfigObj(usr_config_file, interpolation=False))
        return cfg

    def _create_from_template(self, temolate_config, destination, overwrite=False):
        """Writes the default config from a template.

        Args:
            * source: A string that specifies  the template.
            * destination: A string that specifies the path to write.
            * overwite: A boolean that specifies whether to overwite the file.

        Returns:
            None.
        """
        destination = os.path.expanduser(destination)
        if not overwrite and os.path.exists(destination):
            return

        with open(destination, 'w') as fp:
            fp.write(temolate_config)
