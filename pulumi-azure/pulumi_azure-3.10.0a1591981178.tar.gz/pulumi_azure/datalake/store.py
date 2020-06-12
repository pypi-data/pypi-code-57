# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class Store(pulumi.CustomResource):
    encryption_state: pulumi.Output[str]
    """
    Is Encryption enabled on this Data Lake Store Account? Possible values are `Enabled` or `Disabled`. Defaults to `Enabled`.
    """
    encryption_type: pulumi.Output[str]
    """
    The Encryption Type used for this Data Lake Store Account. Currently can be set to `ServiceManaged` when `encryption_state` is `Enabled` - and must be a blank string when it's Disabled.
    """
    endpoint: pulumi.Output[str]
    """
    The Endpoint for the Data Lake Store.
    """
    firewall_allow_azure_ips: pulumi.Output[str]
    """
    are Azure Service IP's allowed through the firewall? Possible values are `Enabled` and `Disabled`. Defaults to `Enabled.`
    """
    firewall_state: pulumi.Output[str]
    """
    the state of the Firewall. Possible values are `Enabled` and `Disabled`. Defaults to `Enabled.`
    """
    location: pulumi.Output[str]
    """
    Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
    """
    name: pulumi.Output[str]
    """
    Specifies the name of the Data Lake Store. Changing this forces a new resource to be created. Has to be between 3 to 24 characters.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group in which to create the Data Lake Store.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    tier: pulumi.Output[str]
    """
    The monthly commitment tier for Data Lake Store. Accepted values are `Consumption`, `Commitment_1TB`, `Commitment_10TB`, `Commitment_100TB`, `Commitment_500TB`, `Commitment_1PB` or `Commitment_5PB`.
    """
    def __init__(__self__, resource_name, opts=None, encryption_state=None, encryption_type=None, firewall_allow_azure_ips=None, firewall_state=None, location=None, name=None, resource_group_name=None, tags=None, tier=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages an Azure Data Lake Store.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="northeurope")
        example_store = azure.datalake.Store("exampleStore",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            encryption_state="Enabled",
            encryption_type="ServiceManaged")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] encryption_state: Is Encryption enabled on this Data Lake Store Account? Possible values are `Enabled` or `Disabled`. Defaults to `Enabled`.
        :param pulumi.Input[str] encryption_type: The Encryption Type used for this Data Lake Store Account. Currently can be set to `ServiceManaged` when `encryption_state` is `Enabled` - and must be a blank string when it's Disabled.
        :param pulumi.Input[str] firewall_allow_azure_ips: are Azure Service IP's allowed through the firewall? Possible values are `Enabled` and `Disabled`. Defaults to `Enabled.`
        :param pulumi.Input[str] firewall_state: the state of the Firewall. Possible values are `Enabled` and `Disabled`. Defaults to `Enabled.`
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Data Lake Store. Changing this forces a new resource to be created. Has to be between 3 to 24 characters.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Data Lake Store.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] tier: The monthly commitment tier for Data Lake Store. Accepted values are `Consumption`, `Commitment_1TB`, `Commitment_10TB`, `Commitment_100TB`, `Commitment_500TB`, `Commitment_1PB` or `Commitment_5PB`.
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

            __props__['encryption_state'] = encryption_state
            __props__['encryption_type'] = encryption_type
            __props__['firewall_allow_azure_ips'] = firewall_allow_azure_ips
            __props__['firewall_state'] = firewall_state
            __props__['location'] = location
            __props__['name'] = name
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['tags'] = tags
            __props__['tier'] = tier
            __props__['endpoint'] = None
        super(Store, __self__).__init__(
            'azure:datalake/store:Store',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, encryption_state=None, encryption_type=None, endpoint=None, firewall_allow_azure_ips=None, firewall_state=None, location=None, name=None, resource_group_name=None, tags=None, tier=None):
        """
        Get an existing Store resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] encryption_state: Is Encryption enabled on this Data Lake Store Account? Possible values are `Enabled` or `Disabled`. Defaults to `Enabled`.
        :param pulumi.Input[str] encryption_type: The Encryption Type used for this Data Lake Store Account. Currently can be set to `ServiceManaged` when `encryption_state` is `Enabled` - and must be a blank string when it's Disabled.
        :param pulumi.Input[str] endpoint: The Endpoint for the Data Lake Store.
        :param pulumi.Input[str] firewall_allow_azure_ips: are Azure Service IP's allowed through the firewall? Possible values are `Enabled` and `Disabled`. Defaults to `Enabled.`
        :param pulumi.Input[str] firewall_state: the state of the Firewall. Possible values are `Enabled` and `Disabled`. Defaults to `Enabled.`
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Data Lake Store. Changing this forces a new resource to be created. Has to be between 3 to 24 characters.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Data Lake Store.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] tier: The monthly commitment tier for Data Lake Store. Accepted values are `Consumption`, `Commitment_1TB`, `Commitment_10TB`, `Commitment_100TB`, `Commitment_500TB`, `Commitment_1PB` or `Commitment_5PB`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["encryption_state"] = encryption_state
        __props__["encryption_type"] = encryption_type
        __props__["endpoint"] = endpoint
        __props__["firewall_allow_azure_ips"] = firewall_allow_azure_ips
        __props__["firewall_state"] = firewall_state
        __props__["location"] = location
        __props__["name"] = name
        __props__["resource_group_name"] = resource_group_name
        __props__["tags"] = tags
        __props__["tier"] = tier
        return Store(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
