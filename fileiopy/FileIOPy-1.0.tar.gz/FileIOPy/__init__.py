import os
import shutil


class IncorrectModeError(Exception):
    """Raised when anyone enters incorrect mode"""


class IncorrectLineNoError(Exception):
    """Raised when anyone enters -1, -2... no"""


def make_file(name='Untitled'):
    open(f'{name}', 'w').close()


def delete_file(__path):
    os.remove(__path)


class FileIOPy:

    def __init__(self, __file_path):
        self.__file_path = __file_path

    def write_file(self, __content, __mode):

        """
        Using this Function, You can write any content in your file
        you can write your content in two types:
        : write mode
            if you choose write mode, first your file data will clear and
            then you can write your content
        : Continue mode
            if you choose continue mode, you can write your content without
            losing any data
        """

        if __mode == 'w':
            __file = open(f'{self.__file_path}', 'w')
            __file.write(__content)
            __file.close()
            if __file.closed:
                pass
            else:
                __file.close()

        elif __mode == 'c':
            __file = open(f'{self.__file_path}', 'a')
            __file.write(__content)
            if __file.closed:
                pass
            else:
                __file.close()

        else:
            raise IncorrectModeError(f"incorrect mode '{__mode}'")

    def read_file(self):
        """
        Using this function, you read your file data
        """
        __file = open(self.__file_path)
        __content = __file.read()
        if __file.closed:
            pass
        else:
            __file.close()
        return __content

    def read_lines(self, lines=0):
        """
        Read files line by line
        """
        __file = open(self.__file_path)

        if lines == 0:
            __content = __file.readlines()
            __file.close()
            return __content

        elif lines < 0:
            __file.close()
            raise IncorrectLineNoError(f"Incorrect line no '{lines}'")

        else:
            __content = __file.readlines()
            __file.close()
            return __content

    def clear_file(self):
        """
        Clears the all data of the file
        """
        __file = open(self.__file_path, 'w')
        if __file.closed:
            pass
        else:
            __file.close()

    def check_length(self):
        """
        Check how many alphabates in your file have
        """
        __file = open(self.__file_path)
        __content = __file.read()
        __file.close()
        __length = len(__content)
        return __length

    @property
    def file_name(self):
        """
        Returns your file name
        """
        return self.__file_path

    @property
    def file_encoding(self):
        """
        Returns your file encoding
        """
        __file = open(self.__file_path)
        __encoding = __file.encoding
        return __encoding


    def check_lines(self):
        """
        Checks how many lines in your file have
        """
        __file = open(self.__file_path)
        __content = __file.readlines()
        __file.close()
        __lines = 0
        for content in __content:
            __lines += 1
        return __lines

    def blank_lines(self):
        """
        Checks how many blank lines in your file have
        """
        __file = open(self.__file_path)
        __lines = __file.readlines()
        __file.close()
        __blank = 0
        for i in __lines:
            if i == '\n':
                __blank += 1
            else:
                pass
        return __blank

    def search_file(self, __content):
        """
        Returns True if entered content exists in your file
        """
        __file = open(self.__file_path)
        __readed_content = __file.read()
        __file.close()
        if __content in __readed_content:
            return True
        else:
            return False

    def count_file(self, __content):
        """
        returns how many times your content exists in your file
        """
        __file = open(self.__file_path)
        __readed_content = __file.read()
        __file.close()
        return __readed_content.count(__content)

    def move_file(self, __path):
        """
        Move your file to another directory
        """
        shutil.move(self.__file_path, __path)

    def copy_file(self, __path):
        """
        Copy Your file to another directory
        """
        shutil.copyfile(self.__file_path, __path)


    def __len__(self):
        """
        Check how many alphatbates in your file have
        """
        __file = open(self.__file_path)
        __content = __file.read()
        __length = len(__content)
        return __length
