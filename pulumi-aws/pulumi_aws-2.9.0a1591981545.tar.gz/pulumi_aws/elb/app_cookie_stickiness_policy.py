# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class AppCookieStickinessPolicy(pulumi.CustomResource):
    cookie_name: pulumi.Output[str]
    """
    The application cookie whose lifetime the ELB's cookie should follow.
    """
    lb_port: pulumi.Output[float]
    """
    The load balancer port to which the policy
    should be applied. This must be an active listener on the load
    balancer.
    """
    load_balancer: pulumi.Output[str]
    """
    The name of load balancer to which the policy
    should be attached.
    """
    name: pulumi.Output[str]
    """
    The name of the stickiness policy.
    """
    def __init__(__self__, resource_name, opts=None, cookie_name=None, lb_port=None, load_balancer=None, name=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an application cookie stickiness policy, which allows an ELB to wed its sticky cookie's expiration to a cookie generated by your application.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_aws as aws

        lb = aws.elb.LoadBalancer("lb",
            availability_zones=["us-east-1a"],
            listeners=[{
                "instance_port": 8000,
                "instanceProtocol": "http",
                "lb_port": 80,
                "lbProtocol": "http",
            }])
        foo = aws.elb.AppCookieStickinessPolicy("foo",
            cookie_name="MyAppCookie",
            lb_port=80,
            load_balancer=lb.name)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cookie_name: The application cookie whose lifetime the ELB's cookie should follow.
        :param pulumi.Input[float] lb_port: The load balancer port to which the policy
               should be applied. This must be an active listener on the load
               balancer.
        :param pulumi.Input[str] load_balancer: The name of load balancer to which the policy
               should be attached.
        :param pulumi.Input[str] name: The name of the stickiness policy.
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

            if cookie_name is None:
                raise TypeError("Missing required property 'cookie_name'")
            __props__['cookie_name'] = cookie_name
            if lb_port is None:
                raise TypeError("Missing required property 'lb_port'")
            __props__['lb_port'] = lb_port
            if load_balancer is None:
                raise TypeError("Missing required property 'load_balancer'")
            __props__['load_balancer'] = load_balancer
            __props__['name'] = name
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="aws:elasticloadbalancing/appCookieStickinessPolicy:AppCookieStickinessPolicy")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(AppCookieStickinessPolicy, __self__).__init__(
            'aws:elb/appCookieStickinessPolicy:AppCookieStickinessPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, cookie_name=None, lb_port=None, load_balancer=None, name=None):
        """
        Get an existing AppCookieStickinessPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cookie_name: The application cookie whose lifetime the ELB's cookie should follow.
        :param pulumi.Input[float] lb_port: The load balancer port to which the policy
               should be applied. This must be an active listener on the load
               balancer.
        :param pulumi.Input[str] load_balancer: The name of load balancer to which the policy
               should be attached.
        :param pulumi.Input[str] name: The name of the stickiness policy.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["cookie_name"] = cookie_name
        __props__["lb_port"] = lb_port
        __props__["load_balancer"] = load_balancer
        __props__["name"] = name
        return AppCookieStickinessPolicy(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

