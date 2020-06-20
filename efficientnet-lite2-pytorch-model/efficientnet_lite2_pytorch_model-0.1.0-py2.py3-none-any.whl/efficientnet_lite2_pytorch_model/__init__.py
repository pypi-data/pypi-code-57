# Version of the efficientnet_lite2_pytorch_model package
__version__ = "0.1.0"

import os, inspect

class EfficientnetLite2ModelFile(object):

    def __init__( self ):
        pass

    @staticmethod
    def get_model_file_path():
        model_path = os.path.join( os.path.dirname(inspect.getfile( EfficientnetLite2ModelFile )), 'models' )
        return os.path.join( model_path, 'efficientnet-lite2-9656183e.pth' )


'''
from efficientnet_lite2_pytorch_model import EfficientnetLite2ModelFile
print( 'model file path is %s' % ( EfficientnetLite2ModelFile.get_model_file_path() ) )
'''
