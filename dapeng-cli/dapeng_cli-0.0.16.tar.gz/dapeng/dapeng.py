from __future__ import print_function
import os
import uuid
import pika
import socket
import json
import threading
import time
import logging
import click

from .util import upload_file
from .version import VERSION
from .dapeng_api import DapengAPI, JobNotExists

LOGGER = logging.getLogger(__name__)
logging.getLogger("pika").setLevel(logging.ERROR)

BROKER_SERVER_URL = 'amqp://public:Happy123@10.192.225.185'
UNIQUE_ID = uuid.uuid4()
QUEUE_NAME = "dpc-lite.{}.{}".format(socket.gethostname(), UNIQUE_ID)


class TestcaseCheckThread(threading.Thread):
    """Background thread to periodly check tasks status.
    Default interval 60 seconds.
    """
    def __init__(self, case_id, channel, sleep_interval=60):
        super(TestcaseCheckThread, self).__init__()
        self._kill = threading.Event()
        self._interval = sleep_interval
        self.case_id = case_id
        self.channel = channel
        self.max_loop = 60

    def run(self):
        cnt = 0
        while True:
            case_info = DapengAPI.get_testcase(self.case_id)
            cnt += 1
            if cnt >= self.max_loop:
                LOGGER.error("Exceed max timeout: %s, exit!", (self.max_loop * self._interval))
                if self.channel:
                    self.channel.stop_consuming()
                break

            if not case_info:
                continue

            status = case_info['status'].lower()
            LOGGER.debug("checker[%s/%s], %s", cnt, self.max_loop, status)
            if status == 'finished':
                LOGGER.info("Test execution [Finish]")
                if self.channel:
                    self.channel.stop_consuming()
                    break

            # If no kill signal is set, sleep for the interval,
            # If kill signal comes in while sleeping, immediately
            #  wake up and handle
            is_killed = self._kill.wait(self._interval)
            if is_killed:
                break

    def kill(self):
        self._kill.set()

class JobListener(object):
    """Listen job status and logs"""

    def __init__(self, job_id, case_id=None, sync_log=True):
        self.job_id = job_id
        self.case_id = case_id
        self.channel = None
        self.connection = None
        self.consumer_tag = None
        self.case_info = None
        self.checker = None
        self.start_checker = True
        self.sync_log = sync_log

    def _connect_broker(self):
        LOGGER.debug("start to connect to broker")
        binding_key = "*.%s" % self.case_id
        params = pika.URLParameters(BROKER_SERVER_URL)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

        # declare msg queue for current consumer
        self.channel.queue_declare(QUEUE_NAME, auto_delete=True)
        # bind to dapeng state exchange
        self.channel.queue_bind(
            exchange=DapengAPI.DAPENG_STATE_EXCHANGE,
            queue=QUEUE_NAME,
            routing_key=binding_key)

        if self.sync_log:
            # declare log exchange
            self.channel.exchange_declare(
                exchange=DapengAPI.DAPENG_LOG_EXCHANGE,
                exchange_type='topic')
            # bind to dapeng log exchange
            self.channel.queue_bind(
                exchange=DapengAPI.DAPENG_LOG_EXCHANGE,
                queue=QUEUE_NAME,
                routing_key=binding_key)

        LOGGER.debug("connected!")

    def do_query(self):
        if self.job_id and not self.case_id:
            LOGGER.debug("query case id")
            job_info = DapengAPI.get_job(self.job_id, True)
            self.case_id = job_info["detail"][0]["id"]

        assert self.case_id
        self.case_info = DapengAPI.get_testcase(self.case_id)

    def _do_work(self, ch, method, properties, body):
        # handle task status and result
        if method.routing_key.startswith("state"):
            data = json.loads(body)
            status = data.get("status")
            if status:
                status = DapengAPI.DAPENG_TASK_STATUS.get(int(status)).lower()
                self.case_info["status"] = status
                LOGGER.info(" => Task is %s", self.status)

            self.case_info["runresult"] = data.get("result_text")
            LOGGER.debug('Conmuer result: %s', self.case_info["runresult"])

            if self.status == "finished" and self.case_info.get("runresult"):
                ch.stop_consuming()
        else:
            # print logs
            LOGGER.info(body.decode())

    def start_listen(self):
        self.do_query()
        if self.status == "finished":
            LOGGER.debug("job is finised, won't connect!")
            return

        self._connect_broker()
        if not self.connection:
            return

        LOGGER.info('\n------------ Start Listener. To stop test press CTRL+C ------------')
        if self.status:
            LOGGER.info(" => Task is %s", self.status)

        if self.start_checker:
            self.checker = TestcaseCheckThread(self.case_id, self.channel)
            self.checker.start()

        self.consumer_tag = self.channel.basic_consume(
            queue=QUEUE_NAME, on_message_callback=self._do_work, auto_ack=True)
        self.channel.start_consuming()

    def force_quit(self):
        if self.channel:
            self.channel.stop_consuming()
        try:
            self.do_query()
            if self.status != "finished":
                DapengAPI.stop_job(self.job_id)
        except JobNotExists:
            pass

    @property
    def test_result(self):
        if self.status != "finished":
            self.do_query()
        return self.case_info["runresult"]

    @property
    def status(self):
        if self.case_info:
            status = self.case_info['status'].lower()
            return status
        return ""

    def close(self):
        if self.checker:
            LOGGER.debug("cancel checker")
            self.checker.kill()

        if self.channel:
            LOGGER.debug("close connection")
            self.channel.basic_cancel(self.consumer_tag)
            # self.channel.queue_delete(QUEUE_NAME)
            self.channel.close()


def create_dapeng_job(job_config=None, **kwargs):
    image_file = kwargs.get("file")
    if image_file and os.path.exists(image_file):
        image_url = upload_file(kwargs.get("board"), image_file)
    else:
        image_url = image_file

    LOGGER.info("Start to submit job.")
    if not job_config:
        job_config = {
            "header": {
                "suite": kwargs.get("suite"),
                "priority": kwargs.get("priority"),
                "isonthefly": True,
                "routing": kwargs.get("routing"),
                "runaccesstokenlist": kwargs.get("tokens"),
                "app_data_version": kwargs.get("app_data")
            },
            "detail": [
                {
                    "name": kwargs.get("appname"),
                    "compiler": kwargs.get("compiler"),
                    "platform": kwargs.get("board"),
                    "target": kwargs.get("target"),
                    "bin": image_url,
                    "category": kwargs.get("category"),
                }
            ]
        }
    if "name" not in job_config["header"]:
        job_config["header"]["name"] = str(UNIQUE_ID)
    LOGGER.info(json.dumps(job_config['detail'][0], indent=2))
    job_id = DapengAPI.submit_job(job_config)
    job_lis = JobListener(job_id, sync_log=kwargs.get("sync_log", True))
    try:
        job_lis.start_listen()
    except KeyboardInterrupt:
        job_lis.force_quit()
    finally:
        job_lis.close()

    result = job_lis.test_result
    text = "=========== Test result: %s ===========" % result
    if result in ("Pass", "Semi Auto Pass"):
        click.secho(text, fg="green")
        exit(0)
    else:
        click.secho(text, fg="red")
        exit(1)


@click.group(invoke_without_command=True)
@click.option('-log', type=click.Path(), help='log console output to file')
@click.option('--debug', is_flag=True, help='enable debug level')
@click.pass_context
def main(ctx, log, debug):
    if debug:
        level = logging.DEBUG
        format = "debug: %(message)s"
    else:
        level = logging.INFO
        format = "%(message)s"

    logging.basicConfig(level=level, format=format)
    # enable file logging
    if log:
        fh = logging.FileHandler(log)
        fh.setLevel(level)
        LOGGER.addHandler(fh)
    LOGGER.info("Dapeng CLI [Version: %s]\n", VERSION)


@main.command(help="rerun dapeng task")
@click.option('-id', prompt='case id', help='case id')
# @click.option('-a', '--app_data', help='set branch for app_data')
def rerun(id):
    case_info = DapengAPI.get_testcase(id)
    job_id = case_info["campaign_id"]
    DapengAPI.rerun_testcase(job_id, id)
    job_lis = JobListener(job_id, id)
    job_lis.start_checker = False
    try:
        time.sleep(3)
        job_lis.start_listen()
    except KeyboardInterrupt:
        job_lis.force_quit()
    finally:
        job_lis.close()

    result = job_lis.test_result
    text = "=========== Test result: %s ===========" % result
    if result == "Pass":
        click.secho(text, fg="green")
        exit(0)
    else:
        click.secho(text, fg="red")
        exit(1)

@main.command(help="verify dapeng tasks")
@click.option('-id', prompt='case id', help='case id')
@click.option('-a', '--app_data', help='set branch for app_data')
@click.option('-c', '--compiler', help='overried compiler to search, only work with --search')
@click.option('-t', '--target', help='overried target to search, only work with --search')
@click.option("--reserve/--no-reserve", default=True, help='search reserved jobs, only work with --search')
@click.option('--search', is_flag=True, help="search last passed result according the given case")
@click.option('-dpserver', default="production", help='dapeng instance: production/stage.')
def verify(id, app_data, compiler, target, reserve, search, dpserver):
    DapengAPI.setup_instance(dpserver)
    taskinfo = DapengAPI.get_testcase(id)
    if not taskinfo:
        click.secho("invalid task id")
        exit(1)

    if not search:
        click.echo("Verify case: %s" % id)
    else:
        params_to_query = {
            "compiler": taskinfo["compiler"],
            "platform": taskinfo["platform"],
            "target": taskinfo["target"],
            "testcase": taskinfo["test_case"],
            "id": id
        }

        if compiler:
            params_to_query["compiler"] = compiler

        if target:
            params_to_query["target"] = target

        if reserve:
            params_to_query["reserved"] = 'true'

        taskinfo = DapengAPI.get_testcase(id, params_to_query)
        if not taskinfo:
            click.secho("Not found last successful run!", fg="red")
            exit(1)

        click.secho("Found last successful run: {}.".format(taskinfo["id"]), fg="bright_blue")
        click.secho("  date:     %s" % taskinfo['runstarttime'])
        click.secho("  link:     http://dapeng/dapeng/information/requestdetail/{}/".format(taskinfo["id"]))
        click.secho("  source:   %s" % taskinfo["branch"])
        click.secho("  project:  %s" % taskinfo["project"])
        print("-----------------------------------")

    if taskinfo["bin"] in (None, "none", ""):
        click.secho("Invalid Task binary, please check your task", fg="red")
        exit(1)

    job_config = {
        "header": {
            "suite": "ksdk",
            "priority": 3,
            "isonthefly": True,
            "routing": True,
            "runaccesstokenlist": "TEST_RUN,TEST_RUN_68,TEST_RUN_72,TEST_RUN_654",
        },
        "detail": [
            {
                "name": taskinfo["test_case"],
                "compiler": taskinfo["compiler"],
                "platform": taskinfo["platform"],
                "target": taskinfo["target"],
                "bin": taskinfo["bin"],
                "category": taskinfo["category"],
            }
        ]
    }

    if app_data:
        click.secho("AppData Branch:  %s" % app_data)
        job_config["header"]["app_data_version"] = app_data

    create_dapeng_job(job_config=job_config)


def validate_file_option(ctx, param, value):
    if value.startswith('http://') or value.startswith('ftp://'):
        pass
    elif not os.path.exists(value):
        raise click.BadParameter('File does not exists![%s]' % value)
    return value

@main.command(help="run a test on remote")
@click.option(
    '-f', '--file', callback=validate_file_option,
    required=True, help="image file, local file or file link")
@click.option('-b', '--board', required=True, help="board name")
@click.option('-n', '--appname', default="hello_world", help="app name")
@click.option('-c', '--compiler', default="armgcc", help="compiler name")
@click.option(
    '-t', '--target', default="release",
    help="app project target: debug/release")
@click.option(
    '-P', '--priority', default=3, type=click.IntRange(1, 6),
    help="task priority")
@click.option('-S', '--suite',
              default='ksdk',
              type=click.Choice(['ksdk', 'zephyr_test', 'ksdk_wireless']),
              help="suite name, default ksdk")
@click.option(
    '-C', '--category', default="demo_apps",
    help="sdk category, like demo_apps")
@click.option(
    "-A", "--app_data", default="dev",
    help="set branch for app_data")
@click.option(
    "-T", "--tokens",
    default="TEST_RUN,TEST_RUN_68,TEST_RUN_72,TEST_RUN_654,TEST_RUN_A1,TEST_RUN_NPW",
    help="board tokens")
@click.option(
    '--routing/--no-routing', default=True,
    help="use case routing policy")
@click.option(
    "-timeout",
    help="set job timeout in seconds, default is None(12minutes)")
@click.option(
    "--sync-log/--no-sync-log", default=True,
    help="sync remote logs in time")
@click.option(
    '-dpserver', default="production",
    help='dapeng instance: production/stage.')
def test(file, board, appname, compiler, target, priority, suite,
         category, app_data, tokens, routing, timeout, sync_log, dpserver):
    DapengAPI.setup_instance(dpserver)
    create_dapeng_job(
        board=board, compiler=compiler, target=target, appname=appname,
        file=file, routing=routing, priority=priority, suite=suite,
        category=category, app_data=app_data, tokens=tokens, timeout=timeout,
        sync_log=sync_log
    )


@main.command(help="create new jobs on Dapeng")
@click.option('-j', '--jsonfile', required=True, type=click.Path(exists=True), help="Use a JSON config file")
@click.option('-dpserver', default="production", help='dapeng instance: production/stage.')
def new(jsonfile, dpserver):
    DapengAPI.setup_instance(dpserver)
    with open(jsonfile) as fobj:
        job_config = json.load(fobj)
    DapengAPI.submit_job(job_config)


if __name__ == "__main__":
    main()
