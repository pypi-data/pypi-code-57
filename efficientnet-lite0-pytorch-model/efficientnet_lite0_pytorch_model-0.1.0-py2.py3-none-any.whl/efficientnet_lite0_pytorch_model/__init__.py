import os, inspect

class EfficientnetLite0ModelFile(object):

    def __init__( self ):
        pass

    @staticmethod
    def get_model_file_path():
        model_path = os.path.join( os.path.dirname(inspect.getfile( EfficientnetLite0ModelFile )), 'models' )
        return os.path.join( model_path, 'efficientnet-lite0-57934424.pth' )


'''
from efficientnet_lite0_pytorch_model import EfficientnetLite0ModelFile
print( 'model file path is %s' % ( EfficientnetLite0ModelFile.get_model_file_path() ) )
'''
