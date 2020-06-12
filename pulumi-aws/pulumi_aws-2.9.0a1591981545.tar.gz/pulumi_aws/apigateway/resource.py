# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class Resource(pulumi.CustomResource):
    parent_id: pulumi.Output[str]
    """
    The ID of the parent API resource
    """
    path: pulumi.Output[str]
    """
    The complete path for this API resource, including all parent paths.
    """
    path_part: pulumi.Output[str]
    """
    The last path segment of this API resource.
    """
    rest_api: pulumi.Output[str]
    """
    The ID of the associated REST API
    """
    def __init__(__self__, resource_name, opts=None, parent_id=None, path_part=None, rest_api=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an API Gateway Resource.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_aws as aws

        my_demo_api = aws.apigateway.RestApi("myDemoAPI", description="This is my API for demonstration purposes")
        my_demo_resource = aws.apigateway.Resource("myDemoResource",
            parent_id=my_demo_api.root_resource_id,
            path_part="mydemoresource",
            rest_api=my_demo_api.id)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] parent_id: The ID of the parent API resource
        :param pulumi.Input[str] path_part: The last path segment of this API resource.
        :param pulumi.Input[dict] rest_api: The ID of the associated REST API
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

            if parent_id is None:
                raise TypeError("Missing required property 'parent_id'")
            __props__['parent_id'] = parent_id
            if path_part is None:
                raise TypeError("Missing required property 'path_part'")
            __props__['path_part'] = path_part
            if rest_api is None:
                raise TypeError("Missing required property 'rest_api'")
            __props__['rest_api'] = rest_api
            __props__['path'] = None
        super(Resource, __self__).__init__(
            'aws:apigateway/resource:Resource',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, parent_id=None, path=None, path_part=None, rest_api=None):
        """
        Get an existing Resource resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] parent_id: The ID of the parent API resource
        :param pulumi.Input[str] path: The complete path for this API resource, including all parent paths.
        :param pulumi.Input[str] path_part: The last path segment of this API resource.
        :param pulumi.Input[dict] rest_api: The ID of the associated REST API
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["parent_id"] = parent_id
        __props__["path"] = path
        __props__["path_part"] = path_part
        __props__["rest_api"] = rest_api
        return Resource(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

