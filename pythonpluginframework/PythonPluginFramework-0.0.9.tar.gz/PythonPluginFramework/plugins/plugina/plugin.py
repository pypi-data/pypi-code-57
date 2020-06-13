
import sys
import random

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


from six import BytesIO

context = None

def init(context_):
    global context
    context = context_


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Tutorial")

        self.menu = self.menuBar()

        exts = context.find_extension("PL::Basic::Menu")
        for ext in exts:
            ext.add_menu(self.menu)

        self._tool_bar = QToolBar()
        self.addToolBar(self._tool_bar)

        exts = context.find_extension("PL::Basic::ToolBar")
        for ext in exts:
            ext.add_toolbar(self._tool_bar)

        exts = context.find_extension("PL::Basic::Pane")
        for ext in exts:
            ext.add_pane(self)

        self.tabEditor =  QTabWidget()
        self.tabEditor.setTabsClosable(True)
        self.tabEditor.tabCloseRequested.connect(self.closeTab)
        self.setCentralWidget(self.tabEditor)

        # load test data
        data_service = context.find_service("DataService")
        
    def closeTab(self, index):
        currentQWidget = self.tabEditor.widget(index)
        currentQWidget.on_close()
        currentQWidget.deleteLater()
        self.tabEditor.removeTab(index)

class MyApp:
    def name(self):
        return "MyApp"

    def run(self, argv):
        global context
        context.fire("Event1", {"id", 20})

        exts = context.find_extension("PL::Test1")
        for ext in exts:
            ext.test()

        app = QApplication(sys.argv)

        window = MainWindow()
        window.resize(800, 600)
        window.show()

        sys.exit(app.exec_())
            
        print("Hello in MyAPP!!")

MyTest = '''
class MyTest:
    def test(self):
        print("Hello Test!")
'''

MenuExtension = '''
class MenuExtension:
    def add_menu(self, menu_bar):
        print("Hello in add_menu!")
'''

ToolBarExtension = '''
class ToolBarExtension:
    def add_toolbar(self, tool_bar):
        print("Hello in add_toolbar!")
'''

PaneExtension = '''
class PaneExtension:
    def add_pane(self, auiMgr):
        print("Hello in add_pane!")
'''

EditorWidget = '''
class EditorWidget:
    def on_init(self, node):
        return ""
    def on_save(self):
        return ""
    def on_close(self):
        return ""
    def on_update(self):
        return ""
'''

EditorExtension = '''
class EditorExtension:
    def data_kind(self):
        return ""
    def is_match_data(self, node):
        return False
    def create_editor(self, parent):
        return None
'''
    

def HelloServiceFun(a, b):
    print("HelloService:", a+b)

def HelloServiceFun_Decl():
    return {
            "des": "测试服务函数", 
            "name": "HelloServiceFun",
            "return": "",
            'paras':[
                {
                    'name': 'a',
                    'des': '加法运算数A'
                },
                {
                    'name': 'b',
                    'des': '加法运算数B'
                }
            ]
        }

config = {
    'pluginid': 'UI::Core::QtApp',
    "extensions" : [
        {
            "name": "PL::APP",
            "impl": MyApp()
        }
    ],
    "extensions_def" : [
        {
            "name": "PL::Test1",
            "define": MyTest
        },
        {
            "name": "PL::Basic::Menu",
            "define": MenuExtension
        },
        {
            "name": "PL::Basic::Pane",
            "define": PaneExtension
        },
        {
            "name": "PL::Basic::ToolBar",
            "define": ToolBarExtension
        },
        {
            "name": "PL::Basic::Editor",
            "define": EditorExtension
        }
    ],
    "services" : [
        {
            "name": "HelloService",
            "define": HelloServiceFun,
            'declare': HelloServiceFun_Decl()
        }
    ]
}