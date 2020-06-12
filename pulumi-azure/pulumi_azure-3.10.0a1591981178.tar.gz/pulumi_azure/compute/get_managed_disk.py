# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetManagedDiskResult:
    """
    A collection of values returned by getManagedDisk.
    """
    def __init__(__self__, create_option=None, disk_encryption_set_id=None, disk_iops_read_write=None, disk_mbps_read_write=None, disk_size_gb=None, id=None, name=None, os_type=None, resource_group_name=None, source_resource_id=None, source_uri=None, storage_account_id=None, storage_account_type=None, tags=None, zones=None):
        if create_option and not isinstance(create_option, str):
            raise TypeError("Expected argument 'create_option' to be a str")
        __self__.create_option = create_option
        if disk_encryption_set_id and not isinstance(disk_encryption_set_id, str):
            raise TypeError("Expected argument 'disk_encryption_set_id' to be a str")
        __self__.disk_encryption_set_id = disk_encryption_set_id
        """
        The ID of the Disk Encryption Set used to encrypt this Managed Disk.
        """
        if disk_iops_read_write and not isinstance(disk_iops_read_write, float):
            raise TypeError("Expected argument 'disk_iops_read_write' to be a float")
        __self__.disk_iops_read_write = disk_iops_read_write
        """
        The number of IOPS allowed for this disk, where one operation can transfer between 4k and 256k bytes.
        """
        if disk_mbps_read_write and not isinstance(disk_mbps_read_write, float):
            raise TypeError("Expected argument 'disk_mbps_read_write' to be a float")
        __self__.disk_mbps_read_write = disk_mbps_read_write
        """
        The bandwidth allowed for this disk.
        """
        if disk_size_gb and not isinstance(disk_size_gb, float):
            raise TypeError("Expected argument 'disk_size_gb' to be a float")
        __self__.disk_size_gb = disk_size_gb
        """
        The size of the Managed Disk in gigabytes.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if os_type and not isinstance(os_type, str):
            raise TypeError("Expected argument 'os_type' to be a str")
        __self__.os_type = os_type
        """
        The operating system used for this Managed Disk.
        """
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        __self__.resource_group_name = resource_group_name
        if source_resource_id and not isinstance(source_resource_id, str):
            raise TypeError("Expected argument 'source_resource_id' to be a str")
        __self__.source_resource_id = source_resource_id
        """
        The ID of an existing Managed Disk which this Disk was created from.
        """
        if source_uri and not isinstance(source_uri, str):
            raise TypeError("Expected argument 'source_uri' to be a str")
        __self__.source_uri = source_uri
        """
        The Source URI for this Managed Disk.
        """
        if storage_account_id and not isinstance(storage_account_id, str):
            raise TypeError("Expected argument 'storage_account_id' to be a str")
        __self__.storage_account_id = storage_account_id
        """
        The ID of the Storage Account where the `source_uri` is located.
        """
        if storage_account_type and not isinstance(storage_account_type, str):
            raise TypeError("Expected argument 'storage_account_type' to be a str")
        __self__.storage_account_type = storage_account_type
        """
        The storage account type for the Managed Disk.
        """
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags
        """
        A mapping of tags assigned to the resource.
        """
        if zones and not isinstance(zones, list):
            raise TypeError("Expected argument 'zones' to be a list")
        __self__.zones = zones
        """
        A list of Availability Zones where the Managed Disk exists.
        """
class AwaitableGetManagedDiskResult(GetManagedDiskResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetManagedDiskResult(
            create_option=self.create_option,
            disk_encryption_set_id=self.disk_encryption_set_id,
            disk_iops_read_write=self.disk_iops_read_write,
            disk_mbps_read_write=self.disk_mbps_read_write,
            disk_size_gb=self.disk_size_gb,
            id=self.id,
            name=self.name,
            os_type=self.os_type,
            resource_group_name=self.resource_group_name,
            source_resource_id=self.source_resource_id,
            source_uri=self.source_uri,
            storage_account_id=self.storage_account_id,
            storage_account_type=self.storage_account_type,
            tags=self.tags,
            zones=self.zones)

def get_managed_disk(name=None,resource_group_name=None,tags=None,zones=None,opts=None):
    """
    Use this data source to access information about an existing Managed Disk.

    ## Example Usage



    ```python
    import pulumi
    import pulumi_azure as azure

    existing = azure.compute.get_managed_disk(name="example-datadisk",
        resource_group_name="example-resources")
    pulumi.export("id", existing.id)
    ```


    :param str name: Specifies the name of the Managed Disk.
    :param str resource_group_name: Specifies the name of the Resource Group where this Managed Disk exists.
    :param dict tags: A mapping of tags assigned to the resource.
    :param list zones: A list of Availability Zones where the Managed Disk exists.
    """
    __args__ = dict()


    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __args__['tags'] = tags
    __args__['zones'] = zones
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:compute/getManagedDisk:getManagedDisk', __args__, opts=opts).value

    return AwaitableGetManagedDiskResult(
        create_option=__ret__.get('createOption'),
        disk_encryption_set_id=__ret__.get('diskEncryptionSetId'),
        disk_iops_read_write=__ret__.get('diskIopsReadWrite'),
        disk_mbps_read_write=__ret__.get('diskMbpsReadWrite'),
        disk_size_gb=__ret__.get('diskSizeGb'),
        id=__ret__.get('id'),
        name=__ret__.get('name'),
        os_type=__ret__.get('osType'),
        resource_group_name=__ret__.get('resourceGroupName'),
        source_resource_id=__ret__.get('sourceResourceId'),
        source_uri=__ret__.get('sourceUri'),
        storage_account_id=__ret__.get('storageAccountId'),
        storage_account_type=__ret__.get('storageAccountType'),
        tags=__ret__.get('tags'),
        zones=__ret__.get('zones'))
