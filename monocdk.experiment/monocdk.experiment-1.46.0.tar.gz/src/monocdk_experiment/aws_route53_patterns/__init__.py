import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (Construct as _Construct_f50a3f53)
from ..aws_certificatemanager import (ICertificate as _ICertificate_8f3d4c96)
from ..aws_route53 import (IHostedZone as _IHostedZone_59ffab76)


class HttpsRedirect(_Construct_f50a3f53, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_route53_patterns.HttpsRedirect"):
    """Allows creating a domainA -> domainB redirect using CloudFront and S3.

    You can specify multiple domains to be redirected.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, target_domain: str, zone: _IHostedZone_59ffab76, certificate: typing.Optional[_ICertificate_8f3d4c96]=None, record_names: typing.Optional[typing.List[str]]=None) -> None:
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


@jsii.data_type(jsii_type="monocdk-experiment.aws_route53_patterns.HttpsRedirectProps", jsii_struct_bases=[], name_mapping={'target_domain': 'targetDomain', 'zone': 'zone', 'certificate': 'certificate', 'record_names': 'recordNames'})
class HttpsRedirectProps():
    def __init__(self, *, target_domain: str, zone: _IHostedZone_59ffab76, certificate: typing.Optional[_ICertificate_8f3d4c96]=None, record_names: typing.Optional[typing.List[str]]=None) -> None:
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
    def zone(self) -> _IHostedZone_59ffab76:
        """HostedZone of the domain.

        stability
        :stability: experimental
        """
        return self._values.get('zone')

    @builtins.property
    def certificate(self) -> typing.Optional[_ICertificate_8f3d4c96]:
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
