from aws_cdk import core
from aws_cdk.aws_ec2 import Vpc, SubnetConfiguration, SubnetType, Port, DefaultInstanceTenancy, \
    Peer, InstanceClass, InstanceSize
from aws_cdk.aws_ecs import Cluster
from aws_cdk.aws_elasticloadbalancingv2 import ApplicationLoadBalancer, ApplicationProtocol, ApplicationTargetGroup, \
    TargetType

from services.ecs.standalone_fargate_service import StandaloneFargateService
from services.rds.postgres import Postgres


class LabsWebsiteStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        subnet_configurations = [
            SubnetConfiguration(name='public', subnet_type=SubnetType.PUBLIC, cidr_mask=24),
            SubnetConfiguration(name='private', subnet_type=SubnetType.PRIVATE, cidr_mask=24),
        ]
        vpc = Vpc(self, "awakening-vpc",
                  cidr="10.0.0.0/16",
                  enable_dns_support=True,
                  enable_dns_hostnames=True,
                  default_instance_tenancy=DefaultInstanceTenancy.DEFAULT,
                  subnet_configuration=subnet_configurations,
                  max_azs=2)
        db_instance = Postgres(self, "awakening-db", master_username='gic_admin', vpc=vpc,
                               database_name='awakening_production',
                               instance_class=InstanceClass.BURSTABLE3, instance_size=InstanceSize.MEDIUM,
                               instance_identifier='awakening-production')

        load_balancer = ApplicationLoadBalancer(self, 'awakening-lb', vpc=vpc, internet_facing=True,
                                                load_balancer_name='awakening-production-ecs-lb')
        load_balancer.connections.allow_from(Peer.ipv4('203.116.80.0/26'), Port.tcp(443), 'GIC Internal')
        load_balancer.connections.allow_from(Peer.ipv4('203.117.79.224/27'), Port.tcp(443), 'GIC Internal')
        load_balancer.connections.allow_from(Peer.ipv4('203.126.225.0/25'), Port.tcp(443), 'GIC Internal')
        load_balancer.connections.allow_from(Peer.ipv4('203.116.205.128/25'), Port.tcp(443), 'GIC Internal')
        load_balancer.connections.allow_from(Peer.ipv4('80.169.164.0/27'), Port.tcp(443), 'GIC Internal')
        load_balancer.connections.allow_from(Peer.ipv4('65.223.191.160/27'), Port.tcp(443), 'GIC Internal')
        load_balancer.connections.allow_from(Peer.ipv4('206.169.170.240/28'), Port.tcp(443), 'GIC Internal')
        load_balancer.connections.allow_from(Peer.ipv4('203.116.125.128/25'), Port.tcp(443), 'GIC Internal')
        load_balancer.connections.allow_from(Peer.ipv4('64.129.229.24/30'), Port.tcp(443), 'GIC Internal')
        load_balancer.connections.allow_from(Peer.ipv4('129.126.66.38/32'), Port.tcp(443), 'GIC Internal')
        load_balancer.connections.allow_from(Peer.ipv4('182.55.245.32/32'), Port.tcp(443), 'GIC Internal')
        load_balancer.connections.allow_from(Peer.ipv4('183.90.112.163/32'), Port.tcp(443), 'GIC Internal')
        load_balancer.connections.allow_from(Peer.ipv4('202.166.138.105/32'), Port.tcp(443), 'GIC Internal')
        load_balancer.connections.allow_from(Peer.ipv4('155.69.184.14/32'), Port.tcp(443), 'GIC Internal')

        api_target_group = ApplicationTargetGroup(self, 'api-target-group', port=80, vpc=vpc,
                                                  target_type=TargetType.IP)
        ui_target_group = ApplicationTargetGroup(self, 'ui-target-group', port=80, vpc=vpc,
                                                 target_type=TargetType.IP)
        http_listener = load_balancer.add_listener('http-listener', port=80, protocol=ApplicationProtocol.HTTP)
        http_listener.add_redirect_response('redirect-to-https', status_code='HTTP_302', protocol='HTTPS', port='443')
        https_listener = load_balancer.add_listener('https-listener', port=443, protocol=ApplicationProtocol.HTTPS,
                                                    certificate_arns=[
                                                        'arn:aws:acm:ap-southeast-1:538864164357:certificate/cfd3eaa0-666b-4408-ac6b-14f25e81aac1'],
                                                    default_target_groups=[ui_target_group])
        https_listener.add_target_groups('api-target-group', target_groups=[api_target_group], path_pattern='/api*',
                                         priority=1)

        ecs_cluster = Cluster(self, 'awakening-production', cluster_name='awakening-production', vpc=vpc)
        api_service = StandaloneFargateService(self, 'awakening-api', service_name='awakening-api', cluster=ecs_cluster,
                                               task_cpu=256, task_mem_limit_mib=512, ecr_repo_name='awakening-api',
                                               image_tag='production', desired_container_count=2)
        api_service.service_instance.attach_to_application_target_group(api_target_group)
        api_service.service_instance.connections.allow_from(load_balancer, Port.tcp(80),
                                                            description='load balancer target')
        db_instance.allow_connection_from(api_service.service_instance)
        ui_service = StandaloneFargateService(self, 'awakening-ui', service_name='awakening-ui', cluster=ecs_cluster,
                                              task_cpu=256, task_mem_limit_mib=512, ecr_repo_name='awakening-ui',
                                              image_tag='production', desired_container_count=2)
        ui_service.service_instance.attach_to_application_target_group(ui_target_group)
        ui_service.service_instance.connections.allow_from(load_balancer, Port.tcp(80),
                                                           description='load balancer target')
