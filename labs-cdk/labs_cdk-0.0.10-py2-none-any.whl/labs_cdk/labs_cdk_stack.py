from aws_cdk import core

from services.ecs.container_repository import ContainerRepository


class LabsCdkStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ContainerRepository(self, 'test', repository_name='test_repo')
