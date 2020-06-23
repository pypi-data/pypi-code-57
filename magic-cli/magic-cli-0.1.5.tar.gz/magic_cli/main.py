import sys
import os
from pathlib import Path
import shutil

import requests
import typer


app = typer.Typer()

VENV_NAME = "magic_venv"


@app.command()
def sowell():
    """
    Load the portal gun
    """

    typer.echo("IS GOAT")


def download_boilerplate_git_folder(output_filename):
    github_repo_url = "https://api.github.com/repos/jerber/magic-server/tarball/master"
    r = requests.get(github_repo_url, stream=True)
    with open(output_filename, "wb") as f:
        for chunk in r.raw.stream(1024, decode_content=False):
            if chunk:
                f.write(chunk)


def make_venv():
    os.system(f"python3 -m venv {VENV_NAME}")
    os.system(f"source {VENV_NAME}/bin/activate && pip install -r requirements.txt")


@app.command()
def create(project_name: str = typer.Argument("magic-server"), replace: bool = False):
    # TODO add some printing of status
    project_path = Path(project_name)
    if project_path.exists() and not replace:
        typer.echo(
            "There is already a project that exists. If you would like to replace this project, "
            "add the flag --replace to your command"
        )
        raise typer.Exit()

    zip_filename = "boilerplate.tar.gz"
    download_boilerplate_git_folder(zip_filename)

    temp_dir = Path("._magic_")
    shutil.unpack_archive(zip_filename, temp_dir)
    git_folder = list(temp_dir.glob("*"))[0]

    if project_path.exists():
        shutil.rmtree(project_path)

    git_folder.replace(project_path)

    shutil.rmtree(temp_dir)
    os.remove(zip_filename)


@app.command()
def dev(create_venv: bool = True):
    main_filename = "main.py"
    if not Path(main_filename).exists():
        typer.echo(
            "Cannot find the main.py file. Are you sure you created this app with magic?"
        )
        raise typer.Exit()

    command = f"export LOCAL=1 && python {main_filename}"

    prefix = getattr(sys, "prefix", "")
    if VENV_NAME not in prefix and create_venv:
        typer.echo("no venv detected, will make own now")
        make_venv()
        command = f"source {VENV_NAME}/bin/activate && {command}"

    os.system(command)


@app.command()
def version():
    typer.echo("5")


if __name__ == "__main__":
    app()
