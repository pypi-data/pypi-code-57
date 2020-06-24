"""
## Amazon Lambda Node.js Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development. They are subject to non-backward compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This library provides constructs for Node.js Lambda functions.

To use this module, you will need to have Docker installed.

### Node.js Function

Define a `NodejsFunction`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lambda.NodejsFunction(self, "my-handler")
```

By default, the construct will use the name of the defining file and the construct's id to look
up the entry file:

```
.
├── stack.ts # defines a 'NodejsFunction' with 'my-handler' as id
├── stack.my-handler.ts # exports a function named 'handler'
```

This file is used as "entry" for [Parcel](https://parceljs.org/). This means that your code is
automatically transpiled and bundled whether it's written in JavaScript or TypeScript.

Alternatively, an entry file and handler can be specified:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lambda.NodejsFunction(self, "MyFunction",
    entry="/path/to/my/file.ts",
    handler="myExportedFunc"
)
```

All other properties of `lambda.Function` are supported, see also the [AWS Lambda construct library](https://github.com/aws/aws-cdk/tree/master/packages/%40aws-cdk/aws-lambda).

Use the `containerEnvironment` prop to pass environments variables to the Docker container
running Parcel:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lambda.NodejsFunction(self, "my-handler",
    container_environment={
        "NODE_ENV": "production"
    }
)
```

### Configuring Parcel

The `NodejsFunction` construct exposes some [Parcel](https://parceljs.org/) options via properties: `minify`, `sourceMaps`,
`buildDir` and `cacheDir`.

Parcel transpiles your code (every internal module) with [@babel/preset-env](https://babeljs.io/docs/en/babel-preset-env) and uses the
runtime version of your Lambda function as target.

Configuring Babel with Parcel is possible via a `.babelrc` or a `babel` config in `package.json`.
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

import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_logs
import aws_cdk.aws_sqs
import aws_cdk.core


class NodejsFunction(aws_cdk.aws_lambda.Function, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda-nodejs.NodejsFunction"):
    """A Node.js Lambda function bundled using Parcel.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, build_dir: typing.Optional[str]=None, cache_dir: typing.Optional[str]=None, container_environment: typing.Optional[typing.Mapping[str, str]]=None, entry: typing.Optional[str]=None, handler: typing.Optional[str]=None, minify: typing.Optional[bool]=None, node_docker_tag: typing.Optional[str]=None, project_root: typing.Optional[str]=None, runtime: typing.Optional[aws_cdk.aws_lambda.Runtime]=None, source_maps: typing.Optional[bool]=None, allow_all_outbound: typing.Optional[bool]=None, current_version_options: typing.Optional[aws_cdk.aws_lambda.VersionOptions]=None, dead_letter_queue: typing.Optional[aws_cdk.aws_sqs.IQueue]=None, dead_letter_queue_enabled: typing.Optional[bool]=None, description: typing.Optional[str]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, events: typing.Optional[typing.List[aws_cdk.aws_lambda.IEventSource]]=None, function_name: typing.Optional[str]=None, initial_policy: typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]=None, layers: typing.Optional[typing.List[aws_cdk.aws_lambda.ILayerVersion]]=None, log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays]=None, log_retention_retry_options: typing.Optional[aws_cdk.aws_lambda.LogRetentionRetryOptions]=None, log_retention_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, memory_size: typing.Optional[jsii.Number]=None, reserved_concurrent_executions: typing.Optional[jsii.Number]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None, tracing: typing.Optional[aws_cdk.aws_lambda.Tracing]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, max_event_age: typing.Optional[aws_cdk.core.Duration]=None, on_failure: typing.Optional[aws_cdk.aws_lambda.IDestination]=None, on_success: typing.Optional[aws_cdk.aws_lambda.IDestination]=None, retry_attempts: typing.Optional[jsii.Number]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param build_dir: The build directory. Default: - ``.build`` in the entry file directory
        :param cache_dir: The cache directory. Parcel uses a filesystem cache for fast rebuilds. Default: - ``.cache`` in the root directory
        :param container_environment: The environment variables to pass to the container running Parcel. Default: - no environment variables are passed to the container
        :param entry: Path to the entry file (JavaScript or TypeScript). Default: - Derived from the name of the defining file and the construct's id. If the ``NodejsFunction`` is defined in ``stack.ts`` with ``my-handler`` as id (``new NodejsFunction(this, 'my-handler')``), the construct will look at ``stack.my-handler.ts`` and ``stack.my-handler.js``.
        :param handler: The name of the exported handler in the entry file. Default: handler
        :param minify: Whether to minify files when bundling. Default: false
        :param node_docker_tag: The docker tag of the node base image to use in the parcel-bundler docker image. Default: - the ``process.versions.node`` alpine image
        :param project_root: The root of the project. This will be used as the source for the volume mounted in the Docker container. If you specify this prop, ensure that this path includes ``entry`` and any module/dependencies used by your function otherwise bundling will not be possible. Default: - the closest path containing a .git folder
        :param runtime: The runtime environment. Only runtimes of the Node.js family are supported. Default: - ``NODEJS_12_X`` if ``process.versions.node`` >= '12.0.0', ``NODEJS_10_X`` otherwise.
        :param source_maps: Whether to include source maps when bundling. Default: false
        :param allow_all_outbound: Whether to allow the Lambda to send all network traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Default: true
        :param current_version_options: Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: The SQS queue to use if DLQ is enabled. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param description: A description of the function. Default: - No description.
        :param environment: Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param events: Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param function_name: A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param layers: A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by mulitple functions. Default: - No layers.
        :param log_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param memory_size: The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param reserved_concurrent_executions: The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param security_group: What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead. Only used if 'vpc' is supplied. Use securityGroups property instead. Function constructor will throw an error if both are specified. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroups prop, a dedicated security group will be created for this function.
        :param security_groups: The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param timeout: The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. Default: - Function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Note: internet access for Lambdas requires a NAT gateway, so picking Public subnets is not allowed. Default: - the Vpc default strategy if not specified
        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        stability
        :stability: experimental
        """
        props = NodejsFunctionProps(build_dir=build_dir, cache_dir=cache_dir, container_environment=container_environment, entry=entry, handler=handler, minify=minify, node_docker_tag=node_docker_tag, project_root=project_root, runtime=runtime, source_maps=source_maps, allow_all_outbound=allow_all_outbound, current_version_options=current_version_options, dead_letter_queue=dead_letter_queue, dead_letter_queue_enabled=dead_letter_queue_enabled, description=description, environment=environment, events=events, function_name=function_name, initial_policy=initial_policy, layers=layers, log_retention=log_retention, log_retention_retry_options=log_retention_retry_options, log_retention_role=log_retention_role, memory_size=memory_size, reserved_concurrent_executions=reserved_concurrent_executions, role=role, security_group=security_group, security_groups=security_groups, timeout=timeout, tracing=tracing, vpc=vpc, vpc_subnets=vpc_subnets, max_event_age=max_event_age, on_failure=on_failure, on_success=on_success, retry_attempts=retry_attempts)

        jsii.create(NodejsFunction, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-lambda-nodejs.NodejsFunctionProps", jsii_struct_bases=[aws_cdk.aws_lambda.FunctionOptions], name_mapping={'max_event_age': 'maxEventAge', 'on_failure': 'onFailure', 'on_success': 'onSuccess', 'retry_attempts': 'retryAttempts', 'allow_all_outbound': 'allowAllOutbound', 'current_version_options': 'currentVersionOptions', 'dead_letter_queue': 'deadLetterQueue', 'dead_letter_queue_enabled': 'deadLetterQueueEnabled', 'description': 'description', 'environment': 'environment', 'events': 'events', 'function_name': 'functionName', 'initial_policy': 'initialPolicy', 'layers': 'layers', 'log_retention': 'logRetention', 'log_retention_retry_options': 'logRetentionRetryOptions', 'log_retention_role': 'logRetentionRole', 'memory_size': 'memorySize', 'reserved_concurrent_executions': 'reservedConcurrentExecutions', 'role': 'role', 'security_group': 'securityGroup', 'security_groups': 'securityGroups', 'timeout': 'timeout', 'tracing': 'tracing', 'vpc': 'vpc', 'vpc_subnets': 'vpcSubnets', 'build_dir': 'buildDir', 'cache_dir': 'cacheDir', 'container_environment': 'containerEnvironment', 'entry': 'entry', 'handler': 'handler', 'minify': 'minify', 'node_docker_tag': 'nodeDockerTag', 'project_root': 'projectRoot', 'runtime': 'runtime', 'source_maps': 'sourceMaps'})
class NodejsFunctionProps(aws_cdk.aws_lambda.FunctionOptions):
    def __init__(self, *, max_event_age: typing.Optional[aws_cdk.core.Duration]=None, on_failure: typing.Optional[aws_cdk.aws_lambda.IDestination]=None, on_success: typing.Optional[aws_cdk.aws_lambda.IDestination]=None, retry_attempts: typing.Optional[jsii.Number]=None, allow_all_outbound: typing.Optional[bool]=None, current_version_options: typing.Optional[aws_cdk.aws_lambda.VersionOptions]=None, dead_letter_queue: typing.Optional[aws_cdk.aws_sqs.IQueue]=None, dead_letter_queue_enabled: typing.Optional[bool]=None, description: typing.Optional[str]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, events: typing.Optional[typing.List[aws_cdk.aws_lambda.IEventSource]]=None, function_name: typing.Optional[str]=None, initial_policy: typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]=None, layers: typing.Optional[typing.List[aws_cdk.aws_lambda.ILayerVersion]]=None, log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays]=None, log_retention_retry_options: typing.Optional[aws_cdk.aws_lambda.LogRetentionRetryOptions]=None, log_retention_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, memory_size: typing.Optional[jsii.Number]=None, reserved_concurrent_executions: typing.Optional[jsii.Number]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None, tracing: typing.Optional[aws_cdk.aws_lambda.Tracing]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, build_dir: typing.Optional[str]=None, cache_dir: typing.Optional[str]=None, container_environment: typing.Optional[typing.Mapping[str, str]]=None, entry: typing.Optional[str]=None, handler: typing.Optional[str]=None, minify: typing.Optional[bool]=None, node_docker_tag: typing.Optional[str]=None, project_root: typing.Optional[str]=None, runtime: typing.Optional[aws_cdk.aws_lambda.Runtime]=None, source_maps: typing.Optional[bool]=None) -> None:
        """Properties for a NodejsFunction.

        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2
        :param allow_all_outbound: Whether to allow the Lambda to send all network traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Default: true
        :param current_version_options: Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: The SQS queue to use if DLQ is enabled. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param description: A description of the function. Default: - No description.
        :param environment: Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param events: Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param function_name: A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param layers: A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by mulitple functions. Default: - No layers.
        :param log_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param memory_size: The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param reserved_concurrent_executions: The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param security_group: What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead. Only used if 'vpc' is supplied. Use securityGroups property instead. Function constructor will throw an error if both are specified. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroups prop, a dedicated security group will be created for this function.
        :param security_groups: The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param timeout: The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. Default: - Function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Note: internet access for Lambdas requires a NAT gateway, so picking Public subnets is not allowed. Default: - the Vpc default strategy if not specified
        :param build_dir: The build directory. Default: - ``.build`` in the entry file directory
        :param cache_dir: The cache directory. Parcel uses a filesystem cache for fast rebuilds. Default: - ``.cache`` in the root directory
        :param container_environment: The environment variables to pass to the container running Parcel. Default: - no environment variables are passed to the container
        :param entry: Path to the entry file (JavaScript or TypeScript). Default: - Derived from the name of the defining file and the construct's id. If the ``NodejsFunction`` is defined in ``stack.ts`` with ``my-handler`` as id (``new NodejsFunction(this, 'my-handler')``), the construct will look at ``stack.my-handler.ts`` and ``stack.my-handler.js``.
        :param handler: The name of the exported handler in the entry file. Default: handler
        :param minify: Whether to minify files when bundling. Default: false
        :param node_docker_tag: The docker tag of the node base image to use in the parcel-bundler docker image. Default: - the ``process.versions.node`` alpine image
        :param project_root: The root of the project. This will be used as the source for the volume mounted in the Docker container. If you specify this prop, ensure that this path includes ``entry`` and any module/dependencies used by your function otherwise bundling will not be possible. Default: - the closest path containing a .git folder
        :param runtime: The runtime environment. Only runtimes of the Node.js family are supported. Default: - ``NODEJS_12_X`` if ``process.versions.node`` >= '12.0.0', ``NODEJS_10_X`` otherwise.
        :param source_maps: Whether to include source maps when bundling. Default: false

        stability
        :stability: experimental
        """
        if isinstance(current_version_options, dict): current_version_options = aws_cdk.aws_lambda.VersionOptions(**current_version_options)
        if isinstance(log_retention_retry_options, dict): log_retention_retry_options = aws_cdk.aws_lambda.LogRetentionRetryOptions(**log_retention_retry_options)
        if isinstance(vpc_subnets, dict): vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values = {
        }
        if max_event_age is not None: self._values["max_event_age"] = max_event_age
        if on_failure is not None: self._values["on_failure"] = on_failure
        if on_success is not None: self._values["on_success"] = on_success
        if retry_attempts is not None: self._values["retry_attempts"] = retry_attempts
        if allow_all_outbound is not None: self._values["allow_all_outbound"] = allow_all_outbound
        if current_version_options is not None: self._values["current_version_options"] = current_version_options
        if dead_letter_queue is not None: self._values["dead_letter_queue"] = dead_letter_queue
        if dead_letter_queue_enabled is not None: self._values["dead_letter_queue_enabled"] = dead_letter_queue_enabled
        if description is not None: self._values["description"] = description
        if environment is not None: self._values["environment"] = environment
        if events is not None: self._values["events"] = events
        if function_name is not None: self._values["function_name"] = function_name
        if initial_policy is not None: self._values["initial_policy"] = initial_policy
        if layers is not None: self._values["layers"] = layers
        if log_retention is not None: self._values["log_retention"] = log_retention
        if log_retention_retry_options is not None: self._values["log_retention_retry_options"] = log_retention_retry_options
        if log_retention_role is not None: self._values["log_retention_role"] = log_retention_role
        if memory_size is not None: self._values["memory_size"] = memory_size
        if reserved_concurrent_executions is not None: self._values["reserved_concurrent_executions"] = reserved_concurrent_executions
        if role is not None: self._values["role"] = role
        if security_group is not None: self._values["security_group"] = security_group
        if security_groups is not None: self._values["security_groups"] = security_groups
        if timeout is not None: self._values["timeout"] = timeout
        if tracing is not None: self._values["tracing"] = tracing
        if vpc is not None: self._values["vpc"] = vpc
        if vpc_subnets is not None: self._values["vpc_subnets"] = vpc_subnets
        if build_dir is not None: self._values["build_dir"] = build_dir
        if cache_dir is not None: self._values["cache_dir"] = cache_dir
        if container_environment is not None: self._values["container_environment"] = container_environment
        if entry is not None: self._values["entry"] = entry
        if handler is not None: self._values["handler"] = handler
        if minify is not None: self._values["minify"] = minify
        if node_docker_tag is not None: self._values["node_docker_tag"] = node_docker_tag
        if project_root is not None: self._values["project_root"] = project_root
        if runtime is not None: self._values["runtime"] = runtime
        if source_maps is not None: self._values["source_maps"] = source_maps

    @builtins.property
    def max_event_age(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The maximum age of a request that Lambda sends to a function for processing.

        Minimum: 60 seconds
        Maximum: 6 hours

        default
        :default: Duration.hours(6)
        """
        return self._values.get('max_event_age')

    @builtins.property
    def on_failure(self) -> typing.Optional[aws_cdk.aws_lambda.IDestination]:
        """The destination for failed invocations.

        default
        :default: - no destination
        """
        return self._values.get('on_failure')

    @builtins.property
    def on_success(self) -> typing.Optional[aws_cdk.aws_lambda.IDestination]:
        """The destination for successful invocations.

        default
        :default: - no destination
        """
        return self._values.get('on_success')

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        """The maximum number of times to retry when the function returns an error.

        Minimum: 0
        Maximum: 2

        default
        :default: 2
        """
        return self._values.get('retry_attempts')

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[bool]:
        """Whether to allow the Lambda to send all network traffic.

        If set to false, you must individually add traffic rules to allow the
        Lambda to connect to network targets.

        default
        :default: true
        """
        return self._values.get('allow_all_outbound')

    @builtins.property
    def current_version_options(self) -> typing.Optional[aws_cdk.aws_lambda.VersionOptions]:
        """Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method.

        default
        :default: - default options as described in ``VersionOptions``
        """
        return self._values.get('current_version_options')

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[aws_cdk.aws_sqs.IQueue]:
        """The SQS queue to use if DLQ is enabled.

        default
        :default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        """
        return self._values.get('dead_letter_queue')

    @builtins.property
    def dead_letter_queue_enabled(self) -> typing.Optional[bool]:
        """Enabled DLQ.

        If ``deadLetterQueue`` is undefined,
        an SQS queue with default options will be defined for your Function.

        default
        :default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        """
        return self._values.get('dead_letter_queue_enabled')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the function.

        default
        :default: - No description.
        """
        return self._values.get('description')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Key-value pairs that Lambda caches and makes available for your Lambda functions.

        Use environment variables to apply configuration changes, such
        as test and production environment configurations, without changing your
        Lambda function source code.

        default
        :default: - No environment variables.
        """
        return self._values.get('environment')

    @builtins.property
    def events(self) -> typing.Optional[typing.List[aws_cdk.aws_lambda.IEventSource]]:
        """Event sources for this function.

        You can also add event sources using ``addEventSource``.

        default
        :default: - No event sources.
        """
        return self._values.get('events')

    @builtins.property
    def function_name(self) -> typing.Optional[str]:
        """A name for the function.

        default
        :default:

        - AWS CloudFormation generates a unique physical ID and uses that
          ID for the function's name. For more information, see Name Type.
        """
        return self._values.get('function_name')

    @builtins.property
    def initial_policy(self) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """Initial policy statements to add to the created Lambda Role.

        You can call ``addToRolePolicy`` to the created lambda to add statements post creation.

        default
        :default: - No policy statements are added to the created Lambda role.
        """
        return self._values.get('initial_policy')

    @builtins.property
    def layers(self) -> typing.Optional[typing.List[aws_cdk.aws_lambda.ILayerVersion]]:
        """A list of layers to add to the function's execution environment.

        You can configure your Lambda function to pull in
        additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies
        that can be used by mulitple functions.

        default
        :default: - No layers.
        """
        return self._values.get('layers')

    @builtins.property
    def log_retention(self) -> typing.Optional[aws_cdk.aws_logs.RetentionDays]:
        """The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        default
        :default: logs.RetentionDays.INFINITE
        """
        return self._values.get('log_retention')

    @builtins.property
    def log_retention_retry_options(self) -> typing.Optional[aws_cdk.aws_lambda.LogRetentionRetryOptions]:
        """When log retention is specified, a custom resource attempts to create the CloudWatch log group.

        These options control the retry policy when interacting with CloudWatch APIs.

        default
        :default: - Default AWS SDK retry options.
        """
        return self._values.get('log_retention_retry_options')

    @builtins.property
    def log_retention_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The IAM role for the Lambda function associated with the custom resource that sets the retention policy.

        default
        :default: - A new role is created.
        """
        return self._values.get('log_retention_role')

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        """The amount of memory, in MB, that is allocated to your Lambda function.

        Lambda uses this value to proportionally allocate the amount of CPU
        power. For more information, see Resource Model in the AWS Lambda
        Developer Guide.

        default
        :default: 128
        """
        return self._values.get('memory_size')

    @builtins.property
    def reserved_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        """The maximum of concurrent executions you want to reserve for the function.

        default
        :default: - No specific limit - account limit.

        see
        :see: https://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html
        """
        return self._values.get('reserved_concurrent_executions')

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Lambda execution role.

        This is the role that will be assumed by the function upon execution.
        It controls the permissions that the function will have. The Role must
        be assumable by the 'lambda.amazonaws.com' service principal.

        The default Role automatically has permissions granted for Lambda execution. If you
        provide a Role, you must add the relevant AWS managed policies yourself.

        The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and
        "service-role/AWSLambdaVPCAccessExecutionRole".

        default
        :default:

        - A unique role will be generated for this lambda function.
          Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        """
        return self._values.get('role')

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead.

        Only used if 'vpc' is supplied.

        Use securityGroups property instead.
        Function constructor will throw an error if both are specified.

        default
        :default:

        - If the function is placed within a VPC and a security group is
          not specified, either by this or securityGroups prop, a dedicated security
          group will be created for this function.

        deprecated
        :deprecated: - This property is deprecated, use securityGroups instead

        stability
        :stability: deprecated
        """
        return self._values.get('security_group')

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        """The list of security groups to associate with the Lambda's network interfaces.

        Only used if 'vpc' is supplied.

        default
        :default:

        - If the function is placed within a VPC and a security group is
          not specified, either by this or securityGroup prop, a dedicated security
          group will be created for this function.
        """
        return self._values.get('security_groups')

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The function execution time (in seconds) after which Lambda terminates the function.

        Because the execution time affects cost, set this value
        based on the function's expected execution time.

        default
        :default: Duration.seconds(3)
        """
        return self._values.get('timeout')

    @builtins.property
    def tracing(self) -> typing.Optional[aws_cdk.aws_lambda.Tracing]:
        """Enable AWS X-Ray Tracing for Lambda Function.

        default
        :default: Tracing.Disabled
        """
        return self._values.get('tracing')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """VPC network to place Lambda network interfaces.

        Specify this if the Lambda function needs to access resources in a VPC.

        default
        :default: - Function is not placed within a VPC.
        """
        return self._values.get('vpc')

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Where to place the network interfaces within the VPC.

        Only used if 'vpc' is supplied. Note: internet access for Lambdas
        requires a NAT gateway, so picking Public subnets is not allowed.

        default
        :default: - the Vpc default strategy if not specified
        """
        return self._values.get('vpc_subnets')

    @builtins.property
    def build_dir(self) -> typing.Optional[str]:
        """The build directory.

        default
        :default: - ``.build`` in the entry file directory

        stability
        :stability: experimental
        """
        return self._values.get('build_dir')

    @builtins.property
    def cache_dir(self) -> typing.Optional[str]:
        """The cache directory.

        Parcel uses a filesystem cache for fast rebuilds.

        default
        :default: - ``.cache`` in the root directory

        stability
        :stability: experimental
        """
        return self._values.get('cache_dir')

    @builtins.property
    def container_environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The environment variables to pass to the container running Parcel.

        default
        :default: - no environment variables are passed to the container

        stability
        :stability: experimental
        """
        return self._values.get('container_environment')

    @builtins.property
    def entry(self) -> typing.Optional[str]:
        """Path to the entry file (JavaScript or TypeScript).

        default
        :default:

        - Derived from the name of the defining file and the construct's id.
          If the ``NodejsFunction`` is defined in ``stack.ts`` with ``my-handler`` as id
          (``new NodejsFunction(this, 'my-handler')``), the construct will look at ``stack.my-handler.ts``
          and ``stack.my-handler.js``.

        stability
        :stability: experimental
        """
        return self._values.get('entry')

    @builtins.property
    def handler(self) -> typing.Optional[str]:
        """The name of the exported handler in the entry file.

        default
        :default: handler

        stability
        :stability: experimental
        """
        return self._values.get('handler')

    @builtins.property
    def minify(self) -> typing.Optional[bool]:
        """Whether to minify files when bundling.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('minify')

    @builtins.property
    def node_docker_tag(self) -> typing.Optional[str]:
        """The docker tag of the node base image to use in the parcel-bundler docker image.

        default
        :default: - the ``process.versions.node`` alpine image

        see
        :see: https://hub.docker.com/_/node/?tab=tags
        stability
        :stability: experimental
        """
        return self._values.get('node_docker_tag')

    @builtins.property
    def project_root(self) -> typing.Optional[str]:
        """The root of the project.

        This will be used as the source for the volume
        mounted in the Docker container. If you specify this prop, ensure that
        this path includes ``entry`` and any module/dependencies used by your
        function otherwise bundling will not be possible.

        default
        :default: - the closest path containing a .git folder

        stability
        :stability: experimental
        """
        return self._values.get('project_root')

    @builtins.property
    def runtime(self) -> typing.Optional[aws_cdk.aws_lambda.Runtime]:
        """The runtime environment.

        Only runtimes of the Node.js family are
        supported.

        default
        :default:

        - ``NODEJS_12_X`` if ``process.versions.node`` >= '12.0.0',
          ``NODEJS_10_X`` otherwise.

        stability
        :stability: experimental
        """
        return self._values.get('runtime')

    @builtins.property
    def source_maps(self) -> typing.Optional[bool]:
        """Whether to include source maps when bundling.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('source_maps')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NodejsFunctionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "NodejsFunction",
    "NodejsFunctionProps",
]

publication.publish()
