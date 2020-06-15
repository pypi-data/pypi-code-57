# -*- coding: utf-8


from pygments.lexer import RegexLexer
from pygments.lexer import words
from pygments.token import Name

from devyzer.config import Config


class CommandLexer(RegexLexer):
    """Provides highlighting for commands.

    Attributes:
        * config: An instance of Config.
        * config_obj: An instance of ConfigObj.
        * shortcuts: An OrderedDict containing the shortcut commands as the
            keys and their corresponding full commands as the values.
        * shortcut_tokens: A list containing words for each shortcut key:
            key: 'aws ec2 ls' -> shortcut_tokens: ['aws', 'ec2', 'ls'].
        * commands: A tuple, where each tuple element is a list of:
            * commands
            * sub_commands
            * global_options
            * resource_options
        * tokens: A dictionary of pygments tokens.
    """

    config = Config()
    config_obj = config.read_configuration()
    shortcuts = {}
    shortcut_tokens = []
    for shortcut in shortcuts.keys():
        tokens = shortcut.split()
        for token in tokens:
            shortcut_tokens.append(token)

    commands = []

    tokens = {
        'root': [
            (words(
                tuple(shortcut_tokens),
                prefix=r'',
                suffix=r'\b'),
             Name.Exception),
        ]
    }
