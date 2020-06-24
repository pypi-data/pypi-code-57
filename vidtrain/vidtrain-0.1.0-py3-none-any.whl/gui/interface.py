import abc
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from ..datahandler import interface as data_interface

# Booleans
NO = FALSE = OFF = 0
YES = TRUE = ON = 1

# -fill
NONE = 'none'
X = 'x'
Y = 'y'
BOTH = 'both'

# -side
LEFT = 'left'
TOP = 'top'
RIGHT = 'right'
BOTTOM = 'bottom'

# -orient
HORIZONTAL = 'horizontal'
VERTICAL = 'vertical'


def _empty_callback(event=None):
    pass


class RootWindow(metaclass=abc.ABCMeta):
    '''Create an application window'''

    @abc.abstractmethod
    def run(self):
        '''Run the application'''


class Element(metaclass=abc.ABCMeta):
    '''any gui element needs to specify a master'''
    @abc.abstractmethod
    def __init__(self, master):
        '''initialize the panel and define its master container'''

    @abc.abstractmethod
    def show(self, side=LEFT, fill=NONE, expand=OFF, padx=0, pady=0):
        '''show the element'''

    @abc.abstractmethod
    def hide(self):
        '''hide the element'''

    @abc.abstractmethod
    def destroy(self):
        '''destroy the element'''


class Panel(Element):
    '''A user interface container for other elements'''

    @abc.abstractmethod
    def add_label(self, text, side=TOP, fill=NONE, expand=OFF):
        '''add a label to the panel'''

    @abc.abstractmethod
    def edit_label(self, text):
        '''edit the label text'''


class FigurePanel(Panel):
    '''Panel object that contains an interactive matplotlib.pyplot figure'''
    @abc.abstractmethod
    def __init__(self, master: Panel, fig: plt.Figure, toolbar=True, **kw):
        '''initialize FigurePanel
        Arguments: 
        master: Panel into which figure will be placed
        fig: pyplot Figure object 
        toolbar (optional): bool enable or disable the pyplot navigation toolbar (default true)
        '''

    @abc.abstractmethod
    def update(self):
        '''refresh the figure'''

    @abc.abstractmethod
    def add_mouse(self, press_callback=None, drag_callback=None, release_callback=None):
        '''add mouse event callback handler to the matplotlib figure
        Arguments:
        press_callback (optional): function handle executed on mouse button press
        drag_callback (optional): function handle executed on mouse drag (with button pressed)
        release_callback (optional): function handle executed on mouse button release
        '''

    @abc.abstractmethod
    def destroy(self):
        '''close figure and call super().destroy()'''


class ImagePanel(FigurePanel):
    '''Panel object that contains an interactive matplotlib.pyplot figure'''

    @abc.abstractmethod
    def __init__(self, master: Panel, image: np.ndarray, toolbar=True, **kw):
        '''initialize ImagePanel
        Arguments: 
        master: Panel into which figure will be placed
        image: numpy ndarray 
        toolbar (optional): bool enable or disable the pyplot navigation toolbar (default true)
        '''

    @abc.abstractmethod
    def update(self, image=None):
        '''refresh the figure
        Arguments:
        image (optional): np.ndarray replaces the image data 
        '''


class RotatableImagePanel(ImagePanel, data_interface.Rotatable):
    '''StackPanel that also implements data_interface.Rotatable'''

    @abc.abstractmethod
    def add_controls(self, master=None):
        '''add rotation controls
        Arguments:
        master: Panel to which the controls should be added
        '''


class StackPanel(ImagePanel):
    '''StackPanel object that contains controls to show several frames of an image stack'''

    @property
    def frame(self):
        '''int: current frame'''

    @property
    def on_frame_change(self):
        '''callable: callback that is executed once the frame changes'''


class ConfigElement(metaclass=abc.ABCMeta):
    pass


class ConfigPanel(Panel):
    '''create a panel element that contains a configuration GUI'''

    @abc.abstractmethod
    def add_item(self, item: data_interface.ConfigItem):
        '''Add a config item'''


class Filedialog(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def ask_open(self, filetypes):
        '''Open a filedialog and return the path to a file.

        Arguments:
        filetypes: 2d tuple of strings describing the allowed file types 
                   (('description', '*.ext'))

        Returns:
        string: path to file
        '''

    @abc.abstractmethod
    def ask_save(self, filetypes):
        '''Open a filedialog and return the path to a file.

        Arguments:
        filetypes: 2d tuple of strings describing the allowed file types 
                   (('description', '*.ext'))

        Returns:
        string: path to file
        '''

    @abc.abstractmethod
    def ask_directory(self):
        '''open a directory'''


class Dialogs(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, title=None):
        '''set the title for dialogs during initialization'''

    @abc.abstractmethod
    def info(self, message):
        '''Opens a info message dialog with an ok button'''

    @abc.abstractmethod
    def yes_no(self, message):
        '''Opens a yes/no message dialog'''


class Button(Element):
    '''an interactive button'''

    @property
    @abc.abstractmethod
    def on_click(self):
        '''callback function that is executed when the button is clicked'''
