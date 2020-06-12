# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class Plan(pulumi.CustomResource):
    app_service_environment_id: pulumi.Output[str]
    """
    The ID of the App Service Environment where the App Service Plan should be located. Changing forces a new resource to be created.
    """
    is_xenon: pulumi.Output[bool]
    kind: pulumi.Output[str]
    """
    The kind of the App Service Plan to create. Possible values are `Windows` (also available as `App`), `Linux`, `elastic` (for Premium Consumption) and `FunctionApp` (for a Consumption Plan). Defaults to `Windows`. Changing this forces a new resource to be created.
    """
    location: pulumi.Output[str]
    """
    Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
    """
    maximum_elastic_worker_count: pulumi.Output[float]
    """
    The maximum number of total workers allowed for this ElasticScaleEnabled App Service Plan.
    """
    maximum_number_of_workers: pulumi.Output[float]
    """
    The maximum number of workers supported with the App Service Plan's sku.
    """
    name: pulumi.Output[str]
    """
    Specifies the name of the App Service Plan component. Changing this forces a new resource to be created.
    """
    per_site_scaling: pulumi.Output[bool]
    """
    Can Apps assigned to this App Service Plan be scaled independently? If set to `false` apps assigned to this plan will scale to all instances of the plan.  Defaults to `false`.
    """
    reserved: pulumi.Output[bool]
    """
    Is this App Service Plan `Reserved`. Defaults to `false`.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group in which to create the App Service Plan component.
    """
    sku: pulumi.Output[dict]
    """
    A `sku` block as documented below.

      * `capacity` (`float`) - Specifies the number of workers associated with this App Service Plan.
      * `size` (`str`) - Specifies the plan's instance size.
      * `tier` (`str`) - Specifies the plan's pricing tier.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    def __init__(__self__, resource_name, opts=None, app_service_environment_id=None, is_xenon=None, kind=None, location=None, maximum_elastic_worker_count=None, name=None, per_site_scaling=None, reserved=None, resource_group_name=None, sku=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages an App Service Plan component.

        ## Example Usage

        ### Dedicated)

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_plan = azure.appservice.Plan("examplePlan",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku={
                "tier": "Standard",
                "size": "S1",
            })
        ```

        ### Shared / Consumption Plan)

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_plan = azure.appservice.Plan("examplePlan",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            kind="FunctionApp",
            sku={
                "tier": "Dynamic",
                "size": "Y1",
            })
        ```

        ### Linux)

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_plan = azure.appservice.Plan("examplePlan",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            kind="Linux",
            reserved=True,
            sku={
                "tier": "Standard",
                "size": "S1",
            })
        ```

        ### Windows Container)

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_plan = azure.appservice.Plan("examplePlan",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            kind="xenon",
            is_xenon=True,
            sku={
                "tier": "PremiumContainer",
                "size": "PC2",
            })
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] app_service_environment_id: The ID of the App Service Environment where the App Service Plan should be located. Changing forces a new resource to be created.
        :param pulumi.Input[dict] kind: The kind of the App Service Plan to create. Possible values are `Windows` (also available as `App`), `Linux`, `elastic` (for Premium Consumption) and `FunctionApp` (for a Consumption Plan). Defaults to `Windows`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[float] maximum_elastic_worker_count: The maximum number of total workers allowed for this ElasticScaleEnabled App Service Plan.
        :param pulumi.Input[str] name: Specifies the name of the App Service Plan component. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] per_site_scaling: Can Apps assigned to this App Service Plan be scaled independently? If set to `false` apps assigned to this plan will scale to all instances of the plan.  Defaults to `false`.
        :param pulumi.Input[bool] reserved: Is this App Service Plan `Reserved`. Defaults to `false`.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the App Service Plan component.
        :param pulumi.Input[dict] sku: A `sku` block as documented below.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.

        The **sku** object supports the following:

          * `capacity` (`pulumi.Input[float]`) - Specifies the number of workers associated with this App Service Plan.
          * `size` (`pulumi.Input[str]`) - Specifies the plan's instance size.
          * `tier` (`pulumi.Input[str]`) - Specifies the plan's pricing tier.
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

            __props__['app_service_environment_id'] = app_service_environment_id
            __props__['is_xenon'] = is_xenon
            __props__['kind'] = kind
            __props__['location'] = location
            __props__['maximum_elastic_worker_count'] = maximum_elastic_worker_count
            __props__['name'] = name
            __props__['per_site_scaling'] = per_site_scaling
            __props__['reserved'] = reserved
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if sku is None:
                raise TypeError("Missing required property 'sku'")
            __props__['sku'] = sku
            __props__['tags'] = tags
            __props__['maximum_number_of_workers'] = None
        super(Plan, __self__).__init__(
            'azure:appservice/plan:Plan',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, app_service_environment_id=None, is_xenon=None, kind=None, location=None, maximum_elastic_worker_count=None, maximum_number_of_workers=None, name=None, per_site_scaling=None, reserved=None, resource_group_name=None, sku=None, tags=None):
        """
        Get an existing Plan resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] app_service_environment_id: The ID of the App Service Environment where the App Service Plan should be located. Changing forces a new resource to be created.
        :param pulumi.Input[dict] kind: The kind of the App Service Plan to create. Possible values are `Windows` (also available as `App`), `Linux`, `elastic` (for Premium Consumption) and `FunctionApp` (for a Consumption Plan). Defaults to `Windows`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[float] maximum_elastic_worker_count: The maximum number of total workers allowed for this ElasticScaleEnabled App Service Plan.
        :param pulumi.Input[float] maximum_number_of_workers: The maximum number of workers supported with the App Service Plan's sku.
        :param pulumi.Input[str] name: Specifies the name of the App Service Plan component. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] per_site_scaling: Can Apps assigned to this App Service Plan be scaled independently? If set to `false` apps assigned to this plan will scale to all instances of the plan.  Defaults to `false`.
        :param pulumi.Input[bool] reserved: Is this App Service Plan `Reserved`. Defaults to `false`.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the App Service Plan component.
        :param pulumi.Input[dict] sku: A `sku` block as documented below.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.

        The **sku** object supports the following:

          * `capacity` (`pulumi.Input[float]`) - Specifies the number of workers associated with this App Service Plan.
          * `size` (`pulumi.Input[str]`) - Specifies the plan's instance size.
          * `tier` (`pulumi.Input[str]`) - Specifies the plan's pricing tier.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["app_service_environment_id"] = app_service_environment_id
        __props__["is_xenon"] = is_xenon
        __props__["kind"] = kind
        __props__["location"] = location
        __props__["maximum_elastic_worker_count"] = maximum_elastic_worker_count
        __props__["maximum_number_of_workers"] = maximum_number_of_workers
        __props__["name"] = name
        __props__["per_site_scaling"] = per_site_scaling
        __props__["reserved"] = reserved
        __props__["resource_group_name"] = resource_group_name
        __props__["sku"] = sku
        __props__["tags"] = tags
        return Plan(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
