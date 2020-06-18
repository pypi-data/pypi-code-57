"""
celery-t

Usage:
    celery-t new <name> [--verbose]
    celery-t new <name> [-s|--skinos] [--flow] [--verbose]
    celery-t run
    celery-t -h
    celery-t --help
"""

from docopt import docopt

from celeryt import CeleryT


def main_celeryt():
    args = docopt(__doc__)

    if args['new']:
        name: str = args['<name>']
        skinos: bool = bool(args['-s'] or args['--skinos'])
        flow: bool = bool(args['--flow'])
        verbose: bool = bool(args['--verbose'])

        c: CeleryT = CeleryT(name=name, skinos=skinos, flow=flow, verbose=verbose)
        c.new()

    elif args['run']:
        CeleryT.run()
    elif args['-h'] or args['--help']:
        print(__doc__)
        exit()
    else:
        exit(__doc__)


if __name__ == '__main__':
    main_celeryt()
