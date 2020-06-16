import traitlets
import ipywidgets as widgets

class Visua(widgets.HBox):
    """ A class to give a visualisation to ValuePlayerWidget """
    value =traitlets.List()
    #value = traitlets.Tuple()
    def __init__(self, display,dynamic=[]):
        self.__value=dynamic
        widgets.HBox.__init__(self,display)
    