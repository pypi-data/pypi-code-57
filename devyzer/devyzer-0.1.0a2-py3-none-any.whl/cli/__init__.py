# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import os
import platform
import subprocess
import traceback

import click
import requests
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import ThreadedCompleter
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.filters import HasFocus, IsDone
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding.key_processor import KeyPress
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.processors import \
    HighlightMatchingBracketProcessor, ConditionalProcessor
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.shortcuts import PromptSession

from devyzer.constants import AUTOCOMPLETE_ENDPOINT
from devyzer.cli.completer import DevyzerCompleter
from devyzer.cli.keys import KeyManager
from devyzer.cli.lexer import CommandLexer
from devyzer.cli.style import StyleFactory
from devyzer.cli.toolbar import Toolbar
from devyzer.config import Config
from devyzer.state import SessionState


class Cli(object):
    PYGMENTS_CMD = ' | pygmentize -l json'

    def __init__(self, logger):
        self._prompt = None
        self.config = Config()
        self.config_obj = self.config.read_configuration()
        self.theme = self.config_obj[self.config.MAIN][self.config.THEME]
        self.logger = logger

        self.all_commands = []
        self.commands = []
        self.sub_commands = []
        fuzzy_match = self.get_fuzzy_match()
        shortcut_match = self.get_shortcut_match()

        self.completer = DevyzerCompleter(
            self.all_commands,
            self.config,
            self.config_obj,
            self.log_exception,
            fuzzy_match=fuzzy_match,
            shortcut_match=shortcut_match)

        self._create_cli()

    def prompt(self):
        with patch_stdout():
            return self._prompt.prompt()

    def log_exception(self, e, traceback, echo=False):
        """Logs the exception and traceback to the log file ~/.saws.log.

        Args:
            * e: A Exception that specifies the exception.
            * traceback: A Traceback that specifies the traceback.
            * echo: A boolean that specifies whether to echo the exception
                to the console using click.

        Returns:
            None.
        """
        self.logger.debug('exception: %r.', str(e))
        self.logger.error("traceback: %r", traceback.format_exc())
        if echo:
            click.secho(str(e), fg='red')

    def colorize_output(self, text):
        """Highlights output with pygments.

        Only highlights the output if all of the following conditions are True:

        * The color option is enabled
        * The command will be handled by the `devyzer cli`
        * The text does not contain the `configure` command
        * The text does not contain the `help` command, which already does
            output highlighting

        Args:
            * text: A string that represents the input command text.

        Returns:
            A string that represents:
                * The original command text if no highlighting was performed.
                * The pygments highlighted command text otherwise.
        """
        stripped_text = text.strip()
        if not self.get_color() or stripped_text == '':
            return text

        excludes = ['|']
        if not any(substring in stripped_text for substring in excludes):
            return text.strip() + self.PYGMENTS_CMD
        else:
            return text

    def set_color(self, color):
        """Setter for color output mode.

        Used by prompt_toolkit's KeyBindingManager.
        KeyBindingManager expects this function to be callable so we can't use
        @property and @attrib.setter.

        Args:
            * color: A boolean that represents the color flag.

        Returns:
            None.
        """
        self.config_obj[self.config.MAIN][self.config.COLOR] = color

    def get_color(self):
        """Getter for color output mode.

        Used by prompt_toolkit's KeyBindingManager.
        KeyBindingManager expects this function to be callable so we can't use
        @property and @attrib.setter.

        Args:
            * None.

        Returns:
            A boolean that represents the color flag.
        """
        return self.config_obj[self.config.MAIN].as_bool(self.config.COLOR)

    def set_fuzzy_match(self, fuzzy):
        """Setter for fuzzy matching mode

        Used by prompt_toolkit's KeyBindingManager.
        KeyBindingManager expects this function to be callable so we can't use
        @property and @attrib.setter.

        Args:
            * color: A boolean that represents the fuzzy flag.

        Returns:
            None.
        """
        self.config_obj[self.config.MAIN][self.config.FUZZY] = fuzzy
        self.completer.fuzzy_match = fuzzy

    def get_fuzzy_match(self):
        """Getter for fuzzy matching mode

        Used by prompt_toolkit's KeyBindingManager.
        KeyBindingManager expects this function to be callable so we can't use
        @property and @attrib.setter.

        Args:
            * None.

        Returns:
            A boolean that represents the fuzzy flag.
        """
        return self.config_obj[self.config.MAIN].as_bool(self.config.FUZZY)

    def set_shortcut_match(self, shortcut):
        """Setter for shortcut matching mode

        Used by prompt_toolkit's KeyBindingManager.
        KeyBindingManager expects this function to be callable so we can't use
        @property and @attrib.setter.

        Args:
            * color: A boolean that represents the shortcut flag.

        Returns:
            None.
        """
        self.config_obj[self.config.MAIN][self.config.SHORTCUT] = shortcut
        self.completer.shortcut_match = shortcut

    def get_shortcut_match(self):
        """Getter for shortcut matching mode

        Used by prompt_toolkit's KeyBindingManager.
        KeyBindingManager expects this function to be callable so we can't use
        @property and @attrib.setter.

        Args:
            * None.

        Returns:
            A boolean that represents the shortcut flag.
        """
        return self.config_obj[self.config.MAIN].as_bool(self.config.SHORTCUT)

    def _handle_keyboard_interrupt(self, e, platform):
        """Handles keyboard interrupts more gracefully on Mac/Unix/Linux.

        Allows Mac/Unix/Linux to continue running on keyboard interrupt,
        as the user might interrupt a long-running AWS command with Control-C
        while continuing to work with DevyzerTerminal.

        On Windows, the "Terminate batch job (Y/N)" confirmation makes it
        tricky to handle this gracefully.  Thus, we re-raise KeyboardInterrupt.

        Args:
            * e: A KeyboardInterrupt.
            * platform: A string that denotes platform such as
                'Windows', 'Darwin', etc.

        Returns:
            None

        Raises:
            Exception: A KeyboardInterrupt if running on Windows.
        """
        if platform == 'Windows':
            raise e
        else:
            # Clear the renderer and send a carriage return
            self._prompt.app.renderer.clear()
            self._prompt.app.key_processor.feed(KeyPress(Keys.ControlM, u''))
            self._prompt.app.key_processor.process_keys()

    def handle_cd(self, text):
        """Handles a `cd` shell command by calling python's os.chdir.

        Simply passing in the `cd` command to subprocess.call doesn't work.
        Note: Changing the directory within DevyzerTerminal will only be in effect while
        running DevyzerTerminal.  Exiting the program will return you to the directory
        you were in prior to running DevyzerTerminal.

        Attributes:
            * text: A string representing the input command text.

        Returns:
            A boolean representing a `cd` command was found and handled.
        """
        CD_CMD = 'cd'
        stripped_text = text.strip()
        if stripped_text.startswith(CD_CMD):
            directory = ''
            if stripped_text == CD_CMD:
                # Treat `cd` as a change to the root directory.
                # os.path.expanduser does this in a cross platform manner.
                directory = os.path.expanduser('~')
            else:
                tokens = text.split(CD_CMD + ' ')
                directory = tokens[-1]
            try:
                os.chdir(directory)
            except OSError as e:
                self.log_exception(e, traceback, echo=True)
            return True
        return False

    def _process_command(self, text):
        """Processes the input command, called by the cli event loop

        Args:
            * text: A string that represents the input command text.

        Returns:
            None.
        """

        text = self.completer.replace_shortcut(text)

        try:
            if not self._handle_cd(text):
                text = self.colorize_output(text)
                # Pass the command onto the shell so devyzer cli can execute it
                subprocess.call(text, shell=True)
            print('')
        except KeyboardInterrupt as e:
            self._handle_keyboard_interrupt(e, platform.system())
        except Exception as e:
            self.log_exception(e, traceback, echo=True)

    def _create_cli(self):
        """Creates the prompt_toolkit's CommandLineInterface.

        Args:
            * None.

        Returns:
            None.
        """
        history = FileHistory(os.path.expanduser('~/.devyzer-history'))
        toolbar = Toolbar(self.get_color,
                          self.get_fuzzy_match,
                          self.get_shortcut_match)

        key_manager = KeyManager(
            self.set_color,
            self.get_color,
            self.set_fuzzy_match,
            self.get_fuzzy_match,
            self.set_shortcut_match,
            self.get_shortcut_match
        )

        style_factory = StyleFactory(self.theme)

        def get_message():
            state = SessionState()

            res = []

            if state.active_project is not None:
                res.extend([
                    ('class:holder', '<'),
                    ('class:project', state.active_project),
                    ('class:holder', '>')
                ])

            res.extend([
                ('class:folder', state.current_folder),
                ('class:pound', '# '),
            ])

            return res

        self._prompt = PromptSession(
            message=get_message,
            refresh_interval=1,
            reserve_space_for_menu=8,
            lexer=PygmentsLexer(CommandLexer),
            # bottom_toolbar=toolbar.handler,
            input_processors=[
                ConditionalProcessor(
                    processor=HighlightMatchingBracketProcessor(
                        chars='[](){}'),
                    filter=HasFocus(DEFAULT_BUFFER) & ~IsDone())],
            auto_suggest=AutoSuggestFromHistory(),
            enable_history_search=False,
            completer=ThreadedCompleter(self.completer),
            complete_while_typing=True,
            enable_system_prompt=True,
            key_bindings=key_manager.key_bindings,
            style=style_factory.style,
            mouse_support=False,
            include_default_pygments_style=False,
            history=history,

            # multiline=True,

            enable_open_in_editor=True,
            enable_suspend=True,
            search_ignore_case=True

        )
