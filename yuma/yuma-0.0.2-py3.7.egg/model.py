class Permission:
    """
    Permission entity
    """
    # Permission id
    id = 0
    # Permission key
    key = ""
    # Permission memo
    memo = ""
    # Father permission id
    # The parent ID of the root permission is -1
    father_id = -1

    def __init__(self, permission_id: int, key: str, memo: str, father_id: int = -1):
        """
        Initialize with value
        :param permission_id: Permission id
        :param key: Permission key
        :param memo: Permission memo
        :param father_id: Father permission id
        """
        self.id = permission_id
        self.key = key
        self.memo = memo
        self.father_id = father_id


class PermissionGroup:
    """
    Collection of multiple permissions
    """
    # Group key
    key = ""
    # Permissions id list
    _ids = []

    def __init__(self, key):
        """
        Initializing PermissionGroup
        :param key: Group key
        """
        self.key = key

    def add_id(self, permission_id: int):
        """
        Add id to permission group
        :param permission_id: permission id
        :return: self
        """
        self._ids.append(permission_id)
        return self

    def add_ids(self, permission_ids):
        """
        Add id list to permission group
        :param permission_ids: permission_ids
        :return: self
        """
        self._ids = self._ids + permission_ids
        return self

    def have(self, permission_id):
        """
        Check if there is an ID entered in the group
        :param permission_id: permission_id
        :return: Bool
        """
        return permission_id in self._ids
