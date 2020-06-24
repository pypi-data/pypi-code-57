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
    
    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy,
    modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all copies or substantial portions of
    the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
    WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
    OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
    OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    
    Except as contained in this notice, the name(s) of the above copyright holders shall not be used in advertising or
    otherwise to promote the sale, use or other dealings in this Software without prior written authorization.


"""

import logging
import sys

from privex.loghelper import LogHelper
from privex.iota.client import PrivexIota
from privex.iota.objects import Neighbor, NodeInfo, NeighborRes
from privex.iota.status import print_intro, gen_cols, iter_cols, main as iota_status_app, load_node_info

name = 'iota'
VERSION = '0.8.0'

_lh = LogHelper(__name__, handler_level=logging.INFO)
_lh.add_console_handler(stream=sys.stderr)
