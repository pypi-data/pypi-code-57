import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (CfnResource as _CfnResource_7760e8e4, Construct as _Construct_f50a3f53, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, IInspectable as _IInspectable_051e6ed8, TagManager as _TagManager_2508893f, IResolvable as _IResolvable_9ceae33e, CfnTag as _CfnTag_b4661f1a)


@jsii.implements(_IInspectable_051e6ed8)
class CfnNamedQuery(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_athena.CfnNamedQuery"):
    """A CloudFormation ``AWS::Athena::NamedQuery``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html
    cloudformationResource:
    :cloudformationResource:: AWS::Athena::NamedQuery
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, database: str, query_string: str, description: typing.Optional[str]=None, name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Athena::NamedQuery``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param database: ``AWS::Athena::NamedQuery.Database``.
        :param query_string: ``AWS::Athena::NamedQuery.QueryString``.
        :param description: ``AWS::Athena::NamedQuery.Description``.
        :param name: ``AWS::Athena::NamedQuery.Name``.
        """
        props = CfnNamedQueryProps(database=database, query_string=query_string, description=description, name=name)

        jsii.create(CfnNamedQuery, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnNamedQuery":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = _FromCloudFormationOptions_5f49f6f1(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrNamedQueryId")
    def attr_named_query_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: NamedQueryId
        """
        return jsii.get(self, "attrNamedQueryId")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> str:
        """``AWS::Athena::NamedQuery.Database``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-database
        """
        return jsii.get(self, "database")

    @database.setter
    def database(self, value: str) -> None:
        jsii.set(self, "database", value)

    @builtins.property
    @jsii.member(jsii_name="queryString")
    def query_string(self) -> str:
        """``AWS::Athena::NamedQuery.QueryString``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-querystring
        """
        return jsii.get(self, "queryString")

    @query_string.setter
    def query_string(self, value: str) -> None:
        jsii.set(self, "queryString", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::Athena::NamedQuery.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::Athena::NamedQuery.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "name", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_athena.CfnNamedQueryProps", jsii_struct_bases=[], name_mapping={'database': 'database', 'query_string': 'queryString', 'description': 'description', 'name': 'name'})
class CfnNamedQueryProps():
    def __init__(self, *, database: str, query_string: str, description: typing.Optional[str]=None, name: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::Athena::NamedQuery``.

        :param database: ``AWS::Athena::NamedQuery.Database``.
        :param query_string: ``AWS::Athena::NamedQuery.QueryString``.
        :param description: ``AWS::Athena::NamedQuery.Description``.
        :param name: ``AWS::Athena::NamedQuery.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html
        """
        self._values = {
            'database': database,
            'query_string': query_string,
        }
        if description is not None: self._values["description"] = description
        if name is not None: self._values["name"] = name

    @builtins.property
    def database(self) -> str:
        """``AWS::Athena::NamedQuery.Database``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-database
        """
        return self._values.get('database')

    @builtins.property
    def query_string(self) -> str:
        """``AWS::Athena::NamedQuery.QueryString``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-querystring
        """
        return self._values.get('query_string')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::Athena::NamedQuery.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-description
        """
        return self._values.get('description')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::Athena::NamedQuery.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-name
        """
        return self._values.get('name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnNamedQueryProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnWorkGroup(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_athena.CfnWorkGroup"):
    """A CloudFormation ``AWS::Athena::WorkGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::Athena::WorkGroup
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, name: str, description: typing.Optional[str]=None, recursive_delete_option: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, state: typing.Optional[str]=None, tags: typing.Optional["TagsProperty"]=None, work_group_configuration: typing.Optional[typing.Union["WorkGroupConfigurationProperty", _IResolvable_9ceae33e]]=None, work_group_configuration_updates: typing.Optional[typing.Union["WorkGroupConfigurationUpdatesProperty", _IResolvable_9ceae33e]]=None) -> None:
        """Create a new ``AWS::Athena::WorkGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::Athena::WorkGroup.Name``.
        :param description: ``AWS::Athena::WorkGroup.Description``.
        :param recursive_delete_option: ``AWS::Athena::WorkGroup.RecursiveDeleteOption``.
        :param state: ``AWS::Athena::WorkGroup.State``.
        :param tags: ``AWS::Athena::WorkGroup.Tags``.
        :param work_group_configuration: ``AWS::Athena::WorkGroup.WorkGroupConfiguration``.
        :param work_group_configuration_updates: ``AWS::Athena::WorkGroup.WorkGroupConfigurationUpdates``.
        """
        props = CfnWorkGroupProps(name=name, description=description, recursive_delete_option=recursive_delete_option, state=state, tags=tags, work_group_configuration=work_group_configuration, work_group_configuration_updates=work_group_configuration_updates)

        jsii.create(CfnWorkGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnWorkGroup":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = _FromCloudFormationOptions_5f49f6f1(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: CreationTime
        """
        return jsii.get(self, "attrCreationTime")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::Athena::WorkGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::Athena::WorkGroup.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::Athena::WorkGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="recursiveDeleteOption")
    def recursive_delete_option(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::Athena::WorkGroup.RecursiveDeleteOption``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-recursivedeleteoption
        """
        return jsii.get(self, "recursiveDeleteOption")

    @recursive_delete_option.setter
    def recursive_delete_option(self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "recursiveDeleteOption", value)

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> typing.Optional[str]:
        """``AWS::Athena::WorkGroup.State``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-state
        """
        return jsii.get(self, "state")

    @state.setter
    def state(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "state", value)

    @builtins.property
    @jsii.member(jsii_name="workGroupConfiguration")
    def work_group_configuration(self) -> typing.Optional[typing.Union["WorkGroupConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::Athena::WorkGroup.WorkGroupConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-workgroupconfiguration
        """
        return jsii.get(self, "workGroupConfiguration")

    @work_group_configuration.setter
    def work_group_configuration(self, value: typing.Optional[typing.Union["WorkGroupConfigurationProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "workGroupConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="workGroupConfigurationUpdates")
    def work_group_configuration_updates(self) -> typing.Optional[typing.Union["WorkGroupConfigurationUpdatesProperty", _IResolvable_9ceae33e]]:
        """``AWS::Athena::WorkGroup.WorkGroupConfigurationUpdates``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-workgroupconfigurationupdates
        """
        return jsii.get(self, "workGroupConfigurationUpdates")

    @work_group_configuration_updates.setter
    def work_group_configuration_updates(self, value: typing.Optional[typing.Union["WorkGroupConfigurationUpdatesProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "workGroupConfigurationUpdates", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_athena.CfnWorkGroup.EncryptionConfigurationProperty", jsii_struct_bases=[], name_mapping={'encryption_option': 'encryptionOption', 'kms_key': 'kmsKey'})
    class EncryptionConfigurationProperty():
        def __init__(self, *, encryption_option: str, kms_key: typing.Optional[str]=None) -> None:
            """
            :param encryption_option: ``CfnWorkGroup.EncryptionConfigurationProperty.EncryptionOption``.
            :param kms_key: ``CfnWorkGroup.EncryptionConfigurationProperty.KmsKey``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-encryptionconfiguration.html
            """
            self._values = {
                'encryption_option': encryption_option,
            }
            if kms_key is not None: self._values["kms_key"] = kms_key

        @builtins.property
        def encryption_option(self) -> str:
            """``CfnWorkGroup.EncryptionConfigurationProperty.EncryptionOption``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-encryptionconfiguration.html#cfn-athena-workgroup-encryptionconfiguration-encryptionoption
            """
            return self._values.get('encryption_option')

        @builtins.property
        def kms_key(self) -> typing.Optional[str]:
            """``CfnWorkGroup.EncryptionConfigurationProperty.KmsKey``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-encryptionconfiguration.html#cfn-athena-workgroup-encryptionconfiguration-kmskey
            """
            return self._values.get('kms_key')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EncryptionConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_athena.CfnWorkGroup.ResultConfigurationProperty", jsii_struct_bases=[], name_mapping={'encryption_configuration': 'encryptionConfiguration', 'output_location': 'outputLocation'})
    class ResultConfigurationProperty():
        def __init__(self, *, encryption_configuration: typing.Optional[typing.Union["CfnWorkGroup.EncryptionConfigurationProperty", _IResolvable_9ceae33e]]=None, output_location: typing.Optional[str]=None) -> None:
            """
            :param encryption_configuration: ``CfnWorkGroup.ResultConfigurationProperty.EncryptionConfiguration``.
            :param output_location: ``CfnWorkGroup.ResultConfigurationProperty.OutputLocation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfiguration.html
            """
            self._values = {
            }
            if encryption_configuration is not None: self._values["encryption_configuration"] = encryption_configuration
            if output_location is not None: self._values["output_location"] = output_location

        @builtins.property
        def encryption_configuration(self) -> typing.Optional[typing.Union["CfnWorkGroup.EncryptionConfigurationProperty", _IResolvable_9ceae33e]]:
            """``CfnWorkGroup.ResultConfigurationProperty.EncryptionConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfiguration.html#cfn-athena-workgroup-resultconfiguration-encryptionconfiguration
            """
            return self._values.get('encryption_configuration')

        @builtins.property
        def output_location(self) -> typing.Optional[str]:
            """``CfnWorkGroup.ResultConfigurationProperty.OutputLocation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfiguration.html#cfn-athena-workgroup-resultconfiguration-outputlocation
            """
            return self._values.get('output_location')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ResultConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_athena.CfnWorkGroup.ResultConfigurationUpdatesProperty", jsii_struct_bases=[], name_mapping={'encryption_configuration': 'encryptionConfiguration', 'output_location': 'outputLocation', 'remove_encryption_configuration': 'removeEncryptionConfiguration', 'remove_output_location': 'removeOutputLocation'})
    class ResultConfigurationUpdatesProperty():
        def __init__(self, *, encryption_configuration: typing.Optional[typing.Union["CfnWorkGroup.EncryptionConfigurationProperty", _IResolvable_9ceae33e]]=None, output_location: typing.Optional[str]=None, remove_encryption_configuration: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, remove_output_location: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None) -> None:
            """
            :param encryption_configuration: ``CfnWorkGroup.ResultConfigurationUpdatesProperty.EncryptionConfiguration``.
            :param output_location: ``CfnWorkGroup.ResultConfigurationUpdatesProperty.OutputLocation``.
            :param remove_encryption_configuration: ``CfnWorkGroup.ResultConfigurationUpdatesProperty.RemoveEncryptionConfiguration``.
            :param remove_output_location: ``CfnWorkGroup.ResultConfigurationUpdatesProperty.RemoveOutputLocation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfigurationupdates.html
            """
            self._values = {
            }
            if encryption_configuration is not None: self._values["encryption_configuration"] = encryption_configuration
            if output_location is not None: self._values["output_location"] = output_location
            if remove_encryption_configuration is not None: self._values["remove_encryption_configuration"] = remove_encryption_configuration
            if remove_output_location is not None: self._values["remove_output_location"] = remove_output_location

        @builtins.property
        def encryption_configuration(self) -> typing.Optional[typing.Union["CfnWorkGroup.EncryptionConfigurationProperty", _IResolvable_9ceae33e]]:
            """``CfnWorkGroup.ResultConfigurationUpdatesProperty.EncryptionConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfigurationupdates.html#cfn-athena-workgroup-resultconfigurationupdates-encryptionconfiguration
            """
            return self._values.get('encryption_configuration')

        @builtins.property
        def output_location(self) -> typing.Optional[str]:
            """``CfnWorkGroup.ResultConfigurationUpdatesProperty.OutputLocation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfigurationupdates.html#cfn-athena-workgroup-resultconfigurationupdates-outputlocation
            """
            return self._values.get('output_location')

        @builtins.property
        def remove_encryption_configuration(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnWorkGroup.ResultConfigurationUpdatesProperty.RemoveEncryptionConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfigurationupdates.html#cfn-athena-workgroup-resultconfigurationupdates-removeencryptionconfiguration
            """
            return self._values.get('remove_encryption_configuration')

        @builtins.property
        def remove_output_location(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnWorkGroup.ResultConfigurationUpdatesProperty.RemoveOutputLocation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfigurationupdates.html#cfn-athena-workgroup-resultconfigurationupdates-removeoutputlocation
            """
            return self._values.get('remove_output_location')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ResultConfigurationUpdatesProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_athena.CfnWorkGroup.TagsProperty", jsii_struct_bases=[], name_mapping={'tags': 'tags'})
    class TagsProperty():
        def __init__(self, *, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
            """
            :param tags: ``CfnWorkGroup.TagsProperty.Tags``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-tags.html
            """
            self._values = {
            }
            if tags is not None: self._values["tags"] = tags

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
            """``CfnWorkGroup.TagsProperty.Tags``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-tags.html#cfn-athena-workgroup-tags-tags
            """
            return self._values.get('tags')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TagsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_athena.CfnWorkGroup.WorkGroupConfigurationProperty", jsii_struct_bases=[], name_mapping={'bytes_scanned_cutoff_per_query': 'bytesScannedCutoffPerQuery', 'enforce_work_group_configuration': 'enforceWorkGroupConfiguration', 'publish_cloud_watch_metrics_enabled': 'publishCloudWatchMetricsEnabled', 'requester_pays_enabled': 'requesterPaysEnabled', 'result_configuration': 'resultConfiguration'})
    class WorkGroupConfigurationProperty():
        def __init__(self, *, bytes_scanned_cutoff_per_query: typing.Optional[jsii.Number]=None, enforce_work_group_configuration: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, publish_cloud_watch_metrics_enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, requester_pays_enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, result_configuration: typing.Optional[typing.Union["CfnWorkGroup.ResultConfigurationProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param bytes_scanned_cutoff_per_query: ``CfnWorkGroup.WorkGroupConfigurationProperty.BytesScannedCutoffPerQuery``.
            :param enforce_work_group_configuration: ``CfnWorkGroup.WorkGroupConfigurationProperty.EnforceWorkGroupConfiguration``.
            :param publish_cloud_watch_metrics_enabled: ``CfnWorkGroup.WorkGroupConfigurationProperty.PublishCloudWatchMetricsEnabled``.
            :param requester_pays_enabled: ``CfnWorkGroup.WorkGroupConfigurationProperty.RequesterPaysEnabled``.
            :param result_configuration: ``CfnWorkGroup.WorkGroupConfigurationProperty.ResultConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html
            """
            self._values = {
            }
            if bytes_scanned_cutoff_per_query is not None: self._values["bytes_scanned_cutoff_per_query"] = bytes_scanned_cutoff_per_query
            if enforce_work_group_configuration is not None: self._values["enforce_work_group_configuration"] = enforce_work_group_configuration
            if publish_cloud_watch_metrics_enabled is not None: self._values["publish_cloud_watch_metrics_enabled"] = publish_cloud_watch_metrics_enabled
            if requester_pays_enabled is not None: self._values["requester_pays_enabled"] = requester_pays_enabled
            if result_configuration is not None: self._values["result_configuration"] = result_configuration

        @builtins.property
        def bytes_scanned_cutoff_per_query(self) -> typing.Optional[jsii.Number]:
            """``CfnWorkGroup.WorkGroupConfigurationProperty.BytesScannedCutoffPerQuery``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-bytesscannedcutoffperquery
            """
            return self._values.get('bytes_scanned_cutoff_per_query')

        @builtins.property
        def enforce_work_group_configuration(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnWorkGroup.WorkGroupConfigurationProperty.EnforceWorkGroupConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-enforceworkgroupconfiguration
            """
            return self._values.get('enforce_work_group_configuration')

        @builtins.property
        def publish_cloud_watch_metrics_enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnWorkGroup.WorkGroupConfigurationProperty.PublishCloudWatchMetricsEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-publishcloudwatchmetricsenabled
            """
            return self._values.get('publish_cloud_watch_metrics_enabled')

        @builtins.property
        def requester_pays_enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnWorkGroup.WorkGroupConfigurationProperty.RequesterPaysEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-requesterpaysenabled
            """
            return self._values.get('requester_pays_enabled')

        @builtins.property
        def result_configuration(self) -> typing.Optional[typing.Union["CfnWorkGroup.ResultConfigurationProperty", _IResolvable_9ceae33e]]:
            """``CfnWorkGroup.WorkGroupConfigurationProperty.ResultConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-resultconfiguration
            """
            return self._values.get('result_configuration')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'WorkGroupConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_athena.CfnWorkGroup.WorkGroupConfigurationUpdatesProperty", jsii_struct_bases=[], name_mapping={'bytes_scanned_cutoff_per_query': 'bytesScannedCutoffPerQuery', 'enforce_work_group_configuration': 'enforceWorkGroupConfiguration', 'publish_cloud_watch_metrics_enabled': 'publishCloudWatchMetricsEnabled', 'remove_bytes_scanned_cutoff_per_query': 'removeBytesScannedCutoffPerQuery', 'requester_pays_enabled': 'requesterPaysEnabled', 'result_configuration_updates': 'resultConfigurationUpdates'})
    class WorkGroupConfigurationUpdatesProperty():
        def __init__(self, *, bytes_scanned_cutoff_per_query: typing.Optional[jsii.Number]=None, enforce_work_group_configuration: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, publish_cloud_watch_metrics_enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, remove_bytes_scanned_cutoff_per_query: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, requester_pays_enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, result_configuration_updates: typing.Optional[typing.Union["CfnWorkGroup.ResultConfigurationUpdatesProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param bytes_scanned_cutoff_per_query: ``CfnWorkGroup.WorkGroupConfigurationUpdatesProperty.BytesScannedCutoffPerQuery``.
            :param enforce_work_group_configuration: ``CfnWorkGroup.WorkGroupConfigurationUpdatesProperty.EnforceWorkGroupConfiguration``.
            :param publish_cloud_watch_metrics_enabled: ``CfnWorkGroup.WorkGroupConfigurationUpdatesProperty.PublishCloudWatchMetricsEnabled``.
            :param remove_bytes_scanned_cutoff_per_query: ``CfnWorkGroup.WorkGroupConfigurationUpdatesProperty.RemoveBytesScannedCutoffPerQuery``.
            :param requester_pays_enabled: ``CfnWorkGroup.WorkGroupConfigurationUpdatesProperty.RequesterPaysEnabled``.
            :param result_configuration_updates: ``CfnWorkGroup.WorkGroupConfigurationUpdatesProperty.ResultConfigurationUpdates``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfigurationupdates.html
            """
            self._values = {
            }
            if bytes_scanned_cutoff_per_query is not None: self._values["bytes_scanned_cutoff_per_query"] = bytes_scanned_cutoff_per_query
            if enforce_work_group_configuration is not None: self._values["enforce_work_group_configuration"] = enforce_work_group_configuration
            if publish_cloud_watch_metrics_enabled is not None: self._values["publish_cloud_watch_metrics_enabled"] = publish_cloud_watch_metrics_enabled
            if remove_bytes_scanned_cutoff_per_query is not None: self._values["remove_bytes_scanned_cutoff_per_query"] = remove_bytes_scanned_cutoff_per_query
            if requester_pays_enabled is not None: self._values["requester_pays_enabled"] = requester_pays_enabled
            if result_configuration_updates is not None: self._values["result_configuration_updates"] = result_configuration_updates

        @builtins.property
        def bytes_scanned_cutoff_per_query(self) -> typing.Optional[jsii.Number]:
            """``CfnWorkGroup.WorkGroupConfigurationUpdatesProperty.BytesScannedCutoffPerQuery``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfigurationupdates.html#cfn-athena-workgroup-workgroupconfigurationupdates-bytesscannedcutoffperquery
            """
            return self._values.get('bytes_scanned_cutoff_per_query')

        @builtins.property
        def enforce_work_group_configuration(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnWorkGroup.WorkGroupConfigurationUpdatesProperty.EnforceWorkGroupConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfigurationupdates.html#cfn-athena-workgroup-workgroupconfigurationupdates-enforceworkgroupconfiguration
            """
            return self._values.get('enforce_work_group_configuration')

        @builtins.property
        def publish_cloud_watch_metrics_enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnWorkGroup.WorkGroupConfigurationUpdatesProperty.PublishCloudWatchMetricsEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfigurationupdates.html#cfn-athena-workgroup-workgroupconfigurationupdates-publishcloudwatchmetricsenabled
            """
            return self._values.get('publish_cloud_watch_metrics_enabled')

        @builtins.property
        def remove_bytes_scanned_cutoff_per_query(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnWorkGroup.WorkGroupConfigurationUpdatesProperty.RemoveBytesScannedCutoffPerQuery``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfigurationupdates.html#cfn-athena-workgroup-workgroupconfigurationupdates-removebytesscannedcutoffperquery
            """
            return self._values.get('remove_bytes_scanned_cutoff_per_query')

        @builtins.property
        def requester_pays_enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnWorkGroup.WorkGroupConfigurationUpdatesProperty.RequesterPaysEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfigurationupdates.html#cfn-athena-workgroup-workgroupconfigurationupdates-requesterpaysenabled
            """
            return self._values.get('requester_pays_enabled')

        @builtins.property
        def result_configuration_updates(self) -> typing.Optional[typing.Union["CfnWorkGroup.ResultConfigurationUpdatesProperty", _IResolvable_9ceae33e]]:
            """``CfnWorkGroup.WorkGroupConfigurationUpdatesProperty.ResultConfigurationUpdates``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfigurationupdates.html#cfn-athena-workgroup-workgroupconfigurationupdates-resultconfigurationupdates
            """
            return self._values.get('result_configuration_updates')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'WorkGroupConfigurationUpdatesProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_athena.CfnWorkGroupProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'description': 'description', 'recursive_delete_option': 'recursiveDeleteOption', 'state': 'state', 'tags': 'tags', 'work_group_configuration': 'workGroupConfiguration', 'work_group_configuration_updates': 'workGroupConfigurationUpdates'})
class CfnWorkGroupProps():
    def __init__(self, *, name: str, description: typing.Optional[str]=None, recursive_delete_option: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, state: typing.Optional[str]=None, tags: typing.Optional["CfnWorkGroup.TagsProperty"]=None, work_group_configuration: typing.Optional[typing.Union["CfnWorkGroup.WorkGroupConfigurationProperty", _IResolvable_9ceae33e]]=None, work_group_configuration_updates: typing.Optional[typing.Union["CfnWorkGroup.WorkGroupConfigurationUpdatesProperty", _IResolvable_9ceae33e]]=None) -> None:
        """Properties for defining a ``AWS::Athena::WorkGroup``.

        :param name: ``AWS::Athena::WorkGroup.Name``.
        :param description: ``AWS::Athena::WorkGroup.Description``.
        :param recursive_delete_option: ``AWS::Athena::WorkGroup.RecursiveDeleteOption``.
        :param state: ``AWS::Athena::WorkGroup.State``.
        :param tags: ``AWS::Athena::WorkGroup.Tags``.
        :param work_group_configuration: ``AWS::Athena::WorkGroup.WorkGroupConfiguration``.
        :param work_group_configuration_updates: ``AWS::Athena::WorkGroup.WorkGroupConfigurationUpdates``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html
        """
        if isinstance(tags, dict): tags = CfnWorkGroup.TagsProperty(**tags)
        self._values = {
            'name': name,
        }
        if description is not None: self._values["description"] = description
        if recursive_delete_option is not None: self._values["recursive_delete_option"] = recursive_delete_option
        if state is not None: self._values["state"] = state
        if tags is not None: self._values["tags"] = tags
        if work_group_configuration is not None: self._values["work_group_configuration"] = work_group_configuration
        if work_group_configuration_updates is not None: self._values["work_group_configuration_updates"] = work_group_configuration_updates

    @builtins.property
    def name(self) -> str:
        """``AWS::Athena::WorkGroup.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-name
        """
        return self._values.get('name')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::Athena::WorkGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-description
        """
        return self._values.get('description')

    @builtins.property
    def recursive_delete_option(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::Athena::WorkGroup.RecursiveDeleteOption``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-recursivedeleteoption
        """
        return self._values.get('recursive_delete_option')

    @builtins.property
    def state(self) -> typing.Optional[str]:
        """``AWS::Athena::WorkGroup.State``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-state
        """
        return self._values.get('state')

    @builtins.property
    def tags(self) -> typing.Optional["CfnWorkGroup.TagsProperty"]:
        """``AWS::Athena::WorkGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-tags
        """
        return self._values.get('tags')

    @builtins.property
    def work_group_configuration(self) -> typing.Optional[typing.Union["CfnWorkGroup.WorkGroupConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::Athena::WorkGroup.WorkGroupConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-workgroupconfiguration
        """
        return self._values.get('work_group_configuration')

    @builtins.property
    def work_group_configuration_updates(self) -> typing.Optional[typing.Union["CfnWorkGroup.WorkGroupConfigurationUpdatesProperty", _IResolvable_9ceae33e]]:
        """``AWS::Athena::WorkGroup.WorkGroupConfigurationUpdates``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-workgroupconfigurationupdates
        """
        return self._values.get('work_group_configuration_updates')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnWorkGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnNamedQuery",
    "CfnNamedQueryProps",
    "CfnWorkGroup",
    "CfnWorkGroupProps",
]

publication.publish()
