# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class FirewallApplicationRuleCollection(pulumi.CustomResource):
    action: pulumi.Output[str]
    """
    Specifies the action the rule will apply to matching traffic. Possible values are `Allow` and `Deny`.
    """
    azure_firewall_name: pulumi.Output[str]
    """
    Specifies the name of the Firewall in which the Application Rule Collection should be created. Changing this forces a new resource to be created.
    """
    name: pulumi.Output[str]
    """
    Specifies the name of the Application Rule Collection which must be unique within the Firewall. Changing this forces a new resource to be created.
    """
    priority: pulumi.Output[float]
    """
    Specifies the priority of the rule collection. Possible values are between `100` - `65000`.
    """
    resource_group_name: pulumi.Output[str]
    """
    Specifies the name of the Resource Group in which the Firewall exists. Changing this forces a new resource to be created.
    """
    rules: pulumi.Output[list]
    """
    One or more `rule` blocks as defined below.

      * `description` (`str`) - Specifies a description for the rule.
      * `fqdnTags` (`list`) - A list of FQDN tags. Possible values are `AppServiceEnvironment`, `AzureBackup`, `MicrosoftActiveProtectionService`, `WindowsDiagnostics` and `WindowsUpdate`
      * `name` (`str`) - Specifies the name of the rule.
      * `protocols` (`list`) - One or more `protocol` blocks as defined below.
        * `port` (`float`) - Specify a port for the connection.
        * `type` (`str`) - Specifies the type of connection. Possible values are `Http`, `Https` and `Mssql`.

      * `sourceAddresses` (`list`) - A list of source IP addresses and/or IP ranges.
      * `targetFqdns` (`list`) - A list of FQDNs.
    """
    def __init__(__self__, resource_name, opts=None, action=None, azure_firewall_name=None, name=None, priority=None, resource_group_name=None, rules=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages an Application Rule Collection within an Azure Firewall.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="North Europe")
        example_virtual_network = azure.network.VirtualNetwork("exampleVirtualNetwork",
            address_spaces=["10.0.0.0/16"],
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        example_subnet = azure.network.Subnet("exampleSubnet",
            resource_group_name=example_resource_group.name,
            virtual_network_name=example_virtual_network.name,
            address_prefix="10.0.1.0/24")
        example_public_ip = azure.network.PublicIp("examplePublicIp",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            allocation_method="Static",
            sku="Standard")
        example_firewall = azure.network.Firewall("exampleFirewall",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            ip_configuration=[{
                "name": "configuration",
                "subnet_id": example_subnet.id,
                "public_ip_address_id": example_public_ip.id,
            }])
        example_firewall_application_rule_collection = azure.network.FirewallApplicationRuleCollection("exampleFirewallApplicationRuleCollection",
            azure_firewall_name=example_firewall.name,
            resource_group_name=example_resource_group.name,
            priority=100,
            action="Allow",
            rule=[{
                "name": "testrule",
                "sourceAddresses": ["10.0.0.0/16"],
                "targetFqdns": ["*.google.com"],
                "protocol": [{
                    "port": "443",
                    "type": "Https",
                }],
            }])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] action: Specifies the action the rule will apply to matching traffic. Possible values are `Allow` and `Deny`.
        :param pulumi.Input[str] azure_firewall_name: Specifies the name of the Firewall in which the Application Rule Collection should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Application Rule Collection which must be unique within the Firewall. Changing this forces a new resource to be created.
        :param pulumi.Input[float] priority: Specifies the priority of the rule collection. Possible values are between `100` - `65000`.
        :param pulumi.Input[str] resource_group_name: Specifies the name of the Resource Group in which the Firewall exists. Changing this forces a new resource to be created.
        :param pulumi.Input[list] rules: One or more `rule` blocks as defined below.

        The **rules** object supports the following:

          * `description` (`pulumi.Input[str]`) - Specifies a description for the rule.
          * `fqdnTags` (`pulumi.Input[list]`) - A list of FQDN tags. Possible values are `AppServiceEnvironment`, `AzureBackup`, `MicrosoftActiveProtectionService`, `WindowsDiagnostics` and `WindowsUpdate`
          * `name` (`pulumi.Input[str]`) - Specifies the name of the rule.
          * `protocols` (`pulumi.Input[list]`) - One or more `protocol` blocks as defined below.
            * `port` (`pulumi.Input[float]`) - Specify a port for the connection.
            * `type` (`pulumi.Input[str]`) - Specifies the type of connection. Possible values are `Http`, `Https` and `Mssql`.

          * `sourceAddresses` (`pulumi.Input[list]`) - A list of source IP addresses and/or IP ranges.
          * `targetFqdns` (`pulumi.Input[list]`) - A list of FQDNs.
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

            if action is None:
                raise TypeError("Missing required property 'action'")
            __props__['action'] = action
            if azure_firewall_name is None:
                raise TypeError("Missing required property 'azure_firewall_name'")
            __props__['azure_firewall_name'] = azure_firewall_name
            __props__['name'] = name
            if priority is None:
                raise TypeError("Missing required property 'priority'")
            __props__['priority'] = priority
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if rules is None:
                raise TypeError("Missing required property 'rules'")
            __props__['rules'] = rules
        super(FirewallApplicationRuleCollection, __self__).__init__(
            'azure:network/firewallApplicationRuleCollection:FirewallApplicationRuleCollection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, action=None, azure_firewall_name=None, name=None, priority=None, resource_group_name=None, rules=None):
        """
        Get an existing FirewallApplicationRuleCollection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] action: Specifies the action the rule will apply to matching traffic. Possible values are `Allow` and `Deny`.
        :param pulumi.Input[str] azure_firewall_name: Specifies the name of the Firewall in which the Application Rule Collection should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Application Rule Collection which must be unique within the Firewall. Changing this forces a new resource to be created.
        :param pulumi.Input[float] priority: Specifies the priority of the rule collection. Possible values are between `100` - `65000`.
        :param pulumi.Input[str] resource_group_name: Specifies the name of the Resource Group in which the Firewall exists. Changing this forces a new resource to be created.
        :param pulumi.Input[list] rules: One or more `rule` blocks as defined below.

        The **rules** object supports the following:

          * `description` (`pulumi.Input[str]`) - Specifies a description for the rule.
          * `fqdnTags` (`pulumi.Input[list]`) - A list of FQDN tags. Possible values are `AppServiceEnvironment`, `AzureBackup`, `MicrosoftActiveProtectionService`, `WindowsDiagnostics` and `WindowsUpdate`
          * `name` (`pulumi.Input[str]`) - Specifies the name of the rule.
          * `protocols` (`pulumi.Input[list]`) - One or more `protocol` blocks as defined below.
            * `port` (`pulumi.Input[float]`) - Specify a port for the connection.
            * `type` (`pulumi.Input[str]`) - Specifies the type of connection. Possible values are `Http`, `Https` and `Mssql`.

          * `sourceAddresses` (`pulumi.Input[list]`) - A list of source IP addresses and/or IP ranges.
          * `targetFqdns` (`pulumi.Input[list]`) - A list of FQDNs.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["action"] = action
        __props__["azure_firewall_name"] = azure_firewall_name
        __props__["name"] = name
        __props__["priority"] = priority
        __props__["resource_group_name"] = resource_group_name
        __props__["rules"] = rules
        return FirewallApplicationRuleCollection(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
