# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class FirewallRule(pulumi.CustomResource):
    end_ip: pulumi.Output[str]
    """
    The highest IP address included in the range.
    """
    name: pulumi.Output[str]
    """
    The name of the Firewall Rule. Changing this forces a new resource to be created.
    """
    redis_cache_name: pulumi.Output[str]
    """
    The name of the Redis Cache. Changing this forces a new resource to be created.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group in which this Redis Cache exists.
    """
    start_ip: pulumi.Output[str]
    """
    The lowest IP address included in the range
    """
    def __init__(__self__, resource_name, opts=None, end_ip=None, name=None, redis_cache_name=None, resource_group_name=None, start_ip=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages a Firewall Rule associated with a Redis Cache.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_azure as azure
        import pulumi_random as random

        server = random.RandomId("server",
            keepers={
                "azi_id": 1,
            },
            byte_length=8)
        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_cache = azure.redis.Cache("exampleCache",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            capacity=1,
            family="P",
            sku_name="Premium",
            enable_non_ssl_port=False,
            redis_configuration={
                "maxclients": 256,
                "maxmemoryReserved": 2,
                "maxmemoryDelta": 2,
                "maxmemoryPolicy": "allkeys-lru",
            })
        example_firewall_rule = azure.redis.FirewallRule("exampleFirewallRule",
            redis_cache_name=example_cache.name,
            resource_group_name=example_resource_group.name,
            start_ip="1.2.3.4",
            end_ip="2.3.4.5")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] end_ip: The highest IP address included in the range.
        :param pulumi.Input[str] name: The name of the Firewall Rule. Changing this forces a new resource to be created.
        :param pulumi.Input[str] redis_cache_name: The name of the Redis Cache. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which this Redis Cache exists.
        :param pulumi.Input[str] start_ip: The lowest IP address included in the range
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

            if end_ip is None:
                raise TypeError("Missing required property 'end_ip'")
            __props__['end_ip'] = end_ip
            __props__['name'] = name
            if redis_cache_name is None:
                raise TypeError("Missing required property 'redis_cache_name'")
            __props__['redis_cache_name'] = redis_cache_name
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if start_ip is None:
                raise TypeError("Missing required property 'start_ip'")
            __props__['start_ip'] = start_ip
        super(FirewallRule, __self__).__init__(
            'azure:redis/firewallRule:FirewallRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, end_ip=None, name=None, redis_cache_name=None, resource_group_name=None, start_ip=None):
        """
        Get an existing FirewallRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] end_ip: The highest IP address included in the range.
        :param pulumi.Input[str] name: The name of the Firewall Rule. Changing this forces a new resource to be created.
        :param pulumi.Input[str] redis_cache_name: The name of the Redis Cache. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which this Redis Cache exists.
        :param pulumi.Input[str] start_ip: The lowest IP address included in the range
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["end_ip"] = end_ip
        __props__["name"] = name
        __props__["redis_cache_name"] = redis_cache_name
        __props__["resource_group_name"] = resource_group_name
        __props__["start_ip"] = start_ip
        return FirewallRule(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
