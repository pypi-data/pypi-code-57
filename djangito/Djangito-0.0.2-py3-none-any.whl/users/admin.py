from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Company
# from config.admin import custom_admin_site
from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _
# from .forms import UserChangeForm, UserCreationForm


class UserAdminPlus(UserAdmin):
    # form = UserChangeForm
    # add_form = UserCreationForm
    # fieldsets = (("User", {"fields": ("company",)}),) + UserAdmin.fieldsets
    readonly_fields = ('is_staff', 'is_superuser', 'groups', 'user_permissions')
    list_display = ["username", "last_login", "company", "is_superuser", "is_staff", "is_active", "permission_groups"]
    search_fields = ('username', 'first_name', 'last_name', 'email',)  # Ref: https://stackoverflow.com/questions/5768165/django-search-fields-foreign-key-not-working
    # filter_horizontal = ('groups', 'user_permissions',)
    # filter_horizontal = ('groups', 'user_permissions',)
    # tldr: add company and remove user_permissions from fieldset
    fieldsets = (("User", {"fields": ("company",)}),) + (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            # 'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    def permission_groups(self, obj) -> str:
        # tldr: add field to changelist
        lst = []
        for group in obj.groups.all():
            lst.append(str(group))
        return ','.join(lst)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'primary_activity']


admin.site.register(User, UserAdminPlus)
admin.site.register(Company, CompanyAdmin)
