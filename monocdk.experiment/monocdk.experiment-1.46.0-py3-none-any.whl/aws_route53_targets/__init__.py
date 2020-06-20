import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from ..aws_apigateway import (RestApi as _RestApi_efdcda3d, IDomainName as _IDomainName_6a85089a)
from ..aws_cloudfront import (CloudFrontWebDistribution as _CloudFrontWebDistribution_2241efd0)
from ..aws_cognito import (UserPoolDomain as _UserPoolDomain_8fcfabd8)
from ..aws_ec2 import (IInterfaceVpcEndpoint as _IInterfaceVpcEndpoint_7ba1bb25)
from ..aws_elasticloadbalancing import (LoadBalancer as _LoadBalancer_6d00b4b8)
from ..aws_elasticloadbalancingv2 import (ILoadBalancerV2 as _ILoadBalancerV2_3b69d63d)
from ..aws_route53 import (AliasRecordTargetConfig as _AliasRecordTargetConfig_193313da, IRecordSet as _IRecordSet_4a72cb59, IAliasRecordTarget as _IAliasRecordTarget_2ddbe3b4)
from ..aws_s3 import (IBucket as _IBucket_25bad983)


@jsii.implements(_IAliasRecordTarget_2ddbe3b4)
class ApiGatewayDomain(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_route53_targets.ApiGatewayDomain"):
    """Defines an API Gateway domain name as the alias target.

    Use the ``ApiGateway`` class if you wish to map the alias to an REST API with a
    domain name defined throug the ``RestApiProps.domainName`` prop.

    stability
    :stability: experimental
    """
    def __init__(self, domain_name: _IDomainName_6a85089a) -> None:
        """
        :param domain_name: -

        stability
        :stability: experimental
        """
        jsii.create(ApiGatewayDomain, self, [domain_name])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: _IRecordSet_4a72cb59) -> _AliasRecordTargetConfig_193313da:
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_record])


@jsii.implements(_IAliasRecordTarget_2ddbe3b4)
class BucketWebsiteTarget(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_route53_targets.BucketWebsiteTarget"):
    """Use a S3 as an alias record target.

    stability
    :stability: experimental
    """
    def __init__(self, bucket: _IBucket_25bad983) -> None:
        """
        :param bucket: -

        stability
        :stability: experimental
        """
        jsii.create(BucketWebsiteTarget, self, [bucket])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: _IRecordSet_4a72cb59) -> _AliasRecordTargetConfig_193313da:
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_record])


@jsii.implements(_IAliasRecordTarget_2ddbe3b4)
class ClassicLoadBalancerTarget(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_route53_targets.ClassicLoadBalancerTarget"):
    """Use a classic ELB as an alias record target.

    stability
    :stability: experimental
    """
    def __init__(self, load_balancer: _LoadBalancer_6d00b4b8) -> None:
        """
        :param load_balancer: -

        stability
        :stability: experimental
        """
        jsii.create(ClassicLoadBalancerTarget, self, [load_balancer])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: _IRecordSet_4a72cb59) -> _AliasRecordTargetConfig_193313da:
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_record])


@jsii.implements(_IAliasRecordTarget_2ddbe3b4)
class CloudFrontTarget(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_route53_targets.CloudFrontTarget"):
    """Use a CloudFront Distribution as an alias record target.

    stability
    :stability: experimental
    """
    def __init__(self, distribution: _CloudFrontWebDistribution_2241efd0) -> None:
        """
        :param distribution: -

        stability
        :stability: experimental
        """
        jsii.create(CloudFrontTarget, self, [distribution])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: _IRecordSet_4a72cb59) -> _AliasRecordTargetConfig_193313da:
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_record])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CLOUDFRONT_ZONE_ID")
    def CLOUDFRONT_ZONE_ID(cls) -> str:
        """The hosted zone Id if using an alias record in Route53.

        This value never changes.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "CLOUDFRONT_ZONE_ID")


@jsii.implements(_IAliasRecordTarget_2ddbe3b4)
class InterfaceVpcEndpointTarget(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_route53_targets.InterfaceVpcEndpointTarget"):
    """Set an InterfaceVpcEndpoint as a target for an ARecord.

    stability
    :stability: experimental
    """
    def __init__(self, vpc_endpoint: _IInterfaceVpcEndpoint_7ba1bb25) -> None:
        """
        :param vpc_endpoint: -

        stability
        :stability: experimental
        """
        jsii.create(InterfaceVpcEndpointTarget, self, [vpc_endpoint])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: _IRecordSet_4a72cb59) -> _AliasRecordTargetConfig_193313da:
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_record])


@jsii.implements(_IAliasRecordTarget_2ddbe3b4)
class LoadBalancerTarget(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_route53_targets.LoadBalancerTarget"):
    """Use an ELBv2 as an alias record target.

    stability
    :stability: experimental
    """
    def __init__(self, load_balancer: _ILoadBalancerV2_3b69d63d) -> None:
        """
        :param load_balancer: -

        stability
        :stability: experimental
        """
        jsii.create(LoadBalancerTarget, self, [load_balancer])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: _IRecordSet_4a72cb59) -> _AliasRecordTargetConfig_193313da:
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_record])


@jsii.implements(_IAliasRecordTarget_2ddbe3b4)
class UserPoolDomainTarget(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_route53_targets.UserPoolDomainTarget"):
    """Use a user pool domain as an alias record target.

    stability
    :stability: experimental
    """
    def __init__(self, domain: _UserPoolDomain_8fcfabd8) -> None:
        """
        :param domain: -

        stability
        :stability: experimental
        """
        jsii.create(UserPoolDomainTarget, self, [domain])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: _IRecordSet_4a72cb59) -> _AliasRecordTargetConfig_193313da:
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_record])


class ApiGateway(ApiGatewayDomain, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_route53_targets.ApiGateway"):
    """Defines an API Gateway REST API as the alias target. Requires that the domain name will be defined through ``RestApiProps.domainName``.

    You can direct the alias to any ``apigateway.DomainName`` resource through the
    ``ApiGatewayDomain`` class.

    stability
    :stability: experimental
    """
    def __init__(self, api: _RestApi_efdcda3d) -> None:
        """
        :param api: -

        stability
        :stability: experimental
        """
        jsii.create(ApiGateway, self, [api])


__all__ = [
    "ApiGateway",
    "ApiGatewayDomain",
    "BucketWebsiteTarget",
    "ClassicLoadBalancerTarget",
    "CloudFrontTarget",
    "InterfaceVpcEndpointTarget",
    "LoadBalancerTarget",
    "UserPoolDomainTarget",
]

publication.publish()
