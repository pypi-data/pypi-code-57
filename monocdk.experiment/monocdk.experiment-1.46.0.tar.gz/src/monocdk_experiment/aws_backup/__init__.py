import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (Resource as _Resource_884d0774, Construct as _Construct_f50a3f53, Duration as _Duration_5170c158, RemovalPolicy as _RemovalPolicy_5986e9f3, CfnResource as _CfnResource_7760e8e4, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, IResolvable as _IResolvable_9ceae33e, IInspectable as _IInspectable_051e6ed8, IResource as _IResource_72f7ee7e)
from ..aws_dynamodb import (ITable as _ITable_e6850701)
from ..aws_ec2 import (IInstance as _IInstance_cc0e4caa)
from ..aws_efs import (IFileSystem as _IFileSystem_552561fc)
from ..aws_events import (Schedule as _Schedule_11a70620)
from ..aws_iam import (IPrincipal as _IPrincipal_97126874, IGrantable as _IGrantable_0fcfc53a, IRole as _IRole_e69bbae4, PolicyDocument as _PolicyDocument_1d1bca11)
from ..aws_kms import (IKey as _IKey_3336c79d)
from ..aws_rds import (IDatabaseInstance as _IDatabaseInstance_67e1971d)
from ..aws_sns import (ITopic as _ITopic_ef0ebe0e)


@jsii.data_type(jsii_type="monocdk-experiment.aws_backup.BackupPlanProps", jsii_struct_bases=[], name_mapping={'backup_plan_name': 'backupPlanName', 'backup_plan_rules': 'backupPlanRules', 'backup_vault': 'backupVault'})
class BackupPlanProps():
    def __init__(self, *, backup_plan_name: typing.Optional[str]=None, backup_plan_rules: typing.Optional[typing.List["BackupPlanRule"]]=None, backup_vault: typing.Optional["IBackupVault"]=None) -> None:
        """Properties for a BackupPlan.

        :param backup_plan_name: The display name of the backup plan. Default: - A CDK generated name
        :param backup_plan_rules: Rules for the backup plan. Use ``addRule()`` to add rules after instantiation. Default: - use ``addRule()`` to add rules
        :param backup_vault: The backup vault where backups are stored. Default: - use the vault defined at the rule level. If not defined a new common vault for the plan will be created

        stability
        :stability: experimental
        """
        self._values = {
        }
        if backup_plan_name is not None: self._values["backup_plan_name"] = backup_plan_name
        if backup_plan_rules is not None: self._values["backup_plan_rules"] = backup_plan_rules
        if backup_vault is not None: self._values["backup_vault"] = backup_vault

    @builtins.property
    def backup_plan_name(self) -> typing.Optional[str]:
        """The display name of the backup plan.

        default
        :default: - A CDK generated name

        stability
        :stability: experimental
        """
        return self._values.get('backup_plan_name')

    @builtins.property
    def backup_plan_rules(self) -> typing.Optional[typing.List["BackupPlanRule"]]:
        """Rules for the backup plan.

        Use ``addRule()`` to add rules after
        instantiation.

        default
        :default: - use ``addRule()`` to add rules

        stability
        :stability: experimental
        """
        return self._values.get('backup_plan_rules')

    @builtins.property
    def backup_vault(self) -> typing.Optional["IBackupVault"]:
        """The backup vault where backups are stored.

        default
        :default:

        - use the vault defined at the rule level. If not defined a new
          common vault for the plan will be created

        stability
        :stability: experimental
        """
        return self._values.get('backup_vault')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BackupPlanProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class BackupPlanRule(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_backup.BackupPlanRule"):
    """A backup plan rule.

    stability
    :stability: experimental
    """
    def __init__(self, *, backup_vault: typing.Optional["IBackupVault"]=None, completion_window: typing.Optional[_Duration_5170c158]=None, delete_after: typing.Optional[_Duration_5170c158]=None, move_to_cold_storage_after: typing.Optional[_Duration_5170c158]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[_Schedule_11a70620]=None, start_window: typing.Optional[_Duration_5170c158]=None) -> None:
        """
        :param backup_vault: The backup vault where backups are. Default: - use the vault defined at the plan level. If not defined a new common vault for the plan will be created
        :param completion_window: The duration after a backup job is successfully started before it must be completed or it is canceled by AWS Backup. Default: - 8 hours
        :param delete_after: Specifies the duration after creation that a recovery point is deleted. Must be greater than ``moveToColdStorageAfter``. Default: - recovery point is never deleted
        :param move_to_cold_storage_after: Specifies the duration after creation that a recovery point is moved to cold storage. Default: - recovery point is never moved to cold storage
        :param rule_name: A display name for the backup rule. Default: - a CDK generated name
        :param schedule_expression: A CRON expression specifying when AWS Backup initiates a backup job. Default: - no schedule
        :param start_window: The duration after a backup is scheduled before a job is canceled if it doesn't start successfully. Default: - 8 hours

        stability
        :stability: experimental
        """
        props = BackupPlanRuleProps(backup_vault=backup_vault, completion_window=completion_window, delete_after=delete_after, move_to_cold_storage_after=move_to_cold_storage_after, rule_name=rule_name, schedule_expression=schedule_expression, start_window=start_window)

        jsii.create(BackupPlanRule, self, [props])

    @jsii.member(jsii_name="daily")
    @builtins.classmethod
    def daily(cls, backup_vault: typing.Optional["IBackupVault"]=None) -> "BackupPlanRule":
        """Daily with 35 days retention.

        :param backup_vault: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "daily", [backup_vault])

    @jsii.member(jsii_name="monthly1Year")
    @builtins.classmethod
    def monthly1_year(cls, backup_vault: typing.Optional["IBackupVault"]=None) -> "BackupPlanRule":
        """Monthly 1 year retention, move to cold storage after 1 month.

        :param backup_vault: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "monthly1Year", [backup_vault])

    @jsii.member(jsii_name="monthly5Year")
    @builtins.classmethod
    def monthly5_year(cls, backup_vault: typing.Optional["IBackupVault"]=None) -> "BackupPlanRule":
        """Monthly 5 year retention, move to cold storage after 3 months.

        :param backup_vault: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "monthly5Year", [backup_vault])

    @jsii.member(jsii_name="monthly7Year")
    @builtins.classmethod
    def monthly7_year(cls, backup_vault: typing.Optional["IBackupVault"]=None) -> "BackupPlanRule":
        """Monthly 7 year retention, move to cold storage after 3 months.

        :param backup_vault: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "monthly7Year", [backup_vault])

    @jsii.member(jsii_name="weekly")
    @builtins.classmethod
    def weekly(cls, backup_vault: typing.Optional["IBackupVault"]=None) -> "BackupPlanRule":
        """Weekly with 3 months retention.

        :param backup_vault: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "weekly", [backup_vault])

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "BackupPlanRuleProps":
        """Rule properties.

        stability
        :stability: experimental
        """
        return jsii.get(self, "props")


@jsii.data_type(jsii_type="monocdk-experiment.aws_backup.BackupPlanRuleProps", jsii_struct_bases=[], name_mapping={'backup_vault': 'backupVault', 'completion_window': 'completionWindow', 'delete_after': 'deleteAfter', 'move_to_cold_storage_after': 'moveToColdStorageAfter', 'rule_name': 'ruleName', 'schedule_expression': 'scheduleExpression', 'start_window': 'startWindow'})
class BackupPlanRuleProps():
    def __init__(self, *, backup_vault: typing.Optional["IBackupVault"]=None, completion_window: typing.Optional[_Duration_5170c158]=None, delete_after: typing.Optional[_Duration_5170c158]=None, move_to_cold_storage_after: typing.Optional[_Duration_5170c158]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[_Schedule_11a70620]=None, start_window: typing.Optional[_Duration_5170c158]=None) -> None:
        """Properties for a BackupPlanRule.

        :param backup_vault: The backup vault where backups are. Default: - use the vault defined at the plan level. If not defined a new common vault for the plan will be created
        :param completion_window: The duration after a backup job is successfully started before it must be completed or it is canceled by AWS Backup. Default: - 8 hours
        :param delete_after: Specifies the duration after creation that a recovery point is deleted. Must be greater than ``moveToColdStorageAfter``. Default: - recovery point is never deleted
        :param move_to_cold_storage_after: Specifies the duration after creation that a recovery point is moved to cold storage. Default: - recovery point is never moved to cold storage
        :param rule_name: A display name for the backup rule. Default: - a CDK generated name
        :param schedule_expression: A CRON expression specifying when AWS Backup initiates a backup job. Default: - no schedule
        :param start_window: The duration after a backup is scheduled before a job is canceled if it doesn't start successfully. Default: - 8 hours

        stability
        :stability: experimental
        """
        self._values = {
        }
        if backup_vault is not None: self._values["backup_vault"] = backup_vault
        if completion_window is not None: self._values["completion_window"] = completion_window
        if delete_after is not None: self._values["delete_after"] = delete_after
        if move_to_cold_storage_after is not None: self._values["move_to_cold_storage_after"] = move_to_cold_storage_after
        if rule_name is not None: self._values["rule_name"] = rule_name
        if schedule_expression is not None: self._values["schedule_expression"] = schedule_expression
        if start_window is not None: self._values["start_window"] = start_window

    @builtins.property
    def backup_vault(self) -> typing.Optional["IBackupVault"]:
        """The backup vault where backups are.

        default
        :default:

        - use the vault defined at the plan level. If not defined a new
          common vault for the plan will be created

        stability
        :stability: experimental
        """
        return self._values.get('backup_vault')

    @builtins.property
    def completion_window(self) -> typing.Optional[_Duration_5170c158]:
        """The duration after a backup job is successfully started before it must be completed or it is canceled by AWS Backup.

        default
        :default: - 8 hours

        stability
        :stability: experimental
        """
        return self._values.get('completion_window')

    @builtins.property
    def delete_after(self) -> typing.Optional[_Duration_5170c158]:
        """Specifies the duration after creation that a recovery point is deleted.

        Must be greater than ``moveToColdStorageAfter``.

        default
        :default: - recovery point is never deleted

        stability
        :stability: experimental
        """
        return self._values.get('delete_after')

    @builtins.property
    def move_to_cold_storage_after(self) -> typing.Optional[_Duration_5170c158]:
        """Specifies the duration after creation that a recovery point is moved to cold storage.

        default
        :default: - recovery point is never moved to cold storage

        stability
        :stability: experimental
        """
        return self._values.get('move_to_cold_storage_after')

    @builtins.property
    def rule_name(self) -> typing.Optional[str]:
        """A display name for the backup rule.

        default
        :default: - a CDK generated name

        stability
        :stability: experimental
        """
        return self._values.get('rule_name')

    @builtins.property
    def schedule_expression(self) -> typing.Optional[_Schedule_11a70620]:
        """A CRON expression specifying when AWS Backup initiates a backup job.

        default
        :default: - no schedule

        stability
        :stability: experimental
        """
        return self._values.get('schedule_expression')

    @builtins.property
    def start_window(self) -> typing.Optional[_Duration_5170c158]:
        """The duration after a backup is scheduled before a job is canceled if it doesn't start successfully.

        default
        :default: - 8 hours

        stability
        :stability: experimental
        """
        return self._values.get('start_window')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BackupPlanRuleProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class BackupResource(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_backup.BackupResource"):
    """A resource to backup.

    stability
    :stability: experimental
    """
    def __init__(self, resource: typing.Optional[str]=None, tag_condition: typing.Optional["TagCondition"]=None, construct: typing.Optional[_Construct_f50a3f53]=None) -> None:
        """
        :param resource: -
        :param tag_condition: -
        :param construct: -

        stability
        :stability: experimental
        """
        jsii.create(BackupResource, self, [resource, tag_condition, construct])

    @jsii.member(jsii_name="fromArn")
    @builtins.classmethod
    def from_arn(cls, arn: str) -> "BackupResource":
        """A list of ARNs or match patterns such as ``arn:aws:ec2:us-east-1:123456789012:volume/*``.

        :param arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromArn", [arn])

    @jsii.member(jsii_name="fromConstruct")
    @builtins.classmethod
    def from_construct(cls, construct: _Construct_f50a3f53) -> "BackupResource":
        """Adds all supported resources in a construct.

        :param construct: The construct containing resources to backup.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromConstruct", [construct])

    @jsii.member(jsii_name="fromDynamoDbTable")
    @builtins.classmethod
    def from_dynamo_db_table(cls, table: _ITable_e6850701) -> "BackupResource":
        """A DynamoDB table.

        :param table: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromDynamoDbTable", [table])

    @jsii.member(jsii_name="fromEc2Instance")
    @builtins.classmethod
    def from_ec2_instance(cls, instance: _IInstance_cc0e4caa) -> "BackupResource":
        """An EC2 instance.

        :param instance: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromEc2Instance", [instance])

    @jsii.member(jsii_name="fromEfsFileSystem")
    @builtins.classmethod
    def from_efs_file_system(cls, file_system: _IFileSystem_552561fc) -> "BackupResource":
        """An EFS file system.

        :param file_system: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromEfsFileSystem", [file_system])

    @jsii.member(jsii_name="fromRdsDatabaseInstance")
    @builtins.classmethod
    def from_rds_database_instance(cls, instance: _IDatabaseInstance_67e1971d) -> "BackupResource":
        """A RDS database instance.

        :param instance: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromRdsDatabaseInstance", [instance])

    @jsii.member(jsii_name="fromTag")
    @builtins.classmethod
    def from_tag(cls, key: str, value: str, operation: typing.Optional["TagOperation"]=None) -> "BackupResource":
        """A tag condition.

        :param key: -
        :param value: -
        :param operation: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromTag", [key, value, operation])

    @builtins.property
    @jsii.member(jsii_name="construct")
    def construct(self) -> typing.Optional[_Construct_f50a3f53]:
        """A construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "construct")

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> typing.Optional[str]:
        """A resource.

        stability
        :stability: experimental
        """
        return jsii.get(self, "resource")

    @builtins.property
    @jsii.member(jsii_name="tagCondition")
    def tag_condition(self) -> typing.Optional["TagCondition"]:
        """A condition on a tag.

        stability
        :stability: experimental
        """
        return jsii.get(self, "tagCondition")


@jsii.implements(_IGrantable_0fcfc53a)
class BackupSelection(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_backup.BackupSelection"):
    """A backup selection.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, backup_plan: "IBackupPlan", resources: typing.List["BackupResource"], allow_restores: typing.Optional[bool]=None, backup_selection_name: typing.Optional[str]=None, role: typing.Optional[_IRole_e69bbae4]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param backup_plan: The backup plan for this selection.
        :param resources: The resources to backup. Use the helper static methods defined on ``BackupResource``.
        :param allow_restores: Whether to automatically give restores permissions to the role that AWS Backup uses. If ``true``, the ``AWSBackupServiceRolePolicyForRestores`` managed policy will be attached to the role. Default: false
        :param backup_selection_name: The name for this selection. Default: - a CDK generated name
        :param role: The role that AWS Backup uses to authenticate when backuping or restoring the resources. The ``AWSBackupServiceRolePolicyForBackup`` managed policy will be attached to this role. Default: - a new role will be created

        stability
        :stability: experimental
        """
        props = BackupSelectionProps(backup_plan=backup_plan, resources=resources, allow_restores=allow_restores, backup_selection_name=backup_selection_name, role=role)

        jsii.create(BackupSelection, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="backupPlanId")
    def backup_plan_id(self) -> str:
        """The identifier of the backup plan.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "backupPlanId")

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _IPrincipal_97126874:
        """The principal to grant permissions to.

        stability
        :stability: experimental
        """
        return jsii.get(self, "grantPrincipal")

    @builtins.property
    @jsii.member(jsii_name="selectionId")
    def selection_id(self) -> str:
        """The identifier of the backup selection.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "selectionId")


@jsii.data_type(jsii_type="monocdk-experiment.aws_backup.BackupSelectionOptions", jsii_struct_bases=[], name_mapping={'resources': 'resources', 'allow_restores': 'allowRestores', 'backup_selection_name': 'backupSelectionName', 'role': 'role'})
class BackupSelectionOptions():
    def __init__(self, *, resources: typing.List["BackupResource"], allow_restores: typing.Optional[bool]=None, backup_selection_name: typing.Optional[str]=None, role: typing.Optional[_IRole_e69bbae4]=None) -> None:
        """Options for a BackupSelection.

        :param resources: The resources to backup. Use the helper static methods defined on ``BackupResource``.
        :param allow_restores: Whether to automatically give restores permissions to the role that AWS Backup uses. If ``true``, the ``AWSBackupServiceRolePolicyForRestores`` managed policy will be attached to the role. Default: false
        :param backup_selection_name: The name for this selection. Default: - a CDK generated name
        :param role: The role that AWS Backup uses to authenticate when backuping or restoring the resources. The ``AWSBackupServiceRolePolicyForBackup`` managed policy will be attached to this role. Default: - a new role will be created

        stability
        :stability: experimental
        """
        self._values = {
            'resources': resources,
        }
        if allow_restores is not None: self._values["allow_restores"] = allow_restores
        if backup_selection_name is not None: self._values["backup_selection_name"] = backup_selection_name
        if role is not None: self._values["role"] = role

    @builtins.property
    def resources(self) -> typing.List["BackupResource"]:
        """The resources to backup.

        Use the helper static methods defined on ``BackupResource``.

        stability
        :stability: experimental
        """
        return self._values.get('resources')

    @builtins.property
    def allow_restores(self) -> typing.Optional[bool]:
        """Whether to automatically give restores permissions to the role that AWS Backup uses.

        If ``true``, the ``AWSBackupServiceRolePolicyForRestores`` managed
        policy will be attached to the role.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('allow_restores')

    @builtins.property
    def backup_selection_name(self) -> typing.Optional[str]:
        """The name for this selection.

        default
        :default: - a CDK generated name

        stability
        :stability: experimental
        """
        return self._values.get('backup_selection_name')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The role that AWS Backup uses to authenticate when backuping or restoring the resources.

        The ``AWSBackupServiceRolePolicyForBackup`` managed policy
        will be attached to this role.

        default
        :default: - a new role will be created

        stability
        :stability: experimental
        """
        return self._values.get('role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BackupSelectionOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_backup.BackupSelectionProps", jsii_struct_bases=[BackupSelectionOptions], name_mapping={'resources': 'resources', 'allow_restores': 'allowRestores', 'backup_selection_name': 'backupSelectionName', 'role': 'role', 'backup_plan': 'backupPlan'})
class BackupSelectionProps(BackupSelectionOptions):
    def __init__(self, *, resources: typing.List["BackupResource"], allow_restores: typing.Optional[bool]=None, backup_selection_name: typing.Optional[str]=None, role: typing.Optional[_IRole_e69bbae4]=None, backup_plan: "IBackupPlan") -> None:
        """Properties for a BackupSelection.

        :param resources: The resources to backup. Use the helper static methods defined on ``BackupResource``.
        :param allow_restores: Whether to automatically give restores permissions to the role that AWS Backup uses. If ``true``, the ``AWSBackupServiceRolePolicyForRestores`` managed policy will be attached to the role. Default: false
        :param backup_selection_name: The name for this selection. Default: - a CDK generated name
        :param role: The role that AWS Backup uses to authenticate when backuping or restoring the resources. The ``AWSBackupServiceRolePolicyForBackup`` managed policy will be attached to this role. Default: - a new role will be created
        :param backup_plan: The backup plan for this selection.

        stability
        :stability: experimental
        """
        self._values = {
            'resources': resources,
            'backup_plan': backup_plan,
        }
        if allow_restores is not None: self._values["allow_restores"] = allow_restores
        if backup_selection_name is not None: self._values["backup_selection_name"] = backup_selection_name
        if role is not None: self._values["role"] = role

    @builtins.property
    def resources(self) -> typing.List["BackupResource"]:
        """The resources to backup.

        Use the helper static methods defined on ``BackupResource``.

        stability
        :stability: experimental
        """
        return self._values.get('resources')

    @builtins.property
    def allow_restores(self) -> typing.Optional[bool]:
        """Whether to automatically give restores permissions to the role that AWS Backup uses.

        If ``true``, the ``AWSBackupServiceRolePolicyForRestores`` managed
        policy will be attached to the role.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('allow_restores')

    @builtins.property
    def backup_selection_name(self) -> typing.Optional[str]:
        """The name for this selection.

        default
        :default: - a CDK generated name

        stability
        :stability: experimental
        """
        return self._values.get('backup_selection_name')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The role that AWS Backup uses to authenticate when backuping or restoring the resources.

        The ``AWSBackupServiceRolePolicyForBackup`` managed policy
        will be attached to this role.

        default
        :default: - a new role will be created

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def backup_plan(self) -> "IBackupPlan":
        """The backup plan for this selection.

        stability
        :stability: experimental
        """
        return self._values.get('backup_plan')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BackupSelectionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_backup.BackupVaultEvents")
class BackupVaultEvents(enum.Enum):
    """Backup vault events.

    stability
    :stability: experimental
    """
    BACKUP_JOB_STARTED = "BACKUP_JOB_STARTED"
    """BACKUP_JOB_STARTED.

    stability
    :stability: experimental
    """
    BACKUP_JOB_COMPLETED = "BACKUP_JOB_COMPLETED"
    """BACKUP_JOB_COMPLETED.

    stability
    :stability: experimental
    """
    BACKUP_JOB_SUCCESSFUL = "BACKUP_JOB_SUCCESSFUL"
    """BACKUP_JOB_SUCCESSFUL.

    stability
    :stability: experimental
    """
    BACKUP_JOB_FAILED = "BACKUP_JOB_FAILED"
    """BACKUP_JOB_FAILED.

    stability
    :stability: experimental
    """
    BACKUP_JOB_EXPIRED = "BACKUP_JOB_EXPIRED"
    """BACKUP_JOB_EXPIRED.

    stability
    :stability: experimental
    """
    RESTORE_JOB_STARTED = "RESTORE_JOB_STARTED"
    """RESTORE_JOB_STARTED.

    stability
    :stability: experimental
    """
    RESTORE_JOB_COMPLETED = "RESTORE_JOB_COMPLETED"
    """RESTORE_JOB_COMPLETED.

    stability
    :stability: experimental
    """
    RESTORE_JOB_SUCCESSFUL = "RESTORE_JOB_SUCCESSFUL"
    """RESTORE_JOB_SUCCESSFUL.

    stability
    :stability: experimental
    """
    RESTORE_JOB_FAILED = "RESTORE_JOB_FAILED"
    """RESTORE_JOB_FAILED.

    stability
    :stability: experimental
    """
    COPY_JOB_STARTED = "COPY_JOB_STARTED"
    """COPY_JOB_STARTED.

    stability
    :stability: experimental
    """
    COPY_JOB_SUCCESSFUL = "COPY_JOB_SUCCESSFUL"
    """COPY_JOB_SUCCESSFUL.

    stability
    :stability: experimental
    """
    COPY_JOB_FAILED = "COPY_JOB_FAILED"
    """COPY_JOB_FAILED.

    stability
    :stability: experimental
    """
    RECOVERY_POINT_MODIFIED = "RECOVERY_POINT_MODIFIED"
    """RECOVERY_POINT_MODIFIED.

    stability
    :stability: experimental
    """
    BACKUP_PLAN_CREATED = "BACKUP_PLAN_CREATED"
    """BACKUP_PLAN_CREATED.

    stability
    :stability: experimental
    """
    BACKUP_PLAN_MODIFIED = "BACKUP_PLAN_MODIFIED"
    """BACKUP_PLAN_MODIFIED.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.aws_backup.BackupVaultProps", jsii_struct_bases=[], name_mapping={'access_policy': 'accessPolicy', 'backup_vault_name': 'backupVaultName', 'encryption_key': 'encryptionKey', 'notification_events': 'notificationEvents', 'notification_topic': 'notificationTopic', 'removal_policy': 'removalPolicy'})
class BackupVaultProps():
    def __init__(self, *, access_policy: typing.Optional[_PolicyDocument_1d1bca11]=None, backup_vault_name: typing.Optional[str]=None, encryption_key: typing.Optional[_IKey_3336c79d]=None, notification_events: typing.Optional[typing.List["BackupVaultEvents"]]=None, notification_topic: typing.Optional[_ITopic_ef0ebe0e]=None, removal_policy: typing.Optional[_RemovalPolicy_5986e9f3]=None) -> None:
        """Properties for a BackupVault.

        :param access_policy: A resource-based policy that is used to manage access permissions on the backup vault. Default: - access is not restricted
        :param backup_vault_name: The name of a logical container where backups are stored. Default: - A CDK generated name
        :param encryption_key: The server-side encryption key to use to protect your backups. Default: - an Amazon managed KMS key
        :param notification_events: The vault events to send. Default: - all vault events if ``notificationTopic`` is defined
        :param notification_topic: A SNS topic to send vault events to. Default: - no notifications
        :param removal_policy: The removal policy to apply to the vault. Note that removing a vault that contains recovery points will fail. Default: RemovalPolicy.RETAIN

        stability
        :stability: experimental
        """
        self._values = {
        }
        if access_policy is not None: self._values["access_policy"] = access_policy
        if backup_vault_name is not None: self._values["backup_vault_name"] = backup_vault_name
        if encryption_key is not None: self._values["encryption_key"] = encryption_key
        if notification_events is not None: self._values["notification_events"] = notification_events
        if notification_topic is not None: self._values["notification_topic"] = notification_topic
        if removal_policy is not None: self._values["removal_policy"] = removal_policy

    @builtins.property
    def access_policy(self) -> typing.Optional[_PolicyDocument_1d1bca11]:
        """A resource-based policy that is used to manage access permissions on the backup vault.

        default
        :default: - access is not restricted

        stability
        :stability: experimental
        """
        return self._values.get('access_policy')

    @builtins.property
    def backup_vault_name(self) -> typing.Optional[str]:
        """The name of a logical container where backups are stored.

        default
        :default: - A CDK generated name

        stability
        :stability: experimental
        """
        return self._values.get('backup_vault_name')

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The server-side encryption key to use to protect your backups.

        default
        :default: - an Amazon managed KMS key

        stability
        :stability: experimental
        """
        return self._values.get('encryption_key')

    @builtins.property
    def notification_events(self) -> typing.Optional[typing.List["BackupVaultEvents"]]:
        """The vault events to send.

        default
        :default: - all vault events if ``notificationTopic`` is defined

        see
        :see: https://docs.aws.amazon.com/aws-backup/latest/devguide/sns-notifications.html
        stability
        :stability: experimental
        """
        return self._values.get('notification_events')

    @builtins.property
    def notification_topic(self) -> typing.Optional[_ITopic_ef0ebe0e]:
        """A SNS topic to send vault events to.

        default
        :default: - no notifications

        see
        :see: https://docs.aws.amazon.com/aws-backup/latest/devguide/sns-notifications.html
        stability
        :stability: experimental
        """
        return self._values.get('notification_topic')

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_5986e9f3]:
        """The removal policy to apply to the vault.

        Note that removing a vault
        that contains recovery points will fail.

        default
        :default: RemovalPolicy.RETAIN

        stability
        :stability: experimental
        """
        return self._values.get('removal_policy')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BackupVaultProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnBackupPlan(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_backup.CfnBackupPlan"):
    """A CloudFormation ``AWS::Backup::BackupPlan``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupplan.html
    cloudformationResource:
    :cloudformationResource:: AWS::Backup::BackupPlan
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, backup_plan: typing.Union["BackupPlanResourceTypeProperty", _IResolvable_9ceae33e], backup_plan_tags: typing.Any=None) -> None:
        """Create a new ``AWS::Backup::BackupPlan``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param backup_plan: ``AWS::Backup::BackupPlan.BackupPlan``.
        :param backup_plan_tags: ``AWS::Backup::BackupPlan.BackupPlanTags``.
        """
        props = CfnBackupPlanProps(backup_plan=backup_plan, backup_plan_tags=backup_plan_tags)

        jsii.create(CfnBackupPlan, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnBackupPlan":
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
    @jsii.member(jsii_name="attrBackupPlanArn")
    def attr_backup_plan_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: BackupPlanArn
        """
        return jsii.get(self, "attrBackupPlanArn")

    @builtins.property
    @jsii.member(jsii_name="attrBackupPlanId")
    def attr_backup_plan_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: BackupPlanId
        """
        return jsii.get(self, "attrBackupPlanId")

    @builtins.property
    @jsii.member(jsii_name="attrVersionId")
    def attr_version_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: VersionId
        """
        return jsii.get(self, "attrVersionId")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="backupPlan")
    def backup_plan(self) -> typing.Union["BackupPlanResourceTypeProperty", _IResolvable_9ceae33e]:
        """``AWS::Backup::BackupPlan.BackupPlan``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupplan.html#cfn-backup-backupplan-backupplan
        """
        return jsii.get(self, "backupPlan")

    @backup_plan.setter
    def backup_plan(self, value: typing.Union["BackupPlanResourceTypeProperty", _IResolvable_9ceae33e]) -> None:
        jsii.set(self, "backupPlan", value)

    @builtins.property
    @jsii.member(jsii_name="backupPlanTags")
    def backup_plan_tags(self) -> typing.Any:
        """``AWS::Backup::BackupPlan.BackupPlanTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupplan.html#cfn-backup-backupplan-backupplantags
        """
        return jsii.get(self, "backupPlanTags")

    @backup_plan_tags.setter
    def backup_plan_tags(self, value: typing.Any) -> None:
        jsii.set(self, "backupPlanTags", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_backup.CfnBackupPlan.BackupPlanResourceTypeProperty", jsii_struct_bases=[], name_mapping={'backup_plan_name': 'backupPlanName', 'backup_plan_rule': 'backupPlanRule'})
    class BackupPlanResourceTypeProperty():
        def __init__(self, *, backup_plan_name: str, backup_plan_rule: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnBackupPlan.BackupRuleResourceTypeProperty", _IResolvable_9ceae33e]]]) -> None:
            """
            :param backup_plan_name: ``CfnBackupPlan.BackupPlanResourceTypeProperty.BackupPlanName``.
            :param backup_plan_rule: ``CfnBackupPlan.BackupPlanResourceTypeProperty.BackupPlanRule``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupplanresourcetype.html
            """
            self._values = {
                'backup_plan_name': backup_plan_name,
                'backup_plan_rule': backup_plan_rule,
            }

        @builtins.property
        def backup_plan_name(self) -> str:
            """``CfnBackupPlan.BackupPlanResourceTypeProperty.BackupPlanName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupplanresourcetype.html#cfn-backup-backupplan-backupplanresourcetype-backupplanname
            """
            return self._values.get('backup_plan_name')

        @builtins.property
        def backup_plan_rule(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnBackupPlan.BackupRuleResourceTypeProperty", _IResolvable_9ceae33e]]]:
            """``CfnBackupPlan.BackupPlanResourceTypeProperty.BackupPlanRule``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupplanresourcetype.html#cfn-backup-backupplan-backupplanresourcetype-backupplanrule
            """
            return self._values.get('backup_plan_rule')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'BackupPlanResourceTypeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_backup.CfnBackupPlan.BackupRuleResourceTypeProperty", jsii_struct_bases=[], name_mapping={'rule_name': 'ruleName', 'target_backup_vault': 'targetBackupVault', 'completion_window_minutes': 'completionWindowMinutes', 'copy_actions': 'copyActions', 'lifecycle': 'lifecycle', 'recovery_point_tags': 'recoveryPointTags', 'schedule_expression': 'scheduleExpression', 'start_window_minutes': 'startWindowMinutes'})
    class BackupRuleResourceTypeProperty():
        def __init__(self, *, rule_name: str, target_backup_vault: str, completion_window_minutes: typing.Optional[jsii.Number]=None, copy_actions: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnBackupPlan.CopyActionResourceTypeProperty", _IResolvable_9ceae33e]]]]=None, lifecycle: typing.Optional[typing.Union["CfnBackupPlan.LifecycleResourceTypeProperty", _IResolvable_9ceae33e]]=None, recovery_point_tags: typing.Any=None, schedule_expression: typing.Optional[str]=None, start_window_minutes: typing.Optional[jsii.Number]=None) -> None:
            """
            :param rule_name: ``CfnBackupPlan.BackupRuleResourceTypeProperty.RuleName``.
            :param target_backup_vault: ``CfnBackupPlan.BackupRuleResourceTypeProperty.TargetBackupVault``.
            :param completion_window_minutes: ``CfnBackupPlan.BackupRuleResourceTypeProperty.CompletionWindowMinutes``.
            :param copy_actions: ``CfnBackupPlan.BackupRuleResourceTypeProperty.CopyActions``.
            :param lifecycle: ``CfnBackupPlan.BackupRuleResourceTypeProperty.Lifecycle``.
            :param recovery_point_tags: ``CfnBackupPlan.BackupRuleResourceTypeProperty.RecoveryPointTags``.
            :param schedule_expression: ``CfnBackupPlan.BackupRuleResourceTypeProperty.ScheduleExpression``.
            :param start_window_minutes: ``CfnBackupPlan.BackupRuleResourceTypeProperty.StartWindowMinutes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html
            """
            self._values = {
                'rule_name': rule_name,
                'target_backup_vault': target_backup_vault,
            }
            if completion_window_minutes is not None: self._values["completion_window_minutes"] = completion_window_minutes
            if copy_actions is not None: self._values["copy_actions"] = copy_actions
            if lifecycle is not None: self._values["lifecycle"] = lifecycle
            if recovery_point_tags is not None: self._values["recovery_point_tags"] = recovery_point_tags
            if schedule_expression is not None: self._values["schedule_expression"] = schedule_expression
            if start_window_minutes is not None: self._values["start_window_minutes"] = start_window_minutes

        @builtins.property
        def rule_name(self) -> str:
            """``CfnBackupPlan.BackupRuleResourceTypeProperty.RuleName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-rulename
            """
            return self._values.get('rule_name')

        @builtins.property
        def target_backup_vault(self) -> str:
            """``CfnBackupPlan.BackupRuleResourceTypeProperty.TargetBackupVault``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-targetbackupvault
            """
            return self._values.get('target_backup_vault')

        @builtins.property
        def completion_window_minutes(self) -> typing.Optional[jsii.Number]:
            """``CfnBackupPlan.BackupRuleResourceTypeProperty.CompletionWindowMinutes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-completionwindowminutes
            """
            return self._values.get('completion_window_minutes')

        @builtins.property
        def copy_actions(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnBackupPlan.CopyActionResourceTypeProperty", _IResolvable_9ceae33e]]]]:
            """``CfnBackupPlan.BackupRuleResourceTypeProperty.CopyActions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-copyactions
            """
            return self._values.get('copy_actions')

        @builtins.property
        def lifecycle(self) -> typing.Optional[typing.Union["CfnBackupPlan.LifecycleResourceTypeProperty", _IResolvable_9ceae33e]]:
            """``CfnBackupPlan.BackupRuleResourceTypeProperty.Lifecycle``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-lifecycle
            """
            return self._values.get('lifecycle')

        @builtins.property
        def recovery_point_tags(self) -> typing.Any:
            """``CfnBackupPlan.BackupRuleResourceTypeProperty.RecoveryPointTags``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-recoverypointtags
            """
            return self._values.get('recovery_point_tags')

        @builtins.property
        def schedule_expression(self) -> typing.Optional[str]:
            """``CfnBackupPlan.BackupRuleResourceTypeProperty.ScheduleExpression``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-scheduleexpression
            """
            return self._values.get('schedule_expression')

        @builtins.property
        def start_window_minutes(self) -> typing.Optional[jsii.Number]:
            """``CfnBackupPlan.BackupRuleResourceTypeProperty.StartWindowMinutes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-startwindowminutes
            """
            return self._values.get('start_window_minutes')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'BackupRuleResourceTypeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_backup.CfnBackupPlan.CopyActionResourceTypeProperty", jsii_struct_bases=[], name_mapping={'destination_backup_vault_arn': 'destinationBackupVaultArn', 'lifecycle': 'lifecycle'})
    class CopyActionResourceTypeProperty():
        def __init__(self, *, destination_backup_vault_arn: str, lifecycle: typing.Optional[typing.Union["CfnBackupPlan.LifecycleResourceTypeProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param destination_backup_vault_arn: ``CfnBackupPlan.CopyActionResourceTypeProperty.DestinationBackupVaultArn``.
            :param lifecycle: ``CfnBackupPlan.CopyActionResourceTypeProperty.Lifecycle``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-copyactionresourcetype.html
            """
            self._values = {
                'destination_backup_vault_arn': destination_backup_vault_arn,
            }
            if lifecycle is not None: self._values["lifecycle"] = lifecycle

        @builtins.property
        def destination_backup_vault_arn(self) -> str:
            """``CfnBackupPlan.CopyActionResourceTypeProperty.DestinationBackupVaultArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-copyactionresourcetype.html#cfn-backup-backupplan-copyactionresourcetype-destinationbackupvaultarn
            """
            return self._values.get('destination_backup_vault_arn')

        @builtins.property
        def lifecycle(self) -> typing.Optional[typing.Union["CfnBackupPlan.LifecycleResourceTypeProperty", _IResolvable_9ceae33e]]:
            """``CfnBackupPlan.CopyActionResourceTypeProperty.Lifecycle``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-copyactionresourcetype.html#cfn-backup-backupplan-copyactionresourcetype-lifecycle
            """
            return self._values.get('lifecycle')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CopyActionResourceTypeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_backup.CfnBackupPlan.LifecycleResourceTypeProperty", jsii_struct_bases=[], name_mapping={'delete_after_days': 'deleteAfterDays', 'move_to_cold_storage_after_days': 'moveToColdStorageAfterDays'})
    class LifecycleResourceTypeProperty():
        def __init__(self, *, delete_after_days: typing.Optional[jsii.Number]=None, move_to_cold_storage_after_days: typing.Optional[jsii.Number]=None) -> None:
            """
            :param delete_after_days: ``CfnBackupPlan.LifecycleResourceTypeProperty.DeleteAfterDays``.
            :param move_to_cold_storage_after_days: ``CfnBackupPlan.LifecycleResourceTypeProperty.MoveToColdStorageAfterDays``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-lifecycleresourcetype.html
            """
            self._values = {
            }
            if delete_after_days is not None: self._values["delete_after_days"] = delete_after_days
            if move_to_cold_storage_after_days is not None: self._values["move_to_cold_storage_after_days"] = move_to_cold_storage_after_days

        @builtins.property
        def delete_after_days(self) -> typing.Optional[jsii.Number]:
            """``CfnBackupPlan.LifecycleResourceTypeProperty.DeleteAfterDays``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-lifecycleresourcetype.html#cfn-backup-backupplan-lifecycleresourcetype-deleteafterdays
            """
            return self._values.get('delete_after_days')

        @builtins.property
        def move_to_cold_storage_after_days(self) -> typing.Optional[jsii.Number]:
            """``CfnBackupPlan.LifecycleResourceTypeProperty.MoveToColdStorageAfterDays``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-lifecycleresourcetype.html#cfn-backup-backupplan-lifecycleresourcetype-movetocoldstorageafterdays
            """
            return self._values.get('move_to_cold_storage_after_days')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LifecycleResourceTypeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_backup.CfnBackupPlanProps", jsii_struct_bases=[], name_mapping={'backup_plan': 'backupPlan', 'backup_plan_tags': 'backupPlanTags'})
class CfnBackupPlanProps():
    def __init__(self, *, backup_plan: typing.Union["CfnBackupPlan.BackupPlanResourceTypeProperty", _IResolvable_9ceae33e], backup_plan_tags: typing.Any=None) -> None:
        """Properties for defining a ``AWS::Backup::BackupPlan``.

        :param backup_plan: ``AWS::Backup::BackupPlan.BackupPlan``.
        :param backup_plan_tags: ``AWS::Backup::BackupPlan.BackupPlanTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupplan.html
        """
        self._values = {
            'backup_plan': backup_plan,
        }
        if backup_plan_tags is not None: self._values["backup_plan_tags"] = backup_plan_tags

    @builtins.property
    def backup_plan(self) -> typing.Union["CfnBackupPlan.BackupPlanResourceTypeProperty", _IResolvable_9ceae33e]:
        """``AWS::Backup::BackupPlan.BackupPlan``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupplan.html#cfn-backup-backupplan-backupplan
        """
        return self._values.get('backup_plan')

    @builtins.property
    def backup_plan_tags(self) -> typing.Any:
        """``AWS::Backup::BackupPlan.BackupPlanTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupplan.html#cfn-backup-backupplan-backupplantags
        """
        return self._values.get('backup_plan_tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnBackupPlanProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnBackupSelection(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_backup.CfnBackupSelection"):
    """A CloudFormation ``AWS::Backup::BackupSelection``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupselection.html
    cloudformationResource:
    :cloudformationResource:: AWS::Backup::BackupSelection
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, backup_plan_id: str, backup_selection: typing.Union["BackupSelectionResourceTypeProperty", _IResolvable_9ceae33e]) -> None:
        """Create a new ``AWS::Backup::BackupSelection``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param backup_plan_id: ``AWS::Backup::BackupSelection.BackupPlanId``.
        :param backup_selection: ``AWS::Backup::BackupSelection.BackupSelection``.
        """
        props = CfnBackupSelectionProps(backup_plan_id=backup_plan_id, backup_selection=backup_selection)

        jsii.create(CfnBackupSelection, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnBackupSelection":
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
    @jsii.member(jsii_name="attrBackupPlanId")
    def attr_backup_plan_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: BackupPlanId
        """
        return jsii.get(self, "attrBackupPlanId")

    @builtins.property
    @jsii.member(jsii_name="attrSelectionId")
    def attr_selection_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: SelectionId
        """
        return jsii.get(self, "attrSelectionId")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="backupPlanId")
    def backup_plan_id(self) -> str:
        """``AWS::Backup::BackupSelection.BackupPlanId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupselection.html#cfn-backup-backupselection-backupplanid
        """
        return jsii.get(self, "backupPlanId")

    @backup_plan_id.setter
    def backup_plan_id(self, value: str) -> None:
        jsii.set(self, "backupPlanId", value)

    @builtins.property
    @jsii.member(jsii_name="backupSelection")
    def backup_selection(self) -> typing.Union["BackupSelectionResourceTypeProperty", _IResolvable_9ceae33e]:
        """``AWS::Backup::BackupSelection.BackupSelection``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupselection.html#cfn-backup-backupselection-backupselection
        """
        return jsii.get(self, "backupSelection")

    @backup_selection.setter
    def backup_selection(self, value: typing.Union["BackupSelectionResourceTypeProperty", _IResolvable_9ceae33e]) -> None:
        jsii.set(self, "backupSelection", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_backup.CfnBackupSelection.BackupSelectionResourceTypeProperty", jsii_struct_bases=[], name_mapping={'iam_role_arn': 'iamRoleArn', 'selection_name': 'selectionName', 'list_of_tags': 'listOfTags', 'resources': 'resources'})
    class BackupSelectionResourceTypeProperty():
        def __init__(self, *, iam_role_arn: str, selection_name: str, list_of_tags: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnBackupSelection.ConditionResourceTypeProperty", _IResolvable_9ceae33e]]]]=None, resources: typing.Optional[typing.List[str]]=None) -> None:
            """
            :param iam_role_arn: ``CfnBackupSelection.BackupSelectionResourceTypeProperty.IamRoleArn``.
            :param selection_name: ``CfnBackupSelection.BackupSelectionResourceTypeProperty.SelectionName``.
            :param list_of_tags: ``CfnBackupSelection.BackupSelectionResourceTypeProperty.ListOfTags``.
            :param resources: ``CfnBackupSelection.BackupSelectionResourceTypeProperty.Resources``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-backupselectionresourcetype.html
            """
            self._values = {
                'iam_role_arn': iam_role_arn,
                'selection_name': selection_name,
            }
            if list_of_tags is not None: self._values["list_of_tags"] = list_of_tags
            if resources is not None: self._values["resources"] = resources

        @builtins.property
        def iam_role_arn(self) -> str:
            """``CfnBackupSelection.BackupSelectionResourceTypeProperty.IamRoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-backupselectionresourcetype.html#cfn-backup-backupselection-backupselectionresourcetype-iamrolearn
            """
            return self._values.get('iam_role_arn')

        @builtins.property
        def selection_name(self) -> str:
            """``CfnBackupSelection.BackupSelectionResourceTypeProperty.SelectionName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-backupselectionresourcetype.html#cfn-backup-backupselection-backupselectionresourcetype-selectionname
            """
            return self._values.get('selection_name')

        @builtins.property
        def list_of_tags(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnBackupSelection.ConditionResourceTypeProperty", _IResolvable_9ceae33e]]]]:
            """``CfnBackupSelection.BackupSelectionResourceTypeProperty.ListOfTags``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-backupselectionresourcetype.html#cfn-backup-backupselection-backupselectionresourcetype-listoftags
            """
            return self._values.get('list_of_tags')

        @builtins.property
        def resources(self) -> typing.Optional[typing.List[str]]:
            """``CfnBackupSelection.BackupSelectionResourceTypeProperty.Resources``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-backupselectionresourcetype.html#cfn-backup-backupselection-backupselectionresourcetype-resources
            """
            return self._values.get('resources')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'BackupSelectionResourceTypeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_backup.CfnBackupSelection.ConditionResourceTypeProperty", jsii_struct_bases=[], name_mapping={'condition_key': 'conditionKey', 'condition_type': 'conditionType', 'condition_value': 'conditionValue'})
    class ConditionResourceTypeProperty():
        def __init__(self, *, condition_key: str, condition_type: str, condition_value: str) -> None:
            """
            :param condition_key: ``CfnBackupSelection.ConditionResourceTypeProperty.ConditionKey``.
            :param condition_type: ``CfnBackupSelection.ConditionResourceTypeProperty.ConditionType``.
            :param condition_value: ``CfnBackupSelection.ConditionResourceTypeProperty.ConditionValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-conditionresourcetype.html
            """
            self._values = {
                'condition_key': condition_key,
                'condition_type': condition_type,
                'condition_value': condition_value,
            }

        @builtins.property
        def condition_key(self) -> str:
            """``CfnBackupSelection.ConditionResourceTypeProperty.ConditionKey``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-conditionresourcetype.html#cfn-backup-backupselection-conditionresourcetype-conditionkey
            """
            return self._values.get('condition_key')

        @builtins.property
        def condition_type(self) -> str:
            """``CfnBackupSelection.ConditionResourceTypeProperty.ConditionType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-conditionresourcetype.html#cfn-backup-backupselection-conditionresourcetype-conditiontype
            """
            return self._values.get('condition_type')

        @builtins.property
        def condition_value(self) -> str:
            """``CfnBackupSelection.ConditionResourceTypeProperty.ConditionValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-conditionresourcetype.html#cfn-backup-backupselection-conditionresourcetype-conditionvalue
            """
            return self._values.get('condition_value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ConditionResourceTypeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_backup.CfnBackupSelectionProps", jsii_struct_bases=[], name_mapping={'backup_plan_id': 'backupPlanId', 'backup_selection': 'backupSelection'})
class CfnBackupSelectionProps():
    def __init__(self, *, backup_plan_id: str, backup_selection: typing.Union["CfnBackupSelection.BackupSelectionResourceTypeProperty", _IResolvable_9ceae33e]) -> None:
        """Properties for defining a ``AWS::Backup::BackupSelection``.

        :param backup_plan_id: ``AWS::Backup::BackupSelection.BackupPlanId``.
        :param backup_selection: ``AWS::Backup::BackupSelection.BackupSelection``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupselection.html
        """
        self._values = {
            'backup_plan_id': backup_plan_id,
            'backup_selection': backup_selection,
        }

    @builtins.property
    def backup_plan_id(self) -> str:
        """``AWS::Backup::BackupSelection.BackupPlanId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupselection.html#cfn-backup-backupselection-backupplanid
        """
        return self._values.get('backup_plan_id')

    @builtins.property
    def backup_selection(self) -> typing.Union["CfnBackupSelection.BackupSelectionResourceTypeProperty", _IResolvable_9ceae33e]:
        """``AWS::Backup::BackupSelection.BackupSelection``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupselection.html#cfn-backup-backupselection-backupselection
        """
        return self._values.get('backup_selection')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnBackupSelectionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnBackupVault(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_backup.CfnBackupVault"):
    """A CloudFormation ``AWS::Backup::BackupVault``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html
    cloudformationResource:
    :cloudformationResource:: AWS::Backup::BackupVault
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, backup_vault_name: str, access_policy: typing.Any=None, backup_vault_tags: typing.Any=None, encryption_key_arn: typing.Optional[str]=None, notifications: typing.Optional[typing.Union["NotificationObjectTypeProperty", _IResolvable_9ceae33e]]=None) -> None:
        """Create a new ``AWS::Backup::BackupVault``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param backup_vault_name: ``AWS::Backup::BackupVault.BackupVaultName``.
        :param access_policy: ``AWS::Backup::BackupVault.AccessPolicy``.
        :param backup_vault_tags: ``AWS::Backup::BackupVault.BackupVaultTags``.
        :param encryption_key_arn: ``AWS::Backup::BackupVault.EncryptionKeyArn``.
        :param notifications: ``AWS::Backup::BackupVault.Notifications``.
        """
        props = CfnBackupVaultProps(backup_vault_name=backup_vault_name, access_policy=access_policy, backup_vault_tags=backup_vault_tags, encryption_key_arn=encryption_key_arn, notifications=notifications)

        jsii.create(CfnBackupVault, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnBackupVault":
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
    @jsii.member(jsii_name="attrBackupVaultArn")
    def attr_backup_vault_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: BackupVaultArn
        """
        return jsii.get(self, "attrBackupVaultArn")

    @builtins.property
    @jsii.member(jsii_name="attrBackupVaultName")
    def attr_backup_vault_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: BackupVaultName
        """
        return jsii.get(self, "attrBackupVaultName")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="accessPolicy")
    def access_policy(self) -> typing.Any:
        """``AWS::Backup::BackupVault.AccessPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-accesspolicy
        """
        return jsii.get(self, "accessPolicy")

    @access_policy.setter
    def access_policy(self, value: typing.Any) -> None:
        jsii.set(self, "accessPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="backupVaultName")
    def backup_vault_name(self) -> str:
        """``AWS::Backup::BackupVault.BackupVaultName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-backupvaultname
        """
        return jsii.get(self, "backupVaultName")

    @backup_vault_name.setter
    def backup_vault_name(self, value: str) -> None:
        jsii.set(self, "backupVaultName", value)

    @builtins.property
    @jsii.member(jsii_name="backupVaultTags")
    def backup_vault_tags(self) -> typing.Any:
        """``AWS::Backup::BackupVault.BackupVaultTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-backupvaulttags
        """
        return jsii.get(self, "backupVaultTags")

    @backup_vault_tags.setter
    def backup_vault_tags(self, value: typing.Any) -> None:
        jsii.set(self, "backupVaultTags", value)

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyArn")
    def encryption_key_arn(self) -> typing.Optional[str]:
        """``AWS::Backup::BackupVault.EncryptionKeyArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-encryptionkeyarn
        """
        return jsii.get(self, "encryptionKeyArn")

    @encryption_key_arn.setter
    def encryption_key_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "encryptionKeyArn", value)

    @builtins.property
    @jsii.member(jsii_name="notifications")
    def notifications(self) -> typing.Optional[typing.Union["NotificationObjectTypeProperty", _IResolvable_9ceae33e]]:
        """``AWS::Backup::BackupVault.Notifications``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-notifications
        """
        return jsii.get(self, "notifications")

    @notifications.setter
    def notifications(self, value: typing.Optional[typing.Union["NotificationObjectTypeProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "notifications", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_backup.CfnBackupVault.NotificationObjectTypeProperty", jsii_struct_bases=[], name_mapping={'backup_vault_events': 'backupVaultEvents', 'sns_topic_arn': 'snsTopicArn'})
    class NotificationObjectTypeProperty():
        def __init__(self, *, backup_vault_events: typing.List[str], sns_topic_arn: str) -> None:
            """
            :param backup_vault_events: ``CfnBackupVault.NotificationObjectTypeProperty.BackupVaultEvents``.
            :param sns_topic_arn: ``CfnBackupVault.NotificationObjectTypeProperty.SNSTopicArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupvault-notificationobjecttype.html
            """
            self._values = {
                'backup_vault_events': backup_vault_events,
                'sns_topic_arn': sns_topic_arn,
            }

        @builtins.property
        def backup_vault_events(self) -> typing.List[str]:
            """``CfnBackupVault.NotificationObjectTypeProperty.BackupVaultEvents``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupvault-notificationobjecttype.html#cfn-backup-backupvault-notificationobjecttype-backupvaultevents
            """
            return self._values.get('backup_vault_events')

        @builtins.property
        def sns_topic_arn(self) -> str:
            """``CfnBackupVault.NotificationObjectTypeProperty.SNSTopicArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupvault-notificationobjecttype.html#cfn-backup-backupvault-notificationobjecttype-snstopicarn
            """
            return self._values.get('sns_topic_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'NotificationObjectTypeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_backup.CfnBackupVaultProps", jsii_struct_bases=[], name_mapping={'backup_vault_name': 'backupVaultName', 'access_policy': 'accessPolicy', 'backup_vault_tags': 'backupVaultTags', 'encryption_key_arn': 'encryptionKeyArn', 'notifications': 'notifications'})
class CfnBackupVaultProps():
    def __init__(self, *, backup_vault_name: str, access_policy: typing.Any=None, backup_vault_tags: typing.Any=None, encryption_key_arn: typing.Optional[str]=None, notifications: typing.Optional[typing.Union["CfnBackupVault.NotificationObjectTypeProperty", _IResolvable_9ceae33e]]=None) -> None:
        """Properties for defining a ``AWS::Backup::BackupVault``.

        :param backup_vault_name: ``AWS::Backup::BackupVault.BackupVaultName``.
        :param access_policy: ``AWS::Backup::BackupVault.AccessPolicy``.
        :param backup_vault_tags: ``AWS::Backup::BackupVault.BackupVaultTags``.
        :param encryption_key_arn: ``AWS::Backup::BackupVault.EncryptionKeyArn``.
        :param notifications: ``AWS::Backup::BackupVault.Notifications``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html
        """
        self._values = {
            'backup_vault_name': backup_vault_name,
        }
        if access_policy is not None: self._values["access_policy"] = access_policy
        if backup_vault_tags is not None: self._values["backup_vault_tags"] = backup_vault_tags
        if encryption_key_arn is not None: self._values["encryption_key_arn"] = encryption_key_arn
        if notifications is not None: self._values["notifications"] = notifications

    @builtins.property
    def backup_vault_name(self) -> str:
        """``AWS::Backup::BackupVault.BackupVaultName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-backupvaultname
        """
        return self._values.get('backup_vault_name')

    @builtins.property
    def access_policy(self) -> typing.Any:
        """``AWS::Backup::BackupVault.AccessPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-accesspolicy
        """
        return self._values.get('access_policy')

    @builtins.property
    def backup_vault_tags(self) -> typing.Any:
        """``AWS::Backup::BackupVault.BackupVaultTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-backupvaulttags
        """
        return self._values.get('backup_vault_tags')

    @builtins.property
    def encryption_key_arn(self) -> typing.Optional[str]:
        """``AWS::Backup::BackupVault.EncryptionKeyArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-encryptionkeyarn
        """
        return self._values.get('encryption_key_arn')

    @builtins.property
    def notifications(self) -> typing.Optional[typing.Union["CfnBackupVault.NotificationObjectTypeProperty", _IResolvable_9ceae33e]]:
        """``AWS::Backup::BackupVault.Notifications``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-notifications
        """
        return self._values.get('notifications')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnBackupVaultProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="monocdk-experiment.aws_backup.IBackupPlan")
class IBackupPlan(_IResource_72f7ee7e, jsii.compat.Protocol):
    """A backup plan.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IBackupPlanProxy

    @builtins.property
    @jsii.member(jsii_name="backupPlanId")
    def backup_plan_id(self) -> str:
        """The identifier of the backup plan.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IBackupPlanProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """A backup plan.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_backup.IBackupPlan"
    @builtins.property
    @jsii.member(jsii_name="backupPlanId")
    def backup_plan_id(self) -> str:
        """The identifier of the backup plan.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "backupPlanId")


@jsii.interface(jsii_type="monocdk-experiment.aws_backup.IBackupVault")
class IBackupVault(_IResource_72f7ee7e, jsii.compat.Protocol):
    """A backup vault.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IBackupVaultProxy

    @builtins.property
    @jsii.member(jsii_name="backupVaultName")
    def backup_vault_name(self) -> str:
        """The name of a logical container where backups are stored.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IBackupVaultProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """A backup vault.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_backup.IBackupVault"
    @builtins.property
    @jsii.member(jsii_name="backupVaultName")
    def backup_vault_name(self) -> str:
        """The name of a logical container where backups are stored.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "backupVaultName")


@jsii.data_type(jsii_type="monocdk-experiment.aws_backup.TagCondition", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value', 'operation': 'operation'})
class TagCondition():
    def __init__(self, *, key: str, value: str, operation: typing.Optional["TagOperation"]=None) -> None:
        """A tag condition.

        :param key: The key in a key-value pair. For example, in ``"ec2:ResourceTag/Department": "accounting"``, ``ec2:ResourceTag/Department`` is the key.
        :param value: The value in a key-value pair. For example, in ``"ec2:ResourceTag/Department": "accounting"``, ``accounting`` is the value.
        :param operation: An operation that is applied to a key-value pair used to filter resources in a selection. Default: STRING_EQUALS

        stability
        :stability: experimental
        """
        self._values = {
            'key': key,
            'value': value,
        }
        if operation is not None: self._values["operation"] = operation

    @builtins.property
    def key(self) -> str:
        """The key in a key-value pair.

        For example, in ``"ec2:ResourceTag/Department": "accounting"``,
        ``ec2:ResourceTag/Department`` is the key.

        stability
        :stability: experimental
        """
        return self._values.get('key')

    @builtins.property
    def value(self) -> str:
        """The value in a key-value pair.

        For example, in ``"ec2:ResourceTag/Department": "accounting"``,
        ``accounting`` is the value.

        stability
        :stability: experimental
        """
        return self._values.get('value')

    @builtins.property
    def operation(self) -> typing.Optional["TagOperation"]:
        """An operation that is applied to a key-value pair used to filter resources in a selection.

        default
        :default: STRING_EQUALS

        stability
        :stability: experimental
        """
        return self._values.get('operation')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TagCondition(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_backup.TagOperation")
class TagOperation(enum.Enum):
    """An operation that is applied to a key-value pair.

    stability
    :stability: experimental
    """
    STRING_EQUALS = "STRING_EQUALS"
    """StringEquals.

    stability
    :stability: experimental
    """
    DUMMY = "DUMMY"
    """Dummy member.

    stability
    :stability: experimental
    """

@jsii.implements(IBackupPlan)
class BackupPlan(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_backup.BackupPlan"):
    """A backup plan.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, backup_plan_name: typing.Optional[str]=None, backup_plan_rules: typing.Optional[typing.List["BackupPlanRule"]]=None, backup_vault: typing.Optional["IBackupVault"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param backup_plan_name: The display name of the backup plan. Default: - A CDK generated name
        :param backup_plan_rules: Rules for the backup plan. Use ``addRule()`` to add rules after instantiation. Default: - use ``addRule()`` to add rules
        :param backup_vault: The backup vault where backups are stored. Default: - use the vault defined at the rule level. If not defined a new common vault for the plan will be created

        stability
        :stability: experimental
        """
        props = BackupPlanProps(backup_plan_name=backup_plan_name, backup_plan_rules=backup_plan_rules, backup_vault=backup_vault)

        jsii.create(BackupPlan, self, [scope, id, props])

    @jsii.member(jsii_name="daily35DayRetention")
    @builtins.classmethod
    def daily35_day_retention(cls, scope: _Construct_f50a3f53, id: str, backup_vault: typing.Optional["IBackupVault"]=None) -> "BackupPlan":
        """Daily with 35 day retention.

        :param scope: -
        :param id: -
        :param backup_vault: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "daily35DayRetention", [scope, id, backup_vault])

    @jsii.member(jsii_name="dailyMonthly1YearRetention")
    @builtins.classmethod
    def daily_monthly1_year_retention(cls, scope: _Construct_f50a3f53, id: str, backup_vault: typing.Optional["IBackupVault"]=None) -> "BackupPlan":
        """Daily and monthly with 1 year retention.

        :param scope: -
        :param id: -
        :param backup_vault: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "dailyMonthly1YearRetention", [scope, id, backup_vault])

    @jsii.member(jsii_name="dailyWeeklyMonthly5YearRetention")
    @builtins.classmethod
    def daily_weekly_monthly5_year_retention(cls, scope: _Construct_f50a3f53, id: str, backup_vault: typing.Optional["IBackupVault"]=None) -> "BackupPlan":
        """Daily, weekly and monthly with 5 year retention.

        :param scope: -
        :param id: -
        :param backup_vault: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "dailyWeeklyMonthly5YearRetention", [scope, id, backup_vault])

    @jsii.member(jsii_name="dailyWeeklyMonthly7YearRetention")
    @builtins.classmethod
    def daily_weekly_monthly7_year_retention(cls, scope: _Construct_f50a3f53, id: str, backup_vault: typing.Optional["IBackupVault"]=None) -> "BackupPlan":
        """Daily, weekly and monthly with 7 year retention.

        :param scope: -
        :param id: -
        :param backup_vault: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "dailyWeeklyMonthly7YearRetention", [scope, id, backup_vault])

    @jsii.member(jsii_name="fromBackupPlanId")
    @builtins.classmethod
    def from_backup_plan_id(cls, scope: _Construct_f50a3f53, id: str, backup_plan_id: str) -> "IBackupPlan":
        """Import an existing backup plan.

        :param scope: -
        :param id: -
        :param backup_plan_id: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromBackupPlanId", [scope, id, backup_plan_id])

    @jsii.member(jsii_name="addRule")
    def add_rule(self, rule: "BackupPlanRule") -> None:
        """Adds a rule to a plan.

        :param rule: the rule to add.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addRule", [rule])

    @jsii.member(jsii_name="addSelection")
    def add_selection(self, id: str, *, resources: typing.List["BackupResource"], allow_restores: typing.Optional[bool]=None, backup_selection_name: typing.Optional[str]=None, role: typing.Optional[_IRole_e69bbae4]=None) -> "BackupSelection":
        """Adds a selection to this plan.

        :param id: -
        :param resources: The resources to backup. Use the helper static methods defined on ``BackupResource``.
        :param allow_restores: Whether to automatically give restores permissions to the role that AWS Backup uses. If ``true``, the ``AWSBackupServiceRolePolicyForRestores`` managed policy will be attached to the role. Default: false
        :param backup_selection_name: The name for this selection. Default: - a CDK generated name
        :param role: The role that AWS Backup uses to authenticate when backuping or restoring the resources. The ``AWSBackupServiceRolePolicyForBackup`` managed policy will be attached to this role. Default: - a new role will be created

        stability
        :stability: experimental
        """
        options = BackupSelectionOptions(resources=resources, allow_restores=allow_restores, backup_selection_name=backup_selection_name, role=role)

        return jsii.invoke(self, "addSelection", [id, options])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="backupPlanArn")
    def backup_plan_arn(self) -> str:
        """The ARN of the backup plan.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "backupPlanArn")

    @builtins.property
    @jsii.member(jsii_name="backupPlanId")
    def backup_plan_id(self) -> str:
        """The identifier of the backup plan.

        stability
        :stability: experimental
        """
        return jsii.get(self, "backupPlanId")

    @builtins.property
    @jsii.member(jsii_name="backupVault")
    def backup_vault(self) -> "IBackupVault":
        """The backup vault where backups are stored if not defined at the rule level.

        stability
        :stability: experimental
        """
        return jsii.get(self, "backupVault")

    @builtins.property
    @jsii.member(jsii_name="versionId")
    def version_id(self) -> str:
        """Version Id.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "versionId")


@jsii.implements(IBackupVault)
class BackupVault(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_backup.BackupVault"):
    """A backup vault.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, access_policy: typing.Optional[_PolicyDocument_1d1bca11]=None, backup_vault_name: typing.Optional[str]=None, encryption_key: typing.Optional[_IKey_3336c79d]=None, notification_events: typing.Optional[typing.List["BackupVaultEvents"]]=None, notification_topic: typing.Optional[_ITopic_ef0ebe0e]=None, removal_policy: typing.Optional[_RemovalPolicy_5986e9f3]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param access_policy: A resource-based policy that is used to manage access permissions on the backup vault. Default: - access is not restricted
        :param backup_vault_name: The name of a logical container where backups are stored. Default: - A CDK generated name
        :param encryption_key: The server-side encryption key to use to protect your backups. Default: - an Amazon managed KMS key
        :param notification_events: The vault events to send. Default: - all vault events if ``notificationTopic`` is defined
        :param notification_topic: A SNS topic to send vault events to. Default: - no notifications
        :param removal_policy: The removal policy to apply to the vault. Note that removing a vault that contains recovery points will fail. Default: RemovalPolicy.RETAIN

        stability
        :stability: experimental
        """
        props = BackupVaultProps(access_policy=access_policy, backup_vault_name=backup_vault_name, encryption_key=encryption_key, notification_events=notification_events, notification_topic=notification_topic, removal_policy=removal_policy)

        jsii.create(BackupVault, self, [scope, id, props])

    @jsii.member(jsii_name="fromBackupVaultName")
    @builtins.classmethod
    def from_backup_vault_name(cls, scope: _Construct_f50a3f53, id: str, backup_vault_name: str) -> "IBackupVault":
        """Import an existing backup vault.

        :param scope: -
        :param id: -
        :param backup_vault_name: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromBackupVaultName", [scope, id, backup_vault_name])

    @builtins.property
    @jsii.member(jsii_name="backupVaultArn")
    def backup_vault_arn(self) -> str:
        """The ARN of the backup vault.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "backupVaultArn")

    @builtins.property
    @jsii.member(jsii_name="backupVaultName")
    def backup_vault_name(self) -> str:
        """The name of a logical container where backups are stored.

        stability
        :stability: experimental
        """
        return jsii.get(self, "backupVaultName")


__all__ = [
    "BackupPlan",
    "BackupPlanProps",
    "BackupPlanRule",
    "BackupPlanRuleProps",
    "BackupResource",
    "BackupSelection",
    "BackupSelectionOptions",
    "BackupSelectionProps",
    "BackupVault",
    "BackupVaultEvents",
    "BackupVaultProps",
    "CfnBackupPlan",
    "CfnBackupPlanProps",
    "CfnBackupSelection",
    "CfnBackupSelectionProps",
    "CfnBackupVault",
    "CfnBackupVaultProps",
    "IBackupPlan",
    "IBackupVault",
    "TagCondition",
    "TagOperation",
]

publication.publish()
