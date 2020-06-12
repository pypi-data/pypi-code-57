# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class UsagePlanKey(pulumi.CustomResource):
    key_id: pulumi.Output[str]
    """
    The identifier of the API key resource.
    """
    key_type: pulumi.Output[str]
    """
    The type of the API key resource. Currently, the valid key type is API_KEY.
    """
    name: pulumi.Output[str]
    """
    The name of a usage plan key.
    """
    usage_plan_id: pulumi.Output[str]
    """
    The Id of the usage plan resource representing to associate the key to.
    """
    value: pulumi.Output[str]
    """
    The value of a usage plan key.
    """
    def __init__(__self__, resource_name, opts=None, key_id=None, key_type=None, usage_plan_id=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an API Gateway Usage Plan Key.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.apigateway.RestApi("test")
        myusageplan = aws.apigateway.UsagePlan("myusageplan", api_stages=[{
            "api_id": test.id,
            "stage": aws_api_gateway_deployment["foo"]["stage_name"],
        }])
        mykey = aws.apigateway.ApiKey("mykey")
        main = aws.apigateway.UsagePlanKey("main",
            key_id=mykey.id,
            key_type="API_KEY",
            usage_plan_id=myusageplan.id)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] key_id: The identifier of the API key resource.
        :param pulumi.Input[str] key_type: The type of the API key resource. Currently, the valid key type is API_KEY.
        :param pulumi.Input[str] usage_plan_id: The Id of the usage plan resource representing to associate the key to.
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

            if key_id is None:
                raise TypeError("Missing required property 'key_id'")
            __props__['key_id'] = key_id
            if key_type is None:
                raise TypeError("Missing required property 'key_type'")
            __props__['key_type'] = key_type
            if usage_plan_id is None:
                raise TypeError("Missing required property 'usage_plan_id'")
            __props__['usage_plan_id'] = usage_plan_id
            __props__['name'] = None
            __props__['value'] = None
        super(UsagePlanKey, __self__).__init__(
            'aws:apigateway/usagePlanKey:UsagePlanKey',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, key_id=None, key_type=None, name=None, usage_plan_id=None, value=None):
        """
        Get an existing UsagePlanKey resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] key_id: The identifier of the API key resource.
        :param pulumi.Input[str] key_type: The type of the API key resource. Currently, the valid key type is API_KEY.
        :param pulumi.Input[str] name: The name of a usage plan key.
        :param pulumi.Input[str] usage_plan_id: The Id of the usage plan resource representing to associate the key to.
        :param pulumi.Input[str] value: The value of a usage plan key.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["key_id"] = key_id
        __props__["key_type"] = key_type
        __props__["name"] = name
        __props__["usage_plan_id"] = usage_plan_id
        __props__["value"] = value
        return UsagePlanKey(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

