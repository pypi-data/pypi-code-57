import os
import tkinter
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from pandastable import Table
from .. import datahandler
from . import interface


class RootWindow(tkinter.Tk, interface.RootWindow):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.wm_title('vidtrain')

    def run(self):
        self.mainloop()


class ElementMixin(interface.Element):

    def show(self, side=interface.LEFT, fill=interface.NONE, expand=interface.OFF, padx=0, pady=0):
        '''show the panel'''
        self.pack(side=side, fill=fill, expand=expand, padx=padx, pady=pady)

    def hide(self):
        '''hide the panel'''
        self.pack_forget()


class Panel(ttk.Frame, ElementMixin, interface.Panel):
    '''A user interface container for other elements'''

    def __init__(self, master, **kw):
        ttk.Frame.__init__(self, master=master, **kw)
        self.label = None
        self.tk_focusFollowsMouse()

    def add_label(self, text, side=tkinter.TOP, fill=tkinter.NONE, expand=tkinter.OFF):
        self.label = ttk.Label(master=self, text=text)
        self.label.pack(side=side, fill=fill, expand=expand)

    def edit_label(self, text):
        self.label['text'] = text


class PanelKey:
    '''handles keyboard events for FigureCanvas'''

    def __init__(self, master, callback=None):
        self.canvas = master
        self.focus_set()
        self.callback = callback or interface._empty_callback
        self.canvas.bind('<Key>', self.on_key_press, add='+')

    def focus_set(self, _=None):
        self.canvas.focus_set()

    def on_key_press(self, event):
        modifiers = {
            0x1: 'Shift',
            0x4: 'Control',
            0x8: 'Alt'
        }
        mod = '+'.join([v for k, v in modifiers.items() if k & event.state])
        if len(mod) > 0:
            key = mod + '+' + event.keysym
        else:
            key = event.keysym
        self.callback(key)


class Filedialog(interface.Filedialog):
    def ask_open(self, filetypes):
        '''Open a filedialog and return the path to a file.

        Arguments:
        filetypes: 2d tuple of strings describing the allowed file types
                   [('description', '.ext')]

        Returns:
        string: path to file
        '''
        return tkinter.filedialog.askopenfilename(filetypes=filetypes)

    def ask_save(self, filetypes):
        '''Open a filedialog and return the path to a file.

        Arguments:
        filetypes: 2d tuple of strings describing the allowed file types
                   [('description', '.ext')]

        Returns:
        string: path to file
        '''
        return tkinter.filedialog.asksaveasfilename(filetypes=filetypes)

    def ask_directory(self):
        return tkinter.filedialog.askdirectory()


class Dialogs(interface.Dialogs):
    def __init__(self, title=None):
        self.title = title

    def info(self, message):
        tkinter.messagebox.showinfo(title=self.title, message=message)

    def yes_no(self, message):
        return tkinter.messagebox.askyesno(title=self.title, message=message)


class Button(ttk.Button, ElementMixin, interface.Button):
    '''A simple button that enables once a callback is set'''

    def __init__(self, master, text, on_click=None):
        ttk.Button.__init__(self, master=master, text=text, command=self._callback, state=['disabled'])
        if on_click is None:
            self._on_click = interface._empty_callback
        else:
            self.on_click = on_click

    @property
    def on_click(self):
        '''callback function that is executed when the button is clicked'''
        return self._on_click

    @on_click.setter
    def on_click(self, callback):
        '''callback function that is executed when the button is clicked

        Arguments:
        callback: the function to be executed (activates the button) or None (deactivates the button)
        '''
        if callback is None:
            self._on_click = interface._empty_callback
            self.state(['disabled'])
        else:
            self._on_click = callback
            self.state(['!disabled'])

    def _callback(self):
        self.on_click()


class Tabs(Panel):
    def __init__(self, master, tabposition=interface.TOP, on_tab_select=interface._empty_callback):
        Panel.__init__(self, master=master)
        self.style = ttk.Style(self)
        if tabposition == interface.LEFT:
            tp = 'wn'
        elif tabposition == interface.RIGHT:
            tp = 'en'
        elif tabposition == interface.BOTTOM:
            tp = 'sw'
        else:
            tp = 'nw'
        self.style.configure('vidtrain.TNotebook', tabposition=tp)
        self.tabs = ttk.Notebook(master=self, style='vidtrain.TNotebook')
        self.tabs.bind("<<NotebookTabChanged>>", self._tab_selected)
        self.tabs.pack()
        self.on_tab_select = on_tab_select

    def insert(self, i, tab):
        self.tabs.insert(i, tab, text=tab.NAME)

    def remove(self, i):
        self.tabs.forget(i)

    def replace(self, i, tab):
        self.remove(i)
        self.insert(i, tab)

    def append(self, tab):
        self.tabs.add(tab, text=tab.NAME)

    def extend(self, tab_list):
        for tab in tab_list:
            self.append(tab)

    def select(self, tab_id):
        self.tabs.select(tab_id=tab_id)

    def _tab_selected(self, event):
        self.on_tab_select(self.tabs.index('current'))


class FigureSaveButton(NavigationToolbar2Tk):
    toolitems = (('Save', 'Save the figure', 'filesave', 'save_figure'))


class FigureCanvas(FigureCanvasTkAgg):

    def get_toolbar(self, master):
        return NavigationToolbar2Tk(self, master)

    def get_save_button(self, master):
        return FigureSaveButton(self, master)

    def get_widget(self):
        return self.get_tk_widget()

    def show_canvas(self, side=tkinter.TOP, fill=tkinter.BOTH, expand=tkinter.ON):
        self.get_tk_widget().pack(side=side, fill=fill, expand=expand)


class NetworkListPanel(Panel):
    def __init__(self, master, network_list: datahandler.interface.NetworkList, **kw):
        Panel.__init__(self, master, **kw)
        self.network_list = network_list
        self.pandas_table = Table(self, dataframe=self.network_list.networks, showtoolbar=False, showstatusbar=True)
        self.pandas_table.show()
        # TODO: (prio 5) add controls for deleting networks

    def update(self):
        self.pandas_table.redraw()

    def destroy(self):
        self.pandas_table.close()
        super().destroy()


class ConfigElementMixin(Panel):
    def __init__(self, config_item: datahandler.interface.ConfigItem, master=None, **kw):
        Panel.__init__(self, master, **kw)
        self.config_item = config_item
        self._config_callback = self.config_item.on_change
        self.config_item.on_change = self.update_gui
        self._var = tkinter.StringVar(master)

    def update_var(self):
        self._var.set(self.config_item.value)

    def update_gui(self, val):
        self.update_var()
        self._config_callback(val)


class ConfigEntry(ConfigElementMixin):
    def __init__(self, config_item: datahandler.interface.ConfigItem, master=None, **kw):
        ConfigElementMixin.__init__(self, config_item=config_item, master=master, **kw)
        self.label = ttk.Label(self, text=self.config_item.name + ': ')
        self.label.pack(side=interface.LEFT)
        self._var = tkinter.StringVar(master)
        self.update_var()
        self.entry = ttk.Entry(master=self, textvariable=self._var,
                               validate='focusout', validatecommand=self.update_config)
        self.entry.pack(side=interface.LEFT)

    def update_config(self):
        self.config_item.value = self._var.get()
        return True


class ConfigScale(ConfigElementMixin):
    def __init__(self, config_item: datahandler.interface.NumericConfigItem, master=None, **kw):
        ConfigElementMixin.__init__(self, config_item=config_item, master=master, **kw)
        self.scale = ScaleSpinbox(master=self, from_=config_item.from_,
                                  to=config_item.to, increment=config_item.increment,
                                  on_change=self.update_config, label=config_item.name + ':')
        self.update_var()
        self.scale.pack(side=interface.LEFT, fill=interface.X, expand=interface.ON)

    def update_var(self):
        self.scale.value = self.config_item.value

    def update_config(self, event):
        self.config_item.value = self.scale.value


class ConfigSpinbox(ConfigElementMixin):
    def __init__(self, config_item: datahandler.interface.NumericConfigItem, master=None, **kw):
        ConfigElementMixin.__init__(self, config_item=config_item, master=master, **kw)
        self.label = ttk.Label(self, text=self.config_item.name + ': ')
        self.label.pack(side=interface.LEFT)
        self.update_var()
        # use a tkinter spinbox here to avoid problems when the callback is interrupted by a dialog
        self.spinbox = tkinter.Spinbox(master=self, textvariable=self._var, from_=config_item.from_,
                                       to=config_item.to, increment=config_item.increment, width=5,
                                       command=self.update_config, font=('sans', '11'))
        self.spinbox.pack(side=interface.LEFT)

    def update_config(self):
        self.config_item.value = self._var.get()


class ConfigOptionSpinbox(ConfigElementMixin):
    def __init__(self, config_item: datahandler.interface.OptionConfigItem, master=None, **kw):
        Panel.__init__(self, master, **kw)
        ConfigElementMixin.__init__(self, config_item=config_item, master=master, **kw)
        self.label = ttk.Label(self, text=self.config_item.name + ': ')
        self.label.pack(side=interface.LEFT)
        self.update_var()
        self.spinbox = ttk.Spinbox(master=self, textvariable=self._var, state='readonly', values=tuple(self.config_item.options),
                                   command=self.update_config)
        self.spinbox.pack(side=interface.LEFT)
        self.config_item.on_options_change = self.update_options

    def update_var(self):
        self._var.set(self.config_item.current_option)

    def update_config(self):
        self.config_item.current_option = self._var.get()

    def update_options(self):
        self.spinbox['values'] = tuple(self.config_item.options)


class ScaleSpinbox(ttk.Frame):
    """A Ttk Scale widget with a Ttk Spinbox indicating and allowing modification of its current value.

    The Ttk Scale can be accessed through instance.scale, and Ttk Label
    can be accessed through instance.spinbox
    also offers the possibility to add a label.
    """

    def __init__(self, master=None, from_=0, to=100, increment=1, box_width=4, on_change=interface._empty_callback, label=None, variable=None, **kw):
        """Construct a horizontal Scale with parent master, a
        variable to be associated with the Ttk Scale widget and its range.
        If variable is not specified, a tkinter.IntVar is created.
        """
        ttk.Frame.__init__(self, master, **kw)
        if variable is not None:
            self._variable = variable
        elif increment % 1 > 0:
            self._variable = tkinter.DoubleVar(master)
            self._variable.set(from_)
        else:
            self._variable = tkinter.IntVar(master)
            self._variable.set(from_)
        self.last_val = self.value
        self.label_cont = ttk.Frame(self)
        if label is not None:
            self.label = ttk.Label(self.label_cont, text=label)
            self.label.pack(side=interface.LEFT)
        self.label_cont.pack(side=interface.TOP, fill=interface.X, expand=interface.ON)
        self.scale = ttk.Scale(self, variable=self._variable, from_=from_,
                               to=to, command=self._round_scale_val, orient=interface.HORIZONTAL)
        self.spinbox = ttk.Spinbox(self, textvariable=self._variable, from_=from_,
                                   to=to, increment=increment, command=self._round_scale_val, width=box_width)
        self.spinbox.bind('<FocusOut>', self._round_scale_val)
        self.spinbox.pack(side=interface.LEFT)
        self.scale.pack(side=interface.LEFT, fill=interface.X, expand=interface.ON)
        self.increment = increment
        self.on_change = on_change

    def destroy(self):
        """Destroy this widget and possibly its associated variable."""
        del self._variable
        super().destroy()
        self.label = None
        self.scale = None
        self.spinbox = None

    @property
    def to(self):
        """Return current maximum value for scale."""
        return self.scale.cget('to')

    @to.setter
    def to(self, max):
        """Set maximum value for scale."""
        self.scale.configure(to=max)
        self.spinbox.configure(to=max)

    @property
    def from_(self):
        """Return current minimum value for scale."""
        return self.scale.cget('from')

    @from_.setter
    def from_(self, min):
        """Set minimum value for scale."""
        self.scale.configure(from_=min)
        self.spinbox.configure(from_=min)

    @property
    def value(self):
        """Return current scale value."""
        return self._variable.get()

    @value.setter
    def value(self, val):
        """Set new scale value."""
        val = round(val/self.increment) * self.increment
        self._variable.set(val)

    def _round_scale_val(self, event=None):
        self.value = self.value
        if self.last_val != self.value:
            self.last_val = self.value
            self.on_change(self.value)
