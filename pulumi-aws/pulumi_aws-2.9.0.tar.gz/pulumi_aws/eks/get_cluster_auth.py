# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetClusterAuthResult:
    """
    A collection of values returned by getClusterAuth.
    """
    def __init__(__self__, id=None, name=None, token=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if token and not isinstance(token, str):
            raise TypeError("Expected argument 'token' to be a str")
        __self__.token = token
        """
        The token to use to authenticate with the cluster.
        """
class AwaitableGetClusterAuthResult(GetClusterAuthResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetClusterAuthResult(
            id=self.id,
            name=self.name,
            token=self.token)

def get_cluster_auth(name=None,opts=None):
    """
    Get an authentication token to communicate with an EKS cluster.

    Uses IAM credentials from the AWS provider to generate a temporary token that is compatible with
    [AWS IAM Authenticator](https://github.com/kubernetes-sigs/aws-iam-authenticator) authentication.
    This can be used to authenticate to an EKS cluster or to a cluster that has the AWS IAM Authenticator
    server configured.


    :param str name: The name of the cluster
    """
    __args__ = dict()


    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:eks/getClusterAuth:getClusterAuth', __args__, opts=opts).value

    return AwaitableGetClusterAuthResult(
        id=__ret__.get('id'),
        name=__ret__.get('name'),
        token=__ret__.get('token'))
