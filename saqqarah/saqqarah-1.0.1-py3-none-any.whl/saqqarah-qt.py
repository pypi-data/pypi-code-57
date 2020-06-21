#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 17:59:23 2020

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

import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import SIGNAL

from saqqarah import import SaqqarahUI


loader = QUiLoader()


def print_dict(obj):
    for k,v in obj.__dict__.items():
        print(f"{k} : {v}")

def mainwindow_setup(w):
    w.setWindowTitle("MainWindow Title")

app = QtWidgets.QApplication.instance()
if app is None: 
    app = QtWidgets.QApplication(sys.argv)

window = loader.load("saqqarah-qt.ui", None)
uicontrol = SaqqarahUI(window) 

mainwindow_setup(window)
window.show()

window.quitButton.connect(SIGNAL ('clicked()'), app.quit)
#print_dict(window)
sys.exit(app.exec_())

