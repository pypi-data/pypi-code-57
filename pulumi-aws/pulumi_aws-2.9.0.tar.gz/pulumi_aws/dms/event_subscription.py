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
    arn: pulumi.Output[str]
    enabled: pulumi.Output[bool]
    """
    Whether the event subscription should be enabled.
    """
    event_categories: pulumi.Output[list]
    """
    List of event categories to listen for, see `DescribeEventCategories` for a canonical list.
    """
    name: pulumi.Output[str]
    """
    Name of event subscription.
    """
    sns_topic_arn: pulumi.Output[str]
    """
    SNS topic arn to send events on.
    """
    source_ids: pulumi.Output[list]
    """
    Ids of sources to listen to.
    """
    source_type: pulumi.Output[str]
    """
    Type of source for events. Valid values: `replication-instance` or `replication-task`
    """
    tags: pulumi.Output[dict]
    def __init__(__self__, resource_name, opts=None, enabled=None, event_categories=None, name=None, sns_topic_arn=None, source_ids=None, source_type=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a DMS (Data Migration Service) event subscription resource.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.dms.EventSubscription("example",
            enabled=True,
            event_categories=[
                "creation",
                "failure",
            ],
            sns_topic_arn=aws_sns_topic["example"]["arn"],
            source_ids=[aws_dms_replication_task["example"]["replication_task_id"]],
            source_type="replication-task",
            tags={
                "Name": "example",
            })
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] enabled: Whether the event subscription should be enabled.
        :param pulumi.Input[list] event_categories: List of event categories to listen for, see `DescribeEventCategories` for a canonical list.
        :param pulumi.Input[str] name: Name of event subscription.
        :param pulumi.Input[str] sns_topic_arn: SNS topic arn to send events on.
        :param pulumi.Input[list] source_ids: Ids of sources to listen to.
        :param pulumi.Input[str] source_type: Type of source for events. Valid values: `replication-instance` or `replication-task`
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

            __props__['enabled'] = enabled
            if event_categories is None:
                raise TypeError("Missing required property 'event_categories'")
            __props__['event_categories'] = event_categories
            __props__['name'] = name
            if sns_topic_arn is None:
                raise TypeError("Missing required property 'sns_topic_arn'")
            __props__['sns_topic_arn'] = sns_topic_arn
            __props__['source_ids'] = source_ids
            __props__['source_type'] = source_type
            __props__['tags'] = tags
            __props__['arn'] = None
        super(EventSubscription, __self__).__init__(
            'aws:dms/eventSubscription:EventSubscription',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, arn=None, enabled=None, event_categories=None, name=None, sns_topic_arn=None, source_ids=None, source_type=None, tags=None):
        """
        Get an existing EventSubscription resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] enabled: Whether the event subscription should be enabled.
        :param pulumi.Input[list] event_categories: List of event categories to listen for, see `DescribeEventCategories` for a canonical list.
        :param pulumi.Input[str] name: Name of event subscription.
        :param pulumi.Input[str] sns_topic_arn: SNS topic arn to send events on.
        :param pulumi.Input[list] source_ids: Ids of sources to listen to.
        :param pulumi.Input[str] source_type: Type of source for events. Valid values: `replication-instance` or `replication-task`
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["enabled"] = enabled
        __props__["event_categories"] = event_categories
        __props__["name"] = name
        __props__["sns_topic_arn"] = sns_topic_arn
        __props__["source_ids"] = source_ids
        __props__["source_type"] = source_type
        __props__["tags"] = tags
        return EventSubscription(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

