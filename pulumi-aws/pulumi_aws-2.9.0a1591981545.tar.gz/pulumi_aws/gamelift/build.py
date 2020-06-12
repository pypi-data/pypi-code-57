# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class Build(pulumi.CustomResource):
    arn: pulumi.Output[str]
    """
    Gamelift Build ARN.
    """
    name: pulumi.Output[str]
    """
    Name of the build
    """
    operating_system: pulumi.Output[str]
    """
    Operating system that the game server binaries are built to run on. e.g. `WINDOWS_2012` or `AMAZON_LINUX`.
    """
    storage_location: pulumi.Output[dict]
    """
    Information indicating where your game build files are stored. See below.

      * `bucket` (`str`) - Name of your S3 bucket.
      * `key` (`str`) - Name of the zip file containing your build files.
      * `role_arn` (`str`) - ARN of the access role that allows Amazon GameLift to access your S3 bucket.
    """
    tags: pulumi.Output[dict]
    """
    Key-value map of resource tags
    """
    version: pulumi.Output[str]
    """
    Version that is associated with this build.
    """
    def __init__(__self__, resource_name, opts=None, name=None, operating_system=None, storage_location=None, tags=None, version=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an Gamelift Build resource.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.gamelift.Build("test",
            operating_system="WINDOWS_2012",
            storage_location={
                "bucket": aws_s3_bucket["test"]["bucket"],
                "key": aws_s3_bucket_object["test"]["key"],
                "role_arn": aws_iam_role["test"]["arn"],
            })
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: Name of the build
        :param pulumi.Input[str] operating_system: Operating system that the game server binaries are built to run on. e.g. `WINDOWS_2012` or `AMAZON_LINUX`.
        :param pulumi.Input[dict] storage_location: Information indicating where your game build files are stored. See below.
        :param pulumi.Input[dict] tags: Key-value map of resource tags
        :param pulumi.Input[str] version: Version that is associated with this build.

        The **storage_location** object supports the following:

          * `bucket` (`pulumi.Input[str]`) - Name of your S3 bucket.
          * `key` (`pulumi.Input[str]`) - Name of the zip file containing your build files.
          * `role_arn` (`pulumi.Input[str]`) - ARN of the access role that allows Amazon GameLift to access your S3 bucket.
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

            __props__['name'] = name
            if operating_system is None:
                raise TypeError("Missing required property 'operating_system'")
            __props__['operating_system'] = operating_system
            if storage_location is None:
                raise TypeError("Missing required property 'storage_location'")
            __props__['storage_location'] = storage_location
            __props__['tags'] = tags
            __props__['version'] = version
            __props__['arn'] = None
        super(Build, __self__).__init__(
            'aws:gamelift/build:Build',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, arn=None, name=None, operating_system=None, storage_location=None, tags=None, version=None):
        """
        Get an existing Build resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: Gamelift Build ARN.
        :param pulumi.Input[str] name: Name of the build
        :param pulumi.Input[str] operating_system: Operating system that the game server binaries are built to run on. e.g. `WINDOWS_2012` or `AMAZON_LINUX`.
        :param pulumi.Input[dict] storage_location: Information indicating where your game build files are stored. See below.
        :param pulumi.Input[dict] tags: Key-value map of resource tags
        :param pulumi.Input[str] version: Version that is associated with this build.

        The **storage_location** object supports the following:

          * `bucket` (`pulumi.Input[str]`) - Name of your S3 bucket.
          * `key` (`pulumi.Input[str]`) - Name of the zip file containing your build files.
          * `role_arn` (`pulumi.Input[str]`) - ARN of the access role that allows Amazon GameLift to access your S3 bucket.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["name"] = name
        __props__["operating_system"] = operating_system
        __props__["storage_location"] = storage_location
        __props__["tags"] = tags
        __props__["version"] = version
        return Build(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

