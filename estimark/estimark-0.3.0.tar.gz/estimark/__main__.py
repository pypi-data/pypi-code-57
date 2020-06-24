"""
Authark entrypoint
"""

import os
import sys
import logging
from json import loads
from pathlib import Path
from typing import List
from injectark import Injectark
from .core import Config, PRODUCTION_CONFIG
from .factories import factory_builder, strategy_builder
from .presenters.shell import Shell


def main(args: List[str] = None):  # pragma: no cover
    args = args or sys.argv[1:]
    config_path = Path(os.environ.get('ESTIMARK_CONFIG', 'config.json'))
    config = loads(config_path.read_text()) if config_path.is_file() else {}
    config: Config = {**PRODUCTION_CONFIG, **config}

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                        format='%(message)s')

    strategy = strategy_builder.build(config['strategies'])
    factory = factory_builder.build(config)

    injector = Injectark(strategy, factory)

    Shell(config, injector).run(args or [])


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
