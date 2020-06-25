#! -*- encoding: utf-8 -*-
import os
import sys

import click
from autoupgrade import Package

from suite_py.commands import merge_pr
from suite_py.commands import deploy
from suite_py.commands import rollback
from suite_py.commands import create_branch
from suite_py.commands import open_pr
from suite_py.commands import project_lock
from suite_py.commands import ask_review
from suite_py.commands import create_qa
from suite_py.commands import delete_qa
from suite_py.commands import status
from suite_py.commands import check
from suite_py.commands import ip
from suite_py.commands import generator
from suite_py.lib.handler import prompt_utils
from suite_py.lib.config import Config
from suite_py.__version__ import __version__


config = Config()

# TODO: fixme -> write something more smart in locating the current project
def confirm_cwd():
    project_path = os.getcwd()
    project = os.path.basename(project_path)
    if not prompt_utils.ask_confirm(f"Vuoi continuare sul progetto {project}?"):
        sys.exit(-1)
    return project_path


@click.group()
@click.option(
    "--project",
    type=click.Path(exists=True),
    default=confirm_cwd,
    help="Nome del progetto su cui eseguire il comando (default directory corrente)",
)
@click.option(
    "--timeout",
    type=click.INT,
    help="Timeout in secondi per le operazioni di CaptainHook",
)
@click.pass_context
def main(ctx, project, timeout):
    Package("suite_py", verbose=True).smartupgrade()
    print(f"v{__version__}")
    project_name = os.path.basename(project)
    ctx.ensure_object(dict)
    ctx.obj["project"] = project_name
    ctx.obj["captainhook_timeout"] = timeout  # Might be also None
    os.chdir(os.path.join(config.load()["user"]["projects_home"], ctx.obj["project"]))


@main.command(
    "create-branch", help="Crea branch locale e imposta la card di YouTrack in progress"
)
@click.option("--card", type=click.STRING, help="Numero card youtrack (ex. PRIMA-123)")
@click.pass_context
def cli_create_branch(ctx, card):
    create_branch.entrypoint(ctx.obj["project"], card)


@main.command("lock", help="Lock di un progetto su staging o prod")
@click.argument(
    "environment", type=click.Choice(("staging", "production", "deploy", "merge"))
)
@click.pass_context
def cli_lock_project(ctx, environment):
    project_lock.entrypoint(
        ctx.obj["project"], ctx.obj["captainhook_timeout"], environment, "lock"
    )


@main.command("unlock", help="Unlock di un progetto su staging o prod")
@click.argument(
    "environment", type=click.Choice(("staging", "production", "deploy", "merge"))
)
@click.pass_context
def cli_unlock_project(ctx, environment):
    project_lock.entrypoint(
        ctx.obj["project"], ctx.obj["captainhook_timeout"], environment, "unlock"
    )


@main.command("open-pr", help="Apre una PR su GitHub")
@click.pass_context
def cli_open_pr(ctx):
    open_pr.entrypoint(ctx.obj["project"])


@main.command("ask-review", help="Chiede la review di una PR")
@click.pass_context
def cli_ask_review(ctx):
    ask_review.entrypoint(ctx.obj["project"], ctx.obj["captainhook_timeout"])


@main.command("create-qa", help="Crea un QA (integrazione con qainit)")
@click.pass_context
def cli_create_qa(ctx):
    create_qa.entrypoint(ctx.obj["project"])


@main.command("delete-qa", help="Cancella un QA (integrazione con qainit)")
@click.pass_context
def cli_delete_qa(ctx):
    delete_qa.entrypoint(ctx.obj["project"])


@main.command(
    "merge-pr", help="Merge del branch selezionato con master se tutti i check sono ok"
)
@click.pass_context
def cli_merge_pr(ctx):
    merge_pr.entrypoint(ctx.obj["project"], ctx.obj["captainhook_timeout"])


@main.command("deploy", help="Deploy in produzione del branch master")
@click.pass_context
def cli_deploy(ctx):
    deploy.entrypoint(ctx.obj["project"], ctx.obj["captainhook_timeout"])


@main.command("rollback", help="Rollback in produzione")
@click.pass_context
def cli_rollback(ctx):
    rollback.entrypoint(ctx.obj["project"], ctx.obj["captainhook_timeout"])


@main.command("status", help="Stato attuale di un progetto")
@click.pass_context
def cli_status(ctx):
    status.entrypoint(ctx.obj["project"], ctx.obj["captainhook_timeout"])


@main.command("check", help="Verifica autorizzazioni ai servizi di terze parti")
@click.pass_context
def cli_check(ctx):
    check.entrypoint(ctx.obj["captainhook_timeout"])


@main.command(
    "ip", help="Ottieni gli indirizzi IP degli hosts dove il task è running",
)
@click.argument("environment", type=click.Choice(("staging", "production")))
@click.pass_context
def cli_ip(ctx, environment):
    ip.entrypoint(ctx.obj["project"], environment)


@main.command("generator", help="Genera diversi file partendo da dei templates")
def cli_generator():
    generator.entrypoint()
