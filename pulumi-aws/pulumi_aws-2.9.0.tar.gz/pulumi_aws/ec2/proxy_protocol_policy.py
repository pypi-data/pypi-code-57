# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class ProxyProtocolPolicy(pulumi.CustomResource):
    instance_ports: pulumi.Output[list]
    """
    List of instance ports to which the policy
    should be applied. This can be specified if the protocol is SSL or TCP.
    """
    load_balancer: pulumi.Output[str]
    """
    The load balancer to which the policy
    should be attached.
    """
    def __init__(__self__, resource_name, opts=None, instance_ports=None, load_balancer=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a proxy protocol policy, which allows an ELB to carry a client connection information to a backend.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_aws as aws

        lb = aws.elb.LoadBalancer("lb",
            availability_zones=["us-east-1a"],
            listeners=[
                {
                    "instance_port": 25,
                    "instanceProtocol": "tcp",
                    "lb_port": 25,
                    "lbProtocol": "tcp",
                },
                {
                    "instance_port": 587,
                    "instanceProtocol": "tcp",
                    "lb_port": 587,
                    "lbProtocol": "tcp",
                },
            ])
        smtp = aws.ec2.ProxyProtocolPolicy("smtp",
            instance_ports=[
                "25",
                "587",
            ],
            load_balancer=lb.name)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] instance_ports: List of instance ports to which the policy
               should be applied. This can be specified if the protocol is SSL or TCP.
        :param pulumi.Input[str] load_balancer: The load balancer to which the policy
               should be attached.
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

            if instance_ports is None:
                raise TypeError("Missing required property 'instance_ports'")
            __props__['instance_ports'] = instance_ports
            if load_balancer is None:
                raise TypeError("Missing required property 'load_balancer'")
            __props__['load_balancer'] = load_balancer
        super(ProxyProtocolPolicy, __self__).__init__(
            'aws:ec2/proxyProtocolPolicy:ProxyProtocolPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, instance_ports=None, load_balancer=None):
        """
        Get an existing ProxyProtocolPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] instance_ports: List of instance ports to which the policy
               should be applied. This can be specified if the protocol is SSL or TCP.
        :param pulumi.Input[str] load_balancer: The load balancer to which the policy
               should be attached.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["instance_ports"] = instance_ports
        __props__["load_balancer"] = load_balancer
        return ProxyProtocolPolicy(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

