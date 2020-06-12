# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class PrivateEndpointInterfaceLink(pulumi.CustomResource):
    connection_status: pulumi.Output[str]
    """
    Status of the interface endpoint.
    Returns one of the following values:
    """
    delete_requested: pulumi.Output[bool]
    """
    Indicates if Atlas received a request to remove the interface endpoint from the private endpoint connection.
    """
    error_message: pulumi.Output[str]
    """
    Error message pertaining to the interface endpoint. Returns null if there are no errors.
    """
    interface_endpoint_id: pulumi.Output[str]
    """
    Unique identifier of the interface endpoint you created in your VPC with the AWS resource.
    """
    private_link_id: pulumi.Output[str]
    """
    Unique identifier of the AWS PrivateLink connection which is created by `.PrivateEndpoint` resource.
    """
    project_id: pulumi.Output[str]
    """
    Unique identifier for the project.
    """
    def __init__(__self__, resource_name, opts=None, interface_endpoint_id=None, private_link_id=None, project_id=None, __props__=None, __name__=None, __opts__=None):
        """
        `.PrivateEndpointInterfaceLink` provides a Private Endpoint Interface Link resource. This represents a Private Endpoint Interface Link, which adds one interface endpoint to a private endpoint connection in an Atlas project.

        > **IMPORTANT:**You must have one of the following roles to successfully handle the resource:
          * Organization Owner
          * Project Owner

        > **NOTE:** Groups and projects are synonymous terms. You may find group_id in the official documentation.


        ## Example Usage



        ```python
        import pulumi
        import pulumi_aws as aws
        import pulumi_mongodbatlas as mongodbatlas

        test_private_endpoint = mongodbatlas.PrivateEndpoint("testPrivateEndpoint",
            project_id="<PROJECT_ID>",
            provider_name="AWS",
            region="us-east-1")
        ptfe_service = aws.ec2.VpcEndpoint("ptfeService",
            security_group_ids=["sg-3f238186"],
            service_name=test_private_endpoint.endpoint_service_name,
            subnet_ids=["subnet-de0406d2"],
            vpc_endpoint_type="Interface",
            vpc_id="vpc-7fc0a543")
        test_private_endpoint_interface_link = mongodbatlas.PrivateEndpointInterfaceLink("testPrivateEndpointInterfaceLink",
            interface_endpoint_id=ptfe_service.id,
            private_link_id=test_private_endpoint.private_link_id,
            project_id=test_private_endpoint.project_id)
        ```


        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] interface_endpoint_id: Unique identifier of the interface endpoint you created in your VPC with the AWS resource.
        :param pulumi.Input[str] private_link_id: Unique identifier of the AWS PrivateLink connection which is created by `.PrivateEndpoint` resource.
        :param pulumi.Input[str] project_id: Unique identifier for the project.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            if interface_endpoint_id is None:
                raise TypeError("Missing required property 'interface_endpoint_id'")
            __props__['interface_endpoint_id'] = interface_endpoint_id
            if private_link_id is None:
                raise TypeError("Missing required property 'private_link_id'")
            __props__['private_link_id'] = private_link_id
            if project_id is None:
                raise TypeError("Missing required property 'project_id'")
            __props__['project_id'] = project_id
            __props__['connection_status'] = None
            __props__['delete_requested'] = None
            __props__['error_message'] = None
        super(PrivateEndpointInterfaceLink, __self__).__init__(
            'mongodbatlas:index/privateEndpointInterfaceLink:PrivateEndpointInterfaceLink',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, connection_status=None, delete_requested=None, error_message=None, interface_endpoint_id=None, private_link_id=None, project_id=None):
        """
        Get an existing PrivateEndpointInterfaceLink resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] connection_status: Status of the interface endpoint.
               Returns one of the following values:
        :param pulumi.Input[bool] delete_requested: Indicates if Atlas received a request to remove the interface endpoint from the private endpoint connection.
        :param pulumi.Input[str] error_message: Error message pertaining to the interface endpoint. Returns null if there are no errors.
        :param pulumi.Input[str] interface_endpoint_id: Unique identifier of the interface endpoint you created in your VPC with the AWS resource.
        :param pulumi.Input[str] private_link_id: Unique identifier of the AWS PrivateLink connection which is created by `.PrivateEndpoint` resource.
        :param pulumi.Input[str] project_id: Unique identifier for the project.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["connection_status"] = connection_status
        __props__["delete_requested"] = delete_requested
        __props__["error_message"] = error_message
        __props__["interface_endpoint_id"] = interface_endpoint_id
        __props__["private_link_id"] = private_link_id
        __props__["project_id"] = project_id
        return PrivateEndpointInterfaceLink(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

