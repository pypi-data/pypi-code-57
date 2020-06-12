# -*- coding: utf-8 -*-
from difflib import get_close_matches

import click

from spell.cli.exceptions import api_client_exception_handler, ExitException
from spell.cli.utils import prettify_time, tabulate_rows


@click.group(
    name="model",
    short_help="Manage Spell models",
    help="""Spell models are a way for you to track your progress as you work on training models.
    As you run new training runs you can push those outputs to existing model names, and we will
    track those over time for you or create new models. You can take any model version and serve it.

    If you don't specify a subcommand this will list existing models.""",
    hidden=True,
    invoke_without_command=True,
)
@click.option(
    "-m",
    "--model",
    "model_name",
    help="The name of an existing model. If specified this will list all versions of that model. "
    "If unspecified all models will be listed.",
)
@click.pass_context
def model(ctx, model_name):
    if ctx.invoked_subcommand:
        return
    client = ctx.obj["client"]
    with api_client_exception_handler():
        models = client.list_models(ctx.obj["owner"])

        if not model_name:
            print_models_list(models)
            return

        model = next((m for m in models if m.name == model_name), None)
        if not model:
            possible = get_close_matches(model_name, (m.name for m in models), n=1)
            suggestion = ""
            if len(possible) > 0:
                suggestion = " - did you mean '{}'?".format(possible[0])
            raise ExitException("Model {} not found{}".format(model_name, suggestion))
        print_model_versions_list(model)


def print_model_versions_list(model):
    def create_row(v):
        formatted_files = [""]
        if len(v.files) != 1 or v.files[0].resource_path != ".":
            formatted_files = []
            for f in v.files:
                if f.destination_path == f.resource_path:
                    formatted_files.append(f.resource_path)
                else:
                    formatted_files.append("{}:{}".format(f.resource_path, f.destination_path))
        return (
            v.formatted_version,
            v.resource,
            ", ".join(formatted_files),
            prettify_time(v.created_at),
            v.creator.user_name,
        )

    tabulate_rows(
        [create_row(v) for v in model.model_versions],
        headers=["VERSION", "RESOURCE", "FILES", "CREATED", "CREATOR"],
    )


def print_models_list(models):
    def create_row(m):
        latest_version = max(m.model_versions, key=lambda x: x.created_at)
        return (
            m.name,
            latest_version.formatted_version,
            prettify_time(m.created_at),
            m.creator.user_name,
        )

    tabulate_rows(
        [create_row(m) for m in models], headers=["NAME", "LATEST VERSION", "CREATED", "CREATOR"]
    )


@model.command(
    name="create",
    short_help="Create a new model",
    help="""Specify a name for the model, if you use an existing model name a new version
    will be created for you, otherwise a new model will be created. Resource should be a path
    to a top level resource such as 'runs/168'.""",
)
@click.pass_context
@click.argument("name")
@click.argument("resource")
@click.option(
    "--version",
    "-v",
    help="You can specify any string you want as a version, or if omitted "
    "it will be given an integer version, autoincremented from the current highest integer version",
)
@click.option(
    "--file",
    "-f",
    "files",
    multiple=True,
    metavar="PATH WITHIN RESOURCE[:MOUNT PATH]",
    help="""If the run output contains unnecessary information (like intermediate checkpoint files),
    you can whitelist only the needed files with this flag. You can optionally specify a path for each to
    be mounted within a future model server as well. If you omit this we will just use
    '<MODEL NAME>/<PATH WITHIN RESOURCE>'""",
)
def create(ctx, name, resource, version, files):
    client = ctx.obj["client"]
    with api_client_exception_handler():
        model = client.new_model(ctx.obj["owner"], name, resource, version, files)
    click.echo("Successfully created model: {} {}".format(model.model_name, model.version))


@model.command(
    name="rm",
    short_help="Deletes a model or model version",
    help="Marks a model version as deleted. If version is omitted the whole model is marked as deleted.",
)
@click.pass_context
@click.argument("name")
@click.argument("version", required=False)
def rm(ctx, name, version):
    if not version:
        rm_model(ctx, name)
    else:
        rm_model_version(ctx, name, version)


def rm_model(ctx, name):
    if not click.confirm(
        "You didn't specify a version. This will delete all "
        "versions of model {}. Are you sure you want to proceed?".format(name)
    ):
        return

    client = ctx.obj["client"]
    with api_client_exception_handler():
        client.rm_model(ctx.obj["owner"], name)
    click.echo("Successfully deleted all versions of model {}".format(name))


def rm_model_version(ctx, name, version):
    if not click.confirm(
        "Are you sure you want to delete version {} of model {}?".format(version, name)
    ):
        return

    client = ctx.obj["client"]
    with api_client_exception_handler():
        client.rm_model_version(ctx.obj["owner"], name, version)
    click.echo("Successfully deleted model {} version {}".format(name, version))
