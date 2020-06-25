import abc
import os

TEMP_SUFFIX = "_temp.txt"


def get_extension(filename: str) -> str:
    extension = -1
    return os.path.splitext(filename)[extension]


def get_base_name(filename: str) -> str:
    basename = 0
    return os.path.splitext(filename)[basename]


class AbstractFile(abc.ABC):

    @abc.abstractmethod
    def open(self):
        """
        Define the mode to open the file based in its extension.
        :return: text file object
        """
        ...

    @abc.abstractmethod
    def close(self) -> None:
        """
            Just close the file on a security way.
        :return: None
        """
        ...

    @abc.abstractmethod
    def content(self) -> str:
        """
            Return string that represents all text file
        :return:
        """
        ...


class Pdf(AbstractFile):

    def __init__(self, file_path):
        self._file_path = file_path
        self._file = None

    def open(self):
        from .tools import convert_pdf_to_txt
        text = convert_pdf_to_txt(self._file_path)
        self._file = open(get_base_name(self._file_path) + TEMP_SUFFIX, mode='w+', encoding='utf-8', errors='ignore')
        self._file.write(text)
        self._file.seek(0)
        return self._file

    def close(self):
        file_path = self._file.name
        self._file.close()
        os.remove(file_path)

    def content(self) -> str:
        from .tools import convert_pdf_to_txt
        return convert_pdf_to_txt(self._file_path)


class Txt(AbstractFile):

    def __init__(self, file_path):
        self._file_path = file_path
        self._file = None

    def open(self):
        self._file = open(self._file_path, mode='r', encoding='utf-8', errors='ignore')
        return self._file

    def close(self):
        self._file.close()

    def content(self) -> str:
        f = open(self._file_path, mode='r', encoding='utf-8', errors='ignore')
        content = f.read()
        f.close()
        return content
