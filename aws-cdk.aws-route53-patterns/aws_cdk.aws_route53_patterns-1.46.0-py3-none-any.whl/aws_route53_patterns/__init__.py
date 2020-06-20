"""
# Route53 Patterns for the CDK Route53 Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Developer Preview](https://img.shields.io/badge/cdk--constructs-developer--preview-informational.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are in **developer preview** before they become stable. We will only make breaking changes to address unforeseen API issues. Therefore, these APIs are not subject to [Semantic Versioning](https://semver.org/), and breaking changes will be announced in release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This library contains commonly used patterns for Route53.

## HTTPS Redirect

This construct allows creating a simple domainA -> domainB redirect using CloudFront and S3. You can specify multiple domains to be redirected.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
HttpsRedirect(stack, "Redirect",
    record_names=["foo.example.com"],
    target_domain="bar.example.com",
    zone=HostedZone.from_hosted_zone_attributes(stack, "HostedZone",
        hosted_zone_id="ID",
        zone_name="example.com"
    )
)
```

See the documentation of `@aws-cdk/aws-route53-patterns` for more information.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from ._jsii import *

import aws_cdk.aws_certificatemanager
import aws_cdk.aws_route53
import aws_cdk.core


class HttpsRedirect(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53-patterns.HttpsRedirect"):
    """Allows creating a domainA -> domainB redirect using CloudFront and S3.

    You can specify multiple domains to be redirected.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, target_domain: str, zone: aws_cdk.aws_route53.IHostedZone, certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]=None, record_names: typing.Optional[typing.List[str]]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param target_domain: The redirect target domain.
        :param zone: HostedZone of the domain.
        :param certificate: The ACM certificate; Has to be in us-east-1 Default: - create a new certificate in us-east-1
        :param record_names: The domain names to create that will redirect to ``targetDomain``. Default: - the domain name of the zone

        stability
        :stability: experimental
        """
        props = HttpsRedirectProps(target_domain=target_domain, zone=zone, certificate=certificate, record_names=record_names)

        jsii.create(HttpsRedirect, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-route53-patterns.HttpsRedirectProps", jsii_struct_bases=[], name_mapping={'target_domain': 'targetDomain', 'zone': 'zone', 'certificate': 'certificate', 'record_names': 'recordNames'})
class HttpsRedirectProps():
    def __init__(self, *, target_domain: str, zone: aws_cdk.aws_route53.IHostedZone, certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]=None, record_names: typing.Optional[typing.List[str]]=None) -> None:
        """Properties to configure an HTTPS Redirect.

        :param target_domain: The redirect target domain.
        :param zone: HostedZone of the domain.
        :param certificate: The ACM certificate; Has to be in us-east-1 Default: - create a new certificate in us-east-1
        :param record_names: The domain names to create that will redirect to ``targetDomain``. Default: - the domain name of the zone

        stability
        :stability: experimental
        """
        self._values = {
            'target_domain': target_domain,
            'zone': zone,
        }
        if certificate is not None: self._values["certificate"] = certificate
        if record_names is not None: self._values["record_names"] = record_names

    @builtins.property
    def target_domain(self) -> str:
        """The redirect target domain.

        stability
        :stability: experimental
        """
        return self._values.get('target_domain')

    @builtins.property
    def zone(self) -> aws_cdk.aws_route53.IHostedZone:
        """HostedZone of the domain.

        stability
        :stability: experimental
        """
        return self._values.get('zone')

    @builtins.property
    def certificate(self) -> typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]:
        """The ACM certificate;

        Has to be in us-east-1

        default
        :default: - create a new certificate in us-east-1

        stability
        :stability: experimental
        """
        return self._values.get('certificate')

    @builtins.property
    def record_names(self) -> typing.Optional[typing.List[str]]:
        """The domain names to create that will redirect to ``targetDomain``.

        default
        :default: - the domain name of the zone

        stability
        :stability: experimental
        """
        return self._values.get('record_names')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HttpsRedirectProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "HttpsRedirect",
    "HttpsRedirectProps",
]

publication.publish()
