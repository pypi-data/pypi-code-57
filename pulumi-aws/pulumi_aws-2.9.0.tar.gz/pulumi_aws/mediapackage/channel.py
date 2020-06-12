# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class Channel(pulumi.CustomResource):
    arn: pulumi.Output[str]
    """
    The ARN of the channel
    """
    channel_id: pulumi.Output[str]
    """
    A unique identifier describing the channel
    """
    description: pulumi.Output[str]
    """
    A description of the channel
    """
    hls_ingests: pulumi.Output[list]
    """
    A single item list of HLS ingest information

      * `ingestEndpoints` (`list`) - A list of the ingest endpoints
        * `password` (`str`) - The password
        * `url` (`str`) - The URL
        * `username` (`str`) - The username
    """
    tags: pulumi.Output[dict]
    """
    A map of tags to assign to the resource.
    """
    def __init__(__self__, resource_name, opts=None, channel_id=None, description=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an AWS Elemental MediaPackage Channel.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_aws as aws

        kittens = aws.mediapackage.Channel("kittens",
            channel_id="kitten-channel",
            description="A channel dedicated to amusing videos of kittens.")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] channel_id: A unique identifier describing the channel
        :param pulumi.Input[str] description: A description of the channel
        :param pulumi.Input[dict] tags: A map of tags to assign to the resource.
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

            if channel_id is None:
                raise TypeError("Missing required property 'channel_id'")
            __props__['channel_id'] = channel_id
            if description is None:
                description = 'Managed by Pulumi'
            __props__['description'] = description
            __props__['tags'] = tags
            __props__['arn'] = None
            __props__['hls_ingests'] = None
        super(Channel, __self__).__init__(
            'aws:mediapackage/channel:Channel',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, arn=None, channel_id=None, description=None, hls_ingests=None, tags=None):
        """
        Get an existing Channel resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the channel
        :param pulumi.Input[str] channel_id: A unique identifier describing the channel
        :param pulumi.Input[str] description: A description of the channel
        :param pulumi.Input[list] hls_ingests: A single item list of HLS ingest information
        :param pulumi.Input[dict] tags: A map of tags to assign to the resource.

        The **hls_ingests** object supports the following:

          * `ingestEndpoints` (`pulumi.Input[list]`) - A list of the ingest endpoints
            * `password` (`pulumi.Input[str]`) - The password
            * `url` (`pulumi.Input[str]`) - The URL
            * `username` (`pulumi.Input[str]`) - The username
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["channel_id"] = channel_id
        __props__["description"] = description
        __props__["hls_ingests"] = hls_ingests
        __props__["tags"] = tags
        return Channel(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

