#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 19:38:25 2020

@author: yves
"""

from PySide2.QtUiTools import QUiLoader

from . import version, codename
from . import ui

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources


class AboutUI():
    def __init__(self, main_ui):
        loader = QUiLoader()
        
        with pkg_resources.path(ui, 'about.ui') as ui_file:
            about_ui = loader.load(str(ui_file), main_ui.window)
            
        about_ui.versionLabel.setText(f"Version {version()} ({codename()})")
        about_ui.show()
        