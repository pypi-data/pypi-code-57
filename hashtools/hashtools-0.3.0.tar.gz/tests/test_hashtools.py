import unittest
import hashlib
import os
import random
import uuid
from hashtools import get_hash_generator
from hashtools import get_hash_result
from hashtools import get_file_hash
from hashtools import get_files_hash

class TestHashTools(unittest.TestCase):

    def test01(self):
        md5 = get_hash_generator("md5")
        sha1 = get_hash_generator("sha1")
        assert md5.name == "md5"
        assert sha1.name == "sha1"
        assert hasattr(md5, "update")
        assert hasattr(sha1, "update")


    def test02(self):
        md5 = get_hash_generator("md5")
        assert get_hash_result(md5, "generator") == md5
        assert get_hash_result(md5, "hex") == "d41d8cd98f00b204e9800998ecf8427e"
        assert get_hash_result(md5, "base64") == "1B2M2Y8AsgTpgAmY7PhCfg=="
        assert get_hash_result(md5, "bytes") == b'\xd4\x1d\x8c\xd9\x8f\x00\xb2\x04\xe9\x80\t\x98\xec\xf8B~'

    def test03(self):
        data = os.urandom(random.randint(0, 1024*128))
        md5 = hashlib.md5(data)
        code = md5.hexdigest()
        filename = str(uuid.uuid4())
        with open(filename, "wb") as fobj:
            fobj.write(data)
        assert get_file_hash("md5", filename) == code
        os.unlink(filename)

    def test04(self):

        data1 = os.urandom(random.randint(0, 1024*128))
        data2 = os.urandom(random.randint(0, 1024*128))
        data3 = os.urandom(random.randint(0, 1024*128))

        md5 = hashlib.md5()
        md5.update(data1)
        md5.update(data2)
        md5.update(data3)
        code = md5.hexdigest()

        filename1 = str(uuid.uuid4())
        filename2 = str(uuid.uuid4())
        filename3 = str(uuid.uuid4())

        with open(filename1, "wb") as fobj:
            fobj.write(data1)
        with open(filename2, "wb") as fobj:
            fobj.write(data2)
        with open(filename3, "wb") as fobj:
            fobj.write(data3)
    
        assert get_files_hash("md5", [filename1, filename2, filename3]) == code

        os.unlink(filename1)
        os.unlink(filename2)
        os.unlink(filename3)

