from lion_orm.errors import UsingDeletedQuerySetError


class QuerySetIterator(object):
    def __init__(self, models_list, query_set):
        self.index = 0
        self.list = models_list
        self.query_set = query_set

    def __next__(self):
        if len(self.list) <= self.index:
            raise StopIteration
        result = self.list[self.index]
        self.index += 1
        return result


class QuerySet(object):
    def __init__(self, model, query_result):
        self.model = model
        self.deleted = False
        self.container = []
        fields_names = list(model.fields.keys())
        fields_names.append('id')
        for string in query_result:
            cls = model.__class__
            model = object.__new__(cls)
            values = {name: value for name, value in zip(fields_names, string)}
            model.__init__(**values)
            model.actual = True
            self.container.append(model)

    def delete(self):
        if self.deleted:
            raise UsingDeletedQuerySetError
        for model in self.container:
            model.delete()
        self.deleted = True

    def __iter__(self):
        if self.deleted:
            raise UsingDeletedQuerySetError
        return QuerySetIterator(self.container, self)

    def __getitem__(self, key):
        if self.deleted:
            raise UsingDeletedQuerySetError
        if not (type(key) is int):
            raise TypeError(f'incorrect type of key: {type(key)}')
        size = len(self.container)
        if key < 0 or size == 0 or key >= size:
            raise KeyError
        return self.container[key]

    def __len__(self):
        result = len(self.container)
        return result

    def __str__(self):
        deleted = ', deleted' if self.deleted else ''
        return f'<Query set "{self.model.__class__.__name__}" object of {self.__len__()} elements{deleted}>'
