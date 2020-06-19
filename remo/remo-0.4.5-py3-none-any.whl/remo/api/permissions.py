from rest_framework import permissions, status
from rest_framework.exceptions import NotFound


class ValidParentPkPermission(permissions.BasePermission):
    message = 'Parent pk is not valid'

    def has_permission(self, request, view):
        if not view.is_valid_parent_pk():
            raise NotFound
        return True


class ValidGrandParentPkPermission(permissions.BasePermission):
    message = 'Grand parent pk is not valid'

    def has_permission(self, request, view):
        if not view.is_valid_grand_parent_pk():
            raise NotFound
        return True
