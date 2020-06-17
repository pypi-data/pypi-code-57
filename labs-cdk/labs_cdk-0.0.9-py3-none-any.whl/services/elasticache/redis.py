from aws_cdk.aws_ec2 import SecurityGroup, Port, IVpc, SubnetType, IConnectable
from aws_cdk.aws_elasticache import CfnReplicationGroup, CfnSubnetGroup
from aws_cdk.core import Construct


class Redis(Construct):
    def __init__(self, scope: Construct, id: str, *, vpc: IVpc, node_count: int,
                 cache_node_type: str):
        super().__init__(scope, id)
        self.security_group = SecurityGroup(scope, 'redis-security-group', allow_all_outbound=True, vpc=vpc)
        private_subnets = vpc.select_subnets(subnet_type=SubnetType.PRIVATE)
        subnet_group = CfnSubnetGroup(scope, 'redis-subnet-group', description='redis-subnet-groups',
                                      subnet_ids=private_subnets.subnet_ids,
                                      cache_subnet_group_name=f'subnet-group-{id}')
        self.replication_group = CfnReplicationGroup(scope, 'redis-cluster', engine='redis',
                                                     automatic_failover_enabled=True,
                                                     auto_minor_version_upgrade=False, cache_node_type=cache_node_type,
                                                     cache_subnet_group_name=subnet_group.cache_subnet_group_name,
                                                     replicas_per_node_group=node_count,
                                                     security_group_ids=[self.security_group.security_group_id],
                                                     replication_group_description=f'Multi AZ with {node_count} nodes',
                                                     at_rest_encryption_enabled=True,
                                                     transit_encryption_enabled=True,
                                                     )
        self.replication_group.add_depends_on(subnet_group)

    @property
    def primary_address(self):
        return self.replication_group.attr_primary_end_point_address

    @property
    def primary_port(self):
        return self.replication_group.attr_primary_end_point_port

    def allow_connection_from(self, other: IConnectable, port: Port = None):
        connection_port = port or Port.tcp(6379)
        return self.security_group.connections.allow_from(other, connection_port)
