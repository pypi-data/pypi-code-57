import re
import copy
import hashlib
from django.urls import reverse
from .settings import DJANGO_ADMIN_GLOBAL_SIDEBAR_MENUS

def has_menu_permissions(user, menu):
    if not "permissions" in menu:
        return True
    for permissions in menu["permissions"]:
        if isinstance(permissions, str):
            permissions = [permissions]
        if user.has_perms(permissions):
            return True
    return False

def get_menu_url(menu):
    if "url" in menu:
        return menu["url"]
    elif "model" in menu:
        app_label, model_name = menu["model"].split(".")
        return reverse("admin:{}_{}_changelist".format(app_label, model_name))
    elif "view" in menu:
        view_name = menu["view"]
        return reverse(view_name)
    else:
        return "#"

def _fix_menu_id(menu):
    if not "id" in menu:
        menu["id"] = "id" + hashlib.md5(menu["title"].encode("utf-8")).hexdigest()
    return menu["id"]

def _fix_menu_url(menu):
    menu["url"] = get_menu_url(menu)
    return menu["url"]

def _fix_menu_active(menu, request):
    active_patterns = menu.get("active_patterns")
    if not active_patterns:
        if "model" in menu:
            active_patterns = "^(" + menu["url"] + ".*)$"
        else:
            active_patterns = "^" + menu["url"] + "$"
    if isinstance(active_patterns, str):
        active_patterns = [active_patterns]
    menu["active"] = False
    for active_pattern in active_patterns:
        if re.match(active_pattern, request.path):
            menu["active"] = True
            break
    return menu["active"]

def get_user_menus(request):
    menus = []
    user = request.user
    for menu1 in copy.deepcopy(DJANGO_ADMIN_GLOBAL_SIDEBAR_MENUS):
        _fix_menu_id(menu1)
        _fix_menu_url(menu1)
        _fix_menu_active(menu1, request)
        if not "children" in menu1:
            if has_menu_permissions(user, menu1):
                menus.append(menu1)
        else:
            children = []
            active_flag = False
            for menu2 in menu1["children"]:
                if has_menu_permissions(user, menu2):
                    _fix_menu_id(menu2)
                    _fix_menu_url(menu2)
                    flag = _fix_menu_active(menu2, request)
                    if flag:
                        active_flag = True
                    children.append(menu2)
            if active_flag:
                menu1["active"] = True
            if children:
                menu1["children"] = children
                menus.append(menu1)
    return menus
