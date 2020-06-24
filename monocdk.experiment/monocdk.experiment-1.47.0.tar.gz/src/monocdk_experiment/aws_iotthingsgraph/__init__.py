import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (CfnResource as _CfnResource_7760e8e4, Construct as _Construct_f50a3f53, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, IResolvable as _IResolvable_9ceae33e, IInspectable as _IInspectable_051e6ed8)


@jsii.implements(_IInspectable_051e6ed8)
class CfnFlowTemplate(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_iotthingsgraph.CfnFlowTemplate"):
    """A CloudFormation ``AWS::IoTThingsGraph::FlowTemplate``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotthingsgraph-flowtemplate.html
    cloudformationResource:
    :cloudformationResource:: AWS::IoTThingsGraph::FlowTemplate
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, definition: typing.Union["DefinitionDocumentProperty", _IResolvable_9ceae33e], compatible_namespace_version: typing.Optional[jsii.Number]=None) -> None:
        """Create a new ``AWS::IoTThingsGraph::FlowTemplate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param definition: ``AWS::IoTThingsGraph::FlowTemplate.Definition``.
        :param compatible_namespace_version: ``AWS::IoTThingsGraph::FlowTemplate.CompatibleNamespaceVersion``.
        """
        props = CfnFlowTemplateProps(definition=definition, compatible_namespace_version=compatible_namespace_version)

        jsii.create(CfnFlowTemplate, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnFlowTemplate":
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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> typing.Union["DefinitionDocumentProperty", _IResolvable_9ceae33e]:
        """``AWS::IoTThingsGraph::FlowTemplate.Definition``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotthingsgraph-flowtemplate.html#cfn-iotthingsgraph-flowtemplate-definition
        """
        return jsii.get(self, "definition")

    @definition.setter
    def definition(self, value: typing.Union["DefinitionDocumentProperty", _IResolvable_9ceae33e]) -> None:
        jsii.set(self, "definition", value)

    @builtins.property
    @jsii.member(jsii_name="compatibleNamespaceVersion")
    def compatible_namespace_version(self) -> typing.Optional[jsii.Number]:
        """``AWS::IoTThingsGraph::FlowTemplate.CompatibleNamespaceVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotthingsgraph-flowtemplate.html#cfn-iotthingsgraph-flowtemplate-compatiblenamespaceversion
        """
        return jsii.get(self, "compatibleNamespaceVersion")

    @compatible_namespace_version.setter
    def compatible_namespace_version(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "compatibleNamespaceVersion", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_iotthingsgraph.CfnFlowTemplate.DefinitionDocumentProperty", jsii_struct_bases=[], name_mapping={'language': 'language', 'text': 'text'})
    class DefinitionDocumentProperty():
        def __init__(self, *, language: str, text: str) -> None:
            """
            :param language: ``CfnFlowTemplate.DefinitionDocumentProperty.Language``.
            :param text: ``CfnFlowTemplate.DefinitionDocumentProperty.Text``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotthingsgraph-flowtemplate-definitiondocument.html
            """
            self._values = {
                'language': language,
                'text': text,
            }

        @builtins.property
        def language(self) -> str:
            """``CfnFlowTemplate.DefinitionDocumentProperty.Language``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotthingsgraph-flowtemplate-definitiondocument.html#cfn-iotthingsgraph-flowtemplate-definitiondocument-language
            """
            return self._values.get('language')

        @builtins.property
        def text(self) -> str:
            """``CfnFlowTemplate.DefinitionDocumentProperty.Text``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotthingsgraph-flowtemplate-definitiondocument.html#cfn-iotthingsgraph-flowtemplate-definitiondocument-text
            """
            return self._values.get('text')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DefinitionDocumentProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_iotthingsgraph.CfnFlowTemplateProps", jsii_struct_bases=[], name_mapping={'definition': 'definition', 'compatible_namespace_version': 'compatibleNamespaceVersion'})
class CfnFlowTemplateProps():
    def __init__(self, *, definition: typing.Union["CfnFlowTemplate.DefinitionDocumentProperty", _IResolvable_9ceae33e], compatible_namespace_version: typing.Optional[jsii.Number]=None) -> None:
        """Properties for defining a ``AWS::IoTThingsGraph::FlowTemplate``.

        :param definition: ``AWS::IoTThingsGraph::FlowTemplate.Definition``.
        :param compatible_namespace_version: ``AWS::IoTThingsGraph::FlowTemplate.CompatibleNamespaceVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotthingsgraph-flowtemplate.html
        """
        self._values = {
            'definition': definition,
        }
        if compatible_namespace_version is not None: self._values["compatible_namespace_version"] = compatible_namespace_version

    @builtins.property
    def definition(self) -> typing.Union["CfnFlowTemplate.DefinitionDocumentProperty", _IResolvable_9ceae33e]:
        """``AWS::IoTThingsGraph::FlowTemplate.Definition``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotthingsgraph-flowtemplate.html#cfn-iotthingsgraph-flowtemplate-definition
        """
        return self._values.get('definition')

    @builtins.property
    def compatible_namespace_version(self) -> typing.Optional[jsii.Number]:
        """``AWS::IoTThingsGraph::FlowTemplate.CompatibleNamespaceVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotthingsgraph-flowtemplate.html#cfn-iotthingsgraph-flowtemplate-compatiblenamespaceversion
        """
        return self._values.get('compatible_namespace_version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnFlowTemplateProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnFlowTemplate",
    "CfnFlowTemplateProps",
]

publication.publish()
