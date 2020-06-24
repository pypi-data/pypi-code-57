from aws_cdk import core
from aws_cdk.aws_ec2 import Vpc, InstanceClass, InstanceSize, Port, GatewayVpcEndpointAwsService, SubnetType
from aws_cdk.aws_ecs import Cluster
from aws_cdk.aws_elasticloadbalancingv2 import ApplicationTargetGroup, ApplicationLoadBalancer, TargetType, \
    ApplicationProtocol
from aws_cdk.aws_kms import Key

from services.ecs.standalone_fargate_service import StandaloneFargateService
from services.elasticache.redis import Redis
from services.rds.postgres import Postgres
from services.storage.s3 import GICBucket


class ThothStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = Vpc.from_lookup(self, 'thoth-vpc', vpc_id='vpc-0a62453c5ec215001')
        private_subnets = vpc.select_subnets(subnet_type=SubnetType.PRIVATE)
        vpc.add_gateway_endpoint('s3-endpoint', service=GatewayVpcEndpointAwsService.S3,
                                 subnets=private_subnets.subnets)
        redis = Redis(self, 'thoth-redis-cluster',
                      vpc=vpc,
                      node_count=2,
                      cache_node_type='cache.m3.medium')
        bucket_key = Key(self, 'thoth-s3-key',
                         enable_key_rotation=True,
                         description='Key for encrypting bucket contents for Thoth',
                         alias='thoth/s3')
        images_bucket = GICBucket(self, 'images-bucket', 'thoth-gic-production-images', encryption_key=bucket_key)
        files_bucket = GICBucket(self, 'files-bucket', 'thoth-gic-production-uploads', encryption_key=bucket_key)
        database_name = 'thoth'
        db_instance = Postgres(self, "thoth-db",
                               master_username='gic_admin',
                               vpc=vpc,
                               database_name=database_name,
                               instance_class=InstanceClass.BURSTABLE3,
                               instance_size=InstanceSize.MEDIUM,
                               instance_identifier='thoth-db')
        app_env = {
            'SQLALCHEMY_DATABASE_URI': f'postgres://username:password@{db_instance.endpoint}/{database_name}',
            'CELERY_BROKER_URL': f'redis://{redis.primary_address}:{redis.primary_port}',
            'CELERY_RESULT_BACKEND': f'redis://{redis.primary_address}:{redis.primary_port}',
            'S3_BUCKET': files_bucket.bucket_name,
            'IMAGES_S3_BUCKET': images_bucket.bucket_name
        }
        load_balancer = ApplicationLoadBalancer(self, 'thoth-lb', vpc=vpc, internet_facing=True,
                                                load_balancer_name='thoth-production-ecs-lb')
        api_target_group = ApplicationTargetGroup(self, 'api-target-group', port=80, vpc=vpc,
                                                  target_type=TargetType.IP)
        ui_target_group = ApplicationTargetGroup(self, 'ui-target-group', port=80, vpc=vpc,
                                                 target_type=TargetType.IP)
        http_listener = load_balancer.add_listener('http-listener', port=80, protocol=ApplicationProtocol.HTTP)
        http_listener.add_redirect_response('redirect-to-https', status_code='HTTP_302', protocol='HTTPS', port='443')
        https_listener = load_balancer.add_listener('https-listener', port=443, protocol=ApplicationProtocol.HTTPS,
                                                    certificate_arns=[
                                                        'arn:aws:acm:ap-southeast-1:538864164357:certificate/d81663da-0161-4c34-ae43-e922268a047c'],
                                                    default_target_groups=[ui_target_group])
        https_listener.add_target_groups('api-target-group', target_groups=[api_target_group],
                                         host_header='api.thoth.giclabs.com',
                                         priority=1)
        ecs_cluster = Cluster(self, 'thoth', cluster_name='thoth-gic-production', vpc=vpc)
        ui_service = StandaloneFargateService(self, 'thoth-ui', service_name='thoth-ui', cluster=ecs_cluster,
                                              task_cpu=512,
                                              task_mem_limit_mib=1024, ecr_repo_name='thoth-ui', image_tag='production',
                                              desired_container_count=2)
        api_service = StandaloneFargateService(self, 'thoth-api',
                                               service_name='thoth-api',
                                               cluster=ecs_cluster,
                                               task_cpu=1024,
                                               task_mem_limit_mib=2048,
                                               ecr_repo_name='thoth-api',
                                               image_tag='production',
                                               desired_container_count=2,
                                               environment=app_env)
        celery_service = StandaloneFargateService(self, 'thoth-celery', service_name='thoth-celery',
                                                  cluster=ecs_cluster,
                                                  task_cpu=1024, task_mem_limit_mib=2048, ecr_repo_name='thoth-celery',
                                                  image_tag='production', desired_container_count=2,
                                                  environment=app_env)
        db_instance.allow_connection_from(api_service.service_instance)
        db_instance.allow_connection_from(celery_service.service_instance)
        ui_service.service_instance.attach_to_application_target_group(ui_target_group)
        ui_service.allow_connection_from(load_balancer, Port.tcp(80))
        api_service.service_instance.attach_to_application_target_group(api_target_group)
        api_service.allow_connection_from(load_balancer, Port.tcp(80))
        redis.allow_connection_from(api_service.service_instance)
        redis.allow_connection_from(celery_service.service_instance)

