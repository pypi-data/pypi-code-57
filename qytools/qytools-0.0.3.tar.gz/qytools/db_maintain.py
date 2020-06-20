import sqlite3
import pandas as pd
from qytools.db_read import DBReader
from qytools.tools import check_time


class Dbtools:
	def __init__(self, *args):
		self.col_type = [
			'FLOAT', 'INT', 'INTEGER', 'NULL', 'NUMERIC', 'TEXT', 'REAL', 'NONE', 'TINYINT', 'SMALLINT', 'MEDIUMINT',
			'BIGINT', 'UNSIGNED BIG INT', 'INT2', 'INT8', 'CLOB', 'BLOB', 'DOUBLE', 'DOUBLE PRECISION', 'BOOLEAN', 'DATE',
			'DATETIME']
		self.index_col = ['code,datetime', 'datetime', 'date', 'code,date', 'datetime,code', 'date,code']

	def check_col_type(self, cols):
		exception_cols = []
		for col_type in cols.values():
			if col_type.upper() not in self.col_type:
				exception_cols.append(col_type)
		if len(exception_cols) > 0:
			raise ValueError('以下新增列的存储格式不在规范表达列表中：{}'.format(exception_cols))

	@staticmethod
	def sql_time(time, minmode=False, point=0):
		time = check_time(time=time)
		if minmode:
			if point == 0:
				str_time = '"' + time + ' 00:00:00' + '"'
			elif point == 1:
				str_time = '"' + time + ' 23:00:00' + '"'
			else:
				raise ValueError('point必须为0或1')
		else:
			str_time = '"' + time + '"'
		return str_time

	@staticmethod
	def check_index_elementals(df_check, index_col):
		assert index_col in ['code', 'code,datetime', 'datetime', 'date', 'code,date'], \
			"index_col超出可选范围: 'code,datetime', 'datetime', 'date', 'code,date'"
		if len(df_check) == 0:
			raise Exception('df_data不能为空')
		
		if index_col == 'code,date':
			_ = check_time(time=df_check['date'].iloc[0])
			if str(df_check['code'].iloc[0]).isdigit() and isinstance(df_check['date'].iloc[0], str):
				pass
			else:
				raise ValueError('code必须为(int, str), date必须为指定格式str如2018-08-08')
		elif index_col == 'code,datetime':
			_ = check_time(time=df_check['datetime'].iloc[0])
			if str(df_check['code'].iloc[0]).isdigit() and isinstance(df_check['datetime'].iloc[0], str):
				pass
			else:
				raise ValueError('code必须为(int, str), datetime必须为指定格式str如2018-08-08 00:00:00')
		elif index_col == 'datetime':
			_ = check_time(time=df_check['datetime'].iloc[0])
			if isinstance(df_check['datetime'].iloc[0], str):
				pass
			else:
				raise ValueError('code必须为(int, str), datetime必须为指定格式str如2018-08-08 00:00:00')
		elif index_col == 'date':
			_ = check_time(time=df_check['date'].iloc[0])
			if isinstance(df_check['date'].iloc[0], str):
				pass
			else:
				raise ValueError('date必须为指定格式str如2018-08-08')
		elif index_col == 'code':
			if str(df_check['code'].iloc[0]).isdigit():
				pass
			else:
				raise ValueError('code必须为(int, str)')
		else:
			raise Exception('index_col未指定')
		
	@staticmethod
	def check_df_cols(newcols, dfcols):
		if newcols is not None:
			check_df_cols = [x for x in newcols.keys() if x not in dfcols]
			if len(check_df_cols) > 0:
				raise ValueError('输入的newcols含有df_data列索引以外的字段{}'.format(check_df_cols))

	@staticmethod
	def update_creat_update_data(dbpath, df_data, index_col):
		df_data.to_sql('update_data', con=sqlite3.connect(dbpath), if_exists='replace', index=False)
		try:
			conn = sqlite3.connect(dbpath)
		except Exception as e:
			raise Exception('数据库{}连接失败'.format(dbpath), e)
		conn_cursor = conn.cursor()
		try:
			conn_cursor.execute('CREATE INDEX inx_update on update_data(' + index_col + ')')
			conn.commit()
		except Exception as e:
			print('update临时表创建索引失败，更新速度会下降，但不影响流程', e)
		conn_cursor.close()
		conn.close()

	@staticmethod
	def drop_update_data(dbpath):
		conn = sqlite3.connect(dbpath)
		conn_cursor = conn.cursor()
		try:
			conn_cursor.execute('DROP TABLE update_data')
			conn.commit()
		except:
			print(
				'删除{}库中update_data失败, 请手动删除，(删除与否不影响程序运行，仅影响库所占内存，update为多余表)'.format(dbpath))
		conn_cursor.close()
		conn.close()

	@staticmethod
	def update_set_col(dbpath, tablename, newcols):
		if len(newcols) == 0:
			return
		conn = sqlite3.connect(dbpath, isolation_level='')
		conn_cursor = conn.cursor()
		conn_cursor.execute("BEGIN TRANSACTION")  # 事务开启
		try:
			for col in newcols.keys():
				conn_cursor.execute('ALTER TABLE ' + tablename + ' ADD COLUMN ' + col + ' ' + newcols[col])
			conn.commit()  # 智能提交模式
		except Exception as e:
			raise Exception('方法update_set_col执行数据库增列失败，请联系管理员调试', e)

		conn_cursor.close()
		conn.close()

	@staticmethod
	def update_str_main_where(index_col, df_split):
		assert index_col in ['code', 'code,datetime', 'datetime', 'date', 'code,date'], \
			"index_col超出可选范围: 'code,datetime', 'datetime', 'date', 'code,date'"
		str_where = ''
		if index_col == 'code,date':
			mindate = df_split['date'].min()
			maxdate = df_split['date'].max()
			codepool = list(df_split['code'].apply(lambda x: str(x)).unique())
			codepool = '(' + ','.join(codepool) + ')'
			str_code = ' AND code IN ' + codepool
			str_where = ' WHERE date >= ' + '"' + mindate + '" AND date <= ' + '"' + maxdate + '"' + str_code
		elif index_col == 'code,datetime':
			mindate = df_split['datetime'].min()
			maxdate = df_split['datetime'].max()
			codepool = list(df_split['code'].apply(lambda x: str(x)).unique())
			codepool = '(' + ','.join(codepool) + ')'
			str_code = ' AND code IN ' + codepool
			str_where = ' WHERE datetime >= ' + '"' + mindate + '" AND datetime <= ' + '"' + maxdate + '"' + str_code
		elif index_col == 'datetime':
			mindate = df_split['datetime'].min()
			maxdate = df_split['datetime'].max()
			str_where = ' WHERE datetime >= ' + '"' + mindate + '" AND datetime <= ' + '"' + maxdate + '"'
		elif index_col == 'date':
			mindate = df_split['date'].min()
			maxdate = df_split['date'].max()
			str_where = ' WHERE date >= ' + '"' + mindate + '" AND date <= ' + '"' + maxdate + '"'
		else:
			pass
		return str_where

	@staticmethod
	def update_str_where(tablename, index_col):
		assert index_col in ['code', 'code,datetime', 'datetime', 'date', 'code,date'], \
			"index_col超出可选范围: 'code,datetime', 'datetime', 'date', 'code,date'"
		str_where = ''
		if index_col == 'code':
			str_where = ' FROM update_data WHERE update_data.code = ' + tablename + '.code'
		elif index_col == 'code,date':
			str_where = ' FROM update_data WHERE update_data.code = ' + tablename\
				+ '.code AND update_data.date = ' + tablename + '.date'
		elif index_col == 'code,datetime':
			str_where = ' FROM update_data WHERE update_data.code = ' + tablename\
				+ '.code AND update_data.datetime = ' + tablename + '.datetime'
		elif index_col == 'datetime':
			str_where = ' FROM update_data WHERE update_data.datetime = ' + tablename + '.datetime'
		elif index_col == 'date':
			str_where = ' FROM update_data WHERE update_data.date = ' + tablename + '.date'
		else:
			pass
		return str_where

	@staticmethod
	def split_data(dbpath, tablename, index_col, df_split, insert=False, insertmode='new'):
		assert isinstance(insert, bool), 'insert为bool'
		assert insertmode in ['new', 'old', 'in'], 'insertmode为new或old'
		if insertmode == 'in':
			return df_split
		if 'code' in index_col.split(','):
			str_code = ' WHERE code in (1,16,905)'
		else:
			str_code = ''
		if 'date' in index_col.split(','):
			maxdate = pd.read_sql(
				'SELECT MAX(' + 'date' + ') FROM ' + tablename + str_code, con=sqlite3.connect(dbpath)).iloc[0, 0]
			mindate = pd.read_sql(
				'SELECT MIN(' + 'date' + ') FROM ' + tablename + str_code, con=sqlite3.connect(dbpath)).iloc[0, 0]
			if insert:
				if insertmode == 'new':
					if maxdate is not None:
						df_split = df_split[df_split['date'] > maxdate]
				else:
					if mindate is not None:
						df_split = df_split[df_split['date'] < mindate]
			else:
				df_split = df_split[(df_split['date'] >= mindate) & (df_split['date'] <= maxdate)]
			return df_split
		elif 'datetime' in index_col.split(','):
			maxdate = pd.read_sql(
					'SELECT MAX(' + 'datetime' + ') FROM ' + tablename + str_code,
					con=sqlite3.connect(dbpath)).iloc[0, 0]
			mindate = pd.read_sql(
					'SELECT MIN(' + 'datetime' + ') FROM ' + tablename + str_code,
					con=sqlite3.connect(dbpath)).iloc[0, 0]
			if insert:
				if insertmode == 'new':
					if maxdate is not None:
						df_split = df_split[df_split['datetime'] > maxdate]
				else:
					if mindate is not None:
						df_split = df_split[df_split['datetime'] < mindate]
			else:
				df_split = df_split[(df_split['datetime'] >= mindate) & (df_split['datetime'] <= maxdate)]
		else:
			pass
		return df_split

	@staticmethod
	def find_max_min_date(dbpath, tablename, index_col, on='max'):
		assert on in ['max', 'min'], 'on为max或者min'
		date = None
		if 'code' in index_col.split(','):
			str_code = ' WHERE code in (1,16,905)'
		else:
			str_code = ''
		if 'date' in index_col.split(','):
			if on == 'max':
				date = pd.read_sql(
					'SELECT MAX(' + 'date' + ') FROM ' + tablename + str_code, con=sqlite3.connect(dbpath)).iloc[0, 0]
			if on == 'min':
				date = pd.read_sql(
					'SELECT MIN(' + 'date' + ') FROM ' + tablename + str_code, con=sqlite3.connect(dbpath)).iloc[0, 0]
		elif 'datetime' in index_col.split(','):
			if on == 'max':
				date = pd.read_sql(
					'SELECT MAX(' + 'datetime' + ') FROM ' + tablename + str_code, con=sqlite3.connect(dbpath)).iloc[0, 0]
			if on == 'min':
				date = pd.read_sql(
					'SELECT MIN(' + 'datetime' + ') FROM ' + tablename + str_code, con=sqlite3.connect(dbpath)).iloc[0, 0]
		else:
			pass
		return date

	@staticmethod
	def check_update_col(dbpath, tablename, dfcols, updatecols=None):
		assert isinstance(updatecols, list) or updatecols is None, 'updatecols必须是list或None'
		try:
			cols = pd.read_sql('PRAGMA table_info([' + tablename + '])', con=sqlite3.connect(dbpath))['name'].to_list()
		except Exception as e:
			raise Exception('数据库查询表{}字段时发生异常'.format(tablename), e)
		if updatecols is not None:
			errorcols = [x for x in updatecols if x not in dfcols or x not in cols or x in ['date', 'datetime', 'code']]
			if len(errorcols) > 0:
				raise Exception('更新列中包含表{0}没有的列{1}或包含了code,date,datetime'.format(tablename, errorcols))
			true_updatecols = updatecols
		else:
			true_updatecols = [x for x in dfcols if x in cols and x not in ['date', 'datetime', 'code']]
		return true_updatecols

	@staticmethod
	def check_exist_col(dbpath, tablename, newcols, dfcols, autoadd=False):
		if newcols is None and not autoadd:
			return dict(), []
		try:
			cols = pd.read_sql('PRAGMA table_info([' + tablename + '])', con=sqlite3.connect(dbpath))['name'].to_list()
		except Exception as e:
			raise Exception('数据库查询表{}字段时发生异常'.format(tablename), e)
		true_newcols = dict()
		if newcols is not None and autoadd:
			autocols = {x: '' for x in dfcols if x not in list(newcols.keys()) + cols}
			for col in newcols.keys():
				if col not in cols:
					true_newcols[col] = newcols[col]
			for col in autocols.keys():
				true_newcols[col] = ''
			return true_newcols, []
		elif newcols is None and autoadd:
			autocols = {x: '' for x in dfcols if x not in cols}
			for col in autocols.keys():
				true_newcols[col] = ''
			return true_newcols, []
		elif newcols is not None and not autoadd:
			autocols = [x for x in dfcols if x not in list(newcols.keys()) + cols]
			for col in newcols.keys():
				if col not in cols:
					true_newcols[col] = newcols[col]
			return true_newcols, autocols

	def update_data(self, dbpath, tablename, index_col, df_data, newcols=None, autoadd=False, updatecols=None):
		"""
		:param dbpath:数据库文件目录，str，如:D:/test/dbpath_tushare_data.sqlite3
		:param tablename: 数据库内所需要使用的某一个表的表名，str，如ts_day_data
		:param newcols: 新增列，支持dict，如{'pe': 'float', 'pb': 'float', 'eps': 'float'},默认False
		:param index_col: 所需要更改的数据库的唯一索引组合，str,如股票日级别：'code,date',分钟级别'code,datetime'，少数无code
		表如市场表为'date'或'datetime',不接受不含有时间的索引，此类表为截面表，请使用replace_data方法
		:param df_data: 用于添加进数据库的dataframe数据，字段必须含有index_col中的索引
		:param autoadd: 自动添dataframe加多余列，采取默认的sqlite格式，默认False,为True时若newcols不为None则剩余列执行autoadd
		:param updatecols: 指定更新的某些数据库已有列，接受list，默认None为更新传入dataframe中除索引外所有在数据库表里的列，
		否则更新传入的list中列
		"""

		assert len(df_data.columns.unique()) == len(df_data.columns), 'df_data不能含有重复列'
		assert isinstance(tablename, str), 'tablename必须为str'
		assert isinstance(dbpath, str), 'dbpath必须为str'
		assert isinstance(df_data, pd.DataFrame), 'df_data必须为dataframe'
		assert index_col in self.index_col,\
			"index_col超出可选范围: 'code,datetime', 'datetime', 'date', 'code,date'"
		assert isinstance(newcols, dict) or newcols is None, 'newcol为dict或None'
		self.check_df_cols(newcols=newcols, dfcols=df_data.columns)
		self.check_index_elementals(df_check=df_data.iloc[: -1, :], index_col=index_col)
		df_split = self.split_data(dbpath=dbpath, tablename=tablename, index_col=index_col, df_split=df_data)
		if len(df_split) == 0:
			print('数据库已经是最新表，无需更新，返回')
			return 0
		true_newcols, dropcols = self.check_exist_col(
			dbpath=dbpath, tablename=tablename, newcols=newcols, autoadd=autoadd, dfcols=df_split.to_dict())
		if len(dropcols) > 0:
			df_split = df_split.drop(dropcols, axis=1).copy(deep=True)
		true_updatecols = self.check_update_col(
			dbpath=dbpath, tablename=tablename, dfcols=df_split.to_dict(), updatecols=updatecols)
		self.update_creat_update_data(dbpath=dbpath, df_data=df_split, index_col=index_col)
		self.update_set_col(dbpath=dbpath, tablename=tablename, newcols=true_newcols)  # 添加更新库中表没有列名
		conn = sqlite3.connect(dbpath)
		conn_cursor = conn.cursor()
		conn_cursor.execute("BEGIN TRANSACTION")  # 事务开启
		str_where = self.update_str_where(tablename=tablename, index_col=index_col)
		str_where_main = self.update_str_main_where(index_col=index_col, df_split=df_split)
		true_updatecol = list(true_newcols.keys()) + true_updatecols
		true_updatecol = ','.join(true_updatecol)
		# for true_newcol in true_newcols:
		# str_sql =\
		# 	'UPDATE ' + tablename + ' SET ' + true_newcol + ' = (SELECT ' + true_newcol + str_where + ')' \
		# 	+ str_where_main
		# conn_cursor.execute(str_sql)
		# for true_updatecol in true_updatecols:
		str_sql =\
			'UPDATE ' + tablename + ' SET (' + true_updatecol + ') = (SELECT ' + true_updatecol + str_where + ')' \
			+ str_where_main
		conn_cursor.execute(str_sql)
		# conn_cursor.execute('commit')
		conn.commit()
		conn_cursor.close()
		conn.close()
		self.drop_update_data(dbpath=dbpath)
		print(tablename + '表update成功')

	def insert_data(self, dbpath, tablename, index_col, df_data, insertmode='new', newcols=None, autoadd=False):
		"""
		:param dbpath:数据库文件目录，str，如:D:/test/dbpath_tushare_data.sqlite3
		:param tablename: 数据库内所需要使用的某一个表的表名，str，如ts_day_data
		:param index_col: 所需要更改的数据库的唯一索引组合，str,如股票日级别：'code,date',分钟级别'code,datetime'，少数无code
		表如市场表为'date'或'datetime',不接受不含有时间的索引，此类表为截面表，请使用replace_data方法
		:param df_data: 用于添加进数据库的dataframe数据，字段必须含有index_col中的索引
		:param insertmode: insert数据的方向，补全比数据库最早数据还早的旧数据用'old',补足库中最新日期之后的新数据用'new'，插入中
		间数据使用'in'，默认new
		:param newcols: 新增列，支持dict，如{'pe': 'float', 'pb': 'float', 'eps': 'float'},默认False
		:param autoadd: 自动添dataframe加多余列，采取默认的sqlite格式，默认False,为True时若newcols不为None则剩余列执行autoadd
		"""

		assert len(df_data.columns.unique()) == len(df_data.columns), 'df_data不能含有重复列'
		assert isinstance(tablename, str), 'tablename必须为str'
		assert isinstance(dbpath, str), 'dbpath必须为str'
		assert isinstance(df_data, pd.DataFrame), 'df_data必须为dataframe'
		assert insertmode in ['new', 'old', 'in'], 'insertmode为new,old,in之一'
		assert index_col in self.index_col, "index_col超出可选范围: 'code,datetime', 'datetime', 'date', 'code,date'"
		assert isinstance(newcols, dict) or newcols is None, 'newcol为dict或None'
		assert isinstance(autoadd, bool), 'autoadd为bool'
		self.check_df_cols(newcols=newcols, dfcols=df_data.columns)
		self.check_index_elementals(df_check=df_data.iloc[: -1, :], index_col=index_col)
		df_split = self.split_data(
			dbpath=dbpath, tablename=tablename, index_col=index_col, df_split=df_data, insert=True, insertmode=insertmode)
		if len(df_split) == 0:
			print('数据库已经是最新表，无需更新，返回')
			return 0
		true_newcols, dropcols = self.check_exist_col(
			dbpath=dbpath, tablename=tablename, newcols=newcols, autoadd=autoadd, dfcols=df_split.to_dict())
		if len(dropcols) > 0:
			df_split = df_split.drop(dropcols, axis=1).copy(deep=True)
		self.update_set_col(dbpath=dbpath, tablename=tablename, newcols=true_newcols)
		# 	raise ValueError('表{0}没有df中的字段：{1}'.format(tablename, list(true_newcols.keys())))
		try:
			connect = sqlite3.connect(dbpath)
		except Exception as e:
			raise Exception('数据库{}连接失败'.format(dbpath), e)
		try:
			df_split.to_sql(tablename, con=connect, if_exists='append', index=False)
			connect.close()
		except Exception as e:
			raise Exception('数据库insert环节出错：', e)
		print(tablename + '表insert成功')

	def rebuild_data(self, dbpath, tablename, index_col, df_data, newcols=None, autoadd=False):
		"""
		:param dbpath:数据库文件目录，str，如:D:/test/dbpath_tushare_data.sqlite3
		:param tablename: 数据库内所需要使用的某一个表的表名，str，如ts_day_data
		:param newcols: 新增列，支持dict，如{'pe': 'float', 'pb': 'float', 'eps': 'float'},默认False
		:param index_col: 所需要更改的数据库的唯一索引组合，str,如股票日级别：'code,date',分钟级别'code,datetime'，少数无code
		表如市场表为'date'或'datetime',不接受不含有时间的索引，此类表为截面表，请使用replace_data方法
		:param autoadd: 自动添dataframe加多余列，采取默认的sqlite格式，默认False,为True时若newcols不为None则剩余列执行autoadd
		:param df_data: 用于添加进数据库的dataframe数据，字段必须含有index_col中的索引
		"""

		assert len(df_data.columns.unique()) == len(df_data.columns), 'df_data不能含有重复列'
		assert isinstance(tablename, str), 'tablename必须为str'
		assert isinstance(dbpath, str), 'dbpath必须为str'
		assert isinstance(df_data, pd.DataFrame), 'df_data必须为dataframe'
		assert index_col in self.index_col, \
			"index_col超出可选范围: 'code,datetime', 'datetime', 'date', 'code,date'"
		assert isinstance(newcols, dict) or newcols is None, 'newcol为dict或None'
		assert isinstance(autoadd, bool), 'autoadd为bool'
		self.check_df_cols(newcols=newcols, dfcols=df_data.columns)
		self.check_index_elementals(df_check=df_data.iloc[: -1, :], index_col=index_col)
		if 'date' in index_col.split(','):
			str_start = self.sql_time(time=df_data['date'].min())
			str_end = self.sql_time(time=df_data['date'].max())
			str_sql = \
				'DELETE FROM ' + tablename + ' WHERE date >= ' + str_start + ' AND date <= ' + str_end
		elif 'datetime' in index_col.split(','):
			str_start = self.sql_time(time=df_data['date'].min(), minmode=True, point=0)
			str_end = self.sql_time(time=df_data['date'].max(), minmode=True, point=1)
			str_sql = \
				'DELETE FROM ' + tablename + ' WHERE datetime >= ' + str_start + ' AND datetime <= ' + str_end
		else:
			raise Exception('该接口不重构不含时间的截面数据表，请使用navicat')
		# true_newcols, dropcols = self.check_exist_col(
		# 	dbpath=dbpath, tablename=tablename, newcols=newcols, autoadd=autoadd, dfcols=df_data.iloc[: -1, :].to_dict())
		# df_data.drop(dropcols, axis=1, inplace=True)
		# self.update_set_col(dbpath=dbpath, tablename=tablename, newcols=true_newcols)
		try:
			conn = sqlite3.connect(dbpath)
		except Exception as e:
			raise Exception('数据库{}连接失败'.format(dbpath), e)
		conn_cursor = conn.cursor()
		conn_cursor.execute(str_sql)
		conn.commit()
		conn_cursor.close()
		conn.close()
		self.insert_data(
			dbpath=dbpath, tablename=tablename, index_col=index_col, df_data=df_data, newcols=newcols, autoadd=autoadd,
			insertmode='in')
		print(tablename + '表rebuild成功')

	def replace_data(self, dbpath, tablename, index_col, df_data, index_name):
		"""
		:param dbpath:数据库文件目录，str，如:D:/test/dbpath_tushare_data.sqlite3
		:param tablename: 数据库内所需要使用的某一个表的表名，str，如ts_day_data
		:param index_col: 所需要更改的数据库的唯一索引组合，str,如股票日级别：'code,date',分钟级别'code,datetime'
		:param df_data: 用于添加进数据库的dataframe数据，字段必须含有index_col中的索引
		:param index_name: 替换表索引名称，支持str，如'inx_tablename'
		"""

		assert len(df_data.columns.unique()) == len(df_data.columns), 'df_data不能含有重复列'
		assert isinstance(tablename, str), 'tablename必须为str'
		assert isinstance(dbpath, str), 'dbpath必须为str'
		assert isinstance(df_data, pd.DataFrame), 'df_data必须为dataframe'
		assert isinstance(index_name, str), 'index_name必须为str'
		assert index_col in self.index_col, \
			"index_col超出可选范围: 'code,datetime', 'datetime', 'date', 'code,date'"
		self.check_index_elementals(df_check=df_data.iloc[: -1, :], index_col=index_col)
		# assert 'date' not in index_col.split(',') and 'datetime' not in index_col.split(','), \
		# 	"replace仅支持替代截面数据，index_col不能含有时间"
		df_data.to_sql(tablename, con=sqlite3.connect(dbpath), if_exists='replace', index=False)
		conn = sqlite3.connect(dbpath)
		conn_cursor = conn.cursor()
		try:
			conn_cursor.execute('CREATE INDEX ' + index_name + ' on ' + tablename + '(' + index_col + ')')
			conn.commit()
		except Exception as e:
			conn_cursor.close()
			conn.close()
			raise Exception('替换表已生成但索引创建失败，请手动创建索引，可能原因：', e)
		conn_cursor.close()
		conn.close()
		print(tablename + '表replace成功')


if __name__ == '__main__':
	factor = Dbtools('')
	db_read = DBReader('')
	# 准备入库的df
	df = db_read.read_fundamentals(start='2020-01-02', end=20200103, fields='code,date,pb,pe,eps,circ_mv,roe,roa')

	factor.insert_data(df_data=df, dbpath=db_read.dbpath + '\\future_day_data.sqlite3', tablename='future_day_data',
	                   index_col='code,date', autoadd=True)

	a=1
	# # 更新现有数据示例
	# # 只更新基本数据
	# factor.update_data(
	# 	dbpath=db_read.dbpath + '\\fundamentals.sqlite3', tablename='test', df_data=df, index_col='code,date',
	# 	autoadd=False)
	#
	# # 更新并额外增加指定列
	# factor.update_data(
	# 	dbpath=db_read.dbpath + '\\fundamentals.sqlite3', tablename='test',
	# 	newcols={'pe': 'float'}, df_data=df, index_col='code,date', autoadd=False)

	# 更新并额外增加指定列+自动增加其余列
	factor.update_data(
		dbpath=db_read.dbpath + '\\fundamentals.sqlite3', tablename='test',
		newcols={'circ_mv': 'real'}, df_data=df, index_col='code,date', autoadd=True)

	# 增加行示例(insertmode='new'向后补新数据，insertmode='old'向前补旧数据)
	df = db_read.read_fundamentals(start='2020-01-02', end=20200103, fields='code,date,pb,pe,eps,circ_mv,roe,roa')
	factor.insert_data(
			dbpath=db_read.dbpath + '\\fundamentals.sqlite3', tablename='test', df_data=df, index_col='code,date',
			insertmode='new', autoadd=True, newcols={'pb': 'float'})
	#
	# # 重构示例（删了部分数据重入）
	df.drop(['roe', 'roa'], axis=1, inplace=True)
	factor.rebuild_data(
		dbpath=db_read.dbpath + '\\fundamentals.sqlite3', tablename='test', df_data=df, index_col='code,date',
		newcols={'pe': 'float'}, autoadd=False)

	# # 替换示例
	df1 = pd.DataFrame()
	df1['name'] = ['刘', '关', '张', '3']
	df1['code'] = [1, 2, 3, 4]
	df1['date'] = [1, 2, 3, 4]
	factor.replace_data(
		dbpath=db_read.dbpath + '\\fundamentals.sqlite3', tablename='test4', df_data=df1, index_col='code,date',
		index_name='inx_tttt')
	a=1