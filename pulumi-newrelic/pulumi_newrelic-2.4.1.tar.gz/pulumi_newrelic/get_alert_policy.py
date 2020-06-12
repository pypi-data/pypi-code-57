# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class GetAlertPolicyResult:
    """
    A collection of values returned by getAlertPolicy.
    """
    def __init__(__self__, created_at=None, id=None, incident_preference=None, name=None, updated_at=None):
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        __self__.created_at = created_at
        """
        The time the policy was created.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if incident_preference and not isinstance(incident_preference, str):
            raise TypeError("Expected argument 'incident_preference' to be a str")
        __self__.incident_preference = incident_preference
        """
        The rollup strategy for the policy. Options include: PER_POLICY, PER_CONDITION, or PER_CONDITION_AND_TARGET. The default is PER_POLICY.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if updated_at and not isinstance(updated_at, str):
            raise TypeError("Expected argument 'updated_at' to be a str")
        __self__.updated_at = updated_at
        """
        The time the policy was last updated.
        """
class AwaitableGetAlertPolicyResult(GetAlertPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAlertPolicyResult(
            created_at=self.created_at,
            id=self.id,
            incident_preference=self.incident_preference,
            name=self.name,
            updated_at=self.updated_at)

def get_alert_policy(incident_preference=None,name=None,opts=None):
    """
    Use this data source to access information about an existing resource.

    :param str incident_preference: The rollup strategy for the policy. Options include: PER_POLICY, PER_CONDITION, or PER_CONDITION_AND_TARGET. The default is PER_POLICY.
    :param str name: The name of the alert policy in New Relic.
    """
    __args__ = dict()


    __args__['incidentPreference'] = incident_preference
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('newrelic:index/getAlertPolicy:getAlertPolicy', __args__, opts=opts).value

    return AwaitableGetAlertPolicyResult(
        created_at=__ret__.get('createdAt'),
        id=__ret__.get('id'),
        incident_preference=__ret__.get('incidentPreference'),
        name=__ret__.get('name'),
        updated_at=__ret__.get('updatedAt'))
