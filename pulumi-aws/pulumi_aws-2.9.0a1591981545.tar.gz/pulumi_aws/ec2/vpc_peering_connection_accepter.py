# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class VpcPeeringConnectionAccepter(pulumi.CustomResource):
    accept_status: pulumi.Output[str]
    """
    The status of the VPC Peering Connection request.
    """
    accepter: pulumi.Output[dict]
    """
    A configuration block that describes [VPC Peering Connection]
    (https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html) options set for the accepter VPC.

      * `allowClassicLinkToRemoteVpc` (`bool`) - Indicates whether a local ClassicLink connection can communicate
        with the peer VPC over the VPC Peering Connection.
      * `allowRemoteVpcDnsResolution` (`bool`) - Indicates whether a local VPC can resolve public DNS hostnames to
        private IP addresses when queried from instances in a peer VPC.
      * `allowVpcToRemoteClassicLink` (`bool`) - Indicates whether a local VPC can communicate with a ClassicLink
        connection in the peer VPC over the VPC Peering Connection.
    """
    auto_accept: pulumi.Output[bool]
    """
    Whether or not to accept the peering request. Defaults to `false`.
    """
    peer_owner_id: pulumi.Output[str]
    """
    The AWS account ID of the owner of the requester VPC.
    """
    peer_region: pulumi.Output[str]
    """
    The region of the accepter VPC.
    """
    peer_vpc_id: pulumi.Output[str]
    """
    The ID of the requester VPC.
    """
    requester: pulumi.Output[dict]
    """
    A configuration block that describes [VPC Peering Connection]
    (https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html) options set for the requester VPC.

      * `allowClassicLinkToRemoteVpc` (`bool`) - Indicates whether a local ClassicLink connection can communicate
        with the peer VPC over the VPC Peering Connection.
      * `allowRemoteVpcDnsResolution` (`bool`) - Indicates whether a local VPC can resolve public DNS hostnames to
        private IP addresses when queried from instances in a peer VPC.
      * `allowVpcToRemoteClassicLink` (`bool`) - Indicates whether a local VPC can communicate with a ClassicLink
        connection in the peer VPC over the VPC Peering Connection.
    """
    tags: pulumi.Output[dict]
    """
    A map of tags to assign to the resource.
    """
    vpc_id: pulumi.Output[str]
    """
    The ID of the accepter VPC.
    """
    vpc_peering_connection_id: pulumi.Output[str]
    """
    The VPC Peering Connection ID to manage.
    """
    def __init__(__self__, resource_name, opts=None, accepter=None, auto_accept=None, requester=None, tags=None, vpc_peering_connection_id=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a resource to manage the accepter's side of a VPC Peering Connection.

        When a cross-account (requester's AWS account differs from the accepter's AWS account) or an inter-region
        VPC Peering Connection is created, a VPC Peering Connection resource is automatically created in the
        accepter's account.
        The requester can use the `ec2.VpcPeeringConnection` resource to manage its side of the connection
        and the accepter can use the `ec2.VpcPeeringConnectionAccepter` resource to "adopt" its side of the
        connection into management.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_aws as aws
        import pulumi_pulumi as pulumi

        peer = pulumi.providers.Aws("peer", region="us-west-2")
        main = aws.ec2.Vpc("main", cidr_block="10.0.0.0/16")
        peer_vpc = aws.ec2.Vpc("peerVpc", cidr_block="10.1.0.0/16")
        peer_caller_identity = aws.get_caller_identity()
        # Requester's side of the connection.
        peer_vpc_peering_connection = aws.ec2.VpcPeeringConnection("peerVpcPeeringConnection",
            auto_accept=False,
            peer_owner_id=peer_caller_identity.account_id,
            peer_region="us-west-2",
            peer_vpc_id=peer_vpc.id,
            tags={
                "Side": "Requester",
            },
            vpc_id=main.id)
        # Accepter's side of the connection.
        peer_vpc_peering_connection_accepter = aws.ec2.VpcPeeringConnectionAccepter("peerVpcPeeringConnectionAccepter",
            auto_accept=True,
            tags={
                "Side": "Accepter",
            },
            vpc_peering_connection_id=peer_vpc_peering_connection.id)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] accepter: A configuration block that describes [VPC Peering Connection]
               (https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html) options set for the accepter VPC.
        :param pulumi.Input[bool] auto_accept: Whether or not to accept the peering request. Defaults to `false`.
        :param pulumi.Input[dict] requester: A configuration block that describes [VPC Peering Connection]
               (https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html) options set for the requester VPC.
        :param pulumi.Input[dict] tags: A map of tags to assign to the resource.
        :param pulumi.Input[str] vpc_peering_connection_id: The VPC Peering Connection ID to manage.

        The **accepter** object supports the following:

          * `allowClassicLinkToRemoteVpc` (`pulumi.Input[bool]`) - Indicates whether a local ClassicLink connection can communicate
            with the peer VPC over the VPC Peering Connection.
          * `allowRemoteVpcDnsResolution` (`pulumi.Input[bool]`) - Indicates whether a local VPC can resolve public DNS hostnames to
            private IP addresses when queried from instances in a peer VPC.
          * `allowVpcToRemoteClassicLink` (`pulumi.Input[bool]`) - Indicates whether a local VPC can communicate with a ClassicLink
            connection in the peer VPC over the VPC Peering Connection.

        The **requester** object supports the following:

          * `allowClassicLinkToRemoteVpc` (`pulumi.Input[bool]`) - Indicates whether a local ClassicLink connection can communicate
            with the peer VPC over the VPC Peering Connection.
          * `allowRemoteVpcDnsResolution` (`pulumi.Input[bool]`) - Indicates whether a local VPC can resolve public DNS hostnames to
            private IP addresses when queried from instances in a peer VPC.
          * `allowVpcToRemoteClassicLink` (`pulumi.Input[bool]`) - Indicates whether a local VPC can communicate with a ClassicLink
            connection in the peer VPC over the VPC Peering Connection.
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

            __props__['accepter'] = accepter
            __props__['auto_accept'] = auto_accept
            __props__['requester'] = requester
            __props__['tags'] = tags
            if vpc_peering_connection_id is None:
                raise TypeError("Missing required property 'vpc_peering_connection_id'")
            __props__['vpc_peering_connection_id'] = vpc_peering_connection_id
            __props__['accept_status'] = None
            __props__['peer_owner_id'] = None
            __props__['peer_region'] = None
            __props__['peer_vpc_id'] = None
            __props__['vpc_id'] = None
        super(VpcPeeringConnectionAccepter, __self__).__init__(
            'aws:ec2/vpcPeeringConnectionAccepter:VpcPeeringConnectionAccepter',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, accept_status=None, accepter=None, auto_accept=None, peer_owner_id=None, peer_region=None, peer_vpc_id=None, requester=None, tags=None, vpc_id=None, vpc_peering_connection_id=None):
        """
        Get an existing VpcPeeringConnectionAccepter resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] accept_status: The status of the VPC Peering Connection request.
        :param pulumi.Input[dict] accepter: A configuration block that describes [VPC Peering Connection]
               (https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html) options set for the accepter VPC.
        :param pulumi.Input[bool] auto_accept: Whether or not to accept the peering request. Defaults to `false`.
        :param pulumi.Input[str] peer_owner_id: The AWS account ID of the owner of the requester VPC.
        :param pulumi.Input[str] peer_region: The region of the accepter VPC.
        :param pulumi.Input[str] peer_vpc_id: The ID of the requester VPC.
        :param pulumi.Input[dict] requester: A configuration block that describes [VPC Peering Connection]
               (https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html) options set for the requester VPC.
        :param pulumi.Input[dict] tags: A map of tags to assign to the resource.
        :param pulumi.Input[str] vpc_id: The ID of the accepter VPC.
        :param pulumi.Input[str] vpc_peering_connection_id: The VPC Peering Connection ID to manage.

        The **accepter** object supports the following:

          * `allowClassicLinkToRemoteVpc` (`pulumi.Input[bool]`) - Indicates whether a local ClassicLink connection can communicate
            with the peer VPC over the VPC Peering Connection.
          * `allowRemoteVpcDnsResolution` (`pulumi.Input[bool]`) - Indicates whether a local VPC can resolve public DNS hostnames to
            private IP addresses when queried from instances in a peer VPC.
          * `allowVpcToRemoteClassicLink` (`pulumi.Input[bool]`) - Indicates whether a local VPC can communicate with a ClassicLink
            connection in the peer VPC over the VPC Peering Connection.

        The **requester** object supports the following:

          * `allowClassicLinkToRemoteVpc` (`pulumi.Input[bool]`) - Indicates whether a local ClassicLink connection can communicate
            with the peer VPC over the VPC Peering Connection.
          * `allowRemoteVpcDnsResolution` (`pulumi.Input[bool]`) - Indicates whether a local VPC can resolve public DNS hostnames to
            private IP addresses when queried from instances in a peer VPC.
          * `allowVpcToRemoteClassicLink` (`pulumi.Input[bool]`) - Indicates whether a local VPC can communicate with a ClassicLink
            connection in the peer VPC over the VPC Peering Connection.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["accept_status"] = accept_status
        __props__["accepter"] = accepter
        __props__["auto_accept"] = auto_accept
        __props__["peer_owner_id"] = peer_owner_id
        __props__["peer_region"] = peer_region
        __props__["peer_vpc_id"] = peer_vpc_id
        __props__["requester"] = requester
        __props__["tags"] = tags
        __props__["vpc_id"] = vpc_id
        __props__["vpc_peering_connection_id"] = vpc_peering_connection_id
        return VpcPeeringConnectionAccepter(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

