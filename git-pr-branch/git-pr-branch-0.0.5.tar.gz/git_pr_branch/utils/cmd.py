from subprocess import run, PIPE, DEVNULL

import click

from git_pr_branch.config import conf


def get_cmd(*args, hide_stderr=False):
    if conf["verbose"]:
        click.secho(" ".join(args), fg="bright_blue")
    output = run(
        args,
        check=True,
        stdout=PIPE,
        stderr=DEVNULL if hide_stderr else None,
        universal_newlines=True,
    ).stdout
    if output.endswith("\n"):
        output = output[:-1]
    return output


def run_cmd(*args):
    click.secho(" ".join(args), fg="bright_blue")
    click.secho("", fg="blue", reset=False, nl=False)
    try:
        run(args, check=True)
    finally:
        click.secho("", fg="reset", nl=False)
