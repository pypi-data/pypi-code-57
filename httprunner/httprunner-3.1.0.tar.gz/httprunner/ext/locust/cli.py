import multiprocessing
import sys

from httprunner import __version__
from httprunner import logger
from httprunner.utils import init_sentry_sdk

init_sentry_sdk()


def start_locust_main():
    from locust import main as locust_main

    locust_main.main()


def start_master(sys_argv):
    sys_argv.append("--master")
    sys.argv = sys_argv
    start_locust_main()


def start_slave(sys_argv):
    if "--slave" not in sys_argv:
        sys_argv.extend(["--slave"])

    sys.argv = sys_argv
    start_locust_main()


def run_locusts_with_processes(sys_argv, processes_count):
    processes = []
    manager = multiprocessing.Manager()

    for _ in range(processes_count):
        p_slave = multiprocessing.Process(target=start_slave, args=(sys_argv,))
        p_slave.daemon = True
        p_slave.start()
        processes.append(p_slave)

    try:
        if "--slave" in sys_argv:
            [process.join() for process in processes]
        else:
            start_master(sys_argv)
    except KeyboardInterrupt:
        manager.shutdown()


def main():
    """ Performance test with locust: parse command line options and run commands.
    """
    print("HttpRunner version: {}".format(__version__))
    sys.argv[0] = "locust"
    if len(sys.argv) == 1:
        sys.argv.extend(["-h"])

    if sys.argv[1] in ["-h", "--help", "-V", "--version"]:
        start_locust_main()

    def get_arg_index(*target_args):
        for arg in target_args:
            if arg not in sys.argv:
                continue

            return sys.argv.index(arg) + 1

        return None

    # set logging level
    loglevel_index = get_arg_index("-L", "--loglevel")
    if loglevel_index and loglevel_index < len(sys.argv):
        loglevel = sys.argv[loglevel_index]
    else:
        # default
        loglevel = "WARNING"

    logger.setup_logger(loglevel)

    # get testcase file path
    try:
        testcase_index = get_arg_index("-f", "--locustfile")
        assert testcase_index and testcase_index < len(sys.argv)
    except AssertionError:
        print("Testcase file is not specified, exit.")
        sys.exit(1)

    testcase_file_path = sys.argv[testcase_index]
    sys.argv[testcase_index] = parse_locustfile(testcase_file_path)

    if "--processes" in sys.argv:
        """ locusts -f locustfile.py --processes 4
        """
        if "--no-web" in sys.argv:
            logger.log_error("conflict parameter args: --processes & --no-web. \nexit.")
            sys.exit(1)

        processes_index = sys.argv.index("--processes")
        processes_count_index = processes_index + 1
        if processes_count_index >= len(sys.argv):
            """ do not specify processes count explicitly
                locusts -f locustfile.py --processes
            """
            processes_count = multiprocessing.cpu_count()
            logger.log_warning(
                "processes count not specified, use {} by default.".format(
                    processes_count
                )
            )
        else:
            try:
                """ locusts -f locustfile.py --processes 4 """
                processes_count = int(sys.argv[processes_count_index])
                sys.argv.pop(processes_count_index)
            except ValueError:
                """ locusts -f locustfile.py --processes -P 8888 """
                processes_count = multiprocessing.cpu_count()
                logger.log_warning(
                    "processes count not specified, use {} by default.".format(
                        processes_count
                    )
                )

        sys.argv.pop(processes_index)
        run_locusts_with_processes(sys.argv, processes_count)
    else:
        start_locust_main()
