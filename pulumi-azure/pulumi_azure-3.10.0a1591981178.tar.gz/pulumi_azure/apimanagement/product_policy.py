# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class ProductPolicy(pulumi.CustomResource):
    api_management_name: pulumi.Output[str]
    """
    The name of the API Management Service. Changing this forces a new resource to be created.
    """
    product_id: pulumi.Output[str]
    """
    The ID of the API Management Product within the API Management Service. Changing this forces a new resource to be created.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the Resource Group in which the API Management Service exists. Changing this forces a new resource to be created.
    """
    xml_content: pulumi.Output[str]
    """
    The XML Content for this Policy.
    """
    xml_link: pulumi.Output[str]
    """
    A link to a Policy XML Document, which must be publicly available.
    """
    def __init__(__self__, resource_name, opts=None, api_management_name=None, product_id=None, resource_group_name=None, xml_content=None, xml_link=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages an API Management Product Policy


        ## Example Usage



        ```python
        import pulumi
        import pulumi_azure as azure

        example_product = azure.apimanagement.get_product(product_id="my-product",
            api_management_name="example-apim",
            resource_group_name="search-service")
        example_product_policy = azure.apimanagement.ProductPolicy("exampleProductPolicy",
            product_id=example_product.product_id,
            api_management_name=example_product.api_management_name,
            resource_group_name=example_product.resource_group_name,
            xml_content=\"\"\"<policies>
          <inbound>
            <find-and-replace from="xyz" to="abc" />
          </inbound>
        </policies>
        \"\"\")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_management_name: The name of the API Management Service. Changing this forces a new resource to be created.
        :param pulumi.Input[str] product_id: The ID of the API Management Product within the API Management Service. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the API Management Service exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] xml_content: The XML Content for this Policy.
        :param pulumi.Input[str] xml_link: A link to a Policy XML Document, which must be publicly available.
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

            if api_management_name is None:
                raise TypeError("Missing required property 'api_management_name'")
            __props__['api_management_name'] = api_management_name
            if product_id is None:
                raise TypeError("Missing required property 'product_id'")
            __props__['product_id'] = product_id
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['xml_content'] = xml_content
            __props__['xml_link'] = xml_link
        super(ProductPolicy, __self__).__init__(
            'azure:apimanagement/productPolicy:ProductPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, api_management_name=None, product_id=None, resource_group_name=None, xml_content=None, xml_link=None):
        """
        Get an existing ProductPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_management_name: The name of the API Management Service. Changing this forces a new resource to be created.
        :param pulumi.Input[str] product_id: The ID of the API Management Product within the API Management Service. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the API Management Service exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] xml_content: The XML Content for this Policy.
        :param pulumi.Input[str] xml_link: A link to a Policy XML Document, which must be publicly available.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["api_management_name"] = api_management_name
        __props__["product_id"] = product_id
        __props__["resource_group_name"] = resource_group_name
        __props__["xml_content"] = xml_content
        __props__["xml_link"] = xml_link
        return ProductPolicy(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
