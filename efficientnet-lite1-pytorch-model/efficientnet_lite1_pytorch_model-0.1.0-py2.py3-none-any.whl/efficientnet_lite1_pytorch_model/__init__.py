# Version of the efficientnet_lite1_pytorch_model package
__version__ = "0.1.0"

import os, inspect

class EfficientnetLite1ModelFile(object):

    def __init__( self ):
        pass

    @staticmethod
    def get_model_file_path():
        model_path = os.path.join( os.path.dirname(inspect.getfile( EfficientnetLite1ModelFile )), 'models' )
        return os.path.join( model_path, 'efficientnet-lite1-77cc7160.pth' )


'''
from efficientnet_lite1_pytorch_model import EfficientnetLite1ModelFile
print( 'model file path is %s' % ( EfficientnetLite1ModelFile.get_model_file_path() ) )
'''
