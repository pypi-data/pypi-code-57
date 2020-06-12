# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetVaultResult:
    """
    A collection of values returned by getVault.
    """
    def __init__(__self__, arn=None, id=None, kms_key_arn=None, name=None, recovery_points=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        __self__.arn = arn
        """
        The ARN of the vault.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if kms_key_arn and not isinstance(kms_key_arn, str):
            raise TypeError("Expected argument 'kms_key_arn' to be a str")
        __self__.kms_key_arn = kms_key_arn
        """
        The server-side encryption key that is used to protect your backups.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if recovery_points and not isinstance(recovery_points, float):
            raise TypeError("Expected argument 'recovery_points' to be a float")
        __self__.recovery_points = recovery_points
        """
        The number of recovery points that are stored in a backup vault.
        """
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags
        """
        Metadata that you can assign to help organize the resources that you create.
        """
class AwaitableGetVaultResult(GetVaultResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVaultResult(
            arn=self.arn,
            id=self.id,
            kms_key_arn=self.kms_key_arn,
            name=self.name,
            recovery_points=self.recovery_points,
            tags=self.tags)

def get_vault(name=None,tags=None,opts=None):
    """
    Use this data source to get information on an existing backup vault.

    ## Example Usage



    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.backup.get_vault(name="example_backup_vault")
    ```


    :param str name: The name of the backup vault.
    :param dict tags: Metadata that you can assign to help organize the resources that you create.
    """
    __args__ = dict()


    __args__['name'] = name
    __args__['tags'] = tags
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:backup/getVault:getVault', __args__, opts=opts).value

    return AwaitableGetVaultResult(
        arn=__ret__.get('arn'),
        id=__ret__.get('id'),
        kms_key_arn=__ret__.get('kmsKeyArn'),
        name=__ret__.get('name'),
        recovery_points=__ret__.get('recoveryPoints'),
        tags=__ret__.get('tags'))
