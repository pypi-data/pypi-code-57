import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (Construct as _Construct_f50a3f53, Stack as _Stack_05f4505a)
from ..aws_cloudformation import (CloudFormationCapabilities as _CloudFormationCapabilities_979dd343)
from ..aws_codepipeline import (ActionConfig as _ActionConfig_c379766c, IStage as _IStage_b7c853a7, ActionBindOptions as _ActionBindOptions_530c352f, ActionProperties as _ActionProperties_8f5d7a9d, IAction as _IAction_369e77ae, Artifact as _Artifact_af6d98e9)
from ..aws_events import (Rule as _Rule_c38e0b39, IRuleTarget as _IRuleTarget_41800a77, RuleProps as _RuleProps_d60f0abf)
from ..aws_iam import (PolicyStatement as _PolicyStatement_f75dc775, IRole as _IRole_e69bbae4)


@jsii.implements(_IAction_369e77ae)
class PipelineDeployStackAction(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.app_delivery.PipelineDeployStackAction"):
    """A class to deploy a stack that is part of a CDK App, using CodePipeline.

    This composite Action takes care of preparing and executing a CloudFormation ChangeSet.

    It currently does *not* support stacks that make use of ``Asset``s, and
    requires the deployed stack is in the same account and region where the
    CodePipeline is hosted.

    stability
    :stability: experimental
    """
    def __init__(self, *, admin_permissions: bool, input: _Artifact_af6d98e9, stack: _Stack_05f4505a, capabilities: typing.Optional[typing.List[_CloudFormationCapabilities_979dd343]]=None, change_set_name: typing.Optional[str]=None, create_change_set_action_name: typing.Optional[str]=None, create_change_set_run_order: typing.Optional[jsii.Number]=None, execute_change_set_action_name: typing.Optional[str]=None, execute_change_set_run_order: typing.Optional[jsii.Number]=None, role: typing.Optional[_IRole_e69bbae4]=None) -> None:
        """
        :param admin_permissions: Whether to grant admin permissions to CloudFormation while deploying this template. Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you don't specify any alternatives. The default role that will be created for you will have admin (i.e., ``*``) permissions on all resources, and the deployment will have named IAM capabilities (i.e., able to create all IAM resources). This is a shorthand that you can use if you fully trust the templates that are deployed in this pipeline. If you want more fine-grained permissions, use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation deployment is allowed to do.
        :param input: The CodePipeline artifact that holds the synthesized app, which is the contents of the ``<directory>`` when running ``cdk synth -o <directory>``.
        :param stack: The CDK stack to be deployed.
        :param capabilities: Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation might create or update those resources. For example, you must specify AnonymousIAM if your stack template contains AWS Identity and Access Management (IAM) resources. For more information Default: [AnonymousIAM, AutoExpand], unless ``adminPermissions`` is true
        :param change_set_name: The name to use when creating a ChangeSet for the stack. Default: CDK-CodePipeline-ChangeSet
        :param create_change_set_action_name: The name of the CodePipeline action creating the ChangeSet. Default: 'ChangeSet'
        :param create_change_set_run_order: The runOrder for the CodePipeline action creating the ChangeSet. Default: 1
        :param execute_change_set_action_name: The name of the CodePipeline action creating the ChangeSet. Default: 'Execute'
        :param execute_change_set_run_order: The runOrder for the CodePipeline action executing the ChangeSet. Default: ``createChangeSetRunOrder + 1``
        :param role: IAM role to assume when deploying changes. If not specified, a fresh role is created. The role is created with zero permissions unless ``adminPermissions`` is true, in which case the role will have admin permissions. Default: A fresh role with admin or no permissions (depending on the value of ``adminPermissions``).

        stability
        :stability: experimental
        """
        props = PipelineDeployStackActionProps(admin_permissions=admin_permissions, input=input, stack=stack, capabilities=capabilities, change_set_name=change_set_name, create_change_set_action_name=create_change_set_action_name, create_change_set_run_order=create_change_set_run_order, execute_change_set_action_name=execute_change_set_action_name, execute_change_set_run_order=execute_change_set_run_order, role=role)

        jsii.create(PipelineDeployStackAction, self, [props])

    @jsii.member(jsii_name="addToDeploymentRolePolicy")
    def add_to_deployment_role_policy(self, statement: _PolicyStatement_f75dc775) -> None:
        """Add policy statements to the role deploying the stack.

        This role is passed to CloudFormation and must have the IAM permissions
        necessary to deploy the stack or you can grant this role ``adminPermissions``
        by using that option during creation. If you do not grant
        ``adminPermissions`` you need to identify the proper statements to add to
        this role based on the CloudFormation Resources in your stack.

        :param statement: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToDeploymentRolePolicy", [statement])

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

    @builtins.property
    @jsii.member(jsii_name="actionProperties")
    def action_properties(self) -> _ActionProperties_8f5d7a9d:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "actionProperties")

    @builtins.property
    @jsii.member(jsii_name="deploymentRole")
    def deployment_role(self) -> _IRole_e69bbae4:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "deploymentRole")


@jsii.data_type(jsii_type="monocdk-experiment.app_delivery.PipelineDeployStackActionProps", jsii_struct_bases=[], name_mapping={'admin_permissions': 'adminPermissions', 'input': 'input', 'stack': 'stack', 'capabilities': 'capabilities', 'change_set_name': 'changeSetName', 'create_change_set_action_name': 'createChangeSetActionName', 'create_change_set_run_order': 'createChangeSetRunOrder', 'execute_change_set_action_name': 'executeChangeSetActionName', 'execute_change_set_run_order': 'executeChangeSetRunOrder', 'role': 'role'})
class PipelineDeployStackActionProps():
    def __init__(self, *, admin_permissions: bool, input: _Artifact_af6d98e9, stack: _Stack_05f4505a, capabilities: typing.Optional[typing.List[_CloudFormationCapabilities_979dd343]]=None, change_set_name: typing.Optional[str]=None, create_change_set_action_name: typing.Optional[str]=None, create_change_set_run_order: typing.Optional[jsii.Number]=None, execute_change_set_action_name: typing.Optional[str]=None, execute_change_set_run_order: typing.Optional[jsii.Number]=None, role: typing.Optional[_IRole_e69bbae4]=None) -> None:
        """
        :param admin_permissions: Whether to grant admin permissions to CloudFormation while deploying this template. Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you don't specify any alternatives. The default role that will be created for you will have admin (i.e., ``*``) permissions on all resources, and the deployment will have named IAM capabilities (i.e., able to create all IAM resources). This is a shorthand that you can use if you fully trust the templates that are deployed in this pipeline. If you want more fine-grained permissions, use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation deployment is allowed to do.
        :param input: The CodePipeline artifact that holds the synthesized app, which is the contents of the ``<directory>`` when running ``cdk synth -o <directory>``.
        :param stack: The CDK stack to be deployed.
        :param capabilities: Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation might create or update those resources. For example, you must specify AnonymousIAM if your stack template contains AWS Identity and Access Management (IAM) resources. For more information Default: [AnonymousIAM, AutoExpand], unless ``adminPermissions`` is true
        :param change_set_name: The name to use when creating a ChangeSet for the stack. Default: CDK-CodePipeline-ChangeSet
        :param create_change_set_action_name: The name of the CodePipeline action creating the ChangeSet. Default: 'ChangeSet'
        :param create_change_set_run_order: The runOrder for the CodePipeline action creating the ChangeSet. Default: 1
        :param execute_change_set_action_name: The name of the CodePipeline action creating the ChangeSet. Default: 'Execute'
        :param execute_change_set_run_order: The runOrder for the CodePipeline action executing the ChangeSet. Default: ``createChangeSetRunOrder + 1``
        :param role: IAM role to assume when deploying changes. If not specified, a fresh role is created. The role is created with zero permissions unless ``adminPermissions`` is true, in which case the role will have admin permissions. Default: A fresh role with admin or no permissions (depending on the value of ``adminPermissions``).

        stability
        :stability: experimental
        """
        self._values = {
            'admin_permissions': admin_permissions,
            'input': input,
            'stack': stack,
        }
        if capabilities is not None: self._values["capabilities"] = capabilities
        if change_set_name is not None: self._values["change_set_name"] = change_set_name
        if create_change_set_action_name is not None: self._values["create_change_set_action_name"] = create_change_set_action_name
        if create_change_set_run_order is not None: self._values["create_change_set_run_order"] = create_change_set_run_order
        if execute_change_set_action_name is not None: self._values["execute_change_set_action_name"] = execute_change_set_action_name
        if execute_change_set_run_order is not None: self._values["execute_change_set_run_order"] = execute_change_set_run_order
        if role is not None: self._values["role"] = role

    @builtins.property
    def admin_permissions(self) -> bool:
        """Whether to grant admin permissions to CloudFormation while deploying this template.

        Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you
        don't specify any alternatives.

        The default role that will be created for you will have admin (i.e., ``*``)
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
    def input(self) -> _Artifact_af6d98e9:
        """The CodePipeline artifact that holds the synthesized app, which is the contents of the ``<directory>`` when running ``cdk synth -o <directory>``.

        stability
        :stability: experimental
        """
        return self._values.get('input')

    @builtins.property
    def stack(self) -> _Stack_05f4505a:
        """The CDK stack to be deployed.

        stability
        :stability: experimental
        """
        return self._values.get('stack')

    @builtins.property
    def capabilities(self) -> typing.Optional[typing.List[_CloudFormationCapabilities_979dd343]]:
        """Acknowledge certain changes made as part of deployment.

        For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation
        might create or update those resources. For example, you must specify AnonymousIAM if your
        stack template contains AWS Identity and Access Management (IAM) resources. For more
        information

        default
        :default: [AnonymousIAM, AutoExpand], unless ``adminPermissions`` is true

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
        stability
        :stability: experimental
        """
        return self._values.get('capabilities')

    @builtins.property
    def change_set_name(self) -> typing.Optional[str]:
        """The name to use when creating a ChangeSet for the stack.

        default
        :default: CDK-CodePipeline-ChangeSet

        stability
        :stability: experimental
        """
        return self._values.get('change_set_name')

    @builtins.property
    def create_change_set_action_name(self) -> typing.Optional[str]:
        """The name of the CodePipeline action creating the ChangeSet.

        default
        :default: 'ChangeSet'

        stability
        :stability: experimental
        """
        return self._values.get('create_change_set_action_name')

    @builtins.property
    def create_change_set_run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder for the CodePipeline action creating the ChangeSet.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('create_change_set_run_order')

    @builtins.property
    def execute_change_set_action_name(self) -> typing.Optional[str]:
        """The name of the CodePipeline action creating the ChangeSet.

        default
        :default: 'Execute'

        stability
        :stability: experimental
        """
        return self._values.get('execute_change_set_action_name')

    @builtins.property
    def execute_change_set_run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder for the CodePipeline action executing the ChangeSet.

        default
        :default: ``createChangeSetRunOrder + 1``

        stability
        :stability: experimental
        """
        return self._values.get('execute_change_set_run_order')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """IAM role to assume when deploying changes.

        If not specified, a fresh role is created. The role is created with zero
        permissions unless ``adminPermissions`` is true, in which case the role will have
        admin permissions.

        default
        :default: A fresh role with admin or no permissions (depending on the value of ``adminPermissions``).

        stability
        :stability: experimental
        """
        return self._values.get('role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'PipelineDeployStackActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "PipelineDeployStackAction",
    "PipelineDeployStackActionProps",
]

publication.publish()
