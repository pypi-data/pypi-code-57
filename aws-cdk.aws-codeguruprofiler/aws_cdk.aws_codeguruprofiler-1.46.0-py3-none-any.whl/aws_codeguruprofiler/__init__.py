"""
## AWS::CodeGuruProfiler Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

Amazon CodeGuru Profiler collects runtime performance data from your live applications, and provides recommendations that can help you fine-tune your application performance.

### Installation

Import to your project:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_codeguruprofiler as codeguruprofiler
```

### Basic usage

Here's how to setup a profiling group and give your compute role permissions to publish to the profiling group to the profiling agent can publish profiling information:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# The execution role of your application that publishes to the ProfilingGroup via CodeGuru Profiler Profiling Agent. (the following is merely an example)
publish_app_role = Role(stack, "PublishAppRole",
    assumed_by=AccountRootPrincipal()
)

profiling_group = ProfilingGroup(stack, "MyProfilingGroup")
profiling_group.grant_publish(publish_app_role)
```
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

import aws_cdk.aws_iam
import aws_cdk.core


@jsii.implements(aws_cdk.core.IInspectable)
class CfnProfilingGroup(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codeguruprofiler.CfnProfilingGroup"):
    """A CloudFormation ``AWS::CodeGuruProfiler::ProfilingGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::CodeGuruProfiler::ProfilingGroup
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, profiling_group_name: str, agent_permissions: typing.Any=None) -> None:
        """Create a new ``AWS::CodeGuruProfiler::ProfilingGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param profiling_group_name: ``AWS::CodeGuruProfiler::ProfilingGroup.ProfilingGroupName``.
        :param agent_permissions: ``AWS::CodeGuruProfiler::ProfilingGroup.AgentPermissions``.
        """
        props = CfnProfilingGroupProps(profiling_group_name=profiling_group_name, agent_permissions=agent_permissions)

        jsii.create(CfnProfilingGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnProfilingGroup":
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
    @jsii.member(jsii_name="agentPermissions")
    def agent_permissions(self) -> typing.Any:
        """``AWS::CodeGuruProfiler::ProfilingGroup.AgentPermissions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-agentpermissions
        """
        return jsii.get(self, "agentPermissions")

    @agent_permissions.setter
    def agent_permissions(self, value: typing.Any) -> None:
        jsii.set(self, "agentPermissions", value)

    @builtins.property
    @jsii.member(jsii_name="profilingGroupName")
    def profiling_group_name(self) -> str:
        """``AWS::CodeGuruProfiler::ProfilingGroup.ProfilingGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-profilinggroupname
        """
        return jsii.get(self, "profilingGroupName")

    @profiling_group_name.setter
    def profiling_group_name(self, value: str) -> None:
        jsii.set(self, "profilingGroupName", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-codeguruprofiler.CfnProfilingGroupProps", jsii_struct_bases=[], name_mapping={'profiling_group_name': 'profilingGroupName', 'agent_permissions': 'agentPermissions'})
class CfnProfilingGroupProps():
    def __init__(self, *, profiling_group_name: str, agent_permissions: typing.Any=None) -> None:
        """Properties for defining a ``AWS::CodeGuruProfiler::ProfilingGroup``.

        :param profiling_group_name: ``AWS::CodeGuruProfiler::ProfilingGroup.ProfilingGroupName``.
        :param agent_permissions: ``AWS::CodeGuruProfiler::ProfilingGroup.AgentPermissions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html
        """
        self._values = {
            'profiling_group_name': profiling_group_name,
        }
        if agent_permissions is not None: self._values["agent_permissions"] = agent_permissions

    @builtins.property
    def profiling_group_name(self) -> str:
        """``AWS::CodeGuruProfiler::ProfilingGroup.ProfilingGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-profilinggroupname
        """
        return self._values.get('profiling_group_name')

    @builtins.property
    def agent_permissions(self) -> typing.Any:
        """``AWS::CodeGuruProfiler::ProfilingGroup.AgentPermissions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-agentpermissions
        """
        return self._values.get('agent_permissions')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnProfilingGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-codeguruprofiler.IProfilingGroup")
class IProfilingGroup(aws_cdk.core.IResource, jsii.compat.Protocol):
    """IResource represents a Profiling Group.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IProfilingGroupProxy

    @builtins.property
    @jsii.member(jsii_name="profilingGroupName")
    def profiling_group_name(self) -> str:
        """A name for the profiling group.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant access to publish profiling information to the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:ConfigureAgent
        - codeguru-profiler:PostAgentProfile

        :param grantee: Principal to grant publish rights to.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant access to read profiling information from the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:GetProfile
        - codeguru-profiler:DescribeProfilingGroup

        :param grantee: Principal to grant read rights to.

        stability
        :stability: experimental
        """
        ...


class _IProfilingGroupProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """IResource represents a Profiling Group.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-codeguruprofiler.IProfilingGroup"
    @builtins.property
    @jsii.member(jsii_name="profilingGroupName")
    def profiling_group_name(self) -> str:
        """A name for the profiling group.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "profilingGroupName")

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant access to publish profiling information to the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:ConfigureAgent
        - codeguru-profiler:PostAgentProfile

        :param grantee: Principal to grant publish rights to.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantPublish", [grantee])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant access to read profiling information from the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:GetProfile
        - codeguru-profiler:DescribeProfilingGroup

        :param grantee: Principal to grant read rights to.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantRead", [grantee])


@jsii.implements(IProfilingGroup)
class ProfilingGroup(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codeguruprofiler.ProfilingGroup"):
    """A new Profiling Group.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, profiling_group_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param profiling_group_name: A name for the profiling group. Default: - automatically generated name.

        stability
        :stability: experimental
        """
        props = ProfilingGroupProps(profiling_group_name=profiling_group_name)

        jsii.create(ProfilingGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromProfilingGroupArn")
    @builtins.classmethod
    def from_profiling_group_arn(cls, scope: aws_cdk.core.Construct, id: str, profiling_group_arn: str) -> "IProfilingGroup":
        """Import an existing Profiling Group provided an ARN.

        :param scope: The parent creating construct.
        :param id: The construct's name.
        :param profiling_group_arn: Profiling Group ARN.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromProfilingGroupArn", [scope, id, profiling_group_arn])

    @jsii.member(jsii_name="fromProfilingGroupName")
    @builtins.classmethod
    def from_profiling_group_name(cls, scope: aws_cdk.core.Construct, id: str, profiling_group_name: str) -> "IProfilingGroup":
        """Import an existing Profiling Group provided a Profiling Group Name.

        :param scope: The parent creating construct.
        :param id: The construct's name.
        :param profiling_group_name: Profiling Group Name.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromProfilingGroupName", [scope, id, profiling_group_name])

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant access to publish profiling information to the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:ConfigureAgent
        - codeguru-profiler:PostAgentProfile

        :param grantee: Principal to grant publish rights to.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantPublish", [grantee])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant access to read profiling information from the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:GetProfile
        - codeguru-profiler:DescribeProfilingGroup

        :param grantee: Principal to grant read rights to.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantRead", [grantee])

    @builtins.property
    @jsii.member(jsii_name="profilingGroupArn")
    def profiling_group_arn(self) -> str:
        """The ARN of the Profiling Group.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "profilingGroupArn")

    @builtins.property
    @jsii.member(jsii_name="profilingGroupName")
    def profiling_group_name(self) -> str:
        """The name of the Profiling Group.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "profilingGroupName")


@jsii.data_type(jsii_type="@aws-cdk/aws-codeguruprofiler.ProfilingGroupProps", jsii_struct_bases=[], name_mapping={'profiling_group_name': 'profilingGroupName'})
class ProfilingGroupProps():
    def __init__(self, *, profiling_group_name: typing.Optional[str]=None) -> None:
        """Properties for creating a new Profiling Group.

        :param profiling_group_name: A name for the profiling group. Default: - automatically generated name.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if profiling_group_name is not None: self._values["profiling_group_name"] = profiling_group_name

    @builtins.property
    def profiling_group_name(self) -> typing.Optional[str]:
        """A name for the profiling group.

        default
        :default: - automatically generated name.

        stability
        :stability: experimental
        """
        return self._values.get('profiling_group_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ProfilingGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnProfilingGroup",
    "CfnProfilingGroupProps",
    "IProfilingGroup",
    "ProfilingGroup",
    "ProfilingGroupProps",
]

publication.publish()
