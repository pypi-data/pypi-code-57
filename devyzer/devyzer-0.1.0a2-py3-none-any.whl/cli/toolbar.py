# -*- coding: utf-8 -*-


from __future__ import print_function
from __future__ import unicode_literals

from devyzer.utils import get_current_folder_name


class Toolbar(object):
    """Encapsulates the bottom toolbar.

    Attributes:
        * handler: A callable get_toolbar_items.
    """

    def __init__(self, color_cfg, fuzzy_cfg, shortcuts_cfg):
        """Initializes ToolBar.

        Args:
            * color_cfg: A boolean that spedifies whether to color the output.
            * fuzzy_cfg: A boolean that spedifies whether to do fuzzy matching.
            * shortcuts_cfg: A boolean that spedifies whether to match
                shortcuts.

        Returns:
            None
        """
        self.handler = self._create_toolbar_handler(color_cfg,
                                                    fuzzy_cfg,
                                                    shortcuts_cfg)

    def _create_toolbar_handler(self, color_cfg, fuzzy_cfg, shortcuts_cfg):
        """Creates the toolbar handler.

        Args:
            * color_cfg: A boolean that spedifies whether to color the output.
            * fuzzy_cfg: A boolean that spedifies whether to do fuzzy matching.
            * shortcuts_cfg: A boolean that spedifies whether to match
                shortcuts.

        Returns:
            A callable get_toolbar_items.
        """
        assert callable(color_cfg)
        assert callable(fuzzy_cfg)
        assert callable(shortcuts_cfg)

        def get_toolbar_items():
            """Returns bottom menu items.

            Returns:
                A list of Token.Toolbar.
            """
            if color_cfg():
                color_token = 'class:toolbar.on'
                color = 'ON'
            else:
                color_token = 'class:toolbar.off'
                color = 'OFF'
            if fuzzy_cfg():
                fuzzy_token = 'class:toolbar.on'
                fuzzy = 'ON'
            else:
                fuzzy_token = 'class:toolbar.off'
                fuzzy = 'OFF'
            if shortcuts_cfg():
                shortcuts_token = 'class:toolbar.on'
                shortcuts = 'ON'
            else:
                shortcuts_token = 'class:toolbar.off'
                shortcuts = 'OFF'

            return [
                (color_token, ' [F2] Color: {0} '.format(color)),
                (fuzzy_token, ' [F3] Fuzzy: {0} '.format(fuzzy)),
                (shortcuts_token, ' [F4] Shortcuts: {0} '.format(shortcuts)),
                ('', ' [F5] Refresh '),
                ('', ' [F9] Docs '),
                ('', ' [F10] Exit ')
            ]

        return get_toolbar_items
