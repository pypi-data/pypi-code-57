import click
from click_plugins import with_plugins
from pkg_resources import iter_entry_points
import logging
import os

from LbEnv.ProjectEnv import SearchPath

from lb_dev.commands.default_lb_dev import default_lb_dev
from lb_dev.commands.copyright.create_license_file.create_license_file import create_license_file_if_not_exists
from lb_dev.commands.copyright.check_for_license_file.check_for_license import check_for_license
from lb_dev.commands.copyright.check_copyright_comment.check_copyright_comment import check_copyright
from lb_dev.commands.copyright.add_copyright_comment.add_copyright_comment import add_copyright, update_copyright_year
from lb_utils.log_utils import set_up_logging


@with_plugins(iter_entry_points('lb_dev.plugins'))
@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--project')
@click.option('--dev', is_flag=True, help='prepend $LHCBDEV to the search path. Note: the directories are searched in the order specified on the command line.')
@click.option('--dev-dir', multiple=True, default=SearchPath([]), help='prepend DEVDIR to the search path. Note: the directories are searched in the order specified on the command line.')
@click.option('--nightly-base', multiple=True, default=[], help='add the specified directory to the nightly builds search path (must be specified before --nightly)')
@click.option('--nightly', help='Add the required slot of the LHCb nightly builds to the list of DEV dirs. DAY must be a 3 digit abbreviation of the weekday "Today", an ISO formatted date or an integer, the default is Today. Special settings of the CMTPROJECTPATH needed for the nightly build slot are taken into account.')
@click.option('--help-nightly-local', is_flag=True, help='Print instructions on how to install locally and use a nightly slot build')
@click.option('--user-area', default=os.environ.get('User_release_area'), help='Use the specified path as User_release_area instead of the value of the environment variable.')
@click.option('--no-user-area', is_flag=True, help='Ignore the user release area when looking for projects.')
@click.option('--siteroot', '-r', help='path to the installation root, used to add default search path')
@click.option('--platform', '-c', help='runtime platform. With "best", the most appropriate is chosen [default: %(default)s]')
@click.option('--force-platform', is_flag=True, help='ignore platform compatibility check')
@click.option('--list', '-l', is_flag=True, help='list the available versions of the requested project and exit')
@click.option('--list-versions', is_flag=True, help='obsolete spelling of --list')
@click.option('--list-platforms', '-L', is_flag=True, help='list the available platforms for the requested project/version and exit')
@click.option('--name', '-n', help='Name of the local project [default: "<proj>Dev_<vers>"].')
@click.option('--dest-dir', default=os.curdir, help='Where to create the local project [default: current directory].')
@click.option('--git/--no-git', default=True, help='Initialize git repository in the generated directory [default, if git is available].')
@click.option('--with-fortran/--without-fortran', default=False, help='(not) enable FORTRAN support for the generated project')
@click.option('-v', '--verbose', count=True)
def lb_dev(ctx, project, dev, dev_dir, nightly_base, nightly, help_nightly_local, user_area, no_user_area, siteroot, platform, force_platform, list, list_versions, list_platforms, name, dest_dir, git, with_fortran, verbose):
    if ctx.invoked_subcommand is None:
        set_up_logging(verbose)
        default_lb_dev(project, 
        # version, 
        dev, dev_dir, nightly_base, nightly, help_nightly_local, user_area, no_user_area, siteroot, platform, force_platform, list, list_versions, list_platforms, name, dest_dir, git, with_fortran,)

# TODO remove when copyright package is split
@click.command(name='check-for-license', help='Check directory for license file')
@click.option('--path', '-p', default='.')
@click.option('-v', '--verbose', count=True)
def check_for_license_command(path, verbose):
    set_up_logging(verbose)
    check_for_license(path)


# TODO remove when copyright package is split
@click.command(name='create-license-file', help='Create license file in directory')
@click.option('-v', '--verbose', count=True)
@click.option('--path', '-p', default='.')
@click.option('--name', '-n', default='LICENSE')
@click.option('--license', '-l', type=click.Choice(['apache-2.0', 'gpl-3.0', 'mit']), default='gpl-3.0',)
def create_license_file_command(verbose, path, name, license):
    set_up_logging(verbose)
    return create_license_file_if_not_exists(path, name, license)

# TODO remove when copyright package is split
@click.command(name='check-copyright-comment', help='Check that each git tracked source file in the current directory contains a copyright statement.')
@click.option('--reference', '-r', help='commit-ish to use as reference to only check changed file')
@click.option('--porcelain', is_flag=True, help='only print the list of files w/o copyright')
@click.option('-s', 'separator', flag_value='\n', default=True, help='paths are separated with \\n character')
@click.option('-z', 'separator', flag_value='\x00', help='when using --porcelain, paths are separated with NUL character')
@click.option('--inverted', is_flag=True, help='list files w/ copyright, instead of w/o (Default)')
@click.option('--exclude', '-x', multiple=True, help='Regex of filenames that should be ignored')
@click.option('-v', '--verbose', count=True)
def check_copyright_command(reference, porcelain, separator, inverted, exclude, verbose):
    set_up_logging(verbose)
    check_copyright(reference, porcelain, separator, inverted, exclude)

# TODO remove when copyright package is split
@click.command(name='add-copyright', help='Add copyright statement to files.')
@click.argument('files', nargs=-1)
@click.option('--update-year', '-u', default=None, help='Update the year of the license with the year given')
@click.option('--year', '-y', help='copyright year specification (default: current year)')
@click.option('--license-type', '-t', type=click.Choice(['apache-2.0', 'gpl-3.0', 'mit'], case_sensitive=False), default='gpl-3.0', help='Type of license to use in the copyright (default: GPL3)')
@click.option('--owner', '-o', default='CERN for the benefit of the LHCb collaboration', help='rights owner (default: CERN for the benefit of the LHCb collaboration)')
@click.option('--license-fn', '-l', help='Name of the license file (default: COPYING)')
@click.option('--force', '-f', is_flag=True, help='add copyright also to non supported file types')
@click.option('-v', '--verbose', count=True)
def add_copyright_command(files, update_year, year, license_type, owner, license_fn, force, verbose):
    set_up_logging(verbose)
    if update_year is None:
        add_copyright(files, year, license_type, owner, license_fn, force)
    else:
        update_copyright_year(files, update_year)


lb_dev.add_command(check_for_license_command)
lb_dev.add_command(create_license_file_command)
lb_dev.add_command(check_copyright_command)
lb_dev.add_command(add_copyright_command)
