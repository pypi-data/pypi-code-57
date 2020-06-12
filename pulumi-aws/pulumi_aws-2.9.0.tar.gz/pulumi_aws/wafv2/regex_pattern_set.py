# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class RegexPatternSet(pulumi.CustomResource):
    arn: pulumi.Output[str]
    """
    The Amazon Resource Name (ARN) that identifies the cluster.
    """
    description: pulumi.Output[str]
    """
    A friendly description of the regular expression pattern set.
    """
    lock_token: pulumi.Output[str]
    name: pulumi.Output[str]
    """
    A friendly name of the regular expression pattern set.
    """
    regular_expressions: pulumi.Output[list]
    """
    One or more blocks of regular expression patterns that you want AWS WAF to search for, such as `B[a@]dB[o0]t`. See Regular Expression below for details.

      * `regexString` (`str`) - The string representing the regular expression, see the AWS WAF [documentation](https://docs.aws.amazon.com/waf/latest/developerguide/waf-regex-pattern-set-creating.html) for more information.
    """
    scope: pulumi.Output[str]
    """
    Specifies whether this is for an AWS CloudFront distribution or for a regional application. Valid values are `CLOUDFRONT` or `REGIONAL`. To work with CloudFront, you must also specify the region `us-east-1` (N. Virginia) on the AWS provider.
    """
    tags: pulumi.Output[dict]
    """
    An array of key:value pairs to associate with the resource.
    """
    def __init__(__self__, resource_name, opts=None, description=None, name=None, regular_expressions=None, scope=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an AWS WAFv2 Regex Pattern Set Resource

        ## Example Usage



        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.wafv2.RegexPatternSet("example",
            description="Example regex pattern set",
            regular_expressions=[
                {
                    "regexString": "one",
                },
                {
                    "regexString": "two",
                },
            ],
            scope="REGIONAL",
            tags={
                "Tag1": "Value1",
                "Tag2": "Value2",
            })
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A friendly description of the regular expression pattern set.
        :param pulumi.Input[str] name: A friendly name of the regular expression pattern set.
        :param pulumi.Input[list] regular_expressions: One or more blocks of regular expression patterns that you want AWS WAF to search for, such as `B[a@]dB[o0]t`. See Regular Expression below for details.
        :param pulumi.Input[str] scope: Specifies whether this is for an AWS CloudFront distribution or for a regional application. Valid values are `CLOUDFRONT` or `REGIONAL`. To work with CloudFront, you must also specify the region `us-east-1` (N. Virginia) on the AWS provider.
        :param pulumi.Input[dict] tags: An array of key:value pairs to associate with the resource.

        The **regular_expressions** object supports the following:

          * `regexString` (`pulumi.Input[str]`) - The string representing the regular expression, see the AWS WAF [documentation](https://docs.aws.amazon.com/waf/latest/developerguide/waf-regex-pattern-set-creating.html) for more information.
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

            __props__['description'] = description
            __props__['name'] = name
            __props__['regular_expressions'] = regular_expressions
            if scope is None:
                raise TypeError("Missing required property 'scope'")
            __props__['scope'] = scope
            __props__['tags'] = tags
            __props__['arn'] = None
            __props__['lock_token'] = None
        super(RegexPatternSet, __self__).__init__(
            'aws:wafv2/regexPatternSet:RegexPatternSet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, arn=None, description=None, lock_token=None, name=None, regular_expressions=None, scope=None, tags=None):
        """
        Get an existing RegexPatternSet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) that identifies the cluster.
        :param pulumi.Input[str] description: A friendly description of the regular expression pattern set.
        :param pulumi.Input[str] name: A friendly name of the regular expression pattern set.
        :param pulumi.Input[list] regular_expressions: One or more blocks of regular expression patterns that you want AWS WAF to search for, such as `B[a@]dB[o0]t`. See Regular Expression below for details.
        :param pulumi.Input[str] scope: Specifies whether this is for an AWS CloudFront distribution or for a regional application. Valid values are `CLOUDFRONT` or `REGIONAL`. To work with CloudFront, you must also specify the region `us-east-1` (N. Virginia) on the AWS provider.
        :param pulumi.Input[dict] tags: An array of key:value pairs to associate with the resource.

        The **regular_expressions** object supports the following:

          * `regexString` (`pulumi.Input[str]`) - The string representing the regular expression, see the AWS WAF [documentation](https://docs.aws.amazon.com/waf/latest/developerguide/waf-regex-pattern-set-creating.html) for more information.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["description"] = description
        __props__["lock_token"] = lock_token
        __props__["name"] = name
        __props__["regular_expressions"] = regular_expressions
        __props__["scope"] = scope
        __props__["tags"] = tags
        return RegexPatternSet(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

