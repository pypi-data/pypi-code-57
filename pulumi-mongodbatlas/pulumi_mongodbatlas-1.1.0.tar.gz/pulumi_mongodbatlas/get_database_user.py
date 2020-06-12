# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class GetDatabaseUserResult:
    """
    A collection of values returned by getDatabaseUser.
    """
    def __init__(__self__, auth_database_name=None, database_name=None, id=None, labels=None, project_id=None, roles=None, username=None, x509_type=None):
        if auth_database_name and not isinstance(auth_database_name, str):
            raise TypeError("Expected argument 'auth_database_name' to be a str")
        __self__.auth_database_name = auth_database_name
        if database_name and not isinstance(database_name, str):
            raise TypeError("Expected argument 'database_name' to be a str")
        if database_name is not None:
            warnings.warn("use auth_database_name instead", DeprecationWarning)
            pulumi.log.warn("database_name is deprecated: use auth_database_name instead")
        __self__.database_name = database_name
        """
        Database on which the user has the specified role. A role on the `admin` database can include privileges that apply to the other databases.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if labels and not isinstance(labels, list):
            raise TypeError("Expected argument 'labels' to be a list")
        __self__.labels = labels
        if project_id and not isinstance(project_id, str):
            raise TypeError("Expected argument 'project_id' to be a str")
        __self__.project_id = project_id
        if roles and not isinstance(roles, list):
            raise TypeError("Expected argument 'roles' to be a list")
        __self__.roles = roles
        """
        List of user’s roles and the databases / collections on which the roles apply. A role allows the user to perform particular actions on the specified database. A role on the admin database can include privileges that apply to the other databases as well. See Roles below for more details.
        """
        if username and not isinstance(username, str):
            raise TypeError("Expected argument 'username' to be a str")
        __self__.username = username
        if x509_type and not isinstance(x509_type, str):
            raise TypeError("Expected argument 'x509_type' to be a str")
        __self__.x509_type = x509_type
        """
        X.509 method by which the provided username is authenticated.
        """
class AwaitableGetDatabaseUserResult(GetDatabaseUserResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDatabaseUserResult(
            auth_database_name=self.auth_database_name,
            database_name=self.database_name,
            id=self.id,
            labels=self.labels,
            project_id=self.project_id,
            roles=self.roles,
            username=self.username,
            x509_type=self.x509_type)

def get_database_user(auth_database_name=None,database_name=None,project_id=None,username=None,opts=None):
    """
    `.DatabaseUser` describe a Database User. This represents a database user which will be applied to all clusters within the project.

    Each user has a set of roles that provide access to the project’s databases. User's roles apply to all the clusters in the project: if two clusters have a `products` database and a user has a role granting `read` access on the products database, the user has that access on both clusters.

    > **NOTE:** Groups and projects are synonymous terms. You may find group_id in the official documentation.




    :param str auth_database_name: The user’s authentication database. A user must provide both a username and authentication database to log into MongoDB. In Atlas deployments of MongoDB, the authentication database is almost always the admin database, for X509 it is $external.
    :param str database_name: Database on which the user has the specified role. A role on the `admin` database can include privileges that apply to the other databases.
    :param str project_id: The unique ID for the project to create the database user.
    :param str username: Username for authenticating to MongoDB.
    """
    __args__ = dict()


    __args__['authDatabaseName'] = auth_database_name
    __args__['databaseName'] = database_name
    __args__['projectId'] = project_id
    __args__['username'] = username
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('mongodbatlas:index/getDatabaseUser:getDatabaseUser', __args__, opts=opts).value

    return AwaitableGetDatabaseUserResult(
        auth_database_name=__ret__.get('authDatabaseName'),
        database_name=__ret__.get('databaseName'),
        id=__ret__.get('id'),
        labels=__ret__.get('labels'),
        project_id=__ret__.get('projectId'),
        roles=__ret__.get('roles'),
        username=__ret__.get('username'),
        x509_type=__ret__.get('x509Type'))
