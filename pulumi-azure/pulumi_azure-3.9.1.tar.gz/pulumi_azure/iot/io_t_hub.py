# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class IoTHub(pulumi.CustomResource):
    endpoints: pulumi.Output[list]
    """
    An `endpoint` block as defined below.

      * `batch_frequency_in_seconds` (`float`) - Time interval at which blobs are written to storage. Value should be between 60 and 720 seconds. Default value is 300 seconds. This attribute is mandatory for endpoint type `AzureIotHub.StorageContainer`.
      * `connection_string` (`str`) - The connection string for the endpoint.
      * `container_name` (`str`) - The name of storage container in the storage account. This attribute is mandatory for endpoint type `AzureIotHub.StorageContainer`.
      * `encoding` (`str`) - Encoding that is used to serialize messages to blobs. Supported values are 'avro' and 'avrodeflate'. Default value is 'avro'. This attribute is mandatory for endpoint type `AzureIotHub.StorageContainer`.
      * `file_name_format` (`str`) - File name format for the blob. Default format is ``{iothub}/{partition}/{YYYY}/{MM}/{DD}/{HH}/{mm}``. All parameters are mandatory but can be reordered. This attribute is mandatory for endpoint type `AzureIotHub.StorageContainer`.
      * `max_chunk_size_in_bytes` (`float`) - Maximum number of bytes for each blob written to storage. Value should be between 10485760(10MB) and 524288000(500MB). Default value is 314572800(300MB). This attribute is mandatory for endpoint type `AzureIotHub.StorageContainer`.
      * `name` (`str`) - The name of the endpoint. The name must be unique across endpoint types. The following names are reserved:  `events`, `operationsMonitoringEvents`, `fileNotifications` and `$default`.
      * `type` (`str`) - The type of the endpoint. Possible values are `AzureIotHub.StorageContainer`, `AzureIotHub.ServiceBusQueue`, `AzureIotHub.ServiceBusTopic` or `AzureIotHub.EventHub`.
    """
    event_hub_events_endpoint: pulumi.Output[str]
    """
    The EventHub compatible endpoint for events data
    """
    event_hub_events_path: pulumi.Output[str]
    """
    The EventHub compatible path for events data
    """
    event_hub_operations_endpoint: pulumi.Output[str]
    """
    The EventHub compatible endpoint for operational data
    """
    event_hub_operations_path: pulumi.Output[str]
    """
    The EventHub compatible path for operational data
    """
    event_hub_partition_count: pulumi.Output[float]
    """
    The number of device-to-cloud partitions used by backing event hubs. Must be between `2` and `128`.
    """
    event_hub_retention_in_days: pulumi.Output[float]
    """
    The event hub retention to use in days. Must be between `1` and `7`.
    """
    fallback_route: pulumi.Output[dict]
    """
    A `fallback_route` block as defined below. If the fallback route is enabled, messages that don't match any of the supplied routes are automatically sent to this route. Defaults to messages/events.

      * `condition` (`str`) - The condition that is evaluated to apply the routing rule. If no condition is provided, it evaluates to true by default. For grammar, see: https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-query-language.
      * `enabled` (`bool`) - Used to specify whether the fallback route is enabled.
      * `endpoint_names` (`list`) - The endpoints to which messages that satisfy the condition are routed. Currently only 1 endpoint is allowed.
      * `source` (`str`) - The source that the routing rule is to be applied to, such as `DeviceMessages`. Possible values include: `RoutingSourceInvalid`, `RoutingSourceDeviceMessages`, `RoutingSourceTwinChangeEvents`, `RoutingSourceDeviceLifecycleEvents`, `RoutingSourceDeviceJobLifecycleEvents`.
    """
    file_upload: pulumi.Output[dict]
    """
    A `file_upload` block as defined below.

      * `connection_string` (`str`) - The connection string for the Azure Storage account to which files are uploaded.
      * `container_name` (`str`) - The name of the root container where you upload files. The container need not exist but should be creatable using the connection_string specified.
      * `default_ttl` (`str`) - The period of time for which a file upload notification message is available to consume before it is expired by the IoT hub, specified as an [ISO 8601 timespan duration](https://en.wikipedia.org/wiki/ISO_8601#Durations). This value must be between 1 minute and 48 hours, and evaluates to 'PT1H' by default.
      * `lock_duration` (`str`) - The lock duration for the file upload notifications queue, specified as an [ISO 8601 timespan duration](https://en.wikipedia.org/wiki/ISO_8601#Durations). This value must be between 5 and 300 seconds, and evaluates to 'PT1M' by default.
      * `max_delivery_count` (`float`) - The number of times the IoT hub attempts to deliver a file upload notification message. It evaluates to 10 by default.
      * `notifications` (`bool`) - Used to specify whether file notifications are sent to IoT Hub on upload. It evaluates to false by default.
      * `sasTtl` (`str`) - The period of time for which the SAS URI generated by IoT Hub for file upload is valid, specified as an [ISO 8601 timespan duration](https://en.wikipedia.org/wiki/ISO_8601#Durations). This value must be between 1 minute and 24 hours, and evaluates to 'PT1H' by default.
    """
    hostname: pulumi.Output[str]
    """
    The hostname of the IotHub Resource.
    """
    ip_filter_rules: pulumi.Output[list]
    """
    One or more `ip_filter_rule` blocks as defined below.

      * `action` (`str`) - The desired action for requests captured by this rule. Possible values are  `Accept`, `Reject`
      * `ipMask` (`str`) - The IP address range in CIDR notation for the rule.
      * `name` (`str`) - The name of the filter.
    """
    location: pulumi.Output[str]
    """
    Specifies the supported Azure location where the resource has to be createc. Changing this forces a new resource to be created.
    """
    name: pulumi.Output[str]
    """
    Specifies the name of the IotHub resource. Changing this forces a new resource to be created.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group under which the IotHub resource has to be created. Changing this forces a new resource to be created.
    """
    routes: pulumi.Output[list]
    """
    A `route` block as defined below.

      * `condition` (`str`) - The condition that is evaluated to apply the routing rule. If no condition is provided, it evaluates to true by default. For grammar, see: https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-query-language.
      * `enabled` (`bool`) - Used to specify whether a route is enabled.
      * `endpoint_names` (`list`) - The list of endpoints to which messages that satisfy the condition are routed.
      * `name` (`str`) - The name of the route.
      * `source` (`str`) - The source that the routing rule is to be applied to, such as `DeviceMessages`. Possible values include: `RoutingSourceInvalid`, `RoutingSourceDeviceMessages`, `RoutingSourceTwinChangeEvents`, `RoutingSourceDeviceLifecycleEvents`, `RoutingSourceDeviceJobLifecycleEvents`.
    """
    shared_access_policies: pulumi.Output[list]
    """
    One or more `shared_access_policy` blocks as defined below.

      * `key_name` (`str`) - The name of the shared access policy.
      * `permissions` (`str`) - The permissions assigned to the shared access policy.
      * `primary_key` (`str`) - The primary key.
      * `secondary_key` (`str`) - The secondary key.
    """
    sku: pulumi.Output[dict]
    """
    A `sku` block as defined below.

      * `capacity` (`float`) - The number of provisioned IoT Hub units.
      * `name` (`str`) - The name of the sku. Possible values are `B1`, `B2`, `B3`, `F1`, `S1`, `S2`, and `S3`.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    type: pulumi.Output[str]
    """
    The type of the endpoint. Possible values are `AzureIotHub.StorageContainer`, `AzureIotHub.ServiceBusQueue`, `AzureIotHub.ServiceBusTopic` or `AzureIotHub.EventHub`.
    """
    def __init__(__self__, resource_name, opts=None, endpoints=None, event_hub_partition_count=None, event_hub_retention_in_days=None, fallback_route=None, file_upload=None, ip_filter_rules=None, location=None, name=None, resource_group_name=None, routes=None, sku=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages an IotHub

        > **NOTE:** Endpoints can be defined either directly on the `iot.IoTHub` resource, or using the `azurerm_iothub_endpoint_*` resources - but the two ways of defining the endpoints cannot be used together. If both are used against the same IoTHub, spurious changes will occur. Also, defining a `azurerm_iothub_endpoint_*` resource and another endpoint of a different type directly on the `iot.IoTHub` resource is not supported.

        > **NOTE:** Routes can be defined either directly on the `iot.IoTHub` resource, or using the `iot.Route` resource - but the two cannot be used together. If both are used against the same IoTHub, spurious changes will occur.

        > **NOTE:** Fallback route can be defined either directly on the `iot.IoTHub` resource, or using the `iot.FallbackRoute` resource - but the two cannot be used together. If both are used against the same IoTHub, spurious changes will occur.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="Canada Central")
        example_account = azure.storage.Account("exampleAccount",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            account_tier="Standard",
            account_replication_type="LRS")
        example_container = azure.storage.Container("exampleContainer",
            storage_account_name=example_account.name,
            container_access_type="private")
        example_event_hub_namespace = azure.eventhub.EventHubNamespace("exampleEventHubNamespace",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            sku="Basic")
        example_event_hub = azure.eventhub.EventHub("exampleEventHub",
            resource_group_name=example_resource_group.name,
            namespace_name=example_event_hub_namespace.name,
            partition_count=2,
            message_retention=1)
        example_authorization_rule = azure.eventhub.AuthorizationRule("exampleAuthorizationRule",
            resource_group_name=example_resource_group.name,
            namespace_name=example_event_hub_namespace.name,
            eventhub_name=example_event_hub.name,
            send=True)
        example_io_t_hub = azure.iot.IoTHub("exampleIoTHub",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            sku={
                "name": "S1",
                "capacity": "1",
            },
            endpoint=[
                {
                    "type": "AzureIotHub.StorageContainer",
                    "connection_string": example_account.primary_blob_connection_string,
                    "name": "export",
                    "batch_frequency_in_seconds": 60,
                    "max_chunk_size_in_bytes": 10485760,
                    "container_name": example_container.name,
                    "encoding": "Avro",
                    "file_name_format": "{iothub}/{partition}_{YYYY}_{MM}_{DD}_{HH}_{mm}",
                },
                {
                    "type": "AzureIotHub.EventHub",
                    "connection_string": example_authorization_rule.primary_connection_string,
                    "name": "export2",
                },
            ],
            route=[
                {
                    "name": "export",
                    "source": "DeviceMessages",
                    "condition": "true",
                    "endpoint_names": ["export"],
                    "enabled": True,
                },
                {
                    "name": "export2",
                    "source": "DeviceMessages",
                    "condition": "true",
                    "endpoint_names": ["export2"],
                    "enabled": True,
                },
            ],
            tags={
                "purpose": "testing",
            })
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] endpoints: An `endpoint` block as defined below.
        :param pulumi.Input[float] event_hub_partition_count: The number of device-to-cloud partitions used by backing event hubs. Must be between `2` and `128`.
        :param pulumi.Input[float] event_hub_retention_in_days: The event hub retention to use in days. Must be between `1` and `7`.
        :param pulumi.Input[dict] fallback_route: A `fallback_route` block as defined below. If the fallback route is enabled, messages that don't match any of the supplied routes are automatically sent to this route. Defaults to messages/events.
        :param pulumi.Input[dict] file_upload: A `file_upload` block as defined below.
        :param pulumi.Input[list] ip_filter_rules: One or more `ip_filter_rule` blocks as defined below.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource has to be createc. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the IotHub resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group under which the IotHub resource has to be created. Changing this forces a new resource to be created.
        :param pulumi.Input[list] routes: A `route` block as defined below.
        :param pulumi.Input[dict] sku: A `sku` block as defined below.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.

        The **endpoints** object supports the following:

          * `batch_frequency_in_seconds` (`pulumi.Input[float]`) - Time interval at which blobs are written to storage. Value should be between 60 and 720 seconds. Default value is 300 seconds. This attribute is mandatory for endpoint type `AzureIotHub.StorageContainer`.
          * `connection_string` (`pulumi.Input[str]`) - The connection string for the endpoint.
          * `container_name` (`pulumi.Input[str]`) - The name of storage container in the storage account. This attribute is mandatory for endpoint type `AzureIotHub.StorageContainer`.
          * `encoding` (`pulumi.Input[str]`) - Encoding that is used to serialize messages to blobs. Supported values are 'avro' and 'avrodeflate'. Default value is 'avro'. This attribute is mandatory for endpoint type `AzureIotHub.StorageContainer`.
          * `file_name_format` (`pulumi.Input[str]`) - File name format for the blob. Default format is ``{iothub}/{partition}/{YYYY}/{MM}/{DD}/{HH}/{mm}``. All parameters are mandatory but can be reordered. This attribute is mandatory for endpoint type `AzureIotHub.StorageContainer`.
          * `max_chunk_size_in_bytes` (`pulumi.Input[float]`) - Maximum number of bytes for each blob written to storage. Value should be between 10485760(10MB) and 524288000(500MB). Default value is 314572800(300MB). This attribute is mandatory for endpoint type `AzureIotHub.StorageContainer`.
          * `name` (`pulumi.Input[str]`) - The name of the endpoint. The name must be unique across endpoint types. The following names are reserved:  `events`, `operationsMonitoringEvents`, `fileNotifications` and `$default`.
          * `type` (`pulumi.Input[str]`) - The type of the endpoint. Possible values are `AzureIotHub.StorageContainer`, `AzureIotHub.ServiceBusQueue`, `AzureIotHub.ServiceBusTopic` or `AzureIotHub.EventHub`.

        The **fallback_route** object supports the following:

          * `condition` (`pulumi.Input[str]`) - The condition that is evaluated to apply the routing rule. If no condition is provided, it evaluates to true by default. For grammar, see: https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-query-language.
          * `enabled` (`pulumi.Input[bool]`) - Used to specify whether the fallback route is enabled.
          * `endpoint_names` (`pulumi.Input[list]`) - The endpoints to which messages that satisfy the condition are routed. Currently only 1 endpoint is allowed.
          * `source` (`pulumi.Input[str]`) - The source that the routing rule is to be applied to, such as `DeviceMessages`. Possible values include: `RoutingSourceInvalid`, `RoutingSourceDeviceMessages`, `RoutingSourceTwinChangeEvents`, `RoutingSourceDeviceLifecycleEvents`, `RoutingSourceDeviceJobLifecycleEvents`.

        The **file_upload** object supports the following:

          * `connection_string` (`pulumi.Input[str]`) - The connection string for the Azure Storage account to which files are uploaded.
          * `container_name` (`pulumi.Input[str]`) - The name of the root container where you upload files. The container need not exist but should be creatable using the connection_string specified.
          * `default_ttl` (`pulumi.Input[str]`) - The period of time for which a file upload notification message is available to consume before it is expired by the IoT hub, specified as an [ISO 8601 timespan duration](https://en.wikipedia.org/wiki/ISO_8601#Durations). This value must be between 1 minute and 48 hours, and evaluates to 'PT1H' by default.
          * `lock_duration` (`pulumi.Input[str]`) - The lock duration for the file upload notifications queue, specified as an [ISO 8601 timespan duration](https://en.wikipedia.org/wiki/ISO_8601#Durations). This value must be between 5 and 300 seconds, and evaluates to 'PT1M' by default.
          * `max_delivery_count` (`pulumi.Input[float]`) - The number of times the IoT hub attempts to deliver a file upload notification message. It evaluates to 10 by default.
          * `notifications` (`pulumi.Input[bool]`) - Used to specify whether file notifications are sent to IoT Hub on upload. It evaluates to false by default.
          * `sasTtl` (`pulumi.Input[str]`) - The period of time for which the SAS URI generated by IoT Hub for file upload is valid, specified as an [ISO 8601 timespan duration](https://en.wikipedia.org/wiki/ISO_8601#Durations). This value must be between 1 minute and 24 hours, and evaluates to 'PT1H' by default.

        The **ip_filter_rules** object supports the following:

          * `action` (`pulumi.Input[str]`) - The desired action for requests captured by this rule. Possible values are  `Accept`, `Reject`
          * `ipMask` (`pulumi.Input[str]`) - The IP address range in CIDR notation for the rule.
          * `name` (`pulumi.Input[str]`) - The name of the filter.

        The **routes** object supports the following:

          * `condition` (`pulumi.Input[str]`) - The condition that is evaluated to apply the routing rule. If no condition is provided, it evaluates to true by default. For grammar, see: https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-query-language.
          * `enabled` (`pulumi.Input[bool]`) - Used to specify whether a route is enabled.
          * `endpoint_names` (`pulumi.Input[list]`) - The list of endpoints to which messages that satisfy the condition are routed.
          * `name` (`pulumi.Input[str]`) - The name of the route.
          * `source` (`pulumi.Input[str]`) - The source that the routing rule is to be applied to, such as `DeviceMessages`. Possible values include: `RoutingSourceInvalid`, `RoutingSourceDeviceMessages`, `RoutingSourceTwinChangeEvents`, `RoutingSourceDeviceLifecycleEvents`, `RoutingSourceDeviceJobLifecycleEvents`.

        The **sku** object supports the following:

          * `capacity` (`pulumi.Input[float]`) - The number of provisioned IoT Hub units.
          * `name` (`pulumi.Input[str]`) - The name of the sku. Possible values are `B1`, `B2`, `B3`, `F1`, `S1`, `S2`, and `S3`.
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

            __props__['endpoints'] = endpoints
            __props__['event_hub_partition_count'] = event_hub_partition_count
            __props__['event_hub_retention_in_days'] = event_hub_retention_in_days
            __props__['fallback_route'] = fallback_route
            __props__['file_upload'] = file_upload
            __props__['ip_filter_rules'] = ip_filter_rules
            __props__['location'] = location
            __props__['name'] = name
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['routes'] = routes
            if sku is None:
                raise TypeError("Missing required property 'sku'")
            __props__['sku'] = sku
            __props__['tags'] = tags
            __props__['event_hub_events_endpoint'] = None
            __props__['event_hub_events_path'] = None
            __props__['event_hub_operations_endpoint'] = None
            __props__['event_hub_operations_path'] = None
            __props__['hostname'] = None
            __props__['shared_access_policies'] = None
            __props__['type'] = None
        super(IoTHub, __self__).__init__(
            'azure:iot/ioTHub:IoTHub',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, endpoints=None, event_hub_events_endpoint=None, event_hub_events_path=None, event_hub_operations_endpoint=None, event_hub_operations_path=None, event_hub_partition_count=None, event_hub_retention_in_days=None, fallback_route=None, file_upload=None, hostname=None, ip_filter_rules=None, location=None, name=None, resource_group_name=None, routes=None, shared_access_policies=None, sku=None, tags=None, type=None):
        """
        Get an existing IoTHub resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] endpoints: An `endpoint` block as defined below.
        :param pulumi.Input[str] event_hub_events_endpoint: The EventHub compatible endpoint for events data
        :param pulumi.Input[str] event_hub_events_path: The EventHub compatible path for events data
        :param pulumi.Input[str] event_hub_operations_endpoint: The EventHub compatible endpoint for operational data
        :param pulumi.Input[str] event_hub_operations_path: The EventHub compatible path for operational data
        :param pulumi.Input[float] event_hub_partition_count: The number of device-to-cloud partitions used by backing event hubs. Must be between `2` and `128`.
        :param pulumi.Input[float] event_hub_retention_in_days: The event hub retention to use in days. Must be between `1` and `7`.
        :param pulumi.Input[dict] fallback_route: A `fallback_route` block as defined below. If the fallback route is enabled, messages that don't match any of the supplied routes are automatically sent to this route. Defaults to messages/events.
        :param pulumi.Input[dict] file_upload: A `file_upload` block as defined below.
        :param pulumi.Input[str] hostname: The hostname of the IotHub Resource.
        :param pulumi.Input[list] ip_filter_rules: One or more `ip_filter_rule` blocks as defined below.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource has to be createc. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the IotHub resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group under which the IotHub resource has to be created. Changing this forces a new resource to be created.
        :param pulumi.Input[list] routes: A `route` block as defined below.
        :param pulumi.Input[list] shared_access_policies: One or more `shared_access_policy` blocks as defined below.
        :param pulumi.Input[dict] sku: A `sku` block as defined below.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] type: The type of the endpoint. Possible values are `AzureIotHub.StorageContainer`, `AzureIotHub.ServiceBusQueue`, `AzureIotHub.ServiceBusTopic` or `AzureIotHub.EventHub`.

        The **endpoints** object supports the following:

          * `batch_frequency_in_seconds` (`pulumi.Input[float]`) - Time interval at which blobs are written to storage. Value should be between 60 and 720 seconds. Default value is 300 seconds. This attribute is mandatory for endpoint type `AzureIotHub.StorageContainer`.
          * `connection_string` (`pulumi.Input[str]`) - The connection string for the endpoint.
          * `container_name` (`pulumi.Input[str]`) - The name of storage container in the storage account. This attribute is mandatory for endpoint type `AzureIotHub.StorageContainer`.
          * `encoding` (`pulumi.Input[str]`) - Encoding that is used to serialize messages to blobs. Supported values are 'avro' and 'avrodeflate'. Default value is 'avro'. This attribute is mandatory for endpoint type `AzureIotHub.StorageContainer`.
          * `file_name_format` (`pulumi.Input[str]`) - File name format for the blob. Default format is ``{iothub}/{partition}/{YYYY}/{MM}/{DD}/{HH}/{mm}``. All parameters are mandatory but can be reordered. This attribute is mandatory for endpoint type `AzureIotHub.StorageContainer`.
          * `max_chunk_size_in_bytes` (`pulumi.Input[float]`) - Maximum number of bytes for each blob written to storage. Value should be between 10485760(10MB) and 524288000(500MB). Default value is 314572800(300MB). This attribute is mandatory for endpoint type `AzureIotHub.StorageContainer`.
          * `name` (`pulumi.Input[str]`) - The name of the endpoint. The name must be unique across endpoint types. The following names are reserved:  `events`, `operationsMonitoringEvents`, `fileNotifications` and `$default`.
          * `type` (`pulumi.Input[str]`) - The type of the endpoint. Possible values are `AzureIotHub.StorageContainer`, `AzureIotHub.ServiceBusQueue`, `AzureIotHub.ServiceBusTopic` or `AzureIotHub.EventHub`.

        The **fallback_route** object supports the following:

          * `condition` (`pulumi.Input[str]`) - The condition that is evaluated to apply the routing rule. If no condition is provided, it evaluates to true by default. For grammar, see: https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-query-language.
          * `enabled` (`pulumi.Input[bool]`) - Used to specify whether the fallback route is enabled.
          * `endpoint_names` (`pulumi.Input[list]`) - The endpoints to which messages that satisfy the condition are routed. Currently only 1 endpoint is allowed.
          * `source` (`pulumi.Input[str]`) - The source that the routing rule is to be applied to, such as `DeviceMessages`. Possible values include: `RoutingSourceInvalid`, `RoutingSourceDeviceMessages`, `RoutingSourceTwinChangeEvents`, `RoutingSourceDeviceLifecycleEvents`, `RoutingSourceDeviceJobLifecycleEvents`.

        The **file_upload** object supports the following:

          * `connection_string` (`pulumi.Input[str]`) - The connection string for the Azure Storage account to which files are uploaded.
          * `container_name` (`pulumi.Input[str]`) - The name of the root container where you upload files. The container need not exist but should be creatable using the connection_string specified.
          * `default_ttl` (`pulumi.Input[str]`) - The period of time for which a file upload notification message is available to consume before it is expired by the IoT hub, specified as an [ISO 8601 timespan duration](https://en.wikipedia.org/wiki/ISO_8601#Durations). This value must be between 1 minute and 48 hours, and evaluates to 'PT1H' by default.
          * `lock_duration` (`pulumi.Input[str]`) - The lock duration for the file upload notifications queue, specified as an [ISO 8601 timespan duration](https://en.wikipedia.org/wiki/ISO_8601#Durations). This value must be between 5 and 300 seconds, and evaluates to 'PT1M' by default.
          * `max_delivery_count` (`pulumi.Input[float]`) - The number of times the IoT hub attempts to deliver a file upload notification message. It evaluates to 10 by default.
          * `notifications` (`pulumi.Input[bool]`) - Used to specify whether file notifications are sent to IoT Hub on upload. It evaluates to false by default.
          * `sasTtl` (`pulumi.Input[str]`) - The period of time for which the SAS URI generated by IoT Hub for file upload is valid, specified as an [ISO 8601 timespan duration](https://en.wikipedia.org/wiki/ISO_8601#Durations). This value must be between 1 minute and 24 hours, and evaluates to 'PT1H' by default.

        The **ip_filter_rules** object supports the following:

          * `action` (`pulumi.Input[str]`) - The desired action for requests captured by this rule. Possible values are  `Accept`, `Reject`
          * `ipMask` (`pulumi.Input[str]`) - The IP address range in CIDR notation for the rule.
          * `name` (`pulumi.Input[str]`) - The name of the filter.

        The **routes** object supports the following:

          * `condition` (`pulumi.Input[str]`) - The condition that is evaluated to apply the routing rule. If no condition is provided, it evaluates to true by default. For grammar, see: https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-query-language.
          * `enabled` (`pulumi.Input[bool]`) - Used to specify whether a route is enabled.
          * `endpoint_names` (`pulumi.Input[list]`) - The list of endpoints to which messages that satisfy the condition are routed.
          * `name` (`pulumi.Input[str]`) - The name of the route.
          * `source` (`pulumi.Input[str]`) - The source that the routing rule is to be applied to, such as `DeviceMessages`. Possible values include: `RoutingSourceInvalid`, `RoutingSourceDeviceMessages`, `RoutingSourceTwinChangeEvents`, `RoutingSourceDeviceLifecycleEvents`, `RoutingSourceDeviceJobLifecycleEvents`.

        The **shared_access_policies** object supports the following:

          * `key_name` (`pulumi.Input[str]`) - The name of the shared access policy.
          * `permissions` (`pulumi.Input[str]`) - The permissions assigned to the shared access policy.
          * `primary_key` (`pulumi.Input[str]`) - The primary key.
          * `secondary_key` (`pulumi.Input[str]`) - The secondary key.

        The **sku** object supports the following:

          * `capacity` (`pulumi.Input[float]`) - The number of provisioned IoT Hub units.
          * `name` (`pulumi.Input[str]`) - The name of the sku. Possible values are `B1`, `B2`, `B3`, `F1`, `S1`, `S2`, and `S3`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["endpoints"] = endpoints
        __props__["event_hub_events_endpoint"] = event_hub_events_endpoint
        __props__["event_hub_events_path"] = event_hub_events_path
        __props__["event_hub_operations_endpoint"] = event_hub_operations_endpoint
        __props__["event_hub_operations_path"] = event_hub_operations_path
        __props__["event_hub_partition_count"] = event_hub_partition_count
        __props__["event_hub_retention_in_days"] = event_hub_retention_in_days
        __props__["fallback_route"] = fallback_route
        __props__["file_upload"] = file_upload
        __props__["hostname"] = hostname
        __props__["ip_filter_rules"] = ip_filter_rules
        __props__["location"] = location
        __props__["name"] = name
        __props__["resource_group_name"] = resource_group_name
        __props__["routes"] = routes
        __props__["shared_access_policies"] = shared_access_policies
        __props__["sku"] = sku
        __props__["tags"] = tags
        __props__["type"] = type
        return IoTHub(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
