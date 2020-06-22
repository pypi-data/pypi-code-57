from argparse import ArgumentParser
from typing import Optional

import jinja2

from .internal import util as fyoo_util
from .internal import template as fyoo_template


class _FyooSecretParser(ArgumentParser):

    def __init__(self, *args, parent_parser: Optional = None, **kwargs) -> None:
        if not parent_parser:
            raise ValueError("'parent_parser' not provided")
        self.parent_parser = parent_parser
        super().__init__(*args, add_help=False, **kwargs)

    def add_argument(self, *args, **kwargs):
        self.parent_parser.add_argument(*args, **kwargs)
        super().add_argument(*args, **kwargs)


class FyooParser(ArgumentParser):

    """
    Just like an ArgumentParser, but adds a few hidden arguments. These
    hidden arguments will not show up in returned namespaces, rather they
    will simply tweak the full namespace before it comes back.
    """

    FYOO_CONTEXT_HELP = 'Pass in a json or yaml string. Multi-argument (can pass multiple times)'
    FYOO_CONTEXT_FORMAT_HELP = 'Context formatter to use. json, yaml, or auto (default: auto)'
    FYOO_SET_HELP = 'Set a single context variable. Multi-argument (can pass multiple times)'
    FYOO_JINJA_EXTENSION = 'Add a jinja2 extension to load at runtime. Multi-argument (can pass multiple times)'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fyoo_secret_parser = _FyooSecretParser(parent_parser=self)
        self.fyoo_secret_parser.add_argument(
            '-fc', '--fyoo-context', action='append', help=FyooParser.FYOO_CONTEXT_HELP)
        self.fyoo_secret_parser.add_argument(
            '-ff', '--fyoo-context-format', help=FyooParser.FYOO_CONTEXT_FORMAT_HELP)
        self.fyoo_secret_parser.add_argument(
            '-fs', '--fyoo-set', action='append', type=fyoo_util.set_type, help=FyooParser.FYOO_SET_HELP)
        self.fyoo_secret_parser.add_argument(
            '-fj', '--fyoo-jinja-extension', action='append', help=FyooParser.FYOO_JINJA_EXTENSION)

    def parse_known_args(self, args=None, namespace=None):
        secret_known_args, secret_unknown_args = \
            self.fyoo_secret_parser.parse_known_args(args=args, namespace=namespace)

        jinja_env = jinja2.Environment()
        jinja_env.add_extension(fyoo_template.FyooDatetimeExtension)
        jinja_env.add_extension(fyoo_template.FyooEnvExtension)
        jinja_env.add_extension(fyoo_template.FyooThrowExtension)
        if secret_known_args.fyoo_jinja_extension:
            for fyoo_jinja_extension in secret_known_args.fyoo_jinja_extension:
                jinja_env.add_extension(fyoo_jinja_extension)

        # Remove actions from current parser, as they're passed to fyoo inner secret-parser
        # pylint: disable=protected-access
        secret_action_dests = {action.dest for action in self.fyoo_secret_parser._actions}
        for action in list(self._actions):  # Need list to remove unstable iterable
            if action.dest in secret_action_dests:
                self._remove_action(action)

        template_context = fyoo_util.generate_fyoo_context(
            secret_known_args.fyoo_context_format,
            secret_known_args.fyoo_context,
            secret_known_args.fyoo_set,
        )
        if secret_known_args.fyoo_set:
            for key, value in secret_known_args.fyoo_set:
                template_context[key] = value
        jinja_env.globals.update(template_context)

        known_args, unknown_args = super().parse_known_args(
            # Only use args that secret parser did not parse
            args=[
                jinja_env.from_string(arg).render()
                for arg in secret_unknown_args
            ],
            # But use initial optional namespace object
            namespace=namespace,
        )

        return known_args, unknown_args
