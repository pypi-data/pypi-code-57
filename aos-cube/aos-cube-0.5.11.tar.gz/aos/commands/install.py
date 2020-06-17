import click
from aos.util import popen, locale_to_unicode
from aos.usertrace.do_report import set_op, report_op
from aos.managers.addon import AddonManager

@click.group(short_help="Install components or tools")
@click.pass_context
def cli(ctx):
    pass

'''
# Install command
#   - To install component without specified version: install comp <component>
#   - To install component with specified version: install comp <component=x.x.x>
#   - To install component no mater what old version is installed: install comp -f <comp>
'''
@cli.command("comp", short_help="Install components",\
             help="Install components.\n"\
                  "\nIf 'COMPONENTS' argument provided with version info "\
                  "(e.g. test=1.0.0), the specified version will be installed; "\
                  "otherwise, the latest version will be installed.\n"
                  "\nIf '-L' option provided, local package file will be used; "\
                  "otherwise, package source on remote server will be used.\n"\
                  "\nIf '-f' option provided, the components will be installed "\
                  "without asking for user confirm of removing old installed "\
                  "version or dependency installation.")
@click.argument("components", required=False, nargs=-1, metavar="[COMPONENTS...]")
@click.option("-f", "--force", is_flag=True, help="Force to install components")
@click.option("-L", "--location", type=click.STRING, nargs=1,\
              help="Specify the location of the package file to install")
def install_component(components, force, location):
    """  """
    am = AddonManager()

    args = []

    if components:
        args += components

    cmd_content = 'comp'
    if force:
        cmd_content += ' -f'
    if location:
        location = locale_to_unicode(location)
        cmd_content += ' -L'
    if args:
        cmd_content += ' ' + ' '.join(args)

    set_op(op='install', content=cmd_content)

    am.install(force, location, *args)

    set_op(result='success')
    report_op()

@cli.command("pypkg", short_help="Install pip pakcages")
@click.argument("pkgs", required=True, nargs=-1, metavar="[PACKAGES]...")
def install_pypkg(pkgs):
    """ Run pip process to install Python packages. """
    cmd = ["pip", "install", "--upgrade"]
    cmd_content = "install pypkg"

    for p in pkgs:
        cmd += [p]
        cmd_content += " %s" % p

    set_op(op='install', content=cmd_content)

    try:
        ret = popen(cmd)
        if ret != 0:
            cmd.insert(3, "--no-cache-dir")
            popen(cmd)
    except Exception as e:
        set_op(result='fail: ' + format(e))
        report_op()
        raise e

    set_op(result='success')
    report_op()
