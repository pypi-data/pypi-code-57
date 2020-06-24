import logging
from json import loads
from argparse import ArgumentParser, Namespace
from typing import Dict
from injectark import Injectark
from ... import __version__
from ...core import Config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class Shell:
    def __init__(self, config: Config, injector: Injectark) -> None:
        self.injector = injector
        self.config = config

    def run(self, args):
        namespace = self.parse(args)
        namespace.func(vars(namespace))

    def parse(self, args) -> Namespace:
        parser = ArgumentParser('Estimark')
        subparsers = parser.add_subparsers(dest='action')

        # Estimate
        estimate_parser = subparsers.add_parser('estimate')
        estimate_parser.add_argument('-s', '--states')
        estimate_parser.set_defaults(func=self.estimate)

        # Show
        show_parser = subparsers.add_parser('show')
        show_parser.add_argument('-m', '--model', default='task')
        show_parser.set_defaults(func=self.show)

        # Plot
        plot_parser = subparsers.add_parser('plot')
        plot_parser.add_argument('-t', '--type', default='gantt')
        plot_parser.add_argument('-c', '--context', default='{}',
                                 help='JSON plot parameters context.')
        plot_parser.set_defaults(func=self.plot)

        # Version
        version_parser = subparsers.add_parser('version')
        version_parser.set_defaults(func=self.version)

        if len(args) == 0:
            parser.print_help()
            parser.exit()

        return parser.parse_args(args)

    def estimate(self, options_dict: Dict[str, str]) -> None:
        logger.info('<< ESTIMATE >>')
        states = options_dict.get('states')
        if states:
            states = [state.strip() for state in states.split(',')]
        estimation_manager = self.injector['EstimationManager']
        estimation_manager.estimate(states)

    def show(self, options_dict: Dict[str, str]) -> None:
        logger.info('<< SHOW >>')
        estimark_informer = self.injector['EstimarkInformer']
        models = ['task', 'link', 'classifier', 'schedule', 'slot']
        model = options_dict.get('model')
        if model not in models:
            raise ValueError(
                f"The model should be one of: {', '.join(models)}")

        records = estimark_informer.search(model, [])

        logger.info(f'{model} records:')
        for record in records:
            logger.info(record)

    def plot(self, options_dict: Dict[str, str]):
        logger.info('<< PLOT >>')
        estimation_manager = self.injector['EstimationManager']
        type_ = options_dict['type']
        context = loads(options_dict['context'])
        estimation_manager.plot(type_, context)

    def version(self, options_dict: Dict[str, str]):
        logger.info('<< VERSION >>')
        logger.info(__version__)
