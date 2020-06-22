import argparse


unhandled_exit = None


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value"
                                         % value)
    return ivalue


def pytest_addoption(parser):
    group = parser.getgroup('unhandled_exc_exit_code')
    group.addoption(
        '--unhandled-exc-exit-code',
        action='store',
        default=13,
        type=int,
        choices=range(0, 256),
        help='Use this exit code if there was an unhandled exception.'
    )


def pytest_exception_interact(node, call, report):
    """
    Set a different exit code on uncaught exceptions.
    """
    global unhandled_exit
    exctype, value, traceback = call.excinfo._excinfo

    if exctype == AssertionError:
        return report
    unhandled_exit = node.config.getoption('--unhandled-exc-exit-code')


def pytest_sessionfinish(session, exitstatus):
    if unhandled_exit is not None:
        session.exitstatus = unhandled_exit
