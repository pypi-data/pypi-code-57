"""
# monocdk Experiment

[![experimental](http://badges.github.io/stability-badges/dist/experimental.svg)](http://github.com/badges/stability-badges)

An **experiment** to bundle all of the CDK into a single module.

> :warning: Please don't use this module unless you are interested in providing
> feedback about this experience.

## Usage

### Installation

To try out `monocdk-experiment` replace all references to CDK Construct
Libraries (most `@aws-cdk/*` packages) in your `package.json` file with a single
entrey referring to `monocdk-experiment`.

You also need to add a reference to the `constructs` library, according to the
kind of project you are developing:

* For libraries, model the dependency under `devDependencies` **and** `peerDependencies`
* For apps, model the dependency under `dependencies` only

### Use in your code

#### Classic import

You can use a classic import to get access to each service namespaces:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from monocdk_experiment import core, aws_s3 as s3

app = core.App()
stack = core.Stack(app, "MonoCDK-Stack")

s3.Bucket(stack, "TestBucket")
```

#### Barrel import

Alternatively, you can use "barrel" imports:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from monocdk_experiment import App, Stack
from monocdk_experiment.aws_s3 import Bucket

app = App()
stack = Stack(app, "MonoCDK-Stack")

Bucket(stack, "TestBucket")
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

import constructs
from .cx_api import (CloudAssembly as _CloudAssembly_32c4802d, MetadataEntry as _MetadataEntry_206d90cd, CloudAssemblyBuilder as _CloudAssemblyBuilder_d6cb3525, MissingContext as _MissingContext_63fd4283, AssemblyBuildOptions as _AssemblyBuildOptions_44ebd659, RuntimeInfo as _RuntimeInfo_b6d338e9)


@jsii.data_type(jsii_type="monocdk-experiment.AppProps", jsii_struct_bases=[], name_mapping={'auto_synth': 'autoSynth', 'context': 'context', 'outdir': 'outdir', 'runtime_info': 'runtimeInfo', 'stack_traces': 'stackTraces', 'tree_metadata': 'treeMetadata'})
class AppProps():
    def __init__(self, *, auto_synth: typing.Optional[bool]=None, context: typing.Optional[typing.Mapping[str, str]]=None, outdir: typing.Optional[str]=None, runtime_info: typing.Optional[bool]=None, stack_traces: typing.Optional[bool]=None, tree_metadata: typing.Optional[bool]=None) -> None:
        """Initialization props for apps.

        :param auto_synth: Automatically call ``synth()`` before the program exits. If you set this, you don't have to call ``synth()`` explicitly. Note that this feature is only available for certain programming languages, and calling ``synth()`` is still recommended. Default: true if running via CDK CLI (``CDK_OUTDIR`` is set), ``false`` otherwise
        :param context: Additional context values for the application. Context set by the CLI or the ``context`` key in ``cdk.json`` has precedence. Context can be read from any construct using ``node.getContext(key)``. Default: - no additional context
        :param outdir: The output directory into which to emit synthesized artifacts. Default: - If this value is *not* set, considers the environment variable ``CDK_OUTDIR``. If ``CDK_OUTDIR`` is not defined, uses a temp directory.
        :param runtime_info: Include runtime versioning information in cloud assembly manifest. Default: true runtime info is included unless ``aws:cdk:disable-runtime-info`` is set in the context.
        :param stack_traces: Include construct creation stack trace in the ``aws:cdk:trace`` metadata key of all constructs. Default: true stack traces are included unless ``aws:cdk:disable-stack-trace`` is set in the context.
        :param tree_metadata: Include construct tree metadata as part of the Cloud Assembly. Default: true

        stability
        :stability: experimental
        """
        self._values = {
        }
        if auto_synth is not None: self._values["auto_synth"] = auto_synth
        if context is not None: self._values["context"] = context
        if outdir is not None: self._values["outdir"] = outdir
        if runtime_info is not None: self._values["runtime_info"] = runtime_info
        if stack_traces is not None: self._values["stack_traces"] = stack_traces
        if tree_metadata is not None: self._values["tree_metadata"] = tree_metadata

    @builtins.property
    def auto_synth(self) -> typing.Optional[bool]:
        """Automatically call ``synth()`` before the program exits.

        If you set this, you don't have to call ``synth()`` explicitly. Note that
        this feature is only available for certain programming languages, and
        calling ``synth()`` is still recommended.

        default
        :default:

        true if running via CDK CLI (``CDK_OUTDIR`` is set), ``false``
        otherwise

        stability
        :stability: experimental
        """
        return self._values.get('auto_synth')

    @builtins.property
    def context(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Additional context values for the application.

        Context set by the CLI or the ``context`` key in ``cdk.json`` has precedence.

        Context can be read from any construct using ``node.getContext(key)``.

        default
        :default: - no additional context

        stability
        :stability: experimental
        """
        return self._values.get('context')

    @builtins.property
    def outdir(self) -> typing.Optional[str]:
        """The output directory into which to emit synthesized artifacts.

        default
        :default:

        - If this value is *not* set, considers the environment variable ``CDK_OUTDIR``.
          If ``CDK_OUTDIR`` is not defined, uses a temp directory.

        stability
        :stability: experimental
        """
        return self._values.get('outdir')

    @builtins.property
    def runtime_info(self) -> typing.Optional[bool]:
        """Include runtime versioning information in cloud assembly manifest.

        default
        :default: true runtime info is included unless ``aws:cdk:disable-runtime-info`` is set in the context.

        stability
        :stability: experimental
        """
        return self._values.get('runtime_info')

    @builtins.property
    def stack_traces(self) -> typing.Optional[bool]:
        """Include construct creation stack trace in the ``aws:cdk:trace`` metadata key of all constructs.

        default
        :default: true stack traces are included unless ``aws:cdk:disable-stack-trace`` is set in the context.

        stability
        :stability: experimental
        """
        return self._values.get('stack_traces')

    @builtins.property
    def tree_metadata(self) -> typing.Optional[bool]:
        """Include construct tree metadata as part of the Cloud Assembly.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('tree_metadata')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AppProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Arn(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.Arn"):
    """
    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="format")
    @builtins.classmethod
    def format(cls, components: "ArnComponents", stack: "Stack") -> str:
        """Creates an ARN from components.

        If ``partition``, ``region`` or ``account`` are not specified, the stack's
        partition, region and account will be used.

        If any component is the empty string, an empty string will be inserted
        into the generated ARN at the location that component corresponds to.

        The ARN will be formatted as follows:

        arn:{partition}:{service}:{region}:{account}:{resource}{sep}{resource-name}

        The required ARN pieces that are omitted will be taken from the stack that
        the 'scope' is attached to. If all ARN pieces are supplied, the supplied scope
        can be 'undefined'.

        :param components: -
        :param stack: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "format", [components, stack])

    @jsii.member(jsii_name="parse")
    @builtins.classmethod
    def parse(cls, arn: str, sep_if_token: typing.Optional[str]=None, has_name: typing.Optional[bool]=None) -> "ArnComponents":
        """Given an ARN, parses it and returns components.

        If the ARN is a concrete string, it will be parsed and validated. The
        separator (``sep``) will be set to '/' if the 6th component includes a '/',
        in which case, ``resource`` will be set to the value before the '/' and
        ``resourceName`` will be the rest. In case there is no '/', ``resource`` will
        be set to the 6th components and ``resourceName`` will be set to the rest
        of the string.

        If the ARN includes tokens (or is a token), the ARN cannot be validated,
        since we don't have the actual value yet at the time of this function
        call. You will have to know the separator and the type of ARN. The
        resulting ``ArnComponents`` object will contain tokens for the
        subexpressions of the ARN, not string literals. In this case this
        function cannot properly parse the complete final resourceName (path) out
        of ARNs that use '/' to both separate the 'resource' from the
        'resourceName' AND to subdivide the resourceName further. For example, in
        S3 ARNs::

           arn:aws:s3:::my_corporate_bucket/path/to/exampleobject.png

        After parsing the resourceName will not contain
        'path/to/exampleobject.png' but simply 'path'. This is a limitation
        because there is no slicing functionality in CloudFormation templates.

        :param arn: The ARN to parse.
        :param sep_if_token: The separator used to separate resource from resourceName.
        :param has_name: Whether there is a name component in the ARN at all. For example, SNS Topics ARNs have the 'resource' component contain the topic name, and no 'resourceName' component.

        return
        :return:

        an ArnComponents object which allows access to the various
        components of the ARN.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "parse", [arn, sep_if_token, has_name])


@jsii.data_type(jsii_type="monocdk-experiment.ArnComponents", jsii_struct_bases=[], name_mapping={'resource': 'resource', 'service': 'service', 'account': 'account', 'partition': 'partition', 'region': 'region', 'resource_name': 'resourceName', 'sep': 'sep'})
class ArnComponents():
    def __init__(self, *, resource: str, service: str, account: typing.Optional[str]=None, partition: typing.Optional[str]=None, region: typing.Optional[str]=None, resource_name: typing.Optional[str]=None, sep: typing.Optional[str]=None) -> None:
        """
        :param resource: Resource type (e.g. "table", "autoScalingGroup", "certificate"). For some resource types, e.g. S3 buckets, this field defines the bucket name.
        :param service: The service namespace that identifies the AWS product (for example, 's3', 'iam', 'codepipline').
        :param account: The ID of the AWS account that owns the resource, without the hyphens. For example, 123456789012. Note that the ARNs for some resources don't require an account number, so this component might be omitted. Default: The account the stack is deployed to.
        :param partition: The partition that the resource is in. For standard AWS regions, the partition is aws. If you have resources in other partitions, the partition is aws-partitionname. For example, the partition for resources in the China (Beijing) region is aws-cn. Default: The AWS partition the stack is deployed to.
        :param region: The region the resource resides in. Note that the ARNs for some resources do not require a region, so this component might be omitted. Default: The region the stack is deployed to.
        :param resource_name: Resource name or path within the resource (i.e. S3 bucket object key) or a wildcard such as ``"*"``. This is service-dependent.
        :param sep: Separator between resource type and the resource. Can be either '/', ':' or an empty string. Will only be used if resourceName is defined. Default: '/'

        stability
        :stability: experimental
        """
        self._values = {
            'resource': resource,
            'service': service,
        }
        if account is not None: self._values["account"] = account
        if partition is not None: self._values["partition"] = partition
        if region is not None: self._values["region"] = region
        if resource_name is not None: self._values["resource_name"] = resource_name
        if sep is not None: self._values["sep"] = sep

    @builtins.property
    def resource(self) -> str:
        """Resource type (e.g. "table", "autoScalingGroup", "certificate"). For some resource types, e.g. S3 buckets, this field defines the bucket name.

        stability
        :stability: experimental
        """
        return self._values.get('resource')

    @builtins.property
    def service(self) -> str:
        """The service namespace that identifies the AWS product (for example, 's3', 'iam', 'codepipline').

        stability
        :stability: experimental
        """
        return self._values.get('service')

    @builtins.property
    def account(self) -> typing.Optional[str]:
        """The ID of the AWS account that owns the resource, without the hyphens.

        For example, 123456789012. Note that the ARNs for some resources don't
        require an account number, so this component might be omitted.

        default
        :default: The account the stack is deployed to.

        stability
        :stability: experimental
        """
        return self._values.get('account')

    @builtins.property
    def partition(self) -> typing.Optional[str]:
        """The partition that the resource is in.

        For standard AWS regions, the
        partition is aws. If you have resources in other partitions, the
        partition is aws-partitionname. For example, the partition for resources
        in the China (Beijing) region is aws-cn.

        default
        :default: The AWS partition the stack is deployed to.

        stability
        :stability: experimental
        """
        return self._values.get('partition')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """The region the resource resides in.

        Note that the ARNs for some resources
        do not require a region, so this component might be omitted.

        default
        :default: The region the stack is deployed to.

        stability
        :stability: experimental
        """
        return self._values.get('region')

    @builtins.property
    def resource_name(self) -> typing.Optional[str]:
        """Resource name or path within the resource (i.e. S3 bucket object key) or a wildcard such as ``"*"``. This is service-dependent.

        stability
        :stability: experimental
        """
        return self._values.get('resource_name')

    @builtins.property
    def sep(self) -> typing.Optional[str]:
        """Separator between resource type and the resource.

        Can be either '/', ':' or an empty string. Will only be used if resourceName is defined.

        default
        :default: '/'

        stability
        :stability: experimental
        """
        return self._values.get('sep')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ArnComponents(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.AssetHashType")
class AssetHashType(enum.Enum):
    """The type of asset hash.

    stability
    :stability: experimental
    """
    SOURCE = "SOURCE"
    """Based on the content of the source path.

    stability
    :stability: experimental
    """
    BUNDLE = "BUNDLE"
    """Based on the content of the bundled path.

    stability
    :stability: experimental
    """
    CUSTOM = "CUSTOM"
    """Use a custom hash.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.AssetOptions", jsii_struct_bases=[], name_mapping={'asset_hash': 'assetHash', 'asset_hash_type': 'assetHashType', 'bundling': 'bundling'})
class AssetOptions():
    def __init__(self, *, asset_hash: typing.Optional[str]=None, asset_hash_type: typing.Optional["AssetHashType"]=None, bundling: typing.Optional["BundlingOptions"]=None) -> None:
        """Asset hash options.

        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise

        stability
        :stability: experimental
        """
        if isinstance(bundling, dict): bundling = BundlingOptions(**bundling)
        self._values = {
        }
        if asset_hash is not None: self._values["asset_hash"] = asset_hash
        if asset_hash_type is not None: self._values["asset_hash_type"] = asset_hash_type
        if bundling is not None: self._values["bundling"] = bundling

    @builtins.property
    def asset_hash(self) -> typing.Optional[str]:
        """Specify a custom hash for this asset.

        If ``assetHashType`` is set it must
        be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will
        be SHA256 hashed and encoded as hex. The resulting hash will be the asset
        hash.

        NOTE: the hash is used in order to identify a specific revision of the asset, and
        used for optimizing and caching deployment activities related to this asset such as
        packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will
        need to make sure it is updated every time the asset changes, or otherwise it is
        possible that some deployments will not be invalidated.

        default
        :default: - based on ``assetHashType``

        stability
        :stability: experimental
        """
        return self._values.get('asset_hash')

    @builtins.property
    def asset_hash_type(self) -> typing.Optional["AssetHashType"]:
        """Specifies the type of hash to calculate for this asset.

        If ``assetHash`` is configured, this option must be ``undefined`` or
        ``AssetHashType.CUSTOM``.

        default
        :default:

        - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is
          explicitly specified this value defaults to ``AssetHashType.CUSTOM``.

        stability
        :stability: experimental
        """
        return self._values.get('asset_hash_type')

    @builtins.property
    def bundling(self) -> typing.Optional["BundlingOptions"]:
        """Bundle the asset by executing a command in a Docker container.

        The asset path will be mounted at ``/asset-input``. The Docker
        container is responsible for putting content at ``/asset-output``.
        The content at ``/asset-output`` will be zipped and used as the
        final asset.

        default
        :default:

        - uploaded as-is to S3 if the asset is a regular file or a .zip file,
          archived into a .zip file and uploaded to S3 otherwise

        stability
        :stability: experimental
        """
        return self._values.get('bundling')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AssetOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Aws(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.Aws"):
    """Accessor for pseudo parameters.

    Since pseudo parameters need to be anchored to a stack somewhere in the
    construct tree, this class takes an scope parameter; the pseudo parameter
    values can be obtained as properties from an scoped object.

    stability
    :stability: experimental
    """
    @jsii.python.classproperty
    @jsii.member(jsii_name="ACCOUNT_ID")
    def ACCOUNT_ID(cls) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "ACCOUNT_ID")

    @jsii.python.classproperty
    @jsii.member(jsii_name="NO_VALUE")
    def NO_VALUE(cls) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "NO_VALUE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="NOTIFICATION_ARNS")
    def NOTIFICATION_ARNS(cls) -> typing.List[str]:
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "NOTIFICATION_ARNS")

    @jsii.python.classproperty
    @jsii.member(jsii_name="PARTITION")
    def PARTITION(cls) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "PARTITION")

    @jsii.python.classproperty
    @jsii.member(jsii_name="REGION")
    def REGION(cls) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "REGION")

    @jsii.python.classproperty
    @jsii.member(jsii_name="STACK_ID")
    def STACK_ID(cls) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "STACK_ID")

    @jsii.python.classproperty
    @jsii.member(jsii_name="STACK_NAME")
    def STACK_NAME(cls) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "STACK_NAME")

    @jsii.python.classproperty
    @jsii.member(jsii_name="URL_SUFFIX")
    def URL_SUFFIX(cls) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "URL_SUFFIX")


@jsii.data_type(jsii_type="monocdk-experiment.BootstraplessSynthesizerProps", jsii_struct_bases=[], name_mapping={'cloud_formation_execution_role_arn': 'cloudFormationExecutionRoleArn', 'deploy_role_arn': 'deployRoleArn'})
class BootstraplessSynthesizerProps():
    def __init__(self, *, cloud_formation_execution_role_arn: typing.Optional[str]=None, deploy_role_arn: typing.Optional[str]=None) -> None:
        """Construction properties of {@link BootstraplessSynthesizer}.

        :param cloud_formation_execution_role_arn: The CFN execution Role ARN to use. Default: - No CloudFormation role (use CLI credentials)
        :param deploy_role_arn: The deploy Role ARN to use. Default: - No deploy role (use CLI credentials)

        stability
        :stability: experimental
        """
        self._values = {
        }
        if cloud_formation_execution_role_arn is not None: self._values["cloud_formation_execution_role_arn"] = cloud_formation_execution_role_arn
        if deploy_role_arn is not None: self._values["deploy_role_arn"] = deploy_role_arn

    @builtins.property
    def cloud_formation_execution_role_arn(self) -> typing.Optional[str]:
        """The CFN execution Role ARN to use.

        default
        :default: - No CloudFormation role (use CLI credentials)

        stability
        :stability: experimental
        """
        return self._values.get('cloud_formation_execution_role_arn')

    @builtins.property
    def deploy_role_arn(self) -> typing.Optional[str]:
        """The deploy Role ARN to use.

        default
        :default: - No deploy role (use CLI credentials)

        stability
        :stability: experimental
        """
        return self._values.get('deploy_role_arn')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BootstraplessSynthesizerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class BundlingDockerImage(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.BundlingDockerImage"):
    """A Docker image used for asset bundling.

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="fromAsset")
    @builtins.classmethod
    def from_asset(cls, path: str, *, build_args: typing.Optional[typing.Mapping[str, str]]=None) -> "BundlingDockerImage":
        """Reference an image that's built directly from sources on disk.

        :param path: The path to the directory containing the Docker file.
        :param build_args: Build args. Default: - no build args

        stability
        :stability: experimental
        """
        options = DockerBuildOptions(build_args=build_args)

        return jsii.sinvoke(cls, "fromAsset", [path, options])

    @jsii.member(jsii_name="fromRegistry")
    @builtins.classmethod
    def from_registry(cls, image: str) -> "BundlingDockerImage":
        """Reference an image on DockerHub or another online registry.

        :param image: the image name.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromRegistry", [image])

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> str:
        """The Docker image.

        stability
        :stability: experimental
        """
        return jsii.get(self, "image")


@jsii.data_type(jsii_type="monocdk-experiment.BundlingOptions", jsii_struct_bases=[], name_mapping={'image': 'image', 'command': 'command', 'environment': 'environment', 'user': 'user', 'volumes': 'volumes', 'working_directory': 'workingDirectory'})
class BundlingOptions():
    def __init__(self, *, image: "BundlingDockerImage", command: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, user: typing.Optional[str]=None, volumes: typing.Optional[typing.List["DockerVolume"]]=None, working_directory: typing.Optional[str]=None) -> None:
        """Bundling options.

        :param image: The Docker image where the command will run.
        :param command: The command to run in the container. Default: - run the command defined in the image
        :param environment: The environment variables to pass to the container. Default: - no environment variables.
        :param user: The user to use when running the container. user | user:group | uid | uid:gid | user:gid | uid:group Default: - uid:gid of the current user or 1000:1000 on Windows
        :param volumes: Additional Docker volumes to mount. Default: - no additional volumes are mounted
        :param working_directory: Working directory inside the container. Default: /asset-input

        stability
        :stability: experimental
        """
        self._values = {
            'image': image,
        }
        if command is not None: self._values["command"] = command
        if environment is not None: self._values["environment"] = environment
        if user is not None: self._values["user"] = user
        if volumes is not None: self._values["volumes"] = volumes
        if working_directory is not None: self._values["working_directory"] = working_directory

    @builtins.property
    def image(self) -> "BundlingDockerImage":
        """The Docker image where the command will run.

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @builtins.property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The command to run in the container.

        default
        :default: - run the command defined in the image

        see
        :see: https://docs.docker.com/engine/reference/run/
        stability
        :stability: experimental

        Example::

            # Example automatically generated. See https://github.com/aws/jsii/issues/826
            ["npm", "install"]
        """
        return self._values.get('command')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The environment variables to pass to the container.

        default
        :default: - no environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def user(self) -> typing.Optional[str]:
        """The user to use when running the container.

        user | user:group | uid | uid:gid | user:gid | uid:group

        default
        :default: - uid:gid of the current user or 1000:1000 on Windows

        see
        :see: https://docs.docker.com/engine/reference/run/#user
        stability
        :stability: experimental
        """
        return self._values.get('user')

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List["DockerVolume"]]:
        """Additional Docker volumes to mount.

        default
        :default: - no additional volumes are mounted

        stability
        :stability: experimental
        """
        return self._values.get('volumes')

    @builtins.property
    def working_directory(self) -> typing.Optional[str]:
        """Working directory inside the container.

        default
        :default: /asset-input

        stability
        :stability: experimental
        """
        return self._values.get('working_directory')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BundlingOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.CfnAutoScalingReplacingUpdate", jsii_struct_bases=[], name_mapping={'will_replace': 'willReplace'})
class CfnAutoScalingReplacingUpdate():
    def __init__(self, *, will_replace: typing.Optional[bool]=None) -> None:
        """Specifies whether an Auto Scaling group and the instances it contains are replaced during an update.

        During replacement,
        AWS CloudFormation retains the old group until it finishes creating the new one. If the update fails, AWS CloudFormation
        can roll back to the old Auto Scaling group and delete the new Auto Scaling group.

        While AWS CloudFormation creates the new group, it doesn't detach or attach any instances. After successfully creating
        the new Auto Scaling group, AWS CloudFormation deletes the old Auto Scaling group during the cleanup process.

        When you set the WillReplace parameter, remember to specify a matching CreationPolicy. If the minimum number of
        instances (specified by the MinSuccessfulInstancesPercent property) don't signal success within the Timeout period
        (specified in the CreationPolicy policy), the replacement update fails and AWS CloudFormation rolls back to the old
        Auto Scaling group.

        :param will_replace: 

        stability
        :stability: experimental
        """
        self._values = {
        }
        if will_replace is not None: self._values["will_replace"] = will_replace

    @builtins.property
    def will_replace(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('will_replace')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnAutoScalingReplacingUpdate(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.CfnAutoScalingRollingUpdate", jsii_struct_bases=[], name_mapping={'max_batch_size': 'maxBatchSize', 'min_instances_in_service': 'minInstancesInService', 'min_successful_instances_percent': 'minSuccessfulInstancesPercent', 'pause_time': 'pauseTime', 'suspend_processes': 'suspendProcesses', 'wait_on_resource_signals': 'waitOnResourceSignals'})
class CfnAutoScalingRollingUpdate():
    def __init__(self, *, max_batch_size: typing.Optional[jsii.Number]=None, min_instances_in_service: typing.Optional[jsii.Number]=None, min_successful_instances_percent: typing.Optional[jsii.Number]=None, pause_time: typing.Optional[str]=None, suspend_processes: typing.Optional[typing.List[str]]=None, wait_on_resource_signals: typing.Optional[bool]=None) -> None:
        """To specify how AWS CloudFormation handles rolling updates for an Auto Scaling group, use the AutoScalingRollingUpdate policy.

        Rolling updates enable you to specify whether AWS CloudFormation updates instances that are in an Auto Scaling
        group in batches or all at once.

        :param max_batch_size: Specifies the maximum number of instances that AWS CloudFormation updates.
        :param min_instances_in_service: Specifies the minimum number of instances that must be in service within the Auto Scaling group while AWS CloudFormation updates old instances.
        :param min_successful_instances_percent: Specifies the percentage of instances in an Auto Scaling rolling update that must signal success for an update to succeed. You can specify a value from 0 to 100. AWS CloudFormation rounds to the nearest tenth of a percent. For example, if you update five instances with a minimum successful percentage of 50, three instances must signal success. If an instance doesn't send a signal within the time specified in the PauseTime property, AWS CloudFormation assumes that the instance wasn't updated. If you specify this property, you must also enable the WaitOnResourceSignals and PauseTime properties.
        :param pause_time: The amount of time that AWS CloudFormation pauses after making a change to a batch of instances to give those instances time to start software applications. For example, you might need to specify PauseTime when scaling up the number of instances in an Auto Scaling group. If you enable the WaitOnResourceSignals property, PauseTime is the amount of time that AWS CloudFormation should wait for the Auto Scaling group to receive the required number of valid signals from added or replaced instances. If the PauseTime is exceeded before the Auto Scaling group receives the required number of signals, the update fails. For best results, specify a time period that gives your applications sufficient time to get started. If the update needs to be rolled back, a short PauseTime can cause the rollback to fail. Specify PauseTime in the ISO8601 duration format (in the format PT#H#M#S, where each # is the number of hours, minutes, and seconds, respectively). The maximum PauseTime is one hour (PT1H).
        :param suspend_processes: Specifies the Auto Scaling processes to suspend during a stack update. Suspending processes prevents Auto Scaling from interfering with a stack update. For example, you can suspend alarming so that Auto Scaling doesn't execute scaling policies associated with an alarm. For valid values, see the ScalingProcesses.member.N parameter for the SuspendProcesses action in the Auto Scaling API Reference.
        :param wait_on_resource_signals: Specifies whether the Auto Scaling group waits on signals from new instances during an update. Use this property to ensure that instances have completed installing and configuring applications before the Auto Scaling group update proceeds. AWS CloudFormation suspends the update of an Auto Scaling group after new EC2 instances are launched into the group. AWS CloudFormation must receive a signal from each new instance within the specified PauseTime before continuing the update. To signal the Auto Scaling group, use the cfn-signal helper script or SignalResource API. To have instances wait for an Elastic Load Balancing health check before they signal success, add a health-check verification by using the cfn-init helper script. For an example, see the verify_instance_health command in the Auto Scaling rolling updates sample template.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if max_batch_size is not None: self._values["max_batch_size"] = max_batch_size
        if min_instances_in_service is not None: self._values["min_instances_in_service"] = min_instances_in_service
        if min_successful_instances_percent is not None: self._values["min_successful_instances_percent"] = min_successful_instances_percent
        if pause_time is not None: self._values["pause_time"] = pause_time
        if suspend_processes is not None: self._values["suspend_processes"] = suspend_processes
        if wait_on_resource_signals is not None: self._values["wait_on_resource_signals"] = wait_on_resource_signals

    @builtins.property
    def max_batch_size(self) -> typing.Optional[jsii.Number]:
        """Specifies the maximum number of instances that AWS CloudFormation updates.

        stability
        :stability: experimental
        """
        return self._values.get('max_batch_size')

    @builtins.property
    def min_instances_in_service(self) -> typing.Optional[jsii.Number]:
        """Specifies the minimum number of instances that must be in service within the Auto Scaling group while AWS CloudFormation updates old instances.

        stability
        :stability: experimental
        """
        return self._values.get('min_instances_in_service')

    @builtins.property
    def min_successful_instances_percent(self) -> typing.Optional[jsii.Number]:
        """Specifies the percentage of instances in an Auto Scaling rolling update that must signal success for an update to succeed.

        You can specify a value from 0 to 100. AWS CloudFormation rounds to the nearest tenth of a percent. For example, if you
        update five instances with a minimum successful percentage of 50, three instances must signal success.

        If an instance doesn't send a signal within the time specified in the PauseTime property, AWS CloudFormation assumes
        that the instance wasn't updated.

        If you specify this property, you must also enable the WaitOnResourceSignals and PauseTime properties.

        stability
        :stability: experimental
        """
        return self._values.get('min_successful_instances_percent')

    @builtins.property
    def pause_time(self) -> typing.Optional[str]:
        """The amount of time that AWS CloudFormation pauses after making a change to a batch of instances to give those instances time to start software applications.

        For example, you might need to specify PauseTime when scaling up the number of
        instances in an Auto Scaling group.

        If you enable the WaitOnResourceSignals property, PauseTime is the amount of time that AWS CloudFormation should wait
        for the Auto Scaling group to receive the required number of valid signals from added or replaced instances. If the
        PauseTime is exceeded before the Auto Scaling group receives the required number of signals, the update fails. For best
        results, specify a time period that gives your applications sufficient time to get started. If the update needs to be
        rolled back, a short PauseTime can cause the rollback to fail.

        Specify PauseTime in the ISO8601 duration format (in the format PT#H#M#S, where each # is the number of hours, minutes,
        and seconds, respectively). The maximum PauseTime is one hour (PT1H).

        stability
        :stability: experimental
        """
        return self._values.get('pause_time')

    @builtins.property
    def suspend_processes(self) -> typing.Optional[typing.List[str]]:
        """Specifies the Auto Scaling processes to suspend during a stack update.

        Suspending processes prevents Auto Scaling from
        interfering with a stack update. For example, you can suspend alarming so that Auto Scaling doesn't execute scaling
        policies associated with an alarm. For valid values, see the ScalingProcesses.member.N parameter for the SuspendProcesses
        action in the Auto Scaling API Reference.

        stability
        :stability: experimental
        """
        return self._values.get('suspend_processes')

    @builtins.property
    def wait_on_resource_signals(self) -> typing.Optional[bool]:
        """Specifies whether the Auto Scaling group waits on signals from new instances during an update.

        Use this property to
        ensure that instances have completed installing and configuring applications before the Auto Scaling group update proceeds.
        AWS CloudFormation suspends the update of an Auto Scaling group after new EC2 instances are launched into the group.
        AWS CloudFormation must receive a signal from each new instance within the specified PauseTime before continuing the update.
        To signal the Auto Scaling group, use the cfn-signal helper script or SignalResource API.

        To have instances wait for an Elastic Load Balancing health check before they signal success, add a health-check
        verification by using the cfn-init helper script. For an example, see the verify_instance_health command in the Auto Scaling
        rolling updates sample template.

        stability
        :stability: experimental
        """
        return self._values.get('wait_on_resource_signals')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnAutoScalingRollingUpdate(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.CfnAutoScalingScheduledAction", jsii_struct_bases=[], name_mapping={'ignore_unmodified_group_size_properties': 'ignoreUnmodifiedGroupSizeProperties'})
class CfnAutoScalingScheduledAction():
    def __init__(self, *, ignore_unmodified_group_size_properties: typing.Optional[bool]=None) -> None:
        """With scheduled actions, the group size properties of an Auto Scaling group can change at any time.

        When you update a
        stack with an Auto Scaling group and scheduled action, AWS CloudFormation always sets the group size property values of
        your Auto Scaling group to the values that are defined in the AWS::AutoScaling::AutoScalingGroup resource of your template,
        even if a scheduled action is in effect.

        If you do not want AWS CloudFormation to change any of the group size property values when you have a scheduled action in
        effect, use the AutoScalingScheduledAction update policy to prevent AWS CloudFormation from changing the MinSize, MaxSize,
        or DesiredCapacity properties unless you have modified these values in your template.\

        :param ignore_unmodified_group_size_properties: 

        stability
        :stability: experimental
        """
        self._values = {
        }
        if ignore_unmodified_group_size_properties is not None: self._values["ignore_unmodified_group_size_properties"] = ignore_unmodified_group_size_properties

    @builtins.property
    def ignore_unmodified_group_size_properties(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('ignore_unmodified_group_size_properties')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnAutoScalingScheduledAction(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.CfnCapabilities")
class CfnCapabilities(enum.Enum):
    """Capabilities that affect whether CloudFormation is allowed to change IAM resources.

    stability
    :stability: experimental
    """
    NONE = "NONE"
    """No IAM Capabilities.

    Pass this capability if you wish to block the creation IAM resources.

    stability
    :stability: experimental
    link:
    :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
    """
    ANONYMOUS_IAM = "ANONYMOUS_IAM"
    """Capability to create anonymous IAM resources.

    Pass this capability if you're only creating anonymous resources.

    stability
    :stability: experimental
    link:
    :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
    """
    NAMED_IAM = "NAMED_IAM"
    """Capability to create named IAM resources.

    Pass this capability if you're creating IAM resources that have physical
    names.

    ``CloudFormationCapabilities.NamedIAM`` implies ``CloudFormationCapabilities.IAM``; you don't have to pass both.

    stability
    :stability: experimental
    link:
    :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
    """
    AUTO_EXPAND = "AUTO_EXPAND"
    """Capability to run CloudFormation macros.

    Pass this capability if your template includes macros, for example AWS::Include or AWS::Serverless.

    stability
    :stability: experimental
    link:
    :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/APIReference/API_CreateStack.html
    """

@jsii.data_type(jsii_type="monocdk-experiment.CfnCodeDeployLambdaAliasUpdate", jsii_struct_bases=[], name_mapping={'application_name': 'applicationName', 'deployment_group_name': 'deploymentGroupName', 'after_allow_traffic_hook': 'afterAllowTrafficHook', 'before_allow_traffic_hook': 'beforeAllowTrafficHook'})
class CfnCodeDeployLambdaAliasUpdate():
    def __init__(self, *, application_name: str, deployment_group_name: str, after_allow_traffic_hook: typing.Optional[str]=None, before_allow_traffic_hook: typing.Optional[str]=None) -> None:
        """To perform an AWS CodeDeploy deployment when the version changes on an AWS::Lambda::Alias resource, use the CodeDeployLambdaAliasUpdate update policy.

        :param application_name: The name of the AWS CodeDeploy application.
        :param deployment_group_name: The name of the AWS CodeDeploy deployment group. This is where the traffic-shifting policy is set.
        :param after_allow_traffic_hook: The name of the Lambda function to run after traffic routing completes.
        :param before_allow_traffic_hook: The name of the Lambda function to run before traffic routing starts.

        stability
        :stability: experimental
        """
        self._values = {
            'application_name': application_name,
            'deployment_group_name': deployment_group_name,
        }
        if after_allow_traffic_hook is not None: self._values["after_allow_traffic_hook"] = after_allow_traffic_hook
        if before_allow_traffic_hook is not None: self._values["before_allow_traffic_hook"] = before_allow_traffic_hook

    @builtins.property
    def application_name(self) -> str:
        """The name of the AWS CodeDeploy application.

        stability
        :stability: experimental
        """
        return self._values.get('application_name')

    @builtins.property
    def deployment_group_name(self) -> str:
        """The name of the AWS CodeDeploy deployment group.

        This is where the traffic-shifting policy is set.

        stability
        :stability: experimental
        """
        return self._values.get('deployment_group_name')

    @builtins.property
    def after_allow_traffic_hook(self) -> typing.Optional[str]:
        """The name of the Lambda function to run after traffic routing completes.

        stability
        :stability: experimental
        """
        return self._values.get('after_allow_traffic_hook')

    @builtins.property
    def before_allow_traffic_hook(self) -> typing.Optional[str]:
        """The name of the Lambda function to run before traffic routing starts.

        stability
        :stability: experimental
        """
        return self._values.get('before_allow_traffic_hook')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnCodeDeployLambdaAliasUpdate(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.CfnConditionProps", jsii_struct_bases=[], name_mapping={'expression': 'expression'})
class CfnConditionProps():
    def __init__(self, *, expression: typing.Optional["ICfnConditionExpression"]=None) -> None:
        """
        :param expression: The expression that the condition will evaluate. Default: - None.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if expression is not None: self._values["expression"] = expression

    @builtins.property
    def expression(self) -> typing.Optional["ICfnConditionExpression"]:
        """The expression that the condition will evaluate.

        default
        :default: - None.

        stability
        :stability: experimental
        """
        return self._values.get('expression')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnConditionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.CfnCreationPolicy", jsii_struct_bases=[], name_mapping={'auto_scaling_creation_policy': 'autoScalingCreationPolicy', 'resource_signal': 'resourceSignal'})
class CfnCreationPolicy():
    def __init__(self, *, auto_scaling_creation_policy: typing.Optional["CfnResourceAutoScalingCreationPolicy"]=None, resource_signal: typing.Optional["CfnResourceSignal"]=None) -> None:
        """Associate the CreationPolicy attribute with a resource to prevent its status from reaching create complete until AWS CloudFormation receives a specified number of success signals or the timeout period is exceeded.

        To signal a
        resource, you can use the cfn-signal helper script or SignalResource API. AWS CloudFormation publishes valid signals
        to the stack events so that you track the number of signals sent.

        The creation policy is invoked only when AWS CloudFormation creates the associated resource. Currently, the only
        AWS CloudFormation resources that support creation policies are AWS::AutoScaling::AutoScalingGroup, AWS::EC2::Instance,
        and AWS::CloudFormation::WaitCondition.

        Use the CreationPolicy attribute when you want to wait on resource configuration actions before stack creation proceeds.
        For example, if you install and configure software applications on an EC2 instance, you might want those applications to
        be running before proceeding. In such cases, you can add a CreationPolicy attribute to the instance, and then send a success
        signal to the instance after the applications are installed and configured. For a detailed example, see Deploying Applications
        on Amazon EC2 with AWS CloudFormation.

        :param auto_scaling_creation_policy: For an Auto Scaling group replacement update, specifies how many instances must signal success for the update to succeed.
        :param resource_signal: When AWS CloudFormation creates the associated resource, configures the number of required success signals and the length of time that AWS CloudFormation waits for those signals.

        stability
        :stability: experimental
        """
        if isinstance(auto_scaling_creation_policy, dict): auto_scaling_creation_policy = CfnResourceAutoScalingCreationPolicy(**auto_scaling_creation_policy)
        if isinstance(resource_signal, dict): resource_signal = CfnResourceSignal(**resource_signal)
        self._values = {
        }
        if auto_scaling_creation_policy is not None: self._values["auto_scaling_creation_policy"] = auto_scaling_creation_policy
        if resource_signal is not None: self._values["resource_signal"] = resource_signal

    @builtins.property
    def auto_scaling_creation_policy(self) -> typing.Optional["CfnResourceAutoScalingCreationPolicy"]:
        """For an Auto Scaling group replacement update, specifies how many instances must signal success for the update to succeed.

        stability
        :stability: experimental
        """
        return self._values.get('auto_scaling_creation_policy')

    @builtins.property
    def resource_signal(self) -> typing.Optional["CfnResourceSignal"]:
        """When AWS CloudFormation creates the associated resource, configures the number of required success signals and the length of time that AWS CloudFormation waits for those signals.

        stability
        :stability: experimental
        """
        return self._values.get('resource_signal')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnCreationPolicy(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.CfnCustomResourceProps", jsii_struct_bases=[], name_mapping={'service_token': 'serviceToken'})
class CfnCustomResourceProps():
    def __init__(self, *, service_token: str) -> None:
        """Properties for defining a ``AWS::CloudFormation::CustomResource``.

        :param service_token: ``AWS::CloudFormation::CustomResource.ServiceToken``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html
        """
        self._values = {
            'service_token': service_token,
        }

    @builtins.property
    def service_token(self) -> str:
        """``AWS::CloudFormation::CustomResource.ServiceToken``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html#cfn-customresource-servicetoken
        """
        return self._values.get('service_token')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnCustomResourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.CfnDeletionPolicy")
class CfnDeletionPolicy(enum.Enum):
    """With the DeletionPolicy attribute you can preserve or (in some cases) backup a resource when its stack is deleted.

    You specify a DeletionPolicy attribute for each resource that you want to control. If a resource has no DeletionPolicy
    attribute, AWS CloudFormation deletes the resource by default. Note that this capability also applies to update operations
    that lead to resources being removed.

    stability
    :stability: experimental
    """
    DELETE = "DELETE"
    """AWS CloudFormation deletes the resource and all its content if applicable during stack deletion.

    You can add this
    deletion policy to any resource type. By default, if you don't specify a DeletionPolicy, AWS CloudFormation deletes
    your resources. However, be aware of the following considerations:

    stability
    :stability: experimental
    """
    RETAIN = "RETAIN"
    """AWS CloudFormation keeps the resource without deleting the resource or its contents when its stack is deleted.

    You can add this deletion policy to any resource type. Note that when AWS CloudFormation completes the stack deletion,
    the stack will be in Delete_Complete state; however, resources that are retained continue to exist and continue to incur
    applicable charges until you delete those resources.

    stability
    :stability: experimental
    """
    SNAPSHOT = "SNAPSHOT"
    """For resources that support snapshots (AWS::EC2::Volume, AWS::ElastiCache::CacheCluster, AWS::ElastiCache::ReplicationGroup, AWS::RDS::DBInstance, AWS::RDS::DBCluster, and AWS::Redshift::Cluster), AWS CloudFormation creates a snapshot for the resource before deleting it.

    Note that when AWS CloudFormation completes the stack deletion, the stack will be in the
    Delete_Complete state; however, the snapshots that are created with this policy continue to exist and continue to
    incur applicable charges until you delete those snapshots.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.CfnDynamicReferenceProps", jsii_struct_bases=[], name_mapping={'reference_key': 'referenceKey', 'service': 'service'})
class CfnDynamicReferenceProps():
    def __init__(self, *, reference_key: str, service: "CfnDynamicReferenceService") -> None:
        """Properties for a Dynamic Reference.

        :param reference_key: The reference key of the dynamic reference.
        :param service: The service to retrieve the dynamic reference from.

        stability
        :stability: experimental
        """
        self._values = {
            'reference_key': reference_key,
            'service': service,
        }

    @builtins.property
    def reference_key(self) -> str:
        """The reference key of the dynamic reference.

        stability
        :stability: experimental
        """
        return self._values.get('reference_key')

    @builtins.property
    def service(self) -> "CfnDynamicReferenceService":
        """The service to retrieve the dynamic reference from.

        stability
        :stability: experimental
        """
        return self._values.get('service')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDynamicReferenceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.CfnDynamicReferenceService")
class CfnDynamicReferenceService(enum.Enum):
    """The service to retrieve the dynamic reference from.

    stability
    :stability: experimental
    """
    SSM = "SSM"
    """Plaintext value stored in AWS Systems Manager Parameter Store.

    stability
    :stability: experimental
    """
    SSM_SECURE = "SSM_SECURE"
    """Secure string stored in AWS Systems Manager Parameter Store.

    stability
    :stability: experimental
    """
    SECRETS_MANAGER = "SECRETS_MANAGER"
    """Secret stored in AWS Secrets Manager.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.CfnIncludeProps", jsii_struct_bases=[], name_mapping={'template': 'template'})
class CfnIncludeProps():
    def __init__(self, *, template: typing.Mapping[typing.Any, typing.Any]) -> None:
        """
        :param template: The CloudFormation template to include in the stack (as is).

        stability
        :stability: experimental
        """
        self._values = {
            'template': template,
        }

    @builtins.property
    def template(self) -> typing.Mapping[typing.Any, typing.Any]:
        """The CloudFormation template to include in the stack (as is).

        stability
        :stability: experimental
        """
        return self._values.get('template')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnIncludeProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.CfnJsonProps", jsii_struct_bases=[], name_mapping={'value': 'value'})
class CfnJsonProps():
    def __init__(self, *, value: typing.Any) -> None:
        """
        :param value: The value to resolve. Can be any JavaScript object, including tokens and references in keys or values.

        stability
        :stability: experimental
        """
        self._values = {
            'value': value,
        }

    @builtins.property
    def value(self) -> typing.Any:
        """The value to resolve.

        Can be any JavaScript object, including tokens and
        references in keys or values.

        stability
        :stability: experimental
        """
        return self._values.get('value')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnJsonProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.CfnMacroProps", jsii_struct_bases=[], name_mapping={'function_name': 'functionName', 'name': 'name', 'description': 'description', 'log_group_name': 'logGroupName', 'log_role_arn': 'logRoleArn'})
class CfnMacroProps():
    def __init__(self, *, function_name: str, name: str, description: typing.Optional[str]=None, log_group_name: typing.Optional[str]=None, log_role_arn: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::CloudFormation::Macro``.

        :param function_name: ``AWS::CloudFormation::Macro.FunctionName``.
        :param name: ``AWS::CloudFormation::Macro.Name``.
        :param description: ``AWS::CloudFormation::Macro.Description``.
        :param log_group_name: ``AWS::CloudFormation::Macro.LogGroupName``.
        :param log_role_arn: ``AWS::CloudFormation::Macro.LogRoleARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html
        """
        self._values = {
            'function_name': function_name,
            'name': name,
        }
        if description is not None: self._values["description"] = description
        if log_group_name is not None: self._values["log_group_name"] = log_group_name
        if log_role_arn is not None: self._values["log_role_arn"] = log_role_arn

    @builtins.property
    def function_name(self) -> str:
        """``AWS::CloudFormation::Macro.FunctionName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-functionname
        """
        return self._values.get('function_name')

    @builtins.property
    def name(self) -> str:
        """``AWS::CloudFormation::Macro.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-name
        """
        return self._values.get('name')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::CloudFormation::Macro.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-description
        """
        return self._values.get('description')

    @builtins.property
    def log_group_name(self) -> typing.Optional[str]:
        """``AWS::CloudFormation::Macro.LogGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-loggroupname
        """
        return self._values.get('log_group_name')

    @builtins.property
    def log_role_arn(self) -> typing.Optional[str]:
        """``AWS::CloudFormation::Macro.LogRoleARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-logrolearn
        """
        return self._values.get('log_role_arn')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnMacroProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.CfnMappingProps", jsii_struct_bases=[], name_mapping={'mapping': 'mapping'})
class CfnMappingProps():
    def __init__(self, *, mapping: typing.Optional[typing.Mapping[str, typing.Mapping[str, typing.Any]]]=None) -> None:
        """
        :param mapping: Mapping of key to a set of corresponding set of named values. The key identifies a map of name-value pairs and must be unique within the mapping. For example, if you want to set values based on a region, you can create a mapping that uses the region name as a key and contains the values you want to specify for each specific region. Default: - No mapping.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if mapping is not None: self._values["mapping"] = mapping

    @builtins.property
    def mapping(self) -> typing.Optional[typing.Mapping[str, typing.Mapping[str, typing.Any]]]:
        """Mapping of key to a set of corresponding set of named values.

        The key identifies a map of name-value pairs and must be unique within the mapping.

        For example, if you want to set values based on a region, you can create a mapping
        that uses the region name as a key and contains the values you want to specify for
        each specific region.

        default
        :default: - No mapping.

        stability
        :stability: experimental
        """
        return self._values.get('mapping')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnMappingProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.CfnOutputProps", jsii_struct_bases=[], name_mapping={'value': 'value', 'condition': 'condition', 'description': 'description', 'export_name': 'exportName'})
class CfnOutputProps():
    def __init__(self, *, value: str, condition: typing.Optional["CfnCondition"]=None, description: typing.Optional[str]=None, export_name: typing.Optional[str]=None) -> None:
        """
        :param value: The value of the property returned by the aws cloudformation describe-stacks command. The value of an output can include literals, parameter references, pseudo-parameters, a mapping value, or intrinsic functions.
        :param condition: A condition to associate with this output value. If the condition evaluates to ``false``, this output value will not be included in the stack. Default: - No condition is associated with the output.
        :param description: A String type that describes the output value. The description can be a maximum of 4 K in length. Default: - No description.
        :param export_name: The name used to export the value of this output across stacks. To import the value from another stack, use ``Fn.importValue(exportName)``. Default: - the output is not exported

        stability
        :stability: experimental
        """
        self._values = {
            'value': value,
        }
        if condition is not None: self._values["condition"] = condition
        if description is not None: self._values["description"] = description
        if export_name is not None: self._values["export_name"] = export_name

    @builtins.property
    def value(self) -> str:
        """The value of the property returned by the aws cloudformation describe-stacks command.

        The value of an output can include literals, parameter references, pseudo-parameters,
        a mapping value, or intrinsic functions.

        stability
        :stability: experimental
        """
        return self._values.get('value')

    @builtins.property
    def condition(self) -> typing.Optional["CfnCondition"]:
        """A condition to associate with this output value.

        If the condition evaluates
        to ``false``, this output value will not be included in the stack.

        default
        :default: - No condition is associated with the output.

        stability
        :stability: experimental
        """
        return self._values.get('condition')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A String type that describes the output value.

        The description can be a maximum of 4 K in length.

        default
        :default: - No description.

        stability
        :stability: experimental
        """
        return self._values.get('description')

    @builtins.property
    def export_name(self) -> typing.Optional[str]:
        """The name used to export the value of this output across stacks.

        To import the value from another stack, use ``Fn.importValue(exportName)``.

        default
        :default: - the output is not exported

        stability
        :stability: experimental
        """
        return self._values.get('export_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnOutputProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.CfnParameterProps", jsii_struct_bases=[], name_mapping={'allowed_pattern': 'allowedPattern', 'allowed_values': 'allowedValues', 'constraint_description': 'constraintDescription', 'default': 'default', 'description': 'description', 'max_length': 'maxLength', 'max_value': 'maxValue', 'min_length': 'minLength', 'min_value': 'minValue', 'no_echo': 'noEcho', 'type': 'type'})
class CfnParameterProps():
    def __init__(self, *, allowed_pattern: typing.Optional[str]=None, allowed_values: typing.Optional[typing.List[str]]=None, constraint_description: typing.Optional[str]=None, default: typing.Any=None, description: typing.Optional[str]=None, max_length: typing.Optional[jsii.Number]=None, max_value: typing.Optional[jsii.Number]=None, min_length: typing.Optional[jsii.Number]=None, min_value: typing.Optional[jsii.Number]=None, no_echo: typing.Optional[bool]=None, type: typing.Optional[str]=None) -> None:
        """
        :param allowed_pattern: A regular expression that represents the patterns to allow for String types. Default: - No constraints on patterns allowed for parameter.
        :param allowed_values: An array containing the list of values allowed for the parameter. Default: - No constraints on values allowed for parameter.
        :param constraint_description: A string that explains a constraint when the constraint is violated. For example, without a constraint description, a parameter that has an allowed pattern of [A-Za-z0-9]+ displays the following error message when the user specifies an invalid value: Default: - No description with customized error message when user specifies invalid values.
        :param default: A value of the appropriate type for the template to use if no value is specified when a stack is created. If you define constraints for the parameter, you must specify a value that adheres to those constraints. Default: - No default value for parameter.
        :param description: A string of up to 4000 characters that describes the parameter. Default: - No description for the parameter.
        :param max_length: An integer value that determines the largest number of characters you want to allow for String types. Default: - None.
        :param max_value: A numeric value that determines the largest numeric value you want to allow for Number types. Default: - None.
        :param min_length: An integer value that determines the smallest number of characters you want to allow for String types. Default: - None.
        :param min_value: A numeric value that determines the smallest numeric value you want to allow for Number types. Default: - None.
        :param no_echo: Whether to mask the parameter value when anyone makes a call that describes the stack. If you set the value to ``true``, the parameter value is masked with asterisks (``*****``). Default: - Parameter values are not masked.
        :param type: The data type for the parameter (DataType). Default: String

        stability
        :stability: experimental
        """
        self._values = {
        }
        if allowed_pattern is not None: self._values["allowed_pattern"] = allowed_pattern
        if allowed_values is not None: self._values["allowed_values"] = allowed_values
        if constraint_description is not None: self._values["constraint_description"] = constraint_description
        if default is not None: self._values["default"] = default
        if description is not None: self._values["description"] = description
        if max_length is not None: self._values["max_length"] = max_length
        if max_value is not None: self._values["max_value"] = max_value
        if min_length is not None: self._values["min_length"] = min_length
        if min_value is not None: self._values["min_value"] = min_value
        if no_echo is not None: self._values["no_echo"] = no_echo
        if type is not None: self._values["type"] = type

    @builtins.property
    def allowed_pattern(self) -> typing.Optional[str]:
        """A regular expression that represents the patterns to allow for String types.

        default
        :default: - No constraints on patterns allowed for parameter.

        stability
        :stability: experimental
        """
        return self._values.get('allowed_pattern')

    @builtins.property
    def allowed_values(self) -> typing.Optional[typing.List[str]]:
        """An array containing the list of values allowed for the parameter.

        default
        :default: - No constraints on values allowed for parameter.

        stability
        :stability: experimental
        """
        return self._values.get('allowed_values')

    @builtins.property
    def constraint_description(self) -> typing.Optional[str]:
        """A string that explains a constraint when the constraint is violated.

        For example, without a constraint description, a parameter that has an allowed
        pattern of [A-Za-z0-9]+ displays the following error message when the user specifies
        an invalid value:

        default
        :default: - No description with customized error message when user specifies invalid values.

        stability
        :stability: experimental
        """
        return self._values.get('constraint_description')

    @builtins.property
    def default(self) -> typing.Any:
        """A value of the appropriate type for the template to use if no value is specified when a stack is created.

        If you define constraints for the parameter, you must specify
        a value that adheres to those constraints.

        default
        :default: - No default value for parameter.

        stability
        :stability: experimental
        """
        return self._values.get('default')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A string of up to 4000 characters that describes the parameter.

        default
        :default: - No description for the parameter.

        stability
        :stability: experimental
        """
        return self._values.get('description')

    @builtins.property
    def max_length(self) -> typing.Optional[jsii.Number]:
        """An integer value that determines the largest number of characters you want to allow for String types.

        default
        :default: - None.

        stability
        :stability: experimental
        """
        return self._values.get('max_length')

    @builtins.property
    def max_value(self) -> typing.Optional[jsii.Number]:
        """A numeric value that determines the largest numeric value you want to allow for Number types.

        default
        :default: - None.

        stability
        :stability: experimental
        """
        return self._values.get('max_value')

    @builtins.property
    def min_length(self) -> typing.Optional[jsii.Number]:
        """An integer value that determines the smallest number of characters you want to allow for String types.

        default
        :default: - None.

        stability
        :stability: experimental
        """
        return self._values.get('min_length')

    @builtins.property
    def min_value(self) -> typing.Optional[jsii.Number]:
        """A numeric value that determines the smallest numeric value you want to allow for Number types.

        default
        :default: - None.

        stability
        :stability: experimental
        """
        return self._values.get('min_value')

    @builtins.property
    def no_echo(self) -> typing.Optional[bool]:
        """Whether to mask the parameter value when anyone makes a call that describes the stack.

        If you set the value to ``true``, the parameter value is masked with asterisks (``*****``).

        default
        :default: - Parameter values are not masked.

        stability
        :stability: experimental
        """
        return self._values.get('no_echo')

    @builtins.property
    def type(self) -> typing.Optional[str]:
        """The data type for the parameter (DataType).

        default
        :default: String

        stability
        :stability: experimental
        """
        return self._values.get('type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnParameterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.CfnResourceAutoScalingCreationPolicy", jsii_struct_bases=[], name_mapping={'min_successful_instances_percent': 'minSuccessfulInstancesPercent'})
class CfnResourceAutoScalingCreationPolicy():
    def __init__(self, *, min_successful_instances_percent: typing.Optional[jsii.Number]=None) -> None:
        """For an Auto Scaling group replacement update, specifies how many instances must signal success for the update to succeed.

        :param min_successful_instances_percent: Specifies the percentage of instances in an Auto Scaling replacement update that must signal success for the update to succeed. You can specify a value from 0 to 100. AWS CloudFormation rounds to the nearest tenth of a percent. For example, if you update five instances with a minimum successful percentage of 50, three instances must signal success. If an instance doesn't send a signal within the time specified by the Timeout property, AWS CloudFormation assumes that the instance wasn't created.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if min_successful_instances_percent is not None: self._values["min_successful_instances_percent"] = min_successful_instances_percent

    @builtins.property
    def min_successful_instances_percent(self) -> typing.Optional[jsii.Number]:
        """Specifies the percentage of instances in an Auto Scaling replacement update that must signal success for the update to succeed.

        You can specify a value from 0 to 100. AWS CloudFormation rounds to the nearest tenth of a percent.
        For example, if you update five instances with a minimum successful percentage of 50, three instances must signal success.
        If an instance doesn't send a signal within the time specified by the Timeout property, AWS CloudFormation assumes that the
        instance wasn't created.

        stability
        :stability: experimental
        """
        return self._values.get('min_successful_instances_percent')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnResourceAutoScalingCreationPolicy(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.CfnResourceProps", jsii_struct_bases=[], name_mapping={'type': 'type', 'properties': 'properties'})
class CfnResourceProps():
    def __init__(self, *, type: str, properties: typing.Optional[typing.Mapping[str, typing.Any]]=None) -> None:
        """
        :param type: CloudFormation resource type (e.g. ``AWS::S3::Bucket``).
        :param properties: Resource properties. Default: - No resource properties.

        stability
        :stability: experimental
        """
        self._values = {
            'type': type,
        }
        if properties is not None: self._values["properties"] = properties

    @builtins.property
    def type(self) -> str:
        """CloudFormation resource type (e.g. ``AWS::S3::Bucket``).

        stability
        :stability: experimental
        """
        return self._values.get('type')

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Resource properties.

        default
        :default: - No resource properties.

        stability
        :stability: experimental
        """
        return self._values.get('properties')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnResourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.CfnResourceSignal", jsii_struct_bases=[], name_mapping={'count': 'count', 'timeout': 'timeout'})
class CfnResourceSignal():
    def __init__(self, *, count: typing.Optional[jsii.Number]=None, timeout: typing.Optional[str]=None) -> None:
        """When AWS CloudFormation creates the associated resource, configures the number of required success signals and the length of time that AWS CloudFormation waits for those signals.

        :param count: The number of success signals AWS CloudFormation must receive before it sets the resource status as CREATE_COMPLETE. If the resource receives a failure signal or doesn't receive the specified number of signals before the timeout period expires, the resource creation fails and AWS CloudFormation rolls the stack back.
        :param timeout: The length of time that AWS CloudFormation waits for the number of signals that was specified in the Count property. The timeout period starts after AWS CloudFormation starts creating the resource, and the timeout expires no sooner than the time you specify but can occur shortly thereafter. The maximum time that you can specify is 12 hours.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if count is not None: self._values["count"] = count
        if timeout is not None: self._values["timeout"] = timeout

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """The number of success signals AWS CloudFormation must receive before it sets the resource status as CREATE_COMPLETE.

        If the resource receives a failure signal or doesn't receive the specified number of signals before the timeout period
        expires, the resource creation fails and AWS CloudFormation rolls the stack back.

        stability
        :stability: experimental
        """
        return self._values.get('count')

    @builtins.property
    def timeout(self) -> typing.Optional[str]:
        """The length of time that AWS CloudFormation waits for the number of signals that was specified in the Count property.

        The timeout period starts after AWS CloudFormation starts creating the resource, and the timeout expires no sooner
        than the time you specify but can occur shortly thereafter. The maximum time that you can specify is 12 hours.

        stability
        :stability: experimental
        """
        return self._values.get('timeout')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnResourceSignal(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.CfnRuleAssertion", jsii_struct_bases=[], name_mapping={'assert_': 'assert', 'assert_description': 'assertDescription'})
class CfnRuleAssertion():
    def __init__(self, *, assert_: "ICfnConditionExpression", assert_description: str) -> None:
        """A rule assertion.

        :param assert_: The assertion.
        :param assert_description: The assertion description.

        stability
        :stability: experimental
        """
        self._values = {
            'assert_': assert_,
            'assert_description': assert_description,
        }

    @builtins.property
    def assert_(self) -> "ICfnConditionExpression":
        """The assertion.

        stability
        :stability: experimental
        """
        return self._values.get('assert_')

    @builtins.property
    def assert_description(self) -> str:
        """The assertion description.

        stability
        :stability: experimental
        """
        return self._values.get('assert_description')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnRuleAssertion(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.CfnRuleProps", jsii_struct_bases=[], name_mapping={'assertions': 'assertions', 'rule_condition': 'ruleCondition'})
class CfnRuleProps():
    def __init__(self, *, assertions: typing.Optional[typing.List["CfnRuleAssertion"]]=None, rule_condition: typing.Optional["ICfnConditionExpression"]=None) -> None:
        """A rule can include a RuleCondition property and must include an Assertions property.

        For each rule, you can define only one rule condition; you can define one or more asserts within the Assertions property.
        You define a rule condition and assertions by using rule-specific intrinsic functions.

        You can use the following rule-specific intrinsic functions to define rule conditions and assertions:

        Fn::And
        Fn::Contains
        Fn::EachMemberEquals
        Fn::EachMemberIn
        Fn::Equals
        Fn::If
        Fn::Not
        Fn::Or
        Fn::RefAll
        Fn::ValueOf
        Fn::ValueOfAll

        https://docs.aws.amazon.com/servicecatalog/latest/adminguide/reference-template_constraint_rules.html

        :param assertions: Assertions which define the rule. Default: - No assertions for the rule.
        :param rule_condition: If the rule condition evaluates to false, the rule doesn't take effect. If the function in the rule condition evaluates to true, expressions in each assert are evaluated and applied. Default: - Rule's assertions will always take effect.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if assertions is not None: self._values["assertions"] = assertions
        if rule_condition is not None: self._values["rule_condition"] = rule_condition

    @builtins.property
    def assertions(self) -> typing.Optional[typing.List["CfnRuleAssertion"]]:
        """Assertions which define the rule.

        default
        :default: - No assertions for the rule.

        stability
        :stability: experimental
        """
        return self._values.get('assertions')

    @builtins.property
    def rule_condition(self) -> typing.Optional["ICfnConditionExpression"]:
        """If the rule condition evaluates to false, the rule doesn't take effect.

        If the function in the rule condition evaluates to true, expressions in each assert are evaluated and applied.

        default
        :default: - Rule's assertions will always take effect.

        stability
        :stability: experimental
        """
        return self._values.get('rule_condition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnRuleProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.CfnStackProps", jsii_struct_bases=[], name_mapping={'template_url': 'templateUrl', 'notification_arns': 'notificationArns', 'parameters': 'parameters', 'tags': 'tags', 'timeout_in_minutes': 'timeoutInMinutes'})
class CfnStackProps():
    def __init__(self, *, template_url: str, notification_arns: typing.Optional[typing.List[str]]=None, parameters: typing.Optional[typing.Union["IResolvable", typing.Mapping[str, str]]]=None, tags: typing.Optional[typing.List["CfnTag"]]=None, timeout_in_minutes: typing.Optional[jsii.Number]=None) -> None:
        """Properties for defining a ``AWS::CloudFormation::Stack``.

        :param template_url: ``AWS::CloudFormation::Stack.TemplateURL``.
        :param notification_arns: ``AWS::CloudFormation::Stack.NotificationARNs``.
        :param parameters: ``AWS::CloudFormation::Stack.Parameters``.
        :param tags: ``AWS::CloudFormation::Stack.Tags``.
        :param timeout_in_minutes: ``AWS::CloudFormation::Stack.TimeoutInMinutes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html
        """
        self._values = {
            'template_url': template_url,
        }
        if notification_arns is not None: self._values["notification_arns"] = notification_arns
        if parameters is not None: self._values["parameters"] = parameters
        if tags is not None: self._values["tags"] = tags
        if timeout_in_minutes is not None: self._values["timeout_in_minutes"] = timeout_in_minutes

    @builtins.property
    def template_url(self) -> str:
        """``AWS::CloudFormation::Stack.TemplateURL``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-templateurl
        """
        return self._values.get('template_url')

    @builtins.property
    def notification_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::CloudFormation::Stack.NotificationARNs``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-notificationarns
        """
        return self._values.get('notification_arns')

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Union["IResolvable", typing.Mapping[str, str]]]:
        """``AWS::CloudFormation::Stack.Parameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-parameters
        """
        return self._values.get('parameters')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["CfnTag"]]:
        """``AWS::CloudFormation::Stack.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-tags
        """
        return self._values.get('tags')

    @builtins.property
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        """``AWS::CloudFormation::Stack.TimeoutInMinutes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-timeoutinminutes
        """
        return self._values.get('timeout_in_minutes')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnStackProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.CfnTag", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value'})
class CfnTag():
    def __init__(self, *, key: str, value: str) -> None:
        """
        :param key: 
        :param value: 

        stability
        :stability: experimental
        link:
        :link:: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html
        """
        self._values = {
            'key': key,
            'value': value,
        }

    @builtins.property
    def key(self) -> str:
        """
        stability
        :stability: experimental
        link:
        :link:: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html#cfn-resource-tags-key
        """
        return self._values.get('key')

    @builtins.property
    def value(self) -> str:
        """
        stability
        :stability: experimental
        link:
        :link:: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html#cfn-resource-tags-value
        """
        return self._values.get('value')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnTag(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.CfnUpdatePolicy", jsii_struct_bases=[], name_mapping={'auto_scaling_replacing_update': 'autoScalingReplacingUpdate', 'auto_scaling_rolling_update': 'autoScalingRollingUpdate', 'auto_scaling_scheduled_action': 'autoScalingScheduledAction', 'code_deploy_lambda_alias_update': 'codeDeployLambdaAliasUpdate', 'enable_version_upgrade': 'enableVersionUpgrade', 'use_online_resharding': 'useOnlineResharding'})
class CfnUpdatePolicy():
    def __init__(self, *, auto_scaling_replacing_update: typing.Optional["CfnAutoScalingReplacingUpdate"]=None, auto_scaling_rolling_update: typing.Optional["CfnAutoScalingRollingUpdate"]=None, auto_scaling_scheduled_action: typing.Optional["CfnAutoScalingScheduledAction"]=None, code_deploy_lambda_alias_update: typing.Optional["CfnCodeDeployLambdaAliasUpdate"]=None, enable_version_upgrade: typing.Optional[bool]=None, use_online_resharding: typing.Optional[bool]=None) -> None:
        """Use the UpdatePolicy attribute to specify how AWS CloudFormation handles updates to the AWS::AutoScaling::AutoScalingGroup resource.

        AWS CloudFormation invokes one of three update policies depending on the type of change you make or whether a
        scheduled action is associated with the Auto Scaling group.

        :param auto_scaling_replacing_update: Specifies whether an Auto Scaling group and the instances it contains are replaced during an update. During replacement, AWS CloudFormation retains the old group until it finishes creating the new one. If the update fails, AWS CloudFormation can roll back to the old Auto Scaling group and delete the new Auto Scaling group.
        :param auto_scaling_rolling_update: To specify how AWS CloudFormation handles rolling updates for an Auto Scaling group, use the AutoScalingRollingUpdate policy. Rolling updates enable you to specify whether AWS CloudFormation updates instances that are in an Auto Scaling group in batches or all at once.
        :param auto_scaling_scheduled_action: To specify how AWS CloudFormation handles updates for the MinSize, MaxSize, and DesiredCapacity properties when the AWS::AutoScaling::AutoScalingGroup resource has an associated scheduled action, use the AutoScalingScheduledAction policy.
        :param code_deploy_lambda_alias_update: To perform an AWS CodeDeploy deployment when the version changes on an AWS::Lambda::Alias resource, use the CodeDeployLambdaAliasUpdate update policy.
        :param enable_version_upgrade: To upgrade an Amazon ES domain to a new version of Elasticsearch rather than replacing the entire AWS::Elasticsearch::Domain resource, use the EnableVersionUpgrade update policy.
        :param use_online_resharding: To modify a replication group's shards by adding or removing shards, rather than replacing the entire AWS::ElastiCache::ReplicationGroup resource, use the UseOnlineResharding update policy.

        stability
        :stability: experimental
        """
        if isinstance(auto_scaling_replacing_update, dict): auto_scaling_replacing_update = CfnAutoScalingReplacingUpdate(**auto_scaling_replacing_update)
        if isinstance(auto_scaling_rolling_update, dict): auto_scaling_rolling_update = CfnAutoScalingRollingUpdate(**auto_scaling_rolling_update)
        if isinstance(auto_scaling_scheduled_action, dict): auto_scaling_scheduled_action = CfnAutoScalingScheduledAction(**auto_scaling_scheduled_action)
        if isinstance(code_deploy_lambda_alias_update, dict): code_deploy_lambda_alias_update = CfnCodeDeployLambdaAliasUpdate(**code_deploy_lambda_alias_update)
        self._values = {
        }
        if auto_scaling_replacing_update is not None: self._values["auto_scaling_replacing_update"] = auto_scaling_replacing_update
        if auto_scaling_rolling_update is not None: self._values["auto_scaling_rolling_update"] = auto_scaling_rolling_update
        if auto_scaling_scheduled_action is not None: self._values["auto_scaling_scheduled_action"] = auto_scaling_scheduled_action
        if code_deploy_lambda_alias_update is not None: self._values["code_deploy_lambda_alias_update"] = code_deploy_lambda_alias_update
        if enable_version_upgrade is not None: self._values["enable_version_upgrade"] = enable_version_upgrade
        if use_online_resharding is not None: self._values["use_online_resharding"] = use_online_resharding

    @builtins.property
    def auto_scaling_replacing_update(self) -> typing.Optional["CfnAutoScalingReplacingUpdate"]:
        """Specifies whether an Auto Scaling group and the instances it contains are replaced during an update.

        During replacement,
        AWS CloudFormation retains the old group until it finishes creating the new one. If the update fails, AWS CloudFormation
        can roll back to the old Auto Scaling group and delete the new Auto Scaling group.

        stability
        :stability: experimental
        """
        return self._values.get('auto_scaling_replacing_update')

    @builtins.property
    def auto_scaling_rolling_update(self) -> typing.Optional["CfnAutoScalingRollingUpdate"]:
        """To specify how AWS CloudFormation handles rolling updates for an Auto Scaling group, use the AutoScalingRollingUpdate policy.

        Rolling updates enable you to specify whether AWS CloudFormation updates instances that are in an Auto Scaling
        group in batches or all at once.

        stability
        :stability: experimental
        """
        return self._values.get('auto_scaling_rolling_update')

    @builtins.property
    def auto_scaling_scheduled_action(self) -> typing.Optional["CfnAutoScalingScheduledAction"]:
        """To specify how AWS CloudFormation handles updates for the MinSize, MaxSize, and DesiredCapacity properties when the AWS::AutoScaling::AutoScalingGroup resource has an associated scheduled action, use the AutoScalingScheduledAction policy.

        stability
        :stability: experimental
        """
        return self._values.get('auto_scaling_scheduled_action')

    @builtins.property
    def code_deploy_lambda_alias_update(self) -> typing.Optional["CfnCodeDeployLambdaAliasUpdate"]:
        """To perform an AWS CodeDeploy deployment when the version changes on an AWS::Lambda::Alias resource, use the CodeDeployLambdaAliasUpdate update policy.

        stability
        :stability: experimental
        """
        return self._values.get('code_deploy_lambda_alias_update')

    @builtins.property
    def enable_version_upgrade(self) -> typing.Optional[bool]:
        """To upgrade an Amazon ES domain to a new version of Elasticsearch rather than replacing the entire AWS::Elasticsearch::Domain resource, use the EnableVersionUpgrade update policy.

        stability
        :stability: experimental
        """
        return self._values.get('enable_version_upgrade')

    @builtins.property
    def use_online_resharding(self) -> typing.Optional[bool]:
        """To modify a replication group's shards by adding or removing shards, rather than replacing the entire AWS::ElastiCache::ReplicationGroup resource, use the UseOnlineResharding update policy.

        stability
        :stability: experimental
        """
        return self._values.get('use_online_resharding')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnUpdatePolicy(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.CfnWaitConditionProps", jsii_struct_bases=[], name_mapping={'count': 'count', 'handle': 'handle', 'timeout': 'timeout'})
class CfnWaitConditionProps():
    def __init__(self, *, count: typing.Optional[jsii.Number]=None, handle: typing.Optional[str]=None, timeout: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::CloudFormation::WaitCondition``.

        :param count: ``AWS::CloudFormation::WaitCondition.Count``.
        :param handle: ``AWS::CloudFormation::WaitCondition.Handle``.
        :param timeout: ``AWS::CloudFormation::WaitCondition.Timeout``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html
        """
        self._values = {
        }
        if count is not None: self._values["count"] = count
        if handle is not None: self._values["handle"] = handle
        if timeout is not None: self._values["timeout"] = timeout

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """``AWS::CloudFormation::WaitCondition.Count``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-count
        """
        return self._values.get('count')

    @builtins.property
    def handle(self) -> typing.Optional[str]:
        """``AWS::CloudFormation::WaitCondition.Handle``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-handle
        """
        return self._values.get('handle')

    @builtins.property
    def timeout(self) -> typing.Optional[str]:
        """``AWS::CloudFormation::WaitCondition.Timeout``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-timeout
        """
        return self._values.get('timeout')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnWaitConditionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ConstructNode(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.ConstructNode"):
    """Represents the construct node in the scope tree.

    stability
    :stability: experimental
    """
    def __init__(self, host: "Construct", scope: "IConstruct", id: str) -> None:
        """
        :param host: -
        :param scope: -
        :param id: -

        stability
        :stability: experimental
        """
        jsii.create(ConstructNode, self, [host, scope, id])

    @jsii.member(jsii_name="prepare")
    @builtins.classmethod
    def prepare(cls, node: "ConstructNode") -> None:
        """Invokes "prepare" on all constructs (depth-first, post-order) in the tree under ``node``.

        :param node: The root node.

        deprecated
        :deprecated: Use ``app.synth()`` instead

        stability
        :stability: deprecated
        """
        return jsii.sinvoke(cls, "prepare", [node])

    @jsii.member(jsii_name="synth")
    @builtins.classmethod
    def synth(cls, node: "ConstructNode", *, outdir: typing.Optional[str]=None, skip_validation: typing.Optional[bool]=None, runtime_info: typing.Optional[_RuntimeInfo_b6d338e9]=None) -> _CloudAssembly_32c4802d:
        """Synthesizes a CloudAssembly from a construct tree.

        :param node: The root of the construct tree.
        :param outdir: The output directory into which to synthesize the cloud assembly. Default: - creates a temporary directory
        :param skip_validation: Whether synthesis should skip the validation phase. Default: false
        :param runtime_info: Include the specified runtime information (module versions) in manifest. Default: - if this option is not specified, runtime info will not be included

        deprecated
        :deprecated: Use ``app.synth()`` or ``stage.synth()`` instead

        stability
        :stability: deprecated
        """
        options = SynthesisOptions(outdir=outdir, skip_validation=skip_validation, runtime_info=runtime_info)

        return jsii.sinvoke(cls, "synth", [node, options])

    @jsii.member(jsii_name="validate")
    @builtins.classmethod
    def validate(cls, node: "ConstructNode") -> typing.List["ValidationError"]:
        """Invokes "validate" on all constructs in the tree (depth-first, pre-order) and returns the list of all errors.

        An empty list indicates that there are no errors.

        :param node: The root node.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "validate", [node])

    @jsii.member(jsii_name="addDependency")
    def add_dependency(self, *dependencies: "IDependable") -> None:
        """Add an ordering dependency on another Construct.

        All constructs in the dependency's scope will be deployed before any
        construct in this construct's scope.

        :param dependencies: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addDependency", [*dependencies])

    @jsii.member(jsii_name="addError")
    def add_error(self, message: str) -> None:
        """Adds an { "error":  } metadata entry to this construct.

        The toolkit will fail synthesis when errors are reported.

        :param message: The error message.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addError", [message])

    @jsii.member(jsii_name="addInfo")
    def add_info(self, message: str) -> None:
        """Adds a { "info":  } metadata entry to this construct.

        The toolkit will display the info message when apps are synthesized.

        :param message: The info message.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addInfo", [message])

    @jsii.member(jsii_name="addMetadata")
    def add_metadata(self, type: str, data: typing.Any, from_function: typing.Any=None) -> None:
        """Adds a metadata entry to this construct.

        Entries are arbitrary values and will also include a stack trace to allow tracing back to
        the code location for when the entry was added. It can be used, for example, to include source
        mapping in CloudFormation templates to improve diagnostics.

        :param type: a string denoting the type of metadata.
        :param data: the value of the metadata (can be a Token). If null/undefined, metadata will not be added.
        :param from_function: a function under which to restrict the metadata entry's stack trace (defaults to this.addMetadata).

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addMetadata", [type, data, from_function])

    @jsii.member(jsii_name="addWarning")
    def add_warning(self, message: str) -> None:
        """Adds a { "warning":  } metadata entry to this construct.

        The toolkit will display the warning when an app is synthesized, or fail
        if run in --strict mode.

        :param message: The warning message.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addWarning", [message])

    @jsii.member(jsii_name="applyAspect")
    def apply_aspect(self, aspect: "IAspect") -> None:
        """Applies the aspect to this Constructs node.

        :param aspect: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "applyAspect", [aspect])

    @jsii.member(jsii_name="findAll")
    def find_all(self, order: typing.Optional["ConstructOrder"]=None) -> typing.List["IConstruct"]:
        """Return this construct and all of its children in the given order.

        :param order: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "findAll", [order])

    @jsii.member(jsii_name="findChild")
    def find_child(self, id: str) -> "IConstruct":
        """Return a direct child by id.

        Throws an error if the child is not found.

        :param id: Identifier of direct child.

        return
        :return: Child with the given id.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "findChild", [id])

    @jsii.member(jsii_name="setContext")
    def set_context(self, key: str, value: typing.Any) -> None:
        """This can be used to set contextual values.

        Context must be set before any children are added, since children may consult context info during construction.
        If the key already exists, it will be overridden.

        :param key: The context key.
        :param value: The context value.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "setContext", [key, value])

    @jsii.member(jsii_name="tryFindChild")
    def try_find_child(self, id: str) -> typing.Optional["IConstruct"]:
        """Return a direct child by id, or undefined.

        :param id: Identifier of direct child.

        return
        :return: the child if found, or undefined

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "tryFindChild", [id])

    @jsii.member(jsii_name="tryGetContext")
    def try_get_context(self, key: str) -> typing.Any:
        """Retrieves a value from tree context.

        Context is usually initialized at the root, but can be overridden at any point in the tree.

        :param key: The context key.

        return
        :return: The context value or ``undefined`` if there is no context value for thie key.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "tryGetContext", [key])

    @jsii.member(jsii_name="tryRemoveChild")
    def try_remove_child(self, child_name: str) -> bool:
        """Remove the child with the given name, if present.

        :param child_name: -

        return
        :return: Whether a child with the given name was deleted.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "tryRemoveChild", [child_name])

    @jsii.python.classproperty
    @jsii.member(jsii_name="PATH_SEP")
    def PATH_SEP(cls) -> str:
        """Separator used to delimit construct path components.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "PATH_SEP")

    @builtins.property
    @jsii.member(jsii_name="children")
    def children(self) -> typing.List["IConstruct"]:
        """All direct children of this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "children")

    @builtins.property
    @jsii.member(jsii_name="dependencies")
    def dependencies(self) -> typing.List["Dependency"]:
        """Return all dependencies registered on this node or any of its children.

        stability
        :stability: experimental
        """
        return jsii.get(self, "dependencies")

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> str:
        """The id of this construct within the current scope.

        This is a a scope-unique id. To obtain an app-unique id for this construct, use ``uniqueId``.

        stability
        :stability: experimental
        """
        return jsii.get(self, "id")

    @builtins.property
    @jsii.member(jsii_name="locked")
    def locked(self) -> bool:
        """Returns true if this construct or the scopes in which it is defined are locked.

        stability
        :stability: experimental
        """
        return jsii.get(self, "locked")

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.List[_MetadataEntry_206d90cd]:
        """An immutable array of metadata objects associated with this construct.

        This can be used, for example, to implement support for deprecation notices, source mapping, etc.

        stability
        :stability: experimental
        """
        return jsii.get(self, "metadata")

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> str:
        """The full, absolute path of this construct in the tree.

        Components are separated by '/'.

        stability
        :stability: experimental
        """
        return jsii.get(self, "path")

    @builtins.property
    @jsii.member(jsii_name="root")
    def root(self) -> "IConstruct":
        """
        return
        :return: The root of the construct tree.

        stability
        :stability: experimental
        """
        return jsii.get(self, "root")

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List["IConstruct"]:
        """All parent scopes of this construct.

        return
        :return:

        a list of parent scopes. The last element in the list will always
        be the current construct and the first element will be the root of the
        tree.

        stability
        :stability: experimental
        """
        return jsii.get(self, "scopes")

    @builtins.property
    @jsii.member(jsii_name="uniqueId")
    def unique_id(self) -> str:
        """A tree-global unique alphanumeric identifier for this construct.

        Includes all components of the tree.

        stability
        :stability: experimental
        """
        return jsii.get(self, "uniqueId")

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> typing.Optional["IConstruct"]:
        """Returns the scope in which this construct is defined.

        The value is ``undefined`` at the root of the construct scope tree.

        stability
        :stability: experimental
        """
        return jsii.get(self, "scope")

    @builtins.property
    @jsii.member(jsii_name="defaultChild")
    def default_child(self) -> typing.Optional["IConstruct"]:
        """Returns the child construct that has the id ``Default`` or ``Resource"``.

        This is usually the construct that provides the bulk of the underlying functionality.
        Useful for modifications of the underlying construct that are not available at the higher levels.
        Override the defaultChild property.

        This should only be used in the cases where the correct
        default child is not named 'Resource' or 'Default' as it
        should be.

        If you set this to undefined, the default behavior of finding
        the child named 'Resource' or 'Default' will be used.

        return
        :return: a construct or undefined if there is no default child

        stability
        :stability: experimental
        throws:
        :throws:: if there is more than one child
        """
        return jsii.get(self, "defaultChild")

    @default_child.setter
    def default_child(self, value: typing.Optional["IConstruct"]) -> None:
        jsii.set(self, "defaultChild", value)


@jsii.enum(jsii_type="monocdk-experiment.ConstructOrder")
class ConstructOrder(enum.Enum):
    """In what order to return constructs.

    stability
    :stability: experimental
    """
    PREORDER = "PREORDER"
    """Depth-first, pre-order.

    stability
    :stability: experimental
    """
    POSTORDER = "POSTORDER"
    """Depth-first, post-order (leaf nodes first).

    stability
    :stability: experimental
    """

class ContextProvider(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.ContextProvider"):
    """Base class for the model side of context providers.

    Instances of this class communicate with context provider plugins in the 'cdk
    toolkit' via context variables (input), outputting specialized queries for
    more context variables (output).

    ContextProvider needs access to a Construct to hook into the context mechanism.

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="getKey")
    @builtins.classmethod
    def get_key(cls, scope: "Construct", *, provider: str, props: typing.Optional[typing.Mapping[str, typing.Any]]=None) -> "GetContextKeyResult":
        """
        :param scope: -
        :param provider: The context provider to query.
        :param props: Provider-specific properties.

        return
        :return: the context key or undefined if a key cannot be rendered (due to tokens used in any of the props)

        stability
        :stability: experimental
        """
        options = GetContextKeyOptions(provider=provider, props=props)

        return jsii.sinvoke(cls, "getKey", [scope, options])

    @jsii.member(jsii_name="getValue")
    @builtins.classmethod
    def get_value(cls, scope: "Construct", *, dummy_value: typing.Any, provider: str, props: typing.Optional[typing.Mapping[str, typing.Any]]=None) -> "GetContextValueResult":
        """
        :param scope: -
        :param dummy_value: The value to return if the context value was not found and a missing context is reported. This should be a dummy value that should preferably fail during deployment since it represents an invalid state.
        :param provider: The context provider to query.
        :param props: Provider-specific properties.

        stability
        :stability: experimental
        """
        options = GetContextValueOptions(dummy_value=dummy_value, provider=provider, props=props)

        return jsii.sinvoke(cls, "getValue", [scope, options])


@jsii.data_type(jsii_type="monocdk-experiment.CopyOptions", jsii_struct_bases=[], name_mapping={'exclude': 'exclude', 'follow': 'follow'})
class CopyOptions():
    def __init__(self, *, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional["SymlinkFollowMode"]=None) -> None:
        """Obtains applied when copying directories into the staging location.

        :param exclude: Glob patterns to exclude from the copy. Default: - nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER

        stability
        :stability: experimental
        """
        self._values = {
        }
        if exclude is not None: self._values["exclude"] = exclude
        if follow is not None: self._values["follow"] = follow

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[str]]:
        """Glob patterns to exclude from the copy.

        default
        :default: - nothing is excluded

        stability
        :stability: experimental
        """
        return self._values.get('exclude')

    @builtins.property
    def follow(self) -> typing.Optional["SymlinkFollowMode"]:
        """A strategy for how to handle symlinks.

        default
        :default: SymlinkFollowMode.NEVER

        stability
        :stability: experimental
        """
        return self._values.get('follow')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CopyOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.CustomResourceProps", jsii_struct_bases=[], name_mapping={'service_token': 'serviceToken', 'pascal_case_properties': 'pascalCaseProperties', 'properties': 'properties', 'removal_policy': 'removalPolicy', 'resource_type': 'resourceType'})
class CustomResourceProps():
    def __init__(self, *, service_token: str, pascal_case_properties: typing.Optional[bool]=None, properties: typing.Optional[typing.Mapping[str, typing.Any]]=None, removal_policy: typing.Optional["RemovalPolicy"]=None, resource_type: typing.Optional[str]=None) -> None:
        """Properties to provide a Lambda-backed custom resource.

        :param service_token: The ARN of the provider which implements this custom resource type. You can implement a provider by listening to raw AWS CloudFormation events and specify the ARN of an SNS topic (``topic.topicArn``) or the ARN of an AWS Lambda function (``lambda.functionArn``) or use the CDK's custom `resource provider framework <https://docs.aws.amazon.com/cdk/api/latest/docs/custom-resources-readme.html>`_ which makes it easier to implement robust providers. Provider framework:: // use the provider framework from aws-cdk/custom-resources: const provider = new custom_resources.Provider({ onEventHandler: myOnEventLambda, isCompleteHandler: myIsCompleteLambda, // optional }); new CustomResource(this, 'MyResource', { serviceToken: provider.serviceToken }); AWS Lambda function:: // invoke an AWS Lambda function when a lifecycle event occurs: serviceToken: myFunction.functionArn SNS topic:: // publish lifecycle events to an SNS topic: serviceToken: myTopic.topicArn
        :param pascal_case_properties: Convert all property keys to pascal case. Default: false
        :param properties: Properties to pass to the Lambda. Default: - No properties.
        :param removal_policy: The policy to apply when this resource is removed from the application. Default: cdk.RemovalPolicy.Destroy
        :param resource_type: For custom resources, you can specify AWS::CloudFormation::CustomResource (the default) as the resource type, or you can specify your own resource type name. For example, you can use "Custom::MyCustomResourceTypeName". Custom resource type names must begin with "Custom::" and can include alphanumeric characters and the following characters: _@-. You can specify a custom resource type name up to a maximum length of 60 characters. You cannot change the type during an update. Using your own resource type names helps you quickly differentiate the types of custom resources in your stack. For example, if you had two custom resources that conduct two different ping tests, you could name their type as Custom::PingTester to make them easily identifiable as ping testers (instead of using AWS::CloudFormation::CustomResource). Default: - AWS::CloudFormation::CustomResource

        stability
        :stability: experimental
        """
        self._values = {
            'service_token': service_token,
        }
        if pascal_case_properties is not None: self._values["pascal_case_properties"] = pascal_case_properties
        if properties is not None: self._values["properties"] = properties
        if removal_policy is not None: self._values["removal_policy"] = removal_policy
        if resource_type is not None: self._values["resource_type"] = resource_type

    @builtins.property
    def service_token(self) -> str:
        """The ARN of the provider which implements this custom resource type.

        You can implement a provider by listening to raw AWS CloudFormation events
        and specify the ARN of an SNS topic (``topic.topicArn``) or the ARN of an AWS
        Lambda function (``lambda.functionArn``) or use the CDK's custom `resource
        provider framework <https://docs.aws.amazon.com/cdk/api/latest/docs/custom-resources-readme.html>`_ which makes it easier to implement robust providers.

        Provider framework::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           # use the provider framework from aws-cdk/custom-resources:
           provider = custom_resources.Provider(
               on_event_handler=my_on_event_lambda,
               is_complete_handler=my_is_complete_lambda
           )

           CustomResource(self, "MyResource",
               service_token=provider.service_token
           )

        AWS Lambda function::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           serviceToken: myFunction.functionArn

        SNS topic::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           serviceToken: myTopic.topicArn

        stability
        :stability: experimental
        """
        return self._values.get('service_token')

    @builtins.property
    def pascal_case_properties(self) -> typing.Optional[bool]:
        """Convert all property keys to pascal case.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('pascal_case_properties')

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Properties to pass to the Lambda.

        default
        :default: - No properties.

        stability
        :stability: experimental
        """
        return self._values.get('properties')

    @builtins.property
    def removal_policy(self) -> typing.Optional["RemovalPolicy"]:
        """The policy to apply when this resource is removed from the application.

        default
        :default: cdk.RemovalPolicy.Destroy

        stability
        :stability: experimental
        """
        return self._values.get('removal_policy')

    @builtins.property
    def resource_type(self) -> typing.Optional[str]:
        """For custom resources, you can specify AWS::CloudFormation::CustomResource (the default) as the resource type, or you can specify your own resource type name.

        For example, you can use "Custom::MyCustomResourceTypeName".

        Custom resource type names must begin with "Custom::" and can include
        alphanumeric characters and the following characters: _@-. You can specify
        a custom resource type name up to a maximum length of 60 characters. You
        cannot change the type during an update.

        Using your own resource type names helps you quickly differentiate the
        types of custom resources in your stack. For example, if you had two custom
        resources that conduct two different ping tests, you could name their type
        as Custom::PingTester to make them easily identifiable as ping testers
        (instead of using AWS::CloudFormation::CustomResource).

        default
        :default: - AWS::CloudFormation::CustomResource

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html#aws-cfn-resource-type-name
        stability
        :stability: experimental
        """
        return self._values.get('resource_type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CustomResourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.CustomResourceProviderProps", jsii_struct_bases=[], name_mapping={'code_directory': 'codeDirectory', 'runtime': 'runtime', 'memory_size': 'memorySize', 'policy_statements': 'policyStatements', 'timeout': 'timeout'})
class CustomResourceProviderProps():
    def __init__(self, *, code_directory: str, runtime: "CustomResourceProviderRuntime", memory_size: typing.Optional["Size"]=None, policy_statements: typing.Optional[typing.List[typing.Any]]=None, timeout: typing.Optional["Duration"]=None) -> None:
        """Initialization properties for ``CustomResourceProvider``.

        :param code_directory: A local file system directory with the provider's code. The code will be bundled into a zip asset and wired to the provider's AWS Lambda function.
        :param runtime: The AWS Lambda runtime and version to use for the provider.
        :param memory_size: The amount of memory that your function has access to. Increasing the function's memory also increases its CPU allocation. Default: Size.mebibytes(128)
        :param policy_statements: A set of IAM policy statements to include in the inline policy of the provider's lambda function. Default: - no additional inline policy
        :param timeout: AWS Lambda timeout for the provider. Default: Duration.minutes(15)

        stability
        :stability: experimental
        """
        self._values = {
            'code_directory': code_directory,
            'runtime': runtime,
        }
        if memory_size is not None: self._values["memory_size"] = memory_size
        if policy_statements is not None: self._values["policy_statements"] = policy_statements
        if timeout is not None: self._values["timeout"] = timeout

    @builtins.property
    def code_directory(self) -> str:
        """A local file system directory with the provider's code.

        The code will be
        bundled into a zip asset and wired to the provider's AWS Lambda function.

        stability
        :stability: experimental
        """
        return self._values.get('code_directory')

    @builtins.property
    def runtime(self) -> "CustomResourceProviderRuntime":
        """The AWS Lambda runtime and version to use for the provider.

        stability
        :stability: experimental
        """
        return self._values.get('runtime')

    @builtins.property
    def memory_size(self) -> typing.Optional["Size"]:
        """The amount of memory that your function has access to.

        Increasing the
        function's memory also increases its CPU allocation.

        default
        :default: Size.mebibytes(128)

        stability
        :stability: experimental
        """
        return self._values.get('memory_size')

    @builtins.property
    def policy_statements(self) -> typing.Optional[typing.List[typing.Any]]:
        """A set of IAM policy statements to include in the inline policy of the provider's lambda function.

        default
        :default: - no additional inline policy

        stability
        :stability: experimental

        Example::

            # Example automatically generated. See https://github.com/aws/jsii/issues/826
            policyStatements: [ { Effect: 'Allow', Action: 's3:PutObject*', Resource: '*' } ]
        """
        return self._values.get('policy_statements')

    @builtins.property
    def timeout(self) -> typing.Optional["Duration"]:
        """AWS Lambda timeout for the provider.

        default
        :default: Duration.minutes(15)

        stability
        :stability: experimental
        """
        return self._values.get('timeout')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CustomResourceProviderProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.CustomResourceProviderRuntime")
class CustomResourceProviderRuntime(enum.Enum):
    """The lambda runtime to use for the resource provider.

    This also indicates
    which language is used for the handler.

    stability
    :stability: experimental
    """
    NODEJS_12 = "NODEJS_12"
    """Node.js 12.x.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.DefaultStackSynthesizerProps", jsii_struct_bases=[], name_mapping={'cloud_formation_execution_role': 'cloudFormationExecutionRole', 'deploy_role_arn': 'deployRoleArn', 'file_asset_key_arn_export_name': 'fileAssetKeyArnExportName', 'file_asset_publishing_external_id': 'fileAssetPublishingExternalId', 'file_asset_publishing_role_arn': 'fileAssetPublishingRoleArn', 'file_assets_bucket_name': 'fileAssetsBucketName', 'image_asset_publishing_external_id': 'imageAssetPublishingExternalId', 'image_asset_publishing_role_arn': 'imageAssetPublishingRoleArn', 'image_assets_repository_name': 'imageAssetsRepositoryName', 'qualifier': 'qualifier'})
class DefaultStackSynthesizerProps():
    def __init__(self, *, cloud_formation_execution_role: typing.Optional[str]=None, deploy_role_arn: typing.Optional[str]=None, file_asset_key_arn_export_name: typing.Optional[str]=None, file_asset_publishing_external_id: typing.Optional[str]=None, file_asset_publishing_role_arn: typing.Optional[str]=None, file_assets_bucket_name: typing.Optional[str]=None, image_asset_publishing_external_id: typing.Optional[str]=None, image_asset_publishing_role_arn: typing.Optional[str]=None, image_assets_repository_name: typing.Optional[str]=None, qualifier: typing.Optional[str]=None) -> None:
        """Configuration properties for DefaultStackSynthesizer.

        :param cloud_formation_execution_role: The role CloudFormation will assume when deploying the Stack. You must supply this if you have given a non-standard name to the execution role. The placeholders ``${Qualifier}``, ``${AWS::AccountId}`` and ``${AWS::Region}`` will be replaced with the values of qualifier and the stack's account and region, respectively. Default: DefaultStackSynthesizer.DEFAULT_CLOUDFORMATION_ROLE_ARN
        :param deploy_role_arn: The role to assume to initiate a deployment in this environment. You must supply this if you have given a non-standard name to the publishing role. The placeholders ``${Qualifier}``, ``${AWS::AccountId}`` and ``${AWS::Region}`` will be replaced with the values of qualifier and the stack's account and region, respectively. Default: DefaultStackSynthesizer.DEFAULT_DEPLOY_ROLE_ARN
        :param file_asset_key_arn_export_name: Name of the CloudFormation Export with the asset key name. You must supply this if you have given a non-standard name to the KMS key export The placeholders ``${Qualifier}``, ``${AWS::AccountId}`` and ``${AWS::Region}`` will be replaced with the values of qualifier and the stack's account and region, respectively. Default: DefaultStackSynthesizer.DEFAULT_FILE_ASSET_KEY_ARN_EXPORT_NAME
        :param file_asset_publishing_external_id: External ID to use when assuming role for file asset publishing. Default: - No external ID
        :param file_asset_publishing_role_arn: The role to use to publish file assets to the S3 bucket in this environment. You must supply this if you have given a non-standard name to the publishing role. The placeholders ``${Qualifier}``, ``${AWS::AccountId}`` and ``${AWS::Region}`` will be replaced with the values of qualifier and the stack's account and region, respectively. Default: DefaultStackSynthesizer.DEFAULT_FILE_ASSET_PUBLISHING_ROLE_ARN
        :param file_assets_bucket_name: Name of the S3 bucket to hold file assets. You must supply this if you have given a non-standard name to the staging bucket. The placeholders ``${Qualifier}``, ``${AWS::AccountId}`` and ``${AWS::Region}`` will be replaced with the values of qualifier and the stack's account and region, respectively. Default: DefaultStackSynthesizer.DEFAULT_FILE_ASSETS_BUCKET_NAME
        :param image_asset_publishing_external_id: External ID to use when assuming role for image asset publishing. Default: - No external ID
        :param image_asset_publishing_role_arn: The role to use to publish image assets to the ECR repository in this environment. You must supply this if you have given a non-standard name to the publishing role. The placeholders ``${Qualifier}``, ``${AWS::AccountId}`` and ``${AWS::Region}`` will be replaced with the values of qualifier and the stack's account and region, respectively. Default: DefaultStackSynthesizer.DEFAULT_IMAGE_ASSET_PUBLISHING_ROLE_ARN
        :param image_assets_repository_name: Name of the ECR repository to hold Docker Image assets. You must supply this if you have given a non-standard name to the ECR repository. The placeholders ``${Qualifier}``, ``${AWS::AccountId}`` and ``${AWS::Region}`` will be replaced with the values of qualifier and the stack's account and region, respectively. Default: DefaultStackSynthesizer.DEFAULT_IMAGE_ASSETS_REPOSITORY_NAME
        :param qualifier: Qualifier to disambiguate multiple environments in the same account. You can use this and leave the other naming properties empty if you have deployed the bootstrap environment with standard names but only differnet qualifiers. Default: - Value of context key '

        stability
        :stability: experimental
        """
        self._values = {
        }
        if cloud_formation_execution_role is not None: self._values["cloud_formation_execution_role"] = cloud_formation_execution_role
        if deploy_role_arn is not None: self._values["deploy_role_arn"] = deploy_role_arn
        if file_asset_key_arn_export_name is not None: self._values["file_asset_key_arn_export_name"] = file_asset_key_arn_export_name
        if file_asset_publishing_external_id is not None: self._values["file_asset_publishing_external_id"] = file_asset_publishing_external_id
        if file_asset_publishing_role_arn is not None: self._values["file_asset_publishing_role_arn"] = file_asset_publishing_role_arn
        if file_assets_bucket_name is not None: self._values["file_assets_bucket_name"] = file_assets_bucket_name
        if image_asset_publishing_external_id is not None: self._values["image_asset_publishing_external_id"] = image_asset_publishing_external_id
        if image_asset_publishing_role_arn is not None: self._values["image_asset_publishing_role_arn"] = image_asset_publishing_role_arn
        if image_assets_repository_name is not None: self._values["image_assets_repository_name"] = image_assets_repository_name
        if qualifier is not None: self._values["qualifier"] = qualifier

    @builtins.property
    def cloud_formation_execution_role(self) -> typing.Optional[str]:
        """The role CloudFormation will assume when deploying the Stack.

        You must supply this if you have given a non-standard name to the execution role.

        The placeholders ``${Qualifier}``, ``${AWS::AccountId}`` and ``${AWS::Region}`` will
        be replaced with the values of qualifier and the stack's account and region,
        respectively.

        default
        :default: DefaultStackSynthesizer.DEFAULT_CLOUDFORMATION_ROLE_ARN

        stability
        :stability: experimental
        """
        return self._values.get('cloud_formation_execution_role')

    @builtins.property
    def deploy_role_arn(self) -> typing.Optional[str]:
        """The role to assume to initiate a deployment in this environment.

        You must supply this if you have given a non-standard name to the publishing role.

        The placeholders ``${Qualifier}``, ``${AWS::AccountId}`` and ``${AWS::Region}`` will
        be replaced with the values of qualifier and the stack's account and region,
        respectively.

        default
        :default: DefaultStackSynthesizer.DEFAULT_DEPLOY_ROLE_ARN

        stability
        :stability: experimental
        """
        return self._values.get('deploy_role_arn')

    @builtins.property
    def file_asset_key_arn_export_name(self) -> typing.Optional[str]:
        """Name of the CloudFormation Export with the asset key name.

        You must supply this if you have given a non-standard name to the KMS key export

        The placeholders ``${Qualifier}``, ``${AWS::AccountId}`` and ``${AWS::Region}`` will
        be replaced with the values of qualifier and the stack's account and region,
        respectively.

        default
        :default: DefaultStackSynthesizer.DEFAULT_FILE_ASSET_KEY_ARN_EXPORT_NAME

        stability
        :stability: experimental
        """
        return self._values.get('file_asset_key_arn_export_name')

    @builtins.property
    def file_asset_publishing_external_id(self) -> typing.Optional[str]:
        """External ID to use when assuming role for file asset publishing.

        default
        :default: - No external ID

        stability
        :stability: experimental
        """
        return self._values.get('file_asset_publishing_external_id')

    @builtins.property
    def file_asset_publishing_role_arn(self) -> typing.Optional[str]:
        """The role to use to publish file assets to the S3 bucket in this environment.

        You must supply this if you have given a non-standard name to the publishing role.

        The placeholders ``${Qualifier}``, ``${AWS::AccountId}`` and ``${AWS::Region}`` will
        be replaced with the values of qualifier and the stack's account and region,
        respectively.

        default
        :default: DefaultStackSynthesizer.DEFAULT_FILE_ASSET_PUBLISHING_ROLE_ARN

        stability
        :stability: experimental
        """
        return self._values.get('file_asset_publishing_role_arn')

    @builtins.property
    def file_assets_bucket_name(self) -> typing.Optional[str]:
        """Name of the S3 bucket to hold file assets.

        You must supply this if you have given a non-standard name to the staging bucket.

        The placeholders ``${Qualifier}``, ``${AWS::AccountId}`` and ``${AWS::Region}`` will
        be replaced with the values of qualifier and the stack's account and region,
        respectively.

        default
        :default: DefaultStackSynthesizer.DEFAULT_FILE_ASSETS_BUCKET_NAME

        stability
        :stability: experimental
        """
        return self._values.get('file_assets_bucket_name')

    @builtins.property
    def image_asset_publishing_external_id(self) -> typing.Optional[str]:
        """External ID to use when assuming role for image asset publishing.

        default
        :default: - No external ID

        stability
        :stability: experimental
        """
        return self._values.get('image_asset_publishing_external_id')

    @builtins.property
    def image_asset_publishing_role_arn(self) -> typing.Optional[str]:
        """The role to use to publish image assets to the ECR repository in this environment.

        You must supply this if you have given a non-standard name to the publishing role.

        The placeholders ``${Qualifier}``, ``${AWS::AccountId}`` and ``${AWS::Region}`` will
        be replaced with the values of qualifier and the stack's account and region,
        respectively.

        default
        :default: DefaultStackSynthesizer.DEFAULT_IMAGE_ASSET_PUBLISHING_ROLE_ARN

        stability
        :stability: experimental
        """
        return self._values.get('image_asset_publishing_role_arn')

    @builtins.property
    def image_assets_repository_name(self) -> typing.Optional[str]:
        """Name of the ECR repository to hold Docker Image assets.

        You must supply this if you have given a non-standard name to the ECR repository.

        The placeholders ``${Qualifier}``, ``${AWS::AccountId}`` and ``${AWS::Region}`` will
        be replaced with the values of qualifier and the stack's account and region,
        respectively.

        default
        :default: DefaultStackSynthesizer.DEFAULT_IMAGE_ASSETS_REPOSITORY_NAME

        stability
        :stability: experimental
        """
        return self._values.get('image_assets_repository_name')

    @builtins.property
    def qualifier(self) -> typing.Optional[str]:
        """Qualifier to disambiguate multiple environments in the same account.

        You can use this and leave the other naming properties empty if you have deployed
        the bootstrap environment with standard names but only differnet qualifiers.

        default
        :default: - Value of context key '

        stability
        :stability: experimental
        aws-cdk:
        :aws-cdk:: /core:bootstrapQualifier' if set, otherwise ``DefaultStackSynthesizer.DEFAULT_QUALIFIER``
        """
        return self._values.get('qualifier')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DefaultStackSynthesizerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class DependableTrait(metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.DependableTrait"):
    """Trait for IDependable.

    Traits are interfaces that are privately implemented by objects. Instead of
    showing up in the public interface of a class, they need to be queried
    explicitly. This is used to implement certain framework features that are
    not intended to be used by Construct consumers, and so should be hidden
    from accidental use.

    stability
    :stability: experimental

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        # Usage
        roots = DependableTrait.get(construct).dependency_roots
        
        # Definition
        DependableTrait.implement(construct, get dependencyRoots() { return []; }
        )
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _DependableTraitProxy

    def __init__(self) -> None:
        jsii.create(DependableTrait, self, [])

    @jsii.member(jsii_name="get")
    @builtins.classmethod
    def get(cls, instance: "IDependable") -> "DependableTrait":
        """Return the matching DependableTrait for the given class instance.

        :param instance: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "get", [instance])

    @jsii.member(jsii_name="implement")
    @builtins.classmethod
    def implement(cls, instance: "IDependable", trait: "DependableTrait") -> None:
        """Register ``instance`` to have the given DependableTrait.

        Should be called in the class constructor.

        :param instance: -
        :param trait: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "implement", [instance, trait])

    @builtins.property
    @jsii.member(jsii_name="dependencyRoots")
    @abc.abstractmethod
    def dependency_roots(self) -> typing.List["IConstruct"]:
        """The set of constructs that form the root of this dependable.

        All resources under all returned constructs are included in the ordering
        dependency.

        stability
        :stability: experimental
        """
        ...


class _DependableTraitProxy(DependableTrait):
    @builtins.property
    @jsii.member(jsii_name="dependencyRoots")
    def dependency_roots(self) -> typing.List["IConstruct"]:
        """The set of constructs that form the root of this dependable.

        All resources under all returned constructs are included in the ordering
        dependency.

        stability
        :stability: experimental
        """
        return jsii.get(self, "dependencyRoots")


@jsii.data_type(jsii_type="monocdk-experiment.Dependency", jsii_struct_bases=[], name_mapping={'source': 'source', 'target': 'target'})
class Dependency():
    def __init__(self, *, source: "IConstruct", target: "IConstruct") -> None:
        """A single dependency.

        :param source: Source the dependency.
        :param target: Target of the dependency.

        stability
        :stability: experimental
        """
        self._values = {
            'source': source,
            'target': target,
        }

    @builtins.property
    def source(self) -> "IConstruct":
        """Source the dependency.

        stability
        :stability: experimental
        """
        return self._values.get('source')

    @builtins.property
    def target(self) -> "IConstruct":
        """Target of the dependency.

        stability
        :stability: experimental
        """
        return self._values.get('target')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Dependency(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.DockerBuildOptions", jsii_struct_bases=[], name_mapping={'build_args': 'buildArgs'})
class DockerBuildOptions():
    def __init__(self, *, build_args: typing.Optional[typing.Mapping[str, str]]=None) -> None:
        """Docker build options.

        :param build_args: Build args. Default: - no build args

        stability
        :stability: experimental
        """
        self._values = {
        }
        if build_args is not None: self._values["build_args"] = build_args

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Build args.

        default
        :default: - no build args

        stability
        :stability: experimental
        """
        return self._values.get('build_args')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DockerBuildOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.DockerImageAssetLocation", jsii_struct_bases=[], name_mapping={'image_uri': 'imageUri', 'repository_name': 'repositoryName'})
class DockerImageAssetLocation():
    def __init__(self, *, image_uri: str, repository_name: str) -> None:
        """The location of the published docker image.

        This is where the image can be
        consumed at runtime.

        :param image_uri: The URI of the image in Amazon ECR.
        :param repository_name: The name of the ECR repository.

        stability
        :stability: experimental
        """
        self._values = {
            'image_uri': image_uri,
            'repository_name': repository_name,
        }

    @builtins.property
    def image_uri(self) -> str:
        """The URI of the image in Amazon ECR.

        stability
        :stability: experimental
        """
        return self._values.get('image_uri')

    @builtins.property
    def repository_name(self) -> str:
        """The name of the ECR repository.

        stability
        :stability: experimental
        """
        return self._values.get('repository_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DockerImageAssetLocation(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.DockerImageAssetSource", jsii_struct_bases=[], name_mapping={'directory_name': 'directoryName', 'source_hash': 'sourceHash', 'docker_build_args': 'dockerBuildArgs', 'docker_build_target': 'dockerBuildTarget', 'docker_file': 'dockerFile', 'repository_name': 'repositoryName'})
class DockerImageAssetSource():
    def __init__(self, *, directory_name: str, source_hash: str, docker_build_args: typing.Optional[typing.Mapping[str, str]]=None, docker_build_target: typing.Optional[str]=None, docker_file: typing.Optional[str]=None, repository_name: typing.Optional[str]=None) -> None:
        """
        :param directory_name: The directory where the Dockerfile is stored, must be relative to the cloud assembly root.
        :param source_hash: The hash of the contents of the docker build context. This hash is used throughout the system to identify this image and avoid duplicate work in case the source did not change. NOTE: this means that if you wish to update your docker image, you must make a modification to the source (e.g. add some metadata to your Dockerfile).
        :param docker_build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param docker_build_target: Docker target to build to. Default: - no target
        :param docker_file: Path to the Dockerfile (relative to the directory). Default: - no file
        :param repository_name: ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - automatically derived from the asset's ID.

        stability
        :stability: experimental
        """
        self._values = {
            'directory_name': directory_name,
            'source_hash': source_hash,
        }
        if docker_build_args is not None: self._values["docker_build_args"] = docker_build_args
        if docker_build_target is not None: self._values["docker_build_target"] = docker_build_target
        if docker_file is not None: self._values["docker_file"] = docker_file
        if repository_name is not None: self._values["repository_name"] = repository_name

    @builtins.property
    def directory_name(self) -> str:
        """The directory where the Dockerfile is stored, must be relative to the cloud assembly root.

        stability
        :stability: experimental
        """
        return self._values.get('directory_name')

    @builtins.property
    def source_hash(self) -> str:
        """The hash of the contents of the docker build context.

        This hash is used
        throughout the system to identify this image and avoid duplicate work
        in case the source did not change.

        NOTE: this means that if you wish to update your docker image, you
        must make a modification to the source (e.g. add some metadata to your Dockerfile).

        stability
        :stability: experimental
        """
        return self._values.get('source_hash')

    @builtins.property
    def docker_build_args(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Build args to pass to the ``docker build`` command.

        Since Docker build arguments are resolved before deployment, keys and
        values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or
        ``queue.queueUrl``).

        default
        :default: - no build args are passed

        stability
        :stability: experimental
        """
        return self._values.get('docker_build_args')

    @builtins.property
    def docker_build_target(self) -> typing.Optional[str]:
        """Docker target to build to.

        default
        :default: - no target

        stability
        :stability: experimental
        """
        return self._values.get('docker_build_target')

    @builtins.property
    def docker_file(self) -> typing.Optional[str]:
        """Path to the Dockerfile (relative to the directory).

        default
        :default: - no file

        stability
        :stability: experimental
        """
        return self._values.get('docker_file')

    @builtins.property
    def repository_name(self) -> typing.Optional[str]:
        """ECR repository name.

        Specify this property if you need to statically address the image, e.g.
        from a Kubernetes Pod. Note, this is only the repository name, without the
        registry and the tag parts.

        default
        :default: - automatically derived from the asset's ID.

        deprecated
        :deprecated: repository name should be specified at the environment-level and not at the image level

        stability
        :stability: deprecated
        """
        return self._values.get('repository_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DockerImageAssetSource(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.DockerVolume", jsii_struct_bases=[], name_mapping={'container_path': 'containerPath', 'host_path': 'hostPath'})
class DockerVolume():
    def __init__(self, *, container_path: str, host_path: str) -> None:
        """A Docker volume.

        :param container_path: The path where the file or directory is mounted in the container.
        :param host_path: The path to the file or directory on the host machine.

        stability
        :stability: experimental
        """
        self._values = {
            'container_path': container_path,
            'host_path': host_path,
        }

    @builtins.property
    def container_path(self) -> str:
        """The path where the file or directory is mounted in the container.

        stability
        :stability: experimental
        """
        return self._values.get('container_path')

    @builtins.property
    def host_path(self) -> str:
        """The path to the file or directory on the host machine.

        stability
        :stability: experimental
        """
        return self._values.get('host_path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DockerVolume(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Duration(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.Duration"):
    """Represents a length of time.

    The amount can be specified either as a literal value (e.g: ``10``) which
    cannot be negative, or as an unresolved number token.

    When the amount is passed as a token, unit conversion is not possible.

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="days")
    @builtins.classmethod
    def days(cls, amount: jsii.Number) -> "Duration":
        """Create a Duration representing an amount of days.

        :param amount: the amount of Days the ``Duration`` will represent.

        return
        :return: a new ``Duration`` representing ``amount`` Days.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "days", [amount])

    @jsii.member(jsii_name="hours")
    @builtins.classmethod
    def hours(cls, amount: jsii.Number) -> "Duration":
        """Create a Duration representing an amount of hours.

        :param amount: the amount of Hours the ``Duration`` will represent.

        return
        :return: a new ``Duration`` representing ``amount`` Hours.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "hours", [amount])

    @jsii.member(jsii_name="millis")
    @builtins.classmethod
    def millis(cls, amount: jsii.Number) -> "Duration":
        """Create a Duration representing an amount of milliseconds.

        :param amount: the amount of Milliseconds the ``Duration`` will represent.

        return
        :return: a new ``Duration`` representing ``amount`` ms.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "millis", [amount])

    @jsii.member(jsii_name="minutes")
    @builtins.classmethod
    def minutes(cls, amount: jsii.Number) -> "Duration":
        """Create a Duration representing an amount of minutes.

        :param amount: the amount of Minutes the ``Duration`` will represent.

        return
        :return: a new ``Duration`` representing ``amount`` Minutes.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "minutes", [amount])

    @jsii.member(jsii_name="parse")
    @builtins.classmethod
    def parse(cls, duration: str) -> "Duration":
        """Parse a period formatted according to the ISO 8601 standard.

        :param duration: an ISO-formtted duration to be parsed.

        return
        :return: the parsed ``Duration``.

        see
        :see: https://www.iso.org/fr/standard/70907.html
        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "parse", [duration])

    @jsii.member(jsii_name="seconds")
    @builtins.classmethod
    def seconds(cls, amount: jsii.Number) -> "Duration":
        """Create a Duration representing an amount of seconds.

        :param amount: the amount of Seconds the ``Duration`` will represent.

        return
        :return: a new ``Duration`` representing ``amount`` Seconds.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "seconds", [amount])

    @jsii.member(jsii_name="toDays")
    def to_days(self, *, integral: typing.Optional[bool]=None) -> jsii.Number:
        """Return the total number of days in this Duration.

        :param integral: If ``true``, conversions into a larger time unit (e.g. ``Seconds`` to ``Minutes``) will fail if the result is not an integer. Default: true

        return
        :return: the value of this ``Duration`` expressed in Days.

        stability
        :stability: experimental
        """
        opts = TimeConversionOptions(integral=integral)

        return jsii.invoke(self, "toDays", [opts])

    @jsii.member(jsii_name="toHours")
    def to_hours(self, *, integral: typing.Optional[bool]=None) -> jsii.Number:
        """Return the total number of hours in this Duration.

        :param integral: If ``true``, conversions into a larger time unit (e.g. ``Seconds`` to ``Minutes``) will fail if the result is not an integer. Default: true

        return
        :return: the value of this ``Duration`` expressed in Hours.

        stability
        :stability: experimental
        """
        opts = TimeConversionOptions(integral=integral)

        return jsii.invoke(self, "toHours", [opts])

    @jsii.member(jsii_name="toHumanString")
    def to_human_string(self) -> str:
        """Turn this duration into a human-readable string.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toHumanString", [])

    @jsii.member(jsii_name="toIsoString")
    def to_iso_string(self) -> str:
        """Return an ISO 8601 representation of this period.

        return
        :return: a string starting with 'PT' describing the period

        see
        :see: https://www.iso.org/fr/standard/70907.html
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toIsoString", [])

    @jsii.member(jsii_name="toISOString")
    def to_iso_string(self) -> str:
        """Return an ISO 8601 representation of this period.

        return
        :return: a string starting with 'PT' describing the period

        deprecated
        :deprecated: Use ``toIsoString()`` instead.

        see
        :see: https://www.iso.org/fr/standard/70907.html
        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "toISOString", [])

    @jsii.member(jsii_name="toMilliseconds")
    def to_milliseconds(self, *, integral: typing.Optional[bool]=None) -> jsii.Number:
        """Return the total number of milliseconds in this Duration.

        :param integral: If ``true``, conversions into a larger time unit (e.g. ``Seconds`` to ``Minutes``) will fail if the result is not an integer. Default: true

        return
        :return: the value of this ``Duration`` expressed in Milliseconds.

        stability
        :stability: experimental
        """
        opts = TimeConversionOptions(integral=integral)

        return jsii.invoke(self, "toMilliseconds", [opts])

    @jsii.member(jsii_name="toMinutes")
    def to_minutes(self, *, integral: typing.Optional[bool]=None) -> jsii.Number:
        """Return the total number of minutes in this Duration.

        :param integral: If ``true``, conversions into a larger time unit (e.g. ``Seconds`` to ``Minutes``) will fail if the result is not an integer. Default: true

        return
        :return: the value of this ``Duration`` expressed in Minutes.

        stability
        :stability: experimental
        """
        opts = TimeConversionOptions(integral=integral)

        return jsii.invoke(self, "toMinutes", [opts])

    @jsii.member(jsii_name="toSeconds")
    def to_seconds(self, *, integral: typing.Optional[bool]=None) -> jsii.Number:
        """Return the total number of seconds in this Duration.

        :param integral: If ``true``, conversions into a larger time unit (e.g. ``Seconds`` to ``Minutes``) will fail if the result is not an integer. Default: true

        return
        :return: the value of this ``Duration`` expressed in Seconds.

        stability
        :stability: experimental
        """
        opts = TimeConversionOptions(integral=integral)

        return jsii.invoke(self, "toSeconds", [opts])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of this ``Duration`` that is also a Token that cannot be successfully resolved.

        This
        protects users against inadvertently stringifying a ``Duration`` object, when they should have called one of the
        ``to*`` methods instead.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toString", [])


@jsii.data_type(jsii_type="monocdk-experiment.EncodingOptions", jsii_struct_bases=[], name_mapping={'display_hint': 'displayHint'})
class EncodingOptions():
    def __init__(self, *, display_hint: typing.Optional[str]=None) -> None:
        """Properties to string encodings.

        :param display_hint: A hint for the Token's purpose when stringifying it.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if display_hint is not None: self._values["display_hint"] = display_hint

    @builtins.property
    def display_hint(self) -> typing.Optional[str]:
        """A hint for the Token's purpose when stringifying it.

        stability
        :stability: experimental
        """
        return self._values.get('display_hint')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EncodingOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.Environment", jsii_struct_bases=[], name_mapping={'account': 'account', 'region': 'region'})
class Environment():
    def __init__(self, *, account: typing.Optional[str]=None, region: typing.Optional[str]=None) -> None:
        """The deployment environment for a stack.

        :param account: The AWS account ID for this environment. This can be either a concrete value such as ``585191031104`` or ``Aws.accountId`` which indicates that account ID will only be determined during deployment (it will resolve to the CloudFormation intrinsic ``{"Ref":"AWS::AccountId"}``). Note that certain features, such as cross-stack references and environmental context providers require concerete region information and will cause this stack to emit synthesis errors. Default: Aws.accountId which means that the stack will be account-agnostic.
        :param region: The AWS region for this environment. This can be either a concrete value such as ``eu-west-2`` or ``Aws.region`` which indicates that account ID will only be determined during deployment (it will resolve to the CloudFormation intrinsic ``{"Ref":"AWS::Region"}``). Note that certain features, such as cross-stack references and environmental context providers require concerete region information and will cause this stack to emit synthesis errors. Default: Aws.region which means that the stack will be region-agnostic.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if account is not None: self._values["account"] = account
        if region is not None: self._values["region"] = region

    @builtins.property
    def account(self) -> typing.Optional[str]:
        """The AWS account ID for this environment.

        This can be either a concrete value such as ``585191031104`` or ``Aws.accountId`` which
        indicates that account ID will only be determined during deployment (it
        will resolve to the CloudFormation intrinsic ``{"Ref":"AWS::AccountId"}``).
        Note that certain features, such as cross-stack references and
        environmental context providers require concerete region information and
        will cause this stack to emit synthesis errors.

        default
        :default: Aws.accountId which means that the stack will be account-agnostic.

        stability
        :stability: experimental
        """
        return self._values.get('account')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """The AWS region for this environment.

        This can be either a concrete value such as ``eu-west-2`` or ``Aws.region``
        which indicates that account ID will only be determined during deployment
        (it will resolve to the CloudFormation intrinsic ``{"Ref":"AWS::Region"}``).
        Note that certain features, such as cross-stack references and
        environmental context providers require concerete region information and
        will cause this stack to emit synthesis errors.

        default
        :default: Aws.region which means that the stack will be region-agnostic.

        stability
        :stability: experimental
        """
        return self._values.get('region')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Environment(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.FileAssetLocation", jsii_struct_bases=[], name_mapping={'bucket_name': 'bucketName', 'http_url': 'httpUrl', 'object_key': 'objectKey', 's3_object_url': 's3ObjectUrl', 's3_url': 's3Url', 'kms_key_arn': 'kmsKeyArn'})
class FileAssetLocation():
    def __init__(self, *, bucket_name: str, http_url: str, object_key: str, s3_object_url: str, s3_url: str, kms_key_arn: typing.Optional[str]=None) -> None:
        """The location of the published file asset.

        This is where the asset
        can be consumed at runtime.

        :param bucket_name: The name of the Amazon S3 bucket.
        :param http_url: The HTTP URL of this asset on Amazon S3.
        :param object_key: The Amazon S3 object key.
        :param s3_object_url: The S3 URL of this asset on Amazon S3.
        :param s3_url: The HTTP URL of this asset on Amazon S3.
        :param kms_key_arn: The ARN of the KMS key used to encrypt the file asset bucket, if any. If so, the consuming role should be given "kms:Decrypt" permissions in its identity policy. It's the responsibility of they key's creator to make sure that all consumers that the key's key policy is configured such that the key can be used by all consumers that need it. The default bootstrap stack provisioned by the CDK CLI ensures this, and can be used as an example for how to configure the key properly. Default: - Asset bucket is not encrypted

        stability
        :stability: experimental
        """
        self._values = {
            'bucket_name': bucket_name,
            'http_url': http_url,
            'object_key': object_key,
            's3_object_url': s3_object_url,
            's3_url': s3_url,
        }
        if kms_key_arn is not None: self._values["kms_key_arn"] = kms_key_arn

    @builtins.property
    def bucket_name(self) -> str:
        """The name of the Amazon S3 bucket.

        stability
        :stability: experimental
        """
        return self._values.get('bucket_name')

    @builtins.property
    def http_url(self) -> str:
        """The HTTP URL of this asset on Amazon S3.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            https:
        """
        return self._values.get('http_url')

    @builtins.property
    def object_key(self) -> str:
        """The Amazon S3 object key.

        stability
        :stability: experimental
        """
        return self._values.get('object_key')

    @builtins.property
    def s3_object_url(self) -> str:
        """The S3 URL of this asset on Amazon S3.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            s3:
        """
        return self._values.get('s3_object_url')

    @builtins.property
    def s3_url(self) -> str:
        """The HTTP URL of this asset on Amazon S3.

        deprecated
        :deprecated: use ``httpUrl``

        stability
        :stability: deprecated
        """
        return self._values.get('s3_url')

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[str]:
        """The ARN of the KMS key used to encrypt the file asset bucket, if any.

        If so, the consuming role should be given "kms:Decrypt" permissions in its
        identity policy.

        It's the responsibility of they key's creator to make sure that all
        consumers that the key's key policy is configured such that the key can be used
        by all consumers that need it.

        The default bootstrap stack provisioned by the CDK CLI ensures this, and
        can be used as an example for how to configure the key properly.

        default
        :default: - Asset bucket is not encrypted

        stability
        :stability: experimental
        """
        return self._values.get('kms_key_arn')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FileAssetLocation(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.FileAssetPackaging")
class FileAssetPackaging(enum.Enum):
    """Packaging modes for file assets.

    stability
    :stability: experimental
    """
    ZIP_DIRECTORY = "ZIP_DIRECTORY"
    """The asset source path points to a directory, which should be archived using zip and and then uploaded to Amazon S3.

    stability
    :stability: experimental
    """
    FILE = "FILE"
    """The asset source path points to a single file, which should be uploaded to Amazon S3.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.FileAssetSource", jsii_struct_bases=[], name_mapping={'file_name': 'fileName', 'packaging': 'packaging', 'source_hash': 'sourceHash'})
class FileAssetSource():
    def __init__(self, *, file_name: str, packaging: "FileAssetPackaging", source_hash: str) -> None:
        """Represents the source for a file asset.

        :param file_name: The path, relative to the root of the cloud assembly, in which this asset source resides. This can be a path to a file or a directory, dependning on the packaging type.
        :param packaging: Which type of packaging to perform.
        :param source_hash: A hash on the content source. This hash is used to uniquely identify this asset throughout the system. If this value doesn't change, the asset will not be rebuilt or republished.

        stability
        :stability: experimental
        """
        self._values = {
            'file_name': file_name,
            'packaging': packaging,
            'source_hash': source_hash,
        }

    @builtins.property
    def file_name(self) -> str:
        """The path, relative to the root of the cloud assembly, in which this asset source resides.

        This can be a path to a file or a directory, dependning on the
        packaging type.

        stability
        :stability: experimental
        """
        return self._values.get('file_name')

    @builtins.property
    def packaging(self) -> "FileAssetPackaging":
        """Which type of packaging to perform.

        stability
        :stability: experimental
        """
        return self._values.get('packaging')

    @builtins.property
    def source_hash(self) -> str:
        """A hash on the content source.

        This hash is used to uniquely identify this
        asset throughout the system. If this value doesn't change, the asset will
        not be rebuilt or republished.

        stability
        :stability: experimental
        """
        return self._values.get('source_hash')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FileAssetSource(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class FileSystem(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.FileSystem"):
    """File system utilities.

    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        jsii.create(FileSystem, self, [])

    @jsii.member(jsii_name="copyDirectory")
    @builtins.classmethod
    def copy_directory(cls, src_dir: str, dest_dir: str, options: typing.Optional["CopyOptions"]=None, root_dir: typing.Optional[str]=None) -> None:
        """Copies an entire directory structure.

        :param src_dir: Source directory.
        :param dest_dir: Destination directory.
        :param options: options.
        :param root_dir: Root directory to calculate exclusions from.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "copyDirectory", [src_dir, dest_dir, options, root_dir])

    @jsii.member(jsii_name="fingerprint")
    @builtins.classmethod
    def fingerprint(cls, file_or_directory: str, *, extra_hash: typing.Optional[str]=None, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional["SymlinkFollowMode"]=None) -> str:
        """Produces fingerprint based on the contents of a single file or an entire directory tree.

        The fingerprint will also include:

        1. An extra string if defined in ``options.extra``.
        2. The set of exclude patterns, if defined in ``options.exclude``
        3. The symlink follow mode value.

        :param file_or_directory: The directory or file to fingerprint.
        :param extra_hash: Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param exclude: Glob patterns to exclude from the copy. Default: - nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER

        stability
        :stability: experimental
        """
        options = FingerprintOptions(extra_hash=extra_hash, exclude=exclude, follow=follow)

        return jsii.sinvoke(cls, "fingerprint", [file_or_directory, options])

    @jsii.member(jsii_name="isEmpty")
    @builtins.classmethod
    def is_empty(cls, dir: str) -> bool:
        """Checks whether a directory is empty.

        :param dir: The directory to check.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "isEmpty", [dir])

    @jsii.member(jsii_name="mkdtemp")
    @builtins.classmethod
    def mkdtemp(cls, prefix: str) -> str:
        """Creates a unique temporary directory in the **system temp directory**.

        :param prefix: A prefix for the directory name. Six random characters will be generated and appended behind this prefix.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "mkdtemp", [prefix])

    @jsii.python.classproperty
    @jsii.member(jsii_name="tmpdir")
    def tmpdir(cls) -> str:
        """The real path of the system temp directory.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "tmpdir")


@jsii.data_type(jsii_type="monocdk-experiment.FingerprintOptions", jsii_struct_bases=[CopyOptions], name_mapping={'exclude': 'exclude', 'follow': 'follow', 'extra_hash': 'extraHash'})
class FingerprintOptions(CopyOptions):
    def __init__(self, *, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional["SymlinkFollowMode"]=None, extra_hash: typing.Optional[str]=None) -> None:
        """Options related to calculating source hash.

        :param exclude: Glob patterns to exclude from the copy. Default: - nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER
        :param extra_hash: Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content

        stability
        :stability: experimental
        """
        self._values = {
        }
        if exclude is not None: self._values["exclude"] = exclude
        if follow is not None: self._values["follow"] = follow
        if extra_hash is not None: self._values["extra_hash"] = extra_hash

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[str]]:
        """Glob patterns to exclude from the copy.

        default
        :default: - nothing is excluded

        stability
        :stability: experimental
        """
        return self._values.get('exclude')

    @builtins.property
    def follow(self) -> typing.Optional["SymlinkFollowMode"]:
        """A strategy for how to handle symlinks.

        default
        :default: SymlinkFollowMode.NEVER

        stability
        :stability: experimental
        """
        return self._values.get('follow')

    @builtins.property
    def extra_hash(self) -> typing.Optional[str]:
        """Extra information to encode into the fingerprint (e.g. build instructions and other inputs).

        default
        :default: - hash is only based on source content

        stability
        :stability: experimental
        """
        return self._values.get('extra_hash')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FingerprintOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Fn(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.Fn"):
    """CloudFormation intrinsic functions.

    http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference.html

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="base64")
    @builtins.classmethod
    def base64(cls, data: str) -> str:
        """The intrinsic function ``Fn::Base64`` returns the Base64 representation of the input string.

        This function is typically used to pass encoded data to
        Amazon EC2 instances by way of the UserData property.

        :param data: The string value you want to convert to Base64.

        return
        :return: a token represented as a string

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "base64", [data])

    @jsii.member(jsii_name="cidr")
    @builtins.classmethod
    def cidr(cls, ip_block: str, count: jsii.Number, size_mask: typing.Optional[str]=None) -> typing.List[str]:
        """The intrinsic function ``Fn::Cidr`` returns the specified Cidr address block.

        :param ip_block: The user-specified default Cidr address block.
        :param count: The number of subnets' Cidr block wanted. Count can be 1 to 256.
        :param size_mask: The digit covered in the subnet.

        return
        :return: a token represented as a string

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "cidr", [ip_block, count, size_mask])

    @jsii.member(jsii_name="conditionAnd")
    @builtins.classmethod
    def condition_and(cls, *conditions: "ICfnConditionExpression") -> "ICfnConditionExpression":
        """Returns true if all the specified conditions evaluate to true, or returns false if any one of the conditions evaluates to false.

        ``Fn::And`` acts as
        an AND operator. The minimum number of conditions that you can include is
        2, and the maximum is 10.

        :param conditions: conditions to AND.

        return
        :return: an FnCondition token

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "conditionAnd", [*conditions])

    @jsii.member(jsii_name="conditionContains")
    @builtins.classmethod
    def condition_contains(cls, list_of_strings: typing.List[str], value: str) -> "ICfnConditionExpression":
        """Returns true if a specified string matches at least one value in a list of strings.

        :param list_of_strings: A list of strings, such as "A", "B", "C".
        :param value: A string, such as "A", that you want to compare against a list of strings.

        return
        :return: an FnCondition token

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "conditionContains", [list_of_strings, value])

    @jsii.member(jsii_name="conditionEachMemberEquals")
    @builtins.classmethod
    def condition_each_member_equals(cls, list_of_strings: typing.List[str], value: str) -> "ICfnConditionExpression":
        """Returns true if a specified string matches all values in a list.

        :param list_of_strings: A list of strings, such as "A", "B", "C".
        :param value: A string, such as "A", that you want to compare against a list of strings.

        return
        :return: an FnCondition token

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "conditionEachMemberEquals", [list_of_strings, value])

    @jsii.member(jsii_name="conditionEachMemberIn")
    @builtins.classmethod
    def condition_each_member_in(cls, strings_to_check: typing.List[str], strings_to_match: typing.List[str]) -> "ICfnConditionExpression":
        """Returns true if each member in a list of strings matches at least one value in a second list of strings.

        :param strings_to_check: A list of strings, such as "A", "B", "C". AWS CloudFormation checks whether each member in the strings_to_check parameter is in the strings_to_match parameter.
        :param strings_to_match: A list of strings, such as "A", "B", "C". Each member in the strings_to_match parameter is compared against the members of the strings_to_check parameter.

        return
        :return: an FnCondition token

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "conditionEachMemberIn", [strings_to_check, strings_to_match])

    @jsii.member(jsii_name="conditionEquals")
    @builtins.classmethod
    def condition_equals(cls, lhs: typing.Any, rhs: typing.Any) -> "ICfnConditionExpression":
        """Compares if two values are equal.

        Returns true if the two values are equal
        or false if they aren't.

        :param lhs: A value of any type that you want to compare.
        :param rhs: A value of any type that you want to compare.

        return
        :return: an FnCondition token

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "conditionEquals", [lhs, rhs])

    @jsii.member(jsii_name="conditionIf")
    @builtins.classmethod
    def condition_if(cls, condition_id: str, value_if_true: typing.Any, value_if_false: typing.Any) -> "ICfnConditionExpression":
        """Returns one value if the specified condition evaluates to true and another value if the specified condition evaluates to false.

        Currently, AWS
        CloudFormation supports the ``Fn::If`` intrinsic function in the metadata
        attribute, update policy attribute, and property values in the Resources
        section and Outputs sections of a template. You can use the AWS::NoValue
        pseudo parameter as a return value to remove the corresponding property.

        :param condition_id: A reference to a condition in the Conditions section. Use the condition's name to reference it.
        :param value_if_true: A value to be returned if the specified condition evaluates to true.
        :param value_if_false: A value to be returned if the specified condition evaluates to false.

        return
        :return: an FnCondition token

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "conditionIf", [condition_id, value_if_true, value_if_false])

    @jsii.member(jsii_name="conditionNot")
    @builtins.classmethod
    def condition_not(cls, condition: "ICfnConditionExpression") -> "ICfnConditionExpression":
        """Returns true for a condition that evaluates to false or returns false for a condition that evaluates to true.

        ``Fn::Not`` acts as a NOT operator.

        :param condition: A condition such as ``Fn::Equals`` that evaluates to true or false.

        return
        :return: an FnCondition token

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "conditionNot", [condition])

    @jsii.member(jsii_name="conditionOr")
    @builtins.classmethod
    def condition_or(cls, *conditions: "ICfnConditionExpression") -> "ICfnConditionExpression":
        """Returns true if any one of the specified conditions evaluate to true, or returns false if all of the conditions evaluates to false.

        ``Fn::Or`` acts
        as an OR operator. The minimum number of conditions that you can include is
        2, and the maximum is 10.

        :param conditions: conditions that evaluates to true or false.

        return
        :return: an FnCondition token

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "conditionOr", [*conditions])

    @jsii.member(jsii_name="findInMap")
    @builtins.classmethod
    def find_in_map(cls, map_name: str, top_level_key: str, second_level_key: str) -> str:
        """The intrinsic function ``Fn::FindInMap`` returns the value corresponding to keys in a two-level map that is declared in the Mappings section.

        :param map_name: -
        :param top_level_key: -
        :param second_level_key: -

        return
        :return: a token represented as a string

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "findInMap", [map_name, top_level_key, second_level_key])

    @jsii.member(jsii_name="getAtt")
    @builtins.classmethod
    def get_att(cls, logical_name_of_resource: str, attribute_name: str) -> "IResolvable":
        """The ``Fn::GetAtt`` intrinsic function returns the value of an attribute from a resource in the template.

        :param logical_name_of_resource: The logical name (also called logical ID) of the resource that contains the attribute that you want.
        :param attribute_name: The name of the resource-specific attribute whose value you want. See the resource's reference page for details about the attributes available for that resource type.

        return
        :return: an IResolvable object

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "getAtt", [logical_name_of_resource, attribute_name])

    @jsii.member(jsii_name="getAzs")
    @builtins.classmethod
    def get_azs(cls, region: typing.Optional[str]=None) -> typing.List[str]:
        """The intrinsic function ``Fn::GetAZs`` returns an array that lists Availability Zones for a specified region.

        Because customers have access to
        different Availability Zones, the intrinsic function ``Fn::GetAZs`` enables
        template authors to write templates that adapt to the calling user's
        access. That way you don't have to hard-code a full list of Availability
        Zones for a specified region.

        :param region: The name of the region for which you want to get the Availability Zones. You can use the AWS::Region pseudo parameter to specify the region in which the stack is created. Specifying an empty string is equivalent to specifying AWS::Region.

        return
        :return: a token represented as a string array

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "getAzs", [region])

    @jsii.member(jsii_name="importValue")
    @builtins.classmethod
    def import_value(cls, shared_value_to_import: str) -> str:
        """The intrinsic function ``Fn::ImportValue`` returns the value of an output exported by another stack.

        You typically use this function to create
        cross-stack references. In the following example template snippets, Stack A
        exports VPC security group values and Stack B imports them.

        :param shared_value_to_import: The stack output value that you want to import.

        return
        :return: a token represented as a string

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "importValue", [shared_value_to_import])

    @jsii.member(jsii_name="join")
    @builtins.classmethod
    def join(cls, delimiter: str, list_of_values: typing.List[str]) -> str:
        """The intrinsic function ``Fn::Join`` appends a set of values into a single value, separated by the specified delimiter.

        If a delimiter is the empty
        string, the set of values are concatenated with no delimiter.

        :param delimiter: The value you want to occur between fragments. The delimiter will occur between fragments only. It will not terminate the final value.
        :param list_of_values: The list of values you want combined.

        return
        :return: a token represented as a string

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "join", [delimiter, list_of_values])

    @jsii.member(jsii_name="ref")
    @builtins.classmethod
    def ref(cls, logical_name: str) -> str:
        """The ``Ref`` intrinsic function returns the value of the specified parameter or resource.

        Note that it doesn't validate the logicalName, it mainly serves paremeter/resource reference defined in a ``CfnInclude`` template.

        :param logical_name: The logical name of a parameter/resource for which you want to retrieve its value.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "ref", [logical_name])

    @jsii.member(jsii_name="refAll")
    @builtins.classmethod
    def ref_all(cls, parameter_type: str) -> typing.List[str]:
        """Returns all values for a specified parameter type.

        :param parameter_type: An AWS-specific parameter type, such as AWS::EC2::SecurityGroup::Id or AWS::EC2::VPC::Id. For more information, see Parameters in the AWS CloudFormation User Guide.

        return
        :return: a token represented as a string array

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "refAll", [parameter_type])

    @jsii.member(jsii_name="select")
    @builtins.classmethod
    def select(cls, index: jsii.Number, array: typing.List[str]) -> str:
        """The intrinsic function ``Fn::Select`` returns a single object from a list of objects by index.

        :param index: The index of the object to retrieve. This must be a value from zero to N-1, where N represents the number of elements in the array.
        :param array: The list of objects to select from. This list must not be null, nor can it have null entries.

        return
        :return: a token represented as a string

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "select", [index, array])

    @jsii.member(jsii_name="split")
    @builtins.classmethod
    def split(cls, delimiter: str, source: str) -> typing.List[str]:
        """To split a string into a list of string values so that you can select an element from the resulting string list, use the ``Fn::Split`` intrinsic function.

        Specify the location of splits
        with a delimiter, such as , (a comma). After you split a string, use the ``Fn::Select`` function
        to pick a specific element.

        :param delimiter: A string value that determines where the source string is divided.
        :param source: The string value that you want to split.

        return
        :return: a token represented as a string array

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "split", [delimiter, source])

    @jsii.member(jsii_name="sub")
    @builtins.classmethod
    def sub(cls, body: str, variables: typing.Optional[typing.Mapping[str, str]]=None) -> str:
        """The intrinsic function ``Fn::Sub`` substitutes variables in an input string with values that you specify.

        In your templates, you can use this function
        to construct commands or outputs that include values that aren't available
        until you create or update a stack.

        :param body: A string with variables that AWS CloudFormation substitutes with their associated values at runtime. Write variables as ${MyVarName}. Variables can be template parameter names, resource logical IDs, resource attributes, or a variable in a key-value map. If you specify only template parameter names, resource logical IDs, and resource attributes, don't specify a key-value map.
        :param variables: The name of a variable that you included in the String parameter. The value that AWS CloudFormation substitutes for the associated variable name at runtime.

        return
        :return: a token represented as a string

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "sub", [body, variables])

    @jsii.member(jsii_name="transform")
    @builtins.classmethod
    def transform(cls, macro_name: str, parameters: typing.Mapping[str, typing.Any]) -> "IResolvable":
        """Creates a token representing the ``Fn::Transform`` expression.

        :param macro_name: The name of the macro to perform the processing.
        :param parameters: The parameters to be passed to the macro.

        return
        :return: a token representing the transform expression

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-transform.html
        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "transform", [macro_name, parameters])

    @jsii.member(jsii_name="valueOf")
    @builtins.classmethod
    def value_of(cls, parameter_or_logical_id: str, attribute: str) -> str:
        """Returns an attribute value or list of values for a specific parameter and attribute.

        :param parameter_or_logical_id: The name of a parameter for which you want to retrieve attribute values. The parameter must be declared in the Parameters section of the template.
        :param attribute: The name of an attribute from which you want to retrieve a value.

        return
        :return: a token represented as a string

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "valueOf", [parameter_or_logical_id, attribute])

    @jsii.member(jsii_name="valueOfAll")
    @builtins.classmethod
    def value_of_all(cls, parameter_type: str, attribute: str) -> typing.List[str]:
        """Returns a list of all attribute values for a given parameter type and attribute.

        :param parameter_type: An AWS-specific parameter type, such as AWS::EC2::SecurityGroup::Id or AWS::EC2::VPC::Id. For more information, see Parameters in the AWS CloudFormation User Guide.
        :param attribute: The name of an attribute from which you want to retrieve a value. For more information about attributes, see Supported Attributes.

        return
        :return: a token represented as a string array

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "valueOfAll", [parameter_type, attribute])


@jsii.data_type(jsii_type="monocdk-experiment.FromCloudFormationOptions", jsii_struct_bases=[], name_mapping={'finder': 'finder'})
class FromCloudFormationOptions():
    def __init__(self, *, finder: "ICfnFinder") -> None:
        """The interface used as the last argument to the fromCloudFormation static method of the generated L1 classes.

        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        self._values = {
            'finder': finder,
        }

    @builtins.property
    def finder(self) -> "ICfnFinder":
        """The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        return self._values.get('finder')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FromCloudFormationOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.GetContextKeyOptions", jsii_struct_bases=[], name_mapping={'provider': 'provider', 'props': 'props'})
class GetContextKeyOptions():
    def __init__(self, *, provider: str, props: typing.Optional[typing.Mapping[str, typing.Any]]=None) -> None:
        """
        :param provider: The context provider to query.
        :param props: Provider-specific properties.

        stability
        :stability: experimental
        """
        self._values = {
            'provider': provider,
        }
        if props is not None: self._values["props"] = props

    @builtins.property
    def provider(self) -> str:
        """The context provider to query.

        stability
        :stability: experimental
        """
        return self._values.get('provider')

    @builtins.property
    def props(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Provider-specific properties.

        stability
        :stability: experimental
        """
        return self._values.get('props')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GetContextKeyOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.GetContextKeyResult", jsii_struct_bases=[], name_mapping={'key': 'key', 'props': 'props'})
class GetContextKeyResult():
    def __init__(self, *, key: str, props: typing.Mapping[str, typing.Any]) -> None:
        """
        :param key: 
        :param props: 

        stability
        :stability: experimental
        """
        self._values = {
            'key': key,
            'props': props,
        }

    @builtins.property
    def key(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('key')

    @builtins.property
    def props(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('props')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GetContextKeyResult(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.GetContextValueOptions", jsii_struct_bases=[GetContextKeyOptions], name_mapping={'provider': 'provider', 'props': 'props', 'dummy_value': 'dummyValue'})
class GetContextValueOptions(GetContextKeyOptions):
    def __init__(self, *, provider: str, props: typing.Optional[typing.Mapping[str, typing.Any]]=None, dummy_value: typing.Any) -> None:
        """
        :param provider: The context provider to query.
        :param props: Provider-specific properties.
        :param dummy_value: The value to return if the context value was not found and a missing context is reported. This should be a dummy value that should preferably fail during deployment since it represents an invalid state.

        stability
        :stability: experimental
        """
        self._values = {
            'provider': provider,
            'dummy_value': dummy_value,
        }
        if props is not None: self._values["props"] = props

    @builtins.property
    def provider(self) -> str:
        """The context provider to query.

        stability
        :stability: experimental
        """
        return self._values.get('provider')

    @builtins.property
    def props(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Provider-specific properties.

        stability
        :stability: experimental
        """
        return self._values.get('props')

    @builtins.property
    def dummy_value(self) -> typing.Any:
        """The value to return if the context value was not found and a missing context is reported.

        This should be a dummy value that should preferably
        fail during deployment since it represents an invalid state.

        stability
        :stability: experimental
        """
        return self._values.get('dummy_value')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GetContextValueOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.GetContextValueResult", jsii_struct_bases=[], name_mapping={'value': 'value'})
class GetContextValueResult():
    def __init__(self, *, value: typing.Any=None) -> None:
        """
        :param value: 

        stability
        :stability: experimental
        """
        self._values = {
        }
        if value is not None: self._values["value"] = value

    @builtins.property
    def value(self) -> typing.Any:
        """
        stability
        :stability: experimental
        """
        return self._values.get('value')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GetContextValueResult(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="monocdk-experiment.IAnyProducer")
class IAnyProducer(jsii.compat.Protocol):
    """Interface for lazy untyped value producers.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAnyProducerProxy

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Any:
        """Produce the value.

        :param context: -

        stability
        :stability: experimental
        """
        ...


class _IAnyProducerProxy():
    """Interface for lazy untyped value producers.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.IAnyProducer"
    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Any:
        """Produce the value.

        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "produce", [context])


@jsii.interface(jsii_type="monocdk-experiment.IAspect")
class IAspect(jsii.compat.Protocol):
    """Represents an Aspect.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAspectProxy

    @jsii.member(jsii_name="visit")
    def visit(self, node: "IConstruct") -> None:
        """All aspects can visit an IConstruct.

        :param node: -

        stability
        :stability: experimental
        """
        ...


class _IAspectProxy():
    """Represents an Aspect.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.IAspect"
    @jsii.member(jsii_name="visit")
    def visit(self, node: "IConstruct") -> None:
        """All aspects can visit an IConstruct.

        :param node: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "visit", [node])


@jsii.interface(jsii_type="monocdk-experiment.IAsset")
class IAsset(jsii.compat.Protocol):
    """Common interface for all assets.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAssetProxy

    @builtins.property
    @jsii.member(jsii_name="assetHash")
    def asset_hash(self) -> str:
        """A hash of this asset, which is available at construction time.

        As this is a plain string, it
        can be used in construct IDs in order to enforce creation of a new resource when the content
        hash has changed.

        stability
        :stability: experimental
        """
        ...


class _IAssetProxy():
    """Common interface for all assets.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.IAsset"
    @builtins.property
    @jsii.member(jsii_name="assetHash")
    def asset_hash(self) -> str:
        """A hash of this asset, which is available at construction time.

        As this is a plain string, it
        can be used in construct IDs in order to enforce creation of a new resource when the content
        hash has changed.

        stability
        :stability: experimental
        """
        return jsii.get(self, "assetHash")


@jsii.interface(jsii_type="monocdk-experiment.ICfnFinder")
class ICfnFinder(jsii.compat.Protocol):
    """An interface that represents callbacks into a CloudFormation template.

    Used by the fromCloudFormation methods in the generated L1 classes.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ICfnFinderProxy

    @jsii.member(jsii_name="findCondition")
    def find_condition(self, condition_name: str) -> typing.Optional["CfnCondition"]:
        """Return the Condition with the given name from the template.

        If there is no Condition with that name in the template,
        returns undefined.

        :param condition_name: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="findRefTarget")
    def find_ref_target(self, element_name: str) -> typing.Optional["CfnElement"]:
        """Returns the element referenced using a Ref expression with the given name.

        If there is no element with this name in the template,
        return undefined.

        :param element_name: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="findResource")
    def find_resource(self, logical_id: str) -> typing.Optional["CfnResource"]:
        """Returns the resource with the given logical ID in the template.

        If a resource with that logical ID was not found in the template,
        returns undefined.

        :param logical_id: -

        stability
        :stability: experimental
        """
        ...


class _ICfnFinderProxy():
    """An interface that represents callbacks into a CloudFormation template.

    Used by the fromCloudFormation methods in the generated L1 classes.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.ICfnFinder"
    @jsii.member(jsii_name="findCondition")
    def find_condition(self, condition_name: str) -> typing.Optional["CfnCondition"]:
        """Return the Condition with the given name from the template.

        If there is no Condition with that name in the template,
        returns undefined.

        :param condition_name: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "findCondition", [condition_name])

    @jsii.member(jsii_name="findRefTarget")
    def find_ref_target(self, element_name: str) -> typing.Optional["CfnElement"]:
        """Returns the element referenced using a Ref expression with the given name.

        If there is no element with this name in the template,
        return undefined.

        :param element_name: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "findRefTarget", [element_name])

    @jsii.member(jsii_name="findResource")
    def find_resource(self, logical_id: str) -> typing.Optional["CfnResource"]:
        """Returns the resource with the given logical ID in the template.

        If a resource with that logical ID was not found in the template,
        returns undefined.

        :param logical_id: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "findResource", [logical_id])


@jsii.interface(jsii_type="monocdk-experiment.ICfnResourceOptions")
class ICfnResourceOptions(jsii.compat.Protocol):
    """
    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ICfnResourceOptionsProxy

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> typing.Optional["CfnCondition"]:
        """A condition to associate with this resource.

        This means that only if the condition evaluates to 'true' when the stack
        is deployed, the resource will be included. This is provided to allow CDK projects to produce legacy templates, but noramlly
        there is no need to use it in CDK projects.

        stability
        :stability: experimental
        """
        ...

    @condition.setter
    def condition(self, value: typing.Optional["CfnCondition"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="creationPolicy")
    def creation_policy(self) -> typing.Optional["CfnCreationPolicy"]:
        """Associate the CreationPolicy attribute with a resource to prevent its status from reaching create complete until AWS CloudFormation receives a specified number of success signals or the timeout period is exceeded.

        To signal a
        resource, you can use the cfn-signal helper script or SignalResource API. AWS CloudFormation publishes valid signals
        to the stack events so that you track the number of signals sent.

        stability
        :stability: experimental
        """
        ...

    @creation_policy.setter
    def creation_policy(self, value: typing.Optional["CfnCreationPolicy"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="deletionPolicy")
    def deletion_policy(self) -> typing.Optional["CfnDeletionPolicy"]:
        """With the DeletionPolicy attribute you can preserve or (in some cases) backup a resource when its stack is deleted.

        You specify a DeletionPolicy attribute for each resource that you want to control. If a resource has no DeletionPolicy
        attribute, AWS CloudFormation deletes the resource by default. Note that this capability also applies to update operations
        that lead to resources being removed.

        stability
        :stability: experimental
        """
        ...

    @deletion_policy.setter
    def deletion_policy(self, value: typing.Optional["CfnDeletionPolicy"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Metadata associated with the CloudFormation resource.

        This is not the same as the construct metadata which can be added
        using construct.addMetadata(), but would not appear in the CloudFormation template automatically.

        stability
        :stability: experimental
        """
        ...

    @metadata.setter
    def metadata(self, value: typing.Optional[typing.Mapping[str, typing.Any]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="updatePolicy")
    def update_policy(self) -> typing.Optional["CfnUpdatePolicy"]:
        """Use the UpdatePolicy attribute to specify how AWS CloudFormation handles updates to the AWS::AutoScaling::AutoScalingGroup resource.

        AWS CloudFormation invokes one of three update policies depending on the type of change you make or whether a
        scheduled action is associated with the Auto Scaling group.

        stability
        :stability: experimental
        """
        ...

    @update_policy.setter
    def update_policy(self, value: typing.Optional["CfnUpdatePolicy"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="updateReplacePolicy")
    def update_replace_policy(self) -> typing.Optional["CfnDeletionPolicy"]:
        """Use the UpdateReplacePolicy attribute to retain or (in some cases) backup the existing physical instance of a resource when it is replaced during a stack update operation.

        stability
        :stability: experimental
        """
        ...

    @update_replace_policy.setter
    def update_replace_policy(self, value: typing.Optional["CfnDeletionPolicy"]) -> None:
        ...


class _ICfnResourceOptionsProxy():
    """
    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.ICfnResourceOptions"
    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> typing.Optional["CfnCondition"]:
        """A condition to associate with this resource.

        This means that only if the condition evaluates to 'true' when the stack
        is deployed, the resource will be included. This is provided to allow CDK projects to produce legacy templates, but noramlly
        there is no need to use it in CDK projects.

        stability
        :stability: experimental
        """
        return jsii.get(self, "condition")

    @condition.setter
    def condition(self, value: typing.Optional["CfnCondition"]) -> None:
        jsii.set(self, "condition", value)

    @builtins.property
    @jsii.member(jsii_name="creationPolicy")
    def creation_policy(self) -> typing.Optional["CfnCreationPolicy"]:
        """Associate the CreationPolicy attribute with a resource to prevent its status from reaching create complete until AWS CloudFormation receives a specified number of success signals or the timeout period is exceeded.

        To signal a
        resource, you can use the cfn-signal helper script or SignalResource API. AWS CloudFormation publishes valid signals
        to the stack events so that you track the number of signals sent.

        stability
        :stability: experimental
        """
        return jsii.get(self, "creationPolicy")

    @creation_policy.setter
    def creation_policy(self, value: typing.Optional["CfnCreationPolicy"]) -> None:
        jsii.set(self, "creationPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="deletionPolicy")
    def deletion_policy(self) -> typing.Optional["CfnDeletionPolicy"]:
        """With the DeletionPolicy attribute you can preserve or (in some cases) backup a resource when its stack is deleted.

        You specify a DeletionPolicy attribute for each resource that you want to control. If a resource has no DeletionPolicy
        attribute, AWS CloudFormation deletes the resource by default. Note that this capability also applies to update operations
        that lead to resources being removed.

        stability
        :stability: experimental
        """
        return jsii.get(self, "deletionPolicy")

    @deletion_policy.setter
    def deletion_policy(self, value: typing.Optional["CfnDeletionPolicy"]) -> None:
        jsii.set(self, "deletionPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Metadata associated with the CloudFormation resource.

        This is not the same as the construct metadata which can be added
        using construct.addMetadata(), but would not appear in the CloudFormation template automatically.

        stability
        :stability: experimental
        """
        return jsii.get(self, "metadata")

    @metadata.setter
    def metadata(self, value: typing.Optional[typing.Mapping[str, typing.Any]]) -> None:
        jsii.set(self, "metadata", value)

    @builtins.property
    @jsii.member(jsii_name="updatePolicy")
    def update_policy(self) -> typing.Optional["CfnUpdatePolicy"]:
        """Use the UpdatePolicy attribute to specify how AWS CloudFormation handles updates to the AWS::AutoScaling::AutoScalingGroup resource.

        AWS CloudFormation invokes one of three update policies depending on the type of change you make or whether a
        scheduled action is associated with the Auto Scaling group.

        stability
        :stability: experimental
        """
        return jsii.get(self, "updatePolicy")

    @update_policy.setter
    def update_policy(self, value: typing.Optional["CfnUpdatePolicy"]) -> None:
        jsii.set(self, "updatePolicy", value)

    @builtins.property
    @jsii.member(jsii_name="updateReplacePolicy")
    def update_replace_policy(self) -> typing.Optional["CfnDeletionPolicy"]:
        """Use the UpdateReplacePolicy attribute to retain or (in some cases) backup the existing physical instance of a resource when it is replaced during a stack update operation.

        stability
        :stability: experimental
        """
        return jsii.get(self, "updateReplacePolicy")

    @update_replace_policy.setter
    def update_replace_policy(self, value: typing.Optional["CfnDeletionPolicy"]) -> None:
        jsii.set(self, "updateReplacePolicy", value)


@jsii.interface(jsii_type="monocdk-experiment.IDependable")
class IDependable(jsii.compat.Protocol):
    """Trait marker for classes that can be depended upon.

    The presence of this interface indicates that an object has
    an ``IDependableTrait`` implementation.

    This interface can be used to take an (ordering) dependency on a set of
    constructs. An ordering dependency implies that the resources represented by
    those constructs are deployed before the resources depending ON them are
    deployed.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IDependableProxy

    pass

class _IDependableProxy():
    """Trait marker for classes that can be depended upon.

    The presence of this interface indicates that an object has
    an ``IDependableTrait`` implementation.

    This interface can be used to take an (ordering) dependency on a set of
    constructs. An ordering dependency implies that the resources represented by
    those constructs are deployed before the resources depending ON them are
    deployed.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.IDependable"
    pass

@jsii.interface(jsii_type="monocdk-experiment.IFragmentConcatenator")
class IFragmentConcatenator(jsii.compat.Protocol):
    """Function used to concatenate symbols in the target document language.

    Interface so it could potentially be exposed over jsii.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IFragmentConcatenatorProxy

    @jsii.member(jsii_name="join")
    def join(self, left: typing.Any, right: typing.Any) -> typing.Any:
        """Join the fragment on the left and on the right.

        :param left: -
        :param right: -

        stability
        :stability: experimental
        """
        ...


class _IFragmentConcatenatorProxy():
    """Function used to concatenate symbols in the target document language.

    Interface so it could potentially be exposed over jsii.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.IFragmentConcatenator"
    @jsii.member(jsii_name="join")
    def join(self, left: typing.Any, right: typing.Any) -> typing.Any:
        """Join the fragment on the left and on the right.

        :param left: -
        :param right: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "join", [left, right])


@jsii.interface(jsii_type="monocdk-experiment.IInspectable")
class IInspectable(jsii.compat.Protocol):
    """Interface for examining a construct and exposing metadata.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IInspectableProxy

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "TreeInspector") -> None:
        """Examines construct.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        ...


class _IInspectableProxy():
    """Interface for examining a construct and exposing metadata.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.IInspectable"
    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "TreeInspector") -> None:
        """Examines construct.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])


@jsii.interface(jsii_type="monocdk-experiment.IListProducer")
class IListProducer(jsii.compat.Protocol):
    """Interface for lazy list producers.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IListProducerProxy

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[typing.List[str]]:
        """Produce the list value.

        :param context: -

        stability
        :stability: experimental
        """
        ...


class _IListProducerProxy():
    """Interface for lazy list producers.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.IListProducer"
    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[typing.List[str]]:
        """Produce the list value.

        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "produce", [context])


@jsii.interface(jsii_type="monocdk-experiment.INumberProducer")
class INumberProducer(jsii.compat.Protocol):
    """Interface for lazy number producers.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _INumberProducerProxy

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[jsii.Number]:
        """Produce the number value.

        :param context: -

        stability
        :stability: experimental
        """
        ...


class _INumberProducerProxy():
    """Interface for lazy number producers.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.INumberProducer"
    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[jsii.Number]:
        """Produce the number value.

        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "produce", [context])


@jsii.interface(jsii_type="monocdk-experiment.IPostProcessor")
class IPostProcessor(jsii.compat.Protocol):
    """A Token that can post-process the complete resolved value, after resolve() has recursed over it.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IPostProcessorProxy

    @jsii.member(jsii_name="postProcess")
    def post_process(self, input: typing.Any, context: "IResolveContext") -> typing.Any:
        """Process the completely resolved value, after full recursion/resolution has happened.

        :param input: -
        :param context: -

        stability
        :stability: experimental
        """
        ...


class _IPostProcessorProxy():
    """A Token that can post-process the complete resolved value, after resolve() has recursed over it.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.IPostProcessor"
    @jsii.member(jsii_name="postProcess")
    def post_process(self, input: typing.Any, context: "IResolveContext") -> typing.Any:
        """Process the completely resolved value, after full recursion/resolution has happened.

        :param input: -
        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "postProcess", [input, context])


@jsii.interface(jsii_type="monocdk-experiment.IResolvable")
class IResolvable(jsii.compat.Protocol):
    """Interface for values that can be resolvable later.

    Tokens are special objects that participate in synthesis.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IResolvableProxy

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[str]:
        """The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="resolve")
    def resolve(self, context: "IResolveContext") -> typing.Any:
        """Produce the Token's value at resolution time.

        :param context: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Return a string representation of this resolvable object.

        Returns a reversible string representation.

        stability
        :stability: experimental
        """
        ...


class _IResolvableProxy():
    """Interface for values that can be resolvable later.

    Tokens are special objects that participate in synthesis.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.IResolvable"
    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[str]:
        """The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.

        stability
        :stability: experimental
        """
        return jsii.get(self, "creationStack")

    @jsii.member(jsii_name="resolve")
    def resolve(self, context: "IResolveContext") -> typing.Any:
        """Produce the Token's value at resolution time.

        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolve", [context])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Return a string representation of this resolvable object.

        Returns a reversible string representation.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toString", [])


@jsii.interface(jsii_type="monocdk-experiment.IResolveContext")
class IResolveContext(jsii.compat.Protocol):
    """Current resolution context for tokens.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IResolveContextProxy

    @builtins.property
    @jsii.member(jsii_name="preparing")
    def preparing(self) -> bool:
        """True when we are still preparing, false if we're rendering the final output.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> "IConstruct":
        """The scope from which resolution has been initiated.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="registerPostProcessor")
    def register_post_processor(self, post_processor: "IPostProcessor") -> None:
        """Use this postprocessor after the entire token structure has been resolved.

        :param post_processor: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="resolve")
    def resolve(self, x: typing.Any) -> typing.Any:
        """Resolve an inner object.

        :param x: -

        stability
        :stability: experimental
        """
        ...


class _IResolveContextProxy():
    """Current resolution context for tokens.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.IResolveContext"
    @builtins.property
    @jsii.member(jsii_name="preparing")
    def preparing(self) -> bool:
        """True when we are still preparing, false if we're rendering the final output.

        stability
        :stability: experimental
        """
        return jsii.get(self, "preparing")

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> "IConstruct":
        """The scope from which resolution has been initiated.

        stability
        :stability: experimental
        """
        return jsii.get(self, "scope")

    @jsii.member(jsii_name="registerPostProcessor")
    def register_post_processor(self, post_processor: "IPostProcessor") -> None:
        """Use this postprocessor after the entire token structure has been resolved.

        :param post_processor: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "registerPostProcessor", [post_processor])

    @jsii.member(jsii_name="resolve")
    def resolve(self, x: typing.Any) -> typing.Any:
        """Resolve an inner object.

        :param x: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolve", [x])


@jsii.interface(jsii_type="monocdk-experiment.IStackSynthesizer")
class IStackSynthesizer(jsii.compat.Protocol):
    """Encodes information how a certain Stack should be deployed.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IStackSynthesizerProxy

    @jsii.member(jsii_name="addDockerImageAsset")
    def add_docker_image_asset(self, *, directory_name: str, source_hash: str, docker_build_args: typing.Optional[typing.Mapping[str, str]]=None, docker_build_target: typing.Optional[str]=None, docker_file: typing.Optional[str]=None, repository_name: typing.Optional[str]=None) -> "DockerImageAssetLocation":
        """Register a Docker Image Asset.

        Returns the parameters that can be used to refer to the asset inside the template.

        :param directory_name: The directory where the Dockerfile is stored, must be relative to the cloud assembly root.
        :param source_hash: The hash of the contents of the docker build context. This hash is used throughout the system to identify this image and avoid duplicate work in case the source did not change. NOTE: this means that if you wish to update your docker image, you must make a modification to the source (e.g. add some metadata to your Dockerfile).
        :param docker_build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param docker_build_target: Docker target to build to. Default: - no target
        :param docker_file: Path to the Dockerfile (relative to the directory). Default: - no file
        :param repository_name: ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - automatically derived from the asset's ID.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="addFileAsset")
    def add_file_asset(self, *, file_name: str, packaging: "FileAssetPackaging", source_hash: str) -> "FileAssetLocation":
        """Register a File Asset.

        Returns the parameters that can be used to refer to the asset inside the template.

        :param file_name: The path, relative to the root of the cloud assembly, in which this asset source resides. This can be a path to a file or a directory, dependning on the packaging type.
        :param packaging: Which type of packaging to perform.
        :param source_hash: A hash on the content source. This hash is used to uniquely identify this asset throughout the system. If this value doesn't change, the asset will not be rebuilt or republished.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="bind")
    def bind(self, stack: "Stack") -> None:
        """Bind to the stack this environment is going to be used on.

        Must be called before any of the other methods are called.

        :param stack: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="synthesizeStackArtifacts")
    def synthesize_stack_artifacts(self, session: "ISynthesisSession") -> None:
        """Synthesize all artifacts required for the stack into the session.

        :param session: -

        stability
        :stability: experimental
        """
        ...


class _IStackSynthesizerProxy():
    """Encodes information how a certain Stack should be deployed.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.IStackSynthesizer"
    @jsii.member(jsii_name="addDockerImageAsset")
    def add_docker_image_asset(self, *, directory_name: str, source_hash: str, docker_build_args: typing.Optional[typing.Mapping[str, str]]=None, docker_build_target: typing.Optional[str]=None, docker_file: typing.Optional[str]=None, repository_name: typing.Optional[str]=None) -> "DockerImageAssetLocation":
        """Register a Docker Image Asset.

        Returns the parameters that can be used to refer to the asset inside the template.

        :param directory_name: The directory where the Dockerfile is stored, must be relative to the cloud assembly root.
        :param source_hash: The hash of the contents of the docker build context. This hash is used throughout the system to identify this image and avoid duplicate work in case the source did not change. NOTE: this means that if you wish to update your docker image, you must make a modification to the source (e.g. add some metadata to your Dockerfile).
        :param docker_build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param docker_build_target: Docker target to build to. Default: - no target
        :param docker_file: Path to the Dockerfile (relative to the directory). Default: - no file
        :param repository_name: ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - automatically derived from the asset's ID.

        stability
        :stability: experimental
        """
        asset = DockerImageAssetSource(directory_name=directory_name, source_hash=source_hash, docker_build_args=docker_build_args, docker_build_target=docker_build_target, docker_file=docker_file, repository_name=repository_name)

        return jsii.invoke(self, "addDockerImageAsset", [asset])

    @jsii.member(jsii_name="addFileAsset")
    def add_file_asset(self, *, file_name: str, packaging: "FileAssetPackaging", source_hash: str) -> "FileAssetLocation":
        """Register a File Asset.

        Returns the parameters that can be used to refer to the asset inside the template.

        :param file_name: The path, relative to the root of the cloud assembly, in which this asset source resides. This can be a path to a file or a directory, dependning on the packaging type.
        :param packaging: Which type of packaging to perform.
        :param source_hash: A hash on the content source. This hash is used to uniquely identify this asset throughout the system. If this value doesn't change, the asset will not be rebuilt or republished.

        stability
        :stability: experimental
        """
        asset = FileAssetSource(file_name=file_name, packaging=packaging, source_hash=source_hash)

        return jsii.invoke(self, "addFileAsset", [asset])

    @jsii.member(jsii_name="bind")
    def bind(self, stack: "Stack") -> None:
        """Bind to the stack this environment is going to be used on.

        Must be called before any of the other methods are called.

        :param stack: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [stack])

    @jsii.member(jsii_name="synthesizeStackArtifacts")
    def synthesize_stack_artifacts(self, session: "ISynthesisSession") -> None:
        """Synthesize all artifacts required for the stack into the session.

        :param session: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeStackArtifacts", [session])


@jsii.interface(jsii_type="monocdk-experiment.IStringProducer")
class IStringProducer(jsii.compat.Protocol):
    """Interface for lazy string producers.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IStringProducerProxy

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[str]:
        """Produce the string value.

        :param context: -

        stability
        :stability: experimental
        """
        ...


class _IStringProducerProxy():
    """Interface for lazy string producers.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.IStringProducer"
    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[str]:
        """Produce the string value.

        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "produce", [context])


@jsii.interface(jsii_type="monocdk-experiment.ISynthesisSession")
class ISynthesisSession(jsii.compat.Protocol):
    """Represents a single session of synthesis.

    Passed into ``Construct.synthesize()`` methods.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ISynthesisSessionProxy

    @builtins.property
    @jsii.member(jsii_name="assembly")
    def assembly(self) -> _CloudAssemblyBuilder_d6cb3525:
        """Cloud assembly builder.

        stability
        :stability: experimental
        """
        ...

    @assembly.setter
    def assembly(self, value: _CloudAssemblyBuilder_d6cb3525) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> str:
        """The output directory for this synthesis session.

        stability
        :stability: experimental
        """
        ...

    @outdir.setter
    def outdir(self, value: str) -> None:
        ...


class _ISynthesisSessionProxy():
    """Represents a single session of synthesis.

    Passed into ``Construct.synthesize()`` methods.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.ISynthesisSession"
    @builtins.property
    @jsii.member(jsii_name="assembly")
    def assembly(self) -> _CloudAssemblyBuilder_d6cb3525:
        """Cloud assembly builder.

        stability
        :stability: experimental
        """
        return jsii.get(self, "assembly")

    @assembly.setter
    def assembly(self, value: _CloudAssemblyBuilder_d6cb3525) -> None:
        jsii.set(self, "assembly", value)

    @builtins.property
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> str:
        """The output directory for this synthesis session.

        stability
        :stability: experimental
        """
        return jsii.get(self, "outdir")

    @outdir.setter
    def outdir(self, value: str) -> None:
        jsii.set(self, "outdir", value)


@jsii.interface(jsii_type="monocdk-experiment.ITaggable")
class ITaggable(jsii.compat.Protocol):
    """Interface to implement tags.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITaggableProxy

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "TagManager":
        """TagManager to set, remove and format tags.

        stability
        :stability: experimental
        """
        ...


class _ITaggableProxy():
    """Interface to implement tags.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.ITaggable"
    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "TagManager":
        """TagManager to set, remove and format tags.

        stability
        :stability: experimental
        """
        return jsii.get(self, "tags")


@jsii.interface(jsii_type="monocdk-experiment.ITemplateOptions")
class ITemplateOptions(jsii.compat.Protocol):
    """CloudFormation template options for a stack.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITemplateOptionsProxy

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """Gets or sets the description of this stack.

        If provided, it will be included in the CloudFormation template's "Description" attribute.

        stability
        :stability: experimental
        """
        ...

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Metadata associated with the CloudFormation template.

        stability
        :stability: experimental
        """
        ...

    @metadata.setter
    def metadata(self, value: typing.Optional[typing.Mapping[str, typing.Any]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="templateFormatVersion")
    def template_format_version(self) -> typing.Optional[str]:
        """Gets or sets the AWSTemplateFormatVersion field of the CloudFormation template.

        stability
        :stability: experimental
        """
        ...

    @template_format_version.setter
    def template_format_version(self, value: typing.Optional[str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="transform")
    def transform(self) -> typing.Optional[str]:
        """Gets or sets the top-level template transform for this stack (e.g. "AWS::Serverless-2016-10-31").

        deprecated
        :deprecated: use ``transforms`` instead.

        stability
        :stability: deprecated
        """
        ...

    @transform.setter
    def transform(self, value: typing.Optional[str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="transforms")
    def transforms(self) -> typing.Optional[typing.List[str]]:
        """Gets or sets the top-level template transform(s) for this stack (e.g. ``["AWS::Serverless-2016-10-31"]``).

        stability
        :stability: experimental
        """
        ...

    @transforms.setter
    def transforms(self, value: typing.Optional[typing.List[str]]) -> None:
        ...


class _ITemplateOptionsProxy():
    """CloudFormation template options for a stack.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.ITemplateOptions"
    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """Gets or sets the description of this stack.

        If provided, it will be included in the CloudFormation template's "Description" attribute.

        stability
        :stability: experimental
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Metadata associated with the CloudFormation template.

        stability
        :stability: experimental
        """
        return jsii.get(self, "metadata")

    @metadata.setter
    def metadata(self, value: typing.Optional[typing.Mapping[str, typing.Any]]) -> None:
        jsii.set(self, "metadata", value)

    @builtins.property
    @jsii.member(jsii_name="templateFormatVersion")
    def template_format_version(self) -> typing.Optional[str]:
        """Gets or sets the AWSTemplateFormatVersion field of the CloudFormation template.

        stability
        :stability: experimental
        """
        return jsii.get(self, "templateFormatVersion")

    @template_format_version.setter
    def template_format_version(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "templateFormatVersion", value)

    @builtins.property
    @jsii.member(jsii_name="transform")
    def transform(self) -> typing.Optional[str]:
        """Gets or sets the top-level template transform for this stack (e.g. "AWS::Serverless-2016-10-31").

        deprecated
        :deprecated: use ``transforms`` instead.

        stability
        :stability: deprecated
        """
        return jsii.get(self, "transform")

    @transform.setter
    def transform(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "transform", value)

    @builtins.property
    @jsii.member(jsii_name="transforms")
    def transforms(self) -> typing.Optional[typing.List[str]]:
        """Gets or sets the top-level template transform(s) for this stack (e.g. ``["AWS::Serverless-2016-10-31"]``).

        stability
        :stability: experimental
        """
        return jsii.get(self, "transforms")

    @transforms.setter
    def transforms(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "transforms", value)


@jsii.interface(jsii_type="monocdk-experiment.ITokenMapper")
class ITokenMapper(jsii.compat.Protocol):
    """Interface to apply operation to tokens in a string.

    Interface so it can be exported via jsii.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITokenMapperProxy

    @jsii.member(jsii_name="mapToken")
    def map_token(self, t: "IResolvable") -> typing.Any:
        """Replace a single token.

        :param t: -

        stability
        :stability: experimental
        """
        ...


class _ITokenMapperProxy():
    """Interface to apply operation to tokens in a string.

    Interface so it can be exported via jsii.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.ITokenMapper"
    @jsii.member(jsii_name="mapToken")
    def map_token(self, t: "IResolvable") -> typing.Any:
        """Replace a single token.

        :param t: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "mapToken", [t])


@jsii.interface(jsii_type="monocdk-experiment.ITokenResolver")
class ITokenResolver(jsii.compat.Protocol):
    """How to resolve tokens.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITokenResolverProxy

    @jsii.member(jsii_name="resolveList")
    def resolve_list(self, l: typing.List[str], context: "IResolveContext") -> typing.Any:
        """Resolve a tokenized list.

        :param l: -
        :param context: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="resolveString")
    def resolve_string(self, s: "TokenizedStringFragments", context: "IResolveContext") -> typing.Any:
        """Resolve a string with at least one stringified token in it.

        (May use concatenation)

        :param s: -
        :param context: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="resolveToken")
    def resolve_token(self, t: "IResolvable", context: "IResolveContext", post_processor: "IPostProcessor") -> typing.Any:
        """Resolve a single token.

        :param t: -
        :param context: -
        :param post_processor: -

        stability
        :stability: experimental
        """
        ...


class _ITokenResolverProxy():
    """How to resolve tokens.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.ITokenResolver"
    @jsii.member(jsii_name="resolveList")
    def resolve_list(self, l: typing.List[str], context: "IResolveContext") -> typing.Any:
        """Resolve a tokenized list.

        :param l: -
        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolveList", [l, context])

    @jsii.member(jsii_name="resolveString")
    def resolve_string(self, s: "TokenizedStringFragments", context: "IResolveContext") -> typing.Any:
        """Resolve a string with at least one stringified token in it.

        (May use concatenation)

        :param s: -
        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolveString", [s, context])

    @jsii.member(jsii_name="resolveToken")
    def resolve_token(self, t: "IResolvable", context: "IResolveContext", post_processor: "IPostProcessor") -> typing.Any:
        """Resolve a single token.

        :param t: -
        :param context: -
        :param post_processor: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolveToken", [t, context, post_processor])


@jsii.implements(IResolvable)
class Intrinsic(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.Intrinsic"):
    """Token subclass that represents values intrinsic to the target document language.

    WARNING: this class should not be externally exposed, but is currently visible
    because of a limitation of jsii (https://github.com/aws/jsii/issues/524).

    This class will disappear in a future release and should not be used.

    stability
    :stability: experimental
    """
    def __init__(self, value: typing.Any) -> None:
        """
        :param value: -

        stability
        :stability: experimental
        """
        jsii.create(Intrinsic, self, [value])

    @jsii.member(jsii_name="newError")
    def _new_error(self, message: str) -> typing.Any:
        """Creates a throwable Error object that contains the token creation stack trace.

        :param message: Error message.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "newError", [message])

    @jsii.member(jsii_name="resolve")
    def resolve(self, _context: "IResolveContext") -> typing.Any:
        """Produce the Token's value at resolution time.

        :param _context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolve", [_context])

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> typing.Any:
        """Turn this Token into JSON.

        Called automatically when JSON.stringify() is called on a Token.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Convert an instance of this Token to a string.

        This method will be called implicitly by language runtimes if the object
        is embedded into a string. We treat it the same as an explicit
        stringification.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toString", [])

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[str]:
        """The captured stack trace which represents the location in which this token was created.

        stability
        :stability: experimental
        """
        return jsii.get(self, "creationStack")


class Lazy(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.Lazy"):
    """Lazily produce a value.

    Can be used to return a string, list or numeric value whose actual value
    will only be calculated later, during synthesis.

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="anyValue")
    @builtins.classmethod
    def any_value(cls, producer: "IAnyProducer", *, display_hint: typing.Optional[str]=None, omit_empty_array: typing.Optional[bool]=None) -> "IResolvable":
        """
        :param producer: -
        :param display_hint: Use the given name as a display hint. Default: - No hint
        :param omit_empty_array: If the produced value is an array and it is empty, return 'undefined' instead. Default: false

        stability
        :stability: experimental
        """
        options = LazyAnyValueOptions(display_hint=display_hint, omit_empty_array=omit_empty_array)

        return jsii.sinvoke(cls, "anyValue", [producer, options])

    @jsii.member(jsii_name="listValue")
    @builtins.classmethod
    def list_value(cls, producer: "IListProducer", *, display_hint: typing.Optional[str]=None, omit_empty: typing.Optional[bool]=None) -> typing.List[str]:
        """
        :param producer: -
        :param display_hint: Use the given name as a display hint. Default: - No hint
        :param omit_empty: If the produced list is empty, return 'undefined' instead. Default: false

        stability
        :stability: experimental
        """
        options = LazyListValueOptions(display_hint=display_hint, omit_empty=omit_empty)

        return jsii.sinvoke(cls, "listValue", [producer, options])

    @jsii.member(jsii_name="numberValue")
    @builtins.classmethod
    def number_value(cls, producer: "INumberProducer") -> jsii.Number:
        """
        :param producer: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "numberValue", [producer])

    @jsii.member(jsii_name="stringValue")
    @builtins.classmethod
    def string_value(cls, producer: "IStringProducer", *, display_hint: typing.Optional[str]=None) -> str:
        """
        :param producer: -
        :param display_hint: Use the given name as a display hint. Default: - No hint

        stability
        :stability: experimental
        """
        options = LazyStringValueOptions(display_hint=display_hint)

        return jsii.sinvoke(cls, "stringValue", [producer, options])


@jsii.data_type(jsii_type="monocdk-experiment.LazyAnyValueOptions", jsii_struct_bases=[], name_mapping={'display_hint': 'displayHint', 'omit_empty_array': 'omitEmptyArray'})
class LazyAnyValueOptions():
    def __init__(self, *, display_hint: typing.Optional[str]=None, omit_empty_array: typing.Optional[bool]=None) -> None:
        """Options for creating lazy untyped tokens.

        :param display_hint: Use the given name as a display hint. Default: - No hint
        :param omit_empty_array: If the produced value is an array and it is empty, return 'undefined' instead. Default: false

        stability
        :stability: experimental
        """
        self._values = {
        }
        if display_hint is not None: self._values["display_hint"] = display_hint
        if omit_empty_array is not None: self._values["omit_empty_array"] = omit_empty_array

    @builtins.property
    def display_hint(self) -> typing.Optional[str]:
        """Use the given name as a display hint.

        default
        :default: - No hint

        stability
        :stability: experimental
        """
        return self._values.get('display_hint')

    @builtins.property
    def omit_empty_array(self) -> typing.Optional[bool]:
        """If the produced value is an array and it is empty, return 'undefined' instead.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('omit_empty_array')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LazyAnyValueOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.LazyListValueOptions", jsii_struct_bases=[], name_mapping={'display_hint': 'displayHint', 'omit_empty': 'omitEmpty'})
class LazyListValueOptions():
    def __init__(self, *, display_hint: typing.Optional[str]=None, omit_empty: typing.Optional[bool]=None) -> None:
        """Options for creating a lazy list token.

        :param display_hint: Use the given name as a display hint. Default: - No hint
        :param omit_empty: If the produced list is empty, return 'undefined' instead. Default: false

        stability
        :stability: experimental
        """
        self._values = {
        }
        if display_hint is not None: self._values["display_hint"] = display_hint
        if omit_empty is not None: self._values["omit_empty"] = omit_empty

    @builtins.property
    def display_hint(self) -> typing.Optional[str]:
        """Use the given name as a display hint.

        default
        :default: - No hint

        stability
        :stability: experimental
        """
        return self._values.get('display_hint')

    @builtins.property
    def omit_empty(self) -> typing.Optional[bool]:
        """If the produced list is empty, return 'undefined' instead.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('omit_empty')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LazyListValueOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.LazyStringValueOptions", jsii_struct_bases=[], name_mapping={'display_hint': 'displayHint'})
class LazyStringValueOptions():
    def __init__(self, *, display_hint: typing.Optional[str]=None) -> None:
        """Options for creating a lazy string token.

        :param display_hint: Use the given name as a display hint. Default: - No hint

        stability
        :stability: experimental
        """
        self._values = {
        }
        if display_hint is not None: self._values["display_hint"] = display_hint

    @builtins.property
    def display_hint(self) -> typing.Optional[str]:
        """Use the given name as a display hint.

        default
        :default: - No hint

        stability
        :stability: experimental
        """
        return self._values.get('display_hint')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LazyStringValueOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IStackSynthesizer)
class LegacyStackSynthesizer(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.LegacyStackSynthesizer"):
    """Use the original deployment environment.

    This deployment environment is restricted in cross-environment deployments,
    CI/CD deployments, and will use up CloudFormation parameters in your template.

    This is the only StackSynthesizer that supports customizing asset behavior
    by overriding ``Stack.addFileAsset()`` and ``Stack.addDockerImageAsset()``.

    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        jsii.create(LegacyStackSynthesizer, self, [])

    @jsii.member(jsii_name="addDockerImageAsset")
    def add_docker_image_asset(self, *, directory_name: str, source_hash: str, docker_build_args: typing.Optional[typing.Mapping[str, str]]=None, docker_build_target: typing.Optional[str]=None, docker_file: typing.Optional[str]=None, repository_name: typing.Optional[str]=None) -> "DockerImageAssetLocation":
        """Register a Docker Image Asset.

        Returns the parameters that can be used to refer to the asset inside the template.

        :param directory_name: The directory where the Dockerfile is stored, must be relative to the cloud assembly root.
        :param source_hash: The hash of the contents of the docker build context. This hash is used throughout the system to identify this image and avoid duplicate work in case the source did not change. NOTE: this means that if you wish to update your docker image, you must make a modification to the source (e.g. add some metadata to your Dockerfile).
        :param docker_build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param docker_build_target: Docker target to build to. Default: - no target
        :param docker_file: Path to the Dockerfile (relative to the directory). Default: - no file
        :param repository_name: ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - automatically derived from the asset's ID.

        stability
        :stability: experimental
        """
        asset = DockerImageAssetSource(directory_name=directory_name, source_hash=source_hash, docker_build_args=docker_build_args, docker_build_target=docker_build_target, docker_file=docker_file, repository_name=repository_name)

        return jsii.invoke(self, "addDockerImageAsset", [asset])

    @jsii.member(jsii_name="addFileAsset")
    def add_file_asset(self, *, file_name: str, packaging: "FileAssetPackaging", source_hash: str) -> "FileAssetLocation":
        """Register a File Asset.

        Returns the parameters that can be used to refer to the asset inside the template.

        :param file_name: The path, relative to the root of the cloud assembly, in which this asset source resides. This can be a path to a file or a directory, dependning on the packaging type.
        :param packaging: Which type of packaging to perform.
        :param source_hash: A hash on the content source. This hash is used to uniquely identify this asset throughout the system. If this value doesn't change, the asset will not be rebuilt or republished.

        stability
        :stability: experimental
        """
        asset = FileAssetSource(file_name=file_name, packaging=packaging, source_hash=source_hash)

        return jsii.invoke(self, "addFileAsset", [asset])

    @jsii.member(jsii_name="bind")
    def bind(self, stack: "Stack") -> None:
        """Bind to the stack this environment is going to be used on.

        Must be called before any of the other methods are called.

        :param stack: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [stack])

    @jsii.member(jsii_name="synthesizeStackArtifacts")
    def synthesize_stack_artifacts(self, session: "ISynthesisSession") -> None:
        """Synthesize all artifacts required for the stack into the session.

        :param session: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeStackArtifacts", [session])


@jsii.data_type(jsii_type="monocdk-experiment.NestedStackProps", jsii_struct_bases=[], name_mapping={'notification_arns': 'notificationArns', 'parameters': 'parameters', 'timeout': 'timeout'})
class NestedStackProps():
    def __init__(self, *, notification_arns: typing.Optional[typing.List[str]]=None, parameters: typing.Optional[typing.Mapping[str, str]]=None, timeout: typing.Optional["Duration"]=None) -> None:
        """Initialization props for the ``NestedStack`` construct.

        :param notification_arns: The Simple Notification Service (SNS) topics to publish stack related events. Default: - notifications are not sent for this stack.
        :param parameters: The set value pairs that represent the parameters passed to CloudFormation when this nested stack is created. Each parameter has a name corresponding to a parameter defined in the embedded template and a value representing the value that you want to set for the parameter. The nested stack construct will automatically synthesize parameters in order to bind references from the parent stack(s) into the nested stack. Default: - no user-defined parameters are passed to the nested stack
        :param timeout: The length of time that CloudFormation waits for the nested stack to reach the CREATE_COMPLETE state. When CloudFormation detects that the nested stack has reached the CREATE_COMPLETE state, it marks the nested stack resource as CREATE_COMPLETE in the parent stack and resumes creating the parent stack. If the timeout period expires before the nested stack reaches CREATE_COMPLETE, CloudFormation marks the nested stack as failed and rolls back both the nested stack and parent stack. Default: - no timeout

        stability
        :stability: experimental
        """
        self._values = {
        }
        if notification_arns is not None: self._values["notification_arns"] = notification_arns
        if parameters is not None: self._values["parameters"] = parameters
        if timeout is not None: self._values["timeout"] = timeout

    @builtins.property
    def notification_arns(self) -> typing.Optional[typing.List[str]]:
        """The Simple Notification Service (SNS) topics to publish stack related events.

        default
        :default: - notifications are not sent for this stack.

        stability
        :stability: experimental
        """
        return self._values.get('notification_arns')

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The set value pairs that represent the parameters passed to CloudFormation when this nested stack is created.

        Each parameter has a name corresponding
        to a parameter defined in the embedded template and a value representing
        the value that you want to set for the parameter.

        The nested stack construct will automatically synthesize parameters in order
        to bind references from the parent stack(s) into the nested stack.

        default
        :default: - no user-defined parameters are passed to the nested stack

        stability
        :stability: experimental
        """
        return self._values.get('parameters')

    @builtins.property
    def timeout(self) -> typing.Optional["Duration"]:
        """The length of time that CloudFormation waits for the nested stack to reach the CREATE_COMPLETE state.

        When CloudFormation detects that the nested stack has reached the
        CREATE_COMPLETE state, it marks the nested stack resource as
        CREATE_COMPLETE in the parent stack and resumes creating the parent stack.
        If the timeout period expires before the nested stack reaches
        CREATE_COMPLETE, CloudFormation marks the nested stack as failed and rolls
        back both the nested stack and parent stack.

        default
        :default: - no timeout

        stability
        :stability: experimental
        """
        return self._values.get('timeout')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NestedStackProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IStackSynthesizer)
class NestedStackSynthesizer(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.NestedStackSynthesizer"):
    """Deployment environment for a nested stack.

    Interoperates with the StackSynthesizer of the parent stack.

    stability
    :stability: experimental
    """
    def __init__(self, parent_deployment: "IStackSynthesizer") -> None:
        """
        :param parent_deployment: -

        stability
        :stability: experimental
        """
        jsii.create(NestedStackSynthesizer, self, [parent_deployment])

    @jsii.member(jsii_name="addDockerImageAsset")
    def add_docker_image_asset(self, *, directory_name: str, source_hash: str, docker_build_args: typing.Optional[typing.Mapping[str, str]]=None, docker_build_target: typing.Optional[str]=None, docker_file: typing.Optional[str]=None, repository_name: typing.Optional[str]=None) -> "DockerImageAssetLocation":
        """Register a Docker Image Asset.

        Returns the parameters that can be used to refer to the asset inside the template.

        :param directory_name: The directory where the Dockerfile is stored, must be relative to the cloud assembly root.
        :param source_hash: The hash of the contents of the docker build context. This hash is used throughout the system to identify this image and avoid duplicate work in case the source did not change. NOTE: this means that if you wish to update your docker image, you must make a modification to the source (e.g. add some metadata to your Dockerfile).
        :param docker_build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param docker_build_target: Docker target to build to. Default: - no target
        :param docker_file: Path to the Dockerfile (relative to the directory). Default: - no file
        :param repository_name: ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - automatically derived from the asset's ID.

        stability
        :stability: experimental
        """
        asset = DockerImageAssetSource(directory_name=directory_name, source_hash=source_hash, docker_build_args=docker_build_args, docker_build_target=docker_build_target, docker_file=docker_file, repository_name=repository_name)

        return jsii.invoke(self, "addDockerImageAsset", [asset])

    @jsii.member(jsii_name="addFileAsset")
    def add_file_asset(self, *, file_name: str, packaging: "FileAssetPackaging", source_hash: str) -> "FileAssetLocation":
        """Register a File Asset.

        Returns the parameters that can be used to refer to the asset inside the template.

        :param file_name: The path, relative to the root of the cloud assembly, in which this asset source resides. This can be a path to a file or a directory, dependning on the packaging type.
        :param packaging: Which type of packaging to perform.
        :param source_hash: A hash on the content source. This hash is used to uniquely identify this asset throughout the system. If this value doesn't change, the asset will not be rebuilt or republished.

        stability
        :stability: experimental
        """
        asset = FileAssetSource(file_name=file_name, packaging=packaging, source_hash=source_hash)

        return jsii.invoke(self, "addFileAsset", [asset])

    @jsii.member(jsii_name="bind")
    def bind(self, _stack: "Stack") -> None:
        """Bind to the stack this environment is going to be used on.

        Must be called before any of the other methods are called.

        :param _stack: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_stack])

    @jsii.member(jsii_name="synthesizeStackArtifacts")
    def synthesize_stack_artifacts(self, _session: "ISynthesisSession") -> None:
        """Synthesize all artifacts required for the stack into the session.

        :param _session: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeStackArtifacts", [_session])


class PhysicalName(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.PhysicalName"):
    """Includes special markers for automatic generation of physical names.

    stability
    :stability: experimental
    """
    @jsii.python.classproperty
    @jsii.member(jsii_name="GENERATE_IF_NEEDED")
    def GENERATE_IF_NEEDED(cls) -> str:
        """Use this to automatically generate a physical name for an AWS resource only if the resource is referenced across environments (account/region).

        Otherwise, the name will be allocated during deployment by CloudFormation.

        If you are certain that a resource will be referenced across environments,
        you may also specify an explicit physical name for it. This option is
        mostly designed for reusable constructs which may or may not be referenced
        acrossed environments.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "GENERATE_IF_NEEDED")


class Reference(Intrinsic, metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.Reference"):
    """An intrinsic Token that represents a reference to a construct.

    References are recorded.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ReferenceProxy

    def __init__(self, value: typing.Any, target: "IConstruct", display_name: typing.Optional[str]=None) -> None:
        """
        :param value: -
        :param target: -
        :param display_name: -

        stability
        :stability: experimental
        """
        jsii.create(Reference, self, [value, target, display_name])

    @jsii.member(jsii_name="isReference")
    @builtins.classmethod
    def is_reference(cls, x: typing.Any) -> bool:
        """Check whether this is actually a Reference.

        :param x: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "isReference", [x])

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "displayName")

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "IConstruct":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "target")


class _ReferenceProxy(Reference):
    pass

@jsii.enum(jsii_type="monocdk-experiment.RemovalPolicy")
class RemovalPolicy(enum.Enum):
    """
    stability
    :stability: experimental
    """
    DESTROY = "DESTROY"
    """This is the default removal policy.

    It means that when the resource is
    removed from the app, it will be physically destroyed.

    stability
    :stability: experimental
    """
    RETAIN = "RETAIN"
    """This uses the 'Retain' DeletionPolicy, which will cause the resource to be retained in the account, but orphaned from the stack.

    stability
    :stability: experimental
    """
    SNAPSHOT = "SNAPSHOT"
    """This retention policy deletes the resource, but saves a snapshot of its data before deleting, so that it can be re-created later.

    Only available for some stateful resources,
    like databases, EFS volumes, etc.

    see
    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html#aws-attribute-deletionpolicy-options
    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.RemovalPolicyOptions", jsii_struct_bases=[], name_mapping={'apply_to_update_replace_policy': 'applyToUpdateReplacePolicy', 'default': 'default'})
class RemovalPolicyOptions():
    def __init__(self, *, apply_to_update_replace_policy: typing.Optional[bool]=None, default: typing.Optional["RemovalPolicy"]=None) -> None:
        """
        :param apply_to_update_replace_policy: Apply the same deletion policy to the resource's "UpdateReplacePolicy". Default: true
        :param default: The default policy to apply in case the removal policy is not defined. Default: - Default value is resource specific. To determine the default value for a resoure, please consult that specific resource's documentation.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if apply_to_update_replace_policy is not None: self._values["apply_to_update_replace_policy"] = apply_to_update_replace_policy
        if default is not None: self._values["default"] = default

    @builtins.property
    def apply_to_update_replace_policy(self) -> typing.Optional[bool]:
        """Apply the same deletion policy to the resource's "UpdateReplacePolicy".

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('apply_to_update_replace_policy')

    @builtins.property
    def default(self) -> typing.Optional["RemovalPolicy"]:
        """The default policy to apply in case the removal policy is not defined.

        default
        :default:

        - Default value is resource specific. To determine the default value for a resoure,
          please consult that specific resource's documentation.

        stability
        :stability: experimental
        """
        return self._values.get('default')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RemovalPolicyOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IAspect)
class RemoveTag(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.RemoveTag"):
    """The RemoveTag Aspect will handle removing tags from this node and children.

    stability
    :stability: experimental
    """
    def __init__(self, key: str, *, apply_to_launched_instances: typing.Optional[bool]=None, exclude_resource_types: typing.Optional[typing.List[str]]=None, include_resource_types: typing.Optional[typing.List[str]]=None, priority: typing.Optional[jsii.Number]=None) -> None:
        """
        :param key: -
        :param apply_to_launched_instances: Whether the tag should be applied to instances in an AutoScalingGroup. Default: true
        :param exclude_resource_types: An array of Resource Types that will not receive this tag. An empty array will allow this tag to be applied to all resources. A non-empty array will apply this tag only if the Resource type is not in this array. Default: []
        :param include_resource_types: An array of Resource Types that will receive this tag. An empty array will match any Resource. A non-empty array will apply this tag only to Resource types that are included in this array. Default: []
        :param priority: Priority of the tag operation. Higher or equal priority tags will take precedence. Setting priority will enable the user to control tags when they need to not follow the default precedence pattern of last applied and closest to the construct in the tree. Default: Default priorities: - 100 for {@link SetTag} - 200 for {@link RemoveTag} - 50 for tags added directly to CloudFormation resources

        stability
        :stability: experimental
        """
        props = TagProps(apply_to_launched_instances=apply_to_launched_instances, exclude_resource_types=exclude_resource_types, include_resource_types=include_resource_types, priority=priority)

        jsii.create(RemoveTag, self, [key, props])

    @jsii.member(jsii_name="applyTag")
    def _apply_tag(self, resource: "ITaggable") -> None:
        """
        :param resource: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "applyTag", [resource])

    @jsii.member(jsii_name="visit")
    def visit(self, construct: "IConstruct") -> None:
        """All aspects can visit an IConstruct.

        :param construct: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "visit", [construct])

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> str:
        """The string key for the tag.

        stability
        :stability: experimental
        """
        return jsii.get(self, "key")

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "TagProps":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "props")


@jsii.data_type(jsii_type="monocdk-experiment.ResolveOptions", jsii_struct_bases=[], name_mapping={'resolver': 'resolver', 'scope': 'scope', 'preparing': 'preparing'})
class ResolveOptions():
    def __init__(self, *, resolver: "ITokenResolver", scope: "IConstruct", preparing: typing.Optional[bool]=None) -> None:
        """Options to the resolve() operation.

        NOT the same as the ResolveContext; ResolveContext is exposed to Token
        implementors and resolution hooks, whereas this struct is just to bundle
        a number of things that would otherwise be arguments to resolve() in a
        readable way.

        :param resolver: The resolver to apply to any resolvable tokens found.
        :param scope: The scope from which resolution is performed.
        :param preparing: Whether the resolution is being executed during the prepare phase or not. Default: false

        stability
        :stability: experimental
        """
        self._values = {
            'resolver': resolver,
            'scope': scope,
        }
        if preparing is not None: self._values["preparing"] = preparing

    @builtins.property
    def resolver(self) -> "ITokenResolver":
        """The resolver to apply to any resolvable tokens found.

        stability
        :stability: experimental
        """
        return self._values.get('resolver')

    @builtins.property
    def scope(self) -> "IConstruct":
        """The scope from which resolution is performed.

        stability
        :stability: experimental
        """
        return self._values.get('scope')

    @builtins.property
    def preparing(self) -> typing.Optional[bool]:
        """Whether the resolution is being executed during the prepare phase or not.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('preparing')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ResolveOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.ResourceProps", jsii_struct_bases=[], name_mapping={'physical_name': 'physicalName'})
class ResourceProps():
    def __init__(self, *, physical_name: typing.Optional[str]=None) -> None:
        """Construction properties for {@link Resource}.

        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time

        stability
        :stability: experimental
        """
        self._values = {
        }
        if physical_name is not None: self._values["physical_name"] = physical_name

    @builtins.property
    def physical_name(self) -> typing.Optional[str]:
        """The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        default
        :default: - The physical name will be allocated by CloudFormation at deployment time

        stability
        :stability: experimental
        """
        return self._values.get('physical_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ResourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ScopedAws(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.ScopedAws"):
    """Accessor for scoped pseudo parameters.

    These pseudo parameters are anchored to a stack somewhere in the construct
    tree, and their values will be exported automatically.

    stability
    :stability: experimental
    """
    def __init__(self, scope: "Construct") -> None:
        """
        :param scope: -

        stability
        :stability: experimental
        """
        jsii.create(ScopedAws, self, [scope])

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "accountId")

    @builtins.property
    @jsii.member(jsii_name="notificationArns")
    def notification_arns(self) -> typing.List[str]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "notificationArns")

    @builtins.property
    @jsii.member(jsii_name="partition")
    def partition(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "partition")

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "region")

    @builtins.property
    @jsii.member(jsii_name="stackId")
    def stack_id(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "stackId")

    @builtins.property
    @jsii.member(jsii_name="stackName")
    def stack_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "stackName")

    @builtins.property
    @jsii.member(jsii_name="urlSuffix")
    def url_suffix(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "urlSuffix")


class SecretValue(Intrinsic, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.SecretValue"):
    """Work with secret values in the CDK.

    Secret values in the CDK (such as those retrieved from SecretsManager) are
    represented as regular strings, just like other values that are only
    available at deployment time.

    To help you avoid accidental mistakes which would lead to you putting your
    secret values directly into a CloudFormation template, constructs that take
    secret values will not allow you to pass in a literal secret value. They do
    so by calling ``Secret.assertSafeSecret()``.

    You can escape the check by calling ``Secret.plainText()``, but doing
    so is highly discouraged.

    stability
    :stability: experimental
    """
    def __init__(self, value: typing.Any) -> None:
        """
        :param value: -

        stability
        :stability: experimental
        """
        jsii.create(SecretValue, self, [value])

    @jsii.member(jsii_name="cfnDynamicReference")
    @builtins.classmethod
    def cfn_dynamic_reference(cls, ref: "CfnDynamicReference") -> "SecretValue":
        """Obtain the secret value through a CloudFormation dynamic reference.

        If possible, use ``SecretValue.ssmSecure`` or ``SecretValue.secretsManager`` directly.

        :param ref: The dynamic reference to use.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "cfnDynamicReference", [ref])

    @jsii.member(jsii_name="cfnParameter")
    @builtins.classmethod
    def cfn_parameter(cls, param: "CfnParameter") -> "SecretValue":
        """Obtain the secret value through a CloudFormation parameter.

        Generally, this is not a recommended approach. AWS Secrets Manager is the
        recommended way to reference secrets.

        :param param: The CloudFormation parameter to use.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "cfnParameter", [param])

    @jsii.member(jsii_name="plainText")
    @builtins.classmethod
    def plain_text(cls, secret: str) -> "SecretValue":
        """Construct a literal secret value for use with secret-aware constructs.

        *Do not use this method for any secrets that you care about.*

        The only reasonable use case for using this method is when you are testing.

        :param secret: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "plainText", [secret])

    @jsii.member(jsii_name="secretsManager")
    @builtins.classmethod
    def secrets_manager(cls, secret_id: str, *, json_field: typing.Optional[str]=None, version_id: typing.Optional[str]=None, version_stage: typing.Optional[str]=None) -> "SecretValue":
        """Creates a ``SecretValue`` with a value which is dynamically loaded from AWS Secrets Manager.

        :param secret_id: The ID or ARN of the secret.
        :param json_field: The key of a JSON field to retrieve. This can only be used if the secret stores a JSON object. Default: - returns all the content stored in the Secrets Manager secret.
        :param version_id: Specifies the unique identifier of the version of the secret you want to use. Can specify at most one of ``versionId`` and ``versionStage``. Default: AWSCURRENT
        :param version_stage: Specified the secret version that you want to retrieve by the staging label attached to the version. Can specify at most one of ``versionId`` and ``versionStage``. Default: AWSCURRENT

        stability
        :stability: experimental
        """
        options = SecretsManagerSecretOptions(json_field=json_field, version_id=version_id, version_stage=version_stage)

        return jsii.sinvoke(cls, "secretsManager", [secret_id, options])

    @jsii.member(jsii_name="ssmSecure")
    @builtins.classmethod
    def ssm_secure(cls, parameter_name: str, version: str) -> "SecretValue":
        """Use a secret value stored from a Systems Manager (SSM) parameter.

        :param parameter_name: The name of the parameter in the Systems Manager Parameter Store. The parameter name is case-sensitive.
        :param version: An integer that specifies the version of the parameter to use. You must specify the exact version. You cannot currently specify that AWS CloudFormation use the latest version of a parameter.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "ssmSecure", [parameter_name, version])


@jsii.data_type(jsii_type="monocdk-experiment.SecretsManagerSecretOptions", jsii_struct_bases=[], name_mapping={'json_field': 'jsonField', 'version_id': 'versionId', 'version_stage': 'versionStage'})
class SecretsManagerSecretOptions():
    def __init__(self, *, json_field: typing.Optional[str]=None, version_id: typing.Optional[str]=None, version_stage: typing.Optional[str]=None) -> None:
        """Options for referencing a secret value from Secrets Manager.

        :param json_field: The key of a JSON field to retrieve. This can only be used if the secret stores a JSON object. Default: - returns all the content stored in the Secrets Manager secret.
        :param version_id: Specifies the unique identifier of the version of the secret you want to use. Can specify at most one of ``versionId`` and ``versionStage``. Default: AWSCURRENT
        :param version_stage: Specified the secret version that you want to retrieve by the staging label attached to the version. Can specify at most one of ``versionId`` and ``versionStage``. Default: AWSCURRENT

        stability
        :stability: experimental
        """
        self._values = {
        }
        if json_field is not None: self._values["json_field"] = json_field
        if version_id is not None: self._values["version_id"] = version_id
        if version_stage is not None: self._values["version_stage"] = version_stage

    @builtins.property
    def json_field(self) -> typing.Optional[str]:
        """The key of a JSON field to retrieve.

        This can only be used if the secret
        stores a JSON object.

        default
        :default: - returns all the content stored in the Secrets Manager secret.

        stability
        :stability: experimental
        """
        return self._values.get('json_field')

    @builtins.property
    def version_id(self) -> typing.Optional[str]:
        """Specifies the unique identifier of the version of the secret you want to use.

        Can specify at most one of ``versionId`` and ``versionStage``.

        default
        :default: AWSCURRENT

        stability
        :stability: experimental
        """
        return self._values.get('version_id')

    @builtins.property
    def version_stage(self) -> typing.Optional[str]:
        """Specified the secret version that you want to retrieve by the staging label attached to the version.

        Can specify at most one of ``versionId`` and ``versionStage``.

        default
        :default: AWSCURRENT

        stability
        :stability: experimental
        """
        return self._values.get('version_stage')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SecretsManagerSecretOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Size(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.Size"):
    """Represents the amount of digital storage.

    The amount can be specified either as a literal value (e.g: ``10``) which
    cannot be negative, or as an unresolved number token.

    When the amount is passed as a token, unit conversion is not possible.

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="gibibytes")
    @builtins.classmethod
    def gibibytes(cls, amount: jsii.Number) -> "Size":
        """Create a Storage representing an amount gibibytes.

        1 GiB = 1024 MiB

        :param amount: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "gibibytes", [amount])

    @jsii.member(jsii_name="kibibytes")
    @builtins.classmethod
    def kibibytes(cls, amount: jsii.Number) -> "Size":
        """Create a Storage representing an amount kibibytes.

        1 KiB = 1024 bytes

        :param amount: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "kibibytes", [amount])

    @jsii.member(jsii_name="mebibytes")
    @builtins.classmethod
    def mebibytes(cls, amount: jsii.Number) -> "Size":
        """Create a Storage representing an amount mebibytes.

        1 MiB = 1024 KiB

        :param amount: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "mebibytes", [amount])

    @jsii.member(jsii_name="pebibyte")
    @builtins.classmethod
    def pebibyte(cls, amount: jsii.Number) -> "Size":
        """Create a Storage representing an amount pebibytes.

        1 PiB = 1024 TiB

        :param amount: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "pebibyte", [amount])

    @jsii.member(jsii_name="tebibytes")
    @builtins.classmethod
    def tebibytes(cls, amount: jsii.Number) -> "Size":
        """Create a Storage representing an amount tebibytes.

        1 TiB = 1024 GiB

        :param amount: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "tebibytes", [amount])

    @jsii.member(jsii_name="toGibibytes")
    def to_gibibytes(self, *, rounding: typing.Optional["SizeRoundingBehavior"]=None) -> jsii.Number:
        """Return this storage as a total number of gibibytes.

        :param rounding: How conversions should behave when it encounters a non-integer result. Default: SizeRoundingBehavior.FAIL

        stability
        :stability: experimental
        """
        opts = SizeConversionOptions(rounding=rounding)

        return jsii.invoke(self, "toGibibytes", [opts])

    @jsii.member(jsii_name="toKibibytes")
    def to_kibibytes(self, *, rounding: typing.Optional["SizeRoundingBehavior"]=None) -> jsii.Number:
        """Return this storage as a total number of kibibytes.

        :param rounding: How conversions should behave when it encounters a non-integer result. Default: SizeRoundingBehavior.FAIL

        stability
        :stability: experimental
        """
        opts = SizeConversionOptions(rounding=rounding)

        return jsii.invoke(self, "toKibibytes", [opts])

    @jsii.member(jsii_name="toMebibytes")
    def to_mebibytes(self, *, rounding: typing.Optional["SizeRoundingBehavior"]=None) -> jsii.Number:
        """Return this storage as a total number of mebibytes.

        :param rounding: How conversions should behave when it encounters a non-integer result. Default: SizeRoundingBehavior.FAIL

        stability
        :stability: experimental
        """
        opts = SizeConversionOptions(rounding=rounding)

        return jsii.invoke(self, "toMebibytes", [opts])

    @jsii.member(jsii_name="toPebibytes")
    def to_pebibytes(self, *, rounding: typing.Optional["SizeRoundingBehavior"]=None) -> jsii.Number:
        """Return this storage as a total number of pebibytes.

        :param rounding: How conversions should behave when it encounters a non-integer result. Default: SizeRoundingBehavior.FAIL

        stability
        :stability: experimental
        """
        opts = SizeConversionOptions(rounding=rounding)

        return jsii.invoke(self, "toPebibytes", [opts])

    @jsii.member(jsii_name="toTebibytes")
    def to_tebibytes(self, *, rounding: typing.Optional["SizeRoundingBehavior"]=None) -> jsii.Number:
        """Return this storage as a total number of tebibytes.

        :param rounding: How conversions should behave when it encounters a non-integer result. Default: SizeRoundingBehavior.FAIL

        stability
        :stability: experimental
        """
        opts = SizeConversionOptions(rounding=rounding)

        return jsii.invoke(self, "toTebibytes", [opts])


@jsii.data_type(jsii_type="monocdk-experiment.SizeConversionOptions", jsii_struct_bases=[], name_mapping={'rounding': 'rounding'})
class SizeConversionOptions():
    def __init__(self, *, rounding: typing.Optional["SizeRoundingBehavior"]=None) -> None:
        """Options for how to convert time to a different unit.

        :param rounding: How conversions should behave when it encounters a non-integer result. Default: SizeRoundingBehavior.FAIL

        stability
        :stability: experimental
        """
        self._values = {
        }
        if rounding is not None: self._values["rounding"] = rounding

    @builtins.property
    def rounding(self) -> typing.Optional["SizeRoundingBehavior"]:
        """How conversions should behave when it encounters a non-integer result.

        default
        :default: SizeRoundingBehavior.FAIL

        stability
        :stability: experimental
        """
        return self._values.get('rounding')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SizeConversionOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.SizeRoundingBehavior")
class SizeRoundingBehavior(enum.Enum):
    """Rounding behaviour when converting between units of ``Size``.

    stability
    :stability: experimental
    """
    FAIL = "FAIL"
    """Fail the conversion if the result is not an integer.

    stability
    :stability: experimental
    """
    FLOOR = "FLOOR"
    """If the result is not an integer, round it to the closest integer less than the result.

    stability
    :stability: experimental
    """
    NONE = "NONE"
    """Don't round.

    Return even if the result is a fraction.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.StackProps", jsii_struct_bases=[], name_mapping={'description': 'description', 'env': 'env', 'stack_name': 'stackName', 'synthesizer': 'synthesizer', 'tags': 'tags', 'termination_protection': 'terminationProtection'})
class StackProps():
    def __init__(self, *, description: typing.Optional[str]=None, env: typing.Optional["Environment"]=None, stack_name: typing.Optional[str]=None, synthesizer: typing.Optional["IStackSynthesizer"]=None, tags: typing.Optional[typing.Mapping[str, str]]=None, termination_protection: typing.Optional[bool]=None) -> None:
        """
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false

        stability
        :stability: experimental
        """
        if isinstance(env, dict): env = Environment(**env)
        self._values = {
        }
        if description is not None: self._values["description"] = description
        if env is not None: self._values["env"] = env
        if stack_name is not None: self._values["stack_name"] = stack_name
        if synthesizer is not None: self._values["synthesizer"] = synthesizer
        if tags is not None: self._values["tags"] = tags
        if termination_protection is not None: self._values["termination_protection"] = termination_protection

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the stack.

        default
        :default: - No description.

        stability
        :stability: experimental
        """
        return self._values.get('description')

    @builtins.property
    def env(self) -> typing.Optional["Environment"]:
        """The AWS environment (account/region) where this stack will be deployed.

        Set the ``region``/``account`` fields of ``env`` to either a concrete value to
        select the indicated environment (recommended for production stacks), or to
        the values of environment variables
        ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment
        depend on the AWS credentials/configuration that the CDK CLI is executed
        under (recommended for development stacks).

        If the ``Stack`` is instantiated inside a ``Stage``, any undefined
        ``region``/``account`` fields from ``env`` will default to the same field on the
        encompassing ``Stage``, if configured there.

        If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the
        Stack will be considered "*environment-agnostic*"". Environment-agnostic
        stacks can be deployed to any environment but may not be able to take
        advantage of all features of the CDK. For example, they will not be able to
        use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not
        automatically translate Service Principals to the right format based on the
        environment's AWS partition, and other such enhancements.

        default
        :default:

        - The environment of the containing ``Stage`` if available,
          otherwise create the stack will be environment-agnostic.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            # Use a concrete account and region to deploy this stack to:
            # `.account` and `.region` will simply return these values.
            MyStack(app, "Stack1",
                env={
                    "account": "123456789012",
                    "region": "us-east-1"
                }
            )
            
            # Use the CLI's current credentials to determine the target environment:
            # `.account` and `.region` will reflect the account+region the CLI
            # is configured to use (based on the user CLI credentials)
            MyStack(app, "Stack2",
                env={
                    "account": process.env.CDK_DEFAULT_ACCOUNT,
                    "region": process.env.CDK_DEFAULT_REGION
                }
            )
            
            # Define multiple stacks stage associated with an environment
            my_stage = Stage(app, "MyStage",
                env={
                    "account": "123456789012",
                    "region": "us-east-1"
                }
            )
            
            # both of these stavks will use the stage's account/region:
            # `.account` and `.region` will resolve to the concrete values as above
            MyStack(my_stage, "Stack1")
            YourStack(my_stage, "Stack1")
            
            # Define an environment-agnostic stack:
            # `.account` and `.region` will resolve to `{ "Ref": "AWS::AccountId" }` and `{ "Ref": "AWS::Region" }` respectively.
            # which will only resolve to actual values by CloudFormation during deployment.
            MyStack(app, "Stack1")
        """
        return self._values.get('env')

    @builtins.property
    def stack_name(self) -> typing.Optional[str]:
        """Name to deploy the stack with.

        default
        :default: - Derived from construct path.

        stability
        :stability: experimental
        """
        return self._values.get('stack_name')

    @builtins.property
    def synthesizer(self) -> typing.Optional["IStackSynthesizer"]:
        """Synthesis method to use while deploying this stack.

        default
        :default:

        - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag
          is set, ``LegacyStackSynthesizer`` otherwise.

        stability
        :stability: experimental
        """
        return self._values.get('synthesizer')

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Stack tags that will be applied to all the taggable resources and the stack itself.

        default
        :default: {}

        stability
        :stability: experimental
        """
        return self._values.get('tags')

    @builtins.property
    def termination_protection(self) -> typing.Optional[bool]:
        """Whether to enable termination protection for this stack.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('termination_protection')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StackProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.StageProps", jsii_struct_bases=[], name_mapping={'env': 'env', 'outdir': 'outdir'})
class StageProps():
    def __init__(self, *, env: typing.Optional["Environment"]=None, outdir: typing.Optional[str]=None) -> None:
        """Initialization props for a stage.

        :param env: Default AWS environment (account/region) for ``Stack``s in this ``Stage``. Stacks defined inside this ``Stage`` with either ``region`` or ``account`` missing from its env will use the corresponding field given here. If either ``region`` or ``account``is is not configured for ``Stack`` (either on the ``Stack`` itself or on the containing ``Stage``), the Stack will be *environment-agnostic*. Environment-agnostic stacks can be deployed to any environment, may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups, will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environments should be configured on the ``Stack``s.
        :param outdir: The output directory into which to emit synthesized artifacts. Can only be specified if this stage is the root stage (the app). If this is specified and this stage is nested within another stage, an error will be thrown. Default: - for nested stages, outdir will be determined as a relative directory to the outdir of the app. For apps, if outdir is not specified, a temporary directory will be created.

        stability
        :stability: experimental
        """
        if isinstance(env, dict): env = Environment(**env)
        self._values = {
        }
        if env is not None: self._values["env"] = env
        if outdir is not None: self._values["outdir"] = outdir

    @builtins.property
    def env(self) -> typing.Optional["Environment"]:
        """Default AWS environment (account/region) for ``Stack``s in this ``Stage``.

        Stacks defined inside this ``Stage`` with either ``region`` or ``account`` missing
        from its env will use the corresponding field given here.

        If either ``region`` or ``account``is is not configured for ``Stack`` (either on
        the ``Stack`` itself or on the containing ``Stage``), the Stack will be
        *environment-agnostic*.

        Environment-agnostic stacks can be deployed to any environment, may not be
        able to take advantage of all features of the CDK. For example, they will
        not be able to use environmental context lookups, will not automatically
        translate Service Principals to the right format based on the environment's
        AWS partition, and other such enhancements.

        default
        :default: - The environments should be configured on the ``Stack``s.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            # Use a concrete account and region to deploy this Stage to
            MyStage(app, "Stage1",
                env={"account": "123456789012", "region": "us-east-1"}
            )
            
            # Use the CLI's current credentials to determine the target environment
            MyStage(app, "Stage2",
                env={"account": process.env.CDK_DEFAULT_ACCOUNT, "region": process.env.CDK_DEFAULT_REGION}
            )
        """
        return self._values.get('env')

    @builtins.property
    def outdir(self) -> typing.Optional[str]:
        """The output directory into which to emit synthesized artifacts.

        Can only be specified if this stage is the root stage (the app). If this is
        specified and this stage is nested within another stage, an error will be
        thrown.

        default
        :default:

        - for nested stages, outdir will be determined as a relative
          directory to the outdir of the app. For apps, if outdir is not specified, a
          temporary directory will be created.

        stability
        :stability: experimental
        """
        return self._values.get('outdir')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StageProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.StageSynthesisOptions", jsii_struct_bases=[], name_mapping={'skip_validation': 'skipValidation'})
class StageSynthesisOptions():
    def __init__(self, *, skip_validation: typing.Optional[bool]=None) -> None:
        """Options for assemly synthesis.

        :param skip_validation: Should we skip construct validation. Default: - false

        stability
        :stability: experimental
        """
        self._values = {
        }
        if skip_validation is not None: self._values["skip_validation"] = skip_validation

    @builtins.property
    def skip_validation(self) -> typing.Optional[bool]:
        """Should we skip construct validation.

        default
        :default: - false

        stability
        :stability: experimental
        """
        return self._values.get('skip_validation')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StageSynthesisOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IFragmentConcatenator)
class StringConcat(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.StringConcat"):
    """Converts all fragments to strings and concats those.

    Drops 'undefined's.

    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        jsii.create(StringConcat, self, [])

    @jsii.member(jsii_name="join")
    def join(self, left: typing.Any, right: typing.Any) -> typing.Any:
        """Join the fragment on the left and on the right.

        :param left: -
        :param right: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "join", [left, right])


@jsii.enum(jsii_type="monocdk-experiment.SymlinkFollowMode")
class SymlinkFollowMode(enum.Enum):
    """Determines how symlinks are followed.

    stability
    :stability: experimental
    """
    NEVER = "NEVER"
    """Never follow symlinks.

    stability
    :stability: experimental
    """
    ALWAYS = "ALWAYS"
    """Materialize all symlinks, whether they are internal or external to the source directory.

    stability
    :stability: experimental
    """
    EXTERNAL = "EXTERNAL"
    """Only follows symlinks that are external to the source directory.

    stability
    :stability: experimental
    """
    BLOCK_EXTERNAL = "BLOCK_EXTERNAL"
    """Forbids source from having any symlinks pointing outside of the source tree.

    This is the safest mode of operation as it ensures that copy operations
    won't materialize files from the user's file system. Internal symlinks are
    not followed.

    If the copy operation runs into an external symlink, it will fail.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.SynthesisOptions", jsii_struct_bases=[_AssemblyBuildOptions_44ebd659], name_mapping={'runtime_info': 'runtimeInfo', 'outdir': 'outdir', 'skip_validation': 'skipValidation'})
class SynthesisOptions(_AssemblyBuildOptions_44ebd659):
    def __init__(self, *, runtime_info: typing.Optional[_RuntimeInfo_b6d338e9]=None, outdir: typing.Optional[str]=None, skip_validation: typing.Optional[bool]=None) -> None:
        """Options for synthesis.

        :param runtime_info: Include the specified runtime information (module versions) in manifest. Default: - if this option is not specified, runtime info will not be included
        :param outdir: The output directory into which to synthesize the cloud assembly. Default: - creates a temporary directory
        :param skip_validation: Whether synthesis should skip the validation phase. Default: false

        deprecated
        :deprecated: use ``app.synth()`` or ``stage.synth()`` instead

        stability
        :stability: deprecated
        """
        if isinstance(runtime_info, dict): runtime_info = _RuntimeInfo_b6d338e9(**runtime_info)
        self._values = {
        }
        if runtime_info is not None: self._values["runtime_info"] = runtime_info
        if outdir is not None: self._values["outdir"] = outdir
        if skip_validation is not None: self._values["skip_validation"] = skip_validation

    @builtins.property
    def runtime_info(self) -> typing.Optional[_RuntimeInfo_b6d338e9]:
        """Include the specified runtime information (module versions) in manifest.

        default
        :default: - if this option is not specified, runtime info will not be included

        stability
        :stability: experimental
        """
        return self._values.get('runtime_info')

    @builtins.property
    def outdir(self) -> typing.Optional[str]:
        """The output directory into which to synthesize the cloud assembly.

        default
        :default: - creates a temporary directory

        stability
        :stability: deprecated
        """
        return self._values.get('outdir')

    @builtins.property
    def skip_validation(self) -> typing.Optional[bool]:
        """Whether synthesis should skip the validation phase.

        default
        :default: false

        stability
        :stability: deprecated
        """
        return self._values.get('skip_validation')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SynthesisOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IAspect)
class Tag(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.Tag"):
    """The Tag Aspect will handle adding a tag to this node and cascading tags to children.

    stability
    :stability: experimental
    """
    def __init__(self, key: str, value: str, *, apply_to_launched_instances: typing.Optional[bool]=None, exclude_resource_types: typing.Optional[typing.List[str]]=None, include_resource_types: typing.Optional[typing.List[str]]=None, priority: typing.Optional[jsii.Number]=None) -> None:
        """
        :param key: -
        :param value: -
        :param apply_to_launched_instances: Whether the tag should be applied to instances in an AutoScalingGroup. Default: true
        :param exclude_resource_types: An array of Resource Types that will not receive this tag. An empty array will allow this tag to be applied to all resources. A non-empty array will apply this tag only if the Resource type is not in this array. Default: []
        :param include_resource_types: An array of Resource Types that will receive this tag. An empty array will match any Resource. A non-empty array will apply this tag only to Resource types that are included in this array. Default: []
        :param priority: Priority of the tag operation. Higher or equal priority tags will take precedence. Setting priority will enable the user to control tags when they need to not follow the default precedence pattern of last applied and closest to the construct in the tree. Default: Default priorities: - 100 for {@link SetTag} - 200 for {@link RemoveTag} - 50 for tags added directly to CloudFormation resources

        stability
        :stability: experimental
        """
        props = TagProps(apply_to_launched_instances=apply_to_launched_instances, exclude_resource_types=exclude_resource_types, include_resource_types=include_resource_types, priority=priority)

        jsii.create(Tag, self, [key, value, props])

    @jsii.member(jsii_name="add")
    @builtins.classmethod
    def add(cls, scope: "Construct", key: str, value: str, *, apply_to_launched_instances: typing.Optional[bool]=None, exclude_resource_types: typing.Optional[typing.List[str]]=None, include_resource_types: typing.Optional[typing.List[str]]=None, priority: typing.Optional[jsii.Number]=None) -> None:
        """add tags to the node of a construct and all its the taggable children.

        :param scope: -
        :param key: -
        :param value: -
        :param apply_to_launched_instances: Whether the tag should be applied to instances in an AutoScalingGroup. Default: true
        :param exclude_resource_types: An array of Resource Types that will not receive this tag. An empty array will allow this tag to be applied to all resources. A non-empty array will apply this tag only if the Resource type is not in this array. Default: []
        :param include_resource_types: An array of Resource Types that will receive this tag. An empty array will match any Resource. A non-empty array will apply this tag only to Resource types that are included in this array. Default: []
        :param priority: Priority of the tag operation. Higher or equal priority tags will take precedence. Setting priority will enable the user to control tags when they need to not follow the default precedence pattern of last applied and closest to the construct in the tree. Default: Default priorities: - 100 for {@link SetTag} - 200 for {@link RemoveTag} - 50 for tags added directly to CloudFormation resources

        stability
        :stability: experimental
        """
        props = TagProps(apply_to_launched_instances=apply_to_launched_instances, exclude_resource_types=exclude_resource_types, include_resource_types=include_resource_types, priority=priority)

        return jsii.sinvoke(cls, "add", [scope, key, value, props])

    @jsii.member(jsii_name="remove")
    @builtins.classmethod
    def remove(cls, scope: "Construct", key: str, *, apply_to_launched_instances: typing.Optional[bool]=None, exclude_resource_types: typing.Optional[typing.List[str]]=None, include_resource_types: typing.Optional[typing.List[str]]=None, priority: typing.Optional[jsii.Number]=None) -> None:
        """remove tags to the node of a construct and all its the taggable children.

        :param scope: -
        :param key: -
        :param apply_to_launched_instances: Whether the tag should be applied to instances in an AutoScalingGroup. Default: true
        :param exclude_resource_types: An array of Resource Types that will not receive this tag. An empty array will allow this tag to be applied to all resources. A non-empty array will apply this tag only if the Resource type is not in this array. Default: []
        :param include_resource_types: An array of Resource Types that will receive this tag. An empty array will match any Resource. A non-empty array will apply this tag only to Resource types that are included in this array. Default: []
        :param priority: Priority of the tag operation. Higher or equal priority tags will take precedence. Setting priority will enable the user to control tags when they need to not follow the default precedence pattern of last applied and closest to the construct in the tree. Default: Default priorities: - 100 for {@link SetTag} - 200 for {@link RemoveTag} - 50 for tags added directly to CloudFormation resources

        stability
        :stability: experimental
        """
        props = TagProps(apply_to_launched_instances=apply_to_launched_instances, exclude_resource_types=exclude_resource_types, include_resource_types=include_resource_types, priority=priority)

        return jsii.sinvoke(cls, "remove", [scope, key, props])

    @jsii.member(jsii_name="applyTag")
    def _apply_tag(self, resource: "ITaggable") -> None:
        """
        :param resource: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "applyTag", [resource])

    @jsii.member(jsii_name="visit")
    def visit(self, construct: "IConstruct") -> None:
        """All aspects can visit an IConstruct.

        :param construct: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "visit", [construct])

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> str:
        """The string key for the tag.

        stability
        :stability: experimental
        """
        return jsii.get(self, "key")

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "TagProps":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "props")

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> str:
        """The string value of the tag.

        stability
        :stability: experimental
        """
        return jsii.get(self, "value")


class TagManager(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.TagManager"):
    """TagManager facilitates a common implementation of tagging for Constructs.

    stability
    :stability: experimental
    """
    def __init__(self, tag_type: "TagType", resource_type_name: str, tag_structure: typing.Any=None, *, tag_property_name: typing.Optional[str]=None) -> None:
        """
        :param tag_type: -
        :param resource_type_name: -
        :param tag_structure: -
        :param tag_property_name: The name of the property in CloudFormation for these tags. Normally this is ``tags``, but Cognito UserPool uses UserPoolTags Default: "tags"

        stability
        :stability: experimental
        """
        options = TagManagerOptions(tag_property_name=tag_property_name)

        jsii.create(TagManager, self, [tag_type, resource_type_name, tag_structure, options])

    @jsii.member(jsii_name="isTaggable")
    @builtins.classmethod
    def is_taggable(cls, construct: typing.Any) -> bool:
        """Check whether the given construct is Taggable.

        :param construct: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "isTaggable", [construct])

    @jsii.member(jsii_name="applyTagAspectHere")
    def apply_tag_aspect_here(self, include: typing.Optional[typing.List[str]]=None, exclude: typing.Optional[typing.List[str]]=None) -> bool:
        """Determine if the aspect applies here.

        Looks at the include and exclude resourceTypeName arrays to determine if
        the aspect applies here

        :param include: -
        :param exclude: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "applyTagAspectHere", [include, exclude])

    @jsii.member(jsii_name="hasTags")
    def has_tags(self) -> bool:
        """Returns true if there are any tags defined.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "hasTags", [])

    @jsii.member(jsii_name="removeTag")
    def remove_tag(self, key: str, priority: jsii.Number) -> None:
        """Removes the specified tag from the array if it exists.

        :param key: The tag to remove.
        :param priority: The priority of the remove operation.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "removeTag", [key, priority])

    @jsii.member(jsii_name="renderTags")
    def render_tags(self) -> typing.Any:
        """Renders tags into the proper format based on TagType.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "renderTags", [])

    @jsii.member(jsii_name="setTag")
    def set_tag(self, key: str, value: str, priority: typing.Optional[jsii.Number]=None, apply_to_launched_instances: typing.Optional[bool]=None) -> None:
        """Adds the specified tag to the array of tags.

        :param key: -
        :param value: -
        :param priority: -
        :param apply_to_launched_instances: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "setTag", [key, value, priority, apply_to_launched_instances])

    @builtins.property
    @jsii.member(jsii_name="tagPropertyName")
    def tag_property_name(self) -> str:
        """The property name for tag values.

        Normally this is ``tags`` but some resources choose a different name. Cognito
        UserPool uses UserPoolTags

        stability
        :stability: experimental
        """
        return jsii.get(self, "tagPropertyName")


@jsii.data_type(jsii_type="monocdk-experiment.TagManagerOptions", jsii_struct_bases=[], name_mapping={'tag_property_name': 'tagPropertyName'})
class TagManagerOptions():
    def __init__(self, *, tag_property_name: typing.Optional[str]=None) -> None:
        """Options to configure TagManager behavior.

        :param tag_property_name: The name of the property in CloudFormation for these tags. Normally this is ``tags``, but Cognito UserPool uses UserPoolTags Default: "tags"

        stability
        :stability: experimental
        """
        self._values = {
        }
        if tag_property_name is not None: self._values["tag_property_name"] = tag_property_name

    @builtins.property
    def tag_property_name(self) -> typing.Optional[str]:
        """The name of the property in CloudFormation for these tags.

        Normally this is ``tags``, but Cognito UserPool uses UserPoolTags

        default
        :default: "tags"

        stability
        :stability: experimental
        """
        return self._values.get('tag_property_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TagManagerOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.TagProps", jsii_struct_bases=[], name_mapping={'apply_to_launched_instances': 'applyToLaunchedInstances', 'exclude_resource_types': 'excludeResourceTypes', 'include_resource_types': 'includeResourceTypes', 'priority': 'priority'})
class TagProps():
    def __init__(self, *, apply_to_launched_instances: typing.Optional[bool]=None, exclude_resource_types: typing.Optional[typing.List[str]]=None, include_resource_types: typing.Optional[typing.List[str]]=None, priority: typing.Optional[jsii.Number]=None) -> None:
        """Properties for a tag.

        :param apply_to_launched_instances: Whether the tag should be applied to instances in an AutoScalingGroup. Default: true
        :param exclude_resource_types: An array of Resource Types that will not receive this tag. An empty array will allow this tag to be applied to all resources. A non-empty array will apply this tag only if the Resource type is not in this array. Default: []
        :param include_resource_types: An array of Resource Types that will receive this tag. An empty array will match any Resource. A non-empty array will apply this tag only to Resource types that are included in this array. Default: []
        :param priority: Priority of the tag operation. Higher or equal priority tags will take precedence. Setting priority will enable the user to control tags when they need to not follow the default precedence pattern of last applied and closest to the construct in the tree. Default: Default priorities: - 100 for {@link SetTag} - 200 for {@link RemoveTag} - 50 for tags added directly to CloudFormation resources

        stability
        :stability: experimental
        """
        self._values = {
        }
        if apply_to_launched_instances is not None: self._values["apply_to_launched_instances"] = apply_to_launched_instances
        if exclude_resource_types is not None: self._values["exclude_resource_types"] = exclude_resource_types
        if include_resource_types is not None: self._values["include_resource_types"] = include_resource_types
        if priority is not None: self._values["priority"] = priority

    @builtins.property
    def apply_to_launched_instances(self) -> typing.Optional[bool]:
        """Whether the tag should be applied to instances in an AutoScalingGroup.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('apply_to_launched_instances')

    @builtins.property
    def exclude_resource_types(self) -> typing.Optional[typing.List[str]]:
        """An array of Resource Types that will not receive this tag.

        An empty array will allow this tag to be applied to all resources. A
        non-empty array will apply this tag only if the Resource type is not in
        this array.

        default
        :default: []

        stability
        :stability: experimental
        """
        return self._values.get('exclude_resource_types')

    @builtins.property
    def include_resource_types(self) -> typing.Optional[typing.List[str]]:
        """An array of Resource Types that will receive this tag.

        An empty array will match any Resource. A non-empty array will apply this
        tag only to Resource types that are included in this array.

        default
        :default: []

        stability
        :stability: experimental
        """
        return self._values.get('include_resource_types')

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        """Priority of the tag operation.

        Higher or equal priority tags will take precedence.

        Setting priority will enable the user to control tags when they need to not
        follow the default precedence pattern of last applied and closest to the
        construct in the tree.

        default
        :default:

        Default priorities:

        - 100 for {@link SetTag}
        - 200 for {@link RemoveTag}
        - 50 for tags added directly to CloudFormation resources

        stability
        :stability: experimental
        """
        return self._values.get('priority')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TagProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.TagType")
class TagType(enum.Enum):
    """
    stability
    :stability: experimental
    """
    STANDARD = "STANDARD"
    """
    stability
    :stability: experimental
    """
    AUTOSCALING_GROUP = "AUTOSCALING_GROUP"
    """
    stability
    :stability: experimental
    """
    MAP = "MAP"
    """
    stability
    :stability: experimental
    """
    KEY_VALUE = "KEY_VALUE"
    """
    stability
    :stability: experimental
    """
    NOT_TAGGABLE = "NOT_TAGGABLE"
    """
    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.TimeConversionOptions", jsii_struct_bases=[], name_mapping={'integral': 'integral'})
class TimeConversionOptions():
    def __init__(self, *, integral: typing.Optional[bool]=None) -> None:
        """Options for how to convert time to a different unit.

        :param integral: If ``true``, conversions into a larger time unit (e.g. ``Seconds`` to ``Minutes``) will fail if the result is not an integer. Default: true

        stability
        :stability: experimental
        """
        self._values = {
        }
        if integral is not None: self._values["integral"] = integral

    @builtins.property
    def integral(self) -> typing.Optional[bool]:
        """If ``true``, conversions into a larger time unit (e.g. ``Seconds`` to ``Minutes``) will fail if the result is not an integer.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('integral')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TimeConversionOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Token(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.Token"):
    """Represents a special or lazily-evaluated value.

    Can be used to delay evaluation of a certain value in case, for example,
    that it requires some context or late-bound data. Can also be used to
    mark values that need special processing at document rendering time.

    Tokens can be embedded into strings while retaining their original
    semantics.

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="asAny")
    @builtins.classmethod
    def as_any(cls, value: typing.Any) -> "IResolvable":
        """Return a resolvable representation of the given value.

        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "asAny", [value])

    @jsii.member(jsii_name="asList")
    @builtins.classmethod
    def as_list(cls, value: typing.Any, *, display_hint: typing.Optional[str]=None) -> typing.List[str]:
        """Return a reversible list representation of this token.

        :param value: -
        :param display_hint: A hint for the Token's purpose when stringifying it.

        stability
        :stability: experimental
        """
        options = EncodingOptions(display_hint=display_hint)

        return jsii.sinvoke(cls, "asList", [value, options])

    @jsii.member(jsii_name="asNumber")
    @builtins.classmethod
    def as_number(cls, value: typing.Any) -> jsii.Number:
        """Return a reversible number representation of this token.

        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "asNumber", [value])

    @jsii.member(jsii_name="asString")
    @builtins.classmethod
    def as_string(cls, value: typing.Any, *, display_hint: typing.Optional[str]=None) -> str:
        """Return a reversible string representation of this token.

        If the Token is initialized with a literal, the stringified value of the
        literal is returned. Otherwise, a special quoted string representation
        of the Token is returned that can be embedded into other strings.

        Strings with quoted Tokens in them can be restored back into
        complex values with the Tokens restored by calling ``resolve()``
        on the string.

        :param value: -
        :param display_hint: A hint for the Token's purpose when stringifying it.

        stability
        :stability: experimental
        """
        options = EncodingOptions(display_hint=display_hint)

        return jsii.sinvoke(cls, "asString", [value, options])

    @jsii.member(jsii_name="isUnresolved")
    @builtins.classmethod
    def is_unresolved(cls, obj: typing.Any) -> bool:
        """Returns true if obj represents an unresolved value.

        One of these must be true:

        - ``obj`` is an IResolvable
        - ``obj`` is a string containing at least one encoded ``IResolvable``
        - ``obj`` is either an encoded number or list

        This does NOT recurse into lists or objects to see if they
        containing resolvables.

        :param obj: The object to test.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "isUnresolved", [obj])


class Tokenization(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.Tokenization"):
    """Less oft-needed functions to manipulate Tokens.

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="isResolvable")
    @builtins.classmethod
    def is_resolvable(cls, obj: typing.Any) -> bool:
        """Return whether the given object is an IResolvable object.

        This is different from Token.isUnresolved() which will also check for
        encoded Tokens, whereas this method will only do a type check on the given
        object.

        :param obj: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "isResolvable", [obj])

    @jsii.member(jsii_name="resolve")
    @builtins.classmethod
    def resolve(cls, obj: typing.Any, *, resolver: "ITokenResolver", scope: "IConstruct", preparing: typing.Optional[bool]=None) -> typing.Any:
        """Resolves an object by evaluating all tokens and removing any undefined or empty objects or arrays.

        Values can only be primitives, arrays or tokens. Other objects (i.e. with methods) will be rejected.

        :param obj: The object to resolve.
        :param resolver: The resolver to apply to any resolvable tokens found.
        :param scope: The scope from which resolution is performed.
        :param preparing: Whether the resolution is being executed during the prepare phase or not. Default: false

        stability
        :stability: experimental
        """
        options = ResolveOptions(resolver=resolver, scope=scope, preparing=preparing)

        return jsii.sinvoke(cls, "resolve", [obj, options])

    @jsii.member(jsii_name="reverseList")
    @builtins.classmethod
    def reverse_list(cls, l: typing.List[str]) -> typing.Optional["IResolvable"]:
        """Un-encode a Tokenized value from a list.

        :param l: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "reverseList", [l])

    @jsii.member(jsii_name="reverseNumber")
    @builtins.classmethod
    def reverse_number(cls, n: jsii.Number) -> typing.Optional["IResolvable"]:
        """Un-encode a Tokenized value from a number.

        :param n: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "reverseNumber", [n])

    @jsii.member(jsii_name="reverseString")
    @builtins.classmethod
    def reverse_string(cls, s: str) -> "TokenizedStringFragments":
        """Un-encode a string potentially containing encoded tokens.

        :param s: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "reverseString", [s])

    @jsii.member(jsii_name="stringifyNumber")
    @builtins.classmethod
    def stringify_number(cls, x: jsii.Number) -> str:
        """Stringify a number directly or lazily if it's a Token.

        If it is an object (i.e., { Ref: 'SomeLogicalId' }), return it as-is.

        :param x: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "stringifyNumber", [x])


class TokenizedStringFragments(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.TokenizedStringFragments"):
    """Fragments of a concatenated string containing stringified Tokens.

    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        jsii.create(TokenizedStringFragments, self, [])

    @jsii.member(jsii_name="addIntrinsic")
    def add_intrinsic(self, value: typing.Any) -> None:
        """
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addIntrinsic", [value])

    @jsii.member(jsii_name="addLiteral")
    def add_literal(self, lit: typing.Any) -> None:
        """
        :param lit: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addLiteral", [lit])

    @jsii.member(jsii_name="addToken")
    def add_token(self, token: "IResolvable") -> None:
        """
        :param token: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToken", [token])

    @jsii.member(jsii_name="join")
    def join(self, concat: "IFragmentConcatenator") -> typing.Any:
        """Combine the string fragments using the given joiner.

        If there are any

        :param concat: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "join", [concat])

    @jsii.member(jsii_name="mapTokens")
    def map_tokens(self, mapper: "ITokenMapper") -> "TokenizedStringFragments":
        """Apply a transformation function to all tokens in the string.

        :param mapper: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "mapTokens", [mapper])

    @builtins.property
    @jsii.member(jsii_name="firstValue")
    def first_value(self) -> typing.Any:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "firstValue")

    @builtins.property
    @jsii.member(jsii_name="length")
    def length(self) -> jsii.Number:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "length")

    @builtins.property
    @jsii.member(jsii_name="tokens")
    def tokens(self) -> typing.List["IResolvable"]:
        """Return all Tokens from this string.

        stability
        :stability: experimental
        """
        return jsii.get(self, "tokens")

    @builtins.property
    @jsii.member(jsii_name="firstToken")
    def first_token(self) -> typing.Optional["IResolvable"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "firstToken")


class TreeInspector(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.TreeInspector"):
    """Inspector that maintains an attribute bag.

    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        jsii.create(TreeInspector, self, [])

    @jsii.member(jsii_name="addAttribute")
    def add_attribute(self, key: str, value: typing.Any) -> None:
        """Adds attribute to bag.

        Keys should be added by convention to prevent conflicts
        i.e. L1 constructs will contain attributes with keys prefixed with aws:cdk:cloudformation

        :param key: - key for metadata.
        :param value: - value of metadata.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addAttribute", [key, value])

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(self) -> typing.Mapping[str, typing.Any]:
        """Represents the bag of attributes as key-value pairs.

        stability
        :stability: experimental
        """
        return jsii.get(self, "attributes")


@jsii.data_type(jsii_type="monocdk-experiment.ValidationError", jsii_struct_bases=[], name_mapping={'message': 'message', 'source': 'source'})
class ValidationError():
    def __init__(self, *, message: str, source: "Construct") -> None:
        """An error returned during the validation phase.

        :param message: The error message.
        :param source: The construct which emitted the error.

        stability
        :stability: experimental
        """
        self._values = {
            'message': message,
            'source': source,
        }

    @builtins.property
    def message(self) -> str:
        """The error message.

        stability
        :stability: experimental
        """
        return self._values.get('message')

    @builtins.property
    def source(self) -> "Construct":
        """The construct which emitted the error.

        stability
        :stability: experimental
        """
        return self._values.get('source')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ValidationError(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ValidationResult(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.ValidationResult"):
    """Representation of validation results.

    Models a tree of validation errors so that we have as much information as possible
    about the failure that occurred.

    stability
    :stability: experimental
    """
    def __init__(self, error_message: typing.Optional[str]=None, results: typing.Optional["ValidationResults"]=None) -> None:
        """
        :param error_message: -
        :param results: -

        stability
        :stability: experimental
        """
        jsii.create(ValidationResult, self, [error_message, results])

    @jsii.member(jsii_name="assertSuccess")
    def assert_success(self) -> None:
        """Turn a failed validation into an exception.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "assertSuccess", [])

    @jsii.member(jsii_name="errorTree")
    def error_tree(self) -> str:
        """Return a string rendering of the tree of validation failures.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "errorTree", [])

    @jsii.member(jsii_name="prefix")
    def prefix(self, message: str) -> "ValidationResult":
        """Wrap this result with an error message, if it concerns an error.

        :param message: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "prefix", [message])

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "errorMessage")

    @builtins.property
    @jsii.member(jsii_name="isSuccess")
    def is_success(self) -> bool:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "isSuccess")

    @builtins.property
    @jsii.member(jsii_name="results")
    def results(self) -> "ValidationResults":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "results")


class ValidationResults(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.ValidationResults"):
    """A collection of validation results.

    stability
    :stability: experimental
    """
    def __init__(self, results: typing.Optional[typing.List["ValidationResult"]]=None) -> None:
        """
        :param results: -

        stability
        :stability: experimental
        """
        jsii.create(ValidationResults, self, [results])

    @jsii.member(jsii_name="collect")
    def collect(self, result: "ValidationResult") -> None:
        """
        :param result: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "collect", [result])

    @jsii.member(jsii_name="errorTreeList")
    def error_tree_list(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "errorTreeList", [])

    @jsii.member(jsii_name="wrap")
    def wrap(self, message: str) -> "ValidationResult":
        """Wrap up all validation results into a single tree node.

        If there are failures in the collection, add a message, otherwise
        return a success.

        :param message: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "wrap", [message])

    @builtins.property
    @jsii.member(jsii_name="isSuccess")
    def is_success(self) -> bool:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "isSuccess")

    @builtins.property
    @jsii.member(jsii_name="results")
    def results(self) -> typing.List["ValidationResult"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "results")

    @results.setter
    def results(self, value: typing.List["ValidationResult"]) -> None:
        jsii.set(self, "results", value)


@jsii.data_type(jsii_type="monocdk-experiment.AssetStagingProps", jsii_struct_bases=[FingerprintOptions, AssetOptions], name_mapping={'exclude': 'exclude', 'follow': 'follow', 'extra_hash': 'extraHash', 'asset_hash': 'assetHash', 'asset_hash_type': 'assetHashType', 'bundling': 'bundling', 'source_path': 'sourcePath'})
class AssetStagingProps(FingerprintOptions, AssetOptions):
    def __init__(self, *, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional["SymlinkFollowMode"]=None, extra_hash: typing.Optional[str]=None, asset_hash: typing.Optional[str]=None, asset_hash_type: typing.Optional["AssetHashType"]=None, bundling: typing.Optional["BundlingOptions"]=None, source_path: str) -> None:
        """Initialization properties for ``AssetStaging``.

        :param exclude: Glob patterns to exclude from the copy. Default: - nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER
        :param extra_hash: Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise
        :param source_path: The source file or directory to copy from.

        stability
        :stability: experimental
        """
        if isinstance(bundling, dict): bundling = BundlingOptions(**bundling)
        self._values = {
            'source_path': source_path,
        }
        if exclude is not None: self._values["exclude"] = exclude
        if follow is not None: self._values["follow"] = follow
        if extra_hash is not None: self._values["extra_hash"] = extra_hash
        if asset_hash is not None: self._values["asset_hash"] = asset_hash
        if asset_hash_type is not None: self._values["asset_hash_type"] = asset_hash_type
        if bundling is not None: self._values["bundling"] = bundling

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[str]]:
        """Glob patterns to exclude from the copy.

        default
        :default: - nothing is excluded

        stability
        :stability: experimental
        """
        return self._values.get('exclude')

    @builtins.property
    def follow(self) -> typing.Optional["SymlinkFollowMode"]:
        """A strategy for how to handle symlinks.

        default
        :default: SymlinkFollowMode.NEVER

        stability
        :stability: experimental
        """
        return self._values.get('follow')

    @builtins.property
    def extra_hash(self) -> typing.Optional[str]:
        """Extra information to encode into the fingerprint (e.g. build instructions and other inputs).

        default
        :default: - hash is only based on source content

        stability
        :stability: experimental
        """
        return self._values.get('extra_hash')

    @builtins.property
    def asset_hash(self) -> typing.Optional[str]:
        """Specify a custom hash for this asset.

        If ``assetHashType`` is set it must
        be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will
        be SHA256 hashed and encoded as hex. The resulting hash will be the asset
        hash.

        NOTE: the hash is used in order to identify a specific revision of the asset, and
        used for optimizing and caching deployment activities related to this asset such as
        packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will
        need to make sure it is updated every time the asset changes, or otherwise it is
        possible that some deployments will not be invalidated.

        default
        :default: - based on ``assetHashType``

        stability
        :stability: experimental
        """
        return self._values.get('asset_hash')

    @builtins.property
    def asset_hash_type(self) -> typing.Optional["AssetHashType"]:
        """Specifies the type of hash to calculate for this asset.

        If ``assetHash`` is configured, this option must be ``undefined`` or
        ``AssetHashType.CUSTOM``.

        default
        :default:

        - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is
          explicitly specified this value defaults to ``AssetHashType.CUSTOM``.

        stability
        :stability: experimental
        """
        return self._values.get('asset_hash_type')

    @builtins.property
    def bundling(self) -> typing.Optional["BundlingOptions"]:
        """Bundle the asset by executing a command in a Docker container.

        The asset path will be mounted at ``/asset-input``. The Docker
        container is responsible for putting content at ``/asset-output``.
        The content at ``/asset-output`` will be zipped and used as the
        final asset.

        default
        :default:

        - uploaded as-is to S3 if the asset is a regular file or a .zip file,
          archived into a .zip file and uploaded to S3 otherwise

        stability
        :stability: experimental
        """
        return self._values.get('bundling')

    @builtins.property
    def source_path(self) -> str:
        """The source file or directory to copy from.

        stability
        :stability: experimental
        """
        return self._values.get('source_path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AssetStagingProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class CfnDynamicReference(Intrinsic, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.CfnDynamicReference"):
    """References a dynamically retrieved value.

    This is a Construct so that subclasses will (eventually) be able to attach
    metadata to themselves without having to change call signatures.

    see
    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html
    stability
    :stability: experimental
    """
    def __init__(self, service: "CfnDynamicReferenceService", key: str) -> None:
        """
        :param service: -
        :param key: -

        stability
        :stability: experimental
        """
        jsii.create(CfnDynamicReference, self, [service, key])


@jsii.implements(IDependable)
class ConcreteDependable(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.ConcreteDependable"):
    """A set of constructs to be used as a dependable.

    This class can be used when a set of constructs which are disjoint in the
    construct tree needs to be combined to be used as a single dependable.

    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        """
        stability
        :stability: experimental
        """
        jsii.create(ConcreteDependable, self, [])

    @jsii.member(jsii_name="add")
    def add(self, construct: "IConstruct") -> None:
        """Add a construct to the dependency roots.

        :param construct: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "add", [construct])


@jsii.implements(IStackSynthesizer)
class DefaultStackSynthesizer(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.DefaultStackSynthesizer"):
    """Uses conventionally named roles and reify asset storage locations.

    This synthesizer is the only StackSynthesizer that generates
    an asset manifest, and is required to deploy CDK applications using the
    ``@aws-cdk/app-delivery`` CI/CD library.

    Requires the environment to have been bootstrapped with Bootstrap Stack V2.

    stability
    :stability: experimental
    """
    def __init__(self, *, cloud_formation_execution_role: typing.Optional[str]=None, deploy_role_arn: typing.Optional[str]=None, file_asset_key_arn_export_name: typing.Optional[str]=None, file_asset_publishing_external_id: typing.Optional[str]=None, file_asset_publishing_role_arn: typing.Optional[str]=None, file_assets_bucket_name: typing.Optional[str]=None, image_asset_publishing_external_id: typing.Optional[str]=None, image_asset_publishing_role_arn: typing.Optional[str]=None, image_assets_repository_name: typing.Optional[str]=None, qualifier: typing.Optional[str]=None) -> None:
        """
        :param cloud_formation_execution_role: The role CloudFormation will assume when deploying the Stack. You must supply this if you have given a non-standard name to the execution role. The placeholders ``${Qualifier}``, ``${AWS::AccountId}`` and ``${AWS::Region}`` will be replaced with the values of qualifier and the stack's account and region, respectively. Default: DefaultStackSynthesizer.DEFAULT_CLOUDFORMATION_ROLE_ARN
        :param deploy_role_arn: The role to assume to initiate a deployment in this environment. You must supply this if you have given a non-standard name to the publishing role. The placeholders ``${Qualifier}``, ``${AWS::AccountId}`` and ``${AWS::Region}`` will be replaced with the values of qualifier and the stack's account and region, respectively. Default: DefaultStackSynthesizer.DEFAULT_DEPLOY_ROLE_ARN
        :param file_asset_key_arn_export_name: Name of the CloudFormation Export with the asset key name. You must supply this if you have given a non-standard name to the KMS key export The placeholders ``${Qualifier}``, ``${AWS::AccountId}`` and ``${AWS::Region}`` will be replaced with the values of qualifier and the stack's account and region, respectively. Default: DefaultStackSynthesizer.DEFAULT_FILE_ASSET_KEY_ARN_EXPORT_NAME
        :param file_asset_publishing_external_id: External ID to use when assuming role for file asset publishing. Default: - No external ID
        :param file_asset_publishing_role_arn: The role to use to publish file assets to the S3 bucket in this environment. You must supply this if you have given a non-standard name to the publishing role. The placeholders ``${Qualifier}``, ``${AWS::AccountId}`` and ``${AWS::Region}`` will be replaced with the values of qualifier and the stack's account and region, respectively. Default: DefaultStackSynthesizer.DEFAULT_FILE_ASSET_PUBLISHING_ROLE_ARN
        :param file_assets_bucket_name: Name of the S3 bucket to hold file assets. You must supply this if you have given a non-standard name to the staging bucket. The placeholders ``${Qualifier}``, ``${AWS::AccountId}`` and ``${AWS::Region}`` will be replaced with the values of qualifier and the stack's account and region, respectively. Default: DefaultStackSynthesizer.DEFAULT_FILE_ASSETS_BUCKET_NAME
        :param image_asset_publishing_external_id: External ID to use when assuming role for image asset publishing. Default: - No external ID
        :param image_asset_publishing_role_arn: The role to use to publish image assets to the ECR repository in this environment. You must supply this if you have given a non-standard name to the publishing role. The placeholders ``${Qualifier}``, ``${AWS::AccountId}`` and ``${AWS::Region}`` will be replaced with the values of qualifier and the stack's account and region, respectively. Default: DefaultStackSynthesizer.DEFAULT_IMAGE_ASSET_PUBLISHING_ROLE_ARN
        :param image_assets_repository_name: Name of the ECR repository to hold Docker Image assets. You must supply this if you have given a non-standard name to the ECR repository. The placeholders ``${Qualifier}``, ``${AWS::AccountId}`` and ``${AWS::Region}`` will be replaced with the values of qualifier and the stack's account and region, respectively. Default: DefaultStackSynthesizer.DEFAULT_IMAGE_ASSETS_REPOSITORY_NAME
        :param qualifier: Qualifier to disambiguate multiple environments in the same account. You can use this and leave the other naming properties empty if you have deployed the bootstrap environment with standard names but only differnet qualifiers. Default: - Value of context key '

        stability
        :stability: experimental
        """
        props = DefaultStackSynthesizerProps(cloud_formation_execution_role=cloud_formation_execution_role, deploy_role_arn=deploy_role_arn, file_asset_key_arn_export_name=file_asset_key_arn_export_name, file_asset_publishing_external_id=file_asset_publishing_external_id, file_asset_publishing_role_arn=file_asset_publishing_role_arn, file_assets_bucket_name=file_assets_bucket_name, image_asset_publishing_external_id=image_asset_publishing_external_id, image_asset_publishing_role_arn=image_asset_publishing_role_arn, image_assets_repository_name=image_assets_repository_name, qualifier=qualifier)

        jsii.create(DefaultStackSynthesizer, self, [props])

    @jsii.member(jsii_name="addDockerImageAsset")
    def add_docker_image_asset(self, *, directory_name: str, source_hash: str, docker_build_args: typing.Optional[typing.Mapping[str, str]]=None, docker_build_target: typing.Optional[str]=None, docker_file: typing.Optional[str]=None, repository_name: typing.Optional[str]=None) -> "DockerImageAssetLocation":
        """Register a Docker Image Asset.

        Returns the parameters that can be used to refer to the asset inside the template.

        :param directory_name: The directory where the Dockerfile is stored, must be relative to the cloud assembly root.
        :param source_hash: The hash of the contents of the docker build context. This hash is used throughout the system to identify this image and avoid duplicate work in case the source did not change. NOTE: this means that if you wish to update your docker image, you must make a modification to the source (e.g. add some metadata to your Dockerfile).
        :param docker_build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param docker_build_target: Docker target to build to. Default: - no target
        :param docker_file: Path to the Dockerfile (relative to the directory). Default: - no file
        :param repository_name: ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - automatically derived from the asset's ID.

        stability
        :stability: experimental
        """
        asset = DockerImageAssetSource(directory_name=directory_name, source_hash=source_hash, docker_build_args=docker_build_args, docker_build_target=docker_build_target, docker_file=docker_file, repository_name=repository_name)

        return jsii.invoke(self, "addDockerImageAsset", [asset])

    @jsii.member(jsii_name="addFileAsset")
    def add_file_asset(self, *, file_name: str, packaging: "FileAssetPackaging", source_hash: str) -> "FileAssetLocation":
        """Register a File Asset.

        Returns the parameters that can be used to refer to the asset inside the template.

        :param file_name: The path, relative to the root of the cloud assembly, in which this asset source resides. This can be a path to a file or a directory, dependning on the packaging type.
        :param packaging: Which type of packaging to perform.
        :param source_hash: A hash on the content source. This hash is used to uniquely identify this asset throughout the system. If this value doesn't change, the asset will not be rebuilt or republished.

        stability
        :stability: experimental
        """
        asset = FileAssetSource(file_name=file_name, packaging=packaging, source_hash=source_hash)

        return jsii.invoke(self, "addFileAsset", [asset])

    @jsii.member(jsii_name="bind")
    def bind(self, stack: "Stack") -> None:
        """Bind to the stack this environment is going to be used on.

        Must be called before any of the other methods are called.

        :param stack: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [stack])

    @jsii.member(jsii_name="synthesizeStackArtifacts")
    def synthesize_stack_artifacts(self, session: "ISynthesisSession") -> None:
        """Synthesize all artifacts required for the stack into the session.

        :param session: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeStackArtifacts", [session])

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_CLOUDFORMATION_ROLE_ARN")
    def DEFAULT_CLOUDFORMATION_ROLE_ARN(cls) -> str:
        """Default CloudFormation role ARN.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DEFAULT_CLOUDFORMATION_ROLE_ARN")

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_DEPLOY_ROLE_ARN")
    def DEFAULT_DEPLOY_ROLE_ARN(cls) -> str:
        """Default deploy role ARN.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DEFAULT_DEPLOY_ROLE_ARN")

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_FILE_ASSET_KEY_ARN_EXPORT_NAME")
    def DEFAULT_FILE_ASSET_KEY_ARN_EXPORT_NAME(cls) -> str:
        """Name of the CloudFormation Export with the asset key name.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DEFAULT_FILE_ASSET_KEY_ARN_EXPORT_NAME")

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_FILE_ASSET_PUBLISHING_ROLE_ARN")
    def DEFAULT_FILE_ASSET_PUBLISHING_ROLE_ARN(cls) -> str:
        """Default asset publishing role ARN for file (S3) assets.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DEFAULT_FILE_ASSET_PUBLISHING_ROLE_ARN")

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_FILE_ASSETS_BUCKET_NAME")
    def DEFAULT_FILE_ASSETS_BUCKET_NAME(cls) -> str:
        """Default file assets bucket name.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DEFAULT_FILE_ASSETS_BUCKET_NAME")

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_IMAGE_ASSET_PUBLISHING_ROLE_ARN")
    def DEFAULT_IMAGE_ASSET_PUBLISHING_ROLE_ARN(cls) -> str:
        """Default asset publishing role ARN for image (ECR) assets.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DEFAULT_IMAGE_ASSET_PUBLISHING_ROLE_ARN")

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_IMAGE_ASSETS_REPOSITORY_NAME")
    def DEFAULT_IMAGE_ASSETS_REPOSITORY_NAME(cls) -> str:
        """Default image assets repository name.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DEFAULT_IMAGE_ASSETS_REPOSITORY_NAME")

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_QUALIFIER")
    def DEFAULT_QUALIFIER(cls) -> str:
        """Default ARN qualifier.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DEFAULT_QUALIFIER")

    @builtins.property
    @jsii.member(jsii_name="cloudFormationExecutionRoleArn")
    def cloud_formation_execution_role_arn(self) -> str:
        """Returns the ARN of the CFN execution Role.

        stability
        :stability: experimental
        """
        return jsii.get(self, "cloudFormationExecutionRoleArn")

    @builtins.property
    @jsii.member(jsii_name="deployRoleArn")
    def deploy_role_arn(self) -> str:
        """Returns the ARN of the deploy Role.

        stability
        :stability: experimental
        """
        return jsii.get(self, "deployRoleArn")

    @builtins.property
    @jsii.member(jsii_name="stack")
    def _stack(self) -> typing.Optional["Stack"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "stack")


@jsii.implements(ITokenResolver)
class DefaultTokenResolver(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.DefaultTokenResolver"):
    """Default resolver implementation.

    stability
    :stability: experimental
    """
    def __init__(self, concat: "IFragmentConcatenator") -> None:
        """
        :param concat: -

        stability
        :stability: experimental
        """
        jsii.create(DefaultTokenResolver, self, [concat])

    @jsii.member(jsii_name="resolveList")
    def resolve_list(self, xs: typing.List[str], context: "IResolveContext") -> typing.Any:
        """Resolve a tokenized list.

        :param xs: -
        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolveList", [xs, context])

    @jsii.member(jsii_name="resolveString")
    def resolve_string(self, fragments: "TokenizedStringFragments", context: "IResolveContext") -> typing.Any:
        """Resolve string fragments to Tokens.

        :param fragments: -
        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolveString", [fragments, context])

    @jsii.member(jsii_name="resolveToken")
    def resolve_token(self, t: "IResolvable", context: "IResolveContext", post_processor: "IPostProcessor") -> typing.Any:
        """Default Token resolution.

        Resolve the Token, recurse into whatever it returns,
        then finally post-process it.

        :param t: -
        :param context: -
        :param post_processor: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolveToken", [t, context, post_processor])


@jsii.interface(jsii_type="monocdk-experiment.ICfnConditionExpression")
class ICfnConditionExpression(IResolvable, jsii.compat.Protocol):
    """Represents a CloudFormation element that can be used within a Condition.

    You can use intrinsic functions, such as ``Fn.conditionIf``,
    ``Fn.conditionEquals``, and ``Fn.conditionNot``, to conditionally create
    stack resources. These conditions are evaluated based on input parameters
    that you declare when you create or update a stack. After you define all your
    conditions, you can associate them with resources or resource properties in
    the Resources and Outputs sections of a template.

    You define all conditions in the Conditions section of a template except for
    ``Fn.conditionIf`` conditions. You can use the ``Fn.conditionIf`` condition
    in the metadata attribute, update policy attribute, and property values in
    the Resources section and Outputs sections of a template.

    You might use conditions when you want to reuse a template that can create
    resources in different contexts, such as a test environment versus a
    production environment. In your template, you can add an EnvironmentType
    input parameter, which accepts either prod or test as inputs. For the
    production environment, you might include Amazon EC2 instances with certain
    capabilities; however, for the test environment, you want to use less
    capabilities to save costs. With conditions, you can define which resources
    are created and how they're configured for each environment type.

    You can use ``toString`` when you wish to embed a condition expression
    in a property value that accepts a ``string``. For example::

       # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
       sqs.Queue(self, "MyQueue",
           queue_name=Fn.condition_if("Condition", "Hello", "World").to_string()
       )

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ICfnConditionExpressionProxy

    pass

class _ICfnConditionExpressionProxy(jsii.proxy_for(IResolvable)):
    """Represents a CloudFormation element that can be used within a Condition.

    You can use intrinsic functions, such as ``Fn.conditionIf``,
    ``Fn.conditionEquals``, and ``Fn.conditionNot``, to conditionally create
    stack resources. These conditions are evaluated based on input parameters
    that you declare when you create or update a stack. After you define all your
    conditions, you can associate them with resources or resource properties in
    the Resources and Outputs sections of a template.

    You define all conditions in the Conditions section of a template except for
    ``Fn.conditionIf`` conditions. You can use the ``Fn.conditionIf`` condition
    in the metadata attribute, update policy attribute, and property values in
    the Resources section and Outputs sections of a template.

    You might use conditions when you want to reuse a template that can create
    resources in different contexts, such as a test environment versus a
    production environment. In your template, you can add an EnvironmentType
    input parameter, which accepts either prod or test as inputs. For the
    production environment, you might include Amazon EC2 instances with certain
    capabilities; however, for the test environment, you want to use less
    capabilities to save costs. With conditions, you can define which resources
    are created and how they're configured for each environment type.

    You can use ``toString`` when you wish to embed a condition expression
    in a property value that accepts a ``string``. For example::

       # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
       sqs.Queue(self, "MyQueue",
           queue_name=Fn.condition_if("Condition", "Hello", "World").to_string()
       )

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.ICfnConditionExpression"
    pass

@jsii.interface(jsii_type="monocdk-experiment.IConstruct")
class IConstruct(constructs.IConstruct, IDependable, jsii.compat.Protocol):
    """Represents a construct.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IConstructProxy

    @builtins.property
    @jsii.member(jsii_name="node")
    def node(self) -> "ConstructNode":
        """The construct tree node for this construct.

        stability
        :stability: experimental
        """
        ...


class _IConstructProxy(jsii.proxy_for(constructs.IConstruct), jsii.proxy_for(IDependable)):
    """Represents a construct.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.IConstruct"
    @builtins.property
    @jsii.member(jsii_name="node")
    def node(self) -> "ConstructNode":
        """The construct tree node for this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "node")


@jsii.interface(jsii_type="monocdk-experiment.IResource")
class IResource(IConstruct, jsii.compat.Protocol):
    """Interface for the Resource construct.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IResourceProxy

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> "Stack":
        """The stack in which this resource is defined.

        stability
        :stability: experimental
        """
        ...


class _IResourceProxy(jsii.proxy_for(IConstruct)):
    """Interface for the Resource construct.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.IResource"
    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> "Stack":
        """The stack in which this resource is defined.

        stability
        :stability: experimental
        """
        return jsii.get(self, "stack")


class BootstraplessSynthesizer(DefaultStackSynthesizer, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.BootstraplessSynthesizer"):
    """A special synthesizer that behaves similarly to DefaultStackSynthesizer, but doesn't require bootstrapping the environment it operates in.

    Because of that, stacks using it cannot have assets inside of them.
    Used by the CodePipeline construct for the support stacks needed for
    cross-region replication S3 buckets.

    stability
    :stability: experimental
    """
    def __init__(self, *, cloud_formation_execution_role_arn: typing.Optional[str]=None, deploy_role_arn: typing.Optional[str]=None) -> None:
        """
        :param cloud_formation_execution_role_arn: The CFN execution Role ARN to use. Default: - No CloudFormation role (use CLI credentials)
        :param deploy_role_arn: The deploy Role ARN to use. Default: - No deploy role (use CLI credentials)

        stability
        :stability: experimental
        """
        props = BootstraplessSynthesizerProps(cloud_formation_execution_role_arn=cloud_formation_execution_role_arn, deploy_role_arn=deploy_role_arn)

        jsii.create(BootstraplessSynthesizer, self, [props])

    @jsii.member(jsii_name="addDockerImageAsset")
    def add_docker_image_asset(self, *, directory_name: str, source_hash: str, docker_build_args: typing.Optional[typing.Mapping[str, str]]=None, docker_build_target: typing.Optional[str]=None, docker_file: typing.Optional[str]=None, repository_name: typing.Optional[str]=None) -> "DockerImageAssetLocation":
        """Register a Docker Image Asset.

        Returns the parameters that can be used to refer to the asset inside the template.

        :param directory_name: The directory where the Dockerfile is stored, must be relative to the cloud assembly root.
        :param source_hash: The hash of the contents of the docker build context. This hash is used throughout the system to identify this image and avoid duplicate work in case the source did not change. NOTE: this means that if you wish to update your docker image, you must make a modification to the source (e.g. add some metadata to your Dockerfile).
        :param docker_build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param docker_build_target: Docker target to build to. Default: - no target
        :param docker_file: Path to the Dockerfile (relative to the directory). Default: - no file
        :param repository_name: ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - automatically derived from the asset's ID.

        stability
        :stability: experimental
        """
        _asset = DockerImageAssetSource(directory_name=directory_name, source_hash=source_hash, docker_build_args=docker_build_args, docker_build_target=docker_build_target, docker_file=docker_file, repository_name=repository_name)

        return jsii.invoke(self, "addDockerImageAsset", [_asset])

    @jsii.member(jsii_name="addFileAsset")
    def add_file_asset(self, *, file_name: str, packaging: "FileAssetPackaging", source_hash: str) -> "FileAssetLocation":
        """Register a File Asset.

        Returns the parameters that can be used to refer to the asset inside the template.

        :param file_name: The path, relative to the root of the cloud assembly, in which this asset source resides. This can be a path to a file or a directory, dependning on the packaging type.
        :param packaging: Which type of packaging to perform.
        :param source_hash: A hash on the content source. This hash is used to uniquely identify this asset throughout the system. If this value doesn't change, the asset will not be rebuilt or republished.

        stability
        :stability: experimental
        """
        _asset = FileAssetSource(file_name=file_name, packaging=packaging, source_hash=source_hash)

        return jsii.invoke(self, "addFileAsset", [_asset])

    @jsii.member(jsii_name="synthesizeStackArtifacts")
    def synthesize_stack_artifacts(self, session: "ISynthesisSession") -> None:
        """Synthesize all artifacts required for the stack into the session.

        :param session: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeStackArtifacts", [session])


@jsii.implements(IConstruct)
class Construct(constructs.Construct, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.Construct"):
    """Represents the building block of the construct graph.

    All constructs besides the root construct must be created within the scope of
    another construct.

    stability
    :stability: experimental
    """
    def __init__(self, scope: "Construct", id: str) -> None:
        """
        :param scope: -
        :param id: -

        stability
        :stability: experimental
        """
        jsii.create(Construct, self, [scope, id])

    @jsii.member(jsii_name="isConstruct")
    @builtins.classmethod
    def is_construct(cls, x: typing.Any) -> bool:
        """Return whether the given object is a Construct.

        :param x: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "isConstruct", [x])

    @jsii.member(jsii_name="onPrepare")
    def _on_prepare(self) -> None:
        """Perform final modifications before synthesis.

        This method can be implemented by derived constructs in order to perform
        final changes before synthesis. prepare() will be called after child
        constructs have been prepared.

        This is an advanced framework feature. Only use this if you
        understand the implications.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "onPrepare", [])

    @jsii.member(jsii_name="onSynthesize")
    def _on_synthesize(self, session: constructs.ISynthesisSession) -> None:
        """Allows this construct to emit artifacts into the cloud assembly during synthesis.

        This method is usually implemented by framework-level constructs such as ``Stack`` and ``Asset``
        as they participate in synthesizing the cloud assembly.

        :param session: The synthesis session.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "onSynthesize", [session])

    @jsii.member(jsii_name="onValidate")
    def _on_validate(self) -> typing.List[str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        return
        :return: An array of validation error messages, or an empty array if the construct is valid.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "onValidate", [])

    @jsii.member(jsii_name="prepare")
    def _prepare(self) -> None:
        """Perform final modifications before synthesis.

        This method can be implemented by derived constructs in order to perform
        final changes before synthesis. prepare() will be called after child
        constructs have been prepared.

        This is an advanced framework feature. Only use this if you
        understand the implications.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "prepare", [])

    @jsii.member(jsii_name="synthesize")
    def _synthesize(self, session: "ISynthesisSession") -> None:
        """Allows this construct to emit artifacts into the cloud assembly during synthesis.

        This method is usually implemented by framework-level constructs such as ``Stack`` and ``Asset``
        as they participate in synthesizing the cloud assembly.

        :param session: The synthesis session.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesize", [session])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        return
        :return: An array of validation error messages, or an empty array if the construct is valid.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="node")
    def node(self) -> "ConstructNode":
        """The construct tree node associated with this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "node")


class CustomResourceProvider(Construct, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.CustomResourceProvider"):
    """An AWS-Lambda backed custom resource provider.

    stability
    :stability: experimental
    """
    def __init__(self, scope: "Construct", id: str, *, code_directory: str, runtime: "CustomResourceProviderRuntime", memory_size: typing.Optional["Size"]=None, policy_statements: typing.Optional[typing.List[typing.Any]]=None, timeout: typing.Optional["Duration"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param code_directory: A local file system directory with the provider's code. The code will be bundled into a zip asset and wired to the provider's AWS Lambda function.
        :param runtime: The AWS Lambda runtime and version to use for the provider.
        :param memory_size: The amount of memory that your function has access to. Increasing the function's memory also increases its CPU allocation. Default: Size.mebibytes(128)
        :param policy_statements: A set of IAM policy statements to include in the inline policy of the provider's lambda function. Default: - no additional inline policy
        :param timeout: AWS Lambda timeout for the provider. Default: Duration.minutes(15)

        stability
        :stability: experimental
        """
        props = CustomResourceProviderProps(code_directory=code_directory, runtime=runtime, memory_size=memory_size, policy_statements=policy_statements, timeout=timeout)

        jsii.create(CustomResourceProvider, self, [scope, id, props])

    @jsii.member(jsii_name="getOrCreate")
    @builtins.classmethod
    def get_or_create(cls, scope: "Construct", uniqueid: str, *, code_directory: str, runtime: "CustomResourceProviderRuntime", memory_size: typing.Optional["Size"]=None, policy_statements: typing.Optional[typing.List[typing.Any]]=None, timeout: typing.Optional["Duration"]=None) -> str:
        """Returns a stack-level singleton ARN (service token) for the custom resource provider.

        :param scope: Construct scope.
        :param uniqueid: A globally unique id that will be used for the stack-level construct.
        :param code_directory: A local file system directory with the provider's code. The code will be bundled into a zip asset and wired to the provider's AWS Lambda function.
        :param runtime: The AWS Lambda runtime and version to use for the provider.
        :param memory_size: The amount of memory that your function has access to. Increasing the function's memory also increases its CPU allocation. Default: Size.mebibytes(128)
        :param policy_statements: A set of IAM policy statements to include in the inline policy of the provider's lambda function. Default: - no additional inline policy
        :param timeout: AWS Lambda timeout for the provider. Default: Duration.minutes(15)

        return
        :return:

        the service token of the custom resource provider, which should be
        used when defining a ``CustomResource``.

        stability
        :stability: experimental
        """
        props = CustomResourceProviderProps(code_directory=code_directory, runtime=runtime, memory_size=memory_size, policy_statements=policy_statements, timeout=timeout)

        return jsii.sinvoke(cls, "getOrCreate", [scope, uniqueid, props])

    @builtins.property
    @jsii.member(jsii_name="serviceToken")
    def service_token(self) -> str:
        """The ARN of the provider's AWS Lambda function which should be used as the ``serviceToken`` when defining a custom resource.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            CustomResource(self, "MyCustomResource",
                # ...
                service_token=provider.service_token
            )
        """
        return jsii.get(self, "serviceToken")


@jsii.implements(IResource)
class Resource(Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.Resource"):
    """A construct which represents an AWS resource.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ResourceProxy

    def __init__(self, scope: "Construct", id: str, *, physical_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time

        stability
        :stability: experimental
        """
        props = ResourceProps(physical_name=physical_name)

        jsii.create(Resource, self, [scope, id, props])

    @jsii.member(jsii_name="generatePhysicalName")
    def _generate_physical_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "generatePhysicalName", [])

    @jsii.member(jsii_name="getResourceArnAttribute")
    def _get_resource_arn_attribute(self, arn_attr: str, *, resource: str, service: str, account: typing.Optional[str]=None, partition: typing.Optional[str]=None, region: typing.Optional[str]=None, resource_name: typing.Optional[str]=None, sep: typing.Optional[str]=None) -> str:
        """Returns an environment-sensitive token that should be used for the resource's "ARN" attribute (e.g. ``bucket.bucketArn``).

        Normally, this token will resolve to ``arnAttr``, but if the resource is
        referenced across environments, ``arnComponents`` will be used to synthesize
        a concrete ARN with the resource's physical name. Make sure to reference
        ``this.physicalName`` in ``arnComponents``.

        :param arn_attr: The CFN attribute which resolves to the ARN of the resource. Commonly it will be called "Arn" (e.g. ``resource.attrArn``), but sometimes it's the CFN resource's ``ref``.
        :param resource: Resource type (e.g. "table", "autoScalingGroup", "certificate"). For some resource types, e.g. S3 buckets, this field defines the bucket name.
        :param service: The service namespace that identifies the AWS product (for example, 's3', 'iam', 'codepipline').
        :param account: The ID of the AWS account that owns the resource, without the hyphens. For example, 123456789012. Note that the ARNs for some resources don't require an account number, so this component might be omitted. Default: The account the stack is deployed to.
        :param partition: The partition that the resource is in. For standard AWS regions, the partition is aws. If you have resources in other partitions, the partition is aws-partitionname. For example, the partition for resources in the China (Beijing) region is aws-cn. Default: The AWS partition the stack is deployed to.
        :param region: The region the resource resides in. Note that the ARNs for some resources do not require a region, so this component might be omitted. Default: The region the stack is deployed to.
        :param resource_name: Resource name or path within the resource (i.e. S3 bucket object key) or a wildcard such as ``"*"``. This is service-dependent.
        :param sep: Separator between resource type and the resource. Can be either '/', ':' or an empty string. Will only be used if resourceName is defined. Default: '/'

        stability
        :stability: experimental
        """
        arn_components = ArnComponents(resource=resource, service=service, account=account, partition=partition, region=region, resource_name=resource_name, sep=sep)

        return jsii.invoke(self, "getResourceArnAttribute", [arn_attr, arn_components])

    @jsii.member(jsii_name="getResourceNameAttribute")
    def _get_resource_name_attribute(self, name_attr: str) -> str:
        """Returns an environment-sensitive token that should be used for the resource's "name" attribute (e.g. ``bucket.bucketName``).

        Normally, this token will resolve to ``nameAttr``, but if the resource is
        referenced across environments, it will be resolved to ``this.physicalName``,
        which will be a concrete name.

        :param name_attr: The CFN attribute which resolves to the resource's name. Commonly this is the resource's ``ref``.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getResourceNameAttribute", [name_attr])

    @builtins.property
    @jsii.member(jsii_name="physicalName")
    def _physical_name(self) -> str:
        """Returns a string-encoded token that resolves to the physical name that should be passed to the CloudFormation resource.

        This value will resolve to one of the following:

        - a concrete value (e.g. ``"my-awesome-bucket"``)
        - ``undefined``, when a name should be generated by CloudFormation
        - a concrete name generated automatically during synthesis, in
          cross-environment scenarios.

        stability
        :stability: experimental
        """
        return jsii.get(self, "physicalName")

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> "Stack":
        """The stack in which this resource is defined.

        stability
        :stability: experimental
        """
        return jsii.get(self, "stack")


class _ResourceProxy(Resource):
    pass

@jsii.implements(ITaggable)
class Stack(Construct, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.Stack"):
    """A root construct which represents a single CloudFormation stack.

    stability
    :stability: experimental
    """
    def __init__(self, scope: typing.Optional["Construct"]=None, id: typing.Optional[str]=None, *, description: typing.Optional[str]=None, env: typing.Optional["Environment"]=None, stack_name: typing.Optional[str]=None, synthesizer: typing.Optional["IStackSynthesizer"]=None, tags: typing.Optional[typing.Mapping[str, str]]=None, termination_protection: typing.Optional[bool]=None) -> None:
        """Creates a new stack.

        :param scope: Parent of this stack, usually a Program instance.
        :param id: The construct ID of this stack. If ``stackName`` is not explicitly defined, this id (and any parent IDs) will be used to determine the physical ID of the stack.
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false

        stability
        :stability: experimental
        """
        props = StackProps(description=description, env=env, stack_name=stack_name, synthesizer=synthesizer, tags=tags, termination_protection=termination_protection)

        jsii.create(Stack, self, [scope, id, props])

    @jsii.member(jsii_name="isStack")
    @builtins.classmethod
    def is_stack(cls, x: typing.Any) -> bool:
        """Return whether the given object is a Stack.

        We do attribute detection since we can't reliably use 'instanceof'.

        :param x: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "isStack", [x])

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, construct: "IConstruct") -> "Stack":
        """Looks up the first stack scope in which ``construct`` is defined.

        Fails if there is no stack up the tree.

        :param construct: The construct to start the search from.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "of", [construct])

    @jsii.member(jsii_name="addDependency")
    def add_dependency(self, target: "Stack", reason: typing.Optional[str]=None) -> None:
        """Add a dependency between this stack and another stack.

        This can be used to define dependencies between any two stacks within an
        app, and also supports nested stacks.

        :param target: -
        :param reason: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addDependency", [target, reason])

    @jsii.member(jsii_name="addDockerImageAsset")
    def add_docker_image_asset(self, *, directory_name: str, source_hash: str, docker_build_args: typing.Optional[typing.Mapping[str, str]]=None, docker_build_target: typing.Optional[str]=None, docker_file: typing.Optional[str]=None, repository_name: typing.Optional[str]=None) -> "DockerImageAssetLocation":
        """Register a docker image asset on this Stack.

        :param directory_name: The directory where the Dockerfile is stored, must be relative to the cloud assembly root.
        :param source_hash: The hash of the contents of the docker build context. This hash is used throughout the system to identify this image and avoid duplicate work in case the source did not change. NOTE: this means that if you wish to update your docker image, you must make a modification to the source (e.g. add some metadata to your Dockerfile).
        :param docker_build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param docker_build_target: Docker target to build to. Default: - no target
        :param docker_file: Path to the Dockerfile (relative to the directory). Default: - no file
        :param repository_name: ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - automatically derived from the asset's ID.

        deprecated
        :deprecated:

        Use ``stack.synthesizer.addDockerImageAsset()`` if you are calling,
        and a different ``IDeploymentEnvironment`` class if you are implementing.

        stability
        :stability: deprecated
        """
        asset = DockerImageAssetSource(directory_name=directory_name, source_hash=source_hash, docker_build_args=docker_build_args, docker_build_target=docker_build_target, docker_file=docker_file, repository_name=repository_name)

        return jsii.invoke(self, "addDockerImageAsset", [asset])

    @jsii.member(jsii_name="addFileAsset")
    def add_file_asset(self, *, file_name: str, packaging: "FileAssetPackaging", source_hash: str) -> "FileAssetLocation":
        """Register a file asset on this Stack.

        :param file_name: The path, relative to the root of the cloud assembly, in which this asset source resides. This can be a path to a file or a directory, dependning on the packaging type.
        :param packaging: Which type of packaging to perform.
        :param source_hash: A hash on the content source. This hash is used to uniquely identify this asset throughout the system. If this value doesn't change, the asset will not be rebuilt or republished.

        deprecated
        :deprecated:

        Use ``stack.synthesizer.addFileAsset()`` if you are calling,
        and a different IDeploymentEnvironment class if you are implementing.

        stability
        :stability: deprecated
        """
        asset = FileAssetSource(file_name=file_name, packaging=packaging, source_hash=source_hash)

        return jsii.invoke(self, "addFileAsset", [asset])

    @jsii.member(jsii_name="addTransform")
    def add_transform(self, transform: str) -> None:
        """Add a Transform to this stack. A Transform is a macro that AWS CloudFormation uses to process your template.

        Duplicate values are removed when stack is synthesized.

        :param transform: The transform to add.

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/transform-section-structure.html
        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            add_transform("AWS::Serverless-2016-10-31")
        """
        return jsii.invoke(self, "addTransform", [transform])

    @jsii.member(jsii_name="allocateLogicalId")
    def _allocate_logical_id(self, cfn_element: "CfnElement") -> str:
        """Returns the naming scheme used to allocate logical IDs.

        By default, uses
        the ``HashedAddressingScheme`` but this method can be overridden to customize
        this behavior.

        In order to make sure logical IDs are unique and stable, we hash the resource
        construct tree path (i.e. toplevel/secondlevel/.../myresource) and add it as
        a suffix to the path components joined without a separator (CloudFormation
        IDs only allow alphanumeric characters).

        The result will be:

        <path.join('')><md5(path.join('/')>
        "human"      "hash"

        If the "human" part of the ID exceeds 240 characters, we simply trim it so
        the total ID doesn't exceed CloudFormation's 255 character limit.

        We only take 8 characters from the md5 hash (0.000005 chance of collision).

        Special cases:

        - If the path only contains a single component (i.e. it's a top-level
          resource), we won't add the hash to it. The hash is not needed for
          disamiguation and also, it allows for a more straightforward migration an
          existing CloudFormation template to a CDK stack without logical ID changes
          (or renames).
        - For aesthetic reasons, if the last components of the path are the same
          (i.e. ``L1/L2/Pipeline/Pipeline``), they will be de-duplicated to make the
          resulting human portion of the ID more pleasing: ``L1L2Pipeline<HASH>``
          instead of ``L1L2PipelinePipeline<HASH>``
        - If a component is named "Default" it will be omitted from the path. This
          allows refactoring higher level abstractions around constructs without affecting
          the IDs of already deployed resources.
        - If a component is named "Resource" it will be omitted from the user-visible
          path, but included in the hash. This reduces visual noise in the human readable
          part of the identifier.

        :param cfn_element: The element for which the logical ID is allocated.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "allocateLogicalId", [cfn_element])

    @jsii.member(jsii_name="formatArn")
    def format_arn(self, *, resource: str, service: str, account: typing.Optional[str]=None, partition: typing.Optional[str]=None, region: typing.Optional[str]=None, resource_name: typing.Optional[str]=None, sep: typing.Optional[str]=None) -> str:
        """Creates an ARN from components.

        If ``partition``, ``region`` or ``account`` are not specified, the stack's
        partition, region and account will be used.

        If any component is the empty string, an empty string will be inserted
        into the generated ARN at the location that component corresponds to.

        The ARN will be formatted as follows:

        arn:{partition}:{service}:{region}:{account}:{resource}{sep}}{resource-name}

        The required ARN pieces that are omitted will be taken from the stack that
        the 'scope' is attached to. If all ARN pieces are supplied, the supplied scope
        can be 'undefined'.

        :param resource: Resource type (e.g. "table", "autoScalingGroup", "certificate"). For some resource types, e.g. S3 buckets, this field defines the bucket name.
        :param service: The service namespace that identifies the AWS product (for example, 's3', 'iam', 'codepipline').
        :param account: The ID of the AWS account that owns the resource, without the hyphens. For example, 123456789012. Note that the ARNs for some resources don't require an account number, so this component might be omitted. Default: The account the stack is deployed to.
        :param partition: The partition that the resource is in. For standard AWS regions, the partition is aws. If you have resources in other partitions, the partition is aws-partitionname. For example, the partition for resources in the China (Beijing) region is aws-cn. Default: The AWS partition the stack is deployed to.
        :param region: The region the resource resides in. Note that the ARNs for some resources do not require a region, so this component might be omitted. Default: The region the stack is deployed to.
        :param resource_name: Resource name or path within the resource (i.e. S3 bucket object key) or a wildcard such as ``"*"``. This is service-dependent.
        :param sep: Separator between resource type and the resource. Can be either '/', ':' or an empty string. Will only be used if resourceName is defined. Default: '/'

        stability
        :stability: experimental
        """
        components = ArnComponents(resource=resource, service=service, account=account, partition=partition, region=region, resource_name=resource_name, sep=sep)

        return jsii.invoke(self, "formatArn", [components])

    @jsii.member(jsii_name="getLogicalId")
    def get_logical_id(self, element: "CfnElement") -> str:
        """Allocates a stack-unique CloudFormation-compatible logical identity for a specific resource.

        This method is called when a ``CfnElement`` is created and used to render the
        initial logical identity of resources. Logical ID renames are applied at
        this stage.

        This method uses the protected method ``allocateLogicalId`` to render the
        logical ID for an element. To modify the naming scheme, extend the ``Stack``
        class and override this method.

        :param element: The CloudFormation element for which a logical identity is needed.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getLogicalId", [element])

    @jsii.member(jsii_name="parseArn")
    def parse_arn(self, arn: str, sep_if_token: typing.Optional[str]=None, has_name: typing.Optional[bool]=None) -> "ArnComponents":
        """Given an ARN, parses it and returns components.

        If the ARN is a concrete string, it will be parsed and validated. The
        separator (``sep``) will be set to '/' if the 6th component includes a '/',
        in which case, ``resource`` will be set to the value before the '/' and
        ``resourceName`` will be the rest. In case there is no '/', ``resource`` will
        be set to the 6th components and ``resourceName`` will be set to the rest
        of the string.

        If the ARN includes tokens (or is a token), the ARN cannot be validated,
        since we don't have the actual value yet at the time of this function
        call. You will have to know the separator and the type of ARN. The
        resulting ``ArnComponents`` object will contain tokens for the
        subexpressions of the ARN, not string literals. In this case this
        function cannot properly parse the complete final resourceName (path) out
        of ARNs that use '/' to both separate the 'resource' from the
        'resourceName' AND to subdivide the resourceName further. For example, in
        S3 ARNs::

           arn:aws:s3:::my_corporate_bucket/path/to/exampleobject.png

        After parsing the resourceName will not contain
        'path/to/exampleobject.png' but simply 'path'. This is a limitation
        because there is no slicing functionality in CloudFormation templates.

        :param arn: The ARN string to parse.
        :param sep_if_token: The separator used to separate resource from resourceName.
        :param has_name: Whether there is a name component in the ARN at all. For example, SNS Topics ARNs have the 'resource' component contain the topic name, and no 'resourceName' component.

        return
        :return:

        an ArnComponents object which allows access to the various
        components of the ARN.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "parseArn", [arn, sep_if_token, has_name])

    @jsii.member(jsii_name="prepareCrossReference")
    def _prepare_cross_reference(self, _source_stack: "Stack", reference: "Reference") -> "IResolvable":
        """Deprecated.

        :param _source_stack: -
        :param reference: -

        return
        :return: reference itself without any change

        deprecated
        :deprecated: cross reference handling has been moved to ``App.prepare()``.

        see
        :see: https://github.com/aws/aws-cdk/pull/7187
        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "prepareCrossReference", [_source_stack, reference])

    @jsii.member(jsii_name="renameLogicalId")
    def rename_logical_id(self, old_id: str, new_id: str) -> None:
        """Rename a generated logical identities.

        To modify the naming scheme strategy, extend the ``Stack`` class and
        override the ``allocateLogicalId`` method.

        :param old_id: -
        :param new_id: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "renameLogicalId", [old_id, new_id])

    @jsii.member(jsii_name="reportMissingContext")
    def report_missing_context(self, *, key: str, props: typing.Mapping[str, typing.Any], provider: str) -> None:
        """Indicate that a context key was expected.

        Contains instructions which will be emitted into the cloud assembly on how
        the key should be supplied.

        :param key: The missing context key.
        :param props: A set of provider-specific options. (This is the old untyped definition, which is necessary for backwards compatibility. See cxschema for a type definition.)
        :param provider: The provider from which we expect this context key to be obtained. (This is the old untyped definition, which is necessary for backwards compatibility. See cxschema for a type definition.)

        stability
        :stability: experimental
        """
        report = _MissingContext_63fd4283(key=key, props=props, provider=provider)

        return jsii.invoke(self, "reportMissingContext", [report])

    @jsii.member(jsii_name="resolve")
    def resolve(self, obj: typing.Any) -> typing.Any:
        """Resolve a tokenized value in the context of the current stack.

        :param obj: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolve", [obj])

    @jsii.member(jsii_name="synthesize")
    def _synthesize(self, session: "ISynthesisSession") -> None:
        """Allows this construct to emit artifacts into the cloud assembly during synthesis.

        This method is usually implemented by framework-level constructs such as ``Stack`` and ``Asset``
        as they participate in synthesizing the cloud assembly.

        :param session: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesize", [session])

    @jsii.member(jsii_name="toJsonString")
    def to_json_string(self, obj: typing.Any, space: typing.Optional[jsii.Number]=None) -> str:
        """Convert an object, potentially containing tokens, to a JSON string.

        :param obj: -
        :param space: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toJsonString", [obj, space])

    @builtins.property
    @jsii.member(jsii_name="account")
    def account(self) -> str:
        """The AWS account into which this stack will be deployed.

        This value is resolved according to the following rules:

        1. The value provided to ``env.account`` when the stack is defined. This can
           either be a concerete account (e.g. ``585695031111``) or the
           ``Aws.accountId`` token.
        2. ``Aws.accountId``, which represents the CloudFormation intrinsic reference
           ``{ "Ref": "AWS::AccountId" }`` encoded as a string token.

        Preferably, you should use the return value as an opaque string and not
        attempt to parse it to implement your logic. If you do, you must first
        check that it is a concerete value an not an unresolved token. If this
        value is an unresolved token (``Token.isUnresolved(stack.account)`` returns
        ``true``), this implies that the user wishes that this stack will synthesize
        into a **account-agnostic template**. In this case, your code should either
        fail (throw an error, emit a synth error using ``node.addError``) or
        implement some other region-agnostic behavior.

        stability
        :stability: experimental
        """
        return jsii.get(self, "account")

    @builtins.property
    @jsii.member(jsii_name="artifactId")
    def artifact_id(self) -> str:
        """The ID of the cloud assembly artifact for this stack.

        stability
        :stability: experimental
        """
        return jsii.get(self, "artifactId")

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[str]:
        """Returnst the list of AZs that are availability in the AWS environment (account/region) associated with this stack.

        If the stack is environment-agnostic (either account and/or region are
        tokens), this property will return an array with 2 tokens that will resolve
        at deploy-time to the first two availability zones returned from CloudFormation's
        ``Fn::GetAZs`` intrinsic function.

        If they are not available in the context, returns a set of dummy values and
        reports them as missing, and let the CLI resolve them by calling EC2
        ``DescribeAvailabilityZones`` on the target environment.

        stability
        :stability: experimental
        """
        return jsii.get(self, "availabilityZones")

    @builtins.property
    @jsii.member(jsii_name="dependencies")
    def dependencies(self) -> typing.List["Stack"]:
        """Return the stacks this stack depends on.

        stability
        :stability: experimental
        """
        return jsii.get(self, "dependencies")

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> str:
        """The environment coordinates in which this stack is deployed.

        In the form
        ``aws://account/region``. Use ``stack.account`` and ``stack.region`` to obtain
        the specific values, no need to parse.

        You can use this value to determine if two stacks are targeting the same
        environment.

        If either ``stack.account`` or ``stack.region`` are not concrete values (e.g.
        ``Aws.account`` or ``Aws.region``) the special strings ``unknown-account`` and/or
        ``unknown-region`` will be used respectively to indicate this stack is
        region/account-agnostic.

        stability
        :stability: experimental
        """
        return jsii.get(self, "environment")

    @builtins.property
    @jsii.member(jsii_name="nested")
    def nested(self) -> bool:
        """Indicates if this is a nested stack, in which case ``parentStack`` will include a reference to it's parent.

        stability
        :stability: experimental
        """
        return jsii.get(self, "nested")

    @builtins.property
    @jsii.member(jsii_name="notificationArns")
    def notification_arns(self) -> typing.List[str]:
        """Returns the list of notification Amazon Resource Names (ARNs) for the current stack.

        stability
        :stability: experimental
        """
        return jsii.get(self, "notificationArns")

    @builtins.property
    @jsii.member(jsii_name="partition")
    def partition(self) -> str:
        """The partition in which this stack is defined.

        stability
        :stability: experimental
        """
        return jsii.get(self, "partition")

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> str:
        """The AWS region into which this stack will be deployed (e.g. ``us-west-2``).

        This value is resolved according to the following rules:

        1. The value provided to ``env.region`` when the stack is defined. This can
           either be a concerete region (e.g. ``us-west-2``) or the ``Aws.region``
           token.
        2. ``Aws.region``, which is represents the CloudFormation intrinsic reference
           ``{ "Ref": "AWS::Region" }`` encoded as a string token.

        Preferably, you should use the return value as an opaque string and not
        attempt to parse it to implement your logic. If you do, you must first
        check that it is a concerete value an not an unresolved token. If this
        value is an unresolved token (``Token.isUnresolved(stack.region)`` returns
        ``true``), this implies that the user wishes that this stack will synthesize
        into a **region-agnostic template**. In this case, your code should either
        fail (throw an error, emit a synth error using ``node.addError``) or
        implement some other region-agnostic behavior.

        stability
        :stability: experimental
        """
        return jsii.get(self, "region")

    @builtins.property
    @jsii.member(jsii_name="stackId")
    def stack_id(self) -> str:
        """The ID of the stack.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            Afterresolving , lookslikearn:aws:cloudformation:us-west-2123456789012stack / teststack / 51af3dc0 - da77 - 11e4 - 872e-1234567db123
        """
        return jsii.get(self, "stackId")

    @builtins.property
    @jsii.member(jsii_name="stackName")
    def stack_name(self) -> str:
        """The concrete CloudFormation physical stack name.

        This is either the name defined explicitly in the ``stackName`` prop or
        allocated based on the stack's location in the construct tree. Stacks that
        are directly defined under the app use their construct ``id`` as their stack
        name. Stacks that are defined deeper within the tree will use a hashed naming
        scheme based on the construct path to ensure uniqueness.

        If you wish to obtain the deploy-time AWS::StackName intrinsic,
        you can use ``Aws.stackName`` directly.

        stability
        :stability: experimental
        """
        return jsii.get(self, "stackName")

    @builtins.property
    @jsii.member(jsii_name="synthesizer")
    def synthesizer(self) -> "IStackSynthesizer":
        """Synthesis method for this stack.

        stability
        :stability: experimental
        """
        return jsii.get(self, "synthesizer")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "TagManager":
        """Tags to be applied to the stack.

        stability
        :stability: experimental
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="templateFile")
    def template_file(self) -> str:
        """The name of the CloudFormation template file emitted to the output directory during synthesis.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            MyStack.template.json
        """
        return jsii.get(self, "templateFile")

    @builtins.property
    @jsii.member(jsii_name="templateOptions")
    def template_options(self) -> "ITemplateOptions":
        """Options for CloudFormation template (like version, transform, description).

        stability
        :stability: experimental
        """
        return jsii.get(self, "templateOptions")

    @builtins.property
    @jsii.member(jsii_name="urlSuffix")
    def url_suffix(self) -> str:
        """The Amazon domain suffix for the region in which this stack is defined.

        stability
        :stability: experimental
        """
        return jsii.get(self, "urlSuffix")

    @builtins.property
    @jsii.member(jsii_name="nestedStackParent")
    def nested_stack_parent(self) -> typing.Optional["Stack"]:
        """If this is a nested stack, returns it's parent stack.

        stability
        :stability: experimental
        """
        return jsii.get(self, "nestedStackParent")

    @builtins.property
    @jsii.member(jsii_name="nestedStackResource")
    def nested_stack_resource(self) -> typing.Optional["CfnResource"]:
        """If this is a nested stack, this represents its ``AWS::CloudFormation::Stack`` resource.

        ``undefined`` for top-level (non-nested) stacks.

        stability
        :stability: experimental
        """
        return jsii.get(self, "nestedStackResource")

    @builtins.property
    @jsii.member(jsii_name="parentStack")
    def parent_stack(self) -> typing.Optional["Stack"]:
        """Returns the parent of a nested stack.

        deprecated
        :deprecated: use ``nestedStackParent``

        stability
        :stability: deprecated
        """
        return jsii.get(self, "parentStack")

    @builtins.property
    @jsii.member(jsii_name="terminationProtection")
    def termination_protection(self) -> typing.Optional[bool]:
        """Whether termination protection is enabled for this stack.

        stability
        :stability: experimental
        """
        return jsii.get(self, "terminationProtection")


class Stage(Construct, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.Stage"):
    """An abstract application modeling unit consisting of Stacks that should be deployed together.

    Derive a subclass of ``Stage`` and use it to model a single instance of your
    application.

    You can then instantiate your subclass multiple times to model multiple
    copies of your application which should be be deployed to different
    environments.

    stability
    :stability: experimental
    """
    def __init__(self, scope: "Construct", id: str, *, env: typing.Optional["Environment"]=None, outdir: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param env: Default AWS environment (account/region) for ``Stack``s in this ``Stage``. Stacks defined inside this ``Stage`` with either ``region`` or ``account`` missing from its env will use the corresponding field given here. If either ``region`` or ``account``is is not configured for ``Stack`` (either on the ``Stack`` itself or on the containing ``Stage``), the Stack will be *environment-agnostic*. Environment-agnostic stacks can be deployed to any environment, may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups, will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environments should be configured on the ``Stack``s.
        :param outdir: The output directory into which to emit synthesized artifacts. Can only be specified if this stage is the root stage (the app). If this is specified and this stage is nested within another stage, an error will be thrown. Default: - for nested stages, outdir will be determined as a relative directory to the outdir of the app. For apps, if outdir is not specified, a temporary directory will be created.

        stability
        :stability: experimental
        """
        props = StageProps(env=env, outdir=outdir)

        jsii.create(Stage, self, [scope, id, props])

    @jsii.member(jsii_name="isStage")
    @builtins.classmethod
    def is_stage(cls, x: typing.Any) -> bool:
        """Test whether the given construct is a stage.

        :param x: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "isStage", [x])

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, construct: "IConstruct") -> typing.Optional["Stage"]:
        """Return the stage this construct is contained with, if available.

        If called
        on a nested stage, returns its parent.

        :param construct: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "of", [construct])

    @jsii.member(jsii_name="synth")
    def synth(self, *, skip_validation: typing.Optional[bool]=None) -> _CloudAssembly_32c4802d:
        """Synthesize this stage into a cloud assembly.

        Once an assembly has been synthesized, it cannot be modified. Subsequent
        calls will return the same assembly.

        :param skip_validation: Should we skip construct validation. Default: - false

        stability
        :stability: experimental
        """
        options = StageSynthesisOptions(skip_validation=skip_validation)

        return jsii.invoke(self, "synth", [options])

    @builtins.property
    @jsii.member(jsii_name="artifactId")
    def artifact_id(self) -> str:
        """Artifact ID of the assembly if it is a nested stage. The root stage (app) will return an empty string.

        Derived from the construct path.

        stability
        :stability: experimental
        """
        return jsii.get(self, "artifactId")

    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> str:
        """The name of the stage.

        Based on names of the parent stages separated by
        hypens.

        stability
        :stability: experimental
        """
        return jsii.get(self, "stageName")

    @builtins.property
    @jsii.member(jsii_name="account")
    def account(self) -> typing.Optional[str]:
        """The default account for all resources defined within this stage.

        stability
        :stability: experimental
        """
        return jsii.get(self, "account")

    @builtins.property
    @jsii.member(jsii_name="parentStage")
    def parent_stage(self) -> typing.Optional["Stage"]:
        """The parent stage or ``undefined`` if this is the app.

        -

        stability
        :stability: experimental
        """
        return jsii.get(self, "parentStage")

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[str]:
        """The default region for all resources defined within this stage.

        stability
        :stability: experimental
        """
        return jsii.get(self, "region")


class App(Stage, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.App"):
    """A construct which represents an entire CDK app. This construct is normally the root of the construct tree.

    You would normally define an ``App`` instance in your program's entrypoint,
    then define constructs where the app is used as the parent scope.

    After all the child constructs are defined within the app, you should call
    ``app.synth()`` which will emit a "cloud assembly" from this app into the
    directory specified by ``outdir``. Cloud assemblies includes artifacts such as
    CloudFormation templates and assets that are needed to deploy this app into
    the AWS cloud.

    see
    :see: https://docs.aws.amazon.com/cdk/latest/guide/apps.html
    stability
    :stability: experimental
    """
    def __init__(self, *, auto_synth: typing.Optional[bool]=None, context: typing.Optional[typing.Mapping[str, str]]=None, outdir: typing.Optional[str]=None, runtime_info: typing.Optional[bool]=None, stack_traces: typing.Optional[bool]=None, tree_metadata: typing.Optional[bool]=None) -> None:
        """Initializes a CDK application.

        :param auto_synth: Automatically call ``synth()`` before the program exits. If you set this, you don't have to call ``synth()`` explicitly. Note that this feature is only available for certain programming languages, and calling ``synth()`` is still recommended. Default: true if running via CDK CLI (``CDK_OUTDIR`` is set), ``false`` otherwise
        :param context: Additional context values for the application. Context set by the CLI or the ``context`` key in ``cdk.json`` has precedence. Context can be read from any construct using ``node.getContext(key)``. Default: - no additional context
        :param outdir: The output directory into which to emit synthesized artifacts. Default: - If this value is *not* set, considers the environment variable ``CDK_OUTDIR``. If ``CDK_OUTDIR`` is not defined, uses a temp directory.
        :param runtime_info: Include runtime versioning information in cloud assembly manifest. Default: true runtime info is included unless ``aws:cdk:disable-runtime-info`` is set in the context.
        :param stack_traces: Include construct creation stack trace in the ``aws:cdk:trace`` metadata key of all constructs. Default: true stack traces are included unless ``aws:cdk:disable-stack-trace`` is set in the context.
        :param tree_metadata: Include construct tree metadata as part of the Cloud Assembly. Default: true

        stability
        :stability: experimental
        """
        props = AppProps(auto_synth=auto_synth, context=context, outdir=outdir, runtime_info=runtime_info, stack_traces=stack_traces, tree_metadata=tree_metadata)

        jsii.create(App, self, [props])

    @jsii.member(jsii_name="isApp")
    @builtins.classmethod
    def is_app(cls, obj: typing.Any) -> bool:
        """Checks if an object is an instance of the ``App`` class.

        :param obj: The object to evaluate.

        return
        :return: ``true`` if ``obj`` is an ``App``.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "isApp", [obj])


class AssetStaging(Construct, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.AssetStaging"):
    """Stages a file or directory from a location on the file system into a staging directory.

    This is controlled by the context key 'aws:cdk:asset-staging' and enabled
    by the CLI by default in order to ensure that when the CDK app exists, all
    assets are available for deployment. Otherwise, if an app references assets
    in temporary locations, those will not be available when it exists (see
    https://github.com/aws/aws-cdk/issues/1716).

    The ``stagedPath`` property is a stringified token that represents the location
    of the file or directory after staging. It will be resolved only during the
    "prepare" stage and may be either the original path or the staged path
    depending on the context setting.

    The file/directory are staged based on their content hash (fingerprint). This
    means that only if content was changed, copy will happen.

    stability
    :stability: experimental
    """
    def __init__(self, scope: "Construct", id: str, *, source_path: str, extra_hash: typing.Optional[str]=None, asset_hash: typing.Optional[str]=None, asset_hash_type: typing.Optional["AssetHashType"]=None, bundling: typing.Optional["BundlingOptions"]=None, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional["SymlinkFollowMode"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param source_path: The source file or directory to copy from.
        :param extra_hash: Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise
        :param exclude: Glob patterns to exclude from the copy. Default: - nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER

        stability
        :stability: experimental
        """
        props = AssetStagingProps(source_path=source_path, extra_hash=extra_hash, asset_hash=asset_hash, asset_hash_type=asset_hash_type, bundling=bundling, exclude=exclude, follow=follow)

        jsii.create(AssetStaging, self, [scope, id, props])

    @jsii.member(jsii_name="synthesize")
    def _synthesize(self, session: "ISynthesisSession") -> None:
        """Allows this construct to emit artifacts into the cloud assembly during synthesis.

        This method is usually implemented by framework-level constructs such as ``Stack`` and ``Asset``
        as they participate in synthesizing the cloud assembly.

        :param session: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesize", [session])

    @jsii.python.classproperty
    @jsii.member(jsii_name="BUNDLING_INPUT_DIR")
    def BUNDLING_INPUT_DIR(cls) -> str:
        """The directory inside the bundling container into which the asset sources will be mounted.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "BUNDLING_INPUT_DIR")

    @jsii.python.classproperty
    @jsii.member(jsii_name="BUNDLING_OUTPUT_DIR")
    def BUNDLING_OUTPUT_DIR(cls) -> str:
        """The directory inside the bundling container into which the bundled output should be written.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "BUNDLING_OUTPUT_DIR")

    @builtins.property
    @jsii.member(jsii_name="assetHash")
    def asset_hash(self) -> str:
        """A cryptographic hash of the asset.

        stability
        :stability: experimental
        """
        return jsii.get(self, "assetHash")

    @builtins.property
    @jsii.member(jsii_name="sourceHash")
    def source_hash(self) -> str:
        """A cryptographic hash of the asset.

        deprecated
        :deprecated: see ``assetHash``.

        stability
        :stability: deprecated
        """
        return jsii.get(self, "sourceHash")

    @builtins.property
    @jsii.member(jsii_name="sourcePath")
    def source_path(self) -> str:
        """The path of the asset as it was referenced by the user.

        stability
        :stability: experimental
        """
        return jsii.get(self, "sourcePath")

    @builtins.property
    @jsii.member(jsii_name="stagedPath")
    def staged_path(self) -> str:
        """The path to the asset (stringinfied token).

        If asset staging is disabled, this will just be the original path.
        If asset staging is enabled it will be the staged path.

        stability
        :stability: experimental
        """
        return jsii.get(self, "stagedPath")


class CfnElement(Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.CfnElement"):
    """An element of a CloudFormation stack.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _CfnElementProxy

    def __init__(self, scope: "Construct", id: str) -> None:
        """Creates an entity and binds it to a tree.

        Note that the root of the tree must be a Stack object (not just any Root).

        :param scope: The parent construct.
        :param id: -

        stability
        :stability: experimental
        """
        jsii.create(CfnElement, self, [scope, id])

    @jsii.member(jsii_name="isCfnElement")
    @builtins.classmethod
    def is_cfn_element(cls, x: typing.Any) -> bool:
        """Returns ``true`` if a construct is a stack element (i.e. part of the synthesized cloudformation template).

        Uses duck-typing instead of ``instanceof`` to allow stack elements from different
        versions of this library to be included in the same stack.

        :param x: -

        return
        :return: The construct as a stack element or undefined if it is not a stack element.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "isCfnElement", [x])

    @jsii.member(jsii_name="overrideLogicalId")
    def override_logical_id(self, new_logical_id: str) -> None:
        """Overrides the auto-generated logical ID with a specific ID.

        :param new_logical_id: The new logical ID to use for this stack element.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "overrideLogicalId", [new_logical_id])

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[str]:
        """
        return
        :return:

        the stack trace of the point where this Resource was created from, sourced
        from the +metadata+ entry typed +aws:cdk:logicalId+, and with the bottom-most
        node +internal+ entries filtered.

        stability
        :stability: experimental
        """
        return jsii.get(self, "creationStack")

    @builtins.property
    @jsii.member(jsii_name="logicalId")
    def logical_id(self) -> str:
        """The logical ID for this CloudFormation stack element.

        The logical ID of the element
        is calculated from the path of the resource node in the construct tree.

        To override this value, use ``overrideLogicalId(newLogicalId)``.

        return
        :return:

        the logical ID as a stringified token. This value will only get
        resolved during synthesis.

        stability
        :stability: experimental
        """
        return jsii.get(self, "logicalId")

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> "Stack":
        """The stack in which this element is defined.

        CfnElements must be defined within a stack scope (directly or indirectly).

        stability
        :stability: experimental
        """
        return jsii.get(self, "stack")


class _CfnElementProxy(CfnElement):
    pass

class CfnInclude(CfnElement, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.CfnInclude"):
    """Includes a CloudFormation template into a stack.

    All elements of the template will be merged into
    the current stack, together with any elements created programmatically.

    stability
    :stability: experimental
    """
    def __init__(self, scope: "Construct", id: str, *, template: typing.Mapping[typing.Any, typing.Any]) -> None:
        """Creates an adopted template construct.

        The template will be incorporated into the stack as-is with no changes at all.
        This means that logical IDs of entities within this template may conflict with logical IDs of entities that are part of the
        stack.

        :param scope: The parent construct of this template.
        :param id: The ID of this construct.
        :param template: The CloudFormation template to include in the stack (as is).

        stability
        :stability: experimental
        """
        props = CfnIncludeProps(template=template)

        jsii.create(CfnInclude, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> typing.Mapping[typing.Any, typing.Any]:
        """The included template.

        stability
        :stability: experimental
        """
        return jsii.get(self, "template")


@jsii.implements(IResolvable)
class CfnJson(Construct, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.CfnJson"):
    """Captures a synthesis-time JSON object a CloudFormation reference which resolves during deployment to the resolved values of the JSON object.

    The main use case for this is to overcome a limitation in CloudFormation that
    does not allow using intrinsic functions as dictionary keys (because
    dictionary keys in JSON must be strings). Specifically this is common in IAM
    conditions such as ``StringEquals: { lhs: "rhs" }`` where you want "lhs" to be
    a reference.

    This object is resolvable, so it can be used as a value.

    This construct is backed by a custom resource.

    stability
    :stability: experimental
    """
    def __init__(self, scope: "Construct", id: str, *, value: typing.Any) -> None:
        """
        :param scope: -
        :param id: -
        :param value: The value to resolve. Can be any JavaScript object, including tokens and references in keys or values.

        stability
        :stability: experimental
        """
        props = CfnJsonProps(value=value)

        jsii.create(CfnJson, self, [scope, id, props])

    @jsii.member(jsii_name="resolve")
    def resolve(self, _: "IResolveContext") -> typing.Any:
        """Produce the Token's value at resolution time.

        :param _: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolve", [_])

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> str:
        """This is required in case someone JSON.stringifys an object which refrences this object. Otherwise, we'll get a cyclic JSON reference.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toJSON", [])

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[str]:
        """The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.

        stability
        :stability: experimental
        """
        return jsii.get(self, "creationStack")


class CfnOutput(CfnElement, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.CfnOutput"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: "Construct", id: str, *, value: str, condition: typing.Optional["CfnCondition"]=None, description: typing.Optional[str]=None, export_name: typing.Optional[str]=None) -> None:
        """Creates an CfnOutput value for this stack.

        :param scope: The parent construct.
        :param id: -
        :param value: The value of the property returned by the aws cloudformation describe-stacks command. The value of an output can include literals, parameter references, pseudo-parameters, a mapping value, or intrinsic functions.
        :param condition: A condition to associate with this output value. If the condition evaluates to ``false``, this output value will not be included in the stack. Default: - No condition is associated with the output.
        :param description: A String type that describes the output value. The description can be a maximum of 4 K in length. Default: - No description.
        :param export_name: The name used to export the value of this output across stacks. To import the value from another stack, use ``Fn.importValue(exportName)``. Default: - the output is not exported

        stability
        :stability: experimental
        """
        props = CfnOutputProps(value=value, condition=condition, description=description, export_name=export_name)

        jsii.create(CfnOutput, self, [scope, id, props])


class CfnParameter(CfnElement, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.CfnParameter"):
    """A CloudFormation parameter.

    Use the optional Parameters section to customize your templates.
    Parameters enable you to input custom values to your template each time you create or
    update a stack.

    stability
    :stability: experimental
    """
    def __init__(self, scope: "Construct", id: str, *, allowed_pattern: typing.Optional[str]=None, allowed_values: typing.Optional[typing.List[str]]=None, constraint_description: typing.Optional[str]=None, default: typing.Any=None, description: typing.Optional[str]=None, max_length: typing.Optional[jsii.Number]=None, max_value: typing.Optional[jsii.Number]=None, min_length: typing.Optional[jsii.Number]=None, min_value: typing.Optional[jsii.Number]=None, no_echo: typing.Optional[bool]=None, type: typing.Optional[str]=None) -> None:
        """Creates a parameter construct.

        Note that the name (logical ID) of the parameter will derive from it's ``coname`` and location
        within the stack. Therefore, it is recommended that parameters are defined at the stack level.

        :param scope: The parent construct.
        :param id: -
        :param allowed_pattern: A regular expression that represents the patterns to allow for String types. Default: - No constraints on patterns allowed for parameter.
        :param allowed_values: An array containing the list of values allowed for the parameter. Default: - No constraints on values allowed for parameter.
        :param constraint_description: A string that explains a constraint when the constraint is violated. For example, without a constraint description, a parameter that has an allowed pattern of [A-Za-z0-9]+ displays the following error message when the user specifies an invalid value: Default: - No description with customized error message when user specifies invalid values.
        :param default: A value of the appropriate type for the template to use if no value is specified when a stack is created. If you define constraints for the parameter, you must specify a value that adheres to those constraints. Default: - No default value for parameter.
        :param description: A string of up to 4000 characters that describes the parameter. Default: - No description for the parameter.
        :param max_length: An integer value that determines the largest number of characters you want to allow for String types. Default: - None.
        :param max_value: A numeric value that determines the largest numeric value you want to allow for Number types. Default: - None.
        :param min_length: An integer value that determines the smallest number of characters you want to allow for String types. Default: - None.
        :param min_value: A numeric value that determines the smallest numeric value you want to allow for Number types. Default: - None.
        :param no_echo: Whether to mask the parameter value when anyone makes a call that describes the stack. If you set the value to ``true``, the parameter value is masked with asterisks (``*****``). Default: - Parameter values are not masked.
        :param type: The data type for the parameter (DataType). Default: String

        stability
        :stability: experimental
        """
        props = CfnParameterProps(allowed_pattern=allowed_pattern, allowed_values=allowed_values, constraint_description=constraint_description, default=default, description=description, max_length=max_length, max_value=max_value, min_length=min_length, min_value=min_value, no_echo=no_echo, type=type)

        jsii.create(CfnParameter, self, [scope, id, props])

    @jsii.member(jsii_name="resolve")
    def resolve(self, _context: "IResolveContext") -> typing.Any:
        """
        :param _context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolve", [_context])

    @builtins.property
    @jsii.member(jsii_name="noEcho")
    def no_echo(self) -> bool:
        """Indicates if this parameter is configured with "NoEcho" enabled.

        stability
        :stability: experimental
        """
        return jsii.get(self, "noEcho")

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> "IResolvable":
        """The parameter value as a Token.

        stability
        :stability: experimental
        """
        return jsii.get(self, "value")

    @builtins.property
    @jsii.member(jsii_name="valueAsList")
    def value_as_list(self) -> typing.List[str]:
        """The parameter value, if it represents a string list.

        stability
        :stability: experimental
        """
        return jsii.get(self, "valueAsList")

    @builtins.property
    @jsii.member(jsii_name="valueAsNumber")
    def value_as_number(self) -> jsii.Number:
        """The parameter value, if it represents a number.

        stability
        :stability: experimental
        """
        return jsii.get(self, "valueAsNumber")

    @builtins.property
    @jsii.member(jsii_name="valueAsString")
    def value_as_string(self) -> str:
        """The parameter value, if it represents a string.

        stability
        :stability: experimental
        """
        return jsii.get(self, "valueAsString")


class CfnRefElement(CfnElement, metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.CfnRefElement"):
    """Base class for referenceable CloudFormation constructs which are not Resources.

    These constructs are things like Conditions and Parameters, can be
    referenced by taking the ``.ref`` attribute.

    Resource constructs do not inherit from CfnRefElement because they have their
    own, more specific types returned from the .ref attribute. Also, some
    resources aren't referenceable at all (such as BucketPolicies or GatewayAttachments).

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _CfnRefElementProxy

    def __init__(self, scope: "Construct", id: str) -> None:
        """Creates an entity and binds it to a tree.

        Note that the root of the tree must be a Stack object (not just any Root).

        :param scope: The parent construct.
        :param id: -

        stability
        :stability: experimental
        """
        jsii.create(CfnRefElement, self, [scope, id])

    @builtins.property
    @jsii.member(jsii_name="ref")
    def ref(self) -> str:
        """Return a string that will be resolved to a CloudFormation ``{ Ref }`` for this element.

        If, by any chance, the intrinsic reference of a resource is not a string, you could
        coerce it to an IResolvable through ``Lazy.any({ produce: resource.ref })``.

        stability
        :stability: experimental
        """
        return jsii.get(self, "ref")


class _CfnRefElementProxy(CfnRefElement, jsii.proxy_for(CfnElement)):
    pass

class CfnResource(CfnRefElement, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.CfnResource"):
    """Represents a CloudFormation resource.

    stability
    :stability: experimental
    """
    def __init__(self, scope: "Construct", id: str, *, type: str, properties: typing.Optional[typing.Mapping[str, typing.Any]]=None) -> None:
        """Creates a resource construct.

        :param scope: -
        :param id: -
        :param type: CloudFormation resource type (e.g. ``AWS::S3::Bucket``).
        :param properties: Resource properties. Default: - No resource properties.

        stability
        :stability: experimental
        """
        props = CfnResourceProps(type=type, properties=properties)

        jsii.create(CfnResource, self, [scope, id, props])

    @jsii.member(jsii_name="isCfnResource")
    @builtins.classmethod
    def is_cfn_resource(cls, construct: "IConstruct") -> bool:
        """Check whether the given construct is a CfnResource.

        :param construct: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "isCfnResource", [construct])

    @jsii.member(jsii_name="addDeletionOverride")
    def add_deletion_override(self, path: str) -> None:
        """Syntactic sugar for ``addOverride(path, undefined)``.

        :param path: The path of the value to delete.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addDeletionOverride", [path])

    @jsii.member(jsii_name="addDependsOn")
    def add_depends_on(self, target: "CfnResource") -> None:
        """Indicates that this resource depends on another resource and cannot be provisioned unless the other resource has been successfully provisioned.

        This can be used for resources across stacks (or nested stack) boundaries
        and the dependency will automatically be transferred to the relevant scope.

        :param target: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addDependsOn", [target])

    @jsii.member(jsii_name="addOverride")
    def add_override(self, path: str, value: typing.Any) -> None:
        """Adds an override to the synthesized CloudFormation resource.

        To add a
        property override, either use ``addPropertyOverride`` or prefix ``path`` with
        "Properties." (i.e. ``Properties.TopicName``).

        If the override is nested, separate each nested level using a dot (.) in the path parameter.
        If there is an array as part of the nesting, specify the index in the path.

        For example::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           add_override("Properties.GlobalSecondaryIndexes.0.Projection.NonKeyAttributes", ["myattribute"])
           add_override("Properties.GlobalSecondaryIndexes.1.ProjectionType", "INCLUDE")

        would add the overrides Example::

           "Properties": {
              "GlobalSecondaryIndexes": [
                {
                  "Projection": {
                    "NonKeyAttributes": [ "myattribute" ]
                    ...
                  }
                  ...
                },
                {
                  "ProjectionType": "INCLUDE"
                  ...
                },
              ]
              ...
           }

        :param path: - The path of the property, you can use dot notation to override values in complex types. Any intermdediate keys will be created as needed.
        :param value: - The value. Could be primitive or complex.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addOverride", [path, value])

    @jsii.member(jsii_name="addPropertyDeletionOverride")
    def add_property_deletion_override(self, property_path: str) -> None:
        """Adds an override that deletes the value of a property from the resource definition.

        :param property_path: The path to the property.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addPropertyDeletionOverride", [property_path])

    @jsii.member(jsii_name="addPropertyOverride")
    def add_property_override(self, property_path: str, value: typing.Any) -> None:
        """Adds an override to a resource property.

        Syntactic sugar for ``addOverride("Properties.<...>", value)``.

        :param property_path: The path of the property.
        :param value: The value.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addPropertyOverride", [property_path, value])

    @jsii.member(jsii_name="applyRemovalPolicy")
    def apply_removal_policy(self, policy: typing.Optional["RemovalPolicy"]=None, *, apply_to_update_replace_policy: typing.Optional[bool]=None, default: typing.Optional["RemovalPolicy"]=None) -> None:
        """Sets the deletion policy of the resource based on the removal policy specified.

        :param policy: -
        :param apply_to_update_replace_policy: Apply the same deletion policy to the resource's "UpdateReplacePolicy". Default: true
        :param default: The default policy to apply in case the removal policy is not defined. Default: - Default value is resource specific. To determine the default value for a resoure, please consult that specific resource's documentation.

        stability
        :stability: experimental
        """
        options = RemovalPolicyOptions(apply_to_update_replace_policy=apply_to_update_replace_policy, default=default)

        return jsii.invoke(self, "applyRemovalPolicy", [policy, options])

    @jsii.member(jsii_name="getAtt")
    def get_att(self, attribute_name: str) -> "Reference":
        """Returns a token for an runtime attribute of this resource.

        Ideally, use generated attribute accessors (e.g. ``resource.arn``), but this can be used for future compatibility
        in case there is no generated attribute.

        :param attribute_name: The name of the attribute.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getAtt", [attribute_name])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of this construct.

        return
        :return: a string representation of this resource

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toString", [])

    @jsii.member(jsii_name="validateProperties")
    def _validate_properties(self, _properties: typing.Any) -> None:
        """
        :param _properties: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "validateProperties", [_properties])

    @builtins.property
    @jsii.member(jsii_name="cfnOptions")
    def cfn_options(self) -> "ICfnResourceOptions":
        """Options for this resource, such as condition, update policy etc.

        stability
        :stability: experimental
        """
        return jsii.get(self, "cfnOptions")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="cfnResourceType")
    def cfn_resource_type(self) -> str:
        """AWS resource type.

        stability
        :stability: experimental
        """
        return jsii.get(self, "cfnResourceType")

    @builtins.property
    @jsii.member(jsii_name="updatedProperites")
    def _updated_properites(self) -> typing.Mapping[str, typing.Any]:
        """Return properties modified after initiation.

        Resources that expose mutable properties should override this function to
        collect and return the properties object for this resource.

        stability
        :stability: experimental
        """
        return jsii.get(self, "updatedProperites")


class CfnRule(CfnRefElement, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.CfnRule"):
    """The Rules that define template constraints in an AWS Service Catalog portfolio describe when end users can use the template and which values they can specify for parameters that are declared in the AWS CloudFormation template used to create the product they are attempting to use.

    Rules
    are useful for preventing end users from inadvertently specifying an incorrect value.
    For example, you can add a rule to verify whether end users specified a valid subnet in a
    given VPC or used m1.small instance types for test environments. AWS CloudFormation uses
    rules to validate parameter values before it creates the resources for the product.

    A rule can include a RuleCondition property and must include an Assertions property.
    For each rule, you can define only one rule condition; you can define one or more asserts within the Assertions property.
    You define a rule condition and assertions by using rule-specific intrinsic functions.

    stability
    :stability: experimental
    link:
    :link:: https://docs.aws.amazon.com/servicecatalog/latest/adminguide/reference-template_constraint_rules.html
    """
    def __init__(self, scope: "Construct", id: str, *, assertions: typing.Optional[typing.List["CfnRuleAssertion"]]=None, rule_condition: typing.Optional["ICfnConditionExpression"]=None) -> None:
        """Creates and adds a rule.

        :param scope: The parent construct.
        :param id: -
        :param assertions: Assertions which define the rule. Default: - No assertions for the rule.
        :param rule_condition: If the rule condition evaluates to false, the rule doesn't take effect. If the function in the rule condition evaluates to true, expressions in each assert are evaluated and applied. Default: - Rule's assertions will always take effect.

        stability
        :stability: experimental
        """
        props = CfnRuleProps(assertions=assertions, rule_condition=rule_condition)

        jsii.create(CfnRule, self, [scope, id, props])

    @jsii.member(jsii_name="addAssertion")
    def add_assertion(self, condition: "ICfnConditionExpression", description: str) -> None:
        """Adds an assertion to the rule.

        :param condition: The expression to evaluation.
        :param description: The description of the assertion.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addAssertion", [condition, description])


@jsii.implements(IInspectable)
class CfnStack(CfnResource, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.CfnStack"):
    """A CloudFormation ``AWS::CloudFormation::Stack``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html
    cloudformationResource:
    :cloudformationResource:: AWS::CloudFormation::Stack
    """
    def __init__(self, scope: "Construct", id: str, *, template_url: str, notification_arns: typing.Optional[typing.List[str]]=None, parameters: typing.Optional[typing.Union["IResolvable", typing.Mapping[str, str]]]=None, tags: typing.Optional[typing.List["CfnTag"]]=None, timeout_in_minutes: typing.Optional[jsii.Number]=None) -> None:
        """Create a new ``AWS::CloudFormation::Stack``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param template_url: ``AWS::CloudFormation::Stack.TemplateURL``.
        :param notification_arns: ``AWS::CloudFormation::Stack.NotificationARNs``.
        :param parameters: ``AWS::CloudFormation::Stack.Parameters``.
        :param tags: ``AWS::CloudFormation::Stack.Tags``.
        :param timeout_in_minutes: ``AWS::CloudFormation::Stack.TimeoutInMinutes``.
        """
        props = CfnStackProps(template_url=template_url, notification_arns=notification_arns, parameters=parameters, tags=tags, timeout_in_minutes=timeout_in_minutes)

        jsii.create(CfnStack, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: "Construct", id: str, resource_attributes: typing.Any, *, finder: "ICfnFinder") -> "CfnStack":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "TreeInspector") -> None:
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
    def tags(self) -> "TagManager":
        """``AWS::CloudFormation::Stack.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="templateUrl")
    def template_url(self) -> str:
        """``AWS::CloudFormation::Stack.TemplateURL``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-templateurl
        """
        return jsii.get(self, "templateUrl")

    @template_url.setter
    def template_url(self, value: str) -> None:
        jsii.set(self, "templateUrl", value)

    @builtins.property
    @jsii.member(jsii_name="notificationArns")
    def notification_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::CloudFormation::Stack.NotificationARNs``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-notificationarns
        """
        return jsii.get(self, "notificationArns")

    @notification_arns.setter
    def notification_arns(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "notificationArns", value)

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Optional[typing.Union["IResolvable", typing.Mapping[str, str]]]:
        """``AWS::CloudFormation::Stack.Parameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-parameters
        """
        return jsii.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: typing.Optional[typing.Union["IResolvable", typing.Mapping[str, str]]]) -> None:
        jsii.set(self, "parameters", value)

    @builtins.property
    @jsii.member(jsii_name="timeoutInMinutes")
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        """``AWS::CloudFormation::Stack.TimeoutInMinutes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-timeoutinminutes
        """
        return jsii.get(self, "timeoutInMinutes")

    @timeout_in_minutes.setter
    def timeout_in_minutes(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "timeoutInMinutes", value)


@jsii.implements(IInspectable)
class CfnWaitCondition(CfnResource, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.CfnWaitCondition"):
    """A CloudFormation ``AWS::CloudFormation::WaitCondition``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html
    cloudformationResource:
    :cloudformationResource:: AWS::CloudFormation::WaitCondition
    """
    def __init__(self, scope: "Construct", id: str, *, count: typing.Optional[jsii.Number]=None, handle: typing.Optional[str]=None, timeout: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::CloudFormation::WaitCondition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param count: ``AWS::CloudFormation::WaitCondition.Count``.
        :param handle: ``AWS::CloudFormation::WaitCondition.Handle``.
        :param timeout: ``AWS::CloudFormation::WaitCondition.Timeout``.
        """
        props = CfnWaitConditionProps(count=count, handle=handle, timeout=timeout)

        jsii.create(CfnWaitCondition, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: "Construct", id: str, resource_attributes: typing.Any, *, finder: "ICfnFinder") -> "CfnWaitCondition":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "TreeInspector") -> None:
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
    @jsii.member(jsii_name="attrData")
    def attr_data(self) -> "IResolvable":
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Data
        """
        return jsii.get(self, "attrData")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> typing.Optional[jsii.Number]:
        """``AWS::CloudFormation::WaitCondition.Count``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-count
        """
        return jsii.get(self, "count")

    @count.setter
    def count(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "count", value)

    @builtins.property
    @jsii.member(jsii_name="handle")
    def handle(self) -> typing.Optional[str]:
        """``AWS::CloudFormation::WaitCondition.Handle``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-handle
        """
        return jsii.get(self, "handle")

    @handle.setter
    def handle(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "handle", value)

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[str]:
        """``AWS::CloudFormation::WaitCondition.Timeout``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-timeout
        """
        return jsii.get(self, "timeout")

    @timeout.setter
    def timeout(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "timeout", value)


@jsii.implements(IInspectable)
class CfnWaitConditionHandle(CfnResource, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.CfnWaitConditionHandle"):
    """A CloudFormation ``AWS::CloudFormation::WaitConditionHandle``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitconditionhandle.html
    cloudformationResource:
    :cloudformationResource:: AWS::CloudFormation::WaitConditionHandle
    """
    def __init__(self, scope: "Construct", id: str) -> None:
        """Create a new ``AWS::CloudFormation::WaitConditionHandle``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        """
        jsii.create(CfnWaitConditionHandle, self, [scope, id])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: "Construct", id: str, resource_attributes: typing.Any, *, finder: "ICfnFinder") -> "CfnWaitConditionHandle":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "TreeInspector") -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")


class CustomResource(Resource, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.CustomResource"):
    """Custom resource that is implemented using a Lambda.

    As a custom resource author, you should be publishing a subclass of this class
    that hides the choice of provider, and accepts a strongly-typed properties
    object with the properties your provider accepts.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::CloudFormation::CustomResource
    """
    def __init__(self, scope: "Construct", id: str, *, service_token: str, pascal_case_properties: typing.Optional[bool]=None, properties: typing.Optional[typing.Mapping[str, typing.Any]]=None, removal_policy: typing.Optional["RemovalPolicy"]=None, resource_type: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param service_token: The ARN of the provider which implements this custom resource type. You can implement a provider by listening to raw AWS CloudFormation events and specify the ARN of an SNS topic (``topic.topicArn``) or the ARN of an AWS Lambda function (``lambda.functionArn``) or use the CDK's custom `resource provider framework <https://docs.aws.amazon.com/cdk/api/latest/docs/custom-resources-readme.html>`_ which makes it easier to implement robust providers. Provider framework:: // use the provider framework from aws-cdk/custom-resources: const provider = new custom_resources.Provider({ onEventHandler: myOnEventLambda, isCompleteHandler: myIsCompleteLambda, // optional }); new CustomResource(this, 'MyResource', { serviceToken: provider.serviceToken }); AWS Lambda function:: // invoke an AWS Lambda function when a lifecycle event occurs: serviceToken: myFunction.functionArn SNS topic:: // publish lifecycle events to an SNS topic: serviceToken: myTopic.topicArn
        :param pascal_case_properties: Convert all property keys to pascal case. Default: false
        :param properties: Properties to pass to the Lambda. Default: - No properties.
        :param removal_policy: The policy to apply when this resource is removed from the application. Default: cdk.RemovalPolicy.Destroy
        :param resource_type: For custom resources, you can specify AWS::CloudFormation::CustomResource (the default) as the resource type, or you can specify your own resource type name. For example, you can use "Custom::MyCustomResourceTypeName". Custom resource type names must begin with "Custom::" and can include alphanumeric characters and the following characters: _@-. You can specify a custom resource type name up to a maximum length of 60 characters. You cannot change the type during an update. Using your own resource type names helps you quickly differentiate the types of custom resources in your stack. For example, if you had two custom resources that conduct two different ping tests, you could name their type as Custom::PingTester to make them easily identifiable as ping testers (instead of using AWS::CloudFormation::CustomResource). Default: - AWS::CloudFormation::CustomResource

        stability
        :stability: experimental
        """
        props = CustomResourceProps(service_token=service_token, pascal_case_properties=pascal_case_properties, properties=properties, removal_policy=removal_policy, resource_type=resource_type)

        jsii.create(CustomResource, self, [scope, id, props])

    @jsii.member(jsii_name="getAtt")
    def get_att(self, attribute_name: str) -> "Reference":
        """Returns the value of an attribute of the custom resource of an arbitrary type.

        Attributes are returned from the custom resource provider through the
        ``Data`` map where the key is the attribute name.

        :param attribute_name: the name of the attribute.

        return
        :return:

        a token for ``Fn::GetAtt``. Use ``Token.asXxx`` to encode the returned ``Reference`` as a specific type or
        use the convenience ``getAttString`` for string attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getAtt", [attribute_name])

    @jsii.member(jsii_name="getAttString")
    def get_att_string(self, attribute_name: str) -> str:
        """Returns the value of an attribute of the custom resource of type string.

        Attributes are returned from the custom resource provider through the
        ``Data`` map where the key is the attribute name.

        :param attribute_name: the name of the attribute.

        return
        :return: a token for ``Fn::GetAtt`` encoded as a string.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getAttString", [attribute_name])

    @builtins.property
    @jsii.member(jsii_name="ref")
    def ref(self) -> str:
        """The physical name of this custom resource.

        stability
        :stability: experimental
        """
        return jsii.get(self, "ref")


class NestedStack(Stack, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.NestedStack"):
    """A CloudFormation nested stack.

    When you apply template changes to update a top-level stack, CloudFormation
    updates the top-level stack and initiates an update to its nested stacks.
    CloudFormation updates the resources of modified nested stacks, but does not
    update the resources of unmodified nested stacks.

    Furthermore, this stack will not be treated as an independent deployment
    artifact (won't be listed in "cdk list" or deployable through "cdk deploy"),
    but rather only synthesized as a template and uploaded as an asset to S3.

    Cross references of resource attributes between the parent stack and the
    nested stack will automatically be translated to stack parameters and
    outputs.

    stability
    :stability: experimental
    """
    def __init__(self, scope: "Construct", id: str, *, notification_arns: typing.Optional[typing.List[str]]=None, parameters: typing.Optional[typing.Mapping[str, str]]=None, timeout: typing.Optional["Duration"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param notification_arns: The Simple Notification Service (SNS) topics to publish stack related events. Default: - notifications are not sent for this stack.
        :param parameters: The set value pairs that represent the parameters passed to CloudFormation when this nested stack is created. Each parameter has a name corresponding to a parameter defined in the embedded template and a value representing the value that you want to set for the parameter. The nested stack construct will automatically synthesize parameters in order to bind references from the parent stack(s) into the nested stack. Default: - no user-defined parameters are passed to the nested stack
        :param timeout: The length of time that CloudFormation waits for the nested stack to reach the CREATE_COMPLETE state. When CloudFormation detects that the nested stack has reached the CREATE_COMPLETE state, it marks the nested stack resource as CREATE_COMPLETE in the parent stack and resumes creating the parent stack. If the timeout period expires before the nested stack reaches CREATE_COMPLETE, CloudFormation marks the nested stack as failed and rolls back both the nested stack and parent stack. Default: - no timeout

        stability
        :stability: experimental
        """
        props = NestedStackProps(notification_arns=notification_arns, parameters=parameters, timeout=timeout)

        jsii.create(NestedStack, self, [scope, id, props])

    @jsii.member(jsii_name="isNestedStack")
    @builtins.classmethod
    def is_nested_stack(cls, x: typing.Any) -> bool:
        """Checks if ``x`` is an object of type ``NestedStack``.

        :param x: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "isNestedStack", [x])

    @jsii.member(jsii_name="setParameter")
    def set_parameter(self, name: str, value: str) -> None:
        """Assign a value to one of the nested stack parameters.

        :param name: The parameter name (ID).
        :param value: The value to assign.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "setParameter", [name, value])

    @builtins.property
    @jsii.member(jsii_name="stackId")
    def stack_id(self) -> str:
        """An attribute that represents the ID of the stack.

        This is a context aware attribute:

        - If this is referenced from the parent stack, it will return ``{ "Ref": "LogicalIdOfNestedStackResource" }``.
        - If this is referenced from the context of the nested stack, it will return ``{ "Ref": "AWS::StackId" }``

        stability
        :stability: experimental
        attribute:
        :attribute:: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "arn:aws:cloudformation:us-east-2:123456789012:stack/mystack-mynestedstack-sggfrhxhum7w/f449b250-b969-11e0-a185-5081d0136786"
        """
        return jsii.get(self, "stackId")

    @builtins.property
    @jsii.member(jsii_name="stackName")
    def stack_name(self) -> str:
        """An attribute that represents the name of the nested stack.

        This is a context aware attribute:

        - If this is referenced from the parent stack, it will return a token that parses the name from the stack ID.
        - If this is referenced from the context of the nested stack, it will return ``{ "Ref": "AWS::StackName" }``

        stability
        :stability: experimental
        attribute:
        :attribute:: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            mystack - mynestedstack - sggfrhxhum7w
        """
        return jsii.get(self, "stackName")

    @builtins.property
    @jsii.member(jsii_name="templateFile")
    def template_file(self) -> str:
        """The name of the CloudFormation template file emitted to the output directory during synthesis.

        stability
        :stability: experimental
        """
        return jsii.get(self, "templateFile")

    @builtins.property
    @jsii.member(jsii_name="nestedStackResource")
    def nested_stack_resource(self) -> typing.Optional["CfnResource"]:
        """If this is a nested stack, this represents its ``AWS::CloudFormation::Stack`` resource.

        ``undefined`` for top-level (non-nested) stacks.

        stability
        :stability: experimental
        """
        return jsii.get(self, "nestedStackResource")


@jsii.implements(ICfnConditionExpression, IResolvable)
class CfnCondition(CfnElement, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.CfnCondition"):
    """Represents a CloudFormation condition, for resources which must be conditionally created and the determination must be made at deploy time.

    stability
    :stability: experimental
    """
    def __init__(self, scope: "Construct", id: str, *, expression: typing.Optional["ICfnConditionExpression"]=None) -> None:
        """Build a new condition.

        The condition must be constructed with a condition token,
        that the condition is based on.

        :param scope: -
        :param id: -
        :param expression: The expression that the condition will evaluate. Default: - None.

        stability
        :stability: experimental
        """
        props = CfnConditionProps(expression=expression)

        jsii.create(CfnCondition, self, [scope, id, props])

    @jsii.member(jsii_name="resolve")
    def resolve(self, _context: "IResolveContext") -> typing.Any:
        """Synthesizes the condition.

        :param _context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolve", [_context])

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> typing.Optional["ICfnConditionExpression"]:
        """The condition statement.

        stability
        :stability: experimental
        """
        return jsii.get(self, "expression")

    @expression.setter
    def expression(self, value: typing.Optional["ICfnConditionExpression"]) -> None:
        jsii.set(self, "expression", value)


@jsii.implements(IInspectable)
class CfnCustomResource(CfnResource, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.CfnCustomResource"):
    """A CloudFormation ``AWS::CloudFormation::CustomResource``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html
    cloudformationResource:
    :cloudformationResource:: AWS::CloudFormation::CustomResource
    """
    def __init__(self, scope: "Construct", id: str, *, service_token: str) -> None:
        """Create a new ``AWS::CloudFormation::CustomResource``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param service_token: ``AWS::CloudFormation::CustomResource.ServiceToken``.
        """
        props = CfnCustomResourceProps(service_token=service_token)

        jsii.create(CfnCustomResource, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: "Construct", id: str, resource_attributes: typing.Any, *, finder: "ICfnFinder") -> "CfnCustomResource":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "TreeInspector") -> None:
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
    @jsii.member(jsii_name="serviceToken")
    def service_token(self) -> str:
        """``AWS::CloudFormation::CustomResource.ServiceToken``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html#cfn-customresource-servicetoken
        """
        return jsii.get(self, "serviceToken")

    @service_token.setter
    def service_token(self, value: str) -> None:
        jsii.set(self, "serviceToken", value)


@jsii.implements(IInspectable)
class CfnMacro(CfnResource, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.CfnMacro"):
    """A CloudFormation ``AWS::CloudFormation::Macro``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html
    cloudformationResource:
    :cloudformationResource:: AWS::CloudFormation::Macro
    """
    def __init__(self, scope: "Construct", id: str, *, function_name: str, name: str, description: typing.Optional[str]=None, log_group_name: typing.Optional[str]=None, log_role_arn: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::CloudFormation::Macro``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param function_name: ``AWS::CloudFormation::Macro.FunctionName``.
        :param name: ``AWS::CloudFormation::Macro.Name``.
        :param description: ``AWS::CloudFormation::Macro.Description``.
        :param log_group_name: ``AWS::CloudFormation::Macro.LogGroupName``.
        :param log_role_arn: ``AWS::CloudFormation::Macro.LogRoleARN``.
        """
        props = CfnMacroProps(function_name=function_name, name=name, description=description, log_group_name=log_group_name, log_role_arn=log_role_arn)

        jsii.create(CfnMacro, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: "Construct", id: str, resource_attributes: typing.Any, *, finder: "ICfnFinder") -> "CfnMacro":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "TreeInspector") -> None:
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
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> str:
        """``AWS::CloudFormation::Macro.FunctionName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-functionname
        """
        return jsii.get(self, "functionName")

    @function_name.setter
    def function_name(self, value: str) -> None:
        jsii.set(self, "functionName", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::CloudFormation::Macro.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::CloudFormation::Macro.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> typing.Optional[str]:
        """``AWS::CloudFormation::Macro.LogGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-loggroupname
        """
        return jsii.get(self, "logGroupName")

    @log_group_name.setter
    def log_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="logRoleArn")
    def log_role_arn(self) -> typing.Optional[str]:
        """``AWS::CloudFormation::Macro.LogRoleARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-logrolearn
        """
        return jsii.get(self, "logRoleArn")

    @log_role_arn.setter
    def log_role_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "logRoleArn", value)


class CfnMapping(CfnRefElement, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.CfnMapping"):
    """Represents a CloudFormation mapping.

    stability
    :stability: experimental
    """
    def __init__(self, scope: "Construct", id: str, *, mapping: typing.Optional[typing.Mapping[str, typing.Mapping[str, typing.Any]]]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param mapping: Mapping of key to a set of corresponding set of named values. The key identifies a map of name-value pairs and must be unique within the mapping. For example, if you want to set values based on a region, you can create a mapping that uses the region name as a key and contains the values you want to specify for each specific region. Default: - No mapping.

        stability
        :stability: experimental
        """
        props = CfnMappingProps(mapping=mapping)

        jsii.create(CfnMapping, self, [scope, id, props])

    @jsii.member(jsii_name="findInMap")
    def find_in_map(self, key1: str, key2: str) -> str:
        """
        :param key1: -
        :param key2: -

        return
        :return: A reference to a value in the map based on the two keys.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "findInMap", [key1, key2])

    @jsii.member(jsii_name="setValue")
    def set_value(self, key1: str, key2: str, value: typing.Any) -> None:
        """Sets a value in the map based on the two keys.

        :param key1: -
        :param key2: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "setValue", [key1, key2, value])


__all__ = [
    "App",
    "AppProps",
    "Arn",
    "ArnComponents",
    "AssetHashType",
    "AssetOptions",
    "AssetStaging",
    "AssetStagingProps",
    "Aws",
    "BootstraplessSynthesizer",
    "BootstraplessSynthesizerProps",
    "BundlingDockerImage",
    "BundlingOptions",
    "CfnAutoScalingReplacingUpdate",
    "CfnAutoScalingRollingUpdate",
    "CfnAutoScalingScheduledAction",
    "CfnCapabilities",
    "CfnCodeDeployLambdaAliasUpdate",
    "CfnCondition",
    "CfnConditionProps",
    "CfnCreationPolicy",
    "CfnCustomResource",
    "CfnCustomResourceProps",
    "CfnDeletionPolicy",
    "CfnDynamicReference",
    "CfnDynamicReferenceProps",
    "CfnDynamicReferenceService",
    "CfnElement",
    "CfnInclude",
    "CfnIncludeProps",
    "CfnJson",
    "CfnJsonProps",
    "CfnMacro",
    "CfnMacroProps",
    "CfnMapping",
    "CfnMappingProps",
    "CfnOutput",
    "CfnOutputProps",
    "CfnParameter",
    "CfnParameterProps",
    "CfnRefElement",
    "CfnResource",
    "CfnResourceAutoScalingCreationPolicy",
    "CfnResourceProps",
    "CfnResourceSignal",
    "CfnRule",
    "CfnRuleAssertion",
    "CfnRuleProps",
    "CfnStack",
    "CfnStackProps",
    "CfnTag",
    "CfnUpdatePolicy",
    "CfnWaitCondition",
    "CfnWaitConditionHandle",
    "CfnWaitConditionProps",
    "ConcreteDependable",
    "Construct",
    "ConstructNode",
    "ConstructOrder",
    "ContextProvider",
    "CopyOptions",
    "CustomResource",
    "CustomResourceProps",
    "CustomResourceProvider",
    "CustomResourceProviderProps",
    "CustomResourceProviderRuntime",
    "DefaultStackSynthesizer",
    "DefaultStackSynthesizerProps",
    "DefaultTokenResolver",
    "DependableTrait",
    "Dependency",
    "DockerBuildOptions",
    "DockerImageAssetLocation",
    "DockerImageAssetSource",
    "DockerVolume",
    "Duration",
    "EncodingOptions",
    "Environment",
    "FileAssetLocation",
    "FileAssetPackaging",
    "FileAssetSource",
    "FileSystem",
    "FingerprintOptions",
    "Fn",
    "FromCloudFormationOptions",
    "GetContextKeyOptions",
    "GetContextKeyResult",
    "GetContextValueOptions",
    "GetContextValueResult",
    "IAnyProducer",
    "IAspect",
    "IAsset",
    "ICfnConditionExpression",
    "ICfnFinder",
    "ICfnResourceOptions",
    "IConstruct",
    "IDependable",
    "IFragmentConcatenator",
    "IInspectable",
    "IListProducer",
    "INumberProducer",
    "IPostProcessor",
    "IResolvable",
    "IResolveContext",
    "IResource",
    "IStackSynthesizer",
    "IStringProducer",
    "ISynthesisSession",
    "ITaggable",
    "ITemplateOptions",
    "ITokenMapper",
    "ITokenResolver",
    "Intrinsic",
    "Lazy",
    "LazyAnyValueOptions",
    "LazyListValueOptions",
    "LazyStringValueOptions",
    "LegacyStackSynthesizer",
    "NestedStack",
    "NestedStackProps",
    "NestedStackSynthesizer",
    "PhysicalName",
    "Reference",
    "RemovalPolicy",
    "RemovalPolicyOptions",
    "RemoveTag",
    "ResolveOptions",
    "Resource",
    "ResourceProps",
    "ScopedAws",
    "SecretValue",
    "SecretsManagerSecretOptions",
    "Size",
    "SizeConversionOptions",
    "SizeRoundingBehavior",
    "Stack",
    "StackProps",
    "Stage",
    "StageProps",
    "StageSynthesisOptions",
    "StringConcat",
    "SymlinkFollowMode",
    "SynthesisOptions",
    "Tag",
    "TagManager",
    "TagManagerOptions",
    "TagProps",
    "TagType",
    "TimeConversionOptions",
    "Token",
    "Tokenization",
    "TokenizedStringFragments",
    "TreeInspector",
    "ValidationError",
    "ValidationResult",
    "ValidationResults",
]

publication.publish()
