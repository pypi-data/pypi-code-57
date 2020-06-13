# -*- encoding: utf-8 -*-
"""
本模块用于对sql server数据库的简单操作，使用前应先安装好pymssql库
"""
import pymssql
import logging
import re

__all__ = ['Sqldb', ]


# 创建一个数据库对象，该对象与数据库的连接以及游标将保持至该对象被释放
class Sqldb(object):
    def __init__(self, database, user='sa', password='admin1810300215', server='localhost', charset='utf8'):
        """
        :param database: 数据库名
        :type database: str
        :param user: 数据库用户名
        :type user: str
        :param password: 数据库密码
        :type password: str
        :param server: 数据库服务器
        :type server: str
        :param charset: 数据库使用的编码类型
        :type charset: str
        """
        self.__db_base_info = {
            'database': database,
            'user': user,
            'password': password,
            'server': server,
            'charset': charset
        }
        self.__db = self.__connect()
        logging.info('数据库连接成功！')
        self.__cursor = self.__create_cursor()
        self.tables = self.__get_db_tables()
        self.table_data = self.__set_db_tables()

    # 在对象被释放时执行此方法
    def __del__(self):
        logging.info('正在与数据库断开连接...')
        try:
            self.__db.close()
            self.__cursor.close()
        except pymssql.Error:
            logging.error('An error orurred while disconnecting from the database.')
            raise pymssql.Error('与数据库断开连接时发生了错误')
        else:
            logging.info('与数据库的连接已断开')

    def delete_table(self, name):
        """
        :param name: 要删除的表名
        :type name: str
        :return:
        """
        if name in self.tables:
            self.exec(
                f'''
                        drop table {name}
                        '''
            )
            del self.table_data[name]
            for index in range(0, len(self.tables)):
                if self.tables[index] == name:
                    del self.tables[index]
                    break
        else:
            logging.error('表信息不存在，请输入正确的表名')

    def __get_db_tables(self):
        t_ls = []
        r_ls = self.exec(
            f'''
            select name from {self.__db_base_info['database']}..sysobjects where xtype='u' order by name
            '''
        )
        for item in r_ls:
            t_ls.append(item['name'])
        return t_ls

    # 为数据库中的每一个表创建一个表对象
    def __set_db_tables(self):
        tbs = {}
        for table in self.tables:
            tbs[table.__str__()] = Table(self, table)
        return tbs

    def __connect(self):
        """
        :return: 返回一个数据库连接对象
        """
        logging.info('正在连接数据库...')
        return pymssql.connect(
            database=self.__db_base_info['database'],
            user=self.__db_base_info['user'],
            password=self.__db_base_info['password'],
            server=self.__db_base_info['server'],
            charset=self.__db_base_info['charset'],
            autocommit=True,
            as_dict=True,
            timeout=30,
            login_timeout=60
        )

    def exec(self, query):
        """
        :param query: 需要执行的t-sql语句，一般为数据库查询表语句；若要查询表数据，建议使用Table类中的exec，
                    因为从逻辑上看，数据库不应直接对表进行操作
        :type query: str
        :return: 若有查询结果，则返回该查询结果，否则返回None
        """
        if query:
            self.__cursor.execute(query)
            try:
                ls = self.__cursor.fetchall()
            # 无结果的查询
            except pymssql.OperationalError:
                return None
            # 有结果的查询
            else:
                return ls
        else:
            raise pymssql.ProgrammingError('执行语句为空或存在语法异常')

    def __create_cursor(self):
        cur = None
        try:
            cur = self.__db.cursor()
        # 如果数据库连接中断，重新连接
        except pymssql.OperationalError:
            self.__db = self.__connect()
            cur = self.__db.cursor()
        except Exception as e:
            raise e
        finally:
            return cur


class Table(object):
    def __init__(self, db, name):
        """
        :param db: 数据库对象
        :type db: Sqldb
        :param name: 表名
        :type name str
        """
        self.__db = db
        self.name = name
        self.table_info = self.__parse_table()
        pks = []
        for pk in self.exec(
                f'''
                select b.column_name
                from information_schema.table_constraints a
                inner join information_schema.constraint_column_usage b
                on a.constraint_name = b.constraint_name
                where a.constraint_type = 'primary key' and a.table_name = '{self.name}'
                '''
        ):
            pks.append(pk['column_name'])
        self.pk = pks

    def clear_table_data(self):
        logging.warning(f'正在试图清空数据表-{self.name}')
        self.exec(
            f'''
                truncate table {self.name}
                '''
        )
        logging.info('数据表已清空')

    def delete_item(self, **kv):
        """
        删除符合筛选要求的数据项
        :param kv: 需要删除的数据项的筛选条件
        :type kv: dict
        :return:
        """
        if not set(kv.keys()).issubset(self.table_info['rough_info']):
            logging.error('输入的键值有误')
            exit(0)
        condi_ls = []
        type_ls = self.__get_data_type(kv)
        for item in list(kv.keys()):
            if type_ls[item]['type'] == 'str':
                condi_ls.append(f"{item} = '{kv[item]}'")
            else:
                condi_ls.append(f"{item} = {kv[item]}")
        condition = ' and '.join(condi_ls)
        query = f"delete {self.name} where {condition}"
        self.exec(query)

    @staticmethod
    def __get_data_type(data_dict):
        """
        :param data_dict: 一个值的列表
        :type data_dict: dict
        :return: 返回该值列表所对应的符合需求的数据类型的字典，与源数据对应
        """
        type_ls = {}
        for data in list(data_dict.keys()):
            string = f'{type(data_dict[data])}'
            tmp = {
                'val': data_dict[data],
                'type': re.search(pattern=r"(?<=<class ').*(?='>)", string=string).group(0)
            }
            type_ls[data] = tmp
        return type_ls

    def __check_constraint(self, kv):
        """
        :param kv: 要插入的数据项信息，包括数据类型
        :type kv: dict
        :return: 若要插入的数据项与表格中的约束发生冲突，返回True，否则返回False
        """
        # 当前表中不存在任何约束
        if len(self.pk) == 0:
            return False
        type_dict = self.__get_data_type(kv)
        query = f'''select * from {self.name}'''
        # 主键为单键
        if len(self.pk) == 1:
            if type_dict[self.pk[0]]['type'] == 'str':
                query += f" where {self.pk[0]} =  '{type_dict[self.pk[0]]['val']}'"
            else:
                query += f" where {self.pk[0]} = {type_dict[self.pk[0]]['val']}"
        # 主键为组合键
        # 此时，若输入的数据组合与数据库中存在的一致，则发生了冲突
        elif len(self.pk) > 1:
            pk_ls = []
            for pk in self.pk:
                if type_dict[pk]['type'] == 'str':
                    tmp = f"{pk} = '{kv[pk]}'"
                else:
                    tmp = f"{pk} = {kv[pk]}"
                pk_ls.append(tmp)
            query += f" where {' and '.join(pk_ls)}"
        # 产生了一个结果，表明数据库中已存有相同数据
        if self.exec(query):
            return True
        else:
            return False

    def add_item(self, **kv):
        """
        :param kv: 要插入到表中的数据
        :type kv: dict
            It must be surrounded by double quotation marks that item's type is string.
            Besides, the items that are inserted must conform to table whole constraint.
            e.g
            >>>from aux_db import db
            >>>db = Sqldb('movie')
            >>>db.table_data['movie'].add_item(name="'Julia'", birthday="'2000-04-03'", gender="'man'", age=20)
        """
        if self.__check_constraint(kv):
            logging.error('表中已存在相同数据，将跳过本次操作')
            exit(0)
        # 获取表属性
        rough = self.table_info['rough_info']
        detail = self.table_info['detail_info']
        # 检验数据项的正确性
        keys = list(kv.keys())
        if set(keys).issubset(set(rough)):
            di = []
            for key in keys:
                each_col = key.__str__()
                for prop in detail:
                    if prop['column_name'] == each_col:
                        di.append(prop)
            # 生成query语句
            target_col = ', '.join(keys)
            val_dict = {}
            # 遍历一遍刚才创建的插入信息，每一个item是一个dict
            for item in di:
                # 只有日期和字符串需要在值的两边加''
                # 创建筛选项
                string = ['char', 'varchar', 'nchar', 'nvarchar', 'ntext', 'text']
                date = ['datetime', 'smalldatetime', 'date', 'time', 'datetime2', 'datetimeoffset']
                # 取并集检测
                if item['type'] in string + date:
                    tmp = {
                        'val': "'" + kv[item['column_name']].__str__() + "'"
                    }
                else:
                    tmp = {
                        'val': kv[item['column_name']]
                    }
                val_dict[item['column_name']] = tmp
            val_col_ls = []
            for index in range(0, len(keys)):
                val_col_ls.append(val_dict[keys[index]]['val'].__str__())
            target_val = ', '.join(val_col_ls)
            query = f"insert into {self.name}({target_col}) values({target_val})"
            try:
                self.exec(query)
            except pymssql.OperationalError as e:
                print(e)
                logging.error('所给数据中存在错误，数据插入失败')
            else:
                logging.info('数据插入成功')

    @property
    def data(self):
        """
        :return: 返回当前表的数据
        """
        return self.exec(
            f'''
                select * from {self.name}
                '''
        )

    def set_data(self, kv, **kv_condi):
        """
        :param kv: 需要修改的键值，注意：若是字符串或日期类型的数据，数据格式需设置为"'{数据内容}'"，除此之外，对于日期类型的数据，应使用datetime模块，
        并且严格按照'%Y-%m-%d %H:%M:%S'的时间戳
        :type kv: dict
        :param kv_condi: 关系的关键字，能唯一确定一条数据。注意：若是字符串或时间类型的数据，数据格式需设置为"'{数据内容}'"，除此之外，对于日期类型的数据，
        应使用datetime模块，并且严格按照'%Y-%m-%d %H:%M:%S'的时间戳
            e.g
            >>>from sql import Sqldb
            >>>import datetime
            >>>db = Sqldb('movie')
            >>>db.table_data['movie'].set_data({'name': "'T'", 'actors': "'xx/xx'", 'public_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, hash="'sadw'")
        """
        # 排错
        for k in kv.keys():
            if k not in self.table_info['rough_info']:
                raise pymssql.OperationalError('传入的数据存在错误')
        for k_condi in kv_condi.keys():
            if k_condi not in self.table_info['rough_info']:
                raise pymssql.OperationalError('传入的数据存在错误')
        # 拼接query
        query = f"update {self.name} set "
        query_component = []
        condi_component = []
        for k, v in kv.items():
            query_component.append(f'{k} = {v}')
        query += ', '.join(query_component) + ' where '
        for k_condi, v_condi in kv_condi.items():
            condi_component.append(f'{k_condi} = {v_condi}')
        query += ' and '.join(condi_component)
        try:
            self.exec(query)
        except pymssql.ProgrammingError:
            logging.error('在修改过程中发生错误')
            import traceback
            traceback.print_exc()
            exit(1)
        else:
            logging.info('修改成功')

    @property
    def data_num(self):
        """
        :return: 当前表的数据量
        :rtype: int
        """
        return len(self.data)

    def __parse_table(self):
        """
        :return: 当前表的信息
        :rtype: dict
        """
        # 获取表中所有的列
        columns = self.exec(
            f'''
                select a.name 表名,b.name 字段名,c.name 字段类型,c.length 字段长度 from sysobjects a,syscolumns b,systypes c where a.id=b.id
                and a.name='{self.name}' and a.xtype='U'
                and b.xtype=c.xtype
                '''
        )
        # 删除重复数据：sysname
        cols = []
        for col in columns:
            if col['字段类型'] != 'sysname':
                cols.append(col)
        table_info = {}
        rough = []
        detail = []
        for column in cols:
            info = {
                'column_name': column['字段名'],
                'type': column['字段类型'],
                'length': column['字段长度']
            }
            rough.append(info['column_name'])
            detail.append(info)
        table_info['detail_info'] = detail
        table_info['rough_info'] = rough
        table_info['column_num'] = len(rough)
        return table_info

    def exec(self, query):
        """
        :param query: 需要执行的t-sql语句
        :type query: str
        :return: 若有查询结果，则返回该查询结果，否则返回None
        """
        if query:
            return self.__db.exec(query)
        else:
            raise pymssql.ProgrammingError('执行语句为空或存在语法异常')
