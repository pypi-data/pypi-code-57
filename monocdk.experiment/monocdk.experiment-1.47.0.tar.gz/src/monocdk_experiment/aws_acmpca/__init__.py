import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (CfnResource as _CfnResource_7760e8e4, Construct as _Construct_f50a3f53, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, IResolvable as _IResolvable_9ceae33e, IInspectable as _IInspectable_051e6ed8, TagManager as _TagManager_2508893f, CfnTag as _CfnTag_b4661f1a)


@jsii.implements(_IInspectable_051e6ed8)
class CfnCertificate(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_acmpca.CfnCertificate"):
    """A CloudFormation ``AWS::ACMPCA::Certificate``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html
    cloudformationResource:
    :cloudformationResource:: AWS::ACMPCA::Certificate
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, certificate_authority_arn: str, certificate_signing_request: str, signing_algorithm: str, validity: typing.Union["ValidityProperty", _IResolvable_9ceae33e], template_arn: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ACMPCA::Certificate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param certificate_authority_arn: ``AWS::ACMPCA::Certificate.CertificateAuthorityArn``.
        :param certificate_signing_request: ``AWS::ACMPCA::Certificate.CertificateSigningRequest``.
        :param signing_algorithm: ``AWS::ACMPCA::Certificate.SigningAlgorithm``.
        :param validity: ``AWS::ACMPCA::Certificate.Validity``.
        :param template_arn: ``AWS::ACMPCA::Certificate.TemplateArn``.
        """
        props = CfnCertificateProps(certificate_authority_arn=certificate_authority_arn, certificate_signing_request=certificate_signing_request, signing_algorithm=signing_algorithm, validity=validity, template_arn=template_arn)

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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property
    @jsii.member(jsii_name="attrCertificate")
    def attr_certificate(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Certificate
        """
        return jsii.get(self, "attrCertificate")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityArn")
    def certificate_authority_arn(self) -> str:
        """``AWS::ACMPCA::Certificate.CertificateAuthorityArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-certificateauthorityarn
        """
        return jsii.get(self, "certificateAuthorityArn")

    @certificate_authority_arn.setter
    def certificate_authority_arn(self, value: str) -> None:
        jsii.set(self, "certificateAuthorityArn", value)

    @builtins.property
    @jsii.member(jsii_name="certificateSigningRequest")
    def certificate_signing_request(self) -> str:
        """``AWS::ACMPCA::Certificate.CertificateSigningRequest``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-certificatesigningrequest
        """
        return jsii.get(self, "certificateSigningRequest")

    @certificate_signing_request.setter
    def certificate_signing_request(self, value: str) -> None:
        jsii.set(self, "certificateSigningRequest", value)

    @builtins.property
    @jsii.member(jsii_name="signingAlgorithm")
    def signing_algorithm(self) -> str:
        """``AWS::ACMPCA::Certificate.SigningAlgorithm``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-signingalgorithm
        """
        return jsii.get(self, "signingAlgorithm")

    @signing_algorithm.setter
    def signing_algorithm(self, value: str) -> None:
        jsii.set(self, "signingAlgorithm", value)

    @builtins.property
    @jsii.member(jsii_name="validity")
    def validity(self) -> typing.Union["ValidityProperty", _IResolvable_9ceae33e]:
        """``AWS::ACMPCA::Certificate.Validity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-validity
        """
        return jsii.get(self, "validity")

    @validity.setter
    def validity(self, value: typing.Union["ValidityProperty", _IResolvable_9ceae33e]) -> None:
        jsii.set(self, "validity", value)

    @builtins.property
    @jsii.member(jsii_name="templateArn")
    def template_arn(self) -> typing.Optional[str]:
        """``AWS::ACMPCA::Certificate.TemplateArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-templatearn
        """
        return jsii.get(self, "templateArn")

    @template_arn.setter
    def template_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "templateArn", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_acmpca.CfnCertificate.ValidityProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'value': 'value'})
    class ValidityProperty():
        def __init__(self, *, type: str, value: jsii.Number) -> None:
            """
            :param type: ``CfnCertificate.ValidityProperty.Type``.
            :param value: ``CfnCertificate.ValidityProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-validity.html
            """
            self._values = {
                'type': type,
                'value': value,
            }

        @builtins.property
        def type(self) -> str:
            """``CfnCertificate.ValidityProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-validity.html#cfn-acmpca-certificate-validity-type
            """
            return self._values.get('type')

        @builtins.property
        def value(self) -> jsii.Number:
            """``CfnCertificate.ValidityProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-validity.html#cfn-acmpca-certificate-validity-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ValidityProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.implements(_IInspectable_051e6ed8)
class CfnCertificateAuthority(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_acmpca.CfnCertificateAuthority"):
    """A CloudFormation ``AWS::ACMPCA::CertificateAuthority``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html
    cloudformationResource:
    :cloudformationResource:: AWS::ACMPCA::CertificateAuthority
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, key_algorithm: str, signing_algorithm: str, subject: typing.Union["SubjectProperty", _IResolvable_9ceae33e], type: str, revocation_configuration: typing.Optional[typing.Union["RevocationConfigurationProperty", _IResolvable_9ceae33e]]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Create a new ``AWS::ACMPCA::CertificateAuthority``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param key_algorithm: ``AWS::ACMPCA::CertificateAuthority.KeyAlgorithm``.
        :param signing_algorithm: ``AWS::ACMPCA::CertificateAuthority.SigningAlgorithm``.
        :param subject: ``AWS::ACMPCA::CertificateAuthority.Subject``.
        :param type: ``AWS::ACMPCA::CertificateAuthority.Type``.
        :param revocation_configuration: ``AWS::ACMPCA::CertificateAuthority.RevocationConfiguration``.
        :param tags: ``AWS::ACMPCA::CertificateAuthority.Tags``.
        """
        props = CfnCertificateAuthorityProps(key_algorithm=key_algorithm, signing_algorithm=signing_algorithm, subject=subject, type=type, revocation_configuration=revocation_configuration, tags=tags)

        jsii.create(CfnCertificateAuthority, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnCertificateAuthority":
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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property
    @jsii.member(jsii_name="attrCertificateSigningRequest")
    def attr_certificate_signing_request(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: CertificateSigningRequest
        """
        return jsii.get(self, "attrCertificateSigningRequest")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::ACMPCA::CertificateAuthority.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="keyAlgorithm")
    def key_algorithm(self) -> str:
        """``AWS::ACMPCA::CertificateAuthority.KeyAlgorithm``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-keyalgorithm
        """
        return jsii.get(self, "keyAlgorithm")

    @key_algorithm.setter
    def key_algorithm(self, value: str) -> None:
        jsii.set(self, "keyAlgorithm", value)

    @builtins.property
    @jsii.member(jsii_name="signingAlgorithm")
    def signing_algorithm(self) -> str:
        """``AWS::ACMPCA::CertificateAuthority.SigningAlgorithm``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-signingalgorithm
        """
        return jsii.get(self, "signingAlgorithm")

    @signing_algorithm.setter
    def signing_algorithm(self, value: str) -> None:
        jsii.set(self, "signingAlgorithm", value)

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> typing.Union["SubjectProperty", _IResolvable_9ceae33e]:
        """``AWS::ACMPCA::CertificateAuthority.Subject``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-subject
        """
        return jsii.get(self, "subject")

    @subject.setter
    def subject(self, value: typing.Union["SubjectProperty", _IResolvable_9ceae33e]) -> None:
        jsii.set(self, "subject", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        """``AWS::ACMPCA::CertificateAuthority.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-type
        """
        return jsii.get(self, "type")

    @type.setter
    def type(self, value: str) -> None:
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="revocationConfiguration")
    def revocation_configuration(self) -> typing.Optional[typing.Union["RevocationConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::ACMPCA::CertificateAuthority.RevocationConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-revocationconfiguration
        """
        return jsii.get(self, "revocationConfiguration")

    @revocation_configuration.setter
    def revocation_configuration(self, value: typing.Optional[typing.Union["RevocationConfigurationProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "revocationConfiguration", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_acmpca.CfnCertificateAuthority.CrlConfigurationProperty", jsii_struct_bases=[], name_mapping={'custom_cname': 'customCname', 'enabled': 'enabled', 'expiration_in_days': 'expirationInDays', 's3_bucket_name': 's3BucketName'})
    class CrlConfigurationProperty():
        def __init__(self, *, custom_cname: typing.Optional[str]=None, enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, expiration_in_days: typing.Optional[jsii.Number]=None, s3_bucket_name: typing.Optional[str]=None) -> None:
            """
            :param custom_cname: ``CfnCertificateAuthority.CrlConfigurationProperty.CustomCname``.
            :param enabled: ``CfnCertificateAuthority.CrlConfigurationProperty.Enabled``.
            :param expiration_in_days: ``CfnCertificateAuthority.CrlConfigurationProperty.ExpirationInDays``.
            :param s3_bucket_name: ``CfnCertificateAuthority.CrlConfigurationProperty.S3BucketName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html
            """
            self._values = {
            }
            if custom_cname is not None: self._values["custom_cname"] = custom_cname
            if enabled is not None: self._values["enabled"] = enabled
            if expiration_in_days is not None: self._values["expiration_in_days"] = expiration_in_days
            if s3_bucket_name is not None: self._values["s3_bucket_name"] = s3_bucket_name

        @builtins.property
        def custom_cname(self) -> typing.Optional[str]:
            """``CfnCertificateAuthority.CrlConfigurationProperty.CustomCname``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-customcname
            """
            return self._values.get('custom_cname')

        @builtins.property
        def enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnCertificateAuthority.CrlConfigurationProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-enabled
            """
            return self._values.get('enabled')

        @builtins.property
        def expiration_in_days(self) -> typing.Optional[jsii.Number]:
            """``CfnCertificateAuthority.CrlConfigurationProperty.ExpirationInDays``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-expirationindays
            """
            return self._values.get('expiration_in_days')

        @builtins.property
        def s3_bucket_name(self) -> typing.Optional[str]:
            """``CfnCertificateAuthority.CrlConfigurationProperty.S3BucketName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-s3bucketname
            """
            return self._values.get('s3_bucket_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CrlConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_acmpca.CfnCertificateAuthority.RevocationConfigurationProperty", jsii_struct_bases=[], name_mapping={'crl_configuration': 'crlConfiguration'})
    class RevocationConfigurationProperty():
        def __init__(self, *, crl_configuration: typing.Optional[typing.Union["CfnCertificateAuthority.CrlConfigurationProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param crl_configuration: ``CfnCertificateAuthority.RevocationConfigurationProperty.CrlConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-revocationconfiguration.html
            """
            self._values = {
            }
            if crl_configuration is not None: self._values["crl_configuration"] = crl_configuration

        @builtins.property
        def crl_configuration(self) -> typing.Optional[typing.Union["CfnCertificateAuthority.CrlConfigurationProperty", _IResolvable_9ceae33e]]:
            """``CfnCertificateAuthority.RevocationConfigurationProperty.CrlConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-revocationconfiguration.html#cfn-acmpca-certificateauthority-revocationconfiguration-crlconfiguration
            """
            return self._values.get('crl_configuration')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RevocationConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_acmpca.CfnCertificateAuthority.SubjectProperty", jsii_struct_bases=[], name_mapping={'common_name': 'commonName', 'country': 'country', 'distinguished_name_qualifier': 'distinguishedNameQualifier', 'generation_qualifier': 'generationQualifier', 'given_name': 'givenName', 'initials': 'initials', 'locality': 'locality', 'organization': 'organization', 'organizational_unit': 'organizationalUnit', 'pseudonym': 'pseudonym', 'serial_number': 'serialNumber', 'state': 'state', 'surname': 'surname', 'title': 'title'})
    class SubjectProperty():
        def __init__(self, *, common_name: typing.Optional[str]=None, country: typing.Optional[str]=None, distinguished_name_qualifier: typing.Optional[str]=None, generation_qualifier: typing.Optional[str]=None, given_name: typing.Optional[str]=None, initials: typing.Optional[str]=None, locality: typing.Optional[str]=None, organization: typing.Optional[str]=None, organizational_unit: typing.Optional[str]=None, pseudonym: typing.Optional[str]=None, serial_number: typing.Optional[str]=None, state: typing.Optional[str]=None, surname: typing.Optional[str]=None, title: typing.Optional[str]=None) -> None:
            """
            :param common_name: ``CfnCertificateAuthority.SubjectProperty.CommonName``.
            :param country: ``CfnCertificateAuthority.SubjectProperty.Country``.
            :param distinguished_name_qualifier: ``CfnCertificateAuthority.SubjectProperty.DistinguishedNameQualifier``.
            :param generation_qualifier: ``CfnCertificateAuthority.SubjectProperty.GenerationQualifier``.
            :param given_name: ``CfnCertificateAuthority.SubjectProperty.GivenName``.
            :param initials: ``CfnCertificateAuthority.SubjectProperty.Initials``.
            :param locality: ``CfnCertificateAuthority.SubjectProperty.Locality``.
            :param organization: ``CfnCertificateAuthority.SubjectProperty.Organization``.
            :param organizational_unit: ``CfnCertificateAuthority.SubjectProperty.OrganizationalUnit``.
            :param pseudonym: ``CfnCertificateAuthority.SubjectProperty.Pseudonym``.
            :param serial_number: ``CfnCertificateAuthority.SubjectProperty.SerialNumber``.
            :param state: ``CfnCertificateAuthority.SubjectProperty.State``.
            :param surname: ``CfnCertificateAuthority.SubjectProperty.Surname``.
            :param title: ``CfnCertificateAuthority.SubjectProperty.Title``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html
            """
            self._values = {
            }
            if common_name is not None: self._values["common_name"] = common_name
            if country is not None: self._values["country"] = country
            if distinguished_name_qualifier is not None: self._values["distinguished_name_qualifier"] = distinguished_name_qualifier
            if generation_qualifier is not None: self._values["generation_qualifier"] = generation_qualifier
            if given_name is not None: self._values["given_name"] = given_name
            if initials is not None: self._values["initials"] = initials
            if locality is not None: self._values["locality"] = locality
            if organization is not None: self._values["organization"] = organization
            if organizational_unit is not None: self._values["organizational_unit"] = organizational_unit
            if pseudonym is not None: self._values["pseudonym"] = pseudonym
            if serial_number is not None: self._values["serial_number"] = serial_number
            if state is not None: self._values["state"] = state
            if surname is not None: self._values["surname"] = surname
            if title is not None: self._values["title"] = title

        @builtins.property
        def common_name(self) -> typing.Optional[str]:
            """``CfnCertificateAuthority.SubjectProperty.CommonName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-commonname
            """
            return self._values.get('common_name')

        @builtins.property
        def country(self) -> typing.Optional[str]:
            """``CfnCertificateAuthority.SubjectProperty.Country``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-country
            """
            return self._values.get('country')

        @builtins.property
        def distinguished_name_qualifier(self) -> typing.Optional[str]:
            """``CfnCertificateAuthority.SubjectProperty.DistinguishedNameQualifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-distinguishednamequalifier
            """
            return self._values.get('distinguished_name_qualifier')

        @builtins.property
        def generation_qualifier(self) -> typing.Optional[str]:
            """``CfnCertificateAuthority.SubjectProperty.GenerationQualifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-generationqualifier
            """
            return self._values.get('generation_qualifier')

        @builtins.property
        def given_name(self) -> typing.Optional[str]:
            """``CfnCertificateAuthority.SubjectProperty.GivenName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-givenname
            """
            return self._values.get('given_name')

        @builtins.property
        def initials(self) -> typing.Optional[str]:
            """``CfnCertificateAuthority.SubjectProperty.Initials``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-initials
            """
            return self._values.get('initials')

        @builtins.property
        def locality(self) -> typing.Optional[str]:
            """``CfnCertificateAuthority.SubjectProperty.Locality``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-locality
            """
            return self._values.get('locality')

        @builtins.property
        def organization(self) -> typing.Optional[str]:
            """``CfnCertificateAuthority.SubjectProperty.Organization``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-organization
            """
            return self._values.get('organization')

        @builtins.property
        def organizational_unit(self) -> typing.Optional[str]:
            """``CfnCertificateAuthority.SubjectProperty.OrganizationalUnit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-organizationalunit
            """
            return self._values.get('organizational_unit')

        @builtins.property
        def pseudonym(self) -> typing.Optional[str]:
            """``CfnCertificateAuthority.SubjectProperty.Pseudonym``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-pseudonym
            """
            return self._values.get('pseudonym')

        @builtins.property
        def serial_number(self) -> typing.Optional[str]:
            """``CfnCertificateAuthority.SubjectProperty.SerialNumber``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-serialnumber
            """
            return self._values.get('serial_number')

        @builtins.property
        def state(self) -> typing.Optional[str]:
            """``CfnCertificateAuthority.SubjectProperty.State``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-state
            """
            return self._values.get('state')

        @builtins.property
        def surname(self) -> typing.Optional[str]:
            """``CfnCertificateAuthority.SubjectProperty.Surname``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-surname
            """
            return self._values.get('surname')

        @builtins.property
        def title(self) -> typing.Optional[str]:
            """``CfnCertificateAuthority.SubjectProperty.Title``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-title
            """
            return self._values.get('title')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SubjectProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.implements(_IInspectable_051e6ed8)
class CfnCertificateAuthorityActivation(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_acmpca.CfnCertificateAuthorityActivation"):
    """A CloudFormation ``AWS::ACMPCA::CertificateAuthorityActivation``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html
    cloudformationResource:
    :cloudformationResource:: AWS::ACMPCA::CertificateAuthorityActivation
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, certificate: str, certificate_authority_arn: str, certificate_chain: typing.Optional[str]=None, status: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ACMPCA::CertificateAuthorityActivation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param certificate: ``AWS::ACMPCA::CertificateAuthorityActivation.Certificate``.
        :param certificate_authority_arn: ``AWS::ACMPCA::CertificateAuthorityActivation.CertificateAuthorityArn``.
        :param certificate_chain: ``AWS::ACMPCA::CertificateAuthorityActivation.CertificateChain``.
        :param status: ``AWS::ACMPCA::CertificateAuthorityActivation.Status``.
        """
        props = CfnCertificateAuthorityActivationProps(certificate=certificate, certificate_authority_arn=certificate_authority_arn, certificate_chain=certificate_chain, status=status)

        jsii.create(CfnCertificateAuthorityActivation, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnCertificateAuthorityActivation":
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
    @jsii.member(jsii_name="attrCompleteCertificateChain")
    def attr_complete_certificate_chain(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: CompleteCertificateChain
        """
        return jsii.get(self, "attrCompleteCertificateChain")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> str:
        """``AWS::ACMPCA::CertificateAuthorityActivation.Certificate``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificate
        """
        return jsii.get(self, "certificate")

    @certificate.setter
    def certificate(self, value: str) -> None:
        jsii.set(self, "certificate", value)

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityArn")
    def certificate_authority_arn(self) -> str:
        """``AWS::ACMPCA::CertificateAuthorityActivation.CertificateAuthorityArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificateauthorityarn
        """
        return jsii.get(self, "certificateAuthorityArn")

    @certificate_authority_arn.setter
    def certificate_authority_arn(self, value: str) -> None:
        jsii.set(self, "certificateAuthorityArn", value)

    @builtins.property
    @jsii.member(jsii_name="certificateChain")
    def certificate_chain(self) -> typing.Optional[str]:
        """``AWS::ACMPCA::CertificateAuthorityActivation.CertificateChain``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificatechain
        """
        return jsii.get(self, "certificateChain")

    @certificate_chain.setter
    def certificate_chain(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "certificateChain", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[str]:
        """``AWS::ACMPCA::CertificateAuthorityActivation.Status``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-status
        """
        return jsii.get(self, "status")

    @status.setter
    def status(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "status", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_acmpca.CfnCertificateAuthorityActivationProps", jsii_struct_bases=[], name_mapping={'certificate': 'certificate', 'certificate_authority_arn': 'certificateAuthorityArn', 'certificate_chain': 'certificateChain', 'status': 'status'})
class CfnCertificateAuthorityActivationProps():
    def __init__(self, *, certificate: str, certificate_authority_arn: str, certificate_chain: typing.Optional[str]=None, status: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::ACMPCA::CertificateAuthorityActivation``.

        :param certificate: ``AWS::ACMPCA::CertificateAuthorityActivation.Certificate``.
        :param certificate_authority_arn: ``AWS::ACMPCA::CertificateAuthorityActivation.CertificateAuthorityArn``.
        :param certificate_chain: ``AWS::ACMPCA::CertificateAuthorityActivation.CertificateChain``.
        :param status: ``AWS::ACMPCA::CertificateAuthorityActivation.Status``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html
        """
        self._values = {
            'certificate': certificate,
            'certificate_authority_arn': certificate_authority_arn,
        }
        if certificate_chain is not None: self._values["certificate_chain"] = certificate_chain
        if status is not None: self._values["status"] = status

    @builtins.property
    def certificate(self) -> str:
        """``AWS::ACMPCA::CertificateAuthorityActivation.Certificate``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificate
        """
        return self._values.get('certificate')

    @builtins.property
    def certificate_authority_arn(self) -> str:
        """``AWS::ACMPCA::CertificateAuthorityActivation.CertificateAuthorityArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificateauthorityarn
        """
        return self._values.get('certificate_authority_arn')

    @builtins.property
    def certificate_chain(self) -> typing.Optional[str]:
        """``AWS::ACMPCA::CertificateAuthorityActivation.CertificateChain``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificatechain
        """
        return self._values.get('certificate_chain')

    @builtins.property
    def status(self) -> typing.Optional[str]:
        """``AWS::ACMPCA::CertificateAuthorityActivation.Status``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-status
        """
        return self._values.get('status')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnCertificateAuthorityActivationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_acmpca.CfnCertificateAuthorityProps", jsii_struct_bases=[], name_mapping={'key_algorithm': 'keyAlgorithm', 'signing_algorithm': 'signingAlgorithm', 'subject': 'subject', 'type': 'type', 'revocation_configuration': 'revocationConfiguration', 'tags': 'tags'})
class CfnCertificateAuthorityProps():
    def __init__(self, *, key_algorithm: str, signing_algorithm: str, subject: typing.Union["CfnCertificateAuthority.SubjectProperty", _IResolvable_9ceae33e], type: str, revocation_configuration: typing.Optional[typing.Union["CfnCertificateAuthority.RevocationConfigurationProperty", _IResolvable_9ceae33e]]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Properties for defining a ``AWS::ACMPCA::CertificateAuthority``.

        :param key_algorithm: ``AWS::ACMPCA::CertificateAuthority.KeyAlgorithm``.
        :param signing_algorithm: ``AWS::ACMPCA::CertificateAuthority.SigningAlgorithm``.
        :param subject: ``AWS::ACMPCA::CertificateAuthority.Subject``.
        :param type: ``AWS::ACMPCA::CertificateAuthority.Type``.
        :param revocation_configuration: ``AWS::ACMPCA::CertificateAuthority.RevocationConfiguration``.
        :param tags: ``AWS::ACMPCA::CertificateAuthority.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html
        """
        self._values = {
            'key_algorithm': key_algorithm,
            'signing_algorithm': signing_algorithm,
            'subject': subject,
            'type': type,
        }
        if revocation_configuration is not None: self._values["revocation_configuration"] = revocation_configuration
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def key_algorithm(self) -> str:
        """``AWS::ACMPCA::CertificateAuthority.KeyAlgorithm``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-keyalgorithm
        """
        return self._values.get('key_algorithm')

    @builtins.property
    def signing_algorithm(self) -> str:
        """``AWS::ACMPCA::CertificateAuthority.SigningAlgorithm``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-signingalgorithm
        """
        return self._values.get('signing_algorithm')

    @builtins.property
    def subject(self) -> typing.Union["CfnCertificateAuthority.SubjectProperty", _IResolvable_9ceae33e]:
        """``AWS::ACMPCA::CertificateAuthority.Subject``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-subject
        """
        return self._values.get('subject')

    @builtins.property
    def type(self) -> str:
        """``AWS::ACMPCA::CertificateAuthority.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-type
        """
        return self._values.get('type')

    @builtins.property
    def revocation_configuration(self) -> typing.Optional[typing.Union["CfnCertificateAuthority.RevocationConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::ACMPCA::CertificateAuthority.RevocationConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-revocationconfiguration
        """
        return self._values.get('revocation_configuration')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::ACMPCA::CertificateAuthority.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnCertificateAuthorityProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_acmpca.CfnCertificateProps", jsii_struct_bases=[], name_mapping={'certificate_authority_arn': 'certificateAuthorityArn', 'certificate_signing_request': 'certificateSigningRequest', 'signing_algorithm': 'signingAlgorithm', 'validity': 'validity', 'template_arn': 'templateArn'})
class CfnCertificateProps():
    def __init__(self, *, certificate_authority_arn: str, certificate_signing_request: str, signing_algorithm: str, validity: typing.Union["CfnCertificate.ValidityProperty", _IResolvable_9ceae33e], template_arn: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::ACMPCA::Certificate``.

        :param certificate_authority_arn: ``AWS::ACMPCA::Certificate.CertificateAuthorityArn``.
        :param certificate_signing_request: ``AWS::ACMPCA::Certificate.CertificateSigningRequest``.
        :param signing_algorithm: ``AWS::ACMPCA::Certificate.SigningAlgorithm``.
        :param validity: ``AWS::ACMPCA::Certificate.Validity``.
        :param template_arn: ``AWS::ACMPCA::Certificate.TemplateArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html
        """
        self._values = {
            'certificate_authority_arn': certificate_authority_arn,
            'certificate_signing_request': certificate_signing_request,
            'signing_algorithm': signing_algorithm,
            'validity': validity,
        }
        if template_arn is not None: self._values["template_arn"] = template_arn

    @builtins.property
    def certificate_authority_arn(self) -> str:
        """``AWS::ACMPCA::Certificate.CertificateAuthorityArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-certificateauthorityarn
        """
        return self._values.get('certificate_authority_arn')

    @builtins.property
    def certificate_signing_request(self) -> str:
        """``AWS::ACMPCA::Certificate.CertificateSigningRequest``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-certificatesigningrequest
        """
        return self._values.get('certificate_signing_request')

    @builtins.property
    def signing_algorithm(self) -> str:
        """``AWS::ACMPCA::Certificate.SigningAlgorithm``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-signingalgorithm
        """
        return self._values.get('signing_algorithm')

    @builtins.property
    def validity(self) -> typing.Union["CfnCertificate.ValidityProperty", _IResolvable_9ceae33e]:
        """``AWS::ACMPCA::Certificate.Validity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-validity
        """
        return self._values.get('validity')

    @builtins.property
    def template_arn(self) -> typing.Optional[str]:
        """``AWS::ACMPCA::Certificate.TemplateArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-templatearn
        """
        return self._values.get('template_arn')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnCertificateProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnCertificate",
    "CfnCertificateAuthority",
    "CfnCertificateAuthorityActivation",
    "CfnCertificateAuthorityActivationProps",
    "CfnCertificateAuthorityProps",
    "CfnCertificateProps",
]

publication.publish()
