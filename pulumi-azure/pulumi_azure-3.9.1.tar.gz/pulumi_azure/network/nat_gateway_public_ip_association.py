# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class NatGatewayPublicIpAssociation(pulumi.CustomResource):
    nat_gateway_id: pulumi.Output[str]
    """
    The ID of the Nat Gateway. Changing this forces a new resource to be created.
    """
    public_ip_address_id: pulumi.Output[str]
    """
    The ID of the Public IP which this Nat Gateway which should be connected to. Changing this forces a new resource to be created.
    """
    def __init__(__self__, resource_name, opts=None, nat_gateway_id=None, public_ip_address_id=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages the association between a Nat Gateway and a Public IP.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_public_ip = azure.network.PublicIp("examplePublicIp",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            allocation_method="Static",
            sku="Standard")
        example_nat_gateway = azure.network.NatGateway("exampleNatGateway",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku_name="Standard")
        example_nat_gateway_public_ip_association = azure.network.NatGatewayPublicIpAssociation("exampleNatGatewayPublicIpAssociation",
            nat_gateway_id=example_nat_gateway.id,
            public_ip_address_id=example_public_ip.id)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] nat_gateway_id: The ID of the Nat Gateway. Changing this forces a new resource to be created.
        :param pulumi.Input[str] public_ip_address_id: The ID of the Public IP which this Nat Gateway which should be connected to. Changing this forces a new resource to be created.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            if nat_gateway_id is None:
                raise TypeError("Missing required property 'nat_gateway_id'")
            __props__['nat_gateway_id'] = nat_gateway_id
            if public_ip_address_id is None:
                raise TypeError("Missing required property 'public_ip_address_id'")
            __props__['public_ip_address_id'] = public_ip_address_id
        super(NatGatewayPublicIpAssociation, __self__).__init__(
            'azure:network/natGatewayPublicIpAssociation:NatGatewayPublicIpAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, nat_gateway_id=None, public_ip_address_id=None):
        """
        Get an existing NatGatewayPublicIpAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] nat_gateway_id: The ID of the Nat Gateway. Changing this forces a new resource to be created.
        :param pulumi.Input[str] public_ip_address_id: The ID of the Public IP which this Nat Gateway which should be connected to. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["nat_gateway_id"] = nat_gateway_id
        __props__["public_ip_address_id"] = public_ip_address_id
        return NatGatewayPublicIpAssociation(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
