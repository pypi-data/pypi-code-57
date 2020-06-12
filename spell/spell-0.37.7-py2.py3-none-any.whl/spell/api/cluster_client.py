from spell.api import base_client
from spell.api.utils import url_path_join

CLUSTER_RESOURCE_URL = "clusters"


class ClusterClient(base_client.BaseClient):
    def get_cluster(self, cluster_name):
        """Get info for a cluster given a cluster_name.

        Keyword arguments:
        cluster_name -- the name of the cluster
        """
        r = self.request("get", url_path_join(CLUSTER_RESOURCE_URL, self.owner, cluster_name))
        self.check_and_raise(r)
        return self.get_json(r)["cluster"]

    def list_clusters(self):
        """List info for all current owner clusters."""
        r = self.request("get", url_path_join(CLUSTER_RESOURCE_URL, self.owner))
        self.check_and_raise(r)
        return self.get_json(r)["clusters"]

    def validate_cluster_name(self, name):
        """Throws an error if this name is an illegal name for a cluster.

        Keyword arguments:
        name -- a potential name for a cluster
        """
        r = self.request(
            "get", url_path_join(CLUSTER_RESOURCE_URL, self.owner, "validate_name", name),
        )
        self.check_and_raise(r)

    def create_aws_cluster(
        self,
        name,
        role_arn,
        external_id,
        read_policy,
        security_group_id,
        s3_bucket,
        vpc_id,
        subnets,
        region,
    ):
        """Construct a cluster to map to a users aws cluster.

        Keyword arguments:
        name -- a display name for the cluster
        role_arn -- the aws arn of a role granting Spell necessary permissions to manage the cluster
        external_id -- needed to assume the role
        read_policy -- name of the s3 read policy associated with the IAM role
        security_group_id -- security group in the VPC with SSH and Docker port access to workers
        s3_bucket - a bucket to store run outputs in
        vpc_id - the id of vpc to setup this cluster in
        subnets - all subnets which Spell will attempt to launch machines in
            (due to aws capacity constraints more is preferable)
        region - the aws region of this vpc
        """
        payload = {
            "cluster_name": name,
            "role_arn": role_arn,
            "external_id": external_id,
            "read_policy": read_policy,
            "security_group_id": security_group_id,
            "s3_bucket": s3_bucket,
            "vpc_id": vpc_id,
            "subnets": subnets,
            "region": region,
        }
        endpoint = url_path_join(CLUSTER_RESOURCE_URL, self.owner, "aws")
        r = self.request("put", endpoint, payload=payload)
        self.check_and_raise(r)
        return self.get_json(r)["cluster"]

    def create_gcp_cluster(
        self,
        name,
        service_account_id,
        gs_bucket,
        vpc_id,
        subnet,
        region,
        project,
        gs_access_key_id,
        gs_secret_access_key,
        api_key,
    ):
        """Construct a cluster to map to a users gcp cluster.

        Keyword arguments:
        name -- a display name for the cluster
        service_account_id -- the email of a service account granting Spell necessary permissions to manage the cluster
        gs_bucket - a bucket to store run outputs in
        vpc_id - name of network to run machines in
        subnets - a subnet in vpc_id to run machines in
        region - region in which the subnets live
        project - project that network lives in
        gs_access_key_id - gs interoperable s3 access key
        gs_secret_access_key - gs interoperable s3 access secret
        """

        payload = {
            "cluster_name": name,
            "gs_bucket": gs_bucket,
            "vpc_id": vpc_id,
            "subnet": subnet,
            "region": region,
            "project": project,
            "service_account_id": service_account_id,
            "gs_access_key_id": gs_access_key_id,
            "gs_secret_access_key": gs_secret_access_key,
            "gcp_account_api_key": api_key,
        }
        endpoint = url_path_join(CLUSTER_RESOURCE_URL, self.owner, "gcp")
        r = self.request("put", endpoint, payload=payload)
        self.check_and_raise(r)
        return self.get_json(r)["cluster"]

    def register_serving_cluster(self, cluster_name, kube_config, default_sg_config):
        """Submit a model-server kubeconfig to be stored as the
        active model-server cluster for the current org.

        Keyword arguments:
        cluster_name -- the name of the cluster to update
        kube_config -- a string containing a yaml kubeconfig
        default_sg_config -- a dict containing the config params of the default serving group
        """
        payload = {
            "kube_config": kube_config,
            "default_serving_group_config": default_sg_config,
        }
        endpoint = url_path_join(CLUSTER_RESOURCE_URL, self.owner, cluster_name, "kube_config")
        r = self.request("put", endpoint, payload=payload)
        self.check_and_raise(r)
        return r.status_code

    def deregister_serving_cluster(self, cluster_name):
        """Unregister a model server kubeconfig from the given cluster

        Keyword arguments:
        cluster_name -- the name of the cluster to update
        """
        endpoint = url_path_join(CLUSTER_RESOURCE_URL, self.owner, cluster_name, "kube_config")
        r = self.request("delete", endpoint)
        self.check_and_raise(r)

    def generate_serving_group_config(
        self,
        cluster_name,
        name,
        instance_type,
        accelerators=None,
        min_nodes=None,
        max_nodes=None,
        spot=None,
        disk_size=None,
    ):
        """Create an autoscaling node group within a model serving cluster

        Keyword arguments:
        cluster_name -- the name of the cluster to update
        name -- the name of the new autoscaling group
        instance_type -- the instance type of the nodes to bring up
        accelerators -- (gcp specific) list of accelerators and counts to attach to nodes
        min_nodes -- minimum nodes for autoscaling
        max_nodes -- maximum nodes for autoscaling
        spot -- enable spot instances for nodes
        disk_size -- disk size (GB) to attach to nodes
        """
        payload = {
            "name": name,
            "instance_type": instance_type,
            "accelerators": accelerators,
            "is_spot": spot,
            "disk_size_gb": disk_size,
            "min_nodes": min_nodes,
            "max_nodes": max_nodes,
        }
        endpoint = url_path_join(
            CLUSTER_RESOURCE_URL, self.owner, cluster_name, "serving_groups", "config",
        )
        r = self.request("get", endpoint, params=payload)
        self.check_and_raise(r)
        return self.get_json(r)["config"]

    def create_serving_group(
        self, cluster_name, name, config_contents,
    ):
        """Create an autoscaling node group within a model serving cluster

        Keyword arguments:
        cluster_name -- the name of the cluster to update
        name -- the name of the new serving group
        config_contents -- contents of explicit eksctl or GKE node group config
        """
        payload = {
            "name": name,
            "config_contents": config_contents,
        }
        endpoint = url_path_join(CLUSTER_RESOURCE_URL, self.owner, cluster_name, "serving_groups")
        r = self.request("post", endpoint, payload=payload)
        self.check_and_raise(r)
        return self.get_json(r)["serving_group"]

    def scale_serving_group(
        self, cluster_name, name, min_nodes=None, max_nodes=None,
    ):
        """Adjust min/max nodes of a serving group

        Keyword arguments:
        cluster_name -- the name of the cluster to update
        name -- the name of the serving group
        min_nodes -- new min nodes value
        max_nodes -- new min nodes value
        """
        payload = {
            "min_nodes": min_nodes,
            "max_nodes": max_nodes,
        }
        endpoint = url_path_join(
            CLUSTER_RESOURCE_URL, self.owner, cluster_name, "serving_groups", name, "scale"
        )
        r = self.request("post", endpoint, payload=payload)
        self.check_and_raise(r)

    def delete_serving_group(
        self, cluster_name, name,
    ):
        """Delete a serving group

        Keyword arguments:
        cluster_name -- the name of the cluster to update
        name -- the name of the serving group
        """
        endpoint = url_path_join(
            CLUSTER_RESOURCE_URL, self.owner, cluster_name, "serving_groups", name,
        )
        r = self.request("delete", endpoint)
        self.check_and_raise(r)

    def add_bucket(self, bucket_name, cluster_name, provider):
        """Add a bucket to SpellFS using the permissions of the specified cluster

        Keyword arguments:
        bucket_name -- the name of the bucket
        cluster_name -- the name of the cluster
        provider -- storage provider for bucket ("s3", "gs", etc.)
        """
        payload = {"bucket": bucket_name, "provider": provider}
        endpoint = url_path_join(CLUSTER_RESOURCE_URL, self.owner, cluster_name, "bucket")
        r = self.request("put", endpoint, payload=payload)
        self.check_and_raise(r)

    def update_cluster_version(self, cluster_name, version):
        """Updates a cluster's version number in the database

        Keyword arguments:
        cluster_name -- the name of the cluster
        version -- the new version number to write to the database
        """
        payload = {"version": version}
        endpoint = url_path_join(CLUSTER_RESOURCE_URL, self.owner, cluster_name, "update_version")
        r = self.request("put", endpoint, payload=payload)
        self.check_and_raise(r)

    def update_gcp_cluster_credentials(
        self, cluster_name, access_key=None, secret=None, api_key=None
    ):
        """Updates a cluster's HMAC key and secret in the database

        Keyword arguments:
        cluster_name -- the name of the cluster
        access_key -- the access key for the service account, for hmac
        secret -- the secret associated with the access key, for hmac
        api_key -- api key for service account
        """
        payload = {"access_key": access_key, "secret": secret, "gcp_account_api_key": api_key}
        endpoint = url_path_join(
            CLUSTER_RESOURCE_URL, self.owner, cluster_name, "update_gcp_s3_key"
        )
        r = self.request("put", endpoint, payload=payload)
        self.check_and_raise(r)

    def delete_cluster_contents(self, cluster_name):
        """Deletes all associated Spell managed infrastructure for a cluster

        Keyword arguments:
        cluster_name -- the name of the cluster
        """
        url = url_path_join(CLUSTER_RESOURCE_URL, self.owner, cluster_name, "delete_contents")
        r = self.request("put", url)
        self.check_and_raise(r)

    def is_cluster_drained(self, cluster_name):
        """Returns 200 if the cluster is drained and 400 if not

        Keyword arguments:
        cluster_name -- the name of the cluster
        """
        url = url_path_join(CLUSTER_RESOURCE_URL, self.owner, cluster_name, "is_drained")
        r = self.request("get", url)
        self.check_and_raise(r)

    def delete_cluster(self, cluster_name):
        """Marks a cluster as deleted in the db

        Keyword arguments:
        cluster_name -- the name of the cluster
        """
        url = url_path_join(CLUSTER_RESOURCE_URL, self.owner, cluster_name)
        r = self.request("delete", url)
        self.check_and_raise(r)

    def create_machine_type(
        self,
        cluster_name,
        machine_type_name,
        instance_type,
        spot,
        storage_size,
        additional_images,
        min_instances,
        max_instances,
        idle_timeout_minutes,
    ):
        payload = {
            "name": machine_type_name,
            "instance_type": instance_type,
            "is_spot": spot,
            "storage_size": int(storage_size),
            "warm_frameworks": additional_images,
            "min_instances": int(min_instances),
            "max_instances": int(max_instances),
            "idle_timeout_seconds": int(idle_timeout_minutes * 60),
        }
        endpoint = url_path_join(CLUSTER_RESOURCE_URL, self.owner, cluster_name, "supply_config")
        r = self.request("post", endpoint, payload=payload)
        self.check_and_raise(r)

    def scale_machine_type(
        self, cluster_name, machine_type_id, min_instances, max_instances, idle_timeout_minutes,
    ):
        payload = {
            "min_instances": int(min_instances),
            "max_instances": int(max_instances),
            "idle_timeout_seconds": int(idle_timeout_minutes * 60),
        }
        endpoint = url_path_join(
            CLUSTER_RESOURCE_URL,
            self.owner,
            cluster_name,
            "supply_config",
            machine_type_id,
            "edit",
        )
        r = self.request("post", endpoint, payload=payload)
        self.check_and_raise(r)

    def delete_machine_type(self, cluster_name, machine_type_id):
        endpoint = url_path_join(
            CLUSTER_RESOURCE_URL, self.owner, cluster_name, "supply_config", machine_type_id,
        )
        r = self.request("delete", endpoint)
        self.check_and_raise(r)

    def renew_token_machine_type(self, cluster_name, machine_type_id):
        endpoint = url_path_join(
            CLUSTER_RESOURCE_URL,
            self.owner,
            cluster_name,
            "supply_config",
            machine_type_id,
            "new_token",
        )
        r = self.request("post", endpoint)
        self.check_and_raise(r)
        return self.get_json(r)

    def get_serving_groups(self, cluster_name):
        url = url_path_join(CLUSTER_RESOURCE_URL, self.owner, cluster_name, "serving_groups")
        r = self.request("get", url)
        self.check_and_raise(r)
        return self.get_json(r)["serving_groups"]

    def get_serving_group(self, cluster_name, name):
        url = url_path_join(CLUSTER_RESOURCE_URL, self.owner, cluster_name, "serving_groups", name)
        r = self.request("get", url)
        self.check_and_raise(r)
        return self.get_json(r)["serving_group"]
