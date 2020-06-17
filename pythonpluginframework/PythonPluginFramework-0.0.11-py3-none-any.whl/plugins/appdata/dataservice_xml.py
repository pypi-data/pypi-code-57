import os
import sys
import json

import xml.etree.ElementTree as ET

sys.path.append(os.path.dirname(__file__))

import base_data as DS

context = None

class DataNodeXML(DS.DataNodeBase):
    def __init__(self, xml_node = None, kind = None, name = None):
        super().__init__(kind, name)

        self._xml_ = xml_node
        if xml_node:
            props = self._xml_.findall('./Props/Prop')
            for prop in props:
                self._props_[prop.attrib['key']] = prop.attrib['default']
    def clone(self):
        new_node = DataNodeXML(self._xml_, self._kind_, self._name_)
        new_node._props_ = json.loads(json.dumps(self._props_))
        new_node._parent_ = self._parent_

        children = []
        for child in self._child_:
            child_clone = child.clone()
            child_clone._parent_ = new_node
            children.append(child_clone)
        new_node._child_ = children
        return new_node

    def get_child_kinds(self):
        children = self._xml_.findall('./children/Node')
        kinds = []
        for child in children:
            kinds.append(child.attrib['kind'])
        return kinds
        
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
            cnode = DataNodeXML()
            cnode.load(service, child)
            self._child_.append(cnode)
            cnode.set_parent(self)
        self._xml_ = service._map_node_[self._kind_]

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

class DataServiceXML:
    def __init__(self, config):
        self._xml_ = ET.ElementTree(file=config)
        self._map_node_ = {}

        root = self._xml_.getroot()
        self._map_node_[root.attrib['kind']] = root

        nodes = self._xml_.findall('.//Node')
        for node in nodes:
            kind = node.attrib['kind']
            if not kind in self._map_node_:
                self._map_node_[kind] = node
                #print(node.attrib['kind'])

        self._root_node_ = None
        self._file_ = None
    def service_id(self):
        return 'Core::DataService::Config::XML'
    def project_file(self):
        return self._file_
    def root_node(self):
        return self._root_node_
    def create_rootnode(self, name):
        root = self._xml_.getroot()

        if self._root_node_:
            return None

        self._root_node_ = DataNodeXML(root, root.attrib['kind'], name)

        context.fire('event::NewRootDataNode', self._root_node_)
        return self._root_node_
    def create_node(self, kind, name):
        if not kind in self._map_node_:
            print("Not exist kind!!")
            return None
        xml = self._map_node_[kind]
        node = DataNodeXML(xml, kind, name)

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
        cnode = DataNodeXML()
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
    def close(self):
        context.fire('event::Project::Close', self._root_node_)
        self._root_node_ = None
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