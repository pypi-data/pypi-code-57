from pathlib import Path

import click

from apeiron.config import cfg
from apeiron.models import ManifestIndex
from apeiron.manifest import get_manifest_index_path
from apeiron.manifest import save_manifests


from apeiron.view import print_config


def create_dir_if_not_exist(path: Path, name: str):
    if not path.exists():
        click.echo(click.style(f"{name.capitalize()} not found, creating…", fg="yellow"))
        try:
            path.mkdir(parents=True)
        except IOError as e:
            click.echo(click.style(f"Failed to create {name}, reason: {str(e)}", fg="red"))
            exit(1)
        else:
            click.echo(click.style(f"Created empty {name}: {path.as_posix()}", fg="green"))


def check():
    click.echo(click.style("Application config", fg="blue", bold=True))
    click.echo(print_config(cfg))

    source_dir: Path = Path(cfg.sources_dir)
    create_dir_if_not_exist(source_dir, "source dir")

    package_dir: Path = Path(cfg.packages_dir)
    create_dir_if_not_exist(package_dir, "package dir")

    manifest_index_path: Path = get_manifest_index_path()
    if not manifest_index_path.exists():
        click.echo(click.style(f"Manifests index not found, writing stub…", fg="yellow"))
        try:
            save_manifests(ManifestIndex())
        except IOError as e:
            click.echo(click.style(f"Failed to write manifests index, reason: {e}", fg="red"))
            exit(1)
        else:
            click.echo(click.style(f"Wrote empty manifest index to: {manifest_index_path.as_posix()}", fg="green"))
