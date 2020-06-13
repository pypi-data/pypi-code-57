
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


context = None
data_service = None
_dataexplore_view = None
_frame = None

def init(context_):
    global context
    context = context_


class DataExploreView(QDockWidget):
    def __init__(self):
        super().__init__()

        self._open = None
        self._menu = None

        self.treeWidget = QTreeWidget()
        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeWidget.setColumnCount(2)
        self.treeWidget.setHeaderLabels(['Name', 'Kind'])
        self.treeWidget.setColumnWidth(0, 160)

        # 右键菜单
        self.treeWidget.customContextMenuRequested.connect(self.openMenu)
        # 双击编辑名称
        self.treeWidget.itemDoubleClicked.connect(self.double_click)
        # 选择改变
        self.treeWidget.itemPressed.connect(self.itemPressed)

        self.setWidget(self.treeWidget)
    def openMenu(self, position):
        item = self.treeWidget.currentItem()

        class ActionNewNode:
            def __init__(self, kind, parent = None):
                self._kind = kind
                self._parent = parent
            def get_name(self, kind):
                text, ok = QInputDialog().getText(None, "input "+kind+"'s name", "name:", QLineEdit.Normal)
                return text, ok
            def on_new_node(self, value):
                global context

                print("on_new_node")

                name, ok = self.get_name(self._kind)
                if not (ok and name):
                    return 

                data_service = context.find_service("DataService")
                print(self._parent)
                if not self._parent:
                    # 创建根节点
                    new_node = data_service.create_rootnode(name)
                else:
                    # 创建子节点
                    node = self._parent.data(0, Qt.UserRole)
                    new_node = data_service.create_node(self._kind, name)
                    node.add_child(new_node)
            def on_delete(self, value):
                global context

                node = self._parent.data(0, Qt.UserRole)
                print("on_delete:", self._parent)
                node.delete()
                
        
        # 弹出菜单
        menu = QMenu()
        self._menu = menu
        
        if not item:
            action = menu.addAction(self.tr("新建根节点"))

            obj = ActionNewNode("")
            action.triggered.connect(obj.on_new_node)
        else:
            node = item.data(0, Qt.UserRole)
            kinds =  node.get_child_kinds()
            objs = []
            for kind in kinds:
                action = menu.addAction(self.tr("新建"+kind))
                
                obj = ActionNewNode(kind, item)
                objs.append(obj)
                action.triggered.connect(obj.on_new_node)

            action = menu.addAction("删除")

            obj = ActionNewNode("", item)
            objs.append(obj)
            action.triggered.connect(obj.on_delete)

            action = menu.addAction("重命名")
            action.triggered.connect(self.on_rename)

        # 获取类型节点注册的菜单
        node = None
        if item:
            node = item.data(0, Qt.UserRole)
        exts = context.find_extension("PL::DataExplore::Menu")
        for ext in exts:
            ext.add_menu(menu, node)

        menu.exec_(self.treeWidget.viewport().mapToGlobal(position))
    def on_rename(self, value):
        item = self.treeWidget.currentItem()
        if not item:
            return 

        self._open = item
        self.treeWidget.openPersistentEditor(item, 0)

    def double_click(self, item, col):
        node = item.data(0, Qt.UserRole)
        
        exts = context.find_extension("PL::Basic::Editor")
        for ext in exts:
            if (ext.is_match_data(node)):
                global _frame
                tabWidget = _frame.centralWidget ()
                widget = ext.create_editor(tabWidget)
                widget.on_init(node)
                tabWidget.addTab(widget, node.get_name())
                break

    def itemPressed(self, item, col):
        if self._open:
            item = self._open
            self.treeWidget.closePersistentEditor(self._open,0)
            self._open = None

            node = item.data(0, Qt.UserRole)
            print("name.....:", item.text(0))
            node.set_name(item.text(0))
        
        global context
        context.fire('event::DataNode::Select', item.data(0, Qt.UserRole))

    def _new_node(self, node, parent = None):
        global context

        new_item = None
        if not parent:
            new_item = QTreeWidgetItem(self.treeWidget)
        else:
            new_item = QTreeWidgetItem(parent)
            print("parent:",new_item.parent())
        
        

        class RootNodeCallback:
            def __init__(self, item, node):
                self._item = item
                self._node = node
            def set_name(self, event, node, old_name):
                if node != self._node:
                    return 
                name = node.get_name()
                self._item.setText(0, name)
            def set_prop(self, event, node, key, value):
                return 
            def delete(self, event, node):
                if node != self._node:
                    return
                
                global context
                context.remove_suscribe('event::DataNode::Modify::Name' , self.set_name)
                context.remove_suscribe('event::DataNode::Modify::Prop' , self.set_prop)
                context.remove_suscribe('event::DataNode::Delete' , self.delete)
                context.remove_suscribe('event::DataNode::Modify::AddChild' , self.add_child)
                context.remove_suscribe('event::DataNode::Modify::RemoveChild' , self.remove_child)

            def add_child(self, event, node, child):
                if node != self._node:
                    return
                
                item = QTreeWidgetItem(self._item)
                item.setText(0, child.get_name())
                item.setText(1, child.get_kind())
                item.setData(0, Qt.UserRole, child)
                print("current:", item)
                print("parent:", item.parent())

                global context
                obj = RootNodeCallback(item , child)
                item.setData(0, Qt.UserRole+1, obj)

                context.add_subscribe('event::DataNode::Modify::Name' , obj.set_name)
                context.add_subscribe('event::DataNode::Modify::Prop' , obj.set_prop)
                context.add_subscribe('event::DataNode::Delete' , obj.delete)
                context.add_subscribe('event::DataNode::Modify::AddChild' , obj.add_child)
                context.add_subscribe('event::DataNode::Modify::RemoveChild' , obj.remove_child)
            
            def remove_child(self, event, node, child):
                if node != self._node:
                    return

                for i in range(0, self._item.childCount()):
                    item = self._item.child(i)
                    child_node = item.data(0, Qt.UserRole)
                    if child_node == child:
                        self._item.removeChild(item)
                        break

        obj = RootNodeCallback(new_item , node)

        new_item.setText(0, node.get_name())
        new_item.setText(1, node.get_kind())
        new_item.setData(0, Qt.UserRole, node)
        new_item.setData(0, Qt.UserRole+1, obj)

        global context
        context.add_subscribe('event::DataNode::Modify::Name' , obj.set_name)
        context.add_subscribe('event::DataNode::Modify::Prop' , obj.set_prop)
        context.add_subscribe('event::DataNode::Delete' , obj.delete)
        context.add_subscribe('event::DataNode::Modify::AddChild' , obj.add_child)
        context.add_subscribe('event::DataNode::Modify::RemoveChild' , obj.remove_child)

        return new_item

    

    def on_project_open(self, node):
        data_service = context.find_service("DataService")
        root = data_service.root_node()

        root_item = self._new_node(root)

        nodes = []
        items = []
        nodes.append(root)
        items.append(root_item)

        while len(nodes) > 0:
            node = nodes[0]
            item = items[0]

            nodes.pop(0)
            items.pop(0)

            children = node.get_children()
            for child in children:
                new_item = self._new_node(child, item)
                nodes.append(child)
                items.append(new_item)


class DataExploreExtension:
    def add_pane(self, frame):
        global _dataexplore_view
        self._dock1 = DataExploreView()
        _dataexplore_view = self._dock1
        self._dock1.setWindowTitle('DataExplore')
        frame.addDockWidget(Qt.LeftDockWidgetArea, self._dock1)

        global _frame
        _frame = frame


class PaneExtensionToolbar:
    def __init__(self):
        self._file = None

    def add_toolbar(self, toolBar):

        action = toolBar.addAction(QIcon(os.path.dirname(__file__) + "/images/down.png"),"Open")
        action.setToolTip("Open")
        action.triggered.connect(self.open)
        action = toolBar.addAction(QIcon(os.path.dirname(__file__) + "/images/left.png"),"Save")
        action.setToolTip("Save")
        action.triggered.connect(self.save)
        action = toolBar.addAction(QIcon(os.path.dirname(__file__) + "/images/right.png"),"Save As")
        action.setToolTip("Save As")
        action.triggered.connect(self.saveas)
    def add_menu(self, menu_bar):
        self.file_menu = menu_bar.addMenu("File")

        self.action1 = QAction("Open")
        self.action1.triggered.connect(self.open)
        self.file_menu.addAction(self.action1)
        

        self.action2 = QAction("Save")
        self.action2.triggered.connect(self.save)
        self.file_menu.addAction(self.action2)

        self.action3 = QAction("Save As")
        self.action3.triggered.connect(self.saveas)
        self.file_menu.addAction(self.action3)

    def saveas(self, obj):
        global context
        data_service = context.find_service("DataService")

        fileName, ok = QFileDialog.getSaveFileName(None, "Save Project", "", "X Project Files (*.xxx)")
        if not fileName:
            return 

        data_service.save(fileName)
        self._file = fileName
    def save(self, obj):
        if self._file:
            global context
            data_service = context.find_service("DataService")
            data_service.save(self._file)
        else:
            self.saveas("")
    def open(self, obj):
        fileName, ok = QFileDialog.getOpenFileName(None, "Open Project", "", "X Project Files (*.xxx)")
        if not fileName:
            return 

        global context
        data_service = context.find_service("DataService")
        data_service.load(fileName)
        self._file = fileName
    


def OnOpenProject(event, node):
    global _dataexplore_view
    print(".------------------")
    _dataexplore_view.on_project_open(node)

def OnRootNodeNew(event, node):
    global _dataexplore_view
    _dataexplore_view._new_node(node)


DataExploreMenu = '''
class DataExploreMenu:
    def add_menu(self, menu, node):
        pass
'''

config = {
    'pluginid': 'UI::Core::DataExplore',
    "extensions_def" : [
        {
            "name": "PL::DataExplore::Menu",
            "define": DataExploreMenu
        }
    ],
    "extensions" : [
        {
            "name": "PL::Basic::Pane",
            "impl": DataExploreExtension()
        },
        {
            "name": "PL::Basic::Menu",
            "impl": PaneExtensionToolbar()
        },
        {
            "name": "PL::Basic::ToolBar",
            "impl": PaneExtensionToolbar()
        }
    ],
    "subscribes" : [
        {
            "name": 'event::Project::Open',
            "define": OnOpenProject
        },
        {
            "name": 'event::NewRootDataNode',
            "define": OnRootNodeNew
        }
    ]
}