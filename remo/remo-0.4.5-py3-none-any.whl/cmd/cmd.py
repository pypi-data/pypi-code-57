import os
from typing import List

import requests
import typer
import platform

from remo.config import REMO_HOME
from . import postgres
from .db import migrate, is_database_uptodate
from .installer import get_instance
from .config import create_config, create_or_update_user
from .killer import list_and_confirm_kill_remo, is_remo_server_running
from .log import Log
from .runtime import install_cert_path, setup_vips
from .server import run_server, delayed_browse
from .checker import check_runtime_requirements
from remo_app import __version__
from remo_app.config.config import Config
from remo_app.remo.stores.version_store import Version

app = typer.Typer(add_completion=False, add_help_option=False)


def make_db_url(db):
    engine = db.get('engine')
    if engine != 'postgres':
        Log.exit(f"""Not supported DB engine - {engine}.

Please use 'postgres'.
""")

    host, name, password, port, user = db.get('host'), db.get('name'), db.get('password'), db.get('port'), db.get('user')
    return f'{engine}://{user}:{password}@{host}:{port}/{name}'


def set_db_url(url):
    os.environ['DATABASE_URL'] = url


@app.command(add_help_option=False, options_metavar='')
def init():
    Log.msg('Initiailizing Remo:')

    installer = get_instance()
    dependencies = installer.dependencies()
    if dependencies:
        fmt_deps_list = '\n   * '.join(dependencies)
        msg = f"""
This will download and install the following packages as needed: \n   * {fmt_deps_list}
Do you want to continue?"""
        if not typer.confirm(msg, default=True):
            Log.installation_aborted()

    db_config = installer.install(postgres=postgres.get_instance())
    db_url = make_db_url(db_config)
    set_db_url(db_url)
    migrate()

    config = create_config(db_url)
    if config.viewer == 'electron':
        installer.download_electron_app()

    Log.msg("""

    (\\(\\
    (>':')  Remo successfully initiliazed.
    You can launch remo using the command 'python -m remo_app'
    """)


@app.command(add_help_option=False, options_metavar='')
def run_jobs():
    from remo_app.remo.use_cases import jobs
    Log.msg('Running background jobs:')
    for job in jobs.all_jobs:
        job()


@app.command(add_help_option=False, options_metavar='')
def debug():
    config = Config.load()
    run_server(config, debug=True, background_job=run_jobs)


@app.command(add_help_option=False, options_metavar='')
def kill():
    config = Config.load()
    list_and_confirm_kill_remo(config)


@app.command(add_help_option=False, options_metavar='')
def open():
    config = Config.load()
    if is_remo_server_running(config):
        delayed_browse(config)
    else:
        Log.msg('Remo app is not running, you can run it with command: python -m remo_app')


def table(headers: List[str], rows: List[List[str]]):
    columns_width = [len(val) for val in headers]

    for row in rows:
        for i, val in enumerate(row):
            columns_width[i] = max(columns_width[i], len(val))

    columns_width = list(map(lambda x: x + 2, columns_width))

    lines = [
        [f' {val:{width - 1}s}' for width, val in zip(columns_width, headers)],
        ['=' * width for width in columns_width]
    ]
    for row in rows:
        lines.append([f' {val:{width - 1}s}' for width, val in zip(columns_width, row)])

    return '\n'.join(map('|'.join, lines))


@app.command(add_help_option=False, options_metavar='')
def remove_dataset():
    from remo_app.config.standalone.wsgi import application
    from remo_app.remo.models import Dataset
    datasets = Dataset.objects.all()
    if not datasets:
        Log.msg('No datasets found.')
        return

    Log.msg('List of existing datasets:')
    lookup = {}
    for ds in datasets:
        lookup[ds.id] = ds

    rows = [[str(ds.id), ds.name] for ds in datasets]
    Log.msg(table(['ID', 'Dataset name'], rows))

    confirm = input('\nType the dataset ID you want to delete, or type "all" to delete all of them: ')
    id = confirm.lower().strip()
    if id == 'all':
        for ds in lookup.values():
            delete_dataset(ds)
    else:
        try:
            id = int(id)
        except Exception:
            Log.exit('failed to parse dataset id')

        if id not in lookup:
            Log.exit('dataset id not found')

        delete_dataset(lookup[id])


def delete_dataset(ds):
    typer.echo(f'Deleting Dataset {ds.id} - {ds.name}... ', nl=False)
    ds.delete()
    typer.secho("DONE", fg=typer.colors.GREEN, bold=True)


@app.command(add_help_option=False, options_metavar='')
def delete():
    msg = "Do you want to delete all remo data and metadata?"
    if not typer.confirm(msg, default=True):
        Log.exit_msg('\nUninstallation aborted.')

    Log.msg('\nUninstalling Remo...')
    config = Config.load()
    installer = get_instance()
    installer.uninstall(postgres.get_instance(), config.parse_db_params())
    Log.msg("""Remo data was successfully deleted

To completely remove remo, run:
$ pip uninstall remo""")


def version_callback(value: bool):
    if value:
        show_remo_version()
        raise typer.Exit()


def latest_remo_version():
    try:
        resp = requests.get(f'https://app.remo.ai/version?check-updates-for-version={__version__}').json()
        return resp.get('version'), resp.get('msg')
    except Exception:
        pass


def is_new_version_available():
    result = latest_remo_version()
    if not result:
        return

    latest, msg = result
    if Version.to_num(latest) > Version.to_num(__version__):
        return latest, msg


def show_new_available_version():
    result = is_new_version_available()
    if not result:
        return

    new_version, msg = result
    if new_version:
        Log.msg(f"New version available: {new_version}. Run pip install remo --upgrade to install it")
    if msg:
        Log.msg(msg)


def show_remo_version():
    Log.msg(logo)
    show_new_available_version()


def show_help_info():
    Log.msg(f"""
remo version: v{__version__}

Commands: you can use python -m remo_app with the following options:

  (no command)    - start server and open the default frontend
  no-browser      - start server
  init            - initialize settings and download additional packages
  run-jobs        - run periodic jobs
  kill            - kill running remo instances
  open            - open the Electron app
  remove-dataset  - delete datasets
  delete          - delete all the datasets and metadata

  --version       - show remo version
  --help          - show help info

""")


@app.command(add_help_option=False, options_metavar='')
def help():
    show_help_info()


@app.command(add_help_option=False, options_metavar='')
def version():
    show_remo_version()


def help_callback(value: bool):
    if value:
        show_help_info()
        raise typer.Exit()


@app.command(add_help_option=False, options_metavar='')
def no_browser():
    config = Config.load()
    run_server(config, background_job=run_jobs, with_browser=False)


@app.callback(invoke_without_command=True, options_metavar='', subcommand_metavar='')
def main(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", callback=version_callback, is_eager=True),
    help: bool = typer.Option(None, "--help", callback=help_callback, is_eager=True),
):
    if ctx.invoked_subcommand not in ('help', 'version', 'kill'):

        os.environ["DJANGO_SETTINGS_MODULE"] = "remo_app.config.standalone.settings"
        Log.msg(logo)

        # check_installation_requirements()
        install_cert_path()

        if ctx.invoked_subcommand != 'init':
            if not Config.is_exists():
                Log.exit(f"""Remo not fully initialized, config file was not found at {REMO_HOME}.

Please run: python -m remo_app init
            """)

            setup_vips()

            config = Config.load()
            if not config.db_url:
                Log.exit_msg("""
         You installed a new version of Remo that uses PostgreSQL database for faster processing.
         To use it, you need to run 'python -m remo_app init'.
WARNING: Your current data in SQLite database will be lost.

To proceed, just run: python -m remo_app init
                """)

            set_db_url(config.db_url)
            check_runtime_requirements(config.parse_db_params())

            from remo_app.config.standalone.wsgi import application
            if not is_database_uptodate():
                migrate()

            name, email, password = create_or_update_user(config.user_name, config.user_email, config.user_password)
            config.update(user_name=name, user_email=email, user_password=password)
            config.save()

    if ctx.invoked_subcommand is None:
        show_new_available_version()
        run_server(config, background_job=run_jobs)


logo = (f"""
===============================================
    (\\(\\
    (>':')  Remo: v{__version__}
===============================================
Python: {platform.python_version()}, {platform.platform()}
""")
