# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class User(pulumi.CustomResource):
    arn: pulumi.Output[str]
    """
    The ARN assigned by AWS for this user.
    """
    force_destroy: pulumi.Output[bool]
    """
    When destroying this user, destroy even if it
    has non-provider-managed IAM access keys, login profile or MFA devices. Without `force_destroy`
    a user with non-provider-managed access keys and login profile will fail to be destroyed.
    """
    name: pulumi.Output[str]
    """
    The user's name. The name must consist of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: `=,.@-_.`. User names are not distinguished by case. For example, you cannot create users named both "TESTUSER" and "testuser".
    """
    path: pulumi.Output[str]
    """
    Path in which to create the user.
    """
    permissions_boundary: pulumi.Output[str]
    """
    The ARN of the policy that is used to set the permissions boundary for the user.
    """
    tags: pulumi.Output[dict]
    """
    Key-value mapping of tags for the IAM user
    """
    unique_id: pulumi.Output[str]
    """
    The [unique ID][1] assigned by AWS.
    """
    def __init__(__self__, resource_name, opts=None, force_destroy=None, name=None, path=None, permissions_boundary=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an IAM user.

        > *NOTE:* If policies are attached to the user via the `iam.PolicyAttachment` resource and you are modifying the user `name` or `path`, the `force_destroy` argument must be set to `true` and applied before attempting the operation otherwise you will encounter a `DeleteConflict` error. The `iam.UserPolicyAttachment` resource (recommended) does not have this requirement.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_aws as aws

        lb_user = aws.iam.User("lbUser",
            path="/system/",
            tags={
                "tag-key": "tag-value",
            })
        lb_access_key = aws.iam.AccessKey("lbAccessKey", user=lb_user.name)
        lb_ro = aws.iam.UserPolicy("lbRo",
            policy=\"\"\"{
          "Version": "2012-10-17",
          "Statement": [
            {
              "Action": [
                "ec2:Describe*"
              ],
              "Effect": "Allow",
              "Resource": "*"
            }
          ]
        }

        \"\"\",
            user=lb_user.name)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] force_destroy: When destroying this user, destroy even if it
               has non-provider-managed IAM access keys, login profile or MFA devices. Without `force_destroy`
               a user with non-provider-managed access keys and login profile will fail to be destroyed.
        :param pulumi.Input[str] name: The user's name. The name must consist of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: `=,.@-_.`. User names are not distinguished by case. For example, you cannot create users named both "TESTUSER" and "testuser".
        :param pulumi.Input[str] path: Path in which to create the user.
        :param pulumi.Input[str] permissions_boundary: The ARN of the policy that is used to set the permissions boundary for the user.
        :param pulumi.Input[dict] tags: Key-value mapping of tags for the IAM user
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

            __props__['force_destroy'] = force_destroy
            __props__['name'] = name
            __props__['path'] = path
            __props__['permissions_boundary'] = permissions_boundary
            __props__['tags'] = tags
            __props__['arn'] = None
            __props__['unique_id'] = None
        super(User, __self__).__init__(
            'aws:iam/user:User',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, arn=None, force_destroy=None, name=None, path=None, permissions_boundary=None, tags=None, unique_id=None):
        """
        Get an existing User resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN assigned by AWS for this user.
        :param pulumi.Input[bool] force_destroy: When destroying this user, destroy even if it
               has non-provider-managed IAM access keys, login profile or MFA devices. Without `force_destroy`
               a user with non-provider-managed access keys and login profile will fail to be destroyed.
        :param pulumi.Input[str] name: The user's name. The name must consist of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: `=,.@-_.`. User names are not distinguished by case. For example, you cannot create users named both "TESTUSER" and "testuser".
        :param pulumi.Input[str] path: Path in which to create the user.
        :param pulumi.Input[str] permissions_boundary: The ARN of the policy that is used to set the permissions boundary for the user.
        :param pulumi.Input[dict] tags: Key-value mapping of tags for the IAM user
        :param pulumi.Input[str] unique_id: The [unique ID][1] assigned by AWS.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["force_destroy"] = force_destroy
        __props__["name"] = name
        __props__["path"] = path
        __props__["permissions_boundary"] = permissions_boundary
        __props__["tags"] = tags
        __props__["unique_id"] = unique_id
        return User(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

