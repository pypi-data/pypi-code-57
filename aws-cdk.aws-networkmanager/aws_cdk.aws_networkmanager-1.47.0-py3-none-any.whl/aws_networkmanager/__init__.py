"""
## AWS::NetworkManager Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_networkmanager as networkmanager
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
class CfnCustomerGatewayAssociation(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-networkmanager.CfnCustomerGatewayAssociation"):
    """A CloudFormation ``AWS::NetworkManager::CustomerGatewayAssociation``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html
    cloudformationResource:
    :cloudformationResource:: AWS::NetworkManager::CustomerGatewayAssociation
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, customer_gateway_arn: str, device_id: str, global_network_id: str, link_id: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::NetworkManager::CustomerGatewayAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param customer_gateway_arn: ``AWS::NetworkManager::CustomerGatewayAssociation.CustomerGatewayArn``.
        :param device_id: ``AWS::NetworkManager::CustomerGatewayAssociation.DeviceId``.
        :param global_network_id: ``AWS::NetworkManager::CustomerGatewayAssociation.GlobalNetworkId``.
        :param link_id: ``AWS::NetworkManager::CustomerGatewayAssociation.LinkId``.
        """
        props = CfnCustomerGatewayAssociationProps(customer_gateway_arn=customer_gateway_arn, device_id=device_id, global_network_id=global_network_id, link_id=link_id)

        jsii.create(CfnCustomerGatewayAssociation, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnCustomerGatewayAssociation":
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
    @jsii.member(jsii_name="customerGatewayArn")
    def customer_gateway_arn(self) -> str:
        """``AWS::NetworkManager::CustomerGatewayAssociation.CustomerGatewayArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-customergatewayarn
        """
        return jsii.get(self, "customerGatewayArn")

    @customer_gateway_arn.setter
    def customer_gateway_arn(self, value: str) -> None:
        jsii.set(self, "customerGatewayArn", value)

    @builtins.property
    @jsii.member(jsii_name="deviceId")
    def device_id(self) -> str:
        """``AWS::NetworkManager::CustomerGatewayAssociation.DeviceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-deviceid
        """
        return jsii.get(self, "deviceId")

    @device_id.setter
    def device_id(self, value: str) -> None:
        jsii.set(self, "deviceId", value)

    @builtins.property
    @jsii.member(jsii_name="globalNetworkId")
    def global_network_id(self) -> str:
        """``AWS::NetworkManager::CustomerGatewayAssociation.GlobalNetworkId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-globalnetworkid
        """
        return jsii.get(self, "globalNetworkId")

    @global_network_id.setter
    def global_network_id(self, value: str) -> None:
        jsii.set(self, "globalNetworkId", value)

    @builtins.property
    @jsii.member(jsii_name="linkId")
    def link_id(self) -> typing.Optional[str]:
        """``AWS::NetworkManager::CustomerGatewayAssociation.LinkId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-linkid
        """
        return jsii.get(self, "linkId")

    @link_id.setter
    def link_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "linkId", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-networkmanager.CfnCustomerGatewayAssociationProps", jsii_struct_bases=[], name_mapping={'customer_gateway_arn': 'customerGatewayArn', 'device_id': 'deviceId', 'global_network_id': 'globalNetworkId', 'link_id': 'linkId'})
class CfnCustomerGatewayAssociationProps():
    def __init__(self, *, customer_gateway_arn: str, device_id: str, global_network_id: str, link_id: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::NetworkManager::CustomerGatewayAssociation``.

        :param customer_gateway_arn: ``AWS::NetworkManager::CustomerGatewayAssociation.CustomerGatewayArn``.
        :param device_id: ``AWS::NetworkManager::CustomerGatewayAssociation.DeviceId``.
        :param global_network_id: ``AWS::NetworkManager::CustomerGatewayAssociation.GlobalNetworkId``.
        :param link_id: ``AWS::NetworkManager::CustomerGatewayAssociation.LinkId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html
        """
        self._values = {
            'customer_gateway_arn': customer_gateway_arn,
            'device_id': device_id,
            'global_network_id': global_network_id,
        }
        if link_id is not None: self._values["link_id"] = link_id

    @builtins.property
    def customer_gateway_arn(self) -> str:
        """``AWS::NetworkManager::CustomerGatewayAssociation.CustomerGatewayArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-customergatewayarn
        """
        return self._values.get('customer_gateway_arn')

    @builtins.property
    def device_id(self) -> str:
        """``AWS::NetworkManager::CustomerGatewayAssociation.DeviceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-deviceid
        """
        return self._values.get('device_id')

    @builtins.property
    def global_network_id(self) -> str:
        """``AWS::NetworkManager::CustomerGatewayAssociation.GlobalNetworkId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-globalnetworkid
        """
        return self._values.get('global_network_id')

    @builtins.property
    def link_id(self) -> typing.Optional[str]:
        """``AWS::NetworkManager::CustomerGatewayAssociation.LinkId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-linkid
        """
        return self._values.get('link_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnCustomerGatewayAssociationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDevice(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-networkmanager.CfnDevice"):
    """A CloudFormation ``AWS::NetworkManager::Device``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html
    cloudformationResource:
    :cloudformationResource:: AWS::NetworkManager::Device
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, global_network_id: str, description: typing.Optional[str]=None, location: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "LocationProperty"]]=None, model: typing.Optional[str]=None, serial_number: typing.Optional[str]=None, site_id: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, type: typing.Optional[str]=None, vendor: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::NetworkManager::Device``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param global_network_id: ``AWS::NetworkManager::Device.GlobalNetworkId``.
        :param description: ``AWS::NetworkManager::Device.Description``.
        :param location: ``AWS::NetworkManager::Device.Location``.
        :param model: ``AWS::NetworkManager::Device.Model``.
        :param serial_number: ``AWS::NetworkManager::Device.SerialNumber``.
        :param site_id: ``AWS::NetworkManager::Device.SiteId``.
        :param tags: ``AWS::NetworkManager::Device.Tags``.
        :param type: ``AWS::NetworkManager::Device.Type``.
        :param vendor: ``AWS::NetworkManager::Device.Vendor``.
        """
        props = CfnDeviceProps(global_network_id=global_network_id, description=description, location=location, model=model, serial_number=serial_number, site_id=site_id, tags=tags, type=type, vendor=vendor)

        jsii.create(CfnDevice, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnDevice":
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
    @jsii.member(jsii_name="attrDeviceArn")
    def attr_device_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: DeviceArn
        """
        return jsii.get(self, "attrDeviceArn")

    @builtins.property
    @jsii.member(jsii_name="attrDeviceId")
    def attr_device_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: DeviceId
        """
        return jsii.get(self, "attrDeviceId")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::NetworkManager::Device.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="globalNetworkId")
    def global_network_id(self) -> str:
        """``AWS::NetworkManager::Device.GlobalNetworkId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-globalnetworkid
        """
        return jsii.get(self, "globalNetworkId")

    @global_network_id.setter
    def global_network_id(self, value: str) -> None:
        jsii.set(self, "globalNetworkId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::NetworkManager::Device.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "LocationProperty"]]:
        """``AWS::NetworkManager::Device.Location``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-location
        """
        return jsii.get(self, "location")

    @location.setter
    def location(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "LocationProperty"]]) -> None:
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="model")
    def model(self) -> typing.Optional[str]:
        """``AWS::NetworkManager::Device.Model``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-model
        """
        return jsii.get(self, "model")

    @model.setter
    def model(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "model", value)

    @builtins.property
    @jsii.member(jsii_name="serialNumber")
    def serial_number(self) -> typing.Optional[str]:
        """``AWS::NetworkManager::Device.SerialNumber``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-serialnumber
        """
        return jsii.get(self, "serialNumber")

    @serial_number.setter
    def serial_number(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "serialNumber", value)

    @builtins.property
    @jsii.member(jsii_name="siteId")
    def site_id(self) -> typing.Optional[str]:
        """``AWS::NetworkManager::Device.SiteId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-siteid
        """
        return jsii.get(self, "siteId")

    @site_id.setter
    def site_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "siteId", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[str]:
        """``AWS::NetworkManager::Device.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-type
        """
        return jsii.get(self, "type")

    @type.setter
    def type(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="vendor")
    def vendor(self) -> typing.Optional[str]:
        """``AWS::NetworkManager::Device.Vendor``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-vendor
        """
        return jsii.get(self, "vendor")

    @vendor.setter
    def vendor(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "vendor", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-networkmanager.CfnDevice.LocationProperty", jsii_struct_bases=[], name_mapping={'address': 'address', 'latitude': 'latitude', 'longitude': 'longitude'})
    class LocationProperty():
        def __init__(self, *, address: typing.Optional[str]=None, latitude: typing.Optional[str]=None, longitude: typing.Optional[str]=None) -> None:
            """
            :param address: ``CfnDevice.LocationProperty.Address``.
            :param latitude: ``CfnDevice.LocationProperty.Latitude``.
            :param longitude: ``CfnDevice.LocationProperty.Longitude``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-device-location.html
            """
            self._values = {
            }
            if address is not None: self._values["address"] = address
            if latitude is not None: self._values["latitude"] = latitude
            if longitude is not None: self._values["longitude"] = longitude

        @builtins.property
        def address(self) -> typing.Optional[str]:
            """``CfnDevice.LocationProperty.Address``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-device-location.html#cfn-networkmanager-device-location-address
            """
            return self._values.get('address')

        @builtins.property
        def latitude(self) -> typing.Optional[str]:
            """``CfnDevice.LocationProperty.Latitude``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-device-location.html#cfn-networkmanager-device-location-latitude
            """
            return self._values.get('latitude')

        @builtins.property
        def longitude(self) -> typing.Optional[str]:
            """``CfnDevice.LocationProperty.Longitude``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-device-location.html#cfn-networkmanager-device-location-longitude
            """
            return self._values.get('longitude')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LocationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-networkmanager.CfnDeviceProps", jsii_struct_bases=[], name_mapping={'global_network_id': 'globalNetworkId', 'description': 'description', 'location': 'location', 'model': 'model', 'serial_number': 'serialNumber', 'site_id': 'siteId', 'tags': 'tags', 'type': 'type', 'vendor': 'vendor'})
class CfnDeviceProps():
    def __init__(self, *, global_network_id: str, description: typing.Optional[str]=None, location: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDevice.LocationProperty"]]=None, model: typing.Optional[str]=None, serial_number: typing.Optional[str]=None, site_id: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, type: typing.Optional[str]=None, vendor: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::NetworkManager::Device``.

        :param global_network_id: ``AWS::NetworkManager::Device.GlobalNetworkId``.
        :param description: ``AWS::NetworkManager::Device.Description``.
        :param location: ``AWS::NetworkManager::Device.Location``.
        :param model: ``AWS::NetworkManager::Device.Model``.
        :param serial_number: ``AWS::NetworkManager::Device.SerialNumber``.
        :param site_id: ``AWS::NetworkManager::Device.SiteId``.
        :param tags: ``AWS::NetworkManager::Device.Tags``.
        :param type: ``AWS::NetworkManager::Device.Type``.
        :param vendor: ``AWS::NetworkManager::Device.Vendor``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html
        """
        self._values = {
            'global_network_id': global_network_id,
        }
        if description is not None: self._values["description"] = description
        if location is not None: self._values["location"] = location
        if model is not None: self._values["model"] = model
        if serial_number is not None: self._values["serial_number"] = serial_number
        if site_id is not None: self._values["site_id"] = site_id
        if tags is not None: self._values["tags"] = tags
        if type is not None: self._values["type"] = type
        if vendor is not None: self._values["vendor"] = vendor

    @builtins.property
    def global_network_id(self) -> str:
        """``AWS::NetworkManager::Device.GlobalNetworkId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-globalnetworkid
        """
        return self._values.get('global_network_id')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::NetworkManager::Device.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-description
        """
        return self._values.get('description')

    @builtins.property
    def location(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDevice.LocationProperty"]]:
        """``AWS::NetworkManager::Device.Location``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-location
        """
        return self._values.get('location')

    @builtins.property
    def model(self) -> typing.Optional[str]:
        """``AWS::NetworkManager::Device.Model``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-model
        """
        return self._values.get('model')

    @builtins.property
    def serial_number(self) -> typing.Optional[str]:
        """``AWS::NetworkManager::Device.SerialNumber``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-serialnumber
        """
        return self._values.get('serial_number')

    @builtins.property
    def site_id(self) -> typing.Optional[str]:
        """``AWS::NetworkManager::Device.SiteId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-siteid
        """
        return self._values.get('site_id')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::NetworkManager::Device.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-tags
        """
        return self._values.get('tags')

    @builtins.property
    def type(self) -> typing.Optional[str]:
        """``AWS::NetworkManager::Device.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-type
        """
        return self._values.get('type')

    @builtins.property
    def vendor(self) -> typing.Optional[str]:
        """``AWS::NetworkManager::Device.Vendor``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-vendor
        """
        return self._values.get('vendor')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDeviceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnGlobalNetwork(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-networkmanager.CfnGlobalNetwork"):
    """A CloudFormation ``AWS::NetworkManager::GlobalNetwork``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-globalnetwork.html
    cloudformationResource:
    :cloudformationResource:: AWS::NetworkManager::GlobalNetwork
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, description: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::NetworkManager::GlobalNetwork``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::NetworkManager::GlobalNetwork.Description``.
        :param tags: ``AWS::NetworkManager::GlobalNetwork.Tags``.
        """
        props = CfnGlobalNetworkProps(description=description, tags=tags)

        jsii.create(CfnGlobalNetwork, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnGlobalNetwork":
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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

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
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::NetworkManager::GlobalNetwork.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-globalnetwork.html#cfn-networkmanager-globalnetwork-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::NetworkManager::GlobalNetwork.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-globalnetwork.html#cfn-networkmanager-globalnetwork-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-networkmanager.CfnGlobalNetworkProps", jsii_struct_bases=[], name_mapping={'description': 'description', 'tags': 'tags'})
class CfnGlobalNetworkProps():
    def __init__(self, *, description: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Properties for defining a ``AWS::NetworkManager::GlobalNetwork``.

        :param description: ``AWS::NetworkManager::GlobalNetwork.Description``.
        :param tags: ``AWS::NetworkManager::GlobalNetwork.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-globalnetwork.html
        """
        self._values = {
        }
        if description is not None: self._values["description"] = description
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::NetworkManager::GlobalNetwork.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-globalnetwork.html#cfn-networkmanager-globalnetwork-description
        """
        return self._values.get('description')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::NetworkManager::GlobalNetwork.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-globalnetwork.html#cfn-networkmanager-globalnetwork-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnGlobalNetworkProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnLink(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-networkmanager.CfnLink"):
    """A CloudFormation ``AWS::NetworkManager::Link``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html
    cloudformationResource:
    :cloudformationResource:: AWS::NetworkManager::Link
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, bandwidth: typing.Union["BandwidthProperty", aws_cdk.core.IResolvable], global_network_id: str, site_id: str, description: typing.Optional[str]=None, provider: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, type: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::NetworkManager::Link``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param bandwidth: ``AWS::NetworkManager::Link.Bandwidth``.
        :param global_network_id: ``AWS::NetworkManager::Link.GlobalNetworkId``.
        :param site_id: ``AWS::NetworkManager::Link.SiteId``.
        :param description: ``AWS::NetworkManager::Link.Description``.
        :param provider: ``AWS::NetworkManager::Link.Provider``.
        :param tags: ``AWS::NetworkManager::Link.Tags``.
        :param type: ``AWS::NetworkManager::Link.Type``.
        """
        props = CfnLinkProps(bandwidth=bandwidth, global_network_id=global_network_id, site_id=site_id, description=description, provider=provider, tags=tags, type=type)

        jsii.create(CfnLink, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnLink":
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
    @jsii.member(jsii_name="attrLinkArn")
    def attr_link_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: LinkArn
        """
        return jsii.get(self, "attrLinkArn")

    @builtins.property
    @jsii.member(jsii_name="attrLinkId")
    def attr_link_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: LinkId
        """
        return jsii.get(self, "attrLinkId")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::NetworkManager::Link.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="bandwidth")
    def bandwidth(self) -> typing.Union["BandwidthProperty", aws_cdk.core.IResolvable]:
        """``AWS::NetworkManager::Link.Bandwidth``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-bandwidth
        """
        return jsii.get(self, "bandwidth")

    @bandwidth.setter
    def bandwidth(self, value: typing.Union["BandwidthProperty", aws_cdk.core.IResolvable]) -> None:
        jsii.set(self, "bandwidth", value)

    @builtins.property
    @jsii.member(jsii_name="globalNetworkId")
    def global_network_id(self) -> str:
        """``AWS::NetworkManager::Link.GlobalNetworkId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-globalnetworkid
        """
        return jsii.get(self, "globalNetworkId")

    @global_network_id.setter
    def global_network_id(self, value: str) -> None:
        jsii.set(self, "globalNetworkId", value)

    @builtins.property
    @jsii.member(jsii_name="siteId")
    def site_id(self) -> str:
        """``AWS::NetworkManager::Link.SiteId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-siteid
        """
        return jsii.get(self, "siteId")

    @site_id.setter
    def site_id(self, value: str) -> None:
        jsii.set(self, "siteId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::NetworkManager::Link.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> typing.Optional[str]:
        """``AWS::NetworkManager::Link.Provider``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-provider
        """
        return jsii.get(self, "provider")

    @provider.setter
    def provider(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "provider", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[str]:
        """``AWS::NetworkManager::Link.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-type
        """
        return jsii.get(self, "type")

    @type.setter
    def type(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "type", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-networkmanager.CfnLink.BandwidthProperty", jsii_struct_bases=[], name_mapping={'download_speed': 'downloadSpeed', 'upload_speed': 'uploadSpeed'})
    class BandwidthProperty():
        def __init__(self, *, download_speed: typing.Optional[jsii.Number]=None, upload_speed: typing.Optional[jsii.Number]=None) -> None:
            """
            :param download_speed: ``CfnLink.BandwidthProperty.DownloadSpeed``.
            :param upload_speed: ``CfnLink.BandwidthProperty.UploadSpeed``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-link-bandwidth.html
            """
            self._values = {
            }
            if download_speed is not None: self._values["download_speed"] = download_speed
            if upload_speed is not None: self._values["upload_speed"] = upload_speed

        @builtins.property
        def download_speed(self) -> typing.Optional[jsii.Number]:
            """``CfnLink.BandwidthProperty.DownloadSpeed``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-link-bandwidth.html#cfn-networkmanager-link-bandwidth-downloadspeed
            """
            return self._values.get('download_speed')

        @builtins.property
        def upload_speed(self) -> typing.Optional[jsii.Number]:
            """``CfnLink.BandwidthProperty.UploadSpeed``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-link-bandwidth.html#cfn-networkmanager-link-bandwidth-uploadspeed
            """
            return self._values.get('upload_speed')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'BandwidthProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.implements(aws_cdk.core.IInspectable)
class CfnLinkAssociation(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-networkmanager.CfnLinkAssociation"):
    """A CloudFormation ``AWS::NetworkManager::LinkAssociation``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html
    cloudformationResource:
    :cloudformationResource:: AWS::NetworkManager::LinkAssociation
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, device_id: str, global_network_id: str, link_id: str) -> None:
        """Create a new ``AWS::NetworkManager::LinkAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param device_id: ``AWS::NetworkManager::LinkAssociation.DeviceId``.
        :param global_network_id: ``AWS::NetworkManager::LinkAssociation.GlobalNetworkId``.
        :param link_id: ``AWS::NetworkManager::LinkAssociation.LinkId``.
        """
        props = CfnLinkAssociationProps(device_id=device_id, global_network_id=global_network_id, link_id=link_id)

        jsii.create(CfnLinkAssociation, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnLinkAssociation":
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
    @jsii.member(jsii_name="deviceId")
    def device_id(self) -> str:
        """``AWS::NetworkManager::LinkAssociation.DeviceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html#cfn-networkmanager-linkassociation-deviceid
        """
        return jsii.get(self, "deviceId")

    @device_id.setter
    def device_id(self, value: str) -> None:
        jsii.set(self, "deviceId", value)

    @builtins.property
    @jsii.member(jsii_name="globalNetworkId")
    def global_network_id(self) -> str:
        """``AWS::NetworkManager::LinkAssociation.GlobalNetworkId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html#cfn-networkmanager-linkassociation-globalnetworkid
        """
        return jsii.get(self, "globalNetworkId")

    @global_network_id.setter
    def global_network_id(self, value: str) -> None:
        jsii.set(self, "globalNetworkId", value)

    @builtins.property
    @jsii.member(jsii_name="linkId")
    def link_id(self) -> str:
        """``AWS::NetworkManager::LinkAssociation.LinkId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html#cfn-networkmanager-linkassociation-linkid
        """
        return jsii.get(self, "linkId")

    @link_id.setter
    def link_id(self, value: str) -> None:
        jsii.set(self, "linkId", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-networkmanager.CfnLinkAssociationProps", jsii_struct_bases=[], name_mapping={'device_id': 'deviceId', 'global_network_id': 'globalNetworkId', 'link_id': 'linkId'})
class CfnLinkAssociationProps():
    def __init__(self, *, device_id: str, global_network_id: str, link_id: str) -> None:
        """Properties for defining a ``AWS::NetworkManager::LinkAssociation``.

        :param device_id: ``AWS::NetworkManager::LinkAssociation.DeviceId``.
        :param global_network_id: ``AWS::NetworkManager::LinkAssociation.GlobalNetworkId``.
        :param link_id: ``AWS::NetworkManager::LinkAssociation.LinkId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html
        """
        self._values = {
            'device_id': device_id,
            'global_network_id': global_network_id,
            'link_id': link_id,
        }

    @builtins.property
    def device_id(self) -> str:
        """``AWS::NetworkManager::LinkAssociation.DeviceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html#cfn-networkmanager-linkassociation-deviceid
        """
        return self._values.get('device_id')

    @builtins.property
    def global_network_id(self) -> str:
        """``AWS::NetworkManager::LinkAssociation.GlobalNetworkId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html#cfn-networkmanager-linkassociation-globalnetworkid
        """
        return self._values.get('global_network_id')

    @builtins.property
    def link_id(self) -> str:
        """``AWS::NetworkManager::LinkAssociation.LinkId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html#cfn-networkmanager-linkassociation-linkid
        """
        return self._values.get('link_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnLinkAssociationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-networkmanager.CfnLinkProps", jsii_struct_bases=[], name_mapping={'bandwidth': 'bandwidth', 'global_network_id': 'globalNetworkId', 'site_id': 'siteId', 'description': 'description', 'provider': 'provider', 'tags': 'tags', 'type': 'type'})
class CfnLinkProps():
    def __init__(self, *, bandwidth: typing.Union["CfnLink.BandwidthProperty", aws_cdk.core.IResolvable], global_network_id: str, site_id: str, description: typing.Optional[str]=None, provider: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, type: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::NetworkManager::Link``.

        :param bandwidth: ``AWS::NetworkManager::Link.Bandwidth``.
        :param global_network_id: ``AWS::NetworkManager::Link.GlobalNetworkId``.
        :param site_id: ``AWS::NetworkManager::Link.SiteId``.
        :param description: ``AWS::NetworkManager::Link.Description``.
        :param provider: ``AWS::NetworkManager::Link.Provider``.
        :param tags: ``AWS::NetworkManager::Link.Tags``.
        :param type: ``AWS::NetworkManager::Link.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html
        """
        self._values = {
            'bandwidth': bandwidth,
            'global_network_id': global_network_id,
            'site_id': site_id,
        }
        if description is not None: self._values["description"] = description
        if provider is not None: self._values["provider"] = provider
        if tags is not None: self._values["tags"] = tags
        if type is not None: self._values["type"] = type

    @builtins.property
    def bandwidth(self) -> typing.Union["CfnLink.BandwidthProperty", aws_cdk.core.IResolvable]:
        """``AWS::NetworkManager::Link.Bandwidth``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-bandwidth
        """
        return self._values.get('bandwidth')

    @builtins.property
    def global_network_id(self) -> str:
        """``AWS::NetworkManager::Link.GlobalNetworkId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-globalnetworkid
        """
        return self._values.get('global_network_id')

    @builtins.property
    def site_id(self) -> str:
        """``AWS::NetworkManager::Link.SiteId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-siteid
        """
        return self._values.get('site_id')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::NetworkManager::Link.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-description
        """
        return self._values.get('description')

    @builtins.property
    def provider(self) -> typing.Optional[str]:
        """``AWS::NetworkManager::Link.Provider``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-provider
        """
        return self._values.get('provider')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::NetworkManager::Link.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-tags
        """
        return self._values.get('tags')

    @builtins.property
    def type(self) -> typing.Optional[str]:
        """``AWS::NetworkManager::Link.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-type
        """
        return self._values.get('type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnLinkProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnSite(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-networkmanager.CfnSite"):
    """A CloudFormation ``AWS::NetworkManager::Site``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html
    cloudformationResource:
    :cloudformationResource:: AWS::NetworkManager::Site
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, global_network_id: str, description: typing.Optional[str]=None, location: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "LocationProperty"]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::NetworkManager::Site``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param global_network_id: ``AWS::NetworkManager::Site.GlobalNetworkId``.
        :param description: ``AWS::NetworkManager::Site.Description``.
        :param location: ``AWS::NetworkManager::Site.Location``.
        :param tags: ``AWS::NetworkManager::Site.Tags``.
        """
        props = CfnSiteProps(global_network_id=global_network_id, description=description, location=location, tags=tags)

        jsii.create(CfnSite, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnSite":
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
    @jsii.member(jsii_name="attrSiteArn")
    def attr_site_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: SiteArn
        """
        return jsii.get(self, "attrSiteArn")

    @builtins.property
    @jsii.member(jsii_name="attrSiteId")
    def attr_site_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: SiteId
        """
        return jsii.get(self, "attrSiteId")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::NetworkManager::Site.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="globalNetworkId")
    def global_network_id(self) -> str:
        """``AWS::NetworkManager::Site.GlobalNetworkId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-globalnetworkid
        """
        return jsii.get(self, "globalNetworkId")

    @global_network_id.setter
    def global_network_id(self, value: str) -> None:
        jsii.set(self, "globalNetworkId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::NetworkManager::Site.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "LocationProperty"]]:
        """``AWS::NetworkManager::Site.Location``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-location
        """
        return jsii.get(self, "location")

    @location.setter
    def location(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "LocationProperty"]]) -> None:
        jsii.set(self, "location", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-networkmanager.CfnSite.LocationProperty", jsii_struct_bases=[], name_mapping={'address': 'address', 'latitude': 'latitude', 'longitude': 'longitude'})
    class LocationProperty():
        def __init__(self, *, address: typing.Optional[str]=None, latitude: typing.Optional[str]=None, longitude: typing.Optional[str]=None) -> None:
            """
            :param address: ``CfnSite.LocationProperty.Address``.
            :param latitude: ``CfnSite.LocationProperty.Latitude``.
            :param longitude: ``CfnSite.LocationProperty.Longitude``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-site-location.html
            """
            self._values = {
            }
            if address is not None: self._values["address"] = address
            if latitude is not None: self._values["latitude"] = latitude
            if longitude is not None: self._values["longitude"] = longitude

        @builtins.property
        def address(self) -> typing.Optional[str]:
            """``CfnSite.LocationProperty.Address``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-site-location.html#cfn-networkmanager-site-location-address
            """
            return self._values.get('address')

        @builtins.property
        def latitude(self) -> typing.Optional[str]:
            """``CfnSite.LocationProperty.Latitude``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-site-location.html#cfn-networkmanager-site-location-latitude
            """
            return self._values.get('latitude')

        @builtins.property
        def longitude(self) -> typing.Optional[str]:
            """``CfnSite.LocationProperty.Longitude``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-site-location.html#cfn-networkmanager-site-location-longitude
            """
            return self._values.get('longitude')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LocationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-networkmanager.CfnSiteProps", jsii_struct_bases=[], name_mapping={'global_network_id': 'globalNetworkId', 'description': 'description', 'location': 'location', 'tags': 'tags'})
class CfnSiteProps():
    def __init__(self, *, global_network_id: str, description: typing.Optional[str]=None, location: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnSite.LocationProperty"]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Properties for defining a ``AWS::NetworkManager::Site``.

        :param global_network_id: ``AWS::NetworkManager::Site.GlobalNetworkId``.
        :param description: ``AWS::NetworkManager::Site.Description``.
        :param location: ``AWS::NetworkManager::Site.Location``.
        :param tags: ``AWS::NetworkManager::Site.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html
        """
        self._values = {
            'global_network_id': global_network_id,
        }
        if description is not None: self._values["description"] = description
        if location is not None: self._values["location"] = location
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def global_network_id(self) -> str:
        """``AWS::NetworkManager::Site.GlobalNetworkId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-globalnetworkid
        """
        return self._values.get('global_network_id')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::NetworkManager::Site.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-description
        """
        return self._values.get('description')

    @builtins.property
    def location(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnSite.LocationProperty"]]:
        """``AWS::NetworkManager::Site.Location``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-location
        """
        return self._values.get('location')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::NetworkManager::Site.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnSiteProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnTransitGatewayRegistration(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-networkmanager.CfnTransitGatewayRegistration"):
    """A CloudFormation ``AWS::NetworkManager::TransitGatewayRegistration``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayregistration.html
    cloudformationResource:
    :cloudformationResource:: AWS::NetworkManager::TransitGatewayRegistration
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, global_network_id: str, transit_gateway_arn: str) -> None:
        """Create a new ``AWS::NetworkManager::TransitGatewayRegistration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param global_network_id: ``AWS::NetworkManager::TransitGatewayRegistration.GlobalNetworkId``.
        :param transit_gateway_arn: ``AWS::NetworkManager::TransitGatewayRegistration.TransitGatewayArn``.
        """
        props = CfnTransitGatewayRegistrationProps(global_network_id=global_network_id, transit_gateway_arn=transit_gateway_arn)

        jsii.create(CfnTransitGatewayRegistration, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnTransitGatewayRegistration":
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
    @jsii.member(jsii_name="globalNetworkId")
    def global_network_id(self) -> str:
        """``AWS::NetworkManager::TransitGatewayRegistration.GlobalNetworkId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayregistration.html#cfn-networkmanager-transitgatewayregistration-globalnetworkid
        """
        return jsii.get(self, "globalNetworkId")

    @global_network_id.setter
    def global_network_id(self, value: str) -> None:
        jsii.set(self, "globalNetworkId", value)

    @builtins.property
    @jsii.member(jsii_name="transitGatewayArn")
    def transit_gateway_arn(self) -> str:
        """``AWS::NetworkManager::TransitGatewayRegistration.TransitGatewayArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayregistration.html#cfn-networkmanager-transitgatewayregistration-transitgatewayarn
        """
        return jsii.get(self, "transitGatewayArn")

    @transit_gateway_arn.setter
    def transit_gateway_arn(self, value: str) -> None:
        jsii.set(self, "transitGatewayArn", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-networkmanager.CfnTransitGatewayRegistrationProps", jsii_struct_bases=[], name_mapping={'global_network_id': 'globalNetworkId', 'transit_gateway_arn': 'transitGatewayArn'})
class CfnTransitGatewayRegistrationProps():
    def __init__(self, *, global_network_id: str, transit_gateway_arn: str) -> None:
        """Properties for defining a ``AWS::NetworkManager::TransitGatewayRegistration``.

        :param global_network_id: ``AWS::NetworkManager::TransitGatewayRegistration.GlobalNetworkId``.
        :param transit_gateway_arn: ``AWS::NetworkManager::TransitGatewayRegistration.TransitGatewayArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayregistration.html
        """
        self._values = {
            'global_network_id': global_network_id,
            'transit_gateway_arn': transit_gateway_arn,
        }

    @builtins.property
    def global_network_id(self) -> str:
        """``AWS::NetworkManager::TransitGatewayRegistration.GlobalNetworkId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayregistration.html#cfn-networkmanager-transitgatewayregistration-globalnetworkid
        """
        return self._values.get('global_network_id')

    @builtins.property
    def transit_gateway_arn(self) -> str:
        """``AWS::NetworkManager::TransitGatewayRegistration.TransitGatewayArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayregistration.html#cfn-networkmanager-transitgatewayregistration-transitgatewayarn
        """
        return self._values.get('transit_gateway_arn')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnTransitGatewayRegistrationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnCustomerGatewayAssociation",
    "CfnCustomerGatewayAssociationProps",
    "CfnDevice",
    "CfnDeviceProps",
    "CfnGlobalNetwork",
    "CfnGlobalNetworkProps",
    "CfnLink",
    "CfnLinkAssociation",
    "CfnLinkAssociationProps",
    "CfnLinkProps",
    "CfnSite",
    "CfnSiteProps",
    "CfnTransitGatewayRegistration",
    "CfnTransitGatewayRegistrationProps",
]

publication.publish()
