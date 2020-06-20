import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (CfnResource as _CfnResource_7760e8e4, Construct as _Construct_f50a3f53, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, TagManager as _TagManager_2508893f, IInspectable as _IInspectable_051e6ed8, IResolvable as _IResolvable_9ceae33e)


@jsii.implements(_IInspectable_051e6ed8)
class CfnFleet(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_robomaker.CfnFleet"):
    """A CloudFormation ``AWS::RoboMaker::Fleet``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-fleet.html
    cloudformationResource:
    :cloudformationResource:: AWS::RoboMaker::Fleet
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, name: typing.Optional[str]=None, tags: typing.Any=None) -> None:
        """Create a new ``AWS::RoboMaker::Fleet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::RoboMaker::Fleet.Name``.
        :param tags: ``AWS::RoboMaker::Fleet.Tags``.
        """
        props = CfnFleetProps(name=name, tags=tags)

        jsii.create(CfnFleet, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnFleet":
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
        """``AWS::RoboMaker::Fleet.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-fleet.html#cfn-robomaker-fleet-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::RoboMaker::Fleet.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-fleet.html#cfn-robomaker-fleet-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "name", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_robomaker.CfnFleetProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'tags': 'tags'})
class CfnFleetProps():
    def __init__(self, *, name: typing.Optional[str]=None, tags: typing.Any=None) -> None:
        """Properties for defining a ``AWS::RoboMaker::Fleet``.

        :param name: ``AWS::RoboMaker::Fleet.Name``.
        :param tags: ``AWS::RoboMaker::Fleet.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-fleet.html
        """
        self._values = {
        }
        if name is not None: self._values["name"] = name
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::RoboMaker::Fleet.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-fleet.html#cfn-robomaker-fleet-name
        """
        return self._values.get('name')

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::RoboMaker::Fleet.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-fleet.html#cfn-robomaker-fleet-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnFleetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnRobot(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_robomaker.CfnRobot"):
    """A CloudFormation ``AWS::RoboMaker::Robot``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html
    cloudformationResource:
    :cloudformationResource:: AWS::RoboMaker::Robot
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, architecture: str, greengrass_group_id: str, fleet: typing.Optional[str]=None, name: typing.Optional[str]=None, tags: typing.Any=None) -> None:
        """Create a new ``AWS::RoboMaker::Robot``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param architecture: ``AWS::RoboMaker::Robot.Architecture``.
        :param greengrass_group_id: ``AWS::RoboMaker::Robot.GreengrassGroupId``.
        :param fleet: ``AWS::RoboMaker::Robot.Fleet``.
        :param name: ``AWS::RoboMaker::Robot.Name``.
        :param tags: ``AWS::RoboMaker::Robot.Tags``.
        """
        props = CfnRobotProps(architecture=architecture, greengrass_group_id=greengrass_group_id, fleet=fleet, name=name, tags=tags)

        jsii.create(CfnRobot, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnRobot":
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
        """``AWS::RoboMaker::Robot.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="architecture")
    def architecture(self) -> str:
        """``AWS::RoboMaker::Robot.Architecture``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-architecture
        """
        return jsii.get(self, "architecture")

    @architecture.setter
    def architecture(self, value: str) -> None:
        jsii.set(self, "architecture", value)

    @builtins.property
    @jsii.member(jsii_name="greengrassGroupId")
    def greengrass_group_id(self) -> str:
        """``AWS::RoboMaker::Robot.GreengrassGroupId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-greengrassgroupid
        """
        return jsii.get(self, "greengrassGroupId")

    @greengrass_group_id.setter
    def greengrass_group_id(self, value: str) -> None:
        jsii.set(self, "greengrassGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="fleet")
    def fleet(self) -> typing.Optional[str]:
        """``AWS::RoboMaker::Robot.Fleet``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-fleet
        """
        return jsii.get(self, "fleet")

    @fleet.setter
    def fleet(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "fleet", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::RoboMaker::Robot.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "name", value)


@jsii.implements(_IInspectable_051e6ed8)
class CfnRobotApplication(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_robomaker.CfnRobotApplication"):
    """A CloudFormation ``AWS::RoboMaker::RobotApplication``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html
    cloudformationResource:
    :cloudformationResource:: AWS::RoboMaker::RobotApplication
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, robot_software_suite: typing.Union["RobotSoftwareSuiteProperty", _IResolvable_9ceae33e], sources: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["SourceConfigProperty", _IResolvable_9ceae33e]]], current_revision_id: typing.Optional[str]=None, name: typing.Optional[str]=None, tags: typing.Any=None) -> None:
        """Create a new ``AWS::RoboMaker::RobotApplication``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param robot_software_suite: ``AWS::RoboMaker::RobotApplication.RobotSoftwareSuite``.
        :param sources: ``AWS::RoboMaker::RobotApplication.Sources``.
        :param current_revision_id: ``AWS::RoboMaker::RobotApplication.CurrentRevisionId``.
        :param name: ``AWS::RoboMaker::RobotApplication.Name``.
        :param tags: ``AWS::RoboMaker::RobotApplication.Tags``.
        """
        props = CfnRobotApplicationProps(robot_software_suite=robot_software_suite, sources=sources, current_revision_id=current_revision_id, name=name, tags=tags)

        jsii.create(CfnRobotApplication, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnRobotApplication":
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
    @jsii.member(jsii_name="attrCurrentRevisionId")
    def attr_current_revision_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: CurrentRevisionId
        """
        return jsii.get(self, "attrCurrentRevisionId")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::RoboMaker::RobotApplication.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="robotSoftwareSuite")
    def robot_software_suite(self) -> typing.Union["RobotSoftwareSuiteProperty", _IResolvable_9ceae33e]:
        """``AWS::RoboMaker::RobotApplication.RobotSoftwareSuite``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-robotsoftwaresuite
        """
        return jsii.get(self, "robotSoftwareSuite")

    @robot_software_suite.setter
    def robot_software_suite(self, value: typing.Union["RobotSoftwareSuiteProperty", _IResolvable_9ceae33e]) -> None:
        jsii.set(self, "robotSoftwareSuite", value)

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["SourceConfigProperty", _IResolvable_9ceae33e]]]:
        """``AWS::RoboMaker::RobotApplication.Sources``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-sources
        """
        return jsii.get(self, "sources")

    @sources.setter
    def sources(self, value: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["SourceConfigProperty", _IResolvable_9ceae33e]]]) -> None:
        jsii.set(self, "sources", value)

    @builtins.property
    @jsii.member(jsii_name="currentRevisionId")
    def current_revision_id(self) -> typing.Optional[str]:
        """``AWS::RoboMaker::RobotApplication.CurrentRevisionId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-currentrevisionid
        """
        return jsii.get(self, "currentRevisionId")

    @current_revision_id.setter
    def current_revision_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "currentRevisionId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::RoboMaker::RobotApplication.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "name", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_robomaker.CfnRobotApplication.RobotSoftwareSuiteProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'version': 'version'})
    class RobotSoftwareSuiteProperty():
        def __init__(self, *, name: str, version: str) -> None:
            """
            :param name: ``CfnRobotApplication.RobotSoftwareSuiteProperty.Name``.
            :param version: ``CfnRobotApplication.RobotSoftwareSuiteProperty.Version``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-robotapplication-robotsoftwaresuite.html
            """
            self._values = {
                'name': name,
                'version': version,
            }

        @builtins.property
        def name(self) -> str:
            """``CfnRobotApplication.RobotSoftwareSuiteProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-robotapplication-robotsoftwaresuite.html#cfn-robomaker-robotapplication-robotsoftwaresuite-name
            """
            return self._values.get('name')

        @builtins.property
        def version(self) -> str:
            """``CfnRobotApplication.RobotSoftwareSuiteProperty.Version``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-robotapplication-robotsoftwaresuite.html#cfn-robomaker-robotapplication-robotsoftwaresuite-version
            """
            return self._values.get('version')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RobotSoftwareSuiteProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_robomaker.CfnRobotApplication.SourceConfigProperty", jsii_struct_bases=[], name_mapping={'architecture': 'architecture', 's3_bucket': 's3Bucket', 's3_key': 's3Key'})
    class SourceConfigProperty():
        def __init__(self, *, architecture: str, s3_bucket: str, s3_key: str) -> None:
            """
            :param architecture: ``CfnRobotApplication.SourceConfigProperty.Architecture``.
            :param s3_bucket: ``CfnRobotApplication.SourceConfigProperty.S3Bucket``.
            :param s3_key: ``CfnRobotApplication.SourceConfigProperty.S3Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-robotapplication-sourceconfig.html
            """
            self._values = {
                'architecture': architecture,
                's3_bucket': s3_bucket,
                's3_key': s3_key,
            }

        @builtins.property
        def architecture(self) -> str:
            """``CfnRobotApplication.SourceConfigProperty.Architecture``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-robotapplication-sourceconfig.html#cfn-robomaker-robotapplication-sourceconfig-architecture
            """
            return self._values.get('architecture')

        @builtins.property
        def s3_bucket(self) -> str:
            """``CfnRobotApplication.SourceConfigProperty.S3Bucket``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-robotapplication-sourceconfig.html#cfn-robomaker-robotapplication-sourceconfig-s3bucket
            """
            return self._values.get('s3_bucket')

        @builtins.property
        def s3_key(self) -> str:
            """``CfnRobotApplication.SourceConfigProperty.S3Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-robotapplication-sourceconfig.html#cfn-robomaker-robotapplication-sourceconfig-s3key
            """
            return self._values.get('s3_key')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SourceConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_robomaker.CfnRobotApplicationProps", jsii_struct_bases=[], name_mapping={'robot_software_suite': 'robotSoftwareSuite', 'sources': 'sources', 'current_revision_id': 'currentRevisionId', 'name': 'name', 'tags': 'tags'})
class CfnRobotApplicationProps():
    def __init__(self, *, robot_software_suite: typing.Union["CfnRobotApplication.RobotSoftwareSuiteProperty", _IResolvable_9ceae33e], sources: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnRobotApplication.SourceConfigProperty", _IResolvable_9ceae33e]]], current_revision_id: typing.Optional[str]=None, name: typing.Optional[str]=None, tags: typing.Any=None) -> None:
        """Properties for defining a ``AWS::RoboMaker::RobotApplication``.

        :param robot_software_suite: ``AWS::RoboMaker::RobotApplication.RobotSoftwareSuite``.
        :param sources: ``AWS::RoboMaker::RobotApplication.Sources``.
        :param current_revision_id: ``AWS::RoboMaker::RobotApplication.CurrentRevisionId``.
        :param name: ``AWS::RoboMaker::RobotApplication.Name``.
        :param tags: ``AWS::RoboMaker::RobotApplication.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html
        """
        self._values = {
            'robot_software_suite': robot_software_suite,
            'sources': sources,
        }
        if current_revision_id is not None: self._values["current_revision_id"] = current_revision_id
        if name is not None: self._values["name"] = name
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def robot_software_suite(self) -> typing.Union["CfnRobotApplication.RobotSoftwareSuiteProperty", _IResolvable_9ceae33e]:
        """``AWS::RoboMaker::RobotApplication.RobotSoftwareSuite``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-robotsoftwaresuite
        """
        return self._values.get('robot_software_suite')

    @builtins.property
    def sources(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnRobotApplication.SourceConfigProperty", _IResolvable_9ceae33e]]]:
        """``AWS::RoboMaker::RobotApplication.Sources``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-sources
        """
        return self._values.get('sources')

    @builtins.property
    def current_revision_id(self) -> typing.Optional[str]:
        """``AWS::RoboMaker::RobotApplication.CurrentRevisionId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-currentrevisionid
        """
        return self._values.get('current_revision_id')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::RoboMaker::RobotApplication.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-name
        """
        return self._values.get('name')

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::RoboMaker::RobotApplication.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnRobotApplicationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnRobotApplicationVersion(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_robomaker.CfnRobotApplicationVersion"):
    """A CloudFormation ``AWS::RoboMaker::RobotApplicationVersion``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplicationversion.html
    cloudformationResource:
    :cloudformationResource:: AWS::RoboMaker::RobotApplicationVersion
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, application: str, current_revision_id: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::RoboMaker::RobotApplicationVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application: ``AWS::RoboMaker::RobotApplicationVersion.Application``.
        :param current_revision_id: ``AWS::RoboMaker::RobotApplicationVersion.CurrentRevisionId``.
        """
        props = CfnRobotApplicationVersionProps(application=application, current_revision_id=current_revision_id)

        jsii.create(CfnRobotApplicationVersion, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnRobotApplicationVersion":
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
    @jsii.member(jsii_name="application")
    def application(self) -> str:
        """``AWS::RoboMaker::RobotApplicationVersion.Application``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplicationversion.html#cfn-robomaker-robotapplicationversion-application
        """
        return jsii.get(self, "application")

    @application.setter
    def application(self, value: str) -> None:
        jsii.set(self, "application", value)

    @builtins.property
    @jsii.member(jsii_name="currentRevisionId")
    def current_revision_id(self) -> typing.Optional[str]:
        """``AWS::RoboMaker::RobotApplicationVersion.CurrentRevisionId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplicationversion.html#cfn-robomaker-robotapplicationversion-currentrevisionid
        """
        return jsii.get(self, "currentRevisionId")

    @current_revision_id.setter
    def current_revision_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "currentRevisionId", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_robomaker.CfnRobotApplicationVersionProps", jsii_struct_bases=[], name_mapping={'application': 'application', 'current_revision_id': 'currentRevisionId'})
class CfnRobotApplicationVersionProps():
    def __init__(self, *, application: str, current_revision_id: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::RoboMaker::RobotApplicationVersion``.

        :param application: ``AWS::RoboMaker::RobotApplicationVersion.Application``.
        :param current_revision_id: ``AWS::RoboMaker::RobotApplicationVersion.CurrentRevisionId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplicationversion.html
        """
        self._values = {
            'application': application,
        }
        if current_revision_id is not None: self._values["current_revision_id"] = current_revision_id

    @builtins.property
    def application(self) -> str:
        """``AWS::RoboMaker::RobotApplicationVersion.Application``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplicationversion.html#cfn-robomaker-robotapplicationversion-application
        """
        return self._values.get('application')

    @builtins.property
    def current_revision_id(self) -> typing.Optional[str]:
        """``AWS::RoboMaker::RobotApplicationVersion.CurrentRevisionId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplicationversion.html#cfn-robomaker-robotapplicationversion-currentrevisionid
        """
        return self._values.get('current_revision_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnRobotApplicationVersionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_robomaker.CfnRobotProps", jsii_struct_bases=[], name_mapping={'architecture': 'architecture', 'greengrass_group_id': 'greengrassGroupId', 'fleet': 'fleet', 'name': 'name', 'tags': 'tags'})
class CfnRobotProps():
    def __init__(self, *, architecture: str, greengrass_group_id: str, fleet: typing.Optional[str]=None, name: typing.Optional[str]=None, tags: typing.Any=None) -> None:
        """Properties for defining a ``AWS::RoboMaker::Robot``.

        :param architecture: ``AWS::RoboMaker::Robot.Architecture``.
        :param greengrass_group_id: ``AWS::RoboMaker::Robot.GreengrassGroupId``.
        :param fleet: ``AWS::RoboMaker::Robot.Fleet``.
        :param name: ``AWS::RoboMaker::Robot.Name``.
        :param tags: ``AWS::RoboMaker::Robot.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html
        """
        self._values = {
            'architecture': architecture,
            'greengrass_group_id': greengrass_group_id,
        }
        if fleet is not None: self._values["fleet"] = fleet
        if name is not None: self._values["name"] = name
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def architecture(self) -> str:
        """``AWS::RoboMaker::Robot.Architecture``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-architecture
        """
        return self._values.get('architecture')

    @builtins.property
    def greengrass_group_id(self) -> str:
        """``AWS::RoboMaker::Robot.GreengrassGroupId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-greengrassgroupid
        """
        return self._values.get('greengrass_group_id')

    @builtins.property
    def fleet(self) -> typing.Optional[str]:
        """``AWS::RoboMaker::Robot.Fleet``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-fleet
        """
        return self._values.get('fleet')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::RoboMaker::Robot.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-name
        """
        return self._values.get('name')

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::RoboMaker::Robot.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnRobotProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnSimulationApplication(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_robomaker.CfnSimulationApplication"):
    """A CloudFormation ``AWS::RoboMaker::SimulationApplication``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html
    cloudformationResource:
    :cloudformationResource:: AWS::RoboMaker::SimulationApplication
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, rendering_engine: typing.Union["RenderingEngineProperty", _IResolvable_9ceae33e], robot_software_suite: typing.Union["RobotSoftwareSuiteProperty", _IResolvable_9ceae33e], simulation_software_suite: typing.Union["SimulationSoftwareSuiteProperty", _IResolvable_9ceae33e], sources: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["SourceConfigProperty", _IResolvable_9ceae33e]]], current_revision_id: typing.Optional[str]=None, name: typing.Optional[str]=None, tags: typing.Any=None) -> None:
        """Create a new ``AWS::RoboMaker::SimulationApplication``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param rendering_engine: ``AWS::RoboMaker::SimulationApplication.RenderingEngine``.
        :param robot_software_suite: ``AWS::RoboMaker::SimulationApplication.RobotSoftwareSuite``.
        :param simulation_software_suite: ``AWS::RoboMaker::SimulationApplication.SimulationSoftwareSuite``.
        :param sources: ``AWS::RoboMaker::SimulationApplication.Sources``.
        :param current_revision_id: ``AWS::RoboMaker::SimulationApplication.CurrentRevisionId``.
        :param name: ``AWS::RoboMaker::SimulationApplication.Name``.
        :param tags: ``AWS::RoboMaker::SimulationApplication.Tags``.
        """
        props = CfnSimulationApplicationProps(rendering_engine=rendering_engine, robot_software_suite=robot_software_suite, simulation_software_suite=simulation_software_suite, sources=sources, current_revision_id=current_revision_id, name=name, tags=tags)

        jsii.create(CfnSimulationApplication, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnSimulationApplication":
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
    @jsii.member(jsii_name="attrCurrentRevisionId")
    def attr_current_revision_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: CurrentRevisionId
        """
        return jsii.get(self, "attrCurrentRevisionId")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::RoboMaker::SimulationApplication.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="renderingEngine")
    def rendering_engine(self) -> typing.Union["RenderingEngineProperty", _IResolvable_9ceae33e]:
        """``AWS::RoboMaker::SimulationApplication.RenderingEngine``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-renderingengine
        """
        return jsii.get(self, "renderingEngine")

    @rendering_engine.setter
    def rendering_engine(self, value: typing.Union["RenderingEngineProperty", _IResolvable_9ceae33e]) -> None:
        jsii.set(self, "renderingEngine", value)

    @builtins.property
    @jsii.member(jsii_name="robotSoftwareSuite")
    def robot_software_suite(self) -> typing.Union["RobotSoftwareSuiteProperty", _IResolvable_9ceae33e]:
        """``AWS::RoboMaker::SimulationApplication.RobotSoftwareSuite``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-robotsoftwaresuite
        """
        return jsii.get(self, "robotSoftwareSuite")

    @robot_software_suite.setter
    def robot_software_suite(self, value: typing.Union["RobotSoftwareSuiteProperty", _IResolvable_9ceae33e]) -> None:
        jsii.set(self, "robotSoftwareSuite", value)

    @builtins.property
    @jsii.member(jsii_name="simulationSoftwareSuite")
    def simulation_software_suite(self) -> typing.Union["SimulationSoftwareSuiteProperty", _IResolvable_9ceae33e]:
        """``AWS::RoboMaker::SimulationApplication.SimulationSoftwareSuite``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-simulationsoftwaresuite
        """
        return jsii.get(self, "simulationSoftwareSuite")

    @simulation_software_suite.setter
    def simulation_software_suite(self, value: typing.Union["SimulationSoftwareSuiteProperty", _IResolvable_9ceae33e]) -> None:
        jsii.set(self, "simulationSoftwareSuite", value)

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["SourceConfigProperty", _IResolvable_9ceae33e]]]:
        """``AWS::RoboMaker::SimulationApplication.Sources``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-sources
        """
        return jsii.get(self, "sources")

    @sources.setter
    def sources(self, value: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["SourceConfigProperty", _IResolvable_9ceae33e]]]) -> None:
        jsii.set(self, "sources", value)

    @builtins.property
    @jsii.member(jsii_name="currentRevisionId")
    def current_revision_id(self) -> typing.Optional[str]:
        """``AWS::RoboMaker::SimulationApplication.CurrentRevisionId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-currentrevisionid
        """
        return jsii.get(self, "currentRevisionId")

    @current_revision_id.setter
    def current_revision_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "currentRevisionId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::RoboMaker::SimulationApplication.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "name", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_robomaker.CfnSimulationApplication.RenderingEngineProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'version': 'version'})
    class RenderingEngineProperty():
        def __init__(self, *, name: str, version: str) -> None:
            """
            :param name: ``CfnSimulationApplication.RenderingEngineProperty.Name``.
            :param version: ``CfnSimulationApplication.RenderingEngineProperty.Version``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-renderingengine.html
            """
            self._values = {
                'name': name,
                'version': version,
            }

        @builtins.property
        def name(self) -> str:
            """``CfnSimulationApplication.RenderingEngineProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-renderingengine.html#cfn-robomaker-simulationapplication-renderingengine-name
            """
            return self._values.get('name')

        @builtins.property
        def version(self) -> str:
            """``CfnSimulationApplication.RenderingEngineProperty.Version``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-renderingengine.html#cfn-robomaker-simulationapplication-renderingengine-version
            """
            return self._values.get('version')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RenderingEngineProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_robomaker.CfnSimulationApplication.RobotSoftwareSuiteProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'version': 'version'})
    class RobotSoftwareSuiteProperty():
        def __init__(self, *, name: str, version: str) -> None:
            """
            :param name: ``CfnSimulationApplication.RobotSoftwareSuiteProperty.Name``.
            :param version: ``CfnSimulationApplication.RobotSoftwareSuiteProperty.Version``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-robotsoftwaresuite.html
            """
            self._values = {
                'name': name,
                'version': version,
            }

        @builtins.property
        def name(self) -> str:
            """``CfnSimulationApplication.RobotSoftwareSuiteProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-robotsoftwaresuite.html#cfn-robomaker-simulationapplication-robotsoftwaresuite-name
            """
            return self._values.get('name')

        @builtins.property
        def version(self) -> str:
            """``CfnSimulationApplication.RobotSoftwareSuiteProperty.Version``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-robotsoftwaresuite.html#cfn-robomaker-simulationapplication-robotsoftwaresuite-version
            """
            return self._values.get('version')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RobotSoftwareSuiteProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_robomaker.CfnSimulationApplication.SimulationSoftwareSuiteProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'version': 'version'})
    class SimulationSoftwareSuiteProperty():
        def __init__(self, *, name: str, version: str) -> None:
            """
            :param name: ``CfnSimulationApplication.SimulationSoftwareSuiteProperty.Name``.
            :param version: ``CfnSimulationApplication.SimulationSoftwareSuiteProperty.Version``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-simulationsoftwaresuite.html
            """
            self._values = {
                'name': name,
                'version': version,
            }

        @builtins.property
        def name(self) -> str:
            """``CfnSimulationApplication.SimulationSoftwareSuiteProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-simulationsoftwaresuite.html#cfn-robomaker-simulationapplication-simulationsoftwaresuite-name
            """
            return self._values.get('name')

        @builtins.property
        def version(self) -> str:
            """``CfnSimulationApplication.SimulationSoftwareSuiteProperty.Version``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-simulationsoftwaresuite.html#cfn-robomaker-simulationapplication-simulationsoftwaresuite-version
            """
            return self._values.get('version')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SimulationSoftwareSuiteProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_robomaker.CfnSimulationApplication.SourceConfigProperty", jsii_struct_bases=[], name_mapping={'architecture': 'architecture', 's3_bucket': 's3Bucket', 's3_key': 's3Key'})
    class SourceConfigProperty():
        def __init__(self, *, architecture: str, s3_bucket: str, s3_key: str) -> None:
            """
            :param architecture: ``CfnSimulationApplication.SourceConfigProperty.Architecture``.
            :param s3_bucket: ``CfnSimulationApplication.SourceConfigProperty.S3Bucket``.
            :param s3_key: ``CfnSimulationApplication.SourceConfigProperty.S3Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-sourceconfig.html
            """
            self._values = {
                'architecture': architecture,
                's3_bucket': s3_bucket,
                's3_key': s3_key,
            }

        @builtins.property
        def architecture(self) -> str:
            """``CfnSimulationApplication.SourceConfigProperty.Architecture``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-sourceconfig.html#cfn-robomaker-simulationapplication-sourceconfig-architecture
            """
            return self._values.get('architecture')

        @builtins.property
        def s3_bucket(self) -> str:
            """``CfnSimulationApplication.SourceConfigProperty.S3Bucket``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-sourceconfig.html#cfn-robomaker-simulationapplication-sourceconfig-s3bucket
            """
            return self._values.get('s3_bucket')

        @builtins.property
        def s3_key(self) -> str:
            """``CfnSimulationApplication.SourceConfigProperty.S3Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-sourceconfig.html#cfn-robomaker-simulationapplication-sourceconfig-s3key
            """
            return self._values.get('s3_key')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SourceConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_robomaker.CfnSimulationApplicationProps", jsii_struct_bases=[], name_mapping={'rendering_engine': 'renderingEngine', 'robot_software_suite': 'robotSoftwareSuite', 'simulation_software_suite': 'simulationSoftwareSuite', 'sources': 'sources', 'current_revision_id': 'currentRevisionId', 'name': 'name', 'tags': 'tags'})
class CfnSimulationApplicationProps():
    def __init__(self, *, rendering_engine: typing.Union["CfnSimulationApplication.RenderingEngineProperty", _IResolvable_9ceae33e], robot_software_suite: typing.Union["CfnSimulationApplication.RobotSoftwareSuiteProperty", _IResolvable_9ceae33e], simulation_software_suite: typing.Union["CfnSimulationApplication.SimulationSoftwareSuiteProperty", _IResolvable_9ceae33e], sources: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnSimulationApplication.SourceConfigProperty", _IResolvable_9ceae33e]]], current_revision_id: typing.Optional[str]=None, name: typing.Optional[str]=None, tags: typing.Any=None) -> None:
        """Properties for defining a ``AWS::RoboMaker::SimulationApplication``.

        :param rendering_engine: ``AWS::RoboMaker::SimulationApplication.RenderingEngine``.
        :param robot_software_suite: ``AWS::RoboMaker::SimulationApplication.RobotSoftwareSuite``.
        :param simulation_software_suite: ``AWS::RoboMaker::SimulationApplication.SimulationSoftwareSuite``.
        :param sources: ``AWS::RoboMaker::SimulationApplication.Sources``.
        :param current_revision_id: ``AWS::RoboMaker::SimulationApplication.CurrentRevisionId``.
        :param name: ``AWS::RoboMaker::SimulationApplication.Name``.
        :param tags: ``AWS::RoboMaker::SimulationApplication.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html
        """
        self._values = {
            'rendering_engine': rendering_engine,
            'robot_software_suite': robot_software_suite,
            'simulation_software_suite': simulation_software_suite,
            'sources': sources,
        }
        if current_revision_id is not None: self._values["current_revision_id"] = current_revision_id
        if name is not None: self._values["name"] = name
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def rendering_engine(self) -> typing.Union["CfnSimulationApplication.RenderingEngineProperty", _IResolvable_9ceae33e]:
        """``AWS::RoboMaker::SimulationApplication.RenderingEngine``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-renderingengine
        """
        return self._values.get('rendering_engine')

    @builtins.property
    def robot_software_suite(self) -> typing.Union["CfnSimulationApplication.RobotSoftwareSuiteProperty", _IResolvable_9ceae33e]:
        """``AWS::RoboMaker::SimulationApplication.RobotSoftwareSuite``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-robotsoftwaresuite
        """
        return self._values.get('robot_software_suite')

    @builtins.property
    def simulation_software_suite(self) -> typing.Union["CfnSimulationApplication.SimulationSoftwareSuiteProperty", _IResolvable_9ceae33e]:
        """``AWS::RoboMaker::SimulationApplication.SimulationSoftwareSuite``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-simulationsoftwaresuite
        """
        return self._values.get('simulation_software_suite')

    @builtins.property
    def sources(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnSimulationApplication.SourceConfigProperty", _IResolvable_9ceae33e]]]:
        """``AWS::RoboMaker::SimulationApplication.Sources``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-sources
        """
        return self._values.get('sources')

    @builtins.property
    def current_revision_id(self) -> typing.Optional[str]:
        """``AWS::RoboMaker::SimulationApplication.CurrentRevisionId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-currentrevisionid
        """
        return self._values.get('current_revision_id')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::RoboMaker::SimulationApplication.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-name
        """
        return self._values.get('name')

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::RoboMaker::SimulationApplication.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnSimulationApplicationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnSimulationApplicationVersion(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_robomaker.CfnSimulationApplicationVersion"):
    """A CloudFormation ``AWS::RoboMaker::SimulationApplicationVersion``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplicationversion.html
    cloudformationResource:
    :cloudformationResource:: AWS::RoboMaker::SimulationApplicationVersion
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, application: str, current_revision_id: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::RoboMaker::SimulationApplicationVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application: ``AWS::RoboMaker::SimulationApplicationVersion.Application``.
        :param current_revision_id: ``AWS::RoboMaker::SimulationApplicationVersion.CurrentRevisionId``.
        """
        props = CfnSimulationApplicationVersionProps(application=application, current_revision_id=current_revision_id)

        jsii.create(CfnSimulationApplicationVersion, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnSimulationApplicationVersion":
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
    @jsii.member(jsii_name="application")
    def application(self) -> str:
        """``AWS::RoboMaker::SimulationApplicationVersion.Application``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplicationversion.html#cfn-robomaker-simulationapplicationversion-application
        """
        return jsii.get(self, "application")

    @application.setter
    def application(self, value: str) -> None:
        jsii.set(self, "application", value)

    @builtins.property
    @jsii.member(jsii_name="currentRevisionId")
    def current_revision_id(self) -> typing.Optional[str]:
        """``AWS::RoboMaker::SimulationApplicationVersion.CurrentRevisionId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplicationversion.html#cfn-robomaker-simulationapplicationversion-currentrevisionid
        """
        return jsii.get(self, "currentRevisionId")

    @current_revision_id.setter
    def current_revision_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "currentRevisionId", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_robomaker.CfnSimulationApplicationVersionProps", jsii_struct_bases=[], name_mapping={'application': 'application', 'current_revision_id': 'currentRevisionId'})
class CfnSimulationApplicationVersionProps():
    def __init__(self, *, application: str, current_revision_id: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::RoboMaker::SimulationApplicationVersion``.

        :param application: ``AWS::RoboMaker::SimulationApplicationVersion.Application``.
        :param current_revision_id: ``AWS::RoboMaker::SimulationApplicationVersion.CurrentRevisionId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplicationversion.html
        """
        self._values = {
            'application': application,
        }
        if current_revision_id is not None: self._values["current_revision_id"] = current_revision_id

    @builtins.property
    def application(self) -> str:
        """``AWS::RoboMaker::SimulationApplicationVersion.Application``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplicationversion.html#cfn-robomaker-simulationapplicationversion-application
        """
        return self._values.get('application')

    @builtins.property
    def current_revision_id(self) -> typing.Optional[str]:
        """``AWS::RoboMaker::SimulationApplicationVersion.CurrentRevisionId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplicationversion.html#cfn-robomaker-simulationapplicationversion-currentrevisionid
        """
        return self._values.get('current_revision_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnSimulationApplicationVersionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnFleet",
    "CfnFleetProps",
    "CfnRobot",
    "CfnRobotApplication",
    "CfnRobotApplicationProps",
    "CfnRobotApplicationVersion",
    "CfnRobotApplicationVersionProps",
    "CfnRobotProps",
    "CfnSimulationApplication",
    "CfnSimulationApplicationProps",
    "CfnSimulationApplicationVersion",
    "CfnSimulationApplicationVersionProps",
]

publication.publish()
