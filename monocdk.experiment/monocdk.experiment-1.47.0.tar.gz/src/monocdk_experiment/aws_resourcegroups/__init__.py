import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (CfnResource as _CfnResource_7760e8e4, Construct as _Construct_f50a3f53, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, TagManager as _TagManager_2508893f, IResolvable as _IResolvable_9ceae33e, IInspectable as _IInspectable_051e6ed8)


@jsii.implements(_IInspectable_051e6ed8)
class CfnGroup(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_resourcegroups.CfnGroup"):
    """A CloudFormation ``AWS::ResourceGroups::Group``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html
    cloudformationResource:
    :cloudformationResource:: AWS::ResourceGroups::Group
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, name: str, description: typing.Optional[str]=None, resource_query: typing.Optional[typing.Union["ResourceQueryProperty", _IResolvable_9ceae33e]]=None, tags: typing.Any=None) -> None:
        """Create a new ``AWS::ResourceGroups::Group``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::ResourceGroups::Group.Name``.
        :param description: ``AWS::ResourceGroups::Group.Description``.
        :param resource_query: ``AWS::ResourceGroups::Group.ResourceQuery``.
        :param tags: ``AWS::ResourceGroups::Group.Tags``.
        """
        props = CfnGroupProps(name=name, description=description, resource_query=resource_query, tags=tags)

        jsii.create(CfnGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnGroup":
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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::ResourceGroups::Group.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::ResourceGroups::Group.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ResourceGroups::Group.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="resourceQuery")
    def resource_query(self) -> typing.Optional[typing.Union["ResourceQueryProperty", _IResolvable_9ceae33e]]:
        """``AWS::ResourceGroups::Group.ResourceQuery``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-resourcequery
        """
        return jsii.get(self, "resourceQuery")

    @resource_query.setter
    def resource_query(self, value: typing.Optional[typing.Union["ResourceQueryProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "resourceQuery", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_resourcegroups.CfnGroup.QueryProperty", jsii_struct_bases=[], name_mapping={'resource_type_filters': 'resourceTypeFilters', 'stack_identifier': 'stackIdentifier', 'tag_filters': 'tagFilters'})
    class QueryProperty():
        def __init__(self, *, resource_type_filters: typing.Optional[typing.List[str]]=None, stack_identifier: typing.Optional[str]=None, tag_filters: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnGroup.TagFilterProperty", _IResolvable_9ceae33e]]]]=None) -> None:
            """
            :param resource_type_filters: ``CfnGroup.QueryProperty.ResourceTypeFilters``.
            :param stack_identifier: ``CfnGroup.QueryProperty.StackIdentifier``.
            :param tag_filters: ``CfnGroup.QueryProperty.TagFilters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-query.html
            """
            self._values = {
            }
            if resource_type_filters is not None: self._values["resource_type_filters"] = resource_type_filters
            if stack_identifier is not None: self._values["stack_identifier"] = stack_identifier
            if tag_filters is not None: self._values["tag_filters"] = tag_filters

        @builtins.property
        def resource_type_filters(self) -> typing.Optional[typing.List[str]]:
            """``CfnGroup.QueryProperty.ResourceTypeFilters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-query.html#cfn-resourcegroups-group-query-resourcetypefilters
            """
            return self._values.get('resource_type_filters')

        @builtins.property
        def stack_identifier(self) -> typing.Optional[str]:
            """``CfnGroup.QueryProperty.StackIdentifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-query.html#cfn-resourcegroups-group-query-stackidentifier
            """
            return self._values.get('stack_identifier')

        @builtins.property
        def tag_filters(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnGroup.TagFilterProperty", _IResolvable_9ceae33e]]]]:
            """``CfnGroup.QueryProperty.TagFilters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-query.html#cfn-resourcegroups-group-query-tagfilters
            """
            return self._values.get('tag_filters')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'QueryProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_resourcegroups.CfnGroup.ResourceQueryProperty", jsii_struct_bases=[], name_mapping={'query': 'query', 'type': 'type'})
    class ResourceQueryProperty():
        def __init__(self, *, query: typing.Optional[typing.Union["CfnGroup.QueryProperty", _IResolvable_9ceae33e]]=None, type: typing.Optional[str]=None) -> None:
            """
            :param query: ``CfnGroup.ResourceQueryProperty.Query``.
            :param type: ``CfnGroup.ResourceQueryProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-resourcequery.html
            """
            self._values = {
            }
            if query is not None: self._values["query"] = query
            if type is not None: self._values["type"] = type

        @builtins.property
        def query(self) -> typing.Optional[typing.Union["CfnGroup.QueryProperty", _IResolvable_9ceae33e]]:
            """``CfnGroup.ResourceQueryProperty.Query``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-resourcequery.html#cfn-resourcegroups-group-resourcequery-query
            """
            return self._values.get('query')

        @builtins.property
        def type(self) -> typing.Optional[str]:
            """``CfnGroup.ResourceQueryProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-resourcequery.html#cfn-resourcegroups-group-resourcequery-type
            """
            return self._values.get('type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ResourceQueryProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_resourcegroups.CfnGroup.TagFilterProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'values': 'values'})
    class TagFilterProperty():
        def __init__(self, *, key: typing.Optional[str]=None, values: typing.Optional[typing.List[str]]=None) -> None:
            """
            :param key: ``CfnGroup.TagFilterProperty.Key``.
            :param values: ``CfnGroup.TagFilterProperty.Values``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-tagfilter.html
            """
            self._values = {
            }
            if key is not None: self._values["key"] = key
            if values is not None: self._values["values"] = values

        @builtins.property
        def key(self) -> typing.Optional[str]:
            """``CfnGroup.TagFilterProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-tagfilter.html#cfn-resourcegroups-group-tagfilter-key
            """
            return self._values.get('key')

        @builtins.property
        def values(self) -> typing.Optional[typing.List[str]]:
            """``CfnGroup.TagFilterProperty.Values``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-tagfilter.html#cfn-resourcegroups-group-tagfilter-values
            """
            return self._values.get('values')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TagFilterProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_resourcegroups.CfnGroupProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'description': 'description', 'resource_query': 'resourceQuery', 'tags': 'tags'})
class CfnGroupProps():
    def __init__(self, *, name: str, description: typing.Optional[str]=None, resource_query: typing.Optional[typing.Union["CfnGroup.ResourceQueryProperty", _IResolvable_9ceae33e]]=None, tags: typing.Any=None) -> None:
        """Properties for defining a ``AWS::ResourceGroups::Group``.

        :param name: ``AWS::ResourceGroups::Group.Name``.
        :param description: ``AWS::ResourceGroups::Group.Description``.
        :param resource_query: ``AWS::ResourceGroups::Group.ResourceQuery``.
        :param tags: ``AWS::ResourceGroups::Group.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html
        """
        self._values = {
            'name': name,
        }
        if description is not None: self._values["description"] = description
        if resource_query is not None: self._values["resource_query"] = resource_query
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def name(self) -> str:
        """``AWS::ResourceGroups::Group.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-name
        """
        return self._values.get('name')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ResourceGroups::Group.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-description
        """
        return self._values.get('description')

    @builtins.property
    def resource_query(self) -> typing.Optional[typing.Union["CfnGroup.ResourceQueryProperty", _IResolvable_9ceae33e]]:
        """``AWS::ResourceGroups::Group.ResourceQuery``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-resourcequery
        """
        return self._values.get('resource_query')

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::ResourceGroups::Group.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnGroup",
    "CfnGroupProps",
]

publication.publish()
