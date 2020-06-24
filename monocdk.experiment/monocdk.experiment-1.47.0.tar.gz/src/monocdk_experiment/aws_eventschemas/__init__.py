import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (CfnResource as _CfnResource_7760e8e4, Construct as _Construct_f50a3f53, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, TagManager as _TagManager_2508893f, IInspectable as _IInspectable_051e6ed8)


@jsii.implements(_IInspectable_051e6ed8)
class CfnDiscoverer(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_eventschemas.CfnDiscoverer"):
    """A CloudFormation ``AWS::EventSchemas::Discoverer``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-discoverer.html
    cloudformationResource:
    :cloudformationResource:: AWS::EventSchemas::Discoverer
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, source_arn: str, description: typing.Optional[str]=None, tags: typing.Optional[typing.List["TagsEntryProperty"]]=None) -> None:
        """Create a new ``AWS::EventSchemas::Discoverer``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param source_arn: ``AWS::EventSchemas::Discoverer.SourceArn``.
        :param description: ``AWS::EventSchemas::Discoverer.Description``.
        :param tags: ``AWS::EventSchemas::Discoverer.Tags``.
        """
        props = CfnDiscovererProps(source_arn=source_arn, description=description, tags=tags)

        jsii.create(CfnDiscoverer, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnDiscoverer":
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
    @jsii.member(jsii_name="attrDiscovererArn")
    def attr_discoverer_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: DiscovererArn
        """
        return jsii.get(self, "attrDiscovererArn")

    @builtins.property
    @jsii.member(jsii_name="attrDiscovererId")
    def attr_discoverer_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: DiscovererId
        """
        return jsii.get(self, "attrDiscovererId")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::EventSchemas::Discoverer.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-discoverer.html#cfn-eventschemas-discoverer-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="sourceArn")
    def source_arn(self) -> str:
        """``AWS::EventSchemas::Discoverer.SourceArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-discoverer.html#cfn-eventschemas-discoverer-sourcearn
        """
        return jsii.get(self, "sourceArn")

    @source_arn.setter
    def source_arn(self, value: str) -> None:
        jsii.set(self, "sourceArn", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::EventSchemas::Discoverer.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-discoverer.html#cfn-eventschemas-discoverer-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_eventschemas.CfnDiscoverer.TagsEntryProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value'})
    class TagsEntryProperty():
        def __init__(self, *, key: str, value: str) -> None:
            """
            :param key: ``CfnDiscoverer.TagsEntryProperty.Key``.
            :param value: ``CfnDiscoverer.TagsEntryProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-discoverer-tagsentry.html
            """
            self._values = {
                'key': key,
                'value': value,
            }

        @builtins.property
        def key(self) -> str:
            """``CfnDiscoverer.TagsEntryProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-discoverer-tagsentry.html#cfn-eventschemas-discoverer-tagsentry-key
            """
            return self._values.get('key')

        @builtins.property
        def value(self) -> str:
            """``CfnDiscoverer.TagsEntryProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-discoverer-tagsentry.html#cfn-eventschemas-discoverer-tagsentry-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TagsEntryProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_eventschemas.CfnDiscovererProps", jsii_struct_bases=[], name_mapping={'source_arn': 'sourceArn', 'description': 'description', 'tags': 'tags'})
class CfnDiscovererProps():
    def __init__(self, *, source_arn: str, description: typing.Optional[str]=None, tags: typing.Optional[typing.List["CfnDiscoverer.TagsEntryProperty"]]=None) -> None:
        """Properties for defining a ``AWS::EventSchemas::Discoverer``.

        :param source_arn: ``AWS::EventSchemas::Discoverer.SourceArn``.
        :param description: ``AWS::EventSchemas::Discoverer.Description``.
        :param tags: ``AWS::EventSchemas::Discoverer.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-discoverer.html
        """
        self._values = {
            'source_arn': source_arn,
        }
        if description is not None: self._values["description"] = description
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def source_arn(self) -> str:
        """``AWS::EventSchemas::Discoverer.SourceArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-discoverer.html#cfn-eventschemas-discoverer-sourcearn
        """
        return self._values.get('source_arn')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::EventSchemas::Discoverer.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-discoverer.html#cfn-eventschemas-discoverer-description
        """
        return self._values.get('description')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["CfnDiscoverer.TagsEntryProperty"]]:
        """``AWS::EventSchemas::Discoverer.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-discoverer.html#cfn-eventschemas-discoverer-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDiscovererProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnRegistry(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_eventschemas.CfnRegistry"):
    """A CloudFormation ``AWS::EventSchemas::Registry``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registry.html
    cloudformationResource:
    :cloudformationResource:: AWS::EventSchemas::Registry
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, description: typing.Optional[str]=None, registry_name: typing.Optional[str]=None, tags: typing.Optional[typing.List["TagsEntryProperty"]]=None) -> None:
        """Create a new ``AWS::EventSchemas::Registry``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::EventSchemas::Registry.Description``.
        :param registry_name: ``AWS::EventSchemas::Registry.RegistryName``.
        :param tags: ``AWS::EventSchemas::Registry.Tags``.
        """
        props = CfnRegistryProps(description=description, registry_name=registry_name, tags=tags)

        jsii.create(CfnRegistry, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnRegistry":
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
    @jsii.member(jsii_name="attrRegistryArn")
    def attr_registry_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: RegistryArn
        """
        return jsii.get(self, "attrRegistryArn")

    @builtins.property
    @jsii.member(jsii_name="attrRegistryName")
    def attr_registry_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: RegistryName
        """
        return jsii.get(self, "attrRegistryName")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::EventSchemas::Registry.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registry.html#cfn-eventschemas-registry-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::EventSchemas::Registry.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registry.html#cfn-eventschemas-registry-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="registryName")
    def registry_name(self) -> typing.Optional[str]:
        """``AWS::EventSchemas::Registry.RegistryName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registry.html#cfn-eventschemas-registry-registryname
        """
        return jsii.get(self, "registryName")

    @registry_name.setter
    def registry_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "registryName", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_eventschemas.CfnRegistry.TagsEntryProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value'})
    class TagsEntryProperty():
        def __init__(self, *, key: str, value: str) -> None:
            """
            :param key: ``CfnRegistry.TagsEntryProperty.Key``.
            :param value: ``CfnRegistry.TagsEntryProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-registry-tagsentry.html
            """
            self._values = {
                'key': key,
                'value': value,
            }

        @builtins.property
        def key(self) -> str:
            """``CfnRegistry.TagsEntryProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-registry-tagsentry.html#cfn-eventschemas-registry-tagsentry-key
            """
            return self._values.get('key')

        @builtins.property
        def value(self) -> str:
            """``CfnRegistry.TagsEntryProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-registry-tagsentry.html#cfn-eventschemas-registry-tagsentry-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TagsEntryProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.implements(_IInspectable_051e6ed8)
class CfnRegistryPolicy(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_eventschemas.CfnRegistryPolicy"):
    """A CloudFormation ``AWS::EventSchemas::RegistryPolicy``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registrypolicy.html
    cloudformationResource:
    :cloudformationResource:: AWS::EventSchemas::RegistryPolicy
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, policy: typing.Any, registry_name: str, revision_id: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EventSchemas::RegistryPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy: ``AWS::EventSchemas::RegistryPolicy.Policy``.
        :param registry_name: ``AWS::EventSchemas::RegistryPolicy.RegistryName``.
        :param revision_id: ``AWS::EventSchemas::RegistryPolicy.RevisionId``.
        """
        props = CfnRegistryPolicyProps(policy=policy, registry_name=registry_name, revision_id=revision_id)

        jsii.create(CfnRegistryPolicy, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnRegistryPolicy":
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
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Id
        """
        return jsii.get(self, "attrId")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Any:
        """``AWS::EventSchemas::RegistryPolicy.Policy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registrypolicy.html#cfn-eventschemas-registrypolicy-policy
        """
        return jsii.get(self, "policy")

    @policy.setter
    def policy(self, value: typing.Any) -> None:
        jsii.set(self, "policy", value)

    @builtins.property
    @jsii.member(jsii_name="registryName")
    def registry_name(self) -> str:
        """``AWS::EventSchemas::RegistryPolicy.RegistryName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registrypolicy.html#cfn-eventschemas-registrypolicy-registryname
        """
        return jsii.get(self, "registryName")

    @registry_name.setter
    def registry_name(self, value: str) -> None:
        jsii.set(self, "registryName", value)

    @builtins.property
    @jsii.member(jsii_name="revisionId")
    def revision_id(self) -> typing.Optional[str]:
        """``AWS::EventSchemas::RegistryPolicy.RevisionId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registrypolicy.html#cfn-eventschemas-registrypolicy-revisionid
        """
        return jsii.get(self, "revisionId")

    @revision_id.setter
    def revision_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "revisionId", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_eventschemas.CfnRegistryPolicyProps", jsii_struct_bases=[], name_mapping={'policy': 'policy', 'registry_name': 'registryName', 'revision_id': 'revisionId'})
class CfnRegistryPolicyProps():
    def __init__(self, *, policy: typing.Any, registry_name: str, revision_id: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::EventSchemas::RegistryPolicy``.

        :param policy: ``AWS::EventSchemas::RegistryPolicy.Policy``.
        :param registry_name: ``AWS::EventSchemas::RegistryPolicy.RegistryName``.
        :param revision_id: ``AWS::EventSchemas::RegistryPolicy.RevisionId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registrypolicy.html
        """
        self._values = {
            'policy': policy,
            'registry_name': registry_name,
        }
        if revision_id is not None: self._values["revision_id"] = revision_id

    @builtins.property
    def policy(self) -> typing.Any:
        """``AWS::EventSchemas::RegistryPolicy.Policy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registrypolicy.html#cfn-eventschemas-registrypolicy-policy
        """
        return self._values.get('policy')

    @builtins.property
    def registry_name(self) -> str:
        """``AWS::EventSchemas::RegistryPolicy.RegistryName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registrypolicy.html#cfn-eventschemas-registrypolicy-registryname
        """
        return self._values.get('registry_name')

    @builtins.property
    def revision_id(self) -> typing.Optional[str]:
        """``AWS::EventSchemas::RegistryPolicy.RevisionId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registrypolicy.html#cfn-eventschemas-registrypolicy-revisionid
        """
        return self._values.get('revision_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnRegistryPolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_eventschemas.CfnRegistryProps", jsii_struct_bases=[], name_mapping={'description': 'description', 'registry_name': 'registryName', 'tags': 'tags'})
class CfnRegistryProps():
    def __init__(self, *, description: typing.Optional[str]=None, registry_name: typing.Optional[str]=None, tags: typing.Optional[typing.List["CfnRegistry.TagsEntryProperty"]]=None) -> None:
        """Properties for defining a ``AWS::EventSchemas::Registry``.

        :param description: ``AWS::EventSchemas::Registry.Description``.
        :param registry_name: ``AWS::EventSchemas::Registry.RegistryName``.
        :param tags: ``AWS::EventSchemas::Registry.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registry.html
        """
        self._values = {
        }
        if description is not None: self._values["description"] = description
        if registry_name is not None: self._values["registry_name"] = registry_name
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::EventSchemas::Registry.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registry.html#cfn-eventschemas-registry-description
        """
        return self._values.get('description')

    @builtins.property
    def registry_name(self) -> typing.Optional[str]:
        """``AWS::EventSchemas::Registry.RegistryName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registry.html#cfn-eventschemas-registry-registryname
        """
        return self._values.get('registry_name')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["CfnRegistry.TagsEntryProperty"]]:
        """``AWS::EventSchemas::Registry.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registry.html#cfn-eventschemas-registry-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnRegistryProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnSchema(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_eventschemas.CfnSchema"):
    """A CloudFormation ``AWS::EventSchemas::Schema``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html
    cloudformationResource:
    :cloudformationResource:: AWS::EventSchemas::Schema
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, content: str, registry_name: str, type: str, description: typing.Optional[str]=None, schema_name: typing.Optional[str]=None, tags: typing.Optional[typing.List["TagsEntryProperty"]]=None) -> None:
        """Create a new ``AWS::EventSchemas::Schema``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param content: ``AWS::EventSchemas::Schema.Content``.
        :param registry_name: ``AWS::EventSchemas::Schema.RegistryName``.
        :param type: ``AWS::EventSchemas::Schema.Type``.
        :param description: ``AWS::EventSchemas::Schema.Description``.
        :param schema_name: ``AWS::EventSchemas::Schema.SchemaName``.
        :param tags: ``AWS::EventSchemas::Schema.Tags``.
        """
        props = CfnSchemaProps(content=content, registry_name=registry_name, type=type, description=description, schema_name=schema_name, tags=tags)

        jsii.create(CfnSchema, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnSchema":
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
    @jsii.member(jsii_name="attrSchemaArn")
    def attr_schema_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: SchemaArn
        """
        return jsii.get(self, "attrSchemaArn")

    @builtins.property
    @jsii.member(jsii_name="attrSchemaName")
    def attr_schema_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: SchemaName
        """
        return jsii.get(self, "attrSchemaName")

    @builtins.property
    @jsii.member(jsii_name="attrSchemaVersion")
    def attr_schema_version(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: SchemaVersion
        """
        return jsii.get(self, "attrSchemaVersion")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::EventSchemas::Schema.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> str:
        """``AWS::EventSchemas::Schema.Content``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-content
        """
        return jsii.get(self, "content")

    @content.setter
    def content(self, value: str) -> None:
        jsii.set(self, "content", value)

    @builtins.property
    @jsii.member(jsii_name="registryName")
    def registry_name(self) -> str:
        """``AWS::EventSchemas::Schema.RegistryName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-registryname
        """
        return jsii.get(self, "registryName")

    @registry_name.setter
    def registry_name(self, value: str) -> None:
        jsii.set(self, "registryName", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        """``AWS::EventSchemas::Schema.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-type
        """
        return jsii.get(self, "type")

    @type.setter
    def type(self, value: str) -> None:
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::EventSchemas::Schema.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="schemaName")
    def schema_name(self) -> typing.Optional[str]:
        """``AWS::EventSchemas::Schema.SchemaName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-schemaname
        """
        return jsii.get(self, "schemaName")

    @schema_name.setter
    def schema_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "schemaName", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_eventschemas.CfnSchema.TagsEntryProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value'})
    class TagsEntryProperty():
        def __init__(self, *, key: str, value: str) -> None:
            """
            :param key: ``CfnSchema.TagsEntryProperty.Key``.
            :param value: ``CfnSchema.TagsEntryProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-schema-tagsentry.html
            """
            self._values = {
                'key': key,
                'value': value,
            }

        @builtins.property
        def key(self) -> str:
            """``CfnSchema.TagsEntryProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-schema-tagsentry.html#cfn-eventschemas-schema-tagsentry-key
            """
            return self._values.get('key')

        @builtins.property
        def value(self) -> str:
            """``CfnSchema.TagsEntryProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-schema-tagsentry.html#cfn-eventschemas-schema-tagsentry-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TagsEntryProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_eventschemas.CfnSchemaProps", jsii_struct_bases=[], name_mapping={'content': 'content', 'registry_name': 'registryName', 'type': 'type', 'description': 'description', 'schema_name': 'schemaName', 'tags': 'tags'})
class CfnSchemaProps():
    def __init__(self, *, content: str, registry_name: str, type: str, description: typing.Optional[str]=None, schema_name: typing.Optional[str]=None, tags: typing.Optional[typing.List["CfnSchema.TagsEntryProperty"]]=None) -> None:
        """Properties for defining a ``AWS::EventSchemas::Schema``.

        :param content: ``AWS::EventSchemas::Schema.Content``.
        :param registry_name: ``AWS::EventSchemas::Schema.RegistryName``.
        :param type: ``AWS::EventSchemas::Schema.Type``.
        :param description: ``AWS::EventSchemas::Schema.Description``.
        :param schema_name: ``AWS::EventSchemas::Schema.SchemaName``.
        :param tags: ``AWS::EventSchemas::Schema.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html
        """
        self._values = {
            'content': content,
            'registry_name': registry_name,
            'type': type,
        }
        if description is not None: self._values["description"] = description
        if schema_name is not None: self._values["schema_name"] = schema_name
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def content(self) -> str:
        """``AWS::EventSchemas::Schema.Content``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-content
        """
        return self._values.get('content')

    @builtins.property
    def registry_name(self) -> str:
        """``AWS::EventSchemas::Schema.RegistryName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-registryname
        """
        return self._values.get('registry_name')

    @builtins.property
    def type(self) -> str:
        """``AWS::EventSchemas::Schema.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-type
        """
        return self._values.get('type')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::EventSchemas::Schema.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-description
        """
        return self._values.get('description')

    @builtins.property
    def schema_name(self) -> typing.Optional[str]:
        """``AWS::EventSchemas::Schema.SchemaName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-schemaname
        """
        return self._values.get('schema_name')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["CfnSchema.TagsEntryProperty"]]:
        """``AWS::EventSchemas::Schema.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnSchemaProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnDiscoverer",
    "CfnDiscovererProps",
    "CfnRegistry",
    "CfnRegistryPolicy",
    "CfnRegistryPolicyProps",
    "CfnRegistryProps",
    "CfnSchema",
    "CfnSchemaProps",
]

publication.publish()
