"""
Utilities for str
"""
import uuid

"""
Dot "."
"""
DOT = "."
"""
Low bar "_"
"""
LOW_BAR = "_"


class RFUtilsStr:

    @staticmethod
    def is_not_emtpy(value):
        """
        Method to check value is not empty
        :param value: to check
        :return: True if value is not None and isinstance str and strip() != ""
        """
        return value is not None and isinstance(value, str) and value.strip() != ""

    @staticmethod
    def is_empty(value):
        """
        Method to check value is empty
        :param value: to check
        :return: True if value is None or non instance of str or value.strip() == ""
        """
        return RFUtilsStr.is_not_emtpy(value) is False

    @staticmethod
    def split(value, separator):
        """
        Method for split str
        :param value: to split
        :param separator: for apply split
        :return: data split if value is not empty and separator is not None
        """
        ar_response = None
        if RFUtilsStr.is_not_emtpy(value) and separator is not None:
            ar_response = value.split(separator)

        return ar_response

    @staticmethod
    def unique_str(time_execute: int = 1):
        """
        Method for generate unique str
        :param time_execute for exeucte concat unique str
        :return: unique str
        """
        unique = ""
        counter: int = 0

        if time_execute is None or time_execute < 0:
            time_execute = 1

        while counter < time_execute:
            counter = counter + 1
            unique = unique + uuid.uuid4().hex.upper()

        return unique

    @staticmethod
    def replace(text: str, str_find_replace: str, str_replace_find: str):
        """
        MEthod for replace ocurences in text
        :param text: to find replacementes
        :param str_find_replace: to find replace
        :param str_replace_find: to replace find
        :return: text replace if text is not empty
        """
        result = None
        if RFUtilsStr.is_not_emtpy(text):
            result = text.replace(str_find_replace, str_replace_find)
        return result

    @staticmethod
    def contains(text: str, str_find: str):
        """
        Method to check text contains data
        :param text: to check
        :param str_find: to find
        :return: True if find str False if not
        """
        result = False
        if RFUtilsStr.is_not_emtpy(text) and RFUtilsStr.is_not_emtpy(str_find):
            try:
                index = text.index(str_find)
                result = True
            except ValueError:
                pass
        return result
