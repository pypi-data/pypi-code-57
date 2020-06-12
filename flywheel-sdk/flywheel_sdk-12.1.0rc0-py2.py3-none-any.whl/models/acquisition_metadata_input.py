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

from flywheel.models.file_entry import FileEntry  # noqa: F401,E501

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.


class AcquisitionMetadataInput(object):

    swagger_types = {
        'label': 'str',
        'info': 'object',
        'metadata': 'object',
        'measurement': 'str',
        'instrument': 'str',
        'uid': 'str',
        'tags': 'list[str]',
        'timestamp': 'datetime',
        'timezone': 'str',
        'files': 'list[FileEntry]'
    }

    attribute_map = {
        'label': 'label',
        'info': 'info',
        'metadata': 'metadata',
        'measurement': 'measurement',
        'instrument': 'instrument',
        'uid': 'uid',
        'tags': 'tags',
        'timestamp': 'timestamp',
        'timezone': 'timezone',
        'files': 'files'
    }

    rattribute_map = {
        'label': 'label',
        'info': 'info',
        'metadata': 'metadata',
        'measurement': 'measurement',
        'instrument': 'instrument',
        'uid': 'uid',
        'tags': 'tags',
        'timestamp': 'timestamp',
        'timezone': 'timezone',
        'files': 'files'
    }

    def __init__(self, label=None, info=None, metadata=None, measurement=None, instrument=None, uid=None, tags=None, timestamp=None, timezone=None, files=None):  # noqa: E501
        """AcquisitionMetadataInput - a model defined in Swagger"""
        super(AcquisitionMetadataInput, self).__init__()

        self._label = None
        self._info = None
        self._metadata = None
        self._measurement = None
        self._instrument = None
        self._uid = None
        self._tags = None
        self._timestamp = None
        self._timezone = None
        self._files = None
        self.discriminator = None
        self.alt_discriminator = None

        if label is not None:
            self.label = label
        if info is not None:
            self.info = info
        if metadata is not None:
            self.metadata = metadata
        if measurement is not None:
            self.measurement = measurement
        if instrument is not None:
            self.instrument = instrument
        if uid is not None:
            self.uid = uid
        if tags is not None:
            self.tags = tags
        if timestamp is not None:
            self.timestamp = timestamp
        if timezone is not None:
            self.timezone = timezone
        if files is not None:
            self.files = files

    @property
    def label(self):
        """Gets the label of this AcquisitionMetadataInput.


        :return: The label of this AcquisitionMetadataInput.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this AcquisitionMetadataInput.


        :param label: The label of this AcquisitionMetadataInput.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def info(self):
        """Gets the info of this AcquisitionMetadataInput.


        :return: The info of this AcquisitionMetadataInput.
        :rtype: object
        """
        return self._info

    @info.setter
    def info(self, info):
        """Sets the info of this AcquisitionMetadataInput.


        :param info: The info of this AcquisitionMetadataInput.  # noqa: E501
        :type: object
        """

        self._info = info

    @property
    def metadata(self):
        """Gets the metadata of this AcquisitionMetadataInput.


        :return: The metadata of this AcquisitionMetadataInput.
        :rtype: object
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this AcquisitionMetadataInput.


        :param metadata: The metadata of this AcquisitionMetadataInput.  # noqa: E501
        :type: object
        """

        self._metadata = metadata

    @property
    def measurement(self):
        """Gets the measurement of this AcquisitionMetadataInput.


        :return: The measurement of this AcquisitionMetadataInput.
        :rtype: str
        """
        return self._measurement

    @measurement.setter
    def measurement(self, measurement):
        """Sets the measurement of this AcquisitionMetadataInput.


        :param measurement: The measurement of this AcquisitionMetadataInput.  # noqa: E501
        :type: str
        """

        self._measurement = measurement

    @property
    def instrument(self):
        """Gets the instrument of this AcquisitionMetadataInput.


        :return: The instrument of this AcquisitionMetadataInput.
        :rtype: str
        """
        return self._instrument

    @instrument.setter
    def instrument(self, instrument):
        """Sets the instrument of this AcquisitionMetadataInput.


        :param instrument: The instrument of this AcquisitionMetadataInput.  # noqa: E501
        :type: str
        """

        self._instrument = instrument

    @property
    def uid(self):
        """Gets the uid of this AcquisitionMetadataInput.


        :return: The uid of this AcquisitionMetadataInput.
        :rtype: str
        """
        return self._uid

    @uid.setter
    def uid(self, uid):
        """Sets the uid of this AcquisitionMetadataInput.


        :param uid: The uid of this AcquisitionMetadataInput.  # noqa: E501
        :type: str
        """

        self._uid = uid

    @property
    def tags(self):
        """Gets the tags of this AcquisitionMetadataInput.

        Array of application-specific tags

        :return: The tags of this AcquisitionMetadataInput.
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this AcquisitionMetadataInput.

        Array of application-specific tags

        :param tags: The tags of this AcquisitionMetadataInput.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def timestamp(self):
        """Gets the timestamp of this AcquisitionMetadataInput.


        :return: The timestamp of this AcquisitionMetadataInput.
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this AcquisitionMetadataInput.


        :param timestamp: The timestamp of this AcquisitionMetadataInput.  # noqa: E501
        :type: datetime
        """

        self._timestamp = timestamp

    @property
    def timezone(self):
        """Gets the timezone of this AcquisitionMetadataInput.


        :return: The timezone of this AcquisitionMetadataInput.
        :rtype: str
        """
        return self._timezone

    @timezone.setter
    def timezone(self, timezone):
        """Sets the timezone of this AcquisitionMetadataInput.


        :param timezone: The timezone of this AcquisitionMetadataInput.  # noqa: E501
        :type: str
        """

        self._timezone = timezone

    @property
    def files(self):
        """Gets the files of this AcquisitionMetadataInput.


        :return: The files of this AcquisitionMetadataInput.
        :rtype: list[FileEntry]
        """
        return self._files

    @files.setter
    def files(self, files):
        """Sets the files of this AcquisitionMetadataInput.


        :param files: The files of this AcquisitionMetadataInput.  # noqa: E501
        :type: list[FileEntry]
        """

        self._files = files


    @staticmethod
    def positional_to_model(value):
        """Converts a positional argument to a model value"""
        return value

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
        if not isinstance(other, AcquisitionMetadataInput):
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
