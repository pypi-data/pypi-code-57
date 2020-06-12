# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class ConditionalForwader(pulumi.CustomResource):
    directory_id: pulumi.Output[str]
    """
    The id of directory.
    """
    dns_ips: pulumi.Output[list]
    """
    A list of forwarder IP addresses.
    """
    remote_domain_name: pulumi.Output[str]
    """
    The fully qualified domain name of the remote domain for which forwarders will be used.
    """
    def __init__(__self__, resource_name, opts=None, directory_id=None, dns_ips=None, remote_domain_name=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a conditional forwarder for managed Microsoft AD in AWS Directory Service.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.directoryservice.ConditionalForwader("example",
            directory_id=aws_directory_service_directory["ad"]["id"],
            dns_ips=[
                "8.8.8.8",
                "8.8.4.4",
            ],
            remote_domain_name="example.com")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] directory_id: The id of directory.
        :param pulumi.Input[list] dns_ips: A list of forwarder IP addresses.
        :param pulumi.Input[str] remote_domain_name: The fully qualified domain name of the remote domain for which forwarders will be used.
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

            if directory_id is None:
                raise TypeError("Missing required property 'directory_id'")
            __props__['directory_id'] = directory_id
            if dns_ips is None:
                raise TypeError("Missing required property 'dns_ips'")
            __props__['dns_ips'] = dns_ips
            if remote_domain_name is None:
                raise TypeError("Missing required property 'remote_domain_name'")
            __props__['remote_domain_name'] = remote_domain_name
        super(ConditionalForwader, __self__).__init__(
            'aws:directoryservice/conditionalForwader:ConditionalForwader',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, directory_id=None, dns_ips=None, remote_domain_name=None):
        """
        Get an existing ConditionalForwader resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] directory_id: The id of directory.
        :param pulumi.Input[list] dns_ips: A list of forwarder IP addresses.
        :param pulumi.Input[str] remote_domain_name: The fully qualified domain name of the remote domain for which forwarders will be used.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["directory_id"] = directory_id
        __props__["dns_ips"] = dns_ips
        __props__["remote_domain_name"] = remote_domain_name
        return ConditionalForwader(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

