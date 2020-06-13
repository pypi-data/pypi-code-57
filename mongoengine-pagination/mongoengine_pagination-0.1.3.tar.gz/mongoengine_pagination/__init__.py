import mongoengine
from .lib.pagination import Pagination

print('''
##################################################################################################################
##################################################################################################################
how to use mongoengine_pagination？                           |##| 
examples：                                                    |##|
1、                                                           |##|
class User(DocumentPro):                                      |##|
    user_id = IntField()                                      |##|
    name = StringField()                                      |##|
                                                              |##|
page_index = 2                                                |##|
page_size = 20                                                |##|
user_list = User.objects().paginate(page_index, page_size)    |##|
                                                              |##|
result_list = result.items                                    |##|
total_items = result.total                                    |##|
total_page = result.pages                                     |##|
##################################################################################################################
####### ↑↑↑ User Guide ↑↑↑ ###########################################################################################
''')


class BaseQuerySet(mongoengine.QuerySet):
    def paginate(self, page, per_page, **kwargs):
        return Pagination(self, page, per_page)

    def paginate_field(self, field_name, doc_id, page, per_page, total=None):
        item = self.get(id=doc_id)
        count = getattr(item, field_name + "_count", '')
        total = total or count or len(getattr(item, field_name))
        return ListFieldPagination(self, doc_id, field_name, page, per_page,
                                   total=total)


class DocumentPro(mongoengine.Document):
    meta = {'abstract': True,
            'queryset_class': BaseQuerySet}

    def paginate_field(self, field_name, page, per_page, total=None):
        count = getattr(self, field_name + "_count", '')
        total = total or count or len(getattr(self, field_name))
        return ListFieldPagination(self.__class__.objects, self.pk, field_name,
                                   page, per_page, total=total)


class ListFieldPagination(Pagination):

    def __init__(self, queryset, doc_id, field_name, page, per_page,
                 total=None):
        if page < 1:
            assert False, ('"page_index" is not allowed to be less than 1')

        self.page = page
        self.per_page = per_page

        self.queryset = queryset
        self.doc_id = doc_id
        self.field_name = field_name

        start_index = (page - 1) * per_page

        field_attrs = {field_name: {"$slice": [start_index, per_page]}}

        qs = queryset(pk=doc_id)
        self.items = getattr(qs.fields(**field_attrs).first(), field_name)
        self.total = total or len(getattr(qs.fields(**{field_name: 1}).first(),
                                          field_name))

        if not self.items and page != 1:
            assert False, ('"page_index" is not allowed to be less than 1')

    def prev(self, error_out=False):
        assert self.items is not None, ('a query object is required '
                                        'for this method to work')
        return self.__class__(self.queryset, self.doc_id, self.field_name,
                              self.page - 1, self.per_page, self.total)

    def next(self, error_out=False):
        assert self.items is not None, ('a query object is required '
                                        'for this method to work')
        return self.__class__(self.queryset, self.doc_id, self.field_name,
                              self.page + 1, self.per_page, self.total)
