import typing

from aws_cdk.aws_certificatemanager import ICertificate
from aws_cdk.aws_ecr import Repository
from aws_cdk.aws_ecs import ICluster, FargateTaskDefinition, ContainerImage, LogDriver, PortMapping, Protocol
from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService
from aws_cdk.aws_elasticloadbalancingv2 import ApplicationProtocol, IApplicationLoadBalancer
from aws_cdk.aws_logs import RetentionDays
from aws_cdk.aws_route53 import HostedZone
from aws_cdk.core import Construct
from jsii import Number


class AlbFargateService(Construct):
    def __init__(self, scope: Construct, id: str, *, service_name: str, cluster: ICluster, task_cpu: Number,
                 task_mem_limit_mib: Number, ecr_repo_name: str, image_tag: str, desired_container_count: int,
                 environment: typing.Optional[typing.Mapping[str, str]] = None,
                 load_balancer: typing.Optional[IApplicationLoadBalancer] = None,
                 certificate: typing.Optional[ICertificate] = None):
        super().__init__(scope, id)

        task_definition = FargateTaskDefinition(scope, f'{service_name}-task-definition', cpu=task_cpu,
                                                memory_limit_mib=task_mem_limit_mib)
        image_repo = Repository.from_repository_name(scope, f'{service_name}-repository',
                                                     repository_name=ecr_repo_name)
        container_definition = task_definition.add_container(
            f'{service_name}-container',
            image=ContainerImage.from_ecr_repository(image_repo, tag=image_tag),
            logging=LogDriver.aws_logs(stream_prefix=service_name, log_retention=RetentionDays.ONE_WEEK),
            memory_limit_mib=task_mem_limit_mib, cpu=task_cpu, environment=environment)
        container_definition.add_port_mappings(PortMapping(container_port=80, host_port=80, protocol=Protocol.TCP))
        self.service = ApplicationLoadBalancedFargateService(
            scope, f'{service_name}-service',
            cpu=desired_container_count * task_cpu,
            memory_limit_mib=desired_container_count * task_mem_limit_mib,
            task_definition=task_definition,
            cluster=cluster,
            desired_count=desired_container_count,
            min_healthy_percent=50,
            max_healthy_percent=100, listener_port=80,
            public_load_balancer=True,
            protocol=ApplicationProtocol.HTTPS,
            domain_name='giclabs.com',
            domain_zone=HostedZone.from_hosted_zone_attributes(scope, f'giclabs-zone-{id}',
                                                               hosted_zone_id='Z3U2I70U6FV8LX',
                                                               zone_name='giclabs.com'),
            service_name=service_name,
            load_balancer=load_balancer,
            certificate=certificate)

    @property
    def load_balancer(self):
        return self.service.load_balancer

    @property
    def service_instance(self):
        return self.service.service
