import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (Resource as _Resource_884d0774, Construct as _Construct_f50a3f53, CfnResource as _CfnResource_7760e8e4, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, TagManager as _TagManager_2508893f, IResolvable as _IResolvable_9ceae33e, IInspectable as _IInspectable_051e6ed8, CfnTag as _CfnTag_b4661f1a, IResource as _IResource_72f7ee7e)


@jsii.data_type(jsii_type="monocdk-experiment.aws_globalaccelerator.AcceleratorAttributes", jsii_struct_bases=[], name_mapping={'accelerator_arn': 'acceleratorArn', 'dns_name': 'dnsName'})
class AcceleratorAttributes():
    def __init__(self, *, accelerator_arn: str, dns_name: str) -> None:
        """Attributes required to import an existing accelerator to the stack.

        :param accelerator_arn: The ARN of the accelerator.
        :param dns_name: The DNS name of the accelerator.

        stability
        :stability: experimental
        """
        self._values = {
            'accelerator_arn': accelerator_arn,
            'dns_name': dns_name,
        }

    @builtins.property
    def accelerator_arn(self) -> str:
        """The ARN of the accelerator.

        stability
        :stability: experimental
        """
        return self._values.get('accelerator_arn')

    @builtins.property
    def dns_name(self) -> str:
        """The DNS name of the accelerator.

        stability
        :stability: experimental
        """
        return self._values.get('dns_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AcceleratorAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_globalaccelerator.AcceleratorProps", jsii_struct_bases=[], name_mapping={'accelerator_name': 'acceleratorName', 'enabled': 'enabled'})
class AcceleratorProps():
    def __init__(self, *, accelerator_name: typing.Optional[str]=None, enabled: typing.Optional[bool]=None) -> None:
        """Construct properties of the Accelerator.

        :param accelerator_name: The name of the accelerator. Default: - resource ID
        :param enabled: Indicates whether the accelerator is enabled. Default: true

        stability
        :stability: experimental
        """
        self._values = {
        }
        if accelerator_name is not None: self._values["accelerator_name"] = accelerator_name
        if enabled is not None: self._values["enabled"] = enabled

    @builtins.property
    def accelerator_name(self) -> typing.Optional[str]:
        """The name of the accelerator.

        default
        :default: - resource ID

        stability
        :stability: experimental
        """
        return self._values.get('accelerator_name')

    @builtins.property
    def enabled(self) -> typing.Optional[bool]:
        """Indicates whether the accelerator is enabled.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('enabled')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AcceleratorProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnAccelerator(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_globalaccelerator.CfnAccelerator"):
    """A CloudFormation ``AWS::GlobalAccelerator::Accelerator``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html
    cloudformationResource:
    :cloudformationResource:: AWS::GlobalAccelerator::Accelerator
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, name: str, enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, ip_addresses: typing.Optional[typing.List[str]]=None, ip_address_type: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Create a new ``AWS::GlobalAccelerator::Accelerator``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::GlobalAccelerator::Accelerator.Name``.
        :param enabled: ``AWS::GlobalAccelerator::Accelerator.Enabled``.
        :param ip_addresses: ``AWS::GlobalAccelerator::Accelerator.IpAddresses``.
        :param ip_address_type: ``AWS::GlobalAccelerator::Accelerator.IpAddressType``.
        :param tags: ``AWS::GlobalAccelerator::Accelerator.Tags``.
        """
        props = CfnAcceleratorProps(name=name, enabled=enabled, ip_addresses=ip_addresses, ip_address_type=ip_address_type, tags=tags)

        jsii.create(CfnAccelerator, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnAccelerator":
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
    @jsii.member(jsii_name="attrAcceleratorArn")
    def attr_accelerator_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: AcceleratorArn
        """
        return jsii.get(self, "attrAcceleratorArn")

    @builtins.property
    @jsii.member(jsii_name="attrDnsName")
    def attr_dns_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: DnsName
        """
        return jsii.get(self, "attrDnsName")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::GlobalAccelerator::Accelerator.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::GlobalAccelerator::Accelerator.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::GlobalAccelerator::Accelerator.Enabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-enabled
        """
        return jsii.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddresses")
    def ip_addresses(self) -> typing.Optional[typing.List[str]]:
        """``AWS::GlobalAccelerator::Accelerator.IpAddresses``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-ipaddresses
        """
        return jsii.get(self, "ipAddresses")

    @ip_addresses.setter
    def ip_addresses(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "ipAddresses", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddressType")
    def ip_address_type(self) -> typing.Optional[str]:
        """``AWS::GlobalAccelerator::Accelerator.IpAddressType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-ipaddresstype
        """
        return jsii.get(self, "ipAddressType")

    @ip_address_type.setter
    def ip_address_type(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "ipAddressType", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_globalaccelerator.CfnAcceleratorProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'enabled': 'enabled', 'ip_addresses': 'ipAddresses', 'ip_address_type': 'ipAddressType', 'tags': 'tags'})
class CfnAcceleratorProps():
    def __init__(self, *, name: str, enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, ip_addresses: typing.Optional[typing.List[str]]=None, ip_address_type: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Properties for defining a ``AWS::GlobalAccelerator::Accelerator``.

        :param name: ``AWS::GlobalAccelerator::Accelerator.Name``.
        :param enabled: ``AWS::GlobalAccelerator::Accelerator.Enabled``.
        :param ip_addresses: ``AWS::GlobalAccelerator::Accelerator.IpAddresses``.
        :param ip_address_type: ``AWS::GlobalAccelerator::Accelerator.IpAddressType``.
        :param tags: ``AWS::GlobalAccelerator::Accelerator.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html
        """
        self._values = {
            'name': name,
        }
        if enabled is not None: self._values["enabled"] = enabled
        if ip_addresses is not None: self._values["ip_addresses"] = ip_addresses
        if ip_address_type is not None: self._values["ip_address_type"] = ip_address_type
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def name(self) -> str:
        """``AWS::GlobalAccelerator::Accelerator.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-name
        """
        return self._values.get('name')

    @builtins.property
    def enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::GlobalAccelerator::Accelerator.Enabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-enabled
        """
        return self._values.get('enabled')

    @builtins.property
    def ip_addresses(self) -> typing.Optional[typing.List[str]]:
        """``AWS::GlobalAccelerator::Accelerator.IpAddresses``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-ipaddresses
        """
        return self._values.get('ip_addresses')

    @builtins.property
    def ip_address_type(self) -> typing.Optional[str]:
        """``AWS::GlobalAccelerator::Accelerator.IpAddressType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-ipaddresstype
        """
        return self._values.get('ip_address_type')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::GlobalAccelerator::Accelerator.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnAcceleratorProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnEndpointGroup(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_globalaccelerator.CfnEndpointGroup"):
    """A CloudFormation ``AWS::GlobalAccelerator::EndpointGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::GlobalAccelerator::EndpointGroup
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, endpoint_group_region: str, listener_arn: str, endpoint_configurations: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["EndpointConfigurationProperty", _IResolvable_9ceae33e]]]]=None, health_check_interval_seconds: typing.Optional[jsii.Number]=None, health_check_path: typing.Optional[str]=None, health_check_port: typing.Optional[jsii.Number]=None, health_check_protocol: typing.Optional[str]=None, threshold_count: typing.Optional[jsii.Number]=None, traffic_dial_percentage: typing.Optional[jsii.Number]=None) -> None:
        """Create a new ``AWS::GlobalAccelerator::EndpointGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param endpoint_group_region: ``AWS::GlobalAccelerator::EndpointGroup.EndpointGroupRegion``.
        :param listener_arn: ``AWS::GlobalAccelerator::EndpointGroup.ListenerArn``.
        :param endpoint_configurations: ``AWS::GlobalAccelerator::EndpointGroup.EndpointConfigurations``.
        :param health_check_interval_seconds: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckIntervalSeconds``.
        :param health_check_path: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPath``.
        :param health_check_port: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPort``.
        :param health_check_protocol: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckProtocol``.
        :param threshold_count: ``AWS::GlobalAccelerator::EndpointGroup.ThresholdCount``.
        :param traffic_dial_percentage: ``AWS::GlobalAccelerator::EndpointGroup.TrafficDialPercentage``.
        """
        props = CfnEndpointGroupProps(endpoint_group_region=endpoint_group_region, listener_arn=listener_arn, endpoint_configurations=endpoint_configurations, health_check_interval_seconds=health_check_interval_seconds, health_check_path=health_check_path, health_check_port=health_check_port, health_check_protocol=health_check_protocol, threshold_count=threshold_count, traffic_dial_percentage=traffic_dial_percentage)

        jsii.create(CfnEndpointGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnEndpointGroup":
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
    @jsii.member(jsii_name="attrEndpointGroupArn")
    def attr_endpoint_group_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: EndpointGroupArn
        """
        return jsii.get(self, "attrEndpointGroupArn")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="endpointGroupRegion")
    def endpoint_group_region(self) -> str:
        """``AWS::GlobalAccelerator::EndpointGroup.EndpointGroupRegion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-endpointgroupregion
        """
        return jsii.get(self, "endpointGroupRegion")

    @endpoint_group_region.setter
    def endpoint_group_region(self, value: str) -> None:
        jsii.set(self, "endpointGroupRegion", value)

    @builtins.property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> str:
        """``AWS::GlobalAccelerator::EndpointGroup.ListenerArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-listenerarn
        """
        return jsii.get(self, "listenerArn")

    @listener_arn.setter
    def listener_arn(self, value: str) -> None:
        jsii.set(self, "listenerArn", value)

    @builtins.property
    @jsii.member(jsii_name="endpointConfigurations")
    def endpoint_configurations(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["EndpointConfigurationProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::GlobalAccelerator::EndpointGroup.EndpointConfigurations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-endpointconfigurations
        """
        return jsii.get(self, "endpointConfigurations")

    @endpoint_configurations.setter
    def endpoint_configurations(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["EndpointConfigurationProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "endpointConfigurations", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckIntervalSeconds")
    def health_check_interval_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::GlobalAccelerator::EndpointGroup.HealthCheckIntervalSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckintervalseconds
        """
        return jsii.get(self, "healthCheckIntervalSeconds")

    @health_check_interval_seconds.setter
    def health_check_interval_seconds(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "healthCheckIntervalSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckPath")
    def health_check_path(self) -> typing.Optional[str]:
        """``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPath``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckpath
        """
        return jsii.get(self, "healthCheckPath")

    @health_check_path.setter
    def health_check_path(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "healthCheckPath", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckPort")
    def health_check_port(self) -> typing.Optional[jsii.Number]:
        """``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPort``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckport
        """
        return jsii.get(self, "healthCheckPort")

    @health_check_port.setter
    def health_check_port(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "healthCheckPort", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckProtocol")
    def health_check_protocol(self) -> typing.Optional[str]:
        """``AWS::GlobalAccelerator::EndpointGroup.HealthCheckProtocol``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckprotocol
        """
        return jsii.get(self, "healthCheckProtocol")

    @health_check_protocol.setter
    def health_check_protocol(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "healthCheckProtocol", value)

    @builtins.property
    @jsii.member(jsii_name="thresholdCount")
    def threshold_count(self) -> typing.Optional[jsii.Number]:
        """``AWS::GlobalAccelerator::EndpointGroup.ThresholdCount``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-thresholdcount
        """
        return jsii.get(self, "thresholdCount")

    @threshold_count.setter
    def threshold_count(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "thresholdCount", value)

    @builtins.property
    @jsii.member(jsii_name="trafficDialPercentage")
    def traffic_dial_percentage(self) -> typing.Optional[jsii.Number]:
        """``AWS::GlobalAccelerator::EndpointGroup.TrafficDialPercentage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-trafficdialpercentage
        """
        return jsii.get(self, "trafficDialPercentage")

    @traffic_dial_percentage.setter
    def traffic_dial_percentage(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "trafficDialPercentage", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_globalaccelerator.CfnEndpointGroup.EndpointConfigurationProperty", jsii_struct_bases=[], name_mapping={'endpoint_id': 'endpointId', 'client_ip_preservation_enabled': 'clientIpPreservationEnabled', 'weight': 'weight'})
    class EndpointConfigurationProperty():
        def __init__(self, *, endpoint_id: str, client_ip_preservation_enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, weight: typing.Optional[jsii.Number]=None) -> None:
            """
            :param endpoint_id: ``CfnEndpointGroup.EndpointConfigurationProperty.EndpointId``.
            :param client_ip_preservation_enabled: ``CfnEndpointGroup.EndpointConfigurationProperty.ClientIPPreservationEnabled``.
            :param weight: ``CfnEndpointGroup.EndpointConfigurationProperty.Weight``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-endpointconfiguration.html
            """
            self._values = {
                'endpoint_id': endpoint_id,
            }
            if client_ip_preservation_enabled is not None: self._values["client_ip_preservation_enabled"] = client_ip_preservation_enabled
            if weight is not None: self._values["weight"] = weight

        @builtins.property
        def endpoint_id(self) -> str:
            """``CfnEndpointGroup.EndpointConfigurationProperty.EndpointId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-endpointconfiguration.html#cfn-globalaccelerator-endpointgroup-endpointconfiguration-endpointid
            """
            return self._values.get('endpoint_id')

        @builtins.property
        def client_ip_preservation_enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnEndpointGroup.EndpointConfigurationProperty.ClientIPPreservationEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-endpointconfiguration.html#cfn-globalaccelerator-endpointgroup-endpointconfiguration-clientippreservationenabled
            """
            return self._values.get('client_ip_preservation_enabled')

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            """``CfnEndpointGroup.EndpointConfigurationProperty.Weight``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-endpointconfiguration.html#cfn-globalaccelerator-endpointgroup-endpointconfiguration-weight
            """
            return self._values.get('weight')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EndpointConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_globalaccelerator.CfnEndpointGroupProps", jsii_struct_bases=[], name_mapping={'endpoint_group_region': 'endpointGroupRegion', 'listener_arn': 'listenerArn', 'endpoint_configurations': 'endpointConfigurations', 'health_check_interval_seconds': 'healthCheckIntervalSeconds', 'health_check_path': 'healthCheckPath', 'health_check_port': 'healthCheckPort', 'health_check_protocol': 'healthCheckProtocol', 'threshold_count': 'thresholdCount', 'traffic_dial_percentage': 'trafficDialPercentage'})
class CfnEndpointGroupProps():
    def __init__(self, *, endpoint_group_region: str, listener_arn: str, endpoint_configurations: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnEndpointGroup.EndpointConfigurationProperty", _IResolvable_9ceae33e]]]]=None, health_check_interval_seconds: typing.Optional[jsii.Number]=None, health_check_path: typing.Optional[str]=None, health_check_port: typing.Optional[jsii.Number]=None, health_check_protocol: typing.Optional[str]=None, threshold_count: typing.Optional[jsii.Number]=None, traffic_dial_percentage: typing.Optional[jsii.Number]=None) -> None:
        """Properties for defining a ``AWS::GlobalAccelerator::EndpointGroup``.

        :param endpoint_group_region: ``AWS::GlobalAccelerator::EndpointGroup.EndpointGroupRegion``.
        :param listener_arn: ``AWS::GlobalAccelerator::EndpointGroup.ListenerArn``.
        :param endpoint_configurations: ``AWS::GlobalAccelerator::EndpointGroup.EndpointConfigurations``.
        :param health_check_interval_seconds: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckIntervalSeconds``.
        :param health_check_path: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPath``.
        :param health_check_port: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPort``.
        :param health_check_protocol: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckProtocol``.
        :param threshold_count: ``AWS::GlobalAccelerator::EndpointGroup.ThresholdCount``.
        :param traffic_dial_percentage: ``AWS::GlobalAccelerator::EndpointGroup.TrafficDialPercentage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html
        """
        self._values = {
            'endpoint_group_region': endpoint_group_region,
            'listener_arn': listener_arn,
        }
        if endpoint_configurations is not None: self._values["endpoint_configurations"] = endpoint_configurations
        if health_check_interval_seconds is not None: self._values["health_check_interval_seconds"] = health_check_interval_seconds
        if health_check_path is not None: self._values["health_check_path"] = health_check_path
        if health_check_port is not None: self._values["health_check_port"] = health_check_port
        if health_check_protocol is not None: self._values["health_check_protocol"] = health_check_protocol
        if threshold_count is not None: self._values["threshold_count"] = threshold_count
        if traffic_dial_percentage is not None: self._values["traffic_dial_percentage"] = traffic_dial_percentage

    @builtins.property
    def endpoint_group_region(self) -> str:
        """``AWS::GlobalAccelerator::EndpointGroup.EndpointGroupRegion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-endpointgroupregion
        """
        return self._values.get('endpoint_group_region')

    @builtins.property
    def listener_arn(self) -> str:
        """``AWS::GlobalAccelerator::EndpointGroup.ListenerArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-listenerarn
        """
        return self._values.get('listener_arn')

    @builtins.property
    def endpoint_configurations(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnEndpointGroup.EndpointConfigurationProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::GlobalAccelerator::EndpointGroup.EndpointConfigurations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-endpointconfigurations
        """
        return self._values.get('endpoint_configurations')

    @builtins.property
    def health_check_interval_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::GlobalAccelerator::EndpointGroup.HealthCheckIntervalSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckintervalseconds
        """
        return self._values.get('health_check_interval_seconds')

    @builtins.property
    def health_check_path(self) -> typing.Optional[str]:
        """``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPath``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckpath
        """
        return self._values.get('health_check_path')

    @builtins.property
    def health_check_port(self) -> typing.Optional[jsii.Number]:
        """``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPort``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckport
        """
        return self._values.get('health_check_port')

    @builtins.property
    def health_check_protocol(self) -> typing.Optional[str]:
        """``AWS::GlobalAccelerator::EndpointGroup.HealthCheckProtocol``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckprotocol
        """
        return self._values.get('health_check_protocol')

    @builtins.property
    def threshold_count(self) -> typing.Optional[jsii.Number]:
        """``AWS::GlobalAccelerator::EndpointGroup.ThresholdCount``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-thresholdcount
        """
        return self._values.get('threshold_count')

    @builtins.property
    def traffic_dial_percentage(self) -> typing.Optional[jsii.Number]:
        """``AWS::GlobalAccelerator::EndpointGroup.TrafficDialPercentage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-trafficdialpercentage
        """
        return self._values.get('traffic_dial_percentage')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnEndpointGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnListener(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_globalaccelerator.CfnListener"):
    """A CloudFormation ``AWS::GlobalAccelerator::Listener``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html
    cloudformationResource:
    :cloudformationResource:: AWS::GlobalAccelerator::Listener
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, accelerator_arn: str, port_ranges: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["PortRangeProperty", _IResolvable_9ceae33e]]], protocol: str, client_affinity: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::GlobalAccelerator::Listener``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param accelerator_arn: ``AWS::GlobalAccelerator::Listener.AcceleratorArn``.
        :param port_ranges: ``AWS::GlobalAccelerator::Listener.PortRanges``.
        :param protocol: ``AWS::GlobalAccelerator::Listener.Protocol``.
        :param client_affinity: ``AWS::GlobalAccelerator::Listener.ClientAffinity``.
        """
        props = CfnListenerProps(accelerator_arn=accelerator_arn, port_ranges=port_ranges, protocol=protocol, client_affinity=client_affinity)

        jsii.create(CfnListener, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnListener":
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
    @jsii.member(jsii_name="attrListenerArn")
    def attr_listener_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ListenerArn
        """
        return jsii.get(self, "attrListenerArn")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="acceleratorArn")
    def accelerator_arn(self) -> str:
        """``AWS::GlobalAccelerator::Listener.AcceleratorArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-acceleratorarn
        """
        return jsii.get(self, "acceleratorArn")

    @accelerator_arn.setter
    def accelerator_arn(self, value: str) -> None:
        jsii.set(self, "acceleratorArn", value)

    @builtins.property
    @jsii.member(jsii_name="portRanges")
    def port_ranges(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["PortRangeProperty", _IResolvable_9ceae33e]]]:
        """``AWS::GlobalAccelerator::Listener.PortRanges``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-portranges
        """
        return jsii.get(self, "portRanges")

    @port_ranges.setter
    def port_ranges(self, value: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["PortRangeProperty", _IResolvable_9ceae33e]]]) -> None:
        jsii.set(self, "portRanges", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> str:
        """``AWS::GlobalAccelerator::Listener.Protocol``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-protocol
        """
        return jsii.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: str) -> None:
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="clientAffinity")
    def client_affinity(self) -> typing.Optional[str]:
        """``AWS::GlobalAccelerator::Listener.ClientAffinity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-clientaffinity
        """
        return jsii.get(self, "clientAffinity")

    @client_affinity.setter
    def client_affinity(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "clientAffinity", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_globalaccelerator.CfnListener.PortRangeProperty", jsii_struct_bases=[], name_mapping={'from_port': 'fromPort', 'to_port': 'toPort'})
    class PortRangeProperty():
        def __init__(self, *, from_port: jsii.Number, to_port: jsii.Number) -> None:
            """
            :param from_port: ``CfnListener.PortRangeProperty.FromPort``.
            :param to_port: ``CfnListener.PortRangeProperty.ToPort``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-listener-portrange.html
            """
            self._values = {
                'from_port': from_port,
                'to_port': to_port,
            }

        @builtins.property
        def from_port(self) -> jsii.Number:
            """``CfnListener.PortRangeProperty.FromPort``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-listener-portrange.html#cfn-globalaccelerator-listener-portrange-fromport
            """
            return self._values.get('from_port')

        @builtins.property
        def to_port(self) -> jsii.Number:
            """``CfnListener.PortRangeProperty.ToPort``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-listener-portrange.html#cfn-globalaccelerator-listener-portrange-toport
            """
            return self._values.get('to_port')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PortRangeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_globalaccelerator.CfnListenerProps", jsii_struct_bases=[], name_mapping={'accelerator_arn': 'acceleratorArn', 'port_ranges': 'portRanges', 'protocol': 'protocol', 'client_affinity': 'clientAffinity'})
class CfnListenerProps():
    def __init__(self, *, accelerator_arn: str, port_ranges: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnListener.PortRangeProperty", _IResolvable_9ceae33e]]], protocol: str, client_affinity: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::GlobalAccelerator::Listener``.

        :param accelerator_arn: ``AWS::GlobalAccelerator::Listener.AcceleratorArn``.
        :param port_ranges: ``AWS::GlobalAccelerator::Listener.PortRanges``.
        :param protocol: ``AWS::GlobalAccelerator::Listener.Protocol``.
        :param client_affinity: ``AWS::GlobalAccelerator::Listener.ClientAffinity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html
        """
        self._values = {
            'accelerator_arn': accelerator_arn,
            'port_ranges': port_ranges,
            'protocol': protocol,
        }
        if client_affinity is not None: self._values["client_affinity"] = client_affinity

    @builtins.property
    def accelerator_arn(self) -> str:
        """``AWS::GlobalAccelerator::Listener.AcceleratorArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-acceleratorarn
        """
        return self._values.get('accelerator_arn')

    @builtins.property
    def port_ranges(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnListener.PortRangeProperty", _IResolvable_9ceae33e]]]:
        """``AWS::GlobalAccelerator::Listener.PortRanges``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-portranges
        """
        return self._values.get('port_ranges')

    @builtins.property
    def protocol(self) -> str:
        """``AWS::GlobalAccelerator::Listener.Protocol``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-protocol
        """
        return self._values.get('protocol')

    @builtins.property
    def client_affinity(self) -> typing.Optional[str]:
        """``AWS::GlobalAccelerator::Listener.ClientAffinity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-clientaffinity
        """
        return self._values.get('client_affinity')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnListenerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_globalaccelerator.ClientAffinity")
class ClientAffinity(enum.Enum):
    """Client affinity lets you direct all requests from a user to the same endpoint, if you have stateful applications, regardless of the port and protocol of the client request.

    Client affinity gives you control over whether to always
    route each client to the same specific endpoint. If you want a given client to always be routed to the same
    endpoint, set client affinity to SOURCE_IP.

    see
    :see: https://docs.aws.amazon.com/global-accelerator/latest/dg/about-listeners.html#about-listeners-client-affinity
    stability
    :stability: experimental
    """
    NONE = "NONE"
    """default affinity.

    stability
    :stability: experimental
    """
    SOURCE_IP = "SOURCE_IP"
    """affinity by source IP.

    stability
    :stability: experimental
    """

@jsii.enum(jsii_type="monocdk-experiment.aws_globalaccelerator.ConnectionProtocol")
class ConnectionProtocol(enum.Enum):
    """The protocol for the connections from clients to the accelerator.

    stability
    :stability: experimental
    """
    TCP = "TCP"
    """TCP.

    stability
    :stability: experimental
    """
    UDP = "UDP"
    """UDP.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.aws_globalaccelerator.Ec2Instance", jsii_struct_bases=[], name_mapping={'instance_id': 'instanceId'})
class Ec2Instance():
    def __init__(self, *, instance_id: str) -> None:
        """EC2 Instance interface.

        :param instance_id: The id of the instance resource.

        stability
        :stability: experimental
        """
        self._values = {
            'instance_id': instance_id,
        }

    @builtins.property
    def instance_id(self) -> str:
        """The id of the instance resource.

        stability
        :stability: experimental
        """
        return self._values.get('instance_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Ec2Instance(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_globalaccelerator.ElasticIpAddress", jsii_struct_bases=[], name_mapping={'attr_allocation_id': 'attrAllocationId'})
class ElasticIpAddress():
    def __init__(self, *, attr_allocation_id: str) -> None:
        """EIP Interface.

        :param attr_allocation_id: allocation ID of the EIP resoruce.

        stability
        :stability: experimental
        """
        self._values = {
            'attr_allocation_id': attr_allocation_id,
        }

    @builtins.property
    def attr_allocation_id(self) -> str:
        """allocation ID of the EIP resoruce.

        stability
        :stability: experimental
        """
        return self._values.get('attr_allocation_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ElasticIpAddress(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class EndpointConfiguration(_Construct_f50a3f53, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_globalaccelerator.EndpointConfiguration"):
    """The class for endpoint configuration.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, endpoint_group: "EndpointGroup", endpoint_id: str, client_ip_reservation: typing.Optional[bool]=None, weight: typing.Optional[jsii.Number]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param endpoint_group: The endopoint group reesource. [disable-awslint:ref-via-interface]
        :param endpoint_id: An ID for the endpoint. If the endpoint is a Network Load Balancer or Application Load Balancer, this is the Amazon Resource Name (ARN) of the resource. If the endpoint is an Elastic IP address, this is the Elastic IP address allocation ID. For EC2 instances, this is the EC2 instance ID.
        :param client_ip_reservation: Indicates whether client IP address preservation is enabled for an Application Load Balancer endpoint. Default: true
        :param weight: The weight associated with the endpoint. When you add weights to endpoints, you configure AWS Global Accelerator to route traffic based on proportions that you specify. For example, you might specify endpoint weights of 4, 5, 5, and 6 (sum=20). The result is that 4/20 of your traffic, on average, is routed to the first endpoint, 5/20 is routed both to the second and third endpoints, and 6/20 is routed to the last endpoint. Default: - not specified

        stability
        :stability: experimental
        """
        props = EndpointConfigurationProps(endpoint_group=endpoint_group, endpoint_id=endpoint_id, client_ip_reservation=client_ip_reservation, weight=weight)

        jsii.create(EndpointConfiguration, self, [scope, id, props])

    @jsii.member(jsii_name="renderEndpointConfiguration")
    def render_endpoint_configuration(self) -> "CfnEndpointGroup.EndpointConfigurationProperty":
        """render the endpoint configuration for the endpoint group.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "renderEndpointConfiguration", [])

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "EndpointConfigurationProps":
        """The property containing all the configuration to be rendered.

        stability
        :stability: experimental
        """
        return jsii.get(self, "props")


@jsii.data_type(jsii_type="monocdk-experiment.aws_globalaccelerator.EndpointConfigurationOptions", jsii_struct_bases=[], name_mapping={'client_ip_reservation': 'clientIpReservation', 'weight': 'weight'})
class EndpointConfigurationOptions():
    def __init__(self, *, client_ip_reservation: typing.Optional[bool]=None, weight: typing.Optional[jsii.Number]=None) -> None:
        """Options for ``addLoadBalancer``, ``addElasticIpAddress`` and ``addEc2Instance`` to add endpoints into the endpoint group.

        :param client_ip_reservation: Indicates whether client IP address preservation is enabled for an Application Load Balancer endpoint. Default: true
        :param weight: The weight associated with the endpoint. When you add weights to endpoints, you configure AWS Global Accelerator to route traffic based on proportions that you specify. For example, you might specify endpoint weights of 4, 5, 5, and 6 (sum=20). The result is that 4/20 of your traffic, on average, is routed to the first endpoint, 5/20 is routed both to the second and third endpoints, and 6/20 is routed to the last endpoint. Default: - not specified

        stability
        :stability: experimental
        """
        self._values = {
        }
        if client_ip_reservation is not None: self._values["client_ip_reservation"] = client_ip_reservation
        if weight is not None: self._values["weight"] = weight

    @builtins.property
    def client_ip_reservation(self) -> typing.Optional[bool]:
        """Indicates whether client IP address preservation is enabled for an Application Load Balancer endpoint.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('client_ip_reservation')

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        """The weight associated with the endpoint.

        When you add weights to endpoints, you configure AWS Global Accelerator
        to route traffic based on proportions that you specify. For example, you might specify endpoint weights of 4, 5,
        5, and 6 (sum=20). The result is that 4/20 of your traffic, on average, is routed to the first endpoint, 5/20 is
        routed both to the second and third endpoints, and 6/20 is routed to the last endpoint.

        default
        :default: - not specified

        see
        :see: https://docs.aws.amazon.com/global-accelerator/latest/dg/about-endpoints-endpoint-weights.html
        stability
        :stability: experimental
        """
        return self._values.get('weight')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EndpointConfigurationOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_globalaccelerator.EndpointConfigurationProps", jsii_struct_bases=[EndpointConfigurationOptions], name_mapping={'client_ip_reservation': 'clientIpReservation', 'weight': 'weight', 'endpoint_group': 'endpointGroup', 'endpoint_id': 'endpointId'})
class EndpointConfigurationProps(EndpointConfigurationOptions):
    def __init__(self, *, client_ip_reservation: typing.Optional[bool]=None, weight: typing.Optional[jsii.Number]=None, endpoint_group: "EndpointGroup", endpoint_id: str) -> None:
        """Properties to create EndpointConfiguration.

        :param client_ip_reservation: Indicates whether client IP address preservation is enabled for an Application Load Balancer endpoint. Default: true
        :param weight: The weight associated with the endpoint. When you add weights to endpoints, you configure AWS Global Accelerator to route traffic based on proportions that you specify. For example, you might specify endpoint weights of 4, 5, 5, and 6 (sum=20). The result is that 4/20 of your traffic, on average, is routed to the first endpoint, 5/20 is routed both to the second and third endpoints, and 6/20 is routed to the last endpoint. Default: - not specified
        :param endpoint_group: The endopoint group reesource. [disable-awslint:ref-via-interface]
        :param endpoint_id: An ID for the endpoint. If the endpoint is a Network Load Balancer or Application Load Balancer, this is the Amazon Resource Name (ARN) of the resource. If the endpoint is an Elastic IP address, this is the Elastic IP address allocation ID. For EC2 instances, this is the EC2 instance ID.

        stability
        :stability: experimental
        """
        self._values = {
            'endpoint_group': endpoint_group,
            'endpoint_id': endpoint_id,
        }
        if client_ip_reservation is not None: self._values["client_ip_reservation"] = client_ip_reservation
        if weight is not None: self._values["weight"] = weight

    @builtins.property
    def client_ip_reservation(self) -> typing.Optional[bool]:
        """Indicates whether client IP address preservation is enabled for an Application Load Balancer endpoint.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('client_ip_reservation')

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        """The weight associated with the endpoint.

        When you add weights to endpoints, you configure AWS Global Accelerator
        to route traffic based on proportions that you specify. For example, you might specify endpoint weights of 4, 5,
        5, and 6 (sum=20). The result is that 4/20 of your traffic, on average, is routed to the first endpoint, 5/20 is
        routed both to the second and third endpoints, and 6/20 is routed to the last endpoint.

        default
        :default: - not specified

        see
        :see: https://docs.aws.amazon.com/global-accelerator/latest/dg/about-endpoints-endpoint-weights.html
        stability
        :stability: experimental
        """
        return self._values.get('weight')

    @builtins.property
    def endpoint_group(self) -> "EndpointGroup":
        """The endopoint group reesource.

        [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        return self._values.get('endpoint_group')

    @builtins.property
    def endpoint_id(self) -> str:
        """An ID for the endpoint.

        If the endpoint is a Network Load Balancer or Application Load Balancer,
        this is the Amazon Resource Name (ARN) of the resource. If the endpoint is an Elastic IP address,
        this is the Elastic IP address allocation ID. For EC2 instances, this is the EC2 instance ID.

        stability
        :stability: experimental
        """
        return self._values.get('endpoint_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EndpointConfigurationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_globalaccelerator.EndpointGroupProps", jsii_struct_bases=[], name_mapping={'listener': 'listener', 'endpoint_group_name': 'endpointGroupName', 'region': 'region'})
class EndpointGroupProps():
    def __init__(self, *, listener: "IListener", endpoint_group_name: typing.Optional[str]=None, region: typing.Optional[str]=None) -> None:
        """Property of the EndpointGroup.

        :param listener: The Amazon Resource Name (ARN) of the listener.
        :param endpoint_group_name: Name of the endpoint group. Default: - logical ID of the resource
        :param region: The AWS Region where the endpoint group is located. Default: - the region of the current stack

        stability
        :stability: experimental
        """
        self._values = {
            'listener': listener,
        }
        if endpoint_group_name is not None: self._values["endpoint_group_name"] = endpoint_group_name
        if region is not None: self._values["region"] = region

    @builtins.property
    def listener(self) -> "IListener":
        """The Amazon Resource Name (ARN) of the listener.

        stability
        :stability: experimental
        """
        return self._values.get('listener')

    @builtins.property
    def endpoint_group_name(self) -> typing.Optional[str]:
        """Name of the endpoint group.

        default
        :default: - logical ID of the resource

        stability
        :stability: experimental
        """
        return self._values.get('endpoint_group_name')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """The AWS Region where the endpoint group is located.

        default
        :default: - the region of the current stack

        stability
        :stability: experimental
        """
        return self._values.get('region')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EndpointGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="monocdk-experiment.aws_globalaccelerator.IAccelerator")
class IAccelerator(_IResource_72f7ee7e, jsii.compat.Protocol):
    """The interface of the Accelerator.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAcceleratorProxy

    @builtins.property
    @jsii.member(jsii_name="acceleratorArn")
    def accelerator_arn(self) -> str:
        """The ARN of the accelerator.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> str:
        """The Domain Name System (DNS) name that Global Accelerator creates that points to your accelerator's static IP addresses.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IAcceleratorProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """The interface of the Accelerator.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_globalaccelerator.IAccelerator"
    @builtins.property
    @jsii.member(jsii_name="acceleratorArn")
    def accelerator_arn(self) -> str:
        """The ARN of the accelerator.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "acceleratorArn")

    @builtins.property
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> str:
        """The Domain Name System (DNS) name that Global Accelerator creates that points to your accelerator's static IP addresses.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "dnsName")


@jsii.interface(jsii_type="monocdk-experiment.aws_globalaccelerator.IEndpointGroup")
class IEndpointGroup(_IResource_72f7ee7e, jsii.compat.Protocol):
    """The interface of the EndpointGroup.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IEndpointGroupProxy

    @builtins.property
    @jsii.member(jsii_name="endpointGroupArn")
    def endpoint_group_arn(self) -> str:
        """EndpointGroup ARN.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IEndpointGroupProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """The interface of the EndpointGroup.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_globalaccelerator.IEndpointGroup"
    @builtins.property
    @jsii.member(jsii_name="endpointGroupArn")
    def endpoint_group_arn(self) -> str:
        """EndpointGroup ARN.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "endpointGroupArn")


@jsii.interface(jsii_type="monocdk-experiment.aws_globalaccelerator.IListener")
class IListener(_IResource_72f7ee7e, jsii.compat.Protocol):
    """Interface of the Listener.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IListenerProxy

    @builtins.property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> str:
        """The ARN of the listener.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IListenerProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """Interface of the Listener.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_globalaccelerator.IListener"
    @builtins.property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> str:
        """The ARN of the listener.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "listenerArn")


@jsii.implements(IListener)
class Listener(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_globalaccelerator.Listener"):
    """The construct for the Listener.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, accelerator: "IAccelerator", port_ranges: typing.List["PortRange"], client_affinity: typing.Optional["ClientAffinity"]=None, listener_name: typing.Optional[str]=None, protocol: typing.Optional["ConnectionProtocol"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param accelerator: The accelerator for this listener.
        :param port_ranges: The list of port ranges for the connections from clients to the accelerator.
        :param client_affinity: Client affinity to direct all requests from a user to the same endpoint. Default: NONE
        :param listener_name: Name of the listener. Default: - logical ID of the resource
        :param protocol: The protocol for the connections from clients to the accelerator. Default: TCP

        stability
        :stability: experimental
        """
        props = ListenerProps(accelerator=accelerator, port_ranges=port_ranges, client_affinity=client_affinity, listener_name=listener_name, protocol=protocol)

        jsii.create(Listener, self, [scope, id, props])

    @jsii.member(jsii_name="fromListenerArn")
    @builtins.classmethod
    def from_listener_arn(cls, scope: _Construct_f50a3f53, id: str, listener_arn: str) -> "IListener":
        """import from ARN.

        :param scope: -
        :param id: -
        :param listener_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromListenerArn", [scope, id, listener_arn])

    @builtins.property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> str:
        """The ARN of the listener.

        stability
        :stability: experimental
        """
        return jsii.get(self, "listenerArn")

    @builtins.property
    @jsii.member(jsii_name="listenerName")
    def listener_name(self) -> str:
        """The name of the listener.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "listenerName")


@jsii.data_type(jsii_type="monocdk-experiment.aws_globalaccelerator.ListenerProps", jsii_struct_bases=[], name_mapping={'accelerator': 'accelerator', 'port_ranges': 'portRanges', 'client_affinity': 'clientAffinity', 'listener_name': 'listenerName', 'protocol': 'protocol'})
class ListenerProps():
    def __init__(self, *, accelerator: "IAccelerator", port_ranges: typing.List["PortRange"], client_affinity: typing.Optional["ClientAffinity"]=None, listener_name: typing.Optional[str]=None, protocol: typing.Optional["ConnectionProtocol"]=None) -> None:
        """construct properties for Listener.

        :param accelerator: The accelerator for this listener.
        :param port_ranges: The list of port ranges for the connections from clients to the accelerator.
        :param client_affinity: Client affinity to direct all requests from a user to the same endpoint. Default: NONE
        :param listener_name: Name of the listener. Default: - logical ID of the resource
        :param protocol: The protocol for the connections from clients to the accelerator. Default: TCP

        stability
        :stability: experimental
        """
        self._values = {
            'accelerator': accelerator,
            'port_ranges': port_ranges,
        }
        if client_affinity is not None: self._values["client_affinity"] = client_affinity
        if listener_name is not None: self._values["listener_name"] = listener_name
        if protocol is not None: self._values["protocol"] = protocol

    @builtins.property
    def accelerator(self) -> "IAccelerator":
        """The accelerator for this listener.

        stability
        :stability: experimental
        """
        return self._values.get('accelerator')

    @builtins.property
    def port_ranges(self) -> typing.List["PortRange"]:
        """The list of port ranges for the connections from clients to the accelerator.

        stability
        :stability: experimental
        """
        return self._values.get('port_ranges')

    @builtins.property
    def client_affinity(self) -> typing.Optional["ClientAffinity"]:
        """Client affinity to direct all requests from a user to the same endpoint.

        default
        :default: NONE

        stability
        :stability: experimental
        """
        return self._values.get('client_affinity')

    @builtins.property
    def listener_name(self) -> typing.Optional[str]:
        """Name of the listener.

        default
        :default: - logical ID of the resource

        stability
        :stability: experimental
        """
        return self._values.get('listener_name')

    @builtins.property
    def protocol(self) -> typing.Optional["ConnectionProtocol"]:
        """The protocol for the connections from clients to the accelerator.

        default
        :default: TCP

        stability
        :stability: experimental
        """
        return self._values.get('protocol')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ListenerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_globalaccelerator.LoadBalancer", jsii_struct_bases=[], name_mapping={'load_balancer_arn': 'loadBalancerArn'})
class LoadBalancer():
    def __init__(self, *, load_balancer_arn: str) -> None:
        """LoadBalancer Interface.

        :param load_balancer_arn: The ARN of this load balancer.

        stability
        :stability: experimental
        """
        self._values = {
            'load_balancer_arn': load_balancer_arn,
        }

    @builtins.property
    def load_balancer_arn(self) -> str:
        """The ARN of this load balancer.

        stability
        :stability: experimental
        """
        return self._values.get('load_balancer_arn')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LoadBalancer(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_globalaccelerator.PortRange", jsii_struct_bases=[], name_mapping={'from_port': 'fromPort', 'to_port': 'toPort'})
class PortRange():
    def __init__(self, *, from_port: jsii.Number, to_port: jsii.Number) -> None:
        """The list of port ranges for the connections from clients to the accelerator.

        :param from_port: The first port in the range of ports, inclusive.
        :param to_port: The last port in the range of ports, inclusive.

        stability
        :stability: experimental
        """
        self._values = {
            'from_port': from_port,
            'to_port': to_port,
        }

    @builtins.property
    def from_port(self) -> jsii.Number:
        """The first port in the range of ports, inclusive.

        stability
        :stability: experimental
        """
        return self._values.get('from_port')

    @builtins.property
    def to_port(self) -> jsii.Number:
        """The last port in the range of ports, inclusive.

        stability
        :stability: experimental
        """
        return self._values.get('to_port')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'PortRange(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IAccelerator)
class Accelerator(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_globalaccelerator.Accelerator"):
    """The Accelerator construct.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, accelerator_name: typing.Optional[str]=None, enabled: typing.Optional[bool]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param accelerator_name: The name of the accelerator. Default: - resource ID
        :param enabled: Indicates whether the accelerator is enabled. Default: true

        stability
        :stability: experimental
        """
        props = AcceleratorProps(accelerator_name=accelerator_name, enabled=enabled)

        jsii.create(Accelerator, self, [scope, id, props])

    @jsii.member(jsii_name="fromAcceleratorAttributes")
    @builtins.classmethod
    def from_accelerator_attributes(cls, scope: _Construct_f50a3f53, id: str, *, accelerator_arn: str, dns_name: str) -> "IAccelerator":
        """import from attributes.

        :param scope: -
        :param id: -
        :param accelerator_arn: The ARN of the accelerator.
        :param dns_name: The DNS name of the accelerator.

        stability
        :stability: experimental
        """
        attrs = AcceleratorAttributes(accelerator_arn=accelerator_arn, dns_name=dns_name)

        return jsii.sinvoke(cls, "fromAcceleratorAttributes", [scope, id, attrs])

    @builtins.property
    @jsii.member(jsii_name="acceleratorArn")
    def accelerator_arn(self) -> str:
        """The ARN of the accelerator.

        stability
        :stability: experimental
        """
        return jsii.get(self, "acceleratorArn")

    @builtins.property
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> str:
        """The Domain Name System (DNS) name that Global Accelerator creates that points to your accelerator's static IP addresses.

        stability
        :stability: experimental
        """
        return jsii.get(self, "dnsName")


@jsii.implements(IEndpointGroup)
class EndpointGroup(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_globalaccelerator.EndpointGroup"):
    """EndpointGroup construct.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, listener: "IListener", endpoint_group_name: typing.Optional[str]=None, region: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param listener: The Amazon Resource Name (ARN) of the listener.
        :param endpoint_group_name: Name of the endpoint group. Default: - logical ID of the resource
        :param region: The AWS Region where the endpoint group is located. Default: - the region of the current stack

        stability
        :stability: experimental
        """
        props = EndpointGroupProps(listener=listener, endpoint_group_name=endpoint_group_name, region=region)

        jsii.create(EndpointGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromEndpointGroupArn")
    @builtins.classmethod
    def from_endpoint_group_arn(cls, scope: _Construct_f50a3f53, id: str, endpoint_group_arn: str) -> "IEndpointGroup":
        """import from ARN.

        :param scope: -
        :param id: -
        :param endpoint_group_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromEndpointGroupArn", [scope, id, endpoint_group_arn])

    @jsii.member(jsii_name="addEc2Instance")
    def add_ec2_instance(self, id: str, instance: "Ec2Instance", *, client_ip_reservation: typing.Optional[bool]=None, weight: typing.Optional[jsii.Number]=None) -> "EndpointConfiguration":
        """Add an EC2 Instance as an endpoint in this endpoint group.

        :param id: -
        :param instance: -
        :param client_ip_reservation: Indicates whether client IP address preservation is enabled for an Application Load Balancer endpoint. Default: true
        :param weight: The weight associated with the endpoint. When you add weights to endpoints, you configure AWS Global Accelerator to route traffic based on proportions that you specify. For example, you might specify endpoint weights of 4, 5, 5, and 6 (sum=20). The result is that 4/20 of your traffic, on average, is routed to the first endpoint, 5/20 is routed both to the second and third endpoints, and 6/20 is routed to the last endpoint. Default: - not specified

        stability
        :stability: experimental
        """
        props = EndpointConfigurationOptions(client_ip_reservation=client_ip_reservation, weight=weight)

        return jsii.invoke(self, "addEc2Instance", [id, instance, props])

    @jsii.member(jsii_name="addElasticIpAddress")
    def add_elastic_ip_address(self, id: str, eip: "ElasticIpAddress", *, client_ip_reservation: typing.Optional[bool]=None, weight: typing.Optional[jsii.Number]=None) -> "EndpointConfiguration":
        """Add an EIP as an endpoint in this endpoint group.

        :param id: -
        :param eip: -
        :param client_ip_reservation: Indicates whether client IP address preservation is enabled for an Application Load Balancer endpoint. Default: true
        :param weight: The weight associated with the endpoint. When you add weights to endpoints, you configure AWS Global Accelerator to route traffic based on proportions that you specify. For example, you might specify endpoint weights of 4, 5, 5, and 6 (sum=20). The result is that 4/20 of your traffic, on average, is routed to the first endpoint, 5/20 is routed both to the second and third endpoints, and 6/20 is routed to the last endpoint. Default: - not specified

        stability
        :stability: experimental
        """
        props = EndpointConfigurationOptions(client_ip_reservation=client_ip_reservation, weight=weight)

        return jsii.invoke(self, "addElasticIpAddress", [id, eip, props])

    @jsii.member(jsii_name="addEndpoint")
    def add_endpoint(self, id: str, endpoint_id: str, *, client_ip_reservation: typing.Optional[bool]=None, weight: typing.Optional[jsii.Number]=None) -> "EndpointConfiguration":
        """Add an endpoint.

        :param id: -
        :param endpoint_id: -
        :param client_ip_reservation: Indicates whether client IP address preservation is enabled for an Application Load Balancer endpoint. Default: true
        :param weight: The weight associated with the endpoint. When you add weights to endpoints, you configure AWS Global Accelerator to route traffic based on proportions that you specify. For example, you might specify endpoint weights of 4, 5, 5, and 6 (sum=20). The result is that 4/20 of your traffic, on average, is routed to the first endpoint, 5/20 is routed both to the second and third endpoints, and 6/20 is routed to the last endpoint. Default: - not specified

        stability
        :stability: experimental
        """
        props = EndpointConfigurationOptions(client_ip_reservation=client_ip_reservation, weight=weight)

        return jsii.invoke(self, "addEndpoint", [id, endpoint_id, props])

    @jsii.member(jsii_name="addLoadBalancer")
    def add_load_balancer(self, id: str, lb: "LoadBalancer", *, client_ip_reservation: typing.Optional[bool]=None, weight: typing.Optional[jsii.Number]=None) -> "EndpointConfiguration":
        """Add an Elastic Load Balancer as an endpoint in this endpoint group.

        :param id: -
        :param lb: -
        :param client_ip_reservation: Indicates whether client IP address preservation is enabled for an Application Load Balancer endpoint. Default: true
        :param weight: The weight associated with the endpoint. When you add weights to endpoints, you configure AWS Global Accelerator to route traffic based on proportions that you specify. For example, you might specify endpoint weights of 4, 5, 5, and 6 (sum=20). The result is that 4/20 of your traffic, on average, is routed to the first endpoint, 5/20 is routed both to the second and third endpoints, and 6/20 is routed to the last endpoint. Default: - not specified

        stability
        :stability: experimental
        """
        props = EndpointConfigurationOptions(client_ip_reservation=client_ip_reservation, weight=weight)

        return jsii.invoke(self, "addLoadBalancer", [id, lb, props])

    @builtins.property
    @jsii.member(jsii_name="endpointGroupArn")
    def endpoint_group_arn(self) -> str:
        """EndpointGroup ARN.

        stability
        :stability: experimental
        """
        return jsii.get(self, "endpointGroupArn")

    @builtins.property
    @jsii.member(jsii_name="endpointGroupName")
    def endpoint_group_name(self) -> str:
        """The name of the endpoint group.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "endpointGroupName")

    @builtins.property
    @jsii.member(jsii_name="endpoints")
    def _endpoints(self) -> typing.List["EndpointConfiguration"]:
        """The array of the endpoints in this endpoint group.

        stability
        :stability: experimental
        """
        return jsii.get(self, "endpoints")


__all__ = [
    "Accelerator",
    "AcceleratorAttributes",
    "AcceleratorProps",
    "CfnAccelerator",
    "CfnAcceleratorProps",
    "CfnEndpointGroup",
    "CfnEndpointGroupProps",
    "CfnListener",
    "CfnListenerProps",
    "ClientAffinity",
    "ConnectionProtocol",
    "Ec2Instance",
    "ElasticIpAddress",
    "EndpointConfiguration",
    "EndpointConfigurationOptions",
    "EndpointConfigurationProps",
    "EndpointGroup",
    "EndpointGroupProps",
    "IAccelerator",
    "IEndpointGroup",
    "IListener",
    "Listener",
    "ListenerProps",
    "LoadBalancer",
    "PortRange",
]

publication.publish()
