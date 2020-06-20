import pytest
import os

from efficientnet_lite0_pytorch_model import EfficientnetLite0ModelFile

def test_get_model_path():
    model_file_path = EfficientnetLite0ModelFile.get_model_file_path()

    assert os.path.exists( model_file_path ), 'Model file path does not exist!'
                
