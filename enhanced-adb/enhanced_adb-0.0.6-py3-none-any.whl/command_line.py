import argparse
import logging
import sys
from logging import basicConfig, CRITICAL, ERROR, WARNING, INFO, DEBUG

from .apk_repo.repo import Repo
from rich.logging import RichHandler


def inspect_apk(args):
    from .inspect.inspecter import do_inspect
    result = do_inspect(args.path)

    if result is None:
        return False

    from .inspect.output import rich_text
    rich_text(result, args)
    return True


def repo(args):
    logging.debug("run repo")
    r = Repo()
    r.ls()

    return True


def event(args):
    from .analyze import analyze_catcher
    analyze_catcher.show_analyze(args)


def foo(args):
    from .foo import fooooo
    fooooo.do_test(args)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    from rich.traceback import install
    install()

    parser = argparse.ArgumentParser("eadb")

    parser.add_argument("-v", "--verbose", action="count")
    parser.add_argument("-q", "--quiet", action="count")

    subparsers = parser.add_subparsers(title='support commands')

    # inspect
    inspect = subparsers.add_parser('inspect', help='inspect apk file, usage: eadb inspect path/to/apk')
    inspect.add_argument('path', metavar='APK_PATH', help='the apk path')
    inspect.add_argument('-m', "--manifest", action='count', help="show manifest content")
    inspect.add_argument('-p', "--properties", action='count', help="show properties content")

    inspect.set_defaults(func=inspect_apk)

    # analyze catcher
    event_parser = subparsers.add_parser('event')
    event_parser.add_argument("--no-adsdk", action='store_true')
    event_parser.add_argument("--search", nargs='?')
    event_parser.set_defaults(func=event)

    # foo
    foo_parser = subparsers.add_parser('foo')
    foo_parser.add_argument("interval", type=int, nargs='?')
    foo_parser.add_argument("--times", metavar="times", type=int, default=999999)
    foo_parser.set_defaults(func=foo)

    # repo
    repository = subparsers.add_parser('repo', help="apk repository")
    repository.set_defaults(func=repo)

    args = parser.parse_args(argv)

    log_level = WARNING

    if args.verbose:
        log_level = DEBUG

    if args.quiet:
        log_level = CRITICAL

    FORMAT = "%(message)s"
    basicConfig(level=log_level, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_usage()


if __name__ == '__main__':
    main()
