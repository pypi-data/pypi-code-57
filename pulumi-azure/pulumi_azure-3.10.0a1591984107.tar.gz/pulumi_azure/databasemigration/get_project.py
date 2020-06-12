# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetProjectResult:
    """
    A collection of values returned by getProject.
    """
    def __init__(__self__, id=None, location=None, name=None, resource_group_name=None, service_name=None, source_platform=None, tags=None, target_platform=None):
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
        Azure location where the resource exists.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        __self__.resource_group_name = resource_group_name
        if service_name and not isinstance(service_name, str):
            raise TypeError("Expected argument 'service_name' to be a str")
        __self__.service_name = service_name
        if source_platform and not isinstance(source_platform, str):
            raise TypeError("Expected argument 'source_platform' to be a str")
        __self__.source_platform = source_platform
        """
        The platform type of the migration source.
        """
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags
        """
        A mapping of tags to assigned to the resource.
        """
        if target_platform and not isinstance(target_platform, str):
            raise TypeError("Expected argument 'target_platform' to be a str")
        __self__.target_platform = target_platform
        """
        The platform type of the migration target.
        """
class AwaitableGetProjectResult(GetProjectResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProjectResult(
            id=self.id,
            location=self.location,
            name=self.name,
            resource_group_name=self.resource_group_name,
            service_name=self.service_name,
            source_platform=self.source_platform,
            tags=self.tags,
            target_platform=self.target_platform)

def get_project(name=None,resource_group_name=None,service_name=None,opts=None):
    """
    Use this data source to access information about an existing Database Migration Project.

    ## Example Usage



    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.databasemigration.get_project(name="example-dbms-project",
        resource_group_name="example-rg",
        service_name="example-dbms")
    pulumi.export("name", example.name)
    ```


    :param str name: Name of the database migration project.
    :param str resource_group_name: Name of the resource group where resource belongs to.
    :param str service_name: Name of the database migration service where resource belongs to.
    """
    __args__ = dict()


    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __args__['serviceName'] = service_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:databasemigration/getProject:getProject', __args__, opts=opts).value

    return AwaitableGetProjectResult(
        id=__ret__.get('id'),
        location=__ret__.get('location'),
        name=__ret__.get('name'),
        resource_group_name=__ret__.get('resourceGroupName'),
        service_name=__ret__.get('serviceName'),
        source_platform=__ret__.get('sourcePlatform'),
        tags=__ret__.get('tags'),
        target_platform=__ret__.get('targetPlatform'))
