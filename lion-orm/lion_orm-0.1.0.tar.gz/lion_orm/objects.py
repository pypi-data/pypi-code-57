from lion_orm.query import Query
from lion_orm.query_builder import QueryBuilder
from lion_orm.errors import SaveEmptyModelError, AutoIncrementError, GettingMultipleObjectsError, EmptyDeleteError
from lion_orm.query_set import QuerySet


class Objects(object):
    def __init__(self, model, _class=False):
        if _class:
            self.model_name = model.__name__
        else:
            self.model = model
            self.model_name = model.__class__.__name__
        self._class = _class

    def select(self, **equals):
        where = QueryBuilder.where_equals(**equals) if len(equals) else None
        result = Query(self.model_name).select(where=where)
        query_set = QuerySet(self.model, result)
        return query_set

    def get(self, **equals):
        result = self.select(**equals)
        if len(result) == 0:
            return None
        elif len(result) > 1:
            raise GettingMultipleObjectsError
        return result[0]

    def _save(self):
        self.model.blocked = False
        filled = {}
        empty = {}
        for field_name in self.model.fields:
            if field_name != 'id':
                field = self.model.fields[field_name]
                if field.filled:
                    filled[field_name] = field
                else:
                    empty[field_name] = field
        if len(filled) + len(empty):
            filled_id = self.model.id.filled
            if not filled_id:
                autoincremently = self.model.id.autoincrement
                if autoincremently:
                    if sum(1 for x in empty if empty[x].required):
                        raise SaveEmptyModelError
                    filled = {x: filled[x].value for x in filled}
                    Query(self.model_name).insert(**filled)
                else:
                    raise AutoIncrementError
            else:
                where = QueryBuilder.where_equals(id=self.model.fields['id'].value)
                update(where, **{x: filled[x].value for x in filled})
        self.model.blocked = True
        self.model.actual = True

    def _delete(self):
        id = self.model.id
        if id is None:
            raise EmptyDeleteError
        Query(self.model_name).delete_by_id(id)
