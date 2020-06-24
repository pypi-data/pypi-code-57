"""
# Event Targets for Amazon EventBridge

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This library contains integration classes to send Amazon EventBridge to any
number of supported AWS Services. Instances of these classes should be passed
to the `rule.addTarget()` method.

Currently supported are:

* Start a CodeBuild build
* Start a CodePipeline pipeline
* Run an ECS task
* Invoke a Lambda function
* Publish a message to an SNS topic
* Send a message to an SQS queue
* Start a StepFunctions state machine
* Queue a Batch job
* Make an AWS API call
* Put a record to a Kinesis stream

See the README of the `@aws-cdk/aws-events` library for more information on
EventBridge.
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

import aws_cdk.aws_batch
import aws_cdk.aws_codebuild
import aws_cdk.aws_codepipeline
import aws_cdk.aws_ec2
import aws_cdk.aws_ecs
import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.aws_kinesis
import aws_cdk.aws_lambda
import aws_cdk.aws_sns
import aws_cdk.aws_sqs
import aws_cdk.aws_stepfunctions


@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class AwsApi(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events-targets.AwsApi"):
    """Use an AWS Lambda function that makes API calls as an event rule target."""
    def __init__(self, *, policy_statement: typing.Optional[aws_cdk.aws_iam.PolicyStatement]=None, action: str, service: str, api_version: typing.Optional[str]=None, catch_error_pattern: typing.Optional[str]=None, parameters: typing.Any=None) -> None:
        """
        :param policy_statement: The IAM policy statement to allow the API call. Use only if resource restriction is needed. Default: - extract the permission from the API call
        :param action: The service action to call.
        :param service: The service to call.
        :param api_version: API version to use for the service. Default: - use latest available API version
        :param catch_error_pattern: The regex pattern to use to catch API errors. The ``code`` property of the ``Error`` object will be tested against this pattern. If there is a match an error will not be thrown. Default: - do not catch errors
        :param parameters: The parameters for the service action. Default: - no parameters
        """
        props = AwsApiProps(policy_statement=policy_statement, action=action, service=service, api_version=api_version, catch_error_pattern=catch_error_pattern, parameters=parameters)

        jsii.create(AwsApi, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, rule: aws_cdk.aws_events.IRule, id: typing.Optional[str]=None) -> aws_cdk.aws_events.RuleTargetConfig:
        """Returns a RuleTarget that can be used to trigger this AwsApi as a result from an EventBridge event.

        :param rule: -
        :param id: -
        """
        return jsii.invoke(self, "bind", [rule, id])


@jsii.data_type(jsii_type="@aws-cdk/aws-events-targets.AwsApiInput", jsii_struct_bases=[], name_mapping={'action': 'action', 'service': 'service', 'api_version': 'apiVersion', 'catch_error_pattern': 'catchErrorPattern', 'parameters': 'parameters'})
class AwsApiInput():
    def __init__(self, *, action: str, service: str, api_version: typing.Optional[str]=None, catch_error_pattern: typing.Optional[str]=None, parameters: typing.Any=None) -> None:
        """Rule target input for an AwsApi target.

        :param action: The service action to call.
        :param service: The service to call.
        :param api_version: API version to use for the service. Default: - use latest available API version
        :param catch_error_pattern: The regex pattern to use to catch API errors. The ``code`` property of the ``Error`` object will be tested against this pattern. If there is a match an error will not be thrown. Default: - do not catch errors
        :param parameters: The parameters for the service action. Default: - no parameters
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
        """
        return self._values.get('action')

    @builtins.property
    def service(self) -> str:
        """The service to call.

        see
        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        """
        return self._values.get('service')

    @builtins.property
    def api_version(self) -> typing.Optional[str]:
        """API version to use for the service.

        default
        :default: - use latest available API version

        see
        :see: https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/locking-api-versions.html
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
        """
        return self._values.get('catch_error_pattern')

    @builtins.property
    def parameters(self) -> typing.Any:
        """The parameters for the service action.

        default
        :default: - no parameters

        see
        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        """
        return self._values.get('parameters')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AwsApiInput(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-events-targets.AwsApiProps", jsii_struct_bases=[AwsApiInput], name_mapping={'action': 'action', 'service': 'service', 'api_version': 'apiVersion', 'catch_error_pattern': 'catchErrorPattern', 'parameters': 'parameters', 'policy_statement': 'policyStatement'})
class AwsApiProps(AwsApiInput):
    def __init__(self, *, action: str, service: str, api_version: typing.Optional[str]=None, catch_error_pattern: typing.Optional[str]=None, parameters: typing.Any=None, policy_statement: typing.Optional[aws_cdk.aws_iam.PolicyStatement]=None) -> None:
        """Properties for an AwsApi target.

        :param action: The service action to call.
        :param service: The service to call.
        :param api_version: API version to use for the service. Default: - use latest available API version
        :param catch_error_pattern: The regex pattern to use to catch API errors. The ``code`` property of the ``Error`` object will be tested against this pattern. If there is a match an error will not be thrown. Default: - do not catch errors
        :param parameters: The parameters for the service action. Default: - no parameters
        :param policy_statement: The IAM policy statement to allow the API call. Use only if resource restriction is needed. Default: - extract the permission from the API call
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
        """
        return self._values.get('action')

    @builtins.property
    def service(self) -> str:
        """The service to call.

        see
        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        """
        return self._values.get('service')

    @builtins.property
    def api_version(self) -> typing.Optional[str]:
        """API version to use for the service.

        default
        :default: - use latest available API version

        see
        :see: https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/locking-api-versions.html
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
        """
        return self._values.get('catch_error_pattern')

    @builtins.property
    def parameters(self) -> typing.Any:
        """The parameters for the service action.

        default
        :default: - no parameters

        see
        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        """
        return self._values.get('parameters')

    @builtins.property
    def policy_statement(self) -> typing.Optional[aws_cdk.aws_iam.PolicyStatement]:
        """The IAM policy statement to allow the API call.

        Use only if
        resource restriction is needed.

        default
        :default: - extract the permission from the API call
        """
        return self._values.get('policy_statement')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AwsApiProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class BatchJob(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events-targets.BatchJob"):
    """Use an AWS Batch Job / Queue as an event rule target.

    stability
    :stability: experimental
    """
    def __init__(self, job_queue: aws_cdk.aws_batch.IJobQueue, job_definition: aws_cdk.aws_batch.IJobDefinition, *, attempts: typing.Optional[jsii.Number]=None, event: typing.Optional[aws_cdk.aws_events.RuleTargetInput]=None, job_name: typing.Optional[str]=None, size: typing.Optional[jsii.Number]=None) -> None:
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
    def bind(self, rule: aws_cdk.aws_events.IRule, _id: typing.Optional[str]=None) -> aws_cdk.aws_events.RuleTargetConfig:
        """Returns a RuleTarget that can be used to trigger queue this batch job as a result from an EventBridge event.

        :param rule: -
        :param _id: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [rule, _id])


@jsii.data_type(jsii_type="@aws-cdk/aws-events-targets.BatchJobProps", jsii_struct_bases=[], name_mapping={'attempts': 'attempts', 'event': 'event', 'job_name': 'jobName', 'size': 'size'})
class BatchJobProps():
    def __init__(self, *, attempts: typing.Optional[jsii.Number]=None, event: typing.Optional[aws_cdk.aws_events.RuleTargetInput]=None, job_name: typing.Optional[str]=None, size: typing.Optional[jsii.Number]=None) -> None:
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
    def event(self) -> typing.Optional[aws_cdk.aws_events.RuleTargetInput]:
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


@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class CodeBuildProject(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events-targets.CodeBuildProject"):
    """Start a CodeBuild build when an Amazon EventBridge rule is triggered."""
    def __init__(self, project: aws_cdk.aws_codebuild.IProject, *, event: typing.Optional[aws_cdk.aws_events.RuleTargetInput]=None) -> None:
        """
        :param project: -
        :param event: The event to send to CodeBuild. This will be the payload for the StartBuild API. Default: - the entire EventBridge event
        """
        props = CodeBuildProjectProps(event=event)

        jsii.create(CodeBuildProject, self, [project, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _rule: aws_cdk.aws_events.IRule, _id: typing.Optional[str]=None) -> aws_cdk.aws_events.RuleTargetConfig:
        """Allows using build projects as event rule targets.

        :param _rule: -
        :param _id: -
        """
        return jsii.invoke(self, "bind", [_rule, _id])


@jsii.data_type(jsii_type="@aws-cdk/aws-events-targets.CodeBuildProjectProps", jsii_struct_bases=[], name_mapping={'event': 'event'})
class CodeBuildProjectProps():
    def __init__(self, *, event: typing.Optional[aws_cdk.aws_events.RuleTargetInput]=None) -> None:
        """Customize the CodeBuild Event Target.

        :param event: The event to send to CodeBuild. This will be the payload for the StartBuild API. Default: - the entire EventBridge event
        """
        self._values = {
        }
        if event is not None: self._values["event"] = event

    @builtins.property
    def event(self) -> typing.Optional[aws_cdk.aws_events.RuleTargetInput]:
        """The event to send to CodeBuild.

        This will be the payload for the StartBuild API.

        default
        :default: - the entire EventBridge event
        """
        return self._values.get('event')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CodeBuildProjectProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class CodePipeline(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events-targets.CodePipeline"):
    """Allows the pipeline to be used as an EventBridge rule target."""
    def __init__(self, pipeline: aws_cdk.aws_codepipeline.IPipeline, *, event_role: typing.Optional[aws_cdk.aws_iam.IRole]=None) -> None:
        """
        :param pipeline: -
        :param event_role: The role to assume before invoking the target (i.e., the pipeline) when the given rule is triggered. Default: - a new role will be created
        """
        options = CodePipelineTargetOptions(event_role=event_role)

        jsii.create(CodePipeline, self, [pipeline, options])

    @jsii.member(jsii_name="bind")
    def bind(self, _rule: aws_cdk.aws_events.IRule, _id: typing.Optional[str]=None) -> aws_cdk.aws_events.RuleTargetConfig:
        """Returns the rule target specification.

        NOTE: Do not use the various ``inputXxx`` options. They can be set in a call to ``addTarget``.

        :param _rule: -
        :param _id: -
        """
        return jsii.invoke(self, "bind", [_rule, _id])


@jsii.data_type(jsii_type="@aws-cdk/aws-events-targets.CodePipelineTargetOptions", jsii_struct_bases=[], name_mapping={'event_role': 'eventRole'})
class CodePipelineTargetOptions():
    def __init__(self, *, event_role: typing.Optional[aws_cdk.aws_iam.IRole]=None) -> None:
        """Customization options when creating a {@link CodePipeline} event target.

        :param event_role: The role to assume before invoking the target (i.e., the pipeline) when the given rule is triggered. Default: - a new role will be created
        """
        self._values = {
        }
        if event_role is not None: self._values["event_role"] = event_role

    @builtins.property
    def event_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The role to assume before invoking the target (i.e., the pipeline) when the given rule is triggered.

        default
        :default: - a new role will be created
        """
        return self._values.get('event_role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CodePipelineTargetOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-events-targets.ContainerOverride", jsii_struct_bases=[], name_mapping={'container_name': 'containerName', 'command': 'command', 'cpu': 'cpu', 'environment': 'environment', 'memory_limit': 'memoryLimit', 'memory_reservation': 'memoryReservation'})
class ContainerOverride():
    def __init__(self, *, container_name: str, command: typing.Optional[typing.List[str]]=None, cpu: typing.Optional[jsii.Number]=None, environment: typing.Optional[typing.List["TaskEnvironmentVariable"]]=None, memory_limit: typing.Optional[jsii.Number]=None, memory_reservation: typing.Optional[jsii.Number]=None) -> None:
        """
        :param container_name: Name of the container inside the task definition.
        :param command: Command to run inside the container. Default: Default command
        :param cpu: The number of cpu units reserved for the container. Default: The default value from the task definition.
        :param environment: Variables to set in the container's environment.
        :param memory_limit: Hard memory limit on the container. Default: The default value from the task definition.
        :param memory_reservation: Soft memory limit on the container. Default: The default value from the task definition.
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
        """Name of the container inside the task definition."""
        return self._values.get('container_name')

    @builtins.property
    def command(self) -> typing.Optional[typing.List[str]]:
        """Command to run inside the container.

        default
        :default: Default command
        """
        return self._values.get('command')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units reserved for the container.

        default
        :default: The default value from the task definition.
        """
        return self._values.get('cpu')

    @builtins.property
    def environment(self) -> typing.Optional[typing.List["TaskEnvironmentVariable"]]:
        """Variables to set in the container's environment."""
        return self._values.get('environment')

    @builtins.property
    def memory_limit(self) -> typing.Optional[jsii.Number]:
        """Hard memory limit on the container.

        default
        :default: The default value from the task definition.
        """
        return self._values.get('memory_limit')

    @builtins.property
    def memory_reservation(self) -> typing.Optional[jsii.Number]:
        """Soft memory limit on the container.

        default
        :default: The default value from the task definition.
        """
        return self._values.get('memory_reservation')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ContainerOverride(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class EcsTask(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events-targets.EcsTask"):
    """Start a task on an ECS cluster."""
    def __init__(self, *, cluster: aws_cdk.aws_ecs.ICluster, task_definition: aws_cdk.aws_ecs.TaskDefinition, container_overrides: typing.Optional[typing.List["ContainerOverride"]]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]=None, subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, task_count: typing.Optional[jsii.Number]=None) -> None:
        """
        :param cluster: Cluster where service will be deployed.
        :param task_definition: Task Definition of the task that should be started.
        :param container_overrides: Container setting overrides. Key is the name of the container to override, value is the values you want to override.
        :param security_group: Existing security group to use for the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: A new security group is created
        :param security_groups: Existing security groups to use for the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: A new security group is created
        :param subnet_selection: In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        :param task_count: How many tasks should be started when this event is triggered. Default: 1
        """
        props = EcsTaskProps(cluster=cluster, task_definition=task_definition, container_overrides=container_overrides, security_group=security_group, security_groups=security_groups, subnet_selection=subnet_selection, task_count=task_count)

        jsii.create(EcsTask, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _rule: aws_cdk.aws_events.IRule, _id: typing.Optional[str]=None) -> aws_cdk.aws_events.RuleTargetConfig:
        """Allows using tasks as target of EventBridge events.

        :param _rule: -
        :param _id: -
        """
        return jsii.invoke(self, "bind", [_rule, _id])

    @builtins.property
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
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
    def security_groups(self) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        """The security groups associated with the task.

        Only applicable with awsvpc network mode.

        default
        :default: - A new security group is created.
        """
        return jsii.get(self, "securityGroups")


@jsii.data_type(jsii_type="@aws-cdk/aws-events-targets.EcsTaskProps", jsii_struct_bases=[], name_mapping={'cluster': 'cluster', 'task_definition': 'taskDefinition', 'container_overrides': 'containerOverrides', 'security_group': 'securityGroup', 'security_groups': 'securityGroups', 'subnet_selection': 'subnetSelection', 'task_count': 'taskCount'})
class EcsTaskProps():
    def __init__(self, *, cluster: aws_cdk.aws_ecs.ICluster, task_definition: aws_cdk.aws_ecs.TaskDefinition, container_overrides: typing.Optional[typing.List["ContainerOverride"]]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]=None, subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, task_count: typing.Optional[jsii.Number]=None) -> None:
        """Properties to define an ECS Event Task.

        :param cluster: Cluster where service will be deployed.
        :param task_definition: Task Definition of the task that should be started.
        :param container_overrides: Container setting overrides. Key is the name of the container to override, value is the values you want to override.
        :param security_group: Existing security group to use for the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: A new security group is created
        :param security_groups: Existing security groups to use for the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: A new security group is created
        :param subnet_selection: In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        :param task_count: How many tasks should be started when this event is triggered. Default: 1
        """
        if isinstance(subnet_selection, dict): subnet_selection = aws_cdk.aws_ec2.SubnetSelection(**subnet_selection)
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
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """Cluster where service will be deployed."""
        return self._values.get('cluster')

    @builtins.property
    def task_definition(self) -> aws_cdk.aws_ecs.TaskDefinition:
        """Task Definition of the task that should be started."""
        return self._values.get('task_definition')

    @builtins.property
    def container_overrides(self) -> typing.Optional[typing.List["ContainerOverride"]]:
        """Container setting overrides.

        Key is the name of the container to override, value is the
        values you want to override.
        """
        return self._values.get('container_overrides')

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
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
    def security_groups(self) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        """Existing security groups to use for the task's ENIs.

        (Only applicable in case the TaskDefinition is configured for AwsVpc networking)

        default
        :default: A new security group is created
        """
        return self._values.get('security_groups')

    @builtins.property
    def subnet_selection(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """In what subnets to place the task's ENIs.

        (Only applicable in case the TaskDefinition is configured for AwsVpc networking)

        default
        :default: Private subnets
        """
        return self._values.get('subnet_selection')

    @builtins.property
    def task_count(self) -> typing.Optional[jsii.Number]:
        """How many tasks should be started when this event is triggered.

        default
        :default: 1
        """
        return self._values.get('task_count')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EcsTaskProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class KinesisStream(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events-targets.KinesisStream"):
    """Use a Kinesis Stream as a target for AWS CloudWatch event rules.

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        # put to a Kinesis stream every time code is committed
        # to a CodeCommit repository
        repository.on_commit(targets.KinesisStream(stream))
    """
    def __init__(self, stream: aws_cdk.aws_kinesis.IStream, *, message: typing.Optional[aws_cdk.aws_events.RuleTargetInput]=None, partition_key_path: typing.Optional[str]=None) -> None:
        """
        :param stream: -
        :param message: The message to send to the stream. Must be a valid JSON text passed to the target stream. Default: - the entire CloudWatch event
        :param partition_key_path: Partition Key Path for records sent to this stream. Default: - eventId as the partition key
        """
        props = KinesisStreamProps(message=message, partition_key_path=partition_key_path)

        jsii.create(KinesisStream, self, [stream, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _rule: aws_cdk.aws_events.IRule, _id: typing.Optional[str]=None) -> aws_cdk.aws_events.RuleTargetConfig:
        """Returns a RuleTarget that can be used to trigger this Kinesis Stream as a result from a CloudWatch event.

        :param _rule: -
        :param _id: -
        """
        return jsii.invoke(self, "bind", [_rule, _id])


@jsii.data_type(jsii_type="@aws-cdk/aws-events-targets.KinesisStreamProps", jsii_struct_bases=[], name_mapping={'message': 'message', 'partition_key_path': 'partitionKeyPath'})
class KinesisStreamProps():
    def __init__(self, *, message: typing.Optional[aws_cdk.aws_events.RuleTargetInput]=None, partition_key_path: typing.Optional[str]=None) -> None:
        """Customize the Kinesis Stream Event Target.

        :param message: The message to send to the stream. Must be a valid JSON text passed to the target stream. Default: - the entire CloudWatch event
        :param partition_key_path: Partition Key Path for records sent to this stream. Default: - eventId as the partition key
        """
        self._values = {
        }
        if message is not None: self._values["message"] = message
        if partition_key_path is not None: self._values["partition_key_path"] = partition_key_path

    @builtins.property
    def message(self) -> typing.Optional[aws_cdk.aws_events.RuleTargetInput]:
        """The message to send to the stream.

        Must be a valid JSON text passed to the target stream.

        default
        :default: - the entire CloudWatch event
        """
        return self._values.get('message')

    @builtins.property
    def partition_key_path(self) -> typing.Optional[str]:
        """Partition Key Path for records sent to this stream.

        default
        :default: - eventId as the partition key
        """
        return self._values.get('partition_key_path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'KinesisStreamProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class LambdaFunction(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events-targets.LambdaFunction"):
    """Use an AWS Lambda function as an event rule target."""
    def __init__(self, handler: aws_cdk.aws_lambda.IFunction, *, event: typing.Optional[aws_cdk.aws_events.RuleTargetInput]=None) -> None:
        """
        :param handler: -
        :param event: The event to send to the Lambda. This will be the payload sent to the Lambda Function. Default: the entire EventBridge event
        """
        props = LambdaFunctionProps(event=event)

        jsii.create(LambdaFunction, self, [handler, props])

    @jsii.member(jsii_name="bind")
    def bind(self, rule: aws_cdk.aws_events.IRule, _id: typing.Optional[str]=None) -> aws_cdk.aws_events.RuleTargetConfig:
        """Returns a RuleTarget that can be used to trigger this Lambda as a result from an EventBridge event.

        :param rule: -
        :param _id: -
        """
        return jsii.invoke(self, "bind", [rule, _id])


@jsii.data_type(jsii_type="@aws-cdk/aws-events-targets.LambdaFunctionProps", jsii_struct_bases=[], name_mapping={'event': 'event'})
class LambdaFunctionProps():
    def __init__(self, *, event: typing.Optional[aws_cdk.aws_events.RuleTargetInput]=None) -> None:
        """Customize the Lambda Event Target.

        :param event: The event to send to the Lambda. This will be the payload sent to the Lambda Function. Default: the entire EventBridge event
        """
        self._values = {
        }
        if event is not None: self._values["event"] = event

    @builtins.property
    def event(self) -> typing.Optional[aws_cdk.aws_events.RuleTargetInput]:
        """The event to send to the Lambda.

        This will be the payload sent to the Lambda Function.

        default
        :default: the entire EventBridge event
        """
        return self._values.get('event')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LambdaFunctionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class SfnStateMachine(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events-targets.SfnStateMachine"):
    """Use a StepFunctions state machine as a target for Amazon EventBridge rules."""
    def __init__(self, machine: aws_cdk.aws_stepfunctions.IStateMachine, *, input: typing.Optional[aws_cdk.aws_events.RuleTargetInput]=None) -> None:
        """
        :param machine: -
        :param input: The input to the state machine execution. Default: the entire EventBridge event
        """
        props = SfnStateMachineProps(input=input)

        jsii.create(SfnStateMachine, self, [machine, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _rule: aws_cdk.aws_events.IRule, _id: typing.Optional[str]=None) -> aws_cdk.aws_events.RuleTargetConfig:
        """Returns a properties that are used in an Rule to trigger this State Machine.

        :param _rule: -
        :param _id: -

        see
        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/resource-based-policies-eventbridge.html#sns-permissions
        """
        return jsii.invoke(self, "bind", [_rule, _id])

    @builtins.property
    @jsii.member(jsii_name="machine")
    def machine(self) -> aws_cdk.aws_stepfunctions.IStateMachine:
        return jsii.get(self, "machine")


@jsii.data_type(jsii_type="@aws-cdk/aws-events-targets.SfnStateMachineProps", jsii_struct_bases=[], name_mapping={'input': 'input'})
class SfnStateMachineProps():
    def __init__(self, *, input: typing.Optional[aws_cdk.aws_events.RuleTargetInput]=None) -> None:
        """Customize the Step Functions State Machine target.

        :param input: The input to the state machine execution. Default: the entire EventBridge event
        """
        self._values = {
        }
        if input is not None: self._values["input"] = input

    @builtins.property
    def input(self) -> typing.Optional[aws_cdk.aws_events.RuleTargetInput]:
        """The input to the state machine execution.

        default
        :default: the entire EventBridge event
        """
        return self._values.get('input')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SfnStateMachineProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class SnsTopic(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events-targets.SnsTopic"):
    """Use an SNS topic as a target for Amazon EventBridge rules.

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        # publish to an SNS topic every time code is committed
        # to a CodeCommit repository
        repository.on_commit(targets.SnsTopic(topic))
    """
    def __init__(self, topic: aws_cdk.aws_sns.ITopic, *, message: typing.Optional[aws_cdk.aws_events.RuleTargetInput]=None) -> None:
        """
        :param topic: -
        :param message: The message to send to the topic. Default: the entire EventBridge event
        """
        props = SnsTopicProps(message=message)

        jsii.create(SnsTopic, self, [topic, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _rule: aws_cdk.aws_events.IRule, _id: typing.Optional[str]=None) -> aws_cdk.aws_events.RuleTargetConfig:
        """Returns a RuleTarget that can be used to trigger this SNS topic as a result from an EventBridge event.

        :param _rule: -
        :param _id: -

        see
        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/resource-based-policies-eventbridge.html#sns-permissions
        """
        return jsii.invoke(self, "bind", [_rule, _id])

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> aws_cdk.aws_sns.ITopic:
        return jsii.get(self, "topic")


@jsii.data_type(jsii_type="@aws-cdk/aws-events-targets.SnsTopicProps", jsii_struct_bases=[], name_mapping={'message': 'message'})
class SnsTopicProps():
    def __init__(self, *, message: typing.Optional[aws_cdk.aws_events.RuleTargetInput]=None) -> None:
        """Customize the SNS Topic Event Target.

        :param message: The message to send to the topic. Default: the entire EventBridge event
        """
        self._values = {
        }
        if message is not None: self._values["message"] = message

    @builtins.property
    def message(self) -> typing.Optional[aws_cdk.aws_events.RuleTargetInput]:
        """The message to send to the topic.

        default
        :default: the entire EventBridge event
        """
        return self._values.get('message')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SnsTopicProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class SqsQueue(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events-targets.SqsQueue"):
    """Use an SQS Queue as a target for Amazon EventBridge rules.

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        # publish to an SQS queue every time code is committed
        # to a CodeCommit repository
        repository.on_commit(targets.SqsQueue(queue))
    """
    def __init__(self, queue: aws_cdk.aws_sqs.IQueue, *, message: typing.Optional[aws_cdk.aws_events.RuleTargetInput]=None, message_group_id: typing.Optional[str]=None) -> None:
        """
        :param queue: -
        :param message: The message to send to the queue. Must be a valid JSON text passed to the target queue. Default: the entire EventBridge event
        :param message_group_id: Message Group ID for messages sent to this queue. Required for FIFO queues, leave empty for regular queues. Default: - no message group ID (regular queue)
        """
        props = SqsQueueProps(message=message, message_group_id=message_group_id)

        jsii.create(SqsQueue, self, [queue, props])

    @jsii.member(jsii_name="bind")
    def bind(self, rule: aws_cdk.aws_events.IRule, _id: typing.Optional[str]=None) -> aws_cdk.aws_events.RuleTargetConfig:
        """Returns a RuleTarget that can be used to trigger this SQS queue as a result from an EventBridge event.

        :param rule: -
        :param _id: -

        see
        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/resource-based-policies-eventbridge.html#sqs-permissions
        """
        return jsii.invoke(self, "bind", [rule, _id])

    @builtins.property
    @jsii.member(jsii_name="queue")
    def queue(self) -> aws_cdk.aws_sqs.IQueue:
        return jsii.get(self, "queue")


@jsii.data_type(jsii_type="@aws-cdk/aws-events-targets.SqsQueueProps", jsii_struct_bases=[], name_mapping={'message': 'message', 'message_group_id': 'messageGroupId'})
class SqsQueueProps():
    def __init__(self, *, message: typing.Optional[aws_cdk.aws_events.RuleTargetInput]=None, message_group_id: typing.Optional[str]=None) -> None:
        """Customize the SQS Queue Event Target.

        :param message: The message to send to the queue. Must be a valid JSON text passed to the target queue. Default: the entire EventBridge event
        :param message_group_id: Message Group ID for messages sent to this queue. Required for FIFO queues, leave empty for regular queues. Default: - no message group ID (regular queue)
        """
        self._values = {
        }
        if message is not None: self._values["message"] = message
        if message_group_id is not None: self._values["message_group_id"] = message_group_id

    @builtins.property
    def message(self) -> typing.Optional[aws_cdk.aws_events.RuleTargetInput]:
        """The message to send to the queue.

        Must be a valid JSON text passed to the target queue.

        default
        :default: the entire EventBridge event
        """
        return self._values.get('message')

    @builtins.property
    def message_group_id(self) -> typing.Optional[str]:
        """Message Group ID for messages sent to this queue.

        Required for FIFO queues, leave empty for regular queues.

        default
        :default: - no message group ID (regular queue)
        """
        return self._values.get('message_group_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SqsQueueProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-events-targets.TaskEnvironmentVariable", jsii_struct_bases=[], name_mapping={'name': 'name', 'value': 'value'})
class TaskEnvironmentVariable():
    def __init__(self, *, name: str, value: str) -> None:
        """An environment variable to be set in the container run as a task.

        :param name: Name for the environment variable. Exactly one of ``name`` and ``namePath`` must be specified.
        :param value: Value of the environment variable. Exactly one of ``value`` and ``valuePath`` must be specified.
        """
        self._values = {
            'name': name,
            'value': value,
        }

    @builtins.property
    def name(self) -> str:
        """Name for the environment variable.

        Exactly one of ``name`` and ``namePath`` must be specified.
        """
        return self._values.get('name')

    @builtins.property
    def value(self) -> str:
        """Value of the environment variable.

        Exactly one of ``value`` and ``valuePath`` must be specified.
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
