class QueryBuilder(object):
    select_base = 'SELECT {columns} FROM {table}{where}'
    insert_base = 'INSERT INTO {table}({columns}) VALUES ({question_marks})'
    create_table_base = 'CREATE TABLE {if_not_exist}{table} ({columns})'
    update_base = 'UPDATE {table} SET {columns} {where}'
    delete_base = 'DELETE FROM {table} {where}'

    def __init__(self, table_name):
        self.table = table_name

    def create_table(self, columns_dict, if_not_exist=False, autoincrement_fields=('id',)):
        if_not_exist = 'IF NOT EXISTS ' if if_not_exist else ''
        columns = ', '.join([f'{x} {columns_dict[x].upper()}' for x in columns_dict])
        if not (autoincrement_fields is None):
            for field in autoincrement_fields:
                old = f'{field} INTEGER'
                new = f'{field} INTEGER PRIMARY KEY AUTOINCREMENT'
                columns = columns.replace(old, new)
        query = self.create_table_base.format(table=self.table, columns=columns, if_not_exist=if_not_exist)
        return query

    def select(self, *columns, where=''):
        columns = ', '.join(columns) if columns else '*'
        where = f' {where}' if where else ''
        query = self.select_base.format(table=self.table, columns=columns, where=where)
        return query

    def insert(self, columns):
        number_of_values = len(columns)
        columns = ', '.join(columns)
        if not self.table:
            raise InternalError('Nothing where to make query')
        if number_of_values <= 0:
            raise InternalError('Number of values is incorrect')
        question_marks = ', '.join(['?' for _ in range(number_of_values)])
        query = self.insert_base.format(table=self.table, question_marks=question_marks, columns=columns)
        return query

    def update(self, where, **values):
        columns = ', '.join([f'{x} = {values[x]}' for x in values])
        query = update_base.format(where=where, table=self.table, columns=columns)
        return query

    def delete(self, where):
        query = self.delete_base.format(where=where, table=self.table)
        return query

    @staticmethod
    def where_equals(**equals):
        decorators = {
            "<class 'str'>": lambda x: f'"{x}"',
            "<class 'int'>": lambda x: f'{x}',
        }
        decor_vars = lambda x: decorators[str(type(x))](x)
        equals = ' AND '.join([f'{x} = {decor_vars(equals[x])}' for x in equals])
        result = f'WHERE {equals}'
        return result
