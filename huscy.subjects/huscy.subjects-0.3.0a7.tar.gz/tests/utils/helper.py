from django.contrib.auth.models import Permission


def add_permission(user, permission):
    permission = Permission.objects.get(codename=permission)
    user.user_permissions.add(permission)
