"""
    Describes the data structure of IR models design.
"""
from os import path, listdir
from typing import List, DefaultDict, Set

from matchup.structure.occurrence import Occurrence
from matchup.structure.weighting.idf import IDF
from matchup.structure.weighting.tf import TF

from matchup.structure.index.inverted_index import InvertedIndex

from matchup.presentation.sanitizer import Sanitizer


LIB_PATH = path.abspath("./static/lib")
SAVED_FILE_NAME = 'collection.bin'


class Vocabulary:
    """
        Crucial data structure that represents and storage all text processing.
    """

    def __init__(self, save, **kwargs):
        """
        :param response: Path to save processed Vocabulary
        :param kwargs: only accepts 'stopwords', with the stopwords file path
        """
        self._index = InvertedIndex() if kwargs.get('indexer') is None else kwargs.get('indexer')

        self._idf = None
        self._tf = None
        self._path = self.__make_prefix(save) + f"/{SAVED_FILE_NAME}"
        self._sanitizer = self.__make_sanitizer(**kwargs)

        self.file_names = set()

    def import_file(self, file_path: str) -> bool:
        """
            Given a file path of a document, this function append this document into some structure, case the path are
            correct. The processing of this file can be started running function index_files()

        :param file_path: string that represents a relative or absolute path of an txt file
        :return: boolean flag that indicates if the file has been identified
        """
        if path.exists(file_path):
            self.file_names.add(file_path)
            return True
        return False

    def import_folder(self, folder_path: str) -> bool:
        """
            Generalization of import_file(). This function receive a folder path and try to append all documents of
            this folder into some structure. he processing of all this file can be started running function
             index_files()

        :param folder_path: string that represents a relative or absolute path of an folder
        :return: boolean flag that indicates if the folder has been identified
        """
        if path.isdir(folder_path):
            list_dir = filter(lambda x: f'{SAVED_FILE_NAME}' not in x, listdir(folder_path))
            for filename in list_dir:
                self.import_file(folder_path + "/" + filename)
            return True
        raise FileNotFoundError

    def generate_idf(self):
        self._idf.generate(self)

    @property
    def idf(self) -> IDF:
        """
            Get the data structure that represents the IDF weighting
        :return: IDF object
        """
        return self._idf

    @idf.setter
    def idf(self, idf: IDF) -> None:
        """
            This function just calculate IDF of all keywords on vocabulary
        :return: None
        """
        self._idf = idf
        self._idf.generate(self)

    @property
    def tf(self) -> TF:
        """
            Get the data structure that represents the TF weighting
        :return: TF object
        """
        return self._tf

    @tf.setter
    def tf(self, tf: TF) -> None:
        """
            Set the data structure that represents the TF weighting
        :param tf: TF Object
        :return: None
        """
        self._tf = tf

    @property
    def sanitizer(self) -> "Sanitizer":
        """
            Sanitizer property getter
        :return:
        """
        return self._sanitizer

    def import_collection(self) -> bool:
        """
            This is a function that recover the vocabulary previously generated.
        :return: boolean flag that indicates success or failure in case the vocabulary has no generated yet.
        """
        files = self._index.load(path=self._path)
        if files:
            self.file_names = files
            return True
        return False

    def index_files(self) -> None:
        """
            This function try to process all content of files that have been inserted before, generating
            the vocabulary data structure ready for use.
        :return: None
        """
        self._index.process(self.file_names, sanitizer=self._sanitizer)

    def save(self) -> bool:
        """
            Persist data structure on disc.
        :return: boolean flag that indicates if the data structure can be persisted.
        """
        return self._index.save(path=self._path)

    def maximum_frequencies_per_document(self) -> DefaultDict[str, float]:
        return self._index.maximum_frequencies_per_document()

    def documents_with_keywords(self, kwds: Set[str]) -> Set[str]:
        return self._index.documents_with_keywords(kwds)

    @property
    def keys(self) -> List[str]:
        """
            Get all keywords presents in vocabulary
        :return: list of all keywords
        """
        return self._index.keys

    def __str__(self) -> str:
        """
            Transform an Vocabulary object in an String
        :return: String that represents the structure of vocabulary
        """
        return str(self._index)

    def __contains__(self, item: str) -> bool:
        """
            This function enables the user to make the associative operation with 'in'
        :param item: keyword
        :return: boolean flag that return true if the keyword are in vocabulary
        """
        return item in self._index

    def __getitem__(self, item: str) -> List[Occurrence]:
        """
            Get some vocabulary occurrences by item, or initialize it on data structure
        :param item: keyword
        :return: Occurrences of keyword
        """
        return self._index[item]

    @classmethod
    def __make_sanitizer(cls, **kwargs) -> Sanitizer:
        """
            Function that allows the Sanitizer initialization
        :param kwargs: expected: stopwords named param with the stopwords text file path
        :return:
        """
        stopwords = kwargs.get("stopwords")
        stemming = kwargs.get("stemming") if kwargs.get("stemming") else False
        if stopwords:
            return Sanitizer(stopwords_path=stopwords, stemming=stemming)
        else:
            return Sanitizer(stemming=stemming)

    @classmethod
    def __make_prefix(cls, save):
        """
            Function that build the path to save the create_collection
        :param save: path to save
        :return:
        """
        return save if save else LIB_PATH
