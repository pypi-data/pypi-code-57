# -*- coding: utf-8 -*-
from PyQt5.QtCore import QObject

class MouseEventsController(object):
    def __init__(self, parent):
        self.exec_super_method: bool = True

    def mouseMoveEvent(self, ev):
        pass

    def mouseReleaseEvent(self, ev):
        pass

    def mousePressEvent(self, ev):
        pass
