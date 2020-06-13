

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import os
import sys

sys.path.append(os.path.dirname(__file__) + '/QtProperty' )
sys.path.append(os.path.dirname(__file__) + '/libqt5' )

from PyQt5.QtWidgets import QApplication, QLineEdit
from PyQt5.QtCore import (
    QTranslator, 
    QVariant, 
    QDate, 
    QTime, 
    QDateTime, 
    Qt, 
    QLocale, 
    QPoint, 
    QPointF, 
    QSize, 
    QSizeF, 
    QRect, 
    QRectF
    )

from PyQt5.QtGui import QKeySequence
from pyqtcore import QList
from qtvariantproperty import QtVariantEditorFactory, QtVariantPropertyManager
from qttreepropertybrowser import QtTreePropertyBrowser

context = None
_property_view = None

def init(context_):
    global context
    context = context_


class PropertyViewDock(QDockWidget):
    def __init__(self):
        super().__init__()

        self._props = {}
        self._init = False

        self.variantManager = QtVariantPropertyManager()
        self.variantFactory = QtVariantEditorFactory()

        self.variantEditor = QtTreePropertyBrowser()
        self.variantEditor.setFactoryForManager(self.variantManager, self.variantFactory)
        #variantEditor.addProperty(topItem)
        self.variantEditor.setPropertiesWithoutValueMarked(True)
        self.variantEditor.setRootIsDecorated(False)

        self.setWidget(self.variantEditor)
        self.setWindowTitle('Property View')

        self.variantManager.valueChangedSignal.connect(self.on_value_change)

    def on_value_change(self, prop, value):
        self._item.set_prop(prop.propertyName(), value)
    
    def select_item(self, item):
        self._props = {}
        self.variantEditor.clear()

        if not item:
            return 

        self._init = True
        self._item = item
        props = item.get_props()
        for prop in props:
            item = self.variantManager.addProperty(QVariant.String, prop)
            item.setValue(props[prop])
            self.variantEditor.addProperty(item)
            self._props[prop] = item
        self._init = False

    def update_item(self, item, prop):
        if self._item != item:
            return 
        if prop in self._props:
            value = item.get_prop(prop)
            self._props[prop].setValue(value)
        else:
            value = item.get_prop(prop)
            item = self.variantManager.addProperty(QVariant.String, prop)
            item.setValue(value)
            self.variantEditor.addProperty(item)
            self._props[prop] = item

class PaneExtension:
    def add_pane(self, frame):
        global _property_view

        self._view = PropertyViewDock()
        _property_view = self._view
        frame.addDockWidget(Qt.RightDockWidgetArea, self._view)

def on_select_item(event, node):
    global _property_view
    _property_view.select_item(node)

def on_item_prop_change(event, node, prop, old_value):
    global _property_view
    _property_view.update_item(node, prop)

config = {
    'pluginid': 'UI::Core::PropertyView',
    "extensions" : [
        {
            "name": "PL::Basic::Pane",
            "impl": PaneExtension()
        }
    ],
    "subscribes" : [
        {
            "name": 'event::DataNode::Select',
            "define": on_select_item
        },
        {
            "name": 'event::DataNode::Modify::Prop',
            "define": on_item_prop_change
        }
    ]
}