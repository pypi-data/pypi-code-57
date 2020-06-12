# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class ActionRuleActionGroup(pulumi.CustomResource):
    action_group_id: pulumi.Output[str]
    """
    Specifies the resource id of monitor action group.
    """
    condition: pulumi.Output[dict]
    """
    A `condition` block as defined below.

      * `alertContext` (`dict`) - A `alert_context` block as defined below.
        * `operator` (`str`) - The operator for a given condition. Possible values are `Equals`, `NotEquals`, `Contains`, and `DoesNotContain`.
        * `values` (`list`) - A list of values to match for a given condition.

      * `alertRuleId` (`dict`) - A `alert_rule_id` block as defined below.
        * `operator` (`str`) - The operator for a given condition. Possible values are `Equals`, `NotEquals`, `Contains`, and `DoesNotContain`.
        * `values` (`list`) - A list of values to match for a given condition.

      * `description` (`dict`) - A `description` block as defined below.
        * `operator` (`str`) - The operator for a given condition. Possible values are `Equals`, `NotEquals`, `Contains`, and `DoesNotContain`.
        * `values` (`list`) - A list of values to match for a given condition.

      * `monitor` (`dict`) - A `monitor` block as defined below.
        * `operator` (`str`) - The operator for a given condition. Possible values are `Equals` and `NotEquals`.
        * `values` (`list`) - A list of values to match for a given condition. Possible values are `Fired` and `Resolved`.

      * `monitorService` (`dict`) - A `monitor_service` as block defined below.
        * `operator` (`str`) - The operator for a given condition. Possible values are `Equals` and `NotEquals`.
        * `values` (`list`) - A list of values to match for a given condition. Possible values are `ActivityLog Administrative`, `ActivityLog Autoscale`, `ActivityLog Policy`, `ActivityLog Recommendation`, `ActivityLog Security`, `Application Insights`, `Azure Backup`, `Data Box Edge`, `Data Box Gateway`, `Health Platform`, `Log Analytics`, `Platform`, and `Resource Health`.

      * `severity` (`dict`) - A `severity` block as defined below.
        * `operator` (`str`) - The operator for a given condition. Possible values are `Equals`and `NotEquals`.
        * `values` (`list`) - A list of values to match for a given condition. Possible values are `Sev0`, `Sev1`, `Sev2`, `Sev3`, and `Sev4`.

      * `targetResourceType` (`dict`) - A `target_resource_type` block as defined below.
        * `operator` (`str`) - The operator for a given condition. Possible values are `Equals` and `NotEquals`.
        * `values` (`list`) - A list of values to match for a given condition. The values should be valid resource types.
    """
    description: pulumi.Output[str]
    """
    Specifies a description for the Action Rule.
    """
    enabled: pulumi.Output[bool]
    """
    Is the Action Rule enabled? Defaults to `true`.
    """
    name: pulumi.Output[str]
    """
    Specifies the name of the Monitor Action Rule. Changing this forces a new resource to be created.
    """
    resource_group_name: pulumi.Output[str]
    """
    Specifies the name of the resource group in which the Monitor Action Rule should exist. Changing this forces a new resource to be created.
    """
    scope: pulumi.Output[dict]
    """
    A `scope` block as defined below.

      * `resourceIds` (`list`) - A list of resource IDs of the given scope type which will be the target of action rule.
      * `type` (`str`) - Specifies the type of target scope. Possible values are `ResourceGroup` and `Resource`.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    def __init__(__self__, resource_name, opts=None, action_group_id=None, condition=None, description=None, enabled=None, name=None, resource_group_name=None, scope=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages an Monitor Action Rule which type is action group.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_action_group = azure.monitoring.ActionGroup("exampleActionGroup",
            resource_group_name=example_resource_group.name,
            short_name="exampleactiongroup")
        example_action_rule_action_group = azure.monitoring.ActionRuleActionGroup("exampleActionRuleActionGroup",
            resource_group_name=example_resource_group.name,
            action_group_id=example_action_group.id,
            scope={
                "type": "ResourceGroup",
                "resourceIds": [example_resource_group.id],
            },
            tags={
                "foo": "bar",
            })
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] action_group_id: Specifies the resource id of monitor action group.
        :param pulumi.Input[dict] condition: A `condition` block as defined below.
        :param pulumi.Input[str] description: Specifies a description for the Action Rule.
        :param pulumi.Input[bool] enabled: Is the Action Rule enabled? Defaults to `true`.
        :param pulumi.Input[str] name: Specifies the name of the Monitor Action Rule. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: Specifies the name of the resource group in which the Monitor Action Rule should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] scope: A `scope` block as defined below.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.

        The **condition** object supports the following:

          * `alertContext` (`pulumi.Input[dict]`) - A `alert_context` block as defined below.
            * `operator` (`pulumi.Input[str]`) - The operator for a given condition. Possible values are `Equals`, `NotEquals`, `Contains`, and `DoesNotContain`.
            * `values` (`pulumi.Input[list]`) - A list of values to match for a given condition.

          * `alertRuleId` (`pulumi.Input[dict]`) - A `alert_rule_id` block as defined below.
            * `operator` (`pulumi.Input[str]`) - The operator for a given condition. Possible values are `Equals`, `NotEquals`, `Contains`, and `DoesNotContain`.
            * `values` (`pulumi.Input[list]`) - A list of values to match for a given condition.

          * `description` (`pulumi.Input[dict]`) - A `description` block as defined below.
            * `operator` (`pulumi.Input[str]`) - The operator for a given condition. Possible values are `Equals`, `NotEquals`, `Contains`, and `DoesNotContain`.
            * `values` (`pulumi.Input[list]`) - A list of values to match for a given condition.

          * `monitor` (`pulumi.Input[dict]`) - A `monitor` block as defined below.
            * `operator` (`pulumi.Input[str]`) - The operator for a given condition. Possible values are `Equals` and `NotEquals`.
            * `values` (`pulumi.Input[list]`) - A list of values to match for a given condition. Possible values are `Fired` and `Resolved`.

          * `monitorService` (`pulumi.Input[dict]`) - A `monitor_service` as block defined below.
            * `operator` (`pulumi.Input[str]`) - The operator for a given condition. Possible values are `Equals` and `NotEquals`.
            * `values` (`pulumi.Input[list]`) - A list of values to match for a given condition. Possible values are `ActivityLog Administrative`, `ActivityLog Autoscale`, `ActivityLog Policy`, `ActivityLog Recommendation`, `ActivityLog Security`, `Application Insights`, `Azure Backup`, `Data Box Edge`, `Data Box Gateway`, `Health Platform`, `Log Analytics`, `Platform`, and `Resource Health`.

          * `severity` (`pulumi.Input[dict]`) - A `severity` block as defined below.
            * `operator` (`pulumi.Input[str]`) - The operator for a given condition. Possible values are `Equals`and `NotEquals`.
            * `values` (`pulumi.Input[list]`) - A list of values to match for a given condition. Possible values are `Sev0`, `Sev1`, `Sev2`, `Sev3`, and `Sev4`.

          * `targetResourceType` (`pulumi.Input[dict]`) - A `target_resource_type` block as defined below.
            * `operator` (`pulumi.Input[str]`) - The operator for a given condition. Possible values are `Equals` and `NotEquals`.
            * `values` (`pulumi.Input[list]`) - A list of values to match for a given condition. The values should be valid resource types.

        The **scope** object supports the following:

          * `resourceIds` (`pulumi.Input[list]`) - A list of resource IDs of the given scope type which will be the target of action rule.
          * `type` (`pulumi.Input[str]`) - Specifies the type of target scope. Possible values are `ResourceGroup` and `Resource`.
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

            if action_group_id is None:
                raise TypeError("Missing required property 'action_group_id'")
            __props__['action_group_id'] = action_group_id
            __props__['condition'] = condition
            __props__['description'] = description
            __props__['enabled'] = enabled
            __props__['name'] = name
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['scope'] = scope
            __props__['tags'] = tags
        super(ActionRuleActionGroup, __self__).__init__(
            'azure:monitoring/actionRuleActionGroup:ActionRuleActionGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, action_group_id=None, condition=None, description=None, enabled=None, name=None, resource_group_name=None, scope=None, tags=None):
        """
        Get an existing ActionRuleActionGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] action_group_id: Specifies the resource id of monitor action group.
        :param pulumi.Input[dict] condition: A `condition` block as defined below.
        :param pulumi.Input[str] description: Specifies a description for the Action Rule.
        :param pulumi.Input[bool] enabled: Is the Action Rule enabled? Defaults to `true`.
        :param pulumi.Input[str] name: Specifies the name of the Monitor Action Rule. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: Specifies the name of the resource group in which the Monitor Action Rule should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] scope: A `scope` block as defined below.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.

        The **condition** object supports the following:

          * `alertContext` (`pulumi.Input[dict]`) - A `alert_context` block as defined below.
            * `operator` (`pulumi.Input[str]`) - The operator for a given condition. Possible values are `Equals`, `NotEquals`, `Contains`, and `DoesNotContain`.
            * `values` (`pulumi.Input[list]`) - A list of values to match for a given condition.

          * `alertRuleId` (`pulumi.Input[dict]`) - A `alert_rule_id` block as defined below.
            * `operator` (`pulumi.Input[str]`) - The operator for a given condition. Possible values are `Equals`, `NotEquals`, `Contains`, and `DoesNotContain`.
            * `values` (`pulumi.Input[list]`) - A list of values to match for a given condition.

          * `description` (`pulumi.Input[dict]`) - A `description` block as defined below.
            * `operator` (`pulumi.Input[str]`) - The operator for a given condition. Possible values are `Equals`, `NotEquals`, `Contains`, and `DoesNotContain`.
            * `values` (`pulumi.Input[list]`) - A list of values to match for a given condition.

          * `monitor` (`pulumi.Input[dict]`) - A `monitor` block as defined below.
            * `operator` (`pulumi.Input[str]`) - The operator for a given condition. Possible values are `Equals` and `NotEquals`.
            * `values` (`pulumi.Input[list]`) - A list of values to match for a given condition. Possible values are `Fired` and `Resolved`.

          * `monitorService` (`pulumi.Input[dict]`) - A `monitor_service` as block defined below.
            * `operator` (`pulumi.Input[str]`) - The operator for a given condition. Possible values are `Equals` and `NotEquals`.
            * `values` (`pulumi.Input[list]`) - A list of values to match for a given condition. Possible values are `ActivityLog Administrative`, `ActivityLog Autoscale`, `ActivityLog Policy`, `ActivityLog Recommendation`, `ActivityLog Security`, `Application Insights`, `Azure Backup`, `Data Box Edge`, `Data Box Gateway`, `Health Platform`, `Log Analytics`, `Platform`, and `Resource Health`.

          * `severity` (`pulumi.Input[dict]`) - A `severity` block as defined below.
            * `operator` (`pulumi.Input[str]`) - The operator for a given condition. Possible values are `Equals`and `NotEquals`.
            * `values` (`pulumi.Input[list]`) - A list of values to match for a given condition. Possible values are `Sev0`, `Sev1`, `Sev2`, `Sev3`, and `Sev4`.

          * `targetResourceType` (`pulumi.Input[dict]`) - A `target_resource_type` block as defined below.
            * `operator` (`pulumi.Input[str]`) - The operator for a given condition. Possible values are `Equals` and `NotEquals`.
            * `values` (`pulumi.Input[list]`) - A list of values to match for a given condition. The values should be valid resource types.

        The **scope** object supports the following:

          * `resourceIds` (`pulumi.Input[list]`) - A list of resource IDs of the given scope type which will be the target of action rule.
          * `type` (`pulumi.Input[str]`) - Specifies the type of target scope. Possible values are `ResourceGroup` and `Resource`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["action_group_id"] = action_group_id
        __props__["condition"] = condition
        __props__["description"] = description
        __props__["enabled"] = enabled
        __props__["name"] = name
        __props__["resource_group_name"] = resource_group_name
        __props__["scope"] = scope
        __props__["tags"] = tags
        return ActionRuleActionGroup(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
