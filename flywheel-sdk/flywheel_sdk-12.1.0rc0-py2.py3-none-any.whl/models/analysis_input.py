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

from flywheel.models.common_info import CommonInfo  # noqa: F401,E501
from flywheel.models.file_reference import FileReference  # noqa: F401,E501
from flywheel.models.job import Job  # noqa: F401,E501

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.


class AnalysisInput(object):

    swagger_types = {
        'inputs': 'list[FileReference]',
        'description': 'str',
        'info': 'CommonInfo',
        'label': 'str',
        'job': 'Job',
        'compute_provider_id': 'str'
    }

    attribute_map = {
        'inputs': 'inputs',
        'description': 'description',
        'info': 'info',
        'label': 'label',
        'job': 'job',
        'compute_provider_id': 'compute_provider_id'
    }

    rattribute_map = {
        'inputs': 'inputs',
        'description': 'description',
        'info': 'info',
        'label': 'label',
        'job': 'job',
        'compute_provider_id': 'compute_provider_id'
    }

    def __init__(self, inputs=None, description=None, info=None, label=None, job=None, compute_provider_id=None):  # noqa: E501
        """AnalysisInput - a model defined in Swagger"""
        super(AnalysisInput, self).__init__()

        self._inputs = None
        self._description = None
        self._info = None
        self._label = None
        self._job = None
        self._compute_provider_id = None
        self.discriminator = None
        self.alt_discriminator = None

        if inputs is not None:
            self.inputs = inputs
        if description is not None:
            self.description = description
        if info is not None:
            self.info = info
        if label is not None:
            self.label = label
        if job is not None:
            self.job = job
        if compute_provider_id is not None:
            self.compute_provider_id = compute_provider_id

    @property
    def inputs(self):
        """Gets the inputs of this AnalysisInput.

        The set of inputs that this analysis is based on

        :return: The inputs of this AnalysisInput.
        :rtype: list[FileReference]
        """
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        """Sets the inputs of this AnalysisInput.

        The set of inputs that this analysis is based on

        :param inputs: The inputs of this AnalysisInput.  # noqa: E501
        :type: list[FileReference]
        """

        self._inputs = inputs

    @property
    def description(self):
        """Gets the description of this AnalysisInput.


        :return: The description of this AnalysisInput.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this AnalysisInput.


        :param description: The description of this AnalysisInput.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def info(self):
        """Gets the info of this AnalysisInput.


        :return: The info of this AnalysisInput.
        :rtype: CommonInfo
        """
        return self._info

    @info.setter
    def info(self, info):
        """Sets the info of this AnalysisInput.


        :param info: The info of this AnalysisInput.  # noqa: E501
        :type: CommonInfo
        """

        self._info = info

    @property
    def label(self):
        """Gets the label of this AnalysisInput.

        Application-specific label

        :return: The label of this AnalysisInput.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this AnalysisInput.

        Application-specific label

        :param label: The label of this AnalysisInput.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def job(self):
        """Gets the job of this AnalysisInput.


        :return: The job of this AnalysisInput.
        :rtype: Job
        """
        return self._job

    @job.setter
    def job(self, job):
        """Sets the job of this AnalysisInput.


        :param job: The job of this AnalysisInput.  # noqa: E501
        :type: Job
        """

        self._job = job

    @property
    def compute_provider_id(self):
        """Gets the compute_provider_id of this AnalysisInput.

        Unique database ID

        :return: The compute_provider_id of this AnalysisInput.
        :rtype: str
        """
        return self._compute_provider_id

    @compute_provider_id.setter
    def compute_provider_id(self, compute_provider_id):
        """Sets the compute_provider_id of this AnalysisInput.

        Unique database ID

        :param compute_provider_id: The compute_provider_id of this AnalysisInput.  # noqa: E501
        :type: str
        """

        self._compute_provider_id = compute_provider_id


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
        if not isinstance(other, AnalysisInput):
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
