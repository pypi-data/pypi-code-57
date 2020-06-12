# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class Eip(pulumi.CustomResource):
    allocation_id: pulumi.Output[str]
    associate_with_private_ip: pulumi.Output[str]
    """
    A user specified primary or secondary private IP address to
    associate with the Elastic IP address. If no private IP address is specified,
    the Elastic IP address is associated with the primary private IP address.
    """
    association_id: pulumi.Output[str]
    customer_owned_ip: pulumi.Output[str]
    """
    Customer owned IP.
    """
    customer_owned_ipv4_pool: pulumi.Output[str]
    """
    The  ID  of a customer-owned address pool. For more on customer owned IP addressed check out [Customer-owned IP addresses guide](https://docs.aws.amazon.com/outposts/latest/userguide/outposts-networking-components.html#ip-addressing)
    """
    domain: pulumi.Output[str]
    instance: pulumi.Output[str]
    """
    EC2 instance ID.
    """
    network_interface: pulumi.Output[str]
    """
    Network interface ID to associate with.
    """
    private_dns: pulumi.Output[str]
    """
    The Private DNS associated with the Elastic IP address (if in VPC).
    """
    private_ip: pulumi.Output[str]
    """
    Contains the private IP address (if in VPC).
    """
    public_dns: pulumi.Output[str]
    """
    Public DNS associated with the Elastic IP address.
    """
    public_ip: pulumi.Output[str]
    """
    Contains the public IP address.
    """
    public_ipv4_pool: pulumi.Output[str]
    """
    EC2 IPv4 address pool identifier or `amazon`. This option is only available for VPC EIPs.
    """
    tags: pulumi.Output[dict]
    """
    A map of tags to assign to the resource.
    """
    vpc: pulumi.Output[bool]
    """
    Boolean if the EIP is in a VPC or not.
    """
    def __init__(__self__, resource_name, opts=None, associate_with_private_ip=None, customer_owned_ipv4_pool=None, instance=None, network_interface=None, public_ipv4_pool=None, tags=None, vpc=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an Elastic IP resource.

        > **Note:** EIP may require IGW to exist prior to association. Use `depends_on` to set an explicit dependency on the IGW.

        > **Note:** Do not use `network_interface` to associate the EIP to `lb.LoadBalancer` or `ec2.NatGateway` resources. Instead use the `allocation_id` available in those resources to allow AWS to manage the association, otherwise you will see `AuthFailure` errors.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_aws as aws

        lb = aws.ec2.Eip("lb",
            instance=aws_instance["web"]["id"],
            vpc=True)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] associate_with_private_ip: A user specified primary or secondary private IP address to
               associate with the Elastic IP address. If no private IP address is specified,
               the Elastic IP address is associated with the primary private IP address.
        :param pulumi.Input[str] customer_owned_ipv4_pool: The  ID  of a customer-owned address pool. For more on customer owned IP addressed check out [Customer-owned IP addresses guide](https://docs.aws.amazon.com/outposts/latest/userguide/outposts-networking-components.html#ip-addressing)
        :param pulumi.Input[str] instance: EC2 instance ID.
        :param pulumi.Input[str] network_interface: Network interface ID to associate with.
        :param pulumi.Input[str] public_ipv4_pool: EC2 IPv4 address pool identifier or `amazon`. This option is only available for VPC EIPs.
        :param pulumi.Input[dict] tags: A map of tags to assign to the resource.
        :param pulumi.Input[bool] vpc: Boolean if the EIP is in a VPC or not.
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

            __props__['associate_with_private_ip'] = associate_with_private_ip
            __props__['customer_owned_ipv4_pool'] = customer_owned_ipv4_pool
            __props__['instance'] = instance
            __props__['network_interface'] = network_interface
            __props__['public_ipv4_pool'] = public_ipv4_pool
            __props__['tags'] = tags
            __props__['vpc'] = vpc
            __props__['allocation_id'] = None
            __props__['association_id'] = None
            __props__['customer_owned_ip'] = None
            __props__['domain'] = None
            __props__['private_dns'] = None
            __props__['private_ip'] = None
            __props__['public_dns'] = None
            __props__['public_ip'] = None
        super(Eip, __self__).__init__(
            'aws:ec2/eip:Eip',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, allocation_id=None, associate_with_private_ip=None, association_id=None, customer_owned_ip=None, customer_owned_ipv4_pool=None, domain=None, instance=None, network_interface=None, private_dns=None, private_ip=None, public_dns=None, public_ip=None, public_ipv4_pool=None, tags=None, vpc=None):
        """
        Get an existing Eip resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] associate_with_private_ip: A user specified primary or secondary private IP address to
               associate with the Elastic IP address. If no private IP address is specified,
               the Elastic IP address is associated with the primary private IP address.
        :param pulumi.Input[str] customer_owned_ip: Customer owned IP.
        :param pulumi.Input[str] customer_owned_ipv4_pool: The  ID  of a customer-owned address pool. For more on customer owned IP addressed check out [Customer-owned IP addresses guide](https://docs.aws.amazon.com/outposts/latest/userguide/outposts-networking-components.html#ip-addressing)
        :param pulumi.Input[str] instance: EC2 instance ID.
        :param pulumi.Input[str] network_interface: Network interface ID to associate with.
        :param pulumi.Input[str] private_dns: The Private DNS associated with the Elastic IP address (if in VPC).
        :param pulumi.Input[str] private_ip: Contains the private IP address (if in VPC).
        :param pulumi.Input[str] public_dns: Public DNS associated with the Elastic IP address.
        :param pulumi.Input[str] public_ip: Contains the public IP address.
        :param pulumi.Input[str] public_ipv4_pool: EC2 IPv4 address pool identifier or `amazon`. This option is only available for VPC EIPs.
        :param pulumi.Input[dict] tags: A map of tags to assign to the resource.
        :param pulumi.Input[bool] vpc: Boolean if the EIP is in a VPC or not.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["allocation_id"] = allocation_id
        __props__["associate_with_private_ip"] = associate_with_private_ip
        __props__["association_id"] = association_id
        __props__["customer_owned_ip"] = customer_owned_ip
        __props__["customer_owned_ipv4_pool"] = customer_owned_ipv4_pool
        __props__["domain"] = domain
        __props__["instance"] = instance
        __props__["network_interface"] = network_interface
        __props__["private_dns"] = private_dns
        __props__["private_ip"] = private_ip
        __props__["public_dns"] = public_dns
        __props__["public_ip"] = public_ip
        __props__["public_ipv4_pool"] = public_ipv4_pool
        __props__["tags"] = tags
        __props__["vpc"] = vpc
        return Eip(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

