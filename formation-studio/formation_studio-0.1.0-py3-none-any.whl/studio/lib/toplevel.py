"""
Toplevel widget factory. Creates a Frame resembling window manager on your
platform.
"""
# ======================================================================= #
# Copyright (C) 2020 Hoverset Group.                                      #
# ======================================================================= #
import tkinter as tk

from hoverset.ui.icons import get_icon
from hoverset.ui.widgets import Frame
from studio.lib.pseudo import PseudoWidget, Groups


class BaseTopLevel(PseudoWidget, Frame):
    display_name = 'Toplevel'
    group = Groups.container
    icon = get_icon("labelframe")
    impl = tk.Toplevel

    def __init__(self, master, id_):
        super().__init__(master)
        self.id = id_
        self.setup_widget()

    def set_name(self, name):
        self.title(name)