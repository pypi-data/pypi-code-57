# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class GetAuditingResult:
    """
    A collection of values returned by getAuditing.
    """
    def __init__(__self__, audit_authorization_success=None, audit_filter=None, configuration_type=None, enabled=None, id=None, project_id=None):
        if audit_authorization_success and not isinstance(audit_authorization_success, bool):
            raise TypeError("Expected argument 'audit_authorization_success' to be a bool")
        __self__.audit_authorization_success = audit_authorization_success
        """
        JSON-formatted audit filter used by the project
        """
        if audit_filter and not isinstance(audit_filter, str):
            raise TypeError("Expected argument 'audit_filter' to be a str")
        __self__.audit_filter = audit_filter
        """
        Indicates whether the auditing system captures successful authentication attempts for audit filters using the "atype" : "authCheck" auditing event. For more information, see auditAuthorizationSuccess
        """
        if configuration_type and not isinstance(configuration_type, str):
            raise TypeError("Expected argument 'configuration_type' to be a str")
        __self__.configuration_type = configuration_type
        """
        Denotes the configuration method for the audit filter. Possible values are: NONE - auditing not configured for the project.m FILTER_BUILDER - auditing configured via Atlas UI filter builderm FILTER_JSON - auditing configured via Atlas custom filter or API.
        """
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        __self__.enabled = enabled
        """
        Denotes whether or not the project associated with the {GROUP-ID} has database auditing enabled.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if project_id and not isinstance(project_id, str):
            raise TypeError("Expected argument 'project_id' to be a str")
        __self__.project_id = project_id
class AwaitableGetAuditingResult(GetAuditingResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAuditingResult(
            audit_authorization_success=self.audit_authorization_success,
            audit_filter=self.audit_filter,
            configuration_type=self.configuration_type,
            enabled=self.enabled,
            id=self.id,
            project_id=self.project_id)

def get_auditing(project_id=None,opts=None):
    """
    `.Auditing` describes a Auditing.

    > **NOTE:** Groups and projects are synonymous terms. You may find **group_id** in the official documentation.





    :param str project_id: The unique ID for the project to create the database user.
    """
    __args__ = dict()


    __args__['projectId'] = project_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('mongodbatlas:index/getAuditing:getAuditing', __args__, opts=opts).value

    return AwaitableGetAuditingResult(
        audit_authorization_success=__ret__.get('auditAuthorizationSuccess'),
        audit_filter=__ret__.get('auditFilter'),
        configuration_type=__ret__.get('configurationType'),
        enabled=__ret__.get('enabled'),
        id=__ret__.get('id'),
        project_id=__ret__.get('projectId'))
