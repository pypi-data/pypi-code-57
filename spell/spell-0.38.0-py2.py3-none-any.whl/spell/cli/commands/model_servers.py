import click
import re
import yaml
import os

from spell.cli.exceptions import (
    api_client_exception_handler,
    ExitException,
    SPELL_INVALID_CONFIG,
)
from spell.cli.utils import (
    group,
    HiddenOption,
    tabulate_rows,
    convert_to_local_time,
    with_emoji,
    git_utils,
    ellipses,
    parse_utils,
    prettify_time,
)
from spell.cli.log import logger
from spell.cli.utils.command_options import (
    dependency_params,
    workspace_spec_params,
    cli_params,
    description_param,
    mount_params,
)
from spell.cli.utils.parse_utils import validate_attached_resources
from spell.client.utils import (
    get_conda_contents,
    get_requirements_file,
    format_pip_apt_versions,
)
from spell.api.models import (
    ContainerResourceRequirements,
    PodAutoscaleConfig,
    ResourceRequirement,
    SpellModelServerRequest,
    Environment,
)


@group(
    name="model-servers",
    short_help="Manage model servers",
    help="""Manage model servers

             With no subcommand, displays all of your model servers""",
    invoke_without_command=True,
)
@click.option(
    "--raw", help="display output in raw format", is_flag=True, default=False, cls=HiddenOption
)
@click.pass_context
def model_servers(ctx, raw):
    if not ctx.invoked_subcommand:
        client = ctx.obj["client"]
        with api_client_exception_handler():
            model_servers = client.get_model_servers()
        if len(model_servers) == 0:
            click.echo("There are no model servers to display.")
        else:
            data = [
                (
                    ms.get_specifier(),
                    ms.url,
                    "{}/{}".format(len([p for p in ms.pods if p.ready_at]), len(ms.pods)),
                    ms.get_age(),
                )
                for ms in model_servers
            ]
            tabulate_rows(data, headers=["NAME", "URL", "PODS (READY/TOTAL)", "AGE"], raw=raw)


@model_servers.command(
    name="create",
    short_help="Create a new model server",
    help="""Create a new Tensorflow model server with the specified NAME from
                       resources stored at PATH. NAME should be fully qualified, following the
                       format: <model_name>:<tag>""",
)
@click.pass_context
@click.argument("name")
@click.argument("path")
@click.option(
    "--type",
    "-t",
    type=click.Choice(["tensorflow", "pytorch"]),
    help="""Please see the documentation located at https://spell.ml/docs/model_servers
                   to correctly structure your model for the various supported types.""",
)
@click.option(
    "--cluster-name", type=str, help="Name of the cluster where the model server will be created"
)
def create(ctx, name, path, type, cluster_name):
    server_name, tag = get_name_and_tag(name)
    client = ctx.obj["client"]
    with api_client_exception_handler():
        model_server = client.new_model_server(
            server_name=server_name, tag=tag, path=path, type=type, cluster_name=cluster_name
        )
    click.echo("Successfully created model server: {}".format(model_server.get_specifier()))


@model_servers.command(
    name="serve",
    short_help="Create a new model server using a model",
    hidden=True,
    help="""Create a new model server based on an existing model and entrypoint
            to a Python class able to serve said model.""",
)
@click.argument("model")
@click.argument("entrypoint")
@click.option("--name", type=str, help="Name of the model server. Defaults to the model name.")
@click.option(
    "--serving-group",
    help="Serving group to schedule the server to. Defaults to initial serving group.",
)
@dependency_params(include_docker=False)
@workspace_spec_params
@description_param
@cli_params
@mount_params
@click.option(
    "--min-pods",
    type=int,
    default=1,
    help="The autoscaler will never scale to fewer pods than this.",
)
@click.option(
    "--max-pods",
    type=int,
    default=5,
    help="The autoscaler will never scale to more pods than this.",
)
@click.option(
    "--target-cpu-utilization",
    default=0.8,
    type=float,
    help="If average pod CPU usage goes higher than this times the cpu-request the autoscaler "
    "will spin up a new pod.",
)
@click.option(
    "--cpu-request",
    type=float,
    default=0.9,
    help="The amount of vCPU cores you expect each pod to use",
)
@click.option("--cpu-limit", type=float, help="The maximum amount of vCPU cores a pod can use")
@click.option(
    "--ram-request", type=int, help="The amount of RAM you expect each pod to use in MB",
)
@click.option(
    "--ram-limit",
    type=int,
    help="The maximum amount of RAM a pod can use in MB. It will be terminated if it exceeds this.",
)
@click.pass_context
def serve(
    ctx,
    model,
    entrypoint,
    name,
    serving_group,
    github_url,
    github_ref,
    pip_packages,
    requirements_file,
    apt_packages,
    commit_ref,
    description,
    envvars,
    force,
    verbose,
    conda_file,
    raw_resources,
    min_pods,
    max_pods,
    target_cpu_utilization,
    cpu_request,
    cpu_limit,
    ram_request,
    ram_limit,
    **kwargs
):
    model_name, tag = get_name_and_tag(model)
    if tag is None:
        raise ExitException("A model tag must be specified in the form model_name:version")
    model_version_id, model_version_name = parse_tag(tag)
    if name is None:
        name = model_name

    server_req = create_modelserver_request(
        ctx,
        model_name,
        model_version_id,
        model_version_name,
        entrypoint,
        name,
        serving_group,
        pip_packages,
        requirements_file,
        apt_packages,
        commit_ref,
        description,
        envvars,
        force,
        verbose,
        github_url,
        github_ref,
        conda_file,
        raw_resources,
        min_pods,
        max_pods,
        target_cpu_utilization,
        cpu_request,
        cpu_limit,
        ram_request,
        ram_limit,
        **kwargs
    )
    client = ctx.obj["client"]
    logger.info("sending model server request to api")
    with api_client_exception_handler():
        server = client.new_custom_model_server(server_req)

    utf8 = ctx.obj["utf8"]
    server_name = server.server_name
    if server.tag != "":
        server_name = server_name + ":" + server.tag
    click.echo(with_emoji(u"💫", "Starting server {}".format(server_name), utf8) + ellipses(utf8))


def create_modelserver_request(
    ctx,
    model_name,
    model_version_id,
    model_version_name,
    entrypoint,
    name,
    serving_group,
    pip_packages,
    requirements_file,
    apt_packages,
    commit_ref,
    description,
    envvars,
    force,
    verbose,
    github_url,
    github_ref,
    conda_file,
    raw_resources,
    min_pods,
    max_pods,
    target_cpu_utilization,
    cpu_request,
    cpu_limit,
    ram_request,
    ram_limit,
    **kwargs
):

    repo = git_utils.detect_repo(
        ctx,
        github_url=github_url,
        github_ref=github_ref,
        force=force,
        description=description,
        commit_ref=commit_ref,
        allow_missing=False,
        resource_type="model server",
    )

    if github_url is None:
        if not os.path.isfile(entrypoint):
            raise ExitException(
                "ENTRYPOINT {} file not found.".format(entrypoint), SPELL_INVALID_CONFIG
            )
        entrypoint = git_utils.get_tracked_repo_path(repo, entrypoint)
        if entrypoint is None:
            raise ExitException(
                "ENTRYPOINT must be a path within the repository.", SPELL_INVALID_CONFIG,
            )

    # TODO(ian) remove when we support custom docker images
    docker_image = None
    if docker_image is not None and (pip_packages or apt_packages or requirements_file):
        raise ExitException(
            "--apt, --pip, or --pip-req cannot be specified when --from is provided."
            " Please install packages in the specified Dockerfile.",
            SPELL_INVALID_CONFIG,
        )

    conda_file = get_conda_contents(conda_file)

    # grab pip packages from requirements file
    pip_packages = list(pip_packages)
    pip_packages.extend(get_requirements_file(requirements_file))

    # extract envvars into a dictionary
    curr_envvars = parse_utils.parse_env_vars(envvars)
    pip, apt = format_pip_apt_versions(pip_packages, apt_packages)
    environment = Environment(
        pip=pip, apt=apt, docker_image=docker_image, env_vars=curr_envvars, conda_file=conda_file,
    )

    attached_resources = validate_attached_resources(raw_resources)

    pod_autoscale_config = PodAutoscaleConfig(min_pods=min_pods, max_pods=max_pods)
    if target_cpu_utilization is not None:
        pod_autoscale_config.target_cpu_utilization = int(target_cpu_utilization * 100)

    resource_request = ResourceRequirement(memory_mebibytes=ram_request)
    if cpu_request is not None:
        resource_request.cpu_millicores = int(cpu_request * 1000)
    resource_limit = ResourceRequirement(memory_mebibytes=ram_limit)
    if cpu_limit is not None:
        resource_limit.cpu_millicores = int(cpu_limit * 1000)
    resource_requirements = ContainerResourceRequirements(
        resource_request=resource_request, resource_limit=resource_limit,
    )

    return SpellModelServerRequest(
        model_name=model_name,
        model_version_id=model_version_id,
        model_version_name=model_version_name,
        server_name=name,
        serving_group=serving_group,
        entrypoint=entrypoint,
        environment=environment,
        attached_resources=attached_resources,
        description=description,
        repository=repo,
        pod_autoscale_config=pod_autoscale_config,
        resource_requirements=resource_requirements,
    )


@model_servers.command(
    name="rm",
    short_help="Remove a model server",
    help="""Remove the model server with the specified NAME""",
)
@click.pass_context
@click.argument("name")
def remove(ctx, name):
    server_name, tag = get_name_and_tag(name)
    client = ctx.obj["client"]
    with api_client_exception_handler():
        client.delete_model_server(server_name=server_name, tag=tag)
    click.echo("Successfully removed model server {}".format(name))


@model_servers.command(
    name="start",
    short_help="Start a model server",
    help="""Start the model server with the specified NAME""",
)
@click.pass_context
@click.argument("name")
def start(ctx, name):
    server_name, tag = get_name_and_tag(name)
    client = ctx.obj["client"]
    with api_client_exception_handler():
        client.start_model_server(server_name=server_name, tag=tag)
    click.echo("Successfully started model server {}".format(name))


@model_servers.command(
    name="stop",
    short_help="Stop a model server",
    help="""Stop the model server with the specified NAME""",
)
@click.pass_context
@click.argument("name")
def stop(ctx, name):
    server_name, tag = get_name_and_tag(name)
    client = ctx.obj["client"]
    with api_client_exception_handler():
        client.stop_model_server(server_name=server_name, tag=tag)
    click.echo("Successfully stopped model server {}".format(name))


@model_servers.command(
    name="update",
    short_help="Update a model server with new configuration",
    help="""Update the model server with the specified NAME to have a new configuration""",
)
@click.pass_context
@click.argument("name")
@click.argument("path")
def update(ctx, name, path):
    server_name, tag = get_name_and_tag(name)
    client = ctx.obj["client"]
    with api_client_exception_handler():
        client.update_model_server(server_name=server_name, tag=tag, path=path)
    click.echo(
        "Successfully updated model server {}. Starting rolling updates to servers...".format(name)
    )


# Doc: https://docs.google.com/document/d/1DgLLe8zOz5Omdb9YETKW1w0oWmTNoMZbQGD-NG7B2uo
@model_servers.command(
    name="apply",
    short_help="Update model servers based on a user-specified YAML file",
    help="\b\nCreate/update/delete multiple model servers with a YAML file"
    "\b\nProperties:"
    "\b\n   specifier   REQUIRED (ex: image_classifier:v1)"
    "\b\n   path        REQUIRED (ex: runs/8/mymodel.pt)"
    "\b\n   type        OPTIONAL "
    "(ex: tensorflow OR pytorch. Use auto-detected type if not specified)"
    "\b\n   owner       OPTIONAL "
    "(Uses this value if specified, if not then cmd line argument is used if specified,"
    " and finally current active spell owner is used as a default if neither is specified)"
    "\b\n   clusterName OPTIONAL "
    "(Uses this value if specified, if not then cmd line argument is used if specified."
    " If neither is specified, the spell owner should have exactly ONE cluster,"
    " which will be used as default)",
)
@click.pass_context
@click.argument("path", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--delete",
    "-d",
    is_flag=True,
    help="Delete any currently existing model servers in this cluster "
    "that are missing from the YAML file",
)
@click.option(
    "--owner",
    type=str,
    help="Default owner for model servers unspecified in the YAML file. "
    "Only use if you would like to specify an alternative owner to the currently active one.",
)
@click.option(
    "--cluster-name",
    type=str,
    help="""Default cluster name for model servers unspecified in the YAML file""",
)
def apply(ctx, path, delete, owner, cluster_name):
    required_props = ["specifier", "path"]
    # Get current model server list
    client = ctx.obj["client"]
    model_servers = client.get_model_servers()
    # Store specifier-path pairs in a map
    model_server_map = dict()  # Key: specifier; Value: path
    for ms in model_servers:
        model_server_map[ms.get_specifier()] = ms.resource_path
    # Read configurations from yaml file
    config_specifier_set = set()
    with open(path, "r") as stream:
        try:
            configs = yaml.safe_load_all(stream)
            for config in configs:
                # Check if the configuration contains required props
                for prop in required_props:
                    if prop not in config:
                        raise ExitException(
                            "'{}' is required. Please double check your YAML file.".format(prop)
                        )
                # Store all specifiers from the configurations
                config_specifier_set.add(config["specifier"])
                # Compare configurations in yaml file with current model server list
                if config["specifier"] in model_server_map:
                    # Update model servers whose path is different from as defined in YAML file
                    if config["path"] != model_server_map[config["specifier"]]:
                        server_name, tag, owner_new, _ = getConfigInfo(config, owner, cluster_name)
                        with api_client_exception_handler():
                            client.update_model_server(
                                server_name=server_name,
                                tag=tag,
                                path=config["path"],
                                owner=owner_new,
                            )
                        click.echo(
                            "Successfully updated model server {}. "
                            "Starting rolling updates to servers...".format(config["specifier"])
                        )
                else:
                    # Create new model server
                    server_name, tag, owner_new, cluster_name_new = getConfigInfo(
                        config, owner, cluster_name
                    )
                    with api_client_exception_handler():
                        client.new_model_server(
                            server_name=server_name,
                            tag=tag,
                            path=config["path"],
                            type=config["type"] if "type" in config else None,
                            cluster_name=cluster_name_new,
                            owner=owner_new,
                        )
                    click.echo("Successfully created model server: {}".format(config["specifier"]))
        except yaml.YAMLError as exc:
            raise ExitException(
                "Your YAML file contains invalid syntax! Please fix and try again: {}".format(exc)
            )
    # Delete model servers not listed in the yaml file
    if delete:
        for specifier in model_server_map.keys():
            if specifier in config_specifier_set:
                continue
            server_name, tag = get_name_and_tag(specifier)
            with api_client_exception_handler():
                client.delete_model_server(server_name=server_name, tag=tag)
            click.echo("Successfully removed model server {}".format(specifier))


@model_servers.command(
    name="info",
    short_help="Get info about a model server",
    help="""Get info about the model server with the specified NAME""",
)
@click.pass_context
@click.argument("name")
def get(ctx, name):
    server_name, tag = get_name_and_tag(name)
    client = ctx.obj["client"]
    with api_client_exception_handler():
        ms = client.get_model_server(server_name=server_name, tag=tag)
    lines = [("Server Name", ms.server_name)]
    if ms.tag:
        lines.append(("Server Tag", ms.tag))
    lines.append(("Type", ms.type))
    if ms.model_version:
        lines.extend(get_custom_model_server_info_lines(ms))
    else:
        lines.append(("Resource", ms.resource_path))
    lines.append(("Date Created", convert_to_local_time(ms.created_at)))
    lines.append(
        (
            "Pods (Ready/Total)",
            "{}/{}".format(len([p for p in ms.pods if p.ready_at]), len(ms.pods)),
        )
    )
    lines.append(("Time Running", ms.get_age()))
    lines.append(("URL", ms.url))
    if ms.cluster:
        lines.append(("*NOTE*", "This will only be accessible within the same VPC of the cluster"))
    else:
        lines.append(("Access Token", ms.access_token))

    tabulate_rows(lines)


def get_custom_model_server_info_lines(ms):
    lines = []
    specifier = ms.model_version.specifier
    if specifier:
        lines.append(("Model", specifier))
    lines.append(("Resource", ms.model_version.resource))
    if ms.workspace:
        lines.append(("Repository", ms.workspace.name))
    if ms.github_url:
        lines.append(("GitHub URL", ms.github_url))
    if ms.entrypoint:
        lines.append(("Entrypoint", ms.entrypoint))
    if ms.git_commit_hash:
        formatted_hash = ms.git_commit_hash
        if ms.has_uncommitted:
            formatted_hash += "[Uncommitted]"
        lines.append(("GitCommitHash", formatted_hash))
    if ms.request_limits:
        memory = ms.request_limits.memory_mebibytes
        cpu = ms.request_limits.cpu_millicores
        if memory:
            if memory.request:
                lines.append(("Memory Request", "{} MiB".format(memory.request)))
            if memory.limit:
                lines.append(("Memory Limit", "{} MiB".format(memory.limit)))
        if cpu:
            if cpu.request:
                lines.append(("CPU Request", "{}m".format(cpu.request)))
            if cpu.limit:
                lines.append(("CPU Limit", "{}m".format(cpu.limit)))
    return lines


@model_servers.command(name="status", help="Get the status of all pods for this server.")
@click.pass_context
@click.argument("name")
def status(ctx, name):
    server_name, tag = get_name_and_tag(name)
    with api_client_exception_handler():
        ms = ctx.obj["client"].get_model_server(server_name=server_name, tag=tag)
    print_pod_statuses(ms)


def print_pod_statuses(model_server):
    rows = []
    for p in model_server.pods:
        ready_at = prettify_time(p.ready_at) if p.ready_at else "-"
        rows.append([p.id, prettify_time(p.created_at), ready_at])
    tabulate_rows(rows, headers=["POD ID", "CREATED AT", "READY AT"])


@model_servers.command(
    name="renew-token",
    short_help="Renews the access token for model server",
    help="""Renews the access token for model server with the specified NAME""",
)
@click.pass_context
@click.argument("name")
def renew_token(ctx, name):
    server_name, tag = get_name_and_tag(name)
    client = ctx.obj["client"]
    with api_client_exception_handler():
        ms = client.renew_model_server_token(server_name=server_name, tag=tag)
    click.echo("New access token: {}".format(ms.access_token))


@model_servers.command(
    name="logs",
    short_help="Get logs from a model server",
    help="""Get logs for the model server with the specified NAME""",
)
@click.pass_context
@click.option("-f", "--follow", is_flag=True, help="Follow log output")
@click.option(
    "-p", "--pod", help="The ID of the pod you would like logs for. Omit to get a list of all pods."
)
@click.argument("name")
def logs(ctx, name, pod, follow):
    server_name, tag = get_name_and_tag(name)
    client = ctx.obj["client"]

    # Prompt with all pods so user can select one
    if not pod:
        with api_client_exception_handler():
            ms = client.get_model_server(server_name=server_name, tag=tag)
        print_pod_statuses(ms)
        pod_ids = [str(pod.id) for pod in ms.pods]
        pod = click.prompt(
            "Enter the ID of the pod you would like logs for", type=click.Choice(pod_ids)
        )

    utf8 = ctx.obj["utf8"]
    with api_client_exception_handler():
        try:
            for entry in client.get_model_server_log_entries(server_name, tag, pod, follow=follow):
                click.echo(entry.log)
        except KeyboardInterrupt:
            if follow:
                click.echo()
                click.echo(
                    with_emoji(
                        u"✨",
                        "Use 'spell model-servers logs -f {}' to view logs again".format(name),
                        utf8,
                    )
                )


def parse_tag(tag):
    # returns a tuple of (version, name), where one is None
    if not tag.startswith("v"):
        return None, tag
    version_string = tag[1:]
    if version_string.isnumeric():
        return int(version_string), None
    return None, tag


def get_name_and_tag(specifier):
    name, _, tag = specifier.partition(":")
    if tag and not is_valid_specifier_part(tag):
        raise ExitException("Invalid tag {}".format(specifier))
    if not is_valid_specifier_part(name):
        raise ExitException("Invalid name {}".format(specifier))
    return (name, tag if tag != "" else None)


def is_valid_specifier_part(part):
    return re.match(r"^\w+[\w\.-]*", part)


def getConfigInfo(config, owner, cluster_name):
    server_name, tag = get_name_and_tag(config["specifier"])
    owner = owner if "owner" not in config else config["owner"]
    cluster_name = cluster_name if "clusterName" not in config else config["clusterName"]
    return server_name, tag, owner, cluster_name
