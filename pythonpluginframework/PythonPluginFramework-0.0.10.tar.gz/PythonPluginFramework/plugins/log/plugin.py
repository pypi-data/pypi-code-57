

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (QAction, QApplication, QHeaderView, QHBoxLayout, QLabel, QLineEdit, QMenu,
                               QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QTreeWidgetItem,
                               QVBoxLayout, QWidget, QToolBar, QDockWidget, QTreeWidget, QInputDialog)


import time

context = None
data_service = None

def init(context_):
    global context
    context = context_
    context.add_subscribe("*", OnEvent)

class DataExploreExtension:
    def add_pane(self, frame):
        print(".................")

def OnEvent(event, value1 = None, value2 = None, value3 = None, value4 = None, value5 = None):
    print("-----------on event------------------")
    print(event)
    if value1:
        print(value1)
    if value2:
        print(value2)
    if value3:
        print(value3)
    if value4:
        print(value4)
    if value5:
        print(value5)

config = {
    'pluginid': 'Core::Log',
}