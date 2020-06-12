# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetCustomerGatewayResult:
    """
    A collection of values returned by getCustomerGateway.
    """
    def __init__(__self__, bgp_asn=None, filters=None, id=None, ip_address=None, tags=None, type=None):
        if bgp_asn and not isinstance(bgp_asn, float):
            raise TypeError("Expected argument 'bgp_asn' to be a float")
        __self__.bgp_asn = bgp_asn
        """
        (Optional) The gateway's Border Gateway Protocol (BGP) Autonomous System Number (ASN).
        """
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        __self__.filters = filters
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        if ip_address and not isinstance(ip_address, str):
            raise TypeError("Expected argument 'ip_address' to be a str")
        __self__.ip_address = ip_address
        """
        (Optional) The IP address of the gateway's Internet-routable external interface.
        """
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags
        """
        Map of key-value pairs assigned to the gateway.
        """
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        __self__.type = type
        """
        (Optional) The type of customer gateway. The only type AWS supports at this time is "ipsec.1".
        """
class AwaitableGetCustomerGatewayResult(GetCustomerGatewayResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCustomerGatewayResult(
            bgp_asn=self.bgp_asn,
            filters=self.filters,
            id=self.id,
            ip_address=self.ip_address,
            tags=self.tags,
            type=self.type)

def get_customer_gateway(filters=None,id=None,tags=None,opts=None):
    """
    Get an existing AWS Customer Gateway.

    ## Example Usage



    ```python
    import pulumi
    import pulumi_aws as aws

    foo = aws.ec2.get_customer_gateway(filters=[{
        "name": "tag:Name",
        "values": ["foo-prod"],
    }])
    main = aws.ec2.VpnGateway("main",
        amazon_side_asn=7224,
        vpc_id=aws_vpc["main"]["id"])
    transit = aws.ec2.VpnConnection("transit",
        customer_gateway_id=foo.id,
        static_routes_only=False,
        type=foo.type,
        vpn_gateway_id=main.id)
    ```


    :param list filters: One or more [name-value pairs][dcg-filters] to filter by.
    :param str id: The ID of the gateway.
    :param dict tags: Map of key-value pairs assigned to the gateway.

    The **filters** object supports the following:

      * `name` (`str`)
      * `values` (`list`)
    """
    __args__ = dict()


    __args__['filters'] = filters
    __args__['id'] = id
    __args__['tags'] = tags
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:ec2/getCustomerGateway:getCustomerGateway', __args__, opts=opts).value

    return AwaitableGetCustomerGatewayResult(
        bgp_asn=__ret__.get('bgpAsn'),
        filters=__ret__.get('filters'),
        id=__ret__.get('id'),
        ip_address=__ret__.get('ipAddress'),
        tags=__ret__.get('tags'),
        type=__ret__.get('type'))
