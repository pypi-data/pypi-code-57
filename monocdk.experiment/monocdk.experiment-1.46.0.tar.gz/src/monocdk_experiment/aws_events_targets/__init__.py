import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from ..aws_batch import (IJobQueue as _IJobQueue_370c9b9b, IJobDefinition as _IJobDefinition_48a64d37)
from ..aws_codebuild import (IProject as _IProject_2a66e54e)
from ..aws_codepipeline import (IPipeline as _IPipeline_0346f658)
from ..aws_ec2 import (ISecurityGroup as _ISecurityGroup_d72ab8e8, SubnetSelection as _SubnetSelection_36a13cd6)
from ..aws_ecs import (ICluster as _ICluster_5cbcc408, TaskDefinition as _TaskDefinition_acfbb011)
from ..aws_events import (RuleTargetConfig as _RuleTargetConfig_98e52371, IRule as _IRule_f3f4a615, IRuleTarget as _IRuleTarget_41800a77, RuleTargetInput as _RuleTargetInput_01c951fa)
from ..aws_iam import (PolicyStatement as _PolicyStatement_f75dc775, IRole as _IRole_e69bbae4)
from ..aws_kinesis import (IStream as _IStream_c7ff3ed6)
from ..aws_lambda import (IFunction as _IFunction_1c1de0bc)
from ..aws_sns import (ITopic as _ITopic_ef0ebe0e)
from ..aws_sqs import (IQueue as _IQueue_b743f559)
from ..aws_stepfunctions import (IStateMachine as _IStateMachine_b2ad61f3)


@jsii.implements(_IRuleTarget_41800a77)
class AwsApi(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_events_targets.AwsApi"):
    """Use an AWS Lambda function that makes API calls as an event rule target.

    stability
    :stability: experimental
    """
    def __init__(self, *, policy_statement: typing.Optional[_PolicyStatement_f75dc775]=None, action: str, service: str, api_version: typing.Optional[str]=None, catch_error_pattern: typing.Optional[str]=None, parameters: typing.Any=None) -> None:
        """
        :param policy_statement: The IAM policy statement to allow the API call. Use only if resource restriction is needed. Default: - extract the permission from the API call
        :param action: The service action to call.
        :param service: The service to call.
        :param api_version: API version to use for the service. Default: - use latest available API version
        :param catch_error_pattern: The regex pattern to use to catch API errors. The ``code`` property of the ``Error`` object will be tested against this pattern. If there is a match an error will not be thrown. Default: - do not catch errors
        :param parameters: The parameters for the service action. Default: - no parameters

        stability
        :stability: experimental
        """
        props = AwsApiProps(policy_statement=policy_statement, action=action, service=service, api_version=api_version, catch_error_pattern=catch_error_pattern, parameters=parameters)

        jsii.create(AwsApi, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, rule: _IRule_f3f4a615, id: typing.Optional[str]=None) -> _RuleTargetConfig_98e52371:
        """Returns a RuleTarget that can be used to trigger this AwsApi as a result from an EventBridge event.

        :param rule: -
        :param id: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [rule, id])


@jsii.data_type(jsii_type="monocdk-experiment.aws_events_targets.AwsApiInput", jsii_struct_bases=[], name_mapping={'action': 'action', 'service': 'service', 'api_version': 'apiVersion', 'catch_error_pattern': 'catchErrorPattern', 'parameters': 'parameters'})
class AwsApiInput():
    def __init__(self, *, action: str, service: str, api_version: typing.Optional[str]=None, catch_error_pattern: typing.Optional[str]=None, parameters: typing.Any=None) -> None:
        """Rule target input for an AwsApi target.

        :param action: The service action to call.
        :param service: The service to call.
        :param api_version: API version to use for the service. Default: - use latest available API version
        :param catch_error_pattern: The regex pattern to use to catch API errors. The ``code`` property of the ``Error`` object will be tested against this pattern. If there is a match an error will not be thrown. Default: - do not catch errors
        :param parameters: The parameters for the service action. Default: - no parameters

        stability
        :stability: experimental
        """
        self._values = {
            'action': action,
            'service': service,
        }
        if api_version is not None: self._values["api_version"] = api_version
        if catch_error_pattern is not None: self._values["catch_error_pattern"] = catch_error_pattern
        if parameters is not None: self._values["parameters"] = parameters

    @builtins.property
    def action(self) -> str:
        """The service action to call.

        see
        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        stability
        :stability: experimental
        """
        return self._values.get('action')

    @builtins.property
    def service(self) -> str:
        """The service to call.

        see
        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        stability
        :stability: experimental
        """
        return self._values.get('service')

    @builtins.property
    def api_version(self) -> typing.Optional[str]:
        """API version to use for the service.

        default
        :default: - use latest available API version

        see
        :see: https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/locking-api-versions.html
        stability
        :stability: experimental
        """
        return self._values.get('api_version')

    @builtins.property
    def catch_error_pattern(self) -> typing.Optional[str]:
        """The regex pattern to use to catch API errors.

        The ``code`` property of the
        ``Error`` object will be tested against this pattern. If there is a match an
        error will not be thrown.

        default
        :default: - do not catch errors

        stability
        :stability: experimental
        """
        return self._values.get('catch_error_pattern')

    @builtins.property
    def parameters(self) -> typing.Any:
        """The parameters for the service action.

        default
        :default: - no parameters

        see
        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        stability
        :stability: experimental
        """
        return self._values.get('parameters')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AwsApiInput(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_events_targets.AwsApiProps", jsii_struct_bases=[AwsApiInput], name_mapping={'action': 'action', 'service': 'service', 'api_version': 'apiVersion', 'catch_error_pattern': 'catchErrorPattern', 'parameters': 'parameters', 'policy_statement': 'policyStatement'})
class AwsApiProps(AwsApiInput):
    def __init__(self, *, action: str, service: str, api_version: typing.Optional[str]=None, catch_error_pattern: typing.Optional[str]=None, parameters: typing.Any=None, policy_statement: typing.Optional[_PolicyStatement_f75dc775]=None) -> None:
        """Properties for an AwsApi target.

        :param action: The service action to call.
        :param service: The service to call.
        :param api_version: API version to use for the service. Default: - use latest available API version
        :param catch_error_pattern: The regex pattern to use to catch API errors. The ``code`` property of the ``Error`` object will be tested against this pattern. If there is a match an error will not be thrown. Default: - do not catch errors
        :param parameters: The parameters for the service action. Default: - no parameters
        :param policy_statement: The IAM policy statement to allow the API call. Use only if resource restriction is needed. Default: - extract the permission from the API call

        stability
        :stability: experimental
        """
        self._values = {
            'action': action,
            'service': service,
        }
        if api_version is not None: self._values["api_version"] = api_version
        if catch_error_pattern is not None: self._values["catch_error_pattern"] = catch_error_pattern
        if parameters is not None: self._values["parameters"] = parameters
        if policy_statement is not None: self._values["policy_statement"] = policy_statement

    @builtins.property
    def action(self) -> str:
        """The service action to call.

        see
        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        stability
        :stability: experimental
        """
        return self._values.get('action')

    @builtins.property
    def service(self) -> str:
        """The service to call.

        see
        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        stability
        :stability: experimental
        """
        return self._values.get('service')

    @builtins.property
    def api_version(self) -> typing.Optional[str]:
        """API version to use for the service.

        default
        :default: - use latest available API version

        see
        :see: https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/locking-api-versions.html
        stability
        :stability: experimental
        """
        return self._values.get('api_version')

    @builtins.property
    def catch_error_pattern(self) -> typing.Optional[str]:
        """The regex pattern to use to catch API errors.

        The ``code`` property of the
        ``Error`` object will be tested against this pattern. If there is a match an
        error will not be thrown.

        default
        :default: - do not catch errors

        stability
        :stability: experimental
        """
        return self._values.get('catch_error_pattern')

    @builtins.property
    def parameters(self) -> typing.Any:
        """The parameters for the service action.

        default
        :default: - no parameters

        see
        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        stability
        :stability: experimental
        """
        return self._values.get('parameters')

    @builtins.property
    def policy_statement(self) -> typing.Optional[_PolicyStatement_f75dc775]:
        """The IAM policy statement to allow the API call.

        Use only if
        resource restriction is needed.

        default
        :default: - extract the permission from the API call

        stability
        :stability: experimental
        """
        return self._values.get('policy_statement')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AwsApiProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IRuleTarget_41800a77)
class BatchJob(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_events_targets.BatchJob"):
    """Use an AWS Batch Job / Queue as an event rule target.

    stability
    :stability: experimental
    """
    def __init__(self, job_queue: _IJobQueue_370c9b9b, job_definition: _IJobDefinition_48a64d37, *, attempts: typing.Optional[jsii.Number]=None, event: typing.Optional[_RuleTargetInput_01c951fa]=None, job_name: typing.Optional[str]=None, size: typing.Optional[jsii.Number]=None) -> None:
        """
        :param job_queue: -
        :param job_definition: -
        :param attempts: The number of times to attempt to retry, if the job fails. Valid values are 1–10. Default: no retryStrategy is set
        :param event: The event to send to the Lambda. This will be the payload sent to the Lambda Function. Default: the entire EventBridge event
        :param job_name: The name of the submitted job. Default: - Automatically generated
        :param size: The size of the array, if this is an array batch job. Valid values are integers between 2 and 10,000. Default: no arrayProperties are set

        stability
        :stability: experimental
        """
        props = BatchJobProps(attempts=attempts, event=event, job_name=job_name, size=size)

        jsii.create(BatchJob, self, [job_queue, job_definition, props])

    @jsii.member(jsii_name="bind")
    def bind(self, rule: _IRule_f3f4a615, _id: typing.Optional[str]=None) -> _RuleTargetConfig_98e52371:
        """Returns a RuleTarget that can be used to trigger queue this batch job as a result from an EventBridge event.

        :param rule: -
        :param _id: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [rule, _id])


@jsii.data_type(jsii_type="monocdk-experiment.aws_events_targets.BatchJobProps", jsii_struct_bases=[], name_mapping={'attempts': 'attempts', 'event': 'event', 'job_name': 'jobName', 'size': 'size'})
class BatchJobProps():
    def __init__(self, *, attempts: typing.Optional[jsii.Number]=None, event: typing.Optional[_RuleTargetInput_01c951fa]=None, job_name: typing.Optional[str]=None, size: typing.Optional[jsii.Number]=None) -> None:
        """Customize the Batch Job Event Target.

        :param attempts: The number of times to attempt to retry, if the job fails. Valid values are 1–10. Default: no retryStrategy is set
        :param event: The event to send to the Lambda. This will be the payload sent to the Lambda Function. Default: the entire EventBridge event
        :param job_name: The name of the submitted job. Default: - Automatically generated
        :param size: The size of the array, if this is an array batch job. Valid values are integers between 2 and 10,000. Default: no arrayProperties are set

        stability
        :stability: experimental
        """
        self._values = {
        }
        if attempts is not None: self._values["attempts"] = attempts
        if event is not None: self._values["event"] = event
        if job_name is not None: self._values["job_name"] = job_name
        if size is not None: self._values["size"] = size

    @builtins.property
    def attempts(self) -> typing.Optional[jsii.Number]:
        """The number of times to attempt to retry, if the job fails.

        Valid values are 1–10.

        default
        :default: no retryStrategy is set

        stability
        :stability: experimental
        """
        return self._values.get('attempts')

    @builtins.property
    def event(self) -> typing.Optional[_RuleTargetInput_01c951fa]:
        """The event to send to the Lambda.

        This will be the payload sent to the Lambda Function.

        default
        :default: the entire EventBridge event

        stability
        :stability: experimental
        """
        return self._values.get('event')

    @builtins.property
    def job_name(self) -> typing.Optional[str]:
        """The name of the submitted job.

        default
        :default: - Automatically generated

        stability
        :stability: experimental
        """
        return self._values.get('job_name')

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        """The size of the array, if this is an array batch job.

        Valid values are integers between 2 and 10,000.

        default
        :default: no arrayProperties are set

        stability
        :stability: experimental
        """
        return self._values.get('size')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BatchJobProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IRuleTarget_41800a77)
class CodeBuildProject(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_events_targets.CodeBuildProject"):
    """Start a CodeBuild build when an Amazon EventBridge rule is triggered.

    stability
    :stability: experimental
    """
    def __init__(self, project: _IProject_2a66e54e, *, event: typing.Optional[_RuleTargetInput_01c951fa]=None) -> None:
        """
        :param project: -
        :param event: The event to send to CodeBuild. This will be the payload for the StartBuild API. Default: - the entire EventBridge event

        stability
        :stability: experimental
        """
        props = CodeBuildProjectProps(event=event)

        jsii.create(CodeBuildProject, self, [project, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _rule: _IRule_f3f4a615, _id: typing.Optional[str]=None) -> _RuleTargetConfig_98e52371:
        """Allows using build projects as event rule targets.

        :param _rule: -
        :param _id: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_rule, _id])


@jsii.data_type(jsii_type="monocdk-experiment.aws_events_targets.CodeBuildProjectProps", jsii_struct_bases=[], name_mapping={'event': 'event'})
class CodeBuildProjectProps():
    def __init__(self, *, event: typing.Optional[_RuleTargetInput_01c951fa]=None) -> None:
        """Customize the CodeBuild Event Target.

        :param event: The event to send to CodeBuild. This will be the payload for the StartBuild API. Default: - the entire EventBridge event

        stability
        :stability: experimental
        """
        self._values = {
        }
        if event is not None: self._values["event"] = event

    @builtins.property
    def event(self) -> typing.Optional[_RuleTargetInput_01c951fa]:
        """The event to send to CodeBuild.

        This will be the payload for the StartBuild API.

        default
        :default: - the entire EventBridge event

        stability
        :stability: experimental
        """
        return self._values.get('event')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CodeBuildProjectProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IRuleTarget_41800a77)
class CodePipeline(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_events_targets.CodePipeline"):
    """Allows the pipeline to be used as an EventBridge rule target.

    stability
    :stability: experimental
    """
    def __init__(self, pipeline: _IPipeline_0346f658, *, event_role: typing.Optional[_IRole_e69bbae4]=None) -> None:
        """
        :param pipeline: -
        :param event_role: The role to assume before invoking the target (i.e., the pipeline) when the given rule is triggered. Default: - a new role will be created

        stability
        :stability: experimental
        """
        options = CodePipelineTargetOptions(event_role=event_role)

        jsii.create(CodePipeline, self, [pipeline, options])

    @jsii.member(jsii_name="bind")
    def bind(self, _rule: _IRule_f3f4a615, _id: typing.Optional[str]=None) -> _RuleTargetConfig_98e52371:
        """Returns the rule target specification.

        NOTE: Do not use the various ``inputXxx`` options. They can be set in a call to ``addTarget``.

        :param _rule: -
        :param _id: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_rule, _id])


@jsii.data_type(jsii_type="monocdk-experiment.aws_events_targets.CodePipelineTargetOptions", jsii_struct_bases=[], name_mapping={'event_role': 'eventRole'})
class CodePipelineTargetOptions():
    def __init__(self, *, event_role: typing.Optional[_IRole_e69bbae4]=None) -> None:
        """Customization options when creating a {@link CodePipeline} event target.

        :param event_role: The role to assume before invoking the target (i.e., the pipeline) when the given rule is triggered. Default: - a new role will be created

        stability
        :stability: experimental
        """
        self._values = {
        }
        if event_role is not None: self._values["event_role"] = event_role

    @builtins.property
    def event_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The role to assume before invoking the target (i.e., the pipeline) when the given rule is triggered.

        default
        :default: - a new role will be created

        stability
        :stability: experimental
        """
        return self._values.get('event_role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CodePipelineTargetOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_events_targets.ContainerOverride", jsii_struct_bases=[], name_mapping={'container_name': 'containerName', 'command': 'command', 'cpu': 'cpu', 'environment': 'environment', 'memory_limit': 'memoryLimit', 'memory_reservation': 'memoryReservation'})
class ContainerOverride():
    def __init__(self, *, container_name: str, command: typing.Optional[typing.List[str]]=None, cpu: typing.Optional[jsii.Number]=None, environment: typing.Optional[typing.List["TaskEnvironmentVariable"]]=None, memory_limit: typing.Optional[jsii.Number]=None, memory_reservation: typing.Optional[jsii.Number]=None) -> None:
        """
        :param container_name: Name of the container inside the task definition.
        :param command: Command to run inside the container. Default: Default command
        :param cpu: The number of cpu units reserved for the container. Default: The default value from the task definition.
        :param environment: Variables to set in the container's environment.
        :param memory_limit: Hard memory limit on the container. Default: The default value from the task definition.
        :param memory_reservation: Soft memory limit on the container. Default: The default value from the task definition.

        stability
        :stability: experimental
        """
        self._values = {
            'container_name': container_name,
        }
        if command is not None: self._values["command"] = command
        if cpu is not None: self._values["cpu"] = cpu
        if environment is not None: self._values["environment"] = environment
        if memory_limit is not None: self._values["memory_limit"] = memory_limit
        if memory_reservation is not None: self._values["memory_reservation"] = memory_reservation

    @builtins.property
    def container_name(self) -> str:
        """Name of the container inside the task definition.

        stability
        :stability: experimental
        """
        return self._values.get('container_name')

    @builtins.property
    def command(self) -> typing.Optional[typing.List[str]]:
        """Command to run inside the container.

        default
        :default: Default command

        stability
        :stability: experimental
        """
        return self._values.get('command')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units reserved for the container.

        default
        :default: The default value from the task definition.

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @builtins.property
    def environment(self) -> typing.Optional[typing.List["TaskEnvironmentVariable"]]:
        """Variables to set in the container's environment.

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def memory_limit(self) -> typing.Optional[jsii.Number]:
        """Hard memory limit on the container.

        default
        :default: The default value from the task definition.

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit')

    @builtins.property
    def memory_reservation(self) -> typing.Optional[jsii.Number]:
        """Soft memory limit on the container.

        default
        :default: The default value from the task definition.

        stability
        :stability: experimental
        """
        return self._values.get('memory_reservation')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ContainerOverride(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IRuleTarget_41800a77)
class EcsTask(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_events_targets.EcsTask"):
    """Start a task on an ECS cluster.

    stability
    :stability: experimental
    """
    def __init__(self, *, cluster: _ICluster_5cbcc408, task_definition: _TaskDefinition_acfbb011, container_overrides: typing.Optional[typing.List["ContainerOverride"]]=None, security_group: typing.Optional[_ISecurityGroup_d72ab8e8]=None, security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]=None, subnet_selection: typing.Optional[_SubnetSelection_36a13cd6]=None, task_count: typing.Optional[jsii.Number]=None) -> None:
        """
        :param cluster: Cluster where service will be deployed.
        :param task_definition: Task Definition of the task that should be started.
        :param container_overrides: Container setting overrides. Key is the name of the container to override, value is the values you want to override.
        :param security_group: Existing security group to use for the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: A new security group is created
        :param security_groups: Existing security groups to use for the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: A new security group is created
        :param subnet_selection: In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        :param task_count: How many tasks should be started when this event is triggered. Default: 1

        stability
        :stability: experimental
        """
        props = EcsTaskProps(cluster=cluster, task_definition=task_definition, container_overrides=container_overrides, security_group=security_group, security_groups=security_groups, subnet_selection=subnet_selection, task_count=task_count)

        jsii.create(EcsTask, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _rule: _IRule_f3f4a615, _id: typing.Optional[str]=None) -> _RuleTargetConfig_98e52371:
        """Allows using tasks as target of EventBridge events.

        :param _rule: -
        :param _id: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_rule, _id])

    @builtins.property
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> typing.Optional[_ISecurityGroup_d72ab8e8]:
        """The security group associated with the task.

        Only applicable with awsvpc network mode.

        default
        :default: - A new security group is created.

        deprecated
        :deprecated: use securityGroups instead.

        stability
        :stability: deprecated
        """
        return jsii.get(self, "securityGroup")

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]:
        """The security groups associated with the task.

        Only applicable with awsvpc network mode.

        default
        :default: - A new security group is created.

        stability
        :stability: experimental
        """
        return jsii.get(self, "securityGroups")


@jsii.data_type(jsii_type="monocdk-experiment.aws_events_targets.EcsTaskProps", jsii_struct_bases=[], name_mapping={'cluster': 'cluster', 'task_definition': 'taskDefinition', 'container_overrides': 'containerOverrides', 'security_group': 'securityGroup', 'security_groups': 'securityGroups', 'subnet_selection': 'subnetSelection', 'task_count': 'taskCount'})
class EcsTaskProps():
    def __init__(self, *, cluster: _ICluster_5cbcc408, task_definition: _TaskDefinition_acfbb011, container_overrides: typing.Optional[typing.List["ContainerOverride"]]=None, security_group: typing.Optional[_ISecurityGroup_d72ab8e8]=None, security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]=None, subnet_selection: typing.Optional[_SubnetSelection_36a13cd6]=None, task_count: typing.Optional[jsii.Number]=None) -> None:
        """Properties to define an ECS Event Task.

        :param cluster: Cluster where service will be deployed.
        :param task_definition: Task Definition of the task that should be started.
        :param container_overrides: Container setting overrides. Key is the name of the container to override, value is the values you want to override.
        :param security_group: Existing security group to use for the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: A new security group is created
        :param security_groups: Existing security groups to use for the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: A new security group is created
        :param subnet_selection: In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        :param task_count: How many tasks should be started when this event is triggered. Default: 1

        stability
        :stability: experimental
        """
        if isinstance(subnet_selection, dict): subnet_selection = _SubnetSelection_36a13cd6(**subnet_selection)
        self._values = {
            'cluster': cluster,
            'task_definition': task_definition,
        }
        if container_overrides is not None: self._values["container_overrides"] = container_overrides
        if security_group is not None: self._values["security_group"] = security_group
        if security_groups is not None: self._values["security_groups"] = security_groups
        if subnet_selection is not None: self._values["subnet_selection"] = subnet_selection
        if task_count is not None: self._values["task_count"] = task_count

    @builtins.property
    def cluster(self) -> _ICluster_5cbcc408:
        """Cluster where service will be deployed.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def task_definition(self) -> _TaskDefinition_acfbb011:
        """Task Definition of the task that should be started.

        stability
        :stability: experimental
        """
        return self._values.get('task_definition')

    @builtins.property
    def container_overrides(self) -> typing.Optional[typing.List["ContainerOverride"]]:
        """Container setting overrides.

        Key is the name of the container to override, value is the
        values you want to override.

        stability
        :stability: experimental
        """
        return self._values.get('container_overrides')

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_d72ab8e8]:
        """Existing security group to use for the task's ENIs.

        (Only applicable in case the TaskDefinition is configured for AwsVpc networking)

        default
        :default: A new security group is created

        deprecated
        :deprecated: use securityGroups instead

        stability
        :stability: deprecated
        """
        return self._values.get('security_group')

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]:
        """Existing security groups to use for the task's ENIs.

        (Only applicable in case the TaskDefinition is configured for AwsVpc networking)

        default
        :default: A new security group is created

        stability
        :stability: experimental
        """
        return self._values.get('security_groups')

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """In what subnets to place the task's ENIs.

        (Only applicable in case the TaskDefinition is configured for AwsVpc networking)

        default
        :default: Private subnets

        stability
        :stability: experimental
        """
        return self._values.get('subnet_selection')

    @builtins.property
    def task_count(self) -> typing.Optional[jsii.Number]:
        """How many tasks should be started when this event is triggered.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('task_count')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EcsTaskProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IRuleTarget_41800a77)
class KinesisStream(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_events_targets.KinesisStream"):
    """Use a Kinesis Stream as a target for AWS CloudWatch event rules.

    stability
    :stability: experimental

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        # put to a Kinesis stream every time code is committed
        # to a CodeCommit repository
        repository.on_commit(targets.KinesisStream(stream))
    """
    def __init__(self, stream: _IStream_c7ff3ed6, *, message: typing.Optional[_RuleTargetInput_01c951fa]=None, partition_key_path: typing.Optional[str]=None) -> None:
        """
        :param stream: -
        :param message: The message to send to the stream. Must be a valid JSON text passed to the target stream. Default: - the entire CloudWatch event
        :param partition_key_path: Partition Key Path for records sent to this stream. Default: - eventId as the partition key

        stability
        :stability: experimental
        """
        props = KinesisStreamProps(message=message, partition_key_path=partition_key_path)

        jsii.create(KinesisStream, self, [stream, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _rule: _IRule_f3f4a615, _id: typing.Optional[str]=None) -> _RuleTargetConfig_98e52371:
        """Returns a RuleTarget that can be used to trigger this Kinesis Stream as a result from a CloudWatch event.

        :param _rule: -
        :param _id: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_rule, _id])


@jsii.data_type(jsii_type="monocdk-experiment.aws_events_targets.KinesisStreamProps", jsii_struct_bases=[], name_mapping={'message': 'message', 'partition_key_path': 'partitionKeyPath'})
class KinesisStreamProps():
    def __init__(self, *, message: typing.Optional[_RuleTargetInput_01c951fa]=None, partition_key_path: typing.Optional[str]=None) -> None:
        """Customize the Kinesis Stream Event Target.

        :param message: The message to send to the stream. Must be a valid JSON text passed to the target stream. Default: - the entire CloudWatch event
        :param partition_key_path: Partition Key Path for records sent to this stream. Default: - eventId as the partition key

        stability
        :stability: experimental
        """
        self._values = {
        }
        if message is not None: self._values["message"] = message
        if partition_key_path is not None: self._values["partition_key_path"] = partition_key_path

    @builtins.property
    def message(self) -> typing.Optional[_RuleTargetInput_01c951fa]:
        """The message to send to the stream.

        Must be a valid JSON text passed to the target stream.

        default
        :default: - the entire CloudWatch event

        stability
        :stability: experimental
        """
        return self._values.get('message')

    @builtins.property
    def partition_key_path(self) -> typing.Optional[str]:
        """Partition Key Path for records sent to this stream.

        default
        :default: - eventId as the partition key

        stability
        :stability: experimental
        """
        return self._values.get('partition_key_path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'KinesisStreamProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IRuleTarget_41800a77)
class LambdaFunction(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_events_targets.LambdaFunction"):
    """Use an AWS Lambda function as an event rule target.

    stability
    :stability: experimental
    """
    def __init__(self, handler: _IFunction_1c1de0bc, *, event: typing.Optional[_RuleTargetInput_01c951fa]=None) -> None:
        """
        :param handler: -
        :param event: The event to send to the Lambda. This will be the payload sent to the Lambda Function. Default: the entire EventBridge event

        stability
        :stability: experimental
        """
        props = LambdaFunctionProps(event=event)

        jsii.create(LambdaFunction, self, [handler, props])

    @jsii.member(jsii_name="bind")
    def bind(self, rule: _IRule_f3f4a615, _id: typing.Optional[str]=None) -> _RuleTargetConfig_98e52371:
        """Returns a RuleTarget that can be used to trigger this Lambda as a result from an EventBridge event.

        :param rule: -
        :param _id: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [rule, _id])


@jsii.data_type(jsii_type="monocdk-experiment.aws_events_targets.LambdaFunctionProps", jsii_struct_bases=[], name_mapping={'event': 'event'})
class LambdaFunctionProps():
    def __init__(self, *, event: typing.Optional[_RuleTargetInput_01c951fa]=None) -> None:
        """Customize the Lambda Event Target.

        :param event: The event to send to the Lambda. This will be the payload sent to the Lambda Function. Default: the entire EventBridge event

        stability
        :stability: experimental
        """
        self._values = {
        }
        if event is not None: self._values["event"] = event

    @builtins.property
    def event(self) -> typing.Optional[_RuleTargetInput_01c951fa]:
        """The event to send to the Lambda.

        This will be the payload sent to the Lambda Function.

        default
        :default: the entire EventBridge event

        stability
        :stability: experimental
        """
        return self._values.get('event')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LambdaFunctionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IRuleTarget_41800a77)
class SfnStateMachine(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_events_targets.SfnStateMachine"):
    """Use a StepFunctions state machine as a target for Amazon EventBridge rules.

    stability
    :stability: experimental
    """
    def __init__(self, machine: _IStateMachine_b2ad61f3, *, input: typing.Optional[_RuleTargetInput_01c951fa]=None) -> None:
        """
        :param machine: -
        :param input: The input to the state machine execution. Default: the entire EventBridge event

        stability
        :stability: experimental
        """
        props = SfnStateMachineProps(input=input)

        jsii.create(SfnStateMachine, self, [machine, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _rule: _IRule_f3f4a615, _id: typing.Optional[str]=None) -> _RuleTargetConfig_98e52371:
        """Returns a properties that are used in an Rule to trigger this State Machine.

        :param _rule: -
        :param _id: -

        see
        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/resource-based-policies-eventbridge.html#sns-permissions
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_rule, _id])

    @builtins.property
    @jsii.member(jsii_name="machine")
    def machine(self) -> _IStateMachine_b2ad61f3:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "machine")


@jsii.data_type(jsii_type="monocdk-experiment.aws_events_targets.SfnStateMachineProps", jsii_struct_bases=[], name_mapping={'input': 'input'})
class SfnStateMachineProps():
    def __init__(self, *, input: typing.Optional[_RuleTargetInput_01c951fa]=None) -> None:
        """Customize the Step Functions State Machine target.

        :param input: The input to the state machine execution. Default: the entire EventBridge event

        stability
        :stability: experimental
        """
        self._values = {
        }
        if input is not None: self._values["input"] = input

    @builtins.property
    def input(self) -> typing.Optional[_RuleTargetInput_01c951fa]:
        """The input to the state machine execution.

        default
        :default: the entire EventBridge event

        stability
        :stability: experimental
        """
        return self._values.get('input')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SfnStateMachineProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IRuleTarget_41800a77)
class SnsTopic(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_events_targets.SnsTopic"):
    """Use an SNS topic as a target for Amazon EventBridge rules.

    stability
    :stability: experimental

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        # publish to an SNS topic every time code is committed
        # to a CodeCommit repository
        repository.on_commit(targets.SnsTopic(topic))
    """
    def __init__(self, topic: _ITopic_ef0ebe0e, *, message: typing.Optional[_RuleTargetInput_01c951fa]=None) -> None:
        """
        :param topic: -
        :param message: The message to send to the topic. Default: the entire EventBridge event

        stability
        :stability: experimental
        """
        props = SnsTopicProps(message=message)

        jsii.create(SnsTopic, self, [topic, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _rule: _IRule_f3f4a615, _id: typing.Optional[str]=None) -> _RuleTargetConfig_98e52371:
        """Returns a RuleTarget that can be used to trigger this SNS topic as a result from an EventBridge event.

        :param _rule: -
        :param _id: -

        see
        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/resource-based-policies-eventbridge.html#sns-permissions
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_rule, _id])

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> _ITopic_ef0ebe0e:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "topic")


@jsii.data_type(jsii_type="monocdk-experiment.aws_events_targets.SnsTopicProps", jsii_struct_bases=[], name_mapping={'message': 'message'})
class SnsTopicProps():
    def __init__(self, *, message: typing.Optional[_RuleTargetInput_01c951fa]=None) -> None:
        """Customize the SNS Topic Event Target.

        :param message: The message to send to the topic. Default: the entire EventBridge event

        stability
        :stability: experimental
        """
        self._values = {
        }
        if message is not None: self._values["message"] = message

    @builtins.property
    def message(self) -> typing.Optional[_RuleTargetInput_01c951fa]:
        """The message to send to the topic.

        default
        :default: the entire EventBridge event

        stability
        :stability: experimental
        """
        return self._values.get('message')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SnsTopicProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IRuleTarget_41800a77)
class SqsQueue(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_events_targets.SqsQueue"):
    """Use an SQS Queue as a target for Amazon EventBridge rules.

    stability
    :stability: experimental

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        # publish to an SQS queue every time code is committed
        # to a CodeCommit repository
        repository.on_commit(targets.SqsQueue(queue))
    """
    def __init__(self, queue: _IQueue_b743f559, *, message: typing.Optional[_RuleTargetInput_01c951fa]=None, message_group_id: typing.Optional[str]=None) -> None:
        """
        :param queue: -
        :param message: The message to send to the queue. Must be a valid JSON text passed to the target queue. Default: the entire EventBridge event
        :param message_group_id: Message Group ID for messages sent to this queue. Required for FIFO queues, leave empty for regular queues. Default: - no message group ID (regular queue)

        stability
        :stability: experimental
        """
        props = SqsQueueProps(message=message, message_group_id=message_group_id)

        jsii.create(SqsQueue, self, [queue, props])

    @jsii.member(jsii_name="bind")
    def bind(self, rule: _IRule_f3f4a615, _id: typing.Optional[str]=None) -> _RuleTargetConfig_98e52371:
        """Returns a RuleTarget that can be used to trigger this SQS queue as a result from an EventBridge event.

        :param rule: -
        :param _id: -

        see
        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/resource-based-policies-eventbridge.html#sqs-permissions
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [rule, _id])

    @builtins.property
    @jsii.member(jsii_name="queue")
    def queue(self) -> _IQueue_b743f559:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "queue")


@jsii.data_type(jsii_type="monocdk-experiment.aws_events_targets.SqsQueueProps", jsii_struct_bases=[], name_mapping={'message': 'message', 'message_group_id': 'messageGroupId'})
class SqsQueueProps():
    def __init__(self, *, message: typing.Optional[_RuleTargetInput_01c951fa]=None, message_group_id: typing.Optional[str]=None) -> None:
        """Customize the SQS Queue Event Target.

        :param message: The message to send to the queue. Must be a valid JSON text passed to the target queue. Default: the entire EventBridge event
        :param message_group_id: Message Group ID for messages sent to this queue. Required for FIFO queues, leave empty for regular queues. Default: - no message group ID (regular queue)

        stability
        :stability: experimental
        """
        self._values = {
        }
        if message is not None: self._values["message"] = message
        if message_group_id is not None: self._values["message_group_id"] = message_group_id

    @builtins.property
    def message(self) -> typing.Optional[_RuleTargetInput_01c951fa]:
        """The message to send to the queue.

        Must be a valid JSON text passed to the target queue.

        default
        :default: the entire EventBridge event

        stability
        :stability: experimental
        """
        return self._values.get('message')

    @builtins.property
    def message_group_id(self) -> typing.Optional[str]:
        """Message Group ID for messages sent to this queue.

        Required for FIFO queues, leave empty for regular queues.

        default
        :default: - no message group ID (regular queue)

        stability
        :stability: experimental
        """
        return self._values.get('message_group_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SqsQueueProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_events_targets.TaskEnvironmentVariable", jsii_struct_bases=[], name_mapping={'name': 'name', 'value': 'value'})
class TaskEnvironmentVariable():
    def __init__(self, *, name: str, value: str) -> None:
        """An environment variable to be set in the container run as a task.

        :param name: Name for the environment variable. Exactly one of ``name`` and ``namePath`` must be specified.
        :param value: Value of the environment variable. Exactly one of ``value`` and ``valuePath`` must be specified.

        stability
        :stability: experimental
        """
        self._values = {
            'name': name,
            'value': value,
        }

    @builtins.property
    def name(self) -> str:
        """Name for the environment variable.

        Exactly one of ``name`` and ``namePath`` must be specified.

        stability
        :stability: experimental
        """
        return self._values.get('name')

    @builtins.property
    def value(self) -> str:
        """Value of the environment variable.

        Exactly one of ``value`` and ``valuePath`` must be specified.

        stability
        :stability: experimental
        """
        return self._values.get('value')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TaskEnvironmentVariable(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "AwsApi",
    "AwsApiInput",
    "AwsApiProps",
    "BatchJob",
    "BatchJobProps",
    "CodeBuildProject",
    "CodeBuildProjectProps",
    "CodePipeline",
    "CodePipelineTargetOptions",
    "ContainerOverride",
    "EcsTask",
    "EcsTaskProps",
    "KinesisStream",
    "KinesisStreamProps",
    "LambdaFunction",
    "LambdaFunctionProps",
    "SfnStateMachine",
    "SfnStateMachineProps",
    "SnsTopic",
    "SnsTopicProps",
    "SqsQueue",
    "SqsQueueProps",
    "TaskEnvironmentVariable",
]

publication.publish()
