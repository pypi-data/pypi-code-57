import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (Construct as _Construct_f50a3f53, SecretValue as _SecretValue_99478b8b, Duration as _Duration_5170c158, IConstruct as _IConstruct_db0cc7e3)
from ..aws_cloudformation import (CloudFormationCapabilities as _CloudFormationCapabilities_979dd343)
from ..aws_codebuild import (IProject as _IProject_2a66e54e, BuildEnvironmentVariable as _BuildEnvironmentVariable_dda665dd)
from ..aws_codecommit import (IRepository as _IRepository_91f381de)
from ..aws_codedeploy import (IEcsDeploymentGroup as _IEcsDeploymentGroup_458435fe, IServerDeploymentGroup as _IServerDeploymentGroup_b0b16347)
from ..aws_codepipeline import (ActionProperties as _ActionProperties_8f5d7a9d, ActionConfig as _ActionConfig_c379766c, IStage as _IStage_b7c853a7, ActionBindOptions as _ActionBindOptions_530c352f, IAction as _IAction_369e77ae, CommonActionProps as _CommonActionProps_dd892888, Artifact as _Artifact_af6d98e9, CommonAwsActionProps as _CommonAwsActionProps_3b39a615, ArtifactPath as _ArtifactPath_8730c13b)
from ..aws_ecr import (IRepository as _IRepository_aa6e452c)
from ..aws_ecs import (IBaseService as _IBaseService_de6ed13e)
from ..aws_events import (Rule as _Rule_c38e0b39, IRuleTarget as _IRuleTarget_41800a77, RuleProps as _RuleProps_d60f0abf)
from ..aws_iam import (IRole as _IRole_e69bbae4, PolicyStatement as _PolicyStatement_f75dc775)
from ..aws_lambda import (IFunction as _IFunction_1c1de0bc)
from ..aws_s3 import (IBucket as _IBucket_25bad983, BucketAccessControl as _BucketAccessControl_028b0d87)
from ..aws_sns import (ITopic as _ITopic_ef0ebe0e)


@jsii.implements(_IAction_369e77ae)
class Action(metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.aws_codepipeline_actions.Action"):
    """Low-level class for generic CodePipeline Actions.

    WARNING: this class should not be externally exposed, but is currently visible
    because of a limitation of jsii (https://github.com/aws/jsii/issues/524).

    This class will disappear in a future release and should not be used.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ActionProxy

    def __init__(self, *, action_name: str, artifact_bounds: _ActionArtifactBounds_30ad3b7c, category: _ActionCategory_83677319, provider: str, account: typing.Optional[str]=None, inputs: typing.Optional[typing.List[_Artifact_af6d98e9]]=None, outputs: typing.Optional[typing.List[_Artifact_af6d98e9]]=None, owner: typing.Optional[str]=None, region: typing.Optional[str]=None, resource: typing.Optional[_IResource_72f7ee7e]=None, role: typing.Optional[_IRole_e69bbae4]=None, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None, version: typing.Optional[str]=None) -> None:
        """
        :param action_name: 
        :param artifact_bounds: 
        :param category: The category of the action. The category defines which action type the owner (the entity that performs the action) performs.
        :param provider: The service provider that the action calls.
        :param account: The account the Action is supposed to live in. For Actions backed by resources, this is inferred from the Stack {@link resource} is part of. However, some Actions, like the CloudFormation ones, are not backed by any resource, and they still might want to be cross-account. In general, a concrete Action class should specify either {@link resource}, or {@link account} - but not both.
        :param inputs: 
        :param outputs: 
        :param owner: 
        :param region: The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param resource: The optional resource that is backing this Action. This is used for automatically handling Actions backed by resources from a different account and/or region.
        :param role: 
        :param run_order: The order in which AWS CodePipeline runs this action. For more information, see the AWS CodePipeline User Guide. https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html#action-requirements
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names
        :param version: 

        stability
        :stability: experimental
        """
        action_properties = _ActionProperties_8f5d7a9d(action_name=action_name, artifact_bounds=artifact_bounds, category=category, provider=provider, account=account, inputs=inputs, outputs=outputs, owner=owner, region=region, resource=resource, role=role, run_order=run_order, variables_namespace=variables_namespace, version=version)

        jsii.create(Action, self, [action_properties])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_f50a3f53, stage: _IStage_b7c853a7, *, bucket: _IBucket_25bad983, role: _IRole_e69bbae4) -> _ActionConfig_c379766c:
        """
        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bind", [scope, stage, options])

    @jsii.member(jsii_name="bound")
    @abc.abstractmethod
    def _bound(self, scope: _Construct_f50a3f53, stage: _IStage_b7c853a7, *, bucket: _IBucket_25bad983, role: _IRole_e69bbae4) -> _ActionConfig_c379766c:
        """The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, name: str, target: typing.Optional[_IRuleTarget_41800a77]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_bus: typing.Optional[_IEventBus_ed4f1700]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, schedule: typing.Optional[_Schedule_11a70620]=None, targets: typing.Optional[typing.List[_IRuleTarget_41800a77]]=None) -> _Rule_c38e0b39:
        """
        :param name: -
        :param target: -
        :param description: A description of the rule's purpose. Default: - No description.
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: Describes which events EventBridge routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon EventBridge User Guide. Default: - None.
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: The schedule or rate (frequency) that determines when EventBridge runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon EventBridge User Guide. Default: - None.
        :param targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.

        stability
        :stability: experimental
        """
        options = _RuleProps_d60f0abf(description=description, enabled=enabled, event_bus=event_bus, event_pattern=event_pattern, rule_name=rule_name, schedule=schedule, targets=targets)

        return jsii.invoke(self, "onStateChange", [name, target, options])

    @jsii.member(jsii_name="variableExpression")
    def _variable_expression(self, variable_name: str) -> str:
        """
        :param variable_name: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "variableExpression", [variable_name])

    @builtins.property
    @jsii.member(jsii_name="actionProperties")
    def action_properties(self) -> _ActionProperties_8f5d7a9d:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "actionProperties")


class _ActionProxy(Action):
    @jsii.member(jsii_name="bound")
    def _bound(self, scope: _Construct_f50a3f53, stage: _IStage_b7c853a7, *, bucket: _IBucket_25bad983, role: _IRole_e69bbae4) -> _ActionConfig_c379766c:
        """The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [scope, stage, options])


class AlexaSkillDeployAction(Action, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codepipeline_actions.AlexaSkillDeployAction"):
    """Deploys the skill to Alexa.

    stability
    :stability: experimental
    """
    def __init__(self, *, client_id: str, client_secret: _SecretValue_99478b8b, input: _Artifact_af6d98e9, refresh_token: _SecretValue_99478b8b, skill_id: str, parameter_overrides_artifact: typing.Optional[_Artifact_af6d98e9]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None) -> None:
        """
        :param client_id: The client id of the developer console token.
        :param client_secret: The client secret of the developer console token.
        :param input: The source artifact containing the voice model and skill manifest.
        :param refresh_token: The refresh token of the developer console token.
        :param skill_id: The Alexa skill id.
        :param parameter_overrides_artifact: An optional artifact containing overrides for the skill manifest.
        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        stability
        :stability: experimental
        """
        props = AlexaSkillDeployActionProps(client_id=client_id, client_secret=client_secret, input=input, refresh_token=refresh_token, skill_id=skill_id, parameter_overrides_artifact=parameter_overrides_artifact, action_name=action_name, run_order=run_order, variables_namespace=variables_namespace)

        jsii.create(AlexaSkillDeployAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, _scope: _Construct_f50a3f53, _stage: _IStage_b7c853a7, *, bucket: _IBucket_25bad983, role: _IRole_e69bbae4) -> _ActionConfig_c379766c:
        """The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param _stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        _options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [_scope, _stage, _options])


@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.AlexaSkillDeployActionProps", jsii_struct_bases=[_CommonActionProps_dd892888], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'variables_namespace': 'variablesNamespace', 'client_id': 'clientId', 'client_secret': 'clientSecret', 'input': 'input', 'refresh_token': 'refreshToken', 'skill_id': 'skillId', 'parameter_overrides_artifact': 'parameterOverridesArtifact'})
class AlexaSkillDeployActionProps(_CommonActionProps_dd892888):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None, client_id: str, client_secret: _SecretValue_99478b8b, input: _Artifact_af6d98e9, refresh_token: _SecretValue_99478b8b, skill_id: str, parameter_overrides_artifact: typing.Optional[_Artifact_af6d98e9]=None) -> None:
        """Construction properties of the {@link AlexaSkillDeployAction Alexa deploy Action}.

        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param client_id: The client id of the developer console token.
        :param client_secret: The client secret of the developer console token.
        :param input: The source artifact containing the voice model and skill manifest.
        :param refresh_token: The refresh token of the developer console token.
        :param skill_id: The Alexa skill id.
        :param parameter_overrides_artifact: An optional artifact containing overrides for the skill manifest.

        stability
        :stability: experimental
        """
        self._values = {
            'action_name': action_name,
            'client_id': client_id,
            'client_secret': client_secret,
            'input': input,
            'refresh_token': refresh_token,
            'skill_id': skill_id,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if variables_namespace is not None: self._values["variables_namespace"] = variables_namespace
        if parameter_overrides_artifact is not None: self._values["parameter_overrides_artifact"] = parameter_overrides_artifact

    @builtins.property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        stability
        :stability: experimental
        """
        return self._values.get('action_name')

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        stability
        :stability: experimental
        """
        return self._values.get('run_order')

    @builtins.property
    def variables_namespace(self) -> typing.Optional[str]:
        """The name of the namespace to use for variables emitted by this action.

        default
        :default:

        - a name will be generated, based on the stage and action names,
          if any of the action's variables were referenced - otherwise,
          no namespace will be set

        stability
        :stability: experimental
        """
        return self._values.get('variables_namespace')

    @builtins.property
    def client_id(self) -> str:
        """The client id of the developer console token.

        stability
        :stability: experimental
        """
        return self._values.get('client_id')

    @builtins.property
    def client_secret(self) -> _SecretValue_99478b8b:
        """The client secret of the developer console token.

        stability
        :stability: experimental
        """
        return self._values.get('client_secret')

    @builtins.property
    def input(self) -> _Artifact_af6d98e9:
        """The source artifact containing the voice model and skill manifest.

        stability
        :stability: experimental
        """
        return self._values.get('input')

    @builtins.property
    def refresh_token(self) -> _SecretValue_99478b8b:
        """The refresh token of the developer console token.

        stability
        :stability: experimental
        """
        return self._values.get('refresh_token')

    @builtins.property
    def skill_id(self) -> str:
        """The Alexa skill id.

        stability
        :stability: experimental
        """
        return self._values.get('skill_id')

    @builtins.property
    def parameter_overrides_artifact(self) -> typing.Optional[_Artifact_af6d98e9]:
        """An optional artifact containing overrides for the skill manifest.

        stability
        :stability: experimental
        """
        return self._values.get('parameter_overrides_artifact')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AlexaSkillDeployActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class BitBucketSourceAction(Action, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codepipeline_actions.BitBucketSourceAction"):
    """A CodePipeline source action for BitBucket.

    stability
    :stability: experimental
    """
    def __init__(self, *, connection_arn: str, output: _Artifact_af6d98e9, owner: str, repo: str, branch: typing.Optional[str]=None, code_build_clone_output: typing.Optional[bool]=None, role: typing.Optional[_IRole_e69bbae4]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None) -> None:
        """
        :param connection_arn: The ARN of the CodeStar Connection created in the AWS console that has permissions to access this BitBucket repository.
        :param output: The output artifact that this action produces. Can be used as input for further pipeline actions.
        :param owner: The owning user or organization of the repository.
        :param repo: The name of the repository.
        :param branch: The branch to build. Default: 'master'
        :param code_build_clone_output: Whether the output should be the contents of the repository (which is the default), or a link that allows CodeBuild to clone the repository before building. **Note**: if this option is true, then only CodeBuild actions can use the resulting {@link output}. Default: false
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        stability
        :stability: experimental
        """
        props = BitBucketSourceActionProps(connection_arn=connection_arn, output=output, owner=owner, repo=repo, branch=branch, code_build_clone_output=code_build_clone_output, role=role, action_name=action_name, run_order=run_order, variables_namespace=variables_namespace)

        jsii.create(BitBucketSourceAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, _scope: _Construct_f50a3f53, _stage: _IStage_b7c853a7, *, bucket: _IBucket_25bad983, role: _IRole_e69bbae4) -> _ActionConfig_c379766c:
        """The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param _stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [_scope, _stage, options])


@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.BitBucketSourceActionProps", jsii_struct_bases=[_CommonAwsActionProps_3b39a615], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'variables_namespace': 'variablesNamespace', 'role': 'role', 'connection_arn': 'connectionArn', 'output': 'output', 'owner': 'owner', 'repo': 'repo', 'branch': 'branch', 'code_build_clone_output': 'codeBuildCloneOutput'})
class BitBucketSourceActionProps(_CommonAwsActionProps_3b39a615):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None, role: typing.Optional[_IRole_e69bbae4]=None, connection_arn: str, output: _Artifact_af6d98e9, owner: str, repo: str, branch: typing.Optional[str]=None, code_build_clone_output: typing.Optional[bool]=None) -> None:
        """Construction properties for {@link BitBucketSourceAction}.

        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param connection_arn: The ARN of the CodeStar Connection created in the AWS console that has permissions to access this BitBucket repository.
        :param output: The output artifact that this action produces. Can be used as input for further pipeline actions.
        :param owner: The owning user or organization of the repository.
        :param repo: The name of the repository.
        :param branch: The branch to build. Default: 'master'
        :param code_build_clone_output: Whether the output should be the contents of the repository (which is the default), or a link that allows CodeBuild to clone the repository before building. **Note**: if this option is true, then only CodeBuild actions can use the resulting {@link output}. Default: false

        stability
        :stability: experimental
        """
        self._values = {
            'action_name': action_name,
            'connection_arn': connection_arn,
            'output': output,
            'owner': owner,
            'repo': repo,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if variables_namespace is not None: self._values["variables_namespace"] = variables_namespace
        if role is not None: self._values["role"] = role
        if branch is not None: self._values["branch"] = branch
        if code_build_clone_output is not None: self._values["code_build_clone_output"] = code_build_clone_output

    @builtins.property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        stability
        :stability: experimental
        """
        return self._values.get('action_name')

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        stability
        :stability: experimental
        """
        return self._values.get('run_order')

    @builtins.property
    def variables_namespace(self) -> typing.Optional[str]:
        """The name of the namespace to use for variables emitted by this action.

        default
        :default:

        - a name will be generated, based on the stage and action names,
          if any of the action's variables were referenced - otherwise,
          no namespace will be set

        stability
        :stability: experimental
        """
        return self._values.get('variables_namespace')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def connection_arn(self) -> str:
        """The ARN of the CodeStar Connection created in the AWS console that has permissions to access this BitBucket repository.

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/connections-create.html
        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "arn:aws:codestar-connections:us-east-1:123456789012:connection/12345678-abcd-12ab-34cdef5678gh"
        """
        return self._values.get('connection_arn')

    @builtins.property
    def output(self) -> _Artifact_af6d98e9:
        """The output artifact that this action produces.

        Can be used as input for further pipeline actions.

        stability
        :stability: experimental
        """
        return self._values.get('output')

    @builtins.property
    def owner(self) -> str:
        """The owning user or organization of the repository.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "aws"
        """
        return self._values.get('owner')

    @builtins.property
    def repo(self) -> str:
        """The name of the repository.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "aws-cdk"
        """
        return self._values.get('repo')

    @builtins.property
    def branch(self) -> typing.Optional[str]:
        """The branch to build.

        default
        :default: 'master'

        stability
        :stability: experimental
        """
        return self._values.get('branch')

    @builtins.property
    def code_build_clone_output(self) -> typing.Optional[bool]:
        """Whether the output should be the contents of the repository (which is the default), or a link that allows CodeBuild to clone the repository before building.

        **Note**: if this option is true,
        then only CodeBuild actions can use the resulting {@link output}.

        default
        :default: false

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-CodestarConnectionSource.html#action-reference-CodestarConnectionSource-config
        stability
        :stability: experimental
        """
        return self._values.get('code_build_clone_output')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BitBucketSourceActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class CacheControl(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codepipeline_actions.CacheControl"):
    """Used for HTTP cache-control header, which influences downstream caches.

    Use the provided static factory methods to construct instances of this class.
    Used in the {@link S3DeployActionProps.cacheControl} property.

    see
    :see: https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.9
    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(cls, s: str) -> "CacheControl":
        """Allows you to create an arbitrary cache control directive, in case our support is missing a method for a particular directive.

        :param s: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromString", [s])

    @jsii.member(jsii_name="maxAge")
    @builtins.classmethod
    def max_age(cls, t: _Duration_5170c158) -> "CacheControl":
        """The 'max-age' cache control directive.

        :param t: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "maxAge", [t])

    @jsii.member(jsii_name="mustRevalidate")
    @builtins.classmethod
    def must_revalidate(cls) -> "CacheControl":
        """The 'must-revalidate' cache control directive.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "mustRevalidate", [])

    @jsii.member(jsii_name="noCache")
    @builtins.classmethod
    def no_cache(cls) -> "CacheControl":
        """The 'no-cache' cache control directive.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "noCache", [])

    @jsii.member(jsii_name="noTransform")
    @builtins.classmethod
    def no_transform(cls) -> "CacheControl":
        """The 'no-transform' cache control directive.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "noTransform", [])

    @jsii.member(jsii_name="proxyRevalidate")
    @builtins.classmethod
    def proxy_revalidate(cls) -> "CacheControl":
        """The 'proxy-revalidate' cache control directive.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "proxyRevalidate", [])

    @jsii.member(jsii_name="setPrivate")
    @builtins.classmethod
    def set_private(cls) -> "CacheControl":
        """The 'private' cache control directive.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "setPrivate", [])

    @jsii.member(jsii_name="setPublic")
    @builtins.classmethod
    def set_public(cls) -> "CacheControl":
        """The 'public' cache control directive.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "setPublic", [])

    @jsii.member(jsii_name="sMaxAge")
    @builtins.classmethod
    def s_max_age(cls, t: _Duration_5170c158) -> "CacheControl":
        """The 's-max-age' cache control directive.

        :param t: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "sMaxAge", [t])

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> str:
        """the actual text value of the created directive.

        stability
        :stability: experimental
        """
        return jsii.get(self, "value")

    @value.setter
    def value(self, value: str) -> None:
        jsii.set(self, "value", value)


class CloudFormationCreateReplaceChangeSetAction(Action, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codepipeline_actions.CloudFormationCreateReplaceChangeSetAction"):
    """CodePipeline action to prepare a change set.

    Creates the change set if it doesn't exist based on the stack name and template that you submit.
    If the change set exists, AWS CloudFormation deletes it, and then creates a new one.

    stability
    :stability: experimental
    """
    def __init__(self, *, admin_permissions: bool, change_set_name: str, stack_name: str, template_path: _ArtifactPath_8730c13b, account: typing.Optional[str]=None, capabilities: typing.Optional[typing.List[_CloudFormationCapabilities_979dd343]]=None, deployment_role: typing.Optional[_IRole_e69bbae4]=None, extra_inputs: typing.Optional[typing.List[_Artifact_af6d98e9]]=None, output: typing.Optional[_Artifact_af6d98e9]=None, output_file_name: typing.Optional[str]=None, parameter_overrides: typing.Optional[typing.Mapping[str, typing.Any]]=None, region: typing.Optional[str]=None, template_configuration: typing.Optional[_ArtifactPath_8730c13b]=None, role: typing.Optional[_IRole_e69bbae4]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None) -> None:
        """
        :param admin_permissions: Whether to grant full permissions to CloudFormation while deploying this template. Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you don't specify any alternatives. The default role that will be created for you will have full (i.e., ``*``) permissions on all resources, and the deployment will have named IAM capabilities (i.e., able to create all IAM resources). This is a shorthand that you can use if you fully trust the templates that are deployed in this pipeline. If you want more fine-grained permissions, use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation deployment is allowed to do.
        :param change_set_name: Name of the change set to create or update.
        :param stack_name: The name of the stack to apply this action to.
        :param template_path: Input artifact with the ChangeSet's CloudFormation template.
        :param account: The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does. Default: - action resides in the same account as the pipeline
        :param capabilities: Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM`` if your stack template contains AWS Identity and Access Management (IAM) resources. For more information see the link below. Default: None, unless ``adminPermissions`` is true
        :param deployment_role: IAM role to assume when deploying changes. If not specified, a fresh role is created. The role is created with zero permissions unless ``adminPermissions`` is true, in which case the role will have full permissions. Default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).
        :param extra_inputs: The list of additional input Artifacts for this Action. This is especially useful when used in conjunction with the ``parameterOverrides`` property. For example, if you have: parameterOverrides: { 'Param1': action1.outputArtifact.bucketName, 'Param2': action2.outputArtifact.objectKey, } , if the output Artifacts of ``action1`` and ``action2`` were not used to set either the ``templateConfiguration`` or the ``templatePath`` properties, you need to make sure to include them in the ``extraInputs`` - otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.
        :param output: The name of the output artifact to generate. Only applied if ``outputFileName`` is set as well. Default: Automatically generated artifact name.
        :param output_file_name: A name for the filename in the output artifact to store the AWS CloudFormation call's result. The file will contain the result of the call to AWS CloudFormation (for example the call to UpdateStack or CreateChangeSet). AWS CodePipeline adds the file to the output artifact after performing the specified action. Default: No output artifact generated
        :param parameter_overrides: Additional template parameters. Template parameters specified here take precedence over template parameters found in the artifact specified by the ``templateConfiguration`` property. We recommend that you use the template configuration file to specify most of your parameter values. Use parameter overrides to specify only dynamic parameter values (values that are unknown until you run the pipeline). All parameter names must be present in the stack template. Note: the entire object cannot be more than 1kB. Default: No overrides
        :param region: The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param template_configuration: Input artifact to use for template parameters values and stack policy. The template configuration file should contain a JSON object that should look like this: ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information, see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_. Note that if you include sensitive information, such as passwords, restrict access to this file. Default: No template configuration based on input artifacts
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        stability
        :stability: experimental
        """
        props = CloudFormationCreateReplaceChangeSetActionProps(admin_permissions=admin_permissions, change_set_name=change_set_name, stack_name=stack_name, template_path=template_path, account=account, capabilities=capabilities, deployment_role=deployment_role, extra_inputs=extra_inputs, output=output, output_file_name=output_file_name, parameter_overrides=parameter_overrides, region=region, template_configuration=template_configuration, role=role, action_name=action_name, run_order=run_order, variables_namespace=variables_namespace)

        jsii.create(CloudFormationCreateReplaceChangeSetAction, self, [props])

    @jsii.member(jsii_name="addToDeploymentRolePolicy")
    def add_to_deployment_role_policy(self, statement: _PolicyStatement_f75dc775) -> bool:
        """Add statement to the service role assumed by CloudFormation while executing this action.

        :param statement: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToDeploymentRolePolicy", [statement])

    @jsii.member(jsii_name="bound")
    def _bound(self, scope: _Construct_f50a3f53, stage: _IStage_b7c853a7, *, bucket: _IBucket_25bad983, role: _IRole_e69bbae4) -> _ActionConfig_c379766c:
        """The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [scope, stage, options])

    @builtins.property
    @jsii.member(jsii_name="deploymentRole")
    def deployment_role(self) -> _IRole_e69bbae4:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "deploymentRole")


@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.CloudFormationCreateReplaceChangeSetActionProps", jsii_struct_bases=[_CommonAwsActionProps_3b39a615], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'variables_namespace': 'variablesNamespace', 'role': 'role', 'admin_permissions': 'adminPermissions', 'change_set_name': 'changeSetName', 'stack_name': 'stackName', 'template_path': 'templatePath', 'account': 'account', 'capabilities': 'capabilities', 'deployment_role': 'deploymentRole', 'extra_inputs': 'extraInputs', 'output': 'output', 'output_file_name': 'outputFileName', 'parameter_overrides': 'parameterOverrides', 'region': 'region', 'template_configuration': 'templateConfiguration'})
class CloudFormationCreateReplaceChangeSetActionProps(_CommonAwsActionProps_3b39a615):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None, role: typing.Optional[_IRole_e69bbae4]=None, admin_permissions: bool, change_set_name: str, stack_name: str, template_path: _ArtifactPath_8730c13b, account: typing.Optional[str]=None, capabilities: typing.Optional[typing.List[_CloudFormationCapabilities_979dd343]]=None, deployment_role: typing.Optional[_IRole_e69bbae4]=None, extra_inputs: typing.Optional[typing.List[_Artifact_af6d98e9]]=None, output: typing.Optional[_Artifact_af6d98e9]=None, output_file_name: typing.Optional[str]=None, parameter_overrides: typing.Optional[typing.Mapping[str, typing.Any]]=None, region: typing.Optional[str]=None, template_configuration: typing.Optional[_ArtifactPath_8730c13b]=None) -> None:
        """Properties for the CloudFormationCreateReplaceChangeSetAction.

        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param admin_permissions: Whether to grant full permissions to CloudFormation while deploying this template. Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you don't specify any alternatives. The default role that will be created for you will have full (i.e., ``*``) permissions on all resources, and the deployment will have named IAM capabilities (i.e., able to create all IAM resources). This is a shorthand that you can use if you fully trust the templates that are deployed in this pipeline. If you want more fine-grained permissions, use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation deployment is allowed to do.
        :param change_set_name: Name of the change set to create or update.
        :param stack_name: The name of the stack to apply this action to.
        :param template_path: Input artifact with the ChangeSet's CloudFormation template.
        :param account: The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does. Default: - action resides in the same account as the pipeline
        :param capabilities: Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM`` if your stack template contains AWS Identity and Access Management (IAM) resources. For more information see the link below. Default: None, unless ``adminPermissions`` is true
        :param deployment_role: IAM role to assume when deploying changes. If not specified, a fresh role is created. The role is created with zero permissions unless ``adminPermissions`` is true, in which case the role will have full permissions. Default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).
        :param extra_inputs: The list of additional input Artifacts for this Action. This is especially useful when used in conjunction with the ``parameterOverrides`` property. For example, if you have: parameterOverrides: { 'Param1': action1.outputArtifact.bucketName, 'Param2': action2.outputArtifact.objectKey, } , if the output Artifacts of ``action1`` and ``action2`` were not used to set either the ``templateConfiguration`` or the ``templatePath`` properties, you need to make sure to include them in the ``extraInputs`` - otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.
        :param output: The name of the output artifact to generate. Only applied if ``outputFileName`` is set as well. Default: Automatically generated artifact name.
        :param output_file_name: A name for the filename in the output artifact to store the AWS CloudFormation call's result. The file will contain the result of the call to AWS CloudFormation (for example the call to UpdateStack or CreateChangeSet). AWS CodePipeline adds the file to the output artifact after performing the specified action. Default: No output artifact generated
        :param parameter_overrides: Additional template parameters. Template parameters specified here take precedence over template parameters found in the artifact specified by the ``templateConfiguration`` property. We recommend that you use the template configuration file to specify most of your parameter values. Use parameter overrides to specify only dynamic parameter values (values that are unknown until you run the pipeline). All parameter names must be present in the stack template. Note: the entire object cannot be more than 1kB. Default: No overrides
        :param region: The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param template_configuration: Input artifact to use for template parameters values and stack policy. The template configuration file should contain a JSON object that should look like this: ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information, see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_. Note that if you include sensitive information, such as passwords, restrict access to this file. Default: No template configuration based on input artifacts

        stability
        :stability: experimental
        """
        self._values = {
            'action_name': action_name,
            'admin_permissions': admin_permissions,
            'change_set_name': change_set_name,
            'stack_name': stack_name,
            'template_path': template_path,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if variables_namespace is not None: self._values["variables_namespace"] = variables_namespace
        if role is not None: self._values["role"] = role
        if account is not None: self._values["account"] = account
        if capabilities is not None: self._values["capabilities"] = capabilities
        if deployment_role is not None: self._values["deployment_role"] = deployment_role
        if extra_inputs is not None: self._values["extra_inputs"] = extra_inputs
        if output is not None: self._values["output"] = output
        if output_file_name is not None: self._values["output_file_name"] = output_file_name
        if parameter_overrides is not None: self._values["parameter_overrides"] = parameter_overrides
        if region is not None: self._values["region"] = region
        if template_configuration is not None: self._values["template_configuration"] = template_configuration

    @builtins.property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        stability
        :stability: experimental
        """
        return self._values.get('action_name')

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        stability
        :stability: experimental
        """
        return self._values.get('run_order')

    @builtins.property
    def variables_namespace(self) -> typing.Optional[str]:
        """The name of the namespace to use for variables emitted by this action.

        default
        :default:

        - a name will be generated, based on the stage and action names,
          if any of the action's variables were referenced - otherwise,
          no namespace will be set

        stability
        :stability: experimental
        """
        return self._values.get('variables_namespace')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def admin_permissions(self) -> bool:
        """Whether to grant full permissions to CloudFormation while deploying this template.

        Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you
        don't specify any alternatives.

        The default role that will be created for you will have full (i.e., ``*``)
        permissions on all resources, and the deployment will have named IAM
        capabilities (i.e., able to create all IAM resources).

        This is a shorthand that you can use if you fully trust the templates that
        are deployed in this pipeline. If you want more fine-grained permissions,
        use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation
        deployment is allowed to do.

        stability
        :stability: experimental
        """
        return self._values.get('admin_permissions')

    @builtins.property
    def change_set_name(self) -> str:
        """Name of the change set to create or update.

        stability
        :stability: experimental
        """
        return self._values.get('change_set_name')

    @builtins.property
    def stack_name(self) -> str:
        """The name of the stack to apply this action to.

        stability
        :stability: experimental
        """
        return self._values.get('stack_name')

    @builtins.property
    def template_path(self) -> _ArtifactPath_8730c13b:
        """Input artifact with the ChangeSet's CloudFormation template.

        stability
        :stability: experimental
        """
        return self._values.get('template_path')

    @builtins.property
    def account(self) -> typing.Optional[str]:
        """The AWS account this Action is supposed to operate in.

        **Note**: if you specify the ``role`` property,
        this is ignored - the action will operate in the same region the passed role does.

        default
        :default: - action resides in the same account as the pipeline

        stability
        :stability: experimental
        """
        return self._values.get('account')

    @builtins.property
    def capabilities(self) -> typing.Optional[typing.List[_CloudFormationCapabilities_979dd343]]:
        """Acknowledge certain changes made as part of deployment.

        For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation
        might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM``
        if your stack template contains AWS Identity and Access Management (IAM) resources. For more
        information see the link below.

        default
        :default: None, unless ``adminPermissions`` is true

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
        stability
        :stability: experimental
        """
        return self._values.get('capabilities')

    @builtins.property
    def deployment_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """IAM role to assume when deploying changes.

        If not specified, a fresh role is created. The role is created with zero
        permissions unless ``adminPermissions`` is true, in which case the role will have
        full permissions.

        default
        :default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).

        stability
        :stability: experimental
        """
        return self._values.get('deployment_role')

    @builtins.property
    def extra_inputs(self) -> typing.Optional[typing.List[_Artifact_af6d98e9]]:
        """The list of additional input Artifacts for this Action.

        This is especially useful when used in conjunction with the ``parameterOverrides`` property.
        For example, if you have:

        parameterOverrides: {
        'Param1': action1.outputArtifact.bucketName,
        'Param2': action2.outputArtifact.objectKey,
        }

        , if the output Artifacts of ``action1`` and ``action2`` were not used to
        set either the ``templateConfiguration`` or the ``templatePath`` properties,
        you need to make sure to include them in the ``extraInputs`` -
        otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.

        stability
        :stability: experimental
        """
        return self._values.get('extra_inputs')

    @builtins.property
    def output(self) -> typing.Optional[_Artifact_af6d98e9]:
        """The name of the output artifact to generate.

        Only applied if ``outputFileName`` is set as well.

        default
        :default: Automatically generated artifact name.

        stability
        :stability: experimental
        """
        return self._values.get('output')

    @builtins.property
    def output_file_name(self) -> typing.Optional[str]:
        """A name for the filename in the output artifact to store the AWS CloudFormation call's result.

        The file will contain the result of the call to AWS CloudFormation (for example
        the call to UpdateStack or CreateChangeSet).

        AWS CodePipeline adds the file to the output artifact after performing
        the specified action.

        default
        :default: No output artifact generated

        stability
        :stability: experimental
        """
        return self._values.get('output_file_name')

    @builtins.property
    def parameter_overrides(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Additional template parameters.

        Template parameters specified here take precedence over template parameters
        found in the artifact specified by the ``templateConfiguration`` property.

        We recommend that you use the template configuration file to specify
        most of your parameter values. Use parameter overrides to specify only
        dynamic parameter values (values that are unknown until you run the
        pipeline).

        All parameter names must be present in the stack template.

        Note: the entire object cannot be more than 1kB.

        default
        :default: No overrides

        stability
        :stability: experimental
        """
        return self._values.get('parameter_overrides')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """The AWS region the given Action resides in.

        Note that a cross-region Pipeline requires replication buckets to function correctly.
        You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property.
        If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets,
        that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack.

        default
        :default: the Action resides in the same region as the Pipeline

        stability
        :stability: experimental
        """
        return self._values.get('region')

    @builtins.property
    def template_configuration(self) -> typing.Optional[_ArtifactPath_8730c13b]:
        """Input artifact to use for template parameters values and stack policy.

        The template configuration file should contain a JSON object that should look like this:
        ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information,
        see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_.

        Note that if you include sensitive information, such as passwords, restrict access to this
        file.

        default
        :default: No template configuration based on input artifacts

        stability
        :stability: experimental
        """
        return self._values.get('template_configuration')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CloudFormationCreateReplaceChangeSetActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class CloudFormationCreateUpdateStackAction(Action, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codepipeline_actions.CloudFormationCreateUpdateStackAction"):
    """CodePipeline action to deploy a stack.

    Creates the stack if the specified stack doesn't exist. If the stack exists,
    AWS CloudFormation updates the stack. Use this action to update existing
    stacks.

    AWS CodePipeline won't replace the stack, and will fail deployment if the
    stack is in a failed state. Use ``ReplaceOnFailure`` for an action that
    will delete and recreate the stack to try and recover from failed states.

    Use this action to automatically replace failed stacks without recovering or
    troubleshooting them. You would typically choose this mode for testing.

    stability
    :stability: experimental
    """
    def __init__(self, *, admin_permissions: bool, stack_name: str, template_path: _ArtifactPath_8730c13b, account: typing.Optional[str]=None, capabilities: typing.Optional[typing.List[_CloudFormationCapabilities_979dd343]]=None, deployment_role: typing.Optional[_IRole_e69bbae4]=None, extra_inputs: typing.Optional[typing.List[_Artifact_af6d98e9]]=None, output: typing.Optional[_Artifact_af6d98e9]=None, output_file_name: typing.Optional[str]=None, parameter_overrides: typing.Optional[typing.Mapping[str, typing.Any]]=None, region: typing.Optional[str]=None, replace_on_failure: typing.Optional[bool]=None, template_configuration: typing.Optional[_ArtifactPath_8730c13b]=None, role: typing.Optional[_IRole_e69bbae4]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None) -> None:
        """
        :param admin_permissions: Whether to grant full permissions to CloudFormation while deploying this template. Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you don't specify any alternatives. The default role that will be created for you will have full (i.e., ``*``) permissions on all resources, and the deployment will have named IAM capabilities (i.e., able to create all IAM resources). This is a shorthand that you can use if you fully trust the templates that are deployed in this pipeline. If you want more fine-grained permissions, use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation deployment is allowed to do.
        :param stack_name: The name of the stack to apply this action to.
        :param template_path: Input artifact with the CloudFormation template to deploy.
        :param account: The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does. Default: - action resides in the same account as the pipeline
        :param capabilities: Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM`` if your stack template contains AWS Identity and Access Management (IAM) resources. For more information see the link below. Default: None, unless ``adminPermissions`` is true
        :param deployment_role: IAM role to assume when deploying changes. If not specified, a fresh role is created. The role is created with zero permissions unless ``adminPermissions`` is true, in which case the role will have full permissions. Default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).
        :param extra_inputs: The list of additional input Artifacts for this Action. This is especially useful when used in conjunction with the ``parameterOverrides`` property. For example, if you have: parameterOverrides: { 'Param1': action1.outputArtifact.bucketName, 'Param2': action2.outputArtifact.objectKey, } , if the output Artifacts of ``action1`` and ``action2`` were not used to set either the ``templateConfiguration`` or the ``templatePath`` properties, you need to make sure to include them in the ``extraInputs`` - otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.
        :param output: The name of the output artifact to generate. Only applied if ``outputFileName`` is set as well. Default: Automatically generated artifact name.
        :param output_file_name: A name for the filename in the output artifact to store the AWS CloudFormation call's result. The file will contain the result of the call to AWS CloudFormation (for example the call to UpdateStack or CreateChangeSet). AWS CodePipeline adds the file to the output artifact after performing the specified action. Default: No output artifact generated
        :param parameter_overrides: Additional template parameters. Template parameters specified here take precedence over template parameters found in the artifact specified by the ``templateConfiguration`` property. We recommend that you use the template configuration file to specify most of your parameter values. Use parameter overrides to specify only dynamic parameter values (values that are unknown until you run the pipeline). All parameter names must be present in the stack template. Note: the entire object cannot be more than 1kB. Default: No overrides
        :param region: The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param replace_on_failure: Replace the stack if it's in a failed state. If this is set to true and the stack is in a failed state (one of ROLLBACK_COMPLETE, ROLLBACK_FAILED, CREATE_FAILED, DELETE_FAILED, or UPDATE_ROLLBACK_FAILED), AWS CloudFormation deletes the stack and then creates a new stack. If this is not set to true and the stack is in a failed state, the deployment fails. Default: false
        :param template_configuration: Input artifact to use for template parameters values and stack policy. The template configuration file should contain a JSON object that should look like this: ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information, see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_. Note that if you include sensitive information, such as passwords, restrict access to this file. Default: No template configuration based on input artifacts
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        stability
        :stability: experimental
        """
        props = CloudFormationCreateUpdateStackActionProps(admin_permissions=admin_permissions, stack_name=stack_name, template_path=template_path, account=account, capabilities=capabilities, deployment_role=deployment_role, extra_inputs=extra_inputs, output=output, output_file_name=output_file_name, parameter_overrides=parameter_overrides, region=region, replace_on_failure=replace_on_failure, template_configuration=template_configuration, role=role, action_name=action_name, run_order=run_order, variables_namespace=variables_namespace)

        jsii.create(CloudFormationCreateUpdateStackAction, self, [props])

    @jsii.member(jsii_name="addToDeploymentRolePolicy")
    def add_to_deployment_role_policy(self, statement: _PolicyStatement_f75dc775) -> bool:
        """Add statement to the service role assumed by CloudFormation while executing this action.

        :param statement: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToDeploymentRolePolicy", [statement])

    @jsii.member(jsii_name="bound")
    def _bound(self, scope: _Construct_f50a3f53, stage: _IStage_b7c853a7, *, bucket: _IBucket_25bad983, role: _IRole_e69bbae4) -> _ActionConfig_c379766c:
        """The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [scope, stage, options])

    @builtins.property
    @jsii.member(jsii_name="deploymentRole")
    def deployment_role(self) -> _IRole_e69bbae4:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "deploymentRole")


@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.CloudFormationCreateUpdateStackActionProps", jsii_struct_bases=[_CommonAwsActionProps_3b39a615], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'variables_namespace': 'variablesNamespace', 'role': 'role', 'admin_permissions': 'adminPermissions', 'stack_name': 'stackName', 'template_path': 'templatePath', 'account': 'account', 'capabilities': 'capabilities', 'deployment_role': 'deploymentRole', 'extra_inputs': 'extraInputs', 'output': 'output', 'output_file_name': 'outputFileName', 'parameter_overrides': 'parameterOverrides', 'region': 'region', 'replace_on_failure': 'replaceOnFailure', 'template_configuration': 'templateConfiguration'})
class CloudFormationCreateUpdateStackActionProps(_CommonAwsActionProps_3b39a615):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None, role: typing.Optional[_IRole_e69bbae4]=None, admin_permissions: bool, stack_name: str, template_path: _ArtifactPath_8730c13b, account: typing.Optional[str]=None, capabilities: typing.Optional[typing.List[_CloudFormationCapabilities_979dd343]]=None, deployment_role: typing.Optional[_IRole_e69bbae4]=None, extra_inputs: typing.Optional[typing.List[_Artifact_af6d98e9]]=None, output: typing.Optional[_Artifact_af6d98e9]=None, output_file_name: typing.Optional[str]=None, parameter_overrides: typing.Optional[typing.Mapping[str, typing.Any]]=None, region: typing.Optional[str]=None, replace_on_failure: typing.Optional[bool]=None, template_configuration: typing.Optional[_ArtifactPath_8730c13b]=None) -> None:
        """Properties for the CloudFormationCreateUpdateStackAction.

        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param admin_permissions: Whether to grant full permissions to CloudFormation while deploying this template. Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you don't specify any alternatives. The default role that will be created for you will have full (i.e., ``*``) permissions on all resources, and the deployment will have named IAM capabilities (i.e., able to create all IAM resources). This is a shorthand that you can use if you fully trust the templates that are deployed in this pipeline. If you want more fine-grained permissions, use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation deployment is allowed to do.
        :param stack_name: The name of the stack to apply this action to.
        :param template_path: Input artifact with the CloudFormation template to deploy.
        :param account: The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does. Default: - action resides in the same account as the pipeline
        :param capabilities: Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM`` if your stack template contains AWS Identity and Access Management (IAM) resources. For more information see the link below. Default: None, unless ``adminPermissions`` is true
        :param deployment_role: IAM role to assume when deploying changes. If not specified, a fresh role is created. The role is created with zero permissions unless ``adminPermissions`` is true, in which case the role will have full permissions. Default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).
        :param extra_inputs: The list of additional input Artifacts for this Action. This is especially useful when used in conjunction with the ``parameterOverrides`` property. For example, if you have: parameterOverrides: { 'Param1': action1.outputArtifact.bucketName, 'Param2': action2.outputArtifact.objectKey, } , if the output Artifacts of ``action1`` and ``action2`` were not used to set either the ``templateConfiguration`` or the ``templatePath`` properties, you need to make sure to include them in the ``extraInputs`` - otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.
        :param output: The name of the output artifact to generate. Only applied if ``outputFileName`` is set as well. Default: Automatically generated artifact name.
        :param output_file_name: A name for the filename in the output artifact to store the AWS CloudFormation call's result. The file will contain the result of the call to AWS CloudFormation (for example the call to UpdateStack or CreateChangeSet). AWS CodePipeline adds the file to the output artifact after performing the specified action. Default: No output artifact generated
        :param parameter_overrides: Additional template parameters. Template parameters specified here take precedence over template parameters found in the artifact specified by the ``templateConfiguration`` property. We recommend that you use the template configuration file to specify most of your parameter values. Use parameter overrides to specify only dynamic parameter values (values that are unknown until you run the pipeline). All parameter names must be present in the stack template. Note: the entire object cannot be more than 1kB. Default: No overrides
        :param region: The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param replace_on_failure: Replace the stack if it's in a failed state. If this is set to true and the stack is in a failed state (one of ROLLBACK_COMPLETE, ROLLBACK_FAILED, CREATE_FAILED, DELETE_FAILED, or UPDATE_ROLLBACK_FAILED), AWS CloudFormation deletes the stack and then creates a new stack. If this is not set to true and the stack is in a failed state, the deployment fails. Default: false
        :param template_configuration: Input artifact to use for template parameters values and stack policy. The template configuration file should contain a JSON object that should look like this: ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information, see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_. Note that if you include sensitive information, such as passwords, restrict access to this file. Default: No template configuration based on input artifacts

        stability
        :stability: experimental
        """
        self._values = {
            'action_name': action_name,
            'admin_permissions': admin_permissions,
            'stack_name': stack_name,
            'template_path': template_path,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if variables_namespace is not None: self._values["variables_namespace"] = variables_namespace
        if role is not None: self._values["role"] = role
        if account is not None: self._values["account"] = account
        if capabilities is not None: self._values["capabilities"] = capabilities
        if deployment_role is not None: self._values["deployment_role"] = deployment_role
        if extra_inputs is not None: self._values["extra_inputs"] = extra_inputs
        if output is not None: self._values["output"] = output
        if output_file_name is not None: self._values["output_file_name"] = output_file_name
        if parameter_overrides is not None: self._values["parameter_overrides"] = parameter_overrides
        if region is not None: self._values["region"] = region
        if replace_on_failure is not None: self._values["replace_on_failure"] = replace_on_failure
        if template_configuration is not None: self._values["template_configuration"] = template_configuration

    @builtins.property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        stability
        :stability: experimental
        """
        return self._values.get('action_name')

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        stability
        :stability: experimental
        """
        return self._values.get('run_order')

    @builtins.property
    def variables_namespace(self) -> typing.Optional[str]:
        """The name of the namespace to use for variables emitted by this action.

        default
        :default:

        - a name will be generated, based on the stage and action names,
          if any of the action's variables were referenced - otherwise,
          no namespace will be set

        stability
        :stability: experimental
        """
        return self._values.get('variables_namespace')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def admin_permissions(self) -> bool:
        """Whether to grant full permissions to CloudFormation while deploying this template.

        Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you
        don't specify any alternatives.

        The default role that will be created for you will have full (i.e., ``*``)
        permissions on all resources, and the deployment will have named IAM
        capabilities (i.e., able to create all IAM resources).

        This is a shorthand that you can use if you fully trust the templates that
        are deployed in this pipeline. If you want more fine-grained permissions,
        use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation
        deployment is allowed to do.

        stability
        :stability: experimental
        """
        return self._values.get('admin_permissions')

    @builtins.property
    def stack_name(self) -> str:
        """The name of the stack to apply this action to.

        stability
        :stability: experimental
        """
        return self._values.get('stack_name')

    @builtins.property
    def template_path(self) -> _ArtifactPath_8730c13b:
        """Input artifact with the CloudFormation template to deploy.

        stability
        :stability: experimental
        """
        return self._values.get('template_path')

    @builtins.property
    def account(self) -> typing.Optional[str]:
        """The AWS account this Action is supposed to operate in.

        **Note**: if you specify the ``role`` property,
        this is ignored - the action will operate in the same region the passed role does.

        default
        :default: - action resides in the same account as the pipeline

        stability
        :stability: experimental
        """
        return self._values.get('account')

    @builtins.property
    def capabilities(self) -> typing.Optional[typing.List[_CloudFormationCapabilities_979dd343]]:
        """Acknowledge certain changes made as part of deployment.

        For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation
        might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM``
        if your stack template contains AWS Identity and Access Management (IAM) resources. For more
        information see the link below.

        default
        :default: None, unless ``adminPermissions`` is true

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
        stability
        :stability: experimental
        """
        return self._values.get('capabilities')

    @builtins.property
    def deployment_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """IAM role to assume when deploying changes.

        If not specified, a fresh role is created. The role is created with zero
        permissions unless ``adminPermissions`` is true, in which case the role will have
        full permissions.

        default
        :default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).

        stability
        :stability: experimental
        """
        return self._values.get('deployment_role')

    @builtins.property
    def extra_inputs(self) -> typing.Optional[typing.List[_Artifact_af6d98e9]]:
        """The list of additional input Artifacts for this Action.

        This is especially useful when used in conjunction with the ``parameterOverrides`` property.
        For example, if you have:

        parameterOverrides: {
        'Param1': action1.outputArtifact.bucketName,
        'Param2': action2.outputArtifact.objectKey,
        }

        , if the output Artifacts of ``action1`` and ``action2`` were not used to
        set either the ``templateConfiguration`` or the ``templatePath`` properties,
        you need to make sure to include them in the ``extraInputs`` -
        otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.

        stability
        :stability: experimental
        """
        return self._values.get('extra_inputs')

    @builtins.property
    def output(self) -> typing.Optional[_Artifact_af6d98e9]:
        """The name of the output artifact to generate.

        Only applied if ``outputFileName`` is set as well.

        default
        :default: Automatically generated artifact name.

        stability
        :stability: experimental
        """
        return self._values.get('output')

    @builtins.property
    def output_file_name(self) -> typing.Optional[str]:
        """A name for the filename in the output artifact to store the AWS CloudFormation call's result.

        The file will contain the result of the call to AWS CloudFormation (for example
        the call to UpdateStack or CreateChangeSet).

        AWS CodePipeline adds the file to the output artifact after performing
        the specified action.

        default
        :default: No output artifact generated

        stability
        :stability: experimental
        """
        return self._values.get('output_file_name')

    @builtins.property
    def parameter_overrides(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Additional template parameters.

        Template parameters specified here take precedence over template parameters
        found in the artifact specified by the ``templateConfiguration`` property.

        We recommend that you use the template configuration file to specify
        most of your parameter values. Use parameter overrides to specify only
        dynamic parameter values (values that are unknown until you run the
        pipeline).

        All parameter names must be present in the stack template.

        Note: the entire object cannot be more than 1kB.

        default
        :default: No overrides

        stability
        :stability: experimental
        """
        return self._values.get('parameter_overrides')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """The AWS region the given Action resides in.

        Note that a cross-region Pipeline requires replication buckets to function correctly.
        You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property.
        If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets,
        that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack.

        default
        :default: the Action resides in the same region as the Pipeline

        stability
        :stability: experimental
        """
        return self._values.get('region')

    @builtins.property
    def replace_on_failure(self) -> typing.Optional[bool]:
        """Replace the stack if it's in a failed state.

        If this is set to true and the stack is in a failed state (one of
        ROLLBACK_COMPLETE, ROLLBACK_FAILED, CREATE_FAILED, DELETE_FAILED, or
        UPDATE_ROLLBACK_FAILED), AWS CloudFormation deletes the stack and then
        creates a new stack.

        If this is not set to true and the stack is in a failed state,
        the deployment fails.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('replace_on_failure')

    @builtins.property
    def template_configuration(self) -> typing.Optional[_ArtifactPath_8730c13b]:
        """Input artifact to use for template parameters values and stack policy.

        The template configuration file should contain a JSON object that should look like this:
        ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information,
        see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_.

        Note that if you include sensitive information, such as passwords, restrict access to this
        file.

        default
        :default: No template configuration based on input artifacts

        stability
        :stability: experimental
        """
        return self._values.get('template_configuration')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CloudFormationCreateUpdateStackActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class CloudFormationDeleteStackAction(Action, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codepipeline_actions.CloudFormationDeleteStackAction"):
    """CodePipeline action to delete a stack.

    Deletes a stack. If you specify a stack that doesn't exist, the action completes successfully
    without deleting a stack.

    stability
    :stability: experimental
    """
    def __init__(self, *, admin_permissions: bool, stack_name: str, account: typing.Optional[str]=None, capabilities: typing.Optional[typing.List[_CloudFormationCapabilities_979dd343]]=None, deployment_role: typing.Optional[_IRole_e69bbae4]=None, extra_inputs: typing.Optional[typing.List[_Artifact_af6d98e9]]=None, output: typing.Optional[_Artifact_af6d98e9]=None, output_file_name: typing.Optional[str]=None, parameter_overrides: typing.Optional[typing.Mapping[str, typing.Any]]=None, region: typing.Optional[str]=None, template_configuration: typing.Optional[_ArtifactPath_8730c13b]=None, role: typing.Optional[_IRole_e69bbae4]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None) -> None:
        """
        :param admin_permissions: Whether to grant full permissions to CloudFormation while deploying this template. Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you don't specify any alternatives. The default role that will be created for you will have full (i.e., ``*``) permissions on all resources, and the deployment will have named IAM capabilities (i.e., able to create all IAM resources). This is a shorthand that you can use if you fully trust the templates that are deployed in this pipeline. If you want more fine-grained permissions, use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation deployment is allowed to do.
        :param stack_name: The name of the stack to apply this action to.
        :param account: The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does. Default: - action resides in the same account as the pipeline
        :param capabilities: Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM`` if your stack template contains AWS Identity and Access Management (IAM) resources. For more information see the link below. Default: None, unless ``adminPermissions`` is true
        :param deployment_role: IAM role to assume when deploying changes. If not specified, a fresh role is created. The role is created with zero permissions unless ``adminPermissions`` is true, in which case the role will have full permissions. Default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).
        :param extra_inputs: The list of additional input Artifacts for this Action. This is especially useful when used in conjunction with the ``parameterOverrides`` property. For example, if you have: parameterOverrides: { 'Param1': action1.outputArtifact.bucketName, 'Param2': action2.outputArtifact.objectKey, } , if the output Artifacts of ``action1`` and ``action2`` were not used to set either the ``templateConfiguration`` or the ``templatePath`` properties, you need to make sure to include them in the ``extraInputs`` - otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.
        :param output: The name of the output artifact to generate. Only applied if ``outputFileName`` is set as well. Default: Automatically generated artifact name.
        :param output_file_name: A name for the filename in the output artifact to store the AWS CloudFormation call's result. The file will contain the result of the call to AWS CloudFormation (for example the call to UpdateStack or CreateChangeSet). AWS CodePipeline adds the file to the output artifact after performing the specified action. Default: No output artifact generated
        :param parameter_overrides: Additional template parameters. Template parameters specified here take precedence over template parameters found in the artifact specified by the ``templateConfiguration`` property. We recommend that you use the template configuration file to specify most of your parameter values. Use parameter overrides to specify only dynamic parameter values (values that are unknown until you run the pipeline). All parameter names must be present in the stack template. Note: the entire object cannot be more than 1kB. Default: No overrides
        :param region: The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param template_configuration: Input artifact to use for template parameters values and stack policy. The template configuration file should contain a JSON object that should look like this: ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information, see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_. Note that if you include sensitive information, such as passwords, restrict access to this file. Default: No template configuration based on input artifacts
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        stability
        :stability: experimental
        """
        props = CloudFormationDeleteStackActionProps(admin_permissions=admin_permissions, stack_name=stack_name, account=account, capabilities=capabilities, deployment_role=deployment_role, extra_inputs=extra_inputs, output=output, output_file_name=output_file_name, parameter_overrides=parameter_overrides, region=region, template_configuration=template_configuration, role=role, action_name=action_name, run_order=run_order, variables_namespace=variables_namespace)

        jsii.create(CloudFormationDeleteStackAction, self, [props])

    @jsii.member(jsii_name="addToDeploymentRolePolicy")
    def add_to_deployment_role_policy(self, statement: _PolicyStatement_f75dc775) -> bool:
        """Add statement to the service role assumed by CloudFormation while executing this action.

        :param statement: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToDeploymentRolePolicy", [statement])

    @jsii.member(jsii_name="bound")
    def _bound(self, scope: _Construct_f50a3f53, stage: _IStage_b7c853a7, *, bucket: _IBucket_25bad983, role: _IRole_e69bbae4) -> _ActionConfig_c379766c:
        """The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [scope, stage, options])

    @builtins.property
    @jsii.member(jsii_name="deploymentRole")
    def deployment_role(self) -> _IRole_e69bbae4:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "deploymentRole")


@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.CloudFormationDeleteStackActionProps", jsii_struct_bases=[_CommonAwsActionProps_3b39a615], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'variables_namespace': 'variablesNamespace', 'role': 'role', 'admin_permissions': 'adminPermissions', 'stack_name': 'stackName', 'account': 'account', 'capabilities': 'capabilities', 'deployment_role': 'deploymentRole', 'extra_inputs': 'extraInputs', 'output': 'output', 'output_file_name': 'outputFileName', 'parameter_overrides': 'parameterOverrides', 'region': 'region', 'template_configuration': 'templateConfiguration'})
class CloudFormationDeleteStackActionProps(_CommonAwsActionProps_3b39a615):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None, role: typing.Optional[_IRole_e69bbae4]=None, admin_permissions: bool, stack_name: str, account: typing.Optional[str]=None, capabilities: typing.Optional[typing.List[_CloudFormationCapabilities_979dd343]]=None, deployment_role: typing.Optional[_IRole_e69bbae4]=None, extra_inputs: typing.Optional[typing.List[_Artifact_af6d98e9]]=None, output: typing.Optional[_Artifact_af6d98e9]=None, output_file_name: typing.Optional[str]=None, parameter_overrides: typing.Optional[typing.Mapping[str, typing.Any]]=None, region: typing.Optional[str]=None, template_configuration: typing.Optional[_ArtifactPath_8730c13b]=None) -> None:
        """Properties for the CloudFormationDeleteStackAction.

        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param admin_permissions: Whether to grant full permissions to CloudFormation while deploying this template. Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you don't specify any alternatives. The default role that will be created for you will have full (i.e., ``*``) permissions on all resources, and the deployment will have named IAM capabilities (i.e., able to create all IAM resources). This is a shorthand that you can use if you fully trust the templates that are deployed in this pipeline. If you want more fine-grained permissions, use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation deployment is allowed to do.
        :param stack_name: The name of the stack to apply this action to.
        :param account: The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does. Default: - action resides in the same account as the pipeline
        :param capabilities: Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM`` if your stack template contains AWS Identity and Access Management (IAM) resources. For more information see the link below. Default: None, unless ``adminPermissions`` is true
        :param deployment_role: IAM role to assume when deploying changes. If not specified, a fresh role is created. The role is created with zero permissions unless ``adminPermissions`` is true, in which case the role will have full permissions. Default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).
        :param extra_inputs: The list of additional input Artifacts for this Action. This is especially useful when used in conjunction with the ``parameterOverrides`` property. For example, if you have: parameterOverrides: { 'Param1': action1.outputArtifact.bucketName, 'Param2': action2.outputArtifact.objectKey, } , if the output Artifacts of ``action1`` and ``action2`` were not used to set either the ``templateConfiguration`` or the ``templatePath`` properties, you need to make sure to include them in the ``extraInputs`` - otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.
        :param output: The name of the output artifact to generate. Only applied if ``outputFileName`` is set as well. Default: Automatically generated artifact name.
        :param output_file_name: A name for the filename in the output artifact to store the AWS CloudFormation call's result. The file will contain the result of the call to AWS CloudFormation (for example the call to UpdateStack or CreateChangeSet). AWS CodePipeline adds the file to the output artifact after performing the specified action. Default: No output artifact generated
        :param parameter_overrides: Additional template parameters. Template parameters specified here take precedence over template parameters found in the artifact specified by the ``templateConfiguration`` property. We recommend that you use the template configuration file to specify most of your parameter values. Use parameter overrides to specify only dynamic parameter values (values that are unknown until you run the pipeline). All parameter names must be present in the stack template. Note: the entire object cannot be more than 1kB. Default: No overrides
        :param region: The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param template_configuration: Input artifact to use for template parameters values and stack policy. The template configuration file should contain a JSON object that should look like this: ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information, see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_. Note that if you include sensitive information, such as passwords, restrict access to this file. Default: No template configuration based on input artifacts

        stability
        :stability: experimental
        """
        self._values = {
            'action_name': action_name,
            'admin_permissions': admin_permissions,
            'stack_name': stack_name,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if variables_namespace is not None: self._values["variables_namespace"] = variables_namespace
        if role is not None: self._values["role"] = role
        if account is not None: self._values["account"] = account
        if capabilities is not None: self._values["capabilities"] = capabilities
        if deployment_role is not None: self._values["deployment_role"] = deployment_role
        if extra_inputs is not None: self._values["extra_inputs"] = extra_inputs
        if output is not None: self._values["output"] = output
        if output_file_name is not None: self._values["output_file_name"] = output_file_name
        if parameter_overrides is not None: self._values["parameter_overrides"] = parameter_overrides
        if region is not None: self._values["region"] = region
        if template_configuration is not None: self._values["template_configuration"] = template_configuration

    @builtins.property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        stability
        :stability: experimental
        """
        return self._values.get('action_name')

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        stability
        :stability: experimental
        """
        return self._values.get('run_order')

    @builtins.property
    def variables_namespace(self) -> typing.Optional[str]:
        """The name of the namespace to use for variables emitted by this action.

        default
        :default:

        - a name will be generated, based on the stage and action names,
          if any of the action's variables were referenced - otherwise,
          no namespace will be set

        stability
        :stability: experimental
        """
        return self._values.get('variables_namespace')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def admin_permissions(self) -> bool:
        """Whether to grant full permissions to CloudFormation while deploying this template.

        Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you
        don't specify any alternatives.

        The default role that will be created for you will have full (i.e., ``*``)
        permissions on all resources, and the deployment will have named IAM
        capabilities (i.e., able to create all IAM resources).

        This is a shorthand that you can use if you fully trust the templates that
        are deployed in this pipeline. If you want more fine-grained permissions,
        use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation
        deployment is allowed to do.

        stability
        :stability: experimental
        """
        return self._values.get('admin_permissions')

    @builtins.property
    def stack_name(self) -> str:
        """The name of the stack to apply this action to.

        stability
        :stability: experimental
        """
        return self._values.get('stack_name')

    @builtins.property
    def account(self) -> typing.Optional[str]:
        """The AWS account this Action is supposed to operate in.

        **Note**: if you specify the ``role`` property,
        this is ignored - the action will operate in the same region the passed role does.

        default
        :default: - action resides in the same account as the pipeline

        stability
        :stability: experimental
        """
        return self._values.get('account')

    @builtins.property
    def capabilities(self) -> typing.Optional[typing.List[_CloudFormationCapabilities_979dd343]]:
        """Acknowledge certain changes made as part of deployment.

        For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation
        might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM``
        if your stack template contains AWS Identity and Access Management (IAM) resources. For more
        information see the link below.

        default
        :default: None, unless ``adminPermissions`` is true

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
        stability
        :stability: experimental
        """
        return self._values.get('capabilities')

    @builtins.property
    def deployment_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """IAM role to assume when deploying changes.

        If not specified, a fresh role is created. The role is created with zero
        permissions unless ``adminPermissions`` is true, in which case the role will have
        full permissions.

        default
        :default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).

        stability
        :stability: experimental
        """
        return self._values.get('deployment_role')

    @builtins.property
    def extra_inputs(self) -> typing.Optional[typing.List[_Artifact_af6d98e9]]:
        """The list of additional input Artifacts for this Action.

        This is especially useful when used in conjunction with the ``parameterOverrides`` property.
        For example, if you have:

        parameterOverrides: {
        'Param1': action1.outputArtifact.bucketName,
        'Param2': action2.outputArtifact.objectKey,
        }

        , if the output Artifacts of ``action1`` and ``action2`` were not used to
        set either the ``templateConfiguration`` or the ``templatePath`` properties,
        you need to make sure to include them in the ``extraInputs`` -
        otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.

        stability
        :stability: experimental
        """
        return self._values.get('extra_inputs')

    @builtins.property
    def output(self) -> typing.Optional[_Artifact_af6d98e9]:
        """The name of the output artifact to generate.

        Only applied if ``outputFileName`` is set as well.

        default
        :default: Automatically generated artifact name.

        stability
        :stability: experimental
        """
        return self._values.get('output')

    @builtins.property
    def output_file_name(self) -> typing.Optional[str]:
        """A name for the filename in the output artifact to store the AWS CloudFormation call's result.

        The file will contain the result of the call to AWS CloudFormation (for example
        the call to UpdateStack or CreateChangeSet).

        AWS CodePipeline adds the file to the output artifact after performing
        the specified action.

        default
        :default: No output artifact generated

        stability
        :stability: experimental
        """
        return self._values.get('output_file_name')

    @builtins.property
    def parameter_overrides(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Additional template parameters.

        Template parameters specified here take precedence over template parameters
        found in the artifact specified by the ``templateConfiguration`` property.

        We recommend that you use the template configuration file to specify
        most of your parameter values. Use parameter overrides to specify only
        dynamic parameter values (values that are unknown until you run the
        pipeline).

        All parameter names must be present in the stack template.

        Note: the entire object cannot be more than 1kB.

        default
        :default: No overrides

        stability
        :stability: experimental
        """
        return self._values.get('parameter_overrides')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """The AWS region the given Action resides in.

        Note that a cross-region Pipeline requires replication buckets to function correctly.
        You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property.
        If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets,
        that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack.

        default
        :default: the Action resides in the same region as the Pipeline

        stability
        :stability: experimental
        """
        return self._values.get('region')

    @builtins.property
    def template_configuration(self) -> typing.Optional[_ArtifactPath_8730c13b]:
        """Input artifact to use for template parameters values and stack policy.

        The template configuration file should contain a JSON object that should look like this:
        ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information,
        see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_.

        Note that if you include sensitive information, such as passwords, restrict access to this
        file.

        default
        :default: No template configuration based on input artifacts

        stability
        :stability: experimental
        """
        return self._values.get('template_configuration')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CloudFormationDeleteStackActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class CloudFormationExecuteChangeSetAction(Action, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codepipeline_actions.CloudFormationExecuteChangeSetAction"):
    """CodePipeline action to execute a prepared change set.

    stability
    :stability: experimental
    """
    def __init__(self, *, change_set_name: str, stack_name: str, account: typing.Optional[str]=None, output: typing.Optional[_Artifact_af6d98e9]=None, output_file_name: typing.Optional[str]=None, region: typing.Optional[str]=None, role: typing.Optional[_IRole_e69bbae4]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None) -> None:
        """
        :param change_set_name: Name of the change set to execute.
        :param stack_name: The name of the stack to apply this action to.
        :param account: The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does. Default: - action resides in the same account as the pipeline
        :param output: The name of the output artifact to generate. Only applied if ``outputFileName`` is set as well. Default: Automatically generated artifact name.
        :param output_file_name: A name for the filename in the output artifact to store the AWS CloudFormation call's result. The file will contain the result of the call to AWS CloudFormation (for example the call to UpdateStack or CreateChangeSet). AWS CodePipeline adds the file to the output artifact after performing the specified action. Default: No output artifact generated
        :param region: The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        stability
        :stability: experimental
        """
        props = CloudFormationExecuteChangeSetActionProps(change_set_name=change_set_name, stack_name=stack_name, account=account, output=output, output_file_name=output_file_name, region=region, role=role, action_name=action_name, run_order=run_order, variables_namespace=variables_namespace)

        jsii.create(CloudFormationExecuteChangeSetAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, scope: _Construct_f50a3f53, stage: _IStage_b7c853a7, *, bucket: _IBucket_25bad983, role: _IRole_e69bbae4) -> _ActionConfig_c379766c:
        """The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [scope, stage, options])


@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.CloudFormationExecuteChangeSetActionProps", jsii_struct_bases=[_CommonAwsActionProps_3b39a615], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'variables_namespace': 'variablesNamespace', 'role': 'role', 'change_set_name': 'changeSetName', 'stack_name': 'stackName', 'account': 'account', 'output': 'output', 'output_file_name': 'outputFileName', 'region': 'region'})
class CloudFormationExecuteChangeSetActionProps(_CommonAwsActionProps_3b39a615):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None, role: typing.Optional[_IRole_e69bbae4]=None, change_set_name: str, stack_name: str, account: typing.Optional[str]=None, output: typing.Optional[_Artifact_af6d98e9]=None, output_file_name: typing.Optional[str]=None, region: typing.Optional[str]=None) -> None:
        """Properties for the CloudFormationExecuteChangeSetAction.

        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param change_set_name: Name of the change set to execute.
        :param stack_name: The name of the stack to apply this action to.
        :param account: The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does. Default: - action resides in the same account as the pipeline
        :param output: The name of the output artifact to generate. Only applied if ``outputFileName`` is set as well. Default: Automatically generated artifact name.
        :param output_file_name: A name for the filename in the output artifact to store the AWS CloudFormation call's result. The file will contain the result of the call to AWS CloudFormation (for example the call to UpdateStack or CreateChangeSet). AWS CodePipeline adds the file to the output artifact after performing the specified action. Default: No output artifact generated
        :param region: The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline

        stability
        :stability: experimental
        """
        self._values = {
            'action_name': action_name,
            'change_set_name': change_set_name,
            'stack_name': stack_name,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if variables_namespace is not None: self._values["variables_namespace"] = variables_namespace
        if role is not None: self._values["role"] = role
        if account is not None: self._values["account"] = account
        if output is not None: self._values["output"] = output
        if output_file_name is not None: self._values["output_file_name"] = output_file_name
        if region is not None: self._values["region"] = region

    @builtins.property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        stability
        :stability: experimental
        """
        return self._values.get('action_name')

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        stability
        :stability: experimental
        """
        return self._values.get('run_order')

    @builtins.property
    def variables_namespace(self) -> typing.Optional[str]:
        """The name of the namespace to use for variables emitted by this action.

        default
        :default:

        - a name will be generated, based on the stage and action names,
          if any of the action's variables were referenced - otherwise,
          no namespace will be set

        stability
        :stability: experimental
        """
        return self._values.get('variables_namespace')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def change_set_name(self) -> str:
        """Name of the change set to execute.

        stability
        :stability: experimental
        """
        return self._values.get('change_set_name')

    @builtins.property
    def stack_name(self) -> str:
        """The name of the stack to apply this action to.

        stability
        :stability: experimental
        """
        return self._values.get('stack_name')

    @builtins.property
    def account(self) -> typing.Optional[str]:
        """The AWS account this Action is supposed to operate in.

        **Note**: if you specify the ``role`` property,
        this is ignored - the action will operate in the same region the passed role does.

        default
        :default: - action resides in the same account as the pipeline

        stability
        :stability: experimental
        """
        return self._values.get('account')

    @builtins.property
    def output(self) -> typing.Optional[_Artifact_af6d98e9]:
        """The name of the output artifact to generate.

        Only applied if ``outputFileName`` is set as well.

        default
        :default: Automatically generated artifact name.

        stability
        :stability: experimental
        """
        return self._values.get('output')

    @builtins.property
    def output_file_name(self) -> typing.Optional[str]:
        """A name for the filename in the output artifact to store the AWS CloudFormation call's result.

        The file will contain the result of the call to AWS CloudFormation (for example
        the call to UpdateStack or CreateChangeSet).

        AWS CodePipeline adds the file to the output artifact after performing
        the specified action.

        default
        :default: No output artifact generated

        stability
        :stability: experimental
        """
        return self._values.get('output_file_name')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """The AWS region the given Action resides in.

        Note that a cross-region Pipeline requires replication buckets to function correctly.
        You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property.
        If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets,
        that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack.

        default
        :default: the Action resides in the same region as the Pipeline

        stability
        :stability: experimental
        """
        return self._values.get('region')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CloudFormationExecuteChangeSetActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class CodeBuildAction(Action, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codepipeline_actions.CodeBuildAction"):
    """CodePipeline build action that uses AWS CodeBuild.

    stability
    :stability: experimental
    """
    def __init__(self, *, input: _Artifact_af6d98e9, project: _IProject_2a66e54e, environment_variables: typing.Optional[typing.Mapping[str, _BuildEnvironmentVariable_dda665dd]]=None, extra_inputs: typing.Optional[typing.List[_Artifact_af6d98e9]]=None, outputs: typing.Optional[typing.List[_Artifact_af6d98e9]]=None, type: typing.Optional["CodeBuildActionType"]=None, role: typing.Optional[_IRole_e69bbae4]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None) -> None:
        """
        :param input: The source to use as input for this action.
        :param project: The action's Project.
        :param environment_variables: The environment variables to pass to the CodeBuild project when this action executes. If a variable with the same name was set both on the project level, and here, this value will take precedence. Default: - No additional environment variables are specified.
        :param extra_inputs: The list of additional input Artifacts for this action. The directories the additional inputs will be available at are available during the project's build in the CODEBUILD_SRC_DIR_ environment variables. The project's build always starts in the directory with the primary input artifact checked out, the one pointed to by the {@link input} property. For more information, see https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html .
        :param outputs: The list of output Artifacts for this action. **Note**: if you specify more than one output Artifact here, you cannot use the primary 'artifacts' section of the buildspec; you have to use the 'secondary-artifacts' section instead. See https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html for details. Default: the action will not have any outputs
        :param type: The type of the action that determines its CodePipeline Category - Build, or Test. Default: CodeBuildActionType.BUILD
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        stability
        :stability: experimental
        """
        props = CodeBuildActionProps(input=input, project=project, environment_variables=environment_variables, extra_inputs=extra_inputs, outputs=outputs, type=type, role=role, action_name=action_name, run_order=run_order, variables_namespace=variables_namespace)

        jsii.create(CodeBuildAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, scope: _Construct_f50a3f53, _stage: _IStage_b7c853a7, *, bucket: _IBucket_25bad983, role: _IRole_e69bbae4) -> _ActionConfig_c379766c:
        """The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param _stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [scope, _stage, options])

    @jsii.member(jsii_name="variable")
    def variable(self, variable_name: str) -> str:
        """Reference a CodePipeline variable defined by the CodeBuild project this action points to.

        Variables in CodeBuild actions are defined using the 'exported-variables' subsection of the 'env'
        section of the buildspec.

        :param variable_name: the name of the variable to reference. A variable by this name must be present in the 'exported-variables' section of the buildspec

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec-ref-syntax
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "variable", [variable_name])


@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.CodeBuildActionProps", jsii_struct_bases=[_CommonAwsActionProps_3b39a615], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'variables_namespace': 'variablesNamespace', 'role': 'role', 'input': 'input', 'project': 'project', 'environment_variables': 'environmentVariables', 'extra_inputs': 'extraInputs', 'outputs': 'outputs', 'type': 'type'})
class CodeBuildActionProps(_CommonAwsActionProps_3b39a615):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None, role: typing.Optional[_IRole_e69bbae4]=None, input: _Artifact_af6d98e9, project: _IProject_2a66e54e, environment_variables: typing.Optional[typing.Mapping[str, _BuildEnvironmentVariable_dda665dd]]=None, extra_inputs: typing.Optional[typing.List[_Artifact_af6d98e9]]=None, outputs: typing.Optional[typing.List[_Artifact_af6d98e9]]=None, type: typing.Optional["CodeBuildActionType"]=None) -> None:
        """Construction properties of the {@link CodeBuildAction CodeBuild build CodePipeline action}.

        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param input: The source to use as input for this action.
        :param project: The action's Project.
        :param environment_variables: The environment variables to pass to the CodeBuild project when this action executes. If a variable with the same name was set both on the project level, and here, this value will take precedence. Default: - No additional environment variables are specified.
        :param extra_inputs: The list of additional input Artifacts for this action. The directories the additional inputs will be available at are available during the project's build in the CODEBUILD_SRC_DIR_ environment variables. The project's build always starts in the directory with the primary input artifact checked out, the one pointed to by the {@link input} property. For more information, see https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html .
        :param outputs: The list of output Artifacts for this action. **Note**: if you specify more than one output Artifact here, you cannot use the primary 'artifacts' section of the buildspec; you have to use the 'secondary-artifacts' section instead. See https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html for details. Default: the action will not have any outputs
        :param type: The type of the action that determines its CodePipeline Category - Build, or Test. Default: CodeBuildActionType.BUILD

        stability
        :stability: experimental
        """
        self._values = {
            'action_name': action_name,
            'input': input,
            'project': project,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if variables_namespace is not None: self._values["variables_namespace"] = variables_namespace
        if role is not None: self._values["role"] = role
        if environment_variables is not None: self._values["environment_variables"] = environment_variables
        if extra_inputs is not None: self._values["extra_inputs"] = extra_inputs
        if outputs is not None: self._values["outputs"] = outputs
        if type is not None: self._values["type"] = type

    @builtins.property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        stability
        :stability: experimental
        """
        return self._values.get('action_name')

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        stability
        :stability: experimental
        """
        return self._values.get('run_order')

    @builtins.property
    def variables_namespace(self) -> typing.Optional[str]:
        """The name of the namespace to use for variables emitted by this action.

        default
        :default:

        - a name will be generated, based on the stage and action names,
          if any of the action's variables were referenced - otherwise,
          no namespace will be set

        stability
        :stability: experimental
        """
        return self._values.get('variables_namespace')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def input(self) -> _Artifact_af6d98e9:
        """The source to use as input for this action.

        stability
        :stability: experimental
        """
        return self._values.get('input')

    @builtins.property
    def project(self) -> _IProject_2a66e54e:
        """The action's Project.

        stability
        :stability: experimental
        """
        return self._values.get('project')

    @builtins.property
    def environment_variables(self) -> typing.Optional[typing.Mapping[str, _BuildEnvironmentVariable_dda665dd]]:
        """The environment variables to pass to the CodeBuild project when this action executes.

        If a variable with the same name was set both on the project level, and here,
        this value will take precedence.

        default
        :default: - No additional environment variables are specified.

        stability
        :stability: experimental
        """
        return self._values.get('environment_variables')

    @builtins.property
    def extra_inputs(self) -> typing.Optional[typing.List[_Artifact_af6d98e9]]:
        """The list of additional input Artifacts for this action.

        The directories the additional inputs will be available at are available
        during the project's build in the CODEBUILD_SRC_DIR_ environment variables.
        The project's build always starts in the directory with the primary input artifact checked out,
        the one pointed to by the {@link input} property.
        For more information,
        see https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html .

        stability
        :stability: experimental
        """
        return self._values.get('extra_inputs')

    @builtins.property
    def outputs(self) -> typing.Optional[typing.List[_Artifact_af6d98e9]]:
        """The list of output Artifacts for this action.

        **Note**: if you specify more than one output Artifact here,
        you cannot use the primary 'artifacts' section of the buildspec;
        you have to use the 'secondary-artifacts' section instead.
        See https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html
        for details.

        default
        :default: the action will not have any outputs

        stability
        :stability: experimental
        """
        return self._values.get('outputs')

    @builtins.property
    def type(self) -> typing.Optional["CodeBuildActionType"]:
        """The type of the action that determines its CodePipeline Category - Build, or Test.

        default
        :default: CodeBuildActionType.BUILD

        stability
        :stability: experimental
        """
        return self._values.get('type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CodeBuildActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_codepipeline_actions.CodeBuildActionType")
class CodeBuildActionType(enum.Enum):
    """The type of the CodeBuild action that determines its CodePipeline Category - Build, or Test.

    The default is Build.

    stability
    :stability: experimental
    """
    BUILD = "BUILD"
    """The action will have the Build Category.

    This is the default.

    stability
    :stability: experimental
    """
    TEST = "TEST"
    """The action will have the Test Category.

    stability
    :stability: experimental
    """

class CodeCommitSourceAction(Action, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codepipeline_actions.CodeCommitSourceAction"):
    """CodePipeline Source that is provided by an AWS CodeCommit repository.

    stability
    :stability: experimental
    """
    def __init__(self, *, output: _Artifact_af6d98e9, repository: _IRepository_91f381de, branch: typing.Optional[str]=None, trigger: typing.Optional["CodeCommitTrigger"]=None, role: typing.Optional[_IRole_e69bbae4]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None) -> None:
        """
        :param output: 
        :param repository: The CodeCommit repository.
        :param branch: Default: 'master'
        :param trigger: How should CodePipeline detect source changes for this Action. Default: CodeCommitTrigger.EVENTS
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        stability
        :stability: experimental
        """
        props = CodeCommitSourceActionProps(output=output, repository=repository, branch=branch, trigger=trigger, role=role, action_name=action_name, run_order=run_order, variables_namespace=variables_namespace)

        jsii.create(CodeCommitSourceAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, _scope: _Construct_f50a3f53, stage: _IStage_b7c853a7, *, bucket: _IBucket_25bad983, role: _IRole_e69bbae4) -> _ActionConfig_c379766c:
        """The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [_scope, stage, options])

    @builtins.property
    @jsii.member(jsii_name="variables")
    def variables(self) -> "CodeCommitSourceVariables":
        """The variables emitted by this action.

        stability
        :stability: experimental
        """
        return jsii.get(self, "variables")


@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.CodeCommitSourceActionProps", jsii_struct_bases=[_CommonAwsActionProps_3b39a615], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'variables_namespace': 'variablesNamespace', 'role': 'role', 'output': 'output', 'repository': 'repository', 'branch': 'branch', 'trigger': 'trigger'})
class CodeCommitSourceActionProps(_CommonAwsActionProps_3b39a615):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None, role: typing.Optional[_IRole_e69bbae4]=None, output: _Artifact_af6d98e9, repository: _IRepository_91f381de, branch: typing.Optional[str]=None, trigger: typing.Optional["CodeCommitTrigger"]=None) -> None:
        """Construction properties of the {@link CodeCommitSourceAction CodeCommit source CodePipeline Action}.

        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param output: 
        :param repository: The CodeCommit repository.
        :param branch: Default: 'master'
        :param trigger: How should CodePipeline detect source changes for this Action. Default: CodeCommitTrigger.EVENTS

        stability
        :stability: experimental
        """
        self._values = {
            'action_name': action_name,
            'output': output,
            'repository': repository,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if variables_namespace is not None: self._values["variables_namespace"] = variables_namespace
        if role is not None: self._values["role"] = role
        if branch is not None: self._values["branch"] = branch
        if trigger is not None: self._values["trigger"] = trigger

    @builtins.property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        stability
        :stability: experimental
        """
        return self._values.get('action_name')

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        stability
        :stability: experimental
        """
        return self._values.get('run_order')

    @builtins.property
    def variables_namespace(self) -> typing.Optional[str]:
        """The name of the namespace to use for variables emitted by this action.

        default
        :default:

        - a name will be generated, based on the stage and action names,
          if any of the action's variables were referenced - otherwise,
          no namespace will be set

        stability
        :stability: experimental
        """
        return self._values.get('variables_namespace')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def output(self) -> _Artifact_af6d98e9:
        """
        stability
        :stability: experimental
        """
        return self._values.get('output')

    @builtins.property
    def repository(self) -> _IRepository_91f381de:
        """The CodeCommit repository.

        stability
        :stability: experimental
        """
        return self._values.get('repository')

    @builtins.property
    def branch(self) -> typing.Optional[str]:
        """
        default
        :default: 'master'

        stability
        :stability: experimental
        """
        return self._values.get('branch')

    @builtins.property
    def trigger(self) -> typing.Optional["CodeCommitTrigger"]:
        """How should CodePipeline detect source changes for this Action.

        default
        :default: CodeCommitTrigger.EVENTS

        stability
        :stability: experimental
        """
        return self._values.get('trigger')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CodeCommitSourceActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.CodeCommitSourceVariables", jsii_struct_bases=[], name_mapping={'author_date': 'authorDate', 'branch_name': 'branchName', 'commit_id': 'commitId', 'commit_message': 'commitMessage', 'committer_date': 'committerDate', 'repository_name': 'repositoryName'})
class CodeCommitSourceVariables():
    def __init__(self, *, author_date: str, branch_name: str, commit_id: str, commit_message: str, committer_date: str, repository_name: str) -> None:
        """The CodePipeline variables emitted by the CodeCommit source Action.

        :param author_date: The date the currently last commit on the tracked branch was authored, in ISO-8601 format.
        :param branch_name: The name of the branch this action tracks.
        :param commit_id: The SHA1 hash of the currently last commit on the tracked branch.
        :param commit_message: The message of the currently last commit on the tracked branch.
        :param committer_date: The date the currently last commit on the tracked branch was committed, in ISO-8601 format.
        :param repository_name: The name of the repository this action points to.

        stability
        :stability: experimental
        """
        self._values = {
            'author_date': author_date,
            'branch_name': branch_name,
            'commit_id': commit_id,
            'commit_message': commit_message,
            'committer_date': committer_date,
            'repository_name': repository_name,
        }

    @builtins.property
    def author_date(self) -> str:
        """The date the currently last commit on the tracked branch was authored, in ISO-8601 format.

        stability
        :stability: experimental
        """
        return self._values.get('author_date')

    @builtins.property
    def branch_name(self) -> str:
        """The name of the branch this action tracks.

        stability
        :stability: experimental
        """
        return self._values.get('branch_name')

    @builtins.property
    def commit_id(self) -> str:
        """The SHA1 hash of the currently last commit on the tracked branch.

        stability
        :stability: experimental
        """
        return self._values.get('commit_id')

    @builtins.property
    def commit_message(self) -> str:
        """The message of the currently last commit on the tracked branch.

        stability
        :stability: experimental
        """
        return self._values.get('commit_message')

    @builtins.property
    def committer_date(self) -> str:
        """The date the currently last commit on the tracked branch was committed, in ISO-8601 format.

        stability
        :stability: experimental
        """
        return self._values.get('committer_date')

    @builtins.property
    def repository_name(self) -> str:
        """The name of the repository this action points to.

        stability
        :stability: experimental
        """
        return self._values.get('repository_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CodeCommitSourceVariables(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_codepipeline_actions.CodeCommitTrigger")
class CodeCommitTrigger(enum.Enum):
    """How should the CodeCommit Action detect changes.

    This is the type of the {@link CodeCommitSourceAction.trigger} property.

    stability
    :stability: experimental
    """
    NONE = "NONE"
    """The Action will never detect changes - the Pipeline it's part of will only begin a run when explicitly started.

    stability
    :stability: experimental
    """
    POLL = "POLL"
    """CodePipeline will poll the repository to detect changes.

    stability
    :stability: experimental
    """
    EVENTS = "EVENTS"
    """CodePipeline will use CloudWatch Events to be notified of changes.

    This is the default method of detecting changes.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.CodeDeployEcsContainerImageInput", jsii_struct_bases=[], name_mapping={'input': 'input', 'task_definition_placeholder': 'taskDefinitionPlaceholder'})
class CodeDeployEcsContainerImageInput():
    def __init__(self, *, input: _Artifact_af6d98e9, task_definition_placeholder: typing.Optional[str]=None) -> None:
        """Configuration for replacing a placeholder string in the ECS task definition template file with an image URI.

        :param input: The artifact that contains an ``imageDetails.json`` file with the image URI. The artifact's ``imageDetails.json`` file must be a JSON file containing an ``ImageURI`` property. For example: ``{ "ImageURI": "ACCOUNTID.dkr.ecr.us-west-2.amazonaws.com/dk-image-repo@sha256:example3" }``
        :param task_definition_placeholder: The placeholder string in the ECS task definition template file that will be replaced with the image URI. The placeholder string must be surrounded by angle brackets in the template file. For example, if the task definition template file contains a placeholder like ``"image": "<PLACEHOLDER>"``, then the ``taskDefinitionPlaceholder`` value should be ``PLACEHOLDER``. Default: IMAGE

        stability
        :stability: experimental
        """
        self._values = {
            'input': input,
        }
        if task_definition_placeholder is not None: self._values["task_definition_placeholder"] = task_definition_placeholder

    @builtins.property
    def input(self) -> _Artifact_af6d98e9:
        """The artifact that contains an ``imageDetails.json`` file with the image URI.

        The artifact's ``imageDetails.json`` file must be a JSON file containing an
        ``ImageURI`` property.  For example:
        ``{ "ImageURI": "ACCOUNTID.dkr.ecr.us-west-2.amazonaws.com/dk-image-repo@sha256:example3" }``

        stability
        :stability: experimental
        """
        return self._values.get('input')

    @builtins.property
    def task_definition_placeholder(self) -> typing.Optional[str]:
        """The placeholder string in the ECS task definition template file that will be replaced with the image URI.

        The placeholder string must be surrounded by angle brackets in the template file.
        For example, if the task definition template file contains a placeholder like
        ``"image": "<PLACEHOLDER>"``, then the ``taskDefinitionPlaceholder`` value should
        be ``PLACEHOLDER``.

        default
        :default: IMAGE

        stability
        :stability: experimental
        """
        return self._values.get('task_definition_placeholder')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CodeDeployEcsContainerImageInput(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class CodeDeployEcsDeployAction(Action, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codepipeline_actions.CodeDeployEcsDeployAction"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, *, deployment_group: _IEcsDeploymentGroup_458435fe, app_spec_template_file: typing.Optional[_ArtifactPath_8730c13b]=None, app_spec_template_input: typing.Optional[_Artifact_af6d98e9]=None, container_image_inputs: typing.Optional[typing.List["CodeDeployEcsContainerImageInput"]]=None, task_definition_template_file: typing.Optional[_ArtifactPath_8730c13b]=None, task_definition_template_input: typing.Optional[_Artifact_af6d98e9]=None, role: typing.Optional[_IRole_e69bbae4]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None) -> None:
        """
        :param deployment_group: The CodeDeploy ECS Deployment Group to deploy to.
        :param app_spec_template_file: The name of the CodeDeploy AppSpec file. During deployment, a new task definition will be registered with ECS, and the new task definition ID will be inserted into the CodeDeploy AppSpec file. The AppSpec file contents will be provided to CodeDeploy for the deployment. Use this property if you want to use a different name for this file than the default 'appspec.yaml'. If you use this property, you don't need to specify the ``appSpecTemplateInput`` property. Default: - one of this property, or ``appSpecTemplateInput``, is required
        :param app_spec_template_input: The artifact containing the CodeDeploy AppSpec file. During deployment, a new task definition will be registered with ECS, and the new task definition ID will be inserted into the CodeDeploy AppSpec file. The AppSpec file contents will be provided to CodeDeploy for the deployment. If you use this property, it's assumed the file is called 'appspec.yaml'. If your AppSpec file uses a different filename, leave this property empty, and use the ``appSpecTemplateFile`` property instead. Default: - one of this property, or ``appSpecTemplateFile``, is required
        :param container_image_inputs: Configuration for dynamically updated images in the task definition. Provide pairs of an image details input artifact and a placeholder string that will be used to dynamically update the ECS task definition template file prior to deployment. A maximum of 4 images can be given.
        :param task_definition_template_file: The name of the ECS task definition template file. During deployment, the task definition template file contents will be registered with ECS. Use this property if you want to use a different name for this file than the default 'taskdef.json'. If you use this property, you don't need to specify the ``taskDefinitionTemplateInput`` property. Default: - one of this property, or ``taskDefinitionTemplateInput``, is required
        :param task_definition_template_input: The artifact containing the ECS task definition template file. During deployment, the task definition template file contents will be registered with ECS. If you use this property, it's assumed the file is called 'taskdef.json'. If your task definition template uses a different filename, leave this property empty, and use the ``taskDefinitionTemplateFile`` property instead. Default: - one of this property, or ``taskDefinitionTemplateFile``, is required
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        stability
        :stability: experimental
        """
        props = CodeDeployEcsDeployActionProps(deployment_group=deployment_group, app_spec_template_file=app_spec_template_file, app_spec_template_input=app_spec_template_input, container_image_inputs=container_image_inputs, task_definition_template_file=task_definition_template_file, task_definition_template_input=task_definition_template_input, role=role, action_name=action_name, run_order=run_order, variables_namespace=variables_namespace)

        jsii.create(CodeDeployEcsDeployAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, _scope: _Construct_f50a3f53, _stage: _IStage_b7c853a7, *, bucket: _IBucket_25bad983, role: _IRole_e69bbae4) -> _ActionConfig_c379766c:
        """The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param _stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [_scope, _stage, options])


@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.CodeDeployEcsDeployActionProps", jsii_struct_bases=[_CommonAwsActionProps_3b39a615], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'variables_namespace': 'variablesNamespace', 'role': 'role', 'deployment_group': 'deploymentGroup', 'app_spec_template_file': 'appSpecTemplateFile', 'app_spec_template_input': 'appSpecTemplateInput', 'container_image_inputs': 'containerImageInputs', 'task_definition_template_file': 'taskDefinitionTemplateFile', 'task_definition_template_input': 'taskDefinitionTemplateInput'})
class CodeDeployEcsDeployActionProps(_CommonAwsActionProps_3b39a615):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None, role: typing.Optional[_IRole_e69bbae4]=None, deployment_group: _IEcsDeploymentGroup_458435fe, app_spec_template_file: typing.Optional[_ArtifactPath_8730c13b]=None, app_spec_template_input: typing.Optional[_Artifact_af6d98e9]=None, container_image_inputs: typing.Optional[typing.List["CodeDeployEcsContainerImageInput"]]=None, task_definition_template_file: typing.Optional[_ArtifactPath_8730c13b]=None, task_definition_template_input: typing.Optional[_Artifact_af6d98e9]=None) -> None:
        """Construction properties of the {@link CodeDeployEcsDeployAction CodeDeploy ECS deploy CodePipeline Action}.

        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param deployment_group: The CodeDeploy ECS Deployment Group to deploy to.
        :param app_spec_template_file: The name of the CodeDeploy AppSpec file. During deployment, a new task definition will be registered with ECS, and the new task definition ID will be inserted into the CodeDeploy AppSpec file. The AppSpec file contents will be provided to CodeDeploy for the deployment. Use this property if you want to use a different name for this file than the default 'appspec.yaml'. If you use this property, you don't need to specify the ``appSpecTemplateInput`` property. Default: - one of this property, or ``appSpecTemplateInput``, is required
        :param app_spec_template_input: The artifact containing the CodeDeploy AppSpec file. During deployment, a new task definition will be registered with ECS, and the new task definition ID will be inserted into the CodeDeploy AppSpec file. The AppSpec file contents will be provided to CodeDeploy for the deployment. If you use this property, it's assumed the file is called 'appspec.yaml'. If your AppSpec file uses a different filename, leave this property empty, and use the ``appSpecTemplateFile`` property instead. Default: - one of this property, or ``appSpecTemplateFile``, is required
        :param container_image_inputs: Configuration for dynamically updated images in the task definition. Provide pairs of an image details input artifact and a placeholder string that will be used to dynamically update the ECS task definition template file prior to deployment. A maximum of 4 images can be given.
        :param task_definition_template_file: The name of the ECS task definition template file. During deployment, the task definition template file contents will be registered with ECS. Use this property if you want to use a different name for this file than the default 'taskdef.json'. If you use this property, you don't need to specify the ``taskDefinitionTemplateInput`` property. Default: - one of this property, or ``taskDefinitionTemplateInput``, is required
        :param task_definition_template_input: The artifact containing the ECS task definition template file. During deployment, the task definition template file contents will be registered with ECS. If you use this property, it's assumed the file is called 'taskdef.json'. If your task definition template uses a different filename, leave this property empty, and use the ``taskDefinitionTemplateFile`` property instead. Default: - one of this property, or ``taskDefinitionTemplateFile``, is required

        stability
        :stability: experimental
        """
        self._values = {
            'action_name': action_name,
            'deployment_group': deployment_group,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if variables_namespace is not None: self._values["variables_namespace"] = variables_namespace
        if role is not None: self._values["role"] = role
        if app_spec_template_file is not None: self._values["app_spec_template_file"] = app_spec_template_file
        if app_spec_template_input is not None: self._values["app_spec_template_input"] = app_spec_template_input
        if container_image_inputs is not None: self._values["container_image_inputs"] = container_image_inputs
        if task_definition_template_file is not None: self._values["task_definition_template_file"] = task_definition_template_file
        if task_definition_template_input is not None: self._values["task_definition_template_input"] = task_definition_template_input

    @builtins.property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        stability
        :stability: experimental
        """
        return self._values.get('action_name')

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        stability
        :stability: experimental
        """
        return self._values.get('run_order')

    @builtins.property
    def variables_namespace(self) -> typing.Optional[str]:
        """The name of the namespace to use for variables emitted by this action.

        default
        :default:

        - a name will be generated, based on the stage and action names,
          if any of the action's variables were referenced - otherwise,
          no namespace will be set

        stability
        :stability: experimental
        """
        return self._values.get('variables_namespace')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def deployment_group(self) -> _IEcsDeploymentGroup_458435fe:
        """The CodeDeploy ECS Deployment Group to deploy to.

        stability
        :stability: experimental
        """
        return self._values.get('deployment_group')

    @builtins.property
    def app_spec_template_file(self) -> typing.Optional[_ArtifactPath_8730c13b]:
        """The name of the CodeDeploy AppSpec file.

        During deployment, a new task definition will be registered
        with ECS, and the new task definition ID will be inserted into
        the CodeDeploy AppSpec file.  The AppSpec file contents will be
        provided to CodeDeploy for the deployment.

        Use this property if you want to use a different name for this file than the default 'appspec.yaml'.
        If you use this property, you don't need to specify the ``appSpecTemplateInput`` property.

        default
        :default: - one of this property, or ``appSpecTemplateInput``, is required

        stability
        :stability: experimental
        """
        return self._values.get('app_spec_template_file')

    @builtins.property
    def app_spec_template_input(self) -> typing.Optional[_Artifact_af6d98e9]:
        """The artifact containing the CodeDeploy AppSpec file.

        During deployment, a new task definition will be registered
        with ECS, and the new task definition ID will be inserted into
        the CodeDeploy AppSpec file.  The AppSpec file contents will be
        provided to CodeDeploy for the deployment.

        If you use this property, it's assumed the file is called 'appspec.yaml'.
        If your AppSpec file uses a different filename, leave this property empty,
        and use the ``appSpecTemplateFile`` property instead.

        default
        :default: - one of this property, or ``appSpecTemplateFile``, is required

        stability
        :stability: experimental
        """
        return self._values.get('app_spec_template_input')

    @builtins.property
    def container_image_inputs(self) -> typing.Optional[typing.List["CodeDeployEcsContainerImageInput"]]:
        """Configuration for dynamically updated images in the task definition.

        Provide pairs of an image details input artifact and a placeholder string
        that will be used to dynamically update the ECS task definition template
        file prior to deployment. A maximum of 4 images can be given.

        stability
        :stability: experimental
        """
        return self._values.get('container_image_inputs')

    @builtins.property
    def task_definition_template_file(self) -> typing.Optional[_ArtifactPath_8730c13b]:
        """The name of the ECS task definition template file.

        During deployment, the task definition template file contents
        will be registered with ECS.

        Use this property if you want to use a different name for this file than the default 'taskdef.json'.
        If you use this property, you don't need to specify the ``taskDefinitionTemplateInput`` property.

        default
        :default: - one of this property, or ``taskDefinitionTemplateInput``, is required

        stability
        :stability: experimental
        """
        return self._values.get('task_definition_template_file')

    @builtins.property
    def task_definition_template_input(self) -> typing.Optional[_Artifact_af6d98e9]:
        """The artifact containing the ECS task definition template file.

        During deployment, the task definition template file contents
        will be registered with ECS.

        If you use this property, it's assumed the file is called 'taskdef.json'.
        If your task definition template uses a different filename, leave this property empty,
        and use the ``taskDefinitionTemplateFile`` property instead.

        default
        :default: - one of this property, or ``taskDefinitionTemplateFile``, is required

        stability
        :stability: experimental
        """
        return self._values.get('task_definition_template_input')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CodeDeployEcsDeployActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class CodeDeployServerDeployAction(Action, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codepipeline_actions.CodeDeployServerDeployAction"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, *, deployment_group: _IServerDeploymentGroup_b0b16347, input: _Artifact_af6d98e9, role: typing.Optional[_IRole_e69bbae4]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None) -> None:
        """
        :param deployment_group: The CodeDeploy server Deployment Group to deploy to.
        :param input: The source to use as input for deployment.
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        stability
        :stability: experimental
        """
        props = CodeDeployServerDeployActionProps(deployment_group=deployment_group, input=input, role=role, action_name=action_name, run_order=run_order, variables_namespace=variables_namespace)

        jsii.create(CodeDeployServerDeployAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, _scope: _Construct_f50a3f53, _stage: _IStage_b7c853a7, *, bucket: _IBucket_25bad983, role: _IRole_e69bbae4) -> _ActionConfig_c379766c:
        """The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param _stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [_scope, _stage, options])


@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.CodeDeployServerDeployActionProps", jsii_struct_bases=[_CommonAwsActionProps_3b39a615], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'variables_namespace': 'variablesNamespace', 'role': 'role', 'deployment_group': 'deploymentGroup', 'input': 'input'})
class CodeDeployServerDeployActionProps(_CommonAwsActionProps_3b39a615):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None, role: typing.Optional[_IRole_e69bbae4]=None, deployment_group: _IServerDeploymentGroup_b0b16347, input: _Artifact_af6d98e9) -> None:
        """Construction properties of the {@link CodeDeployServerDeployAction CodeDeploy server deploy CodePipeline Action}.

        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param deployment_group: The CodeDeploy server Deployment Group to deploy to.
        :param input: The source to use as input for deployment.

        stability
        :stability: experimental
        """
        self._values = {
            'action_name': action_name,
            'deployment_group': deployment_group,
            'input': input,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if variables_namespace is not None: self._values["variables_namespace"] = variables_namespace
        if role is not None: self._values["role"] = role

    @builtins.property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        stability
        :stability: experimental
        """
        return self._values.get('action_name')

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        stability
        :stability: experimental
        """
        return self._values.get('run_order')

    @builtins.property
    def variables_namespace(self) -> typing.Optional[str]:
        """The name of the namespace to use for variables emitted by this action.

        default
        :default:

        - a name will be generated, based on the stage and action names,
          if any of the action's variables were referenced - otherwise,
          no namespace will be set

        stability
        :stability: experimental
        """
        return self._values.get('variables_namespace')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def deployment_group(self) -> _IServerDeploymentGroup_b0b16347:
        """The CodeDeploy server Deployment Group to deploy to.

        stability
        :stability: experimental
        """
        return self._values.get('deployment_group')

    @builtins.property
    def input(self) -> _Artifact_af6d98e9:
        """The source to use as input for deployment.

        stability
        :stability: experimental
        """
        return self._values.get('input')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CodeDeployServerDeployActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class EcrSourceAction(Action, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codepipeline_actions.EcrSourceAction"):
    """The ECR Repository source CodePipeline Action.

    Will trigger the pipeline as soon as the target tag in the repository
    changes, but only if there is a CloudTrail Trail in the account that
    captures the ECR event.

    stability
    :stability: experimental
    """
    def __init__(self, *, output: _Artifact_af6d98e9, repository: _IRepository_aa6e452c, image_tag: typing.Optional[str]=None, role: typing.Optional[_IRole_e69bbae4]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None) -> None:
        """
        :param output: 
        :param repository: The repository that will be watched for changes.
        :param image_tag: The image tag that will be checked for changes. Default: 'latest'
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        stability
        :stability: experimental
        """
        props = EcrSourceActionProps(output=output, repository=repository, image_tag=image_tag, role=role, action_name=action_name, run_order=run_order, variables_namespace=variables_namespace)

        jsii.create(EcrSourceAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, _scope: _Construct_f50a3f53, stage: _IStage_b7c853a7, *, bucket: _IBucket_25bad983, role: _IRole_e69bbae4) -> _ActionConfig_c379766c:
        """The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [_scope, stage, options])

    @builtins.property
    @jsii.member(jsii_name="variables")
    def variables(self) -> "EcrSourceVariables":
        """The variables emitted by this action.

        stability
        :stability: experimental
        """
        return jsii.get(self, "variables")


@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.EcrSourceActionProps", jsii_struct_bases=[_CommonAwsActionProps_3b39a615], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'variables_namespace': 'variablesNamespace', 'role': 'role', 'output': 'output', 'repository': 'repository', 'image_tag': 'imageTag'})
class EcrSourceActionProps(_CommonAwsActionProps_3b39a615):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None, role: typing.Optional[_IRole_e69bbae4]=None, output: _Artifact_af6d98e9, repository: _IRepository_aa6e452c, image_tag: typing.Optional[str]=None) -> None:
        """Construction properties of {@link EcrSourceAction}.

        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param output: 
        :param repository: The repository that will be watched for changes.
        :param image_tag: The image tag that will be checked for changes. Default: 'latest'

        stability
        :stability: experimental
        """
        self._values = {
            'action_name': action_name,
            'output': output,
            'repository': repository,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if variables_namespace is not None: self._values["variables_namespace"] = variables_namespace
        if role is not None: self._values["role"] = role
        if image_tag is not None: self._values["image_tag"] = image_tag

    @builtins.property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        stability
        :stability: experimental
        """
        return self._values.get('action_name')

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        stability
        :stability: experimental
        """
        return self._values.get('run_order')

    @builtins.property
    def variables_namespace(self) -> typing.Optional[str]:
        """The name of the namespace to use for variables emitted by this action.

        default
        :default:

        - a name will be generated, based on the stage and action names,
          if any of the action's variables were referenced - otherwise,
          no namespace will be set

        stability
        :stability: experimental
        """
        return self._values.get('variables_namespace')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def output(self) -> _Artifact_af6d98e9:
        """
        stability
        :stability: experimental
        """
        return self._values.get('output')

    @builtins.property
    def repository(self) -> _IRepository_aa6e452c:
        """The repository that will be watched for changes.

        stability
        :stability: experimental
        """
        return self._values.get('repository')

    @builtins.property
    def image_tag(self) -> typing.Optional[str]:
        """The image tag that will be checked for changes.

        default
        :default: 'latest'

        stability
        :stability: experimental
        """
        return self._values.get('image_tag')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EcrSourceActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.EcrSourceVariables", jsii_struct_bases=[], name_mapping={'image_digest': 'imageDigest', 'image_tag': 'imageTag', 'image_uri': 'imageUri', 'registry_id': 'registryId', 'repository_name': 'repositoryName'})
class EcrSourceVariables():
    def __init__(self, *, image_digest: str, image_tag: str, image_uri: str, registry_id: str, repository_name: str) -> None:
        """The CodePipeline variables emitted by the ECR source Action.

        :param image_digest: The digest of the current image, in the form ':'.
        :param image_tag: The Docker tag of the current image.
        :param image_uri: The full ECR Docker URI of the current image.
        :param registry_id: The identifier of the registry. In ECR, this is usually the ID of the AWS account owning it.
        :param repository_name: The physical name of the repository that this action tracks.

        stability
        :stability: experimental
        """
        self._values = {
            'image_digest': image_digest,
            'image_tag': image_tag,
            'image_uri': image_uri,
            'registry_id': registry_id,
            'repository_name': repository_name,
        }

    @builtins.property
    def image_digest(self) -> str:
        """The digest of the current image, in the form ':'.

        stability
        :stability: experimental
        """
        return self._values.get('image_digest')

    @builtins.property
    def image_tag(self) -> str:
        """The Docker tag of the current image.

        stability
        :stability: experimental
        """
        return self._values.get('image_tag')

    @builtins.property
    def image_uri(self) -> str:
        """The full ECR Docker URI of the current image.

        stability
        :stability: experimental
        """
        return self._values.get('image_uri')

    @builtins.property
    def registry_id(self) -> str:
        """The identifier of the registry.

        In ECR, this is usually the ID of the AWS account owning it.

        stability
        :stability: experimental
        """
        return self._values.get('registry_id')

    @builtins.property
    def repository_name(self) -> str:
        """The physical name of the repository that this action tracks.

        stability
        :stability: experimental
        """
        return self._values.get('repository_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EcrSourceVariables(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class EcsDeployAction(Action, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codepipeline_actions.EcsDeployAction"):
    """CodePipeline Action to deploy an ECS Service.

    stability
    :stability: experimental
    """
    def __init__(self, *, service: _IBaseService_de6ed13e, image_file: typing.Optional[_ArtifactPath_8730c13b]=None, input: typing.Optional[_Artifact_af6d98e9]=None, role: typing.Optional[_IRole_e69bbae4]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None) -> None:
        """
        :param service: The ECS Service to deploy.
        :param image_file: The name of the JSON image definitions file to use for deployments. The JSON file is a list of objects, each with 2 keys: ``name`` is the name of the container in the Task Definition, and ``imageUri`` is the Docker image URI you want to update your service with. Use this property if you want to use a different name for this file than the default 'imagedefinitions.json'. If you use this property, you don't need to specify the ``input`` property. Default: - one of this property, or ``input``, is required
        :param input: The input artifact that contains the JSON image definitions file to use for deployments. The JSON file is a list of objects, each with 2 keys: ``name`` is the name of the container in the Task Definition, and ``imageUri`` is the Docker image URI you want to update your service with. If you use this property, it's assumed the file is called 'imagedefinitions.json'. If your build uses a different file, leave this property empty, and use the ``imageFile`` property instead. Default: - one of this property, or ``imageFile``, is required
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        stability
        :stability: experimental
        """
        props = EcsDeployActionProps(service=service, image_file=image_file, input=input, role=role, action_name=action_name, run_order=run_order, variables_namespace=variables_namespace)

        jsii.create(EcsDeployAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, _scope: _Construct_f50a3f53, _stage: _IStage_b7c853a7, *, bucket: _IBucket_25bad983, role: _IRole_e69bbae4) -> _ActionConfig_c379766c:
        """The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param _stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [_scope, _stage, options])


@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.EcsDeployActionProps", jsii_struct_bases=[_CommonAwsActionProps_3b39a615], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'variables_namespace': 'variablesNamespace', 'role': 'role', 'service': 'service', 'image_file': 'imageFile', 'input': 'input'})
class EcsDeployActionProps(_CommonAwsActionProps_3b39a615):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None, role: typing.Optional[_IRole_e69bbae4]=None, service: _IBaseService_de6ed13e, image_file: typing.Optional[_ArtifactPath_8730c13b]=None, input: typing.Optional[_Artifact_af6d98e9]=None) -> None:
        """Construction properties of {@link EcsDeployAction}.

        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param service: The ECS Service to deploy.
        :param image_file: The name of the JSON image definitions file to use for deployments. The JSON file is a list of objects, each with 2 keys: ``name`` is the name of the container in the Task Definition, and ``imageUri`` is the Docker image URI you want to update your service with. Use this property if you want to use a different name for this file than the default 'imagedefinitions.json'. If you use this property, you don't need to specify the ``input`` property. Default: - one of this property, or ``input``, is required
        :param input: The input artifact that contains the JSON image definitions file to use for deployments. The JSON file is a list of objects, each with 2 keys: ``name`` is the name of the container in the Task Definition, and ``imageUri`` is the Docker image URI you want to update your service with. If you use this property, it's assumed the file is called 'imagedefinitions.json'. If your build uses a different file, leave this property empty, and use the ``imageFile`` property instead. Default: - one of this property, or ``imageFile``, is required

        stability
        :stability: experimental
        """
        self._values = {
            'action_name': action_name,
            'service': service,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if variables_namespace is not None: self._values["variables_namespace"] = variables_namespace
        if role is not None: self._values["role"] = role
        if image_file is not None: self._values["image_file"] = image_file
        if input is not None: self._values["input"] = input

    @builtins.property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        stability
        :stability: experimental
        """
        return self._values.get('action_name')

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        stability
        :stability: experimental
        """
        return self._values.get('run_order')

    @builtins.property
    def variables_namespace(self) -> typing.Optional[str]:
        """The name of the namespace to use for variables emitted by this action.

        default
        :default:

        - a name will be generated, based on the stage and action names,
          if any of the action's variables were referenced - otherwise,
          no namespace will be set

        stability
        :stability: experimental
        """
        return self._values.get('variables_namespace')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def service(self) -> _IBaseService_de6ed13e:
        """The ECS Service to deploy.

        stability
        :stability: experimental
        """
        return self._values.get('service')

    @builtins.property
    def image_file(self) -> typing.Optional[_ArtifactPath_8730c13b]:
        """The name of the JSON image definitions file to use for deployments.

        The JSON file is a list of objects,
        each with 2 keys: ``name`` is the name of the container in the Task Definition,
        and ``imageUri`` is the Docker image URI you want to update your service with.
        Use this property if you want to use a different name for this file than the default 'imagedefinitions.json'.
        If you use this property, you don't need to specify the ``input`` property.

        default
        :default: - one of this property, or ``input``, is required

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/pipelines-create.html#pipelines-create-image-definitions
        stability
        :stability: experimental
        """
        return self._values.get('image_file')

    @builtins.property
    def input(self) -> typing.Optional[_Artifact_af6d98e9]:
        """The input artifact that contains the JSON image definitions file to use for deployments.

        The JSON file is a list of objects,
        each with 2 keys: ``name`` is the name of the container in the Task Definition,
        and ``imageUri`` is the Docker image URI you want to update your service with.
        If you use this property, it's assumed the file is called 'imagedefinitions.json'.
        If your build uses a different file, leave this property empty,
        and use the ``imageFile`` property instead.

        default
        :default: - one of this property, or ``imageFile``, is required

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/pipelines-create.html#pipelines-create-image-definitions
        stability
        :stability: experimental
        """
        return self._values.get('input')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EcsDeployActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class GitHubSourceAction(Action, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codepipeline_actions.GitHubSourceAction"):
    """Source that is provided by a GitHub repository.

    stability
    :stability: experimental
    """
    def __init__(self, *, oauth_token: _SecretValue_99478b8b, output: _Artifact_af6d98e9, owner: str, repo: str, branch: typing.Optional[str]=None, trigger: typing.Optional["GitHubTrigger"]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None) -> None:
        """
        :param oauth_token: A GitHub OAuth token to use for authentication. It is recommended to use a Secrets Manager ``Secret`` to obtain the token: const oauth = cdk.SecretValue.secretsManager('my-github-token'); new GitHubSource(this, 'GitHubAction', { oauthToken: oauth, ... });
        :param output: 
        :param owner: The GitHub account/user that owns the repo.
        :param repo: The name of the repo, without the username.
        :param branch: The branch to use. Default: "master"
        :param trigger: How AWS CodePipeline should be triggered. With the default value "WEBHOOK", a webhook is created in GitHub that triggers the action With "POLL", CodePipeline periodically checks the source for changes With "None", the action is not triggered through changes in the source Default: GitHubTrigger.WEBHOOK
        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        stability
        :stability: experimental
        """
        props = GitHubSourceActionProps(oauth_token=oauth_token, output=output, owner=owner, repo=repo, branch=branch, trigger=trigger, action_name=action_name, run_order=run_order, variables_namespace=variables_namespace)

        jsii.create(GitHubSourceAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, scope: _Construct_f50a3f53, stage: _IStage_b7c853a7, *, bucket: _IBucket_25bad983, role: _IRole_e69bbae4) -> _ActionConfig_c379766c:
        """The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        _options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [scope, stage, _options])

    @builtins.property
    @jsii.member(jsii_name="variables")
    def variables(self) -> "GitHubSourceVariables":
        """The variables emitted by this action.

        stability
        :stability: experimental
        """
        return jsii.get(self, "variables")


@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.GitHubSourceActionProps", jsii_struct_bases=[_CommonActionProps_dd892888], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'variables_namespace': 'variablesNamespace', 'oauth_token': 'oauthToken', 'output': 'output', 'owner': 'owner', 'repo': 'repo', 'branch': 'branch', 'trigger': 'trigger'})
class GitHubSourceActionProps(_CommonActionProps_dd892888):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None, oauth_token: _SecretValue_99478b8b, output: _Artifact_af6d98e9, owner: str, repo: str, branch: typing.Optional[str]=None, trigger: typing.Optional["GitHubTrigger"]=None) -> None:
        """Construction properties of the {@link GitHubSourceAction GitHub source action}.

        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param oauth_token: A GitHub OAuth token to use for authentication. It is recommended to use a Secrets Manager ``Secret`` to obtain the token: const oauth = cdk.SecretValue.secretsManager('my-github-token'); new GitHubSource(this, 'GitHubAction', { oauthToken: oauth, ... });
        :param output: 
        :param owner: The GitHub account/user that owns the repo.
        :param repo: The name of the repo, without the username.
        :param branch: The branch to use. Default: "master"
        :param trigger: How AWS CodePipeline should be triggered. With the default value "WEBHOOK", a webhook is created in GitHub that triggers the action With "POLL", CodePipeline periodically checks the source for changes With "None", the action is not triggered through changes in the source Default: GitHubTrigger.WEBHOOK

        stability
        :stability: experimental
        """
        self._values = {
            'action_name': action_name,
            'oauth_token': oauth_token,
            'output': output,
            'owner': owner,
            'repo': repo,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if variables_namespace is not None: self._values["variables_namespace"] = variables_namespace
        if branch is not None: self._values["branch"] = branch
        if trigger is not None: self._values["trigger"] = trigger

    @builtins.property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        stability
        :stability: experimental
        """
        return self._values.get('action_name')

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        stability
        :stability: experimental
        """
        return self._values.get('run_order')

    @builtins.property
    def variables_namespace(self) -> typing.Optional[str]:
        """The name of the namespace to use for variables emitted by this action.

        default
        :default:

        - a name will be generated, based on the stage and action names,
          if any of the action's variables were referenced - otherwise,
          no namespace will be set

        stability
        :stability: experimental
        """
        return self._values.get('variables_namespace')

    @builtins.property
    def oauth_token(self) -> _SecretValue_99478b8b:
        """A GitHub OAuth token to use for authentication.

        It is recommended to use a Secrets Manager ``Secret`` to obtain the token:

        const oauth = cdk.SecretValue.secretsManager('my-github-token');
        new GitHubSource(this, 'GitHubAction', { oauthToken: oauth, ... });

        stability
        :stability: experimental
        """
        return self._values.get('oauth_token')

    @builtins.property
    def output(self) -> _Artifact_af6d98e9:
        """
        stability
        :stability: experimental
        """
        return self._values.get('output')

    @builtins.property
    def owner(self) -> str:
        """The GitHub account/user that owns the repo.

        stability
        :stability: experimental
        """
        return self._values.get('owner')

    @builtins.property
    def repo(self) -> str:
        """The name of the repo, without the username.

        stability
        :stability: experimental
        """
        return self._values.get('repo')

    @builtins.property
    def branch(self) -> typing.Optional[str]:
        """The branch to use.

        default
        :default: "master"

        stability
        :stability: experimental
        """
        return self._values.get('branch')

    @builtins.property
    def trigger(self) -> typing.Optional["GitHubTrigger"]:
        """How AWS CodePipeline should be triggered.

        With the default value "WEBHOOK", a webhook is created in GitHub that triggers the action
        With "POLL", CodePipeline periodically checks the source for changes
        With "None", the action is not triggered through changes in the source

        default
        :default: GitHubTrigger.WEBHOOK

        stability
        :stability: experimental
        """
        return self._values.get('trigger')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GitHubSourceActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.GitHubSourceVariables", jsii_struct_bases=[], name_mapping={'author_date': 'authorDate', 'branch_name': 'branchName', 'commit_id': 'commitId', 'commit_message': 'commitMessage', 'committer_date': 'committerDate', 'commit_url': 'commitUrl', 'repository_name': 'repositoryName'})
class GitHubSourceVariables():
    def __init__(self, *, author_date: str, branch_name: str, commit_id: str, commit_message: str, committer_date: str, commit_url: str, repository_name: str) -> None:
        """The CodePipeline variables emitted by GitHub source Action.

        :param author_date: The date the currently last commit on the tracked branch was authored, in ISO-8601 format.
        :param branch_name: The name of the branch this action tracks.
        :param commit_id: The SHA1 hash of the currently last commit on the tracked branch.
        :param commit_message: The message of the currently last commit on the tracked branch.
        :param committer_date: The date the currently last commit on the tracked branch was committed, in ISO-8601 format.
        :param commit_url: The GitHub API URL of the currently last commit on the tracked branch.
        :param repository_name: The name of the repository this action points to.

        stability
        :stability: experimental
        """
        self._values = {
            'author_date': author_date,
            'branch_name': branch_name,
            'commit_id': commit_id,
            'commit_message': commit_message,
            'committer_date': committer_date,
            'commit_url': commit_url,
            'repository_name': repository_name,
        }

    @builtins.property
    def author_date(self) -> str:
        """The date the currently last commit on the tracked branch was authored, in ISO-8601 format.

        stability
        :stability: experimental
        """
        return self._values.get('author_date')

    @builtins.property
    def branch_name(self) -> str:
        """The name of the branch this action tracks.

        stability
        :stability: experimental
        """
        return self._values.get('branch_name')

    @builtins.property
    def commit_id(self) -> str:
        """The SHA1 hash of the currently last commit on the tracked branch.

        stability
        :stability: experimental
        """
        return self._values.get('commit_id')

    @builtins.property
    def commit_message(self) -> str:
        """The message of the currently last commit on the tracked branch.

        stability
        :stability: experimental
        """
        return self._values.get('commit_message')

    @builtins.property
    def committer_date(self) -> str:
        """The date the currently last commit on the tracked branch was committed, in ISO-8601 format.

        stability
        :stability: experimental
        """
        return self._values.get('committer_date')

    @builtins.property
    def commit_url(self) -> str:
        """The GitHub API URL of the currently last commit on the tracked branch.

        stability
        :stability: experimental
        """
        return self._values.get('commit_url')

    @builtins.property
    def repository_name(self) -> str:
        """The name of the repository this action points to.

        stability
        :stability: experimental
        """
        return self._values.get('repository_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GitHubSourceVariables(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_codepipeline_actions.GitHubTrigger")
class GitHubTrigger(enum.Enum):
    """If and how the GitHub source action should be triggered.

    stability
    :stability: experimental
    """
    NONE = "NONE"
    """
    stability
    :stability: experimental
    """
    POLL = "POLL"
    """
    stability
    :stability: experimental
    """
    WEBHOOK = "WEBHOOK"
    """
    stability
    :stability: experimental
    """

@jsii.interface(jsii_type="monocdk-experiment.aws_codepipeline_actions.IJenkinsProvider")
class IJenkinsProvider(_IConstruct_db0cc7e3, jsii.compat.Protocol):
    """A Jenkins provider.

    If you want to create a new Jenkins provider managed alongside your CDK code,
    instantiate the {@link JenkinsProvider} class directly.

    If you want to reference an already registered provider,
    use the {@link JenkinsProvider#fromJenkinsProviderAttributes} method.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IJenkinsProviderProxy

    @builtins.property
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="serverUrl")
    def server_url(self) -> str:
        """
        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> str:
        """
        stability
        :stability: experimental
        """
        ...


class _IJenkinsProviderProxy(jsii.proxy_for(_IConstruct_db0cc7e3)):
    """A Jenkins provider.

    If you want to create a new Jenkins provider managed alongside your CDK code,
    instantiate the {@link JenkinsProvider} class directly.

    If you want to reference an already registered provider,
    use the {@link JenkinsProvider#fromJenkinsProviderAttributes} method.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_codepipeline_actions.IJenkinsProvider"
    @builtins.property
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "providerName")

    @builtins.property
    @jsii.member(jsii_name="serverUrl")
    def server_url(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "serverUrl")

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "version")


class JenkinsAction(Action, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codepipeline_actions.JenkinsAction"):
    """Jenkins build CodePipeline Action.

    see
    :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/tutorials-four-stage-pipeline.html
    stability
    :stability: experimental
    """
    def __init__(self, *, jenkins_provider: "IJenkinsProvider", project_name: str, type: "JenkinsActionType", inputs: typing.Optional[typing.List[_Artifact_af6d98e9]]=None, outputs: typing.Optional[typing.List[_Artifact_af6d98e9]]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None) -> None:
        """
        :param jenkins_provider: The Jenkins Provider for this Action.
        :param project_name: The name of the project (sometimes also called job, or task) on your Jenkins installation that will be invoked by this Action.
        :param type: The type of the Action - Build, or Test.
        :param inputs: The source to use as input for this build.
        :param outputs: 
        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        stability
        :stability: experimental
        """
        props = JenkinsActionProps(jenkins_provider=jenkins_provider, project_name=project_name, type=type, inputs=inputs, outputs=outputs, action_name=action_name, run_order=run_order, variables_namespace=variables_namespace)

        jsii.create(JenkinsAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, _scope: _Construct_f50a3f53, _stage: _IStage_b7c853a7, *, bucket: _IBucket_25bad983, role: _IRole_e69bbae4) -> _ActionConfig_c379766c:
        """The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param _stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        _options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [_scope, _stage, _options])


@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.JenkinsActionProps", jsii_struct_bases=[_CommonActionProps_dd892888], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'variables_namespace': 'variablesNamespace', 'jenkins_provider': 'jenkinsProvider', 'project_name': 'projectName', 'type': 'type', 'inputs': 'inputs', 'outputs': 'outputs'})
class JenkinsActionProps(_CommonActionProps_dd892888):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None, jenkins_provider: "IJenkinsProvider", project_name: str, type: "JenkinsActionType", inputs: typing.Optional[typing.List[_Artifact_af6d98e9]]=None, outputs: typing.Optional[typing.List[_Artifact_af6d98e9]]=None) -> None:
        """Construction properties of {@link JenkinsAction}.

        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param jenkins_provider: The Jenkins Provider for this Action.
        :param project_name: The name of the project (sometimes also called job, or task) on your Jenkins installation that will be invoked by this Action.
        :param type: The type of the Action - Build, or Test.
        :param inputs: The source to use as input for this build.
        :param outputs: 

        stability
        :stability: experimental
        """
        self._values = {
            'action_name': action_name,
            'jenkins_provider': jenkins_provider,
            'project_name': project_name,
            'type': type,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if variables_namespace is not None: self._values["variables_namespace"] = variables_namespace
        if inputs is not None: self._values["inputs"] = inputs
        if outputs is not None: self._values["outputs"] = outputs

    @builtins.property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        stability
        :stability: experimental
        """
        return self._values.get('action_name')

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        stability
        :stability: experimental
        """
        return self._values.get('run_order')

    @builtins.property
    def variables_namespace(self) -> typing.Optional[str]:
        """The name of the namespace to use for variables emitted by this action.

        default
        :default:

        - a name will be generated, based on the stage and action names,
          if any of the action's variables were referenced - otherwise,
          no namespace will be set

        stability
        :stability: experimental
        """
        return self._values.get('variables_namespace')

    @builtins.property
    def jenkins_provider(self) -> "IJenkinsProvider":
        """The Jenkins Provider for this Action.

        stability
        :stability: experimental
        """
        return self._values.get('jenkins_provider')

    @builtins.property
    def project_name(self) -> str:
        """The name of the project (sometimes also called job, or task) on your Jenkins installation that will be invoked by this Action.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "MyJob"
        """
        return self._values.get('project_name')

    @builtins.property
    def type(self) -> "JenkinsActionType":
        """The type of the Action - Build, or Test.

        stability
        :stability: experimental
        """
        return self._values.get('type')

    @builtins.property
    def inputs(self) -> typing.Optional[typing.List[_Artifact_af6d98e9]]:
        """The source to use as input for this build.

        stability
        :stability: experimental
        """
        return self._values.get('inputs')

    @builtins.property
    def outputs(self) -> typing.Optional[typing.List[_Artifact_af6d98e9]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('outputs')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'JenkinsActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_codepipeline_actions.JenkinsActionType")
class JenkinsActionType(enum.Enum):
    """The type of the Jenkins Action that determines its CodePipeline Category - Build, or Test.

    Note that a Jenkins provider, even if it has the same name,
    must be separately registered for each type.

    stability
    :stability: experimental
    """
    BUILD = "BUILD"
    """The Action will have the Build Category.

    stability
    :stability: experimental
    """
    TEST = "TEST"
    """The Action will have the Test Category.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.JenkinsProviderAttributes", jsii_struct_bases=[], name_mapping={'provider_name': 'providerName', 'server_url': 'serverUrl', 'version': 'version'})
class JenkinsProviderAttributes():
    def __init__(self, *, provider_name: str, server_url: str, version: typing.Optional[str]=None) -> None:
        """Properties for importing an existing Jenkins provider.

        :param provider_name: The name of the Jenkins provider that you set in the AWS CodePipeline plugin configuration of your Jenkins project.
        :param server_url: The base URL of your Jenkins server.
        :param version: The version of your provider. Default: '1'

        stability
        :stability: experimental
        """
        self._values = {
            'provider_name': provider_name,
            'server_url': server_url,
        }
        if version is not None: self._values["version"] = version

    @builtins.property
    def provider_name(self) -> str:
        """The name of the Jenkins provider that you set in the AWS CodePipeline plugin configuration of your Jenkins project.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "MyJenkinsProvider"
        """
        return self._values.get('provider_name')

    @builtins.property
    def server_url(self) -> str:
        """The base URL of your Jenkins server.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "http://myjenkins.com:8080"
        """
        return self._values.get('server_url')

    @builtins.property
    def version(self) -> typing.Optional[str]:
        """The version of your provider.

        default
        :default: '1'

        stability
        :stability: experimental
        """
        return self._values.get('version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'JenkinsProviderAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.JenkinsProviderProps", jsii_struct_bases=[], name_mapping={'provider_name': 'providerName', 'server_url': 'serverUrl', 'for_build': 'forBuild', 'for_test': 'forTest', 'version': 'version'})
class JenkinsProviderProps():
    def __init__(self, *, provider_name: str, server_url: str, for_build: typing.Optional[bool]=None, for_test: typing.Optional[bool]=None, version: typing.Optional[str]=None) -> None:
        """
        :param provider_name: The name of the Jenkins provider that you set in the AWS CodePipeline plugin configuration of your Jenkins project.
        :param server_url: The base URL of your Jenkins server.
        :param for_build: Whether to immediately register a Jenkins Provider for the build category. The Provider will always be registered if you create a {@link JenkinsAction}. Default: false
        :param for_test: Whether to immediately register a Jenkins Provider for the test category. The Provider will always be registered if you create a {@link JenkinsTestAction}. Default: false
        :param version: The version of your provider. Default: '1'

        stability
        :stability: experimental
        """
        self._values = {
            'provider_name': provider_name,
            'server_url': server_url,
        }
        if for_build is not None: self._values["for_build"] = for_build
        if for_test is not None: self._values["for_test"] = for_test
        if version is not None: self._values["version"] = version

    @builtins.property
    def provider_name(self) -> str:
        """The name of the Jenkins provider that you set in the AWS CodePipeline plugin configuration of your Jenkins project.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "MyJenkinsProvider"
        """
        return self._values.get('provider_name')

    @builtins.property
    def server_url(self) -> str:
        """The base URL of your Jenkins server.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "http://myjenkins.com:8080"
        """
        return self._values.get('server_url')

    @builtins.property
    def for_build(self) -> typing.Optional[bool]:
        """Whether to immediately register a Jenkins Provider for the build category.

        The Provider will always be registered if you create a {@link JenkinsAction}.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('for_build')

    @builtins.property
    def for_test(self) -> typing.Optional[bool]:
        """Whether to immediately register a Jenkins Provider for the test category.

        The Provider will always be registered if you create a {@link JenkinsTestAction}.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('for_test')

    @builtins.property
    def version(self) -> typing.Optional[str]:
        """The version of your provider.

        default
        :default: '1'

        stability
        :stability: experimental
        """
        return self._values.get('version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'JenkinsProviderProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class LambdaInvokeAction(Action, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codepipeline_actions.LambdaInvokeAction"):
    """CodePipeline invoke Action that is provided by an AWS Lambda function.

    see
    :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/actions-invoke-lambda-function.html
    stability
    :stability: experimental
    """
    def __init__(self, *, lambda_: _IFunction_1c1de0bc, inputs: typing.Optional[typing.List[_Artifact_af6d98e9]]=None, outputs: typing.Optional[typing.List[_Artifact_af6d98e9]]=None, user_parameters: typing.Optional[typing.Mapping[str, typing.Any]]=None, role: typing.Optional[_IRole_e69bbae4]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None) -> None:
        """
        :param lambda_: The lambda function to invoke.
        :param inputs: The optional input Artifacts of the Action. A Lambda Action can have up to 5 inputs. The inputs will appear in the event passed to the Lambda, under the ``'CodePipeline.job'.data.inputArtifacts`` path. Default: the Action will not have any inputs
        :param outputs: The optional names of the output Artifacts of the Action. A Lambda Action can have up to 5 outputs. The outputs will appear in the event passed to the Lambda, under the ``'CodePipeline.job'.data.outputArtifacts`` path. It is the responsibility of the Lambda to upload ZIP files with the Artifact contents to the provided locations. Default: the Action will not have any outputs
        :param user_parameters: A set of key-value pairs that will be accessible to the invoked Lambda inside the event that the Pipeline will call it with.
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        stability
        :stability: experimental
        """
        props = LambdaInvokeActionProps(lambda_=lambda_, inputs=inputs, outputs=outputs, user_parameters=user_parameters, role=role, action_name=action_name, run_order=run_order, variables_namespace=variables_namespace)

        jsii.create(LambdaInvokeAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, scope: _Construct_f50a3f53, _stage: _IStage_b7c853a7, *, bucket: _IBucket_25bad983, role: _IRole_e69bbae4) -> _ActionConfig_c379766c:
        """The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param _stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [scope, _stage, options])

    @jsii.member(jsii_name="variable")
    def variable(self, variable_name: str) -> str:
        """Reference a CodePipeline variable defined by the Lambda function this action points to.

        Variables in Lambda invoke actions are defined by calling the PutJobSuccessResult CodePipeline API call
        with the 'outputVariables' property filled.

        :param variable_name: the name of the variable to reference. A variable by this name must be present in the 'outputVariables' section of the PutJobSuccessResult request that the Lambda function calls when the action is invoked

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/APIReference/API_PutJobSuccessResult.html
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "variable", [variable_name])


@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.LambdaInvokeActionProps", jsii_struct_bases=[_CommonAwsActionProps_3b39a615], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'variables_namespace': 'variablesNamespace', 'role': 'role', 'lambda_': 'lambda', 'inputs': 'inputs', 'outputs': 'outputs', 'user_parameters': 'userParameters'})
class LambdaInvokeActionProps(_CommonAwsActionProps_3b39a615):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None, role: typing.Optional[_IRole_e69bbae4]=None, lambda_: _IFunction_1c1de0bc, inputs: typing.Optional[typing.List[_Artifact_af6d98e9]]=None, outputs: typing.Optional[typing.List[_Artifact_af6d98e9]]=None, user_parameters: typing.Optional[typing.Mapping[str, typing.Any]]=None) -> None:
        """Construction properties of the {@link LambdaInvokeAction Lambda invoke CodePipeline Action}.

        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param lambda_: The lambda function to invoke.
        :param inputs: The optional input Artifacts of the Action. A Lambda Action can have up to 5 inputs. The inputs will appear in the event passed to the Lambda, under the ``'CodePipeline.job'.data.inputArtifacts`` path. Default: the Action will not have any inputs
        :param outputs: The optional names of the output Artifacts of the Action. A Lambda Action can have up to 5 outputs. The outputs will appear in the event passed to the Lambda, under the ``'CodePipeline.job'.data.outputArtifacts`` path. It is the responsibility of the Lambda to upload ZIP files with the Artifact contents to the provided locations. Default: the Action will not have any outputs
        :param user_parameters: A set of key-value pairs that will be accessible to the invoked Lambda inside the event that the Pipeline will call it with.

        stability
        :stability: experimental
        """
        self._values = {
            'action_name': action_name,
            'lambda_': lambda_,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if variables_namespace is not None: self._values["variables_namespace"] = variables_namespace
        if role is not None: self._values["role"] = role
        if inputs is not None: self._values["inputs"] = inputs
        if outputs is not None: self._values["outputs"] = outputs
        if user_parameters is not None: self._values["user_parameters"] = user_parameters

    @builtins.property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        stability
        :stability: experimental
        """
        return self._values.get('action_name')

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        stability
        :stability: experimental
        """
        return self._values.get('run_order')

    @builtins.property
    def variables_namespace(self) -> typing.Optional[str]:
        """The name of the namespace to use for variables emitted by this action.

        default
        :default:

        - a name will be generated, based on the stage and action names,
          if any of the action's variables were referenced - otherwise,
          no namespace will be set

        stability
        :stability: experimental
        """
        return self._values.get('variables_namespace')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def lambda_(self) -> _IFunction_1c1de0bc:
        """The lambda function to invoke.

        stability
        :stability: experimental
        """
        return self._values.get('lambda_')

    @builtins.property
    def inputs(self) -> typing.Optional[typing.List[_Artifact_af6d98e9]]:
        """The optional input Artifacts of the Action.

        A Lambda Action can have up to 5 inputs.
        The inputs will appear in the event passed to the Lambda,
        under the ``'CodePipeline.job'.data.inputArtifacts`` path.

        default
        :default: the Action will not have any inputs

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/actions-invoke-lambda-function.html#actions-invoke-lambda-function-json-event-example
        stability
        :stability: experimental
        """
        return self._values.get('inputs')

    @builtins.property
    def outputs(self) -> typing.Optional[typing.List[_Artifact_af6d98e9]]:
        """The optional names of the output Artifacts of the Action.

        A Lambda Action can have up to 5 outputs.
        The outputs will appear in the event passed to the Lambda,
        under the ``'CodePipeline.job'.data.outputArtifacts`` path.
        It is the responsibility of the Lambda to upload ZIP files with the Artifact contents to the provided locations.

        default
        :default: the Action will not have any outputs

        stability
        :stability: experimental
        """
        return self._values.get('outputs')

    @builtins.property
    def user_parameters(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """A set of key-value pairs that will be accessible to the invoked Lambda inside the event that the Pipeline will call it with.

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/actions-invoke-lambda-function.html#actions-invoke-lambda-function-json-event-example
        stability
        :stability: experimental
        """
        return self._values.get('user_parameters')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LambdaInvokeActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ManualApprovalAction(Action, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codepipeline_actions.ManualApprovalAction"):
    """Manual approval action.

    stability
    :stability: experimental
    """
    def __init__(self, *, additional_information: typing.Optional[str]=None, external_entity_link: typing.Optional[str]=None, notification_topic: typing.Optional[_ITopic_ef0ebe0e]=None, notify_emails: typing.Optional[typing.List[str]]=None, role: typing.Optional[_IRole_e69bbae4]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None) -> None:
        """
        :param additional_information: Any additional information that you want to include in the notification email message.
        :param external_entity_link: URL you want to provide to the reviewer as part of the approval request. Default: - the approval request will not have an external link
        :param notification_topic: Optional SNS topic to send notifications to when an approval is pending.
        :param notify_emails: A list of email addresses to subscribe to notifications when this Action is pending approval. If this has been provided, but not ``notificationTopic``, a new Topic will be created.
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        stability
        :stability: experimental
        """
        props = ManualApprovalActionProps(additional_information=additional_information, external_entity_link=external_entity_link, notification_topic=notification_topic, notify_emails=notify_emails, role=role, action_name=action_name, run_order=run_order, variables_namespace=variables_namespace)

        jsii.create(ManualApprovalAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, scope: _Construct_f50a3f53, _stage: _IStage_b7c853a7, *, bucket: _IBucket_25bad983, role: _IRole_e69bbae4) -> _ActionConfig_c379766c:
        """The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param _stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [scope, _stage, options])

    @builtins.property
    @jsii.member(jsii_name="notificationTopic")
    def notification_topic(self) -> typing.Optional[_ITopic_ef0ebe0e]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "notificationTopic")


@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.ManualApprovalActionProps", jsii_struct_bases=[_CommonAwsActionProps_3b39a615], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'variables_namespace': 'variablesNamespace', 'role': 'role', 'additional_information': 'additionalInformation', 'external_entity_link': 'externalEntityLink', 'notification_topic': 'notificationTopic', 'notify_emails': 'notifyEmails'})
class ManualApprovalActionProps(_CommonAwsActionProps_3b39a615):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None, role: typing.Optional[_IRole_e69bbae4]=None, additional_information: typing.Optional[str]=None, external_entity_link: typing.Optional[str]=None, notification_topic: typing.Optional[_ITopic_ef0ebe0e]=None, notify_emails: typing.Optional[typing.List[str]]=None) -> None:
        """Construction properties of the {@link ManualApprovalAction}.

        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param additional_information: Any additional information that you want to include in the notification email message.
        :param external_entity_link: URL you want to provide to the reviewer as part of the approval request. Default: - the approval request will not have an external link
        :param notification_topic: Optional SNS topic to send notifications to when an approval is pending.
        :param notify_emails: A list of email addresses to subscribe to notifications when this Action is pending approval. If this has been provided, but not ``notificationTopic``, a new Topic will be created.

        stability
        :stability: experimental
        """
        self._values = {
            'action_name': action_name,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if variables_namespace is not None: self._values["variables_namespace"] = variables_namespace
        if role is not None: self._values["role"] = role
        if additional_information is not None: self._values["additional_information"] = additional_information
        if external_entity_link is not None: self._values["external_entity_link"] = external_entity_link
        if notification_topic is not None: self._values["notification_topic"] = notification_topic
        if notify_emails is not None: self._values["notify_emails"] = notify_emails

    @builtins.property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        stability
        :stability: experimental
        """
        return self._values.get('action_name')

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        stability
        :stability: experimental
        """
        return self._values.get('run_order')

    @builtins.property
    def variables_namespace(self) -> typing.Optional[str]:
        """The name of the namespace to use for variables emitted by this action.

        default
        :default:

        - a name will be generated, based on the stage and action names,
          if any of the action's variables were referenced - otherwise,
          no namespace will be set

        stability
        :stability: experimental
        """
        return self._values.get('variables_namespace')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def additional_information(self) -> typing.Optional[str]:
        """Any additional information that you want to include in the notification email message.

        stability
        :stability: experimental
        """
        return self._values.get('additional_information')

    @builtins.property
    def external_entity_link(self) -> typing.Optional[str]:
        """URL you want to provide to the reviewer as part of the approval request.

        default
        :default: - the approval request will not have an external link

        stability
        :stability: experimental
        """
        return self._values.get('external_entity_link')

    @builtins.property
    def notification_topic(self) -> typing.Optional[_ITopic_ef0ebe0e]:
        """Optional SNS topic to send notifications to when an approval is pending.

        stability
        :stability: experimental
        """
        return self._values.get('notification_topic')

    @builtins.property
    def notify_emails(self) -> typing.Optional[typing.List[str]]:
        """A list of email addresses to subscribe to notifications when this Action is pending approval.

        If this has been provided, but not ``notificationTopic``,
        a new Topic will be created.

        stability
        :stability: experimental
        """
        return self._values.get('notify_emails')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ManualApprovalActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class S3DeployAction(Action, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codepipeline_actions.S3DeployAction"):
    """Deploys the sourceArtifact to Amazon S3.

    stability
    :stability: experimental
    """
    def __init__(self, *, bucket: _IBucket_25bad983, input: _Artifact_af6d98e9, access_control: typing.Optional[_BucketAccessControl_028b0d87]=None, cache_control: typing.Optional[typing.List["CacheControl"]]=None, extract: typing.Optional[bool]=None, object_key: typing.Optional[str]=None, role: typing.Optional[_IRole_e69bbae4]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None) -> None:
        """
        :param bucket: The Amazon S3 bucket that is the deploy target.
        :param input: The input Artifact to deploy to Amazon S3.
        :param access_control: The specified canned ACL to objects deployed to Amazon S3. This overwrites any existing ACL that was applied to the object. Default: - the original object ACL
        :param cache_control: The caching behavior for requests/responses for objects in the bucket. The final cache control property will be the result of joining all of the provided array elements with a comma (plus a space after the comma). Default: - none, decided by the HTTP client
        :param extract: Should the deploy action extract the artifact before deploying to Amazon S3. Default: true
        :param object_key: The key of the target object. This is required if extract is false.
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        stability
        :stability: experimental
        """
        props = S3DeployActionProps(bucket=bucket, input=input, access_control=access_control, cache_control=cache_control, extract=extract, object_key=object_key, role=role, action_name=action_name, run_order=run_order, variables_namespace=variables_namespace)

        jsii.create(S3DeployAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, _scope: _Construct_f50a3f53, _stage: _IStage_b7c853a7, *, bucket: _IBucket_25bad983, role: _IRole_e69bbae4) -> _ActionConfig_c379766c:
        """The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param _stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [_scope, _stage, options])


@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.S3DeployActionProps", jsii_struct_bases=[_CommonAwsActionProps_3b39a615], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'variables_namespace': 'variablesNamespace', 'role': 'role', 'bucket': 'bucket', 'input': 'input', 'access_control': 'accessControl', 'cache_control': 'cacheControl', 'extract': 'extract', 'object_key': 'objectKey'})
class S3DeployActionProps(_CommonAwsActionProps_3b39a615):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None, role: typing.Optional[_IRole_e69bbae4]=None, bucket: _IBucket_25bad983, input: _Artifact_af6d98e9, access_control: typing.Optional[_BucketAccessControl_028b0d87]=None, cache_control: typing.Optional[typing.List["CacheControl"]]=None, extract: typing.Optional[bool]=None, object_key: typing.Optional[str]=None) -> None:
        """Construction properties of the {@link S3DeployAction S3 deploy Action}.

        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param bucket: The Amazon S3 bucket that is the deploy target.
        :param input: The input Artifact to deploy to Amazon S3.
        :param access_control: The specified canned ACL to objects deployed to Amazon S3. This overwrites any existing ACL that was applied to the object. Default: - the original object ACL
        :param cache_control: The caching behavior for requests/responses for objects in the bucket. The final cache control property will be the result of joining all of the provided array elements with a comma (plus a space after the comma). Default: - none, decided by the HTTP client
        :param extract: Should the deploy action extract the artifact before deploying to Amazon S3. Default: true
        :param object_key: The key of the target object. This is required if extract is false.

        stability
        :stability: experimental
        """
        self._values = {
            'action_name': action_name,
            'bucket': bucket,
            'input': input,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if variables_namespace is not None: self._values["variables_namespace"] = variables_namespace
        if role is not None: self._values["role"] = role
        if access_control is not None: self._values["access_control"] = access_control
        if cache_control is not None: self._values["cache_control"] = cache_control
        if extract is not None: self._values["extract"] = extract
        if object_key is not None: self._values["object_key"] = object_key

    @builtins.property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        stability
        :stability: experimental
        """
        return self._values.get('action_name')

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        stability
        :stability: experimental
        """
        return self._values.get('run_order')

    @builtins.property
    def variables_namespace(self) -> typing.Optional[str]:
        """The name of the namespace to use for variables emitted by this action.

        default
        :default:

        - a name will be generated, based on the stage and action names,
          if any of the action's variables were referenced - otherwise,
          no namespace will be set

        stability
        :stability: experimental
        """
        return self._values.get('variables_namespace')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def bucket(self) -> _IBucket_25bad983:
        """The Amazon S3 bucket that is the deploy target.

        stability
        :stability: experimental
        """
        return self._values.get('bucket')

    @builtins.property
    def input(self) -> _Artifact_af6d98e9:
        """The input Artifact to deploy to Amazon S3.

        stability
        :stability: experimental
        """
        return self._values.get('input')

    @builtins.property
    def access_control(self) -> typing.Optional[_BucketAccessControl_028b0d87]:
        """The specified canned ACL to objects deployed to Amazon S3.

        This overwrites any existing ACL that was applied to the object.

        default
        :default: - the original object ACL

        stability
        :stability: experimental
        """
        return self._values.get('access_control')

    @builtins.property
    def cache_control(self) -> typing.Optional[typing.List["CacheControl"]]:
        """The caching behavior for requests/responses for objects in the bucket.

        The final cache control property will be the result of joining all of the provided array elements with a comma
        (plus a space after the comma).

        default
        :default: - none, decided by the HTTP client

        stability
        :stability: experimental
        """
        return self._values.get('cache_control')

    @builtins.property
    def extract(self) -> typing.Optional[bool]:
        """Should the deploy action extract the artifact before deploying to Amazon S3.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('extract')

    @builtins.property
    def object_key(self) -> typing.Optional[str]:
        """The key of the target object.

        This is required if extract is false.

        stability
        :stability: experimental
        """
        return self._values.get('object_key')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'S3DeployActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class S3SourceAction(Action, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codepipeline_actions.S3SourceAction"):
    """Source that is provided by a specific Amazon S3 object.

    Will trigger the pipeline as soon as the S3 object changes, but only if there is
    a CloudTrail Trail in the account that captures the S3 event.

    stability
    :stability: experimental
    """
    def __init__(self, *, bucket: _IBucket_25bad983, bucket_key: str, output: _Artifact_af6d98e9, trigger: typing.Optional["S3Trigger"]=None, role: typing.Optional[_IRole_e69bbae4]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None) -> None:
        """
        :param bucket: The Amazon S3 bucket that stores the source code.
        :param bucket_key: The key within the S3 bucket that stores the source code.
        :param output: 
        :param trigger: How should CodePipeline detect source changes for this Action. Note that if this is S3Trigger.EVENTS, you need to make sure to include the source Bucket in a CloudTrail Trail, as otherwise the CloudWatch Events will not be emitted. Default: S3Trigger.POLL
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        stability
        :stability: experimental
        """
        props = S3SourceActionProps(bucket=bucket, bucket_key=bucket_key, output=output, trigger=trigger, role=role, action_name=action_name, run_order=run_order, variables_namespace=variables_namespace)

        jsii.create(S3SourceAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, _scope: _Construct_f50a3f53, stage: _IStage_b7c853a7, *, bucket: _IBucket_25bad983, role: _IRole_e69bbae4) -> _ActionConfig_c379766c:
        """The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [_scope, stage, options])

    @builtins.property
    @jsii.member(jsii_name="variables")
    def variables(self) -> "S3SourceVariables":
        """The variables emitted by this action.

        stability
        :stability: experimental
        """
        return jsii.get(self, "variables")


@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.S3SourceActionProps", jsii_struct_bases=[_CommonAwsActionProps_3b39a615], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'variables_namespace': 'variablesNamespace', 'role': 'role', 'bucket': 'bucket', 'bucket_key': 'bucketKey', 'output': 'output', 'trigger': 'trigger'})
class S3SourceActionProps(_CommonAwsActionProps_3b39a615):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, variables_namespace: typing.Optional[str]=None, role: typing.Optional[_IRole_e69bbae4]=None, bucket: _IBucket_25bad983, bucket_key: str, output: _Artifact_af6d98e9, trigger: typing.Optional["S3Trigger"]=None) -> None:
        """Construction properties of the {@link S3SourceAction S3 source Action}.

        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param bucket: The Amazon S3 bucket that stores the source code.
        :param bucket_key: The key within the S3 bucket that stores the source code.
        :param output: 
        :param trigger: How should CodePipeline detect source changes for this Action. Note that if this is S3Trigger.EVENTS, you need to make sure to include the source Bucket in a CloudTrail Trail, as otherwise the CloudWatch Events will not be emitted. Default: S3Trigger.POLL

        stability
        :stability: experimental
        """
        self._values = {
            'action_name': action_name,
            'bucket': bucket,
            'bucket_key': bucket_key,
            'output': output,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if variables_namespace is not None: self._values["variables_namespace"] = variables_namespace
        if role is not None: self._values["role"] = role
        if trigger is not None: self._values["trigger"] = trigger

    @builtins.property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        stability
        :stability: experimental
        """
        return self._values.get('action_name')

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        stability
        :stability: experimental
        """
        return self._values.get('run_order')

    @builtins.property
    def variables_namespace(self) -> typing.Optional[str]:
        """The name of the namespace to use for variables emitted by this action.

        default
        :default:

        - a name will be generated, based on the stage and action names,
          if any of the action's variables were referenced - otherwise,
          no namespace will be set

        stability
        :stability: experimental
        """
        return self._values.get('variables_namespace')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def bucket(self) -> _IBucket_25bad983:
        """The Amazon S3 bucket that stores the source code.

        stability
        :stability: experimental
        """
        return self._values.get('bucket')

    @builtins.property
    def bucket_key(self) -> str:
        """The key within the S3 bucket that stores the source code.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "path/to/file.zip"
        """
        return self._values.get('bucket_key')

    @builtins.property
    def output(self) -> _Artifact_af6d98e9:
        """
        stability
        :stability: experimental
        """
        return self._values.get('output')

    @builtins.property
    def trigger(self) -> typing.Optional["S3Trigger"]:
        """How should CodePipeline detect source changes for this Action.

        Note that if this is S3Trigger.EVENTS, you need to make sure to include the source Bucket in a CloudTrail Trail,
        as otherwise the CloudWatch Events will not be emitted.

        default
        :default: S3Trigger.POLL

        see
        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/log-s3-data-events.html
        stability
        :stability: experimental
        """
        return self._values.get('trigger')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'S3SourceActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_codepipeline_actions.S3SourceVariables", jsii_struct_bases=[], name_mapping={'e_tag': 'eTag', 'version_id': 'versionId'})
class S3SourceVariables():
    def __init__(self, *, e_tag: str, version_id: str) -> None:
        """The CodePipeline variables emitted by the S3 source Action.

        :param e_tag: The e-tag of the S3 version of the object that triggered the build.
        :param version_id: The identifier of the S3 version of the object that triggered the build.

        stability
        :stability: experimental
        """
        self._values = {
            'e_tag': e_tag,
            'version_id': version_id,
        }

    @builtins.property
    def e_tag(self) -> str:
        """The e-tag of the S3 version of the object that triggered the build.

        stability
        :stability: experimental
        """
        return self._values.get('e_tag')

    @builtins.property
    def version_id(self) -> str:
        """The identifier of the S3 version of the object that triggered the build.

        stability
        :stability: experimental
        """
        return self._values.get('version_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'S3SourceVariables(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_codepipeline_actions.S3Trigger")
class S3Trigger(enum.Enum):
    """How should the S3 Action detect changes.

    This is the type of the {@link S3SourceAction.trigger} property.

    stability
    :stability: experimental
    """
    NONE = "NONE"
    """The Action will never detect changes - the Pipeline it's part of will only begin a run when explicitly started.

    stability
    :stability: experimental
    """
    POLL = "POLL"
    """CodePipeline will poll S3 to detect changes.

    This is the default method of detecting changes.

    stability
    :stability: experimental
    """
    EVENTS = "EVENTS"
    """CodePipeline will use CloudWatch Events to be notified of changes.

    Note that the Bucket that the Action uses needs to be part of a CloudTrail Trail
    for the events to be delivered.

    stability
    :stability: experimental
    """

@jsii.implements(IJenkinsProvider)
class BaseJenkinsProvider(_Construct_f50a3f53, metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.aws_codepipeline_actions.BaseJenkinsProvider"):
    """
    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _BaseJenkinsProviderProxy

    def __init__(self, scope: _Construct_f50a3f53, id: str, version: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param version: -

        stability
        :stability: experimental
        """
        jsii.create(BaseJenkinsProvider, self, [scope, id, version])

    @builtins.property
    @jsii.member(jsii_name="providerName")
    @abc.abstractmethod
    def provider_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="serverUrl")
    @abc.abstractmethod
    def server_url(self) -> str:
        """
        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "version")


class _BaseJenkinsProviderProxy(BaseJenkinsProvider):
    @builtins.property
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "providerName")

    @builtins.property
    @jsii.member(jsii_name="serverUrl")
    def server_url(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "serverUrl")


class JenkinsProvider(BaseJenkinsProvider, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codepipeline_actions.JenkinsProvider"):
    """A class representing Jenkins providers.

    see
    :see: #import
    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, provider_name: str, server_url: str, for_build: typing.Optional[bool]=None, for_test: typing.Optional[bool]=None, version: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param provider_name: The name of the Jenkins provider that you set in the AWS CodePipeline plugin configuration of your Jenkins project.
        :param server_url: The base URL of your Jenkins server.
        :param for_build: Whether to immediately register a Jenkins Provider for the build category. The Provider will always be registered if you create a {@link JenkinsAction}. Default: false
        :param for_test: Whether to immediately register a Jenkins Provider for the test category. The Provider will always be registered if you create a {@link JenkinsTestAction}. Default: false
        :param version: The version of your provider. Default: '1'

        stability
        :stability: experimental
        """
        props = JenkinsProviderProps(provider_name=provider_name, server_url=server_url, for_build=for_build, for_test=for_test, version=version)

        jsii.create(JenkinsProvider, self, [scope, id, props])

    @jsii.member(jsii_name="fromJenkinsProviderAttributes")
    @builtins.classmethod
    def from_jenkins_provider_attributes(cls, scope: _Construct_f50a3f53, id: str, *, provider_name: str, server_url: str, version: typing.Optional[str]=None) -> "IJenkinsProvider":
        """Import a Jenkins provider registered either outside the CDK, or in a different CDK Stack.

        :param scope: the parent Construct for the new provider.
        :param id: the identifier of the new provider Construct.
        :param provider_name: The name of the Jenkins provider that you set in the AWS CodePipeline plugin configuration of your Jenkins project.
        :param server_url: The base URL of your Jenkins server.
        :param version: The version of your provider. Default: '1'

        return
        :return: a new Construct representing a reference to an existing Jenkins provider

        stability
        :stability: experimental
        """
        attrs = JenkinsProviderAttributes(provider_name=provider_name, server_url=server_url, version=version)

        return jsii.sinvoke(cls, "fromJenkinsProviderAttributes", [scope, id, attrs])

    @builtins.property
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "providerName")

    @builtins.property
    @jsii.member(jsii_name="serverUrl")
    def server_url(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "serverUrl")


__all__ = [
    "Action",
    "AlexaSkillDeployAction",
    "AlexaSkillDeployActionProps",
    "BaseJenkinsProvider",
    "BitBucketSourceAction",
    "BitBucketSourceActionProps",
    "CacheControl",
    "CloudFormationCreateReplaceChangeSetAction",
    "CloudFormationCreateReplaceChangeSetActionProps",
    "CloudFormationCreateUpdateStackAction",
    "CloudFormationCreateUpdateStackActionProps",
    "CloudFormationDeleteStackAction",
    "CloudFormationDeleteStackActionProps",
    "CloudFormationExecuteChangeSetAction",
    "CloudFormationExecuteChangeSetActionProps",
    "CodeBuildAction",
    "CodeBuildActionProps",
    "CodeBuildActionType",
    "CodeCommitSourceAction",
    "CodeCommitSourceActionProps",
    "CodeCommitSourceVariables",
    "CodeCommitTrigger",
    "CodeDeployEcsContainerImageInput",
    "CodeDeployEcsDeployAction",
    "CodeDeployEcsDeployActionProps",
    "CodeDeployServerDeployAction",
    "CodeDeployServerDeployActionProps",
    "EcrSourceAction",
    "EcrSourceActionProps",
    "EcrSourceVariables",
    "EcsDeployAction",
    "EcsDeployActionProps",
    "GitHubSourceAction",
    "GitHubSourceActionProps",
    "GitHubSourceVariables",
    "GitHubTrigger",
    "IJenkinsProvider",
    "JenkinsAction",
    "JenkinsActionProps",
    "JenkinsActionType",
    "JenkinsProvider",
    "JenkinsProviderAttributes",
    "JenkinsProviderProps",
    "LambdaInvokeAction",
    "LambdaInvokeActionProps",
    "ManualApprovalAction",
    "ManualApprovalActionProps",
    "S3DeployAction",
    "S3DeployActionProps",
    "S3SourceAction",
    "S3SourceActionProps",
    "S3SourceVariables",
    "S3Trigger",
]

publication.publish()
