# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class EndpointConfiguration(pulumi.CustomResource):
    arn: pulumi.Output[str]
    """
    The Amazon Resource Name (ARN) assigned by AWS to this endpoint configuration.
    """
    kms_key_arn: pulumi.Output[str]
    """
    Amazon Resource Name (ARN) of a AWS Key Management Service key that Amazon SageMaker uses to encrypt data on the storage volume attached to the ML compute instance that hosts the endpoint.
    """
    name: pulumi.Output[str]
    """
    The name of the endpoint configuration. If omitted, this provider will assign a random, unique name.
    """
    production_variants: pulumi.Output[list]
    """
    Fields are documented below.

      * `acceleratorType` (`str`) - The size of the Elastic Inference (EI) instance to use for the production variant.
      * `initialInstanceCount` (`float`) - Initial number of instances used for auto-scaling.
      * `initialVariantWeight` (`float`) - Determines initial traffic distribution among all of the models that you specify in the endpoint configuration. If unspecified, it defaults to 1.0.
      * `instance_type` (`str`) - The type of instance to start.
      * `modelName` (`str`) - The name of the model to use.
      * `variantName` (`str`) - The name of the variant. If omitted, this provider will assign a random, unique name.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    def __init__(__self__, resource_name, opts=None, kms_key_arn=None, name=None, production_variants=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a SageMaker endpoint configuration resource.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_aws as aws

        ec = aws.sagemaker.EndpointConfiguration("ec",
            production_variants=[{
                "initialInstanceCount": 1,
                "instance_type": "ml.t2.medium",
                "modelName": aws_sagemaker_model["m"]["name"],
                "variantName": "variant-1",
            }],
            tags={
                "Name": "foo",
            })
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] kms_key_arn: Amazon Resource Name (ARN) of a AWS Key Management Service key that Amazon SageMaker uses to encrypt data on the storage volume attached to the ML compute instance that hosts the endpoint.
        :param pulumi.Input[str] name: The name of the endpoint configuration. If omitted, this provider will assign a random, unique name.
        :param pulumi.Input[list] production_variants: Fields are documented below.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.

        The **production_variants** object supports the following:

          * `acceleratorType` (`pulumi.Input[str]`) - The size of the Elastic Inference (EI) instance to use for the production variant.
          * `initialInstanceCount` (`pulumi.Input[float]`) - Initial number of instances used for auto-scaling.
          * `initialVariantWeight` (`pulumi.Input[float]`) - Determines initial traffic distribution among all of the models that you specify in the endpoint configuration. If unspecified, it defaults to 1.0.
          * `instance_type` (`pulumi.Input[str]`) - The type of instance to start.
          * `modelName` (`pulumi.Input[str]`) - The name of the model to use.
          * `variantName` (`pulumi.Input[str]`) - The name of the variant. If omitted, this provider will assign a random, unique name.
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

            __props__['kms_key_arn'] = kms_key_arn
            __props__['name'] = name
            if production_variants is None:
                raise TypeError("Missing required property 'production_variants'")
            __props__['production_variants'] = production_variants
            __props__['tags'] = tags
            __props__['arn'] = None
        super(EndpointConfiguration, __self__).__init__(
            'aws:sagemaker/endpointConfiguration:EndpointConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, arn=None, kms_key_arn=None, name=None, production_variants=None, tags=None):
        """
        Get an existing EndpointConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) assigned by AWS to this endpoint configuration.
        :param pulumi.Input[str] kms_key_arn: Amazon Resource Name (ARN) of a AWS Key Management Service key that Amazon SageMaker uses to encrypt data on the storage volume attached to the ML compute instance that hosts the endpoint.
        :param pulumi.Input[str] name: The name of the endpoint configuration. If omitted, this provider will assign a random, unique name.
        :param pulumi.Input[list] production_variants: Fields are documented below.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.

        The **production_variants** object supports the following:

          * `acceleratorType` (`pulumi.Input[str]`) - The size of the Elastic Inference (EI) instance to use for the production variant.
          * `initialInstanceCount` (`pulumi.Input[float]`) - Initial number of instances used for auto-scaling.
          * `initialVariantWeight` (`pulumi.Input[float]`) - Determines initial traffic distribution among all of the models that you specify in the endpoint configuration. If unspecified, it defaults to 1.0.
          * `instance_type` (`pulumi.Input[str]`) - The type of instance to start.
          * `modelName` (`pulumi.Input[str]`) - The name of the model to use.
          * `variantName` (`pulumi.Input[str]`) - The name of the variant. If omitted, this provider will assign a random, unique name.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["kms_key_arn"] = kms_key_arn
        __props__["name"] = name
        __props__["production_variants"] = production_variants
        __props__["tags"] = tags
        return EndpointConfiguration(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

