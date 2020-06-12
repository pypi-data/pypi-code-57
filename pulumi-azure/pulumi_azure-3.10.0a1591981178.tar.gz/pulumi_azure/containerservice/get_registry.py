# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetRegistryResult:
    """
    A collection of values returned by getRegistry.
    """
    def __init__(__self__, admin_enabled=None, admin_password=None, admin_username=None, id=None, location=None, login_server=None, name=None, resource_group_name=None, sku=None, storage_account_id=None, tags=None):
        if admin_enabled and not isinstance(admin_enabled, bool):
            raise TypeError("Expected argument 'admin_enabled' to be a bool")
        __self__.admin_enabled = admin_enabled
        """
        Is the Administrator account enabled for this Container Registry.
        """
        if admin_password and not isinstance(admin_password, str):
            raise TypeError("Expected argument 'admin_password' to be a str")
        __self__.admin_password = admin_password
        """
        The Password associated with the Container Registry Admin account - if the admin account is enabled.
        """
        if admin_username and not isinstance(admin_username, str):
            raise TypeError("Expected argument 'admin_username' to be a str")
        __self__.admin_username = admin_username
        """
        The Username associated with the Container Registry Admin account - if the admin account is enabled.
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
        The Azure Region in which this Container Registry exists.
        """
        if login_server and not isinstance(login_server, str):
            raise TypeError("Expected argument 'login_server' to be a str")
        __self__.login_server = login_server
        """
        The URL that can be used to log into the container registry.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        __self__.resource_group_name = resource_group_name
        if sku and not isinstance(sku, str):
            raise TypeError("Expected argument 'sku' to be a str")
        __self__.sku = sku
        """
        The SKU of this Container Registry, such as `Basic`.
        """
        if storage_account_id and not isinstance(storage_account_id, str):
            raise TypeError("Expected argument 'storage_account_id' to be a str")
        __self__.storage_account_id = storage_account_id
        """
        The ID of the Storage Account used for this Container Registry. This is only returned for `Classic` SKU's.
        """
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags
        """
        A map of tags assigned to the Container Registry.
        """
class AwaitableGetRegistryResult(GetRegistryResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRegistryResult(
            admin_enabled=self.admin_enabled,
            admin_password=self.admin_password,
            admin_username=self.admin_username,
            id=self.id,
            location=self.location,
            login_server=self.login_server,
            name=self.name,
            resource_group_name=self.resource_group_name,
            sku=self.sku,
            storage_account_id=self.storage_account_id,
            tags=self.tags)

def get_registry(name=None,resource_group_name=None,opts=None):
    """
    Use this data source to access information about an existing Container Registry.

    ## Example Usage



    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.containerservice.get_registry(name="testacr",
        resource_group_name="test")
    pulumi.export("loginServer", example.login_server)
    ```


    :param str name: The name of the Container Registry.
    :param str resource_group_name: The Name of the Resource Group where this Container Registry exists.
    """
    __args__ = dict()


    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:containerservice/getRegistry:getRegistry', __args__, opts=opts).value

    return AwaitableGetRegistryResult(
        admin_enabled=__ret__.get('adminEnabled'),
        admin_password=__ret__.get('adminPassword'),
        admin_username=__ret__.get('adminUsername'),
        id=__ret__.get('id'),
        location=__ret__.get('location'),
        login_server=__ret__.get('loginServer'),
        name=__ret__.get('name'),
        resource_group_name=__ret__.get('resourceGroupName'),
        sku=__ret__.get('sku'),
        storage_account_id=__ret__.get('storageAccountId'),
        tags=__ret__.get('tags'))
