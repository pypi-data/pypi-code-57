"""
## AWS IoT Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.
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

import aws_cdk.core


@jsii.implements(aws_cdk.core.IInspectable)
class CfnCertificate(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iot.CfnCertificate"):
    """A CloudFormation ``AWS::IoT::Certificate``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-certificate.html
    cloudformationResource:
    :cloudformationResource:: AWS::IoT::Certificate
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, certificate_signing_request: str, status: str) -> None:
        """Create a new ``AWS::IoT::Certificate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param certificate_signing_request: ``AWS::IoT::Certificate.CertificateSigningRequest``.
        :param status: ``AWS::IoT::Certificate.Status``.
        """
        props = CfnCertificateProps(certificate_signing_request=certificate_signing_request, status=status)

        jsii.create(CfnCertificate, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnCertificate":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="certificateSigningRequest")
    def certificate_signing_request(self) -> str:
        """``AWS::IoT::Certificate.CertificateSigningRequest``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-certificate.html#cfn-iot-certificate-certificatesigningrequest
        """
        return jsii.get(self, "certificateSigningRequest")

    @certificate_signing_request.setter
    def certificate_signing_request(self, value: str) -> None:
        jsii.set(self, "certificateSigningRequest", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> str:
        """``AWS::IoT::Certificate.Status``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-certificate.html#cfn-iot-certificate-status
        """
        return jsii.get(self, "status")

    @status.setter
    def status(self, value: str) -> None:
        jsii.set(self, "status", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnCertificateProps", jsii_struct_bases=[], name_mapping={'certificate_signing_request': 'certificateSigningRequest', 'status': 'status'})
class CfnCertificateProps():
    def __init__(self, *, certificate_signing_request: str, status: str) -> None:
        """Properties for defining a ``AWS::IoT::Certificate``.

        :param certificate_signing_request: ``AWS::IoT::Certificate.CertificateSigningRequest``.
        :param status: ``AWS::IoT::Certificate.Status``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-certificate.html
        """
        self._values = {
            'certificate_signing_request': certificate_signing_request,
            'status': status,
        }

    @builtins.property
    def certificate_signing_request(self) -> str:
        """``AWS::IoT::Certificate.CertificateSigningRequest``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-certificate.html#cfn-iot-certificate-certificatesigningrequest
        """
        return self._values.get('certificate_signing_request')

    @builtins.property
    def status(self) -> str:
        """``AWS::IoT::Certificate.Status``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-certificate.html#cfn-iot-certificate-status
        """
        return self._values.get('status')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnCertificateProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnPolicy(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iot.CfnPolicy"):
    """A CloudFormation ``AWS::IoT::Policy``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-policy.html
    cloudformationResource:
    :cloudformationResource:: AWS::IoT::Policy
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, policy_document: typing.Any, policy_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::IoT::Policy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy_document: ``AWS::IoT::Policy.PolicyDocument``.
        :param policy_name: ``AWS::IoT::Policy.PolicyName``.
        """
        props = CfnPolicyProps(policy_document=policy_document, policy_name=policy_name)

        jsii.create(CfnPolicy, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnPolicy":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="policyDocument")
    def policy_document(self) -> typing.Any:
        """``AWS::IoT::Policy.PolicyDocument``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-policy.html#cfn-iot-policy-policydocument
        """
        return jsii.get(self, "policyDocument")

    @policy_document.setter
    def policy_document(self, value: typing.Any) -> None:
        jsii.set(self, "policyDocument", value)

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> typing.Optional[str]:
        """``AWS::IoT::Policy.PolicyName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-policy.html#cfn-iot-policy-policyname
        """
        return jsii.get(self, "policyName")

    @policy_name.setter
    def policy_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "policyName", value)


@jsii.implements(aws_cdk.core.IInspectable)
class CfnPolicyPrincipalAttachment(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iot.CfnPolicyPrincipalAttachment"):
    """A CloudFormation ``AWS::IoT::PolicyPrincipalAttachment``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-policyprincipalattachment.html
    cloudformationResource:
    :cloudformationResource:: AWS::IoT::PolicyPrincipalAttachment
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, policy_name: str, principal: str) -> None:
        """Create a new ``AWS::IoT::PolicyPrincipalAttachment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy_name: ``AWS::IoT::PolicyPrincipalAttachment.PolicyName``.
        :param principal: ``AWS::IoT::PolicyPrincipalAttachment.Principal``.
        """
        props = CfnPolicyPrincipalAttachmentProps(policy_name=policy_name, principal=principal)

        jsii.create(CfnPolicyPrincipalAttachment, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnPolicyPrincipalAttachment":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
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
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> str:
        """``AWS::IoT::PolicyPrincipalAttachment.PolicyName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-policyprincipalattachment.html#cfn-iot-policyprincipalattachment-policyname
        """
        return jsii.get(self, "policyName")

    @policy_name.setter
    def policy_name(self, value: str) -> None:
        jsii.set(self, "policyName", value)

    @builtins.property
    @jsii.member(jsii_name="principal")
    def principal(self) -> str:
        """``AWS::IoT::PolicyPrincipalAttachment.Principal``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-policyprincipalattachment.html#cfn-iot-policyprincipalattachment-principal
        """
        return jsii.get(self, "principal")

    @principal.setter
    def principal(self, value: str) -> None:
        jsii.set(self, "principal", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnPolicyPrincipalAttachmentProps", jsii_struct_bases=[], name_mapping={'policy_name': 'policyName', 'principal': 'principal'})
class CfnPolicyPrincipalAttachmentProps():
    def __init__(self, *, policy_name: str, principal: str) -> None:
        """Properties for defining a ``AWS::IoT::PolicyPrincipalAttachment``.

        :param policy_name: ``AWS::IoT::PolicyPrincipalAttachment.PolicyName``.
        :param principal: ``AWS::IoT::PolicyPrincipalAttachment.Principal``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-policyprincipalattachment.html
        """
        self._values = {
            'policy_name': policy_name,
            'principal': principal,
        }

    @builtins.property
    def policy_name(self) -> str:
        """``AWS::IoT::PolicyPrincipalAttachment.PolicyName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-policyprincipalattachment.html#cfn-iot-policyprincipalattachment-policyname
        """
        return self._values.get('policy_name')

    @builtins.property
    def principal(self) -> str:
        """``AWS::IoT::PolicyPrincipalAttachment.Principal``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-policyprincipalattachment.html#cfn-iot-policyprincipalattachment-principal
        """
        return self._values.get('principal')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnPolicyPrincipalAttachmentProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnPolicyProps", jsii_struct_bases=[], name_mapping={'policy_document': 'policyDocument', 'policy_name': 'policyName'})
class CfnPolicyProps():
    def __init__(self, *, policy_document: typing.Any, policy_name: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::IoT::Policy``.

        :param policy_document: ``AWS::IoT::Policy.PolicyDocument``.
        :param policy_name: ``AWS::IoT::Policy.PolicyName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-policy.html
        """
        self._values = {
            'policy_document': policy_document,
        }
        if policy_name is not None: self._values["policy_name"] = policy_name

    @builtins.property
    def policy_document(self) -> typing.Any:
        """``AWS::IoT::Policy.PolicyDocument``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-policy.html#cfn-iot-policy-policydocument
        """
        return self._values.get('policy_document')

    @builtins.property
    def policy_name(self) -> typing.Optional[str]:
        """``AWS::IoT::Policy.PolicyName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-policy.html#cfn-iot-policy-policyname
        """
        return self._values.get('policy_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnPolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnProvisioningTemplate(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iot.CfnProvisioningTemplate"):
    """A CloudFormation ``AWS::IoT::ProvisioningTemplate``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-provisioningtemplate.html
    cloudformationResource:
    :cloudformationResource:: AWS::IoT::ProvisioningTemplate
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, provisioning_role_arn: str, template_body: str, description: typing.Optional[str]=None, enabled: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]=None, pre_provisioning_hook: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "ProvisioningHookProperty"]]=None, tags: typing.Optional[typing.List[typing.Any]]=None, template_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::IoT::ProvisioningTemplate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param provisioning_role_arn: ``AWS::IoT::ProvisioningTemplate.ProvisioningRoleArn``.
        :param template_body: ``AWS::IoT::ProvisioningTemplate.TemplateBody``.
        :param description: ``AWS::IoT::ProvisioningTemplate.Description``.
        :param enabled: ``AWS::IoT::ProvisioningTemplate.Enabled``.
        :param pre_provisioning_hook: ``AWS::IoT::ProvisioningTemplate.PreProvisioningHook``.
        :param tags: ``AWS::IoT::ProvisioningTemplate.Tags``.
        :param template_name: ``AWS::IoT::ProvisioningTemplate.TemplateName``.
        """
        props = CfnProvisioningTemplateProps(provisioning_role_arn=provisioning_role_arn, template_body=template_body, description=description, enabled=enabled, pre_provisioning_hook=pre_provisioning_hook, tags=tags, template_name=template_name)

        jsii.create(CfnProvisioningTemplate, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnProvisioningTemplate":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
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
    @jsii.member(jsii_name="attrTemplateArn")
    def attr_template_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: TemplateArn
        """
        return jsii.get(self, "attrTemplateArn")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="provisioningRoleArn")
    def provisioning_role_arn(self) -> str:
        """``AWS::IoT::ProvisioningTemplate.ProvisioningRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-provisioningtemplate.html#cfn-iot-provisioningtemplate-provisioningrolearn
        """
        return jsii.get(self, "provisioningRoleArn")

    @provisioning_role_arn.setter
    def provisioning_role_arn(self, value: str) -> None:
        jsii.set(self, "provisioningRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="templateBody")
    def template_body(self) -> str:
        """``AWS::IoT::ProvisioningTemplate.TemplateBody``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-provisioningtemplate.html#cfn-iot-provisioningtemplate-templatebody
        """
        return jsii.get(self, "templateBody")

    @template_body.setter
    def template_body(self, value: str) -> None:
        jsii.set(self, "templateBody", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::IoT::ProvisioningTemplate.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-provisioningtemplate.html#cfn-iot-provisioningtemplate-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::IoT::ProvisioningTemplate.Enabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-provisioningtemplate.html#cfn-iot-provisioningtemplate-enabled
        """
        return jsii.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]) -> None:
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="preProvisioningHook")
    def pre_provisioning_hook(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "ProvisioningHookProperty"]]:
        """``AWS::IoT::ProvisioningTemplate.PreProvisioningHook``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-provisioningtemplate.html#cfn-iot-provisioningtemplate-preprovisioninghook
        """
        return jsii.get(self, "preProvisioningHook")

    @pre_provisioning_hook.setter
    def pre_provisioning_hook(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "ProvisioningHookProperty"]]) -> None:
        jsii.set(self, "preProvisioningHook", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List[typing.Any]]:
        """``AWS::IoT::ProvisioningTemplate.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-provisioningtemplate.html#cfn-iot-provisioningtemplate-tags
        """
        return jsii.get(self, "tags")

    @tags.setter
    def tags(self, value: typing.Optional[typing.List[typing.Any]]) -> None:
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="templateName")
    def template_name(self) -> typing.Optional[str]:
        """``AWS::IoT::ProvisioningTemplate.TemplateName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-provisioningtemplate.html#cfn-iot-provisioningtemplate-templatename
        """
        return jsii.get(self, "templateName")

    @template_name.setter
    def template_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "templateName", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnProvisioningTemplate.ProvisioningHookProperty", jsii_struct_bases=[], name_mapping={'payload_version': 'payloadVersion', 'target_arn': 'targetArn'})
    class ProvisioningHookProperty():
        def __init__(self, *, payload_version: typing.Optional[str]=None, target_arn: typing.Optional[str]=None) -> None:
            """
            :param payload_version: ``CfnProvisioningTemplate.ProvisioningHookProperty.PayloadVersion``.
            :param target_arn: ``CfnProvisioningTemplate.ProvisioningHookProperty.TargetArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-provisioningtemplate-provisioninghook.html
            """
            self._values = {
            }
            if payload_version is not None: self._values["payload_version"] = payload_version
            if target_arn is not None: self._values["target_arn"] = target_arn

        @builtins.property
        def payload_version(self) -> typing.Optional[str]:
            """``CfnProvisioningTemplate.ProvisioningHookProperty.PayloadVersion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-provisioningtemplate-provisioninghook.html#cfn-iot-provisioningtemplate-provisioninghook-payloadversion
            """
            return self._values.get('payload_version')

        @builtins.property
        def target_arn(self) -> typing.Optional[str]:
            """``CfnProvisioningTemplate.ProvisioningHookProperty.TargetArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-provisioningtemplate-provisioninghook.html#cfn-iot-provisioningtemplate-provisioninghook-targetarn
            """
            return self._values.get('target_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ProvisioningHookProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnProvisioningTemplateProps", jsii_struct_bases=[], name_mapping={'provisioning_role_arn': 'provisioningRoleArn', 'template_body': 'templateBody', 'description': 'description', 'enabled': 'enabled', 'pre_provisioning_hook': 'preProvisioningHook', 'tags': 'tags', 'template_name': 'templateName'})
class CfnProvisioningTemplateProps():
    def __init__(self, *, provisioning_role_arn: str, template_body: str, description: typing.Optional[str]=None, enabled: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]=None, pre_provisioning_hook: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnProvisioningTemplate.ProvisioningHookProperty"]]=None, tags: typing.Optional[typing.List[typing.Any]]=None, template_name: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::IoT::ProvisioningTemplate``.

        :param provisioning_role_arn: ``AWS::IoT::ProvisioningTemplate.ProvisioningRoleArn``.
        :param template_body: ``AWS::IoT::ProvisioningTemplate.TemplateBody``.
        :param description: ``AWS::IoT::ProvisioningTemplate.Description``.
        :param enabled: ``AWS::IoT::ProvisioningTemplate.Enabled``.
        :param pre_provisioning_hook: ``AWS::IoT::ProvisioningTemplate.PreProvisioningHook``.
        :param tags: ``AWS::IoT::ProvisioningTemplate.Tags``.
        :param template_name: ``AWS::IoT::ProvisioningTemplate.TemplateName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-provisioningtemplate.html
        """
        self._values = {
            'provisioning_role_arn': provisioning_role_arn,
            'template_body': template_body,
        }
        if description is not None: self._values["description"] = description
        if enabled is not None: self._values["enabled"] = enabled
        if pre_provisioning_hook is not None: self._values["pre_provisioning_hook"] = pre_provisioning_hook
        if tags is not None: self._values["tags"] = tags
        if template_name is not None: self._values["template_name"] = template_name

    @builtins.property
    def provisioning_role_arn(self) -> str:
        """``AWS::IoT::ProvisioningTemplate.ProvisioningRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-provisioningtemplate.html#cfn-iot-provisioningtemplate-provisioningrolearn
        """
        return self._values.get('provisioning_role_arn')

    @builtins.property
    def template_body(self) -> str:
        """``AWS::IoT::ProvisioningTemplate.TemplateBody``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-provisioningtemplate.html#cfn-iot-provisioningtemplate-templatebody
        """
        return self._values.get('template_body')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::IoT::ProvisioningTemplate.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-provisioningtemplate.html#cfn-iot-provisioningtemplate-description
        """
        return self._values.get('description')

    @builtins.property
    def enabled(self) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::IoT::ProvisioningTemplate.Enabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-provisioningtemplate.html#cfn-iot-provisioningtemplate-enabled
        """
        return self._values.get('enabled')

    @builtins.property
    def pre_provisioning_hook(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnProvisioningTemplate.ProvisioningHookProperty"]]:
        """``AWS::IoT::ProvisioningTemplate.PreProvisioningHook``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-provisioningtemplate.html#cfn-iot-provisioningtemplate-preprovisioninghook
        """
        return self._values.get('pre_provisioning_hook')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[typing.Any]]:
        """``AWS::IoT::ProvisioningTemplate.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-provisioningtemplate.html#cfn-iot-provisioningtemplate-tags
        """
        return self._values.get('tags')

    @builtins.property
    def template_name(self) -> typing.Optional[str]:
        """``AWS::IoT::ProvisioningTemplate.TemplateName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-provisioningtemplate.html#cfn-iot-provisioningtemplate-templatename
        """
        return self._values.get('template_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnProvisioningTemplateProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnThing(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iot.CfnThing"):
    """A CloudFormation ``AWS::IoT::Thing``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-thing.html
    cloudformationResource:
    :cloudformationResource:: AWS::IoT::Thing
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, attribute_payload: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "AttributePayloadProperty"]]=None, thing_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::IoT::Thing``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param attribute_payload: ``AWS::IoT::Thing.AttributePayload``.
        :param thing_name: ``AWS::IoT::Thing.ThingName``.
        """
        props = CfnThingProps(attribute_payload=attribute_payload, thing_name=thing_name)

        jsii.create(CfnThing, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnThing":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
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
    @jsii.member(jsii_name="attributePayload")
    def attribute_payload(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "AttributePayloadProperty"]]:
        """``AWS::IoT::Thing.AttributePayload``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-thing.html#cfn-iot-thing-attributepayload
        """
        return jsii.get(self, "attributePayload")

    @attribute_payload.setter
    def attribute_payload(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "AttributePayloadProperty"]]) -> None:
        jsii.set(self, "attributePayload", value)

    @builtins.property
    @jsii.member(jsii_name="thingName")
    def thing_name(self) -> typing.Optional[str]:
        """``AWS::IoT::Thing.ThingName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-thing.html#cfn-iot-thing-thingname
        """
        return jsii.get(self, "thingName")

    @thing_name.setter
    def thing_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "thingName", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnThing.AttributePayloadProperty", jsii_struct_bases=[], name_mapping={'attributes': 'attributes'})
    class AttributePayloadProperty():
        def __init__(self, *, attributes: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[str, str]]]=None) -> None:
            """
            :param attributes: ``CfnThing.AttributePayloadProperty.Attributes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-thing-attributepayload.html
            """
            self._values = {
            }
            if attributes is not None: self._values["attributes"] = attributes

        @builtins.property
        def attributes(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[str, str]]]:
            """``CfnThing.AttributePayloadProperty.Attributes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-thing-attributepayload.html#cfn-iot-thing-attributepayload-attributes
            """
            return self._values.get('attributes')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AttributePayloadProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.implements(aws_cdk.core.IInspectable)
class CfnThingPrincipalAttachment(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iot.CfnThingPrincipalAttachment"):
    """A CloudFormation ``AWS::IoT::ThingPrincipalAttachment``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-thingprincipalattachment.html
    cloudformationResource:
    :cloudformationResource:: AWS::IoT::ThingPrincipalAttachment
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, principal: str, thing_name: str) -> None:
        """Create a new ``AWS::IoT::ThingPrincipalAttachment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param principal: ``AWS::IoT::ThingPrincipalAttachment.Principal``.
        :param thing_name: ``AWS::IoT::ThingPrincipalAttachment.ThingName``.
        """
        props = CfnThingPrincipalAttachmentProps(principal=principal, thing_name=thing_name)

        jsii.create(CfnThingPrincipalAttachment, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnThingPrincipalAttachment":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
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
    @jsii.member(jsii_name="principal")
    def principal(self) -> str:
        """``AWS::IoT::ThingPrincipalAttachment.Principal``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-thingprincipalattachment.html#cfn-iot-thingprincipalattachment-principal
        """
        return jsii.get(self, "principal")

    @principal.setter
    def principal(self, value: str) -> None:
        jsii.set(self, "principal", value)

    @builtins.property
    @jsii.member(jsii_name="thingName")
    def thing_name(self) -> str:
        """``AWS::IoT::ThingPrincipalAttachment.ThingName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-thingprincipalattachment.html#cfn-iot-thingprincipalattachment-thingname
        """
        return jsii.get(self, "thingName")

    @thing_name.setter
    def thing_name(self, value: str) -> None:
        jsii.set(self, "thingName", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnThingPrincipalAttachmentProps", jsii_struct_bases=[], name_mapping={'principal': 'principal', 'thing_name': 'thingName'})
class CfnThingPrincipalAttachmentProps():
    def __init__(self, *, principal: str, thing_name: str) -> None:
        """Properties for defining a ``AWS::IoT::ThingPrincipalAttachment``.

        :param principal: ``AWS::IoT::ThingPrincipalAttachment.Principal``.
        :param thing_name: ``AWS::IoT::ThingPrincipalAttachment.ThingName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-thingprincipalattachment.html
        """
        self._values = {
            'principal': principal,
            'thing_name': thing_name,
        }

    @builtins.property
    def principal(self) -> str:
        """``AWS::IoT::ThingPrincipalAttachment.Principal``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-thingprincipalattachment.html#cfn-iot-thingprincipalattachment-principal
        """
        return self._values.get('principal')

    @builtins.property
    def thing_name(self) -> str:
        """``AWS::IoT::ThingPrincipalAttachment.ThingName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-thingprincipalattachment.html#cfn-iot-thingprincipalattachment-thingname
        """
        return self._values.get('thing_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnThingPrincipalAttachmentProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnThingProps", jsii_struct_bases=[], name_mapping={'attribute_payload': 'attributePayload', 'thing_name': 'thingName'})
class CfnThingProps():
    def __init__(self, *, attribute_payload: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnThing.AttributePayloadProperty"]]=None, thing_name: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::IoT::Thing``.

        :param attribute_payload: ``AWS::IoT::Thing.AttributePayload``.
        :param thing_name: ``AWS::IoT::Thing.ThingName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-thing.html
        """
        self._values = {
        }
        if attribute_payload is not None: self._values["attribute_payload"] = attribute_payload
        if thing_name is not None: self._values["thing_name"] = thing_name

    @builtins.property
    def attribute_payload(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnThing.AttributePayloadProperty"]]:
        """``AWS::IoT::Thing.AttributePayload``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-thing.html#cfn-iot-thing-attributepayload
        """
        return self._values.get('attribute_payload')

    @builtins.property
    def thing_name(self) -> typing.Optional[str]:
        """``AWS::IoT::Thing.ThingName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-thing.html#cfn-iot-thing-thingname
        """
        return self._values.get('thing_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnThingProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnTopicRule(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iot.CfnTopicRule"):
    """A CloudFormation ``AWS::IoT::TopicRule``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-topicrule.html
    cloudformationResource:
    :cloudformationResource:: AWS::IoT::TopicRule
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, topic_rule_payload: typing.Union[aws_cdk.core.IResolvable, "TopicRulePayloadProperty"], rule_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::IoT::TopicRule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param topic_rule_payload: ``AWS::IoT::TopicRule.TopicRulePayload``.
        :param rule_name: ``AWS::IoT::TopicRule.RuleName``.
        """
        props = CfnTopicRuleProps(topic_rule_payload=topic_rule_payload, rule_name=rule_name)

        jsii.create(CfnTopicRule, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnTopicRule":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="topicRulePayload")
    def topic_rule_payload(self) -> typing.Union[aws_cdk.core.IResolvable, "TopicRulePayloadProperty"]:
        """``AWS::IoT::TopicRule.TopicRulePayload``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-topicrule.html#cfn-iot-topicrule-topicrulepayload
        """
        return jsii.get(self, "topicRulePayload")

    @topic_rule_payload.setter
    def topic_rule_payload(self, value: typing.Union[aws_cdk.core.IResolvable, "TopicRulePayloadProperty"]) -> None:
        jsii.set(self, "topicRulePayload", value)

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> typing.Optional[str]:
        """``AWS::IoT::TopicRule.RuleName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-topicrule.html#cfn-iot-topicrule-rulename
        """
        return jsii.get(self, "ruleName")

    @rule_name.setter
    def rule_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "ruleName", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.ActionProperty", jsii_struct_bases=[], name_mapping={'cloudwatch_alarm': 'cloudwatchAlarm', 'cloudwatch_metric': 'cloudwatchMetric', 'dynamo_db': 'dynamoDb', 'dynamo_d_bv2': 'dynamoDBv2', 'elasticsearch': 'elasticsearch', 'firehose': 'firehose', 'http': 'http', 'iot_analytics': 'iotAnalytics', 'iot_events': 'iotEvents', 'iot_site_wise': 'iotSiteWise', 'kinesis': 'kinesis', 'lambda_': 'lambda', 'republish': 'republish', 's3': 's3', 'sns': 'sns', 'sqs': 'sqs', 'step_functions': 'stepFunctions'})
    class ActionProperty():
        def __init__(self, *, cloudwatch_alarm: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.CloudwatchAlarmActionProperty"]]=None, cloudwatch_metric: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.CloudwatchMetricActionProperty"]]=None, dynamo_db: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.DynamoDBActionProperty"]]=None, dynamo_d_bv2: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.DynamoDBv2ActionProperty"]]=None, elasticsearch: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.ElasticsearchActionProperty"]]=None, firehose: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.FirehoseActionProperty"]]=None, http: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.HttpActionProperty"]]=None, iot_analytics: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.IotAnalyticsActionProperty"]]=None, iot_events: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.IotEventsActionProperty"]]=None, iot_site_wise: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.IotSiteWiseActionProperty"]]=None, kinesis: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.KinesisActionProperty"]]=None, lambda_: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.LambdaActionProperty"]]=None, republish: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.RepublishActionProperty"]]=None, s3: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.S3ActionProperty"]]=None, sns: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.SnsActionProperty"]]=None, sqs: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.SqsActionProperty"]]=None, step_functions: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.StepFunctionsActionProperty"]]=None) -> None:
            """
            :param cloudwatch_alarm: ``CfnTopicRule.ActionProperty.CloudwatchAlarm``.
            :param cloudwatch_metric: ``CfnTopicRule.ActionProperty.CloudwatchMetric``.
            :param dynamo_db: ``CfnTopicRule.ActionProperty.DynamoDB``.
            :param dynamo_d_bv2: ``CfnTopicRule.ActionProperty.DynamoDBv2``.
            :param elasticsearch: ``CfnTopicRule.ActionProperty.Elasticsearch``.
            :param firehose: ``CfnTopicRule.ActionProperty.Firehose``.
            :param http: ``CfnTopicRule.ActionProperty.Http``.
            :param iot_analytics: ``CfnTopicRule.ActionProperty.IotAnalytics``.
            :param iot_events: ``CfnTopicRule.ActionProperty.IotEvents``.
            :param iot_site_wise: ``CfnTopicRule.ActionProperty.IotSiteWise``.
            :param kinesis: ``CfnTopicRule.ActionProperty.Kinesis``.
            :param lambda_: ``CfnTopicRule.ActionProperty.Lambda``.
            :param republish: ``CfnTopicRule.ActionProperty.Republish``.
            :param s3: ``CfnTopicRule.ActionProperty.S3``.
            :param sns: ``CfnTopicRule.ActionProperty.Sns``.
            :param sqs: ``CfnTopicRule.ActionProperty.Sqs``.
            :param step_functions: ``CfnTopicRule.ActionProperty.StepFunctions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html
            """
            self._values = {
            }
            if cloudwatch_alarm is not None: self._values["cloudwatch_alarm"] = cloudwatch_alarm
            if cloudwatch_metric is not None: self._values["cloudwatch_metric"] = cloudwatch_metric
            if dynamo_db is not None: self._values["dynamo_db"] = dynamo_db
            if dynamo_d_bv2 is not None: self._values["dynamo_d_bv2"] = dynamo_d_bv2
            if elasticsearch is not None: self._values["elasticsearch"] = elasticsearch
            if firehose is not None: self._values["firehose"] = firehose
            if http is not None: self._values["http"] = http
            if iot_analytics is not None: self._values["iot_analytics"] = iot_analytics
            if iot_events is not None: self._values["iot_events"] = iot_events
            if iot_site_wise is not None: self._values["iot_site_wise"] = iot_site_wise
            if kinesis is not None: self._values["kinesis"] = kinesis
            if lambda_ is not None: self._values["lambda_"] = lambda_
            if republish is not None: self._values["republish"] = republish
            if s3 is not None: self._values["s3"] = s3
            if sns is not None: self._values["sns"] = sns
            if sqs is not None: self._values["sqs"] = sqs
            if step_functions is not None: self._values["step_functions"] = step_functions

        @builtins.property
        def cloudwatch_alarm(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.CloudwatchAlarmActionProperty"]]:
            """``CfnTopicRule.ActionProperty.CloudwatchAlarm``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-cloudwatchalarm
            """
            return self._values.get('cloudwatch_alarm')

        @builtins.property
        def cloudwatch_metric(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.CloudwatchMetricActionProperty"]]:
            """``CfnTopicRule.ActionProperty.CloudwatchMetric``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-cloudwatchmetric
            """
            return self._values.get('cloudwatch_metric')

        @builtins.property
        def dynamo_db(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.DynamoDBActionProperty"]]:
            """``CfnTopicRule.ActionProperty.DynamoDB``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-dynamodb
            """
            return self._values.get('dynamo_db')

        @builtins.property
        def dynamo_d_bv2(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.DynamoDBv2ActionProperty"]]:
            """``CfnTopicRule.ActionProperty.DynamoDBv2``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-dynamodbv2
            """
            return self._values.get('dynamo_d_bv2')

        @builtins.property
        def elasticsearch(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.ElasticsearchActionProperty"]]:
            """``CfnTopicRule.ActionProperty.Elasticsearch``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-elasticsearch
            """
            return self._values.get('elasticsearch')

        @builtins.property
        def firehose(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.FirehoseActionProperty"]]:
            """``CfnTopicRule.ActionProperty.Firehose``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-firehose
            """
            return self._values.get('firehose')

        @builtins.property
        def http(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.HttpActionProperty"]]:
            """``CfnTopicRule.ActionProperty.Http``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-http
            """
            return self._values.get('http')

        @builtins.property
        def iot_analytics(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.IotAnalyticsActionProperty"]]:
            """``CfnTopicRule.ActionProperty.IotAnalytics``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-iotanalytics
            """
            return self._values.get('iot_analytics')

        @builtins.property
        def iot_events(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.IotEventsActionProperty"]]:
            """``CfnTopicRule.ActionProperty.IotEvents``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-iotevents
            """
            return self._values.get('iot_events')

        @builtins.property
        def iot_site_wise(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.IotSiteWiseActionProperty"]]:
            """``CfnTopicRule.ActionProperty.IotSiteWise``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-iotsitewise
            """
            return self._values.get('iot_site_wise')

        @builtins.property
        def kinesis(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.KinesisActionProperty"]]:
            """``CfnTopicRule.ActionProperty.Kinesis``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-kinesis
            """
            return self._values.get('kinesis')

        @builtins.property
        def lambda_(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.LambdaActionProperty"]]:
            """``CfnTopicRule.ActionProperty.Lambda``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-lambda
            """
            return self._values.get('lambda_')

        @builtins.property
        def republish(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.RepublishActionProperty"]]:
            """``CfnTopicRule.ActionProperty.Republish``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-republish
            """
            return self._values.get('republish')

        @builtins.property
        def s3(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.S3ActionProperty"]]:
            """``CfnTopicRule.ActionProperty.S3``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-s3
            """
            return self._values.get('s3')

        @builtins.property
        def sns(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.SnsActionProperty"]]:
            """``CfnTopicRule.ActionProperty.Sns``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-sns
            """
            return self._values.get('sns')

        @builtins.property
        def sqs(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.SqsActionProperty"]]:
            """``CfnTopicRule.ActionProperty.Sqs``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-sqs
            """
            return self._values.get('sqs')

        @builtins.property
        def step_functions(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.StepFunctionsActionProperty"]]:
            """``CfnTopicRule.ActionProperty.StepFunctions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-stepfunctions
            """
            return self._values.get('step_functions')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.AssetPropertyTimestampProperty", jsii_struct_bases=[], name_mapping={'time_in_seconds': 'timeInSeconds', 'offset_in_nanos': 'offsetInNanos'})
    class AssetPropertyTimestampProperty():
        def __init__(self, *, time_in_seconds: str, offset_in_nanos: typing.Optional[str]=None) -> None:
            """
            :param time_in_seconds: ``CfnTopicRule.AssetPropertyTimestampProperty.TimeInSeconds``.
            :param offset_in_nanos: ``CfnTopicRule.AssetPropertyTimestampProperty.OffsetInNanos``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-assetpropertytimestamp.html
            """
            self._values = {
                'time_in_seconds': time_in_seconds,
            }
            if offset_in_nanos is not None: self._values["offset_in_nanos"] = offset_in_nanos

        @builtins.property
        def time_in_seconds(self) -> str:
            """``CfnTopicRule.AssetPropertyTimestampProperty.TimeInSeconds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-assetpropertytimestamp.html#cfn-iot-topicrule-assetpropertytimestamp-timeinseconds
            """
            return self._values.get('time_in_seconds')

        @builtins.property
        def offset_in_nanos(self) -> typing.Optional[str]:
            """``CfnTopicRule.AssetPropertyTimestampProperty.OffsetInNanos``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-assetpropertytimestamp.html#cfn-iot-topicrule-assetpropertytimestamp-offsetinnanos
            """
            return self._values.get('offset_in_nanos')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AssetPropertyTimestampProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.AssetPropertyValueProperty", jsii_struct_bases=[], name_mapping={'timestamp': 'timestamp', 'value': 'value', 'quality': 'quality'})
    class AssetPropertyValueProperty():
        def __init__(self, *, timestamp: typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.AssetPropertyTimestampProperty"], value: typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.AssetPropertyVariantProperty"], quality: typing.Optional[str]=None) -> None:
            """
            :param timestamp: ``CfnTopicRule.AssetPropertyValueProperty.Timestamp``.
            :param value: ``CfnTopicRule.AssetPropertyValueProperty.Value``.
            :param quality: ``CfnTopicRule.AssetPropertyValueProperty.Quality``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-assetpropertyvalue.html
            """
            self._values = {
                'timestamp': timestamp,
                'value': value,
            }
            if quality is not None: self._values["quality"] = quality

        @builtins.property
        def timestamp(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.AssetPropertyTimestampProperty"]:
            """``CfnTopicRule.AssetPropertyValueProperty.Timestamp``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-assetpropertyvalue.html#cfn-iot-topicrule-assetpropertyvalue-timestamp
            """
            return self._values.get('timestamp')

        @builtins.property
        def value(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.AssetPropertyVariantProperty"]:
            """``CfnTopicRule.AssetPropertyValueProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-assetpropertyvalue.html#cfn-iot-topicrule-assetpropertyvalue-value
            """
            return self._values.get('value')

        @builtins.property
        def quality(self) -> typing.Optional[str]:
            """``CfnTopicRule.AssetPropertyValueProperty.Quality``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-assetpropertyvalue.html#cfn-iot-topicrule-assetpropertyvalue-quality
            """
            return self._values.get('quality')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AssetPropertyValueProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.AssetPropertyVariantProperty", jsii_struct_bases=[], name_mapping={'boolean_value': 'booleanValue', 'double_value': 'doubleValue', 'integer_value': 'integerValue', 'string_value': 'stringValue'})
    class AssetPropertyVariantProperty():
        def __init__(self, *, boolean_value: typing.Optional[str]=None, double_value: typing.Optional[str]=None, integer_value: typing.Optional[str]=None, string_value: typing.Optional[str]=None) -> None:
            """
            :param boolean_value: ``CfnTopicRule.AssetPropertyVariantProperty.BooleanValue``.
            :param double_value: ``CfnTopicRule.AssetPropertyVariantProperty.DoubleValue``.
            :param integer_value: ``CfnTopicRule.AssetPropertyVariantProperty.IntegerValue``.
            :param string_value: ``CfnTopicRule.AssetPropertyVariantProperty.StringValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-assetpropertyvariant.html
            """
            self._values = {
            }
            if boolean_value is not None: self._values["boolean_value"] = boolean_value
            if double_value is not None: self._values["double_value"] = double_value
            if integer_value is not None: self._values["integer_value"] = integer_value
            if string_value is not None: self._values["string_value"] = string_value

        @builtins.property
        def boolean_value(self) -> typing.Optional[str]:
            """``CfnTopicRule.AssetPropertyVariantProperty.BooleanValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-assetpropertyvariant.html#cfn-iot-topicrule-assetpropertyvariant-booleanvalue
            """
            return self._values.get('boolean_value')

        @builtins.property
        def double_value(self) -> typing.Optional[str]:
            """``CfnTopicRule.AssetPropertyVariantProperty.DoubleValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-assetpropertyvariant.html#cfn-iot-topicrule-assetpropertyvariant-doublevalue
            """
            return self._values.get('double_value')

        @builtins.property
        def integer_value(self) -> typing.Optional[str]:
            """``CfnTopicRule.AssetPropertyVariantProperty.IntegerValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-assetpropertyvariant.html#cfn-iot-topicrule-assetpropertyvariant-integervalue
            """
            return self._values.get('integer_value')

        @builtins.property
        def string_value(self) -> typing.Optional[str]:
            """``CfnTopicRule.AssetPropertyVariantProperty.StringValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-assetpropertyvariant.html#cfn-iot-topicrule-assetpropertyvariant-stringvalue
            """
            return self._values.get('string_value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AssetPropertyVariantProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.CloudwatchAlarmActionProperty", jsii_struct_bases=[], name_mapping={'alarm_name': 'alarmName', 'role_arn': 'roleArn', 'state_reason': 'stateReason', 'state_value': 'stateValue'})
    class CloudwatchAlarmActionProperty():
        def __init__(self, *, alarm_name: str, role_arn: str, state_reason: str, state_value: str) -> None:
            """
            :param alarm_name: ``CfnTopicRule.CloudwatchAlarmActionProperty.AlarmName``.
            :param role_arn: ``CfnTopicRule.CloudwatchAlarmActionProperty.RoleArn``.
            :param state_reason: ``CfnTopicRule.CloudwatchAlarmActionProperty.StateReason``.
            :param state_value: ``CfnTopicRule.CloudwatchAlarmActionProperty.StateValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-cloudwatchalarmaction.html
            """
            self._values = {
                'alarm_name': alarm_name,
                'role_arn': role_arn,
                'state_reason': state_reason,
                'state_value': state_value,
            }

        @builtins.property
        def alarm_name(self) -> str:
            """``CfnTopicRule.CloudwatchAlarmActionProperty.AlarmName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-cloudwatchalarmaction.html#cfn-iot-topicrule-cloudwatchalarmaction-alarmname
            """
            return self._values.get('alarm_name')

        @builtins.property
        def role_arn(self) -> str:
            """``CfnTopicRule.CloudwatchAlarmActionProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-cloudwatchalarmaction.html#cfn-iot-topicrule-cloudwatchalarmaction-rolearn
            """
            return self._values.get('role_arn')

        @builtins.property
        def state_reason(self) -> str:
            """``CfnTopicRule.CloudwatchAlarmActionProperty.StateReason``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-cloudwatchalarmaction.html#cfn-iot-topicrule-cloudwatchalarmaction-statereason
            """
            return self._values.get('state_reason')

        @builtins.property
        def state_value(self) -> str:
            """``CfnTopicRule.CloudwatchAlarmActionProperty.StateValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-cloudwatchalarmaction.html#cfn-iot-topicrule-cloudwatchalarmaction-statevalue
            """
            return self._values.get('state_value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CloudwatchAlarmActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.CloudwatchMetricActionProperty", jsii_struct_bases=[], name_mapping={'metric_name': 'metricName', 'metric_namespace': 'metricNamespace', 'metric_unit': 'metricUnit', 'metric_value': 'metricValue', 'role_arn': 'roleArn', 'metric_timestamp': 'metricTimestamp'})
    class CloudwatchMetricActionProperty():
        def __init__(self, *, metric_name: str, metric_namespace: str, metric_unit: str, metric_value: str, role_arn: str, metric_timestamp: typing.Optional[str]=None) -> None:
            """
            :param metric_name: ``CfnTopicRule.CloudwatchMetricActionProperty.MetricName``.
            :param metric_namespace: ``CfnTopicRule.CloudwatchMetricActionProperty.MetricNamespace``.
            :param metric_unit: ``CfnTopicRule.CloudwatchMetricActionProperty.MetricUnit``.
            :param metric_value: ``CfnTopicRule.CloudwatchMetricActionProperty.MetricValue``.
            :param role_arn: ``CfnTopicRule.CloudwatchMetricActionProperty.RoleArn``.
            :param metric_timestamp: ``CfnTopicRule.CloudwatchMetricActionProperty.MetricTimestamp``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-cloudwatchmetricaction.html
            """
            self._values = {
                'metric_name': metric_name,
                'metric_namespace': metric_namespace,
                'metric_unit': metric_unit,
                'metric_value': metric_value,
                'role_arn': role_arn,
            }
            if metric_timestamp is not None: self._values["metric_timestamp"] = metric_timestamp

        @builtins.property
        def metric_name(self) -> str:
            """``CfnTopicRule.CloudwatchMetricActionProperty.MetricName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-cloudwatchmetricaction.html#cfn-iot-topicrule-cloudwatchmetricaction-metricname
            """
            return self._values.get('metric_name')

        @builtins.property
        def metric_namespace(self) -> str:
            """``CfnTopicRule.CloudwatchMetricActionProperty.MetricNamespace``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-cloudwatchmetricaction.html#cfn-iot-topicrule-cloudwatchmetricaction-metricnamespace
            """
            return self._values.get('metric_namespace')

        @builtins.property
        def metric_unit(self) -> str:
            """``CfnTopicRule.CloudwatchMetricActionProperty.MetricUnit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-cloudwatchmetricaction.html#cfn-iot-topicrule-cloudwatchmetricaction-metricunit
            """
            return self._values.get('metric_unit')

        @builtins.property
        def metric_value(self) -> str:
            """``CfnTopicRule.CloudwatchMetricActionProperty.MetricValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-cloudwatchmetricaction.html#cfn-iot-topicrule-cloudwatchmetricaction-metricvalue
            """
            return self._values.get('metric_value')

        @builtins.property
        def role_arn(self) -> str:
            """``CfnTopicRule.CloudwatchMetricActionProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-cloudwatchmetricaction.html#cfn-iot-topicrule-cloudwatchmetricaction-rolearn
            """
            return self._values.get('role_arn')

        @builtins.property
        def metric_timestamp(self) -> typing.Optional[str]:
            """``CfnTopicRule.CloudwatchMetricActionProperty.MetricTimestamp``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-cloudwatchmetricaction.html#cfn-iot-topicrule-cloudwatchmetricaction-metrictimestamp
            """
            return self._values.get('metric_timestamp')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CloudwatchMetricActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.DynamoDBActionProperty", jsii_struct_bases=[], name_mapping={'hash_key_field': 'hashKeyField', 'hash_key_value': 'hashKeyValue', 'role_arn': 'roleArn', 'table_name': 'tableName', 'hash_key_type': 'hashKeyType', 'payload_field': 'payloadField', 'range_key_field': 'rangeKeyField', 'range_key_type': 'rangeKeyType', 'range_key_value': 'rangeKeyValue'})
    class DynamoDBActionProperty():
        def __init__(self, *, hash_key_field: str, hash_key_value: str, role_arn: str, table_name: str, hash_key_type: typing.Optional[str]=None, payload_field: typing.Optional[str]=None, range_key_field: typing.Optional[str]=None, range_key_type: typing.Optional[str]=None, range_key_value: typing.Optional[str]=None) -> None:
            """
            :param hash_key_field: ``CfnTopicRule.DynamoDBActionProperty.HashKeyField``.
            :param hash_key_value: ``CfnTopicRule.DynamoDBActionProperty.HashKeyValue``.
            :param role_arn: ``CfnTopicRule.DynamoDBActionProperty.RoleArn``.
            :param table_name: ``CfnTopicRule.DynamoDBActionProperty.TableName``.
            :param hash_key_type: ``CfnTopicRule.DynamoDBActionProperty.HashKeyType``.
            :param payload_field: ``CfnTopicRule.DynamoDBActionProperty.PayloadField``.
            :param range_key_field: ``CfnTopicRule.DynamoDBActionProperty.RangeKeyField``.
            :param range_key_type: ``CfnTopicRule.DynamoDBActionProperty.RangeKeyType``.
            :param range_key_value: ``CfnTopicRule.DynamoDBActionProperty.RangeKeyValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbaction.html
            """
            self._values = {
                'hash_key_field': hash_key_field,
                'hash_key_value': hash_key_value,
                'role_arn': role_arn,
                'table_name': table_name,
            }
            if hash_key_type is not None: self._values["hash_key_type"] = hash_key_type
            if payload_field is not None: self._values["payload_field"] = payload_field
            if range_key_field is not None: self._values["range_key_field"] = range_key_field
            if range_key_type is not None: self._values["range_key_type"] = range_key_type
            if range_key_value is not None: self._values["range_key_value"] = range_key_value

        @builtins.property
        def hash_key_field(self) -> str:
            """``CfnTopicRule.DynamoDBActionProperty.HashKeyField``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbaction.html#cfn-iot-topicrule-dynamodbaction-hashkeyfield
            """
            return self._values.get('hash_key_field')

        @builtins.property
        def hash_key_value(self) -> str:
            """``CfnTopicRule.DynamoDBActionProperty.HashKeyValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbaction.html#cfn-iot-topicrule-dynamodbaction-hashkeyvalue
            """
            return self._values.get('hash_key_value')

        @builtins.property
        def role_arn(self) -> str:
            """``CfnTopicRule.DynamoDBActionProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbaction.html#cfn-iot-topicrule-dynamodbaction-rolearn
            """
            return self._values.get('role_arn')

        @builtins.property
        def table_name(self) -> str:
            """``CfnTopicRule.DynamoDBActionProperty.TableName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbaction.html#cfn-iot-topicrule-dynamodbaction-tablename
            """
            return self._values.get('table_name')

        @builtins.property
        def hash_key_type(self) -> typing.Optional[str]:
            """``CfnTopicRule.DynamoDBActionProperty.HashKeyType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbaction.html#cfn-iot-topicrule-dynamodbaction-hashkeytype
            """
            return self._values.get('hash_key_type')

        @builtins.property
        def payload_field(self) -> typing.Optional[str]:
            """``CfnTopicRule.DynamoDBActionProperty.PayloadField``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbaction.html#cfn-iot-topicrule-dynamodbaction-payloadfield
            """
            return self._values.get('payload_field')

        @builtins.property
        def range_key_field(self) -> typing.Optional[str]:
            """``CfnTopicRule.DynamoDBActionProperty.RangeKeyField``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbaction.html#cfn-iot-topicrule-dynamodbaction-rangekeyfield
            """
            return self._values.get('range_key_field')

        @builtins.property
        def range_key_type(self) -> typing.Optional[str]:
            """``CfnTopicRule.DynamoDBActionProperty.RangeKeyType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbaction.html#cfn-iot-topicrule-dynamodbaction-rangekeytype
            """
            return self._values.get('range_key_type')

        @builtins.property
        def range_key_value(self) -> typing.Optional[str]:
            """``CfnTopicRule.DynamoDBActionProperty.RangeKeyValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbaction.html#cfn-iot-topicrule-dynamodbaction-rangekeyvalue
            """
            return self._values.get('range_key_value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DynamoDBActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.DynamoDBv2ActionProperty", jsii_struct_bases=[], name_mapping={'put_item': 'putItem', 'role_arn': 'roleArn'})
    class DynamoDBv2ActionProperty():
        def __init__(self, *, put_item: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.PutItemInputProperty"]]=None, role_arn: typing.Optional[str]=None) -> None:
            """
            :param put_item: ``CfnTopicRule.DynamoDBv2ActionProperty.PutItem``.
            :param role_arn: ``CfnTopicRule.DynamoDBv2ActionProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbv2action.html
            """
            self._values = {
            }
            if put_item is not None: self._values["put_item"] = put_item
            if role_arn is not None: self._values["role_arn"] = role_arn

        @builtins.property
        def put_item(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.PutItemInputProperty"]]:
            """``CfnTopicRule.DynamoDBv2ActionProperty.PutItem``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbv2action.html#cfn-iot-topicrule-dynamodbv2action-putitem
            """
            return self._values.get('put_item')

        @builtins.property
        def role_arn(self) -> typing.Optional[str]:
            """``CfnTopicRule.DynamoDBv2ActionProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbv2action.html#cfn-iot-topicrule-dynamodbv2action-rolearn
            """
            return self._values.get('role_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DynamoDBv2ActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.ElasticsearchActionProperty", jsii_struct_bases=[], name_mapping={'endpoint': 'endpoint', 'id': 'id', 'index': 'index', 'role_arn': 'roleArn', 'type': 'type'})
    class ElasticsearchActionProperty():
        def __init__(self, *, endpoint: str, id: str, index: str, role_arn: str, type: str) -> None:
            """
            :param endpoint: ``CfnTopicRule.ElasticsearchActionProperty.Endpoint``.
            :param id: ``CfnTopicRule.ElasticsearchActionProperty.Id``.
            :param index: ``CfnTopicRule.ElasticsearchActionProperty.Index``.
            :param role_arn: ``CfnTopicRule.ElasticsearchActionProperty.RoleArn``.
            :param type: ``CfnTopicRule.ElasticsearchActionProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-elasticsearchaction.html
            """
            self._values = {
                'endpoint': endpoint,
                'id': id,
                'index': index,
                'role_arn': role_arn,
                'type': type,
            }

        @builtins.property
        def endpoint(self) -> str:
            """``CfnTopicRule.ElasticsearchActionProperty.Endpoint``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-elasticsearchaction.html#cfn-iot-topicrule-elasticsearchaction-endpoint
            """
            return self._values.get('endpoint')

        @builtins.property
        def id(self) -> str:
            """``CfnTopicRule.ElasticsearchActionProperty.Id``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-elasticsearchaction.html#cfn-iot-topicrule-elasticsearchaction-id
            """
            return self._values.get('id')

        @builtins.property
        def index(self) -> str:
            """``CfnTopicRule.ElasticsearchActionProperty.Index``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-elasticsearchaction.html#cfn-iot-topicrule-elasticsearchaction-index
            """
            return self._values.get('index')

        @builtins.property
        def role_arn(self) -> str:
            """``CfnTopicRule.ElasticsearchActionProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-elasticsearchaction.html#cfn-iot-topicrule-elasticsearchaction-rolearn
            """
            return self._values.get('role_arn')

        @builtins.property
        def type(self) -> str:
            """``CfnTopicRule.ElasticsearchActionProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-elasticsearchaction.html#cfn-iot-topicrule-elasticsearchaction-type
            """
            return self._values.get('type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ElasticsearchActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.FirehoseActionProperty", jsii_struct_bases=[], name_mapping={'delivery_stream_name': 'deliveryStreamName', 'role_arn': 'roleArn', 'separator': 'separator'})
    class FirehoseActionProperty():
        def __init__(self, *, delivery_stream_name: str, role_arn: str, separator: typing.Optional[str]=None) -> None:
            """
            :param delivery_stream_name: ``CfnTopicRule.FirehoseActionProperty.DeliveryStreamName``.
            :param role_arn: ``CfnTopicRule.FirehoseActionProperty.RoleArn``.
            :param separator: ``CfnTopicRule.FirehoseActionProperty.Separator``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-firehoseaction.html
            """
            self._values = {
                'delivery_stream_name': delivery_stream_name,
                'role_arn': role_arn,
            }
            if separator is not None: self._values["separator"] = separator

        @builtins.property
        def delivery_stream_name(self) -> str:
            """``CfnTopicRule.FirehoseActionProperty.DeliveryStreamName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-firehoseaction.html#cfn-iot-topicrule-firehoseaction-deliverystreamname
            """
            return self._values.get('delivery_stream_name')

        @builtins.property
        def role_arn(self) -> str:
            """``CfnTopicRule.FirehoseActionProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-firehoseaction.html#cfn-iot-topicrule-firehoseaction-rolearn
            """
            return self._values.get('role_arn')

        @builtins.property
        def separator(self) -> typing.Optional[str]:
            """``CfnTopicRule.FirehoseActionProperty.Separator``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-firehoseaction.html#cfn-iot-topicrule-firehoseaction-separator
            """
            return self._values.get('separator')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'FirehoseActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.HttpActionHeaderProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value'})
    class HttpActionHeaderProperty():
        def __init__(self, *, key: str, value: str) -> None:
            """
            :param key: ``CfnTopicRule.HttpActionHeaderProperty.Key``.
            :param value: ``CfnTopicRule.HttpActionHeaderProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-httpactionheader.html
            """
            self._values = {
                'key': key,
                'value': value,
            }

        @builtins.property
        def key(self) -> str:
            """``CfnTopicRule.HttpActionHeaderProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-httpactionheader.html#cfn-iot-topicrule-httpactionheader-key
            """
            return self._values.get('key')

        @builtins.property
        def value(self) -> str:
            """``CfnTopicRule.HttpActionHeaderProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-httpactionheader.html#cfn-iot-topicrule-httpactionheader-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HttpActionHeaderProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.HttpActionProperty", jsii_struct_bases=[], name_mapping={'url': 'url', 'auth': 'auth', 'confirmation_url': 'confirmationUrl', 'headers': 'headers'})
    class HttpActionProperty():
        def __init__(self, *, url: str, auth: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.HttpAuthorizationProperty"]]=None, confirmation_url: typing.Optional[str]=None, headers: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.HttpActionHeaderProperty"]]]]=None) -> None:
            """
            :param url: ``CfnTopicRule.HttpActionProperty.Url``.
            :param auth: ``CfnTopicRule.HttpActionProperty.Auth``.
            :param confirmation_url: ``CfnTopicRule.HttpActionProperty.ConfirmationUrl``.
            :param headers: ``CfnTopicRule.HttpActionProperty.Headers``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-httpaction.html
            """
            self._values = {
                'url': url,
            }
            if auth is not None: self._values["auth"] = auth
            if confirmation_url is not None: self._values["confirmation_url"] = confirmation_url
            if headers is not None: self._values["headers"] = headers

        @builtins.property
        def url(self) -> str:
            """``CfnTopicRule.HttpActionProperty.Url``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-httpaction.html#cfn-iot-topicrule-httpaction-url
            """
            return self._values.get('url')

        @builtins.property
        def auth(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.HttpAuthorizationProperty"]]:
            """``CfnTopicRule.HttpActionProperty.Auth``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-httpaction.html#cfn-iot-topicrule-httpaction-auth
            """
            return self._values.get('auth')

        @builtins.property
        def confirmation_url(self) -> typing.Optional[str]:
            """``CfnTopicRule.HttpActionProperty.ConfirmationUrl``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-httpaction.html#cfn-iot-topicrule-httpaction-confirmationurl
            """
            return self._values.get('confirmation_url')

        @builtins.property
        def headers(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.HttpActionHeaderProperty"]]]]:
            """``CfnTopicRule.HttpActionProperty.Headers``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-httpaction.html#cfn-iot-topicrule-httpaction-headers
            """
            return self._values.get('headers')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HttpActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.HttpAuthorizationProperty", jsii_struct_bases=[], name_mapping={'sigv4': 'sigv4'})
    class HttpAuthorizationProperty():
        def __init__(self, *, sigv4: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.SigV4AuthorizationProperty"]]=None) -> None:
            """
            :param sigv4: ``CfnTopicRule.HttpAuthorizationProperty.Sigv4``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-httpauthorization.html
            """
            self._values = {
            }
            if sigv4 is not None: self._values["sigv4"] = sigv4

        @builtins.property
        def sigv4(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.SigV4AuthorizationProperty"]]:
            """``CfnTopicRule.HttpAuthorizationProperty.Sigv4``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-httpauthorization.html#cfn-iot-topicrule-httpauthorization-sigv4
            """
            return self._values.get('sigv4')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HttpAuthorizationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.IotAnalyticsActionProperty", jsii_struct_bases=[], name_mapping={'channel_name': 'channelName', 'role_arn': 'roleArn'})
    class IotAnalyticsActionProperty():
        def __init__(self, *, channel_name: str, role_arn: str) -> None:
            """
            :param channel_name: ``CfnTopicRule.IotAnalyticsActionProperty.ChannelName``.
            :param role_arn: ``CfnTopicRule.IotAnalyticsActionProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-iotanalyticsaction.html
            """
            self._values = {
                'channel_name': channel_name,
                'role_arn': role_arn,
            }

        @builtins.property
        def channel_name(self) -> str:
            """``CfnTopicRule.IotAnalyticsActionProperty.ChannelName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-iotanalyticsaction.html#cfn-iot-topicrule-iotanalyticsaction-channelname
            """
            return self._values.get('channel_name')

        @builtins.property
        def role_arn(self) -> str:
            """``CfnTopicRule.IotAnalyticsActionProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-iotanalyticsaction.html#cfn-iot-topicrule-iotanalyticsaction-rolearn
            """
            return self._values.get('role_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'IotAnalyticsActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.IotEventsActionProperty", jsii_struct_bases=[], name_mapping={'input_name': 'inputName', 'role_arn': 'roleArn', 'message_id': 'messageId'})
    class IotEventsActionProperty():
        def __init__(self, *, input_name: str, role_arn: str, message_id: typing.Optional[str]=None) -> None:
            """
            :param input_name: ``CfnTopicRule.IotEventsActionProperty.InputName``.
            :param role_arn: ``CfnTopicRule.IotEventsActionProperty.RoleArn``.
            :param message_id: ``CfnTopicRule.IotEventsActionProperty.MessageId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-ioteventsaction.html
            """
            self._values = {
                'input_name': input_name,
                'role_arn': role_arn,
            }
            if message_id is not None: self._values["message_id"] = message_id

        @builtins.property
        def input_name(self) -> str:
            """``CfnTopicRule.IotEventsActionProperty.InputName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-ioteventsaction.html#cfn-iot-topicrule-ioteventsaction-inputname
            """
            return self._values.get('input_name')

        @builtins.property
        def role_arn(self) -> str:
            """``CfnTopicRule.IotEventsActionProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-ioteventsaction.html#cfn-iot-topicrule-ioteventsaction-rolearn
            """
            return self._values.get('role_arn')

        @builtins.property
        def message_id(self) -> typing.Optional[str]:
            """``CfnTopicRule.IotEventsActionProperty.MessageId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-ioteventsaction.html#cfn-iot-topicrule-ioteventsaction-messageid
            """
            return self._values.get('message_id')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'IotEventsActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.IotSiteWiseActionProperty", jsii_struct_bases=[], name_mapping={'put_asset_property_value_entries': 'putAssetPropertyValueEntries', 'role_arn': 'roleArn'})
    class IotSiteWiseActionProperty():
        def __init__(self, *, put_asset_property_value_entries: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.PutAssetPropertyValueEntryProperty"]]], role_arn: str) -> None:
            """
            :param put_asset_property_value_entries: ``CfnTopicRule.IotSiteWiseActionProperty.PutAssetPropertyValueEntries``.
            :param role_arn: ``CfnTopicRule.IotSiteWiseActionProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-iotsitewiseaction.html
            """
            self._values = {
                'put_asset_property_value_entries': put_asset_property_value_entries,
                'role_arn': role_arn,
            }

        @builtins.property
        def put_asset_property_value_entries(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.PutAssetPropertyValueEntryProperty"]]]:
            """``CfnTopicRule.IotSiteWiseActionProperty.PutAssetPropertyValueEntries``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-iotsitewiseaction.html#cfn-iot-topicrule-iotsitewiseaction-putassetpropertyvalueentries
            """
            return self._values.get('put_asset_property_value_entries')

        @builtins.property
        def role_arn(self) -> str:
            """``CfnTopicRule.IotSiteWiseActionProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-iotsitewiseaction.html#cfn-iot-topicrule-iotsitewiseaction-rolearn
            """
            return self._values.get('role_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'IotSiteWiseActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.KinesisActionProperty", jsii_struct_bases=[], name_mapping={'role_arn': 'roleArn', 'stream_name': 'streamName', 'partition_key': 'partitionKey'})
    class KinesisActionProperty():
        def __init__(self, *, role_arn: str, stream_name: str, partition_key: typing.Optional[str]=None) -> None:
            """
            :param role_arn: ``CfnTopicRule.KinesisActionProperty.RoleArn``.
            :param stream_name: ``CfnTopicRule.KinesisActionProperty.StreamName``.
            :param partition_key: ``CfnTopicRule.KinesisActionProperty.PartitionKey``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-kinesisaction.html
            """
            self._values = {
                'role_arn': role_arn,
                'stream_name': stream_name,
            }
            if partition_key is not None: self._values["partition_key"] = partition_key

        @builtins.property
        def role_arn(self) -> str:
            """``CfnTopicRule.KinesisActionProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-kinesisaction.html#cfn-iot-topicrule-kinesisaction-rolearn
            """
            return self._values.get('role_arn')

        @builtins.property
        def stream_name(self) -> str:
            """``CfnTopicRule.KinesisActionProperty.StreamName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-kinesisaction.html#cfn-iot-topicrule-kinesisaction-streamname
            """
            return self._values.get('stream_name')

        @builtins.property
        def partition_key(self) -> typing.Optional[str]:
            """``CfnTopicRule.KinesisActionProperty.PartitionKey``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-kinesisaction.html#cfn-iot-topicrule-kinesisaction-partitionkey
            """
            return self._values.get('partition_key')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'KinesisActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.LambdaActionProperty", jsii_struct_bases=[], name_mapping={'function_arn': 'functionArn'})
    class LambdaActionProperty():
        def __init__(self, *, function_arn: typing.Optional[str]=None) -> None:
            """
            :param function_arn: ``CfnTopicRule.LambdaActionProperty.FunctionArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-lambdaaction.html
            """
            self._values = {
            }
            if function_arn is not None: self._values["function_arn"] = function_arn

        @builtins.property
        def function_arn(self) -> typing.Optional[str]:
            """``CfnTopicRule.LambdaActionProperty.FunctionArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-lambdaaction.html#cfn-iot-topicrule-lambdaaction-functionarn
            """
            return self._values.get('function_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LambdaActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.PutAssetPropertyValueEntryProperty", jsii_struct_bases=[], name_mapping={'property_values': 'propertyValues', 'asset_id': 'assetId', 'entry_id': 'entryId', 'property_alias': 'propertyAlias', 'property_id': 'propertyId'})
    class PutAssetPropertyValueEntryProperty():
        def __init__(self, *, property_values: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.AssetPropertyValueProperty"]]], asset_id: typing.Optional[str]=None, entry_id: typing.Optional[str]=None, property_alias: typing.Optional[str]=None, property_id: typing.Optional[str]=None) -> None:
            """
            :param property_values: ``CfnTopicRule.PutAssetPropertyValueEntryProperty.PropertyValues``.
            :param asset_id: ``CfnTopicRule.PutAssetPropertyValueEntryProperty.AssetId``.
            :param entry_id: ``CfnTopicRule.PutAssetPropertyValueEntryProperty.EntryId``.
            :param property_alias: ``CfnTopicRule.PutAssetPropertyValueEntryProperty.PropertyAlias``.
            :param property_id: ``CfnTopicRule.PutAssetPropertyValueEntryProperty.PropertyId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-putassetpropertyvalueentry.html
            """
            self._values = {
                'property_values': property_values,
            }
            if asset_id is not None: self._values["asset_id"] = asset_id
            if entry_id is not None: self._values["entry_id"] = entry_id
            if property_alias is not None: self._values["property_alias"] = property_alias
            if property_id is not None: self._values["property_id"] = property_id

        @builtins.property
        def property_values(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.AssetPropertyValueProperty"]]]:
            """``CfnTopicRule.PutAssetPropertyValueEntryProperty.PropertyValues``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-putassetpropertyvalueentry.html#cfn-iot-topicrule-putassetpropertyvalueentry-propertyvalues
            """
            return self._values.get('property_values')

        @builtins.property
        def asset_id(self) -> typing.Optional[str]:
            """``CfnTopicRule.PutAssetPropertyValueEntryProperty.AssetId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-putassetpropertyvalueentry.html#cfn-iot-topicrule-putassetpropertyvalueentry-assetid
            """
            return self._values.get('asset_id')

        @builtins.property
        def entry_id(self) -> typing.Optional[str]:
            """``CfnTopicRule.PutAssetPropertyValueEntryProperty.EntryId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-putassetpropertyvalueentry.html#cfn-iot-topicrule-putassetpropertyvalueentry-entryid
            """
            return self._values.get('entry_id')

        @builtins.property
        def property_alias(self) -> typing.Optional[str]:
            """``CfnTopicRule.PutAssetPropertyValueEntryProperty.PropertyAlias``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-putassetpropertyvalueentry.html#cfn-iot-topicrule-putassetpropertyvalueentry-propertyalias
            """
            return self._values.get('property_alias')

        @builtins.property
        def property_id(self) -> typing.Optional[str]:
            """``CfnTopicRule.PutAssetPropertyValueEntryProperty.PropertyId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-putassetpropertyvalueentry.html#cfn-iot-topicrule-putassetpropertyvalueentry-propertyid
            """
            return self._values.get('property_id')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PutAssetPropertyValueEntryProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.PutItemInputProperty", jsii_struct_bases=[], name_mapping={'table_name': 'tableName'})
    class PutItemInputProperty():
        def __init__(self, *, table_name: str) -> None:
            """
            :param table_name: ``CfnTopicRule.PutItemInputProperty.TableName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-putiteminput.html
            """
            self._values = {
                'table_name': table_name,
            }

        @builtins.property
        def table_name(self) -> str:
            """``CfnTopicRule.PutItemInputProperty.TableName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-putiteminput.html#cfn-iot-topicrule-putiteminput-tablename
            """
            return self._values.get('table_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PutItemInputProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.RepublishActionProperty", jsii_struct_bases=[], name_mapping={'role_arn': 'roleArn', 'topic': 'topic', 'qos': 'qos'})
    class RepublishActionProperty():
        def __init__(self, *, role_arn: str, topic: str, qos: typing.Optional[jsii.Number]=None) -> None:
            """
            :param role_arn: ``CfnTopicRule.RepublishActionProperty.RoleArn``.
            :param topic: ``CfnTopicRule.RepublishActionProperty.Topic``.
            :param qos: ``CfnTopicRule.RepublishActionProperty.Qos``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-republishaction.html
            """
            self._values = {
                'role_arn': role_arn,
                'topic': topic,
            }
            if qos is not None: self._values["qos"] = qos

        @builtins.property
        def role_arn(self) -> str:
            """``CfnTopicRule.RepublishActionProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-republishaction.html#cfn-iot-topicrule-republishaction-rolearn
            """
            return self._values.get('role_arn')

        @builtins.property
        def topic(self) -> str:
            """``CfnTopicRule.RepublishActionProperty.Topic``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-republishaction.html#cfn-iot-topicrule-republishaction-topic
            """
            return self._values.get('topic')

        @builtins.property
        def qos(self) -> typing.Optional[jsii.Number]:
            """``CfnTopicRule.RepublishActionProperty.Qos``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-republishaction.html#cfn-iot-topicrule-republishaction-qos
            """
            return self._values.get('qos')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RepublishActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.S3ActionProperty", jsii_struct_bases=[], name_mapping={'bucket_name': 'bucketName', 'key': 'key', 'role_arn': 'roleArn'})
    class S3ActionProperty():
        def __init__(self, *, bucket_name: str, key: str, role_arn: str) -> None:
            """
            :param bucket_name: ``CfnTopicRule.S3ActionProperty.BucketName``.
            :param key: ``CfnTopicRule.S3ActionProperty.Key``.
            :param role_arn: ``CfnTopicRule.S3ActionProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-s3action.html
            """
            self._values = {
                'bucket_name': bucket_name,
                'key': key,
                'role_arn': role_arn,
            }

        @builtins.property
        def bucket_name(self) -> str:
            """``CfnTopicRule.S3ActionProperty.BucketName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-s3action.html#cfn-iot-topicrule-s3action-bucketname
            """
            return self._values.get('bucket_name')

        @builtins.property
        def key(self) -> str:
            """``CfnTopicRule.S3ActionProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-s3action.html#cfn-iot-topicrule-s3action-key
            """
            return self._values.get('key')

        @builtins.property
        def role_arn(self) -> str:
            """``CfnTopicRule.S3ActionProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-s3action.html#cfn-iot-topicrule-s3action-rolearn
            """
            return self._values.get('role_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'S3ActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.SigV4AuthorizationProperty", jsii_struct_bases=[], name_mapping={'role_arn': 'roleArn', 'service_name': 'serviceName', 'signing_region': 'signingRegion'})
    class SigV4AuthorizationProperty():
        def __init__(self, *, role_arn: str, service_name: str, signing_region: str) -> None:
            """
            :param role_arn: ``CfnTopicRule.SigV4AuthorizationProperty.RoleArn``.
            :param service_name: ``CfnTopicRule.SigV4AuthorizationProperty.ServiceName``.
            :param signing_region: ``CfnTopicRule.SigV4AuthorizationProperty.SigningRegion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-sigv4authorization.html
            """
            self._values = {
                'role_arn': role_arn,
                'service_name': service_name,
                'signing_region': signing_region,
            }

        @builtins.property
        def role_arn(self) -> str:
            """``CfnTopicRule.SigV4AuthorizationProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-sigv4authorization.html#cfn-iot-topicrule-sigv4authorization-rolearn
            """
            return self._values.get('role_arn')

        @builtins.property
        def service_name(self) -> str:
            """``CfnTopicRule.SigV4AuthorizationProperty.ServiceName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-sigv4authorization.html#cfn-iot-topicrule-sigv4authorization-servicename
            """
            return self._values.get('service_name')

        @builtins.property
        def signing_region(self) -> str:
            """``CfnTopicRule.SigV4AuthorizationProperty.SigningRegion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-sigv4authorization.html#cfn-iot-topicrule-sigv4authorization-signingregion
            """
            return self._values.get('signing_region')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SigV4AuthorizationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.SnsActionProperty", jsii_struct_bases=[], name_mapping={'role_arn': 'roleArn', 'target_arn': 'targetArn', 'message_format': 'messageFormat'})
    class SnsActionProperty():
        def __init__(self, *, role_arn: str, target_arn: str, message_format: typing.Optional[str]=None) -> None:
            """
            :param role_arn: ``CfnTopicRule.SnsActionProperty.RoleArn``.
            :param target_arn: ``CfnTopicRule.SnsActionProperty.TargetArn``.
            :param message_format: ``CfnTopicRule.SnsActionProperty.MessageFormat``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-snsaction.html
            """
            self._values = {
                'role_arn': role_arn,
                'target_arn': target_arn,
            }
            if message_format is not None: self._values["message_format"] = message_format

        @builtins.property
        def role_arn(self) -> str:
            """``CfnTopicRule.SnsActionProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-snsaction.html#cfn-iot-topicrule-snsaction-rolearn
            """
            return self._values.get('role_arn')

        @builtins.property
        def target_arn(self) -> str:
            """``CfnTopicRule.SnsActionProperty.TargetArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-snsaction.html#cfn-iot-topicrule-snsaction-targetarn
            """
            return self._values.get('target_arn')

        @builtins.property
        def message_format(self) -> typing.Optional[str]:
            """``CfnTopicRule.SnsActionProperty.MessageFormat``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-snsaction.html#cfn-iot-topicrule-snsaction-messageformat
            """
            return self._values.get('message_format')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SnsActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.SqsActionProperty", jsii_struct_bases=[], name_mapping={'queue_url': 'queueUrl', 'role_arn': 'roleArn', 'use_base64': 'useBase64'})
    class SqsActionProperty():
        def __init__(self, *, queue_url: str, role_arn: str, use_base64: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]=None) -> None:
            """
            :param queue_url: ``CfnTopicRule.SqsActionProperty.QueueUrl``.
            :param role_arn: ``CfnTopicRule.SqsActionProperty.RoleArn``.
            :param use_base64: ``CfnTopicRule.SqsActionProperty.UseBase64``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-sqsaction.html
            """
            self._values = {
                'queue_url': queue_url,
                'role_arn': role_arn,
            }
            if use_base64 is not None: self._values["use_base64"] = use_base64

        @builtins.property
        def queue_url(self) -> str:
            """``CfnTopicRule.SqsActionProperty.QueueUrl``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-sqsaction.html#cfn-iot-topicrule-sqsaction-queueurl
            """
            return self._values.get('queue_url')

        @builtins.property
        def role_arn(self) -> str:
            """``CfnTopicRule.SqsActionProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-sqsaction.html#cfn-iot-topicrule-sqsaction-rolearn
            """
            return self._values.get('role_arn')

        @builtins.property
        def use_base64(self) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
            """``CfnTopicRule.SqsActionProperty.UseBase64``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-sqsaction.html#cfn-iot-topicrule-sqsaction-usebase64
            """
            return self._values.get('use_base64')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SqsActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.StepFunctionsActionProperty", jsii_struct_bases=[], name_mapping={'role_arn': 'roleArn', 'state_machine_name': 'stateMachineName', 'execution_name_prefix': 'executionNamePrefix'})
    class StepFunctionsActionProperty():
        def __init__(self, *, role_arn: str, state_machine_name: str, execution_name_prefix: typing.Optional[str]=None) -> None:
            """
            :param role_arn: ``CfnTopicRule.StepFunctionsActionProperty.RoleArn``.
            :param state_machine_name: ``CfnTopicRule.StepFunctionsActionProperty.StateMachineName``.
            :param execution_name_prefix: ``CfnTopicRule.StepFunctionsActionProperty.ExecutionNamePrefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-stepfunctionsaction.html
            """
            self._values = {
                'role_arn': role_arn,
                'state_machine_name': state_machine_name,
            }
            if execution_name_prefix is not None: self._values["execution_name_prefix"] = execution_name_prefix

        @builtins.property
        def role_arn(self) -> str:
            """``CfnTopicRule.StepFunctionsActionProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-stepfunctionsaction.html#cfn-iot-topicrule-stepfunctionsaction-rolearn
            """
            return self._values.get('role_arn')

        @builtins.property
        def state_machine_name(self) -> str:
            """``CfnTopicRule.StepFunctionsActionProperty.StateMachineName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-stepfunctionsaction.html#cfn-iot-topicrule-stepfunctionsaction-statemachinename
            """
            return self._values.get('state_machine_name')

        @builtins.property
        def execution_name_prefix(self) -> typing.Optional[str]:
            """``CfnTopicRule.StepFunctionsActionProperty.ExecutionNamePrefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-stepfunctionsaction.html#cfn-iot-topicrule-stepfunctionsaction-executionnameprefix
            """
            return self._values.get('execution_name_prefix')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'StepFunctionsActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.TopicRulePayloadProperty", jsii_struct_bases=[], name_mapping={'actions': 'actions', 'rule_disabled': 'ruleDisabled', 'sql': 'sql', 'aws_iot_sql_version': 'awsIotSqlVersion', 'description': 'description', 'error_action': 'errorAction'})
    class TopicRulePayloadProperty():
        def __init__(self, *, actions: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.ActionProperty"]]], rule_disabled: typing.Union[bool, aws_cdk.core.IResolvable], sql: str, aws_iot_sql_version: typing.Optional[str]=None, description: typing.Optional[str]=None, error_action: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.ActionProperty"]]=None) -> None:
            """
            :param actions: ``CfnTopicRule.TopicRulePayloadProperty.Actions``.
            :param rule_disabled: ``CfnTopicRule.TopicRulePayloadProperty.RuleDisabled``.
            :param sql: ``CfnTopicRule.TopicRulePayloadProperty.Sql``.
            :param aws_iot_sql_version: ``CfnTopicRule.TopicRulePayloadProperty.AwsIotSqlVersion``.
            :param description: ``CfnTopicRule.TopicRulePayloadProperty.Description``.
            :param error_action: ``CfnTopicRule.TopicRulePayloadProperty.ErrorAction``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-topicrulepayload.html
            """
            self._values = {
                'actions': actions,
                'rule_disabled': rule_disabled,
                'sql': sql,
            }
            if aws_iot_sql_version is not None: self._values["aws_iot_sql_version"] = aws_iot_sql_version
            if description is not None: self._values["description"] = description
            if error_action is not None: self._values["error_action"] = error_action

        @builtins.property
        def actions(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.ActionProperty"]]]:
            """``CfnTopicRule.TopicRulePayloadProperty.Actions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-topicrulepayload.html#cfn-iot-topicrule-topicrulepayload-actions
            """
            return self._values.get('actions')

        @builtins.property
        def rule_disabled(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
            """``CfnTopicRule.TopicRulePayloadProperty.RuleDisabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-topicrulepayload.html#cfn-iot-topicrule-topicrulepayload-ruledisabled
            """
            return self._values.get('rule_disabled')

        @builtins.property
        def sql(self) -> str:
            """``CfnTopicRule.TopicRulePayloadProperty.Sql``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-topicrulepayload.html#cfn-iot-topicrule-topicrulepayload-sql
            """
            return self._values.get('sql')

        @builtins.property
        def aws_iot_sql_version(self) -> typing.Optional[str]:
            """``CfnTopicRule.TopicRulePayloadProperty.AwsIotSqlVersion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-topicrulepayload.html#cfn-iot-topicrule-topicrulepayload-awsiotsqlversion
            """
            return self._values.get('aws_iot_sql_version')

        @builtins.property
        def description(self) -> typing.Optional[str]:
            """``CfnTopicRule.TopicRulePayloadProperty.Description``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-topicrulepayload.html#cfn-iot-topicrule-topicrulepayload-description
            """
            return self._values.get('description')

        @builtins.property
        def error_action(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.ActionProperty"]]:
            """``CfnTopicRule.TopicRulePayloadProperty.ErrorAction``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-topicrulepayload.html#cfn-iot-topicrule-topicrulepayload-erroraction
            """
            return self._values.get('error_action')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TopicRulePayloadProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRuleProps", jsii_struct_bases=[], name_mapping={'topic_rule_payload': 'topicRulePayload', 'rule_name': 'ruleName'})
class CfnTopicRuleProps():
    def __init__(self, *, topic_rule_payload: typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.TopicRulePayloadProperty"], rule_name: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::IoT::TopicRule``.

        :param topic_rule_payload: ``AWS::IoT::TopicRule.TopicRulePayload``.
        :param rule_name: ``AWS::IoT::TopicRule.RuleName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-topicrule.html
        """
        self._values = {
            'topic_rule_payload': topic_rule_payload,
        }
        if rule_name is not None: self._values["rule_name"] = rule_name

    @builtins.property
    def topic_rule_payload(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnTopicRule.TopicRulePayloadProperty"]:
        """``AWS::IoT::TopicRule.TopicRulePayload``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-topicrule.html#cfn-iot-topicrule-topicrulepayload
        """
        return self._values.get('topic_rule_payload')

    @builtins.property
    def rule_name(self) -> typing.Optional[str]:
        """``AWS::IoT::TopicRule.RuleName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-topicrule.html#cfn-iot-topicrule-rulename
        """
        return self._values.get('rule_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnTopicRuleProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnCertificate",
    "CfnCertificateProps",
    "CfnPolicy",
    "CfnPolicyPrincipalAttachment",
    "CfnPolicyPrincipalAttachmentProps",
    "CfnPolicyProps",
    "CfnProvisioningTemplate",
    "CfnProvisioningTemplateProps",
    "CfnThing",
    "CfnThingPrincipalAttachment",
    "CfnThingPrincipalAttachmentProps",
    "CfnThingProps",
    "CfnTopicRule",
    "CfnTopicRuleProps",
]

publication.publish()
