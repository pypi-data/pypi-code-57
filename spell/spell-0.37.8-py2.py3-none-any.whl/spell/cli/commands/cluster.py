# -*- coding: utf-8 -*-
import click

from spell.cli.log import logger
from spell.cli.commands.cluster_aws import (
    create_aws,
    EKS_DEFAULT_SERVINGGROUP_TYPE,
    eks_init,
    eks_add_nodegroup,
    eks_scale_nodegroup,
    eks_delete_nodegroup,
    eks_delete_cluster,
    add_s3_bucket,
    update_aws_cluster,
    delete_aws_cluster,
)
from spell.cli.commands.cluster_aws import add_ec_registry, delete_ec_registry
from spell.cli.commands.cluster_gcp import (
    create_gcp,
    GKE_DEFAULT_SERVINGGROUP_TYPE,
    gke_init,
    gke_add_nodepool,
    gke_scale_nodepool,
    gke_delete_nodepool,
    gke_delete_cluster,
    add_gs_bucket,
    update_gcp_cluster,
    delete_gcp_cluster,
)
from spell.cli.commands.cluster_gcp import add_gc_registry, delete_gc_registry
from spell.cli.commands.machine_type import (
    add_machine_type,
    scale_machine_type,
    delete_machine_type,
    get_machine_type_token,
)
from spell.cli.utils import (
    require_import,
    require_install,
    cluster_utils,
    prettify_time,
    tabulate_rows,
    HiddenOption,
    command,
)
from spell.cli.exceptions import api_client_exception_handler, ExitException


@click.group(
    name="cluster",
    short_help="Manage external clusters",
    help="Manage external clusters on Spell\n\n"
    "With no subcommand, display all your external clusters",
    invoke_without_command=True,
)
@click.pass_context
def cluster(ctx):
    """
    List all external clusters for current owner
    """
    if ctx.invoked_subcommand:
        return

    spell_client = ctx.obj["client"]
    # TODO(ian) Allow read access to 'member' role
    cluster_utils.validate_org_perms(spell_client, ctx.obj["owner"])
    clusters = spell_client.list_clusters()
    if len(clusters) == 0:
        click.echo("There are no external clusters to display.")
        return

    def create_row(cluster):
        provider = cluster["cloud_provider"]
        networking = cluster["networking"][provider.lower()]
        vpc = networking["vpc_id"] if provider == "AWS" else networking["vpc"]
        return (
            cluster["name"],
            provider,
            cluster["storage_uri"],
            vpc,
            networking["region"],
            cluster["version"],
            cluster["has_kube_config"],
        )

    tabulate_rows(
        [create_row(c) for c in clusters],
        headers=[
            "NAME",
            "PROVIDER",
            "BUCKET NAME",
            "VPC",
            "REGION",
            "CLUSTER VERSION",
            "MODEL SERVING ENABLED",
        ],
    )


@click.command(name="add-bucket", short_help="Adds a cloud storage bucket to SpellFS")
@click.pass_context
@cluster_utils.pass_cluster
@click.option(
    "-p",
    "--profile",
    help="This AWS profile will be used to get your Access Key ID and Secret as well as your Region. "
    "You will be prompted to confirm the Key and Region are correct before continuing. "
    "This key will be used to adjust IAM permissions of the role associated with the cluster "
    "that the bucket is being added to.",
)
@click.option("--bucket", "bucket_name", help="Name of bucket")
@cluster_utils.for_gcp(
    require_import("google.cloud.storage", pkg_extras="cluster-gcp"),
    cluster_utils.gcp_handle_aws_profile_flag,
)
@cluster_utils.for_aws(
    cluster_utils.pass_aws_session(
        perms=[
            "List your buckets to generate an options menu of buckets that can be added to Spell",
            "Add list and read permissions for that bucket to the IAM role associated with the cluster",
        ],
    ),
)
def add_bucket(ctx, cluster, bucket_name, aws_session=None):
    """
    This command adds a cloud storage bucket (S3 or GS) to SpellFS, which enables interaction with the bucket objects
    via ls, cp, and mounts. It will also updates the permissions of that bucket to allow Spell read access to it
    """
    spell_client = ctx.obj["client"]
    cluster_type = cluster["cloud_provider"]
    if cluster_type == "AWS":
        add_s3_bucket(spell_client, aws_session, cluster, bucket_name)
    elif cluster_type == "GCP":
        add_gs_bucket(spell_client, cluster, bucket_name)


@click.command(
    name="add-docker-registry",
    short_help="Configures your cluster to enable runs with docker images in the private registry"
    " hosted by your cloud provider (ECR or GCR respectively)",
)
@click.pass_context
@click.option(
    "--cluster-name", default=None, help="Name of cluster to add registry permissions to",
)
@click.option("--repo", "repo_name", help="Name of repository. ECR only")
@click.option(
    "-p",
    "--profile",
    "profile",
    default="default",
    help="This AWS profile will be used to get your Access Key ID and Secret as well as your Region. "
    "You will be prompted to confirm the Key and Region are correct before continuing. "
    "This key will be used to adjust IAM permissions of the role associated with the cluster "
    "that needs access to the registry.",
)
def add_docker_registry(ctx, cluster_name, repo_name, profile):
    """
    This command enables pulling docker images from a private registry.
    Read permissions to the registry will be added to the IAM role associated with the cluster.
    """
    cluster = cluster_utils.deduce_cluster(ctx, cluster_name)

    cluster_type = cluster["cloud_provider"]
    if cluster_type == "AWS":
        ctx.invoke(add_ec_registry, repo_name=repo_name, cluster=cluster, profile=profile)
    elif cluster_type == "GCP":
        if profile != "default":
            click.echo("--profile is not a valid option for GCP clusters")
            ctx.exit(1)
        ctx.invoke(add_gc_registry, cluster=cluster)
    else:
        raise ExitException("Unknown cluster with provider {}, exiting.".format(cluster_type))


@click.command(
    name="delete-docker-registry",
    short_help="Removes your cluster's access to docker images in the private registry"
    " hosted by your cloud provider (ECR or GCR respectively).",
)
@click.pass_context
@click.option("--repo", "repo_name", help="Name of repository. ECR only")
@click.option(
    "--cluster-name", default=None, help="Name of cluster to remove registry permissions from",
)
@click.option(
    "-p",
    "--profile",
    "profile",
    default="default",
    help="This AWS profile will be used to get your Access Key ID and Secret as well as your Region. "
    "You will be prompted to confirm the Key and Region are correct before continuing. "
    "This key will be used to adjust IAM permissions of the role associated with the cluster "
    "that has access to the registry.",
)
def delete_docker_registry(ctx, cluster_name, repo_name, profile):
    """
    This command removes your cluster's access to docker images in the private registry hosted by your cloud provider.
    """
    cluster = cluster_utils.deduce_cluster(ctx, cluster_name)

    cluster_type = cluster["cloud_provider"]
    if cluster_type == "AWS":
        ctx.invoke(delete_ec_registry, repo_name=repo_name, cluster=cluster, profile=profile)
    elif cluster_type == "GCP":
        if profile != "default":
            click.echo("--profile is not a valid option for GCP clusters")
            ctx.exit(1)
        ctx.invoke(delete_gc_registry, cluster=cluster)
    else:
        raise ExitException("Unknown cluster with provider {}, exiting.".format(cluster_type))


@click.command(
    name="update",
    short_help="Makes sure your Spell cluster is fully up to date and able to support the latest features",
)
@click.pass_context
@click.option("--cluster-name", default=None, help="Name of cluster to update", cls=HiddenOption)
@click.option(
    "-p",
    "--profile",
    "profile",
    default="default",
    help="This AWS profile will be used to get your Access Key ID and Secret as well as your Region. "
    "You will be prompted to confirm the Key and Region are correct before continuing. "
    "This key will be used to adjust IAM permissions of the role associated with the cluster "
    "that the bucket is being added to.",
)
def update(ctx, cluster_name, profile):
    """
    This command makes sure your Spell cluster is fully up to date and able to support the latest features
    """
    cluster = cluster_utils.deduce_cluster(ctx, cluster_name)

    cluster_type = cluster["cloud_provider"]
    if cluster_type == "AWS":
        ctx.invoke(update_aws_cluster, cluster=cluster, profile=profile)
    elif cluster_type == "GCP":
        if profile != "default":
            click.echo("--profile is not a valid option for GCP clusters")
            ctx.exit(1)
        ctx.invoke(update_gcp_cluster, cluster=cluster)
    else:
        raise Exception("Unknown cluster with provider {}, exiting.".format(cluster_type))


@command(
    name="init-model-server",
    short_help="Sets up a GKE/EKS cluster to host model servers",
    help="Sets up a GKE or EKS cluster to host model servers",
)
@click.pass_context
@cluster_utils.pass_cluster
@click.option(
    "-p", "--profile", help="AWS profile to pull credentials from",
)
@click.option(
    "--model-serving-cluster",
    cls=HiddenOption,
    default="spell-model-serving",
    help="Name of the newly created GKE/EKS cluster",
)
@click.option(
    "--auth-api-url",
    cls=HiddenOption,
    type=str,
    help="URL of the spell API server used by Ambassador for authentication. "
    "This must be externally accessible",
)
@click.option(
    "--nodes-min",
    type=int,
    default=1,
    help="Minimum number of nodes in the model serving cluster (default 1)",
)
@click.option(
    "--nodes-max",
    type=int,
    default=2,
    help="Minimum number of nodes in the model serving cluster (default 2)",
)
@click.option(
    "--node-disk-size",
    type=int,
    default=50,
    help="Size of disks on each node in GB (default 50GB)",
)
@click.option(
    "--aws-zones",
    type=str,
    default=None,
    help="Allows AWS clusters to explicitly list the availability zones used for the EKS cluster. "
    "List the desired AZs as comma separated values, ex: 'us-east-1a,us-east-1c,us-east-1d'. "
    "NOTE: Most users will NOT have to do this. This is useful if there are problems with "
    "one or more of the AZs in the region of your cluster.",
)
@cluster_utils.for_aws(
    require_import("kubernetes", pkg_extras="cluster-aws"),
    require_install("eksctl", "kubectl", "aws-iam-authenticator"),
    cluster_utils.pass_aws_session(
        perms=[
            "Leverage eksctl to create an EKS cluster",
            "Leverage eksctl to create an auto scaling group to back the cluster",
        ]
    ),
)
@cluster_utils.for_gcp(
    require_import("kubernetes", "googleapiclient", pkg_extras="cluster-gcp"),
    require_install("gcloud", "kubectl"),
    cluster_utils.pass_gcp_project_creds,
    cluster_utils.gcp_handle_aws_profile_flag,
)
def init_model_server(
    ctx,
    cluster,
    model_serving_cluster,
    auth_api_url,
    nodes_min,
    nodes_max,
    node_disk_size,
    aws_zones,
    aws_session=None,
    gcp_project=None,
    gcp_creds=None,
):
    """
    Deploy a GKE or EKS cluster for model serving
    by auto-detecting the cluster provider.
    """
    spell_client = ctx.obj["client"]
    if cluster["cloud_provider"] == "AWS":
        kubecfg_yaml = eks_init(
            ctx,
            aws_session,
            cluster,
            auth_api_url,
            model_serving_cluster,
            nodes_min,
            nodes_max,
            node_disk_size,
            aws_zones,
        )
    elif cluster["cloud_provider"] == "GCP":
        kubecfg_yaml = gke_init(
            ctx,
            gcp_project,
            gcp_creds,
            cluster,
            auth_api_url,
            model_serving_cluster,
            nodes_min,
            nodes_max,
            node_disk_size,
        )
    else:
        raise ExitException("Unsupported cloud provider: {}".format(cluster["cloud_provider"]))

    cluster_utils.echo_delimiter()
    with api_client_exception_handler():
        click.echo("Generating default serving group config...")
        default_sg_config = {
            "min_nodes": nodes_min,
            "max_nodes": nodes_max,
            "disk_size_gb": node_disk_size,
        }
        if cluster["cloud_provider"] == "AWS":
            default_sg_config["instance_type"] = EKS_DEFAULT_SERVINGGROUP_TYPE
            default_sg_config["name"] = "default"
        if cluster["cloud_provider"] == "GCP":
            default_sg_config["instance_type"] = GKE_DEFAULT_SERVINGGROUP_TYPE
            default_sg_config["name"] = "default-pool"

        click.echo("Uploading config to Spell...")
        status_code = spell_client.register_serving_cluster(
            cluster["name"], kubecfg_yaml, default_sg_config,
        )
        if status_code == 202:
            click.echo(
                "Config successfully uploaded to Spell, "
                "please wait a few minutes for DNS entries to propagate."
            )
        else:
            click.echo("Config successfully uploaded to Spell!")

    cluster_utils.echo_delimiter()
    click.echo("Cluster setup complete!")


@command(
    name="delete-model-server", help="Delete a model-serving cluster", hidden=True,
)
@click.pass_context
@cluster_utils.pass_cluster
@click.option(
    "-p", "--profile", help="AWS profile to pull credentials from",
)
@cluster_utils.for_aws(
    require_install("eksctl"),
    cluster_utils.pass_aws_session(perms=["Leverage eksctl to delete the model serving cluster"]),
)
@cluster_utils.for_gcp(
    require_install("gcloud"), cluster_utils.gcp_handle_aws_profile_flag,
)
def delete_model_server(ctx, cluster, aws_session=None):
    serving_cluster_name = cluster.get("serving_cluster_name")
    if not serving_cluster_name:
        click.echo("No serving cluster found, nothing to do!")
        return

    if cluster["cloud_provider"] == "AWS":
        eks_delete_cluster(aws_session.profile_name, serving_cluster_name)
    if cluster["cloud_provider"] == "GCP":
        project_id = cluster["networking"]["gcp"]["project"]
        gke_delete_cluster(project_id, serving_cluster_name)

    spell_client = ctx.obj["client"]
    with api_client_exception_handler():
        spell_client.deregister_serving_cluster(cluster["name"])
    click.echo("Cluster delete complete!")


@click.group(
    name="serving-group",
    short_help="Manage serving groups",
    help="Manage serving groups used for model serving cluster nodes\n\n"
    "With no subcommand, display all your serving groups",
    invoke_without_command=True,
    # TODO(peter): Un-hide this
    hidden=True,
)
@click.pass_context
@cluster_utils.pass_cluster
def serving_group(ctx, cluster):
    if ctx.invoked_subcommand:
        return
    spell_client = ctx.obj["client"]
    with api_client_exception_handler():
        serving_groups = spell_client.get_serving_groups(cluster["name"])
    if serving_groups:

        def prettify_instance_type(instance_type, accels, is_spot):
            type_str = instance_type or "Custom"
            accels_str = ""
            if accels:
                accel_strs = []
                for accel in accels:
                    accel_type = accel["type"]
                    # GCP accelerator types start with "nvidia-tesla-" so we can trim the prefix
                    if accel_type.startswith("nvidia-tesla-"):
                        accel_type = accel_type[len("nvidia-tesla-") :]
                    accel_strs.append("{}x{}".format(accel_type, accel["count"]))
                accels_str = "+" + ",".join(accel_strs)
            cluster_spot_name = "preemptible" if cluster["cloud_provider"] == "GCP" else "spot"
            spot_str = " ({})".format(cluster_spot_name) if is_spot else ""
            return "{}{}{}".format(type_str, accels_str, spot_str)

        tabulate_rows(
            [
                (
                    sg["name"],
                    prettify_instance_type(sg["instance_type"], sg["accelerators"], sg["is_spot"]),
                    sg["disk_size_gb"],
                    sg["min_nodes"],
                    sg["max_nodes"],
                )
                for sg in serving_groups
            ],
            headers=["NAME", "INSTANCE TYPE", "DISK SIZE", "MIN NODES", "MAX NODES"],
        )
    else:
        click.echo("No serving groups found for cluster {}".format(cluster["name"]))


@click.command(name="add", short_help="Add a new serving group to a Spell model serving cluster")
@click.pass_context
@cluster_utils.pass_cluster
@click.option(
    "-p",
    "--profile",
    help="Specify an AWS profile to pull credentials from to perform the NodeGroup create operation",
)
@click.option(
    "--name", required=True, help="Name of the serving group",
)
@click.option(
    "--instance-type", help="Instance type to use for serving group nodes",
)
@click.option(
    "--accelerator",
    "accelerators",
    multiple=True,
    metavar="NAME[:COUNT]",
    help="(GCP only) Accelerator to attach to nodes, can be specified multiple times for multiple accelerator types",
)
@click.option(
    "--min-nodes", type=int, help="Minimum number of autoscaled nodes in the serving group",
)
@click.option(
    "--max-nodes", type=int, help="Maximum number of autoscaled nodes in the serving group",
)
@click.option(
    "--spot", is_flag=True, default=None, help="Use spot instances for serving group nodes",
)
@click.option(
    "--disk-size", type=int, help="Size of disks on each node in GB",
)
@click.option(
    "--config-file",
    type=click.Path(exists=True, dir_okay=False),
    help="Path to file containing eksctl NodeGroup or GKE node pool spec. Note this is "
    "an advanced option for users who want to specify a custom node group or node pool configuration.",
)
@cluster_utils.for_aws(
    cluster_utils.pass_aws_session(
        perms=["Leverage eksctl to create a new autoscaling group to back the serving group"],
    ),
)
@cluster_utils.for_gcp(
    require_import("googleapiclient.discovery", pkg_extras="cluster-gcp"),
    cluster_utils.pass_gcp_project_creds,
    cluster_utils.gcp_handle_aws_profile_flag,
)
def serving_group_add(
    ctx,
    cluster,
    name,
    instance_type,
    accelerators,
    min_nodes,
    max_nodes,
    spot,
    disk_size,
    config_file,
    aws_session=None,
    gcp_project=None,
    gcp_creds=None,
):
    """
    Deploy a GKE node pool or eksctl node group for model serving
    """
    spell_client = ctx.obj["client"]

    accel_configs = ",".join(accelerators)

    config_contents = None
    if config_file:
        with open(config_file) as f:
            config_contents = f.read()

    cluster_utils.validate_org_perms(spell_client, ctx.obj["owner"])

    if config_contents is None:
        click.echo("Retrieving config...")
        with api_client_exception_handler():
            config = spell_client.generate_serving_group_config(
                cluster["name"],
                name,
                instance_type,
                accel_configs,
                min_nodes,
                max_nodes,
                spot,
                disk_size,
            )

    if cluster["cloud_provider"] == "AWS":
        eks_add_nodegroup(name, config, aws_session.profile_name)
    elif cluster["cloud_provider"] == "GCP":
        gke_add_nodepool(name, config, gcp_creds)
    else:
        raise ExitException("Cluster has invalid provider {}".format(cluster["cloud_provider"]))

    with api_client_exception_handler():
        spell_client.create_serving_group(cluster["name"], name, config)
    click.echo("Successfully created serving group {}!".format(name))


@click.command(
    name="scale", short_help="Adjust minimum and maximium node counts for a given serving group",
)
@click.pass_context
@cluster_utils.pass_cluster
@click.option(
    "-p",
    "--profile",
    help="Specify an AWS profile to pull credentials from to perform the NodeGroup scale operation",
)
@click.option(
    "--min-nodes", type=int, help="Minimum number of autoscaled nodes in the serving group",
)
@click.option(
    "--max-nodes", type=int, help="Maximum number of autoscaled nodes in the serving group",
)
@click.argument("serving_group_name")
@cluster_utils.for_gcp(
    require_import("googleapiclient.discovery", pkg_extras="cluster-gcp"),
    cluster_utils.pass_gcp_project_creds,
    cluster_utils.gcp_handle_aws_profile_flag,
)
@cluster_utils.for_aws(
    require_install("eksctl"),
    cluster_utils.pass_aws_session(
        perms=[
            "Retrieve the EC2 autoscaling group corresponding to the serving group",
            "Adjust the MinSize and MaxSize of the autoscaling group",
        ],
    ),
)
def serving_group_scale(
    ctx,
    cluster,
    serving_group_name,
    min_nodes,
    max_nodes,
    aws_session=None,
    gcp_project=None,
    gcp_creds=None,
):
    """
    Adjust autoscaling min/max nodes for a serving group
    """
    if min_nodes is None and max_nodes is None:
        raise click.UsageError("One of --min-nodes or --max-nodes must be specified")

    spell_client = ctx.obj["client"]
    with api_client_exception_handler():
        serving_group = spell_client.get_serving_group(cluster["name"], serving_group_name)

    if serving_group.is_default and max_nodes is not None and max_nodes < 1:
        raise ExitException(
            'Cannot scale default serving group "{}" to below 1 node'.format(serving_group_name)
        )

    # Special-case scaling GPU serving group types to be manually scaled until GPU HPA
    # is implemented
    is_gpu_type = False
    if cluster["cloud_provider"] == "AWS":
        is_gpu_type = cluster_utils.is_gpu_instance_type(serving_group.instance_type)
    elif cluster["cloud_provider"] == "GCP":
        is_gpu_type = bool(serving_group.accelerators)
    if is_gpu_type:
        msg = "Autoscaling is not yet supported for GPU types."
        if max_nodes:
            msg += " Use the --min-nodes flag exclusively to manually scale the serving group."
            raise click.UsageError(msg)
        if cluster["cloud_provider"] == "GCP" and min_nodes == 0:
            msg += " Max nodes cannot be set to 0, consider deleting the serving group instead."
            msg += " Setting min nodes to 0 and max nodes to 1."
            logger.warning(msg)
            max_nodes = 1
        else:
            msg += " Statically scaling the serving group to {} nodes.".format(min_nodes)
            logger.warning(msg)
            max_nodes = min_nodes

    min_nodes = serving_group.min_nodes if min_nodes is None else min_nodes
    max_nodes = serving_group.max_nodes if max_nodes is None else max_nodes
    if cluster["cloud_provider"] == "AWS":
        eks_scale_nodegroup(aws_session, serving_group_name, min_nodes, max_nodes)
    elif cluster["cloud_provider"] == "GCP":
        gke_scale_nodepool(gcp_creds, serving_group, min_nodes, max_nodes)
    else:
        raise ExitException("Cluster has invalid provider {}".format(cluster["cloud_provider"]))

    with api_client_exception_handler():
        spell_client.scale_serving_group(cluster["name"], serving_group_name, min_nodes, max_nodes)
    click.echo("Successfully scaled serving group {}!".format(serving_group_name))


@click.command(
    name="delete", short_help="Delete a serving group",
)
@click.pass_context
@cluster_utils.pass_cluster
@click.option(
    "-p", "--profile", help="AWS profile to pull credentials from",
)
@click.argument("serving_group_name")
@cluster_utils.for_aws(
    require_install("eksctl"),
    cluster_utils.pass_aws_session(
        perms=["Leverage eksctl to delete the autoscaling group backing the serving group"],
    ),
)
@cluster_utils.for_gcp(
    require_import("googleapiclient.discovery", pkg_extras="cluster-gcp"),
    cluster_utils.pass_gcp_project_creds,
    cluster_utils.gcp_handle_aws_profile_flag,
)
def serving_group_delete(
    ctx, cluster, serving_group_name, aws_session=None, gcp_project=None, gcp_creds=None,
):
    """
    Delete a serving group
    """
    spell_client = ctx.obj["client"]

    cluster_utils.validate_org_perms(spell_client, ctx.obj["owner"])

    with api_client_exception_handler():
        serving_group = spell_client.get_serving_group(cluster["name"], serving_group_name)

    if serving_group.is_default:
        raise ExitException(
            'Cannot delete cluster default serving group "{}"'.format(serving_group_name)
        )

    if cluster["cloud_provider"] == "AWS":
        eks_delete_nodegroup(aws_session.profile_name, serving_group)
    elif cluster["cloud_provider"] == "GCP":
        gke_delete_nodepool(gcp_creds, serving_group)
    else:
        raise ExitException("Cluster has invalid provider {}".format(cluster["cloud_provider"]))

    with api_client_exception_handler():
        spell_client.delete_serving_group(cluster["name"], serving_group_name)
    click.echo("Successfully deleted serving group {}!".format(serving_group_name)),


@click.command(
    name="delete",
    short_help="Deletes a given cluster",
    help="Facilitates the deletion of your Spell cluster by removing the associated "
    "infrastructure on Spell as well as deleting all associated cloud resources. "
    "It will OPTIONALLY delete the data in your output bucket - including run outputs.",
)
@click.pass_context
@click.option(
    "-c",
    "--cluster",
    "cluster_name",
    type=str,
    help="The name of the Spell cluster that you would like to delete. "
    "If it's not specified, it will default to the ONE cluster the current owner has, "
    "or prompt if the current owner has more than one cluster.",
    cls=HiddenOption,
)
@click.option(
    "-p",
    "--profile",
    "profile",
    help="This AWS profile will be used to get your Access Key ID and Secret as well as your Region. "
    "You will be prompted to confirm the Key and Region are correct before continuing. "
    "This key will be used to destroy the VPC, IAM Roles, and optionally the S3 bucket "
    "created for the cluster.",
)
# If this cluster was constructed in an existing VPC (likely in on-prem mode) this option will prevent
# the vpc from being deleted
@click.option("--keep-vpc", "keep_vpc", is_flag=True, hidden=True)
def delete(ctx, cluster_name, profile, keep_vpc):
    cluster = cluster_utils.deduce_cluster(ctx, cluster_name)
    if cluster is None:
        return

    cluster_type = cluster["cloud_provider"]
    if cluster_type == "AWS":
        delete_aws_cluster(ctx, cluster, profile, keep_vpc)
    elif cluster_type == "GCP":
        if keep_vpc:
            click.echo("--keep-vpc is not currently supported for GCP. Contact Spell for support.")
        if profile:
            click.echo("--profile is not a valid option for GCP clusters")
            ctx.exit(1)
        delete_gcp_cluster(ctx, cluster)
    else:
        raise Exception("Unknown cluster with provider {}, exiting.".format(cluster_type))


@cluster.group(
    name="init",
    short_help="Create a cluster",
    help="Create a new aws/gcp cluster for your org account\n\n"
    "Set up a cluster to use machines in your own AWS/GCP account",
)
@click.pass_context
def init(ctx):
    pass


@cluster.group(
    name="machine-type",
    short_help="Manage machine types",
    help="Manage groups of similar machines which can be used for training runs and workspaces on Spell\n\n"
    "With no subcommand, display all your machine types",
    invoke_without_command=True,
)
@click.option(
    "-c",
    "--cluster",
    "cluster_name",
    type=str,
    help="The name of the Spell cluster",
    cls=HiddenOption,
)
@click.pass_context
def machine_type(ctx, cluster_name):
    # TODO(ian) Allow read access to 'member' role
    ctx.obj["cluster"] = cluster_utils.deduce_cluster(ctx, cluster_name)
    if ctx.invoked_subcommand:
        return

    def create_row(machine_type):
        machines = machine_type["machines"]
        return (
            machine_type["name"],
            machine_type["spell_type"],
            machine_type["is_spot"],
            machine_type["instance_spec"].get("storage_size"),
            ", ".join(machine_type["warm_frameworks"]),
            prettify_time(machine_type["created_at"]),
            prettify_time(machine_type["updated_at"]),
            machine_type["min_instances"],
            machine_type["max_instances"],
            machine_type["idle_timeout_seconds"] / 60,
            len([m for m in machines if m["status"] == "Starting"]),
            len([m for m in machines if m["status"] == "Idle"]),
            len([m for m in machines if m["status"] == "In use"]),
        )

    machine_types = ctx.obj["cluster"]["machine_types"]
    tabulate_rows(
        [create_row(mt) for mt in machine_types],
        headers=[
            "NAME",
            "TYPE",
            "SPOT",
            "DISK SIZE",
            "IMAGES",
            "CREATED",
            "LAST MODIFIED",
            "MIN",
            "MAX",
            "IDLE TIMEOUT",
            "STARTING",
            "IDLE",
            "IN USE",
        ],
    )


# register generic subcommands
cluster.add_command(add_bucket)
cluster.add_command(add_docker_registry)
cluster.add_command(delete_docker_registry)
cluster.add_command(update)
cluster.add_command(delete)

# register init subcommands
init.add_command(create_aws)
init.add_command(create_gcp)

# register model serving subcommands
cluster.add_command(init_model_server)
cluster.add_command(delete_model_server)
cluster.add_command(serving_group)
serving_group.add_command(serving_group_add)
serving_group.add_command(serving_group_scale)
serving_group.add_command(serving_group_delete)

# register machine-type subcommands
machine_type.add_command(add_machine_type)
machine_type.add_command(scale_machine_type)
machine_type.add_command(delete_machine_type)
machine_type.add_command(get_machine_type_token)
