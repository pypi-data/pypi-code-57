"""
Copyright::

    +===================================================+
    |                 © 2020 Privex Inc.                |
    |               https://www.privex.io               |
    +===================================================+
    |                                                   |
    |        Privex's Random IOTA Tools                 |
    |        License: X11/MIT                           |
    |                                                   |
    |        Core Developer(s):                         |
    |                                                   |
    |          (+)  Chris (@someguy123) [Privex]        |
    |                                                   |
    +===================================================+

    Privex's Random IOTA Tools
    Copyright (c) 2020    Privex Inc. ( https://www.privex.io )

"""
from privex.helpers import env_bool
from os import getenv as env

IOTA_HOST = env('IOTA_HOST', 'http://localhost:14265')

RAW_MODE = env_bool('RAW_MODE', False)

