import typing

from aws_cdk.aws_ecr import Repository, LifecycleRule, TagStatus
from aws_cdk.core import Construct, RemovalPolicy


class ContainerRepository(Construct):
    def __init__(self, scope: Construct, id: str, *, repository_name: typing.Optional[str] = None):
        super().__init__(scope, id)
        remove_untagged_images_rule = LifecycleRule(description='Remove untagged images', max_image_count=1,
                                                    rule_priority=1,
                                                    tag_status=TagStatus.UNTAGGED)
        Repository(scope, f'${id}-repository', image_scan_on_push=True, repository_name=repository_name,
                   removal_policy=RemovalPolicy.DESTROY,
                   lifecycle_rules=[remove_untagged_images_rule])
