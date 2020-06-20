"""
## AWS::IoTEvents Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_iotevents as iotevents
```
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from ._jsii import *

import aws_cdk.core


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDetectorModel(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel"):
    """A CloudFormation ``AWS::IoTEvents::DetectorModel``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html
    cloudformationResource:
    :cloudformationResource:: AWS::IoTEvents::DetectorModel
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, detector_model_definition: typing.Optional[typing.Union["DetectorModelDefinitionProperty", aws_cdk.core.IResolvable]]=None, detector_model_description: typing.Optional[str]=None, detector_model_name: typing.Optional[str]=None, evaluation_method: typing.Optional[str]=None, key: typing.Optional[str]=None, role_arn: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::IoTEvents::DetectorModel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param detector_model_definition: ``AWS::IoTEvents::DetectorModel.DetectorModelDefinition``.
        :param detector_model_description: ``AWS::IoTEvents::DetectorModel.DetectorModelDescription``.
        :param detector_model_name: ``AWS::IoTEvents::DetectorModel.DetectorModelName``.
        :param evaluation_method: ``AWS::IoTEvents::DetectorModel.EvaluationMethod``.
        :param key: ``AWS::IoTEvents::DetectorModel.Key``.
        :param role_arn: ``AWS::IoTEvents::DetectorModel.RoleArn``.
        :param tags: ``AWS::IoTEvents::DetectorModel.Tags``.
        """
        props = CfnDetectorModelProps(detector_model_definition=detector_model_definition, detector_model_description=detector_model_description, detector_model_name=detector_model_name, evaluation_method=evaluation_method, key=key, role_arn=role_arn, tags=tags)

        jsii.create(CfnDetectorModel, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnDetectorModel":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
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
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::IoTEvents::DetectorModel.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="detectorModelDefinition")
    def detector_model_definition(self) -> typing.Optional[typing.Union["DetectorModelDefinitionProperty", aws_cdk.core.IResolvable]]:
        """``AWS::IoTEvents::DetectorModel.DetectorModelDefinition``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-detectormodeldefinition
        """
        return jsii.get(self, "detectorModelDefinition")

    @detector_model_definition.setter
    def detector_model_definition(self, value: typing.Optional[typing.Union["DetectorModelDefinitionProperty", aws_cdk.core.IResolvable]]) -> None:
        jsii.set(self, "detectorModelDefinition", value)

    @builtins.property
    @jsii.member(jsii_name="detectorModelDescription")
    def detector_model_description(self) -> typing.Optional[str]:
        """``AWS::IoTEvents::DetectorModel.DetectorModelDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-detectormodeldescription
        """
        return jsii.get(self, "detectorModelDescription")

    @detector_model_description.setter
    def detector_model_description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "detectorModelDescription", value)

    @builtins.property
    @jsii.member(jsii_name="detectorModelName")
    def detector_model_name(self) -> typing.Optional[str]:
        """``AWS::IoTEvents::DetectorModel.DetectorModelName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-detectormodelname
        """
        return jsii.get(self, "detectorModelName")

    @detector_model_name.setter
    def detector_model_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "detectorModelName", value)

    @builtins.property
    @jsii.member(jsii_name="evaluationMethod")
    def evaluation_method(self) -> typing.Optional[str]:
        """``AWS::IoTEvents::DetectorModel.EvaluationMethod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-evaluationmethod
        """
        return jsii.get(self, "evaluationMethod")

    @evaluation_method.setter
    def evaluation_method(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "evaluationMethod", value)

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> typing.Optional[str]:
        """``AWS::IoTEvents::DetectorModel.Key``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-key
        """
        return jsii.get(self, "key")

    @key.setter
    def key(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[str]:
        """``AWS::IoTEvents::DetectorModel.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter
    def role_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "roleArn", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.ActionProperty", jsii_struct_bases=[], name_mapping={'clear_timer': 'clearTimer', 'dynamo_db': 'dynamoDb', 'dynamo_d_bv2': 'dynamoDBv2', 'firehose': 'firehose', 'iot_events': 'iotEvents', 'iot_site_wise': 'iotSiteWise', 'iot_topic_publish': 'iotTopicPublish', 'lambda_': 'lambda', 'reset_timer': 'resetTimer', 'set_timer': 'setTimer', 'set_variable': 'setVariable', 'sns': 'sns', 'sqs': 'sqs'})
    class ActionProperty():
        def __init__(self, *, clear_timer: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.ClearTimerProperty"]]=None, dynamo_db: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.DynamoDBProperty"]]=None, dynamo_d_bv2: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.DynamoDBv2Property"]]=None, firehose: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.FirehoseProperty"]]=None, iot_events: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.IotEventsProperty"]]=None, iot_site_wise: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.IotSiteWiseProperty"]]=None, iot_topic_publish: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.IotTopicPublishProperty"]]=None, lambda_: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.LambdaProperty"]]=None, reset_timer: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.ResetTimerProperty"]]=None, set_timer: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.SetTimerProperty"]]=None, set_variable: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.SetVariableProperty"]]=None, sns: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.SnsProperty"]]=None, sqs: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.SqsProperty"]]=None) -> None:
            """
            :param clear_timer: ``CfnDetectorModel.ActionProperty.ClearTimer``.
            :param dynamo_db: ``CfnDetectorModel.ActionProperty.DynamoDB``.
            :param dynamo_d_bv2: ``CfnDetectorModel.ActionProperty.DynamoDBv2``.
            :param firehose: ``CfnDetectorModel.ActionProperty.Firehose``.
            :param iot_events: ``CfnDetectorModel.ActionProperty.IotEvents``.
            :param iot_site_wise: ``CfnDetectorModel.ActionProperty.IotSiteWise``.
            :param iot_topic_publish: ``CfnDetectorModel.ActionProperty.IotTopicPublish``.
            :param lambda_: ``CfnDetectorModel.ActionProperty.Lambda``.
            :param reset_timer: ``CfnDetectorModel.ActionProperty.ResetTimer``.
            :param set_timer: ``CfnDetectorModel.ActionProperty.SetTimer``.
            :param set_variable: ``CfnDetectorModel.ActionProperty.SetVariable``.
            :param sns: ``CfnDetectorModel.ActionProperty.Sns``.
            :param sqs: ``CfnDetectorModel.ActionProperty.Sqs``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html
            """
            self._values = {
            }
            if clear_timer is not None: self._values["clear_timer"] = clear_timer
            if dynamo_db is not None: self._values["dynamo_db"] = dynamo_db
            if dynamo_d_bv2 is not None: self._values["dynamo_d_bv2"] = dynamo_d_bv2
            if firehose is not None: self._values["firehose"] = firehose
            if iot_events is not None: self._values["iot_events"] = iot_events
            if iot_site_wise is not None: self._values["iot_site_wise"] = iot_site_wise
            if iot_topic_publish is not None: self._values["iot_topic_publish"] = iot_topic_publish
            if lambda_ is not None: self._values["lambda_"] = lambda_
            if reset_timer is not None: self._values["reset_timer"] = reset_timer
            if set_timer is not None: self._values["set_timer"] = set_timer
            if set_variable is not None: self._values["set_variable"] = set_variable
            if sns is not None: self._values["sns"] = sns
            if sqs is not None: self._values["sqs"] = sqs

        @builtins.property
        def clear_timer(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.ClearTimerProperty"]]:
            """``CfnDetectorModel.ActionProperty.ClearTimer``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-cleartimer
            """
            return self._values.get('clear_timer')

        @builtins.property
        def dynamo_db(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.DynamoDBProperty"]]:
            """``CfnDetectorModel.ActionProperty.DynamoDB``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-dynamodb
            """
            return self._values.get('dynamo_db')

        @builtins.property
        def dynamo_d_bv2(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.DynamoDBv2Property"]]:
            """``CfnDetectorModel.ActionProperty.DynamoDBv2``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-dynamodbv2
            """
            return self._values.get('dynamo_d_bv2')

        @builtins.property
        def firehose(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.FirehoseProperty"]]:
            """``CfnDetectorModel.ActionProperty.Firehose``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-firehose
            """
            return self._values.get('firehose')

        @builtins.property
        def iot_events(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.IotEventsProperty"]]:
            """``CfnDetectorModel.ActionProperty.IotEvents``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-iotevents
            """
            return self._values.get('iot_events')

        @builtins.property
        def iot_site_wise(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.IotSiteWiseProperty"]]:
            """``CfnDetectorModel.ActionProperty.IotSiteWise``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-iotsitewise
            """
            return self._values.get('iot_site_wise')

        @builtins.property
        def iot_topic_publish(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.IotTopicPublishProperty"]]:
            """``CfnDetectorModel.ActionProperty.IotTopicPublish``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-iottopicpublish
            """
            return self._values.get('iot_topic_publish')

        @builtins.property
        def lambda_(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.LambdaProperty"]]:
            """``CfnDetectorModel.ActionProperty.Lambda``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-lambda
            """
            return self._values.get('lambda_')

        @builtins.property
        def reset_timer(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.ResetTimerProperty"]]:
            """``CfnDetectorModel.ActionProperty.ResetTimer``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-resettimer
            """
            return self._values.get('reset_timer')

        @builtins.property
        def set_timer(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.SetTimerProperty"]]:
            """``CfnDetectorModel.ActionProperty.SetTimer``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-settimer
            """
            return self._values.get('set_timer')

        @builtins.property
        def set_variable(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.SetVariableProperty"]]:
            """``CfnDetectorModel.ActionProperty.SetVariable``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-setvariable
            """
            return self._values.get('set_variable')

        @builtins.property
        def sns(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.SnsProperty"]]:
            """``CfnDetectorModel.ActionProperty.Sns``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-sns
            """
            return self._values.get('sns')

        @builtins.property
        def sqs(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.SqsProperty"]]:
            """``CfnDetectorModel.ActionProperty.Sqs``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-sqs
            """
            return self._values.get('sqs')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.AssetPropertyTimestampProperty", jsii_struct_bases=[], name_mapping={'offset_in_nanos': 'offsetInNanos', 'time_in_seconds': 'timeInSeconds'})
    class AssetPropertyTimestampProperty():
        def __init__(self, *, offset_in_nanos: typing.Optional[str]=None, time_in_seconds: typing.Optional[str]=None) -> None:
            """
            :param offset_in_nanos: ``CfnDetectorModel.AssetPropertyTimestampProperty.OffsetInNanos``.
            :param time_in_seconds: ``CfnDetectorModel.AssetPropertyTimestampProperty.TimeInSeconds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertytimestamp.html
            """
            self._values = {
            }
            if offset_in_nanos is not None: self._values["offset_in_nanos"] = offset_in_nanos
            if time_in_seconds is not None: self._values["time_in_seconds"] = time_in_seconds

        @builtins.property
        def offset_in_nanos(self) -> typing.Optional[str]:
            """``CfnDetectorModel.AssetPropertyTimestampProperty.OffsetInNanos``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertytimestamp.html#cfn-iotevents-detectormodel-assetpropertytimestamp-offsetinnanos
            """
            return self._values.get('offset_in_nanos')

        @builtins.property
        def time_in_seconds(self) -> typing.Optional[str]:
            """``CfnDetectorModel.AssetPropertyTimestampProperty.TimeInSeconds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertytimestamp.html#cfn-iotevents-detectormodel-assetpropertytimestamp-timeinseconds
            """
            return self._values.get('time_in_seconds')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AssetPropertyTimestampProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.AssetPropertyValueProperty", jsii_struct_bases=[], name_mapping={'quality': 'quality', 'timestamp': 'timestamp', 'value': 'value'})
    class AssetPropertyValueProperty():
        def __init__(self, *, quality: typing.Optional[str]=None, timestamp: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.AssetPropertyTimestampProperty"]]=None, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.AssetPropertyVariantProperty"]]=None) -> None:
            """
            :param quality: ``CfnDetectorModel.AssetPropertyValueProperty.Quality``.
            :param timestamp: ``CfnDetectorModel.AssetPropertyValueProperty.Timestamp``.
            :param value: ``CfnDetectorModel.AssetPropertyValueProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvalue.html
            """
            self._values = {
            }
            if quality is not None: self._values["quality"] = quality
            if timestamp is not None: self._values["timestamp"] = timestamp
            if value is not None: self._values["value"] = value

        @builtins.property
        def quality(self) -> typing.Optional[str]:
            """``CfnDetectorModel.AssetPropertyValueProperty.Quality``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvalue.html#cfn-iotevents-detectormodel-assetpropertyvalue-quality
            """
            return self._values.get('quality')

        @builtins.property
        def timestamp(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.AssetPropertyTimestampProperty"]]:
            """``CfnDetectorModel.AssetPropertyValueProperty.Timestamp``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvalue.html#cfn-iotevents-detectormodel-assetpropertyvalue-timestamp
            """
            return self._values.get('timestamp')

        @builtins.property
        def value(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.AssetPropertyVariantProperty"]]:
            """``CfnDetectorModel.AssetPropertyValueProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvalue.html#cfn-iotevents-detectormodel-assetpropertyvalue-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AssetPropertyValueProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.AssetPropertyVariantProperty", jsii_struct_bases=[], name_mapping={'boolean_value': 'booleanValue', 'double_value': 'doubleValue', 'integer_value': 'integerValue', 'string_value': 'stringValue'})
    class AssetPropertyVariantProperty():
        def __init__(self, *, boolean_value: typing.Optional[str]=None, double_value: typing.Optional[str]=None, integer_value: typing.Optional[str]=None, string_value: typing.Optional[str]=None) -> None:
            """
            :param boolean_value: ``CfnDetectorModel.AssetPropertyVariantProperty.BooleanValue``.
            :param double_value: ``CfnDetectorModel.AssetPropertyVariantProperty.DoubleValue``.
            :param integer_value: ``CfnDetectorModel.AssetPropertyVariantProperty.IntegerValue``.
            :param string_value: ``CfnDetectorModel.AssetPropertyVariantProperty.StringValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvariant.html
            """
            self._values = {
            }
            if boolean_value is not None: self._values["boolean_value"] = boolean_value
            if double_value is not None: self._values["double_value"] = double_value
            if integer_value is not None: self._values["integer_value"] = integer_value
            if string_value is not None: self._values["string_value"] = string_value

        @builtins.property
        def boolean_value(self) -> typing.Optional[str]:
            """``CfnDetectorModel.AssetPropertyVariantProperty.BooleanValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvariant.html#cfn-iotevents-detectormodel-assetpropertyvariant-booleanvalue
            """
            return self._values.get('boolean_value')

        @builtins.property
        def double_value(self) -> typing.Optional[str]:
            """``CfnDetectorModel.AssetPropertyVariantProperty.DoubleValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvariant.html#cfn-iotevents-detectormodel-assetpropertyvariant-doublevalue
            """
            return self._values.get('double_value')

        @builtins.property
        def integer_value(self) -> typing.Optional[str]:
            """``CfnDetectorModel.AssetPropertyVariantProperty.IntegerValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvariant.html#cfn-iotevents-detectormodel-assetpropertyvariant-integervalue
            """
            return self._values.get('integer_value')

        @builtins.property
        def string_value(self) -> typing.Optional[str]:
            """``CfnDetectorModel.AssetPropertyVariantProperty.StringValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvariant.html#cfn-iotevents-detectormodel-assetpropertyvariant-stringvalue
            """
            return self._values.get('string_value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AssetPropertyVariantProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.ClearTimerProperty", jsii_struct_bases=[], name_mapping={'timer_name': 'timerName'})
    class ClearTimerProperty():
        def __init__(self, *, timer_name: typing.Optional[str]=None) -> None:
            """
            :param timer_name: ``CfnDetectorModel.ClearTimerProperty.TimerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-cleartimer.html
            """
            self._values = {
            }
            if timer_name is not None: self._values["timer_name"] = timer_name

        @builtins.property
        def timer_name(self) -> typing.Optional[str]:
            """``CfnDetectorModel.ClearTimerProperty.TimerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-cleartimer.html#cfn-iotevents-detectormodel-cleartimer-timername
            """
            return self._values.get('timer_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ClearTimerProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.DetectorModelDefinitionProperty", jsii_struct_bases=[], name_mapping={'initial_state_name': 'initialStateName', 'states': 'states'})
    class DetectorModelDefinitionProperty():
        def __init__(self, *, initial_state_name: typing.Optional[str]=None, states: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.StateProperty"]]]]=None) -> None:
            """
            :param initial_state_name: ``CfnDetectorModel.DetectorModelDefinitionProperty.InitialStateName``.
            :param states: ``CfnDetectorModel.DetectorModelDefinitionProperty.States``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-detectormodeldefinition.html
            """
            self._values = {
            }
            if initial_state_name is not None: self._values["initial_state_name"] = initial_state_name
            if states is not None: self._values["states"] = states

        @builtins.property
        def initial_state_name(self) -> typing.Optional[str]:
            """``CfnDetectorModel.DetectorModelDefinitionProperty.InitialStateName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-detectormodeldefinition.html#cfn-iotevents-detectormodel-detectormodeldefinition-initialstatename
            """
            return self._values.get('initial_state_name')

        @builtins.property
        def states(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.StateProperty"]]]]:
            """``CfnDetectorModel.DetectorModelDefinitionProperty.States``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-detectormodeldefinition.html#cfn-iotevents-detectormodel-detectormodeldefinition-states
            """
            return self._values.get('states')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DetectorModelDefinitionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.DynamoDBProperty", jsii_struct_bases=[], name_mapping={'hash_key_field': 'hashKeyField', 'hash_key_type': 'hashKeyType', 'hash_key_value': 'hashKeyValue', 'operation': 'operation', 'payload': 'payload', 'payload_field': 'payloadField', 'range_key_field': 'rangeKeyField', 'range_key_type': 'rangeKeyType', 'range_key_value': 'rangeKeyValue', 'table_name': 'tableName'})
    class DynamoDBProperty():
        def __init__(self, *, hash_key_field: typing.Optional[str]=None, hash_key_type: typing.Optional[str]=None, hash_key_value: typing.Optional[str]=None, operation: typing.Optional[str]=None, payload: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.PayloadProperty"]]=None, payload_field: typing.Optional[str]=None, range_key_field: typing.Optional[str]=None, range_key_type: typing.Optional[str]=None, range_key_value: typing.Optional[str]=None, table_name: typing.Optional[str]=None) -> None:
            """
            :param hash_key_field: ``CfnDetectorModel.DynamoDBProperty.HashKeyField``.
            :param hash_key_type: ``CfnDetectorModel.DynamoDBProperty.HashKeyType``.
            :param hash_key_value: ``CfnDetectorModel.DynamoDBProperty.HashKeyValue``.
            :param operation: ``CfnDetectorModel.DynamoDBProperty.Operation``.
            :param payload: ``CfnDetectorModel.DynamoDBProperty.Payload``.
            :param payload_field: ``CfnDetectorModel.DynamoDBProperty.PayloadField``.
            :param range_key_field: ``CfnDetectorModel.DynamoDBProperty.RangeKeyField``.
            :param range_key_type: ``CfnDetectorModel.DynamoDBProperty.RangeKeyType``.
            :param range_key_value: ``CfnDetectorModel.DynamoDBProperty.RangeKeyValue``.
            :param table_name: ``CfnDetectorModel.DynamoDBProperty.TableName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html
            """
            self._values = {
            }
            if hash_key_field is not None: self._values["hash_key_field"] = hash_key_field
            if hash_key_type is not None: self._values["hash_key_type"] = hash_key_type
            if hash_key_value is not None: self._values["hash_key_value"] = hash_key_value
            if operation is not None: self._values["operation"] = operation
            if payload is not None: self._values["payload"] = payload
            if payload_field is not None: self._values["payload_field"] = payload_field
            if range_key_field is not None: self._values["range_key_field"] = range_key_field
            if range_key_type is not None: self._values["range_key_type"] = range_key_type
            if range_key_value is not None: self._values["range_key_value"] = range_key_value
            if table_name is not None: self._values["table_name"] = table_name

        @builtins.property
        def hash_key_field(self) -> typing.Optional[str]:
            """``CfnDetectorModel.DynamoDBProperty.HashKeyField``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-hashkeyfield
            """
            return self._values.get('hash_key_field')

        @builtins.property
        def hash_key_type(self) -> typing.Optional[str]:
            """``CfnDetectorModel.DynamoDBProperty.HashKeyType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-hashkeytype
            """
            return self._values.get('hash_key_type')

        @builtins.property
        def hash_key_value(self) -> typing.Optional[str]:
            """``CfnDetectorModel.DynamoDBProperty.HashKeyValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-hashkeyvalue
            """
            return self._values.get('hash_key_value')

        @builtins.property
        def operation(self) -> typing.Optional[str]:
            """``CfnDetectorModel.DynamoDBProperty.Operation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-operation
            """
            return self._values.get('operation')

        @builtins.property
        def payload(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.PayloadProperty"]]:
            """``CfnDetectorModel.DynamoDBProperty.Payload``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-payload
            """
            return self._values.get('payload')

        @builtins.property
        def payload_field(self) -> typing.Optional[str]:
            """``CfnDetectorModel.DynamoDBProperty.PayloadField``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-payloadfield
            """
            return self._values.get('payload_field')

        @builtins.property
        def range_key_field(self) -> typing.Optional[str]:
            """``CfnDetectorModel.DynamoDBProperty.RangeKeyField``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-rangekeyfield
            """
            return self._values.get('range_key_field')

        @builtins.property
        def range_key_type(self) -> typing.Optional[str]:
            """``CfnDetectorModel.DynamoDBProperty.RangeKeyType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-rangekeytype
            """
            return self._values.get('range_key_type')

        @builtins.property
        def range_key_value(self) -> typing.Optional[str]:
            """``CfnDetectorModel.DynamoDBProperty.RangeKeyValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-rangekeyvalue
            """
            return self._values.get('range_key_value')

        @builtins.property
        def table_name(self) -> typing.Optional[str]:
            """``CfnDetectorModel.DynamoDBProperty.TableName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-tablename
            """
            return self._values.get('table_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DynamoDBProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.DynamoDBv2Property", jsii_struct_bases=[], name_mapping={'payload': 'payload', 'table_name': 'tableName'})
    class DynamoDBv2Property():
        def __init__(self, *, payload: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.PayloadProperty"]]=None, table_name: typing.Optional[str]=None) -> None:
            """
            :param payload: ``CfnDetectorModel.DynamoDBv2Property.Payload``.
            :param table_name: ``CfnDetectorModel.DynamoDBv2Property.TableName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodbv2.html
            """
            self._values = {
            }
            if payload is not None: self._values["payload"] = payload
            if table_name is not None: self._values["table_name"] = table_name

        @builtins.property
        def payload(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.PayloadProperty"]]:
            """``CfnDetectorModel.DynamoDBv2Property.Payload``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodbv2.html#cfn-iotevents-detectormodel-dynamodbv2-payload
            """
            return self._values.get('payload')

        @builtins.property
        def table_name(self) -> typing.Optional[str]:
            """``CfnDetectorModel.DynamoDBv2Property.TableName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodbv2.html#cfn-iotevents-detectormodel-dynamodbv2-tablename
            """
            return self._values.get('table_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DynamoDBv2Property(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.EventProperty", jsii_struct_bases=[], name_mapping={'actions': 'actions', 'condition': 'condition', 'event_name': 'eventName'})
    class EventProperty():
        def __init__(self, *, actions: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.ActionProperty"]]]]=None, condition: typing.Optional[str]=None, event_name: typing.Optional[str]=None) -> None:
            """
            :param actions: ``CfnDetectorModel.EventProperty.Actions``.
            :param condition: ``CfnDetectorModel.EventProperty.Condition``.
            :param event_name: ``CfnDetectorModel.EventProperty.EventName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-event.html
            """
            self._values = {
            }
            if actions is not None: self._values["actions"] = actions
            if condition is not None: self._values["condition"] = condition
            if event_name is not None: self._values["event_name"] = event_name

        @builtins.property
        def actions(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.ActionProperty"]]]]:
            """``CfnDetectorModel.EventProperty.Actions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-event.html#cfn-iotevents-detectormodel-event-actions
            """
            return self._values.get('actions')

        @builtins.property
        def condition(self) -> typing.Optional[str]:
            """``CfnDetectorModel.EventProperty.Condition``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-event.html#cfn-iotevents-detectormodel-event-condition
            """
            return self._values.get('condition')

        @builtins.property
        def event_name(self) -> typing.Optional[str]:
            """``CfnDetectorModel.EventProperty.EventName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-event.html#cfn-iotevents-detectormodel-event-eventname
            """
            return self._values.get('event_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EventProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.FirehoseProperty", jsii_struct_bases=[], name_mapping={'delivery_stream_name': 'deliveryStreamName', 'payload': 'payload', 'separator': 'separator'})
    class FirehoseProperty():
        def __init__(self, *, delivery_stream_name: typing.Optional[str]=None, payload: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.PayloadProperty"]]=None, separator: typing.Optional[str]=None) -> None:
            """
            :param delivery_stream_name: ``CfnDetectorModel.FirehoseProperty.DeliveryStreamName``.
            :param payload: ``CfnDetectorModel.FirehoseProperty.Payload``.
            :param separator: ``CfnDetectorModel.FirehoseProperty.Separator``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-firehose.html
            """
            self._values = {
            }
            if delivery_stream_name is not None: self._values["delivery_stream_name"] = delivery_stream_name
            if payload is not None: self._values["payload"] = payload
            if separator is not None: self._values["separator"] = separator

        @builtins.property
        def delivery_stream_name(self) -> typing.Optional[str]:
            """``CfnDetectorModel.FirehoseProperty.DeliveryStreamName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-firehose.html#cfn-iotevents-detectormodel-firehose-deliverystreamname
            """
            return self._values.get('delivery_stream_name')

        @builtins.property
        def payload(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.PayloadProperty"]]:
            """``CfnDetectorModel.FirehoseProperty.Payload``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-firehose.html#cfn-iotevents-detectormodel-firehose-payload
            """
            return self._values.get('payload')

        @builtins.property
        def separator(self) -> typing.Optional[str]:
            """``CfnDetectorModel.FirehoseProperty.Separator``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-firehose.html#cfn-iotevents-detectormodel-firehose-separator
            """
            return self._values.get('separator')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'FirehoseProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.IotEventsProperty", jsii_struct_bases=[], name_mapping={'input_name': 'inputName', 'payload': 'payload'})
    class IotEventsProperty():
        def __init__(self, *, input_name: typing.Optional[str]=None, payload: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.PayloadProperty"]]=None) -> None:
            """
            :param input_name: ``CfnDetectorModel.IotEventsProperty.InputName``.
            :param payload: ``CfnDetectorModel.IotEventsProperty.Payload``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotevents.html
            """
            self._values = {
            }
            if input_name is not None: self._values["input_name"] = input_name
            if payload is not None: self._values["payload"] = payload

        @builtins.property
        def input_name(self) -> typing.Optional[str]:
            """``CfnDetectorModel.IotEventsProperty.InputName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotevents.html#cfn-iotevents-detectormodel-iotevents-inputname
            """
            return self._values.get('input_name')

        @builtins.property
        def payload(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.PayloadProperty"]]:
            """``CfnDetectorModel.IotEventsProperty.Payload``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotevents.html#cfn-iotevents-detectormodel-iotevents-payload
            """
            return self._values.get('payload')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'IotEventsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.IotSiteWiseProperty", jsii_struct_bases=[], name_mapping={'asset_id': 'assetId', 'entry_id': 'entryId', 'property_alias': 'propertyAlias', 'property_id': 'propertyId', 'property_value': 'propertyValue'})
    class IotSiteWiseProperty():
        def __init__(self, *, asset_id: typing.Optional[str]=None, entry_id: typing.Optional[str]=None, property_alias: typing.Optional[str]=None, property_id: typing.Optional[str]=None, property_value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.AssetPropertyValueProperty"]]=None) -> None:
            """
            :param asset_id: ``CfnDetectorModel.IotSiteWiseProperty.AssetId``.
            :param entry_id: ``CfnDetectorModel.IotSiteWiseProperty.EntryId``.
            :param property_alias: ``CfnDetectorModel.IotSiteWiseProperty.PropertyAlias``.
            :param property_id: ``CfnDetectorModel.IotSiteWiseProperty.PropertyId``.
            :param property_value: ``CfnDetectorModel.IotSiteWiseProperty.PropertyValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotsitewise.html
            """
            self._values = {
            }
            if asset_id is not None: self._values["asset_id"] = asset_id
            if entry_id is not None: self._values["entry_id"] = entry_id
            if property_alias is not None: self._values["property_alias"] = property_alias
            if property_id is not None: self._values["property_id"] = property_id
            if property_value is not None: self._values["property_value"] = property_value

        @builtins.property
        def asset_id(self) -> typing.Optional[str]:
            """``CfnDetectorModel.IotSiteWiseProperty.AssetId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotsitewise.html#cfn-iotevents-detectormodel-iotsitewise-assetid
            """
            return self._values.get('asset_id')

        @builtins.property
        def entry_id(self) -> typing.Optional[str]:
            """``CfnDetectorModel.IotSiteWiseProperty.EntryId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotsitewise.html#cfn-iotevents-detectormodel-iotsitewise-entryid
            """
            return self._values.get('entry_id')

        @builtins.property
        def property_alias(self) -> typing.Optional[str]:
            """``CfnDetectorModel.IotSiteWiseProperty.PropertyAlias``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotsitewise.html#cfn-iotevents-detectormodel-iotsitewise-propertyalias
            """
            return self._values.get('property_alias')

        @builtins.property
        def property_id(self) -> typing.Optional[str]:
            """``CfnDetectorModel.IotSiteWiseProperty.PropertyId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotsitewise.html#cfn-iotevents-detectormodel-iotsitewise-propertyid
            """
            return self._values.get('property_id')

        @builtins.property
        def property_value(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.AssetPropertyValueProperty"]]:
            """``CfnDetectorModel.IotSiteWiseProperty.PropertyValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotsitewise.html#cfn-iotevents-detectormodel-iotsitewise-propertyvalue
            """
            return self._values.get('property_value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'IotSiteWiseProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.IotTopicPublishProperty", jsii_struct_bases=[], name_mapping={'mqtt_topic': 'mqttTopic', 'payload': 'payload'})
    class IotTopicPublishProperty():
        def __init__(self, *, mqtt_topic: typing.Optional[str]=None, payload: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.PayloadProperty"]]=None) -> None:
            """
            :param mqtt_topic: ``CfnDetectorModel.IotTopicPublishProperty.MqttTopic``.
            :param payload: ``CfnDetectorModel.IotTopicPublishProperty.Payload``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iottopicpublish.html
            """
            self._values = {
            }
            if mqtt_topic is not None: self._values["mqtt_topic"] = mqtt_topic
            if payload is not None: self._values["payload"] = payload

        @builtins.property
        def mqtt_topic(self) -> typing.Optional[str]:
            """``CfnDetectorModel.IotTopicPublishProperty.MqttTopic``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iottopicpublish.html#cfn-iotevents-detectormodel-iottopicpublish-mqtttopic
            """
            return self._values.get('mqtt_topic')

        @builtins.property
        def payload(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.PayloadProperty"]]:
            """``CfnDetectorModel.IotTopicPublishProperty.Payload``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iottopicpublish.html#cfn-iotevents-detectormodel-iottopicpublish-payload
            """
            return self._values.get('payload')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'IotTopicPublishProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.LambdaProperty", jsii_struct_bases=[], name_mapping={'function_arn': 'functionArn', 'payload': 'payload'})
    class LambdaProperty():
        def __init__(self, *, function_arn: typing.Optional[str]=None, payload: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.PayloadProperty"]]=None) -> None:
            """
            :param function_arn: ``CfnDetectorModel.LambdaProperty.FunctionArn``.
            :param payload: ``CfnDetectorModel.LambdaProperty.Payload``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-lambda.html
            """
            self._values = {
            }
            if function_arn is not None: self._values["function_arn"] = function_arn
            if payload is not None: self._values["payload"] = payload

        @builtins.property
        def function_arn(self) -> typing.Optional[str]:
            """``CfnDetectorModel.LambdaProperty.FunctionArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-lambda.html#cfn-iotevents-detectormodel-lambda-functionarn
            """
            return self._values.get('function_arn')

        @builtins.property
        def payload(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.PayloadProperty"]]:
            """``CfnDetectorModel.LambdaProperty.Payload``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-lambda.html#cfn-iotevents-detectormodel-lambda-payload
            """
            return self._values.get('payload')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LambdaProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.OnEnterProperty", jsii_struct_bases=[], name_mapping={'events': 'events'})
    class OnEnterProperty():
        def __init__(self, *, events: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.EventProperty"]]]]=None) -> None:
            """
            :param events: ``CfnDetectorModel.OnEnterProperty.Events``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-onenter.html
            """
            self._values = {
            }
            if events is not None: self._values["events"] = events

        @builtins.property
        def events(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.EventProperty"]]]]:
            """``CfnDetectorModel.OnEnterProperty.Events``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-onenter.html#cfn-iotevents-detectormodel-onenter-events
            """
            return self._values.get('events')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'OnEnterProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.OnExitProperty", jsii_struct_bases=[], name_mapping={'events': 'events'})
    class OnExitProperty():
        def __init__(self, *, events: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.EventProperty"]]]]=None) -> None:
            """
            :param events: ``CfnDetectorModel.OnExitProperty.Events``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-onexit.html
            """
            self._values = {
            }
            if events is not None: self._values["events"] = events

        @builtins.property
        def events(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.EventProperty"]]]]:
            """``CfnDetectorModel.OnExitProperty.Events``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-onexit.html#cfn-iotevents-detectormodel-onexit-events
            """
            return self._values.get('events')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'OnExitProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.OnInputProperty", jsii_struct_bases=[], name_mapping={'events': 'events', 'transition_events': 'transitionEvents'})
    class OnInputProperty():
        def __init__(self, *, events: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.EventProperty"]]]]=None, transition_events: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.TransitionEventProperty"]]]]=None) -> None:
            """
            :param events: ``CfnDetectorModel.OnInputProperty.Events``.
            :param transition_events: ``CfnDetectorModel.OnInputProperty.TransitionEvents``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-oninput.html
            """
            self._values = {
            }
            if events is not None: self._values["events"] = events
            if transition_events is not None: self._values["transition_events"] = transition_events

        @builtins.property
        def events(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.EventProperty"]]]]:
            """``CfnDetectorModel.OnInputProperty.Events``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-oninput.html#cfn-iotevents-detectormodel-oninput-events
            """
            return self._values.get('events')

        @builtins.property
        def transition_events(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.TransitionEventProperty"]]]]:
            """``CfnDetectorModel.OnInputProperty.TransitionEvents``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-oninput.html#cfn-iotevents-detectormodel-oninput-transitionevents
            """
            return self._values.get('transition_events')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'OnInputProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.PayloadProperty", jsii_struct_bases=[], name_mapping={'content_expression': 'contentExpression', 'type': 'type'})
    class PayloadProperty():
        def __init__(self, *, content_expression: typing.Optional[str]=None, type: typing.Optional[str]=None) -> None:
            """
            :param content_expression: ``CfnDetectorModel.PayloadProperty.ContentExpression``.
            :param type: ``CfnDetectorModel.PayloadProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-payload.html
            """
            self._values = {
            }
            if content_expression is not None: self._values["content_expression"] = content_expression
            if type is not None: self._values["type"] = type

        @builtins.property
        def content_expression(self) -> typing.Optional[str]:
            """``CfnDetectorModel.PayloadProperty.ContentExpression``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-payload.html#cfn-iotevents-detectormodel-payload-contentexpression
            """
            return self._values.get('content_expression')

        @builtins.property
        def type(self) -> typing.Optional[str]:
            """``CfnDetectorModel.PayloadProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-payload.html#cfn-iotevents-detectormodel-payload-type
            """
            return self._values.get('type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PayloadProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.ResetTimerProperty", jsii_struct_bases=[], name_mapping={'timer_name': 'timerName'})
    class ResetTimerProperty():
        def __init__(self, *, timer_name: typing.Optional[str]=None) -> None:
            """
            :param timer_name: ``CfnDetectorModel.ResetTimerProperty.TimerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-resettimer.html
            """
            self._values = {
            }
            if timer_name is not None: self._values["timer_name"] = timer_name

        @builtins.property
        def timer_name(self) -> typing.Optional[str]:
            """``CfnDetectorModel.ResetTimerProperty.TimerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-resettimer.html#cfn-iotevents-detectormodel-resettimer-timername
            """
            return self._values.get('timer_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ResetTimerProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.SetTimerProperty", jsii_struct_bases=[], name_mapping={'duration_expression': 'durationExpression', 'seconds': 'seconds', 'timer_name': 'timerName'})
    class SetTimerProperty():
        def __init__(self, *, duration_expression: typing.Optional[str]=None, seconds: typing.Optional[jsii.Number]=None, timer_name: typing.Optional[str]=None) -> None:
            """
            :param duration_expression: ``CfnDetectorModel.SetTimerProperty.DurationExpression``.
            :param seconds: ``CfnDetectorModel.SetTimerProperty.Seconds``.
            :param timer_name: ``CfnDetectorModel.SetTimerProperty.TimerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-settimer.html
            """
            self._values = {
            }
            if duration_expression is not None: self._values["duration_expression"] = duration_expression
            if seconds is not None: self._values["seconds"] = seconds
            if timer_name is not None: self._values["timer_name"] = timer_name

        @builtins.property
        def duration_expression(self) -> typing.Optional[str]:
            """``CfnDetectorModel.SetTimerProperty.DurationExpression``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-settimer.html#cfn-iotevents-detectormodel-settimer-durationexpression
            """
            return self._values.get('duration_expression')

        @builtins.property
        def seconds(self) -> typing.Optional[jsii.Number]:
            """``CfnDetectorModel.SetTimerProperty.Seconds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-settimer.html#cfn-iotevents-detectormodel-settimer-seconds
            """
            return self._values.get('seconds')

        @builtins.property
        def timer_name(self) -> typing.Optional[str]:
            """``CfnDetectorModel.SetTimerProperty.TimerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-settimer.html#cfn-iotevents-detectormodel-settimer-timername
            """
            return self._values.get('timer_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SetTimerProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.SetVariableProperty", jsii_struct_bases=[], name_mapping={'value': 'value', 'variable_name': 'variableName'})
    class SetVariableProperty():
        def __init__(self, *, value: typing.Optional[str]=None, variable_name: typing.Optional[str]=None) -> None:
            """
            :param value: ``CfnDetectorModel.SetVariableProperty.Value``.
            :param variable_name: ``CfnDetectorModel.SetVariableProperty.VariableName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-setvariable.html
            """
            self._values = {
            }
            if value is not None: self._values["value"] = value
            if variable_name is not None: self._values["variable_name"] = variable_name

        @builtins.property
        def value(self) -> typing.Optional[str]:
            """``CfnDetectorModel.SetVariableProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-setvariable.html#cfn-iotevents-detectormodel-setvariable-value
            """
            return self._values.get('value')

        @builtins.property
        def variable_name(self) -> typing.Optional[str]:
            """``CfnDetectorModel.SetVariableProperty.VariableName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-setvariable.html#cfn-iotevents-detectormodel-setvariable-variablename
            """
            return self._values.get('variable_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SetVariableProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.SnsProperty", jsii_struct_bases=[], name_mapping={'payload': 'payload', 'target_arn': 'targetArn'})
    class SnsProperty():
        def __init__(self, *, payload: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.PayloadProperty"]]=None, target_arn: typing.Optional[str]=None) -> None:
            """
            :param payload: ``CfnDetectorModel.SnsProperty.Payload``.
            :param target_arn: ``CfnDetectorModel.SnsProperty.TargetArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sns.html
            """
            self._values = {
            }
            if payload is not None: self._values["payload"] = payload
            if target_arn is not None: self._values["target_arn"] = target_arn

        @builtins.property
        def payload(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.PayloadProperty"]]:
            """``CfnDetectorModel.SnsProperty.Payload``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sns.html#cfn-iotevents-detectormodel-sns-payload
            """
            return self._values.get('payload')

        @builtins.property
        def target_arn(self) -> typing.Optional[str]:
            """``CfnDetectorModel.SnsProperty.TargetArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sns.html#cfn-iotevents-detectormodel-sns-targetarn
            """
            return self._values.get('target_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SnsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.SqsProperty", jsii_struct_bases=[], name_mapping={'payload': 'payload', 'queue_url': 'queueUrl', 'use_base64': 'useBase64'})
    class SqsProperty():
        def __init__(self, *, payload: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.PayloadProperty"]]=None, queue_url: typing.Optional[str]=None, use_base64: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]=None) -> None:
            """
            :param payload: ``CfnDetectorModel.SqsProperty.Payload``.
            :param queue_url: ``CfnDetectorModel.SqsProperty.QueueUrl``.
            :param use_base64: ``CfnDetectorModel.SqsProperty.UseBase64``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sqs.html
            """
            self._values = {
            }
            if payload is not None: self._values["payload"] = payload
            if queue_url is not None: self._values["queue_url"] = queue_url
            if use_base64 is not None: self._values["use_base64"] = use_base64

        @builtins.property
        def payload(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.PayloadProperty"]]:
            """``CfnDetectorModel.SqsProperty.Payload``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sqs.html#cfn-iotevents-detectormodel-sqs-payload
            """
            return self._values.get('payload')

        @builtins.property
        def queue_url(self) -> typing.Optional[str]:
            """``CfnDetectorModel.SqsProperty.QueueUrl``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sqs.html#cfn-iotevents-detectormodel-sqs-queueurl
            """
            return self._values.get('queue_url')

        @builtins.property
        def use_base64(self) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
            """``CfnDetectorModel.SqsProperty.UseBase64``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sqs.html#cfn-iotevents-detectormodel-sqs-usebase64
            """
            return self._values.get('use_base64')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SqsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.StateProperty", jsii_struct_bases=[], name_mapping={'on_enter': 'onEnter', 'on_exit': 'onExit', 'on_input': 'onInput', 'state_name': 'stateName'})
    class StateProperty():
        def __init__(self, *, on_enter: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.OnEnterProperty"]]=None, on_exit: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.OnExitProperty"]]=None, on_input: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.OnInputProperty"]]=None, state_name: typing.Optional[str]=None) -> None:
            """
            :param on_enter: ``CfnDetectorModel.StateProperty.OnEnter``.
            :param on_exit: ``CfnDetectorModel.StateProperty.OnExit``.
            :param on_input: ``CfnDetectorModel.StateProperty.OnInput``.
            :param state_name: ``CfnDetectorModel.StateProperty.StateName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-state.html
            """
            self._values = {
            }
            if on_enter is not None: self._values["on_enter"] = on_enter
            if on_exit is not None: self._values["on_exit"] = on_exit
            if on_input is not None: self._values["on_input"] = on_input
            if state_name is not None: self._values["state_name"] = state_name

        @builtins.property
        def on_enter(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.OnEnterProperty"]]:
            """``CfnDetectorModel.StateProperty.OnEnter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-state.html#cfn-iotevents-detectormodel-state-onenter
            """
            return self._values.get('on_enter')

        @builtins.property
        def on_exit(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.OnExitProperty"]]:
            """``CfnDetectorModel.StateProperty.OnExit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-state.html#cfn-iotevents-detectormodel-state-onexit
            """
            return self._values.get('on_exit')

        @builtins.property
        def on_input(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.OnInputProperty"]]:
            """``CfnDetectorModel.StateProperty.OnInput``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-state.html#cfn-iotevents-detectormodel-state-oninput
            """
            return self._values.get('on_input')

        @builtins.property
        def state_name(self) -> typing.Optional[str]:
            """``CfnDetectorModel.StateProperty.StateName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-state.html#cfn-iotevents-detectormodel-state-statename
            """
            return self._values.get('state_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'StateProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.TransitionEventProperty", jsii_struct_bases=[], name_mapping={'actions': 'actions', 'condition': 'condition', 'event_name': 'eventName', 'next_state': 'nextState'})
    class TransitionEventProperty():
        def __init__(self, *, actions: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.ActionProperty"]]]]=None, condition: typing.Optional[str]=None, event_name: typing.Optional[str]=None, next_state: typing.Optional[str]=None) -> None:
            """
            :param actions: ``CfnDetectorModel.TransitionEventProperty.Actions``.
            :param condition: ``CfnDetectorModel.TransitionEventProperty.Condition``.
            :param event_name: ``CfnDetectorModel.TransitionEventProperty.EventName``.
            :param next_state: ``CfnDetectorModel.TransitionEventProperty.NextState``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-transitionevent.html
            """
            self._values = {
            }
            if actions is not None: self._values["actions"] = actions
            if condition is not None: self._values["condition"] = condition
            if event_name is not None: self._values["event_name"] = event_name
            if next_state is not None: self._values["next_state"] = next_state

        @builtins.property
        def actions(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDetectorModel.ActionProperty"]]]]:
            """``CfnDetectorModel.TransitionEventProperty.Actions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-transitionevent.html#cfn-iotevents-detectormodel-transitionevent-actions
            """
            return self._values.get('actions')

        @builtins.property
        def condition(self) -> typing.Optional[str]:
            """``CfnDetectorModel.TransitionEventProperty.Condition``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-transitionevent.html#cfn-iotevents-detectormodel-transitionevent-condition
            """
            return self._values.get('condition')

        @builtins.property
        def event_name(self) -> typing.Optional[str]:
            """``CfnDetectorModel.TransitionEventProperty.EventName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-transitionevent.html#cfn-iotevents-detectormodel-transitionevent-eventname
            """
            return self._values.get('event_name')

        @builtins.property
        def next_state(self) -> typing.Optional[str]:
            """``CfnDetectorModel.TransitionEventProperty.NextState``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-transitionevent.html#cfn-iotevents-detectormodel-transitionevent-nextstate
            """
            return self._values.get('next_state')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TransitionEventProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModelProps", jsii_struct_bases=[], name_mapping={'detector_model_definition': 'detectorModelDefinition', 'detector_model_description': 'detectorModelDescription', 'detector_model_name': 'detectorModelName', 'evaluation_method': 'evaluationMethod', 'key': 'key', 'role_arn': 'roleArn', 'tags': 'tags'})
class CfnDetectorModelProps():
    def __init__(self, *, detector_model_definition: typing.Optional[typing.Union["CfnDetectorModel.DetectorModelDefinitionProperty", aws_cdk.core.IResolvable]]=None, detector_model_description: typing.Optional[str]=None, detector_model_name: typing.Optional[str]=None, evaluation_method: typing.Optional[str]=None, key: typing.Optional[str]=None, role_arn: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Properties for defining a ``AWS::IoTEvents::DetectorModel``.

        :param detector_model_definition: ``AWS::IoTEvents::DetectorModel.DetectorModelDefinition``.
        :param detector_model_description: ``AWS::IoTEvents::DetectorModel.DetectorModelDescription``.
        :param detector_model_name: ``AWS::IoTEvents::DetectorModel.DetectorModelName``.
        :param evaluation_method: ``AWS::IoTEvents::DetectorModel.EvaluationMethod``.
        :param key: ``AWS::IoTEvents::DetectorModel.Key``.
        :param role_arn: ``AWS::IoTEvents::DetectorModel.RoleArn``.
        :param tags: ``AWS::IoTEvents::DetectorModel.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html
        """
        self._values = {
        }
        if detector_model_definition is not None: self._values["detector_model_definition"] = detector_model_definition
        if detector_model_description is not None: self._values["detector_model_description"] = detector_model_description
        if detector_model_name is not None: self._values["detector_model_name"] = detector_model_name
        if evaluation_method is not None: self._values["evaluation_method"] = evaluation_method
        if key is not None: self._values["key"] = key
        if role_arn is not None: self._values["role_arn"] = role_arn
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def detector_model_definition(self) -> typing.Optional[typing.Union["CfnDetectorModel.DetectorModelDefinitionProperty", aws_cdk.core.IResolvable]]:
        """``AWS::IoTEvents::DetectorModel.DetectorModelDefinition``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-detectormodeldefinition
        """
        return self._values.get('detector_model_definition')

    @builtins.property
    def detector_model_description(self) -> typing.Optional[str]:
        """``AWS::IoTEvents::DetectorModel.DetectorModelDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-detectormodeldescription
        """
        return self._values.get('detector_model_description')

    @builtins.property
    def detector_model_name(self) -> typing.Optional[str]:
        """``AWS::IoTEvents::DetectorModel.DetectorModelName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-detectormodelname
        """
        return self._values.get('detector_model_name')

    @builtins.property
    def evaluation_method(self) -> typing.Optional[str]:
        """``AWS::IoTEvents::DetectorModel.EvaluationMethod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-evaluationmethod
        """
        return self._values.get('evaluation_method')

    @builtins.property
    def key(self) -> typing.Optional[str]:
        """``AWS::IoTEvents::DetectorModel.Key``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-key
        """
        return self._values.get('key')

    @builtins.property
    def role_arn(self) -> typing.Optional[str]:
        """``AWS::IoTEvents::DetectorModel.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-rolearn
        """
        return self._values.get('role_arn')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::IoTEvents::DetectorModel.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDetectorModelProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnInput(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iotevents.CfnInput"):
    """A CloudFormation ``AWS::IoTEvents::Input``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html
    cloudformationResource:
    :cloudformationResource:: AWS::IoTEvents::Input
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, input_definition: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "InputDefinitionProperty"]]=None, input_description: typing.Optional[str]=None, input_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::IoTEvents::Input``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param input_definition: ``AWS::IoTEvents::Input.InputDefinition``.
        :param input_description: ``AWS::IoTEvents::Input.InputDescription``.
        :param input_name: ``AWS::IoTEvents::Input.InputName``.
        :param tags: ``AWS::IoTEvents::Input.Tags``.
        """
        props = CfnInputProps(input_definition=input_definition, input_description=input_description, input_name=input_name, tags=tags)

        jsii.create(CfnInput, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnInput":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
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
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::IoTEvents::Input.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html#cfn-iotevents-input-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="inputDefinition")
    def input_definition(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "InputDefinitionProperty"]]:
        """``AWS::IoTEvents::Input.InputDefinition``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html#cfn-iotevents-input-inputdefinition
        """
        return jsii.get(self, "inputDefinition")

    @input_definition.setter
    def input_definition(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "InputDefinitionProperty"]]) -> None:
        jsii.set(self, "inputDefinition", value)

    @builtins.property
    @jsii.member(jsii_name="inputDescription")
    def input_description(self) -> typing.Optional[str]:
        """``AWS::IoTEvents::Input.InputDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html#cfn-iotevents-input-inputdescription
        """
        return jsii.get(self, "inputDescription")

    @input_description.setter
    def input_description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "inputDescription", value)

    @builtins.property
    @jsii.member(jsii_name="inputName")
    def input_name(self) -> typing.Optional[str]:
        """``AWS::IoTEvents::Input.InputName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html#cfn-iotevents-input-inputname
        """
        return jsii.get(self, "inputName")

    @input_name.setter
    def input_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "inputName", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnInput.AttributeProperty", jsii_struct_bases=[], name_mapping={'json_path': 'jsonPath'})
    class AttributeProperty():
        def __init__(self, *, json_path: typing.Optional[str]=None) -> None:
            """
            :param json_path: ``CfnInput.AttributeProperty.JsonPath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-input-attribute.html
            """
            self._values = {
            }
            if json_path is not None: self._values["json_path"] = json_path

        @builtins.property
        def json_path(self) -> typing.Optional[str]:
            """``CfnInput.AttributeProperty.JsonPath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-input-attribute.html#cfn-iotevents-input-attribute-jsonpath
            """
            return self._values.get('json_path')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AttributeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnInput.InputDefinitionProperty", jsii_struct_bases=[], name_mapping={'attributes': 'attributes'})
    class InputDefinitionProperty():
        def __init__(self, *, attributes: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnInput.AttributeProperty"]]]]=None) -> None:
            """
            :param attributes: ``CfnInput.InputDefinitionProperty.Attributes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-input-inputdefinition.html
            """
            self._values = {
            }
            if attributes is not None: self._values["attributes"] = attributes

        @builtins.property
        def attributes(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnInput.AttributeProperty"]]]]:
            """``CfnInput.InputDefinitionProperty.Attributes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-input-inputdefinition.html#cfn-iotevents-input-inputdefinition-attributes
            """
            return self._values.get('attributes')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'InputDefinitionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-iotevents.CfnInputProps", jsii_struct_bases=[], name_mapping={'input_definition': 'inputDefinition', 'input_description': 'inputDescription', 'input_name': 'inputName', 'tags': 'tags'})
class CfnInputProps():
    def __init__(self, *, input_definition: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnInput.InputDefinitionProperty"]]=None, input_description: typing.Optional[str]=None, input_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Properties for defining a ``AWS::IoTEvents::Input``.

        :param input_definition: ``AWS::IoTEvents::Input.InputDefinition``.
        :param input_description: ``AWS::IoTEvents::Input.InputDescription``.
        :param input_name: ``AWS::IoTEvents::Input.InputName``.
        :param tags: ``AWS::IoTEvents::Input.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html
        """
        self._values = {
        }
        if input_definition is not None: self._values["input_definition"] = input_definition
        if input_description is not None: self._values["input_description"] = input_description
        if input_name is not None: self._values["input_name"] = input_name
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def input_definition(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnInput.InputDefinitionProperty"]]:
        """``AWS::IoTEvents::Input.InputDefinition``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html#cfn-iotevents-input-inputdefinition
        """
        return self._values.get('input_definition')

    @builtins.property
    def input_description(self) -> typing.Optional[str]:
        """``AWS::IoTEvents::Input.InputDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html#cfn-iotevents-input-inputdescription
        """
        return self._values.get('input_description')

    @builtins.property
    def input_name(self) -> typing.Optional[str]:
        """``AWS::IoTEvents::Input.InputName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html#cfn-iotevents-input-inputname
        """
        return self._values.get('input_name')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::IoTEvents::Input.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html#cfn-iotevents-input-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnInputProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnDetectorModel",
    "CfnDetectorModelProps",
    "CfnInput",
    "CfnInputProps",
]

publication.publish()
