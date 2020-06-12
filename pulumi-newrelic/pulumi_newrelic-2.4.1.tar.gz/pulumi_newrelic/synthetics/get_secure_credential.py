# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetSecureCredentialResult:
    """
    A collection of values returned by getSecureCredential.
    """
    def __init__(__self__, created_at=None, description=None, id=None, key=None, last_updated=None):
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        __self__.created_at = created_at
        """
        The time the secure credential was created.
        """
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        __self__.description = description
        """
        The secure credential's description.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if key and not isinstance(key, str):
            raise TypeError("Expected argument 'key' to be a str")
        __self__.key = key
        if last_updated and not isinstance(last_updated, str):
            raise TypeError("Expected argument 'last_updated' to be a str")
        __self__.last_updated = last_updated
        """
        The time the secure credential was last updated.
        """
class AwaitableGetSecureCredentialResult(GetSecureCredentialResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSecureCredentialResult(
            created_at=self.created_at,
            description=self.description,
            id=self.id,
            key=self.key,
            last_updated=self.last_updated)

def get_secure_credential(key=None,opts=None):
    """
    Use this data source to get information about a specific Synthetics secure credential in New Relic that already exists.

    Note that the secure credential's value is not returned as an attribute for security reasons.

    ## Example Usage



    ```python
    import pulumi
    import pulumi_newrelic as newrelic

    foo = newrelic.synthetics.get_secure_credential(key="MY_KEY")
    ```



    :param str key: The secure credential's key name.  Regardless of the case used in the configuration, the provider will provide an upcased key to the underlying API.
    """
    __args__ = dict()


    __args__['key'] = key
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('newrelic:synthetics/getSecureCredential:getSecureCredential', __args__, opts=opts).value

    return AwaitableGetSecureCredentialResult(
        created_at=__ret__.get('createdAt'),
        description=__ret__.get('description'),
        id=__ret__.get('id'),
        key=__ret__.get('key'),
        last_updated=__ret__.get('lastUpdated'))
