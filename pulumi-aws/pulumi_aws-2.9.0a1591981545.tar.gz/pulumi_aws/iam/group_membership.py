# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GroupMembership(pulumi.CustomResource):
    group: pulumi.Output[str]
    """
    The IAM Group name to attach the list of `users` to
    """
    name: pulumi.Output[str]
    """
    The name to identify the Group Membership
    """
    users: pulumi.Output[list]
    """
    A list of IAM User names to associate with the Group
    """
    def __init__(__self__, resource_name, opts=None, group=None, name=None, users=None, __props__=None, __name__=None, __opts__=None):
        """
        > **WARNING:** Multiple iam.GroupMembership resources with the same group name will produce inconsistent behavior!

        Provides a top level resource to manage IAM Group membership for IAM Users. For
        more information on managing IAM Groups or IAM Users, see [IAM Groups](https://www.terraform.io/docs/providers/aws/r/iam_group.html) or
        [IAM Users](https://www.terraform.io/docs/providers/aws/r/iam_user.html)

        > **Note:** `iam.GroupMembership` will conflict with itself if used more than once with the same group. To non-exclusively manage the users in a group, see the
        [`iam.UserGroupMembership` resource][3].

        ## Example Usage



        ```python
        import pulumi
        import pulumi_aws as aws

        group = aws.iam.Group("group")
        user_one = aws.iam.User("userOne")
        user_two = aws.iam.User("userTwo")
        team = aws.iam.GroupMembership("team",
            group=group.name,
            users=[
                user_one.name,
                user_two.name,
            ])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] group: The IAM Group name to attach the list of `users` to
        :param pulumi.Input[str] name: The name to identify the Group Membership
        :param pulumi.Input[list] users: A list of IAM User names to associate with the Group
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

            if group is None:
                raise TypeError("Missing required property 'group'")
            __props__['group'] = group
            __props__['name'] = name
            if users is None:
                raise TypeError("Missing required property 'users'")
            __props__['users'] = users
        super(GroupMembership, __self__).__init__(
            'aws:iam/groupMembership:GroupMembership',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, group=None, name=None, users=None):
        """
        Get an existing GroupMembership resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] group: The IAM Group name to attach the list of `users` to
        :param pulumi.Input[str] name: The name to identify the Group Membership
        :param pulumi.Input[list] users: A list of IAM User names to associate with the Group
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["group"] = group
        __props__["name"] = name
        __props__["users"] = users
        return GroupMembership(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

