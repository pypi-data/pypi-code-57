import os, sys
import click
from aos.util import log, info, error, popen, Config, cd_aos_root, \
                     get_config_value, cd_app_root, locale_to_unicode
from aos.config import Global
from aos.constant import APP_CONFIG, AOS_SDK_PATH, NO_AOSSRC_HINT
from aos.usertrace.do_report import set_op, report_op

# Make command
@click.command("debug", short_help="Start gdb server")
@click.argument("target", required=False, nargs=-1)
@click.option("--work-path", "-w", help="Alternative work path if aos_sdk_path unavailable")
@click.option("--binaries-dir", "-b", help="Directory to store debug binaries")
@click.option("--start-client", "-c", is_flag=True, help="Start gdb client")
@click.option("--gdb-args", "-g", help="Arguments pass to gdb client")
def cli(target, work_path, binaries_dir, start_client, gdb_args):
    """ Initialize debug env for aos image. """
    from aos import __version__
    log('aos-cube version: %s\n' % __version__)

    debug_target = ' '.join(target)

    cmd_content = ''
    if target:
        cmd_content += debug_target
    if work_path:
        work_path = locale_to_unicode(work_path)
        cmd_content += " -w %s" % work_path
    if binaries_dir:
        binaries_dir = locale_to_unicode(binaries_dir)
        cmd_content += " -b %s" % binaries_dir
    if start_client:
        cmd_content += " -c"
    if gdb_args:
        cmd_content += " -g %s" + gdb_args

    set_op(op='debug', content=cmd_content)

    if work_path:
        if os.path.isdir(work_path):
            aos_path = work_path
        else:
            error("Can't find dir %s" % work_path)
    else:
        # debug from app project
        ret, orig_dir = cd_app_root()
        app_root_dir = os.getcwd()

        if ret == 'success':
            aos_path = os.environ.get("AOS_SDK_PATH")
            if not aos_path or not os.path.isdir(aos_path):
                log("Looks like AOS_SDK_PATH is not correctly set." )
                error(NO_AOSSRC_HINT)
            work_path = app_root_dir
            if os.path.isdir(orig_dir):
                os.chdir(orig_dir)
        else:
            #cd to aos root_dir
            if os.path.isdir(orig_dir):
                os.chdir(orig_dir)
            ret, original_dir = cd_aos_root()
            if ret != 'success':
                log("[INFO]: Not in AliOS-Things source code directory\n")
                log("[INFO]: Current directory is: '%s'\n" % original_dir)
                if os.path.isdir(original_dir):
                    os.chdir(original_dir)
                aos_path = os.environ.get("AOS_SDK_PATH")
                if not aos_path or not os.path.isdir(aos_path):
                    log("Looks like AOS_SDK_PATH is not correctly set." )
                    error(NO_AOSSRC_HINT)
                else:
                    log("[INFO]: Config Loading OK, use '%s' as sdk path\n" % aos_path)
            else:
                aos_path = os.getcwd()
                log("[INFO]: Currently in aos_sdk_path: '%s'\n" % os.getcwd())

    if work_path:
        work_path = locale_to_unicode(work_path)

    # read app & board from .config
    if debug_target == '':
        # check AliOS Things version
        if not aos_path or not os.path.exists(os.path.join(aos_path, 'build', 'Config.in')):
            error('Target invalid')

        board = None
        app = None
        log("[INFO]: Not set target, read target from .config\n")

        config_file = os.path.join(work_path if work_path else aos_path, '.config')
        if os.path.exists(config_file) == False:
            error('Config file NOT EXIST: %s\n' % config_file)

        board = get_config_value('AOS_BUILD_BOARD', config_file)
        app = get_config_value('AOS_BUILD_APP', config_file)

        if not app and not board:
            error('None target in %s\n' % config_file)
        debug_target = '%s@%s' % (app, board)

    elif '@' not in debug_target or len(debug_target.split('@')) != 2:
        error('Target invalid')

    if work_path and not os.path.isdir(work_path):
        error("Can't find dir %s" % work_path)

    if binaries_dir and not os.path.isdir(binaries_dir):
        error("Can't find dir %s" % binaries_dir)

    # for new board config
    if os.path.exists(os.path.join(aos_path, 'build', 'board_config', 'board_debug.py')):
        sys.path.append(os.path.join(aos_path, 'build', 'board_config'))
        try:
            from board_debug import aos_debug
        except Exception as err:
            info(err)
            info(Exception)
            error("Import board_debug.py: failed %s" % err)
    else:
        sys.path.append(os.path.join(aos_path, 'build', 'site_scons'))
        try:
            from scons_debug import aos_debug
        except Exception as err:
            info(err)
            info(Exception)
            error("Import scons_debug.py: failed %s" % err)

    click.secho("[INFO]: Target: %s" % debug_target, fg="green")
    aos_debug(debug_target, work_path, binaries_dir)

    set_op(result='success')
    report_op()
