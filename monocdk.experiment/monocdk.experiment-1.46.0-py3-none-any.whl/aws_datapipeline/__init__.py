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
class CfnPipeline(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_datapipeline.CfnPipeline"):
    """A CloudFormation ``AWS::DataPipeline::Pipeline``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html
    cloudformationResource:
    :cloudformationResource:: AWS::DataPipeline::Pipeline
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, name: str, parameter_objects: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ParameterObjectProperty", _IResolvable_9ceae33e]]], activate: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, description: typing.Optional[str]=None, parameter_values: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ParameterValueProperty", _IResolvable_9ceae33e]]]]=None, pipeline_objects: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["PipelineObjectProperty", _IResolvable_9ceae33e]]]]=None, pipeline_tags: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["PipelineTagProperty", _IResolvable_9ceae33e]]]]=None) -> None:
        """Create a new ``AWS::DataPipeline::Pipeline``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::DataPipeline::Pipeline.Name``.
        :param parameter_objects: ``AWS::DataPipeline::Pipeline.ParameterObjects``.
        :param activate: ``AWS::DataPipeline::Pipeline.Activate``.
        :param description: ``AWS::DataPipeline::Pipeline.Description``.
        :param parameter_values: ``AWS::DataPipeline::Pipeline.ParameterValues``.
        :param pipeline_objects: ``AWS::DataPipeline::Pipeline.PipelineObjects``.
        :param pipeline_tags: ``AWS::DataPipeline::Pipeline.PipelineTags``.
        """
        props = CfnPipelineProps(name=name, parameter_objects=parameter_objects, activate=activate, description=description, parameter_values=parameter_values, pipeline_objects=pipeline_objects, pipeline_tags=pipeline_tags)

        jsii.create(CfnPipeline, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnPipeline":
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
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::DataPipeline::Pipeline.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="parameterObjects")
    def parameter_objects(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ParameterObjectProperty", _IResolvable_9ceae33e]]]:
        """``AWS::DataPipeline::Pipeline.ParameterObjects``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-parameterobjects
        """
        return jsii.get(self, "parameterObjects")

    @parameter_objects.setter
    def parameter_objects(self, value: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ParameterObjectProperty", _IResolvable_9ceae33e]]]) -> None:
        jsii.set(self, "parameterObjects", value)

    @builtins.property
    @jsii.member(jsii_name="activate")
    def activate(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::DataPipeline::Pipeline.Activate``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-activate
        """
        return jsii.get(self, "activate")

    @activate.setter
    def activate(self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "activate", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::DataPipeline::Pipeline.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="parameterValues")
    def parameter_values(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ParameterValueProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::DataPipeline::Pipeline.ParameterValues``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-parametervalues
        """
        return jsii.get(self, "parameterValues")

    @parameter_values.setter
    def parameter_values(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ParameterValueProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "parameterValues", value)

    @builtins.property
    @jsii.member(jsii_name="pipelineObjects")
    def pipeline_objects(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["PipelineObjectProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::DataPipeline::Pipeline.PipelineObjects``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-pipelineobjects
        """
        return jsii.get(self, "pipelineObjects")

    @pipeline_objects.setter
    def pipeline_objects(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["PipelineObjectProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "pipelineObjects", value)

    @builtins.property
    @jsii.member(jsii_name="pipelineTags")
    def pipeline_tags(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["PipelineTagProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::DataPipeline::Pipeline.PipelineTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-pipelinetags
        """
        return jsii.get(self, "pipelineTags")

    @pipeline_tags.setter
    def pipeline_tags(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["PipelineTagProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "pipelineTags", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_datapipeline.CfnPipeline.FieldProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'ref_value': 'refValue', 'string_value': 'stringValue'})
    class FieldProperty():
        def __init__(self, *, key: str, ref_value: typing.Optional[str]=None, string_value: typing.Optional[str]=None) -> None:
            """
            :param key: ``CfnPipeline.FieldProperty.Key``.
            :param ref_value: ``CfnPipeline.FieldProperty.RefValue``.
            :param string_value: ``CfnPipeline.FieldProperty.StringValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelineobjects-fields.html
            """
            self._values = {
                'key': key,
            }
            if ref_value is not None: self._values["ref_value"] = ref_value
            if string_value is not None: self._values["string_value"] = string_value

        @builtins.property
        def key(self) -> str:
            """``CfnPipeline.FieldProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelineobjects-fields.html#cfn-datapipeline-pipeline-pipelineobjects-fields-key
            """
            return self._values.get('key')

        @builtins.property
        def ref_value(self) -> typing.Optional[str]:
            """``CfnPipeline.FieldProperty.RefValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelineobjects-fields.html#cfn-datapipeline-pipeline-pipelineobjects-fields-refvalue
            """
            return self._values.get('ref_value')

        @builtins.property
        def string_value(self) -> typing.Optional[str]:
            """``CfnPipeline.FieldProperty.StringValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelineobjects-fields.html#cfn-datapipeline-pipeline-pipelineobjects-fields-stringvalue
            """
            return self._values.get('string_value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'FieldProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_datapipeline.CfnPipeline.ParameterAttributeProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'string_value': 'stringValue'})
    class ParameterAttributeProperty():
        def __init__(self, *, key: str, string_value: str) -> None:
            """
            :param key: ``CfnPipeline.ParameterAttributeProperty.Key``.
            :param string_value: ``CfnPipeline.ParameterAttributeProperty.StringValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parameterobjects-attributes.html
            """
            self._values = {
                'key': key,
                'string_value': string_value,
            }

        @builtins.property
        def key(self) -> str:
            """``CfnPipeline.ParameterAttributeProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parameterobjects-attributes.html#cfn-datapipeline-pipeline-parameterobjects-attribtues-key
            """
            return self._values.get('key')

        @builtins.property
        def string_value(self) -> str:
            """``CfnPipeline.ParameterAttributeProperty.StringValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parameterobjects-attributes.html#cfn-datapipeline-pipeline-parameterobjects-attribtues-stringvalue
            """
            return self._values.get('string_value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ParameterAttributeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_datapipeline.CfnPipeline.ParameterObjectProperty", jsii_struct_bases=[], name_mapping={'attributes': 'attributes', 'id': 'id'})
    class ParameterObjectProperty():
        def __init__(self, *, attributes: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnPipeline.ParameterAttributeProperty", _IResolvable_9ceae33e]]], id: str) -> None:
            """
            :param attributes: ``CfnPipeline.ParameterObjectProperty.Attributes``.
            :param id: ``CfnPipeline.ParameterObjectProperty.Id``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parameterobjects.html
            """
            self._values = {
                'attributes': attributes,
                'id': id,
            }

        @builtins.property
        def attributes(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnPipeline.ParameterAttributeProperty", _IResolvable_9ceae33e]]]:
            """``CfnPipeline.ParameterObjectProperty.Attributes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parameterobjects.html#cfn-datapipeline-pipeline-parameterobjects-attributes
            """
            return self._values.get('attributes')

        @builtins.property
        def id(self) -> str:
            """``CfnPipeline.ParameterObjectProperty.Id``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parameterobjects.html#cfn-datapipeline-pipeline-parameterobjects-id
            """
            return self._values.get('id')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ParameterObjectProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_datapipeline.CfnPipeline.ParameterValueProperty", jsii_struct_bases=[], name_mapping={'id': 'id', 'string_value': 'stringValue'})
    class ParameterValueProperty():
        def __init__(self, *, id: str, string_value: str) -> None:
            """
            :param id: ``CfnPipeline.ParameterValueProperty.Id``.
            :param string_value: ``CfnPipeline.ParameterValueProperty.StringValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parametervalues.html
            """
            self._values = {
                'id': id,
                'string_value': string_value,
            }

        @builtins.property
        def id(self) -> str:
            """``CfnPipeline.ParameterValueProperty.Id``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parametervalues.html#cfn-datapipeline-pipeline-parametervalues-id
            """
            return self._values.get('id')

        @builtins.property
        def string_value(self) -> str:
            """``CfnPipeline.ParameterValueProperty.StringValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parametervalues.html#cfn-datapipeline-pipeline-parametervalues-stringvalue
            """
            return self._values.get('string_value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ParameterValueProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_datapipeline.CfnPipeline.PipelineObjectProperty", jsii_struct_bases=[], name_mapping={'fields': 'fields', 'id': 'id', 'name': 'name'})
    class PipelineObjectProperty():
        def __init__(self, *, fields: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnPipeline.FieldProperty", _IResolvable_9ceae33e]]], id: str, name: str) -> None:
            """
            :param fields: ``CfnPipeline.PipelineObjectProperty.Fields``.
            :param id: ``CfnPipeline.PipelineObjectProperty.Id``.
            :param name: ``CfnPipeline.PipelineObjectProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelineobjects.html
            """
            self._values = {
                'fields': fields,
                'id': id,
                'name': name,
            }

        @builtins.property
        def fields(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnPipeline.FieldProperty", _IResolvable_9ceae33e]]]:
            """``CfnPipeline.PipelineObjectProperty.Fields``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelineobjects.html#cfn-datapipeline-pipeline-pipelineobjects-fields
            """
            return self._values.get('fields')

        @builtins.property
        def id(self) -> str:
            """``CfnPipeline.PipelineObjectProperty.Id``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelineobjects.html#cfn-datapipeline-pipeline-pipelineobjects-id
            """
            return self._values.get('id')

        @builtins.property
        def name(self) -> str:
            """``CfnPipeline.PipelineObjectProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelineobjects.html#cfn-datapipeline-pipeline-pipelineobjects-name
            """
            return self._values.get('name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PipelineObjectProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_datapipeline.CfnPipeline.PipelineTagProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value'})
    class PipelineTagProperty():
        def __init__(self, *, key: str, value: str) -> None:
            """
            :param key: ``CfnPipeline.PipelineTagProperty.Key``.
            :param value: ``CfnPipeline.PipelineTagProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelinetags.html
            """
            self._values = {
                'key': key,
                'value': value,
            }

        @builtins.property
        def key(self) -> str:
            """``CfnPipeline.PipelineTagProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelinetags.html#cfn-datapipeline-pipeline-pipelinetags-key
            """
            return self._values.get('key')

        @builtins.property
        def value(self) -> str:
            """``CfnPipeline.PipelineTagProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelinetags.html#cfn-datapipeline-pipeline-pipelinetags-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PipelineTagProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_datapipeline.CfnPipelineProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'parameter_objects': 'parameterObjects', 'activate': 'activate', 'description': 'description', 'parameter_values': 'parameterValues', 'pipeline_objects': 'pipelineObjects', 'pipeline_tags': 'pipelineTags'})
class CfnPipelineProps():
    def __init__(self, *, name: str, parameter_objects: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnPipeline.ParameterObjectProperty", _IResolvable_9ceae33e]]], activate: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, description: typing.Optional[str]=None, parameter_values: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnPipeline.ParameterValueProperty", _IResolvable_9ceae33e]]]]=None, pipeline_objects: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnPipeline.PipelineObjectProperty", _IResolvable_9ceae33e]]]]=None, pipeline_tags: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnPipeline.PipelineTagProperty", _IResolvable_9ceae33e]]]]=None) -> None:
        """Properties for defining a ``AWS::DataPipeline::Pipeline``.

        :param name: ``AWS::DataPipeline::Pipeline.Name``.
        :param parameter_objects: ``AWS::DataPipeline::Pipeline.ParameterObjects``.
        :param activate: ``AWS::DataPipeline::Pipeline.Activate``.
        :param description: ``AWS::DataPipeline::Pipeline.Description``.
        :param parameter_values: ``AWS::DataPipeline::Pipeline.ParameterValues``.
        :param pipeline_objects: ``AWS::DataPipeline::Pipeline.PipelineObjects``.
        :param pipeline_tags: ``AWS::DataPipeline::Pipeline.PipelineTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html
        """
        self._values = {
            'name': name,
            'parameter_objects': parameter_objects,
        }
        if activate is not None: self._values["activate"] = activate
        if description is not None: self._values["description"] = description
        if parameter_values is not None: self._values["parameter_values"] = parameter_values
        if pipeline_objects is not None: self._values["pipeline_objects"] = pipeline_objects
        if pipeline_tags is not None: self._values["pipeline_tags"] = pipeline_tags

    @builtins.property
    def name(self) -> str:
        """``AWS::DataPipeline::Pipeline.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-name
        """
        return self._values.get('name')

    @builtins.property
    def parameter_objects(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnPipeline.ParameterObjectProperty", _IResolvable_9ceae33e]]]:
        """``AWS::DataPipeline::Pipeline.ParameterObjects``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-parameterobjects
        """
        return self._values.get('parameter_objects')

    @builtins.property
    def activate(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::DataPipeline::Pipeline.Activate``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-activate
        """
        return self._values.get('activate')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::DataPipeline::Pipeline.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-description
        """
        return self._values.get('description')

    @builtins.property
    def parameter_values(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnPipeline.ParameterValueProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::DataPipeline::Pipeline.ParameterValues``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-parametervalues
        """
        return self._values.get('parameter_values')

    @builtins.property
    def pipeline_objects(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnPipeline.PipelineObjectProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::DataPipeline::Pipeline.PipelineObjects``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-pipelineobjects
        """
        return self._values.get('pipeline_objects')

    @builtins.property
    def pipeline_tags(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnPipeline.PipelineTagProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::DataPipeline::Pipeline.PipelineTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-pipelinetags
        """
        return self._values.get('pipeline_tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnPipelineProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnPipeline",
    "CfnPipelineProps",
]

publication.publish()
