class Parameter:
    def __init__(self, name, required, description, type_, template, arbitrary=False):
        self.name = name
        self.required = required
        self.description = description
        self.type_ = type_

        self.template = template
        self.arbitrary = arbitrary

    @classmethod
    def from_param_dict(cls, param):
        return cls(name=param['name'], required=param['required'],
                   description=param['description'], type_=param['type'], template=param['template'],
                   arbitrary=param.get('arbitrary', False))

    def modify_query(self, query, value):
        if 'where' in self.template:
            if self.type_.endswith('[]'):
                if self.arbitrary:
                    clause = self.template['where'].format(*value)
                else:
                    value = tuple(value) if len(value) != 1 else f'({repr(value[0])})'
                    clause = self.template['where'].format(value)
            else:
                clause = self.template['where'].format(value)

            query['where'].append(clause)
        else:
            raise NotImplementedError('Other template types are not implemented.')

        return query

    def __repr__(self):
        required = ' REQUIRED' if self.required else ''
        description = self.description[:50] + ('...' if len(self.description) > 50 else '')

        return f'dataset.Parameter(<{self.type_}>{self.name}{required}; {description})'
