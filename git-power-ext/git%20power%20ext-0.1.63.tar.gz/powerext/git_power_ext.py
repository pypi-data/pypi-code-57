import click
from . import git
from . import common

@click.group()
def cli():
    pass

@cli.command()
@click.option("--merged-on-branch", "branch", metavar="BRANCH", default="master", help="which branch to check if merged on it", show_default=True)
@click.option("--local/--no-local", default=False, help="Apply on local branches or not", show_default=True)
@click.option("--remote/--no-remote", default=True, help="Apply on remote branches or not", show_default=True)
@click.option("--dry-run", is_flag=True, default=False, help="List only no actual deletion will be done", show_default=True)
@click.option("--skip-fetch", is_flag=True, default=False, help="Skip fetching the new updates before listing/deleting branches", show_default=True)
@click.option("--yes", "confirmation", is_flag=True, default=False, help="Continue without confirmation BE CAREFUL!!!", show_default=True)
def delete_all_merged_branches(branch, local, remote, dry_run, skip_fetch, confirmation):
    ''' delete all banches merged on given branch '''

    if not skip_fetch:
        git.fetch()

    merged_branches = git.get_merged_branches(branch=branch)
    common.print_seperator()
    common.print_list(merged_branches)
    common.print_seperator()
    click.secho(f"number of merged branches on {branch}: {len(merged_branches)}", bold=True, fg="blue")
    common.print_seperator()

    delete_message = "local and remote" if local and remote else "local" if local else "remote" if remote else ""
    if (local or remote) and len(merged_branches) > 0 and (confirmation or click.confirm(f"Are you sure you want to delete {delete_message} branches?")):
        remote_name = git.get_remote_name()
        for b in merged_branches:
            if dry_run:
                click.secho(f"'{b}' will be deleted if not --dry-run", fg="red")
            else:
                git.delete_branch(branch=b, local=local, remote=remote, remote_name=remote_name)
            
        common.print_seperator()
        print("🎉❌ BRANCHES DELETED ❌🎉")
    else:
        print(" 🚫mission abort 🚫")