
import uuid


context = None

# 基础数据节点接口
class DataNode:
    def __init__(self):
        pass
    def __str__(self):
        pass
    def get_name(self):
        pass
    def set_name(self, name):
        pass
    def get_id(self):
        pass
    def get_kind(self):
        pass
    def get_props(self):
        pass
    def get_prop(self, key):
        pass
    def set_prop(self, key, value):
        pass
    def parent(self):
        pass
    def set_parent(self, parent):
        pass
    def add_child(self, child):
        pass
    def insert_child(self, child, pos_child):
        pass
    def get_children(self):
        pass
    def get_children_by_kind(self, kind):
        pass
    def get_allchildren_by_kind(self, kind):
        pass
    def remove_child(self, child):
        pass
    def delete(self):
        pass
    def get_child_kinds(self):
        pass
    def load(self, service, node):
        pass
    def save(self, parent_node):
        pass


class DataNodeBase(DataNode):
    def __init__(self, kind = None, name = None):
        self._kind_ = kind
        self._name_ = name
        self._props_ = {}
        self._parent_ = None
        self._child_ = []
        self._id_ = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(uuid.uuid1())+str(uuid.uuid4())))
    def __str__(self):
        return self._name_
    def get_name(self):
        return self._name_
    def set_name(self, name):
        old_name = self._name_
        self._name_ = name
        context.fire('event::DataNode::Modify::Name', self, old_name)
    def get_id(self):
        return self._id_
    def get_kind(self):
        return self._kind_
    def get_props(self):
        return self._props_
    def get_prop(self, key):
        if key in self._props_:
            return self._props_[key]
        else:
            return ""
    def set_prop(self, key, value):
        if key in self._props_:
            old_value = self._props_[key]
            if value == old_value:
                return 
        else:
            old_value = ""
        self._props_[key] = value

        context.fire('event::DataNode::Modify::Prop', self, key, old_value)
    def parent(self):
        return self._parent_
    def set_parent(self, parent):
        self._parent_ = parent
    def add_child(self, child):
        self._child_.append(child)
        child.set_parent(self)

        context.fire('event::DataNode::Modify::AddChild', self, child)

    def insert_child(self, child, pos_child):
        for i in range(0, len(self._child_)):
            if self._child_[i] == pos_child:
                self._child_.insert(i, child)
                child.set_parent(self)

        context.fire('event::DataNode::Modify::AddChild', self, child)

    
    def get_children(self):
        return self._child_
    def get_children_by_kind(self, kind):
        return [child for child in self._child_ if child.get_kind()==kind ]
    def get_allchildren_by_kind(self, kind):
        result = []
        stack = []
        stack.append(self)

        while len(stack)>0:
            node = stack.pop(-1)
            if node.get_kind() == kind:
                result.append(node)
            
            for c in node.get_children():
                stack.append(c)
        
        return result

    def remove_child(self, child):
        self._child_.remove(child)

        context.fire('event::DataNode::Modify::RemoveChild', self, child)
    def delete(self):
        # delete all child
        for child in self._child_:
            child.delete()
        if self._parent_:
            self._parent_.remove_child(self)
        context.fire('event::DataNode::Delete', self)
    
