from yuma.model import Permission, PermissionGroup


class PermissionHolder:
    """
    Permission module
    """
    # Permission map, key (Permission id), value (Permission entity)
    _id_map = {}
    # Permission map, key (Permission key), value (dict)
    # dict["current"] permission entity
    # dict["next"] Other Permission map, key (Permission key), value (dict)
    _key_map = {}
    # Permission group map, key (group key), value (PermissionGroup entity)
    _group_map = {}

    def add_permission(self, permission: Permission):
        """
        Add a permission to holder
        :param permission: Permission entity
        :return: self
        """
        self._id_map[permission.id] = permission
        return self

    def add_permission_group(self, permission_group: PermissionGroup):
        """
        Add a permission_group to holder
        :param permission_group: PermissionGroup
        :return: self
        """
        self._group_map[permission_group.key] = permission_group
        return self

    def build_tree(self):
        """
        Build permission map
        :return: self
        """
        self._key_map = self._build_tree()
        return self

    def _build_tree(self, father_id=-1):
        """
        Build permission map
        :param father_id: father_id
        :return: self
        """
        next_nodes = {}
        for key in self._id_map.keys():
            value = self._id_map[key]
            if value.father_id == father_id:
                next_nodes[value.key] = {
                    "current": value,
                    "next": self._build_tree(value.id)
                }
        return next_nodes

    def get_permission_by_id(self, permission_id: int):
        """
        Get permission entity by permission_id
        :param permission_id: permission_id
        :return: permission entity
        """
        return self._id_map[permission_id]

    def get_id_path_by_key_path(self, key_path: str):
        """
        Get id_path by key_path
        :param key_path: key split by :
        :return: id_path
        """
        current_map = self._key_map
        # get key list by split :
        keys = key_path.split(":")
        # return ids
        ids = []
        for key in keys:
            if key not in current_map:
                return []
            node = current_map[key]
            ids.append(node["current"].id)
            current_map = node["next"]
        return ids

    def verification(self, group_key, key_path, callback=lambda arg: True, **kwargs):
        # group_key non-existent
        if group_key not in self._group_map:
            return False
        group = self._group_map[group_key]
        # Permission key non-existent
        ids = self.get_id_path_by_key_path(key_path)
        if len(ids) == 0:
            return False
        # verification
        for item in ids:
            if not group.have(item):
                return False
        return callback(kwargs)
