from django.contrib.auth.models import Permission
from wagtail.admin.forms.collections import collection_member_permission_formset_factory
from wagtail.contrib.modeladmin.options import ModelAdmin
from wagtail.contrib.modeladmin.views import \
    CreateView as CreateViewModelAdmin, EditView as EditViewModelAdmin, IndexView as IndexViewModelAdmin
from django.utils.translation import gettext as _
from wagtail.core import hooks
from wagtail.core.models import Collection

from collectionmodeladmin.permissions import CollectionPermissionHelper


class IndexView(IndexViewModelAdmin):
    def get_queryset(self, request=None):
        user = self.request.user
        collections = self.permission_helper.permission_policy._collections_with_perm(user, ['add', 'change', 'delete'])
        if 'collection_id' in self.params and self.params.get('collection_id') == '':
            del self.params['collection_id']
        return super().get_queryset(request).filter(collection__in=collections)

    def get_context_data(self, **kwargs):
        user = self.request.user
        collections = self.permission_helper.permission_policy._collections_with_perm(user, ['add', 'change', 'delete'])
        context = {
            'collections': collections
        }
        if 'collection_id' in self.params:
            current_collection = Collection.objects.get(id=self.params.get('collection_id'))
            context.update({'current_collection': current_collection})

        context.update(kwargs)

        return super().get_context_data(**context)


class CreateView(CreateViewModelAdmin):

    def get_form_class(self):
        form_class = super().get_form_class()
        user = self.request.user

        # If user is superuser then return form_class as is
        # Else filter the collections
        if user.is_superuser:
            return form_class
        else:
            collections = self.permission_helper.permission_policy._collections_with_perm(user, ['add', 'change', 'delete'])
            form_class.base_fields['collection'].queryset = collections
            form_class.base_fields['collection'].choices.queryset = collections
            return form_class


class EditView(EditViewModelAdmin):

    def get_form_class(self):
        form_class = super().get_form_class()
        user = self.request.user

        # If user is superuser then return form_class as is
        # Else filter the collections
        if user.is_superuser:
            return form_class
        else:
            collections = self.permission_helper.permission_policy._collections_with_perm(user, ['add', 'change', 'delete'])
            form_class.base_fields['collection'].queryset = collections
            form_class.base_fields['collection'].choices.queryset = collections
            return form_class


class CollectionModelAdmin(ModelAdmin):
    index_view_class = IndexView
    create_view_class = CreateView
    edit_view_class = EditView
    permission_helper_class = CollectionPermissionHelper
    index_template_name = 'collectionmodeladmin/index.html'

    def get_permissions_for_registration(self):
        return Permission.objects.none()


def collection_modeladmin_register(modeladmin_class):
    """
    Method for registering CollectionModelAdmin or CollectionModelAdminGroup classes with Wagtail.
    """
    instance = modeladmin_class()
    instance.register_with_wagtail()

    @hooks.register('register_group_permission_panel')
    def register_collection_model_permissions_panel():
        return collection_member_permission_formset_factory(
            modeladmin_class.model,
            [
                ('add_%s' % modeladmin_class.model._meta.model_name, _("Add"), _("Add/edit %s you own" % modeladmin_class.model._meta.verbose_name)),
                ('change_%s' % modeladmin_class.model._meta.model_name, _("Edit"), _("Edit any %s" % modeladmin_class.model._meta.verbose_name)),
            ],
            "collectionmodeladmin/permissions/includes/collectionmodel_permissions_formset.html"
        )

    return modeladmin_class
