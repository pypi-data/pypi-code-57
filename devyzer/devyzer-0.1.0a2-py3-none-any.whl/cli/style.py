# -*- coding: utf-8


import pygments.styles
from prompt_toolkit.styles import merge_styles, style_from_pygments_cls, Style
from pygments.util import ClassNotFound


class StyleFactory(object):
    """Creates a custom saws style.

    Provides styles for the completions menu and toolbar.

    Attributes:
        * style: An instance of a Pygments Style.
    """

    def __init__(self, name):
        """Initializes StyleFactory.

        Args:
            * name: A string representing the pygments style.

        Returns:
            An instance of CliStyle.
        """
        self.style = self.style_factory(name)

    def style_factory(self, name):
        """Retrieves the specified pygments style.

        If the specified style is not found, the native style is returned.

        Args:
            * name: A string representing the pygments style.

        Returns:
            An instance of CliStyle.
        """
        try:
            style = pygments.styles.get_style_by_name(name)
        except ClassNotFound:
            style = pygments.styles.get_style_by_name('native')

        # Create styles dictionary.
        return merge_styles([
            style_from_pygments_cls(style),
            Style.from_dict({
                # User input (default text).
                '': '#ff0066',

                # Prompt.
                'folder': '#00aa00',
                'holder': '#884444',
                'pound': '#00aa00',
                'project': 'ansicyan',
                'colon': '#0000aa',

                'scrollbar': 'bg:#00aaaa',
                'scrollbar.button': 'bg:#003333',
                'completion-menu.completion': 'bg:#008888 #ffffff',
                'completion-menu.completion.current': 'bg:#00aaaa #000000',
                'system-toolbar': 'noinherit bold',
                'search-toolbar': 'noinherit bold',
                'search-toolbar.text': 'nobold',
                'arg-toolbar': 'noinherit bold',
                'arg-toolbar.text': 'nobold',
                'bottom-toolbar': 'bg:#222222 #cccccc',
                'toolbar.off': 'bg:#222222 #696969',
                'toolbar.on': 'bg:#222222 #ffffff',
            })
        ])
