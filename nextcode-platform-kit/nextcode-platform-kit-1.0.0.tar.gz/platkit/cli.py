import sys, os
import click
from sqlalchemy import create_engine
import yaml
import time
from urllib.parse import urlsplit

from flask.cli import AppGroup

MASTER_DB = "postgres"


def get_server_from_connection_string(connection_string):
    return urlsplit(connection_string).netloc.split("@")[-1]


def get_db_from_connection_string(connection_string):
    return urlsplit(connection_string).path[1:]


def setup_commands(app):
    # database management
    db_manage_cli = AppGroup("dbmanage")

    connection_string = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    main_db_name = get_db_from_connection_string(connection_string)
    test_db_name = main_db_name + "-test"
    master_connection_string = connection_string.replace("/" + main_db_name, "/postgres")

    @db_manage_cli.command("create")
    @click.option("-t", "--test", is_flag=True, default=False)
    def create_db(test):
        db_name = test_db_name if test else main_db_name
        return _create_db(master_connection_string, db_name)

    @db_manage_cli.command("recreate")
    @click.option("-t", "--test", is_flag=True, default=False)
    def recreate_db(test):
        db_name = test_db_name if test else main_db_name
        _drop_db(master_connection_string, db_name, silent=True)
        return _create_db(master_connection_string, db_name)

    @db_manage_cli.command("drop")
    @click.option("-t", "--test", is_flag=True, default=False)
    def drop_db(test):
        db_name = test_db_name if test else main_db_name
        _drop_db(master_connection_string, db_name)

    app.cli.add_command(db_manage_cli)

    # build info file
    build_info_cli = AppGroup("buildinfo")

    @build_info_cli.command("update", context_settings=dict(ignore_unknown_options=True))
    @click.argument("option_args", nargs=-1, type=click.UNPROCESSED)
    def update_buildinfo(option_args):
        _update_buildinfo(option_args)

    app.cli.add_command(build_info_cli)

    # bump version
    @app.cli.command()
    @click.argument("which", type=click.Choice(["major", "minor", "patch", "set"]), required=True)
    @click.argument("version", required=False)
    def bumpversion(which, version):
        """
        Use 'major', 'minor' or 'patch' to bump respective versions.
        Use 'set' to set an explicit version string in the format 'major.minor.patch'
        """
        package_name = app.config["APP_MODULE_NAME"]
        filename = os.path.join(package_name, "VERSION")
        major, minor, patch = (0, 1, 0)
        old_version = ""
        try:
            with open(filename, "r") as f:
                old_version = f.readline().strip()
        except Exception:
            pass
        major, minor, patch = old_version.split(".")

        if which == "major":
            major = int(major) + 1
            minor = 0
            patch = 0
        elif which == "minor":
            minor = int(minor) + 1
            patch = 0
        elif which == "patch":
            patch = int(patch.split("-")[0]) + 1

        new_version = "%s.%s.%s" % (major, minor, patch)
        if which == "set":
            new_version = version

        with open(filename, "w") as f:
            f.write(new_version)

        click.echo("Version has been changed from %s -> %s" % (old_version, new_version))


def connect(connection_string):
    engine = create_engine(
        connection_string, isolation_level="AUTOCOMMIT", connect_args={"connect_timeout": 5}
    )
    error_string = None
    for i in range(5):
        try:
            engine.execute("COMMIT")
            return engine
        except Exception as e:
            error_string = "Error connecting to database '{}': {}\n".format(
                connection_string, str(e)
            )
            if "does not exist" in repr(e):
                error_string += "This script requires the master database 'postgres' to be present"
                break
            elif "could not connect to server" in repr(e):
                error_string += (
                    "Database server not found. Are you sure the postgres server is running?"
                )
                time.sleep(1.0)
                continue
            else:
                break

    click.secho(error_string, fg="red")
    sys.exit(1)


def _drop_db(master_connection_string, db_name, silent=False):
    click.echo(click.style("Dropping database '%s'..." % (db_name), fg="yellow"))
    engine = connect(master_connection_string)
    engine.execute(
        "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{}';".format(
            db_name
        )
    )
    try:
        sql = 'DROP DATABASE "{}";'.format(db_name)
        engine.execute(sql)
    except Exception as e:
        if not silent:
            click.echo(click.style(str(e), fg="red"))


def _create_db(master_connection_string, db_name):
    click.echo("Creating database '%s'..." % (db_name))
    engine = connect(master_connection_string)
    try:
        sql = 'CREATE DATABASE "{}";'.format(db_name)
        engine.execute(sql)
    except Exception as e:
        if "already exists" in repr(e):
            click.echo(
                "Database '%s' already exists. To drop it and create again run 'recreate'" % db_name
            )
            sys.exit(0)
        click.echo(click.style("Unable to create database! Error was %s" % str(e), fg="red"))
        click.echo("Is the postgres server running?")
        sys.exit(1)

    click.echo(click.style("\nEmpty database '%s' has been created." % (db_name), fg="green"))
    if "test" not in db_name:
        click.echo("\nInitialize with 'flask db upgrade'")


def _update_buildinfo(option_args):
    if len(option_args) % 2 != 0:
        raise ValueError("You must supply key and value in groups of 2")
    options = [option_args[n: n + 2] for n in range(0, len(option_args), 2)]

    build_info = {}
    try:
        with open(".build_info.yml", "r") as f:
            build_info = yaml.safe_load(f) or {}
    except Exception:
        pass
    for v in options:
        build_info[v[0]] = v[1]
    with open(".build_info.yml", "w") as f:
        yaml.dump(build_info, f)
