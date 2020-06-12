# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class GremlinGraph(pulumi.CustomResource):
    account_name: pulumi.Output[str]
    """
    The name of the CosmosDB Account to create the Gremlin Graph within. Changing this forces a new resource to be created.
    """
    conflict_resolution_policies: pulumi.Output[list]
    """
    The conflict resolution policy for the graph. One or more `conflict_resolution_policy` blocks as defined below. Changing this forces a new resource to be created.

      * `conflictResolutionPath` (`str`) - The conflict resolution path in the case of LastWriterWins mode.
      * `conflictResolutionProcedure` (`str`) - The procedure to resolve conflicts in the case of custom mode.
      * `mode` (`str`) - Indicates the conflict resolution mode. Possible values include: `LastWriterWins`, `Custom`.
    """
    database_name: pulumi.Output[str]
    """
    The name of the Cosmos DB Graph Database in which the Cosmos DB Gremlin Graph is created. Changing this forces a new resource to be created.
    """
    index_policies: pulumi.Output[list]
    """
    The configuration of the indexing policy. One or more `index_policy` blocks as defined below. Changing this forces a new resource to be created.

      * `automatic` (`bool`) - Indicates if the indexing policy is automatic. Defaults to `true`.
      * `excludedPaths` (`list`) - List of paths to exclude from indexing. Required if `indexing_mode` is `Consistent` or `Lazy`.
      * `includedPaths` (`list`) - List of paths to include in the indexing. Required if `indexing_mode` is `Consistent` or `Lazy`.
      * `indexingMode` (`str`) - Indicates the indexing mode. Possible values include: `Consistent`, `Lazy`, `None`.
    """
    name: pulumi.Output[str]
    """
    Specifies the name of the Cosmos DB Gremlin Graph. Changing this forces a new resource to be created.
    """
    partition_key_path: pulumi.Output[str]
    """
    Define a partition key. Changing this forces a new resource to be created.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group in which the Cosmos DB Gremlin Graph is created. Changing this forces a new resource to be created.
    """
    throughput: pulumi.Output[float]
    """
    The throughput of the Gremlin database (RU/s). Must be set in increments of `100`. The minimum value is `400`. This must be set upon database creation otherwise it cannot be updated without a manual resource destroy-apply.
    """
    unique_keys: pulumi.Output[list]
    """
    One or more `unique_key` blocks as defined below. Changing this forces a new resource to be created.

      * `paths` (`list`) - A list of paths to use for this unique key.
    """
    def __init__(__self__, resource_name, opts=None, account_name=None, conflict_resolution_policies=None, database_name=None, index_policies=None, name=None, partition_key_path=None, resource_group_name=None, throughput=None, unique_keys=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages a Gremlin Graph within a Cosmos DB Account.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_azure as azure

        example_account = azure.cosmosdb.get_account(name="tfex-cosmosdb-account",
            resource_group_name="tfex-cosmosdb-account-rg")
        example_gremlin_database = azure.cosmosdb.GremlinDatabase("exampleGremlinDatabase",
            resource_group_name=example_account.resource_group_name,
            account_name=example_account.name)
        example_gremlin_graph = azure.cosmosdb.GremlinGraph("exampleGremlinGraph",
            resource_group_name=azurerm_cosmosdb_account["example"]["resource_group_name"],
            account_name=azurerm_cosmosdb_account["example"]["name"],
            database_name=example_gremlin_database.name,
            partition_key_path="/Example",
            throughput=400,
            index_policy=[{
                "automatic": True,
                "indexingMode": "Consistent",
                "includedPaths": ["/*"],
                "excludedPaths": ["/\"_etag\"/?"],
            }],
            conflict_resolution_policy=[{
                "mode": "LastWriterWins",
                "conflictResolutionPath": "/_ts",
            }],
            unique_key=[{
                "paths": [
                    "/definition/id1",
                    "/definition/id2",
                ],
            }])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the CosmosDB Account to create the Gremlin Graph within. Changing this forces a new resource to be created.
        :param pulumi.Input[list] conflict_resolution_policies: The conflict resolution policy for the graph. One or more `conflict_resolution_policy` blocks as defined below. Changing this forces a new resource to be created.
        :param pulumi.Input[str] database_name: The name of the Cosmos DB Graph Database in which the Cosmos DB Gremlin Graph is created. Changing this forces a new resource to be created.
        :param pulumi.Input[list] index_policies: The configuration of the indexing policy. One or more `index_policy` blocks as defined below. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Cosmos DB Gremlin Graph. Changing this forces a new resource to be created.
        :param pulumi.Input[str] partition_key_path: Define a partition key. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which the Cosmos DB Gremlin Graph is created. Changing this forces a new resource to be created.
        :param pulumi.Input[float] throughput: The throughput of the Gremlin database (RU/s). Must be set in increments of `100`. The minimum value is `400`. This must be set upon database creation otherwise it cannot be updated without a manual resource destroy-apply.
        :param pulumi.Input[list] unique_keys: One or more `unique_key` blocks as defined below. Changing this forces a new resource to be created.

        The **conflict_resolution_policies** object supports the following:

          * `conflictResolutionPath` (`pulumi.Input[str]`) - The conflict resolution path in the case of LastWriterWins mode.
          * `conflictResolutionProcedure` (`pulumi.Input[str]`) - The procedure to resolve conflicts in the case of custom mode.
          * `mode` (`pulumi.Input[str]`) - Indicates the conflict resolution mode. Possible values include: `LastWriterWins`, `Custom`.

        The **index_policies** object supports the following:

          * `automatic` (`pulumi.Input[bool]`) - Indicates if the indexing policy is automatic. Defaults to `true`.
          * `excludedPaths` (`pulumi.Input[list]`) - List of paths to exclude from indexing. Required if `indexing_mode` is `Consistent` or `Lazy`.
          * `includedPaths` (`pulumi.Input[list]`) - List of paths to include in the indexing. Required if `indexing_mode` is `Consistent` or `Lazy`.
          * `indexingMode` (`pulumi.Input[str]`) - Indicates the indexing mode. Possible values include: `Consistent`, `Lazy`, `None`.

        The **unique_keys** object supports the following:

          * `paths` (`pulumi.Input[list]`) - A list of paths to use for this unique key.
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

            if account_name is None:
                raise TypeError("Missing required property 'account_name'")
            __props__['account_name'] = account_name
            if conflict_resolution_policies is None:
                raise TypeError("Missing required property 'conflict_resolution_policies'")
            __props__['conflict_resolution_policies'] = conflict_resolution_policies
            if database_name is None:
                raise TypeError("Missing required property 'database_name'")
            __props__['database_name'] = database_name
            if index_policies is None:
                raise TypeError("Missing required property 'index_policies'")
            __props__['index_policies'] = index_policies
            __props__['name'] = name
            __props__['partition_key_path'] = partition_key_path
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['throughput'] = throughput
            __props__['unique_keys'] = unique_keys
        super(GremlinGraph, __self__).__init__(
            'azure:cosmosdb/gremlinGraph:GremlinGraph',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, account_name=None, conflict_resolution_policies=None, database_name=None, index_policies=None, name=None, partition_key_path=None, resource_group_name=None, throughput=None, unique_keys=None):
        """
        Get an existing GremlinGraph resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the CosmosDB Account to create the Gremlin Graph within. Changing this forces a new resource to be created.
        :param pulumi.Input[list] conflict_resolution_policies: The conflict resolution policy for the graph. One or more `conflict_resolution_policy` blocks as defined below. Changing this forces a new resource to be created.
        :param pulumi.Input[str] database_name: The name of the Cosmos DB Graph Database in which the Cosmos DB Gremlin Graph is created. Changing this forces a new resource to be created.
        :param pulumi.Input[list] index_policies: The configuration of the indexing policy. One or more `index_policy` blocks as defined below. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Cosmos DB Gremlin Graph. Changing this forces a new resource to be created.
        :param pulumi.Input[str] partition_key_path: Define a partition key. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which the Cosmos DB Gremlin Graph is created. Changing this forces a new resource to be created.
        :param pulumi.Input[float] throughput: The throughput of the Gremlin database (RU/s). Must be set in increments of `100`. The minimum value is `400`. This must be set upon database creation otherwise it cannot be updated without a manual resource destroy-apply.
        :param pulumi.Input[list] unique_keys: One or more `unique_key` blocks as defined below. Changing this forces a new resource to be created.

        The **conflict_resolution_policies** object supports the following:

          * `conflictResolutionPath` (`pulumi.Input[str]`) - The conflict resolution path in the case of LastWriterWins mode.
          * `conflictResolutionProcedure` (`pulumi.Input[str]`) - The procedure to resolve conflicts in the case of custom mode.
          * `mode` (`pulumi.Input[str]`) - Indicates the conflict resolution mode. Possible values include: `LastWriterWins`, `Custom`.

        The **index_policies** object supports the following:

          * `automatic` (`pulumi.Input[bool]`) - Indicates if the indexing policy is automatic. Defaults to `true`.
          * `excludedPaths` (`pulumi.Input[list]`) - List of paths to exclude from indexing. Required if `indexing_mode` is `Consistent` or `Lazy`.
          * `includedPaths` (`pulumi.Input[list]`) - List of paths to include in the indexing. Required if `indexing_mode` is `Consistent` or `Lazy`.
          * `indexingMode` (`pulumi.Input[str]`) - Indicates the indexing mode. Possible values include: `Consistent`, `Lazy`, `None`.

        The **unique_keys** object supports the following:

          * `paths` (`pulumi.Input[list]`) - A list of paths to use for this unique key.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["account_name"] = account_name
        __props__["conflict_resolution_policies"] = conflict_resolution_policies
        __props__["database_name"] = database_name
        __props__["index_policies"] = index_policies
        __props__["name"] = name
        __props__["partition_key_path"] = partition_key_path
        __props__["resource_group_name"] = resource_group_name
        __props__["throughput"] = throughput
        __props__["unique_keys"] = unique_keys
        return GremlinGraph(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
