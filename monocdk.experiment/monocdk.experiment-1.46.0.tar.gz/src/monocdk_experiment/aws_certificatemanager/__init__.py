import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (Resource as _Resource_884d0774, Construct as _Construct_f50a3f53, CfnResource as _CfnResource_7760e8e4, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, TagManager as _TagManager_2508893f, IResolvable as _IResolvable_9ceae33e, IInspectable as _IInspectable_051e6ed8, CfnTag as _CfnTag_b4661f1a, IResource as _IResource_72f7ee7e)
from ..aws_iam import (IRole as _IRole_e69bbae4)
from ..aws_route53 import (IHostedZone as _IHostedZone_59ffab76)


@jsii.data_type(jsii_type="monocdk-experiment.aws_certificatemanager.CertificateProps", jsii_struct_bases=[], name_mapping={'domain_name': 'domainName', 'subject_alternative_names': 'subjectAlternativeNames', 'validation_domains': 'validationDomains', 'validation_method': 'validationMethod'})
class CertificateProps():
    def __init__(self, *, domain_name: str, subject_alternative_names: typing.Optional[typing.List[str]]=None, validation_domains: typing.Optional[typing.Mapping[str, str]]=None, validation_method: typing.Optional["ValidationMethod"]=None) -> None:
        """Properties for your certificate.

        :param domain_name: Fully-qualified domain name to request a certificate for. May contain wildcards, such as ``*.domain.com``.
        :param subject_alternative_names: Alternative domain names on your certificate. Use this to register alternative domain names that represent the same site. Default: - No additional FQDNs will be included as alternative domain names.
        :param validation_domains: What validation domain to use for every requested domain. Has to be a superdomain of the requested domain. Default: - Apex domain is used for every domain that's not overridden.
        :param validation_method: Validation method used to assert domain ownership. Default: ValidationMethod.EMAIL

        stability
        :stability: experimental
        """
        self._values = {
            'domain_name': domain_name,
        }
        if subject_alternative_names is not None: self._values["subject_alternative_names"] = subject_alternative_names
        if validation_domains is not None: self._values["validation_domains"] = validation_domains
        if validation_method is not None: self._values["validation_method"] = validation_method

    @builtins.property
    def domain_name(self) -> str:
        """Fully-qualified domain name to request a certificate for.

        May contain wildcards, such as ``*.domain.com``.

        stability
        :stability: experimental
        """
        return self._values.get('domain_name')

    @builtins.property
    def subject_alternative_names(self) -> typing.Optional[typing.List[str]]:
        """Alternative domain names on your certificate.

        Use this to register alternative domain names that represent the same site.

        default
        :default: - No additional FQDNs will be included as alternative domain names.

        stability
        :stability: experimental
        """
        return self._values.get('subject_alternative_names')

    @builtins.property
    def validation_domains(self) -> typing.Optional[typing.Mapping[str, str]]:
        """What validation domain to use for every requested domain.

        Has to be a superdomain of the requested domain.

        default
        :default: - Apex domain is used for every domain that's not overridden.

        stability
        :stability: experimental
        """
        return self._values.get('validation_domains')

    @builtins.property
    def validation_method(self) -> typing.Optional["ValidationMethod"]:
        """Validation method used to assert domain ownership.

        default
        :default: ValidationMethod.EMAIL

        stability
        :stability: experimental
        """
        return self._values.get('validation_method')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CertificateProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnCertificate(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_certificatemanager.CfnCertificate"):
    """A CloudFormation ``AWS::CertificateManager::Certificate``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html
    cloudformationResource:
    :cloudformationResource:: AWS::CertificateManager::Certificate
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, domain_name: str, certificate_authority_arn: typing.Optional[str]=None, certificate_transparency_logging_preference: typing.Optional[str]=None, domain_validation_options: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["DomainValidationOptionProperty", _IResolvable_9ceae33e]]]]=None, subject_alternative_names: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None, validation_method: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::CertificateManager::Certificate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param domain_name: ``AWS::CertificateManager::Certificate.DomainName``.
        :param certificate_authority_arn: ``AWS::CertificateManager::Certificate.CertificateAuthorityArn``.
        :param certificate_transparency_logging_preference: ``AWS::CertificateManager::Certificate.CertificateTransparencyLoggingPreference``.
        :param domain_validation_options: ``AWS::CertificateManager::Certificate.DomainValidationOptions``.
        :param subject_alternative_names: ``AWS::CertificateManager::Certificate.SubjectAlternativeNames``.
        :param tags: ``AWS::CertificateManager::Certificate.Tags``.
        :param validation_method: ``AWS::CertificateManager::Certificate.ValidationMethod``.
        """
        props = CfnCertificateProps(domain_name=domain_name, certificate_authority_arn=certificate_authority_arn, certificate_transparency_logging_preference=certificate_transparency_logging_preference, domain_validation_options=domain_validation_options, subject_alternative_names=subject_alternative_names, tags=tags, validation_method=validation_method)

        jsii.create(CfnCertificate, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnCertificate":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = _FromCloudFormationOptions_5f49f6f1(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::CertificateManager::Certificate.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """``AWS::CertificateManager::Certificate.DomainName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-domainname
        """
        return jsii.get(self, "domainName")

    @domain_name.setter
    def domain_name(self, value: str) -> None:
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityArn")
    def certificate_authority_arn(self) -> typing.Optional[str]:
        """``AWS::CertificateManager::Certificate.CertificateAuthorityArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-certificateauthorityarn
        """
        return jsii.get(self, "certificateAuthorityArn")

    @certificate_authority_arn.setter
    def certificate_authority_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "certificateAuthorityArn", value)

    @builtins.property
    @jsii.member(jsii_name="certificateTransparencyLoggingPreference")
    def certificate_transparency_logging_preference(self) -> typing.Optional[str]:
        """``AWS::CertificateManager::Certificate.CertificateTransparencyLoggingPreference``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-certificatetransparencyloggingpreference
        """
        return jsii.get(self, "certificateTransparencyLoggingPreference")

    @certificate_transparency_logging_preference.setter
    def certificate_transparency_logging_preference(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "certificateTransparencyLoggingPreference", value)

    @builtins.property
    @jsii.member(jsii_name="domainValidationOptions")
    def domain_validation_options(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["DomainValidationOptionProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::CertificateManager::Certificate.DomainValidationOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-domainvalidationoptions
        """
        return jsii.get(self, "domainValidationOptions")

    @domain_validation_options.setter
    def domain_validation_options(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["DomainValidationOptionProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "domainValidationOptions", value)

    @builtins.property
    @jsii.member(jsii_name="subjectAlternativeNames")
    def subject_alternative_names(self) -> typing.Optional[typing.List[str]]:
        """``AWS::CertificateManager::Certificate.SubjectAlternativeNames``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-subjectalternativenames
        """
        return jsii.get(self, "subjectAlternativeNames")

    @subject_alternative_names.setter
    def subject_alternative_names(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "subjectAlternativeNames", value)

    @builtins.property
    @jsii.member(jsii_name="validationMethod")
    def validation_method(self) -> typing.Optional[str]:
        """``AWS::CertificateManager::Certificate.ValidationMethod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-validationmethod
        """
        return jsii.get(self, "validationMethod")

    @validation_method.setter
    def validation_method(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "validationMethod", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_certificatemanager.CfnCertificate.DomainValidationOptionProperty", jsii_struct_bases=[], name_mapping={'domain_name': 'domainName', 'hosted_zone_id': 'hostedZoneId', 'validation_domain': 'validationDomain'})
    class DomainValidationOptionProperty():
        def __init__(self, *, domain_name: str, hosted_zone_id: typing.Optional[str]=None, validation_domain: typing.Optional[str]=None) -> None:
            """
            :param domain_name: ``CfnCertificate.DomainValidationOptionProperty.DomainName``.
            :param hosted_zone_id: ``CfnCertificate.DomainValidationOptionProperty.HostedZoneId``.
            :param validation_domain: ``CfnCertificate.DomainValidationOptionProperty.ValidationDomain``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-certificatemanager-certificate-domainvalidationoption.html
            """
            self._values = {
                'domain_name': domain_name,
            }
            if hosted_zone_id is not None: self._values["hosted_zone_id"] = hosted_zone_id
            if validation_domain is not None: self._values["validation_domain"] = validation_domain

        @builtins.property
        def domain_name(self) -> str:
            """``CfnCertificate.DomainValidationOptionProperty.DomainName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-certificatemanager-certificate-domainvalidationoption.html#cfn-certificatemanager-certificate-domainvalidationoptions-domainname
            """
            return self._values.get('domain_name')

        @builtins.property
        def hosted_zone_id(self) -> typing.Optional[str]:
            """``CfnCertificate.DomainValidationOptionProperty.HostedZoneId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-certificatemanager-certificate-domainvalidationoption.html#cfn-certificatemanager-certificate-domainvalidationoption-hostedzoneid
            """
            return self._values.get('hosted_zone_id')

        @builtins.property
        def validation_domain(self) -> typing.Optional[str]:
            """``CfnCertificate.DomainValidationOptionProperty.ValidationDomain``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-certificatemanager-certificate-domainvalidationoption.html#cfn-certificatemanager-certificate-domainvalidationoption-validationdomain
            """
            return self._values.get('validation_domain')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DomainValidationOptionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_certificatemanager.CfnCertificateProps", jsii_struct_bases=[], name_mapping={'domain_name': 'domainName', 'certificate_authority_arn': 'certificateAuthorityArn', 'certificate_transparency_logging_preference': 'certificateTransparencyLoggingPreference', 'domain_validation_options': 'domainValidationOptions', 'subject_alternative_names': 'subjectAlternativeNames', 'tags': 'tags', 'validation_method': 'validationMethod'})
class CfnCertificateProps():
    def __init__(self, *, domain_name: str, certificate_authority_arn: typing.Optional[str]=None, certificate_transparency_logging_preference: typing.Optional[str]=None, domain_validation_options: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnCertificate.DomainValidationOptionProperty", _IResolvable_9ceae33e]]]]=None, subject_alternative_names: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None, validation_method: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::CertificateManager::Certificate``.

        :param domain_name: ``AWS::CertificateManager::Certificate.DomainName``.
        :param certificate_authority_arn: ``AWS::CertificateManager::Certificate.CertificateAuthorityArn``.
        :param certificate_transparency_logging_preference: ``AWS::CertificateManager::Certificate.CertificateTransparencyLoggingPreference``.
        :param domain_validation_options: ``AWS::CertificateManager::Certificate.DomainValidationOptions``.
        :param subject_alternative_names: ``AWS::CertificateManager::Certificate.SubjectAlternativeNames``.
        :param tags: ``AWS::CertificateManager::Certificate.Tags``.
        :param validation_method: ``AWS::CertificateManager::Certificate.ValidationMethod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html
        """
        self._values = {
            'domain_name': domain_name,
        }
        if certificate_authority_arn is not None: self._values["certificate_authority_arn"] = certificate_authority_arn
        if certificate_transparency_logging_preference is not None: self._values["certificate_transparency_logging_preference"] = certificate_transparency_logging_preference
        if domain_validation_options is not None: self._values["domain_validation_options"] = domain_validation_options
        if subject_alternative_names is not None: self._values["subject_alternative_names"] = subject_alternative_names
        if tags is not None: self._values["tags"] = tags
        if validation_method is not None: self._values["validation_method"] = validation_method

    @builtins.property
    def domain_name(self) -> str:
        """``AWS::CertificateManager::Certificate.DomainName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-domainname
        """
        return self._values.get('domain_name')

    @builtins.property
    def certificate_authority_arn(self) -> typing.Optional[str]:
        """``AWS::CertificateManager::Certificate.CertificateAuthorityArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-certificateauthorityarn
        """
        return self._values.get('certificate_authority_arn')

    @builtins.property
    def certificate_transparency_logging_preference(self) -> typing.Optional[str]:
        """``AWS::CertificateManager::Certificate.CertificateTransparencyLoggingPreference``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-certificatetransparencyloggingpreference
        """
        return self._values.get('certificate_transparency_logging_preference')

    @builtins.property
    def domain_validation_options(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnCertificate.DomainValidationOptionProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::CertificateManager::Certificate.DomainValidationOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-domainvalidationoptions
        """
        return self._values.get('domain_validation_options')

    @builtins.property
    def subject_alternative_names(self) -> typing.Optional[typing.List[str]]:
        """``AWS::CertificateManager::Certificate.SubjectAlternativeNames``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-subjectalternativenames
        """
        return self._values.get('subject_alternative_names')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::CertificateManager::Certificate.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-tags
        """
        return self._values.get('tags')

    @builtins.property
    def validation_method(self) -> typing.Optional[str]:
        """``AWS::CertificateManager::Certificate.ValidationMethod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-validationmethod
        """
        return self._values.get('validation_method')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnCertificateProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_certificatemanager.DnsValidatedCertificateProps", jsii_struct_bases=[CertificateProps], name_mapping={'domain_name': 'domainName', 'subject_alternative_names': 'subjectAlternativeNames', 'validation_domains': 'validationDomains', 'validation_method': 'validationMethod', 'hosted_zone': 'hostedZone', 'custom_resource_role': 'customResourceRole', 'region': 'region', 'route53_endpoint': 'route53Endpoint'})
class DnsValidatedCertificateProps(CertificateProps):
    def __init__(self, *, domain_name: str, subject_alternative_names: typing.Optional[typing.List[str]]=None, validation_domains: typing.Optional[typing.Mapping[str, str]]=None, validation_method: typing.Optional["ValidationMethod"]=None, hosted_zone: _IHostedZone_59ffab76, custom_resource_role: typing.Optional[_IRole_e69bbae4]=None, region: typing.Optional[str]=None, route53_endpoint: typing.Optional[str]=None) -> None:
        """Properties to create a DNS validated certificate managed by AWS Certificate Manager.

        :param domain_name: Fully-qualified domain name to request a certificate for. May contain wildcards, such as ``*.domain.com``.
        :param subject_alternative_names: Alternative domain names on your certificate. Use this to register alternative domain names that represent the same site. Default: - No additional FQDNs will be included as alternative domain names.
        :param validation_domains: What validation domain to use for every requested domain. Has to be a superdomain of the requested domain. Default: - Apex domain is used for every domain that's not overridden.
        :param validation_method: Validation method used to assert domain ownership. Default: ValidationMethod.EMAIL
        :param hosted_zone: Route 53 Hosted Zone used to perform DNS validation of the request. The zone must be authoritative for the domain name specified in the Certificate Request.
        :param custom_resource_role: Role to use for the custom resource that creates the validated certificate. Default: - A new role will be created
        :param region: AWS region that will host the certificate. This is needed especially for certificates used for CloudFront distributions, which require the region to be us-east-1. Default: the region the stack is deployed in.
        :param route53_endpoint: An endpoint of Route53 service, which is not necessary as AWS SDK could figure out the right endpoints for most regions, but for some regions such as those in aws-cn partition, the default endpoint is not working now, hence the right endpoint need to be specified through this prop. Route53 is not been offically launched in China, it is only available for AWS internal accounts now. To make DnsValidatedCertificate work for internal accounts now, a special endpoint needs to be provided. Default: - The AWS SDK will determine the Route53 endpoint to use based on region

        stability
        :stability: experimental
        """
        self._values = {
            'domain_name': domain_name,
            'hosted_zone': hosted_zone,
        }
        if subject_alternative_names is not None: self._values["subject_alternative_names"] = subject_alternative_names
        if validation_domains is not None: self._values["validation_domains"] = validation_domains
        if validation_method is not None: self._values["validation_method"] = validation_method
        if custom_resource_role is not None: self._values["custom_resource_role"] = custom_resource_role
        if region is not None: self._values["region"] = region
        if route53_endpoint is not None: self._values["route53_endpoint"] = route53_endpoint

    @builtins.property
    def domain_name(self) -> str:
        """Fully-qualified domain name to request a certificate for.

        May contain wildcards, such as ``*.domain.com``.

        stability
        :stability: experimental
        """
        return self._values.get('domain_name')

    @builtins.property
    def subject_alternative_names(self) -> typing.Optional[typing.List[str]]:
        """Alternative domain names on your certificate.

        Use this to register alternative domain names that represent the same site.

        default
        :default: - No additional FQDNs will be included as alternative domain names.

        stability
        :stability: experimental
        """
        return self._values.get('subject_alternative_names')

    @builtins.property
    def validation_domains(self) -> typing.Optional[typing.Mapping[str, str]]:
        """What validation domain to use for every requested domain.

        Has to be a superdomain of the requested domain.

        default
        :default: - Apex domain is used for every domain that's not overridden.

        stability
        :stability: experimental
        """
        return self._values.get('validation_domains')

    @builtins.property
    def validation_method(self) -> typing.Optional["ValidationMethod"]:
        """Validation method used to assert domain ownership.

        default
        :default: ValidationMethod.EMAIL

        stability
        :stability: experimental
        """
        return self._values.get('validation_method')

    @builtins.property
    def hosted_zone(self) -> _IHostedZone_59ffab76:
        """Route 53 Hosted Zone used to perform DNS validation of the request.

        The zone
        must be authoritative for the domain name specified in the Certificate Request.

        stability
        :stability: experimental
        """
        return self._values.get('hosted_zone')

    @builtins.property
    def custom_resource_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Role to use for the custom resource that creates the validated certificate.

        default
        :default: - A new role will be created

        stability
        :stability: experimental
        """
        return self._values.get('custom_resource_role')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """AWS region that will host the certificate.

        This is needed especially
        for certificates used for CloudFront distributions, which require the region
        to be us-east-1.

        default
        :default: the region the stack is deployed in.

        stability
        :stability: experimental
        """
        return self._values.get('region')

    @builtins.property
    def route53_endpoint(self) -> typing.Optional[str]:
        """An endpoint of Route53 service, which is not necessary as AWS SDK could figure out the right endpoints for most regions, but for some regions such as those in aws-cn partition, the default endpoint is not working now, hence the right endpoint need to be specified through this prop.

        Route53 is not been offically launched in China, it is only available for AWS
        internal accounts now. To make DnsValidatedCertificate work for internal accounts
        now, a special endpoint needs to be provided.

        default
        :default: - The AWS SDK will determine the Route53 endpoint to use based on region

        stability
        :stability: experimental
        """
        return self._values.get('route53_endpoint')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DnsValidatedCertificateProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="monocdk-experiment.aws_certificatemanager.ICertificate")
class ICertificate(_IResource_72f7ee7e, jsii.compat.Protocol):
    """Represents a certificate in AWS Certificate Manager.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ICertificateProxy

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> str:
        """The certificate's ARN.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _ICertificateProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """Represents a certificate in AWS Certificate Manager.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_certificatemanager.ICertificate"
    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> str:
        """The certificate's ARN.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "certificateArn")


@jsii.enum(jsii_type="monocdk-experiment.aws_certificatemanager.ValidationMethod")
class ValidationMethod(enum.Enum):
    """Method used to assert ownership of the domain.

    stability
    :stability: experimental
    """
    EMAIL = "EMAIL"
    """Send email to a number of email addresses associated with the domain.

    see
    :see: https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-email.html
    stability
    :stability: experimental
    """
    DNS = "DNS"
    """Validate ownership by adding appropriate DNS records.

    see
    :see: https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html
    stability
    :stability: experimental
    """

@jsii.implements(ICertificate)
class Certificate(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_certificatemanager.Certificate"):
    """A certificate managed by AWS Certificate Manager.

    IMPORTANT: if you are creating a certificate as part of your stack, the stack
    will not complete creating until you read and follow the instructions in the
    email that you will receive.

    ACM will send validation emails to the following addresses:

    admin@domain.com
    administrator@domain.com
    hostmaster@domain.com
    postmaster@domain.com
    webmaster@domain.com

    For every domain that you register.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, domain_name: str, subject_alternative_names: typing.Optional[typing.List[str]]=None, validation_domains: typing.Optional[typing.Mapping[str, str]]=None, validation_method: typing.Optional["ValidationMethod"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param domain_name: Fully-qualified domain name to request a certificate for. May contain wildcards, such as ``*.domain.com``.
        :param subject_alternative_names: Alternative domain names on your certificate. Use this to register alternative domain names that represent the same site. Default: - No additional FQDNs will be included as alternative domain names.
        :param validation_domains: What validation domain to use for every requested domain. Has to be a superdomain of the requested domain. Default: - Apex domain is used for every domain that's not overridden.
        :param validation_method: Validation method used to assert domain ownership. Default: ValidationMethod.EMAIL

        stability
        :stability: experimental
        """
        props = CertificateProps(domain_name=domain_name, subject_alternative_names=subject_alternative_names, validation_domains=validation_domains, validation_method=validation_method)

        jsii.create(Certificate, self, [scope, id, props])

    @jsii.member(jsii_name="fromCertificateArn")
    @builtins.classmethod
    def from_certificate_arn(cls, scope: _Construct_f50a3f53, id: str, certificate_arn: str) -> "ICertificate":
        """Import a certificate.

        :param scope: -
        :param id: -
        :param certificate_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromCertificateArn", [scope, id, certificate_arn])

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> str:
        """The certificate's ARN.

        stability
        :stability: experimental
        """
        return jsii.get(self, "certificateArn")


@jsii.implements(ICertificate)
class DnsValidatedCertificate(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_certificatemanager.DnsValidatedCertificate"):
    """A certificate managed by AWS Certificate Manager.

    Will be automatically
    validated using DNS validation against the specified Route 53 hosted zone.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::CertificateManager::Certificate
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, hosted_zone: _IHostedZone_59ffab76, custom_resource_role: typing.Optional[_IRole_e69bbae4]=None, region: typing.Optional[str]=None, route53_endpoint: typing.Optional[str]=None, domain_name: str, subject_alternative_names: typing.Optional[typing.List[str]]=None, validation_domains: typing.Optional[typing.Mapping[str, str]]=None, validation_method: typing.Optional["ValidationMethod"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param hosted_zone: Route 53 Hosted Zone used to perform DNS validation of the request. The zone must be authoritative for the domain name specified in the Certificate Request.
        :param custom_resource_role: Role to use for the custom resource that creates the validated certificate. Default: - A new role will be created
        :param region: AWS region that will host the certificate. This is needed especially for certificates used for CloudFront distributions, which require the region to be us-east-1. Default: the region the stack is deployed in.
        :param route53_endpoint: An endpoint of Route53 service, which is not necessary as AWS SDK could figure out the right endpoints for most regions, but for some regions such as those in aws-cn partition, the default endpoint is not working now, hence the right endpoint need to be specified through this prop. Route53 is not been offically launched in China, it is only available for AWS internal accounts now. To make DnsValidatedCertificate work for internal accounts now, a special endpoint needs to be provided. Default: - The AWS SDK will determine the Route53 endpoint to use based on region
        :param domain_name: Fully-qualified domain name to request a certificate for. May contain wildcards, such as ``*.domain.com``.
        :param subject_alternative_names: Alternative domain names on your certificate. Use this to register alternative domain names that represent the same site. Default: - No additional FQDNs will be included as alternative domain names.
        :param validation_domains: What validation domain to use for every requested domain. Has to be a superdomain of the requested domain. Default: - Apex domain is used for every domain that's not overridden.
        :param validation_method: Validation method used to assert domain ownership. Default: ValidationMethod.EMAIL

        stability
        :stability: experimental
        """
        props = DnsValidatedCertificateProps(hosted_zone=hosted_zone, custom_resource_role=custom_resource_role, region=region, route53_endpoint=route53_endpoint, domain_name=domain_name, subject_alternative_names=subject_alternative_names, validation_domains=validation_domains, validation_method=validation_method)

        jsii.create(DnsValidatedCertificate, self, [scope, id, props])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> str:
        """The certificate's ARN.

        stability
        :stability: experimental
        """
        return jsii.get(self, "certificateArn")


__all__ = [
    "Certificate",
    "CertificateProps",
    "CfnCertificate",
    "CfnCertificateProps",
    "DnsValidatedCertificate",
    "DnsValidatedCertificateProps",
    "ICertificate",
    "ValidationMethod",
]

publication.publish()
