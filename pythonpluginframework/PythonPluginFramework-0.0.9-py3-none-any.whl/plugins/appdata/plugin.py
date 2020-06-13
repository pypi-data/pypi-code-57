import os
import sys

sys.path.append(os.path.dirname(__file__))

import base_data as DS
import dataservice_xml as DSXML
import dataservice_reg as DSREG

context = None

def init(context_):
    global context
    context = context_
    DS.context = context_
    DSXML.context = context_
    DSREG.context = context_


DataServiceExtension = '''
class DataService:
    def __init__(self):
        pass
    def service_id(self):
        pass
    def project_file(self):
        pass
    def root_node(self):
        pass
    def create_rootnode(self, name):
        pass
    def create_node(self, kind, name):
        pass
    def load(self, file_):
        pass
    def save(self, file_):
        pass
'''



class DataServiceManage:
    def __init__(self):
        self.service = None
    def config(self, main_service):
        #print('config in DataServiceManage: ', main_service)
        exts = context.find_extension("Core::DataService")
        for ext in exts:
            if ext.service_id() == main_service:
                self.service = ext
                break
            
        if len(exts)>0 and self.service == None:
            self.service = exts[0]
    def project_file(self):
        return self.service.project_file()
    def project_file_des(self):
        return {
            "des":"获取项目文件", 
            "name": "project_file",
            "return": "项目保存文件"
        }

    def root_node(self):
        return self.service.root_node()
    def root_node_des(self):
        return {
            "des":"获取根节点", 
            "name": "root_node",
            "return": "项目根节点"
        }

    def create_rootnode(self, name):
        return self.service.create_rootnode(name)
    def create_rootnode_des(self):
        return {
            "des":"创建根节点", 
            "name": "create_rootnode",
            "return": "项目根节点",
            'paras':[
                {
                    'name': 'name',
                    'des': '根节点名称'
                }
            ]
        }

    def create_node(self, kind, name):
        return self.service.create_node(kind, name)
    def create_node_des(self):
        return {
            "des":"创建节点", 
            "name": "create_node",
            "return": "创建节点",
            'paras':[
                {
                    'name': 'kind',
                    'des': '节点类型'
                },
                {
                    'name': 'name',
                    'des': '节点名称'
                }
            ]
        }
    
    def load(self, file_):
        return self.service.load(file_)
    def load_des(self):
        return {
            "des":"加载项目", 
            "name": "load",
            "return": "",
            'paras':[
                {
                    'name': 'file_',
                    'des': '项目文件'
                }
            ]
        }

    def save(self, file_):
        return self.service.save(file_)
    def save_des(self):
        return {
            "des": "保存项目", 
            "name": "save",
            "return": "",
            'paras':[
                {
                    'name': 'file_',
                    'des': '项目保存结果文件'
                }
            ]
        }

_g_dataservice_ = DataServiceManage()
_g_config_ = None

# 服务接口描述
def dataservice_declare():
    decl = []
    for fun in dir(_g_dataservice_):
        if type(fun) != type(''):
            continue

        if fun+"_des" in dir(_g_dataservice_):
            decl.append(eval('_g_dataservice_.'+fun+'_des()'))
    
    return decl

config = {
    'pluginid': 'Core::AppData',
    "services" : [
        {
            "name": "DataService",
            "define": _g_dataservice_,
            'declare': dataservice_declare()
        },
        {
            "name": "DataNodeRegService",
            "define": DSREG.g_datanode_kind_service,
            'declare': DSREG.dataservice_declare()
        }
    ],
    "extensions_def" : [
        {
            "name": "Core::DataService",
            "define": DataServiceExtension
        },
        {
            'name': "Core::DataNode::Reg",
            'define': DSREG.DataNodeExtension
        }
    ],
    "extensions" : [
        {
            "name": "Core::DataService",
            "impl": DSXML.DataServiceXML("./configs/dataservice_config.xml")
        },
        {
            "name": "Core::DataService",
            "impl": DSREG.DataServiceREG()
        },
        {
            "name": "Core::DataNode::Reg",
            "impl": DSREG.DataNodeProject()
        },
        {
            "name": "Core::DataNode::Reg",
            "impl": DSREG.DataNodeGroup()
        },
        {
            "name": "Core::DataNode::Reg",
            "impl": DSREG.DataNodeFile()
        },
    ],
    'events' : [
        {
            'name': 'event::NewRootDataNode',
            'value1': 'DataNode'
        },
        {
            'name': 'event::Project::Open',
            'value1': 'DataNode'
        },
        {
            'name': 'event::NewDataNode',
            'value1': 'DataNode'
        },
        {
            'name': 'event::DataNode::Delete',
            'value1': 'DataNode'
        },
        {
            'name': 'event::DataNode::Modify::Name',
            'value1': 'DataNode',
            'value2': 'string'    # old name

        },
        {
            'name': 'event::DataNode::Modify::Prop',
            'value1': 'DataNode',
            'value2': 'string',  # prop key
            'value3': 'string'   # old prop value
        },
        {
            'name': 'event::DataNode::Modify::AddChild',
            'value1': 'DataNode',
            'value2': 'DataNode'  # child
        },
        {
            'name': 'event::DataNode::Modify::RemoveChild',
            'value1': 'DataNode',
            'value2': 'DataNode'  # child
        },
        {
            'name': 'event::DataNode::Select',
            'value1': 'DataNode'
        },
    ]
}