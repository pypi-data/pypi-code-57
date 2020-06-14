import Xlib
from Xlib.xobject.drawable import Window
from dataclasses import dataclass


@dataclass
class Window:

    xlib_win: Window

    def __repr__(self):
        _id = self.xlib_win.get_attributes()
        return f"Window(name='{self.name}')"

    @property
    def name(self):
        display = Xlib.display.Display()
        atom_net_wm_name = display.intern_atom("_NET_WM_NAME")
        name = self.xlib_win.get_full_text_property(atom_net_wm_name, 0)
        return name

    @classmethod
    def from_xlib_window(cls, xlib_win):
        window = Window(xlib_win=xlib_win)
        return window
