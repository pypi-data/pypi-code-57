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

from flywheel.models.analysis_output import AnalysisOutput  # noqa: F401,E501
from flywheel.models.common_info import CommonInfo  # noqa: F401,E501
from flywheel.models.container_parents import ContainerParents  # noqa: F401,E501
from flywheel.models.file_entry import FileEntry  # noqa: F401,E501
from flywheel.models.note import Note  # noqa: F401,E501
from flywheel.models.roles_backwards_compatible_role_assignment import RolesBackwardsCompatibleRoleAssignment  # noqa: F401,E501
from flywheel.models.subject import Subject  # noqa: F401,E501

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.

from .mixins import SessionMixin

class Session(SessionMixin):

    swagger_types = {
        'operator': 'str',
        'label': 'str',
        'info': 'CommonInfo',
        'project': 'str',
        'uid': 'str',
        'timestamp': 'datetime',
        'timezone': 'str',
        'subject': 'Subject',
        'age': 'int',
        'weight': 'float',
        'id': 'str',
        'info_exists': 'bool',
        'parents': 'ContainerParents',
        'created': 'datetime',
        'modified': 'datetime',
        'revision': 'int',
        'permissions': 'list[RolesBackwardsCompatibleRoleAssignment]',
        'group': 'str',
        'project_has_template': 'bool',
        'satisfies_template': 'bool',
        'files': 'list[FileEntry]',
        'notes': 'list[Note]',
        'tags': 'list[str]',
        'analyses': 'list[AnalysisOutput]'
    }

    attribute_map = {
        'operator': 'operator',
        'label': 'label',
        'info': 'info',
        'project': 'project',
        'uid': 'uid',
        'timestamp': 'timestamp',
        'timezone': 'timezone',
        'subject': 'subject',
        'age': 'age',
        'weight': 'weight',
        'id': '_id',
        'info_exists': 'info_exists',
        'parents': 'parents',
        'created': 'created',
        'modified': 'modified',
        'revision': 'revision',
        'permissions': 'permissions',
        'group': 'group',
        'project_has_template': 'project_has_template',
        'satisfies_template': 'satisfies_template',
        'files': 'files',
        'notes': 'notes',
        'tags': 'tags',
        'analyses': 'analyses'
    }

    rattribute_map = {
        'operator': 'operator',
        'label': 'label',
        'info': 'info',
        'project': 'project',
        'uid': 'uid',
        'timestamp': 'timestamp',
        'timezone': 'timezone',
        'subject': 'subject',
        'age': 'age',
        'weight': 'weight',
        '_id': 'id',
        'info_exists': 'info_exists',
        'parents': 'parents',
        'created': 'created',
        'modified': 'modified',
        'revision': 'revision',
        'permissions': 'permissions',
        'group': 'group',
        'project_has_template': 'project_has_template',
        'satisfies_template': 'satisfies_template',
        'files': 'files',
        'notes': 'notes',
        'tags': 'tags',
        'analyses': 'analyses'
    }

    def __init__(self, operator=None, label=None, info=None, project=None, uid=None, timestamp=None, timezone=None, subject=None, age=None, weight=None, id=None, info_exists=None, parents=None, created=None, modified=None, revision=None, permissions=None, group=None, project_has_template=None, satisfies_template=None, files=None, notes=None, tags=None, analyses=None):  # noqa: E501
        """Session - a model defined in Swagger"""
        super(Session, self).__init__()

        self._operator = None
        self._label = None
        self._info = None
        self._project = None
        self._uid = None
        self._timestamp = None
        self._timezone = None
        self._subject = None
        self._age = None
        self._weight = None
        self._id = None
        self._info_exists = None
        self._parents = None
        self._created = None
        self._modified = None
        self._revision = None
        self._permissions = None
        self._group = None
        self._project_has_template = None
        self._satisfies_template = None
        self._files = None
        self._notes = None
        self._tags = None
        self._analyses = None
        self.discriminator = None
        self.alt_discriminator = None

        if operator is not None:
            self.operator = operator
        if label is not None:
            self.label = label
        if info is not None:
            self.info = info
        if project is not None:
            self.project = project
        if uid is not None:
            self.uid = uid
        if timestamp is not None:
            self.timestamp = timestamp
        if timezone is not None:
            self.timezone = timezone
        if subject is not None:
            self.subject = subject
        if age is not None:
            self.age = age
        if weight is not None:
            self.weight = weight
        if id is not None:
            self.id = id
        if info_exists is not None:
            self.info_exists = info_exists
        if parents is not None:
            self.parents = parents
        if created is not None:
            self.created = created
        if modified is not None:
            self.modified = modified
        if revision is not None:
            self.revision = revision
        if permissions is not None:
            self.permissions = permissions
        if group is not None:
            self.group = group
        if project_has_template is not None:
            self.project_has_template = project_has_template
        if satisfies_template is not None:
            self.satisfies_template = satisfies_template
        if files is not None:
            self.files = files
        if notes is not None:
            self.notes = notes
        if tags is not None:
            self.tags = tags
        if analyses is not None:
            self.analyses = analyses

    @property
    def operator(self):
        """Gets the operator of this Session.

        The name of the operator

        :return: The operator of this Session.
        :rtype: str
        """
        return self._operator

    @operator.setter
    def operator(self, operator):
        """Sets the operator of this Session.

        The name of the operator

        :param operator: The operator of this Session.  # noqa: E501
        :type: str
        """

        self._operator = operator

    @property
    def label(self):
        """Gets the label of this Session.

        Application-specific label

        :return: The label of this Session.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this Session.

        Application-specific label

        :param label: The label of this Session.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def info(self):
        """Gets the info of this Session.


        :return: The info of this Session.
        :rtype: CommonInfo
        """
        return self._info

    @info.setter
    def info(self, info):
        """Sets the info of this Session.


        :param info: The info of this Session.  # noqa: E501
        :type: CommonInfo
        """

        self._info = info

    @property
    def project(self):
        """Gets the project of this Session.

        Unique database ID

        :return: The project of this Session.
        :rtype: str
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this Session.

        Unique database ID

        :param project: The project of this Session.  # noqa: E501
        :type: str
        """

        self._project = project

    @property
    def uid(self):
        """Gets the uid of this Session.

        A user database ID

        :return: The uid of this Session.
        :rtype: str
        """
        return self._uid

    @uid.setter
    def uid(self, uid):
        """Sets the uid of this Session.

        A user database ID

        :param uid: The uid of this Session.  # noqa: E501
        :type: str
        """

        self._uid = uid

    @property
    def timestamp(self):
        """Gets the timestamp of this Session.


        :return: The timestamp of this Session.
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this Session.


        :param timestamp: The timestamp of this Session.  # noqa: E501
        :type: datetime
        """

        self._timestamp = timestamp

    @property
    def timezone(self):
        """Gets the timezone of this Session.


        :return: The timezone of this Session.
        :rtype: str
        """
        return self._timezone

    @timezone.setter
    def timezone(self, timezone):
        """Sets the timezone of this Session.


        :param timezone: The timezone of this Session.  # noqa: E501
        :type: str
        """

        self._timezone = timezone

    @property
    def subject(self):
        """Gets the subject of this Session.


        :return: The subject of this Session.
        :rtype: Subject
        """
        return self._subject

    @subject.setter
    def subject(self, subject):
        """Sets the subject of this Session.


        :param subject: The subject of this Session.  # noqa: E501
        :type: Subject
        """

        self._subject = subject

    @property
    def age(self):
        """Gets the age of this Session.

        Subject age at time of session, in seconds

        :return: The age of this Session.
        :rtype: int
        """
        return self._age

    @age.setter
    def age(self, age):
        """Sets the age of this Session.

        Subject age at time of session, in seconds

        :param age: The age of this Session.  # noqa: E501
        :type: int
        """

        self._age = age

    @property
    def weight(self):
        """Gets the weight of this Session.

        Subject weight at time of session, in kilograms

        :return: The weight of this Session.
        :rtype: float
        """
        return self._weight

    @weight.setter
    def weight(self, weight):
        """Sets the weight of this Session.

        Subject weight at time of session, in kilograms

        :param weight: The weight of this Session.  # noqa: E501
        :type: float
        """

        self._weight = weight

    @property
    def id(self):
        """Gets the id of this Session.

        Unique database ID

        :return: The id of this Session.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Session.

        Unique database ID

        :param id: The id of this Session.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def info_exists(self):
        """Gets the info_exists of this Session.

        Flag that indicates whether or not info exists on this container

        :return: The info_exists of this Session.
        :rtype: bool
        """
        return self._info_exists

    @info_exists.setter
    def info_exists(self, info_exists):
        """Sets the info_exists of this Session.

        Flag that indicates whether or not info exists on this container

        :param info_exists: The info_exists of this Session.  # noqa: E501
        :type: bool
        """

        self._info_exists = info_exists

    @property
    def parents(self):
        """Gets the parents of this Session.


        :return: The parents of this Session.
        :rtype: ContainerParents
        """
        return self._parents

    @parents.setter
    def parents(self, parents):
        """Sets the parents of this Session.


        :param parents: The parents of this Session.  # noqa: E501
        :type: ContainerParents
        """

        self._parents = parents

    @property
    def created(self):
        """Gets the created of this Session.

        Creation time (automatically set)

        :return: The created of this Session.
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this Session.

        Creation time (automatically set)

        :param created: The created of this Session.  # noqa: E501
        :type: datetime
        """

        self._created = created

    @property
    def modified(self):
        """Gets the modified of this Session.

        Last modification time (automatically updated)

        :return: The modified of this Session.
        :rtype: datetime
        """
        return self._modified

    @modified.setter
    def modified(self, modified):
        """Sets the modified of this Session.

        Last modification time (automatically updated)

        :param modified: The modified of this Session.  # noqa: E501
        :type: datetime
        """

        self._modified = modified

    @property
    def revision(self):
        """Gets the revision of this Session.

        An incremental document revision number

        :return: The revision of this Session.
        :rtype: int
        """
        return self._revision

    @revision.setter
    def revision(self, revision):
        """Sets the revision of this Session.

        An incremental document revision number

        :param revision: The revision of this Session.  # noqa: E501
        :type: int
        """

        self._revision = revision

    @property
    def permissions(self):
        """Gets the permissions of this Session.


        :return: The permissions of this Session.
        :rtype: list[RolesBackwardsCompatibleRoleAssignment]
        """
        return self._permissions

    @permissions.setter
    def permissions(self, permissions):
        """Sets the permissions of this Session.


        :param permissions: The permissions of this Session.  # noqa: E501
        :type: list[RolesBackwardsCompatibleRoleAssignment]
        """

        self._permissions = permissions

    @property
    def group(self):
        """Gets the group of this Session.


        :return: The group of this Session.
        :rtype: str
        """
        return self._group

    @group.setter
    def group(self, group):
        """Sets the group of this Session.


        :param group: The group of this Session.  # noqa: E501
        :type: str
        """

        self._group = group

    @property
    def project_has_template(self):
        """Gets the project_has_template of this Session.


        :return: The project_has_template of this Session.
        :rtype: bool
        """
        return self._project_has_template

    @project_has_template.setter
    def project_has_template(self, project_has_template):
        """Sets the project_has_template of this Session.


        :param project_has_template: The project_has_template of this Session.  # noqa: E501
        :type: bool
        """

        self._project_has_template = project_has_template

    @property
    def satisfies_template(self):
        """Gets the satisfies_template of this Session.


        :return: The satisfies_template of this Session.
        :rtype: bool
        """
        return self._satisfies_template

    @satisfies_template.setter
    def satisfies_template(self, satisfies_template):
        """Sets the satisfies_template of this Session.


        :param satisfies_template: The satisfies_template of this Session.  # noqa: E501
        :type: bool
        """

        self._satisfies_template = satisfies_template

    @property
    def files(self):
        """Gets the files of this Session.


        :return: The files of this Session.
        :rtype: list[FileEntry]
        """
        return self._files

    @files.setter
    def files(self, files):
        """Sets the files of this Session.


        :param files: The files of this Session.  # noqa: E501
        :type: list[FileEntry]
        """

        self._files = files

    @property
    def notes(self):
        """Gets the notes of this Session.


        :return: The notes of this Session.
        :rtype: list[Note]
        """
        return self._notes

    @notes.setter
    def notes(self, notes):
        """Sets the notes of this Session.


        :param notes: The notes of this Session.  # noqa: E501
        :type: list[Note]
        """

        self._notes = notes

    @property
    def tags(self):
        """Gets the tags of this Session.

        Array of application-specific tags

        :return: The tags of this Session.
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this Session.

        Array of application-specific tags

        :param tags: The tags of this Session.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def analyses(self):
        """Gets the analyses of this Session.


        :return: The analyses of this Session.
        :rtype: list[AnalysisOutput]
        """
        return self._analyses

    @analyses.setter
    def analyses(self, analyses):
        """Sets the analyses of this Session.


        :param analyses: The analyses of this Session.  # noqa: E501
        :type: list[AnalysisOutput]
        """

        self._analyses = analyses


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
        if not isinstance(other, Session):
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
