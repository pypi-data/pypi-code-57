# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class EventSubscription(pulumi.CustomResource):
    advanced_filter: pulumi.Output[dict]
    """
    A `advanced_filter` block as defined below.

      * `boolEquals` (`list`) - Compares a value of an event using a single boolean value.
        * `key` (`str`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
        * `value` (`bool`) - Specifies a single value to compare to when using a single value operator.

      * `numberGreaterThanOrEquals` (`list`) - Compares a value of an event using a single floating point number.
        * `key` (`str`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
        * `value` (`float`) - Specifies a single value to compare to when using a single value operator.

      * `numberGreaterThans` (`list`) - Compares a value of an event using a single floating point number.
        * `key` (`str`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
        * `value` (`float`) - Specifies a single value to compare to when using a single value operator.

      * `numberIns` (`list`) - Compares a value of an event using multiple floating point numbers.
        * `key` (`str`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
        * `values` (`list`) - Specifies an array of values to compare to when using a multiple values operator.

      * `numberLessThanOrEquals` (`list`) - Compares a value of an event using a single floating point number.
        * `key` (`str`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
        * `value` (`float`) - Specifies a single value to compare to when using a single value operator.

      * `numberLessThans` (`list`) - Compares a value of an event using a single floating point number.
        * `key` (`str`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
        * `value` (`float`) - Specifies a single value to compare to when using a single value operator.

      * `numberNotIns` (`list`) - Compares a value of an event using multiple floating point numbers.
        * `key` (`str`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
        * `values` (`list`) - Specifies an array of values to compare to when using a multiple values operator.

      * `stringBeginsWiths` (`list`) - Compares a value of an event using multiple string values.
        * `key` (`str`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
        * `values` (`list`) - Specifies an array of values to compare to when using a multiple values operator.

      * `stringContains` (`list`) - Compares a value of an event using multiple string values.
        * `key` (`str`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
        * `values` (`list`) - Specifies an array of values to compare to when using a multiple values operator.

      * `stringEndsWiths` (`list`) - Compares a value of an event using multiple string values.
        * `key` (`str`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
        * `values` (`list`) - Specifies an array of values to compare to when using a multiple values operator.

      * `stringIns` (`list`) - Compares a value of an event using multiple string values.
        * `key` (`str`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
        * `values` (`list`) - Specifies an array of values to compare to when using a multiple values operator.

      * `stringNotIns` (`list`) - Compares a value of an event using multiple string values.
        * `key` (`str`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
        * `values` (`list`) - Specifies an array of values to compare to when using a multiple values operator.
    """
    azure_function_endpoint: pulumi.Output[dict]
    """
    An `azure_function_endpoint` block as defined below.

      * `functionId` (`str`) - Specifies the ID of the Function where the Event Subscription will receive events.
      * `maxEventsPerBatch` (`float`) - Maximum number of events per batch.
      * `preferredBatchSizeInKilobytes` (`float`) - Preferred batch size in Kilobytes.
    """
    event_delivery_schema: pulumi.Output[str]
    """
    Specifies the event delivery schema for the event subscription. Possible values include: `EventGridSchema`, `CloudEventSchemaV1_0`, `CustomInputSchema`. Defaults to `EventGridSchema`. Changing this forces a new resource to be created.
    """
    eventhub_endpoint: pulumi.Output[dict]
    """
    A `eventhub_endpoint` block as defined below.

      * `eventhub_id` (`str`) - Specifies the id of the eventhub where the Event Subscription will receive events.
    """
    eventhub_endpoint_id: pulumi.Output[str]
    """
    Specifies the id where the Event Hub is located.
    """
    expiration_time_utc: pulumi.Output[str]
    """
    Specifies the expiration time of the event subscription (Datetime Format `RFC 3339`).
    """
    hybrid_connection_endpoint: pulumi.Output[dict]
    """
    A `hybrid_connection_endpoint` block as defined below.

      * `hybridConnectionId` (`str`) - Specifies the id of the hybrid connection where the Event Subscription will receive events.
    """
    hybrid_connection_endpoint_id: pulumi.Output[str]
    """
    Specifies the id where the Hybrid Connection is located.
    """
    included_event_types: pulumi.Output[list]
    """
    A list of applicable event types that need to be part of the event subscription.
    """
    labels: pulumi.Output[list]
    """
    A list of labels to assign to the event subscription.
    """
    name: pulumi.Output[str]
    """
    Specifies the name of the EventGrid Event Subscription resource. Changing this forces a new resource to be created.
    """
    retry_policy: pulumi.Output[dict]
    """
    A `retry_policy` block as defined below.

      * `eventTimeToLive` (`float`) - Specifies the time to live (in minutes) for events.
      * `maxDeliveryAttempts` (`float`) - Specifies the maximum number of delivery retry attempts for events.
    """
    scope: pulumi.Output[str]
    """
    Specifies the scope at which the EventGrid Event Subscription should be created. Changing this forces a new resource to be created.
    """
    service_bus_queue_endpoint_id: pulumi.Output[str]
    """
    Specifies the id where the Service Bus Queue is located.
    """
    service_bus_topic_endpoint_id: pulumi.Output[str]
    """
    Specifies the id where the Service Bus Topic is located.
    """
    storage_blob_dead_letter_destination: pulumi.Output[dict]
    """
    A `storage_blob_dead_letter_destination` block as defined below.

      * `storage_account_id` (`str`) - Specifies the id of the storage account id where the storage blob is located.
      * `storageBlobContainerName` (`str`) - Specifies the name of the Storage blob container that is the destination of the deadletter events.
    """
    storage_queue_endpoint: pulumi.Output[dict]
    """
    A `storage_queue_endpoint` block as defined below.

      * `queue_name` (`str`) - Specifies the name of the storage queue where the Event Subscription will receive events.
      * `storage_account_id` (`str`) - Specifies the id of the storage account id where the storage queue is located.
    """
    subject_filter: pulumi.Output[dict]
    """
    A `subject_filter` block as defined below.

      * `caseSensitive` (`bool`) - Specifies if `subject_begins_with` and `subject_ends_with` case sensitive. This value defaults to `false`.
      * `subjectBeginsWith` (`str`) - A string to filter events for an event subscription based on a resource path prefix.
      * `subjectEndsWith` (`str`) - A string to filter events for an event subscription based on a resource path suffix.
    """
    topic_name: pulumi.Output[str]
    """
    (Optional) Specifies the name of the topic to associate with the event subscription.
    """
    webhook_endpoint: pulumi.Output[dict]
    """
    A `webhook_endpoint` block as defined below.

      * `activeDirectoryAppIdOrUri` (`str`) - The Azure Active Directory Application ID or URI to get the access token that will be included as the bearer token in delivery requests.
      * `activeDirectoryTenantId` (`str`) - The Azure Active Directory Tenant ID to get the access token that will be included as the bearer token in delivery requests.
      * `baseUrl` (`str`) - The base url of the webhook where the Event Subscription will receive events.
      * `maxEventsPerBatch` (`float`) - Maximum number of events per batch.
      * `preferredBatchSizeInKilobytes` (`float`) - Preferred batch size in Kilobytes.
      * `url` (`str`) - Specifies the url of the webhook where the Event Subscription will receive events.
    """
    def __init__(__self__, resource_name, opts=None, advanced_filter=None, azure_function_endpoint=None, event_delivery_schema=None, eventhub_endpoint=None, eventhub_endpoint_id=None, expiration_time_utc=None, hybrid_connection_endpoint=None, hybrid_connection_endpoint_id=None, included_event_types=None, labels=None, name=None, retry_policy=None, scope=None, service_bus_queue_endpoint_id=None, service_bus_topic_endpoint_id=None, storage_blob_dead_letter_destination=None, storage_queue_endpoint=None, subject_filter=None, topic_name=None, webhook_endpoint=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages an EventGrid Event Subscription

        ## Example Usage



        ```python
        import pulumi
        import pulumi_azure as azure

        default_resource_group = azure.core.ResourceGroup("defaultResourceGroup", location="West US 2")
        default_account = azure.storage.Account("defaultAccount",
            resource_group_name=default_resource_group.name,
            location=default_resource_group.location,
            account_tier="Standard",
            account_replication_type="LRS",
            tags={
                "environment": "staging",
            })
        default_queue = azure.storage.Queue("defaultQueue", storage_account_name=default_account.name)
        default_event_subscription = azure.eventgrid.EventSubscription("defaultEventSubscription",
            scope=default_resource_group.id,
            storage_queue_endpoint={
                "storage_account_id": default_account.id,
                "queue_name": default_queue.name,
            })
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] advanced_filter: A `advanced_filter` block as defined below.
        :param pulumi.Input[dict] azure_function_endpoint: An `azure_function_endpoint` block as defined below.
        :param pulumi.Input[str] event_delivery_schema: Specifies the event delivery schema for the event subscription. Possible values include: `EventGridSchema`, `CloudEventSchemaV1_0`, `CustomInputSchema`. Defaults to `EventGridSchema`. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] eventhub_endpoint: A `eventhub_endpoint` block as defined below.
        :param pulumi.Input[str] eventhub_endpoint_id: Specifies the id where the Event Hub is located.
        :param pulumi.Input[str] expiration_time_utc: Specifies the expiration time of the event subscription (Datetime Format `RFC 3339`).
        :param pulumi.Input[dict] hybrid_connection_endpoint: A `hybrid_connection_endpoint` block as defined below.
        :param pulumi.Input[str] hybrid_connection_endpoint_id: Specifies the id where the Hybrid Connection is located.
        :param pulumi.Input[list] included_event_types: A list of applicable event types that need to be part of the event subscription.
        :param pulumi.Input[list] labels: A list of labels to assign to the event subscription.
        :param pulumi.Input[str] name: Specifies the name of the EventGrid Event Subscription resource. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] retry_policy: A `retry_policy` block as defined below.
        :param pulumi.Input[str] scope: Specifies the scope at which the EventGrid Event Subscription should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] service_bus_queue_endpoint_id: Specifies the id where the Service Bus Queue is located.
        :param pulumi.Input[str] service_bus_topic_endpoint_id: Specifies the id where the Service Bus Topic is located.
        :param pulumi.Input[dict] storage_blob_dead_letter_destination: A `storage_blob_dead_letter_destination` block as defined below.
        :param pulumi.Input[dict] storage_queue_endpoint: A `storage_queue_endpoint` block as defined below.
        :param pulumi.Input[dict] subject_filter: A `subject_filter` block as defined below.
        :param pulumi.Input[str] topic_name: (Optional) Specifies the name of the topic to associate with the event subscription.
        :param pulumi.Input[dict] webhook_endpoint: A `webhook_endpoint` block as defined below.

        The **advanced_filter** object supports the following:

          * `boolEquals` (`pulumi.Input[list]`) - Compares a value of an event using a single boolean value.
            * `key` (`pulumi.Input[str]`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
            * `value` (`pulumi.Input[bool]`) - Specifies a single value to compare to when using a single value operator.

          * `numberGreaterThanOrEquals` (`pulumi.Input[list]`) - Compares a value of an event using a single floating point number.
            * `key` (`pulumi.Input[str]`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
            * `value` (`pulumi.Input[float]`) - Specifies a single value to compare to when using a single value operator.

          * `numberGreaterThans` (`pulumi.Input[list]`) - Compares a value of an event using a single floating point number.
            * `key` (`pulumi.Input[str]`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
            * `value` (`pulumi.Input[float]`) - Specifies a single value to compare to when using a single value operator.

          * `numberIns` (`pulumi.Input[list]`) - Compares a value of an event using multiple floating point numbers.
            * `key` (`pulumi.Input[str]`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
            * `values` (`pulumi.Input[list]`) - Specifies an array of values to compare to when using a multiple values operator.

          * `numberLessThanOrEquals` (`pulumi.Input[list]`) - Compares a value of an event using a single floating point number.
            * `key` (`pulumi.Input[str]`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
            * `value` (`pulumi.Input[float]`) - Specifies a single value to compare to when using a single value operator.

          * `numberLessThans` (`pulumi.Input[list]`) - Compares a value of an event using a single floating point number.
            * `key` (`pulumi.Input[str]`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
            * `value` (`pulumi.Input[float]`) - Specifies a single value to compare to when using a single value operator.

          * `numberNotIns` (`pulumi.Input[list]`) - Compares a value of an event using multiple floating point numbers.
            * `key` (`pulumi.Input[str]`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
            * `values` (`pulumi.Input[list]`) - Specifies an array of values to compare to when using a multiple values operator.

          * `stringBeginsWiths` (`pulumi.Input[list]`) - Compares a value of an event using multiple string values.
            * `key` (`pulumi.Input[str]`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
            * `values` (`pulumi.Input[list]`) - Specifies an array of values to compare to when using a multiple values operator.

          * `stringContains` (`pulumi.Input[list]`) - Compares a value of an event using multiple string values.
            * `key` (`pulumi.Input[str]`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
            * `values` (`pulumi.Input[list]`) - Specifies an array of values to compare to when using a multiple values operator.

          * `stringEndsWiths` (`pulumi.Input[list]`) - Compares a value of an event using multiple string values.
            * `key` (`pulumi.Input[str]`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
            * `values` (`pulumi.Input[list]`) - Specifies an array of values to compare to when using a multiple values operator.

          * `stringIns` (`pulumi.Input[list]`) - Compares a value of an event using multiple string values.
            * `key` (`pulumi.Input[str]`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
            * `values` (`pulumi.Input[list]`) - Specifies an array of values to compare to when using a multiple values operator.

          * `stringNotIns` (`pulumi.Input[list]`) - Compares a value of an event using multiple string values.
            * `key` (`pulumi.Input[str]`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
            * `values` (`pulumi.Input[list]`) - Specifies an array of values to compare to when using a multiple values operator.

        The **azure_function_endpoint** object supports the following:

          * `functionId` (`pulumi.Input[str]`) - Specifies the ID of the Function where the Event Subscription will receive events.
          * `maxEventsPerBatch` (`pulumi.Input[float]`) - Maximum number of events per batch.
          * `preferredBatchSizeInKilobytes` (`pulumi.Input[float]`) - Preferred batch size in Kilobytes.

        The **eventhub_endpoint** object supports the following:

          * `eventhub_id` (`pulumi.Input[str]`) - Specifies the id of the eventhub where the Event Subscription will receive events.

        The **hybrid_connection_endpoint** object supports the following:

          * `hybridConnectionId` (`pulumi.Input[str]`) - Specifies the id of the hybrid connection where the Event Subscription will receive events.

        The **retry_policy** object supports the following:

          * `eventTimeToLive` (`pulumi.Input[float]`) - Specifies the time to live (in minutes) for events.
          * `maxDeliveryAttempts` (`pulumi.Input[float]`) - Specifies the maximum number of delivery retry attempts for events.

        The **storage_blob_dead_letter_destination** object supports the following:

          * `storage_account_id` (`pulumi.Input[str]`) - Specifies the id of the storage account id where the storage blob is located.
          * `storageBlobContainerName` (`pulumi.Input[str]`) - Specifies the name of the Storage blob container that is the destination of the deadletter events.

        The **storage_queue_endpoint** object supports the following:

          * `queue_name` (`pulumi.Input[str]`) - Specifies the name of the storage queue where the Event Subscription will receive events.
          * `storage_account_id` (`pulumi.Input[str]`) - Specifies the id of the storage account id where the storage queue is located.

        The **subject_filter** object supports the following:

          * `caseSensitive` (`pulumi.Input[bool]`) - Specifies if `subject_begins_with` and `subject_ends_with` case sensitive. This value defaults to `false`.
          * `subjectBeginsWith` (`pulumi.Input[str]`) - A string to filter events for an event subscription based on a resource path prefix.
          * `subjectEndsWith` (`pulumi.Input[str]`) - A string to filter events for an event subscription based on a resource path suffix.

        The **webhook_endpoint** object supports the following:

          * `activeDirectoryAppIdOrUri` (`pulumi.Input[str]`) - The Azure Active Directory Application ID or URI to get the access token that will be included as the bearer token in delivery requests.
          * `activeDirectoryTenantId` (`pulumi.Input[str]`) - The Azure Active Directory Tenant ID to get the access token that will be included as the bearer token in delivery requests.
          * `baseUrl` (`pulumi.Input[str]`) - The base url of the webhook where the Event Subscription will receive events.
          * `maxEventsPerBatch` (`pulumi.Input[float]`) - Maximum number of events per batch.
          * `preferredBatchSizeInKilobytes` (`pulumi.Input[float]`) - Preferred batch size in Kilobytes.
          * `url` (`pulumi.Input[str]`) - Specifies the url of the webhook where the Event Subscription will receive events.
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

            __props__['advanced_filter'] = advanced_filter
            __props__['azure_function_endpoint'] = azure_function_endpoint
            __props__['event_delivery_schema'] = event_delivery_schema
            if eventhub_endpoint is not None:
                warnings.warn("Deprecated in favour of `eventhub_endpoint_id`", DeprecationWarning)
                pulumi.log.warn("eventhub_endpoint is deprecated: Deprecated in favour of `eventhub_endpoint_id`")
            __props__['eventhub_endpoint'] = eventhub_endpoint
            __props__['eventhub_endpoint_id'] = eventhub_endpoint_id
            __props__['expiration_time_utc'] = expiration_time_utc
            if hybrid_connection_endpoint is not None:
                warnings.warn("Deprecated in favour of `hybrid_connection_endpoint_id`", DeprecationWarning)
                pulumi.log.warn("hybrid_connection_endpoint is deprecated: Deprecated in favour of `hybrid_connection_endpoint_id`")
            __props__['hybrid_connection_endpoint'] = hybrid_connection_endpoint
            __props__['hybrid_connection_endpoint_id'] = hybrid_connection_endpoint_id
            __props__['included_event_types'] = included_event_types
            __props__['labels'] = labels
            __props__['name'] = name
            __props__['retry_policy'] = retry_policy
            if scope is None:
                raise TypeError("Missing required property 'scope'")
            __props__['scope'] = scope
            __props__['service_bus_queue_endpoint_id'] = service_bus_queue_endpoint_id
            __props__['service_bus_topic_endpoint_id'] = service_bus_topic_endpoint_id
            __props__['storage_blob_dead_letter_destination'] = storage_blob_dead_letter_destination
            __props__['storage_queue_endpoint'] = storage_queue_endpoint
            __props__['subject_filter'] = subject_filter
            __props__['topic_name'] = topic_name
            __props__['webhook_endpoint'] = webhook_endpoint
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure:eventhub/eventSubscription:EventSubscription")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(EventSubscription, __self__).__init__(
            'azure:eventgrid/eventSubscription:EventSubscription',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, advanced_filter=None, azure_function_endpoint=None, event_delivery_schema=None, eventhub_endpoint=None, eventhub_endpoint_id=None, expiration_time_utc=None, hybrid_connection_endpoint=None, hybrid_connection_endpoint_id=None, included_event_types=None, labels=None, name=None, retry_policy=None, scope=None, service_bus_queue_endpoint_id=None, service_bus_topic_endpoint_id=None, storage_blob_dead_letter_destination=None, storage_queue_endpoint=None, subject_filter=None, topic_name=None, webhook_endpoint=None):
        """
        Get an existing EventSubscription resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] advanced_filter: A `advanced_filter` block as defined below.
        :param pulumi.Input[dict] azure_function_endpoint: An `azure_function_endpoint` block as defined below.
        :param pulumi.Input[str] event_delivery_schema: Specifies the event delivery schema for the event subscription. Possible values include: `EventGridSchema`, `CloudEventSchemaV1_0`, `CustomInputSchema`. Defaults to `EventGridSchema`. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] eventhub_endpoint: A `eventhub_endpoint` block as defined below.
        :param pulumi.Input[str] eventhub_endpoint_id: Specifies the id where the Event Hub is located.
        :param pulumi.Input[str] expiration_time_utc: Specifies the expiration time of the event subscription (Datetime Format `RFC 3339`).
        :param pulumi.Input[dict] hybrid_connection_endpoint: A `hybrid_connection_endpoint` block as defined below.
        :param pulumi.Input[str] hybrid_connection_endpoint_id: Specifies the id where the Hybrid Connection is located.
        :param pulumi.Input[list] included_event_types: A list of applicable event types that need to be part of the event subscription.
        :param pulumi.Input[list] labels: A list of labels to assign to the event subscription.
        :param pulumi.Input[str] name: Specifies the name of the EventGrid Event Subscription resource. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] retry_policy: A `retry_policy` block as defined below.
        :param pulumi.Input[str] scope: Specifies the scope at which the EventGrid Event Subscription should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] service_bus_queue_endpoint_id: Specifies the id where the Service Bus Queue is located.
        :param pulumi.Input[str] service_bus_topic_endpoint_id: Specifies the id where the Service Bus Topic is located.
        :param pulumi.Input[dict] storage_blob_dead_letter_destination: A `storage_blob_dead_letter_destination` block as defined below.
        :param pulumi.Input[dict] storage_queue_endpoint: A `storage_queue_endpoint` block as defined below.
        :param pulumi.Input[dict] subject_filter: A `subject_filter` block as defined below.
        :param pulumi.Input[str] topic_name: (Optional) Specifies the name of the topic to associate with the event subscription.
        :param pulumi.Input[dict] webhook_endpoint: A `webhook_endpoint` block as defined below.

        The **advanced_filter** object supports the following:

          * `boolEquals` (`pulumi.Input[list]`) - Compares a value of an event using a single boolean value.
            * `key` (`pulumi.Input[str]`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
            * `value` (`pulumi.Input[bool]`) - Specifies a single value to compare to when using a single value operator.

          * `numberGreaterThanOrEquals` (`pulumi.Input[list]`) - Compares a value of an event using a single floating point number.
            * `key` (`pulumi.Input[str]`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
            * `value` (`pulumi.Input[float]`) - Specifies a single value to compare to when using a single value operator.

          * `numberGreaterThans` (`pulumi.Input[list]`) - Compares a value of an event using a single floating point number.
            * `key` (`pulumi.Input[str]`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
            * `value` (`pulumi.Input[float]`) - Specifies a single value to compare to when using a single value operator.

          * `numberIns` (`pulumi.Input[list]`) - Compares a value of an event using multiple floating point numbers.
            * `key` (`pulumi.Input[str]`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
            * `values` (`pulumi.Input[list]`) - Specifies an array of values to compare to when using a multiple values operator.

          * `numberLessThanOrEquals` (`pulumi.Input[list]`) - Compares a value of an event using a single floating point number.
            * `key` (`pulumi.Input[str]`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
            * `value` (`pulumi.Input[float]`) - Specifies a single value to compare to when using a single value operator.

          * `numberLessThans` (`pulumi.Input[list]`) - Compares a value of an event using a single floating point number.
            * `key` (`pulumi.Input[str]`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
            * `value` (`pulumi.Input[float]`) - Specifies a single value to compare to when using a single value operator.

          * `numberNotIns` (`pulumi.Input[list]`) - Compares a value of an event using multiple floating point numbers.
            * `key` (`pulumi.Input[str]`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
            * `values` (`pulumi.Input[list]`) - Specifies an array of values to compare to when using a multiple values operator.

          * `stringBeginsWiths` (`pulumi.Input[list]`) - Compares a value of an event using multiple string values.
            * `key` (`pulumi.Input[str]`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
            * `values` (`pulumi.Input[list]`) - Specifies an array of values to compare to when using a multiple values operator.

          * `stringContains` (`pulumi.Input[list]`) - Compares a value of an event using multiple string values.
            * `key` (`pulumi.Input[str]`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
            * `values` (`pulumi.Input[list]`) - Specifies an array of values to compare to when using a multiple values operator.

          * `stringEndsWiths` (`pulumi.Input[list]`) - Compares a value of an event using multiple string values.
            * `key` (`pulumi.Input[str]`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
            * `values` (`pulumi.Input[list]`) - Specifies an array of values to compare to when using a multiple values operator.

          * `stringIns` (`pulumi.Input[list]`) - Compares a value of an event using multiple string values.
            * `key` (`pulumi.Input[str]`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
            * `values` (`pulumi.Input[list]`) - Specifies an array of values to compare to when using a multiple values operator.

          * `stringNotIns` (`pulumi.Input[list]`) - Compares a value of an event using multiple string values.
            * `key` (`pulumi.Input[str]`) - Specifies the field within the event data that you want to use for filtering. Type of the field can be a number, boolean, or string.
            * `values` (`pulumi.Input[list]`) - Specifies an array of values to compare to when using a multiple values operator.

        The **azure_function_endpoint** object supports the following:

          * `functionId` (`pulumi.Input[str]`) - Specifies the ID of the Function where the Event Subscription will receive events.
          * `maxEventsPerBatch` (`pulumi.Input[float]`) - Maximum number of events per batch.
          * `preferredBatchSizeInKilobytes` (`pulumi.Input[float]`) - Preferred batch size in Kilobytes.

        The **eventhub_endpoint** object supports the following:

          * `eventhub_id` (`pulumi.Input[str]`) - Specifies the id of the eventhub where the Event Subscription will receive events.

        The **hybrid_connection_endpoint** object supports the following:

          * `hybridConnectionId` (`pulumi.Input[str]`) - Specifies the id of the hybrid connection where the Event Subscription will receive events.

        The **retry_policy** object supports the following:

          * `eventTimeToLive` (`pulumi.Input[float]`) - Specifies the time to live (in minutes) for events.
          * `maxDeliveryAttempts` (`pulumi.Input[float]`) - Specifies the maximum number of delivery retry attempts for events.

        The **storage_blob_dead_letter_destination** object supports the following:

          * `storage_account_id` (`pulumi.Input[str]`) - Specifies the id of the storage account id where the storage blob is located.
          * `storageBlobContainerName` (`pulumi.Input[str]`) - Specifies the name of the Storage blob container that is the destination of the deadletter events.

        The **storage_queue_endpoint** object supports the following:

          * `queue_name` (`pulumi.Input[str]`) - Specifies the name of the storage queue where the Event Subscription will receive events.
          * `storage_account_id` (`pulumi.Input[str]`) - Specifies the id of the storage account id where the storage queue is located.

        The **subject_filter** object supports the following:

          * `caseSensitive` (`pulumi.Input[bool]`) - Specifies if `subject_begins_with` and `subject_ends_with` case sensitive. This value defaults to `false`.
          * `subjectBeginsWith` (`pulumi.Input[str]`) - A string to filter events for an event subscription based on a resource path prefix.
          * `subjectEndsWith` (`pulumi.Input[str]`) - A string to filter events for an event subscription based on a resource path suffix.

        The **webhook_endpoint** object supports the following:

          * `activeDirectoryAppIdOrUri` (`pulumi.Input[str]`) - The Azure Active Directory Application ID or URI to get the access token that will be included as the bearer token in delivery requests.
          * `activeDirectoryTenantId` (`pulumi.Input[str]`) - The Azure Active Directory Tenant ID to get the access token that will be included as the bearer token in delivery requests.
          * `baseUrl` (`pulumi.Input[str]`) - The base url of the webhook where the Event Subscription will receive events.
          * `maxEventsPerBatch` (`pulumi.Input[float]`) - Maximum number of events per batch.
          * `preferredBatchSizeInKilobytes` (`pulumi.Input[float]`) - Preferred batch size in Kilobytes.
          * `url` (`pulumi.Input[str]`) - Specifies the url of the webhook where the Event Subscription will receive events.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["advanced_filter"] = advanced_filter
        __props__["azure_function_endpoint"] = azure_function_endpoint
        __props__["event_delivery_schema"] = event_delivery_schema
        __props__["eventhub_endpoint"] = eventhub_endpoint
        __props__["eventhub_endpoint_id"] = eventhub_endpoint_id
        __props__["expiration_time_utc"] = expiration_time_utc
        __props__["hybrid_connection_endpoint"] = hybrid_connection_endpoint
        __props__["hybrid_connection_endpoint_id"] = hybrid_connection_endpoint_id
        __props__["included_event_types"] = included_event_types
        __props__["labels"] = labels
        __props__["name"] = name
        __props__["retry_policy"] = retry_policy
        __props__["scope"] = scope
        __props__["service_bus_queue_endpoint_id"] = service_bus_queue_endpoint_id
        __props__["service_bus_topic_endpoint_id"] = service_bus_topic_endpoint_id
        __props__["storage_blob_dead_letter_destination"] = storage_blob_dead_letter_destination
        __props__["storage_queue_endpoint"] = storage_queue_endpoint
        __props__["subject_filter"] = subject_filter
        __props__["topic_name"] = topic_name
        __props__["webhook_endpoint"] = webhook_endpoint
        return EventSubscription(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
