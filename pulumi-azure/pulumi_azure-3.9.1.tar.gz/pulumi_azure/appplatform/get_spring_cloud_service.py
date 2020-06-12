# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetSpringCloudServiceResult:
    """
    A collection of values returned by getSpringCloudService.
    """
    def __init__(__self__, config_server_git_settings=None, id=None, location=None, name=None, resource_group_name=None, tags=None):
        if config_server_git_settings and not isinstance(config_server_git_settings, list):
            raise TypeError("Expected argument 'config_server_git_settings' to be a list")
        __self__.config_server_git_settings = config_server_git_settings
        """
        A `config_server_git_setting` block as defined below.
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
        The location of Spring Cloud Service.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        """
        The name to identify on the Git repository.
        """
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        __self__.resource_group_name = resource_group_name
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags
        """
        A mapping of tags assigned to Spring Cloud Service.
        """
class AwaitableGetSpringCloudServiceResult(GetSpringCloudServiceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSpringCloudServiceResult(
            config_server_git_settings=self.config_server_git_settings,
            id=self.id,
            location=self.location,
            name=self.name,
            resource_group_name=self.resource_group_name,
            tags=self.tags)

def get_spring_cloud_service(name=None,resource_group_name=None,opts=None):
    """
    Use this data source to access information about an existing Spring Cloud Service.

    ## Example Usage



    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.appplatform.get_spring_cloud_service(name=azurerm_spring_cloud_service["example"]["name"],
        resource_group_name=azurerm_spring_cloud_service["example"]["resource_group_name"])
    pulumi.export("springCloudServiceId", example.id)
    ```


    :param str name: Specifies The name of the Spring Cloud Service resource.
    :param str resource_group_name: Specifies the name of the Resource Group where the Spring Cloud Service exists.
    """
    __args__ = dict()


    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:appplatform/getSpringCloudService:getSpringCloudService', __args__, opts=opts).value

    return AwaitableGetSpringCloudServiceResult(
        config_server_git_settings=__ret__.get('configServerGitSettings'),
        id=__ret__.get('id'),
        location=__ret__.get('location'),
        name=__ret__.get('name'),
        resource_group_name=__ret__.get('resourceGroupName'),
        tags=__ret__.get('tags'))
