"""
Utilities for built
"""
from rfpyutils.str.rf_utils_str import RFUtilsStr


class RFUtilsBuilt:

    @staticmethod
    def has_attr(object_attr, attr):
        """
        Method to know has attr
        :param object_attr: to check if has attr
        :param attr: to check
        :return: True if object_attr is not None and not empty attr and hasattr
        """
        return object_attr is not None and RFUtilsStr.is_not_emtpy(attr) and hasattr(object_attr, attr)

    @staticmethod
    def get_attr(object_attr, attr):
        """
        Method for get attr for object
        :param object_attr: to get attr
        :param attr: to get
        :return: attr if find else return None
        """
        result = None
        if RFUtilsBuilt.has_attr(object_attr, attr):
            result = getattr(object_attr, attr)
            
        return result

    @staticmethod
    def set_attr(object_attr, attr, value_to_set):
        """
        Method for set attr
        :param object_attr: to set attr
        :param attr: to set value
        :param value_to_set:
        :return: True if set attr False if not
        """
        result = False
        if RFUtilsBuilt.has_attr(object_attr, attr):
            setattr(object_attr, attr, value_to_set)
            result = True
        return result
