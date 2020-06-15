import os

import click
from tabulate import tabulate

from .config import conf, ConfigurationException
from .repo import GitRepo
from .utils import get_ellipsised
from .utils.cli import AliasedGroup
from .utils.relationship import get_remote_for_pr, create_pr_branch
from .utils.setup import setup_config


@click.command(cls=AliasedGroup)
@click.option(
    "-c",
    "--config",
    "config_path",
    type=click.Path(exists=True),
    help="Path to the configuration file",
)
@click.option(
    "-u",
    "--upstream-remote",
    help="Name of the remote for the upstream repo (default: origin)",
)
@click.option("-v", "--verbose/--no-verbose", help="Show more stuff")
@click.pass_context
def cli(ctx, config_path, upstream_remote, verbose):
    """Manage branches and pull-requests"""
    ctx.ensure_object(dict)

    if not os.path.exists(conf.path):
        setup_config()

    try:
        conf.load(config_path)
    except ConfigurationException as e:
        raise click.ClickException(e.message)

    if verbose:
        conf["verbose"] = verbose

    ctx.obj["repo"] = repo = GitRepo()

    if upstream_remote:
        repo.get_remote(upstream_remote).set_upstream()


@cli.command()
@click.pass_context
def show(ctx):
    """Show branches and pull requests"""
    repo = ctx.obj["repo"]
    branches = repo.get_branches()
    origin_repo = repo.get_upstream_remote().get_server_repo()
    if not conf["quiet"]:
        click.secho("Gathering data...", fg="bright_cyan")
    data = []
    for branch in branches:
        branch_data = [branch.name]
        pulls = origin_repo.get_pulls(branch)
        if not pulls:
            data.append(branch_data)
            continue
        branch_data.append("\n".join(f"#{pr.number}" for pr in pulls))
        branch_data.append("\n".join(f"[{pr.state}]" for pr in pulls))
        branch_data.append("\n".join(get_ellipsised(pr.title, 80) for pr in pulls))
        branch_data.append("\n".join(pr.html_url for pr in pulls))
        data.append(branch_data)
    click.echo(tabulate(data, headers=["Branch", "PR", "State", "Title", "URL"]))


@cli.command()
@click.option(
    "--remotes/--no-remotes",
    "prune_remotes",
    default=True,
    show_default=True,
    help="Also prune remote references",
)
@click.pass_context
def prune(ctx, prune_remotes):
    """Remove branches whose pull requests are closed"""
    repo = ctx.obj["repo"]
    to_prune = []
    origin_remote = repo.get_upstream_remote()
    origin_repo = origin_remote.get_server_repo()
    click.echo("Branches to prune:")
    for branch in repo.get_branches():
        pulls = origin_repo.get_pulls(branch)
        if not pulls:
            continue
        if all([pr.state == "closed" for pr in pulls]):
            click.echo(branch.name)
            to_prune.append(branch)
    if to_prune:
        answer = click.confirm("Should they be deleted locally?")
        if answer:
            current_branch = repo.get_current_branch()
            default_branch = origin_remote.get_default_branch()
            if current_branch in to_prune:
                default_branch.checkout()
            for branch in to_prune:
                branch.delete(force=True)
        else:
            click.echo("OK, aborting here.")
    else:
        click.echo("No branch to prune.")
    if prune_remotes:
        click.secho("Cleaning up remote references", fg="bright_cyan")
        for remote in repo.get_remotes():
            remote.prune()


@cli.command(alias="co")
@click.argument("pr-number", type=int)
@click.pass_context
def checkout(ctx, pr_number):
    """Check out a pull request in a local branch"""
    repo = ctx.obj["repo"]
    pr_branches = [
        b for b in repo.get_branches() if b.name.startswith(f"PR/{pr_number}/")
    ]
    origin_remote = repo.get_upstream_remote()
    origin_repo = origin_remote.get_server_repo()
    default_branch = origin_remote.get_default_branch()
    pr = origin_repo.get_pull(pr_number)

    if pr.state == "closed":
        answer = click.confirm(
            "This PR is closed, are you sure you want to check it out?"
        )
        if not answer:
            click.echo("Aborting.")
            return

    # Move the default branch (usually master)
    default_branch.checkout(quiet=True)
    # Get or create the remote for this PR
    remote = get_remote_for_pr(repo, pr)
    remote.fetch(quiet=True)
    branch_id = len(pr_branches) + 1
    if branch_id == 1:
        # Initial checkout: also check out previous reviews
        for review in pr.get_reviews():
            if review.username == pr.username:
                # Review requests show up as review comments in the API
                continue
            timestamp = review.datetime.strftime("%x %X")
            click.secho(
                f"Checking out review by {review.username} on {timestamp} with state "
                f"{review.state} to sub-branch {branch_id}",
                fg="bright_cyan",
            )
            create_pr_branch(pr, branch_id, remote, review.commit_id)
            branch_id += 1

    click.secho(
        f"Checking out PR #{pr.number} to sub-branch {branch_id}", fg="bright_cyan"
    )
    branch = create_pr_branch(pr, branch_id, remote, pr.head_commit)
    branch.checkout()
