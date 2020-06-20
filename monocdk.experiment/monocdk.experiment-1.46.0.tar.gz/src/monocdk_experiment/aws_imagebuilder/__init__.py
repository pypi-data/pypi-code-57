import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (CfnResource as _CfnResource_7760e8e4, Construct as _Construct_f50a3f53, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, IResolvable as _IResolvable_9ceae33e, TagManager as _TagManager_2508893f, IInspectable as _IInspectable_051e6ed8)


@jsii.implements(_IInspectable_051e6ed8)
class CfnComponent(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_imagebuilder.CfnComponent"):
    """A CloudFormation ``AWS::ImageBuilder::Component``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html
    cloudformationResource:
    :cloudformationResource:: AWS::ImageBuilder::Component
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, name: str, platform: str, version: str, change_description: typing.Optional[str]=None, data: typing.Optional[str]=None, description: typing.Optional[str]=None, kms_key_id: typing.Optional[str]=None, tags: typing.Optional[typing.Mapping[str, str]]=None, uri: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ImageBuilder::Component``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::ImageBuilder::Component.Name``.
        :param platform: ``AWS::ImageBuilder::Component.Platform``.
        :param version: ``AWS::ImageBuilder::Component.Version``.
        :param change_description: ``AWS::ImageBuilder::Component.ChangeDescription``.
        :param data: ``AWS::ImageBuilder::Component.Data``.
        :param description: ``AWS::ImageBuilder::Component.Description``.
        :param kms_key_id: ``AWS::ImageBuilder::Component.KmsKeyId``.
        :param tags: ``AWS::ImageBuilder::Component.Tags``.
        :param uri: ``AWS::ImageBuilder::Component.Uri``.
        """
        props = CfnComponentProps(name=name, platform=platform, version=version, change_description=change_description, data=data, description=description, kms_key_id=kms_key_id, tags=tags, uri=uri)

        jsii.create(CfnComponent, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnComponent":
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
    @jsii.member(jsii_name="attrEncrypted")
    def attr_encrypted(self) -> _IResolvable_9ceae33e:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Encrypted
        """
        return jsii.get(self, "attrEncrypted")

    @builtins.property
    @jsii.member(jsii_name="attrType")
    def attr_type(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Type
        """
        return jsii.get(self, "attrType")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::ImageBuilder::Component.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::ImageBuilder::Component.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> str:
        """``AWS::ImageBuilder::Component.Platform``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-platform
        """
        return jsii.get(self, "platform")

    @platform.setter
    def platform(self, value: str) -> None:
        jsii.set(self, "platform", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> str:
        """``AWS::ImageBuilder::Component.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-version
        """
        return jsii.get(self, "version")

    @version.setter
    def version(self, value: str) -> None:
        jsii.set(self, "version", value)

    @builtins.property
    @jsii.member(jsii_name="changeDescription")
    def change_description(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::Component.ChangeDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-changedescription
        """
        return jsii.get(self, "changeDescription")

    @change_description.setter
    def change_description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "changeDescription", value)

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::Component.Data``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-data
        """
        return jsii.get(self, "data")

    @data.setter
    def data(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "data", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::Component.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::Component.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-kmskeyid
        """
        return jsii.get(self, "kmsKeyId")

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::Component.Uri``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-uri
        """
        return jsii.get(self, "uri")

    @uri.setter
    def uri(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "uri", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_imagebuilder.CfnComponentProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'platform': 'platform', 'version': 'version', 'change_description': 'changeDescription', 'data': 'data', 'description': 'description', 'kms_key_id': 'kmsKeyId', 'tags': 'tags', 'uri': 'uri'})
class CfnComponentProps():
    def __init__(self, *, name: str, platform: str, version: str, change_description: typing.Optional[str]=None, data: typing.Optional[str]=None, description: typing.Optional[str]=None, kms_key_id: typing.Optional[str]=None, tags: typing.Optional[typing.Mapping[str, str]]=None, uri: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::ImageBuilder::Component``.

        :param name: ``AWS::ImageBuilder::Component.Name``.
        :param platform: ``AWS::ImageBuilder::Component.Platform``.
        :param version: ``AWS::ImageBuilder::Component.Version``.
        :param change_description: ``AWS::ImageBuilder::Component.ChangeDescription``.
        :param data: ``AWS::ImageBuilder::Component.Data``.
        :param description: ``AWS::ImageBuilder::Component.Description``.
        :param kms_key_id: ``AWS::ImageBuilder::Component.KmsKeyId``.
        :param tags: ``AWS::ImageBuilder::Component.Tags``.
        :param uri: ``AWS::ImageBuilder::Component.Uri``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html
        """
        self._values = {
            'name': name,
            'platform': platform,
            'version': version,
        }
        if change_description is not None: self._values["change_description"] = change_description
        if data is not None: self._values["data"] = data
        if description is not None: self._values["description"] = description
        if kms_key_id is not None: self._values["kms_key_id"] = kms_key_id
        if tags is not None: self._values["tags"] = tags
        if uri is not None: self._values["uri"] = uri

    @builtins.property
    def name(self) -> str:
        """``AWS::ImageBuilder::Component.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-name
        """
        return self._values.get('name')

    @builtins.property
    def platform(self) -> str:
        """``AWS::ImageBuilder::Component.Platform``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-platform
        """
        return self._values.get('platform')

    @builtins.property
    def version(self) -> str:
        """``AWS::ImageBuilder::Component.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-version
        """
        return self._values.get('version')

    @builtins.property
    def change_description(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::Component.ChangeDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-changedescription
        """
        return self._values.get('change_description')

    @builtins.property
    def data(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::Component.Data``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-data
        """
        return self._values.get('data')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::Component.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-description
        """
        return self._values.get('description')

    @builtins.property
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::Component.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-kmskeyid
        """
        return self._values.get('kms_key_id')

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[str, str]]:
        """``AWS::ImageBuilder::Component.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-tags
        """
        return self._values.get('tags')

    @builtins.property
    def uri(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::Component.Uri``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-uri
        """
        return self._values.get('uri')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnComponentProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnDistributionConfiguration(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_imagebuilder.CfnDistributionConfiguration"):
    """A CloudFormation ``AWS::ImageBuilder::DistributionConfiguration``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-distributionconfiguration.html
    cloudformationResource:
    :cloudformationResource:: AWS::ImageBuilder::DistributionConfiguration
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, distributions: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["DistributionProperty", _IResolvable_9ceae33e]]], name: str, description: typing.Optional[str]=None, tags: typing.Optional[typing.Mapping[str, str]]=None) -> None:
        """Create a new ``AWS::ImageBuilder::DistributionConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param distributions: ``AWS::ImageBuilder::DistributionConfiguration.Distributions``.
        :param name: ``AWS::ImageBuilder::DistributionConfiguration.Name``.
        :param description: ``AWS::ImageBuilder::DistributionConfiguration.Description``.
        :param tags: ``AWS::ImageBuilder::DistributionConfiguration.Tags``.
        """
        props = CfnDistributionConfigurationProps(distributions=distributions, name=name, description=description, tags=tags)

        jsii.create(CfnDistributionConfiguration, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnDistributionConfiguration":
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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::ImageBuilder::DistributionConfiguration.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-distributionconfiguration.html#cfn-imagebuilder-distributionconfiguration-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="distributions")
    def distributions(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["DistributionProperty", _IResolvable_9ceae33e]]]:
        """``AWS::ImageBuilder::DistributionConfiguration.Distributions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-distributionconfiguration.html#cfn-imagebuilder-distributionconfiguration-distributions
        """
        return jsii.get(self, "distributions")

    @distributions.setter
    def distributions(self, value: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["DistributionProperty", _IResolvable_9ceae33e]]]) -> None:
        jsii.set(self, "distributions", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::ImageBuilder::DistributionConfiguration.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-distributionconfiguration.html#cfn-imagebuilder-distributionconfiguration-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::DistributionConfiguration.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-distributionconfiguration.html#cfn-imagebuilder-distributionconfiguration-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_imagebuilder.CfnDistributionConfiguration.DistributionProperty", jsii_struct_bases=[], name_mapping={'ami_distribution_configuration': 'amiDistributionConfiguration', 'license_configuration_arns': 'licenseConfigurationArns', 'region': 'region'})
    class DistributionProperty():
        def __init__(self, *, ami_distribution_configuration: typing.Any=None, license_configuration_arns: typing.Optional[typing.List[str]]=None, region: typing.Optional[str]=None) -> None:
            """
            :param ami_distribution_configuration: ``CfnDistributionConfiguration.DistributionProperty.AmiDistributionConfiguration``.
            :param license_configuration_arns: ``CfnDistributionConfiguration.DistributionProperty.LicenseConfigurationArns``.
            :param region: ``CfnDistributionConfiguration.DistributionProperty.Region``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-distribution.html
            """
            self._values = {
            }
            if ami_distribution_configuration is not None: self._values["ami_distribution_configuration"] = ami_distribution_configuration
            if license_configuration_arns is not None: self._values["license_configuration_arns"] = license_configuration_arns
            if region is not None: self._values["region"] = region

        @builtins.property
        def ami_distribution_configuration(self) -> typing.Any:
            """``CfnDistributionConfiguration.DistributionProperty.AmiDistributionConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-distribution.html#cfn-imagebuilder-distributionconfiguration-distribution-amidistributionconfiguration
            """
            return self._values.get('ami_distribution_configuration')

        @builtins.property
        def license_configuration_arns(self) -> typing.Optional[typing.List[str]]:
            """``CfnDistributionConfiguration.DistributionProperty.LicenseConfigurationArns``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-distribution.html#cfn-imagebuilder-distributionconfiguration-distribution-licenseconfigurationarns
            """
            return self._values.get('license_configuration_arns')

        @builtins.property
        def region(self) -> typing.Optional[str]:
            """``CfnDistributionConfiguration.DistributionProperty.Region``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-distribution.html#cfn-imagebuilder-distributionconfiguration-distribution-region
            """
            return self._values.get('region')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DistributionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_imagebuilder.CfnDistributionConfigurationProps", jsii_struct_bases=[], name_mapping={'distributions': 'distributions', 'name': 'name', 'description': 'description', 'tags': 'tags'})
class CfnDistributionConfigurationProps():
    def __init__(self, *, distributions: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDistributionConfiguration.DistributionProperty", _IResolvable_9ceae33e]]], name: str, description: typing.Optional[str]=None, tags: typing.Optional[typing.Mapping[str, str]]=None) -> None:
        """Properties for defining a ``AWS::ImageBuilder::DistributionConfiguration``.

        :param distributions: ``AWS::ImageBuilder::DistributionConfiguration.Distributions``.
        :param name: ``AWS::ImageBuilder::DistributionConfiguration.Name``.
        :param description: ``AWS::ImageBuilder::DistributionConfiguration.Description``.
        :param tags: ``AWS::ImageBuilder::DistributionConfiguration.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-distributionconfiguration.html
        """
        self._values = {
            'distributions': distributions,
            'name': name,
        }
        if description is not None: self._values["description"] = description
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def distributions(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDistributionConfiguration.DistributionProperty", _IResolvable_9ceae33e]]]:
        """``AWS::ImageBuilder::DistributionConfiguration.Distributions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-distributionconfiguration.html#cfn-imagebuilder-distributionconfiguration-distributions
        """
        return self._values.get('distributions')

    @builtins.property
    def name(self) -> str:
        """``AWS::ImageBuilder::DistributionConfiguration.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-distributionconfiguration.html#cfn-imagebuilder-distributionconfiguration-name
        """
        return self._values.get('name')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::DistributionConfiguration.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-distributionconfiguration.html#cfn-imagebuilder-distributionconfiguration-description
        """
        return self._values.get('description')

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[str, str]]:
        """``AWS::ImageBuilder::DistributionConfiguration.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-distributionconfiguration.html#cfn-imagebuilder-distributionconfiguration-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDistributionConfigurationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnImage(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_imagebuilder.CfnImage"):
    """A CloudFormation ``AWS::ImageBuilder::Image``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html
    cloudformationResource:
    :cloudformationResource:: AWS::ImageBuilder::Image
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, image_recipe_arn: str, infrastructure_configuration_arn: str, distribution_configuration_arn: typing.Optional[str]=None, image_tests_configuration: typing.Optional[typing.Union["ImageTestsConfigurationProperty", _IResolvable_9ceae33e]]=None, tags: typing.Optional[typing.Mapping[str, str]]=None) -> None:
        """Create a new ``AWS::ImageBuilder::Image``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param image_recipe_arn: ``AWS::ImageBuilder::Image.ImageRecipeArn``.
        :param infrastructure_configuration_arn: ``AWS::ImageBuilder::Image.InfrastructureConfigurationArn``.
        :param distribution_configuration_arn: ``AWS::ImageBuilder::Image.DistributionConfigurationArn``.
        :param image_tests_configuration: ``AWS::ImageBuilder::Image.ImageTestsConfiguration``.
        :param tags: ``AWS::ImageBuilder::Image.Tags``.
        """
        props = CfnImageProps(image_recipe_arn=image_recipe_arn, infrastructure_configuration_arn=infrastructure_configuration_arn, distribution_configuration_arn=distribution_configuration_arn, image_tests_configuration=image_tests_configuration, tags=tags)

        jsii.create(CfnImage, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnImage":
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
    @jsii.member(jsii_name="attrImageId")
    def attr_image_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ImageId
        """
        return jsii.get(self, "attrImageId")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::ImageBuilder::Image.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html#cfn-imagebuilder-image-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="imageRecipeArn")
    def image_recipe_arn(self) -> str:
        """``AWS::ImageBuilder::Image.ImageRecipeArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html#cfn-imagebuilder-image-imagerecipearn
        """
        return jsii.get(self, "imageRecipeArn")

    @image_recipe_arn.setter
    def image_recipe_arn(self, value: str) -> None:
        jsii.set(self, "imageRecipeArn", value)

    @builtins.property
    @jsii.member(jsii_name="infrastructureConfigurationArn")
    def infrastructure_configuration_arn(self) -> str:
        """``AWS::ImageBuilder::Image.InfrastructureConfigurationArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html#cfn-imagebuilder-image-infrastructureconfigurationarn
        """
        return jsii.get(self, "infrastructureConfigurationArn")

    @infrastructure_configuration_arn.setter
    def infrastructure_configuration_arn(self, value: str) -> None:
        jsii.set(self, "infrastructureConfigurationArn", value)

    @builtins.property
    @jsii.member(jsii_name="distributionConfigurationArn")
    def distribution_configuration_arn(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::Image.DistributionConfigurationArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html#cfn-imagebuilder-image-distributionconfigurationarn
        """
        return jsii.get(self, "distributionConfigurationArn")

    @distribution_configuration_arn.setter
    def distribution_configuration_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "distributionConfigurationArn", value)

    @builtins.property
    @jsii.member(jsii_name="imageTestsConfiguration")
    def image_tests_configuration(self) -> typing.Optional[typing.Union["ImageTestsConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::ImageBuilder::Image.ImageTestsConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html#cfn-imagebuilder-image-imagetestsconfiguration
        """
        return jsii.get(self, "imageTestsConfiguration")

    @image_tests_configuration.setter
    def image_tests_configuration(self, value: typing.Optional[typing.Union["ImageTestsConfigurationProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "imageTestsConfiguration", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_imagebuilder.CfnImage.ImageTestsConfigurationProperty", jsii_struct_bases=[], name_mapping={'image_tests_enabled': 'imageTestsEnabled', 'timeout_minutes': 'timeoutMinutes'})
    class ImageTestsConfigurationProperty():
        def __init__(self, *, image_tests_enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, timeout_minutes: typing.Optional[jsii.Number]=None) -> None:
            """
            :param image_tests_enabled: ``CfnImage.ImageTestsConfigurationProperty.ImageTestsEnabled``.
            :param timeout_minutes: ``CfnImage.ImageTestsConfigurationProperty.TimeoutMinutes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-imagetestsconfiguration.html
            """
            self._values = {
            }
            if image_tests_enabled is not None: self._values["image_tests_enabled"] = image_tests_enabled
            if timeout_minutes is not None: self._values["timeout_minutes"] = timeout_minutes

        @builtins.property
        def image_tests_enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnImage.ImageTestsConfigurationProperty.ImageTestsEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-imagetestsconfiguration.html#cfn-imagebuilder-image-imagetestsconfiguration-imagetestsenabled
            """
            return self._values.get('image_tests_enabled')

        @builtins.property
        def timeout_minutes(self) -> typing.Optional[jsii.Number]:
            """``CfnImage.ImageTestsConfigurationProperty.TimeoutMinutes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-imagetestsconfiguration.html#cfn-imagebuilder-image-imagetestsconfiguration-timeoutminutes
            """
            return self._values.get('timeout_minutes')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ImageTestsConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.implements(_IInspectable_051e6ed8)
class CfnImagePipeline(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_imagebuilder.CfnImagePipeline"):
    """A CloudFormation ``AWS::ImageBuilder::ImagePipeline``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html
    cloudformationResource:
    :cloudformationResource:: AWS::ImageBuilder::ImagePipeline
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, image_recipe_arn: str, infrastructure_configuration_arn: str, name: str, description: typing.Optional[str]=None, distribution_configuration_arn: typing.Optional[str]=None, image_tests_configuration: typing.Optional[typing.Union["ImageTestsConfigurationProperty", _IResolvable_9ceae33e]]=None, schedule: typing.Optional[typing.Union["ScheduleProperty", _IResolvable_9ceae33e]]=None, status: typing.Optional[str]=None, tags: typing.Optional[typing.Mapping[str, str]]=None) -> None:
        """Create a new ``AWS::ImageBuilder::ImagePipeline``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param image_recipe_arn: ``AWS::ImageBuilder::ImagePipeline.ImageRecipeArn``.
        :param infrastructure_configuration_arn: ``AWS::ImageBuilder::ImagePipeline.InfrastructureConfigurationArn``.
        :param name: ``AWS::ImageBuilder::ImagePipeline.Name``.
        :param description: ``AWS::ImageBuilder::ImagePipeline.Description``.
        :param distribution_configuration_arn: ``AWS::ImageBuilder::ImagePipeline.DistributionConfigurationArn``.
        :param image_tests_configuration: ``AWS::ImageBuilder::ImagePipeline.ImageTestsConfiguration``.
        :param schedule: ``AWS::ImageBuilder::ImagePipeline.Schedule``.
        :param status: ``AWS::ImageBuilder::ImagePipeline.Status``.
        :param tags: ``AWS::ImageBuilder::ImagePipeline.Tags``.
        """
        props = CfnImagePipelineProps(image_recipe_arn=image_recipe_arn, infrastructure_configuration_arn=infrastructure_configuration_arn, name=name, description=description, distribution_configuration_arn=distribution_configuration_arn, image_tests_configuration=image_tests_configuration, schedule=schedule, status=status, tags=tags)

        jsii.create(CfnImagePipeline, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnImagePipeline":
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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::ImageBuilder::ImagePipeline.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="imageRecipeArn")
    def image_recipe_arn(self) -> str:
        """``AWS::ImageBuilder::ImagePipeline.ImageRecipeArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-imagerecipearn
        """
        return jsii.get(self, "imageRecipeArn")

    @image_recipe_arn.setter
    def image_recipe_arn(self, value: str) -> None:
        jsii.set(self, "imageRecipeArn", value)

    @builtins.property
    @jsii.member(jsii_name="infrastructureConfigurationArn")
    def infrastructure_configuration_arn(self) -> str:
        """``AWS::ImageBuilder::ImagePipeline.InfrastructureConfigurationArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-infrastructureconfigurationarn
        """
        return jsii.get(self, "infrastructureConfigurationArn")

    @infrastructure_configuration_arn.setter
    def infrastructure_configuration_arn(self, value: str) -> None:
        jsii.set(self, "infrastructureConfigurationArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::ImageBuilder::ImagePipeline.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::ImagePipeline.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="distributionConfigurationArn")
    def distribution_configuration_arn(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::ImagePipeline.DistributionConfigurationArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-distributionconfigurationarn
        """
        return jsii.get(self, "distributionConfigurationArn")

    @distribution_configuration_arn.setter
    def distribution_configuration_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "distributionConfigurationArn", value)

    @builtins.property
    @jsii.member(jsii_name="imageTestsConfiguration")
    def image_tests_configuration(self) -> typing.Optional[typing.Union["ImageTestsConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::ImageBuilder::ImagePipeline.ImageTestsConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-imagetestsconfiguration
        """
        return jsii.get(self, "imageTestsConfiguration")

    @image_tests_configuration.setter
    def image_tests_configuration(self, value: typing.Optional[typing.Union["ImageTestsConfigurationProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "imageTestsConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> typing.Optional[typing.Union["ScheduleProperty", _IResolvable_9ceae33e]]:
        """``AWS::ImageBuilder::ImagePipeline.Schedule``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-schedule
        """
        return jsii.get(self, "schedule")

    @schedule.setter
    def schedule(self, value: typing.Optional[typing.Union["ScheduleProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "schedule", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::ImagePipeline.Status``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-status
        """
        return jsii.get(self, "status")

    @status.setter
    def status(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "status", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_imagebuilder.CfnImagePipeline.ImageTestsConfigurationProperty", jsii_struct_bases=[], name_mapping={'image_tests_enabled': 'imageTestsEnabled', 'timeout_minutes': 'timeoutMinutes'})
    class ImageTestsConfigurationProperty():
        def __init__(self, *, image_tests_enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, timeout_minutes: typing.Optional[jsii.Number]=None) -> None:
            """
            :param image_tests_enabled: ``CfnImagePipeline.ImageTestsConfigurationProperty.ImageTestsEnabled``.
            :param timeout_minutes: ``CfnImagePipeline.ImageTestsConfigurationProperty.TimeoutMinutes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-imagetestsconfiguration.html
            """
            self._values = {
            }
            if image_tests_enabled is not None: self._values["image_tests_enabled"] = image_tests_enabled
            if timeout_minutes is not None: self._values["timeout_minutes"] = timeout_minutes

        @builtins.property
        def image_tests_enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnImagePipeline.ImageTestsConfigurationProperty.ImageTestsEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-imagetestsconfiguration.html#cfn-imagebuilder-imagepipeline-imagetestsconfiguration-imagetestsenabled
            """
            return self._values.get('image_tests_enabled')

        @builtins.property
        def timeout_minutes(self) -> typing.Optional[jsii.Number]:
            """``CfnImagePipeline.ImageTestsConfigurationProperty.TimeoutMinutes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-imagetestsconfiguration.html#cfn-imagebuilder-imagepipeline-imagetestsconfiguration-timeoutminutes
            """
            return self._values.get('timeout_minutes')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ImageTestsConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_imagebuilder.CfnImagePipeline.ScheduleProperty", jsii_struct_bases=[], name_mapping={'pipeline_execution_start_condition': 'pipelineExecutionStartCondition', 'schedule_expression': 'scheduleExpression'})
    class ScheduleProperty():
        def __init__(self, *, pipeline_execution_start_condition: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None) -> None:
            """
            :param pipeline_execution_start_condition: ``CfnImagePipeline.ScheduleProperty.PipelineExecutionStartCondition``.
            :param schedule_expression: ``CfnImagePipeline.ScheduleProperty.ScheduleExpression``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-schedule.html
            """
            self._values = {
            }
            if pipeline_execution_start_condition is not None: self._values["pipeline_execution_start_condition"] = pipeline_execution_start_condition
            if schedule_expression is not None: self._values["schedule_expression"] = schedule_expression

        @builtins.property
        def pipeline_execution_start_condition(self) -> typing.Optional[str]:
            """``CfnImagePipeline.ScheduleProperty.PipelineExecutionStartCondition``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-schedule.html#cfn-imagebuilder-imagepipeline-schedule-pipelineexecutionstartcondition
            """
            return self._values.get('pipeline_execution_start_condition')

        @builtins.property
        def schedule_expression(self) -> typing.Optional[str]:
            """``CfnImagePipeline.ScheduleProperty.ScheduleExpression``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-schedule.html#cfn-imagebuilder-imagepipeline-schedule-scheduleexpression
            """
            return self._values.get('schedule_expression')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ScheduleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_imagebuilder.CfnImagePipelineProps", jsii_struct_bases=[], name_mapping={'image_recipe_arn': 'imageRecipeArn', 'infrastructure_configuration_arn': 'infrastructureConfigurationArn', 'name': 'name', 'description': 'description', 'distribution_configuration_arn': 'distributionConfigurationArn', 'image_tests_configuration': 'imageTestsConfiguration', 'schedule': 'schedule', 'status': 'status', 'tags': 'tags'})
class CfnImagePipelineProps():
    def __init__(self, *, image_recipe_arn: str, infrastructure_configuration_arn: str, name: str, description: typing.Optional[str]=None, distribution_configuration_arn: typing.Optional[str]=None, image_tests_configuration: typing.Optional[typing.Union["CfnImagePipeline.ImageTestsConfigurationProperty", _IResolvable_9ceae33e]]=None, schedule: typing.Optional[typing.Union["CfnImagePipeline.ScheduleProperty", _IResolvable_9ceae33e]]=None, status: typing.Optional[str]=None, tags: typing.Optional[typing.Mapping[str, str]]=None) -> None:
        """Properties for defining a ``AWS::ImageBuilder::ImagePipeline``.

        :param image_recipe_arn: ``AWS::ImageBuilder::ImagePipeline.ImageRecipeArn``.
        :param infrastructure_configuration_arn: ``AWS::ImageBuilder::ImagePipeline.InfrastructureConfigurationArn``.
        :param name: ``AWS::ImageBuilder::ImagePipeline.Name``.
        :param description: ``AWS::ImageBuilder::ImagePipeline.Description``.
        :param distribution_configuration_arn: ``AWS::ImageBuilder::ImagePipeline.DistributionConfigurationArn``.
        :param image_tests_configuration: ``AWS::ImageBuilder::ImagePipeline.ImageTestsConfiguration``.
        :param schedule: ``AWS::ImageBuilder::ImagePipeline.Schedule``.
        :param status: ``AWS::ImageBuilder::ImagePipeline.Status``.
        :param tags: ``AWS::ImageBuilder::ImagePipeline.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html
        """
        self._values = {
            'image_recipe_arn': image_recipe_arn,
            'infrastructure_configuration_arn': infrastructure_configuration_arn,
            'name': name,
        }
        if description is not None: self._values["description"] = description
        if distribution_configuration_arn is not None: self._values["distribution_configuration_arn"] = distribution_configuration_arn
        if image_tests_configuration is not None: self._values["image_tests_configuration"] = image_tests_configuration
        if schedule is not None: self._values["schedule"] = schedule
        if status is not None: self._values["status"] = status
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def image_recipe_arn(self) -> str:
        """``AWS::ImageBuilder::ImagePipeline.ImageRecipeArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-imagerecipearn
        """
        return self._values.get('image_recipe_arn')

    @builtins.property
    def infrastructure_configuration_arn(self) -> str:
        """``AWS::ImageBuilder::ImagePipeline.InfrastructureConfigurationArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-infrastructureconfigurationarn
        """
        return self._values.get('infrastructure_configuration_arn')

    @builtins.property
    def name(self) -> str:
        """``AWS::ImageBuilder::ImagePipeline.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-name
        """
        return self._values.get('name')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::ImagePipeline.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-description
        """
        return self._values.get('description')

    @builtins.property
    def distribution_configuration_arn(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::ImagePipeline.DistributionConfigurationArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-distributionconfigurationarn
        """
        return self._values.get('distribution_configuration_arn')

    @builtins.property
    def image_tests_configuration(self) -> typing.Optional[typing.Union["CfnImagePipeline.ImageTestsConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::ImageBuilder::ImagePipeline.ImageTestsConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-imagetestsconfiguration
        """
        return self._values.get('image_tests_configuration')

    @builtins.property
    def schedule(self) -> typing.Optional[typing.Union["CfnImagePipeline.ScheduleProperty", _IResolvable_9ceae33e]]:
        """``AWS::ImageBuilder::ImagePipeline.Schedule``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-schedule
        """
        return self._values.get('schedule')

    @builtins.property
    def status(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::ImagePipeline.Status``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-status
        """
        return self._values.get('status')

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[str, str]]:
        """``AWS::ImageBuilder::ImagePipeline.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnImagePipelineProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_imagebuilder.CfnImageProps", jsii_struct_bases=[], name_mapping={'image_recipe_arn': 'imageRecipeArn', 'infrastructure_configuration_arn': 'infrastructureConfigurationArn', 'distribution_configuration_arn': 'distributionConfigurationArn', 'image_tests_configuration': 'imageTestsConfiguration', 'tags': 'tags'})
class CfnImageProps():
    def __init__(self, *, image_recipe_arn: str, infrastructure_configuration_arn: str, distribution_configuration_arn: typing.Optional[str]=None, image_tests_configuration: typing.Optional[typing.Union["CfnImage.ImageTestsConfigurationProperty", _IResolvable_9ceae33e]]=None, tags: typing.Optional[typing.Mapping[str, str]]=None) -> None:
        """Properties for defining a ``AWS::ImageBuilder::Image``.

        :param image_recipe_arn: ``AWS::ImageBuilder::Image.ImageRecipeArn``.
        :param infrastructure_configuration_arn: ``AWS::ImageBuilder::Image.InfrastructureConfigurationArn``.
        :param distribution_configuration_arn: ``AWS::ImageBuilder::Image.DistributionConfigurationArn``.
        :param image_tests_configuration: ``AWS::ImageBuilder::Image.ImageTestsConfiguration``.
        :param tags: ``AWS::ImageBuilder::Image.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html
        """
        self._values = {
            'image_recipe_arn': image_recipe_arn,
            'infrastructure_configuration_arn': infrastructure_configuration_arn,
        }
        if distribution_configuration_arn is not None: self._values["distribution_configuration_arn"] = distribution_configuration_arn
        if image_tests_configuration is not None: self._values["image_tests_configuration"] = image_tests_configuration
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def image_recipe_arn(self) -> str:
        """``AWS::ImageBuilder::Image.ImageRecipeArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html#cfn-imagebuilder-image-imagerecipearn
        """
        return self._values.get('image_recipe_arn')

    @builtins.property
    def infrastructure_configuration_arn(self) -> str:
        """``AWS::ImageBuilder::Image.InfrastructureConfigurationArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html#cfn-imagebuilder-image-infrastructureconfigurationarn
        """
        return self._values.get('infrastructure_configuration_arn')

    @builtins.property
    def distribution_configuration_arn(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::Image.DistributionConfigurationArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html#cfn-imagebuilder-image-distributionconfigurationarn
        """
        return self._values.get('distribution_configuration_arn')

    @builtins.property
    def image_tests_configuration(self) -> typing.Optional[typing.Union["CfnImage.ImageTestsConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::ImageBuilder::Image.ImageTestsConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html#cfn-imagebuilder-image-imagetestsconfiguration
        """
        return self._values.get('image_tests_configuration')

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[str, str]]:
        """``AWS::ImageBuilder::Image.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html#cfn-imagebuilder-image-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnImageProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnImageRecipe(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_imagebuilder.CfnImageRecipe"):
    """A CloudFormation ``AWS::ImageBuilder::ImageRecipe``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html
    cloudformationResource:
    :cloudformationResource:: AWS::ImageBuilder::ImageRecipe
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, components: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ComponentConfigurationProperty", _IResolvable_9ceae33e]]], name: str, parent_image: str, version: str, block_device_mappings: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["InstanceBlockDeviceMappingProperty", _IResolvable_9ceae33e]]]]=None, description: typing.Optional[str]=None, tags: typing.Optional[typing.Mapping[str, str]]=None) -> None:
        """Create a new ``AWS::ImageBuilder::ImageRecipe``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param components: ``AWS::ImageBuilder::ImageRecipe.Components``.
        :param name: ``AWS::ImageBuilder::ImageRecipe.Name``.
        :param parent_image: ``AWS::ImageBuilder::ImageRecipe.ParentImage``.
        :param version: ``AWS::ImageBuilder::ImageRecipe.Version``.
        :param block_device_mappings: ``AWS::ImageBuilder::ImageRecipe.BlockDeviceMappings``.
        :param description: ``AWS::ImageBuilder::ImageRecipe.Description``.
        :param tags: ``AWS::ImageBuilder::ImageRecipe.Tags``.
        """
        props = CfnImageRecipeProps(components=components, name=name, parent_image=parent_image, version=version, block_device_mappings=block_device_mappings, description=description, tags=tags)

        jsii.create(CfnImageRecipe, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnImageRecipe":
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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::ImageBuilder::ImageRecipe.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html#cfn-imagebuilder-imagerecipe-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="components")
    def components(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ComponentConfigurationProperty", _IResolvable_9ceae33e]]]:
        """``AWS::ImageBuilder::ImageRecipe.Components``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html#cfn-imagebuilder-imagerecipe-components
        """
        return jsii.get(self, "components")

    @components.setter
    def components(self, value: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ComponentConfigurationProperty", _IResolvable_9ceae33e]]]) -> None:
        jsii.set(self, "components", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::ImageBuilder::ImageRecipe.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html#cfn-imagebuilder-imagerecipe-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="parentImage")
    def parent_image(self) -> str:
        """``AWS::ImageBuilder::ImageRecipe.ParentImage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html#cfn-imagebuilder-imagerecipe-parentimage
        """
        return jsii.get(self, "parentImage")

    @parent_image.setter
    def parent_image(self, value: str) -> None:
        jsii.set(self, "parentImage", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> str:
        """``AWS::ImageBuilder::ImageRecipe.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html#cfn-imagebuilder-imagerecipe-version
        """
        return jsii.get(self, "version")

    @version.setter
    def version(self, value: str) -> None:
        jsii.set(self, "version", value)

    @builtins.property
    @jsii.member(jsii_name="blockDeviceMappings")
    def block_device_mappings(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["InstanceBlockDeviceMappingProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ImageBuilder::ImageRecipe.BlockDeviceMappings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html#cfn-imagebuilder-imagerecipe-blockdevicemappings
        """
        return jsii.get(self, "blockDeviceMappings")

    @block_device_mappings.setter
    def block_device_mappings(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["InstanceBlockDeviceMappingProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "blockDeviceMappings", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::ImageRecipe.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html#cfn-imagebuilder-imagerecipe-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_imagebuilder.CfnImageRecipe.ComponentConfigurationProperty", jsii_struct_bases=[], name_mapping={'component_arn': 'componentArn'})
    class ComponentConfigurationProperty():
        def __init__(self, *, component_arn: typing.Optional[str]=None) -> None:
            """
            :param component_arn: ``CfnImageRecipe.ComponentConfigurationProperty.ComponentArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-componentconfiguration.html
            """
            self._values = {
            }
            if component_arn is not None: self._values["component_arn"] = component_arn

        @builtins.property
        def component_arn(self) -> typing.Optional[str]:
            """``CfnImageRecipe.ComponentConfigurationProperty.ComponentArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-componentconfiguration.html#cfn-imagebuilder-imagerecipe-componentconfiguration-componentarn
            """
            return self._values.get('component_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ComponentConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_imagebuilder.CfnImageRecipe.EbsInstanceBlockDeviceSpecificationProperty", jsii_struct_bases=[], name_mapping={'delete_on_termination': 'deleteOnTermination', 'encrypted': 'encrypted', 'iops': 'iops', 'kms_key_id': 'kmsKeyId', 'snapshot_id': 'snapshotId', 'volume_size': 'volumeSize', 'volume_type': 'volumeType'})
    class EbsInstanceBlockDeviceSpecificationProperty():
        def __init__(self, *, delete_on_termination: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, encrypted: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, iops: typing.Optional[jsii.Number]=None, kms_key_id: typing.Optional[str]=None, snapshot_id: typing.Optional[str]=None, volume_size: typing.Optional[jsii.Number]=None, volume_type: typing.Optional[str]=None) -> None:
            """
            :param delete_on_termination: ``CfnImageRecipe.EbsInstanceBlockDeviceSpecificationProperty.DeleteOnTermination``.
            :param encrypted: ``CfnImageRecipe.EbsInstanceBlockDeviceSpecificationProperty.Encrypted``.
            :param iops: ``CfnImageRecipe.EbsInstanceBlockDeviceSpecificationProperty.Iops``.
            :param kms_key_id: ``CfnImageRecipe.EbsInstanceBlockDeviceSpecificationProperty.KmsKeyId``.
            :param snapshot_id: ``CfnImageRecipe.EbsInstanceBlockDeviceSpecificationProperty.SnapshotId``.
            :param volume_size: ``CfnImageRecipe.EbsInstanceBlockDeviceSpecificationProperty.VolumeSize``.
            :param volume_type: ``CfnImageRecipe.EbsInstanceBlockDeviceSpecificationProperty.VolumeType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification.html
            """
            self._values = {
            }
            if delete_on_termination is not None: self._values["delete_on_termination"] = delete_on_termination
            if encrypted is not None: self._values["encrypted"] = encrypted
            if iops is not None: self._values["iops"] = iops
            if kms_key_id is not None: self._values["kms_key_id"] = kms_key_id
            if snapshot_id is not None: self._values["snapshot_id"] = snapshot_id
            if volume_size is not None: self._values["volume_size"] = volume_size
            if volume_type is not None: self._values["volume_type"] = volume_type

        @builtins.property
        def delete_on_termination(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnImageRecipe.EbsInstanceBlockDeviceSpecificationProperty.DeleteOnTermination``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification.html#cfn-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification-deleteontermination
            """
            return self._values.get('delete_on_termination')

        @builtins.property
        def encrypted(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnImageRecipe.EbsInstanceBlockDeviceSpecificationProperty.Encrypted``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification.html#cfn-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification-encrypted
            """
            return self._values.get('encrypted')

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            """``CfnImageRecipe.EbsInstanceBlockDeviceSpecificationProperty.Iops``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification.html#cfn-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification-iops
            """
            return self._values.get('iops')

        @builtins.property
        def kms_key_id(self) -> typing.Optional[str]:
            """``CfnImageRecipe.EbsInstanceBlockDeviceSpecificationProperty.KmsKeyId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification.html#cfn-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification-kmskeyid
            """
            return self._values.get('kms_key_id')

        @builtins.property
        def snapshot_id(self) -> typing.Optional[str]:
            """``CfnImageRecipe.EbsInstanceBlockDeviceSpecificationProperty.SnapshotId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification.html#cfn-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification-snapshotid
            """
            return self._values.get('snapshot_id')

        @builtins.property
        def volume_size(self) -> typing.Optional[jsii.Number]:
            """``CfnImageRecipe.EbsInstanceBlockDeviceSpecificationProperty.VolumeSize``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification.html#cfn-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification-volumesize
            """
            return self._values.get('volume_size')

        @builtins.property
        def volume_type(self) -> typing.Optional[str]:
            """``CfnImageRecipe.EbsInstanceBlockDeviceSpecificationProperty.VolumeType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification.html#cfn-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification-volumetype
            """
            return self._values.get('volume_type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EbsInstanceBlockDeviceSpecificationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_imagebuilder.CfnImageRecipe.InstanceBlockDeviceMappingProperty", jsii_struct_bases=[], name_mapping={'device_name': 'deviceName', 'ebs': 'ebs', 'no_device': 'noDevice', 'virtual_name': 'virtualName'})
    class InstanceBlockDeviceMappingProperty():
        def __init__(self, *, device_name: typing.Optional[str]=None, ebs: typing.Optional[typing.Union["CfnImageRecipe.EbsInstanceBlockDeviceSpecificationProperty", _IResolvable_9ceae33e]]=None, no_device: typing.Optional[str]=None, virtual_name: typing.Optional[str]=None) -> None:
            """
            :param device_name: ``CfnImageRecipe.InstanceBlockDeviceMappingProperty.DeviceName``.
            :param ebs: ``CfnImageRecipe.InstanceBlockDeviceMappingProperty.Ebs``.
            :param no_device: ``CfnImageRecipe.InstanceBlockDeviceMappingProperty.NoDevice``.
            :param virtual_name: ``CfnImageRecipe.InstanceBlockDeviceMappingProperty.VirtualName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-instanceblockdevicemapping.html
            """
            self._values = {
            }
            if device_name is not None: self._values["device_name"] = device_name
            if ebs is not None: self._values["ebs"] = ebs
            if no_device is not None: self._values["no_device"] = no_device
            if virtual_name is not None: self._values["virtual_name"] = virtual_name

        @builtins.property
        def device_name(self) -> typing.Optional[str]:
            """``CfnImageRecipe.InstanceBlockDeviceMappingProperty.DeviceName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-instanceblockdevicemapping.html#cfn-imagebuilder-imagerecipe-instanceblockdevicemapping-devicename
            """
            return self._values.get('device_name')

        @builtins.property
        def ebs(self) -> typing.Optional[typing.Union["CfnImageRecipe.EbsInstanceBlockDeviceSpecificationProperty", _IResolvable_9ceae33e]]:
            """``CfnImageRecipe.InstanceBlockDeviceMappingProperty.Ebs``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-instanceblockdevicemapping.html#cfn-imagebuilder-imagerecipe-instanceblockdevicemapping-ebs
            """
            return self._values.get('ebs')

        @builtins.property
        def no_device(self) -> typing.Optional[str]:
            """``CfnImageRecipe.InstanceBlockDeviceMappingProperty.NoDevice``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-instanceblockdevicemapping.html#cfn-imagebuilder-imagerecipe-instanceblockdevicemapping-nodevice
            """
            return self._values.get('no_device')

        @builtins.property
        def virtual_name(self) -> typing.Optional[str]:
            """``CfnImageRecipe.InstanceBlockDeviceMappingProperty.VirtualName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-instanceblockdevicemapping.html#cfn-imagebuilder-imagerecipe-instanceblockdevicemapping-virtualname
            """
            return self._values.get('virtual_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'InstanceBlockDeviceMappingProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_imagebuilder.CfnImageRecipeProps", jsii_struct_bases=[], name_mapping={'components': 'components', 'name': 'name', 'parent_image': 'parentImage', 'version': 'version', 'block_device_mappings': 'blockDeviceMappings', 'description': 'description', 'tags': 'tags'})
class CfnImageRecipeProps():
    def __init__(self, *, components: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnImageRecipe.ComponentConfigurationProperty", _IResolvable_9ceae33e]]], name: str, parent_image: str, version: str, block_device_mappings: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnImageRecipe.InstanceBlockDeviceMappingProperty", _IResolvable_9ceae33e]]]]=None, description: typing.Optional[str]=None, tags: typing.Optional[typing.Mapping[str, str]]=None) -> None:
        """Properties for defining a ``AWS::ImageBuilder::ImageRecipe``.

        :param components: ``AWS::ImageBuilder::ImageRecipe.Components``.
        :param name: ``AWS::ImageBuilder::ImageRecipe.Name``.
        :param parent_image: ``AWS::ImageBuilder::ImageRecipe.ParentImage``.
        :param version: ``AWS::ImageBuilder::ImageRecipe.Version``.
        :param block_device_mappings: ``AWS::ImageBuilder::ImageRecipe.BlockDeviceMappings``.
        :param description: ``AWS::ImageBuilder::ImageRecipe.Description``.
        :param tags: ``AWS::ImageBuilder::ImageRecipe.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html
        """
        self._values = {
            'components': components,
            'name': name,
            'parent_image': parent_image,
            'version': version,
        }
        if block_device_mappings is not None: self._values["block_device_mappings"] = block_device_mappings
        if description is not None: self._values["description"] = description
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def components(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnImageRecipe.ComponentConfigurationProperty", _IResolvable_9ceae33e]]]:
        """``AWS::ImageBuilder::ImageRecipe.Components``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html#cfn-imagebuilder-imagerecipe-components
        """
        return self._values.get('components')

    @builtins.property
    def name(self) -> str:
        """``AWS::ImageBuilder::ImageRecipe.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html#cfn-imagebuilder-imagerecipe-name
        """
        return self._values.get('name')

    @builtins.property
    def parent_image(self) -> str:
        """``AWS::ImageBuilder::ImageRecipe.ParentImage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html#cfn-imagebuilder-imagerecipe-parentimage
        """
        return self._values.get('parent_image')

    @builtins.property
    def version(self) -> str:
        """``AWS::ImageBuilder::ImageRecipe.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html#cfn-imagebuilder-imagerecipe-version
        """
        return self._values.get('version')

    @builtins.property
    def block_device_mappings(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnImageRecipe.InstanceBlockDeviceMappingProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ImageBuilder::ImageRecipe.BlockDeviceMappings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html#cfn-imagebuilder-imagerecipe-blockdevicemappings
        """
        return self._values.get('block_device_mappings')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::ImageRecipe.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html#cfn-imagebuilder-imagerecipe-description
        """
        return self._values.get('description')

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[str, str]]:
        """``AWS::ImageBuilder::ImageRecipe.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html#cfn-imagebuilder-imagerecipe-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnImageRecipeProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnInfrastructureConfiguration(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_imagebuilder.CfnInfrastructureConfiguration"):
    """A CloudFormation ``AWS::ImageBuilder::InfrastructureConfiguration``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html
    cloudformationResource:
    :cloudformationResource:: AWS::ImageBuilder::InfrastructureConfiguration
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, instance_profile_name: str, name: str, description: typing.Optional[str]=None, instance_types: typing.Optional[typing.List[str]]=None, key_pair: typing.Optional[str]=None, logging: typing.Any=None, security_group_ids: typing.Optional[typing.List[str]]=None, sns_topic_arn: typing.Optional[str]=None, subnet_id: typing.Optional[str]=None, tags: typing.Optional[typing.Mapping[str, str]]=None, terminate_instance_on_failure: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None) -> None:
        """Create a new ``AWS::ImageBuilder::InfrastructureConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param instance_profile_name: ``AWS::ImageBuilder::InfrastructureConfiguration.InstanceProfileName``.
        :param name: ``AWS::ImageBuilder::InfrastructureConfiguration.Name``.
        :param description: ``AWS::ImageBuilder::InfrastructureConfiguration.Description``.
        :param instance_types: ``AWS::ImageBuilder::InfrastructureConfiguration.InstanceTypes``.
        :param key_pair: ``AWS::ImageBuilder::InfrastructureConfiguration.KeyPair``.
        :param logging: ``AWS::ImageBuilder::InfrastructureConfiguration.Logging``.
        :param security_group_ids: ``AWS::ImageBuilder::InfrastructureConfiguration.SecurityGroupIds``.
        :param sns_topic_arn: ``AWS::ImageBuilder::InfrastructureConfiguration.SnsTopicArn``.
        :param subnet_id: ``AWS::ImageBuilder::InfrastructureConfiguration.SubnetId``.
        :param tags: ``AWS::ImageBuilder::InfrastructureConfiguration.Tags``.
        :param terminate_instance_on_failure: ``AWS::ImageBuilder::InfrastructureConfiguration.TerminateInstanceOnFailure``.
        """
        props = CfnInfrastructureConfigurationProps(instance_profile_name=instance_profile_name, name=name, description=description, instance_types=instance_types, key_pair=key_pair, logging=logging, security_group_ids=security_group_ids, sns_topic_arn=sns_topic_arn, subnet_id=subnet_id, tags=tags, terminate_instance_on_failure=terminate_instance_on_failure)

        jsii.create(CfnInfrastructureConfiguration, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnInfrastructureConfiguration":
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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::ImageBuilder::InfrastructureConfiguration.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="instanceProfileName")
    def instance_profile_name(self) -> str:
        """``AWS::ImageBuilder::InfrastructureConfiguration.InstanceProfileName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-instanceprofilename
        """
        return jsii.get(self, "instanceProfileName")

    @instance_profile_name.setter
    def instance_profile_name(self, value: str) -> None:
        jsii.set(self, "instanceProfileName", value)

    @builtins.property
    @jsii.member(jsii_name="logging")
    def logging(self) -> typing.Any:
        """``AWS::ImageBuilder::InfrastructureConfiguration.Logging``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-logging
        """
        return jsii.get(self, "logging")

    @logging.setter
    def logging(self, value: typing.Any) -> None:
        jsii.set(self, "logging", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::ImageBuilder::InfrastructureConfiguration.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::InfrastructureConfiguration.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="instanceTypes")
    def instance_types(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ImageBuilder::InfrastructureConfiguration.InstanceTypes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-instancetypes
        """
        return jsii.get(self, "instanceTypes")

    @instance_types.setter
    def instance_types(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "instanceTypes", value)

    @builtins.property
    @jsii.member(jsii_name="keyPair")
    def key_pair(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::InfrastructureConfiguration.KeyPair``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-keypair
        """
        return jsii.get(self, "keyPair")

    @key_pair.setter
    def key_pair(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "keyPair", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ImageBuilder::InfrastructureConfiguration.SecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-securitygroupids
        """
        return jsii.get(self, "securityGroupIds")

    @security_group_ids.setter
    def security_group_ids(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "securityGroupIds", value)

    @builtins.property
    @jsii.member(jsii_name="snsTopicArn")
    def sns_topic_arn(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::InfrastructureConfiguration.SnsTopicArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-snstopicarn
        """
        return jsii.get(self, "snsTopicArn")

    @sns_topic_arn.setter
    def sns_topic_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "snsTopicArn", value)

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::InfrastructureConfiguration.SubnetId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-subnetid
        """
        return jsii.get(self, "subnetId")

    @subnet_id.setter
    def subnet_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "subnetId", value)

    @builtins.property
    @jsii.member(jsii_name="terminateInstanceOnFailure")
    def terminate_instance_on_failure(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::ImageBuilder::InfrastructureConfiguration.TerminateInstanceOnFailure``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-terminateinstanceonfailure
        """
        return jsii.get(self, "terminateInstanceOnFailure")

    @terminate_instance_on_failure.setter
    def terminate_instance_on_failure(self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "terminateInstanceOnFailure", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_imagebuilder.CfnInfrastructureConfiguration.LoggingProperty", jsii_struct_bases=[], name_mapping={'s3_logs': 's3Logs'})
    class LoggingProperty():
        def __init__(self, *, s3_logs: typing.Optional[typing.Union["CfnInfrastructureConfiguration.S3LogsProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param s3_logs: ``CfnInfrastructureConfiguration.LoggingProperty.S3Logs``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-infrastructureconfiguration-logging.html
            """
            self._values = {
            }
            if s3_logs is not None: self._values["s3_logs"] = s3_logs

        @builtins.property
        def s3_logs(self) -> typing.Optional[typing.Union["CfnInfrastructureConfiguration.S3LogsProperty", _IResolvable_9ceae33e]]:
            """``CfnInfrastructureConfiguration.LoggingProperty.S3Logs``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-infrastructureconfiguration-logging.html#cfn-imagebuilder-infrastructureconfiguration-logging-s3logs
            """
            return self._values.get('s3_logs')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LoggingProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_imagebuilder.CfnInfrastructureConfiguration.S3LogsProperty", jsii_struct_bases=[], name_mapping={'s3_bucket_name': 's3BucketName', 's3_key_prefix': 's3KeyPrefix'})
    class S3LogsProperty():
        def __init__(self, *, s3_bucket_name: typing.Optional[str]=None, s3_key_prefix: typing.Optional[str]=None) -> None:
            """
            :param s3_bucket_name: ``CfnInfrastructureConfiguration.S3LogsProperty.S3BucketName``.
            :param s3_key_prefix: ``CfnInfrastructureConfiguration.S3LogsProperty.S3KeyPrefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-infrastructureconfiguration-s3logs.html
            """
            self._values = {
            }
            if s3_bucket_name is not None: self._values["s3_bucket_name"] = s3_bucket_name
            if s3_key_prefix is not None: self._values["s3_key_prefix"] = s3_key_prefix

        @builtins.property
        def s3_bucket_name(self) -> typing.Optional[str]:
            """``CfnInfrastructureConfiguration.S3LogsProperty.S3BucketName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-infrastructureconfiguration-s3logs.html#cfn-imagebuilder-infrastructureconfiguration-s3logs-s3bucketname
            """
            return self._values.get('s3_bucket_name')

        @builtins.property
        def s3_key_prefix(self) -> typing.Optional[str]:
            """``CfnInfrastructureConfiguration.S3LogsProperty.S3KeyPrefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-infrastructureconfiguration-s3logs.html#cfn-imagebuilder-infrastructureconfiguration-s3logs-s3keyprefix
            """
            return self._values.get('s3_key_prefix')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'S3LogsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_imagebuilder.CfnInfrastructureConfigurationProps", jsii_struct_bases=[], name_mapping={'instance_profile_name': 'instanceProfileName', 'name': 'name', 'description': 'description', 'instance_types': 'instanceTypes', 'key_pair': 'keyPair', 'logging': 'logging', 'security_group_ids': 'securityGroupIds', 'sns_topic_arn': 'snsTopicArn', 'subnet_id': 'subnetId', 'tags': 'tags', 'terminate_instance_on_failure': 'terminateInstanceOnFailure'})
class CfnInfrastructureConfigurationProps():
    def __init__(self, *, instance_profile_name: str, name: str, description: typing.Optional[str]=None, instance_types: typing.Optional[typing.List[str]]=None, key_pair: typing.Optional[str]=None, logging: typing.Any=None, security_group_ids: typing.Optional[typing.List[str]]=None, sns_topic_arn: typing.Optional[str]=None, subnet_id: typing.Optional[str]=None, tags: typing.Optional[typing.Mapping[str, str]]=None, terminate_instance_on_failure: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None) -> None:
        """Properties for defining a ``AWS::ImageBuilder::InfrastructureConfiguration``.

        :param instance_profile_name: ``AWS::ImageBuilder::InfrastructureConfiguration.InstanceProfileName``.
        :param name: ``AWS::ImageBuilder::InfrastructureConfiguration.Name``.
        :param description: ``AWS::ImageBuilder::InfrastructureConfiguration.Description``.
        :param instance_types: ``AWS::ImageBuilder::InfrastructureConfiguration.InstanceTypes``.
        :param key_pair: ``AWS::ImageBuilder::InfrastructureConfiguration.KeyPair``.
        :param logging: ``AWS::ImageBuilder::InfrastructureConfiguration.Logging``.
        :param security_group_ids: ``AWS::ImageBuilder::InfrastructureConfiguration.SecurityGroupIds``.
        :param sns_topic_arn: ``AWS::ImageBuilder::InfrastructureConfiguration.SnsTopicArn``.
        :param subnet_id: ``AWS::ImageBuilder::InfrastructureConfiguration.SubnetId``.
        :param tags: ``AWS::ImageBuilder::InfrastructureConfiguration.Tags``.
        :param terminate_instance_on_failure: ``AWS::ImageBuilder::InfrastructureConfiguration.TerminateInstanceOnFailure``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html
        """
        self._values = {
            'instance_profile_name': instance_profile_name,
            'name': name,
        }
        if description is not None: self._values["description"] = description
        if instance_types is not None: self._values["instance_types"] = instance_types
        if key_pair is not None: self._values["key_pair"] = key_pair
        if logging is not None: self._values["logging"] = logging
        if security_group_ids is not None: self._values["security_group_ids"] = security_group_ids
        if sns_topic_arn is not None: self._values["sns_topic_arn"] = sns_topic_arn
        if subnet_id is not None: self._values["subnet_id"] = subnet_id
        if tags is not None: self._values["tags"] = tags
        if terminate_instance_on_failure is not None: self._values["terminate_instance_on_failure"] = terminate_instance_on_failure

    @builtins.property
    def instance_profile_name(self) -> str:
        """``AWS::ImageBuilder::InfrastructureConfiguration.InstanceProfileName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-instanceprofilename
        """
        return self._values.get('instance_profile_name')

    @builtins.property
    def name(self) -> str:
        """``AWS::ImageBuilder::InfrastructureConfiguration.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-name
        """
        return self._values.get('name')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::InfrastructureConfiguration.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-description
        """
        return self._values.get('description')

    @builtins.property
    def instance_types(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ImageBuilder::InfrastructureConfiguration.InstanceTypes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-instancetypes
        """
        return self._values.get('instance_types')

    @builtins.property
    def key_pair(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::InfrastructureConfiguration.KeyPair``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-keypair
        """
        return self._values.get('key_pair')

    @builtins.property
    def logging(self) -> typing.Any:
        """``AWS::ImageBuilder::InfrastructureConfiguration.Logging``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-logging
        """
        return self._values.get('logging')

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ImageBuilder::InfrastructureConfiguration.SecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-securitygroupids
        """
        return self._values.get('security_group_ids')

    @builtins.property
    def sns_topic_arn(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::InfrastructureConfiguration.SnsTopicArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-snstopicarn
        """
        return self._values.get('sns_topic_arn')

    @builtins.property
    def subnet_id(self) -> typing.Optional[str]:
        """``AWS::ImageBuilder::InfrastructureConfiguration.SubnetId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-subnetid
        """
        return self._values.get('subnet_id')

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[str, str]]:
        """``AWS::ImageBuilder::InfrastructureConfiguration.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-tags
        """
        return self._values.get('tags')

    @builtins.property
    def terminate_instance_on_failure(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::ImageBuilder::InfrastructureConfiguration.TerminateInstanceOnFailure``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-terminateinstanceonfailure
        """
        return self._values.get('terminate_instance_on_failure')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnInfrastructureConfigurationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnComponent",
    "CfnComponentProps",
    "CfnDistributionConfiguration",
    "CfnDistributionConfigurationProps",
    "CfnImage",
    "CfnImagePipeline",
    "CfnImagePipelineProps",
    "CfnImageProps",
    "CfnImageRecipe",
    "CfnImageRecipeProps",
    "CfnInfrastructureConfiguration",
    "CfnInfrastructureConfigurationProps",
]

publication.publish()
