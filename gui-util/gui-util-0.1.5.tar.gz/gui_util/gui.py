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


def get_recent_windows(exclude, limit):

    wm = EWMH()

    xlib_windows = wm.getClientListStacking()
    windows_recent_last = [Window.from_xlib_window(xlib_win) for xlib_win in xlib_windows]
    windows_recent_first = list(reversed(windows_recent_last))

    windows_result = windows_recent_first

    if exclude:
        for win in windows_result:
            if win.name == exclude:
                windows_result.remove(win)

    if limit:
        windows_result = windows_result[:10]

    return windows_result


def get_recent_window(exclude):

    recent_windows = get_recent_windows(exclude=exclude, limit=1)
    recent_window = recent_windows[0]

    return recent_window
