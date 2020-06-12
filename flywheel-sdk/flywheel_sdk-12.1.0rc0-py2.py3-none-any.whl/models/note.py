# coding: utf-8

"""
    Flywheel

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 12.1.0-rc.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


## NOTE: This file is auto generated by the swagger code generator program.
## Do not edit the file manually.

import pprint
import re  # noqa: F401

import six

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.


class Note(object):

    swagger_types = {
        'text': 'str',
        'id': 'str',
        'created': 'datetime',
        'modified': 'datetime',
        'user': 'str'
    }

    attribute_map = {
        'text': 'text',
        'id': '_id',
        'created': 'created',
        'modified': 'modified',
        'user': 'user'
    }

    rattribute_map = {
        'text': 'text',
        '_id': 'id',
        'created': 'created',
        'modified': 'modified',
        'user': 'user'
    }

    def __init__(self, text=None, id=None, created=None, modified=None, user=None):  # noqa: E501
        """Note - a model defined in Swagger"""
        super(Note, self).__init__()

        self._text = None
        self._id = None
        self._created = None
        self._modified = None
        self._user = None
        self.discriminator = None
        self.alt_discriminator = None

        if text is not None:
            self.text = text
        if id is not None:
            self.id = id
        if created is not None:
            self.created = created
        if modified is not None:
            self.modified = modified
        if user is not None:
            self.user = user

    @property
    def text(self):
        """Gets the text of this Note.

        The actual contents of the note

        :return: The text of this Note.
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, text):
        """Sets the text of this Note.

        The actual contents of the note

        :param text: The text of this Note.  # noqa: E501
        :type: str
        """

        self._text = text

    @property
    def id(self):
        """Gets the id of this Note.

        Unique database ID

        :return: The id of this Note.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Note.

        Unique database ID

        :param id: The id of this Note.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def created(self):
        """Gets the created of this Note.

        Creation time (automatically set)

        :return: The created of this Note.
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this Note.

        Creation time (automatically set)

        :param created: The created of this Note.  # noqa: E501
        :type: datetime
        """

        self._created = created

    @property
    def modified(self):
        """Gets the modified of this Note.

        Last modification time (automatically updated)

        :return: The modified of this Note.
        :rtype: datetime
        """
        return self._modified

    @modified.setter
    def modified(self, modified):
        """Sets the modified of this Note.

        Last modification time (automatically updated)

        :param modified: The modified of this Note.  # noqa: E501
        :type: datetime
        """

        self._modified = modified

    @property
    def user(self):
        """Gets the user of this Note.

        Database ID of a user

        :return: The user of this Note.
        :rtype: str
        """
        return self._user

    @user.setter
    def user(self, user):
        """Sets the user of this Note.

        Database ID of a user

        :param user: The user of this Note.  # noqa: E501
        :type: str
        """

        self._user = user


    @staticmethod
    def positional_to_model(value):
        """Converts a positional argument to a model value"""
        if isinstance(value, (list, dict, Note)):
            return value
        return Note(text=value)

    def return_value(self):
        """Unwraps return value from model"""
        return self

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Note):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

    # Container emulation
    def __getitem__(self, key):
        """Returns the value of key"""
        key = self._map_key(key)
        return getattr(self, key)

    def __setitem__(self, key, value):
        """Sets the value of key"""
        key = self._map_key(key)
        setattr(self, key, value)

    def __contains__(self, key):
        """Checks if the given value is a key in this object"""
        key = self._map_key(key, raise_on_error=False)
        return key is not None

    def keys(self):
        """Returns the list of json properties in the object"""
        return self.__class__.rattribute_map.keys()

    def values(self):
        """Returns the list of values in the object"""
        for key in self.__class__.attribute_map.keys():
            yield getattr(self, key)

    def items(self):
        """Returns the list of json property to value mapping"""
        for key, prop in self.__class__.rattribute_map.items():
            yield key, getattr(self, prop)

    def get(self, key, default=None):
        """Get the value of the provided json property, or default"""
        key = self._map_key(key, raise_on_error=False)
        if key:
            return getattr(self, key, default)
        return default

    def _map_key(self, key, raise_on_error=True):
        result = self.__class__.rattribute_map.get(key)
        if result is None:
            if raise_on_error:
                raise AttributeError('Invalid attribute name: {}'.format(key))
            return None
        return '_' + result
