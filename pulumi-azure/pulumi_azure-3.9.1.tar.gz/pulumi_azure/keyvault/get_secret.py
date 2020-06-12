# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetSecretResult:
    """
    A collection of values returned by getSecret.
    """
    def __init__(__self__, content_type=None, id=None, key_vault_id=None, name=None, tags=None, value=None, version=None):
        if content_type and not isinstance(content_type, str):
            raise TypeError("Expected argument 'content_type' to be a str")
        __self__.content_type = content_type
        """
        The content type for the Key Vault Secret.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if key_vault_id and not isinstance(key_vault_id, str):
            raise TypeError("Expected argument 'key_vault_id' to be a str")
        __self__.key_vault_id = key_vault_id
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags
        """
        Any tags assigned to this resource.
        """
        if value and not isinstance(value, str):
            raise TypeError("Expected argument 'value' to be a str")
        __self__.value = value
        """
        The value of the Key Vault Secret.
        """
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        __self__.version = version
        """
        The current version of the Key Vault Secret.
        """
class AwaitableGetSecretResult(GetSecretResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSecretResult(
            content_type=self.content_type,
            id=self.id,
            key_vault_id=self.key_vault_id,
            name=self.name,
            tags=self.tags,
            value=self.value,
            version=self.version)

def get_secret(key_vault_id=None,name=None,opts=None):
    """
    Use this data source to access information about an existing Key Vault Secret.

    ## Example Usage



    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.keyvault.get_secret(name="secret-sauce",
        key_vault_id=data["azurerm_key_vault"]["existing"]["id"])
    pulumi.export("secretValue", example.value)
    ```


    :param str key_vault_id: Specifies the ID of the Key Vault instance where the Secret resides, available on the `keyvault.KeyVault` Data Source / Resource.
    :param str name: Specifies the name of the Key Vault Secret.
    """
    __args__ = dict()


    __args__['keyVaultId'] = key_vault_id
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:keyvault/getSecret:getSecret', __args__, opts=opts).value

    return AwaitableGetSecretResult(
        content_type=__ret__.get('contentType'),
        id=__ret__.get('id'),
        key_vault_id=__ret__.get('keyVaultId'),
        name=__ret__.get('name'),
        tags=__ret__.get('tags'),
        value=__ret__.get('value'),
        version=__ret__.get('version'))
