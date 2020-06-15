# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import re

from prompt_toolkit.completion import Completer, Completion
import requests
from devyzer.utils import TextUtils
from devyzer.constants import AUTOCOMPLETE_ENDPOINT


class DevyzerCompleter(Completer):
    """Completer for Devyzer
    """

    def __init__(self,
                 all_commands,
                 config,
                 config_obj,
                 log_exception,
                 fuzzy_match=False,
                 shortcut_match=False):
        """Initializes AwsCompleter.

        Args:
            * all_commands: A list of all commands, sub_commands, options, etc
                from data/SOURCES.txt.
            * config: An instance of Config.
            * config_obj: An instance of ConfigObj, reads from ~/.devyzer.rc.
            * log_exception: A callable log_exception from SawsLogger.
            * fuzzy_match: A boolean that determines whether to use
                fuzzy matching.
            * shortcut_match: A boolean that determines whether to
                match shortcuts.

        Returns:
            None.
        """
        self.aws_completions = set()
        self.all_commands = all_commands
        self.config = config
        self.config_obj = config_obj
        self.log_exception = log_exception
        self.text_utils = TextUtils()
        self.fuzzy_match = fuzzy_match
        self.shortcut_match = shortcut_match
        self.shortcuts = []

    def get_completions(self, document, complete_event):
        """Get completions for the current scope.

        Args:
            * document: An instance of prompt_toolkit's Document.
            * _: An instance of prompt_toolkit's CompleteEvent (not used).

        Returns:
            A generator of prompt_toolkit's Completion objects, containing
            matched completions.
        """
        URL = AUTOCOMPLETE_ENDPOINT + "/suggest"
        PARAMS = {'query': document.text}
        # Get list of words.
        result = requests.get(url=URL, params=PARAMS)
        data = result.json()
        # Get word/text before cursor.
        word_before_cursor = document.get_word_before_cursor()

        for suggest in data["suggestions"]:
            yield Completion(suggest, -len(word_before_cursor))
