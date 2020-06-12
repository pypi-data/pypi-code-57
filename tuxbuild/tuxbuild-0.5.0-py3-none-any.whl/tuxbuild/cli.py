# -*- coding: utf-8 -*-

import click
from functools import wraps
import json
import sys
import tuxbuild
import tuxbuild.exceptions
import tuxbuild.gitutils


info = click.echo


def error(msg):
    raise click.ClickException(msg)


def warning(msg):
    click.echo(msg, err=True)


def no_info(_):
    pass


def quiet_output(quiet):
    global info
    if quiet:
        info = no_info


def wait_for_object(build_object):
    result = True
    for state in build_object.watch():
        msg = click.style(
            f"{state.icon} {state.message}: ", fg=state.cli_color, bold=True
        ) + str(state.build)
        if state.errors:
            warning(msg)
            result = False
        elif state.warnings:
            warning(msg)
        else:
            info(msg)
    return result


@click.group(name="tuxbuild")
@click.version_option()  # Implement --version
def cli():
    pass


def common_options(required):
    def option(*args, **kwargs):
        kw = kwargs.copy()
        kw["required"] = False
        for a in args:
            if a in required:
                kw["required"] = True
        return click.option(*args, **kw)

    options = [
        option("--git-repo", help="Git repository"),
        option("--git-ref", help="Git reference"),
        option("--git-sha", help="Git commit"),
        option(
            "--git-head",
            default=False,
            is_flag=True,
            help="Build the current git HEAD. Overrrides --git-repo and --git-ref",
        ),
        option(
            "--target-arch",
            help="Target architecture [arm64|arm|x86|i386|mips|arc|riscv]",
        ),
        option(
            "--kconfig",
            multiple=True,
            help="Kernel kconfig arguments (may be specified multiple times)",
        ),
        option("--toolchain", help="Toolchain [gcc-8|gcc-9|clang-8|clang-9]"),
        option(
            "--kconfig-allconfig",
            help=(
                "Argument used only with allyesconfig/allmodconfig/allnoconfig/randconfig."
                "The argument is a path to a file with specific config symbols which you want to override"
            ),
        ),
        option(
            "--json-out",
            help="Write json build status out to a named file path",
            type=click.File("w", encoding="utf-8"),
        ),
        option(
            "-q",
            "--quiet",
            default=False,
            is_flag=True,
            help="Supress all informational output; prints only the download URL for the build",
        ),
    ]

    def wrapper(f):
        f = wraps(f)(process_git_head(f))
        for opt in options:
            f = opt(f)
        return f

    return wrapper


def process_git_head(f):
    def wrapper(**kw):
        git_head = kw["git_head"]
        if git_head:
            try:
                repo, sha = tuxbuild.gitutils.get_git_head()
                kw["git_repo"] = repo
                kw["git_sha"] = sha
            except Exception as e:
                error(e)
        return f(**kw)

    return wrapper


@cli.command()
@common_options(required=["--target-arch", "--kconfig", "--toolchain"])
def build(json_out=None, quiet=False, git_head=False, **build_params):
    quiet_output(quiet)

    try:
        build = tuxbuild.Build(**build_params)
    except (AssertionError, tuxbuild.exceptions.TuxbuildError) as e:
        error(e)
    info(
        "Building Linux Kernel {} at {}".format(
            build.git_repo, build.git_ref or build.git_sha
        )
    )
    try:
        build.build()
    except tuxbuild.exceptions.BadRequest as e:
        raise (click.ClickException(str(e)))
    build_result = wait_for_object(build)
    if json_out:
        json_out.write(json.dumps(build.status, sort_keys=True, indent=4))
    if quiet:
        print(build.build_data)
    if not build_result:
        sys.exit(1)


@cli.command()
@click.option("--set-name", required=True, help="Set name")
@click.option("--tux-config", help="Path or a web URL to tuxbuild config file")
@common_options(required=[])
def build_set(
    tux_config, set_name, json_out=None, quiet=None, git_head=False, **build_params
):
    quiet_output(quiet)

    try:
        build_set_config = tuxbuild.config.BuildSetConfig(set_name, tux_config)
        build_set = tuxbuild.BuildSet(build_set_config.entries, **build_params)
    except (AssertionError, tuxbuild.exceptions.TuxbuildError) as e:
        error(e)

    info("Building Linux Kernel build set {}".format(set_name))

    try:
        build_set.build()
    except tuxbuild.exceptions.BadRequest as e:
        raise (click.ClickException(str(e)))

    build_set_result = wait_for_object(build_set)

    if json_out:
        json_out.write(json.dumps(build_set.status_list, sort_keys=True, indent=4))

    if quiet:
        for build in build_set.builds:
            print(build.build_data)

    # If any of the builds did not pass, exit with exit code of 1
    if not build_set_result:
        sys.exit(1)


def main():
    cli.main(prog_name="tuxbuild")
