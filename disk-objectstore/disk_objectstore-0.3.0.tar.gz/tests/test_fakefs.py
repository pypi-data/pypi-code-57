import errno
import os
import pytest

## Note: you need to install pyfakefs==4.0.2 to make the 'fs' fixture available

def test_fakefs(fs):  # pytest: disable=invalid-name
    # "fs" is the reference to the fake file system
    fs.set_disk_usage(100) # bytes
    fname = '/var/data/xx1.txt'
    fs.create_file(fname)
    assert os.path.exists(fname)
    with open(fname, 'w') as fhandle:
        fhandle.write("a" * 80)

    with pytest.raises(OSError) as excinfo:
        with open(fname, 'w') as fhandle:
            fhandle.write("a" * 120)

    print(dir(excinfo))
    assert excinfo.value.errno == errno.ENOSPC
