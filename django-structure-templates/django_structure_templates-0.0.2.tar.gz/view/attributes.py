class ViewAttribute:
    def __init__(self, template, view):
        self.data['template'] = template
        self.data['view'] = view

    def get_field(self, field_name):
        if field_name in self.data.keys():
            return self.data[field_name]
        else:
            raise Exception(
                'Class {} has no field {}'.format(self.__name__, field_name))