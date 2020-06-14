import Xlib
from Xlib import Xatom
from Xlib.xobject.drawable import Window
from dataclasses import dataclass


@dataclass
class Window:

    xlib_win: Window

    def __repr__(self):
        _id = self.xlib_win.get_attributes()
        return f'Window(name="{self.name}")'

    @property
    def name(self):
        display = Xlib.display.Display()
        atom_net_wm_name = display.intern_atom('_NET_WM_NAME')
        name = self.xlib_win.get_full_text_property(atom_net_wm_name, 0)
        return name

    @property
    def name_temp(self):
        # return self.xlib_win.get_wm_name()
        # import pdb; pdb.set_trace()

        disp = Xlib.display.Display()
        # NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')
        # aa = disp.intern_atom('_NET_WM_VISIBLE_NAME')
        aa = disp.intern_atom('_NET_WM_NAME')
        # bb = self.xlib_win.get_full_text_property(aa, Xatom.STRING)
        bb = self.xlib_win.get_full_text_property(aa, 0)
        cc = self.xlib_win.get_full_property(aa, 0)
        print(self.xlib_win.get_wm_class())
        print(self.xlib_win.get_wm_transient_for())
        print(self.xlib_win.get_wm_name())
        # import pdb; pdb.set_trace()
        import pdb; pdb.set_trace()
        return self.xlib_win.get_wm_name()
        # return self.xlib_win.get_wm_class()
        # return self.xlib_win.

    @classmethod
    def from_xlib_window(cls, xlib_win):
        window = Window(xlib_win=xlib_win)
        return window


