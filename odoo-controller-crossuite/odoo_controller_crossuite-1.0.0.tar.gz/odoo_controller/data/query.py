# data/query.py

class Query:

    # constructor
    def __init__(self):
        self.search_params = []
        self.modifiers = {}

    # method to add search parameter evaluated as "AND"
    def add_and(self, field, operator, value):
        self.search_params.append((field, operator, value))
        return self

    # method to add search parameter(s) evaluated as "AND"
    def add_and_list(self, *args):
        for item in args:
            self.search_params.append(item)
        return self

    # method to add search parameter(s) evaluated as "OR"
    def add_or_list(self, *args):
        for i in range(len(args)-1):
            self.search_params.append('|')
        for item in args:
            self.search_params.append(item)
        return self

    # method to select fields that should be returned
    def filter(self, fields):
        self.modifiers['fields'] = fields
        return self

    # method to limit results that should be returned
    def limit(self, limit):
        self.modifiers['limit'] = limit
        return self

    # method to set skipped results
    def offset(self, offset):
        self.modifiers['offset'] = offset
        return self

    # method to sort results by field
    def sort(self, field, order='asc'):
        self.modifiers['order'] = '{} {}'.format(field, order)
        return self
