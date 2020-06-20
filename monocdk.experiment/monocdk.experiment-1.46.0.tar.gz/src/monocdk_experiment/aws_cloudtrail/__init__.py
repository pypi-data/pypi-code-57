import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (CfnResource as _CfnResource_7760e8e4, Construct as _Construct_f50a3f53, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, TagManager as _TagManager_2508893f, IResolvable as _IResolvable_9ceae33e, IInspectable as _IInspectable_051e6ed8, CfnTag as _CfnTag_b4661f1a, Resource as _Resource_884d0774)
from ..aws_events import (Rule as _Rule_c38e0b39, OnEventOptions as _OnEventOptions_926fbcf9)
from ..aws_kms import (IKey as _IKey_3336c79d)
from ..aws_lambda import (IFunction as _IFunction_1c1de0bc)
from ..aws_logs import (ILogGroup as _ILogGroup_6b54c8e1, RetentionDays as _RetentionDays_bdc7ad1f)
from ..aws_s3 import (IBucket as _IBucket_25bad983)
from ..aws_sns import (ITopic as _ITopic_ef0ebe0e)


@jsii.data_type(jsii_type="monocdk-experiment.aws_cloudtrail.AddEventSelectorOptions", jsii_struct_bases=[], name_mapping={'include_management_events': 'includeManagementEvents', 'read_write_type': 'readWriteType'})
class AddEventSelectorOptions():
    def __init__(self, *, include_management_events: typing.Optional[bool]=None, read_write_type: typing.Optional["ReadWriteType"]=None) -> None:
        """Options for adding an event selector.

        :param include_management_events: Specifies whether the event selector includes management events for the trail. Default: true
        :param read_write_type: Specifies whether to log read-only events, write-only events, or all events. Default: ReadWriteType.All

        stability
        :stability: experimental
        """
        self._values = {
        }
        if include_management_events is not None: self._values["include_management_events"] = include_management_events
        if read_write_type is not None: self._values["read_write_type"] = read_write_type

    @builtins.property
    def include_management_events(self) -> typing.Optional[bool]:
        """Specifies whether the event selector includes management events for the trail.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('include_management_events')

    @builtins.property
    def read_write_type(self) -> typing.Optional["ReadWriteType"]:
        """Specifies whether to log read-only events, write-only events, or all events.

        default
        :default: ReadWriteType.All

        stability
        :stability: experimental
        """
        return self._values.get('read_write_type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AddEventSelectorOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnTrail(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_cloudtrail.CfnTrail"):
    """A CloudFormation ``AWS::CloudTrail::Trail``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html
    cloudformationResource:
    :cloudformationResource:: AWS::CloudTrail::Trail
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, is_logging: typing.Union[bool, _IResolvable_9ceae33e], s3_bucket_name: str, cloud_watch_logs_log_group_arn: typing.Optional[str]=None, cloud_watch_logs_role_arn: typing.Optional[str]=None, enable_log_file_validation: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, event_selectors: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["EventSelectorProperty", _IResolvable_9ceae33e]]]]=None, include_global_service_events: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, is_multi_region_trail: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, kms_key_id: typing.Optional[str]=None, s3_key_prefix: typing.Optional[str]=None, sns_topic_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None, trail_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::CloudTrail::Trail``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param is_logging: ``AWS::CloudTrail::Trail.IsLogging``.
        :param s3_bucket_name: ``AWS::CloudTrail::Trail.S3BucketName``.
        :param cloud_watch_logs_log_group_arn: ``AWS::CloudTrail::Trail.CloudWatchLogsLogGroupArn``.
        :param cloud_watch_logs_role_arn: ``AWS::CloudTrail::Trail.CloudWatchLogsRoleArn``.
        :param enable_log_file_validation: ``AWS::CloudTrail::Trail.EnableLogFileValidation``.
        :param event_selectors: ``AWS::CloudTrail::Trail.EventSelectors``.
        :param include_global_service_events: ``AWS::CloudTrail::Trail.IncludeGlobalServiceEvents``.
        :param is_multi_region_trail: ``AWS::CloudTrail::Trail.IsMultiRegionTrail``.
        :param kms_key_id: ``AWS::CloudTrail::Trail.KMSKeyId``.
        :param s3_key_prefix: ``AWS::CloudTrail::Trail.S3KeyPrefix``.
        :param sns_topic_name: ``AWS::CloudTrail::Trail.SnsTopicName``.
        :param tags: ``AWS::CloudTrail::Trail.Tags``.
        :param trail_name: ``AWS::CloudTrail::Trail.TrailName``.
        """
        props = CfnTrailProps(is_logging=is_logging, s3_bucket_name=s3_bucket_name, cloud_watch_logs_log_group_arn=cloud_watch_logs_log_group_arn, cloud_watch_logs_role_arn=cloud_watch_logs_role_arn, enable_log_file_validation=enable_log_file_validation, event_selectors=event_selectors, include_global_service_events=include_global_service_events, is_multi_region_trail=is_multi_region_trail, kms_key_id=kms_key_id, s3_key_prefix=s3_key_prefix, sns_topic_name=sns_topic_name, tags=tags, trail_name=trail_name)

        jsii.create(CfnTrail, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnTrail":
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
    @jsii.member(jsii_name="attrSnsTopicArn")
    def attr_sns_topic_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: SnsTopicArn
        """
        return jsii.get(self, "attrSnsTopicArn")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::CloudTrail::Trail.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="isLogging")
    def is_logging(self) -> typing.Union[bool, _IResolvable_9ceae33e]:
        """``AWS::CloudTrail::Trail.IsLogging``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-islogging
        """
        return jsii.get(self, "isLogging")

    @is_logging.setter
    def is_logging(self, value: typing.Union[bool, _IResolvable_9ceae33e]) -> None:
        jsii.set(self, "isLogging", value)

    @builtins.property
    @jsii.member(jsii_name="s3BucketName")
    def s3_bucket_name(self) -> str:
        """``AWS::CloudTrail::Trail.S3BucketName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-s3bucketname
        """
        return jsii.get(self, "s3BucketName")

    @s3_bucket_name.setter
    def s3_bucket_name(self, value: str) -> None:
        jsii.set(self, "s3BucketName", value)

    @builtins.property
    @jsii.member(jsii_name="cloudWatchLogsLogGroupArn")
    def cloud_watch_logs_log_group_arn(self) -> typing.Optional[str]:
        """``AWS::CloudTrail::Trail.CloudWatchLogsLogGroupArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-cloudwatchlogsloggrouparn
        """
        return jsii.get(self, "cloudWatchLogsLogGroupArn")

    @cloud_watch_logs_log_group_arn.setter
    def cloud_watch_logs_log_group_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "cloudWatchLogsLogGroupArn", value)

    @builtins.property
    @jsii.member(jsii_name="cloudWatchLogsRoleArn")
    def cloud_watch_logs_role_arn(self) -> typing.Optional[str]:
        """``AWS::CloudTrail::Trail.CloudWatchLogsRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-cloudwatchlogsrolearn
        """
        return jsii.get(self, "cloudWatchLogsRoleArn")

    @cloud_watch_logs_role_arn.setter
    def cloud_watch_logs_role_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "cloudWatchLogsRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="enableLogFileValidation")
    def enable_log_file_validation(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::CloudTrail::Trail.EnableLogFileValidation``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-enablelogfilevalidation
        """
        return jsii.get(self, "enableLogFileValidation")

    @enable_log_file_validation.setter
    def enable_log_file_validation(self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "enableLogFileValidation", value)

    @builtins.property
    @jsii.member(jsii_name="eventSelectors")
    def event_selectors(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["EventSelectorProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::CloudTrail::Trail.EventSelectors``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-eventselectors
        """
        return jsii.get(self, "eventSelectors")

    @event_selectors.setter
    def event_selectors(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["EventSelectorProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "eventSelectors", value)

    @builtins.property
    @jsii.member(jsii_name="includeGlobalServiceEvents")
    def include_global_service_events(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::CloudTrail::Trail.IncludeGlobalServiceEvents``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-includeglobalserviceevents
        """
        return jsii.get(self, "includeGlobalServiceEvents")

    @include_global_service_events.setter
    def include_global_service_events(self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "includeGlobalServiceEvents", value)

    @builtins.property
    @jsii.member(jsii_name="isMultiRegionTrail")
    def is_multi_region_trail(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::CloudTrail::Trail.IsMultiRegionTrail``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-ismultiregiontrail
        """
        return jsii.get(self, "isMultiRegionTrail")

    @is_multi_region_trail.setter
    def is_multi_region_trail(self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "isMultiRegionTrail", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::CloudTrail::Trail.KMSKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-kmskeyid
        """
        return jsii.get(self, "kmsKeyId")

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="s3KeyPrefix")
    def s3_key_prefix(self) -> typing.Optional[str]:
        """``AWS::CloudTrail::Trail.S3KeyPrefix``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-s3keyprefix
        """
        return jsii.get(self, "s3KeyPrefix")

    @s3_key_prefix.setter
    def s3_key_prefix(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "s3KeyPrefix", value)

    @builtins.property
    @jsii.member(jsii_name="snsTopicName")
    def sns_topic_name(self) -> typing.Optional[str]:
        """``AWS::CloudTrail::Trail.SnsTopicName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-snstopicname
        """
        return jsii.get(self, "snsTopicName")

    @sns_topic_name.setter
    def sns_topic_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "snsTopicName", value)

    @builtins.property
    @jsii.member(jsii_name="trailName")
    def trail_name(self) -> typing.Optional[str]:
        """``AWS::CloudTrail::Trail.TrailName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-trailname
        """
        return jsii.get(self, "trailName")

    @trail_name.setter
    def trail_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "trailName", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_cloudtrail.CfnTrail.DataResourceProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'values': 'values'})
    class DataResourceProperty():
        def __init__(self, *, type: str, values: typing.Optional[typing.List[str]]=None) -> None:
            """
            :param type: ``CfnTrail.DataResourceProperty.Type``.
            :param values: ``CfnTrail.DataResourceProperty.Values``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-dataresource.html
            """
            self._values = {
                'type': type,
            }
            if values is not None: self._values["values"] = values

        @builtins.property
        def type(self) -> str:
            """``CfnTrail.DataResourceProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-dataresource.html#cfn-cloudtrail-trail-dataresource-type
            """
            return self._values.get('type')

        @builtins.property
        def values(self) -> typing.Optional[typing.List[str]]:
            """``CfnTrail.DataResourceProperty.Values``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-dataresource.html#cfn-cloudtrail-trail-dataresource-values
            """
            return self._values.get('values')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DataResourceProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_cloudtrail.CfnTrail.EventSelectorProperty", jsii_struct_bases=[], name_mapping={'data_resources': 'dataResources', 'include_management_events': 'includeManagementEvents', 'read_write_type': 'readWriteType'})
    class EventSelectorProperty():
        def __init__(self, *, data_resources: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTrail.DataResourceProperty", _IResolvable_9ceae33e]]]]=None, include_management_events: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, read_write_type: typing.Optional[str]=None) -> None:
            """
            :param data_resources: ``CfnTrail.EventSelectorProperty.DataResources``.
            :param include_management_events: ``CfnTrail.EventSelectorProperty.IncludeManagementEvents``.
            :param read_write_type: ``CfnTrail.EventSelectorProperty.ReadWriteType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-eventselector.html
            """
            self._values = {
            }
            if data_resources is not None: self._values["data_resources"] = data_resources
            if include_management_events is not None: self._values["include_management_events"] = include_management_events
            if read_write_type is not None: self._values["read_write_type"] = read_write_type

        @builtins.property
        def data_resources(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTrail.DataResourceProperty", _IResolvable_9ceae33e]]]]:
            """``CfnTrail.EventSelectorProperty.DataResources``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-eventselector.html#cfn-cloudtrail-trail-eventselector-dataresources
            """
            return self._values.get('data_resources')

        @builtins.property
        def include_management_events(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnTrail.EventSelectorProperty.IncludeManagementEvents``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-eventselector.html#cfn-cloudtrail-trail-eventselector-includemanagementevents
            """
            return self._values.get('include_management_events')

        @builtins.property
        def read_write_type(self) -> typing.Optional[str]:
            """``CfnTrail.EventSelectorProperty.ReadWriteType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-eventselector.html#cfn-cloudtrail-trail-eventselector-readwritetype
            """
            return self._values.get('read_write_type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EventSelectorProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_cloudtrail.CfnTrailProps", jsii_struct_bases=[], name_mapping={'is_logging': 'isLogging', 's3_bucket_name': 's3BucketName', 'cloud_watch_logs_log_group_arn': 'cloudWatchLogsLogGroupArn', 'cloud_watch_logs_role_arn': 'cloudWatchLogsRoleArn', 'enable_log_file_validation': 'enableLogFileValidation', 'event_selectors': 'eventSelectors', 'include_global_service_events': 'includeGlobalServiceEvents', 'is_multi_region_trail': 'isMultiRegionTrail', 'kms_key_id': 'kmsKeyId', 's3_key_prefix': 's3KeyPrefix', 'sns_topic_name': 'snsTopicName', 'tags': 'tags', 'trail_name': 'trailName'})
class CfnTrailProps():
    def __init__(self, *, is_logging: typing.Union[bool, _IResolvable_9ceae33e], s3_bucket_name: str, cloud_watch_logs_log_group_arn: typing.Optional[str]=None, cloud_watch_logs_role_arn: typing.Optional[str]=None, enable_log_file_validation: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, event_selectors: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTrail.EventSelectorProperty", _IResolvable_9ceae33e]]]]=None, include_global_service_events: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, is_multi_region_trail: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, kms_key_id: typing.Optional[str]=None, s3_key_prefix: typing.Optional[str]=None, sns_topic_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None, trail_name: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::CloudTrail::Trail``.

        :param is_logging: ``AWS::CloudTrail::Trail.IsLogging``.
        :param s3_bucket_name: ``AWS::CloudTrail::Trail.S3BucketName``.
        :param cloud_watch_logs_log_group_arn: ``AWS::CloudTrail::Trail.CloudWatchLogsLogGroupArn``.
        :param cloud_watch_logs_role_arn: ``AWS::CloudTrail::Trail.CloudWatchLogsRoleArn``.
        :param enable_log_file_validation: ``AWS::CloudTrail::Trail.EnableLogFileValidation``.
        :param event_selectors: ``AWS::CloudTrail::Trail.EventSelectors``.
        :param include_global_service_events: ``AWS::CloudTrail::Trail.IncludeGlobalServiceEvents``.
        :param is_multi_region_trail: ``AWS::CloudTrail::Trail.IsMultiRegionTrail``.
        :param kms_key_id: ``AWS::CloudTrail::Trail.KMSKeyId``.
        :param s3_key_prefix: ``AWS::CloudTrail::Trail.S3KeyPrefix``.
        :param sns_topic_name: ``AWS::CloudTrail::Trail.SnsTopicName``.
        :param tags: ``AWS::CloudTrail::Trail.Tags``.
        :param trail_name: ``AWS::CloudTrail::Trail.TrailName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html
        """
        self._values = {
            'is_logging': is_logging,
            's3_bucket_name': s3_bucket_name,
        }
        if cloud_watch_logs_log_group_arn is not None: self._values["cloud_watch_logs_log_group_arn"] = cloud_watch_logs_log_group_arn
        if cloud_watch_logs_role_arn is not None: self._values["cloud_watch_logs_role_arn"] = cloud_watch_logs_role_arn
        if enable_log_file_validation is not None: self._values["enable_log_file_validation"] = enable_log_file_validation
        if event_selectors is not None: self._values["event_selectors"] = event_selectors
        if include_global_service_events is not None: self._values["include_global_service_events"] = include_global_service_events
        if is_multi_region_trail is not None: self._values["is_multi_region_trail"] = is_multi_region_trail
        if kms_key_id is not None: self._values["kms_key_id"] = kms_key_id
        if s3_key_prefix is not None: self._values["s3_key_prefix"] = s3_key_prefix
        if sns_topic_name is not None: self._values["sns_topic_name"] = sns_topic_name
        if tags is not None: self._values["tags"] = tags
        if trail_name is not None: self._values["trail_name"] = trail_name

    @builtins.property
    def is_logging(self) -> typing.Union[bool, _IResolvable_9ceae33e]:
        """``AWS::CloudTrail::Trail.IsLogging``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-islogging
        """
        return self._values.get('is_logging')

    @builtins.property
    def s3_bucket_name(self) -> str:
        """``AWS::CloudTrail::Trail.S3BucketName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-s3bucketname
        """
        return self._values.get('s3_bucket_name')

    @builtins.property
    def cloud_watch_logs_log_group_arn(self) -> typing.Optional[str]:
        """``AWS::CloudTrail::Trail.CloudWatchLogsLogGroupArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-cloudwatchlogsloggrouparn
        """
        return self._values.get('cloud_watch_logs_log_group_arn')

    @builtins.property
    def cloud_watch_logs_role_arn(self) -> typing.Optional[str]:
        """``AWS::CloudTrail::Trail.CloudWatchLogsRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-cloudwatchlogsrolearn
        """
        return self._values.get('cloud_watch_logs_role_arn')

    @builtins.property
    def enable_log_file_validation(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::CloudTrail::Trail.EnableLogFileValidation``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-enablelogfilevalidation
        """
        return self._values.get('enable_log_file_validation')

    @builtins.property
    def event_selectors(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTrail.EventSelectorProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::CloudTrail::Trail.EventSelectors``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-eventselectors
        """
        return self._values.get('event_selectors')

    @builtins.property
    def include_global_service_events(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::CloudTrail::Trail.IncludeGlobalServiceEvents``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-includeglobalserviceevents
        """
        return self._values.get('include_global_service_events')

    @builtins.property
    def is_multi_region_trail(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::CloudTrail::Trail.IsMultiRegionTrail``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-ismultiregiontrail
        """
        return self._values.get('is_multi_region_trail')

    @builtins.property
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::CloudTrail::Trail.KMSKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-kmskeyid
        """
        return self._values.get('kms_key_id')

    @builtins.property
    def s3_key_prefix(self) -> typing.Optional[str]:
        """``AWS::CloudTrail::Trail.S3KeyPrefix``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-s3keyprefix
        """
        return self._values.get('s3_key_prefix')

    @builtins.property
    def sns_topic_name(self) -> typing.Optional[str]:
        """``AWS::CloudTrail::Trail.SnsTopicName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-snstopicname
        """
        return self._values.get('sns_topic_name')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::CloudTrail::Trail.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-tags
        """
        return self._values.get('tags')

    @builtins.property
    def trail_name(self) -> typing.Optional[str]:
        """``AWS::CloudTrail::Trail.TrailName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-trailname
        """
        return self._values.get('trail_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnTrailProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_cloudtrail.DataResourceType")
class DataResourceType(enum.Enum):
    """Resource type for a data event.

    stability
    :stability: experimental
    """
    LAMBDA_FUNCTION = "LAMBDA_FUNCTION"
    """Data resource type for Lambda function.

    stability
    :stability: experimental
    """
    S3_OBJECT = "S3_OBJECT"
    """Data resource type for S3 objects.

    stability
    :stability: experimental
    """

@jsii.enum(jsii_type="monocdk-experiment.aws_cloudtrail.ReadWriteType")
class ReadWriteType(enum.Enum):
    """Types of events that CloudTrail can log.

    stability
    :stability: experimental
    """
    READ_ONLY = "READ_ONLY"
    """Read-only events include API operations that read your resources, but don't make changes.

    For example, read-only events include the Amazon EC2 DescribeSecurityGroups
    and DescribeSubnets API operations.

    stability
    :stability: experimental
    """
    WRITE_ONLY = "WRITE_ONLY"
    """Write-only events include API operations that modify (or might modify) your resources.

    For example, the Amazon EC2 RunInstances and TerminateInstances API
    operations modify your instances.

    stability
    :stability: experimental
    """
    ALL = "ALL"
    """All events.

    stability
    :stability: experimental
    """
    NONE = "NONE"
    """No events.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.aws_cloudtrail.S3EventSelector", jsii_struct_bases=[], name_mapping={'bucket': 'bucket', 'object_prefix': 'objectPrefix'})
class S3EventSelector():
    def __init__(self, *, bucket: _IBucket_25bad983, object_prefix: typing.Optional[str]=None) -> None:
        """Selecting an S3 bucket and an optional prefix to be logged for data events.

        :param bucket: S3 bucket.
        :param object_prefix: Data events for objects whose key matches this prefix will be logged. Default: - all objects

        stability
        :stability: experimental
        """
        self._values = {
            'bucket': bucket,
        }
        if object_prefix is not None: self._values["object_prefix"] = object_prefix

    @builtins.property
    def bucket(self) -> _IBucket_25bad983:
        """S3 bucket.

        stability
        :stability: experimental
        """
        return self._values.get('bucket')

    @builtins.property
    def object_prefix(self) -> typing.Optional[str]:
        """Data events for objects whose key matches this prefix will be logged.

        default
        :default: - all objects

        stability
        :stability: experimental
        """
        return self._values.get('object_prefix')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'S3EventSelector(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Trail(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_cloudtrail.Trail"):
    """Cloud trail allows you to log events that happen in your AWS account For example:.

    import { CloudTrail } from '@aws-cdk/aws-cloudtrail'

    const cloudTrail = new CloudTrail(this, 'MyTrail');

    NOTE the above example creates an UNENCRYPTED bucket by default,
    If you are required to use an Encrypted bucket you can supply a preconfigured bucket
    via TrailProps

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, bucket: typing.Optional[_IBucket_25bad983]=None, cloud_watch_log_group: typing.Optional[_ILogGroup_6b54c8e1]=None, cloud_watch_logs_retention: typing.Optional[_RetentionDays_bdc7ad1f]=None, enable_file_validation: typing.Optional[bool]=None, encryption_key: typing.Optional[_IKey_3336c79d]=None, include_global_service_events: typing.Optional[bool]=None, is_multi_region_trail: typing.Optional[bool]=None, kms_key: typing.Optional[_IKey_3336c79d]=None, management_events: typing.Optional["ReadWriteType"]=None, s3_key_prefix: typing.Optional[str]=None, send_to_cloud_watch_logs: typing.Optional[bool]=None, sns_topic: typing.Optional[_ITopic_ef0ebe0e]=None, trail_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param bucket: The Amazon S3 bucket. Default: - if not supplied a bucket will be created with all the correct permisions
        :param cloud_watch_log_group: Log Group to which CloudTrail to push logs to. Ignored if sendToCloudWatchLogs is set to false. Default: - a new log group is created and used.
        :param cloud_watch_logs_retention: How long to retain logs in CloudWatchLogs. Ignored if sendToCloudWatchLogs is false or if cloudWatchLogGroup is set. Default: logs.RetentionDays.ONE_YEAR
        :param enable_file_validation: To determine whether a log file was modified, deleted, or unchanged after CloudTrail delivered it, you can use CloudTrail log file integrity validation. This feature is built using industry standard algorithms: SHA-256 for hashing and SHA-256 with RSA for digital signing. This makes it computationally infeasible to modify, delete or forge CloudTrail log files without detection. You can use the AWS CLI to validate the files in the location where CloudTrail delivered them. Default: true
        :param encryption_key: The AWS Key Management Service (AWS KMS) key ID that you want to use to encrypt CloudTrail logs. Default: - No encryption.
        :param include_global_service_events: For most services, events are recorded in the region where the action occurred. For global services such as AWS Identity and Access Management (IAM), AWS STS, Amazon CloudFront, and Route 53, events are delivered to any trail that includes global services, and are logged as occurring in US East (N. Virginia) Region. Default: true
        :param is_multi_region_trail: Whether or not this trail delivers log files from multiple regions to a single S3 bucket for a single account. Default: true
        :param kms_key: The AWS Key Management Service (AWS KMS) key ID that you want to use to encrypt CloudTrail logs. Default: - No encryption.
        :param management_events: When an event occurs in your account, CloudTrail evaluates whether the event matches the settings for your trails. Only events that match your trail settings are delivered to your Amazon S3 bucket and Amazon CloudWatch Logs log group. This method sets the management configuration for this trail. Management events provide insight into management operations that are performed on resources in your AWS account. These are also known as control plane operations. Management events can also include non-API events that occur in your account. For example, when a user logs in to your account, CloudTrail logs the ConsoleLogin event. Default: ReadWriteType.ALL
        :param s3_key_prefix: An Amazon S3 object key prefix that precedes the name of all log files. Default: - No prefix.
        :param send_to_cloud_watch_logs: If CloudTrail pushes logs to CloudWatch Logs in addition to S3. Disabled for cost out of the box. Default: false
        :param sns_topic: SNS topic that is notified when new log files are published. Default: - No notifications.
        :param trail_name: The name of the trail. We recoomend customers do not set an explicit name. Default: - AWS CloudFormation generated name.

        stability
        :stability: experimental
        """
        props = TrailProps(bucket=bucket, cloud_watch_log_group=cloud_watch_log_group, cloud_watch_logs_retention=cloud_watch_logs_retention, enable_file_validation=enable_file_validation, encryption_key=encryption_key, include_global_service_events=include_global_service_events, is_multi_region_trail=is_multi_region_trail, kms_key=kms_key, management_events=management_events, s3_key_prefix=s3_key_prefix, send_to_cloud_watch_logs=send_to_cloud_watch_logs, sns_topic=sns_topic, trail_name=trail_name)

        jsii.create(Trail, self, [scope, id, props])

    @jsii.member(jsii_name="onEvent")
    @builtins.classmethod
    def on_event(cls, scope: _Construct_f50a3f53, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Create an event rule for when an event is recorded by any Trail in the account.

        Note that the event doesn't necessarily have to come from this Trail, it can
        be captured from any one.

        Be sure to filter the event further down using an event pattern.

        :param scope: -
        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.sinvoke(cls, "onEvent", [scope, id, options])

    @jsii.member(jsii_name="addEventSelector")
    def add_event_selector(self, data_resource_type: "DataResourceType", data_resource_values: typing.List[str], *, include_management_events: typing.Optional[bool]=None, read_write_type: typing.Optional["ReadWriteType"]=None) -> None:
        """When an event occurs in your account, CloudTrail evaluates whether the event matches the settings for your trails.

        Only events that match your trail settings are delivered to your Amazon S3 bucket and Amazon CloudWatch Logs log group.

        This method adds an Event Selector for filtering events that match either S3 or Lambda function operations.

        Data events: These events provide insight into the resource operations performed on or within a resource.
        These are also known as data plane operations.

        :param data_resource_type: -
        :param data_resource_values: the list of data resource ARNs to include in logging (maximum 250 entries).
        :param include_management_events: Specifies whether the event selector includes management events for the trail. Default: true
        :param read_write_type: Specifies whether to log read-only events, write-only events, or all events. Default: ReadWriteType.All

        stability
        :stability: experimental
        """
        options = AddEventSelectorOptions(include_management_events=include_management_events, read_write_type=read_write_type)

        return jsii.invoke(self, "addEventSelector", [data_resource_type, data_resource_values, options])

    @jsii.member(jsii_name="addLambdaEventSelector")
    def add_lambda_event_selector(self, handlers: typing.List[_IFunction_1c1de0bc], *, include_management_events: typing.Optional[bool]=None, read_write_type: typing.Optional["ReadWriteType"]=None) -> None:
        """When an event occurs in your account, CloudTrail evaluates whether the event matches the settings for your trails.

        Only events that match your trail settings are delivered to your Amazon S3 bucket and Amazon CloudWatch Logs log group.

        This method adds a Lambda Data Event Selector for filtering events that match Lambda function operations.

        Data events: These events provide insight into the resource operations performed on or within a resource.
        These are also known as data plane operations.

        :param handlers: the list of lambda function handlers whose data events should be logged (maximum 250 entries).
        :param include_management_events: Specifies whether the event selector includes management events for the trail. Default: true
        :param read_write_type: Specifies whether to log read-only events, write-only events, or all events. Default: ReadWriteType.All

        stability
        :stability: experimental
        """
        options = AddEventSelectorOptions(include_management_events=include_management_events, read_write_type=read_write_type)

        return jsii.invoke(self, "addLambdaEventSelector", [handlers, options])

    @jsii.member(jsii_name="addS3EventSelector")
    def add_s3_event_selector(self, s3_selector: typing.List["S3EventSelector"], *, include_management_events: typing.Optional[bool]=None, read_write_type: typing.Optional["ReadWriteType"]=None) -> None:
        """When an event occurs in your account, CloudTrail evaluates whether the event matches the settings for your trails.

        Only events that match your trail settings are delivered to your Amazon S3 bucket and Amazon CloudWatch Logs log group.

        This method adds an S3 Data Event Selector for filtering events that match S3 operations.

        Data events: These events provide insight into the resource operations performed on or within a resource.
        These are also known as data plane operations.

        :param s3_selector: the list of S3 bucket with optional prefix to include in logging (maximum 250 entries).
        :param include_management_events: Specifies whether the event selector includes management events for the trail. Default: true
        :param read_write_type: Specifies whether to log read-only events, write-only events, or all events. Default: ReadWriteType.All

        stability
        :stability: experimental
        """
        options = AddEventSelectorOptions(include_management_events=include_management_events, read_write_type=read_write_type)

        return jsii.invoke(self, "addS3EventSelector", [s3_selector, options])

    @jsii.member(jsii_name="logAllLambdaDataEvents")
    def log_all_lambda_data_events(self, *, include_management_events: typing.Optional[bool]=None, read_write_type: typing.Optional["ReadWriteType"]=None) -> None:
        """Log all Lamda data events for all lambda functions the account.

        :param include_management_events: Specifies whether the event selector includes management events for the trail. Default: true
        :param read_write_type: Specifies whether to log read-only events, write-only events, or all events. Default: ReadWriteType.All

        default
        :default: false

        see
        :see: https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html
        stability
        :stability: experimental
        """
        options = AddEventSelectorOptions(include_management_events=include_management_events, read_write_type=read_write_type)

        return jsii.invoke(self, "logAllLambdaDataEvents", [options])

    @jsii.member(jsii_name="logAllS3DataEvents")
    def log_all_s3_data_events(self, *, include_management_events: typing.Optional[bool]=None, read_write_type: typing.Optional["ReadWriteType"]=None) -> None:
        """Log all S3 data events for all objects for all buckets in the account.

        :param include_management_events: Specifies whether the event selector includes management events for the trail. Default: true
        :param read_write_type: Specifies whether to log read-only events, write-only events, or all events. Default: ReadWriteType.All

        default
        :default: false

        see
        :see: https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html
        stability
        :stability: experimental
        """
        options = AddEventSelectorOptions(include_management_events=include_management_events, read_write_type=read_write_type)

        return jsii.invoke(self, "logAllS3DataEvents", [options])

    @jsii.member(jsii_name="onCloudTrailEvent")
    def on_cloud_trail_event(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Create an event rule for when an event is recorded by any Trail in the account.

        Note that the event doesn't necessarily have to come from this Trail, it can
        be captured from any one.

        Be sure to filter the event further down using an event pattern.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        deprecated
        :deprecated: - use Trail.onEvent()

        stability
        :stability: deprecated
        """
        options = _OnEventOptions_926fbcf9(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onCloudTrailEvent", [id, options])

    @builtins.property
    @jsii.member(jsii_name="trailArn")
    def trail_arn(self) -> str:
        """ARN of the CloudTrail trail i.e. arn:aws:cloudtrail:us-east-2:123456789012:trail/myCloudTrail.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "trailArn")

    @builtins.property
    @jsii.member(jsii_name="trailSnsTopicArn")
    def trail_sns_topic_arn(self) -> str:
        """ARN of the Amazon SNS topic that's associated with the CloudTrail trail, i.e. arn:aws:sns:us-east-2:123456789012:mySNSTopic.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "trailSnsTopicArn")

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> typing.Optional[_ILogGroup_6b54c8e1]:
        """The CloudWatch log group to which CloudTrail events are sent.

        ``undefined`` if ``sendToCloudWatchLogs`` property is false.

        stability
        :stability: experimental
        """
        return jsii.get(self, "logGroup")


@jsii.data_type(jsii_type="monocdk-experiment.aws_cloudtrail.TrailProps", jsii_struct_bases=[], name_mapping={'bucket': 'bucket', 'cloud_watch_log_group': 'cloudWatchLogGroup', 'cloud_watch_logs_retention': 'cloudWatchLogsRetention', 'enable_file_validation': 'enableFileValidation', 'encryption_key': 'encryptionKey', 'include_global_service_events': 'includeGlobalServiceEvents', 'is_multi_region_trail': 'isMultiRegionTrail', 'kms_key': 'kmsKey', 'management_events': 'managementEvents', 's3_key_prefix': 's3KeyPrefix', 'send_to_cloud_watch_logs': 'sendToCloudWatchLogs', 'sns_topic': 'snsTopic', 'trail_name': 'trailName'})
class TrailProps():
    def __init__(self, *, bucket: typing.Optional[_IBucket_25bad983]=None, cloud_watch_log_group: typing.Optional[_ILogGroup_6b54c8e1]=None, cloud_watch_logs_retention: typing.Optional[_RetentionDays_bdc7ad1f]=None, enable_file_validation: typing.Optional[bool]=None, encryption_key: typing.Optional[_IKey_3336c79d]=None, include_global_service_events: typing.Optional[bool]=None, is_multi_region_trail: typing.Optional[bool]=None, kms_key: typing.Optional[_IKey_3336c79d]=None, management_events: typing.Optional["ReadWriteType"]=None, s3_key_prefix: typing.Optional[str]=None, send_to_cloud_watch_logs: typing.Optional[bool]=None, sns_topic: typing.Optional[_ITopic_ef0ebe0e]=None, trail_name: typing.Optional[str]=None) -> None:
        """Properties for an AWS CloudTrail trail.

        :param bucket: The Amazon S3 bucket. Default: - if not supplied a bucket will be created with all the correct permisions
        :param cloud_watch_log_group: Log Group to which CloudTrail to push logs to. Ignored if sendToCloudWatchLogs is set to false. Default: - a new log group is created and used.
        :param cloud_watch_logs_retention: How long to retain logs in CloudWatchLogs. Ignored if sendToCloudWatchLogs is false or if cloudWatchLogGroup is set. Default: logs.RetentionDays.ONE_YEAR
        :param enable_file_validation: To determine whether a log file was modified, deleted, or unchanged after CloudTrail delivered it, you can use CloudTrail log file integrity validation. This feature is built using industry standard algorithms: SHA-256 for hashing and SHA-256 with RSA for digital signing. This makes it computationally infeasible to modify, delete or forge CloudTrail log files without detection. You can use the AWS CLI to validate the files in the location where CloudTrail delivered them. Default: true
        :param encryption_key: The AWS Key Management Service (AWS KMS) key ID that you want to use to encrypt CloudTrail logs. Default: - No encryption.
        :param include_global_service_events: For most services, events are recorded in the region where the action occurred. For global services such as AWS Identity and Access Management (IAM), AWS STS, Amazon CloudFront, and Route 53, events are delivered to any trail that includes global services, and are logged as occurring in US East (N. Virginia) Region. Default: true
        :param is_multi_region_trail: Whether or not this trail delivers log files from multiple regions to a single S3 bucket for a single account. Default: true
        :param kms_key: The AWS Key Management Service (AWS KMS) key ID that you want to use to encrypt CloudTrail logs. Default: - No encryption.
        :param management_events: When an event occurs in your account, CloudTrail evaluates whether the event matches the settings for your trails. Only events that match your trail settings are delivered to your Amazon S3 bucket and Amazon CloudWatch Logs log group. This method sets the management configuration for this trail. Management events provide insight into management operations that are performed on resources in your AWS account. These are also known as control plane operations. Management events can also include non-API events that occur in your account. For example, when a user logs in to your account, CloudTrail logs the ConsoleLogin event. Default: ReadWriteType.ALL
        :param s3_key_prefix: An Amazon S3 object key prefix that precedes the name of all log files. Default: - No prefix.
        :param send_to_cloud_watch_logs: If CloudTrail pushes logs to CloudWatch Logs in addition to S3. Disabled for cost out of the box. Default: false
        :param sns_topic: SNS topic that is notified when new log files are published. Default: - No notifications.
        :param trail_name: The name of the trail. We recoomend customers do not set an explicit name. Default: - AWS CloudFormation generated name.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if bucket is not None: self._values["bucket"] = bucket
        if cloud_watch_log_group is not None: self._values["cloud_watch_log_group"] = cloud_watch_log_group
        if cloud_watch_logs_retention is not None: self._values["cloud_watch_logs_retention"] = cloud_watch_logs_retention
        if enable_file_validation is not None: self._values["enable_file_validation"] = enable_file_validation
        if encryption_key is not None: self._values["encryption_key"] = encryption_key
        if include_global_service_events is not None: self._values["include_global_service_events"] = include_global_service_events
        if is_multi_region_trail is not None: self._values["is_multi_region_trail"] = is_multi_region_trail
        if kms_key is not None: self._values["kms_key"] = kms_key
        if management_events is not None: self._values["management_events"] = management_events
        if s3_key_prefix is not None: self._values["s3_key_prefix"] = s3_key_prefix
        if send_to_cloud_watch_logs is not None: self._values["send_to_cloud_watch_logs"] = send_to_cloud_watch_logs
        if sns_topic is not None: self._values["sns_topic"] = sns_topic
        if trail_name is not None: self._values["trail_name"] = trail_name

    @builtins.property
    def bucket(self) -> typing.Optional[_IBucket_25bad983]:
        """The Amazon S3 bucket.

        default
        :default: - if not supplied a bucket will be created with all the correct permisions

        stability
        :stability: experimental
        """
        return self._values.get('bucket')

    @builtins.property
    def cloud_watch_log_group(self) -> typing.Optional[_ILogGroup_6b54c8e1]:
        """Log Group to which CloudTrail to push logs to.

        Ignored if sendToCloudWatchLogs is set to false.

        default
        :default: - a new log group is created and used.

        stability
        :stability: experimental
        """
        return self._values.get('cloud_watch_log_group')

    @builtins.property
    def cloud_watch_logs_retention(self) -> typing.Optional[_RetentionDays_bdc7ad1f]:
        """How long to retain logs in CloudWatchLogs.

        Ignored if sendToCloudWatchLogs is false or if cloudWatchLogGroup is set.

        default
        :default: logs.RetentionDays.ONE_YEAR

        stability
        :stability: experimental
        """
        return self._values.get('cloud_watch_logs_retention')

    @builtins.property
    def enable_file_validation(self) -> typing.Optional[bool]:
        """To determine whether a log file was modified, deleted, or unchanged after CloudTrail delivered it, you can use CloudTrail log file integrity validation.

        This feature is built using industry standard algorithms: SHA-256 for hashing and SHA-256 with RSA for digital signing.
        This makes it computationally infeasible to modify, delete or forge CloudTrail log files without detection.
        You can use the AWS CLI to validate the files in the location where CloudTrail delivered them.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('enable_file_validation')

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The AWS Key Management Service (AWS KMS) key ID that you want to use to encrypt CloudTrail logs.

        default
        :default: - No encryption.

        stability
        :stability: experimental
        """
        return self._values.get('encryption_key')

    @builtins.property
    def include_global_service_events(self) -> typing.Optional[bool]:
        """For most services, events are recorded in the region where the action occurred.

        For global services such as AWS Identity and Access Management (IAM), AWS STS, Amazon CloudFront, and Route 53,
        events are delivered to any trail that includes global services, and are logged as occurring in US East (N. Virginia) Region.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('include_global_service_events')

    @builtins.property
    def is_multi_region_trail(self) -> typing.Optional[bool]:
        """Whether or not this trail delivers log files from multiple regions to a single S3 bucket for a single account.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('is_multi_region_trail')

    @builtins.property
    def kms_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The AWS Key Management Service (AWS KMS) key ID that you want to use to encrypt CloudTrail logs.

        default
        :default: - No encryption.

        deprecated
        :deprecated: - use encryptionKey instead.

        stability
        :stability: deprecated
        """
        return self._values.get('kms_key')

    @builtins.property
    def management_events(self) -> typing.Optional["ReadWriteType"]:
        """When an event occurs in your account, CloudTrail evaluates whether the event matches the settings for your trails.

        Only events that match your trail settings are delivered to your Amazon S3 bucket and Amazon CloudWatch Logs log group.

        This method sets the management configuration for this trail.

        Management events provide insight into management operations that are performed on resources in your AWS account.
        These are also known as control plane operations.
        Management events can also include non-API events that occur in your account.
        For example, when a user logs in to your account, CloudTrail logs the ConsoleLogin event.

        default
        :default: ReadWriteType.ALL

        stability
        :stability: experimental
        """
        return self._values.get('management_events')

    @builtins.property
    def s3_key_prefix(self) -> typing.Optional[str]:
        """An Amazon S3 object key prefix that precedes the name of all log files.

        default
        :default: - No prefix.

        stability
        :stability: experimental
        """
        return self._values.get('s3_key_prefix')

    @builtins.property
    def send_to_cloud_watch_logs(self) -> typing.Optional[bool]:
        """If CloudTrail pushes logs to CloudWatch Logs in addition to S3.

        Disabled for cost out of the box.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('send_to_cloud_watch_logs')

    @builtins.property
    def sns_topic(self) -> typing.Optional[_ITopic_ef0ebe0e]:
        """SNS topic that is notified when new log files are published.

        default
        :default: - No notifications.

        stability
        :stability: experimental
        """
        return self._values.get('sns_topic')

    @builtins.property
    def trail_name(self) -> typing.Optional[str]:
        """The name of the trail.

        We recoomend customers do not set an explicit name.

        default
        :default: - AWS CloudFormation generated name.

        stability
        :stability: experimental
        """
        return self._values.get('trail_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TrailProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "AddEventSelectorOptions",
    "CfnTrail",
    "CfnTrailProps",
    "DataResourceType",
    "ReadWriteType",
    "S3EventSelector",
    "Trail",
    "TrailProps",
]

publication.publish()
