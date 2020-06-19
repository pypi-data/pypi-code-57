import copy

from rest_framework.permissions import BasePermission, DjangoModelPermissions


class ChangeSubjectPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_perm('subjects.change_subject')


class DjangoModelPermissionsWithViewCheck(DjangoModelPermissions):
    def __init__(self):
        # we need assign a copy to perms_map since it is a class-variable of DjangoModelPermissions
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
