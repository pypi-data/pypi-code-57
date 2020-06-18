from functools import wraps
import click
import subprocess
import sys
import tempfile
import time

from spell.api.exceptions import BadRequest
from spell.cli.exceptions import (
    api_client_exception_handler,
    ExitException,
)
from spell.cli.utils import HiddenOption, require_import
from spell.cli.utils.kube_cluster_templates import cluster_statsd_sink_yaml


def get_for_cloud_provider_decorator(cloud_provider):
    def for_cloud_provider(*decorators):
        def for_cloud_provider_wrapper(f):
            @wraps(f)
            def wrapped(*args, cluster=None, **kwargs):
                if cluster is None:
                    raise ExitException(
                        "No cluster defined in for_cloud_provider decorator on {0}! Make sure "
                        "{0} is also decorated with pass_cluster".format(f.__name__)
                    )
                maybe_decorated = f
                if cluster["cloud_provider"] == cloud_provider:
                    for decorator in decorators:
                        maybe_decorated = decorator(maybe_decorated)
                maybe_decorated(*args, cluster=cluster, **kwargs)

            return wrapped

        return for_cloud_provider_wrapper

    return for_cloud_provider


"""
Decorator that conditionally applies the decorators passed into it if the
cluster passed into the command is an AWS cluster

NOTE: Must be used in tandem with the pass_cluster decorator
"""
for_aws = get_for_cloud_provider_decorator("AWS")

"""
Decorator that conditionally applies the decorators passed into it if the
cluster passed into the command is a GCP cluster

NOTE: Must be used in tandem with the pass_cluster decorator
"""
for_gcp = get_for_cloud_provider_decorator("GCP")


def deduce_cluster(ctx, cluster_name):
    spell_client = ctx.obj["client"]
    validate_org_perms(spell_client, ctx.obj["owner"])

    with api_client_exception_handler():
        clusters = spell_client.list_clusters()
    if len(clusters) == 0:
        raise ExitException(
            "No clusters defined, please run `spell cluster init aws` or `spell cluster init gcp`"
        )

    if cluster_name is not None:
        clusters = [c for c in clusters if c["name"] == cluster_name]
        if len(clusters) == 0:
            raise ExitException("No clusters with the name {}.".format(cluster_name))
        elif len(clusters) > 1:
            # This should never happen
            raise ExitException("More than one cluster with the name {}.".format(cluster_name))

    if len(clusters) == 1:
        return clusters[0]

    cluster_names = [c["name"] for c in clusters]
    cluster_name = click.prompt(
        "You have multiple clusters defined. Please select one.", type=click.Choice(cluster_names),
    ).strip()
    for c in clusters:
        if c["name"] == cluster_name:
            return c
    # This should never happen
    raise ExitException("No clusters with the name {}.".format(cluster_name))


def pass_cluster(f):
    """
    Decorator that deduces the org's cluster and passes it into the command
    """

    @click.option("--cluster-name", cls=HiddenOption)
    @wraps(f)
    def wrapped(ctx, *args, cluster_name=None, **kwargs):
        cluster = deduce_cluster(ctx, cluster_name)
        provider = cluster["cloud_provider"]
        if provider not in ("AWS", "GCP"):
            raise ExitException("Cluster with unknown cloud provider {}".format(provider))
        f(ctx=ctx, *args, cluster=cluster, **kwargs)

    return wrapped


def pass_gcp_project_creds(f):
    """
    Decorator that attempts to grab gcloud project and credentials and passes
    them into the command
    """

    @wraps(f)
    @require_import("google.auth", pkg_extras="cluster-gcp")
    def wrapped(*args, **kwargs):
        import google.auth

        try:
            credentials, project = google.auth.default()
        except google.auth.exceptions.DefaultCredentialsError:
            raise ExitException(
                "No gcloud credentials found! Please run `gcloud auth application-default login` "
                "then rerun this command."
            )
        f(*args, gcp_project=project, gcp_creds=credentials, **kwargs)

    return wrapped


def gcp_handle_aws_profile_flag(f):
    """
    Decorator that handles the --profile flag in GCP by swallowing the kwarg
    and raising an error if it has a value
    """

    @wraps(f)
    def wrapped(*args, profile=None, **kwargs):
        if profile is not None:
            raise ExitException("Flag --profile is not a valid option for GCP clusters")
        f(*args, **kwargs)

    return wrapped


def pass_aws_session(perms=[]):
    """
    Decorator that creates and passes a boto session into the command
    queries for a user confirmation after printing permissions info
    """

    def pass_aws_session_wrapper(f):
        @wraps(f)
        @require_import("boto3", "botocore", pkg_extras="cluster-aws")
        def wrapped(*args, profile=None, **kwargs):
            import boto3
            import botocore

            profile = profile or "default"
            try:
                session = boto3.session.Session(profile_name=profile)
            except botocore.exceptions.BotoCoreError as e:
                raise ExitException("Failed to set profile {} with error: {}".format(profile, e))
            if perms:
                perms_msg = "This command will\n"
                perms_msg += "\n".join("    - {}".format(perm) for perm in perms)
                click.echo(perms_msg)
            confirmed = click.confirm(
                "This command will proceed using AWS profile '{}' which has "
                "Access Key ID '{}' in region '{}' - continue?".format(
                    profile, session.get_credentials().access_key, session.region_name,
                )
            )
            if not confirmed:
                sys.exit(1)
            f(*args, aws_session=session, **kwargs)

        return wrapped

    return pass_aws_session_wrapper


def echo_delimiter():
    click.echo("---------------------------------------------")


def validate_org_perms(spell_client, owner):
    with api_client_exception_handler():
        owner_details = spell_client.get_owner_details()
        if owner_details.type != "organization":
            raise ExitException(
                "Only organizations can use cluster features, use `spell owner` "
                "to switch current owner to an organization "
            )
        if owner_details.requestor_role not in ("admin", "manager"):
            raise ExitException(
                "You must be a Manager or Admin with current org {} to proceed".format(owner)
            )


def create_serving_namespace(kconfig, kclient):
    echo_delimiter()
    click.echo("Creating 'serving' namespace...")
    try:
        kconfig.load_kube_config()
        kube_api = kclient.CoreV1Api()
        if any(i.metadata.name == "serving" for i in kube_api.list_namespace().items):
            click.echo("'serving' namespace already exists!")
        else:
            kube_api.create_namespace(
                kclient.V1Namespace(metadata=kclient.V1ObjectMeta(name="serving"))
            )
            click.echo("'serving' namespace created!")
        subprocess.check_call(
            ("kubectl", "config", "set-context", "--current", "--namespace=serving")
        )
    except Exception as e:
        raise ExitException("ERROR: Creating 'serving' namespace failed. Error was: {}".format(e))


def add_statsd():
    echo_delimiter()
    click.echo("Setting up StatsD...")
    try:
        with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w+") as f:
            f.write(cluster_statsd_sink_yaml)
            f.flush()
            subprocess.check_call(
                ("kubectl", "apply", "--namespace", "serving", "--filename", f.name)
            )
        click.echo("StatsD set up!")
    except Exception as e:
        click.echo("ERROR: Setting up StatsD failed. Error was: {}".format(e), err=True)


def block_until_cluster_drained(spell_client, cluster_name):
    """
    Block until cluster is drained. This is necessary because the API will fail to
    drain if we delete the IAM role before the machine types are marked as drained
    """
    num_retries = 10
    for i in range(num_retries):
        try:
            spell_client.is_cluster_drained(cluster_name)
            click.echo("Cluster is drained!")
            return
        except BadRequest:
            # Don't sleep on the last iteration
            if i < num_retries - 1:
                click.echo(
                    "Cluster is still draining all machine types. "
                    "This can take a long time! Retrying in 30s..."
                )
                time.sleep(30)
    raise ExitException(
        "Timed out waiting for Spell to drain the cluster. Please try again "
        "or contact Spell if the problem persists."
    )


# List sourced from this table: https://aws.amazon.com/ec2/instance-types/#Accelerated_Computing
def is_gpu_instance_type(instance_type):
    gpu_prefixes = ("p3.", "p3dn.", "p2.", "inf1.", "g4dn.", "g3s.", "g3.", "f1.")
    return any(instance_type.startswith(prefix) for prefix in gpu_prefixes)
