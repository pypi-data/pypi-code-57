from tgusers.database.database import DataBase


class Table:
    def __init__(self, table_name, db: DataBase):
        self.table_name = table_name
        self.db = db

    def select_all_table_data(self):
        sql = """
                    SELECT *
                    FROM "%s";
        """ % (self.table_name, )
        return self.db.request(sql)
