import os

import click
from sumoappclient.common.logger import get_logger
from sumoapputils.common.utils import touch, USER

logger = get_logger(__name__, LOG_FILEPATH="/tmp/sumoapptestutils.log", LOG_LEVEL=os.environ.get("LOG_LEVEL", "INFO"))

@click.group()
def initializeapp():
    pass

@initializeapp.command(help="For generating initial structure of app folder")
@click.option('-a', '--appname', required=True, help='Sets app name')
@click.option('-t', '--target_directory', type=click.Path(dir_okay=True, file_okay=False), default=os.getcwd(), required=True, help='Sets dir name')
def init(appname, target_directory):
    app_folder = target_directory
    if not os.path.isdir(app_folder):
        os.mkdir(app_folder)

    file_name = appname.replace(" ", '').replace("_", "") + ".json"
    touch(os.path.join(app_folder, file_name))
    if USER.is_partner:
        res_folder = os.path.join(app_folder, "resources")
        os.mkdir(res_folder)
        os.mkdir(os.path.join(res_folder, "screenshots"))
        os.mkdir(os.path.join(res_folder, "icon"))
        os.mkdir(os.path.join(res_folder, "logs"))