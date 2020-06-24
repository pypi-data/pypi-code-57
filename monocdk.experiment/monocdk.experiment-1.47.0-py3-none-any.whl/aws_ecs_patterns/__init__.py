import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (Construct as _Construct_f50a3f53, Duration as _Duration_5170c158)
from ..aws_applicationautoscaling import (ScalingInterval as _ScalingInterval_fac05118, Schedule as _Schedule_6cd13e0d)
from ..aws_certificatemanager import (ICertificate as _ICertificate_8f3d4c96)
from ..aws_ec2 import (IVpc as _IVpc_3795853f, SubnetSelection as _SubnetSelection_36a13cd6)
from ..aws_ecs import (Ec2Service as _Ec2Service_c4ac147a, Ec2TaskDefinition as _Ec2TaskDefinition_96cf505d, CloudMapOptions as _CloudMapOptions_25ce57e4, ICluster as _ICluster_5cbcc408, PropagatedTagSource as _PropagatedTagSource_e36ef3c2, FargateService as _FargateService_e4491ea2, FargateTaskDefinition as _FargateTaskDefinition_c5f42010, FargatePlatformVersion as _FargatePlatformVersion_187ad0f4, BaseService as _BaseService_c6e5f19d, AwsLogDriver as _AwsLogDriver_a24c479b, Cluster as _Cluster_d0079260, ContainerImage as _ContainerImage_99cc4b15, LogDriver as _LogDriver_d09e7eb9, Secret as _Secret_3f6909a4, ContainerDefinition as _ContainerDefinition_1517aa7f, Protocol as _Protocol_dbf5c55c, TaskDefinition as _TaskDefinition_acfbb011)
from ..aws_elasticloadbalancingv2 import (ApplicationProtocol as _ApplicationProtocol_60c416f7, IApplicationLoadBalancer as _IApplicationLoadBalancer_9d681ef6, ApplicationListener as _ApplicationListener_58c10c5c, ApplicationLoadBalancer as _ApplicationLoadBalancer_1e68d65b, ApplicationTargetGroup as _ApplicationTargetGroup_7d0a8d54, INetworkLoadBalancer as _INetworkLoadBalancer_8db68b99, NetworkListener as _NetworkListener_921cec4b, NetworkLoadBalancer as _NetworkLoadBalancer_83adcf1f, NetworkTargetGroup as _NetworkTargetGroup_4f773ed3)
from ..aws_events import (Rule as _Rule_c38e0b39)
from ..aws_events_targets import (EcsTask as _EcsTask_1d951afe)
from ..aws_iam import (IRole as _IRole_e69bbae4)
from ..aws_route53 import (IHostedZone as _IHostedZone_59ffab76)
from ..aws_sqs import (IQueue as _IQueue_b743f559)


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.ApplicationListenerProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'certificate': 'certificate', 'port': 'port', 'protocol': 'protocol'})
class ApplicationListenerProps():
    def __init__(self, *, name: str, certificate: typing.Optional[_ICertificate_8f3d4c96]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional[_ApplicationProtocol_60c416f7]=None) -> None:
        """Properties to define an application listener.

        :param name: Name of the listener.
        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer protocol to HTTPS. Default: - No certificate associated with the load balancer, if using the HTTP protocol. For HTTPS, a DNS-validated certificate will be created for the load balancer's specified domain name.
        :param port: The port on which the listener listens for requests. Default: - Determined from protocol if known.
        :param protocol: The protocol for connections from clients to the load balancer. The load balancer port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS. Default: ApplicationProtocol.HTTP. If a certificate is specified, the protocol will be set by default to ApplicationProtocol.HTTPS.

        stability
        :stability: experimental
        """
        self._values = {
            'name': name,
        }
        if certificate is not None: self._values["certificate"] = certificate
        if port is not None: self._values["port"] = port
        if protocol is not None: self._values["protocol"] = protocol

    @builtins.property
    def name(self) -> str:
        """Name of the listener.

        stability
        :stability: experimental
        """
        return self._values.get('name')

    @builtins.property
    def certificate(self) -> typing.Optional[_ICertificate_8f3d4c96]:
        """Certificate Manager certificate to associate with the load balancer.

        Setting this option will set the load balancer protocol to HTTPS.

        default
        :default:

        - No certificate associated with the load balancer, if using
          the HTTP protocol. For HTTPS, a DNS-validated certificate will be
          created for the load balancer's specified domain name.

        stability
        :stability: experimental
        """
        return self._values.get('certificate')

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """The port on which the listener listens for requests.

        default
        :default: - Determined from protocol if known.

        stability
        :stability: experimental
        """
        return self._values.get('port')

    @builtins.property
    def protocol(self) -> typing.Optional[_ApplicationProtocol_60c416f7]:
        """The protocol for connections from clients to the load balancer.

        The load balancer port is determined from the protocol (port 80 for
        HTTP, port 443 for HTTPS).  A domain name and zone must be also be
        specified if using HTTPS.

        default
        :default:

        ApplicationProtocol.HTTP. If a certificate is specified, the protocol will be
        set by default to ApplicationProtocol.HTTPS.

        stability
        :stability: experimental
        """
        return self._values.get('protocol')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationListenerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ApplicationLoadBalancedServiceBase(_Construct_f50a3f53, metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.aws_ecs_patterns.ApplicationLoadBalancedServiceBase"):
    """The base class for ApplicationLoadBalancedEc2Service and ApplicationLoadBalancedFargateService services.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ApplicationLoadBalancedServiceBaseProxy

    def __init__(self, scope: _Construct_f50a3f53, id: str, *, certificate: typing.Optional[_ICertificate_8f3d4c96]=None, cloud_map_options: typing.Optional[_CloudMapOptions_25ce57e4]=None, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[_IHostedZone_59ffab76]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, listener_port: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[_IApplicationLoadBalancer_9d681ef6]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, protocol: typing.Optional[_ApplicationProtocol_60c416f7]=None, public_load_balancer: typing.Optional[bool]=None, service_name: typing.Optional[str]=None, task_image_options: typing.Optional["ApplicationLoadBalancedTaskImageOptions"]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """Constructs a new instance of the ApplicationLoadBalancedServiceBase class.

        :param scope: -
        :param id: -
        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer protocol to HTTPS. Default: - No certificate associated with the load balancer, if using the HTTP protocol. For HTTPS, a DNS-validated certificate will be created for the load balancer's specified domain name.
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the application load balancer that will serve traffic to the service. Default: - The default listener port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.
        :param load_balancer: The application load balancer that will serve traffic to the service. The VPC attribute of a load balancer must be specified for it to be used to create a new service with this pattern. [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param protocol: The protocol for connections from clients to the load balancer. The load balancer port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS. Default: HTTP. If a certificate is specified, the protocol will be set by default to HTTPS.
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. TaskDefinition or TaskImageOptions must be specified, but not both. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        props = ApplicationLoadBalancedServiceBaseProps(certificate=certificate, cloud_map_options=cloud_map_options, cluster=cluster, desired_count=desired_count, domain_name=domain_name, domain_zone=domain_zone, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, listener_port=listener_port, load_balancer=load_balancer, max_healthy_percent=max_healthy_percent, min_healthy_percent=min_healthy_percent, propagate_tags=propagate_tags, protocol=protocol, public_load_balancer=public_load_balancer, service_name=service_name, task_image_options=task_image_options, vpc=vpc)

        jsii.create(ApplicationLoadBalancedServiceBase, self, [scope, id, props])

    @jsii.member(jsii_name="addServiceAsTarget")
    def _add_service_as_target(self, service: _BaseService_c6e5f19d) -> None:
        """Adds service as a target of the target group.

        :param service: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addServiceAsTarget", [service])

    @jsii.member(jsii_name="createAWSLogDriver")
    def _create_aws_log_driver(self, prefix: str) -> _AwsLogDriver_a24c479b:
        """
        :param prefix: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "createAWSLogDriver", [prefix])

    @jsii.member(jsii_name="getDefaultCluster")
    def _get_default_cluster(self, scope: _Construct_f50a3f53, vpc: typing.Optional[_IVpc_3795853f]=None) -> _Cluster_d0079260:
        """Returns the default cluster.

        :param scope: -
        :param vpc: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getDefaultCluster", [scope, vpc])

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> _ICluster_5cbcc408:
        """The cluster that hosts the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "cluster")

    @builtins.property
    @jsii.member(jsii_name="desiredCount")
    def desired_count(self) -> jsii.Number:
        """The desired number of instantiations of the task definition to keep running on the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "desiredCount")

    @builtins.property
    @jsii.member(jsii_name="listener")
    def listener(self) -> _ApplicationListener_58c10c5c:
        """The listener for the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "listener")

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> _ApplicationLoadBalancer_1e68d65b:
        """The Application Load Balancer for the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "loadBalancer")

    @builtins.property
    @jsii.member(jsii_name="targetGroup")
    def target_group(self) -> _ApplicationTargetGroup_7d0a8d54:
        """The target group for the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "targetGroup")

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> typing.Optional[_ICertificate_8f3d4c96]:
        """Certificate Manager certificate to associate with the load balancer.

        stability
        :stability: experimental
        """
        return jsii.get(self, "certificate")


class _ApplicationLoadBalancedServiceBaseProxy(ApplicationLoadBalancedServiceBase):
    pass

@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.ApplicationLoadBalancedServiceBaseProps", jsii_struct_bases=[], name_mapping={'certificate': 'certificate', 'cloud_map_options': 'cloudMapOptions', 'cluster': 'cluster', 'desired_count': 'desiredCount', 'domain_name': 'domainName', 'domain_zone': 'domainZone', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'listener_port': 'listenerPort', 'load_balancer': 'loadBalancer', 'max_healthy_percent': 'maxHealthyPercent', 'min_healthy_percent': 'minHealthyPercent', 'propagate_tags': 'propagateTags', 'protocol': 'protocol', 'public_load_balancer': 'publicLoadBalancer', 'service_name': 'serviceName', 'task_image_options': 'taskImageOptions', 'vpc': 'vpc'})
class ApplicationLoadBalancedServiceBaseProps():
    def __init__(self, *, certificate: typing.Optional[_ICertificate_8f3d4c96]=None, cloud_map_options: typing.Optional[_CloudMapOptions_25ce57e4]=None, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[_IHostedZone_59ffab76]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, listener_port: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[_IApplicationLoadBalancer_9d681ef6]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, protocol: typing.Optional[_ApplicationProtocol_60c416f7]=None, public_load_balancer: typing.Optional[bool]=None, service_name: typing.Optional[str]=None, task_image_options: typing.Optional["ApplicationLoadBalancedTaskImageOptions"]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """The properties for the base ApplicationLoadBalancedEc2Service or ApplicationLoadBalancedFargateService service.

        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer protocol to HTTPS. Default: - No certificate associated with the load balancer, if using the HTTP protocol. For HTTPS, a DNS-validated certificate will be created for the load balancer's specified domain name.
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the application load balancer that will serve traffic to the service. Default: - The default listener port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.
        :param load_balancer: The application load balancer that will serve traffic to the service. The VPC attribute of a load balancer must be specified for it to be used to create a new service with this pattern. [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param protocol: The protocol for connections from clients to the load balancer. The load balancer port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS. Default: HTTP. If a certificate is specified, the protocol will be set by default to HTTPS.
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. TaskDefinition or TaskImageOptions must be specified, but not both. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = _CloudMapOptions_25ce57e4(**cloud_map_options)
        if isinstance(task_image_options, dict): task_image_options = ApplicationLoadBalancedTaskImageOptions(**task_image_options)
        self._values = {
        }
        if certificate is not None: self._values["certificate"] = certificate
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None: self._values["cluster"] = cluster
        if desired_count is not None: self._values["desired_count"] = desired_count
        if domain_name is not None: self._values["domain_name"] = domain_name
        if domain_zone is not None: self._values["domain_zone"] = domain_zone
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if listener_port is not None: self._values["listener_port"] = listener_port
        if load_balancer is not None: self._values["load_balancer"] = load_balancer
        if max_healthy_percent is not None: self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None: self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if protocol is not None: self._values["protocol"] = protocol
        if public_load_balancer is not None: self._values["public_load_balancer"] = public_load_balancer
        if service_name is not None: self._values["service_name"] = service_name
        if task_image_options is not None: self._values["task_image_options"] = task_image_options
        if vpc is not None: self._values["vpc"] = vpc

    @builtins.property
    def certificate(self) -> typing.Optional[_ICertificate_8f3d4c96]:
        """Certificate Manager certificate to associate with the load balancer.

        Setting this option will set the load balancer protocol to HTTPS.

        default
        :default:

        - No certificate associated with the load balancer, if using
          the HTTP protocol. For HTTPS, a DNS-validated certificate will be
          created for the load balancer's specified domain name.

        stability
        :stability: experimental
        """
        return self._values.get('certificate')

    @builtins.property
    def cloud_map_options(self) -> typing.Optional[_CloudMapOptions_25ce57e4]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.

        stability
        :stability: experimental
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def cluster(self) -> typing.Optional[_ICluster_5cbcc408]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_count')

    @builtins.property
    def domain_name(self) -> typing.Optional[str]:
        """The domain name for the service, e.g. "api.example.com.".

        default
        :default: - No domain name.

        stability
        :stability: experimental
        """
        return self._values.get('domain_name')

    @builtins.property
    def domain_zone(self) -> typing.Optional[_IHostedZone_59ffab76]:
        """The Route53 hosted zone for the domain, e.g. "example.com.".

        default
        :default: - No Route53 hosted domain zone.

        stability
        :stability: experimental
        """
        return self._values.get('domain_zone')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[_Duration_5170c158]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set

        stability
        :stability: experimental
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        """Listener port of the application load balancer that will serve traffic to the service.

        default
        :default:

        - The default listener port is determined from the protocol (port 80 for HTTP,
          port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.

        stability
        :stability: experimental
        """
        return self._values.get('listener_port')

    @builtins.property
    def load_balancer(self) -> typing.Optional[_IApplicationLoadBalancer_9d681ef6]:
        """The application load balancer that will serve traffic to the service.

        The VPC attribute of a load balancer must be specified for it to be used
        to create a new service with this pattern.

        [disable-awslint:ref-via-interface]

        default
        :default: - a new load balancer will be created.

        stability
        :stability: experimental
        """
        return self._values.get('load_balancer')

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        default
        :default: - 100 if daemon, otherwise 200

        stability
        :stability: experimental
        """
        return self._values.get('max_healthy_percent')

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        default
        :default: - 0 if daemon, otherwise 50

        stability
        :stability: experimental
        """
        return self._values.get('min_healthy_percent')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[_PropagatedTagSource_e36ef3c2]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def protocol(self) -> typing.Optional[_ApplicationProtocol_60c416f7]:
        """The protocol for connections from clients to the load balancer.

        The load balancer port is determined from the protocol (port 80 for
        HTTP, port 443 for HTTPS).  A domain name and zone must be also be
        specified if using HTTPS.

        default
        :default:

        HTTP. If a certificate is specified, the protocol will be
        set by default to HTTPS.

        stability
        :stability: experimental
        """
        return self._values.get('protocol')

    @builtins.property
    def public_load_balancer(self) -> typing.Optional[bool]:
        """Determines whether the Load Balancer will be internet-facing.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('public_load_balancer')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.

        stability
        :stability: experimental
        """
        return self._values.get('service_name')

    @builtins.property
    def task_image_options(self) -> typing.Optional["ApplicationLoadBalancedTaskImageOptions"]:
        """The properties required to create a new task definition.

        TaskDefinition or TaskImageOptions must be specified, but not both.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('task_image_options')

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationLoadBalancedServiceBaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.ApplicationLoadBalancedTaskImageOptions", jsii_struct_bases=[], name_mapping={'image': 'image', 'container_name': 'containerName', 'container_port': 'containerPort', 'enable_logging': 'enableLogging', 'environment': 'environment', 'execution_role': 'executionRole', 'family': 'family', 'log_driver': 'logDriver', 'secrets': 'secrets', 'task_role': 'taskRole'})
class ApplicationLoadBalancedTaskImageOptions():
    def __init__(self, *, image: _ContainerImage_99cc4b15, container_name: typing.Optional[str]=None, container_port: typing.Optional[jsii.Number]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, execution_role: typing.Optional[_IRole_e69bbae4]=None, family: typing.Optional[str]=None, log_driver: typing.Optional[_LogDriver_d09e7eb9]=None, secrets: typing.Optional[typing.Mapping[str, _Secret_3f6909a4]]=None, task_role: typing.Optional[_IRole_e69bbae4]=None) -> None:
        """
        :param image: The image used to start a container. Image or taskDefinition must be specified, not both. Default: - none
        :param container_name: The container name value to be specified in the task definition. Default: - none
        :param container_port: The port number on the container that is bound to the user-specified or automatically assigned host port. If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort. If you are using containers in a task with the bridge network mode and you specify a container port and not a host port, your container automatically receives a host port in the ephemeral port range. Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance. For more information, see `hostPort <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PortMapping.html#ECS-Type-PortMapping-hostPort>`_. Default: 80
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param execution_role: The name of the task execution IAM role that grants the Amazon ECS container agent permission to call AWS APIs on your behalf. Default: - No value
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param task_role: The name of the task IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.

        stability
        :stability: experimental
        """
        self._values = {
            'image': image,
        }
        if container_name is not None: self._values["container_name"] = container_name
        if container_port is not None: self._values["container_port"] = container_port
        if enable_logging is not None: self._values["enable_logging"] = enable_logging
        if environment is not None: self._values["environment"] = environment
        if execution_role is not None: self._values["execution_role"] = execution_role
        if family is not None: self._values["family"] = family
        if log_driver is not None: self._values["log_driver"] = log_driver
        if secrets is not None: self._values["secrets"] = secrets
        if task_role is not None: self._values["task_role"] = task_role

    @builtins.property
    def image(self) -> _ContainerImage_99cc4b15:
        """The image used to start a container.

        Image or taskDefinition must be specified, not both.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @builtins.property
    def container_name(self) -> typing.Optional[str]:
        """The container name value to be specified in the task definition.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('container_name')

    @builtins.property
    def container_port(self) -> typing.Optional[jsii.Number]:
        """The port number on the container that is bound to the user-specified or automatically assigned host port.

        If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort.
        If you are using containers in a task with the bridge network mode and you specify a container port and not a host port,
        your container automatically receives a host port in the ephemeral port range.

        Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance.

        For more information, see
        `hostPort <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PortMapping.html#ECS-Type-PortMapping-hostPort>`_.

        default
        :default: 80

        stability
        :stability: experimental
        """
        return self._values.get('container_port')

    @builtins.property
    def enable_logging(self) -> typing.Optional[bool]:
        """Flag to indicate whether to enable logging.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('enable_logging')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The environment variables to pass to the container.

        default
        :default: - No environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def execution_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The name of the task execution IAM role that grants the Amazon ECS container agent permission to call AWS APIs on your behalf.

        default
        :default: - No value

        stability
        :stability: experimental
        """
        return self._values.get('execution_role')

    @builtins.property
    def family(self) -> typing.Optional[str]:
        """The name of a family that this task definition is registered to.

        A family groups multiple versions of a task definition.

        default
        :default: - Automatically generated name.

        stability
        :stability: experimental
        """
        return self._values.get('family')

    @builtins.property
    def log_driver(self) -> typing.Optional[_LogDriver_d09e7eb9]:
        """The log driver to use.

        default
        :default: - AwsLogDriver if enableLogging is true

        stability
        :stability: experimental
        """
        return self._values.get('log_driver')

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[str, _Secret_3f6909a4]]:
        """The secret to expose to the container as an environment variable.

        default
        :default: - No secret environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('secrets')

    @builtins.property
    def task_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The name of the task IAM role that grants containers in the task permission to call AWS APIs on your behalf.

        default
        :default: - A task role is automatically created for you.

        stability
        :stability: experimental
        """
        return self._values.get('task_role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationLoadBalancedTaskImageOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.ApplicationLoadBalancedTaskImageProps", jsii_struct_bases=[], name_mapping={'image': 'image', 'container_name': 'containerName', 'container_ports': 'containerPorts', 'enable_logging': 'enableLogging', 'environment': 'environment', 'execution_role': 'executionRole', 'family': 'family', 'log_driver': 'logDriver', 'secrets': 'secrets', 'task_role': 'taskRole'})
class ApplicationLoadBalancedTaskImageProps():
    def __init__(self, *, image: _ContainerImage_99cc4b15, container_name: typing.Optional[str]=None, container_ports: typing.Optional[typing.List[jsii.Number]]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, execution_role: typing.Optional[_IRole_e69bbae4]=None, family: typing.Optional[str]=None, log_driver: typing.Optional[_LogDriver_d09e7eb9]=None, secrets: typing.Optional[typing.Mapping[str, _Secret_3f6909a4]]=None, task_role: typing.Optional[_IRole_e69bbae4]=None) -> None:
        """Options for configuring a new container.

        :param image: The image used to start a container. Image or taskDefinition must be specified, not both. Default: - none
        :param container_name: The container name value to be specified in the task definition. Default: - web
        :param container_ports: A list of port numbers on the container that is bound to the user-specified or automatically assigned host port. If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort. If you are using containers in a task with the bridge network mode and you specify a container port and not a host port, your container automatically receives a host port in the ephemeral port range. Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance. For more information, see `hostPort <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PortMapping.html#ECS-Type-PortMapping-hostPort>`_. Default: - [80]
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param execution_role: The name of the task execution IAM role that grants the Amazon ECS container agent permission to call AWS APIs on your behalf. Default: - No value
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param secrets: The secrets to expose to the container as an environment variable. Default: - No secret environment variables.
        :param task_role: The name of the task IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.

        stability
        :stability: experimental
        """
        self._values = {
            'image': image,
        }
        if container_name is not None: self._values["container_name"] = container_name
        if container_ports is not None: self._values["container_ports"] = container_ports
        if enable_logging is not None: self._values["enable_logging"] = enable_logging
        if environment is not None: self._values["environment"] = environment
        if execution_role is not None: self._values["execution_role"] = execution_role
        if family is not None: self._values["family"] = family
        if log_driver is not None: self._values["log_driver"] = log_driver
        if secrets is not None: self._values["secrets"] = secrets
        if task_role is not None: self._values["task_role"] = task_role

    @builtins.property
    def image(self) -> _ContainerImage_99cc4b15:
        """The image used to start a container.

        Image or taskDefinition must be specified, not both.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @builtins.property
    def container_name(self) -> typing.Optional[str]:
        """The container name value to be specified in the task definition.

        default
        :default: - web

        stability
        :stability: experimental
        """
        return self._values.get('container_name')

    @builtins.property
    def container_ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        """A list of port numbers on the container that is bound to the user-specified or automatically assigned host port.

        If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort.
        If you are using containers in a task with the bridge network mode and you specify a container port and not a host port,
        your container automatically receives a host port in the ephemeral port range.

        Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance.

        For more information, see
        `hostPort <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PortMapping.html#ECS-Type-PortMapping-hostPort>`_.

        default
        :default: - [80]

        stability
        :stability: experimental
        """
        return self._values.get('container_ports')

    @builtins.property
    def enable_logging(self) -> typing.Optional[bool]:
        """Flag to indicate whether to enable logging.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('enable_logging')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The environment variables to pass to the container.

        default
        :default: - No environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def execution_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The name of the task execution IAM role that grants the Amazon ECS container agent permission to call AWS APIs on your behalf.

        default
        :default: - No value

        stability
        :stability: experimental
        """
        return self._values.get('execution_role')

    @builtins.property
    def family(self) -> typing.Optional[str]:
        """The name of a family that this task definition is registered to.

        A family groups multiple versions of a task definition.

        default
        :default: - Automatically generated name.

        stability
        :stability: experimental
        """
        return self._values.get('family')

    @builtins.property
    def log_driver(self) -> typing.Optional[_LogDriver_d09e7eb9]:
        """The log driver to use.

        default
        :default: - AwsLogDriver if enableLogging is true

        stability
        :stability: experimental
        """
        return self._values.get('log_driver')

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[str, _Secret_3f6909a4]]:
        """The secrets to expose to the container as an environment variable.

        default
        :default: - No secret environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('secrets')

    @builtins.property
    def task_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The name of the task IAM role that grants containers in the task permission to call AWS APIs on your behalf.

        default
        :default: - A task role is automatically created for you.

        stability
        :stability: experimental
        """
        return self._values.get('task_role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationLoadBalancedTaskImageProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.ApplicationLoadBalancerProps", jsii_struct_bases=[], name_mapping={'listeners': 'listeners', 'name': 'name', 'domain_name': 'domainName', 'domain_zone': 'domainZone', 'public_load_balancer': 'publicLoadBalancer'})
class ApplicationLoadBalancerProps():
    def __init__(self, *, listeners: typing.List["ApplicationListenerProps"], name: str, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[_IHostedZone_59ffab76]=None, public_load_balancer: typing.Optional[bool]=None) -> None:
        """Properties to define an application load balancer.

        :param listeners: Listeners (at least one listener) attached to this load balancer.
        :param name: Name of the load balancer.
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true

        stability
        :stability: experimental
        """
        self._values = {
            'listeners': listeners,
            'name': name,
        }
        if domain_name is not None: self._values["domain_name"] = domain_name
        if domain_zone is not None: self._values["domain_zone"] = domain_zone
        if public_load_balancer is not None: self._values["public_load_balancer"] = public_load_balancer

    @builtins.property
    def listeners(self) -> typing.List["ApplicationListenerProps"]:
        """Listeners (at least one listener) attached to this load balancer.

        stability
        :stability: experimental
        """
        return self._values.get('listeners')

    @builtins.property
    def name(self) -> str:
        """Name of the load balancer.

        stability
        :stability: experimental
        """
        return self._values.get('name')

    @builtins.property
    def domain_name(self) -> typing.Optional[str]:
        """The domain name for the service, e.g. "api.example.com.".

        default
        :default: - No domain name.

        stability
        :stability: experimental
        """
        return self._values.get('domain_name')

    @builtins.property
    def domain_zone(self) -> typing.Optional[_IHostedZone_59ffab76]:
        """The Route53 hosted zone for the domain, e.g. "example.com.".

        default
        :default: - No Route53 hosted domain zone.

        stability
        :stability: experimental
        """
        return self._values.get('domain_zone')

    @builtins.property
    def public_load_balancer(self) -> typing.Optional[bool]:
        """Determines whether the Load Balancer will be internet-facing.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('public_load_balancer')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationLoadBalancerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ApplicationMultipleTargetGroupsServiceBase(_Construct_f50a3f53, metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.aws_ecs_patterns.ApplicationMultipleTargetGroupsServiceBase"):
    """The base class for ApplicationMultipleTargetGroupsEc2Service and ApplicationMultipleTargetGroupsFargateService classes.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ApplicationMultipleTargetGroupsServiceBaseProxy

    def __init__(self, scope: _Construct_f50a3f53, id: str, *, cloud_map_options: typing.Optional[_CloudMapOptions_25ce57e4]=None, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, load_balancers: typing.Optional[typing.List["ApplicationLoadBalancerProps"]]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, service_name: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["ApplicationTargetProps"]]=None, task_image_options: typing.Optional["ApplicationLoadBalancedTaskImageProps"]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """Constructs a new instance of the ApplicationMultipleTargetGroupsServiceBase class.

        :param scope: -
        :param id: -
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The application load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify ALB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        props = ApplicationMultipleTargetGroupsServiceBaseProps(cloud_map_options=cloud_map_options, cluster=cluster, desired_count=desired_count, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, load_balancers=load_balancers, propagate_tags=propagate_tags, service_name=service_name, target_groups=target_groups, task_image_options=task_image_options, vpc=vpc)

        jsii.create(ApplicationMultipleTargetGroupsServiceBase, self, [scope, id, props])

    @jsii.member(jsii_name="addPortMappingForTargets")
    def _add_port_mapping_for_targets(self, container: _ContainerDefinition_1517aa7f, targets: typing.List["ApplicationTargetProps"]) -> None:
        """
        :param container: -
        :param targets: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addPortMappingForTargets", [container, targets])

    @jsii.member(jsii_name="createAWSLogDriver")
    def _create_aws_log_driver(self, prefix: str) -> _AwsLogDriver_a24c479b:
        """
        :param prefix: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "createAWSLogDriver", [prefix])

    @jsii.member(jsii_name="findListener")
    def _find_listener(self, name: typing.Optional[str]=None) -> _ApplicationListener_58c10c5c:
        """
        :param name: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "findListener", [name])

    @jsii.member(jsii_name="getDefaultCluster")
    def _get_default_cluster(self, scope: _Construct_f50a3f53, vpc: typing.Optional[_IVpc_3795853f]=None) -> _Cluster_d0079260:
        """Returns the default cluster.

        :param scope: -
        :param vpc: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getDefaultCluster", [scope, vpc])

    @jsii.member(jsii_name="registerECSTargets")
    def _register_ecs_targets(self, service: _BaseService_c6e5f19d, container: _ContainerDefinition_1517aa7f, targets: typing.List["ApplicationTargetProps"]) -> _ApplicationTargetGroup_7d0a8d54:
        """
        :param service: -
        :param container: -
        :param targets: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "registerECSTargets", [service, container, targets])

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> _ICluster_5cbcc408:
        """The cluster that hosts the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "cluster")

    @builtins.property
    @jsii.member(jsii_name="desiredCount")
    def desired_count(self) -> jsii.Number:
        """The desired number of instantiations of the task definition to keep running on the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "desiredCount")

    @builtins.property
    @jsii.member(jsii_name="listener")
    def listener(self) -> _ApplicationListener_58c10c5c:
        """The default listener for the service (first added listener).

        stability
        :stability: experimental
        """
        return jsii.get(self, "listener")

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> _ApplicationLoadBalancer_1e68d65b:
        """The default Application Load Balancer for the service (first added load balancer).

        stability
        :stability: experimental
        """
        return jsii.get(self, "loadBalancer")

    @builtins.property
    @jsii.member(jsii_name="listeners")
    def _listeners(self) -> typing.List[_ApplicationListener_58c10c5c]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "listeners")

    @_listeners.setter
    def _listeners(self, value: typing.List[_ApplicationListener_58c10c5c]) -> None:
        jsii.set(self, "listeners", value)

    @builtins.property
    @jsii.member(jsii_name="targetGroups")
    def _target_groups(self) -> typing.List[_ApplicationTargetGroup_7d0a8d54]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "targetGroups")

    @_target_groups.setter
    def _target_groups(self, value: typing.List[_ApplicationTargetGroup_7d0a8d54]) -> None:
        jsii.set(self, "targetGroups", value)

    @builtins.property
    @jsii.member(jsii_name="logDriver")
    def _log_driver(self) -> typing.Optional[_LogDriver_d09e7eb9]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "logDriver")

    @_log_driver.setter
    def _log_driver(self, value: typing.Optional[_LogDriver_d09e7eb9]) -> None:
        jsii.set(self, "logDriver", value)


class _ApplicationMultipleTargetGroupsServiceBaseProxy(ApplicationMultipleTargetGroupsServiceBase):
    pass

@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.ApplicationMultipleTargetGroupsServiceBaseProps", jsii_struct_bases=[], name_mapping={'cloud_map_options': 'cloudMapOptions', 'cluster': 'cluster', 'desired_count': 'desiredCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'load_balancers': 'loadBalancers', 'propagate_tags': 'propagateTags', 'service_name': 'serviceName', 'target_groups': 'targetGroups', 'task_image_options': 'taskImageOptions', 'vpc': 'vpc'})
class ApplicationMultipleTargetGroupsServiceBaseProps():
    def __init__(self, *, cloud_map_options: typing.Optional[_CloudMapOptions_25ce57e4]=None, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, load_balancers: typing.Optional[typing.List["ApplicationLoadBalancerProps"]]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, service_name: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["ApplicationTargetProps"]]=None, task_image_options: typing.Optional["ApplicationLoadBalancedTaskImageProps"]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """The properties for the base ApplicationMultipleTargetGroupsEc2Service or ApplicationMultipleTargetGroupsFargateService service.

        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The application load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify ALB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = _CloudMapOptions_25ce57e4(**cloud_map_options)
        if isinstance(task_image_options, dict): task_image_options = ApplicationLoadBalancedTaskImageProps(**task_image_options)
        self._values = {
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None: self._values["cluster"] = cluster
        if desired_count is not None: self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if load_balancers is not None: self._values["load_balancers"] = load_balancers
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if service_name is not None: self._values["service_name"] = service_name
        if target_groups is not None: self._values["target_groups"] = target_groups
        if task_image_options is not None: self._values["task_image_options"] = task_image_options
        if vpc is not None: self._values["vpc"] = vpc

    @builtins.property
    def cloud_map_options(self) -> typing.Optional[_CloudMapOptions_25ce57e4]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.

        stability
        :stability: experimental
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def cluster(self) -> typing.Optional[_ICluster_5cbcc408]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_count')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[_Duration_5170c158]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set

        stability
        :stability: experimental
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def load_balancers(self) -> typing.Optional[typing.List["ApplicationLoadBalancerProps"]]:
        """The application load balancer that will serve traffic to the service.

        default
        :default: - a new load balancer with a listener will be created.

        stability
        :stability: experimental
        """
        return self._values.get('load_balancers')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[_PropagatedTagSource_e36ef3c2]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.

        stability
        :stability: experimental
        """
        return self._values.get('service_name')

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List["ApplicationTargetProps"]]:
        """Properties to specify ALB target groups.

        default
        :default: - default portMapping registered as target group and attached to the first defined listener

        stability
        :stability: experimental
        """
        return self._values.get('target_groups')

    @builtins.property
    def task_image_options(self) -> typing.Optional["ApplicationLoadBalancedTaskImageProps"]:
        """The properties required to create a new task definition.

        Only one of TaskDefinition or TaskImageOptions must be specified.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('task_image_options')

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationMultipleTargetGroupsServiceBaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.ApplicationTargetProps", jsii_struct_bases=[], name_mapping={'container_port': 'containerPort', 'host_header': 'hostHeader', 'listener': 'listener', 'path_pattern': 'pathPattern', 'priority': 'priority', 'protocol': 'protocol'})
class ApplicationTargetProps():
    def __init__(self, *, container_port: jsii.Number, host_header: typing.Optional[str]=None, listener: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None, protocol: typing.Optional[_Protocol_dbf5c55c]=None) -> None:
        """Properties to define an application target group.

        :param container_port: The port number of the container. Only applicable when using application/network load balancers.
        :param host_header: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param listener: Name of the listener the target group attached to. Default: - default listener (first added listener)
        :param path_pattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        :param protocol: The protocol used for the port mapping. Only applicable when using application load balancers. Default: ecs.Protocol.TCP

        stability
        :stability: experimental
        """
        self._values = {
            'container_port': container_port,
        }
        if host_header is not None: self._values["host_header"] = host_header
        if listener is not None: self._values["listener"] = listener
        if path_pattern is not None: self._values["path_pattern"] = path_pattern
        if priority is not None: self._values["priority"] = priority
        if protocol is not None: self._values["protocol"] = protocol

    @builtins.property
    def container_port(self) -> jsii.Number:
        """The port number of the container.

        Only applicable when using application/network load balancers.

        stability
        :stability: experimental
        """
        return self._values.get('container_port')

    @builtins.property
    def host_header(self) -> typing.Optional[str]:
        """Rule applies if the requested host matches the indicated host.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        default
        :default: No host condition

        see
        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#host-conditions
        stability
        :stability: experimental
        """
        return self._values.get('host_header')

    @builtins.property
    def listener(self) -> typing.Optional[str]:
        """Name of the listener the target group attached to.

        default
        :default: - default listener (first added listener)

        stability
        :stability: experimental
        """
        return self._values.get('listener')

    @builtins.property
    def path_pattern(self) -> typing.Optional[str]:
        """Rule applies if the requested path matches the given path pattern.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        default
        :default: No path condition

        see
        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        stability
        :stability: experimental
        """
        return self._values.get('path_pattern')

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        """Priority of this target group.

        The rule with the lowest priority will be used for every request.
        If priority is not given, these target groups will be added as
        defaults, and must not have conditions.

        Priorities must be unique.

        default
        :default: Target groups are used as defaults

        stability
        :stability: experimental
        """
        return self._values.get('priority')

    @builtins.property
    def protocol(self) -> typing.Optional[_Protocol_dbf5c55c]:
        """The protocol used for the port mapping.

        Only applicable when using application load balancers.

        default
        :default: ecs.Protocol.TCP

        stability
        :stability: experimental
        """
        return self._values.get('protocol')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationTargetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.NetworkListenerProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'port': 'port'})
class NetworkListenerProps():
    def __init__(self, *, name: str, port: typing.Optional[jsii.Number]=None) -> None:
        """Properties to define an network listener.

        :param name: Name of the listener.
        :param port: The port on which the listener listens for requests. Default: 80

        stability
        :stability: experimental
        """
        self._values = {
            'name': name,
        }
        if port is not None: self._values["port"] = port

    @builtins.property
    def name(self) -> str:
        """Name of the listener.

        stability
        :stability: experimental
        """
        return self._values.get('name')

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """The port on which the listener listens for requests.

        default
        :default: 80

        stability
        :stability: experimental
        """
        return self._values.get('port')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkListenerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class NetworkLoadBalancedServiceBase(_Construct_f50a3f53, metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.aws_ecs_patterns.NetworkLoadBalancedServiceBase"):
    """The base class for NetworkLoadBalancedEc2Service and NetworkLoadBalancedFargateService services.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _NetworkLoadBalancedServiceBaseProxy

    def __init__(self, scope: _Construct_f50a3f53, id: str, *, cloud_map_options: typing.Optional[_CloudMapOptions_25ce57e4]=None, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[_IHostedZone_59ffab76]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, listener_port: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[_INetworkLoadBalancer_8db68b99]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, public_load_balancer: typing.Optional[bool]=None, service_name: typing.Optional[str]=None, task_image_options: typing.Optional["NetworkLoadBalancedTaskImageOptions"]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """Constructs a new instance of the NetworkLoadBalancedServiceBase class.

        :param scope: -
        :param id: -
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the network load balancer that will serve traffic to the service. Default: 80
        :param load_balancer: The network load balancer that will serve traffic to the service. If the load balancer has been imported, the vpc attribute must be specified in the call to fromNetworkLoadBalancerAttributes(). [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. One of taskImageOptions or taskDefinition must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        props = NetworkLoadBalancedServiceBaseProps(cloud_map_options=cloud_map_options, cluster=cluster, desired_count=desired_count, domain_name=domain_name, domain_zone=domain_zone, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, listener_port=listener_port, load_balancer=load_balancer, max_healthy_percent=max_healthy_percent, min_healthy_percent=min_healthy_percent, propagate_tags=propagate_tags, public_load_balancer=public_load_balancer, service_name=service_name, task_image_options=task_image_options, vpc=vpc)

        jsii.create(NetworkLoadBalancedServiceBase, self, [scope, id, props])

    @jsii.member(jsii_name="addServiceAsTarget")
    def _add_service_as_target(self, service: _BaseService_c6e5f19d) -> None:
        """Adds service as a target of the target group.

        :param service: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addServiceAsTarget", [service])

    @jsii.member(jsii_name="createAWSLogDriver")
    def _create_aws_log_driver(self, prefix: str) -> _AwsLogDriver_a24c479b:
        """
        :param prefix: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "createAWSLogDriver", [prefix])

    @jsii.member(jsii_name="getDefaultCluster")
    def _get_default_cluster(self, scope: _Construct_f50a3f53, vpc: typing.Optional[_IVpc_3795853f]=None) -> _Cluster_d0079260:
        """Returns the default cluster.

        :param scope: -
        :param vpc: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getDefaultCluster", [scope, vpc])

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> _ICluster_5cbcc408:
        """The cluster that hosts the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "cluster")

    @builtins.property
    @jsii.member(jsii_name="desiredCount")
    def desired_count(self) -> jsii.Number:
        """The desired number of instantiations of the task definition to keep running on the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "desiredCount")

    @builtins.property
    @jsii.member(jsii_name="listener")
    def listener(self) -> _NetworkListener_921cec4b:
        """The listener for the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "listener")

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> _NetworkLoadBalancer_83adcf1f:
        """The Network Load Balancer for the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "loadBalancer")

    @builtins.property
    @jsii.member(jsii_name="targetGroup")
    def target_group(self) -> _NetworkTargetGroup_4f773ed3:
        """The target group for the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "targetGroup")


class _NetworkLoadBalancedServiceBaseProxy(NetworkLoadBalancedServiceBase):
    pass

@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.NetworkLoadBalancedServiceBaseProps", jsii_struct_bases=[], name_mapping={'cloud_map_options': 'cloudMapOptions', 'cluster': 'cluster', 'desired_count': 'desiredCount', 'domain_name': 'domainName', 'domain_zone': 'domainZone', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'listener_port': 'listenerPort', 'load_balancer': 'loadBalancer', 'max_healthy_percent': 'maxHealthyPercent', 'min_healthy_percent': 'minHealthyPercent', 'propagate_tags': 'propagateTags', 'public_load_balancer': 'publicLoadBalancer', 'service_name': 'serviceName', 'task_image_options': 'taskImageOptions', 'vpc': 'vpc'})
class NetworkLoadBalancedServiceBaseProps():
    def __init__(self, *, cloud_map_options: typing.Optional[_CloudMapOptions_25ce57e4]=None, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[_IHostedZone_59ffab76]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, listener_port: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[_INetworkLoadBalancer_8db68b99]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, public_load_balancer: typing.Optional[bool]=None, service_name: typing.Optional[str]=None, task_image_options: typing.Optional["NetworkLoadBalancedTaskImageOptions"]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """The properties for the base NetworkLoadBalancedEc2Service or NetworkLoadBalancedFargateService service.

        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the network load balancer that will serve traffic to the service. Default: 80
        :param load_balancer: The network load balancer that will serve traffic to the service. If the load balancer has been imported, the vpc attribute must be specified in the call to fromNetworkLoadBalancerAttributes(). [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. One of taskImageOptions or taskDefinition must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = _CloudMapOptions_25ce57e4(**cloud_map_options)
        if isinstance(task_image_options, dict): task_image_options = NetworkLoadBalancedTaskImageOptions(**task_image_options)
        self._values = {
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None: self._values["cluster"] = cluster
        if desired_count is not None: self._values["desired_count"] = desired_count
        if domain_name is not None: self._values["domain_name"] = domain_name
        if domain_zone is not None: self._values["domain_zone"] = domain_zone
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if listener_port is not None: self._values["listener_port"] = listener_port
        if load_balancer is not None: self._values["load_balancer"] = load_balancer
        if max_healthy_percent is not None: self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None: self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if public_load_balancer is not None: self._values["public_load_balancer"] = public_load_balancer
        if service_name is not None: self._values["service_name"] = service_name
        if task_image_options is not None: self._values["task_image_options"] = task_image_options
        if vpc is not None: self._values["vpc"] = vpc

    @builtins.property
    def cloud_map_options(self) -> typing.Optional[_CloudMapOptions_25ce57e4]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.

        stability
        :stability: experimental
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def cluster(self) -> typing.Optional[_ICluster_5cbcc408]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_count')

    @builtins.property
    def domain_name(self) -> typing.Optional[str]:
        """The domain name for the service, e.g. "api.example.com.".

        default
        :default: - No domain name.

        stability
        :stability: experimental
        """
        return self._values.get('domain_name')

    @builtins.property
    def domain_zone(self) -> typing.Optional[_IHostedZone_59ffab76]:
        """The Route53 hosted zone for the domain, e.g. "example.com.".

        default
        :default: - No Route53 hosted domain zone.

        stability
        :stability: experimental
        """
        return self._values.get('domain_zone')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[_Duration_5170c158]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set

        stability
        :stability: experimental
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        """Listener port of the network load balancer that will serve traffic to the service.

        default
        :default: 80

        stability
        :stability: experimental
        """
        return self._values.get('listener_port')

    @builtins.property
    def load_balancer(self) -> typing.Optional[_INetworkLoadBalancer_8db68b99]:
        """The network load balancer that will serve traffic to the service.

        If the load balancer has been imported, the vpc attribute must be specified
        in the call to fromNetworkLoadBalancerAttributes().

        [disable-awslint:ref-via-interface]

        default
        :default: - a new load balancer will be created.

        stability
        :stability: experimental
        """
        return self._values.get('load_balancer')

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        default
        :default: - 100 if daemon, otherwise 200

        stability
        :stability: experimental
        """
        return self._values.get('max_healthy_percent')

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        default
        :default: - 0 if daemon, otherwise 50

        stability
        :stability: experimental
        """
        return self._values.get('min_healthy_percent')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[_PropagatedTagSource_e36ef3c2]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def public_load_balancer(self) -> typing.Optional[bool]:
        """Determines whether the Load Balancer will be internet-facing.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('public_load_balancer')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.

        stability
        :stability: experimental
        """
        return self._values.get('service_name')

    @builtins.property
    def task_image_options(self) -> typing.Optional["NetworkLoadBalancedTaskImageOptions"]:
        """The properties required to create a new task definition.

        One of taskImageOptions or taskDefinition must be specified.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('task_image_options')

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkLoadBalancedServiceBaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.NetworkLoadBalancedTaskImageOptions", jsii_struct_bases=[], name_mapping={'image': 'image', 'container_name': 'containerName', 'container_port': 'containerPort', 'enable_logging': 'enableLogging', 'environment': 'environment', 'execution_role': 'executionRole', 'family': 'family', 'log_driver': 'logDriver', 'secrets': 'secrets', 'task_role': 'taskRole'})
class NetworkLoadBalancedTaskImageOptions():
    def __init__(self, *, image: _ContainerImage_99cc4b15, container_name: typing.Optional[str]=None, container_port: typing.Optional[jsii.Number]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, execution_role: typing.Optional[_IRole_e69bbae4]=None, family: typing.Optional[str]=None, log_driver: typing.Optional[_LogDriver_d09e7eb9]=None, secrets: typing.Optional[typing.Mapping[str, _Secret_3f6909a4]]=None, task_role: typing.Optional[_IRole_e69bbae4]=None) -> None:
        """
        :param image: The image used to start a container. Image or taskDefinition must be specified, but not both. Default: - none
        :param container_name: The container name value to be specified in the task definition. Default: - none
        :param container_port: The port number on the container that is bound to the user-specified or automatically assigned host port. If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort. If you are using containers in a task with the bridge network mode and you specify a container port and not a host port, your container automatically receives a host port in the ephemeral port range. Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance. For more information, see `hostPort <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PortMapping.html#ECS-Type-PortMapping-hostPort>`_. Default: 80
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param execution_role: The name of the task execution IAM role that grants the Amazon ECS container agent permission to call AWS APIs on your behalf. Default: - No value
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param task_role: The name of the task IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.

        stability
        :stability: experimental
        """
        self._values = {
            'image': image,
        }
        if container_name is not None: self._values["container_name"] = container_name
        if container_port is not None: self._values["container_port"] = container_port
        if enable_logging is not None: self._values["enable_logging"] = enable_logging
        if environment is not None: self._values["environment"] = environment
        if execution_role is not None: self._values["execution_role"] = execution_role
        if family is not None: self._values["family"] = family
        if log_driver is not None: self._values["log_driver"] = log_driver
        if secrets is not None: self._values["secrets"] = secrets
        if task_role is not None: self._values["task_role"] = task_role

    @builtins.property
    def image(self) -> _ContainerImage_99cc4b15:
        """The image used to start a container.

        Image or taskDefinition must be specified, but not both.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @builtins.property
    def container_name(self) -> typing.Optional[str]:
        """The container name value to be specified in the task definition.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('container_name')

    @builtins.property
    def container_port(self) -> typing.Optional[jsii.Number]:
        """The port number on the container that is bound to the user-specified or automatically assigned host port.

        If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort.
        If you are using containers in a task with the bridge network mode and you specify a container port and not a host port,
        your container automatically receives a host port in the ephemeral port range.

        Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance.

        For more information, see
        `hostPort <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PortMapping.html#ECS-Type-PortMapping-hostPort>`_.

        default
        :default: 80

        stability
        :stability: experimental
        """
        return self._values.get('container_port')

    @builtins.property
    def enable_logging(self) -> typing.Optional[bool]:
        """Flag to indicate whether to enable logging.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('enable_logging')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The environment variables to pass to the container.

        default
        :default: - No environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def execution_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The name of the task execution IAM role that grants the Amazon ECS container agent permission to call AWS APIs on your behalf.

        default
        :default: - No value

        stability
        :stability: experimental
        """
        return self._values.get('execution_role')

    @builtins.property
    def family(self) -> typing.Optional[str]:
        """The name of a family that this task definition is registered to.

        A family groups multiple versions of a task definition.

        default
        :default: - Automatically generated name.

        stability
        :stability: experimental
        """
        return self._values.get('family')

    @builtins.property
    def log_driver(self) -> typing.Optional[_LogDriver_d09e7eb9]:
        """The log driver to use.

        default
        :default: - AwsLogDriver if enableLogging is true

        stability
        :stability: experimental
        """
        return self._values.get('log_driver')

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[str, _Secret_3f6909a4]]:
        """The secret to expose to the container as an environment variable.

        default
        :default: - No secret environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('secrets')

    @builtins.property
    def task_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The name of the task IAM role that grants containers in the task permission to call AWS APIs on your behalf.

        default
        :default: - A task role is automatically created for you.

        stability
        :stability: experimental
        """
        return self._values.get('task_role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkLoadBalancedTaskImageOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.NetworkLoadBalancedTaskImageProps", jsii_struct_bases=[], name_mapping={'image': 'image', 'container_name': 'containerName', 'container_ports': 'containerPorts', 'enable_logging': 'enableLogging', 'environment': 'environment', 'execution_role': 'executionRole', 'family': 'family', 'log_driver': 'logDriver', 'secrets': 'secrets', 'task_role': 'taskRole'})
class NetworkLoadBalancedTaskImageProps():
    def __init__(self, *, image: _ContainerImage_99cc4b15, container_name: typing.Optional[str]=None, container_ports: typing.Optional[typing.List[jsii.Number]]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, execution_role: typing.Optional[_IRole_e69bbae4]=None, family: typing.Optional[str]=None, log_driver: typing.Optional[_LogDriver_d09e7eb9]=None, secrets: typing.Optional[typing.Mapping[str, _Secret_3f6909a4]]=None, task_role: typing.Optional[_IRole_e69bbae4]=None) -> None:
        """Options for configuring a new container.

        :param image: The image used to start a container. Image or taskDefinition must be specified, but not both. Default: - none
        :param container_name: The container name value to be specified in the task definition. Default: - none
        :param container_ports: A list of port numbers on the container that is bound to the user-specified or automatically assigned host port. If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort. If you are using containers in a task with the bridge network mode and you specify a container port and not a host port, your container automatically receives a host port in the ephemeral port range. Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance. For more information, see `hostPort <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PortMapping.html#ECS-Type-PortMapping-hostPort>`_. Default: - [80]
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param execution_role: The name of the task execution IAM role that grants the Amazon ECS container agent permission to call AWS APIs on your behalf. Default: - No value
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param secrets: The secrets to expose to the container as an environment variable. Default: - No secret environment variables.
        :param task_role: The name of the task IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.

        stability
        :stability: experimental
        """
        self._values = {
            'image': image,
        }
        if container_name is not None: self._values["container_name"] = container_name
        if container_ports is not None: self._values["container_ports"] = container_ports
        if enable_logging is not None: self._values["enable_logging"] = enable_logging
        if environment is not None: self._values["environment"] = environment
        if execution_role is not None: self._values["execution_role"] = execution_role
        if family is not None: self._values["family"] = family
        if log_driver is not None: self._values["log_driver"] = log_driver
        if secrets is not None: self._values["secrets"] = secrets
        if task_role is not None: self._values["task_role"] = task_role

    @builtins.property
    def image(self) -> _ContainerImage_99cc4b15:
        """The image used to start a container.

        Image or taskDefinition must be specified, but not both.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @builtins.property
    def container_name(self) -> typing.Optional[str]:
        """The container name value to be specified in the task definition.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('container_name')

    @builtins.property
    def container_ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        """A list of port numbers on the container that is bound to the user-specified or automatically assigned host port.

        If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort.
        If you are using containers in a task with the bridge network mode and you specify a container port and not a host port,
        your container automatically receives a host port in the ephemeral port range.

        Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance.

        For more information, see
        `hostPort <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PortMapping.html#ECS-Type-PortMapping-hostPort>`_.

        default
        :default: - [80]

        stability
        :stability: experimental
        """
        return self._values.get('container_ports')

    @builtins.property
    def enable_logging(self) -> typing.Optional[bool]:
        """Flag to indicate whether to enable logging.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('enable_logging')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The environment variables to pass to the container.

        default
        :default: - No environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def execution_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The name of the task execution IAM role that grants the Amazon ECS container agent permission to call AWS APIs on your behalf.

        default
        :default: - No value

        stability
        :stability: experimental
        """
        return self._values.get('execution_role')

    @builtins.property
    def family(self) -> typing.Optional[str]:
        """The name of a family that this task definition is registered to.

        A family groups multiple versions of a task definition.

        default
        :default: - Automatically generated name.

        stability
        :stability: experimental
        """
        return self._values.get('family')

    @builtins.property
    def log_driver(self) -> typing.Optional[_LogDriver_d09e7eb9]:
        """The log driver to use.

        default
        :default: - AwsLogDriver if enableLogging is true

        stability
        :stability: experimental
        """
        return self._values.get('log_driver')

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[str, _Secret_3f6909a4]]:
        """The secrets to expose to the container as an environment variable.

        default
        :default: - No secret environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('secrets')

    @builtins.property
    def task_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The name of the task IAM role that grants containers in the task permission to call AWS APIs on your behalf.

        default
        :default: - A task role is automatically created for you.

        stability
        :stability: experimental
        """
        return self._values.get('task_role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkLoadBalancedTaskImageProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.NetworkLoadBalancerProps", jsii_struct_bases=[], name_mapping={'listeners': 'listeners', 'name': 'name', 'domain_name': 'domainName', 'domain_zone': 'domainZone', 'public_load_balancer': 'publicLoadBalancer'})
class NetworkLoadBalancerProps():
    def __init__(self, *, listeners: typing.List["NetworkListenerProps"], name: str, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[_IHostedZone_59ffab76]=None, public_load_balancer: typing.Optional[bool]=None) -> None:
        """Properties to define an network load balancer.

        :param listeners: Listeners (at least one listener) attached to this load balancer. Default: - none
        :param name: Name of the load balancer.
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true

        stability
        :stability: experimental
        """
        self._values = {
            'listeners': listeners,
            'name': name,
        }
        if domain_name is not None: self._values["domain_name"] = domain_name
        if domain_zone is not None: self._values["domain_zone"] = domain_zone
        if public_load_balancer is not None: self._values["public_load_balancer"] = public_load_balancer

    @builtins.property
    def listeners(self) -> typing.List["NetworkListenerProps"]:
        """Listeners (at least one listener) attached to this load balancer.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('listeners')

    @builtins.property
    def name(self) -> str:
        """Name of the load balancer.

        stability
        :stability: experimental
        """
        return self._values.get('name')

    @builtins.property
    def domain_name(self) -> typing.Optional[str]:
        """The domain name for the service, e.g. "api.example.com.".

        default
        :default: - No domain name.

        stability
        :stability: experimental
        """
        return self._values.get('domain_name')

    @builtins.property
    def domain_zone(self) -> typing.Optional[_IHostedZone_59ffab76]:
        """The Route53 hosted zone for the domain, e.g. "example.com.".

        default
        :default: - No Route53 hosted domain zone.

        stability
        :stability: experimental
        """
        return self._values.get('domain_zone')

    @builtins.property
    def public_load_balancer(self) -> typing.Optional[bool]:
        """Determines whether the Load Balancer will be internet-facing.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('public_load_balancer')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkLoadBalancerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class NetworkMultipleTargetGroupsServiceBase(_Construct_f50a3f53, metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.aws_ecs_patterns.NetworkMultipleTargetGroupsServiceBase"):
    """The base class for NetworkMultipleTargetGroupsEc2Service and NetworkMultipleTargetGroupsFargateService classes.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _NetworkMultipleTargetGroupsServiceBaseProxy

    def __init__(self, scope: _Construct_f50a3f53, id: str, *, cloud_map_options: typing.Optional[_CloudMapOptions_25ce57e4]=None, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, load_balancers: typing.Optional[typing.List["NetworkLoadBalancerProps"]]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, service_name: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["NetworkTargetProps"]]=None, task_image_options: typing.Optional["NetworkLoadBalancedTaskImageProps"]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """Constructs a new instance of the NetworkMultipleTargetGroupsServiceBase class.

        :param scope: -
        :param id: -
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The network load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: Name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify NLB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        props = NetworkMultipleTargetGroupsServiceBaseProps(cloud_map_options=cloud_map_options, cluster=cluster, desired_count=desired_count, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, load_balancers=load_balancers, propagate_tags=propagate_tags, service_name=service_name, target_groups=target_groups, task_image_options=task_image_options, vpc=vpc)

        jsii.create(NetworkMultipleTargetGroupsServiceBase, self, [scope, id, props])

    @jsii.member(jsii_name="addPortMappingForTargets")
    def _add_port_mapping_for_targets(self, container: _ContainerDefinition_1517aa7f, targets: typing.List["NetworkTargetProps"]) -> None:
        """
        :param container: -
        :param targets: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addPortMappingForTargets", [container, targets])

    @jsii.member(jsii_name="createAWSLogDriver")
    def _create_aws_log_driver(self, prefix: str) -> _AwsLogDriver_a24c479b:
        """
        :param prefix: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "createAWSLogDriver", [prefix])

    @jsii.member(jsii_name="findListener")
    def _find_listener(self, name: typing.Optional[str]=None) -> _NetworkListener_921cec4b:
        """
        :param name: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "findListener", [name])

    @jsii.member(jsii_name="getDefaultCluster")
    def _get_default_cluster(self, scope: _Construct_f50a3f53, vpc: typing.Optional[_IVpc_3795853f]=None) -> _Cluster_d0079260:
        """Returns the default cluster.

        :param scope: -
        :param vpc: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getDefaultCluster", [scope, vpc])

    @jsii.member(jsii_name="registerECSTargets")
    def _register_ecs_targets(self, service: _BaseService_c6e5f19d, container: _ContainerDefinition_1517aa7f, targets: typing.List["NetworkTargetProps"]) -> _NetworkTargetGroup_4f773ed3:
        """
        :param service: -
        :param container: -
        :param targets: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "registerECSTargets", [service, container, targets])

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> _ICluster_5cbcc408:
        """The cluster that hosts the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "cluster")

    @builtins.property
    @jsii.member(jsii_name="desiredCount")
    def desired_count(self) -> jsii.Number:
        """The desired number of instantiations of the task definition to keep running on the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "desiredCount")

    @builtins.property
    @jsii.member(jsii_name="listener")
    def listener(self) -> _NetworkListener_921cec4b:
        """The listener for the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "listener")

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> _NetworkLoadBalancer_83adcf1f:
        """The Network Load Balancer for the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "loadBalancer")

    @builtins.property
    @jsii.member(jsii_name="listeners")
    def _listeners(self) -> typing.List[_NetworkListener_921cec4b]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "listeners")

    @_listeners.setter
    def _listeners(self, value: typing.List[_NetworkListener_921cec4b]) -> None:
        jsii.set(self, "listeners", value)

    @builtins.property
    @jsii.member(jsii_name="targetGroups")
    def _target_groups(self) -> typing.List[_NetworkTargetGroup_4f773ed3]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "targetGroups")

    @_target_groups.setter
    def _target_groups(self, value: typing.List[_NetworkTargetGroup_4f773ed3]) -> None:
        jsii.set(self, "targetGroups", value)

    @builtins.property
    @jsii.member(jsii_name="logDriver")
    def _log_driver(self) -> typing.Optional[_LogDriver_d09e7eb9]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "logDriver")

    @_log_driver.setter
    def _log_driver(self, value: typing.Optional[_LogDriver_d09e7eb9]) -> None:
        jsii.set(self, "logDriver", value)


class _NetworkMultipleTargetGroupsServiceBaseProxy(NetworkMultipleTargetGroupsServiceBase):
    pass

@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.NetworkMultipleTargetGroupsServiceBaseProps", jsii_struct_bases=[], name_mapping={'cloud_map_options': 'cloudMapOptions', 'cluster': 'cluster', 'desired_count': 'desiredCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'load_balancers': 'loadBalancers', 'propagate_tags': 'propagateTags', 'service_name': 'serviceName', 'target_groups': 'targetGroups', 'task_image_options': 'taskImageOptions', 'vpc': 'vpc'})
class NetworkMultipleTargetGroupsServiceBaseProps():
    def __init__(self, *, cloud_map_options: typing.Optional[_CloudMapOptions_25ce57e4]=None, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, load_balancers: typing.Optional[typing.List["NetworkLoadBalancerProps"]]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, service_name: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["NetworkTargetProps"]]=None, task_image_options: typing.Optional["NetworkLoadBalancedTaskImageProps"]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """The properties for the base NetworkMultipleTargetGroupsEc2Service or NetworkMultipleTargetGroupsFargateService service.

        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The network load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: Name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify NLB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = _CloudMapOptions_25ce57e4(**cloud_map_options)
        if isinstance(task_image_options, dict): task_image_options = NetworkLoadBalancedTaskImageProps(**task_image_options)
        self._values = {
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None: self._values["cluster"] = cluster
        if desired_count is not None: self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if load_balancers is not None: self._values["load_balancers"] = load_balancers
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if service_name is not None: self._values["service_name"] = service_name
        if target_groups is not None: self._values["target_groups"] = target_groups
        if task_image_options is not None: self._values["task_image_options"] = task_image_options
        if vpc is not None: self._values["vpc"] = vpc

    @builtins.property
    def cloud_map_options(self) -> typing.Optional[_CloudMapOptions_25ce57e4]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.

        stability
        :stability: experimental
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def cluster(self) -> typing.Optional[_ICluster_5cbcc408]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_count')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[_Duration_5170c158]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set

        stability
        :stability: experimental
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def load_balancers(self) -> typing.Optional[typing.List["NetworkLoadBalancerProps"]]:
        """The network load balancer that will serve traffic to the service.

        default
        :default: - a new load balancer with a listener will be created.

        stability
        :stability: experimental
        """
        return self._values.get('load_balancers')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[_PropagatedTagSource_e36ef3c2]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """Name of the service.

        default
        :default: - CloudFormation-generated name.

        stability
        :stability: experimental
        """
        return self._values.get('service_name')

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List["NetworkTargetProps"]]:
        """Properties to specify NLB target groups.

        default
        :default: - default portMapping registered as target group and attached to the first defined listener

        stability
        :stability: experimental
        """
        return self._values.get('target_groups')

    @builtins.property
    def task_image_options(self) -> typing.Optional["NetworkLoadBalancedTaskImageProps"]:
        """The properties required to create a new task definition.

        Only one of TaskDefinition or TaskImageOptions must be specified.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('task_image_options')

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkMultipleTargetGroupsServiceBaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.NetworkTargetProps", jsii_struct_bases=[], name_mapping={'container_port': 'containerPort', 'listener': 'listener'})
class NetworkTargetProps():
    def __init__(self, *, container_port: jsii.Number, listener: typing.Optional[str]=None) -> None:
        """Properties to define a network load balancer target group.

        :param container_port: The port number of the container. Only applicable when using application/network load balancers.
        :param listener: Name of the listener the target group attached to. Default: - default listener (first added listener)

        stability
        :stability: experimental
        """
        self._values = {
            'container_port': container_port,
        }
        if listener is not None: self._values["listener"] = listener

    @builtins.property
    def container_port(self) -> jsii.Number:
        """The port number of the container.

        Only applicable when using application/network load balancers.

        stability
        :stability: experimental
        """
        return self._values.get('container_port')

    @builtins.property
    def listener(self) -> typing.Optional[str]:
        """Name of the listener the target group attached to.

        default
        :default: - default listener (first added listener)

        stability
        :stability: experimental
        """
        return self._values.get('listener')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkTargetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class QueueProcessingServiceBase(_Construct_f50a3f53, metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.aws_ecs_patterns.QueueProcessingServiceBase"):
    """The base class for QueueProcessingEc2Service and QueueProcessingFargateService services.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _QueueProcessingServiceBaseProxy

    def __init__(self, scope: _Construct_f50a3f53, id: str, *, image: _ContainerImage_99cc4b15, cluster: typing.Optional[_ICluster_5cbcc408]=None, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, family: typing.Optional[str]=None, log_driver: typing.Optional[_LogDriver_d09e7eb9]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, max_receive_count: typing.Optional[jsii.Number]=None, max_scaling_capacity: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, queue: typing.Optional[_IQueue_b743f559]=None, retention_period: typing.Optional[_Duration_5170c158]=None, scaling_steps: typing.Optional[typing.List[_ScalingInterval_fac05118]]=None, secrets: typing.Optional[typing.Mapping[str, _Secret_3f6909a4]]=None, service_name: typing.Optional[str]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """Constructs a new instance of the QueueProcessingServiceBase class.

        :param scope: -
        :param id: -
        :param image: The image used to start a container.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. The variable ``QUEUE_NAME`` with value ``queue.queueName`` will always be passed. Default: 'QUEUE_NAME: queue.queueName'
        :param family: The name of a family that the task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - default from underlying service.
        :param max_receive_count: The maximum number of times that a message can be received by consumers. When this value is exceeded for a message the message will be automatically sent to the Dead Letter Queue. Default: 3
        :param max_scaling_capacity: Maximum capacity to scale to. Default: (desiredTaskCount * 2)
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - default from underlying service.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_ Default: 'SQSQueue with CloudFormation-generated name'
        :param retention_period: The number of seconds that Dead Letter Queue retains a message. Default: Duration.days(14)
        :param scaling_steps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. See `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_ Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        props = QueueProcessingServiceBaseProps(image=image, cluster=cluster, command=command, desired_task_count=desired_task_count, enable_ecs_managed_tags=enable_ecs_managed_tags, enable_logging=enable_logging, environment=environment, family=family, log_driver=log_driver, max_healthy_percent=max_healthy_percent, max_receive_count=max_receive_count, max_scaling_capacity=max_scaling_capacity, min_healthy_percent=min_healthy_percent, propagate_tags=propagate_tags, queue=queue, retention_period=retention_period, scaling_steps=scaling_steps, secrets=secrets, service_name=service_name, vpc=vpc)

        jsii.create(QueueProcessingServiceBase, self, [scope, id, props])

    @jsii.member(jsii_name="configureAutoscalingForService")
    def _configure_autoscaling_for_service(self, service: _BaseService_c6e5f19d) -> None:
        """Configure autoscaling based off of CPU utilization as well as the number of messages visible in the SQS queue.

        :param service: the ECS/Fargate service for which to apply the autoscaling rules to.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "configureAutoscalingForService", [service])

    @jsii.member(jsii_name="getDefaultCluster")
    def _get_default_cluster(self, scope: _Construct_f50a3f53, vpc: typing.Optional[_IVpc_3795853f]=None) -> _Cluster_d0079260:
        """Returns the default cluster.

        :param scope: -
        :param vpc: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getDefaultCluster", [scope, vpc])

    @jsii.member(jsii_name="grantPermissionsToService")
    def _grant_permissions_to_service(self, service: _BaseService_c6e5f19d) -> None:
        """Grant SQS permissions to an ECS service.

        :param service: the ECS/Fargate service to which to grant SQS permissions.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantPermissionsToService", [service])

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> _ICluster_5cbcc408:
        """The cluster where your service will be deployed.

        stability
        :stability: experimental
        """
        return jsii.get(self, "cluster")

    @builtins.property
    @jsii.member(jsii_name="desiredCount")
    def desired_count(self) -> jsii.Number:
        """The minimum number of tasks to run.

        stability
        :stability: experimental
        """
        return jsii.get(self, "desiredCount")

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Mapping[str, str]:
        """Environment variables that will include the queue name.

        stability
        :stability: experimental
        """
        return jsii.get(self, "environment")

    @builtins.property
    @jsii.member(jsii_name="maxCapacity")
    def max_capacity(self) -> jsii.Number:
        """The maximum number of instances for autoscaling to scale up to.

        stability
        :stability: experimental
        """
        return jsii.get(self, "maxCapacity")

    @builtins.property
    @jsii.member(jsii_name="scalingSteps")
    def scaling_steps(self) -> typing.List[_ScalingInterval_fac05118]:
        """The scaling interval for autoscaling based off an SQS Queue size.

        stability
        :stability: experimental
        """
        return jsii.get(self, "scalingSteps")

    @builtins.property
    @jsii.member(jsii_name="sqsQueue")
    def sqs_queue(self) -> _IQueue_b743f559:
        """The SQS queue that the service will process from.

        stability
        :stability: experimental
        """
        return jsii.get(self, "sqsQueue")

    @builtins.property
    @jsii.member(jsii_name="deadLetterQueue")
    def dead_letter_queue(self) -> typing.Optional[_IQueue_b743f559]:
        """The dead letter queue for the primary SQS queue.

        stability
        :stability: experimental
        """
        return jsii.get(self, "deadLetterQueue")

    @builtins.property
    @jsii.member(jsii_name="logDriver")
    def log_driver(self) -> typing.Optional[_LogDriver_d09e7eb9]:
        """The AwsLogDriver to use for logging if logging is enabled.

        stability
        :stability: experimental
        """
        return jsii.get(self, "logDriver")

    @builtins.property
    @jsii.member(jsii_name="secrets")
    def secrets(self) -> typing.Optional[typing.Mapping[str, _Secret_3f6909a4]]:
        """The secret environment variables.

        stability
        :stability: experimental
        """
        return jsii.get(self, "secrets")


class _QueueProcessingServiceBaseProxy(QueueProcessingServiceBase):
    pass

@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.QueueProcessingServiceBaseProps", jsii_struct_bases=[], name_mapping={'image': 'image', 'cluster': 'cluster', 'command': 'command', 'desired_task_count': 'desiredTaskCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'enable_logging': 'enableLogging', 'environment': 'environment', 'family': 'family', 'log_driver': 'logDriver', 'max_healthy_percent': 'maxHealthyPercent', 'max_receive_count': 'maxReceiveCount', 'max_scaling_capacity': 'maxScalingCapacity', 'min_healthy_percent': 'minHealthyPercent', 'propagate_tags': 'propagateTags', 'queue': 'queue', 'retention_period': 'retentionPeriod', 'scaling_steps': 'scalingSteps', 'secrets': 'secrets', 'service_name': 'serviceName', 'vpc': 'vpc'})
class QueueProcessingServiceBaseProps():
    def __init__(self, *, image: _ContainerImage_99cc4b15, cluster: typing.Optional[_ICluster_5cbcc408]=None, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, family: typing.Optional[str]=None, log_driver: typing.Optional[_LogDriver_d09e7eb9]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, max_receive_count: typing.Optional[jsii.Number]=None, max_scaling_capacity: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, queue: typing.Optional[_IQueue_b743f559]=None, retention_period: typing.Optional[_Duration_5170c158]=None, scaling_steps: typing.Optional[typing.List[_ScalingInterval_fac05118]]=None, secrets: typing.Optional[typing.Mapping[str, _Secret_3f6909a4]]=None, service_name: typing.Optional[str]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """The properties for the base QueueProcessingEc2Service or QueueProcessingFargateService service.

        :param image: The image used to start a container.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. The variable ``QUEUE_NAME`` with value ``queue.queueName`` will always be passed. Default: 'QUEUE_NAME: queue.queueName'
        :param family: The name of a family that the task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - default from underlying service.
        :param max_receive_count: The maximum number of times that a message can be received by consumers. When this value is exceeded for a message the message will be automatically sent to the Dead Letter Queue. Default: 3
        :param max_scaling_capacity: Maximum capacity to scale to. Default: (desiredTaskCount * 2)
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - default from underlying service.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_ Default: 'SQSQueue with CloudFormation-generated name'
        :param retention_period: The number of seconds that Dead Letter Queue retains a message. Default: Duration.days(14)
        :param scaling_steps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. See `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_ Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        self._values = {
            'image': image,
        }
        if cluster is not None: self._values["cluster"] = cluster
        if command is not None: self._values["command"] = command
        if desired_task_count is not None: self._values["desired_task_count"] = desired_task_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if enable_logging is not None: self._values["enable_logging"] = enable_logging
        if environment is not None: self._values["environment"] = environment
        if family is not None: self._values["family"] = family
        if log_driver is not None: self._values["log_driver"] = log_driver
        if max_healthy_percent is not None: self._values["max_healthy_percent"] = max_healthy_percent
        if max_receive_count is not None: self._values["max_receive_count"] = max_receive_count
        if max_scaling_capacity is not None: self._values["max_scaling_capacity"] = max_scaling_capacity
        if min_healthy_percent is not None: self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if queue is not None: self._values["queue"] = queue
        if retention_period is not None: self._values["retention_period"] = retention_period
        if scaling_steps is not None: self._values["scaling_steps"] = scaling_steps
        if secrets is not None: self._values["secrets"] = secrets
        if service_name is not None: self._values["service_name"] = service_name
        if vpc is not None: self._values["vpc"] = vpc

    @builtins.property
    def image(self) -> _ContainerImage_99cc4b15:
        """The image used to start a container.

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @builtins.property
    def cluster(self) -> typing.Optional[_ICluster_5cbcc408]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        default
        :default: - CMD value built into container image.

        stability
        :stability: experimental
        """
        return self._values.get('command')

    @builtins.property
    def desired_task_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_task_count')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def enable_logging(self) -> typing.Optional[bool]:
        """Flag to indicate whether to enable logging.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('enable_logging')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The environment variables to pass to the container.

        The variable ``QUEUE_NAME`` with value ``queue.queueName`` will
        always be passed.

        default
        :default: 'QUEUE_NAME: queue.queueName'

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def family(self) -> typing.Optional[str]:
        """The name of a family that the task definition is registered to.

        A family groups multiple versions of a task definition.

        default
        :default: - Automatically generated name.

        stability
        :stability: experimental
        """
        return self._values.get('family')

    @builtins.property
    def log_driver(self) -> typing.Optional[_LogDriver_d09e7eb9]:
        """The log driver to use.

        default
        :default: - AwsLogDriver if enableLogging is true

        stability
        :stability: experimental
        """
        return self._values.get('log_driver')

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        default
        :default: - default from underlying service.

        stability
        :stability: experimental
        """
        return self._values.get('max_healthy_percent')

    @builtins.property
    def max_receive_count(self) -> typing.Optional[jsii.Number]:
        """The maximum number of times that a message can be received by consumers.

        When this value is exceeded for a message the message will be automatically sent to the Dead Letter Queue.

        default
        :default: 3

        stability
        :stability: experimental
        """
        return self._values.get('max_receive_count')

    @builtins.property
    def max_scaling_capacity(self) -> typing.Optional[jsii.Number]:
        """Maximum capacity to scale to.

        default
        :default: (desiredTaskCount * 2)

        stability
        :stability: experimental
        """
        return self._values.get('max_scaling_capacity')

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        default
        :default: - default from underlying service.

        stability
        :stability: experimental
        """
        return self._values.get('min_healthy_percent')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[_PropagatedTagSource_e36ef3c2]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def queue(self) -> typing.Optional[_IQueue_b743f559]:
        """A queue for which to process items from.

        If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See
        `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_

        default
        :default: 'SQSQueue with CloudFormation-generated name'

        stability
        :stability: experimental
        """
        return self._values.get('queue')

    @builtins.property
    def retention_period(self) -> typing.Optional[_Duration_5170c158]:
        """The number of seconds that Dead Letter Queue retains a message.

        default
        :default: Duration.days(14)

        stability
        :stability: experimental
        """
        return self._values.get('retention_period')

    @builtins.property
    def scaling_steps(self) -> typing.Optional[typing.List[_ScalingInterval_fac05118]]:
        """The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric.

        Maps a range of metric values to a particular scaling behavior. See
        `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_

        default
        :default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]

        stability
        :stability: experimental
        """
        return self._values.get('scaling_steps')

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[str, _Secret_3f6909a4]]:
        """The secret to expose to the container as an environment variable.

        default
        :default: - No secret environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('secrets')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.

        stability
        :stability: experimental
        """
        return self._values.get('service_name')

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'QueueProcessingServiceBaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.ScheduledEc2TaskDefinitionOptions", jsii_struct_bases=[], name_mapping={'task_definition': 'taskDefinition'})
class ScheduledEc2TaskDefinitionOptions():
    def __init__(self, *, task_definition: _Ec2TaskDefinition_96cf505d) -> None:
        """The properties for the ScheduledEc2Task using a task definition.

        :param task_definition: The task definition to use for tasks in the service. One of image or taskDefinition must be specified. [disable-awslint:ref-via-interface] Default: - none

        stability
        :stability: experimental
        """
        self._values = {
            'task_definition': task_definition,
        }

    @builtins.property
    def task_definition(self) -> _Ec2TaskDefinition_96cf505d:
        """The task definition to use for tasks in the service. One of image or taskDefinition must be specified.

        [disable-awslint:ref-via-interface]

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('task_definition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScheduledEc2TaskDefinitionOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.ScheduledFargateTaskDefinitionOptions", jsii_struct_bases=[], name_mapping={'task_definition': 'taskDefinition'})
class ScheduledFargateTaskDefinitionOptions():
    def __init__(self, *, task_definition: _FargateTaskDefinition_c5f42010) -> None:
        """The properties for the ScheduledFargateTask using a task definition.

        :param task_definition: The task definition to use for tasks in the service. Image or taskDefinition must be specified, but not both. [disable-awslint:ref-via-interface] Default: - none

        stability
        :stability: experimental
        """
        self._values = {
            'task_definition': task_definition,
        }

    @builtins.property
    def task_definition(self) -> _FargateTaskDefinition_c5f42010:
        """The task definition to use for tasks in the service. Image or taskDefinition must be specified, but not both.

        [disable-awslint:ref-via-interface]

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('task_definition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScheduledFargateTaskDefinitionOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ScheduledTaskBase(_Construct_f50a3f53, metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.aws_ecs_patterns.ScheduledTaskBase"):
    """The base class for ScheduledEc2Task and ScheduledFargateTask tasks.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ScheduledTaskBaseProxy

    def __init__(self, scope: _Construct_f50a3f53, id: str, *, schedule: _Schedule_6cd13e0d, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_task_count: typing.Optional[jsii.Number]=None, subnet_selection: typing.Optional[_SubnetSelection_36a13cd6]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """Constructs a new instance of the ScheduledTaskBase class.

        :param scope: -
        :param id: -
        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_ in the Amazon CloudWatch User Guide.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param subnet_selection: In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        props = ScheduledTaskBaseProps(schedule=schedule, cluster=cluster, desired_task_count=desired_task_count, subnet_selection=subnet_selection, vpc=vpc)

        jsii.create(ScheduledTaskBase, self, [scope, id, props])

    @jsii.member(jsii_name="addTaskDefinitionToEventTarget")
    def _add_task_definition_to_event_target(self, task_definition: _TaskDefinition_acfbb011) -> _EcsTask_1d951afe:
        """Create an ECS task using the task definition provided and add it to the scheduled event rule.

        :param task_definition: the TaskDefinition to add to the event rule.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addTaskDefinitionToEventTarget", [task_definition])

    @jsii.member(jsii_name="createAWSLogDriver")
    def _create_aws_log_driver(self, prefix: str) -> _AwsLogDriver_a24c479b:
        """Create an AWS Log Driver with the provided streamPrefix.

        :param prefix: the Cloudwatch logging prefix.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "createAWSLogDriver", [prefix])

    @jsii.member(jsii_name="getDefaultCluster")
    def _get_default_cluster(self, scope: _Construct_f50a3f53, vpc: typing.Optional[_IVpc_3795853f]=None) -> _Cluster_d0079260:
        """Returns the default cluster.

        :param scope: -
        :param vpc: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getDefaultCluster", [scope, vpc])

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> _ICluster_5cbcc408:
        """The name of the cluster that hosts the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "cluster")

    @builtins.property
    @jsii.member(jsii_name="desiredTaskCount")
    def desired_task_count(self) -> jsii.Number:
        """The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        stability
        :stability: experimental
        """
        return jsii.get(self, "desiredTaskCount")

    @builtins.property
    @jsii.member(jsii_name="eventRule")
    def event_rule(self) -> _Rule_c38e0b39:
        """The CloudWatch Events rule for the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "eventRule")

    @builtins.property
    @jsii.member(jsii_name="subnetSelection")
    def subnet_selection(self) -> _SubnetSelection_36a13cd6:
        """In what subnets to place the task's ENIs.

        (Only applicable in case the TaskDefinition is configured for AwsVpc networking)

        default
        :default: Private subnets

        stability
        :stability: experimental
        """
        return jsii.get(self, "subnetSelection")


class _ScheduledTaskBaseProxy(ScheduledTaskBase):
    pass

@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.ScheduledTaskBaseProps", jsii_struct_bases=[], name_mapping={'schedule': 'schedule', 'cluster': 'cluster', 'desired_task_count': 'desiredTaskCount', 'subnet_selection': 'subnetSelection', 'vpc': 'vpc'})
class ScheduledTaskBaseProps():
    def __init__(self, *, schedule: _Schedule_6cd13e0d, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_task_count: typing.Optional[jsii.Number]=None, subnet_selection: typing.Optional[_SubnetSelection_36a13cd6]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """The properties for the base ScheduledEc2Task or ScheduledFargateTask task.

        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_ in the Amazon CloudWatch User Guide.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param subnet_selection: In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        if isinstance(subnet_selection, dict): subnet_selection = _SubnetSelection_36a13cd6(**subnet_selection)
        self._values = {
            'schedule': schedule,
        }
        if cluster is not None: self._values["cluster"] = cluster
        if desired_task_count is not None: self._values["desired_task_count"] = desired_task_count
        if subnet_selection is not None: self._values["subnet_selection"] = subnet_selection
        if vpc is not None: self._values["vpc"] = vpc

    @builtins.property
    def schedule(self) -> _Schedule_6cd13e0d:
        """The schedule or rate (frequency) that determines when CloudWatch Events runs the rule.

        For more information, see
        `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_
        in the Amazon CloudWatch User Guide.

        stability
        :stability: experimental
        """
        return self._values.get('schedule')

    @builtins.property
    def cluster(self) -> typing.Optional[_ICluster_5cbcc408]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_task_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_task_count')

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
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScheduledTaskBaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.ScheduledTaskImageProps", jsii_struct_bases=[], name_mapping={'image': 'image', 'command': 'command', 'environment': 'environment', 'log_driver': 'logDriver', 'secrets': 'secrets'})
class ScheduledTaskImageProps():
    def __init__(self, *, image: _ContainerImage_99cc4b15, command: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, log_driver: typing.Optional[_LogDriver_d09e7eb9]=None, secrets: typing.Optional[typing.Mapping[str, _Secret_3f6909a4]]=None) -> None:
        """
        :param image: The image used to start a container. Image or taskDefinition must be specified, but not both. Default: - none
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param environment: The environment variables to pass to the container. Default: none
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.

        stability
        :stability: experimental
        """
        self._values = {
            'image': image,
        }
        if command is not None: self._values["command"] = command
        if environment is not None: self._values["environment"] = environment
        if log_driver is not None: self._values["log_driver"] = log_driver
        if secrets is not None: self._values["secrets"] = secrets

    @builtins.property
    def image(self) -> _ContainerImage_99cc4b15:
        """The image used to start a container.

        Image or taskDefinition must be specified, but not both.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @builtins.property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        default
        :default: - CMD value built into container image.

        stability
        :stability: experimental
        """
        return self._values.get('command')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The environment variables to pass to the container.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def log_driver(self) -> typing.Optional[_LogDriver_d09e7eb9]:
        """The log driver to use.

        default
        :default: - AwsLogDriver if enableLogging is true

        stability
        :stability: experimental
        """
        return self._values.get('log_driver')

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[str, _Secret_3f6909a4]]:
        """The secret to expose to the container as an environment variable.

        default
        :default: - No secret environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('secrets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScheduledTaskImageProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ApplicationLoadBalancedEc2Service(ApplicationLoadBalancedServiceBase, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs_patterns.ApplicationLoadBalancedEc2Service"):
    """An EC2 service running on an ECS cluster fronted by an application load balancer.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, task_definition: typing.Optional[_Ec2TaskDefinition_96cf505d]=None, certificate: typing.Optional[_ICertificate_8f3d4c96]=None, cloud_map_options: typing.Optional[_CloudMapOptions_25ce57e4]=None, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[_IHostedZone_59ffab76]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, listener_port: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[_IApplicationLoadBalancer_9d681ef6]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, protocol: typing.Optional[_ApplicationProtocol_60c416f7]=None, public_load_balancer: typing.Optional[bool]=None, service_name: typing.Optional[str]=None, task_image_options: typing.Optional["ApplicationLoadBalancedTaskImageOptions"]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """Constructs a new instance of the ApplicationLoadBalancedEc2Service class.

        :param scope: -
        :param id: -
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: none
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory reserved.
        :param task_definition: The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both.. [disable-awslint:ref-via-interface] Default: - none
        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer protocol to HTTPS. Default: - No certificate associated with the load balancer, if using the HTTP protocol. For HTTPS, a DNS-validated certificate will be created for the load balancer's specified domain name.
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the application load balancer that will serve traffic to the service. Default: - The default listener port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.
        :param load_balancer: The application load balancer that will serve traffic to the service. The VPC attribute of a load balancer must be specified for it to be used to create a new service with this pattern. [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param protocol: The protocol for connections from clients to the load balancer. The load balancer port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS. Default: HTTP. If a certificate is specified, the protocol will be set by default to HTTPS.
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. TaskDefinition or TaskImageOptions must be specified, but not both. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        props = ApplicationLoadBalancedEc2ServiceProps(cpu=cpu, memory_limit_mib=memory_limit_mib, memory_reservation_mib=memory_reservation_mib, task_definition=task_definition, certificate=certificate, cloud_map_options=cloud_map_options, cluster=cluster, desired_count=desired_count, domain_name=domain_name, domain_zone=domain_zone, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, listener_port=listener_port, load_balancer=load_balancer, max_healthy_percent=max_healthy_percent, min_healthy_percent=min_healthy_percent, propagate_tags=propagate_tags, protocol=protocol, public_load_balancer=public_load_balancer, service_name=service_name, task_image_options=task_image_options, vpc=vpc)

        jsii.create(ApplicationLoadBalancedEc2Service, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> _Ec2Service_c4ac147a:
        """The EC2 service in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "service")

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _Ec2TaskDefinition_96cf505d:
        """The EC2 Task Definition in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "taskDefinition")


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.ApplicationLoadBalancedEc2ServiceProps", jsii_struct_bases=[ApplicationLoadBalancedServiceBaseProps], name_mapping={'certificate': 'certificate', 'cloud_map_options': 'cloudMapOptions', 'cluster': 'cluster', 'desired_count': 'desiredCount', 'domain_name': 'domainName', 'domain_zone': 'domainZone', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'listener_port': 'listenerPort', 'load_balancer': 'loadBalancer', 'max_healthy_percent': 'maxHealthyPercent', 'min_healthy_percent': 'minHealthyPercent', 'propagate_tags': 'propagateTags', 'protocol': 'protocol', 'public_load_balancer': 'publicLoadBalancer', 'service_name': 'serviceName', 'task_image_options': 'taskImageOptions', 'vpc': 'vpc', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB', 'memory_reservation_mib': 'memoryReservationMiB', 'task_definition': 'taskDefinition'})
class ApplicationLoadBalancedEc2ServiceProps(ApplicationLoadBalancedServiceBaseProps):
    def __init__(self, *, certificate: typing.Optional[_ICertificate_8f3d4c96]=None, cloud_map_options: typing.Optional[_CloudMapOptions_25ce57e4]=None, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[_IHostedZone_59ffab76]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, listener_port: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[_IApplicationLoadBalancer_9d681ef6]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, protocol: typing.Optional[_ApplicationProtocol_60c416f7]=None, public_load_balancer: typing.Optional[bool]=None, service_name: typing.Optional[str]=None, task_image_options: typing.Optional["ApplicationLoadBalancedTaskImageOptions"]=None, vpc: typing.Optional[_IVpc_3795853f]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, task_definition: typing.Optional[_Ec2TaskDefinition_96cf505d]=None) -> None:
        """The properties for the ApplicationLoadBalancedEc2Service service.

        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer protocol to HTTPS. Default: - No certificate associated with the load balancer, if using the HTTP protocol. For HTTPS, a DNS-validated certificate will be created for the load balancer's specified domain name.
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the application load balancer that will serve traffic to the service. Default: - The default listener port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.
        :param load_balancer: The application load balancer that will serve traffic to the service. The VPC attribute of a load balancer must be specified for it to be used to create a new service with this pattern. [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param protocol: The protocol for connections from clients to the load balancer. The load balancer port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS. Default: HTTP. If a certificate is specified, the protocol will be set by default to HTTPS.
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. TaskDefinition or TaskImageOptions must be specified, but not both. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: none
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory reserved.
        :param task_definition: The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both.. [disable-awslint:ref-via-interface] Default: - none

        stability
        :stability: experimental
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = _CloudMapOptions_25ce57e4(**cloud_map_options)
        if isinstance(task_image_options, dict): task_image_options = ApplicationLoadBalancedTaskImageOptions(**task_image_options)
        self._values = {
        }
        if certificate is not None: self._values["certificate"] = certificate
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None: self._values["cluster"] = cluster
        if desired_count is not None: self._values["desired_count"] = desired_count
        if domain_name is not None: self._values["domain_name"] = domain_name
        if domain_zone is not None: self._values["domain_zone"] = domain_zone
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if listener_port is not None: self._values["listener_port"] = listener_port
        if load_balancer is not None: self._values["load_balancer"] = load_balancer
        if max_healthy_percent is not None: self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None: self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if protocol is not None: self._values["protocol"] = protocol
        if public_load_balancer is not None: self._values["public_load_balancer"] = public_load_balancer
        if service_name is not None: self._values["service_name"] = service_name
        if task_image_options is not None: self._values["task_image_options"] = task_image_options
        if vpc is not None: self._values["vpc"] = vpc
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None: self._values["memory_reservation_mib"] = memory_reservation_mib
        if task_definition is not None: self._values["task_definition"] = task_definition

    @builtins.property
    def certificate(self) -> typing.Optional[_ICertificate_8f3d4c96]:
        """Certificate Manager certificate to associate with the load balancer.

        Setting this option will set the load balancer protocol to HTTPS.

        default
        :default:

        - No certificate associated with the load balancer, if using
          the HTTP protocol. For HTTPS, a DNS-validated certificate will be
          created for the load balancer's specified domain name.

        stability
        :stability: experimental
        """
        return self._values.get('certificate')

    @builtins.property
    def cloud_map_options(self) -> typing.Optional[_CloudMapOptions_25ce57e4]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.

        stability
        :stability: experimental
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def cluster(self) -> typing.Optional[_ICluster_5cbcc408]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_count')

    @builtins.property
    def domain_name(self) -> typing.Optional[str]:
        """The domain name for the service, e.g. "api.example.com.".

        default
        :default: - No domain name.

        stability
        :stability: experimental
        """
        return self._values.get('domain_name')

    @builtins.property
    def domain_zone(self) -> typing.Optional[_IHostedZone_59ffab76]:
        """The Route53 hosted zone for the domain, e.g. "example.com.".

        default
        :default: - No Route53 hosted domain zone.

        stability
        :stability: experimental
        """
        return self._values.get('domain_zone')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[_Duration_5170c158]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set

        stability
        :stability: experimental
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        """Listener port of the application load balancer that will serve traffic to the service.

        default
        :default:

        - The default listener port is determined from the protocol (port 80 for HTTP,
          port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.

        stability
        :stability: experimental
        """
        return self._values.get('listener_port')

    @builtins.property
    def load_balancer(self) -> typing.Optional[_IApplicationLoadBalancer_9d681ef6]:
        """The application load balancer that will serve traffic to the service.

        The VPC attribute of a load balancer must be specified for it to be used
        to create a new service with this pattern.

        [disable-awslint:ref-via-interface]

        default
        :default: - a new load balancer will be created.

        stability
        :stability: experimental
        """
        return self._values.get('load_balancer')

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        default
        :default: - 100 if daemon, otherwise 200

        stability
        :stability: experimental
        """
        return self._values.get('max_healthy_percent')

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        default
        :default: - 0 if daemon, otherwise 50

        stability
        :stability: experimental
        """
        return self._values.get('min_healthy_percent')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[_PropagatedTagSource_e36ef3c2]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def protocol(self) -> typing.Optional[_ApplicationProtocol_60c416f7]:
        """The protocol for connections from clients to the load balancer.

        The load balancer port is determined from the protocol (port 80 for
        HTTP, port 443 for HTTPS).  A domain name and zone must be also be
        specified if using HTTPS.

        default
        :default:

        HTTP. If a certificate is specified, the protocol will be
        set by default to HTTPS.

        stability
        :stability: experimental
        """
        return self._values.get('protocol')

    @builtins.property
    def public_load_balancer(self) -> typing.Optional[bool]:
        """Determines whether the Load Balancer will be internet-facing.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('public_load_balancer')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.

        stability
        :stability: experimental
        """
        return self._values.get('service_name')

    @builtins.property
    def task_image_options(self) -> typing.Optional["ApplicationLoadBalancedTaskImageOptions"]:
        """The properties required to create a new task definition.

        TaskDefinition or TaskImageOptions must be specified, but not both.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('task_image_options')

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The hard limit (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        default
        :default: - No memory limit.

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        """The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under contention, Docker attempts to keep the
        container memory within the limit. If the container requires more memory,
        it can consume up to the value specified by the Memory property or all of
        the available memory on the container instance—whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        default
        :default: - No memory reserved.

        stability
        :stability: experimental
        """
        return self._values.get('memory_reservation_mib')

    @builtins.property
    def task_definition(self) -> typing.Optional[_Ec2TaskDefinition_96cf505d]:
        """The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both..

        [disable-awslint:ref-via-interface]

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('task_definition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationLoadBalancedEc2ServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ApplicationLoadBalancedFargateService(ApplicationLoadBalancedServiceBase, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs_patterns.ApplicationLoadBalancedFargateService"):
    """A Fargate service running on an ECS cluster fronted by an application load balancer.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, assign_public_ip: typing.Optional[bool]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, platform_version: typing.Optional[_FargatePlatformVersion_187ad0f4]=None, task_definition: typing.Optional[_FargateTaskDefinition_c5f42010]=None, certificate: typing.Optional[_ICertificate_8f3d4c96]=None, cloud_map_options: typing.Optional[_CloudMapOptions_25ce57e4]=None, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[_IHostedZone_59ffab76]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, listener_port: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[_IApplicationLoadBalancer_9d681ef6]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, protocol: typing.Optional[_ApplicationProtocol_60c416f7]=None, public_load_balancer: typing.Optional[bool]=None, service_name: typing.Optional[str]=None, task_image_options: typing.Optional["ApplicationLoadBalancedTaskImageOptions"]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """Constructs a new instance of the ApplicationLoadBalancedFargateService class.

        :param scope: -
        :param id: -
        :param assign_public_ip: Determines whether the service will be assigned a public IP address. Default: false
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param task_definition: The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both. [disable-awslint:ref-via-interface] Default: - none
        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer protocol to HTTPS. Default: - No certificate associated with the load balancer, if using the HTTP protocol. For HTTPS, a DNS-validated certificate will be created for the load balancer's specified domain name.
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the application load balancer that will serve traffic to the service. Default: - The default listener port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.
        :param load_balancer: The application load balancer that will serve traffic to the service. The VPC attribute of a load balancer must be specified for it to be used to create a new service with this pattern. [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param protocol: The protocol for connections from clients to the load balancer. The load balancer port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS. Default: HTTP. If a certificate is specified, the protocol will be set by default to HTTPS.
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. TaskDefinition or TaskImageOptions must be specified, but not both. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        props = ApplicationLoadBalancedFargateServiceProps(assign_public_ip=assign_public_ip, cpu=cpu, memory_limit_mib=memory_limit_mib, platform_version=platform_version, task_definition=task_definition, certificate=certificate, cloud_map_options=cloud_map_options, cluster=cluster, desired_count=desired_count, domain_name=domain_name, domain_zone=domain_zone, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, listener_port=listener_port, load_balancer=load_balancer, max_healthy_percent=max_healthy_percent, min_healthy_percent=min_healthy_percent, propagate_tags=propagate_tags, protocol=protocol, public_load_balancer=public_load_balancer, service_name=service_name, task_image_options=task_image_options, vpc=vpc)

        jsii.create(ApplicationLoadBalancedFargateService, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="assignPublicIp")
    def assign_public_ip(self) -> bool:
        """Determines whether the service will be assigned a public IP address.

        stability
        :stability: experimental
        """
        return jsii.get(self, "assignPublicIp")

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> _FargateService_e4491ea2:
        """The Fargate service in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "service")

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _FargateTaskDefinition_c5f42010:
        """The Fargate task definition in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "taskDefinition")


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.ApplicationLoadBalancedFargateServiceProps", jsii_struct_bases=[ApplicationLoadBalancedServiceBaseProps], name_mapping={'certificate': 'certificate', 'cloud_map_options': 'cloudMapOptions', 'cluster': 'cluster', 'desired_count': 'desiredCount', 'domain_name': 'domainName', 'domain_zone': 'domainZone', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'listener_port': 'listenerPort', 'load_balancer': 'loadBalancer', 'max_healthy_percent': 'maxHealthyPercent', 'min_healthy_percent': 'minHealthyPercent', 'propagate_tags': 'propagateTags', 'protocol': 'protocol', 'public_load_balancer': 'publicLoadBalancer', 'service_name': 'serviceName', 'task_image_options': 'taskImageOptions', 'vpc': 'vpc', 'assign_public_ip': 'assignPublicIp', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB', 'platform_version': 'platformVersion', 'task_definition': 'taskDefinition'})
class ApplicationLoadBalancedFargateServiceProps(ApplicationLoadBalancedServiceBaseProps):
    def __init__(self, *, certificate: typing.Optional[_ICertificate_8f3d4c96]=None, cloud_map_options: typing.Optional[_CloudMapOptions_25ce57e4]=None, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[_IHostedZone_59ffab76]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, listener_port: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[_IApplicationLoadBalancer_9d681ef6]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, protocol: typing.Optional[_ApplicationProtocol_60c416f7]=None, public_load_balancer: typing.Optional[bool]=None, service_name: typing.Optional[str]=None, task_image_options: typing.Optional["ApplicationLoadBalancedTaskImageOptions"]=None, vpc: typing.Optional[_IVpc_3795853f]=None, assign_public_ip: typing.Optional[bool]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, platform_version: typing.Optional[_FargatePlatformVersion_187ad0f4]=None, task_definition: typing.Optional[_FargateTaskDefinition_c5f42010]=None) -> None:
        """The properties for the ApplicationLoadBalancedFargateService service.

        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer protocol to HTTPS. Default: - No certificate associated with the load balancer, if using the HTTP protocol. For HTTPS, a DNS-validated certificate will be created for the load balancer's specified domain name.
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the application load balancer that will serve traffic to the service. Default: - The default listener port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.
        :param load_balancer: The application load balancer that will serve traffic to the service. The VPC attribute of a load balancer must be specified for it to be used to create a new service with this pattern. [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param protocol: The protocol for connections from clients to the load balancer. The load balancer port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS. Default: HTTP. If a certificate is specified, the protocol will be set by default to HTTPS.
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. TaskDefinition or TaskImageOptions must be specified, but not both. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param assign_public_ip: Determines whether the service will be assigned a public IP address. Default: false
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param task_definition: The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both. [disable-awslint:ref-via-interface] Default: - none

        stability
        :stability: experimental
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = _CloudMapOptions_25ce57e4(**cloud_map_options)
        if isinstance(task_image_options, dict): task_image_options = ApplicationLoadBalancedTaskImageOptions(**task_image_options)
        self._values = {
        }
        if certificate is not None: self._values["certificate"] = certificate
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None: self._values["cluster"] = cluster
        if desired_count is not None: self._values["desired_count"] = desired_count
        if domain_name is not None: self._values["domain_name"] = domain_name
        if domain_zone is not None: self._values["domain_zone"] = domain_zone
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if listener_port is not None: self._values["listener_port"] = listener_port
        if load_balancer is not None: self._values["load_balancer"] = load_balancer
        if max_healthy_percent is not None: self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None: self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if protocol is not None: self._values["protocol"] = protocol
        if public_load_balancer is not None: self._values["public_load_balancer"] = public_load_balancer
        if service_name is not None: self._values["service_name"] = service_name
        if task_image_options is not None: self._values["task_image_options"] = task_image_options
        if vpc is not None: self._values["vpc"] = vpc
        if assign_public_ip is not None: self._values["assign_public_ip"] = assign_public_ip
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if platform_version is not None: self._values["platform_version"] = platform_version
        if task_definition is not None: self._values["task_definition"] = task_definition

    @builtins.property
    def certificate(self) -> typing.Optional[_ICertificate_8f3d4c96]:
        """Certificate Manager certificate to associate with the load balancer.

        Setting this option will set the load balancer protocol to HTTPS.

        default
        :default:

        - No certificate associated with the load balancer, if using
          the HTTP protocol. For HTTPS, a DNS-validated certificate will be
          created for the load balancer's specified domain name.

        stability
        :stability: experimental
        """
        return self._values.get('certificate')

    @builtins.property
    def cloud_map_options(self) -> typing.Optional[_CloudMapOptions_25ce57e4]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.

        stability
        :stability: experimental
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def cluster(self) -> typing.Optional[_ICluster_5cbcc408]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_count')

    @builtins.property
    def domain_name(self) -> typing.Optional[str]:
        """The domain name for the service, e.g. "api.example.com.".

        default
        :default: - No domain name.

        stability
        :stability: experimental
        """
        return self._values.get('domain_name')

    @builtins.property
    def domain_zone(self) -> typing.Optional[_IHostedZone_59ffab76]:
        """The Route53 hosted zone for the domain, e.g. "example.com.".

        default
        :default: - No Route53 hosted domain zone.

        stability
        :stability: experimental
        """
        return self._values.get('domain_zone')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[_Duration_5170c158]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set

        stability
        :stability: experimental
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        """Listener port of the application load balancer that will serve traffic to the service.

        default
        :default:

        - The default listener port is determined from the protocol (port 80 for HTTP,
          port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.

        stability
        :stability: experimental
        """
        return self._values.get('listener_port')

    @builtins.property
    def load_balancer(self) -> typing.Optional[_IApplicationLoadBalancer_9d681ef6]:
        """The application load balancer that will serve traffic to the service.

        The VPC attribute of a load balancer must be specified for it to be used
        to create a new service with this pattern.

        [disable-awslint:ref-via-interface]

        default
        :default: - a new load balancer will be created.

        stability
        :stability: experimental
        """
        return self._values.get('load_balancer')

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        default
        :default: - 100 if daemon, otherwise 200

        stability
        :stability: experimental
        """
        return self._values.get('max_healthy_percent')

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        default
        :default: - 0 if daemon, otherwise 50

        stability
        :stability: experimental
        """
        return self._values.get('min_healthy_percent')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[_PropagatedTagSource_e36ef3c2]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def protocol(self) -> typing.Optional[_ApplicationProtocol_60c416f7]:
        """The protocol for connections from clients to the load balancer.

        The load balancer port is determined from the protocol (port 80 for
        HTTP, port 443 for HTTPS).  A domain name and zone must be also be
        specified if using HTTPS.

        default
        :default:

        HTTP. If a certificate is specified, the protocol will be
        set by default to HTTPS.

        stability
        :stability: experimental
        """
        return self._values.get('protocol')

    @builtins.property
    def public_load_balancer(self) -> typing.Optional[bool]:
        """Determines whether the Load Balancer will be internet-facing.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('public_load_balancer')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.

        stability
        :stability: experimental
        """
        return self._values.get('service_name')

    @builtins.property
    def task_image_options(self) -> typing.Optional["ApplicationLoadBalancedTaskImageOptions"]:
        """The properties required to create a new task definition.

        TaskDefinition or TaskImageOptions must be specified, but not both.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('task_image_options')

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[bool]:
        """Determines whether the service will be assigned a public IP address.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('assign_public_ip')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 256

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory used by the task.

        This field is required and you must use one of the following values, which determines your range of valid values
        for the cpu parameter:

        512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU)

        1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU)

        2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU)

        Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU)

        Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU)

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 512

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def platform_version(self) -> typing.Optional[_FargatePlatformVersion_187ad0f4]:
        """The platform version on which to run your service.

        If one is not specified, the LATEST platform version is used by default. For more information, see
        `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_
        in the Amazon Elastic Container Service Developer Guide.

        default
        :default: Latest

        stability
        :stability: experimental
        """
        return self._values.get('platform_version')

    @builtins.property
    def task_definition(self) -> typing.Optional[_FargateTaskDefinition_c5f42010]:
        """The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both.

        [disable-awslint:ref-via-interface]

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('task_definition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationLoadBalancedFargateServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ApplicationMultipleTargetGroupsEc2Service(ApplicationMultipleTargetGroupsServiceBase, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs_patterns.ApplicationMultipleTargetGroupsEc2Service"):
    """An EC2 service running on an ECS cluster fronted by an application load balancer.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, task_definition: typing.Optional[_Ec2TaskDefinition_96cf505d]=None, cloud_map_options: typing.Optional[_CloudMapOptions_25ce57e4]=None, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, load_balancers: typing.Optional[typing.List["ApplicationLoadBalancerProps"]]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, service_name: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["ApplicationTargetProps"]]=None, task_image_options: typing.Optional["ApplicationLoadBalancedTaskImageProps"]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """Constructs a new instance of the ApplicationMultipleTargetGroupsEc2Service class.

        :param scope: -
        :param id: -
        :param cpu: The minimum number of CPU units to reserve for the container. Valid values, which determines your range of valid values for the memory parameter: Default: - No minimum CPU units reserved.
        :param memory_limit_mib: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Note that this setting will be ignored if TaskImagesOptions is specified Default: - No memory reserved.
        :param task_definition: The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified. [disable-awslint:ref-via-interface] Default: - none
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The application load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify ALB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        props = ApplicationMultipleTargetGroupsEc2ServiceProps(cpu=cpu, memory_limit_mib=memory_limit_mib, memory_reservation_mib=memory_reservation_mib, task_definition=task_definition, cloud_map_options=cloud_map_options, cluster=cluster, desired_count=desired_count, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, load_balancers=load_balancers, propagate_tags=propagate_tags, service_name=service_name, target_groups=target_groups, task_image_options=task_image_options, vpc=vpc)

        jsii.create(ApplicationMultipleTargetGroupsEc2Service, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> _Ec2Service_c4ac147a:
        """The EC2 service in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "service")

    @builtins.property
    @jsii.member(jsii_name="targetGroup")
    def target_group(self) -> _ApplicationTargetGroup_7d0a8d54:
        """The default target group for the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "targetGroup")

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _Ec2TaskDefinition_96cf505d:
        """The EC2 Task Definition in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "taskDefinition")


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.ApplicationMultipleTargetGroupsEc2ServiceProps", jsii_struct_bases=[ApplicationMultipleTargetGroupsServiceBaseProps], name_mapping={'cloud_map_options': 'cloudMapOptions', 'cluster': 'cluster', 'desired_count': 'desiredCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'load_balancers': 'loadBalancers', 'propagate_tags': 'propagateTags', 'service_name': 'serviceName', 'target_groups': 'targetGroups', 'task_image_options': 'taskImageOptions', 'vpc': 'vpc', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB', 'memory_reservation_mib': 'memoryReservationMiB', 'task_definition': 'taskDefinition'})
class ApplicationMultipleTargetGroupsEc2ServiceProps(ApplicationMultipleTargetGroupsServiceBaseProps):
    def __init__(self, *, cloud_map_options: typing.Optional[_CloudMapOptions_25ce57e4]=None, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, load_balancers: typing.Optional[typing.List["ApplicationLoadBalancerProps"]]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, service_name: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["ApplicationTargetProps"]]=None, task_image_options: typing.Optional["ApplicationLoadBalancedTaskImageProps"]=None, vpc: typing.Optional[_IVpc_3795853f]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, task_definition: typing.Optional[_Ec2TaskDefinition_96cf505d]=None) -> None:
        """The properties for the ApplicationMultipleTargetGroupsEc2Service service.

        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The application load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify ALB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param cpu: The minimum number of CPU units to reserve for the container. Valid values, which determines your range of valid values for the memory parameter: Default: - No minimum CPU units reserved.
        :param memory_limit_mib: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Note that this setting will be ignored if TaskImagesOptions is specified Default: - No memory reserved.
        :param task_definition: The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified. [disable-awslint:ref-via-interface] Default: - none

        stability
        :stability: experimental
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = _CloudMapOptions_25ce57e4(**cloud_map_options)
        if isinstance(task_image_options, dict): task_image_options = ApplicationLoadBalancedTaskImageProps(**task_image_options)
        self._values = {
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None: self._values["cluster"] = cluster
        if desired_count is not None: self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if load_balancers is not None: self._values["load_balancers"] = load_balancers
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if service_name is not None: self._values["service_name"] = service_name
        if target_groups is not None: self._values["target_groups"] = target_groups
        if task_image_options is not None: self._values["task_image_options"] = task_image_options
        if vpc is not None: self._values["vpc"] = vpc
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None: self._values["memory_reservation_mib"] = memory_reservation_mib
        if task_definition is not None: self._values["task_definition"] = task_definition

    @builtins.property
    def cloud_map_options(self) -> typing.Optional[_CloudMapOptions_25ce57e4]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.

        stability
        :stability: experimental
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def cluster(self) -> typing.Optional[_ICluster_5cbcc408]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_count')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[_Duration_5170c158]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set

        stability
        :stability: experimental
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def load_balancers(self) -> typing.Optional[typing.List["ApplicationLoadBalancerProps"]]:
        """The application load balancer that will serve traffic to the service.

        default
        :default: - a new load balancer with a listener will be created.

        stability
        :stability: experimental
        """
        return self._values.get('load_balancers')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[_PropagatedTagSource_e36ef3c2]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.

        stability
        :stability: experimental
        """
        return self._values.get('service_name')

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List["ApplicationTargetProps"]]:
        """Properties to specify ALB target groups.

        default
        :default: - default portMapping registered as target group and attached to the first defined listener

        stability
        :stability: experimental
        """
        return self._values.get('target_groups')

    @builtins.property
    def task_image_options(self) -> typing.Optional["ApplicationLoadBalancedTaskImageProps"]:
        """The properties required to create a new task definition.

        Only one of TaskDefinition or TaskImageOptions must be specified.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('task_image_options')

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The minimum number of CPU units to reserve for the container.

        Valid values, which determines your range of valid values for the memory parameter:

        default
        :default: - No minimum CPU units reserved.

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        default
        :default: - No memory limit.

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        """The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under heavy contention, Docker attempts to keep the
        container memory to this soft limit. However, your container can consume more
        memory when it needs to, up to either the hard limit specified with the memory
        parameter (if applicable), or all of the available memory on the container
        instance, whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        Note that this setting will be ignored if TaskImagesOptions is specified

        default
        :default: - No memory reserved.

        stability
        :stability: experimental
        """
        return self._values.get('memory_reservation_mib')

    @builtins.property
    def task_definition(self) -> typing.Optional[_Ec2TaskDefinition_96cf505d]:
        """The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified.

        [disable-awslint:ref-via-interface]

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('task_definition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationMultipleTargetGroupsEc2ServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ApplicationMultipleTargetGroupsFargateService(ApplicationMultipleTargetGroupsServiceBase, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs_patterns.ApplicationMultipleTargetGroupsFargateService"):
    """A Fargate service running on an ECS cluster fronted by an application load balancer.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, assign_public_ip: typing.Optional[bool]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, platform_version: typing.Optional[_FargatePlatformVersion_187ad0f4]=None, task_definition: typing.Optional[_FargateTaskDefinition_c5f42010]=None, cloud_map_options: typing.Optional[_CloudMapOptions_25ce57e4]=None, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, load_balancers: typing.Optional[typing.List["ApplicationLoadBalancerProps"]]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, service_name: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["ApplicationTargetProps"]]=None, task_image_options: typing.Optional["ApplicationLoadBalancedTaskImageProps"]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """Constructs a new instance of the ApplicationMultipleTargetGroupsFargateService class.

        :param scope: -
        :param id: -
        :param assign_public_ip: Determines whether the service will be assigned a public IP address. Default: false
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param task_definition: The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified. [disable-awslint:ref-via-interface] Default: - none
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The application load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify ALB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        props = ApplicationMultipleTargetGroupsFargateServiceProps(assign_public_ip=assign_public_ip, cpu=cpu, memory_limit_mib=memory_limit_mib, platform_version=platform_version, task_definition=task_definition, cloud_map_options=cloud_map_options, cluster=cluster, desired_count=desired_count, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, load_balancers=load_balancers, propagate_tags=propagate_tags, service_name=service_name, target_groups=target_groups, task_image_options=task_image_options, vpc=vpc)

        jsii.create(ApplicationMultipleTargetGroupsFargateService, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="assignPublicIp")
    def assign_public_ip(self) -> bool:
        """Determines whether the service will be assigned a public IP address.

        stability
        :stability: experimental
        """
        return jsii.get(self, "assignPublicIp")

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> _FargateService_e4491ea2:
        """The Fargate service in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "service")

    @builtins.property
    @jsii.member(jsii_name="targetGroup")
    def target_group(self) -> _ApplicationTargetGroup_7d0a8d54:
        """The default target group for the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "targetGroup")

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _FargateTaskDefinition_c5f42010:
        """The Fargate task definition in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "taskDefinition")


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.ApplicationMultipleTargetGroupsFargateServiceProps", jsii_struct_bases=[ApplicationMultipleTargetGroupsServiceBaseProps], name_mapping={'cloud_map_options': 'cloudMapOptions', 'cluster': 'cluster', 'desired_count': 'desiredCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'load_balancers': 'loadBalancers', 'propagate_tags': 'propagateTags', 'service_name': 'serviceName', 'target_groups': 'targetGroups', 'task_image_options': 'taskImageOptions', 'vpc': 'vpc', 'assign_public_ip': 'assignPublicIp', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB', 'platform_version': 'platformVersion', 'task_definition': 'taskDefinition'})
class ApplicationMultipleTargetGroupsFargateServiceProps(ApplicationMultipleTargetGroupsServiceBaseProps):
    def __init__(self, *, cloud_map_options: typing.Optional[_CloudMapOptions_25ce57e4]=None, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, load_balancers: typing.Optional[typing.List["ApplicationLoadBalancerProps"]]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, service_name: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["ApplicationTargetProps"]]=None, task_image_options: typing.Optional["ApplicationLoadBalancedTaskImageProps"]=None, vpc: typing.Optional[_IVpc_3795853f]=None, assign_public_ip: typing.Optional[bool]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, platform_version: typing.Optional[_FargatePlatformVersion_187ad0f4]=None, task_definition: typing.Optional[_FargateTaskDefinition_c5f42010]=None) -> None:
        """The properties for the ApplicationMultipleTargetGroupsFargateService service.

        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The application load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify ALB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param assign_public_ip: Determines whether the service will be assigned a public IP address. Default: false
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param task_definition: The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified. [disable-awslint:ref-via-interface] Default: - none

        stability
        :stability: experimental
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = _CloudMapOptions_25ce57e4(**cloud_map_options)
        if isinstance(task_image_options, dict): task_image_options = ApplicationLoadBalancedTaskImageProps(**task_image_options)
        self._values = {
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None: self._values["cluster"] = cluster
        if desired_count is not None: self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if load_balancers is not None: self._values["load_balancers"] = load_balancers
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if service_name is not None: self._values["service_name"] = service_name
        if target_groups is not None: self._values["target_groups"] = target_groups
        if task_image_options is not None: self._values["task_image_options"] = task_image_options
        if vpc is not None: self._values["vpc"] = vpc
        if assign_public_ip is not None: self._values["assign_public_ip"] = assign_public_ip
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if platform_version is not None: self._values["platform_version"] = platform_version
        if task_definition is not None: self._values["task_definition"] = task_definition

    @builtins.property
    def cloud_map_options(self) -> typing.Optional[_CloudMapOptions_25ce57e4]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.

        stability
        :stability: experimental
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def cluster(self) -> typing.Optional[_ICluster_5cbcc408]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_count')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[_Duration_5170c158]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set

        stability
        :stability: experimental
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def load_balancers(self) -> typing.Optional[typing.List["ApplicationLoadBalancerProps"]]:
        """The application load balancer that will serve traffic to the service.

        default
        :default: - a new load balancer with a listener will be created.

        stability
        :stability: experimental
        """
        return self._values.get('load_balancers')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[_PropagatedTagSource_e36ef3c2]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.

        stability
        :stability: experimental
        """
        return self._values.get('service_name')

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List["ApplicationTargetProps"]]:
        """Properties to specify ALB target groups.

        default
        :default: - default portMapping registered as target group and attached to the first defined listener

        stability
        :stability: experimental
        """
        return self._values.get('target_groups')

    @builtins.property
    def task_image_options(self) -> typing.Optional["ApplicationLoadBalancedTaskImageProps"]:
        """The properties required to create a new task definition.

        Only one of TaskDefinition or TaskImageOptions must be specified.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('task_image_options')

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[bool]:
        """Determines whether the service will be assigned a public IP address.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('assign_public_ip')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 256

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory used by the task.

        This field is required and you must use one of the following values, which determines your range of valid values
        for the cpu parameter:

        512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU)

        1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU)

        2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU)

        Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU)

        Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU)

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 512

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def platform_version(self) -> typing.Optional[_FargatePlatformVersion_187ad0f4]:
        """The platform version on which to run your service.

        If one is not specified, the LATEST platform version is used by default. For more information, see
        `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_
        in the Amazon Elastic Container Service Developer Guide.

        default
        :default: Latest

        stability
        :stability: experimental
        """
        return self._values.get('platform_version')

    @builtins.property
    def task_definition(self) -> typing.Optional[_FargateTaskDefinition_c5f42010]:
        """The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified.

        [disable-awslint:ref-via-interface]

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('task_definition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationMultipleTargetGroupsFargateServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class NetworkLoadBalancedEc2Service(NetworkLoadBalancedServiceBase, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs_patterns.NetworkLoadBalancedEc2Service"):
    """An EC2 service running on an ECS cluster fronted by a network load balancer.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, task_definition: typing.Optional[_Ec2TaskDefinition_96cf505d]=None, cloud_map_options: typing.Optional[_CloudMapOptions_25ce57e4]=None, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[_IHostedZone_59ffab76]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, listener_port: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[_INetworkLoadBalancer_8db68b99]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, public_load_balancer: typing.Optional[bool]=None, service_name: typing.Optional[str]=None, task_image_options: typing.Optional["NetworkLoadBalancedTaskImageOptions"]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """Constructs a new instance of the NetworkLoadBalancedEc2Service class.

        :param scope: -
        :param id: -
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: none
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory reserved.
        :param task_definition: The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both.. [disable-awslint:ref-via-interface] Default: - none
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the network load balancer that will serve traffic to the service. Default: 80
        :param load_balancer: The network load balancer that will serve traffic to the service. If the load balancer has been imported, the vpc attribute must be specified in the call to fromNetworkLoadBalancerAttributes(). [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. One of taskImageOptions or taskDefinition must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        props = NetworkLoadBalancedEc2ServiceProps(cpu=cpu, memory_limit_mib=memory_limit_mib, memory_reservation_mib=memory_reservation_mib, task_definition=task_definition, cloud_map_options=cloud_map_options, cluster=cluster, desired_count=desired_count, domain_name=domain_name, domain_zone=domain_zone, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, listener_port=listener_port, load_balancer=load_balancer, max_healthy_percent=max_healthy_percent, min_healthy_percent=min_healthy_percent, propagate_tags=propagate_tags, public_load_balancer=public_load_balancer, service_name=service_name, task_image_options=task_image_options, vpc=vpc)

        jsii.create(NetworkLoadBalancedEc2Service, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> _Ec2Service_c4ac147a:
        """The ECS service in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "service")

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _Ec2TaskDefinition_96cf505d:
        """The EC2 Task Definition in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "taskDefinition")


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.NetworkLoadBalancedEc2ServiceProps", jsii_struct_bases=[NetworkLoadBalancedServiceBaseProps], name_mapping={'cloud_map_options': 'cloudMapOptions', 'cluster': 'cluster', 'desired_count': 'desiredCount', 'domain_name': 'domainName', 'domain_zone': 'domainZone', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'listener_port': 'listenerPort', 'load_balancer': 'loadBalancer', 'max_healthy_percent': 'maxHealthyPercent', 'min_healthy_percent': 'minHealthyPercent', 'propagate_tags': 'propagateTags', 'public_load_balancer': 'publicLoadBalancer', 'service_name': 'serviceName', 'task_image_options': 'taskImageOptions', 'vpc': 'vpc', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB', 'memory_reservation_mib': 'memoryReservationMiB', 'task_definition': 'taskDefinition'})
class NetworkLoadBalancedEc2ServiceProps(NetworkLoadBalancedServiceBaseProps):
    def __init__(self, *, cloud_map_options: typing.Optional[_CloudMapOptions_25ce57e4]=None, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[_IHostedZone_59ffab76]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, listener_port: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[_INetworkLoadBalancer_8db68b99]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, public_load_balancer: typing.Optional[bool]=None, service_name: typing.Optional[str]=None, task_image_options: typing.Optional["NetworkLoadBalancedTaskImageOptions"]=None, vpc: typing.Optional[_IVpc_3795853f]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, task_definition: typing.Optional[_Ec2TaskDefinition_96cf505d]=None) -> None:
        """The properties for the NetworkLoadBalancedEc2Service service.

        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the network load balancer that will serve traffic to the service. Default: 80
        :param load_balancer: The network load balancer that will serve traffic to the service. If the load balancer has been imported, the vpc attribute must be specified in the call to fromNetworkLoadBalancerAttributes(). [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. One of taskImageOptions or taskDefinition must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: none
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory reserved.
        :param task_definition: The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both.. [disable-awslint:ref-via-interface] Default: - none

        stability
        :stability: experimental
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = _CloudMapOptions_25ce57e4(**cloud_map_options)
        if isinstance(task_image_options, dict): task_image_options = NetworkLoadBalancedTaskImageOptions(**task_image_options)
        self._values = {
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None: self._values["cluster"] = cluster
        if desired_count is not None: self._values["desired_count"] = desired_count
        if domain_name is not None: self._values["domain_name"] = domain_name
        if domain_zone is not None: self._values["domain_zone"] = domain_zone
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if listener_port is not None: self._values["listener_port"] = listener_port
        if load_balancer is not None: self._values["load_balancer"] = load_balancer
        if max_healthy_percent is not None: self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None: self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if public_load_balancer is not None: self._values["public_load_balancer"] = public_load_balancer
        if service_name is not None: self._values["service_name"] = service_name
        if task_image_options is not None: self._values["task_image_options"] = task_image_options
        if vpc is not None: self._values["vpc"] = vpc
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None: self._values["memory_reservation_mib"] = memory_reservation_mib
        if task_definition is not None: self._values["task_definition"] = task_definition

    @builtins.property
    def cloud_map_options(self) -> typing.Optional[_CloudMapOptions_25ce57e4]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.

        stability
        :stability: experimental
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def cluster(self) -> typing.Optional[_ICluster_5cbcc408]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_count')

    @builtins.property
    def domain_name(self) -> typing.Optional[str]:
        """The domain name for the service, e.g. "api.example.com.".

        default
        :default: - No domain name.

        stability
        :stability: experimental
        """
        return self._values.get('domain_name')

    @builtins.property
    def domain_zone(self) -> typing.Optional[_IHostedZone_59ffab76]:
        """The Route53 hosted zone for the domain, e.g. "example.com.".

        default
        :default: - No Route53 hosted domain zone.

        stability
        :stability: experimental
        """
        return self._values.get('domain_zone')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[_Duration_5170c158]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set

        stability
        :stability: experimental
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        """Listener port of the network load balancer that will serve traffic to the service.

        default
        :default: 80

        stability
        :stability: experimental
        """
        return self._values.get('listener_port')

    @builtins.property
    def load_balancer(self) -> typing.Optional[_INetworkLoadBalancer_8db68b99]:
        """The network load balancer that will serve traffic to the service.

        If the load balancer has been imported, the vpc attribute must be specified
        in the call to fromNetworkLoadBalancerAttributes().

        [disable-awslint:ref-via-interface]

        default
        :default: - a new load balancer will be created.

        stability
        :stability: experimental
        """
        return self._values.get('load_balancer')

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        default
        :default: - 100 if daemon, otherwise 200

        stability
        :stability: experimental
        """
        return self._values.get('max_healthy_percent')

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        default
        :default: - 0 if daemon, otherwise 50

        stability
        :stability: experimental
        """
        return self._values.get('min_healthy_percent')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[_PropagatedTagSource_e36ef3c2]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def public_load_balancer(self) -> typing.Optional[bool]:
        """Determines whether the Load Balancer will be internet-facing.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('public_load_balancer')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.

        stability
        :stability: experimental
        """
        return self._values.get('service_name')

    @builtins.property
    def task_image_options(self) -> typing.Optional["NetworkLoadBalancedTaskImageOptions"]:
        """The properties required to create a new task definition.

        One of taskImageOptions or taskDefinition must be specified.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('task_image_options')

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The hard limit (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        default
        :default: - No memory limit.

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        """The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under contention, Docker attempts to keep the
        container memory within the limit. If the container requires more memory,
        it can consume up to the value specified by the Memory property or all of
        the available memory on the container instance—whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        default
        :default: - No memory reserved.

        stability
        :stability: experimental
        """
        return self._values.get('memory_reservation_mib')

    @builtins.property
    def task_definition(self) -> typing.Optional[_Ec2TaskDefinition_96cf505d]:
        """The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both..

        [disable-awslint:ref-via-interface]

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('task_definition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkLoadBalancedEc2ServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class NetworkLoadBalancedFargateService(NetworkLoadBalancedServiceBase, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs_patterns.NetworkLoadBalancedFargateService"):
    """A Fargate service running on an ECS cluster fronted by a network load balancer.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, assign_public_ip: typing.Optional[bool]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, platform_version: typing.Optional[_FargatePlatformVersion_187ad0f4]=None, task_definition: typing.Optional[_FargateTaskDefinition_c5f42010]=None, cloud_map_options: typing.Optional[_CloudMapOptions_25ce57e4]=None, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[_IHostedZone_59ffab76]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, listener_port: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[_INetworkLoadBalancer_8db68b99]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, public_load_balancer: typing.Optional[bool]=None, service_name: typing.Optional[str]=None, task_image_options: typing.Optional["NetworkLoadBalancedTaskImageOptions"]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """Constructs a new instance of the NetworkLoadBalancedFargateService class.

        :param scope: -
        :param id: -
        :param assign_public_ip: Determines whether the service will be assigned a public IP address. Default: false
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param task_definition: The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both. [disable-awslint:ref-via-interface] Default: - none
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the network load balancer that will serve traffic to the service. Default: 80
        :param load_balancer: The network load balancer that will serve traffic to the service. If the load balancer has been imported, the vpc attribute must be specified in the call to fromNetworkLoadBalancerAttributes(). [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. One of taskImageOptions or taskDefinition must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        props = NetworkLoadBalancedFargateServiceProps(assign_public_ip=assign_public_ip, cpu=cpu, memory_limit_mib=memory_limit_mib, platform_version=platform_version, task_definition=task_definition, cloud_map_options=cloud_map_options, cluster=cluster, desired_count=desired_count, domain_name=domain_name, domain_zone=domain_zone, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, listener_port=listener_port, load_balancer=load_balancer, max_healthy_percent=max_healthy_percent, min_healthy_percent=min_healthy_percent, propagate_tags=propagate_tags, public_load_balancer=public_load_balancer, service_name=service_name, task_image_options=task_image_options, vpc=vpc)

        jsii.create(NetworkLoadBalancedFargateService, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="assignPublicIp")
    def assign_public_ip(self) -> bool:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "assignPublicIp")

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> _FargateService_e4491ea2:
        """The Fargate service in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "service")

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _FargateTaskDefinition_c5f42010:
        """The Fargate task definition in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "taskDefinition")


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.NetworkLoadBalancedFargateServiceProps", jsii_struct_bases=[NetworkLoadBalancedServiceBaseProps], name_mapping={'cloud_map_options': 'cloudMapOptions', 'cluster': 'cluster', 'desired_count': 'desiredCount', 'domain_name': 'domainName', 'domain_zone': 'domainZone', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'listener_port': 'listenerPort', 'load_balancer': 'loadBalancer', 'max_healthy_percent': 'maxHealthyPercent', 'min_healthy_percent': 'minHealthyPercent', 'propagate_tags': 'propagateTags', 'public_load_balancer': 'publicLoadBalancer', 'service_name': 'serviceName', 'task_image_options': 'taskImageOptions', 'vpc': 'vpc', 'assign_public_ip': 'assignPublicIp', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB', 'platform_version': 'platformVersion', 'task_definition': 'taskDefinition'})
class NetworkLoadBalancedFargateServiceProps(NetworkLoadBalancedServiceBaseProps):
    def __init__(self, *, cloud_map_options: typing.Optional[_CloudMapOptions_25ce57e4]=None, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[_IHostedZone_59ffab76]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, listener_port: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[_INetworkLoadBalancer_8db68b99]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, public_load_balancer: typing.Optional[bool]=None, service_name: typing.Optional[str]=None, task_image_options: typing.Optional["NetworkLoadBalancedTaskImageOptions"]=None, vpc: typing.Optional[_IVpc_3795853f]=None, assign_public_ip: typing.Optional[bool]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, platform_version: typing.Optional[_FargatePlatformVersion_187ad0f4]=None, task_definition: typing.Optional[_FargateTaskDefinition_c5f42010]=None) -> None:
        """The properties for the NetworkLoadBalancedFargateService service.

        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the network load balancer that will serve traffic to the service. Default: 80
        :param load_balancer: The network load balancer that will serve traffic to the service. If the load balancer has been imported, the vpc attribute must be specified in the call to fromNetworkLoadBalancerAttributes(). [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. One of taskImageOptions or taskDefinition must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param assign_public_ip: Determines whether the service will be assigned a public IP address. Default: false
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param task_definition: The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both. [disable-awslint:ref-via-interface] Default: - none

        stability
        :stability: experimental
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = _CloudMapOptions_25ce57e4(**cloud_map_options)
        if isinstance(task_image_options, dict): task_image_options = NetworkLoadBalancedTaskImageOptions(**task_image_options)
        self._values = {
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None: self._values["cluster"] = cluster
        if desired_count is not None: self._values["desired_count"] = desired_count
        if domain_name is not None: self._values["domain_name"] = domain_name
        if domain_zone is not None: self._values["domain_zone"] = domain_zone
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if listener_port is not None: self._values["listener_port"] = listener_port
        if load_balancer is not None: self._values["load_balancer"] = load_balancer
        if max_healthy_percent is not None: self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None: self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if public_load_balancer is not None: self._values["public_load_balancer"] = public_load_balancer
        if service_name is not None: self._values["service_name"] = service_name
        if task_image_options is not None: self._values["task_image_options"] = task_image_options
        if vpc is not None: self._values["vpc"] = vpc
        if assign_public_ip is not None: self._values["assign_public_ip"] = assign_public_ip
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if platform_version is not None: self._values["platform_version"] = platform_version
        if task_definition is not None: self._values["task_definition"] = task_definition

    @builtins.property
    def cloud_map_options(self) -> typing.Optional[_CloudMapOptions_25ce57e4]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.

        stability
        :stability: experimental
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def cluster(self) -> typing.Optional[_ICluster_5cbcc408]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_count')

    @builtins.property
    def domain_name(self) -> typing.Optional[str]:
        """The domain name for the service, e.g. "api.example.com.".

        default
        :default: - No domain name.

        stability
        :stability: experimental
        """
        return self._values.get('domain_name')

    @builtins.property
    def domain_zone(self) -> typing.Optional[_IHostedZone_59ffab76]:
        """The Route53 hosted zone for the domain, e.g. "example.com.".

        default
        :default: - No Route53 hosted domain zone.

        stability
        :stability: experimental
        """
        return self._values.get('domain_zone')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[_Duration_5170c158]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set

        stability
        :stability: experimental
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        """Listener port of the network load balancer that will serve traffic to the service.

        default
        :default: 80

        stability
        :stability: experimental
        """
        return self._values.get('listener_port')

    @builtins.property
    def load_balancer(self) -> typing.Optional[_INetworkLoadBalancer_8db68b99]:
        """The network load balancer that will serve traffic to the service.

        If the load balancer has been imported, the vpc attribute must be specified
        in the call to fromNetworkLoadBalancerAttributes().

        [disable-awslint:ref-via-interface]

        default
        :default: - a new load balancer will be created.

        stability
        :stability: experimental
        """
        return self._values.get('load_balancer')

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        default
        :default: - 100 if daemon, otherwise 200

        stability
        :stability: experimental
        """
        return self._values.get('max_healthy_percent')

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        default
        :default: - 0 if daemon, otherwise 50

        stability
        :stability: experimental
        """
        return self._values.get('min_healthy_percent')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[_PropagatedTagSource_e36ef3c2]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def public_load_balancer(self) -> typing.Optional[bool]:
        """Determines whether the Load Balancer will be internet-facing.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('public_load_balancer')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.

        stability
        :stability: experimental
        """
        return self._values.get('service_name')

    @builtins.property
    def task_image_options(self) -> typing.Optional["NetworkLoadBalancedTaskImageOptions"]:
        """The properties required to create a new task definition.

        One of taskImageOptions or taskDefinition must be specified.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('task_image_options')

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[bool]:
        """Determines whether the service will be assigned a public IP address.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('assign_public_ip')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 256

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory used by the task.

        This field is required and you must use one of the following values, which determines your range of valid values
        for the cpu parameter:

        512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU)

        1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU)

        2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU)

        Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU)

        Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU)

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 512

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def platform_version(self) -> typing.Optional[_FargatePlatformVersion_187ad0f4]:
        """The platform version on which to run your service.

        If one is not specified, the LATEST platform version is used by default. For more information, see
        `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_
        in the Amazon Elastic Container Service Developer Guide.

        default
        :default: Latest

        stability
        :stability: experimental
        """
        return self._values.get('platform_version')

    @builtins.property
    def task_definition(self) -> typing.Optional[_FargateTaskDefinition_c5f42010]:
        """The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both.

        [disable-awslint:ref-via-interface]

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('task_definition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkLoadBalancedFargateServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class NetworkMultipleTargetGroupsEc2Service(NetworkMultipleTargetGroupsServiceBase, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs_patterns.NetworkMultipleTargetGroupsEc2Service"):
    """An EC2 service running on an ECS cluster fronted by a network load balancer.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, task_definition: typing.Optional[_Ec2TaskDefinition_96cf505d]=None, cloud_map_options: typing.Optional[_CloudMapOptions_25ce57e4]=None, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, load_balancers: typing.Optional[typing.List["NetworkLoadBalancerProps"]]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, service_name: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["NetworkTargetProps"]]=None, task_image_options: typing.Optional["NetworkLoadBalancedTaskImageProps"]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """Constructs a new instance of the NetworkMultipleTargetGroupsEc2Service class.

        :param scope: -
        :param id: -
        :param cpu: The minimum number of CPU units to reserve for the container. Valid values, which determines your range of valid values for the memory parameter: Default: - No minimum CPU units reserved.
        :param memory_limit_mib: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Note that this setting will be ignored if TaskImagesOptions is specified. Default: - No memory reserved.
        :param task_definition: The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified. [disable-awslint:ref-via-interface] Default: - none
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The network load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: Name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify NLB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        props = NetworkMultipleTargetGroupsEc2ServiceProps(cpu=cpu, memory_limit_mib=memory_limit_mib, memory_reservation_mib=memory_reservation_mib, task_definition=task_definition, cloud_map_options=cloud_map_options, cluster=cluster, desired_count=desired_count, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, load_balancers=load_balancers, propagate_tags=propagate_tags, service_name=service_name, target_groups=target_groups, task_image_options=task_image_options, vpc=vpc)

        jsii.create(NetworkMultipleTargetGroupsEc2Service, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> _Ec2Service_c4ac147a:
        """The EC2 service in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "service")

    @builtins.property
    @jsii.member(jsii_name="targetGroup")
    def target_group(self) -> _NetworkTargetGroup_4f773ed3:
        """The default target group for the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "targetGroup")

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _Ec2TaskDefinition_96cf505d:
        """The EC2 Task Definition in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "taskDefinition")


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.NetworkMultipleTargetGroupsEc2ServiceProps", jsii_struct_bases=[NetworkMultipleTargetGroupsServiceBaseProps], name_mapping={'cloud_map_options': 'cloudMapOptions', 'cluster': 'cluster', 'desired_count': 'desiredCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'load_balancers': 'loadBalancers', 'propagate_tags': 'propagateTags', 'service_name': 'serviceName', 'target_groups': 'targetGroups', 'task_image_options': 'taskImageOptions', 'vpc': 'vpc', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB', 'memory_reservation_mib': 'memoryReservationMiB', 'task_definition': 'taskDefinition'})
class NetworkMultipleTargetGroupsEc2ServiceProps(NetworkMultipleTargetGroupsServiceBaseProps):
    def __init__(self, *, cloud_map_options: typing.Optional[_CloudMapOptions_25ce57e4]=None, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, load_balancers: typing.Optional[typing.List["NetworkLoadBalancerProps"]]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, service_name: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["NetworkTargetProps"]]=None, task_image_options: typing.Optional["NetworkLoadBalancedTaskImageProps"]=None, vpc: typing.Optional[_IVpc_3795853f]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, task_definition: typing.Optional[_Ec2TaskDefinition_96cf505d]=None) -> None:
        """The properties for the NetworkMultipleTargetGroupsEc2Service service.

        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The network load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: Name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify NLB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param cpu: The minimum number of CPU units to reserve for the container. Valid values, which determines your range of valid values for the memory parameter: Default: - No minimum CPU units reserved.
        :param memory_limit_mib: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Note that this setting will be ignored if TaskImagesOptions is specified. Default: - No memory reserved.
        :param task_definition: The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified. [disable-awslint:ref-via-interface] Default: - none

        stability
        :stability: experimental
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = _CloudMapOptions_25ce57e4(**cloud_map_options)
        if isinstance(task_image_options, dict): task_image_options = NetworkLoadBalancedTaskImageProps(**task_image_options)
        self._values = {
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None: self._values["cluster"] = cluster
        if desired_count is not None: self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if load_balancers is not None: self._values["load_balancers"] = load_balancers
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if service_name is not None: self._values["service_name"] = service_name
        if target_groups is not None: self._values["target_groups"] = target_groups
        if task_image_options is not None: self._values["task_image_options"] = task_image_options
        if vpc is not None: self._values["vpc"] = vpc
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None: self._values["memory_reservation_mib"] = memory_reservation_mib
        if task_definition is not None: self._values["task_definition"] = task_definition

    @builtins.property
    def cloud_map_options(self) -> typing.Optional[_CloudMapOptions_25ce57e4]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.

        stability
        :stability: experimental
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def cluster(self) -> typing.Optional[_ICluster_5cbcc408]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_count')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[_Duration_5170c158]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set

        stability
        :stability: experimental
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def load_balancers(self) -> typing.Optional[typing.List["NetworkLoadBalancerProps"]]:
        """The network load balancer that will serve traffic to the service.

        default
        :default: - a new load balancer with a listener will be created.

        stability
        :stability: experimental
        """
        return self._values.get('load_balancers')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[_PropagatedTagSource_e36ef3c2]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """Name of the service.

        default
        :default: - CloudFormation-generated name.

        stability
        :stability: experimental
        """
        return self._values.get('service_name')

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List["NetworkTargetProps"]]:
        """Properties to specify NLB target groups.

        default
        :default: - default portMapping registered as target group and attached to the first defined listener

        stability
        :stability: experimental
        """
        return self._values.get('target_groups')

    @builtins.property
    def task_image_options(self) -> typing.Optional["NetworkLoadBalancedTaskImageProps"]:
        """The properties required to create a new task definition.

        Only one of TaskDefinition or TaskImageOptions must be specified.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('task_image_options')

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The minimum number of CPU units to reserve for the container.

        Valid values, which determines your range of valid values for the memory parameter:

        default
        :default: - No minimum CPU units reserved.

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        default
        :default: - No memory limit.

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        """The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under heavy contention, Docker attempts to keep the
        container memory to this soft limit. However, your container can consume more
        memory when it needs to, up to either the hard limit specified with the memory
        parameter (if applicable), or all of the available memory on the container
        instance, whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        Note that this setting will be ignored if TaskImagesOptions is specified.

        default
        :default: - No memory reserved.

        stability
        :stability: experimental
        """
        return self._values.get('memory_reservation_mib')

    @builtins.property
    def task_definition(self) -> typing.Optional[_Ec2TaskDefinition_96cf505d]:
        """The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified.

        [disable-awslint:ref-via-interface]

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('task_definition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkMultipleTargetGroupsEc2ServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class NetworkMultipleTargetGroupsFargateService(NetworkMultipleTargetGroupsServiceBase, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs_patterns.NetworkMultipleTargetGroupsFargateService"):
    """A Fargate service running on an ECS cluster fronted by a network load balancer.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, assign_public_ip: typing.Optional[bool]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, platform_version: typing.Optional[_FargatePlatformVersion_187ad0f4]=None, task_definition: typing.Optional[_FargateTaskDefinition_c5f42010]=None, cloud_map_options: typing.Optional[_CloudMapOptions_25ce57e4]=None, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, load_balancers: typing.Optional[typing.List["NetworkLoadBalancerProps"]]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, service_name: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["NetworkTargetProps"]]=None, task_image_options: typing.Optional["NetworkLoadBalancedTaskImageProps"]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """Constructs a new instance of the NetworkMultipleTargetGroupsFargateService class.

        :param scope: -
        :param id: -
        :param assign_public_ip: Determines whether the service will be assigned a public IP address. Default: false
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param task_definition: The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified. [disable-awslint:ref-via-interface] Default: - none
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The network load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: Name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify NLB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        props = NetworkMultipleTargetGroupsFargateServiceProps(assign_public_ip=assign_public_ip, cpu=cpu, memory_limit_mib=memory_limit_mib, platform_version=platform_version, task_definition=task_definition, cloud_map_options=cloud_map_options, cluster=cluster, desired_count=desired_count, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, load_balancers=load_balancers, propagate_tags=propagate_tags, service_name=service_name, target_groups=target_groups, task_image_options=task_image_options, vpc=vpc)

        jsii.create(NetworkMultipleTargetGroupsFargateService, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="assignPublicIp")
    def assign_public_ip(self) -> bool:
        """Determines whether the service will be assigned a public IP address.

        stability
        :stability: experimental
        """
        return jsii.get(self, "assignPublicIp")

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> _FargateService_e4491ea2:
        """The Fargate service in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "service")

    @builtins.property
    @jsii.member(jsii_name="targetGroup")
    def target_group(self) -> _NetworkTargetGroup_4f773ed3:
        """The default target group for the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "targetGroup")

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _FargateTaskDefinition_c5f42010:
        """The Fargate task definition in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "taskDefinition")


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.NetworkMultipleTargetGroupsFargateServiceProps", jsii_struct_bases=[NetworkMultipleTargetGroupsServiceBaseProps], name_mapping={'cloud_map_options': 'cloudMapOptions', 'cluster': 'cluster', 'desired_count': 'desiredCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'load_balancers': 'loadBalancers', 'propagate_tags': 'propagateTags', 'service_name': 'serviceName', 'target_groups': 'targetGroups', 'task_image_options': 'taskImageOptions', 'vpc': 'vpc', 'assign_public_ip': 'assignPublicIp', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB', 'platform_version': 'platformVersion', 'task_definition': 'taskDefinition'})
class NetworkMultipleTargetGroupsFargateServiceProps(NetworkMultipleTargetGroupsServiceBaseProps):
    def __init__(self, *, cloud_map_options: typing.Optional[_CloudMapOptions_25ce57e4]=None, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, load_balancers: typing.Optional[typing.List["NetworkLoadBalancerProps"]]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, service_name: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["NetworkTargetProps"]]=None, task_image_options: typing.Optional["NetworkLoadBalancedTaskImageProps"]=None, vpc: typing.Optional[_IVpc_3795853f]=None, assign_public_ip: typing.Optional[bool]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, platform_version: typing.Optional[_FargatePlatformVersion_187ad0f4]=None, task_definition: typing.Optional[_FargateTaskDefinition_c5f42010]=None) -> None:
        """The properties for the NetworkMultipleTargetGroupsFargateService service.

        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The network load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: Name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify NLB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param assign_public_ip: Determines whether the service will be assigned a public IP address. Default: false
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param task_definition: The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified. [disable-awslint:ref-via-interface] Default: - none

        stability
        :stability: experimental
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = _CloudMapOptions_25ce57e4(**cloud_map_options)
        if isinstance(task_image_options, dict): task_image_options = NetworkLoadBalancedTaskImageProps(**task_image_options)
        self._values = {
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None: self._values["cluster"] = cluster
        if desired_count is not None: self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if load_balancers is not None: self._values["load_balancers"] = load_balancers
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if service_name is not None: self._values["service_name"] = service_name
        if target_groups is not None: self._values["target_groups"] = target_groups
        if task_image_options is not None: self._values["task_image_options"] = task_image_options
        if vpc is not None: self._values["vpc"] = vpc
        if assign_public_ip is not None: self._values["assign_public_ip"] = assign_public_ip
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if platform_version is not None: self._values["platform_version"] = platform_version
        if task_definition is not None: self._values["task_definition"] = task_definition

    @builtins.property
    def cloud_map_options(self) -> typing.Optional[_CloudMapOptions_25ce57e4]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.

        stability
        :stability: experimental
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def cluster(self) -> typing.Optional[_ICluster_5cbcc408]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_count')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[_Duration_5170c158]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set

        stability
        :stability: experimental
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def load_balancers(self) -> typing.Optional[typing.List["NetworkLoadBalancerProps"]]:
        """The network load balancer that will serve traffic to the service.

        default
        :default: - a new load balancer with a listener will be created.

        stability
        :stability: experimental
        """
        return self._values.get('load_balancers')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[_PropagatedTagSource_e36ef3c2]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """Name of the service.

        default
        :default: - CloudFormation-generated name.

        stability
        :stability: experimental
        """
        return self._values.get('service_name')

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List["NetworkTargetProps"]]:
        """Properties to specify NLB target groups.

        default
        :default: - default portMapping registered as target group and attached to the first defined listener

        stability
        :stability: experimental
        """
        return self._values.get('target_groups')

    @builtins.property
    def task_image_options(self) -> typing.Optional["NetworkLoadBalancedTaskImageProps"]:
        """The properties required to create a new task definition.

        Only one of TaskDefinition or TaskImageOptions must be specified.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('task_image_options')

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[bool]:
        """Determines whether the service will be assigned a public IP address.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('assign_public_ip')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 256

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory used by the task.

        This field is required and you must use one of the following values, which determines your range of valid values
        for the cpu parameter:

        512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU)

        1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU)

        2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU)

        Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU)

        Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU)

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 512

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def platform_version(self) -> typing.Optional[_FargatePlatformVersion_187ad0f4]:
        """The platform version on which to run your service.

        If one is not specified, the LATEST platform version is used by default. For more information, see
        `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_
        in the Amazon Elastic Container Service Developer Guide.

        default
        :default: Latest

        stability
        :stability: experimental
        """
        return self._values.get('platform_version')

    @builtins.property
    def task_definition(self) -> typing.Optional[_FargateTaskDefinition_c5f42010]:
        """The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified.

        [disable-awslint:ref-via-interface]

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('task_definition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkMultipleTargetGroupsFargateServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class QueueProcessingEc2Service(QueueProcessingServiceBase, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs_patterns.QueueProcessingEc2Service"):
    """Class to create a queue processing EC2 service.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, image: _ContainerImage_99cc4b15, cluster: typing.Optional[_ICluster_5cbcc408]=None, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, family: typing.Optional[str]=None, log_driver: typing.Optional[_LogDriver_d09e7eb9]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, max_receive_count: typing.Optional[jsii.Number]=None, max_scaling_capacity: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, queue: typing.Optional[_IQueue_b743f559]=None, retention_period: typing.Optional[_Duration_5170c158]=None, scaling_steps: typing.Optional[typing.List[_ScalingInterval_fac05118]]=None, secrets: typing.Optional[typing.Mapping[str, _Secret_3f6909a4]]=None, service_name: typing.Optional[str]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """Constructs a new instance of the QueueProcessingEc2Service class.

        :param scope: -
        :param id: -
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: none
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
        :param image: The image used to start a container.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. The variable ``QUEUE_NAME`` with value ``queue.queueName`` will always be passed. Default: 'QUEUE_NAME: queue.queueName'
        :param family: The name of a family that the task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - default from underlying service.
        :param max_receive_count: The maximum number of times that a message can be received by consumers. When this value is exceeded for a message the message will be automatically sent to the Dead Letter Queue. Default: 3
        :param max_scaling_capacity: Maximum capacity to scale to. Default: (desiredTaskCount * 2)
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - default from underlying service.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_ Default: 'SQSQueue with CloudFormation-generated name'
        :param retention_period: The number of seconds that Dead Letter Queue retains a message. Default: Duration.days(14)
        :param scaling_steps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. See `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_ Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        props = QueueProcessingEc2ServiceProps(cpu=cpu, memory_limit_mib=memory_limit_mib, memory_reservation_mib=memory_reservation_mib, image=image, cluster=cluster, command=command, desired_task_count=desired_task_count, enable_ecs_managed_tags=enable_ecs_managed_tags, enable_logging=enable_logging, environment=environment, family=family, log_driver=log_driver, max_healthy_percent=max_healthy_percent, max_receive_count=max_receive_count, max_scaling_capacity=max_scaling_capacity, min_healthy_percent=min_healthy_percent, propagate_tags=propagate_tags, queue=queue, retention_period=retention_period, scaling_steps=scaling_steps, secrets=secrets, service_name=service_name, vpc=vpc)

        jsii.create(QueueProcessingEc2Service, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> _Ec2Service_c4ac147a:
        """The EC2 service in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "service")

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _Ec2TaskDefinition_96cf505d:
        """The EC2 task definition in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "taskDefinition")


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.QueueProcessingEc2ServiceProps", jsii_struct_bases=[QueueProcessingServiceBaseProps], name_mapping={'image': 'image', 'cluster': 'cluster', 'command': 'command', 'desired_task_count': 'desiredTaskCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'enable_logging': 'enableLogging', 'environment': 'environment', 'family': 'family', 'log_driver': 'logDriver', 'max_healthy_percent': 'maxHealthyPercent', 'max_receive_count': 'maxReceiveCount', 'max_scaling_capacity': 'maxScalingCapacity', 'min_healthy_percent': 'minHealthyPercent', 'propagate_tags': 'propagateTags', 'queue': 'queue', 'retention_period': 'retentionPeriod', 'scaling_steps': 'scalingSteps', 'secrets': 'secrets', 'service_name': 'serviceName', 'vpc': 'vpc', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB', 'memory_reservation_mib': 'memoryReservationMiB'})
class QueueProcessingEc2ServiceProps(QueueProcessingServiceBaseProps):
    def __init__(self, *, image: _ContainerImage_99cc4b15, cluster: typing.Optional[_ICluster_5cbcc408]=None, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, family: typing.Optional[str]=None, log_driver: typing.Optional[_LogDriver_d09e7eb9]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, max_receive_count: typing.Optional[jsii.Number]=None, max_scaling_capacity: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, queue: typing.Optional[_IQueue_b743f559]=None, retention_period: typing.Optional[_Duration_5170c158]=None, scaling_steps: typing.Optional[typing.List[_ScalingInterval_fac05118]]=None, secrets: typing.Optional[typing.Mapping[str, _Secret_3f6909a4]]=None, service_name: typing.Optional[str]=None, vpc: typing.Optional[_IVpc_3795853f]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None) -> None:
        """The properties for the QueueProcessingEc2Service service.

        :param image: The image used to start a container.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. The variable ``QUEUE_NAME`` with value ``queue.queueName`` will always be passed. Default: 'QUEUE_NAME: queue.queueName'
        :param family: The name of a family that the task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - default from underlying service.
        :param max_receive_count: The maximum number of times that a message can be received by consumers. When this value is exceeded for a message the message will be automatically sent to the Dead Letter Queue. Default: 3
        :param max_scaling_capacity: Maximum capacity to scale to. Default: (desiredTaskCount * 2)
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - default from underlying service.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_ Default: 'SQSQueue with CloudFormation-generated name'
        :param retention_period: The number of seconds that Dead Letter Queue retains a message. Default: Duration.days(14)
        :param scaling_steps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. See `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_ Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: none
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.

        stability
        :stability: experimental
        """
        self._values = {
            'image': image,
        }
        if cluster is not None: self._values["cluster"] = cluster
        if command is not None: self._values["command"] = command
        if desired_task_count is not None: self._values["desired_task_count"] = desired_task_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if enable_logging is not None: self._values["enable_logging"] = enable_logging
        if environment is not None: self._values["environment"] = environment
        if family is not None: self._values["family"] = family
        if log_driver is not None: self._values["log_driver"] = log_driver
        if max_healthy_percent is not None: self._values["max_healthy_percent"] = max_healthy_percent
        if max_receive_count is not None: self._values["max_receive_count"] = max_receive_count
        if max_scaling_capacity is not None: self._values["max_scaling_capacity"] = max_scaling_capacity
        if min_healthy_percent is not None: self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if queue is not None: self._values["queue"] = queue
        if retention_period is not None: self._values["retention_period"] = retention_period
        if scaling_steps is not None: self._values["scaling_steps"] = scaling_steps
        if secrets is not None: self._values["secrets"] = secrets
        if service_name is not None: self._values["service_name"] = service_name
        if vpc is not None: self._values["vpc"] = vpc
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None: self._values["memory_reservation_mib"] = memory_reservation_mib

    @builtins.property
    def image(self) -> _ContainerImage_99cc4b15:
        """The image used to start a container.

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @builtins.property
    def cluster(self) -> typing.Optional[_ICluster_5cbcc408]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        default
        :default: - CMD value built into container image.

        stability
        :stability: experimental
        """
        return self._values.get('command')

    @builtins.property
    def desired_task_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_task_count')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def enable_logging(self) -> typing.Optional[bool]:
        """Flag to indicate whether to enable logging.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('enable_logging')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The environment variables to pass to the container.

        The variable ``QUEUE_NAME`` with value ``queue.queueName`` will
        always be passed.

        default
        :default: 'QUEUE_NAME: queue.queueName'

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def family(self) -> typing.Optional[str]:
        """The name of a family that the task definition is registered to.

        A family groups multiple versions of a task definition.

        default
        :default: - Automatically generated name.

        stability
        :stability: experimental
        """
        return self._values.get('family')

    @builtins.property
    def log_driver(self) -> typing.Optional[_LogDriver_d09e7eb9]:
        """The log driver to use.

        default
        :default: - AwsLogDriver if enableLogging is true

        stability
        :stability: experimental
        """
        return self._values.get('log_driver')

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        default
        :default: - default from underlying service.

        stability
        :stability: experimental
        """
        return self._values.get('max_healthy_percent')

    @builtins.property
    def max_receive_count(self) -> typing.Optional[jsii.Number]:
        """The maximum number of times that a message can be received by consumers.

        When this value is exceeded for a message the message will be automatically sent to the Dead Letter Queue.

        default
        :default: 3

        stability
        :stability: experimental
        """
        return self._values.get('max_receive_count')

    @builtins.property
    def max_scaling_capacity(self) -> typing.Optional[jsii.Number]:
        """Maximum capacity to scale to.

        default
        :default: (desiredTaskCount * 2)

        stability
        :stability: experimental
        """
        return self._values.get('max_scaling_capacity')

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        default
        :default: - default from underlying service.

        stability
        :stability: experimental
        """
        return self._values.get('min_healthy_percent')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[_PropagatedTagSource_e36ef3c2]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def queue(self) -> typing.Optional[_IQueue_b743f559]:
        """A queue for which to process items from.

        If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See
        `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_

        default
        :default: 'SQSQueue with CloudFormation-generated name'

        stability
        :stability: experimental
        """
        return self._values.get('queue')

    @builtins.property
    def retention_period(self) -> typing.Optional[_Duration_5170c158]:
        """The number of seconds that Dead Letter Queue retains a message.

        default
        :default: Duration.days(14)

        stability
        :stability: experimental
        """
        return self._values.get('retention_period')

    @builtins.property
    def scaling_steps(self) -> typing.Optional[typing.List[_ScalingInterval_fac05118]]:
        """The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric.

        Maps a range of metric values to a particular scaling behavior. See
        `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_

        default
        :default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]

        stability
        :stability: experimental
        """
        return self._values.get('scaling_steps')

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[str, _Secret_3f6909a4]]:
        """The secret to expose to the container as an environment variable.

        default
        :default: - No secret environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('secrets')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.

        stability
        :stability: experimental
        """
        return self._values.get('service_name')

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The hard limit (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: - No memory limit.

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        """The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under contention, Docker attempts to keep the
        container memory within the limit. If the container requires more memory,
        it can consume up to the value specified by the Memory property or all of
        the available memory on the container instance—whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: - No memory reserved.

        stability
        :stability: experimental
        """
        return self._values.get('memory_reservation_mib')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'QueueProcessingEc2ServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class QueueProcessingFargateService(QueueProcessingServiceBase, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs_patterns.QueueProcessingFargateService"):
    """Class to create a queue processing Fargate service.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, platform_version: typing.Optional[_FargatePlatformVersion_187ad0f4]=None, image: _ContainerImage_99cc4b15, cluster: typing.Optional[_ICluster_5cbcc408]=None, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, family: typing.Optional[str]=None, log_driver: typing.Optional[_LogDriver_d09e7eb9]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, max_receive_count: typing.Optional[jsii.Number]=None, max_scaling_capacity: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, queue: typing.Optional[_IQueue_b743f559]=None, retention_period: typing.Optional[_Duration_5170c158]=None, scaling_steps: typing.Optional[typing.List[_ScalingInterval_fac05118]]=None, secrets: typing.Optional[typing.Mapping[str, _Secret_3f6909a4]]=None, service_name: typing.Optional[str]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """Constructs a new instance of the QueueProcessingFargateService class.

        :param scope: -
        :param id: -
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 0.5GB, 1GB, 2GB - Available cpu values: 256 (.25 vCPU) 1GB, 2GB, 3GB, 4GB - Available cpu values: 512 (.5 vCPU) 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB - Available cpu values: 1024 (1 vCPU) Between 4GB and 16GB in 1GB increments - Available cpu values: 2048 (2 vCPU) Between 8GB and 30GB in 1GB increments - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param image: The image used to start a container.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. The variable ``QUEUE_NAME`` with value ``queue.queueName`` will always be passed. Default: 'QUEUE_NAME: queue.queueName'
        :param family: The name of a family that the task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - default from underlying service.
        :param max_receive_count: The maximum number of times that a message can be received by consumers. When this value is exceeded for a message the message will be automatically sent to the Dead Letter Queue. Default: 3
        :param max_scaling_capacity: Maximum capacity to scale to. Default: (desiredTaskCount * 2)
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - default from underlying service.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_ Default: 'SQSQueue with CloudFormation-generated name'
        :param retention_period: The number of seconds that Dead Letter Queue retains a message. Default: Duration.days(14)
        :param scaling_steps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. See `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_ Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        props = QueueProcessingFargateServiceProps(cpu=cpu, memory_limit_mib=memory_limit_mib, platform_version=platform_version, image=image, cluster=cluster, command=command, desired_task_count=desired_task_count, enable_ecs_managed_tags=enable_ecs_managed_tags, enable_logging=enable_logging, environment=environment, family=family, log_driver=log_driver, max_healthy_percent=max_healthy_percent, max_receive_count=max_receive_count, max_scaling_capacity=max_scaling_capacity, min_healthy_percent=min_healthy_percent, propagate_tags=propagate_tags, queue=queue, retention_period=retention_period, scaling_steps=scaling_steps, secrets=secrets, service_name=service_name, vpc=vpc)

        jsii.create(QueueProcessingFargateService, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> _FargateService_e4491ea2:
        """The Fargate service in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "service")

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _FargateTaskDefinition_c5f42010:
        """The Fargate task definition in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "taskDefinition")


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.QueueProcessingFargateServiceProps", jsii_struct_bases=[QueueProcessingServiceBaseProps], name_mapping={'image': 'image', 'cluster': 'cluster', 'command': 'command', 'desired_task_count': 'desiredTaskCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'enable_logging': 'enableLogging', 'environment': 'environment', 'family': 'family', 'log_driver': 'logDriver', 'max_healthy_percent': 'maxHealthyPercent', 'max_receive_count': 'maxReceiveCount', 'max_scaling_capacity': 'maxScalingCapacity', 'min_healthy_percent': 'minHealthyPercent', 'propagate_tags': 'propagateTags', 'queue': 'queue', 'retention_period': 'retentionPeriod', 'scaling_steps': 'scalingSteps', 'secrets': 'secrets', 'service_name': 'serviceName', 'vpc': 'vpc', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB', 'platform_version': 'platformVersion'})
class QueueProcessingFargateServiceProps(QueueProcessingServiceBaseProps):
    def __init__(self, *, image: _ContainerImage_99cc4b15, cluster: typing.Optional[_ICluster_5cbcc408]=None, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, family: typing.Optional[str]=None, log_driver: typing.Optional[_LogDriver_d09e7eb9]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, max_receive_count: typing.Optional[jsii.Number]=None, max_scaling_capacity: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[_PropagatedTagSource_e36ef3c2]=None, queue: typing.Optional[_IQueue_b743f559]=None, retention_period: typing.Optional[_Duration_5170c158]=None, scaling_steps: typing.Optional[typing.List[_ScalingInterval_fac05118]]=None, secrets: typing.Optional[typing.Mapping[str, _Secret_3f6909a4]]=None, service_name: typing.Optional[str]=None, vpc: typing.Optional[_IVpc_3795853f]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, platform_version: typing.Optional[_FargatePlatformVersion_187ad0f4]=None) -> None:
        """The properties for the QueueProcessingFargateService service.

        :param image: The image used to start a container.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. The variable ``QUEUE_NAME`` with value ``queue.queueName`` will always be passed. Default: 'QUEUE_NAME: queue.queueName'
        :param family: The name of a family that the task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - default from underlying service.
        :param max_receive_count: The maximum number of times that a message can be received by consumers. When this value is exceeded for a message the message will be automatically sent to the Dead Letter Queue. Default: 3
        :param max_scaling_capacity: Maximum capacity to scale to. Default: (desiredTaskCount * 2)
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - default from underlying service.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_ Default: 'SQSQueue with CloudFormation-generated name'
        :param retention_period: The number of seconds that Dead Letter Queue retains a message. Default: Duration.days(14)
        :param scaling_steps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. See `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_ Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 0.5GB, 1GB, 2GB - Available cpu values: 256 (.25 vCPU) 1GB, 2GB, 3GB, 4GB - Available cpu values: 512 (.5 vCPU) 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB - Available cpu values: 1024 (1 vCPU) Between 4GB and 16GB in 1GB increments - Available cpu values: 2048 (2 vCPU) Between 8GB and 30GB in 1GB increments - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest

        stability
        :stability: experimental
        """
        self._values = {
            'image': image,
        }
        if cluster is not None: self._values["cluster"] = cluster
        if command is not None: self._values["command"] = command
        if desired_task_count is not None: self._values["desired_task_count"] = desired_task_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if enable_logging is not None: self._values["enable_logging"] = enable_logging
        if environment is not None: self._values["environment"] = environment
        if family is not None: self._values["family"] = family
        if log_driver is not None: self._values["log_driver"] = log_driver
        if max_healthy_percent is not None: self._values["max_healthy_percent"] = max_healthy_percent
        if max_receive_count is not None: self._values["max_receive_count"] = max_receive_count
        if max_scaling_capacity is not None: self._values["max_scaling_capacity"] = max_scaling_capacity
        if min_healthy_percent is not None: self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if queue is not None: self._values["queue"] = queue
        if retention_period is not None: self._values["retention_period"] = retention_period
        if scaling_steps is not None: self._values["scaling_steps"] = scaling_steps
        if secrets is not None: self._values["secrets"] = secrets
        if service_name is not None: self._values["service_name"] = service_name
        if vpc is not None: self._values["vpc"] = vpc
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if platform_version is not None: self._values["platform_version"] = platform_version

    @builtins.property
    def image(self) -> _ContainerImage_99cc4b15:
        """The image used to start a container.

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @builtins.property
    def cluster(self) -> typing.Optional[_ICluster_5cbcc408]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        default
        :default: - CMD value built into container image.

        stability
        :stability: experimental
        """
        return self._values.get('command')

    @builtins.property
    def desired_task_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_task_count')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def enable_logging(self) -> typing.Optional[bool]:
        """Flag to indicate whether to enable logging.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('enable_logging')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The environment variables to pass to the container.

        The variable ``QUEUE_NAME`` with value ``queue.queueName`` will
        always be passed.

        default
        :default: 'QUEUE_NAME: queue.queueName'

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def family(self) -> typing.Optional[str]:
        """The name of a family that the task definition is registered to.

        A family groups multiple versions of a task definition.

        default
        :default: - Automatically generated name.

        stability
        :stability: experimental
        """
        return self._values.get('family')

    @builtins.property
    def log_driver(self) -> typing.Optional[_LogDriver_d09e7eb9]:
        """The log driver to use.

        default
        :default: - AwsLogDriver if enableLogging is true

        stability
        :stability: experimental
        """
        return self._values.get('log_driver')

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        default
        :default: - default from underlying service.

        stability
        :stability: experimental
        """
        return self._values.get('max_healthy_percent')

    @builtins.property
    def max_receive_count(self) -> typing.Optional[jsii.Number]:
        """The maximum number of times that a message can be received by consumers.

        When this value is exceeded for a message the message will be automatically sent to the Dead Letter Queue.

        default
        :default: 3

        stability
        :stability: experimental
        """
        return self._values.get('max_receive_count')

    @builtins.property
    def max_scaling_capacity(self) -> typing.Optional[jsii.Number]:
        """Maximum capacity to scale to.

        default
        :default: (desiredTaskCount * 2)

        stability
        :stability: experimental
        """
        return self._values.get('max_scaling_capacity')

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        default
        :default: - default from underlying service.

        stability
        :stability: experimental
        """
        return self._values.get('min_healthy_percent')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[_PropagatedTagSource_e36ef3c2]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def queue(self) -> typing.Optional[_IQueue_b743f559]:
        """A queue for which to process items from.

        If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See
        `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_

        default
        :default: 'SQSQueue with CloudFormation-generated name'

        stability
        :stability: experimental
        """
        return self._values.get('queue')

    @builtins.property
    def retention_period(self) -> typing.Optional[_Duration_5170c158]:
        """The number of seconds that Dead Letter Queue retains a message.

        default
        :default: Duration.days(14)

        stability
        :stability: experimental
        """
        return self._values.get('retention_period')

    @builtins.property
    def scaling_steps(self) -> typing.Optional[typing.List[_ScalingInterval_fac05118]]:
        """The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric.

        Maps a range of metric values to a particular scaling behavior. See
        `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_

        default
        :default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]

        stability
        :stability: experimental
        """
        return self._values.get('scaling_steps')

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[str, _Secret_3f6909a4]]:
        """The secret to expose to the container as an environment variable.

        default
        :default: - No secret environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('secrets')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.

        stability
        :stability: experimental
        """
        return self._values.get('service_name')

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 256

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory used by the task.

        This field is required and you must use one of the following values, which determines your range of valid values
        for the cpu parameter:

        0.5GB, 1GB, 2GB - Available cpu values: 256 (.25 vCPU)

        1GB, 2GB, 3GB, 4GB - Available cpu values: 512 (.5 vCPU)

        2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB - Available cpu values: 1024 (1 vCPU)

        Between 4GB and 16GB in 1GB increments - Available cpu values: 2048 (2 vCPU)

        Between 8GB and 30GB in 1GB increments - Available cpu values: 4096 (4 vCPU)

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 512

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def platform_version(self) -> typing.Optional[_FargatePlatformVersion_187ad0f4]:
        """The platform version on which to run your service.

        If one is not specified, the LATEST platform version is used by default. For more information, see
        `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_
        in the Amazon Elastic Container Service Developer Guide.

        default
        :default: Latest

        stability
        :stability: experimental
        """
        return self._values.get('platform_version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'QueueProcessingFargateServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ScheduledEc2Task(ScheduledTaskBase, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs_patterns.ScheduledEc2Task"):
    """A scheduled EC2 task that will be initiated off of CloudWatch Events.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, scheduled_ec2_task_definition_options: typing.Optional["ScheduledEc2TaskDefinitionOptions"]=None, scheduled_ec2_task_image_options: typing.Optional["ScheduledEc2TaskImageOptions"]=None, schedule: _Schedule_6cd13e0d, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_task_count: typing.Optional[jsii.Number]=None, subnet_selection: typing.Optional[_SubnetSelection_36a13cd6]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """Constructs a new instance of the ScheduledEc2Task class.

        :param scope: -
        :param id: -
        :param scheduled_ec2_task_definition_options: The properties to define if using an existing TaskDefinition in this construct. ScheduledEc2TaskDefinitionOptions or ScheduledEc2TaskImageOptions must be defined, but not both. Default: none
        :param scheduled_ec2_task_image_options: The properties to define if the construct is to create a TaskDefinition. ScheduledEc2TaskDefinitionOptions or ScheduledEc2TaskImageOptions must be defined, but not both. Default: none
        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_ in the Amazon CloudWatch User Guide.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param subnet_selection: In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        props = ScheduledEc2TaskProps(scheduled_ec2_task_definition_options=scheduled_ec2_task_definition_options, scheduled_ec2_task_image_options=scheduled_ec2_task_image_options, schedule=schedule, cluster=cluster, desired_task_count=desired_task_count, subnet_selection=subnet_selection, vpc=vpc)

        jsii.create(ScheduledEc2Task, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _Ec2TaskDefinition_96cf505d:
        """The EC2 task definition in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "taskDefinition")


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.ScheduledEc2TaskImageOptions", jsii_struct_bases=[ScheduledTaskImageProps], name_mapping={'image': 'image', 'command': 'command', 'environment': 'environment', 'log_driver': 'logDriver', 'secrets': 'secrets', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB', 'memory_reservation_mib': 'memoryReservationMiB'})
class ScheduledEc2TaskImageOptions(ScheduledTaskImageProps):
    def __init__(self, *, image: _ContainerImage_99cc4b15, command: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, log_driver: typing.Optional[_LogDriver_d09e7eb9]=None, secrets: typing.Optional[typing.Mapping[str, _Secret_3f6909a4]]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None) -> None:
        """The properties for the ScheduledEc2Task using an image.

        :param image: The image used to start a container. Image or taskDefinition must be specified, but not both. Default: - none
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param environment: The environment variables to pass to the container. Default: none
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param cpu: The minimum number of CPU units to reserve for the container. Default: none
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.

        stability
        :stability: experimental
        """
        self._values = {
            'image': image,
        }
        if command is not None: self._values["command"] = command
        if environment is not None: self._values["environment"] = environment
        if log_driver is not None: self._values["log_driver"] = log_driver
        if secrets is not None: self._values["secrets"] = secrets
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None: self._values["memory_reservation_mib"] = memory_reservation_mib

    @builtins.property
    def image(self) -> _ContainerImage_99cc4b15:
        """The image used to start a container.

        Image or taskDefinition must be specified, but not both.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @builtins.property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        default
        :default: - CMD value built into container image.

        stability
        :stability: experimental
        """
        return self._values.get('command')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The environment variables to pass to the container.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def log_driver(self) -> typing.Optional[_LogDriver_d09e7eb9]:
        """The log driver to use.

        default
        :default: - AwsLogDriver if enableLogging is true

        stability
        :stability: experimental
        """
        return self._values.get('log_driver')

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[str, _Secret_3f6909a4]]:
        """The secret to expose to the container as an environment variable.

        default
        :default: - No secret environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('secrets')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The minimum number of CPU units to reserve for the container.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The hard limit (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: - No memory limit.

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        """The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under contention, Docker attempts to keep the
        container memory within the limit. If the container requires more memory,
        it can consume up to the value specified by the Memory property or all of
        the available memory on the container instance—whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: - No memory reserved.

        stability
        :stability: experimental
        """
        return self._values.get('memory_reservation_mib')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScheduledEc2TaskImageOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.ScheduledEc2TaskProps", jsii_struct_bases=[ScheduledTaskBaseProps], name_mapping={'schedule': 'schedule', 'cluster': 'cluster', 'desired_task_count': 'desiredTaskCount', 'subnet_selection': 'subnetSelection', 'vpc': 'vpc', 'scheduled_ec2_task_definition_options': 'scheduledEc2TaskDefinitionOptions', 'scheduled_ec2_task_image_options': 'scheduledEc2TaskImageOptions'})
class ScheduledEc2TaskProps(ScheduledTaskBaseProps):
    def __init__(self, *, schedule: _Schedule_6cd13e0d, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_task_count: typing.Optional[jsii.Number]=None, subnet_selection: typing.Optional[_SubnetSelection_36a13cd6]=None, vpc: typing.Optional[_IVpc_3795853f]=None, scheduled_ec2_task_definition_options: typing.Optional["ScheduledEc2TaskDefinitionOptions"]=None, scheduled_ec2_task_image_options: typing.Optional["ScheduledEc2TaskImageOptions"]=None) -> None:
        """The properties for the ScheduledEc2Task task.

        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_ in the Amazon CloudWatch User Guide.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param subnet_selection: In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param scheduled_ec2_task_definition_options: The properties to define if using an existing TaskDefinition in this construct. ScheduledEc2TaskDefinitionOptions or ScheduledEc2TaskImageOptions must be defined, but not both. Default: none
        :param scheduled_ec2_task_image_options: The properties to define if the construct is to create a TaskDefinition. ScheduledEc2TaskDefinitionOptions or ScheduledEc2TaskImageOptions must be defined, but not both. Default: none

        stability
        :stability: experimental
        """
        if isinstance(subnet_selection, dict): subnet_selection = _SubnetSelection_36a13cd6(**subnet_selection)
        if isinstance(scheduled_ec2_task_definition_options, dict): scheduled_ec2_task_definition_options = ScheduledEc2TaskDefinitionOptions(**scheduled_ec2_task_definition_options)
        if isinstance(scheduled_ec2_task_image_options, dict): scheduled_ec2_task_image_options = ScheduledEc2TaskImageOptions(**scheduled_ec2_task_image_options)
        self._values = {
            'schedule': schedule,
        }
        if cluster is not None: self._values["cluster"] = cluster
        if desired_task_count is not None: self._values["desired_task_count"] = desired_task_count
        if subnet_selection is not None: self._values["subnet_selection"] = subnet_selection
        if vpc is not None: self._values["vpc"] = vpc
        if scheduled_ec2_task_definition_options is not None: self._values["scheduled_ec2_task_definition_options"] = scheduled_ec2_task_definition_options
        if scheduled_ec2_task_image_options is not None: self._values["scheduled_ec2_task_image_options"] = scheduled_ec2_task_image_options

    @builtins.property
    def schedule(self) -> _Schedule_6cd13e0d:
        """The schedule or rate (frequency) that determines when CloudWatch Events runs the rule.

        For more information, see
        `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_
        in the Amazon CloudWatch User Guide.

        stability
        :stability: experimental
        """
        return self._values.get('schedule')

    @builtins.property
    def cluster(self) -> typing.Optional[_ICluster_5cbcc408]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_task_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_task_count')

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
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def scheduled_ec2_task_definition_options(self) -> typing.Optional["ScheduledEc2TaskDefinitionOptions"]:
        """The properties to define if using an existing TaskDefinition in this construct.

        ScheduledEc2TaskDefinitionOptions or ScheduledEc2TaskImageOptions must be defined, but not both.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('scheduled_ec2_task_definition_options')

    @builtins.property
    def scheduled_ec2_task_image_options(self) -> typing.Optional["ScheduledEc2TaskImageOptions"]:
        """The properties to define if the construct is to create a TaskDefinition.

        ScheduledEc2TaskDefinitionOptions or ScheduledEc2TaskImageOptions must be defined, but not both.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('scheduled_ec2_task_image_options')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScheduledEc2TaskProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ScheduledFargateTask(ScheduledTaskBase, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs_patterns.ScheduledFargateTask"):
    """A scheduled Fargate task that will be initiated off of CloudWatch Events.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, scheduled_fargate_task_definition_options: typing.Optional["ScheduledFargateTaskDefinitionOptions"]=None, scheduled_fargate_task_image_options: typing.Optional["ScheduledFargateTaskImageOptions"]=None, schedule: _Schedule_6cd13e0d, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_task_count: typing.Optional[jsii.Number]=None, subnet_selection: typing.Optional[_SubnetSelection_36a13cd6]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """Constructs a new instance of the ScheduledFargateTask class.

        :param scope: -
        :param id: -
        :param scheduled_fargate_task_definition_options: The properties to define if using an existing TaskDefinition in this construct. ScheduledFargateTaskDefinitionOptions or ScheduledFargateTaskImageOptions must be defined, but not both. Default: none
        :param scheduled_fargate_task_image_options: The properties to define if the construct is to create a TaskDefinition. ScheduledFargateTaskDefinitionOptions or ScheduledFargateTaskImageOptions must be defined, but not both. Default: none
        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_ in the Amazon CloudWatch User Guide.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param subnet_selection: In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        props = ScheduledFargateTaskProps(scheduled_fargate_task_definition_options=scheduled_fargate_task_definition_options, scheduled_fargate_task_image_options=scheduled_fargate_task_image_options, schedule=schedule, cluster=cluster, desired_task_count=desired_task_count, subnet_selection=subnet_selection, vpc=vpc)

        jsii.create(ScheduledFargateTask, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _FargateTaskDefinition_c5f42010:
        """The Fargate task definition in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "taskDefinition")


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.ScheduledFargateTaskImageOptions", jsii_struct_bases=[ScheduledTaskImageProps], name_mapping={'image': 'image', 'command': 'command', 'environment': 'environment', 'log_driver': 'logDriver', 'secrets': 'secrets', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB'})
class ScheduledFargateTaskImageOptions(ScheduledTaskImageProps):
    def __init__(self, *, image: _ContainerImage_99cc4b15, command: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, log_driver: typing.Optional[_LogDriver_d09e7eb9]=None, secrets: typing.Optional[typing.Mapping[str, _Secret_3f6909a4]]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None) -> None:
        """The properties for the ScheduledFargateTask using an image.

        :param image: The image used to start a container. Image or taskDefinition must be specified, but not both. Default: - none
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param environment: The environment variables to pass to the container. Default: none
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. Default: 512

        stability
        :stability: experimental
        """
        self._values = {
            'image': image,
        }
        if command is not None: self._values["command"] = command
        if environment is not None: self._values["environment"] = environment
        if log_driver is not None: self._values["log_driver"] = log_driver
        if secrets is not None: self._values["secrets"] = secrets
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib

    @builtins.property
    def image(self) -> _ContainerImage_99cc4b15:
        """The image used to start a container.

        Image or taskDefinition must be specified, but not both.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @builtins.property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        default
        :default: - CMD value built into container image.

        stability
        :stability: experimental
        """
        return self._values.get('command')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The environment variables to pass to the container.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def log_driver(self) -> typing.Optional[_LogDriver_d09e7eb9]:
        """The log driver to use.

        default
        :default: - AwsLogDriver if enableLogging is true

        stability
        :stability: experimental
        """
        return self._values.get('log_driver')

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[str, _Secret_3f6909a4]]:
        """The secret to expose to the container as an environment variable.

        default
        :default: - No secret environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('secrets')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 256

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The hard limit (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        default
        :default: 512

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit_mib')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScheduledFargateTaskImageOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs_patterns.ScheduledFargateTaskProps", jsii_struct_bases=[ScheduledTaskBaseProps], name_mapping={'schedule': 'schedule', 'cluster': 'cluster', 'desired_task_count': 'desiredTaskCount', 'subnet_selection': 'subnetSelection', 'vpc': 'vpc', 'scheduled_fargate_task_definition_options': 'scheduledFargateTaskDefinitionOptions', 'scheduled_fargate_task_image_options': 'scheduledFargateTaskImageOptions'})
class ScheduledFargateTaskProps(ScheduledTaskBaseProps):
    def __init__(self, *, schedule: _Schedule_6cd13e0d, cluster: typing.Optional[_ICluster_5cbcc408]=None, desired_task_count: typing.Optional[jsii.Number]=None, subnet_selection: typing.Optional[_SubnetSelection_36a13cd6]=None, vpc: typing.Optional[_IVpc_3795853f]=None, scheduled_fargate_task_definition_options: typing.Optional["ScheduledFargateTaskDefinitionOptions"]=None, scheduled_fargate_task_image_options: typing.Optional["ScheduledFargateTaskImageOptions"]=None) -> None:
        """The properties for the ScheduledFargateTask task.

        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_ in the Amazon CloudWatch User Guide.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param subnet_selection: In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param scheduled_fargate_task_definition_options: The properties to define if using an existing TaskDefinition in this construct. ScheduledFargateTaskDefinitionOptions or ScheduledFargateTaskImageOptions must be defined, but not both. Default: none
        :param scheduled_fargate_task_image_options: The properties to define if the construct is to create a TaskDefinition. ScheduledFargateTaskDefinitionOptions or ScheduledFargateTaskImageOptions must be defined, but not both. Default: none

        stability
        :stability: experimental
        """
        if isinstance(subnet_selection, dict): subnet_selection = _SubnetSelection_36a13cd6(**subnet_selection)
        if isinstance(scheduled_fargate_task_definition_options, dict): scheduled_fargate_task_definition_options = ScheduledFargateTaskDefinitionOptions(**scheduled_fargate_task_definition_options)
        if isinstance(scheduled_fargate_task_image_options, dict): scheduled_fargate_task_image_options = ScheduledFargateTaskImageOptions(**scheduled_fargate_task_image_options)
        self._values = {
            'schedule': schedule,
        }
        if cluster is not None: self._values["cluster"] = cluster
        if desired_task_count is not None: self._values["desired_task_count"] = desired_task_count
        if subnet_selection is not None: self._values["subnet_selection"] = subnet_selection
        if vpc is not None: self._values["vpc"] = vpc
        if scheduled_fargate_task_definition_options is not None: self._values["scheduled_fargate_task_definition_options"] = scheduled_fargate_task_definition_options
        if scheduled_fargate_task_image_options is not None: self._values["scheduled_fargate_task_image_options"] = scheduled_fargate_task_image_options

    @builtins.property
    def schedule(self) -> _Schedule_6cd13e0d:
        """The schedule or rate (frequency) that determines when CloudWatch Events runs the rule.

        For more information, see
        `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_
        in the Amazon CloudWatch User Guide.

        stability
        :stability: experimental
        """
        return self._values.get('schedule')

    @builtins.property
    def cluster(self) -> typing.Optional[_ICluster_5cbcc408]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_task_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_task_count')

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
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def scheduled_fargate_task_definition_options(self) -> typing.Optional["ScheduledFargateTaskDefinitionOptions"]:
        """The properties to define if using an existing TaskDefinition in this construct.

        ScheduledFargateTaskDefinitionOptions or ScheduledFargateTaskImageOptions must be defined, but not both.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('scheduled_fargate_task_definition_options')

    @builtins.property
    def scheduled_fargate_task_image_options(self) -> typing.Optional["ScheduledFargateTaskImageOptions"]:
        """The properties to define if the construct is to create a TaskDefinition.

        ScheduledFargateTaskDefinitionOptions or ScheduledFargateTaskImageOptions must be defined, but not both.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('scheduled_fargate_task_image_options')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScheduledFargateTaskProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "ApplicationListenerProps",
    "ApplicationLoadBalancedEc2Service",
    "ApplicationLoadBalancedEc2ServiceProps",
    "ApplicationLoadBalancedFargateService",
    "ApplicationLoadBalancedFargateServiceProps",
    "ApplicationLoadBalancedServiceBase",
    "ApplicationLoadBalancedServiceBaseProps",
    "ApplicationLoadBalancedTaskImageOptions",
    "ApplicationLoadBalancedTaskImageProps",
    "ApplicationLoadBalancerProps",
    "ApplicationMultipleTargetGroupsEc2Service",
    "ApplicationMultipleTargetGroupsEc2ServiceProps",
    "ApplicationMultipleTargetGroupsFargateService",
    "ApplicationMultipleTargetGroupsFargateServiceProps",
    "ApplicationMultipleTargetGroupsServiceBase",
    "ApplicationMultipleTargetGroupsServiceBaseProps",
    "ApplicationTargetProps",
    "NetworkListenerProps",
    "NetworkLoadBalancedEc2Service",
    "NetworkLoadBalancedEc2ServiceProps",
    "NetworkLoadBalancedFargateService",
    "NetworkLoadBalancedFargateServiceProps",
    "NetworkLoadBalancedServiceBase",
    "NetworkLoadBalancedServiceBaseProps",
    "NetworkLoadBalancedTaskImageOptions",
    "NetworkLoadBalancedTaskImageProps",
    "NetworkLoadBalancerProps",
    "NetworkMultipleTargetGroupsEc2Service",
    "NetworkMultipleTargetGroupsEc2ServiceProps",
    "NetworkMultipleTargetGroupsFargateService",
    "NetworkMultipleTargetGroupsFargateServiceProps",
    "NetworkMultipleTargetGroupsServiceBase",
    "NetworkMultipleTargetGroupsServiceBaseProps",
    "NetworkTargetProps",
    "QueueProcessingEc2Service",
    "QueueProcessingEc2ServiceProps",
    "QueueProcessingFargateService",
    "QueueProcessingFargateServiceProps",
    "QueueProcessingServiceBase",
    "QueueProcessingServiceBaseProps",
    "ScheduledEc2Task",
    "ScheduledEc2TaskDefinitionOptions",
    "ScheduledEc2TaskImageOptions",
    "ScheduledEc2TaskProps",
    "ScheduledFargateTask",
    "ScheduledFargateTaskDefinitionOptions",
    "ScheduledFargateTaskImageOptions",
    "ScheduledFargateTaskProps",
    "ScheduledTaskBase",
    "ScheduledTaskBaseProps",
    "ScheduledTaskImageProps",
]

publication.publish()
