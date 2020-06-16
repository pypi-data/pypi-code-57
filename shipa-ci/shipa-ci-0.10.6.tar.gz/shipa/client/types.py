from schematics import Model
from schematics.types import StringType, BooleanType, ListType, ModelType, IntType, DictType

from shipa.commands.constant import KUBERNETES_PROVISIONER


class NodeMetadata(Model):
    driver = StringType(required=True)
    address = StringType(required=True)
    iaas = StringType(required=True, default='dockermachine')
    iaas_id = StringType(serialized_name='iaas-id', serialize_when_none=False)
    template = StringType(serialize_when_none=False)


class AddNodeRequest(Model):
    register = BooleanType()
    client_key = StringType(serialized_name='clientKey', serialize_when_none=False)
    client_cert = StringType(serialized_name='clientCert', serialize_when_none=False)
    ca_cert = StringType(serialized_name='caCert', serialize_when_none=False)
    alternative_pools = ListType(StringType, serialized_name='alternativePools', default=tuple())
    pool = StringType(serialized_name='pool', required=True)
    meta_data = ModelType(NodeMetadata, serialized_name='metaData', required=True)


class UpdatePoolRequest(Model):
    force = BooleanType(default=True)
    default = BooleanType(serialize_when_none=False, default=False)
    public = BooleanType(serialize_when_none=False, default=False)
    plan = StringType(serialize_when_none=False)
    accept_drivers = ListType(StringType, serialized_name='acceptdriver', default=tuple())
    app_quota_limit = IntType(serialized_name='appquotalimit', serialize_when_none=False)


class AddPoolRequest(Model):
    force = BooleanType(default=True)
    default = BooleanType(serialize_when_none=False, default=False)
    public = BooleanType(serialize_when_none=False, default=False)
    name = StringType(required=True)
    plan = StringType(serialize_when_none=False)
    accept_drivers = ListType(StringType, serialized_name='acceptdriver', default=tuple())
    app_quota_limit = IntType(serialized_name='appquotalimit', serialize_when_none=False)
    kubernetes_namespace = StringType(serialized_name='kubernetesnamespace', serialize_when_none=False)
    provisioner = StringType(serialize_when_none=False)


class RemovePoolRequest(Model):
    address = StringType(required=True)
    no_rebalance = BooleanType(serialized_name='no-rebalance', default=False)
    destroy = BooleanType(serialized_name='remove-iaas', default=False)


class AddAppRequest(Model):
    name = StringType(required=True)
    platform = StringType(serialize_when_none=False)
    plan = StringType(serialize_when_none=False)
    team = StringType(serialized_name='teamOwner', required=True)
    description = StringType(serialize_when_none=False)
    pool = StringType(serialize_when_none=False)
    router = StringType(serialize_when_none=False)
    dependency_files = ListType(StringType, serialized_name='dependency_filenames', default=tuple())
    tags = ListType(StringType, default=tuple())
    router_opts = DictType(StringType, serialized_name='routeropts', default=dict())


class DeployAppRequest(Model):
    steps = IntType(default=1)
    kind = StringType(default='git')
    step_weight = IntType(serialized_name='step-weight', default=100)
    step_interval = IntType(serialized_name='step-interval', default=1)


class MoveAppRequest(Model):
    pool = StringType(required=True)


class AddClusterRequest(Model):
    name = StringType(required=True)
    default = BooleanType(serialize_when_none=False, default=False)
    provisioner = StringType(default=KUBERNETES_PROVISIONER)
    client_key = StringType(serialized_name='clientKey', serialize_when_none=False)
    client_cert = StringType(serialized_name='clientCert', serialize_when_none=False)
    ca_cert = StringType(serialized_name='caCert', serialize_when_none=False)
    token = StringType(serialize_when_none=False)
    custom_data = DictType(StringType, default=dict())
    address = ListType(StringType, serialized_name='addresses', default=tuple())
    pools = ListType(StringType, default=tuple())
    teams = ListType(StringType, default=tuple())
    ingress_port = IntType(default=0)
    ingress_ip = StringType(serialize_when_none=False)
    ingress_service = StringType(serialized_name='ingress_service_type', serialize_when_none=False)
