
import os
import json

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

class PluginsShowDialog(QDialog):
    def __init__(self):
        super().__init__()

        global context

        layout = QVBoxLayout()
        self.setLayout(layout)

        tabWidget = QTabWidget(self)
        layout.addWidget(tabWidget)

        # 通过树形列表显示插件相关信息
        treeView = QTreeView(tabWidget)
        tabWidget.addTab(treeView, "插件信息")

        #  添加插件信息
        #model = self.to_standardItemModel('[["aaa", "bbb", "ccc"], ["a", "b", "c"], ["-a1", "b1", "c1"], ["abb", "bbb", "cbb"], ["-a2", "b2", "c2"]]')
        model = self.plugin_model()
        treeView.setModel(model)

        # 扩展点
        extdefView = QTreeView(tabWidget)
        tabWidget.addTab(extdefView, "扩展点定义")

        model = self.plugin_extension_def_model()
        extdefView.setModel(model)

        # 事件
        eventView = QTreeView(tabWidget)
        tabWidget.addTab(eventView, "事件定义")

        model = self.plugin_event_model()
        eventView.setModel(model)

        # 服务
        serviceView = QTreeView(tabWidget)
        tabWidget.addTab(serviceView, "服务定义")

        model = self.plugin_service_model()
        serviceView.setModel(model)

        # 扩展
        extView = QTreeView(tabWidget)
        tabWidget.addTab(extView, "扩展实现")

        model = self.plugin_extension_model()
        extView.setModel(model)

        # 订阅
        subscribeView = QTreeView(tabWidget)
        tabWidget.addTab(subscribeView, "事件订阅")

        model = self.plugin_subscribe_model()
        subscribeView.setModel(model)


    def plugin_extension_model(self):
        global context

        model = QStandardItemModel(0, 2)
        model.setHeaderData(0, Qt.Horizontal, '信息')
        model.setHeaderData(1, Qt.Horizontal, '值')

        for extension in context.extensions:
            item = QStandardItem('扩展点名称')
            model.appendRow([item, QStandardItem(extension)])
            for def_ in context.extensions[extension]:
                item.appendRow([QStandardItem('扩展实现'), QStandardItem(str(def_))])

        return model

    def plugin_subscribe_model(self):
        global context

        model = QStandardItemModel(0, 2)
        model.setHeaderData(0, Qt.Horizontal, '信息')
        model.setHeaderData(1, Qt.Horizontal, '值')

        for subscribe in context.subscribes:
            item = QStandardItem('订阅事件')
            model.appendRow([item, QStandardItem(subscribe)])
            for def_ in context.subscribes[subscribe]:
                item.appendRow([QStandardItem('订阅回调'), QStandardItem(str(def_))])

        return model

    def plugin_extension_def_model(self):
        global context

        model = QStandardItemModel(0, 2)
        model.setHeaderData(0, Qt.Horizontal, '信息')
        model.setHeaderData(1, Qt.Horizontal, '值')

        plugins = context.get_plugins()
        for plugin in plugins:
            # 扩展点
            # extensions_def
            if 'extensions_def' in plugin.config:
                for ext in plugin.config['extensions_def']:
                    model.appendRow([QStandardItem('扩展点名称'), QStandardItem(ext['name'])])
                    model.appendRow([QStandardItem('扩展点定义'), QStandardItem(str(ext['define']))])
            
        return model

    def plugin_event_model(self):
        global context

        model = QStandardItemModel(0, 2)
        model.setHeaderData(0, Qt.Horizontal, '信息')
        model.setHeaderData(1, Qt.Horizontal, '值')

        plugins = context.get_plugins()
        for plugin in plugins:
            # 事件
            if 'events' in plugin.config:
                for event in plugin.config['events']:
                    for prop in event:
                        if prop == 'name':
                            model.appendRow([QStandardItem('事件名称'), QStandardItem(event[prop])])
                        else:
                            prop2 = prop.replace('value', '参数')
                            model.appendRow([QStandardItem(prop2), QStandardItem(event[prop])])
            
        return model

    def plugin_service_model(self):
        global context

        model = QStandardItemModel(0, 2)
        model.setHeaderData(0, Qt.Horizontal, '信息')
        model.setHeaderData(1, Qt.Horizontal, '值')

        plugins = context.get_plugins()
        for plugin in plugins:
            # 服务
            if 'services' in plugin.config:
                for service in plugin.config['services']:
                    model.appendRow([QStandardItem('服务名称'), QStandardItem(service['name'])])
                    model.appendRow([QStandardItem('服务接口'), QStandardItem(str(service['declare']))])
            
        return model

    def plugin_model(self):
        global context

        model = QStandardItemModel(0, 2)
        model.setHeaderData(0, Qt.Horizontal, '插件信息')
        model.setHeaderData(1, Qt.Horizontal, '值')

        plugins = context.get_plugins()
        for plugin in plugins:
            plugin_id = QStandardItem(plugin.config['pluginid'])
            plugin_id_val = QStandardItem('')

            model.appendRow([plugin_id, plugin_id_val])

            # 扩展点
            # extensions_def
            if 'extensions_def' in plugin.config:
                ext_def = QStandardItem('扩展点')
                plugin_id.appendRow([ext_def])
                for ext in plugin.config['extensions_def']:
                    ext_def.appendRow([QStandardItem('扩展点名称'), QStandardItem(ext['name'])])
                    ext_def.appendRow([QStandardItem('扩展点定义'), QStandardItem(str(ext['define']))])
            
            # 扩展
            if 'extensions' in plugin.config:
                ext = QStandardItem('扩展')
                plugin_id.appendRow([ext])
                for ex in plugin.config['extensions']:
                    ext.appendRow([QStandardItem('扩展点名称'), QStandardItem(ex['name'])])
                    ext.appendRow([QStandardItem('扩展实现'), QStandardItem(str(ex['impl']))])
            
            # 服务
            if 'services' in plugin.config:
                services = QStandardItem('服务')
                plugin_id.appendRow([services])
                for service in plugin.config['services']:
                    services.appendRow([QStandardItem('服务名称'), QStandardItem(service['name'])])
                    services.appendRow([QStandardItem('服务实现'), QStandardItem(str(service['define']))])
            
            # 事件
            if 'events' in plugin.config:
                events = QStandardItem('事件')
                plugin_id.appendRow([events])
                for event in plugin.config['events']:
                    for prop in event:
                        if prop == 'name':
                            events.appendRow([QStandardItem('事件名称'), QStandardItem(event[prop])])
                        else:
                            prop2 = prop.replace('value', '参数')
                            events.appendRow([QStandardItem(prop2), QStandardItem(event[prop])])
            
            # 订阅
            if 'subscribes' in plugin.config:
                subscribes = QStandardItem('订阅')
                plugin_id.appendRow([subscribes])
                for subscribe in plugin.config['subscribes']:
                    subscribes.appendRow([QStandardItem('订阅事件'), QStandardItem(subscribe['name'])])
                    subscribes.appendRow([QStandardItem('订阅实现'), QStandardItem(str(subscribe['define']))])

        return model


    def to_standardItemModel(self, data):
        # header
        data_v = json.loads(data)
        cols = len(data_v[0])
        
        model = QStandardItemModel(0, cols)
        for i in range(0,cols):
            model.setHeaderData(i, Qt.Horizontal, data_v[0][i])

        # data
        # - 表示子层
        # 例如：
        # [2,3,4],[-21, 31, 41],[-21, 31, 41]
        last_items = []
        last_items.append({'l': -1, 'item': model})

        for i in range(1, len(data_v)):
            # 获取缩进标记
            level = 0
            text = data_v[i][0]

            for k in range(0, len(text)):
                #print(text[k:k+1])
                if text[k:k+1] == '-':
                    level = k+1
                else:
                    break

            parent_level = level-1
            #print('level:', level, '  parent:', parent_level)
            #print(last_items)
            while True:
                parent = last_items[-1]
                if parent['l'] > parent_level:
                    last_items.pop()
                else:
                    break
            
            # 构建QStandardItem
            list_item = []
            for j in range(0, len(data_v[i])):
                list_item.append(QStandardItem(data_v[i][j]))
            
            #print('parent:', parent['item'])
            #print('child', list_item[0])
            parent['item'].appendRow(list_item)

            last_items.append({'l': level, 'item': list_item[0]})

        return model


class PaneExtensionToolbar:
    def __init__(self):
        self._file = None

    def add_menu(self, menu_bar):
        self.plugin_menu = menu_bar.addMenu('Plugin')
        self.plugin_action = self.plugin_menu.addAction('Show')
        self.plugin_action.triggered.connect(self.show_plugins)
        
    def show_plugins(self, obj):
        # 通过对话框进行展示
        # 对话框内构建多个TAB页面进行不同视角的结果展示
        self.dialog = PluginsShowDialog()
        self.dialog.setModal(True)
        self.dialog.show()
        
config = {
    'pluginid': 'UI::Core::PluginExpore',
    "extensions" : [
        {
            "name": "PL::Basic::Menu",
            "impl": PaneExtensionToolbar()
        }
    ]
}