from rolepermissions.permissions import register_object_checker
from django.contrib.auth.models import User
from corgy_erp.roles import Common

@register_object_checker()
def access_commons(role, user: User, commons):
    return user.is_active