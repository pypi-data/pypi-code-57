import typing

from aws_cdk.aws_ec2 import IConnectable, Port
from aws_cdk.aws_ecr import Repository
from aws_cdk.aws_ecs import FargateTaskDefinition, ICluster, ContainerImage, LogDriver, FargateService, PortMapping, \
    Protocol
from aws_cdk.aws_logs import RetentionDays
from aws_cdk.core import Construct
from jsii import Number


class StandaloneFargateService(Construct):
    def __init__(self, scope, id: str, *, service_name: str, cluster: ICluster, task_cpu: Number,
                 task_mem_limit_mib: Number, ecr_repo_name: str, image_tag: str, desired_container_count: int,
                 environment: typing.Optional[typing.Mapping[str, str]] = None):
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
        self.service = FargateService(scope, f'{service_name}-service', task_definition=task_definition,
                                      cluster=cluster,
                                      desired_count=desired_container_count, min_healthy_percent=50,
                                      max_healthy_percent=100,
                                      service_name=service_name)

    @property
    def service_instance(self):
        return self.service

    def allow_connection_from(self, other: IConnectable, port: Port = None):
        connection_port = port or Port.tcp(80)
        return self.service.connections.allow_from(other, connection_port)
