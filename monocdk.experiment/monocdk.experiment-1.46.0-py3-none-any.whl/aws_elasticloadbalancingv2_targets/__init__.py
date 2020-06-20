import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from ..aws_ec2 import (Instance as _Instance_024cd2a8)
from ..aws_elasticloadbalancingv2 import (LoadBalancerTargetProps as _LoadBalancerTargetProps_80dbd4a5, IApplicationTargetGroup as _IApplicationTargetGroup_1bf77cc5, INetworkTargetGroup as _INetworkTargetGroup_1183b98f, IApplicationLoadBalancerTarget as _IApplicationLoadBalancerTarget_079c540c, INetworkLoadBalancerTarget as _INetworkLoadBalancerTarget_c44e1c1e)
from ..aws_lambda import (IFunction as _IFunction_1c1de0bc)


@jsii.implements(_IApplicationLoadBalancerTarget_079c540c, _INetworkLoadBalancerTarget_c44e1c1e)
class InstanceIdTarget(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_elasticloadbalancingv2_targets.InstanceIdTarget"):
    """An EC2 instance that is the target for load balancing.

    If you register a target of this type, you are responsible for making
    sure the load balancer's security group can connect to the instance.

    stability
    :stability: experimental
    """
    def __init__(self, instance_id: str, port: typing.Optional[jsii.Number]=None) -> None:
        """Create a new Instance target.

        :param instance_id: Instance ID of the instance to register to.
        :param port: Override the default port for the target group.

        stability
        :stability: experimental
        """
        jsii.create(InstanceIdTarget, self, [instance_id, port])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: _IApplicationTargetGroup_1bf77cc5) -> _LoadBalancerTargetProps_80dbd4a5:
        """Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: _INetworkTargetGroup_1183b98f) -> _LoadBalancerTargetProps_80dbd4a5:
        """Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])


class InstanceTarget(InstanceIdTarget, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_elasticloadbalancingv2_targets.InstanceTarget"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, instance: _Instance_024cd2a8, port: typing.Optional[jsii.Number]=None) -> None:
        """Create a new Instance target.

        :param instance: Instance to register to.
        :param port: Override the default port for the target group.

        stability
        :stability: experimental
        """
        jsii.create(InstanceTarget, self, [instance, port])


@jsii.implements(_IApplicationLoadBalancerTarget_079c540c, _INetworkLoadBalancerTarget_c44e1c1e)
class IpTarget(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_elasticloadbalancingv2_targets.IpTarget"):
    """An IP address that is a target for load balancing.

    Specify IP addresses from the subnets of the virtual private cloud (VPC) for
    the target group, the RFC 1918 range (10.0.0.0/8, 172.16.0.0/12, and
    192.168.0.0/16), and the RFC 6598 range (100.64.0.0/10). You can't specify
    publicly routable IP addresses.

    If you register a target of this type, you are responsible for making
    sure the load balancer's security group can send packets to the IP address.

    stability
    :stability: experimental
    """
    def __init__(self, ip_address: str, port: typing.Optional[jsii.Number]=None, availability_zone: typing.Optional[str]=None) -> None:
        """Create a new IPAddress target.

        The availabilityZone parameter determines whether the target receives
        traffic from the load balancer nodes in the specified Availability Zone
        or from all enabled Availability Zones for the load balancer.

        This parameter is not supported if the target type of the target group
        is instance. If the IP address is in a subnet of the VPC for the target
        group, the Availability Zone is automatically detected and this
        parameter is optional. If the IP address is outside the VPC, this
        parameter is required.

        With an Application Load Balancer, if the IP address is outside the VPC
        for the target group, the only supported value is all.

        Default is automatic.

        :param ip_address: The IP Address to load balance to.
        :param port: Override the group's default port.
        :param availability_zone: Availability zone to send traffic from.

        stability
        :stability: experimental
        """
        jsii.create(IpTarget, self, [ip_address, port, availability_zone])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: _IApplicationTargetGroup_1bf77cc5) -> _LoadBalancerTargetProps_80dbd4a5:
        """Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: _INetworkTargetGroup_1183b98f) -> _LoadBalancerTargetProps_80dbd4a5:
        """Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])


@jsii.implements(_IApplicationLoadBalancerTarget_079c540c)
class LambdaTarget(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_elasticloadbalancingv2_targets.LambdaTarget"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, fn: _IFunction_1c1de0bc) -> None:
        """Create a new Lambda target.

        :param fn: -

        stability
        :stability: experimental
        """
        jsii.create(LambdaTarget, self, [fn])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: _IApplicationTargetGroup_1bf77cc5) -> _LoadBalancerTargetProps_80dbd4a5:
        """Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: _INetworkTargetGroup_1183b98f) -> _LoadBalancerTargetProps_80dbd4a5:
        """Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])


__all__ = [
    "InstanceIdTarget",
    "InstanceTarget",
    "IpTarget",
    "LambdaTarget",
]

publication.publish()
