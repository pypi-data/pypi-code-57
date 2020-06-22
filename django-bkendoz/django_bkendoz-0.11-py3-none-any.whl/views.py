# import {{{1
import json
from django.db.models.functions import Concat
from django.core import serializers
from django.urls import path
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View, RedirectView
from django.views.generic.edit import FormView
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin

import pyexcel

from .forms import get_generic_form, ImportXlsForm
from .core import get_color_from_class, get_layout_data, get_model_fields_raw, get_model_fields

# list {{{1
class GenericListView(PermissionRequiredMixin, ListView):
    template_name = 'genviews/list.html'
    list_cls = 'generic-list'
    fields = "__all__" 

    def __init__(self, **kwargs):
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.view_{self.model.__name__.lower()}'
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = self.get_list_title();
        context['fields'] = self.get_fields();
        context['list_cls'] = self.list_cls
        context['list_menu'] = self.model.get_list_menu()
        context['layout_data'] = get_layout_data()
        return context

    def get_list_title(self):
        if hasattr(self.model, "LIST_TITLE"):
            return self.model.LIST_TITLE
        else:
            return self.model._meta.verbose_name_plural;

    def get_fields(self):
        if not hasattr(self.model, "VIEWS_STRUCT"):
            print(f"Warning : trying to generate generic list without VIEW_STRUCT with model {self.model.__name__}")
            return get_model_fields(self.model, '__all__')

        fields = self.model.VIEWS_STRUCT["list"]["fields"]
        return get_model_fields(self.model, fields)

# create {{{1
class GenericCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'genviews/form.html'
    color_classes = []

    def __init__(self, **kwargs):
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.add_{self.model.__name__.lower()}'

        if not self.form_class:
 
            if hasattr(self.model, 'VIEWS_STRUCT'):
                if 'create' in self.model.VIEWS_STRUCT and 'fields' in self.model.VIEWS_STRUCT['create']:
                    self.fields = self.model.VIEWS_STRUCT['create']['fields']

            self.form_class = get_generic_form(self.model, self.fields)
            self.fields = None
            self.initial = {'model': self.model}
            super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        current_app = self.request.resolver_match.namespace 
        context = super().get_context_data(**kwargs)
        context['form_title'] = _("Nouveau") + " " + \
              self.model._meta.verbose_name.lower()
        context['form_action'] = reverse_lazy(f"{current_app}:{self.model.__name__.lower()}-create")
        context['layout_data'] = get_layout_data()

        if len(self.color_classes) > 0:
            context['color_palette'] = get_color_from_class(self.color_classes)
       

        print(context)

        return context

    def get_success_url(self):
        if self.success_url:
            return reverse_lazy(self.success_url)
        else:
            current_app = self.request.resolver_match.namespace
            return reverse_lazy(f"{current_app}:{self.model.__name__.lower()}-list")
#update {{{1
class GenericUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'genviews/form.html'
    color_classes = []

    def __init__(self, **kwargs):
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.change_{self.model.__name__.lower()}'

        if not self.form_class:
            self.form_class = get_generic_form(self.model, self.fields)
            self.fields = None
            self.initial = {'model': self.model}
            super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        current_app = self.request.resolver_match.namespace
        context = super().get_context_data(**kwargs)
        context['form_title'] = f"{self.model._meta.verbose_name} {str(self.object)}"
        context['form_action'] = reverse_lazy(
          f"{current_app}:{self.model.__name__.lower()}-update", args=[self.object.pk])
        context['layout_data'] = get_layout_data()
        
        if len(self.color_classes) > 0:
            context['color_palette'] = get_color_from_class(self.color_classes)
        return context

    def get_success_url(self):
        if self.success_url:
            return reverse_lazy(self.success_url)
        else:
            current_app = self.model._meta.app_label
            return reverse_lazy(f"{current_app}:{self.model.__name__.lower()}-detail", args=[self.object.pk])

# detail {{{1
class GenericDetailView(PermissionRequiredMixin, DetailView):
    template_name = 'genviews/detail.html'

    def __init__(self, **kwargs):
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.view_{self.model.__name__.lower()}'
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        current_app = self.request.resolver_match.namespace

        context = super().get_context_data(**kwargs)
        context['layout_data'] = get_layout_data()
        
        if hasattr(self.model, 'VIEWS_STRUCT'):
            if 'detail' in self.model.VIEWS_STRUCT and 'tpl' in self.model.VIEWS_STRUCT['detail']:
                context['obj_tpl'] = self.model.VIEWS_STRUCT['detail']['tpl']

        if hasattr(self, 'actions_extra'):
            context['actions_extra'] = self.actions_extra

        if hasattr(self, 'template_extra'):
            context['template_extra'] = self.template_extra

        return context
#delete {{{1
class GenericDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'genviews/delete.html'

    def __init__(self, **kwargs):
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.delete_{self.model.__name__.lower()}'
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        current_app = self.request.resolver_match.namespace
        context = super().get_context_data(**kwargs)
        context['back_url'] = f"{current_app}:{self.model.__name__.lower()}-detail"
        context['layout_data'] = get_layout_data()
        return context

    def get_success_url(self):
        if self.success_url:
            return reverse_lazy(self.success_url)
        else:
            current_app = self.request.resolver_match.namespace
            return reverse_lazy(f"{current_app}:{self.model.__name__.lower()}-list")

#history {{{1
class GenericHistoryView(PermissionRequiredMixin, DetailView):
    template_name = 'genviews/history.html'

    def __init__(self, **kwargs):
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.history_{self.model.__name__.lower()}'
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        current_app = self.request.resolver_match.namespace
        context = super().get_context_data(**kwargs)
        context['layout_data'] = get_layout_data()
        context['object_list'] = self.object.history.all()
        context['fields'] = get_model_fields(self.model, self.fields)
        return context

#exportxls {{{1
class GenericExportxlsView(PermissionRequiredMixin, View):
    def __init__(self, **kwargs):
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.exportxls_{self.model.__name__.lower()}'
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        if hasattr(self.model, 'get_excel_dict'):
            xls_file = pyexcel.save_as(dest_file_type="xls", adict=self.model.get_excel_dict())
            response = FileResponse(xls_file, as_attachment=True,
                                    filename=f"{self.model.__name__.lower()}_export.xls")
            return response

        else: 
            if self.fields == '__all__':
                objects = self.model.objects.values()
            else:
                # objects = self.model.objects.values(*self.fields)
                objects = self.model.objects.values(*self.fields)

            xls_file = pyexcel.save_as(dest_file_type="xls", records=objects)
            response = FileResponse(xls_file, as_attachment=True,
                  filename=f"{self.model.__name__.lower()}_export.xls")
            return response

#importxls {{{1
class GenericImportxlsView(PermissionRequiredMixin, FormView):
    template_name = 'genviews/import_xls.html'
    form_class = ImportXlsForm

#init {{{2
    def __init__(self, **kwargs):
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.importxls_{self.model.__name__.lower()}'
        super().__init__(**kwargs)

#get context data {{{2
    def get_context_data(self, **kwargs):
        current_app = self.request.resolver_match.namespace
        context = super().get_context_data(**kwargs)
        context['form_title'] = f"Importer des données excel"
        context['form_subtitle'] = self.model._meta.verbose_name
        context['fields'] = self.model.get_fields_data(self.fields)
        context['import_sample'] = self.model.get_samples()
        context['layout_data'] = get_layout_data()
        return context

#form_valid {{{2
    def form_valid(self, form):
        xls_file = form.files['xls_file']
      # print(pyexcel.get_sheet(file_type='xls', file_content=xls_file))
        records = pyexcel.get_records(file_type='xls', file_content=xls_file)

        context = self.get_context_data()
        context['preview'] = True
        context['object_list'] = self.model.create_object_list_from_records(
                records, self.fields)
        context['fields'] = get_model_fields(self.model, self.fields)
        context['model_plural'] = self.model._meta.verbose_name_plural
        context['form_action'] = f"{self.current_app}:{self.model.__name__.lower()}-importxlssave"

        return render(self.request, self.template_name,
              context=context)

      #importxls save {{{1
class GenericImportxlssaveView(PermissionRequiredMixin, View):
    def post(self, request):
        for key, value in request.POST.items():
            if key.startswith("chk_"):
                if value == "off":
                    continue

                index = key.split("_")[1]
                data = json.loads(request.POST[index])
                m = self.model(**self.model.extract_json_dict(data))
                m.save()

        return redirect(reverse_lazy(f"{self.current_app}:{self.model.__name__.lower()}-list"))

#init {{{2
    def __init__(self, **kwargs):
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.importxlssave_{self.model.__name__.lower()}'
        super().__init__(**kwargs)




#   def form_valid(self, form):
#      def testinit(row):
#         # self.model.book_category.field.related_model
#         i = 0
#         new_row = []
#         for field_name in self.fields:
#            related_model = getattr(self.model, field_name).field.related_model
#            if related_model:
#               new_row.append(related_model.objects.get(pk=row[i]))
#            else:
#               new_row.append(row[i])
#            i = i + 1

#         print(new_row)
#         return new_row

#      xls_file = form.files['xls_file']
#      #print(pyexcel.get_sheet(file_type='xls', file_content=xls_file))
#      pyexcel.save_as(file_content=xls_file, file_type='xls',
#                            dest_initializer=testinit,
#                            dest_model=self.model,
#                       start_row=1,
#                       colnames=["book_category", "name"],
#                       dest_mapdict=["book_category", "name"]
#                      )

#      return super().form_valid(form)

#    def get_success_url(self):
#        if self.success_url:
#           return reverse_lazy(self.success_url)
#        else:
#           current_app = self.request.resolver_match.namespace
#           return reverse_lazy(f"{current_app}:{self.model.__name__.lower()}-importxls-preview")

##get {{{2
#   def get(self, request, *args, **kwargs):
#      if self.fields == '__all__':
#         objects = self.model.objects.values()
#      else:
#         objects = self.model.objects.values(*self.fields)

#      xls_file = pyexcel.save_as(dest_file_type="xls", records=objects)
#      response = FileResponse(xls_file, as_attachment=True,
#                              filename=f"{self.model.__name__.lower()}_import.xls")
#      return response
#      # return HttpResponse(xls_file, content_type="application/vnd.ms-excel")
#   pass

# create_model_paths {{{1
def get_gen_path_from_model(model):
    mod_name = model.__name__
    mod_name_low = mod_name.lower()
    path_to_return = []
# get_fields {{{
    def get_fields(view):
        fields = model.get_view_fields(view.lower())
        if fields[0] == "__all__":
            return get_model_fields_raw(model, "__all__")
        else:
            return fields
# }}}
    
    if not hasattr(model, "GENERIC_VIEW_LIST"):
        print(f"Warning : trying to generate generic views without GENERIC_VIEW_LIST with model {model.__name__}")
        return []

    for view in model.GENERIC_VIEW_LIST:
        # print(get_fields(view))
        # print(mod_name + view)
        ClassView = type(
              # name
              mod_name + view + "View", 
              # subclasses
              (globals()['Generic' + view + 'View'], ),
              # attr
              {
                  "model": model,
                  "fields": get_fields(view)
                  }
              )

        view_path = mod_name_low + 's/' + view.lower()
        if view in ['Update', 'Detail', 'Delete', 'History']:
            view_path += '/<int:pk>'

        path_to_return.append(
              path(
                  view_path,
                  ClassView.as_view(),
                  name=mod_name_low + '-' + view.lower()
                  )
              )
    return path_to_return
