# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetKeyVaultResult:
    """
    A collection of values returned by getKeyVault.
    """
    def __init__(__self__, access_policies=None, enabled_for_deployment=None, enabled_for_disk_encryption=None, enabled_for_template_deployment=None, id=None, location=None, name=None, network_acls=None, purge_protection_enabled=None, resource_group_name=None, sku_name=None, soft_delete_enabled=None, tags=None, tenant_id=None, vault_uri=None):
        if access_policies and not isinstance(access_policies, list):
            raise TypeError("Expected argument 'access_policies' to be a list")
        __self__.access_policies = access_policies
        """
        One or more `access_policy` blocks as defined below.
        """
        if enabled_for_deployment and not isinstance(enabled_for_deployment, bool):
            raise TypeError("Expected argument 'enabled_for_deployment' to be a bool")
        __self__.enabled_for_deployment = enabled_for_deployment
        """
        Can Azure Virtual Machines retrieve certificates stored as secrets from the Key Vault?
        """
        if enabled_for_disk_encryption and not isinstance(enabled_for_disk_encryption, bool):
            raise TypeError("Expected argument 'enabled_for_disk_encryption' to be a bool")
        __self__.enabled_for_disk_encryption = enabled_for_disk_encryption
        """
        Can Azure Disk Encryption retrieve secrets from the Key Vault?
        """
        if enabled_for_template_deployment and not isinstance(enabled_for_template_deployment, bool):
            raise TypeError("Expected argument 'enabled_for_template_deployment' to be a bool")
        __self__.enabled_for_template_deployment = enabled_for_template_deployment
        """
        Can Azure Resource Manager retrieve secrets from the Key Vault?
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        __self__.location = location
        """
        The Azure Region in which the Key Vault exists.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if network_acls and not isinstance(network_acls, list):
            raise TypeError("Expected argument 'network_acls' to be a list")
        __self__.network_acls = network_acls
        if purge_protection_enabled and not isinstance(purge_protection_enabled, bool):
            raise TypeError("Expected argument 'purge_protection_enabled' to be a bool")
        __self__.purge_protection_enabled = purge_protection_enabled
        """
        Is purge protection enabled on this Key Vault?
        """
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        __self__.resource_group_name = resource_group_name
        if sku_name and not isinstance(sku_name, str):
            raise TypeError("Expected argument 'sku_name' to be a str")
        __self__.sku_name = sku_name
        """
        The Name of the SKU used for this Key Vault.
        """
        if soft_delete_enabled and not isinstance(soft_delete_enabled, bool):
            raise TypeError("Expected argument 'soft_delete_enabled' to be a bool")
        __self__.soft_delete_enabled = soft_delete_enabled
        """
        Is soft delete enabled on this Key Vault?
        """
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags
        """
        A mapping of tags assigned to the Key Vault.
        """
        if tenant_id and not isinstance(tenant_id, str):
            raise TypeError("Expected argument 'tenant_id' to be a str")
        __self__.tenant_id = tenant_id
        """
        The Azure Active Directory Tenant ID used to authenticate requests for this Key Vault.
        """
        if vault_uri and not isinstance(vault_uri, str):
            raise TypeError("Expected argument 'vault_uri' to be a str")
        __self__.vault_uri = vault_uri
        """
        The URI of the vault for performing operations on keys and secrets.
        """
class AwaitableGetKeyVaultResult(GetKeyVaultResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetKeyVaultResult(
            access_policies=self.access_policies,
            enabled_for_deployment=self.enabled_for_deployment,
            enabled_for_disk_encryption=self.enabled_for_disk_encryption,
            enabled_for_template_deployment=self.enabled_for_template_deployment,
            id=self.id,
            location=self.location,
            name=self.name,
            network_acls=self.network_acls,
            purge_protection_enabled=self.purge_protection_enabled,
            resource_group_name=self.resource_group_name,
            sku_name=self.sku_name,
            soft_delete_enabled=self.soft_delete_enabled,
            tags=self.tags,
            tenant_id=self.tenant_id,
            vault_uri=self.vault_uri)

def get_key_vault(name=None,resource_group_name=None,opts=None):
    """
    Use this data source to access information about an existing Key Vault.

    ## Example Usage



    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.keyvault.get_key_vault(name="mykeyvault",
        resource_group_name="some-resource-group")
    pulumi.export("vaultUri", example.vault_uri)
    ```


    :param str name: Specifies the name of the Key Vault.
    :param str resource_group_name: The name of the Resource Group in which the Key Vault exists.
    """
    __args__ = dict()


    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:keyvault/getKeyVault:getKeyVault', __args__, opts=opts).value

    return AwaitableGetKeyVaultResult(
        access_policies=__ret__.get('accessPolicies'),
        enabled_for_deployment=__ret__.get('enabledForDeployment'),
        enabled_for_disk_encryption=__ret__.get('enabledForDiskEncryption'),
        enabled_for_template_deployment=__ret__.get('enabledForTemplateDeployment'),
        id=__ret__.get('id'),
        location=__ret__.get('location'),
        name=__ret__.get('name'),
        network_acls=__ret__.get('networkAcls'),
        purge_protection_enabled=__ret__.get('purgeProtectionEnabled'),
        resource_group_name=__ret__.get('resourceGroupName'),
        sku_name=__ret__.get('skuName'),
        soft_delete_enabled=__ret__.get('softDeleteEnabled'),
        tags=__ret__.get('tags'),
        tenant_id=__ret__.get('tenantId'),
        vault_uri=__ret__.get('vaultUri'))
