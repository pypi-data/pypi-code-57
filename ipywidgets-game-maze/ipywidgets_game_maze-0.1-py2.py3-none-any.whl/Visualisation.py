import traitlets
import ipywidgets as widgets
__version__ = '0.1'

class Visualisation(widgets.HBox):
    """
        The visualisation we give to valuePlayerWidget
    """
    value =traitlets.List()
    def __init__(self, affichage,values):
        """
            Initialization of the vizualisation
            
            Parameters
            ----------
            affichage : (type:List(widgets)) Elements to put inside the HBox
            values : (type:List) list of elements
            
        """
        self.__value=values
        widgets.HBox.__init__(self,affichage)
    
