import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (Construct as _Construct_f50a3f53, Duration as _Duration_5170c158, CfnResource as _CfnResource_7760e8e4, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, IResolvable as _IResolvable_9ceae33e, IInspectable as _IInspectable_051e6ed8, TagManager as _TagManager_2508893f, Resource as _Resource_884d0774, IResource as _IResource_72f7ee7e)
from ..aws_autoscaling import (CommonAutoScalingGroupProps as _CommonAutoScalingGroupProps_43a23fca, BlockDevice as _BlockDevice_6b64cf0c, HealthCheck as _HealthCheck_ed599e14, Monitoring as _Monitoring_11cb7f01, NotificationConfiguration as _NotificationConfiguration_396b88c6, RollingUpdateConfiguration as _RollingUpdateConfiguration_c96dd49e, UpdateType as _UpdateType_7a2ac17e, AutoScalingGroup as _AutoScalingGroup_003d0b84)
from ..aws_ec2 import (SubnetSelection as _SubnetSelection_36a13cd6, InstanceType as _InstanceType_85a97b30, Connections as _Connections_231f38b5, IVpc as _IVpc_3795853f, ISecurityGroup as _ISecurityGroup_d72ab8e8, MachineImageConfig as _MachineImageConfig_815fc1b9, IMachineImage as _IMachineImage_d5cd7b45, IConnectable as _IConnectable_a587039f)
from ..aws_iam import (IRole as _IRole_e69bbae4, IUser as _IUser_7e7f2b20)
from ..aws_sns import (ITopic as _ITopic_ef0ebe0e)


@jsii.data_type(jsii_type="monocdk-experiment.aws_eks_legacy.AutoScalingGroupOptions", jsii_struct_bases=[], name_mapping={'bootstrap_enabled': 'bootstrapEnabled', 'bootstrap_options': 'bootstrapOptions', 'map_role': 'mapRole'})
class AutoScalingGroupOptions():
    def __init__(self, *, bootstrap_enabled: typing.Optional[bool]=None, bootstrap_options: typing.Optional["BootstrapOptions"]=None, map_role: typing.Optional[bool]=None) -> None:
        """Options for adding an AutoScalingGroup as capacity.

        :param bootstrap_enabled: Configures the EC2 user-data script for instances in this autoscaling group to bootstrap the node (invoke ``/etc/eks/bootstrap.sh``) and associate it with the EKS cluster. If you wish to provide a custom user data script, set this to ``false`` and manually invoke ``autoscalingGroup.addUserData()``. Default: true
        :param bootstrap_options: Allows options for node bootstrapping through EC2 user data.
        :param map_role: Will automatically update the aws-auth ConfigMap to map the IAM instance role to RBAC. This cannot be explicitly set to ``true`` if the cluster has kubectl disabled. Default: - true if the cluster has kubectl enabled (which is the default).

        stability
        :stability: experimental
        """
        if isinstance(bootstrap_options, dict): bootstrap_options = BootstrapOptions(**bootstrap_options)
        self._values = {
        }
        if bootstrap_enabled is not None: self._values["bootstrap_enabled"] = bootstrap_enabled
        if bootstrap_options is not None: self._values["bootstrap_options"] = bootstrap_options
        if map_role is not None: self._values["map_role"] = map_role

    @builtins.property
    def bootstrap_enabled(self) -> typing.Optional[bool]:
        """Configures the EC2 user-data script for instances in this autoscaling group to bootstrap the node (invoke ``/etc/eks/bootstrap.sh``) and associate it with the EKS cluster.

        If you wish to provide a custom user data script, set this to ``false`` and
        manually invoke ``autoscalingGroup.addUserData()``.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('bootstrap_enabled')

    @builtins.property
    def bootstrap_options(self) -> typing.Optional["BootstrapOptions"]:
        """Allows options for node bootstrapping through EC2 user data.

        stability
        :stability: experimental
        """
        return self._values.get('bootstrap_options')

    @builtins.property
    def map_role(self) -> typing.Optional[bool]:
        """Will automatically update the aws-auth ConfigMap to map the IAM instance role to RBAC.

        This cannot be explicitly set to ``true`` if the cluster has kubectl disabled.

        default
        :default: - true if the cluster has kubectl enabled (which is the default).

        stability
        :stability: experimental
        """
        return self._values.get('map_role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AutoScalingGroupOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class AwsAuth(_Construct_f50a3f53, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_eks_legacy.AwsAuth"):
    """Manages mapping between IAM users and roles to Kubernetes RBAC configuration.

    see
    :see: https://docs.aws.amazon.com/en_us/eks/latest/userguide/add-user-role.html
    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, cluster: "Cluster") -> None:
        """
        :param scope: -
        :param id: -
        :param cluster: The EKS cluster to apply this configuration to. [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        props = AwsAuthProps(cluster=cluster)

        jsii.create(AwsAuth, self, [scope, id, props])

    @jsii.member(jsii_name="addAccount")
    def add_account(self, account_id: str) -> None:
        """Additional AWS account to add to the aws-auth configmap.

        :param account_id: account number.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addAccount", [account_id])

    @jsii.member(jsii_name="addMastersRole")
    def add_masters_role(self, role: _IRole_e69bbae4, username: typing.Optional[str]=None) -> None:
        """Adds the specified IAM role to the ``system:masters`` RBAC group, which means that anyone that can assume it will be able to administer this Kubernetes system.

        :param role: The IAM role to add.
        :param username: Optional user (defaults to the role ARN).

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addMastersRole", [role, username])

    @jsii.member(jsii_name="addRoleMapping")
    def add_role_mapping(self, role: _IRole_e69bbae4, *, groups: typing.List[str], username: typing.Optional[str]=None) -> None:
        """Adds a mapping between an IAM role to a Kubernetes user and groups.

        :param role: The IAM role to map.
        :param groups: A list of groups within Kubernetes to which the role is mapped.
        :param username: The user name within Kubernetes to map to the IAM role. Default: - By default, the user name is the ARN of the IAM role.

        stability
        :stability: experimental
        """
        mapping = Mapping(groups=groups, username=username)

        return jsii.invoke(self, "addRoleMapping", [role, mapping])

    @jsii.member(jsii_name="addUserMapping")
    def add_user_mapping(self, user: _IUser_7e7f2b20, *, groups: typing.List[str], username: typing.Optional[str]=None) -> None:
        """Adds a mapping between an IAM user to a Kubernetes user and groups.

        :param user: The IAM user to map.
        :param groups: A list of groups within Kubernetes to which the role is mapped.
        :param username: The user name within Kubernetes to map to the IAM role. Default: - By default, the user name is the ARN of the IAM role.

        stability
        :stability: experimental
        """
        mapping = Mapping(groups=groups, username=username)

        return jsii.invoke(self, "addUserMapping", [user, mapping])


@jsii.data_type(jsii_type="monocdk-experiment.aws_eks_legacy.AwsAuthProps", jsii_struct_bases=[], name_mapping={'cluster': 'cluster'})
class AwsAuthProps():
    def __init__(self, *, cluster: "Cluster") -> None:
        """
        :param cluster: The EKS cluster to apply this configuration to. [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        self._values = {
            'cluster': cluster,
        }

    @builtins.property
    def cluster(self) -> "Cluster":
        """The EKS cluster to apply this configuration to.

        [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AwsAuthProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_eks_legacy.BootstrapOptions", jsii_struct_bases=[], name_mapping={'additional_args': 'additionalArgs', 'aws_api_retry_attempts': 'awsApiRetryAttempts', 'docker_config_json': 'dockerConfigJson', 'enable_docker_bridge': 'enableDockerBridge', 'kubelet_extra_args': 'kubeletExtraArgs', 'use_max_pods': 'useMaxPods'})
class BootstrapOptions():
    def __init__(self, *, additional_args: typing.Optional[str]=None, aws_api_retry_attempts: typing.Optional[jsii.Number]=None, docker_config_json: typing.Optional[str]=None, enable_docker_bridge: typing.Optional[bool]=None, kubelet_extra_args: typing.Optional[str]=None, use_max_pods: typing.Optional[bool]=None) -> None:
        """
        :param additional_args: Additional command line arguments to pass to the ``/etc/eks/bootstrap.sh`` command. Default: - none
        :param aws_api_retry_attempts: Number of retry attempts for AWS API call (DescribeCluster). Default: 3
        :param docker_config_json: The contents of the ``/etc/docker/daemon.json`` file. Useful if you want a custom config differing from the default one in the EKS AMI. Default: - none
        :param enable_docker_bridge: Restores the docker default bridge network. Default: false
        :param kubelet_extra_args: Extra arguments to add to the kubelet. Useful for adding labels or taints. Default: - none
        :param use_max_pods: Sets ``--max-pods`` for the kubelet based on the capacity of the EC2 instance. Default: true

        stability
        :stability: experimental
        """
        self._values = {
        }
        if additional_args is not None: self._values["additional_args"] = additional_args
        if aws_api_retry_attempts is not None: self._values["aws_api_retry_attempts"] = aws_api_retry_attempts
        if docker_config_json is not None: self._values["docker_config_json"] = docker_config_json
        if enable_docker_bridge is not None: self._values["enable_docker_bridge"] = enable_docker_bridge
        if kubelet_extra_args is not None: self._values["kubelet_extra_args"] = kubelet_extra_args
        if use_max_pods is not None: self._values["use_max_pods"] = use_max_pods

    @builtins.property
    def additional_args(self) -> typing.Optional[str]:
        """Additional command line arguments to pass to the ``/etc/eks/bootstrap.sh`` command.

        default
        :default: - none

        see
        :see: https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh
        stability
        :stability: experimental
        """
        return self._values.get('additional_args')

    @builtins.property
    def aws_api_retry_attempts(self) -> typing.Optional[jsii.Number]:
        """Number of retry attempts for AWS API call (DescribeCluster).

        default
        :default: 3

        stability
        :stability: experimental
        """
        return self._values.get('aws_api_retry_attempts')

    @builtins.property
    def docker_config_json(self) -> typing.Optional[str]:
        """The contents of the ``/etc/docker/daemon.json`` file. Useful if you want a custom config differing from the default one in the EKS AMI.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('docker_config_json')

    @builtins.property
    def enable_docker_bridge(self) -> typing.Optional[bool]:
        """Restores the docker default bridge network.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('enable_docker_bridge')

    @builtins.property
    def kubelet_extra_args(self) -> typing.Optional[str]:
        """Extra arguments to add to the kubelet.

        Useful for adding labels or taints.

        default
        :default: - none

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            --node - labelsfoo = bar , goo = far
        """
        return self._values.get('kubelet_extra_args')

    @builtins.property
    def use_max_pods(self) -> typing.Optional[bool]:
        """Sets ``--max-pods`` for the kubelet based on the capacity of the EC2 instance.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('use_max_pods')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BootstrapOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_eks_legacy.CapacityOptions", jsii_struct_bases=[_CommonAutoScalingGroupProps_43a23fca], name_mapping={'allow_all_outbound': 'allowAllOutbound', 'associate_public_ip_address': 'associatePublicIpAddress', 'block_devices': 'blockDevices', 'cooldown': 'cooldown', 'desired_capacity': 'desiredCapacity', 'health_check': 'healthCheck', 'ignore_unmodified_size_properties': 'ignoreUnmodifiedSizeProperties', 'instance_monitoring': 'instanceMonitoring', 'key_name': 'keyName', 'max_capacity': 'maxCapacity', 'max_instance_lifetime': 'maxInstanceLifetime', 'min_capacity': 'minCapacity', 'notifications': 'notifications', 'notifications_topic': 'notificationsTopic', 'replacing_update_min_successful_instances_percent': 'replacingUpdateMinSuccessfulInstancesPercent', 'resource_signal_count': 'resourceSignalCount', 'resource_signal_timeout': 'resourceSignalTimeout', 'rolling_update_configuration': 'rollingUpdateConfiguration', 'spot_price': 'spotPrice', 'update_type': 'updateType', 'vpc_subnets': 'vpcSubnets', 'instance_type': 'instanceType', 'bootstrap_enabled': 'bootstrapEnabled', 'bootstrap_options': 'bootstrapOptions', 'map_role': 'mapRole'})
class CapacityOptions(_CommonAutoScalingGroupProps_43a23fca):
    def __init__(self, *, allow_all_outbound: typing.Optional[bool]=None, associate_public_ip_address: typing.Optional[bool]=None, block_devices: typing.Optional[typing.List[_BlockDevice_6b64cf0c]]=None, cooldown: typing.Optional[_Duration_5170c158]=None, desired_capacity: typing.Optional[jsii.Number]=None, health_check: typing.Optional[_HealthCheck_ed599e14]=None, ignore_unmodified_size_properties: typing.Optional[bool]=None, instance_monitoring: typing.Optional[_Monitoring_11cb7f01]=None, key_name: typing.Optional[str]=None, max_capacity: typing.Optional[jsii.Number]=None, max_instance_lifetime: typing.Optional[_Duration_5170c158]=None, min_capacity: typing.Optional[jsii.Number]=None, notifications: typing.Optional[typing.List[_NotificationConfiguration_396b88c6]]=None, notifications_topic: typing.Optional[_ITopic_ef0ebe0e]=None, replacing_update_min_successful_instances_percent: typing.Optional[jsii.Number]=None, resource_signal_count: typing.Optional[jsii.Number]=None, resource_signal_timeout: typing.Optional[_Duration_5170c158]=None, rolling_update_configuration: typing.Optional[_RollingUpdateConfiguration_c96dd49e]=None, spot_price: typing.Optional[str]=None, update_type: typing.Optional[_UpdateType_7a2ac17e]=None, vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6]=None, instance_type: _InstanceType_85a97b30, bootstrap_enabled: typing.Optional[bool]=None, bootstrap_options: typing.Optional["BootstrapOptions"]=None, map_role: typing.Optional[bool]=None) -> None:
        """Options for adding worker nodes.

        :param allow_all_outbound: Whether the instances can initiate connections to anywhere by default. Default: true
        :param associate_public_ip_address: Whether instances in the Auto Scaling Group should have public IP addresses associated with them. Default: - Use subnet setting.
        :param block_devices: Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes. Each instance that is launched has an associated root device volume, either an Amazon EBS volume or an instance store volume. You can use block device mappings to specify additional EBS volumes or instance store volumes to attach to an instance when it is launched. Default: - Uses the block device mapping of the AMI
        :param cooldown: Default scaling cooldown for this AutoScalingGroup. Default: Duration.minutes(5)
        :param desired_capacity: Initial amount of instances in the fleet. If this is set to a number, every deployment will reset the amount of instances to this number. It is recommended to leave this value blank. Default: minCapacity, and leave unchanged during deployment
        :param health_check: Configuration for health checks. Default: - HealthCheck.ec2 with no grace period
        :param ignore_unmodified_size_properties: If the ASG has scheduled actions, don't reset unchanged group sizes. Only used if the ASG has scheduled actions (which may scale your ASG up or down regardless of cdk deployments). If true, the size of the group will only be reset if it has been changed in the CDK app. If false, the sizes will always be changed back to what they were in the CDK app on deployment. Default: true
        :param instance_monitoring: Controls whether instances in this group are launched with detailed or basic monitoring. When detailed monitoring is enabled, Amazon CloudWatch generates metrics every minute and your account is charged a fee. When you disable detailed monitoring, CloudWatch generates metrics every 5 minutes. Default: - Monitoring.DETAILED
        :param key_name: Name of SSH keypair to grant access to instances. Default: - No SSH access will be possible.
        :param max_capacity: Maximum number of instances in the fleet. Default: desiredCapacity
        :param max_instance_lifetime: The maximum amount of time that an instance can be in service. The maximum duration applies to all current and future instances in the group. As an instance approaches its maximum duration, it is terminated and replaced, and cannot be used again. You must specify a value of at least 604,800 seconds (7 days). To clear a previously set value, simply leave this property undefinied. Default: none
        :param min_capacity: Minimum number of instances in the fleet. Default: 1
        :param notifications: Configure autoscaling group to send notifications about fleet changes to an SNS topic(s). Default: - No fleet change notifications will be sent.
        :param notifications_topic: SNS topic to send notifications about fleet changes. Default: - No fleet change notifications will be sent.
        :param replacing_update_min_successful_instances_percent: Configuration for replacing updates. Only used if updateType == UpdateType.ReplacingUpdate. Specifies how many instances must signal success for the update to succeed. Default: minSuccessfulInstancesPercent
        :param resource_signal_count: How many ResourceSignal calls CloudFormation expects before the resource is considered created. Default: 1
        :param resource_signal_timeout: The length of time to wait for the resourceSignalCount. The maximum value is 43200 (12 hours). Default: Duration.minutes(5)
        :param rolling_update_configuration: Configuration for rolling updates. Only used if updateType == UpdateType.RollingUpdate. Default: - RollingUpdateConfiguration with defaults.
        :param spot_price: The maximum hourly price (in USD) to be paid for any Spot Instance launched to fulfill the request. Spot Instances are launched when the price you specify exceeds the current Spot market price. Default: none
        :param update_type: What to do when an AutoScalingGroup's instance configuration is changed. This is applied when any of the settings on the ASG are changed that affect how the instances should be created (VPC, instance type, startup scripts, etc.). It indicates how the existing instances should be replaced with new instances matching the new config. By default, nothing is done and only new instances are launched with the new config. Default: UpdateType.None
        :param vpc_subnets: Where to place instances within the VPC. Default: - All Private subnets.
        :param instance_type: Instance type of the instances to start.
        :param bootstrap_enabled: Configures the EC2 user-data script for instances in this autoscaling group to bootstrap the node (invoke ``/etc/eks/bootstrap.sh``) and associate it with the EKS cluster. If you wish to provide a custom user data script, set this to ``false`` and manually invoke ``autoscalingGroup.addUserData()``. Default: true
        :param bootstrap_options: EKS node bootstrapping options. Default: - none
        :param map_role: Will automatically update the aws-auth ConfigMap to map the IAM instance role to RBAC. This cannot be explicitly set to ``true`` if the cluster has kubectl disabled. Default: - true if the cluster has kubectl enabled (which is the default).

        stability
        :stability: experimental
        """
        if isinstance(rolling_update_configuration, dict): rolling_update_configuration = _RollingUpdateConfiguration_c96dd49e(**rolling_update_configuration)
        if isinstance(vpc_subnets, dict): vpc_subnets = _SubnetSelection_36a13cd6(**vpc_subnets)
        if isinstance(bootstrap_options, dict): bootstrap_options = BootstrapOptions(**bootstrap_options)
        self._values = {
            'instance_type': instance_type,
        }
        if allow_all_outbound is not None: self._values["allow_all_outbound"] = allow_all_outbound
        if associate_public_ip_address is not None: self._values["associate_public_ip_address"] = associate_public_ip_address
        if block_devices is not None: self._values["block_devices"] = block_devices
        if cooldown is not None: self._values["cooldown"] = cooldown
        if desired_capacity is not None: self._values["desired_capacity"] = desired_capacity
        if health_check is not None: self._values["health_check"] = health_check
        if ignore_unmodified_size_properties is not None: self._values["ignore_unmodified_size_properties"] = ignore_unmodified_size_properties
        if instance_monitoring is not None: self._values["instance_monitoring"] = instance_monitoring
        if key_name is not None: self._values["key_name"] = key_name
        if max_capacity is not None: self._values["max_capacity"] = max_capacity
        if max_instance_lifetime is not None: self._values["max_instance_lifetime"] = max_instance_lifetime
        if min_capacity is not None: self._values["min_capacity"] = min_capacity
        if notifications is not None: self._values["notifications"] = notifications
        if notifications_topic is not None: self._values["notifications_topic"] = notifications_topic
        if replacing_update_min_successful_instances_percent is not None: self._values["replacing_update_min_successful_instances_percent"] = replacing_update_min_successful_instances_percent
        if resource_signal_count is not None: self._values["resource_signal_count"] = resource_signal_count
        if resource_signal_timeout is not None: self._values["resource_signal_timeout"] = resource_signal_timeout
        if rolling_update_configuration is not None: self._values["rolling_update_configuration"] = rolling_update_configuration
        if spot_price is not None: self._values["spot_price"] = spot_price
        if update_type is not None: self._values["update_type"] = update_type
        if vpc_subnets is not None: self._values["vpc_subnets"] = vpc_subnets
        if bootstrap_enabled is not None: self._values["bootstrap_enabled"] = bootstrap_enabled
        if bootstrap_options is not None: self._values["bootstrap_options"] = bootstrap_options
        if map_role is not None: self._values["map_role"] = map_role

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[bool]:
        """Whether the instances can initiate connections to anywhere by default.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('allow_all_outbound')

    @builtins.property
    def associate_public_ip_address(self) -> typing.Optional[bool]:
        """Whether instances in the Auto Scaling Group should have public IP addresses associated with them.

        default
        :default: - Use subnet setting.

        stability
        :stability: experimental
        """
        return self._values.get('associate_public_ip_address')

    @builtins.property
    def block_devices(self) -> typing.Optional[typing.List[_BlockDevice_6b64cf0c]]:
        """Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes.

        Each instance that is launched has an associated root device volume,
        either an Amazon EBS volume or an instance store volume.
        You can use block device mappings to specify additional EBS volumes or
        instance store volumes to attach to an instance when it is launched.

        default
        :default: - Uses the block device mapping of the AMI

        see
        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/block-device-mapping-concepts.html
        stability
        :stability: experimental
        """
        return self._values.get('block_devices')

    @builtins.property
    def cooldown(self) -> typing.Optional[_Duration_5170c158]:
        """Default scaling cooldown for this AutoScalingGroup.

        default
        :default: Duration.minutes(5)

        stability
        :stability: experimental
        """
        return self._values.get('cooldown')

    @builtins.property
    def desired_capacity(self) -> typing.Optional[jsii.Number]:
        """Initial amount of instances in the fleet.

        If this is set to a number, every deployment will reset the amount of
        instances to this number. It is recommended to leave this value blank.

        default
        :default: minCapacity, and leave unchanged during deployment

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-desiredcapacity
        stability
        :stability: experimental
        """
        return self._values.get('desired_capacity')

    @builtins.property
    def health_check(self) -> typing.Optional[_HealthCheck_ed599e14]:
        """Configuration for health checks.

        default
        :default: - HealthCheck.ec2 with no grace period

        stability
        :stability: experimental
        """
        return self._values.get('health_check')

    @builtins.property
    def ignore_unmodified_size_properties(self) -> typing.Optional[bool]:
        """If the ASG has scheduled actions, don't reset unchanged group sizes.

        Only used if the ASG has scheduled actions (which may scale your ASG up
        or down regardless of cdk deployments). If true, the size of the group
        will only be reset if it has been changed in the CDK app. If false, the
        sizes will always be changed back to what they were in the CDK app
        on deployment.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('ignore_unmodified_size_properties')

    @builtins.property
    def instance_monitoring(self) -> typing.Optional[_Monitoring_11cb7f01]:
        """Controls whether instances in this group are launched with detailed or basic monitoring.

        When detailed monitoring is enabled, Amazon CloudWatch generates metrics every minute and your account
        is charged a fee. When you disable detailed monitoring, CloudWatch generates metrics every 5 minutes.

        default
        :default: - Monitoring.DETAILED

        see
        :see: https://docs.aws.amazon.com/autoscaling/latest/userguide/as-instance-monitoring.html#enable-as-instance-metrics
        stability
        :stability: experimental
        """
        return self._values.get('instance_monitoring')

    @builtins.property
    def key_name(self) -> typing.Optional[str]:
        """Name of SSH keypair to grant access to instances.

        default
        :default: - No SSH access will be possible.

        stability
        :stability: experimental
        """
        return self._values.get('key_name')

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        """Maximum number of instances in the fleet.

        default
        :default: desiredCapacity

        stability
        :stability: experimental
        """
        return self._values.get('max_capacity')

    @builtins.property
    def max_instance_lifetime(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum amount of time that an instance can be in service.

        The maximum duration applies
        to all current and future instances in the group. As an instance approaches its maximum duration,
        it is terminated and replaced, and cannot be used again.

        You must specify a value of at least 604,800 seconds (7 days). To clear a previously set value,
        simply leave this property undefinied.

        default
        :default: none

        see
        :see: https://docs.aws.amazon.com/autoscaling/ec2/userguide/asg-max-instance-lifetime.html
        stability
        :stability: experimental
        """
        return self._values.get('max_instance_lifetime')

    @builtins.property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        """Minimum number of instances in the fleet.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('min_capacity')

    @builtins.property
    def notifications(self) -> typing.Optional[typing.List[_NotificationConfiguration_396b88c6]]:
        """Configure autoscaling group to send notifications about fleet changes to an SNS topic(s).

        default
        :default: - No fleet change notifications will be sent.

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-notificationconfigurations
        stability
        :stability: experimental
        """
        return self._values.get('notifications')

    @builtins.property
    def notifications_topic(self) -> typing.Optional[_ITopic_ef0ebe0e]:
        """SNS topic to send notifications about fleet changes.

        default
        :default: - No fleet change notifications will be sent.

        deprecated
        :deprecated: use ``notifications``

        stability
        :stability: deprecated
        """
        return self._values.get('notifications_topic')

    @builtins.property
    def replacing_update_min_successful_instances_percent(self) -> typing.Optional[jsii.Number]:
        """Configuration for replacing updates.

        Only used if updateType == UpdateType.ReplacingUpdate. Specifies how
        many instances must signal success for the update to succeed.

        default
        :default: minSuccessfulInstancesPercent

        stability
        :stability: experimental
        """
        return self._values.get('replacing_update_min_successful_instances_percent')

    @builtins.property
    def resource_signal_count(self) -> typing.Optional[jsii.Number]:
        """How many ResourceSignal calls CloudFormation expects before the resource is considered created.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('resource_signal_count')

    @builtins.property
    def resource_signal_timeout(self) -> typing.Optional[_Duration_5170c158]:
        """The length of time to wait for the resourceSignalCount.

        The maximum value is 43200 (12 hours).

        default
        :default: Duration.minutes(5)

        stability
        :stability: experimental
        """
        return self._values.get('resource_signal_timeout')

    @builtins.property
    def rolling_update_configuration(self) -> typing.Optional[_RollingUpdateConfiguration_c96dd49e]:
        """Configuration for rolling updates.

        Only used if updateType == UpdateType.RollingUpdate.

        default
        :default: - RollingUpdateConfiguration with defaults.

        stability
        :stability: experimental
        """
        return self._values.get('rolling_update_configuration')

    @builtins.property
    def spot_price(self) -> typing.Optional[str]:
        """The maximum hourly price (in USD) to be paid for any Spot Instance launched to fulfill the request.

        Spot Instances are
        launched when the price you specify exceeds the current Spot market price.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('spot_price')

    @builtins.property
    def update_type(self) -> typing.Optional[_UpdateType_7a2ac17e]:
        """What to do when an AutoScalingGroup's instance configuration is changed.

        This is applied when any of the settings on the ASG are changed that
        affect how the instances should be created (VPC, instance type, startup
        scripts, etc.). It indicates how the existing instances should be
        replaced with new instances matching the new config. By default, nothing
        is done and only new instances are launched with the new config.

        default
        :default: UpdateType.None

        stability
        :stability: experimental
        """
        return self._values.get('update_type')

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """Where to place instances within the VPC.

        default
        :default: - All Private subnets.

        stability
        :stability: experimental
        """
        return self._values.get('vpc_subnets')

    @builtins.property
    def instance_type(self) -> _InstanceType_85a97b30:
        """Instance type of the instances to start.

        stability
        :stability: experimental
        """
        return self._values.get('instance_type')

    @builtins.property
    def bootstrap_enabled(self) -> typing.Optional[bool]:
        """Configures the EC2 user-data script for instances in this autoscaling group to bootstrap the node (invoke ``/etc/eks/bootstrap.sh``) and associate it with the EKS cluster.

        If you wish to provide a custom user data script, set this to ``false`` and
        manually invoke ``autoscalingGroup.addUserData()``.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('bootstrap_enabled')

    @builtins.property
    def bootstrap_options(self) -> typing.Optional["BootstrapOptions"]:
        """EKS node bootstrapping options.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('bootstrap_options')

    @builtins.property
    def map_role(self) -> typing.Optional[bool]:
        """Will automatically update the aws-auth ConfigMap to map the IAM instance role to RBAC.

        This cannot be explicitly set to ``true`` if the cluster has kubectl disabled.

        default
        :default: - true if the cluster has kubectl enabled (which is the default).

        stability
        :stability: experimental
        """
        return self._values.get('map_role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CapacityOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnCluster(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_eks_legacy.CfnCluster"):
    """A CloudFormation ``AWS::EKS::Cluster``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html
    cloudformationResource:
    :cloudformationResource:: AWS::EKS::Cluster
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, resources_vpc_config: typing.Union["ResourcesVpcConfigProperty", _IResolvable_9ceae33e], role_arn: str, encryption_config: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["EncryptionConfigProperty", _IResolvable_9ceae33e]]]]=None, name: typing.Optional[str]=None, version: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EKS::Cluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resources_vpc_config: ``AWS::EKS::Cluster.ResourcesVpcConfig``.
        :param role_arn: ``AWS::EKS::Cluster.RoleArn``.
        :param encryption_config: ``AWS::EKS::Cluster.EncryptionConfig``.
        :param name: ``AWS::EKS::Cluster.Name``.
        :param version: ``AWS::EKS::Cluster.Version``.
        """
        props = CfnClusterProps(resources_vpc_config=resources_vpc_config, role_arn=role_arn, encryption_config=encryption_config, name=name, version=version)

        jsii.create(CfnCluster, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnCluster":
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
    @jsii.member(jsii_name="attrCertificateAuthorityData")
    def attr_certificate_authority_data(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: CertificateAuthorityData
        """
        return jsii.get(self, "attrCertificateAuthorityData")

    @builtins.property
    @jsii.member(jsii_name="attrClusterSecurityGroupId")
    def attr_cluster_security_group_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ClusterSecurityGroupId
        """
        return jsii.get(self, "attrClusterSecurityGroupId")

    @builtins.property
    @jsii.member(jsii_name="attrEncryptionConfigKeyArn")
    def attr_encryption_config_key_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: EncryptionConfigKeyArn
        """
        return jsii.get(self, "attrEncryptionConfigKeyArn")

    @builtins.property
    @jsii.member(jsii_name="attrEndpoint")
    def attr_endpoint(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Endpoint
        """
        return jsii.get(self, "attrEndpoint")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="resourcesVpcConfig")
    def resources_vpc_config(self) -> typing.Union["ResourcesVpcConfigProperty", _IResolvable_9ceae33e]:
        """``AWS::EKS::Cluster.ResourcesVpcConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-resourcesvpcconfig
        """
        return jsii.get(self, "resourcesVpcConfig")

    @resources_vpc_config.setter
    def resources_vpc_config(self, value: typing.Union["ResourcesVpcConfigProperty", _IResolvable_9ceae33e]) -> None:
        jsii.set(self, "resourcesVpcConfig", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> str:
        """``AWS::EKS::Cluster.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter
    def role_arn(self, value: str) -> None:
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="encryptionConfig")
    def encryption_config(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["EncryptionConfigProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::EKS::Cluster.EncryptionConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-encryptionconfig
        """
        return jsii.get(self, "encryptionConfig")

    @encryption_config.setter
    def encryption_config(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["EncryptionConfigProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "encryptionConfig", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::EKS::Cluster.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> typing.Optional[str]:
        """``AWS::EKS::Cluster.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-version
        """
        return jsii.get(self, "version")

    @version.setter
    def version(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "version", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_eks_legacy.CfnCluster.EncryptionConfigProperty", jsii_struct_bases=[], name_mapping={'provider': 'provider', 'resources': 'resources'})
    class EncryptionConfigProperty():
        def __init__(self, *, provider: typing.Optional[typing.Union["CfnCluster.ProviderProperty", _IResolvable_9ceae33e]]=None, resources: typing.Optional[typing.List[str]]=None) -> None:
            """
            :param provider: ``CfnCluster.EncryptionConfigProperty.Provider``.
            :param resources: ``CfnCluster.EncryptionConfigProperty.Resources``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-encryptionconfig.html
            """
            self._values = {
            }
            if provider is not None: self._values["provider"] = provider
            if resources is not None: self._values["resources"] = resources

        @builtins.property
        def provider(self) -> typing.Optional[typing.Union["CfnCluster.ProviderProperty", _IResolvable_9ceae33e]]:
            """``CfnCluster.EncryptionConfigProperty.Provider``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-encryptionconfig.html#cfn-eks-cluster-encryptionconfig-provider
            """
            return self._values.get('provider')

        @builtins.property
        def resources(self) -> typing.Optional[typing.List[str]]:
            """``CfnCluster.EncryptionConfigProperty.Resources``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-encryptionconfig.html#cfn-eks-cluster-encryptionconfig-resources
            """
            return self._values.get('resources')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EncryptionConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_eks_legacy.CfnCluster.ProviderProperty", jsii_struct_bases=[], name_mapping={'key_arn': 'keyArn'})
    class ProviderProperty():
        def __init__(self, *, key_arn: typing.Optional[str]=None) -> None:
            """
            :param key_arn: ``CfnCluster.ProviderProperty.KeyArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-provider.html
            """
            self._values = {
            }
            if key_arn is not None: self._values["key_arn"] = key_arn

        @builtins.property
        def key_arn(self) -> typing.Optional[str]:
            """``CfnCluster.ProviderProperty.KeyArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-provider.html#cfn-eks-cluster-provider-keyarn
            """
            return self._values.get('key_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ProviderProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_eks_legacy.CfnCluster.ResourcesVpcConfigProperty", jsii_struct_bases=[], name_mapping={'subnet_ids': 'subnetIds', 'security_group_ids': 'securityGroupIds'})
    class ResourcesVpcConfigProperty():
        def __init__(self, *, subnet_ids: typing.List[str], security_group_ids: typing.Optional[typing.List[str]]=None) -> None:
            """
            :param subnet_ids: ``CfnCluster.ResourcesVpcConfigProperty.SubnetIds``.
            :param security_group_ids: ``CfnCluster.ResourcesVpcConfigProperty.SecurityGroupIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-resourcesvpcconfig.html
            """
            self._values = {
                'subnet_ids': subnet_ids,
            }
            if security_group_ids is not None: self._values["security_group_ids"] = security_group_ids

        @builtins.property
        def subnet_ids(self) -> typing.List[str]:
            """``CfnCluster.ResourcesVpcConfigProperty.SubnetIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-resourcesvpcconfig.html#cfn-eks-cluster-resourcesvpcconfig-subnetids
            """
            return self._values.get('subnet_ids')

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[str]]:
            """``CfnCluster.ResourcesVpcConfigProperty.SecurityGroupIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-resourcesvpcconfig.html#cfn-eks-cluster-resourcesvpcconfig-securitygroupids
            """
            return self._values.get('security_group_ids')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ResourcesVpcConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_eks_legacy.CfnClusterProps", jsii_struct_bases=[], name_mapping={'resources_vpc_config': 'resourcesVpcConfig', 'role_arn': 'roleArn', 'encryption_config': 'encryptionConfig', 'name': 'name', 'version': 'version'})
class CfnClusterProps():
    def __init__(self, *, resources_vpc_config: typing.Union["CfnCluster.ResourcesVpcConfigProperty", _IResolvable_9ceae33e], role_arn: str, encryption_config: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnCluster.EncryptionConfigProperty", _IResolvable_9ceae33e]]]]=None, name: typing.Optional[str]=None, version: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::EKS::Cluster``.

        :param resources_vpc_config: ``AWS::EKS::Cluster.ResourcesVpcConfig``.
        :param role_arn: ``AWS::EKS::Cluster.RoleArn``.
        :param encryption_config: ``AWS::EKS::Cluster.EncryptionConfig``.
        :param name: ``AWS::EKS::Cluster.Name``.
        :param version: ``AWS::EKS::Cluster.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html
        """
        self._values = {
            'resources_vpc_config': resources_vpc_config,
            'role_arn': role_arn,
        }
        if encryption_config is not None: self._values["encryption_config"] = encryption_config
        if name is not None: self._values["name"] = name
        if version is not None: self._values["version"] = version

    @builtins.property
    def resources_vpc_config(self) -> typing.Union["CfnCluster.ResourcesVpcConfigProperty", _IResolvable_9ceae33e]:
        """``AWS::EKS::Cluster.ResourcesVpcConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-resourcesvpcconfig
        """
        return self._values.get('resources_vpc_config')

    @builtins.property
    def role_arn(self) -> str:
        """``AWS::EKS::Cluster.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-rolearn
        """
        return self._values.get('role_arn')

    @builtins.property
    def encryption_config(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnCluster.EncryptionConfigProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::EKS::Cluster.EncryptionConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-encryptionconfig
        """
        return self._values.get('encryption_config')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::EKS::Cluster.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-name
        """
        return self._values.get('name')

    @builtins.property
    def version(self) -> typing.Optional[str]:
        """``AWS::EKS::Cluster.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-version
        """
        return self._values.get('version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnClusterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnNodegroup(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_eks_legacy.CfnNodegroup"):
    """A CloudFormation ``AWS::EKS::Nodegroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::EKS::Nodegroup
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, cluster_name: str, node_role: str, subnets: typing.List[str], ami_type: typing.Optional[str]=None, disk_size: typing.Optional[jsii.Number]=None, force_update_enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, instance_types: typing.Optional[typing.List[str]]=None, labels: typing.Any=None, nodegroup_name: typing.Optional[str]=None, release_version: typing.Optional[str]=None, remote_access: typing.Optional[typing.Union["RemoteAccessProperty", _IResolvable_9ceae33e]]=None, scaling_config: typing.Optional[typing.Union["ScalingConfigProperty", _IResolvable_9ceae33e]]=None, tags: typing.Any=None, version: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EKS::Nodegroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cluster_name: ``AWS::EKS::Nodegroup.ClusterName``.
        :param node_role: ``AWS::EKS::Nodegroup.NodeRole``.
        :param subnets: ``AWS::EKS::Nodegroup.Subnets``.
        :param ami_type: ``AWS::EKS::Nodegroup.AmiType``.
        :param disk_size: ``AWS::EKS::Nodegroup.DiskSize``.
        :param force_update_enabled: ``AWS::EKS::Nodegroup.ForceUpdateEnabled``.
        :param instance_types: ``AWS::EKS::Nodegroup.InstanceTypes``.
        :param labels: ``AWS::EKS::Nodegroup.Labels``.
        :param nodegroup_name: ``AWS::EKS::Nodegroup.NodegroupName``.
        :param release_version: ``AWS::EKS::Nodegroup.ReleaseVersion``.
        :param remote_access: ``AWS::EKS::Nodegroup.RemoteAccess``.
        :param scaling_config: ``AWS::EKS::Nodegroup.ScalingConfig``.
        :param tags: ``AWS::EKS::Nodegroup.Tags``.
        :param version: ``AWS::EKS::Nodegroup.Version``.
        """
        props = CfnNodegroupProps(cluster_name=cluster_name, node_role=node_role, subnets=subnets, ami_type=ami_type, disk_size=disk_size, force_update_enabled=force_update_enabled, instance_types=instance_types, labels=labels, nodegroup_name=nodegroup_name, release_version=release_version, remote_access=remote_access, scaling_config=scaling_config, tags=tags, version=version)

        jsii.create(CfnNodegroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnNodegroup":
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
    @jsii.member(jsii_name="attrClusterName")
    def attr_cluster_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ClusterName
        """
        return jsii.get(self, "attrClusterName")

    @builtins.property
    @jsii.member(jsii_name="attrNodegroupName")
    def attr_nodegroup_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: NodegroupName
        """
        return jsii.get(self, "attrNodegroupName")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::EKS::Nodegroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """``AWS::EKS::Nodegroup.ClusterName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-clustername
        """
        return jsii.get(self, "clusterName")

    @cluster_name.setter
    def cluster_name(self, value: str) -> None:
        jsii.set(self, "clusterName", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Any:
        """``AWS::EKS::Nodegroup.Labels``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-labels
        """
        return jsii.get(self, "labels")

    @labels.setter
    def labels(self, value: typing.Any) -> None:
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="nodeRole")
    def node_role(self) -> str:
        """``AWS::EKS::Nodegroup.NodeRole``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-noderole
        """
        return jsii.get(self, "nodeRole")

    @node_role.setter
    def node_role(self, value: str) -> None:
        jsii.set(self, "nodeRole", value)

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.List[str]:
        """``AWS::EKS::Nodegroup.Subnets``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-subnets
        """
        return jsii.get(self, "subnets")

    @subnets.setter
    def subnets(self, value: typing.List[str]) -> None:
        jsii.set(self, "subnets", value)

    @builtins.property
    @jsii.member(jsii_name="amiType")
    def ami_type(self) -> typing.Optional[str]:
        """``AWS::EKS::Nodegroup.AmiType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-amitype
        """
        return jsii.get(self, "amiType")

    @ami_type.setter
    def ami_type(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "amiType", value)

    @builtins.property
    @jsii.member(jsii_name="diskSize")
    def disk_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::EKS::Nodegroup.DiskSize``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-disksize
        """
        return jsii.get(self, "diskSize")

    @disk_size.setter
    def disk_size(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "diskSize", value)

    @builtins.property
    @jsii.member(jsii_name="forceUpdateEnabled")
    def force_update_enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::EKS::Nodegroup.ForceUpdateEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-forceupdateenabled
        """
        return jsii.get(self, "forceUpdateEnabled")

    @force_update_enabled.setter
    def force_update_enabled(self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "forceUpdateEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="instanceTypes")
    def instance_types(self) -> typing.Optional[typing.List[str]]:
        """``AWS::EKS::Nodegroup.InstanceTypes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-instancetypes
        """
        return jsii.get(self, "instanceTypes")

    @instance_types.setter
    def instance_types(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "instanceTypes", value)

    @builtins.property
    @jsii.member(jsii_name="nodegroupName")
    def nodegroup_name(self) -> typing.Optional[str]:
        """``AWS::EKS::Nodegroup.NodegroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-nodegroupname
        """
        return jsii.get(self, "nodegroupName")

    @nodegroup_name.setter
    def nodegroup_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "nodegroupName", value)

    @builtins.property
    @jsii.member(jsii_name="releaseVersion")
    def release_version(self) -> typing.Optional[str]:
        """``AWS::EKS::Nodegroup.ReleaseVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-releaseversion
        """
        return jsii.get(self, "releaseVersion")

    @release_version.setter
    def release_version(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "releaseVersion", value)

    @builtins.property
    @jsii.member(jsii_name="remoteAccess")
    def remote_access(self) -> typing.Optional[typing.Union["RemoteAccessProperty", _IResolvable_9ceae33e]]:
        """``AWS::EKS::Nodegroup.RemoteAccess``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-remoteaccess
        """
        return jsii.get(self, "remoteAccess")

    @remote_access.setter
    def remote_access(self, value: typing.Optional[typing.Union["RemoteAccessProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "remoteAccess", value)

    @builtins.property
    @jsii.member(jsii_name="scalingConfig")
    def scaling_config(self) -> typing.Optional[typing.Union["ScalingConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::EKS::Nodegroup.ScalingConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-scalingconfig
        """
        return jsii.get(self, "scalingConfig")

    @scaling_config.setter
    def scaling_config(self, value: typing.Optional[typing.Union["ScalingConfigProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "scalingConfig", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> typing.Optional[str]:
        """``AWS::EKS::Nodegroup.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-version
        """
        return jsii.get(self, "version")

    @version.setter
    def version(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "version", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_eks_legacy.CfnNodegroup.RemoteAccessProperty", jsii_struct_bases=[], name_mapping={'ec2_ssh_key': 'ec2SshKey', 'source_security_groups': 'sourceSecurityGroups'})
    class RemoteAccessProperty():
        def __init__(self, *, ec2_ssh_key: str, source_security_groups: typing.Optional[typing.List[str]]=None) -> None:
            """
            :param ec2_ssh_key: ``CfnNodegroup.RemoteAccessProperty.Ec2SshKey``.
            :param source_security_groups: ``CfnNodegroup.RemoteAccessProperty.SourceSecurityGroups``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-remoteaccess.html
            """
            self._values = {
                'ec2_ssh_key': ec2_ssh_key,
            }
            if source_security_groups is not None: self._values["source_security_groups"] = source_security_groups

        @builtins.property
        def ec2_ssh_key(self) -> str:
            """``CfnNodegroup.RemoteAccessProperty.Ec2SshKey``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-remoteaccess.html#cfn-eks-nodegroup-remoteaccess-ec2sshkey
            """
            return self._values.get('ec2_ssh_key')

        @builtins.property
        def source_security_groups(self) -> typing.Optional[typing.List[str]]:
            """``CfnNodegroup.RemoteAccessProperty.SourceSecurityGroups``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-remoteaccess.html#cfn-eks-nodegroup-remoteaccess-sourcesecuritygroups
            """
            return self._values.get('source_security_groups')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RemoteAccessProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_eks_legacy.CfnNodegroup.ScalingConfigProperty", jsii_struct_bases=[], name_mapping={'desired_size': 'desiredSize', 'max_size': 'maxSize', 'min_size': 'minSize'})
    class ScalingConfigProperty():
        def __init__(self, *, desired_size: typing.Optional[jsii.Number]=None, max_size: typing.Optional[jsii.Number]=None, min_size: typing.Optional[jsii.Number]=None) -> None:
            """
            :param desired_size: ``CfnNodegroup.ScalingConfigProperty.DesiredSize``.
            :param max_size: ``CfnNodegroup.ScalingConfigProperty.MaxSize``.
            :param min_size: ``CfnNodegroup.ScalingConfigProperty.MinSize``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-scalingconfig.html
            """
            self._values = {
            }
            if desired_size is not None: self._values["desired_size"] = desired_size
            if max_size is not None: self._values["max_size"] = max_size
            if min_size is not None: self._values["min_size"] = min_size

        @builtins.property
        def desired_size(self) -> typing.Optional[jsii.Number]:
            """``CfnNodegroup.ScalingConfigProperty.DesiredSize``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-scalingconfig.html#cfn-eks-nodegroup-scalingconfig-desiredsize
            """
            return self._values.get('desired_size')

        @builtins.property
        def max_size(self) -> typing.Optional[jsii.Number]:
            """``CfnNodegroup.ScalingConfigProperty.MaxSize``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-scalingconfig.html#cfn-eks-nodegroup-scalingconfig-maxsize
            """
            return self._values.get('max_size')

        @builtins.property
        def min_size(self) -> typing.Optional[jsii.Number]:
            """``CfnNodegroup.ScalingConfigProperty.MinSize``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-scalingconfig.html#cfn-eks-nodegroup-scalingconfig-minsize
            """
            return self._values.get('min_size')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ScalingConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_eks_legacy.CfnNodegroupProps", jsii_struct_bases=[], name_mapping={'cluster_name': 'clusterName', 'node_role': 'nodeRole', 'subnets': 'subnets', 'ami_type': 'amiType', 'disk_size': 'diskSize', 'force_update_enabled': 'forceUpdateEnabled', 'instance_types': 'instanceTypes', 'labels': 'labels', 'nodegroup_name': 'nodegroupName', 'release_version': 'releaseVersion', 'remote_access': 'remoteAccess', 'scaling_config': 'scalingConfig', 'tags': 'tags', 'version': 'version'})
class CfnNodegroupProps():
    def __init__(self, *, cluster_name: str, node_role: str, subnets: typing.List[str], ami_type: typing.Optional[str]=None, disk_size: typing.Optional[jsii.Number]=None, force_update_enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, instance_types: typing.Optional[typing.List[str]]=None, labels: typing.Any=None, nodegroup_name: typing.Optional[str]=None, release_version: typing.Optional[str]=None, remote_access: typing.Optional[typing.Union["CfnNodegroup.RemoteAccessProperty", _IResolvable_9ceae33e]]=None, scaling_config: typing.Optional[typing.Union["CfnNodegroup.ScalingConfigProperty", _IResolvable_9ceae33e]]=None, tags: typing.Any=None, version: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::EKS::Nodegroup``.

        :param cluster_name: ``AWS::EKS::Nodegroup.ClusterName``.
        :param node_role: ``AWS::EKS::Nodegroup.NodeRole``.
        :param subnets: ``AWS::EKS::Nodegroup.Subnets``.
        :param ami_type: ``AWS::EKS::Nodegroup.AmiType``.
        :param disk_size: ``AWS::EKS::Nodegroup.DiskSize``.
        :param force_update_enabled: ``AWS::EKS::Nodegroup.ForceUpdateEnabled``.
        :param instance_types: ``AWS::EKS::Nodegroup.InstanceTypes``.
        :param labels: ``AWS::EKS::Nodegroup.Labels``.
        :param nodegroup_name: ``AWS::EKS::Nodegroup.NodegroupName``.
        :param release_version: ``AWS::EKS::Nodegroup.ReleaseVersion``.
        :param remote_access: ``AWS::EKS::Nodegroup.RemoteAccess``.
        :param scaling_config: ``AWS::EKS::Nodegroup.ScalingConfig``.
        :param tags: ``AWS::EKS::Nodegroup.Tags``.
        :param version: ``AWS::EKS::Nodegroup.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html
        """
        self._values = {
            'cluster_name': cluster_name,
            'node_role': node_role,
            'subnets': subnets,
        }
        if ami_type is not None: self._values["ami_type"] = ami_type
        if disk_size is not None: self._values["disk_size"] = disk_size
        if force_update_enabled is not None: self._values["force_update_enabled"] = force_update_enabled
        if instance_types is not None: self._values["instance_types"] = instance_types
        if labels is not None: self._values["labels"] = labels
        if nodegroup_name is not None: self._values["nodegroup_name"] = nodegroup_name
        if release_version is not None: self._values["release_version"] = release_version
        if remote_access is not None: self._values["remote_access"] = remote_access
        if scaling_config is not None: self._values["scaling_config"] = scaling_config
        if tags is not None: self._values["tags"] = tags
        if version is not None: self._values["version"] = version

    @builtins.property
    def cluster_name(self) -> str:
        """``AWS::EKS::Nodegroup.ClusterName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-clustername
        """
        return self._values.get('cluster_name')

    @builtins.property
    def node_role(self) -> str:
        """``AWS::EKS::Nodegroup.NodeRole``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-noderole
        """
        return self._values.get('node_role')

    @builtins.property
    def subnets(self) -> typing.List[str]:
        """``AWS::EKS::Nodegroup.Subnets``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-subnets
        """
        return self._values.get('subnets')

    @builtins.property
    def ami_type(self) -> typing.Optional[str]:
        """``AWS::EKS::Nodegroup.AmiType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-amitype
        """
        return self._values.get('ami_type')

    @builtins.property
    def disk_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::EKS::Nodegroup.DiskSize``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-disksize
        """
        return self._values.get('disk_size')

    @builtins.property
    def force_update_enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::EKS::Nodegroup.ForceUpdateEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-forceupdateenabled
        """
        return self._values.get('force_update_enabled')

    @builtins.property
    def instance_types(self) -> typing.Optional[typing.List[str]]:
        """``AWS::EKS::Nodegroup.InstanceTypes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-instancetypes
        """
        return self._values.get('instance_types')

    @builtins.property
    def labels(self) -> typing.Any:
        """``AWS::EKS::Nodegroup.Labels``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-labels
        """
        return self._values.get('labels')

    @builtins.property
    def nodegroup_name(self) -> typing.Optional[str]:
        """``AWS::EKS::Nodegroup.NodegroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-nodegroupname
        """
        return self._values.get('nodegroup_name')

    @builtins.property
    def release_version(self) -> typing.Optional[str]:
        """``AWS::EKS::Nodegroup.ReleaseVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-releaseversion
        """
        return self._values.get('release_version')

    @builtins.property
    def remote_access(self) -> typing.Optional[typing.Union["CfnNodegroup.RemoteAccessProperty", _IResolvable_9ceae33e]]:
        """``AWS::EKS::Nodegroup.RemoteAccess``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-remoteaccess
        """
        return self._values.get('remote_access')

    @builtins.property
    def scaling_config(self) -> typing.Optional[typing.Union["CfnNodegroup.ScalingConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::EKS::Nodegroup.ScalingConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-scalingconfig
        """
        return self._values.get('scaling_config')

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::EKS::Nodegroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-tags
        """
        return self._values.get('tags')

    @builtins.property
    def version(self) -> typing.Optional[str]:
        """``AWS::EKS::Nodegroup.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-version
        """
        return self._values.get('version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnNodegroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_eks_legacy.ClusterAttributes", jsii_struct_bases=[], name_mapping={'cluster_arn': 'clusterArn', 'cluster_certificate_authority_data': 'clusterCertificateAuthorityData', 'cluster_endpoint': 'clusterEndpoint', 'cluster_name': 'clusterName', 'security_groups': 'securityGroups', 'vpc': 'vpc'})
class ClusterAttributes():
    def __init__(self, *, cluster_arn: str, cluster_certificate_authority_data: str, cluster_endpoint: str, cluster_name: str, security_groups: typing.List[_ISecurityGroup_d72ab8e8], vpc: _IVpc_3795853f) -> None:
        """
        :param cluster_arn: The unique ARN assigned to the service by AWS in the form of arn:aws:eks:.
        :param cluster_certificate_authority_data: The certificate-authority-data for your cluster.
        :param cluster_endpoint: The API Server endpoint URL.
        :param cluster_name: The physical name of the Cluster.
        :param security_groups: The security groups associated with this cluster.
        :param vpc: The VPC in which this Cluster was created.

        stability
        :stability: experimental
        """
        self._values = {
            'cluster_arn': cluster_arn,
            'cluster_certificate_authority_data': cluster_certificate_authority_data,
            'cluster_endpoint': cluster_endpoint,
            'cluster_name': cluster_name,
            'security_groups': security_groups,
            'vpc': vpc,
        }

    @builtins.property
    def cluster_arn(self) -> str:
        """The unique ARN assigned to the service by AWS in the form of arn:aws:eks:.

        stability
        :stability: experimental
        """
        return self._values.get('cluster_arn')

    @builtins.property
    def cluster_certificate_authority_data(self) -> str:
        """The certificate-authority-data for your cluster.

        stability
        :stability: experimental
        """
        return self._values.get('cluster_certificate_authority_data')

    @builtins.property
    def cluster_endpoint(self) -> str:
        """The API Server endpoint URL.

        stability
        :stability: experimental
        """
        return self._values.get('cluster_endpoint')

    @builtins.property
    def cluster_name(self) -> str:
        """The physical name of the Cluster.

        stability
        :stability: experimental
        """
        return self._values.get('cluster_name')

    @builtins.property
    def security_groups(self) -> typing.List[_ISecurityGroup_d72ab8e8]:
        """The security groups associated with this cluster.

        stability
        :stability: experimental
        """
        return self._values.get('security_groups')

    @builtins.property
    def vpc(self) -> _IVpc_3795853f:
        """The VPC in which this Cluster was created.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ClusterAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_eks_legacy.ClusterProps", jsii_struct_bases=[], name_mapping={'cluster_name': 'clusterName', 'default_capacity': 'defaultCapacity', 'default_capacity_instance': 'defaultCapacityInstance', 'kubectl_enabled': 'kubectlEnabled', 'masters_role': 'mastersRole', 'output_cluster_name': 'outputClusterName', 'output_config_command': 'outputConfigCommand', 'output_masters_role_arn': 'outputMastersRoleArn', 'role': 'role', 'security_group': 'securityGroup', 'version': 'version', 'vpc': 'vpc', 'vpc_subnets': 'vpcSubnets'})
class ClusterProps():
    def __init__(self, *, cluster_name: typing.Optional[str]=None, default_capacity: typing.Optional[jsii.Number]=None, default_capacity_instance: typing.Optional[_InstanceType_85a97b30]=None, kubectl_enabled: typing.Optional[bool]=None, masters_role: typing.Optional[_IRole_e69bbae4]=None, output_cluster_name: typing.Optional[bool]=None, output_config_command: typing.Optional[bool]=None, output_masters_role_arn: typing.Optional[bool]=None, role: typing.Optional[_IRole_e69bbae4]=None, security_group: typing.Optional[_ISecurityGroup_d72ab8e8]=None, version: typing.Optional[str]=None, vpc: typing.Optional[_IVpc_3795853f]=None, vpc_subnets: typing.Optional[typing.List[_SubnetSelection_36a13cd6]]=None) -> None:
        """Properties to instantiate the Cluster.

        :param cluster_name: Name for the cluster. Default: - Automatically generated name
        :param default_capacity: Number of instances to allocate as an initial capacity for this cluster. Instance type can be configured through ``defaultCapacityInstanceType``, which defaults to ``m5.large``. Use ``cluster.addCapacity`` to add additional customized capacity. Set this to ``0`` is you wish to avoid the initial capacity allocation. Default: 2
        :param default_capacity_instance: The instance type to use for the default capacity. This will only be taken into account if ``defaultCapacity`` is > 0. Default: m5.large
        :param kubectl_enabled: Allows defining ``kubectrl``-related resources on this cluster. If this is disabled, it will not be possible to use the following capabilities: - ``addResource`` - ``addRoleMapping`` - ``addUserMapping`` - ``addMastersRole`` and ``props.mastersRole`` If this is disabled, the cluster can only be managed by issuing ``kubectl`` commands from a session that uses the IAM role/user that created the account. *NOTE*: changing this value will destoy the cluster. This is because a managable cluster must be created using an AWS CloudFormation custom resource which executes with an IAM role owned by the CDK app. Default: true The cluster can be managed by the AWS CDK application.
        :param masters_role: An IAM role that will be added to the ``system:masters`` Kubernetes RBAC group. Default: - By default, it will only possible to update this Kubernetes system by adding resources to this cluster via ``addResource`` or by defining ``KubernetesResource`` resources in your AWS CDK app. Use this if you wish to grant cluster administration privileges to another role.
        :param output_cluster_name: Determines whether a CloudFormation output with the name of the cluster will be synthesized. Default: false
        :param output_config_command: Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized. This command will include the cluster name and, if applicable, the ARN of the masters IAM role. Default: true
        :param output_masters_role_arn: Determines whether a CloudFormation output with the ARN of the "masters" IAM role will be synthesized (if ``mastersRole`` is specified). Default: false
        :param role: Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf. Default: - A role is automatically created for you
        :param security_group: Security Group to use for Control Plane ENIs. Default: - A security group is automatically created
        :param version: The Kubernetes version to run in the cluster. Default: - If not supplied, will use Amazon default version
        :param vpc: The VPC in which to create the Cluster. Default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.
        :param vpc_subnets: Where to place EKS Control Plane ENIs. If you want to create public load balancers, this must include public subnets. For example, to only select private subnets, supply the following:: vpcSubnets: [ { subnetType: ec2.SubnetType.Private } ] Default: - All public and private subnets

        stability
        :stability: experimental
        """
        self._values = {
        }
        if cluster_name is not None: self._values["cluster_name"] = cluster_name
        if default_capacity is not None: self._values["default_capacity"] = default_capacity
        if default_capacity_instance is not None: self._values["default_capacity_instance"] = default_capacity_instance
        if kubectl_enabled is not None: self._values["kubectl_enabled"] = kubectl_enabled
        if masters_role is not None: self._values["masters_role"] = masters_role
        if output_cluster_name is not None: self._values["output_cluster_name"] = output_cluster_name
        if output_config_command is not None: self._values["output_config_command"] = output_config_command
        if output_masters_role_arn is not None: self._values["output_masters_role_arn"] = output_masters_role_arn
        if role is not None: self._values["role"] = role
        if security_group is not None: self._values["security_group"] = security_group
        if version is not None: self._values["version"] = version
        if vpc is not None: self._values["vpc"] = vpc
        if vpc_subnets is not None: self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def cluster_name(self) -> typing.Optional[str]:
        """Name for the cluster.

        default
        :default: - Automatically generated name

        stability
        :stability: experimental
        """
        return self._values.get('cluster_name')

    @builtins.property
    def default_capacity(self) -> typing.Optional[jsii.Number]:
        """Number of instances to allocate as an initial capacity for this cluster.

        Instance type can be configured through ``defaultCapacityInstanceType``,
        which defaults to ``m5.large``.

        Use ``cluster.addCapacity`` to add additional customized capacity. Set this
        to ``0`` is you wish to avoid the initial capacity allocation.

        default
        :default: 2

        stability
        :stability: experimental
        """
        return self._values.get('default_capacity')

    @builtins.property
    def default_capacity_instance(self) -> typing.Optional[_InstanceType_85a97b30]:
        """The instance type to use for the default capacity.

        This will only be taken
        into account if ``defaultCapacity`` is > 0.

        default
        :default: m5.large

        stability
        :stability: experimental
        """
        return self._values.get('default_capacity_instance')

    @builtins.property
    def kubectl_enabled(self) -> typing.Optional[bool]:
        """Allows defining ``kubectrl``-related resources on this cluster.

        If this is disabled, it will not be possible to use the following
        capabilities:

        - ``addResource``
        - ``addRoleMapping``
        - ``addUserMapping``
        - ``addMastersRole`` and ``props.mastersRole``

        If this is disabled, the cluster can only be managed by issuing ``kubectl``
        commands from a session that uses the IAM role/user that created the
        account.

        *NOTE*: changing this value will destoy the cluster. This is because a
        managable cluster must be created using an AWS CloudFormation custom
        resource which executes with an IAM role owned by the CDK app.

        default
        :default: true The cluster can be managed by the AWS CDK application.

        stability
        :stability: experimental
        """
        return self._values.get('kubectl_enabled')

    @builtins.property
    def masters_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """An IAM role that will be added to the ``system:masters`` Kubernetes RBAC group.

        default
        :default:

        - By default, it will only possible to update this Kubernetes
          system by adding resources to this cluster via ``addResource`` or
          by defining ``KubernetesResource`` resources in your AWS CDK app.
          Use this if you wish to grant cluster administration privileges
          to another role.

        see
        :see: https://kubernetes.io/docs/reference/access-authn-authz/rbac/#default-roles-and-role-bindings
        stability
        :stability: experimental
        """
        return self._values.get('masters_role')

    @builtins.property
    def output_cluster_name(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the name of the cluster will be synthesized.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('output_cluster_name')

    @builtins.property
    def output_config_command(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized.

        This command will include
        the cluster name and, if applicable, the ARN of the masters IAM role.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('output_config_command')

    @builtins.property
    def output_masters_role_arn(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the ARN of the "masters" IAM role will be synthesized (if ``mastersRole`` is specified).

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('output_masters_role_arn')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf.

        default
        :default: - A role is automatically created for you

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_d72ab8e8]:
        """Security Group to use for Control Plane ENIs.

        default
        :default: - A security group is automatically created

        stability
        :stability: experimental
        """
        return self._values.get('security_group')

    @builtins.property
    def version(self) -> typing.Optional[str]:
        """The Kubernetes version to run in the cluster.

        default
        :default: - If not supplied, will use Amazon default version

        stability
        :stability: experimental
        """
        return self._values.get('version')

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC in which to create the Cluster.

        default
        :default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[typing.List[_SubnetSelection_36a13cd6]]:
        """Where to place EKS Control Plane ENIs.

        If you want to create public load balancers, this must include public subnets.

        For example, to only select private subnets, supply the following::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           vpcSubnets: [
              { subnetType: ec2.SubnetType.Private }
           ]

        default
        :default: - All public and private subnets

        stability
        :stability: experimental
        """
        return self._values.get('vpc_subnets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ClusterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IMachineImage_d5cd7b45)
class EksOptimizedImage(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_eks_legacy.EksOptimizedImage"):
    """Construct an Amazon Linux 2 image from the latest EKS Optimized AMI published in SSM.

    stability
    :stability: experimental
    """
    def __init__(self, *, kubernetes_version: typing.Optional[str]=None, node_type: typing.Optional["NodeType"]=None) -> None:
        """Constructs a new instance of the EcsOptimizedAmi class.

        :param kubernetes_version: The Kubernetes version to use. Default: - The latest version
        :param node_type: What instance type to retrieve the image for (standard or GPU-optimized). Default: NodeType.STANDARD

        stability
        :stability: experimental
        """
        props = EksOptimizedImageProps(kubernetes_version=kubernetes_version, node_type=node_type)

        jsii.create(EksOptimizedImage, self, [props])

    @jsii.member(jsii_name="getImage")
    def get_image(self, scope: _Construct_f50a3f53) -> _MachineImageConfig_815fc1b9:
        """Return the correct image.

        :param scope: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getImage", [scope])


@jsii.data_type(jsii_type="monocdk-experiment.aws_eks_legacy.EksOptimizedImageProps", jsii_struct_bases=[], name_mapping={'kubernetes_version': 'kubernetesVersion', 'node_type': 'nodeType'})
class EksOptimizedImageProps():
    def __init__(self, *, kubernetes_version: typing.Optional[str]=None, node_type: typing.Optional["NodeType"]=None) -> None:
        """Properties for EksOptimizedImage.

        :param kubernetes_version: The Kubernetes version to use. Default: - The latest version
        :param node_type: What instance type to retrieve the image for (standard or GPU-optimized). Default: NodeType.STANDARD

        stability
        :stability: experimental
        """
        self._values = {
        }
        if kubernetes_version is not None: self._values["kubernetes_version"] = kubernetes_version
        if node_type is not None: self._values["node_type"] = node_type

    @builtins.property
    def kubernetes_version(self) -> typing.Optional[str]:
        """The Kubernetes version to use.

        default
        :default: - The latest version

        stability
        :stability: experimental
        """
        return self._values.get('kubernetes_version')

    @builtins.property
    def node_type(self) -> typing.Optional["NodeType"]:
        """What instance type to retrieve the image for (standard or GPU-optimized).

        default
        :default: NodeType.STANDARD

        stability
        :stability: experimental
        """
        return self._values.get('node_type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EksOptimizedImageProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class HelmChart(_Construct_f50a3f53, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_eks_legacy.HelmChart"):
    """Represents a helm chart within the Kubernetes system.

    Applies/deletes the resources using ``kubectl`` in sync with the resource.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, cluster: "Cluster", chart: str, namespace: typing.Optional[str]=None, release: typing.Optional[str]=None, repository: typing.Optional[str]=None, values: typing.Optional[typing.Mapping[str, typing.Any]]=None, version: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster: The EKS cluster to apply this configuration to. [disable-awslint:ref-via-interface]
        :param chart: The name of the chart.
        :param namespace: The Kubernetes namespace scope of the requests. Default: default
        :param release: The name of the release. Default: - If no release name is given, it will use the last 63 characters of the node's unique id.
        :param repository: The repository which contains the chart. For example: https://kubernetes-charts.storage.googleapis.com/ Default: - No repository will be used, which means that the chart needs to be an absolute URL.
        :param values: The values to be used by the chart. Default: - No values are provided to the chart.
        :param version: The chart version to install. Default: - If this is not specified, the latest version is installed

        stability
        :stability: experimental
        """
        props = HelmChartProps(cluster=cluster, chart=chart, namespace=namespace, release=release, repository=repository, values=values, version=version)

        jsii.create(HelmChart, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="RESOURCE_TYPE")
    def RESOURCE_TYPE(cls) -> str:
        """The CloudFormation reosurce type.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "RESOURCE_TYPE")


@jsii.data_type(jsii_type="monocdk-experiment.aws_eks_legacy.HelmChartOptions", jsii_struct_bases=[], name_mapping={'chart': 'chart', 'namespace': 'namespace', 'release': 'release', 'repository': 'repository', 'values': 'values', 'version': 'version'})
class HelmChartOptions():
    def __init__(self, *, chart: str, namespace: typing.Optional[str]=None, release: typing.Optional[str]=None, repository: typing.Optional[str]=None, values: typing.Optional[typing.Mapping[str, typing.Any]]=None, version: typing.Optional[str]=None) -> None:
        """Helm Chart options.

        :param chart: The name of the chart.
        :param namespace: The Kubernetes namespace scope of the requests. Default: default
        :param release: The name of the release. Default: - If no release name is given, it will use the last 63 characters of the node's unique id.
        :param repository: The repository which contains the chart. For example: https://kubernetes-charts.storage.googleapis.com/ Default: - No repository will be used, which means that the chart needs to be an absolute URL.
        :param values: The values to be used by the chart. Default: - No values are provided to the chart.
        :param version: The chart version to install. Default: - If this is not specified, the latest version is installed

        stability
        :stability: experimental
        """
        self._values = {
            'chart': chart,
        }
        if namespace is not None: self._values["namespace"] = namespace
        if release is not None: self._values["release"] = release
        if repository is not None: self._values["repository"] = repository
        if values is not None: self._values["values"] = values
        if version is not None: self._values["version"] = version

    @builtins.property
    def chart(self) -> str:
        """The name of the chart.

        stability
        :stability: experimental
        """
        return self._values.get('chart')

    @builtins.property
    def namespace(self) -> typing.Optional[str]:
        """The Kubernetes namespace scope of the requests.

        default
        :default: default

        stability
        :stability: experimental
        """
        return self._values.get('namespace')

    @builtins.property
    def release(self) -> typing.Optional[str]:
        """The name of the release.

        default
        :default: - If no release name is given, it will use the last 63 characters of the node's unique id.

        stability
        :stability: experimental
        """
        return self._values.get('release')

    @builtins.property
    def repository(self) -> typing.Optional[str]:
        """The repository which contains the chart.

        For example: https://kubernetes-charts.storage.googleapis.com/

        default
        :default: - No repository will be used, which means that the chart needs to be an absolute URL.

        stability
        :stability: experimental
        """
        return self._values.get('repository')

    @builtins.property
    def values(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """The values to be used by the chart.

        default
        :default: - No values are provided to the chart.

        stability
        :stability: experimental
        """
        return self._values.get('values')

    @builtins.property
    def version(self) -> typing.Optional[str]:
        """The chart version to install.

        default
        :default: - If this is not specified, the latest version is installed

        stability
        :stability: experimental
        """
        return self._values.get('version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HelmChartOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_eks_legacy.HelmChartProps", jsii_struct_bases=[HelmChartOptions], name_mapping={'chart': 'chart', 'namespace': 'namespace', 'release': 'release', 'repository': 'repository', 'values': 'values', 'version': 'version', 'cluster': 'cluster'})
class HelmChartProps(HelmChartOptions):
    def __init__(self, *, chart: str, namespace: typing.Optional[str]=None, release: typing.Optional[str]=None, repository: typing.Optional[str]=None, values: typing.Optional[typing.Mapping[str, typing.Any]]=None, version: typing.Optional[str]=None, cluster: "Cluster") -> None:
        """Helm Chart properties.

        :param chart: The name of the chart.
        :param namespace: The Kubernetes namespace scope of the requests. Default: default
        :param release: The name of the release. Default: - If no release name is given, it will use the last 63 characters of the node's unique id.
        :param repository: The repository which contains the chart. For example: https://kubernetes-charts.storage.googleapis.com/ Default: - No repository will be used, which means that the chart needs to be an absolute URL.
        :param values: The values to be used by the chart. Default: - No values are provided to the chart.
        :param version: The chart version to install. Default: - If this is not specified, the latest version is installed
        :param cluster: The EKS cluster to apply this configuration to. [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        self._values = {
            'chart': chart,
            'cluster': cluster,
        }
        if namespace is not None: self._values["namespace"] = namespace
        if release is not None: self._values["release"] = release
        if repository is not None: self._values["repository"] = repository
        if values is not None: self._values["values"] = values
        if version is not None: self._values["version"] = version

    @builtins.property
    def chart(self) -> str:
        """The name of the chart.

        stability
        :stability: experimental
        """
        return self._values.get('chart')

    @builtins.property
    def namespace(self) -> typing.Optional[str]:
        """The Kubernetes namespace scope of the requests.

        default
        :default: default

        stability
        :stability: experimental
        """
        return self._values.get('namespace')

    @builtins.property
    def release(self) -> typing.Optional[str]:
        """The name of the release.

        default
        :default: - If no release name is given, it will use the last 63 characters of the node's unique id.

        stability
        :stability: experimental
        """
        return self._values.get('release')

    @builtins.property
    def repository(self) -> typing.Optional[str]:
        """The repository which contains the chart.

        For example: https://kubernetes-charts.storage.googleapis.com/

        default
        :default: - No repository will be used, which means that the chart needs to be an absolute URL.

        stability
        :stability: experimental
        """
        return self._values.get('repository')

    @builtins.property
    def values(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """The values to be used by the chart.

        default
        :default: - No values are provided to the chart.

        stability
        :stability: experimental
        """
        return self._values.get('values')

    @builtins.property
    def version(self) -> typing.Optional[str]:
        """The chart version to install.

        default
        :default: - If this is not specified, the latest version is installed

        stability
        :stability: experimental
        """
        return self._values.get('version')

    @builtins.property
    def cluster(self) -> "Cluster":
        """The EKS cluster to apply this configuration to.

        [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HelmChartProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="monocdk-experiment.aws_eks_legacy.ICluster")
class ICluster(_IResource_72f7ee7e, _IConnectable_a587039f, jsii.compat.Protocol):
    """An EKS cluster.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IClusterProxy

    @builtins.property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        """The unique ARN assigned to the service by AWS in the form of arn:aws:eks:.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="clusterCertificateAuthorityData")
    def cluster_certificate_authority_data(self) -> str:
        """The certificate-authority-data for your cluster.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> str:
        """The API Server endpoint URL.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """The physical name of the Cluster.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _IVpc_3795853f:
        """The VPC in which this Cluster was created.

        stability
        :stability: experimental
        """
        ...


class _IClusterProxy(jsii.proxy_for(_IResource_72f7ee7e), jsii.proxy_for(_IConnectable_a587039f)):
    """An EKS cluster.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_eks_legacy.ICluster"
    @builtins.property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        """The unique ARN assigned to the service by AWS in the form of arn:aws:eks:.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterArn")

    @builtins.property
    @jsii.member(jsii_name="clusterCertificateAuthorityData")
    def cluster_certificate_authority_data(self) -> str:
        """The certificate-authority-data for your cluster.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterCertificateAuthorityData")

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> str:
        """The API Server endpoint URL.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterEndpoint")

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """The physical name of the Cluster.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterName")

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _IVpc_3795853f:
        """The VPC in which this Cluster was created.

        stability
        :stability: experimental
        """
        return jsii.get(self, "vpc")


class KubernetesResource(_Construct_f50a3f53, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_eks_legacy.KubernetesResource"):
    """Represents a resource within the Kubernetes system.

    Alternatively, you can use ``cluster.addResource(resource[, resource, ...])``
    to define resources on this cluster.

    Applies/deletes the resources using ``kubectl`` in sync with the resource.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, cluster: "Cluster", manifest: typing.List[typing.Any]) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster: The EKS cluster to apply this configuration to. [disable-awslint:ref-via-interface]
        :param manifest: The resource manifest. Consists of any number of child resources. When the resource is created/updated, this manifest will be applied to the cluster through ``kubectl apply`` and when the resource or the stack is deleted, the manifest will be deleted through ``kubectl delete``.

        stability
        :stability: experimental
        """
        props = KubernetesResourceProps(cluster=cluster, manifest=manifest)

        jsii.create(KubernetesResource, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="RESOURCE_TYPE")
    def RESOURCE_TYPE(cls) -> str:
        """The CloudFormation reosurce type.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "RESOURCE_TYPE")


@jsii.data_type(jsii_type="monocdk-experiment.aws_eks_legacy.KubernetesResourceProps", jsii_struct_bases=[], name_mapping={'cluster': 'cluster', 'manifest': 'manifest'})
class KubernetesResourceProps():
    def __init__(self, *, cluster: "Cluster", manifest: typing.List[typing.Any]) -> None:
        """
        :param cluster: The EKS cluster to apply this configuration to. [disable-awslint:ref-via-interface]
        :param manifest: The resource manifest. Consists of any number of child resources. When the resource is created/updated, this manifest will be applied to the cluster through ``kubectl apply`` and when the resource or the stack is deleted, the manifest will be deleted through ``kubectl delete``.

        stability
        :stability: experimental
        """
        self._values = {
            'cluster': cluster,
            'manifest': manifest,
        }

    @builtins.property
    def cluster(self) -> "Cluster":
        """The EKS cluster to apply this configuration to.

        [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def manifest(self) -> typing.List[typing.Any]:
        """The resource manifest.

        Consists of any number of child resources.

        When the resource is created/updated, this manifest will be applied to the
        cluster through ``kubectl apply`` and when the resource or the stack is
        deleted, the manifest will be deleted through ``kubectl delete``.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            apiVersion: 'v1',
                  kind"Pod" , metadataname: 'mypod'spec: {
                    containers: [ { name: 'hello', image: 'paulbouwer/hello-kubernetes:1.5', ports: [ { containerPort: 8080 } ] } ]
                  }
        """
        return self._values.get('manifest')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'KubernetesResourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_eks_legacy.Mapping", jsii_struct_bases=[], name_mapping={'groups': 'groups', 'username': 'username'})
class Mapping():
    def __init__(self, *, groups: typing.List[str], username: typing.Optional[str]=None) -> None:
        """
        :param groups: A list of groups within Kubernetes to which the role is mapped.
        :param username: The user name within Kubernetes to map to the IAM role. Default: - By default, the user name is the ARN of the IAM role.

        stability
        :stability: experimental
        """
        self._values = {
            'groups': groups,
        }
        if username is not None: self._values["username"] = username

    @builtins.property
    def groups(self) -> typing.List[str]:
        """A list of groups within Kubernetes to which the role is mapped.

        see
        :see: https://kubernetes.io/docs/reference/access-authn-authz/rbac/#default-roles-and-role-bindings
        stability
        :stability: experimental
        """
        return self._values.get('groups')

    @builtins.property
    def username(self) -> typing.Optional[str]:
        """The user name within Kubernetes to map to the IAM role.

        default
        :default: - By default, the user name is the ARN of the IAM role.

        stability
        :stability: experimental
        """
        return self._values.get('username')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Mapping(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_eks_legacy.NodeType")
class NodeType(enum.Enum):
    """Whether the worker nodes should support GPU or just standard instances.

    stability
    :stability: experimental
    """
    STANDARD = "STANDARD"
    """Standard instances.

    stability
    :stability: experimental
    """
    GPU = "GPU"
    """GPU instances.

    stability
    :stability: experimental
    """

@jsii.implements(ICluster)
class Cluster(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_eks_legacy.Cluster"):
    """A Cluster represents a managed Kubernetes Service (EKS).

    This is a fully managed cluster of API Servers (control-plane)
    The user is still required to create the worker nodes.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::EKS::Cluster
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, cluster_name: typing.Optional[str]=None, default_capacity: typing.Optional[jsii.Number]=None, default_capacity_instance: typing.Optional[_InstanceType_85a97b30]=None, kubectl_enabled: typing.Optional[bool]=None, masters_role: typing.Optional[_IRole_e69bbae4]=None, output_cluster_name: typing.Optional[bool]=None, output_config_command: typing.Optional[bool]=None, output_masters_role_arn: typing.Optional[bool]=None, role: typing.Optional[_IRole_e69bbae4]=None, security_group: typing.Optional[_ISecurityGroup_d72ab8e8]=None, version: typing.Optional[str]=None, vpc: typing.Optional[_IVpc_3795853f]=None, vpc_subnets: typing.Optional[typing.List[_SubnetSelection_36a13cd6]]=None) -> None:
        """Initiates an EKS Cluster with the supplied arguments.

        :param scope: a Construct, most likely a cdk.Stack created.
        :param id: -
        :param cluster_name: Name for the cluster. Default: - Automatically generated name
        :param default_capacity: Number of instances to allocate as an initial capacity for this cluster. Instance type can be configured through ``defaultCapacityInstanceType``, which defaults to ``m5.large``. Use ``cluster.addCapacity`` to add additional customized capacity. Set this to ``0`` is you wish to avoid the initial capacity allocation. Default: 2
        :param default_capacity_instance: The instance type to use for the default capacity. This will only be taken into account if ``defaultCapacity`` is > 0. Default: m5.large
        :param kubectl_enabled: Allows defining ``kubectrl``-related resources on this cluster. If this is disabled, it will not be possible to use the following capabilities: - ``addResource`` - ``addRoleMapping`` - ``addUserMapping`` - ``addMastersRole`` and ``props.mastersRole`` If this is disabled, the cluster can only be managed by issuing ``kubectl`` commands from a session that uses the IAM role/user that created the account. *NOTE*: changing this value will destoy the cluster. This is because a managable cluster must be created using an AWS CloudFormation custom resource which executes with an IAM role owned by the CDK app. Default: true The cluster can be managed by the AWS CDK application.
        :param masters_role: An IAM role that will be added to the ``system:masters`` Kubernetes RBAC group. Default: - By default, it will only possible to update this Kubernetes system by adding resources to this cluster via ``addResource`` or by defining ``KubernetesResource`` resources in your AWS CDK app. Use this if you wish to grant cluster administration privileges to another role.
        :param output_cluster_name: Determines whether a CloudFormation output with the name of the cluster will be synthesized. Default: false
        :param output_config_command: Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized. This command will include the cluster name and, if applicable, the ARN of the masters IAM role. Default: true
        :param output_masters_role_arn: Determines whether a CloudFormation output with the ARN of the "masters" IAM role will be synthesized (if ``mastersRole`` is specified). Default: false
        :param role: Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf. Default: - A role is automatically created for you
        :param security_group: Security Group to use for Control Plane ENIs. Default: - A security group is automatically created
        :param version: The Kubernetes version to run in the cluster. Default: - If not supplied, will use Amazon default version
        :param vpc: The VPC in which to create the Cluster. Default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.
        :param vpc_subnets: Where to place EKS Control Plane ENIs. If you want to create public load balancers, this must include public subnets. For example, to only select private subnets, supply the following:: vpcSubnets: [ { subnetType: ec2.SubnetType.Private } ] Default: - All public and private subnets

        stability
        :stability: experimental
        """
        props = ClusterProps(cluster_name=cluster_name, default_capacity=default_capacity, default_capacity_instance=default_capacity_instance, kubectl_enabled=kubectl_enabled, masters_role=masters_role, output_cluster_name=output_cluster_name, output_config_command=output_config_command, output_masters_role_arn=output_masters_role_arn, role=role, security_group=security_group, version=version, vpc=vpc, vpc_subnets=vpc_subnets)

        jsii.create(Cluster, self, [scope, id, props])

    @jsii.member(jsii_name="fromClusterAttributes")
    @builtins.classmethod
    def from_cluster_attributes(cls, scope: _Construct_f50a3f53, id: str, *, cluster_arn: str, cluster_certificate_authority_data: str, cluster_endpoint: str, cluster_name: str, security_groups: typing.List[_ISecurityGroup_d72ab8e8], vpc: _IVpc_3795853f) -> "ICluster":
        """Import an existing cluster.

        :param scope: the construct scope, in most cases 'this'.
        :param id: the id or name to import as.
        :param cluster_arn: The unique ARN assigned to the service by AWS in the form of arn:aws:eks:.
        :param cluster_certificate_authority_data: The certificate-authority-data for your cluster.
        :param cluster_endpoint: The API Server endpoint URL.
        :param cluster_name: The physical name of the Cluster.
        :param security_groups: The security groups associated with this cluster.
        :param vpc: The VPC in which this Cluster was created.

        stability
        :stability: experimental
        """
        attrs = ClusterAttributes(cluster_arn=cluster_arn, cluster_certificate_authority_data=cluster_certificate_authority_data, cluster_endpoint=cluster_endpoint, cluster_name=cluster_name, security_groups=security_groups, vpc=vpc)

        return jsii.sinvoke(cls, "fromClusterAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addAutoScalingGroup")
    def add_auto_scaling_group(self, auto_scaling_group: _AutoScalingGroup_003d0b84, *, bootstrap_enabled: typing.Optional[bool]=None, bootstrap_options: typing.Optional["BootstrapOptions"]=None, map_role: typing.Optional[bool]=None) -> None:
        """Add compute capacity to this EKS cluster in the form of an AutoScalingGroup.

        The AutoScalingGroup must be running an EKS-optimized AMI containing the
        /etc/eks/bootstrap.sh script. This method will configure Security Groups,
        add the right policies to the instance role, apply the right tags, and add
        the required user data to the instance's launch configuration.

        Spot instances will be labeled ``lifecycle=Ec2Spot`` and tainted with ``PreferNoSchedule``.
        If kubectl is enabled, the
        `spot interrupt handler <https://github.com/awslabs/ec2-spot-labs/tree/master/ec2-spot-eks-solution/spot-termination-handler>`_
        daemon will be installed on all spot instances to handle
        `EC2 Spot Instance Termination Notices <https://aws.amazon.com/blogs/aws/new-ec2-spot-instance-termination-notices/>`_.

        Prefer to use ``addCapacity`` if possible.

        :param auto_scaling_group: [disable-awslint:ref-via-interface].
        :param bootstrap_enabled: Configures the EC2 user-data script for instances in this autoscaling group to bootstrap the node (invoke ``/etc/eks/bootstrap.sh``) and associate it with the EKS cluster. If you wish to provide a custom user data script, set this to ``false`` and manually invoke ``autoscalingGroup.addUserData()``. Default: true
        :param bootstrap_options: Allows options for node bootstrapping through EC2 user data.
        :param map_role: Will automatically update the aws-auth ConfigMap to map the IAM instance role to RBAC. This cannot be explicitly set to ``true`` if the cluster has kubectl disabled. Default: - true if the cluster has kubectl enabled (which is the default).

        see
        :see: https://docs.aws.amazon.com/eks/latest/userguide/launch-workers.html
        stability
        :stability: experimental
        """
        options = AutoScalingGroupOptions(bootstrap_enabled=bootstrap_enabled, bootstrap_options=bootstrap_options, map_role=map_role)

        return jsii.invoke(self, "addAutoScalingGroup", [auto_scaling_group, options])

    @jsii.member(jsii_name="addCapacity")
    def add_capacity(self, id: str, *, instance_type: _InstanceType_85a97b30, bootstrap_enabled: typing.Optional[bool]=None, bootstrap_options: typing.Optional["BootstrapOptions"]=None, map_role: typing.Optional[bool]=None, allow_all_outbound: typing.Optional[bool]=None, associate_public_ip_address: typing.Optional[bool]=None, block_devices: typing.Optional[typing.List[_BlockDevice_6b64cf0c]]=None, cooldown: typing.Optional[_Duration_5170c158]=None, desired_capacity: typing.Optional[jsii.Number]=None, health_check: typing.Optional[_HealthCheck_ed599e14]=None, ignore_unmodified_size_properties: typing.Optional[bool]=None, instance_monitoring: typing.Optional[_Monitoring_11cb7f01]=None, key_name: typing.Optional[str]=None, max_capacity: typing.Optional[jsii.Number]=None, max_instance_lifetime: typing.Optional[_Duration_5170c158]=None, min_capacity: typing.Optional[jsii.Number]=None, notifications: typing.Optional[typing.List[_NotificationConfiguration_396b88c6]]=None, notifications_topic: typing.Optional[_ITopic_ef0ebe0e]=None, replacing_update_min_successful_instances_percent: typing.Optional[jsii.Number]=None, resource_signal_count: typing.Optional[jsii.Number]=None, resource_signal_timeout: typing.Optional[_Duration_5170c158]=None, rolling_update_configuration: typing.Optional[_RollingUpdateConfiguration_c96dd49e]=None, spot_price: typing.Optional[str]=None, update_type: typing.Optional[_UpdateType_7a2ac17e]=None, vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6]=None) -> _AutoScalingGroup_003d0b84:
        """Add nodes to this EKS cluster.

        The nodes will automatically be configured with the right VPC and AMI
        for the instance type and Kubernetes version.

        Spot instances will be labeled ``lifecycle=Ec2Spot`` and tainted with ``PreferNoSchedule``.
        If kubectl is enabled, the
        `spot interrupt handler <https://github.com/awslabs/ec2-spot-labs/tree/master/ec2-spot-eks-solution/spot-termination-handler>`_
        daemon will be installed on all spot instances to handle
        `EC2 Spot Instance Termination Notices <https://aws.amazon.com/blogs/aws/new-ec2-spot-instance-termination-notices/>`_.

        :param id: -
        :param instance_type: Instance type of the instances to start.
        :param bootstrap_enabled: Configures the EC2 user-data script for instances in this autoscaling group to bootstrap the node (invoke ``/etc/eks/bootstrap.sh``) and associate it with the EKS cluster. If you wish to provide a custom user data script, set this to ``false`` and manually invoke ``autoscalingGroup.addUserData()``. Default: true
        :param bootstrap_options: EKS node bootstrapping options. Default: - none
        :param map_role: Will automatically update the aws-auth ConfigMap to map the IAM instance role to RBAC. This cannot be explicitly set to ``true`` if the cluster has kubectl disabled. Default: - true if the cluster has kubectl enabled (which is the default).
        :param allow_all_outbound: Whether the instances can initiate connections to anywhere by default. Default: true
        :param associate_public_ip_address: Whether instances in the Auto Scaling Group should have public IP addresses associated with them. Default: - Use subnet setting.
        :param block_devices: Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes. Each instance that is launched has an associated root device volume, either an Amazon EBS volume or an instance store volume. You can use block device mappings to specify additional EBS volumes or instance store volumes to attach to an instance when it is launched. Default: - Uses the block device mapping of the AMI
        :param cooldown: Default scaling cooldown for this AutoScalingGroup. Default: Duration.minutes(5)
        :param desired_capacity: Initial amount of instances in the fleet. If this is set to a number, every deployment will reset the amount of instances to this number. It is recommended to leave this value blank. Default: minCapacity, and leave unchanged during deployment
        :param health_check: Configuration for health checks. Default: - HealthCheck.ec2 with no grace period
        :param ignore_unmodified_size_properties: If the ASG has scheduled actions, don't reset unchanged group sizes. Only used if the ASG has scheduled actions (which may scale your ASG up or down regardless of cdk deployments). If true, the size of the group will only be reset if it has been changed in the CDK app. If false, the sizes will always be changed back to what they were in the CDK app on deployment. Default: true
        :param instance_monitoring: Controls whether instances in this group are launched with detailed or basic monitoring. When detailed monitoring is enabled, Amazon CloudWatch generates metrics every minute and your account is charged a fee. When you disable detailed monitoring, CloudWatch generates metrics every 5 minutes. Default: - Monitoring.DETAILED
        :param key_name: Name of SSH keypair to grant access to instances. Default: - No SSH access will be possible.
        :param max_capacity: Maximum number of instances in the fleet. Default: desiredCapacity
        :param max_instance_lifetime: The maximum amount of time that an instance can be in service. The maximum duration applies to all current and future instances in the group. As an instance approaches its maximum duration, it is terminated and replaced, and cannot be used again. You must specify a value of at least 604,800 seconds (7 days). To clear a previously set value, simply leave this property undefinied. Default: none
        :param min_capacity: Minimum number of instances in the fleet. Default: 1
        :param notifications: Configure autoscaling group to send notifications about fleet changes to an SNS topic(s). Default: - No fleet change notifications will be sent.
        :param notifications_topic: SNS topic to send notifications about fleet changes. Default: - No fleet change notifications will be sent.
        :param replacing_update_min_successful_instances_percent: Configuration for replacing updates. Only used if updateType == UpdateType.ReplacingUpdate. Specifies how many instances must signal success for the update to succeed. Default: minSuccessfulInstancesPercent
        :param resource_signal_count: How many ResourceSignal calls CloudFormation expects before the resource is considered created. Default: 1
        :param resource_signal_timeout: The length of time to wait for the resourceSignalCount. The maximum value is 43200 (12 hours). Default: Duration.minutes(5)
        :param rolling_update_configuration: Configuration for rolling updates. Only used if updateType == UpdateType.RollingUpdate. Default: - RollingUpdateConfiguration with defaults.
        :param spot_price: The maximum hourly price (in USD) to be paid for any Spot Instance launched to fulfill the request. Spot Instances are launched when the price you specify exceeds the current Spot market price. Default: none
        :param update_type: What to do when an AutoScalingGroup's instance configuration is changed. This is applied when any of the settings on the ASG are changed that affect how the instances should be created (VPC, instance type, startup scripts, etc.). It indicates how the existing instances should be replaced with new instances matching the new config. By default, nothing is done and only new instances are launched with the new config. Default: UpdateType.None
        :param vpc_subnets: Where to place instances within the VPC. Default: - All Private subnets.

        stability
        :stability: experimental
        """
        options = CapacityOptions(instance_type=instance_type, bootstrap_enabled=bootstrap_enabled, bootstrap_options=bootstrap_options, map_role=map_role, allow_all_outbound=allow_all_outbound, associate_public_ip_address=associate_public_ip_address, block_devices=block_devices, cooldown=cooldown, desired_capacity=desired_capacity, health_check=health_check, ignore_unmodified_size_properties=ignore_unmodified_size_properties, instance_monitoring=instance_monitoring, key_name=key_name, max_capacity=max_capacity, max_instance_lifetime=max_instance_lifetime, min_capacity=min_capacity, notifications=notifications, notifications_topic=notifications_topic, replacing_update_min_successful_instances_percent=replacing_update_min_successful_instances_percent, resource_signal_count=resource_signal_count, resource_signal_timeout=resource_signal_timeout, rolling_update_configuration=rolling_update_configuration, spot_price=spot_price, update_type=update_type, vpc_subnets=vpc_subnets)

        return jsii.invoke(self, "addCapacity", [id, options])

    @jsii.member(jsii_name="addChart")
    def add_chart(self, id: str, *, chart: str, namespace: typing.Optional[str]=None, release: typing.Optional[str]=None, repository: typing.Optional[str]=None, values: typing.Optional[typing.Mapping[str, typing.Any]]=None, version: typing.Optional[str]=None) -> "HelmChart":
        """Defines a Helm chart in this cluster.

        :param id: logical id of this chart.
        :param chart: The name of the chart.
        :param namespace: The Kubernetes namespace scope of the requests. Default: default
        :param release: The name of the release. Default: - If no release name is given, it will use the last 63 characters of the node's unique id.
        :param repository: The repository which contains the chart. For example: https://kubernetes-charts.storage.googleapis.com/ Default: - No repository will be used, which means that the chart needs to be an absolute URL.
        :param values: The values to be used by the chart. Default: - No values are provided to the chart.
        :param version: The chart version to install. Default: - If this is not specified, the latest version is installed

        return
        :return: a ``HelmChart`` object

        stability
        :stability: experimental
        throws:
        :throws:: If ``kubectlEnabled`` is ``false``
        """
        options = HelmChartOptions(chart=chart, namespace=namespace, release=release, repository=repository, values=values, version=version)

        return jsii.invoke(self, "addChart", [id, options])

    @jsii.member(jsii_name="addResource")
    def add_resource(self, id: str, *manifest: typing.Any) -> "KubernetesResource":
        """Defines a Kubernetes resource in this cluster.

        The manifest will be applied/deleted using kubectl as needed.

        :param id: logical id of this manifest.
        :param manifest: a list of Kubernetes resource specifications.

        return
        :return: a ``KubernetesResource`` object.

        stability
        :stability: experimental
        throws:
        :throws:: If ``kubectlEnabled`` is ``false``
        """
        return jsii.invoke(self, "addResource", [id, *manifest])

    @builtins.property
    @jsii.member(jsii_name="awsAuth")
    def aws_auth(self) -> "AwsAuth":
        """Lazily creates the AwsAuth resource, which manages AWS authentication mapping.

        stability
        :stability: experimental
        """
        return jsii.get(self, "awsAuth")

    @builtins.property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        """The AWS generated ARN for the Cluster resource.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            arn:aws:eks:us-west-2666666666666cluster / prod
        """
        return jsii.get(self, "clusterArn")

    @builtins.property
    @jsii.member(jsii_name="clusterCertificateAuthorityData")
    def cluster_certificate_authority_data(self) -> str:
        """The certificate-authority-data for your cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterCertificateAuthorityData")

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> str:
        """The endpoint URL for the Cluster.

        This is the URL inside the kubeconfig file to use with kubectl

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            https:
        """
        return jsii.get(self, "clusterEndpoint")

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """The Name of the created EKS Cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterName")

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_231f38b5:
        """Manages connection rules (Security Group Rules) for the cluster.

        stability
        :stability: experimental
        memberof:
        :memberof:: Cluster
        type:
        :type:: {ec2.Connections}
        """
        return jsii.get(self, "connections")

    @builtins.property
    @jsii.member(jsii_name="kubectlEnabled")
    def kubectl_enabled(self) -> bool:
        """Indicates if ``kubectl`` related operations can be performed on this cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "kubectlEnabled")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _IRole_e69bbae4:
        """IAM role assumed by the EKS Control Plane.

        stability
        :stability: experimental
        """
        return jsii.get(self, "role")

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _IVpc_3795853f:
        """The VPC in which this Cluster was created.

        stability
        :stability: experimental
        """
        return jsii.get(self, "vpc")

    @builtins.property
    @jsii.member(jsii_name="defaultCapacity")
    def default_capacity(self) -> typing.Optional[_AutoScalingGroup_003d0b84]:
        """The auto scaling group that hosts the default capacity for this cluster.

        This will be ``undefined`` if the default capacity is set to 0.

        stability
        :stability: experimental
        """
        return jsii.get(self, "defaultCapacity")


__all__ = [
    "AutoScalingGroupOptions",
    "AwsAuth",
    "AwsAuthProps",
    "BootstrapOptions",
    "CapacityOptions",
    "CfnCluster",
    "CfnClusterProps",
    "CfnNodegroup",
    "CfnNodegroupProps",
    "Cluster",
    "ClusterAttributes",
    "ClusterProps",
    "EksOptimizedImage",
    "EksOptimizedImageProps",
    "HelmChart",
    "HelmChartOptions",
    "HelmChartProps",
    "ICluster",
    "KubernetesResource",
    "KubernetesResourceProps",
    "Mapping",
    "NodeType",
]

publication.publish()
