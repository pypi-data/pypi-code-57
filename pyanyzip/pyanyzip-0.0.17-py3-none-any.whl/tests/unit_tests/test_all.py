import os
import unittest

import pyanyzip.core


class TestAll(unittest.TestCase):

    def testPass(self):
        pass

    def testOpenNotExists(self):
        # python3
        # self.assertRaises(FileNotFoundError, pyanyzip.open, name="data/doesnt_exist.txt", mode="rt")
        # python2
        self.assertRaises(IOError, pyanyzip.core.open, name="data/doesnt_exist.txt", mode="rt")

    def testOpenTextFile(self):
        print(os.getcwd())
        pyanyzip.core.open(name="data/text.txt", mode="rt")
