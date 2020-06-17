import os
import sys
import logging
import text_clean.text_clean as text_clean

dependent_files = [
    "t2s_char_project.txt",
    "t2s_drop_project.txt",
    "t2s_word_project.txt",
    "digital_letter_normal.txt",
    "char_keep.txt"
]


logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    stream=sys.stdout)


class TextClean(object):
    def __init__(self, a=True, b=True, c=False, update=False):
        data_path = os.path.dirname(
            sys.modules[__package__].__file__) + "/data"
        text_clean.init(data_path, a, b, c)
        logging.info("Successfully loaded the default dictionary.")

    def clean(self, text, dign=False):
        try:
            res = text_clean.clean(text, dign)
        except:
            res = text_clean.clean(text.replace('\x00', ''), dign)
        finally:
            return res


__all__ = ["TextClean"]
