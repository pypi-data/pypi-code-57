"""Base Nosql abstract class container"""
from abc import ABC, abstractmethod

__author__ = 'ozgur'
__creation_date__ = '9.09.2019' '14:12'

from typing import Union, Dict, Any, List, Optional


class BaseNosqlConnector(ABC):
    """Base Nosql connector Class"""

    def __init__(self):
        self.tagprefix = "tag:"

    @abstractmethod
    def delete_table(self):
        """
        deletes table from db\n
        :return:
        """

    @abstractmethod
    def create_table(self):
        """
        creates a new table, delete first if exists \n
        :return:
        """

    @abstractmethod
    def dbsize(self) -> int:
        """
        returns the itemcount in db\n
        :return: item count
        """

    @abstractmethod
    def keys(self, pattern='*') -> List[str]:
        """
        returns keys list in db \n
        :param pattern: str urlpathregex
        :return: the keys in db
        """

    @abstractmethod
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        get value by key\n
        :param key: str
        :return: dict or None
        """

    @abstractmethod
    def get_multi(self, keylist: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        get dictionaries by keylist\n
        :param keylist: list of strings
        :return: [objectdict]
        """

    @abstractmethod
    def get_all_as_list(self) -> List[Optional[Dict[str, Any]]]:
        """
        get all values in store \n
        :return: list
        """

    @abstractmethod
    def get_all_as_dict(self) -> Dict[str, Optional[Dict[str, Any]]]:
        """
        get all values in store \n
        :return: dict
        """

    @abstractmethod
    def upsert(self, key: str, value: Dict[str, Any]) -> bool:
        """
        get all values in store \n
        :return: list
        """

    @abstractmethod
    def upsert_multi(self, itemdict: Dict[str, Dict[str, Any]]):
        """
        upsert multiple items at once\n
        :param itemdict: dict of objects dictionaries
        :return: None
        """

    @abstractmethod
    def remove(self, key: str) -> bool:
        """
        removes the key from store\n
        :param key: str or list or tuple
        :return:
        """

    @abstractmethod
    def remove_keys(self, keys: List[str]) -> bool:
        """
        removes the key from store\n
        :param keys:
        :return:
        """

    @abstractmethod
    def flush(self):
        """
        Flushes current store\n
        :return: None
        """

    @abstractmethod
    def tags(self) -> List[str]:
        """
        returns tag list \n
        :return:
        """

    @abstractmethod
    def gettagkeys(self, tag: str) -> List[str]:
        """
        get all keys of given tag \n
        :param tag:
        :return:
        """

    @abstractmethod
    def gettag(self, tag: str) -> List[Optional[Dict[str, Any]]]:
        """
        get all dict items in given tag \n
        :param tag:
        :return: list of dictionaries
        """

    @abstractmethod
    def addtag(self, tag: str, key: str):
        """
        Adds tags to keys \n
        :param tag: list
        :param key: list
        :return: None
        """

    @abstractmethod
    def removefromtag(self, tag: str, key: Union[str, list]):
        """
        Remove items from lists \n
        :param tag: str
        :param key: str or list
        :return: None
        """
