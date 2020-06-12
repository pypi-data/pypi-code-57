# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class WorkerRoute(pulumi.CustomResource):
    pattern: pulumi.Output[str]
    """
    The [route pattern](https://developers.cloudflare.com/workers/about/routes/)
    """
    script_name: pulumi.Output[str]
    """
    Which worker script to run for requests that match the route pattern. If `script_name` is empty, workers will be skipped for matching requests.
    """
    zone_id: pulumi.Output[str]
    """
    The zone ID to add the route to.
    """
    def __init__(__self__, resource_name, opts=None, pattern=None, script_name=None, zone_id=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a Cloudflare worker route resource. A route will also require a `.WorkerScript`. *NOTE:*  This resource uses the Cloudflare account APIs. This requires setting the `CLOUDFLARE_ACCOUNT_ID` environment variable or `account_id` provider argument.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_cloudflare as cloudflare

        my_script = cloudflare.WorkerScript("myScript")
        # see ".WorkerScript" documentation ...
        # Runs the specified worker script for all URLs that match `example.com/*`
        my_route = cloudflare.WorkerRoute("myRoute",
            zone_id="d41d8cd98f00b204e9800998ecf8427e",
            pattern="example.com/*",
            script_name=my_script.name)
        ```


        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] pattern: The [route pattern](https://developers.cloudflare.com/workers/about/routes/)
        :param pulumi.Input[str] script_name: Which worker script to run for requests that match the route pattern. If `script_name` is empty, workers will be skipped for matching requests.
        :param pulumi.Input[str] zone_id: The zone ID to add the route to.
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

            if pattern is None:
                raise TypeError("Missing required property 'pattern'")
            __props__['pattern'] = pattern
            __props__['script_name'] = script_name
            if zone_id is None:
                raise TypeError("Missing required property 'zone_id'")
            __props__['zone_id'] = zone_id
        super(WorkerRoute, __self__).__init__(
            'cloudflare:index/workerRoute:WorkerRoute',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, pattern=None, script_name=None, zone_id=None):
        """
        Get an existing WorkerRoute resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] pattern: The [route pattern](https://developers.cloudflare.com/workers/about/routes/)
        :param pulumi.Input[str] script_name: Which worker script to run for requests that match the route pattern. If `script_name` is empty, workers will be skipped for matching requests.
        :param pulumi.Input[str] zone_id: The zone ID to add the route to.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["pattern"] = pattern
        __props__["script_name"] = script_name
        __props__["zone_id"] = zone_id
        return WorkerRoute(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

