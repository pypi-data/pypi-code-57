#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 23:27:46 2020

@author: yves


    This file is part of Saqqarah.

    Saqqarah is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Saqqarah is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Saqqarah.  If not, see <https://www.gnu.org/licenses/>
"""
from . import ui
try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources
    
from PySide2.QtUiTools import QUiLoader
    
class PreferencesUI:
    resolutions = [ 50, 75, 100, 150, 200, 250, 300, 600 ]
    
    def __init__(self, ui_instance):
        self.ui = ui_instance
        
        loader = QUiLoader()
        with pkg_resources.path(ui, 'preferences.ui') as ui_file:
            self.pref_ui = loader.load(str(ui_file), self.ui.window)
        
        self.pref_ui.show()
        self.resolution_init()
        self.timestamp_init()
        self.linewidth_init()
        self.basename_init()
        self.buttonBox = self.pref_ui.buttonBox
            
    def resolution_init(self):
        
        if self.ui.param.resolution not in self.resolutions:
            self.resolutions.insert(0, self.ui.param.resolution)
            self.resolutions.sort()
        
        actual_index = self.resolutions.index(self.ui.param.resolution)
        
        resolutionCombo = self.pref_ui.resolutionCombo
                
        resolutionCombo.addItems(str(r) for r in self.resolutions)
        resolutionCombo.setCurrentIndex(actual_index)
        
    def timestamp_init(self):
        names_choice= [ 'Add timestamp in file name',
                       'Erase old file when save' ]
        actual_index = 0 if self.ui.param.use_timestamp else 1

        stampCombo = self.pref_ui.timestampCombo
        stampCombo.addItems(names_choice)
        stampCombo.setCurrentIndex(actual_index)
        
    def linewidth_init(self):
        lwbox = self.pref_ui.linewidthBox
        lwbox.setValue(self.ui.param.line_width)
        
    def basename_init(self):
        self.pref_ui.basenameEdit.setPlaceholderText(self.ui.param.basename)
        