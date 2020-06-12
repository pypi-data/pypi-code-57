# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

warnings.warn("azure.eventhub.EventHubConsumerGroup has been deprecated in favor of azure.eventhub.ConsumerGroup", DeprecationWarning)

class EventHubConsumerGroup(pulumi.CustomResource):
    eventhub_name: pulumi.Output[str]
    """
    Specifies the name of the EventHub. Changing this forces a new resource to be created.
    """
    name: pulumi.Output[str]
    """
    Specifies the name of the EventHub Consumer Group resource. Changing this forces a new resource to be created.
    """
    namespace_name: pulumi.Output[str]
    """
    Specifies the name of the grandparent EventHub Namespace. Changing this forces a new resource to be created.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group in which the EventHub Consumer Group's grandparent Namespace exists. Changing this forces a new resource to be created.
    """
    user_metadata: pulumi.Output[str]
    """
    Specifies the user metadata.
    """
    warnings.warn("azure.eventhub.EventHubConsumerGroup has been deprecated in favor of azure.eventhub.ConsumerGroup", DeprecationWarning)
    def __init__(__self__, resource_name, opts=None, eventhub_name=None, name=None, namespace_name=None, resource_group_name=None, user_metadata=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages a Event Hubs Consumer Group as a nested resource within an Event Hub.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West US")
        example_event_hub_namespace = azure.eventhub.EventHubNamespace("exampleEventHubNamespace",
            location="West US",
            resource_group_name=example_resource_group.name,
            sku="Basic",
            capacity=2,
            tags={
                "environment": "Production",
            })
        example_event_hub = azure.eventhub.EventHub("exampleEventHub",
            namespace_name=example_event_hub_namespace.name,
            resource_group_name=example_resource_group.name,
            partition_count=2,
            message_retention=2)
        example_consumer_group = azure.eventhub.ConsumerGroup("exampleConsumerGroup",
            namespace_name=example_event_hub_namespace.name,
            eventhub_name=example_event_hub.name,
            resource_group_name=example_resource_group.name,
            user_metadata="some-meta-data")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] eventhub_name: Specifies the name of the EventHub. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the EventHub Consumer Group resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] namespace_name: Specifies the name of the grandparent EventHub Namespace. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which the EventHub Consumer Group's grandparent Namespace exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] user_metadata: Specifies the user metadata.
        """
        pulumi.log.warn("EventHubConsumerGroup is deprecated: azure.eventhub.EventHubConsumerGroup has been deprecated in favor of azure.eventhub.ConsumerGroup")
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

            if eventhub_name is None:
                raise TypeError("Missing required property 'eventhub_name'")
            __props__['eventhub_name'] = eventhub_name
            __props__['name'] = name
            if namespace_name is None:
                raise TypeError("Missing required property 'namespace_name'")
            __props__['namespace_name'] = namespace_name
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['user_metadata'] = user_metadata
        super(EventHubConsumerGroup, __self__).__init__(
            'azure:eventhub/eventHubConsumerGroup:EventHubConsumerGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, eventhub_name=None, name=None, namespace_name=None, resource_group_name=None, user_metadata=None):
        """
        Get an existing EventHubConsumerGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] eventhub_name: Specifies the name of the EventHub. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the EventHub Consumer Group resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] namespace_name: Specifies the name of the grandparent EventHub Namespace. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which the EventHub Consumer Group's grandparent Namespace exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] user_metadata: Specifies the user metadata.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["eventhub_name"] = eventhub_name
        __props__["name"] = name
        __props__["namespace_name"] = namespace_name
        __props__["resource_group_name"] = resource_group_name
        __props__["user_metadata"] = user_metadata
        return EventHubConsumerGroup(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
