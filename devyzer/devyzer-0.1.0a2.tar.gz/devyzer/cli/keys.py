# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import requests
from prompt_toolkit.key_binding import KeyBindings
from devyzer.constants import EXIT


class KeyManager(object):
    """Creates a Key Manager.

    Attributes:
        * manager: An instance of a prompt_toolkit's KeyBindingManager.
    """

    def __init__(self, set_color, get_color,
                 set_fuzzy_match, get_fuzzy_match,
                 set_shortcut_match, get_shortcut_match):
        """Initializes KeyManager.

        Args:
            * set_color: A function setting the color output config.
            * get_color: A function getting the color output config.
            * set_fuzzy_match: A function setting the fuzzy match config.
            * get_fuzzy_match: A function getting the fuzzy match config.
            * set_shortcut_match: A function setting the shortcut match config.
            * get_shortcut_match: A function getting the shortcut match config.

        Returns:
            None.
        """
        self.manager = None
        self.key_bindings = self._create_key_bindings(
            set_color, get_color, set_fuzzy_match, get_fuzzy_match,
            set_shortcut_match, get_shortcut_match)
        self.is_command = False

    def _create_key_bindings(self, set_color, get_color,
                             set_fuzzy_match, get_fuzzy_match,
                             set_shortcut_match, get_shortcut_match):
        """Creates and initializes the keybinding manager.

        Args:
            * set_color: A function setting the color output config.
            * get_color: A function getting the color output config.
            * set_fuzzy_match: A function setting the fuzzy match config.
            * get_fuzzy_match: A function getting the fuzzy match config.
            * set_shortcut_match: A function setting the shortcut match config.
            * get_shortcut_match: A function getting the shortcut match config.

        Returns:
            A KeyBindingManager.
        """
        assert callable(set_color)
        assert callable(get_color)
        assert callable(set_fuzzy_match)
        assert callable(get_fuzzy_match)
        assert callable(set_shortcut_match)
        assert callable(get_shortcut_match)

        kb = KeyBindings()

        # @kb.add('c-m')
        # def handle_enter(event):
        #     user_input = event.cli.current_buffer.text
        #     set_is_command(user_input)

        @kb.add('f2')
        def handle_f2(_):
            """Enables/Disables color output.

            Args:
                * _: An instance of prompt_toolkit's Event (not used).

            Returns:
                None.
            """
            set_color(not get_color())

        @kb.add('f3')
        def handle_f3(_):
            """Enables/Disables fuzzy matching.

            Args:
                * _: An instance of prompt_toolkit's Event (not used).

            Returns:
                None.
            """
            set_fuzzy_match(not get_fuzzy_match())

        @kb.add('f4')
        def handle_f4(_):
            """Enables/Disables shortcut matching.

            Args:
                * _: An instance of prompt_toolkit's Event (not used).

            Returns:
                None.
            """
            set_shortcut_match(not get_shortcut_match())

        @kb.add('f10')
        def handle_f10(event):
            """Quits when the `F10` key is pressed.

            Args:
                * _: An instance of prompt_toolkit's Event (not used).

            Returns:
                None.
            """
            event.app.exit(EXIT)

        @kb.add('c-space')
        def handle_ctrl_space(event):
            """Initializes autocompletion at the cursor.

            If the autocompletion menu is not showing, display it with the
            appropriate completions for the context.

            If the menu is showing, select the next completion.

            Args:
                * event: An instance of prompt_toolkit's Event.

            Returns:
                None.
            """
            b = event.cli.current_buffer
            if b.complete_state:
                b.complete_next()
            else:
                event.cli.start_completion(select_first=False)

        return kb
