from typing import Tuple, Optional

import Xlib
from ewmh import EWMH

from gui_util.window import Window


def focus_on_window(window_name):

    # from shell_util

    return True


def get_current_window():
    wm = EWMH()
    xlib_win = wm.getActiveWindow()
    window = Window.from_xlib_window(xlib_win)
    return window
