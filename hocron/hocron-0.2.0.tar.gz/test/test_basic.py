import os
import unittest

from hocron import Hocron

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_DIR = os.path.join(
    BASE_DIR, "data"
)


def get_file_path(category, filename):
    return os.path.join(DATA_DIR, category, filename)


def get_hocr(category, filename):
    hocr = Hocron(
        get_file_path(category, filename)
    )
    return hocr


class TestBasic(unittest.TestCase):

    def test_first_word_lidl_1(self):

        hocr = get_hocr("lidl-receipts", "lidl-1.hocr")
        word = hocr.first_word

        self.assertTrue(word)
        self.assertRegex(word, 'L.D.$')

    def test_first_word_lidl_2(self):

        hocr = get_hocr("lidl-receipts", "lidl-2.hocr")
        word = hocr.first_word

        self.assertTrue(word)
        self.assertRegex(word, 'L.D.$')

    def test_first_word_lidl_3(self):

        hocr = get_hocr("lidl-receipts", "lidl-3.hocr")
        word = hocr.first_word

        self.assertTrue(word)
        self.assertRegex(word, 'L.D.$')
