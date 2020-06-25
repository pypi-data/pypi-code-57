import pytest
from easy_publish import utils

def test_listdir_fullpath():
    # Test different paths and ensure utils function handles them properly
    a = utils.listdir_fullpath("/etc")
    b = utils.listdir_fullpath("~")
    c = utils.listdir_fullpath("./tests/fakenotes")
    assert len(a) > 5
    assert len(b) > 5
    assert len(c) > 2

def test_bad_listdir_fullpath():
    with pytest.raises(FileNotFoundError):
        utils.listdir_fullpath("kfjskjflkds")

def test_array_splitter():
    pass

