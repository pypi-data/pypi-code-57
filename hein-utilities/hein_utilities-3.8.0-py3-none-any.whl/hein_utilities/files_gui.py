"""deprecated modules which have been moved to the hein_gui_utilities repository"""
import warnings

warnings.warn('This module has been moved to the hein_gui_utilities repo. Install the hein_utilities_gui '
              'package and look under hein_gui_utilities.files_gui for this class',
              DeprecationWarning)

class Component:
    def __init__(self,
                 name: str,
                 path: str,
                 ):
        raise NotImplementedError('This class has been moved to the hein_gui_utilities repo. Install the '
                                  'hein_utilities_gui '
                                  'package and look under hein_gui_utilities.files_gui for this class')



class Folder(Component):
    def __init__(self,
                 folder_name: str,
                 folder_path: str,
                 ):
        raise NotImplementedError('This class has been moved to the hein_gui_utilities repo. '
                                  'Install the hein_utilities_gui '
                                  'package and look under hein_gui_utilities.files_gui for this class')

