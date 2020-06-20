import pytest
import os

from efficientnet_lite2_pytorch_model import EfficientnetLite2ModelFile

def test_get_model_path():
    model_file_path = EfficientnetLite2ModelFile.get_model_file_path()

    assert os.path.exists( model_file_path ), 'Model file path does not exist!'
                
