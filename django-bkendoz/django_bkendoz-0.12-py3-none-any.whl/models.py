import json
from django.db import models
from django.urls import reverse_lazy
from simple_history.models import HistoricalRecords

# GenericModel {{{1
class GenericModel(models.Model):
    LINK_FIELD = 'name'
    GENERIC_VIEW_LIST = ["Create", "Update", "Detail", "List", "Delete"] 
    GENERIC_LIST_MENU = [("Create", "fa-plus")]
    GENERIC_DETAIL_MENU = [
            ("List", "fa-list", []),
            ("Update", "fa-pen", ["id"]),
            ("Delete", "fa-trash", ["id"]),
            ]

    # Meta {{{2
    class Meta:
        abstract = True

    # get_list_menu {{{2
    @classmethod
    def get_list_menu(cls):
        if not hasattr(cls, "GENERIC_LIST_MENU"):
            print(f"Warning : trying to generate list menu without GENERIC_LIST_MENU with model {cls.__name__}")
            return []
        list_menu = []
        for view_name, faclass in cls.GENERIC_LIST_MENU:
            list_menu.append( (cls.get_url(view_name.lower()), faclass) )
        return list_menu

    # get_url {{{2
    @classmethod
    def get_url(cls, view_name):
       if not hasattr(cls, "GENERIC_VIEW_LIST"):
           print(f"Warning : trying to generate generic urls without GENERIC_VIEW_LIST with model {cls.__name__}")
           return False
       root_path = f"{cls._meta.app_label}:{cls.__name__.lower()}-"
       return root_path + view_name


    # get_urls {{{2
    @classmethod
    def get_urls(cls):
       if not hasattr(cls, "GENERIC_VIEW_LIST"):
           print(f"Warning : trying to generate generic urls without GENERIC_VIEW_LIST with model {cls.__name__}")
           return False

       url_dict = {}
       for view in cls.GENERIC_VIEW_LIST:
           view = view.lower()
           url_dict[view] = cls.get_url(view)
       return url_dict
#
#      'create': root_path + '-create',
#      'update': root_path + '-update',
#      'delete': root_path + '-delete',
#      'detail': root_path + '-detail',
#      'list': root_path + '-list',
#      'exportxls': root_path + '-exportxls',
#      'importxls': root_path + '-importxls',
#      'importxlssave': root_path + '-importxlssave',
#

    # get_view_fieds {{{2
    @classmethod
    def get_view_fields(cls, view):
        # TODO pas de field pour certaines vues
        if view in ['delete', 'detail', 'importxlssave']:
            return '__all__'

        if not hasattr(cls, 'VIEWS_STRUCT'):
            print(f"structure de vue non defini pour {cls}")
            return '__all__'

        if view not in cls.VIEWS_STRUCT:
            print(f"structure pour {cls} vue : {view} non defini")
            return '__all__'
        
        if 'fields' not in cls.VIEWS_STRUCT[view]:
            print(f"fields non definis pour {cls} vue : {view}")
            return '__all__'

        return cls.VIEWS_STRUCT[view]['fields']


    # get_fields_data {{{2
    @classmethod
    def get_fields_data(cls, fieldlist):
        field_data = []
        for field in fieldlist:
            if not hasattr(cls, field):
                continue
            field_data.append( (field, getattr(cls, field).field.verbose_name) )
        return field_data

    # extract json dict {{{2
    @classmethod
    def extract_json_dict(cls, json):
        kwargs = {}
        for key,value in json.items():
            related_model = getattr(cls, key).field.related_model
            if related_model:
                kwargs[key] = related_model.objects.get(pk=value)
            else:
                kwargs[key] = value
        return kwargs
 
 
    # extract excel record dict {{{2
    @classmethod
    def extract_record_dict(cls, record):
        kwargs = {}
        for field in record:
            related_model = getattr(cls, field).field.related_model
            if related_model:
                kwargs[field] = related_model.objects.get(pk=record[field])
            else:
                kwargs[field] = record[field]
        return kwargs

    # create object list from excel records {{{2
    @classmethod
    def create_object_list_from_records(cls, records, fields):
        object_list = []
        index = 0
        print(records)
        print(fields)
        for record in records:
            print(record)
            o = cls(**cls.extract_record_dict(record))
            o_dict = {}
            for field in fields:
                related_model = getattr(cls, field).field.related_model
                if related_model:
                    o_dict[field] = getattr(o, field).pk
                else:
                    o_dict[field] = getattr(o, field)
            o.json = json.dumps(o_dict)
            o.index = index
            index += 1
            object_list.append(o)
        return object_list


    # get_list_menu {{{2
    def get_detail_menu(self):
        if not hasattr(self.__class__, "GENERIC_DETAIL_MENU"):
            print(f"Warning : trying to generate detail menu without GENERIC_DETAIL_MENU with model {cls.__name__}")
            return []
        detail_menu = []
        for view_name, faclass, url_args in self.__class__.GENERIC_DETAIL_MENU:
            args = []
            for field in url_args:
                if not hasattr(self, field):
                    print(f"Warning : trying to acces non existent url arg {field} in {self.__class__}")
                    continue
                args.append(getattr(self, field))

            href = reverse_lazy(self.__class__.get_url(view_name.lower()), args=args)
            detail_menu.append( (href, faclass) )
        return detail_menu

    # get samples {{{2
    @classmethod
    def get_samples(cls):
        return [cls(), cls()]

# GenericHistorizedModel {{{1
class GenericHistorizedModel(GenericModel):
    history = HistoricalRecords(inherit=True)
    GENERIC_VIEW_LIST = GenericModel.GENERIC_VIEW_LIST + ["History"]
    #GENERIC_LIST_MENU = GenericModel.GENERIC_LIST_MENU + [("History", "fa-history")]
    GENERIC_DETAIL_MENU = GenericModel.GENERIC_DETAIL_MENU + [
            ("History", "fa-history", ["id"]),
    ]

    @property
    def hist_date(self):
        return self.history_date

    class Meta:
        abstract = True

# GenericExcelModel {{{1
class GenericExcelModel:
   GENERIC_VIEW_LIST = ["Exportxls", "Importxls", "Importxlssave"]
   GENERIC_LIST_MENU = [
           ("Exportxls", "fa-save"),
           ("Importxls", "fa-file-excel")
           ]
