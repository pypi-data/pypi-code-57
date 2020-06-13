import os
import sys

import xml.etree.ElementTree as ET

sys.path.append(os.path.dirname(__file__))

import base_data as DS

context = None

'''
    DataNode  kind = 'File'
                props 
                    prop  key=''  value=''
                parent kind = ['...', '...']
                child_kind = ['...', '...']
'''

DataNodeExtension = '''
class DataNode:
    def get_kind(self):
        pass
    def get_props(self):
        pass
    def get_parents(self):
        pass
    def get_children(self):
        pass
'''

# 测试数据结构扩展
class DataNodeProject:
    def get_kind(self):
        return "TestProject"
    def get_props(self):
        return {
            'key1': {
                'type': 'String',
                'default': 'project1'
            }
        }
    def get_parents(self):
        return []
    def get_children(self):
        return []
class DataNodeGroup:
    def get_kind(self):
        return "TestGroup"
    def get_props(self):
        return {
            'key1': {
                'type': 'String',
                'default': 'group1'
            }
        }
    def get_parents(self):
        return ['TestProject', 'TestGroup']
    def get_children(self):
        return []
class DataNodeFile:
    def get_kind(self):
        return "TestFile"
    def get_props(self):
        return {
            'key1': {
                'type': 'String',
                'default': 'file1'
            }
        }
    def get_parents(self):
        return ['TestGroup']
    def get_children(self):
        return []


class DataNodeKindService:
    def __init__(self):
        self.root_node = None
        self.nodes = {}
    def config_des(self):
        return {
            "des": "配置应用更节点数据类型", 
            "name": "config_des",
            "return": "",
            'paras':[
                {
                    'name': 'root_kind',
                    'des': '应用根节点数据类型'
                }
            ]
        }
    def config(self, root_kind):
        global context
        exts = context.find_extension("Core::DataNode::Reg")
        for ext in exts:
            kind = ext.get_kind()
            props = ext.get_props()
            parents = ext.get_parents()
            childs  = ext.get_children()

            if kind not in self.nodes:
                self.nodes[kind] = {
                    'props': {},
                    'children': []
                }
            
            for prop in props:
                self.nodes[kind]['props'][prop] = props[prop]
            for child in childs:
                if child not in self.nodes[kind]['children']:
                    self.nodes[kind]['children'].append(child)
            for parent in parents:
                if parent not in self.nodes:
                    self.nodes[parent] = {
                        'props': {},
                        'children': []
                    }
                if kind not in self.nodes[parent]['children']:
                    self.nodes[parent]['children'].append(kind)

            if kind == root_kind:
                self.root_node = kind

        #print(self.nodes)
    
    def get_root_kind(self):
        return self.root_node
    def get_child_kind(self, parent):
        if parent not in self.nodes:
            return []
        return self.nodes[parent]['children']
    def get_props(self, kind):
        if kind not in self.nodes:
            return {}
        return self.nodes[kind]['props']


g_datanode_kind_service = DataNodeKindService()

def dataservice_declare():
    decl = []
    for fun in dir(g_datanode_kind_service):
        if type(fun) != type(''):
            continue

        if fun+"_des" in dir(g_datanode_kind_service):
            decl.append(eval('g_datanode_kind_service.'+fun+'_des()'))
    
    return decl

class DataNodeReg(DS.DataNodeBase):
    def __init__(self, kind = None, name = None):
        super().__init__(kind, name)

        # 获取数据节点属性定义
        #print('------------------------->> DataNodeReg():', kind, name)
        if kind != None:
            props = g_datanode_kind_service.get_props(kind)
            #print('props:', props)
            for prop in props:
                self._props_[prop] = props[prop]['default']

    def get_child_kinds(self):
        return g_datanode_kind_service.get_child_kind(self._kind_)
        
    def load(self, service, node):
        self._name_ = node.attrib['name']
        self._kind_ = node.attrib['kind']

        if 'id' in node.attrib:
            self._id_ = node.attrib['id']

        print("Load Node", self._name_, self._kind_)

        props = node.findall('./Props/Prop')
        for prop in props:
            self._props_[prop.attrib['key']] = prop.attrib['value']
        
        children = node.findall('./Children/Node')
        for child in children:
            cnode = DataNodeReg()
            cnode.load(service, child)
            self._child_.append(cnode)
            cnode.set_parent(self)

    def save(self, parent_node):
        element = ET.Element('Node')
        element.set('kind', self._kind_)
        element.set('name', self._name_)
        element.set('id', self._id_)
        props = ET.Element('Props')
        element.append(props)
        for prop in self._props_:
            propn = ET.Element('Prop')
            propn.set('key', prop)
            propn.set('value', self._props_[prop])
            props.append(propn)
        children = ET.Element("Children")
        element.append(children)
        for child in self._child_:
            child.save(children)
        parent_node.append(element)

class DataServiceREG:
    def __init__(self):
        self._root_node_ = None
        self._file_ = None
    def service_id(self):
        return 'Core::DataService::Config::REG'
    def project_file(self):
        return self._file_
    def root_node(self):
        return self._root_node_
    def create_rootnode(self, name):
        kind = g_datanode_kind_service.get_root_kind()
        self._root_node_ = DataNodeReg(kind, name)

        context.fire('event::NewRootDataNode', self._root_node_)
        return self._root_node_
    def create_node(self, kind, name):
        node = DataNodeReg(kind, name)

        context.fire('event::NewDataNode', node)
        return node
    def load(self, file_):
        tree = ET.parse(file_)
        root = tree.getroot()

        children = root.findall('./Node')
        if len(children) != 1:
            return 

        self._file_ = file_        
        pnode = children[0]
        cnode = DataNodeReg()
        cnode.load(self, pnode)
        self._root_node_ = cnode

        context.fire('event::Project::Open', self._root_node_)

        return ""
    def save(self, file_):
        root = ET.Element('Root')      
        tree = ET.ElementTree(root)    

        if self._root_node_:
            self._root_node_.save(root)
        
        self.__indent(root)
        tree.write(file_, encoding='utf-8', xml_declaration=True)

        self._file_ = file_
        return ""
    def __indent(self, elem, level=0):
        i = "\n" + level*"\t"
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "\t"
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.__indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i