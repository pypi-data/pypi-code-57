import os
from distutils.file_util import copy_file

import click


@click.command()
def init():
    """Initializes an empty skill in the current directory."""
    template_folder = os.path.join(os.path.dirname(__file__), "..", "template", "skill")
    current_folder = os.getcwd()

    for root, dirs, filenames in os.walk(template_folder):
        for file_name in filenames:
            src_file = os.path.join(root, file_name)
            relative_dest_path = os.path.join(root[len(template_folder)+1:], file_name)
            dest_file = os.path.join(current_folder, relative_dest_path)

            if os.path.exists(dest_file):
                click.echo(f"Skipping {relative_dest_path} as it already exists...")
            else:
                click.echo(f"Creating {relative_dest_path} ...")
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                copy_file(src_file, dest_file)

    click.echo("Initialization complete.")

