import os
import click

from aos.util import cd_aos_root, error, simple_error, get_locale, \
                     pqueryerr, popen, error, locale_to_unicode
from aos.constant import GEN_SAL_STAGING, GEN_MAL_STAGING, \
                         GEN_NEWPROJECT, GEN_APPSOURCE, \
                         GEN_NEW_COMPONENT, NO_SDK_HINT, \
                         NOT_INSIDE_SDK_HINT
from aos.usertrace.do_report import set_op, report_op

@click.group(short_help="Create project or component")
@click.pass_context
def cli(ctx):
    pass

# Create sal driver from template
@cli.command("saldriver", short_help="Create SAL driver from template")
@click.argument("drivername", metavar="[DRIVERNAME]")
@click.option("-m", "--mfname", help="The manufacturer of device")
@click.option("-t", "--devicetype", required=True,
              type=click.Choice(["gprs", "wifi", "lte", "nbiot", "eth", "other"]), help="The type of device")
@click.option("-a", "--author", help="The author of driver")
def create_sal_driver(drivername, mfname, devicetype, author):
    """ Create SAL driver staging code from template """

    args = [drivername]
    if mfname:
        args += ["-m%s" % mfname]
    if devicetype:
        args += ["-t%s" % devicetype]
    if author:
        args += ["-a%s" % author]

    cmd_content = 'saldriver ' + ' '.join(args)
    set_op(op='create', content=cmd_content)

    # Get aos source root directory
    ret, original_dir = cd_aos_root()
    if ret != 'success':
        error(NOT_INSIDE_SDK_HINT)

    source_root = os.path.abspath(os.getcwd())
    if os.path.isdir(original_dir):
        os.chdir(original_dir)

    # Run script GEN_SAL_STAGING
    gen_sal_staging = os.path.join(source_root, GEN_SAL_STAGING)
    if os.path.isfile(gen_sal_staging):
        cmd = ["python", gen_sal_staging] + list(args)
        ret, err = pqueryerr(cmd)
        if ret != 0:
            simple_error("Failed to generate SAL driver, error: %s" % err.decode(get_locale()))
    else:
        error("No %s found for current release!" % gen_sal_staging)

    set_op(result='success')
    report_op()

# Create mal driver from template
@cli.command("maldriver", short_help="Create MAL driver from template")
@click.argument("drivername", metavar="[DRIVERNAME]")
@click.option("-m", "--mfname", help="The manufacturer of device")
@click.option("-t", "--devicetype", required=True,
              type=click.Choice(["gprs", "wifi", "lte", "nbiot", "eth", "other"]), help="The type of device")
@click.option("-a", "--author", help="The author of driver")
def create_mal_driver(drivername, mfname, devicetype, author):
    """ Create MAL driver staging code from template """

    args = [drivername]
    if mfname:
        args += ["-m%s" % mfname]
    if devicetype:
        args += ["-t%s" % devicetype]
    if author:
        args += ["-a%s" % author]

    cmd_content = 'maldriver ' + ' '.join(args)
    set_op(op='create', content=cmd_content)

    # Get aos source root directory
    ret, original_dir = cd_aos_root()
    if ret != 'success':
        error(NOT_INSIDE_SDK_HINT)

    source_root = os.path.abspath(os.getcwd())
    if os.path.isdir(original_dir):
        os.chdir(original_dir)

    # Run script GEN_MAL_STAGING
    gen_mal_staging = os.path.join(source_root, GEN_MAL_STAGING)
    if os.path.isfile(gen_mal_staging):
        cmd = ["python", gen_mal_staging] + list(args)
        ret, err = pqueryerr(cmd)
        if ret != 0:
            simple_error("Failed to generate MAL driver, error: %s" % err.decode(get_locale()))
    else:
        error("No %s found for current release!" % gen_mal_staging)

    set_op(result='success')
    report_op()

# Create project
@cli.command("project", short_help="Create user project")
@click.argument("projectname", metavar="[PROJECTNAME]")
@click.option("-b", "--board", required=True, help="Board for creating project")
@click.option("-d", "--projectdir", help="The project directory")
@click.option("-t", "--templateapp", help="Template application for creating project")
def create_project(projectname, board, projectdir, templateapp):
    """ Create new project from template """
    args = [projectname]
    if board:
        args += ["-b%s" % board]
    if projectdir:
        args += ["-d%s" % projectdir]
    if templateapp:
        args += ["-t%s" % templateapp]

    cmd_content = 'project ' + ' '.join(args)
    set_op(op='create', content=cmd_content)

    if "AOS_SDK_PATH" not in os.environ:
        error(NO_SDK_HINT)
    else:
        aos_sdk_path = os.environ["AOS_SDK_PATH"]
        # AOS_SDK_PATH from environ may not unicode, so convert
        aos_sdk_path = locale_to_unicode(aos_sdk_path)

    aos_sdk_path = os.path.abspath(aos_sdk_path)
    gen_newproject = os.path.join(aos_sdk_path, GEN_NEWPROJECT)
    if os.path.isfile(gen_newproject):
        cmd = ["python", gen_newproject] + list(args)
        ret = popen(cmd)
        if ret != 0:
            error("Failed to generate project, errorcode: %d" % ret)
    else:
        error("No %s found for current release!" % gen_newproject)

    set_op(result='success')
    report_op()

# Create sources
@cli.command("source", short_help="Add component sources to build")
@click.argument("sourcelist", nargs=-1, metavar="<SOURCELIST>")
@click.option("-m", "--makefile", help="Target makefile to update")
def add_appsource(sourcelist, makefile):
    """ Add component sources to aos.mk """
    args = []

    if not sourcelist:
        return
    else:
        args += sourcelist

    if makefile:
        args += ["-m %s" % makefile]

    cmd_content = 'source ' + ' '.join(args)
    set_op(op='create', content=cmd_content)

    if "AOS_SDK_PATH" not in os.environ:
        error(NO_SDK_HINT)
    else:
        aos_sdk_path = os.environ["AOS_SDK_PATH"]

    aos_sdk_path = os.path.abspath(aos_sdk_path)
    script = os.path.join(aos_sdk_path, GEN_APPSOURCE)
    if os.path.isfile(script):
        cmd = ["python", script] + list(args)
        ret, err = pqueryerr(cmd)
        if ret != 0:
            simple_error("Failed to add source, error: %s" % err.decode(get_locale()))
    else:
        error("No %s found for current release!" % script)

    set_op(result='success')
    report_op()

# create new component
@cli.command("component", short_help="Create a new component by using templete.")
@click.argument("name", nargs=1, metavar="<name>")
@click.option("-t", "--comptype", required=True, type=click.Choice(["bus", "dm", "fs", "gui", "language", "linkkit", "network", "peripherals", "security", "service", "utility", "wireless", "generals"]), help="The type of the component")
@click.option("-m", "--mfname", help="The manufacturer of the component")
@click.option("-a", "--author", help="The author of the component")
def create_component(name, comptype, mfname, author):
    """ Create a new component by using templete """
    args = [name, "-t%s" % comptype]
    if mfname:
        args += ["-m%s" % mfname]
    if author:
        args += ["-a%s" % author]

    cmd_content = 'component ' + ' '.join(args)
    set_op(op='create', content=cmd_content)

    # Get aos source root directory
    ret, original_dir = cd_aos_root()
    if ret != 'success':
        error(NOT_INSIDE_SDK_HINT)

    source_root = os.path.abspath(os.getcwd())
    if os.path.isdir(original_dir):
        os.chdir(original_dir)

    # Run script GEN_SAL_STAGING
    gen_new_component = os.path.join(source_root, GEN_NEW_COMPONENT)
    if os.path.isfile(gen_new_component):
        cmd = ["python", gen_new_component] + list(args)
        ret, err = pqueryerr(cmd)
        if ret != 0:
            simple_error("Failed to create component, error: %s" % err.decode(get_locale()))
    else:
        error("No %s found for current release!" % gen_mal_staging)

    set_op(result='success')
    report_op()
