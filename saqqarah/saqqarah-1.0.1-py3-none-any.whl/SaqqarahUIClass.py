#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 22:34:32 2020

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

from . import Pyramid, PyramidPrinterImage, PyramidPrinterTikz

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QTimeLine, QThread, QObject, Slot, Signal
from PySide2.QtGui import QRegExpValidator
from PySide2.QtWidgets import QFileDialog, QAction

from PIL.ImageQt import toqpixmap

from . import Parameters
from . import PreferencesUI
from . import AboutUI

from time import strftime


# Create the Slots that will receive signals    
class LookingForPuzzleThread(QThread):
    def __init__(self, ui):
        QThread.__init__(self)
        self.param = ui.param
        self.pyramid = ui.pyramid

    def __del__(self):
        self.wait()

    # TODO : pyramid uses parameters() too
    def run(self):
        self.pyramid.get_puzzle(difficulty=self.param.difficulty,
                                min = self.param.value_min,   
                                max = self.param.value_max,
                                seed = self.param.seed,
                                exclude_zero = self.param.exclude_zero)
   
# use signal too get messages 
# from calculation thread
class LogSignal(QObject):
    log_signal = Signal((str,str,bool))

class SaqqarahUI(QObject):
  
    # reception of the log signal
    @Slot(str, str , bool)
    def print_log(self, text, end, keep):
        self.window.informationLabel.setText(str(text))
        if keep:
            self.logTE.appendPlainText(text)
    
    # sending of the signal
    def information(self, text, *, end='\n', keep=True):
        self.ls.log_signal.emit(text, end, keep)
            
    def __init__(self, window):
        # defaut values are inside
        self.param = Parameters()

        self.images = {}

        self.generating = False

        self.init_ui(window)
        self.ls = LogSignal()
        self.ls.log_signal.connect(self.print_log)

        self.logTE  = self.window.logText
        self.logTE.setPlainText('Saqqarah pyramid generator')
        self.logTE.appendPlainText(strftime("%a, %d %b %Y %H:%M:%S"))
        # 1000 seconds
        self.timeline = QTimeLine(2_000, self.window)
        self.init_timeline()
        self.combo_init()
        self.seed_init()
        self.zero_init()
        self.update_pyramid()
        
    def zero_init(self):
        zeroCheck = self.window.zeroCheckbox
        self.exlude_zero = zeroCheck.isChecked()
        zeroCheck.stateChanged.connect(self.zero_changed)

    def zero_changed(self):
        self.param.exclude_zero = self.window.zeroCheckbox.isChecked()

    def seed_init(self):
        seed = self.window.seedEdit
        seed.setValidator(QRegExpValidator("[1-9][0-9]*"))
        seed.editingFinished.connect(self.seed_changed)
        seed.textEdited.connect(self.seed_edited)
        
    def seed_edited(self):
        self.param.seed = None

    def seed_changed(self):
        value = self.window.seedEdit.text()
        if value:
            self.param.seed = int(value)

    def combo_init(self):
        outCombo = self.window.outputTypeCombo
        outCombo.addItem('Images', userData=PyramidPrinterImage)
        outCombo.addItem('Tikz code', userData=PyramidPrinterTikz)

    def update_pyramid(self):        
        self.pyramid = Pyramid(self.param.size, ui=self)
        self.imagePrinter = PyramidPrinterImage(self.pyramid, self.param, memory_images=True)
        self.clean_images()
           
    def init_ui(self,window):
        self.window = window
        self.window.quitButton.clicked.connect(QtWidgets.QApplication.instance().quit)
        self.window.tabWidget.setCurrentIndex(0)
        self.spinbox_init(window.sizeBox, 
                          value=self.param.size, 
                          min=self.param.size_min, 
                          max=self.param.size_max, 
                          on_change=self.size_changed )
        self.check_size_difficulty()
        self.spinbox_init(window.difficultyBox, 
                          value=self.param.difficulty, 
                          min=self.param.difficulty_min, 
                          max=self.param.difficulty_max,
                          on_change=self.difficulty_changed )
        self.spinbox_init(window.minBox, 
                          value=self.param.value_min, 
                          min=-1000, 
                          max=self.param.value_max-1,
                          on_change=self.min_changed )
        self.spinbox_init(window.maxBox, 
                          value=self.param.value_max, 
                          min=self.param.value_min+1, 
                          max=1000,
                          on_change=self.max_changed )
        self.window.puzzleButton.clicked.connect(self.generate_puzzle)
        self.window.directoryButton.clicked.connect(self.choose_directory)
        self.window.saveButton.clicked.connect(self.save_puzzle)
        self.progressbar_init()
        self.menus_init()
        
    def menus_init(self):
        entryExit = self.window.actionExit
        entryExit.triggered.connect(QtWidgets.QApplication.instance().quit)
        self.window.actionPreferences.triggered.connect(self.preferences_run)
        self.window.actionAbout.triggered.connect(self.about_run)
        
    def about_run(self):
        AboutUI(self)

    def preferences_run(self):
        self.pref_ui = PreferencesUI(self).pref_ui
        self.pref_ui.accepted.connect(self.validate_pref)
  
    def init_timeline(self):
        # 0.1 sec frame
        self.timeline.setUpdateInterval(10)
        self.timeline.setFrameRange(0, 100)
        self.timeline.frameChanged[int].connect(self.update_progressbar)
        #2**12 * 10 seconds is 11 hours
        self.timeline.setLoopCount(2**15)
        self.timeline.setCurveShape(self.timeline.LinearCurve)

    def update_progressbar(self, frame):
        # animation to make sure ui is not locked
        X = frame*2 - 100
        self.window.progressBar.setInvertedAppearance(X >= 0)
        X = 100 - abs(X)
        self.window.progressBar.setValue(X)
     
    def progressbar_init(self):
        self.window.progressBar.setRange(0,100)
        self.window.progressBar.setInvertedAppearance(False)
        self.window.progressBar.reset()

    def progressbar_stop(self):
        self.timeline.stop()
        self.window.progressBar.setInvertedAppearance(False)
        self.window.progressBar.setRange(0,100)
        self.window.progressBar.reset()
        
    def progressbar_run(self):
        self.window.progressBar.setRange(0,100)
        self.window.progressBar.setFormat("Looking…")
        self.window.progressBar.reset()
        self.timeline.start()
        
    def spinbox_init(self, spin, *, value = 0, min=0, max=1000, step=1, on_change = None):
        spin.setRange(min,max)
        spin.setValue(value)
        if on_change:
            spin.valueChanged.connect(on_change)
        
    def size_changed(self, value):
        self.param.size = value
        self.update_pyramid()
        self.check_size_difficulty()

    def check_size_difficulty(self):
        if self.param.size < 5:
            self.window.difficultyBox.setMaximum(3)
        else:
            self.window.difficultyBox.setMaximum(5)
            
    def difficulty_changed(self, value):
        self.param.difficulty = value
    def min_changed(self, value):
        self.param.value_min = value
        self.window.maxBox.setMinimum(value+1)
    def max_changed(self, value):
        self.param.value_max = value
        self.window.minBox.setMaximum(value-1)

    def update_images(self):
        if not self.images:
            return
        
        if 'puzzle' in self.images:
            self.puzzlePix = toqpixmap(self.images['puzzle'])
        if 'solution' in self.images:
            self.solutionPix = toqpixmap(self.images['solution'])
        if 'nopuzzle' in self.images:
            self.puzzlePix = toqpixmap(self.images['nopuzzle'])
            self.solutionPix = toqpixmap(self.images['nopuzzle'])

        self.window.puzzleImageLabel.setPixmap(self.puzzlePix)
        self.window.solutionImageLabel.setPixmap(self.solutionPix)
        
    def generate_puzzle(self):
        # in another thread. That can be long.
        if not self.generating:
            self.generating = True
            self.progressbar_run()  
            self.information("Looking for a puzzle.")
            self.clean_images()
            self.myThread = LookingForPuzzleThread(self)
            self.myThread.finished.connect(self.when_get_puzzle)
            self.myThread.start(QThread.LowPriority)
            self.puzzleButtonText = self.window.puzzleButton.text()
            self.window.puzzleButton.setText("&Cancel")
        else:
            # cancel the running puzzle generation
            self.generating = False
            self.pyramid.cancel = True

    def when_get_puzzle(self):
        if self.pyramid.cancel:
            self.information("Operation cancelled.")
        else:
            self.redraw_images()

        self.generating = False
        self.window.puzzleButton.setText(self.puzzleButtonText)
        self.progressbar_stop()
        del self.myThread
           
    def clean_images(self):
        self.pyramid.puzzle = {}
        self.pyramid.solution = []
        self.redraw_images()

    def choose_directory(self):
        dirDialog = QFileDialog()
        # default irectory to "Documents"
        dirDialog.setDirectory(self.param.output_directory)
        self.param.output_directory = dirDialog.getExistingDirectory(self.window, "Select Directory")
        self.information(f"Output directory : {self.param.output_directory}")

    def save_puzzle(self):
        combo = self.window.outputTypeCombo
        printerClass = combo.currentData()
        printerClass(self.pyramid, self.param).print()
        
    def validate_pref(self):
        ts_index = self.pref_ui.timestampCombo.currentIndex()
        lw = self.pref_ui.linewidthBox.value()
        resolution = int(self.pref_ui.resolutionCombo.currentText())
        basename = self.pref_ui.basenameEdit.text()
        onefile = self.pref_ui.tikzonefileCheckbox.isChecked()
        
        self.param.use_timestamp = True if ts_index == 0 else False
        self.param.line_width = lw
        self.param.resolution = resolution
        if basename:
            self.param.basename = basename
        self.param.tikz_onefile = onefile
        self.redraw_images()
            
    def redraw_images(self):
        #redraw images with new parameters
        self.imagePrinter.print()
        self.images = self.imagePrinter.get_images()
        self.update_images()    

        
        
        
