from wagtail.contrib.modeladmin.helpers import PermissionHelper
from wagtail.core.permission_policies.collections import CollectionPermissionPolicy


class CollectionPermissionHelper(PermissionHelper):
    """
    Provides permission-related helper functions to help determine what a
    user can do with a 'typical' model (where permissions are granted
    model-wide), and to a specific instance of that model.
    """

    def __init__(self, model, inspect_view_enabled=False):
        super().__init__(model, inspect_view_enabled)
        self.permission_policy = CollectionPermissionPolicy(model)

    def user_has_specific_permission(self, user, action):
        """
        Delegate to permission policy
        """
        return self.permission_policy.user_has_permission(user, action)

    def user_has_any_permissions(self, user):
        """
        Delegate to permission policy
        """
        return self.permission_policy.user_has_any_permission(
            user, actions=['add', 'change', 'delete']
        )

    def user_has_permission_for_instance(self, user, action, instance):
        return self.permission_policy.user_has_permission_for_instance(
            user, action, instance
        )

    def user_has_any_permission_for_instance(self, user, actions, instance):
        return self.permission_policy.user_has_any_permission_for_instance(
            user, actions, instance
        )

    def user_can_create(self, user):
        return self.user_has_specific_permission(user, action='add')

    def user_can_inspect_obj(self, user, obj):
        """
        Return a boolean to indicate whether `user` is permitted to 'inspect'
        a specific `self.model` instance.
        """
        return self.inspect_view_enabled and self.user_has_any_permission_for_instance(
            user=user, actions=['add', 'change', 'delete'], instance=obj)

    def user_can_edit_obj(self, user, obj):
        return self.user_has_permission_for_instance(user, action='change', instance=obj)

    def user_can_delete_obj(self, user, obj):
        return self.user_has_permission_for_instance(user, action='delete', instance=obj)
