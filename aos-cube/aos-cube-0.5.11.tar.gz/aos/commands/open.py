import os, sys
import click

from aos.util import error, simple_error, pqueryerr, locale_to_unicode, get_locale
from aos.usertrace.do_report import set_op, report_op
from aos.constant import GEN_NEWPROJECT, NO_SDK_HINT

# open command
@click.command("open", short_help="Open an example project",
               help="Open the example project of a specified "
                    "component on a specified board.")
@click.argument("compname", required=True, nargs=1, metavar="<component_name>")
@click.option("-b", "--board", required=True, help="Board for creating project")
@click.option("-d", "--projectdir", help="The project directory")
def cli(compname, board, projectdir):
    """ Open the example project of a specified component on a specified board.

        Show more ARGS with: $ aos open help
    """

    args = [compname, '-b ' + board]

    if projectdir:
        projectdir = locale_to_unicode(projectdir)
        args += ['-d ' + projectdir]

    cmd_content = ' '.join(args)
    set_op(op='open', content=cmd_content)

    if "AOS_SDK_PATH" not in os.environ:
        error(NO_SDK_HINT)
    else:
        aos_sdk_path = os.environ["AOS_SDK_PATH"]

    aos_sdk_path = locale_to_unicode(os.path.abspath(aos_sdk_path))

    # run get_newproject script
    new_project_args = ["-b%s" % board, "-t%s" % (compname + '_app'), compname + 'app']
    if projectdir:
        new_project_args += ["-d%s" % projectdir]
    gen_newproject = os.path.join(aos_sdk_path, GEN_NEWPROJECT)
    if os.path.isfile(gen_newproject):
        cmd = ["python", gen_newproject] + list(new_project_args)
        ret, err = pqueryerr(cmd)
        if ret != 0:
            simple_error("Failed to open example project, error: %s" % err.decode(get_locale()))
    else:
        error("No %s found for current release!" % gen_newproject)

    '''
    # run aos create project command
    try:
        cmd = ["aos", "create", "project", "-b " + board, "-d " + projectdir, "-t " + compname, "compname"]
        popen(cmd)
    except Exception as e:
        error("Failed to open example project for %s, error message: %s" % (compname, format(e)))
    '''

    set_op(result='success')
    report_op()
