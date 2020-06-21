# -*- encoding: utf-8 -*-
# @ModuleName: Db_Reader
# @Function: 	read_tdx_1min_data 获取分钟数据
# 				read_ts_top_inst 获取龙虎榜机构明细
# 				read_ts_top_list 获取龙虎榜股票明细
# 				read_ts_day_data 获取日线综合数据
# 				read_ts_index_daily 获取指数日线数据
# 				read_ts_limit_list 获取每日涨停板数据
# 				read_ts_moneyflow_hsgt 获取沪深港通资金流数据
# 				read_concept_data 获取板块信息
# @Author: Yulin Qiu
# @Time: 2020-3-6 20:08:00


import sqlite3
import pandas as pd
import datetime
import os
import tushare as ts
import numpy as np
from pathlib import Path


class DBReader:
	"""
	_init_参数： configpath:配置文件路径，无须包含文件名 如../filepath/test/

	方法:
	read_tdx_1min_data 获取分钟数据
	read_ts_top_inst 获取龙虎榜机构明细
	read_ts_top_list 获取龙虎榜股票明细
	read_ts_day_data 获取日线综合数据
	read_ts_index_daily 获取指数日线数据
	read_ts_limit_list 获取每日涨停板数据
	read_ts_moneyflow_hsgt 获取沪深港通资金流数据
	read_concept_data 获取板块信息数据
	"""

	def __init__(self, *args):
		self.dbpath = None
		self.file_used = None
		self.tradetime = {
			'1min': [
				'09:31:00', '09:32:00', '09:33:00', '09:34:00', '09:35:00', '09:36:00', '09:37:00', '09:38:00',
				'09:39:00', '09:40:00', '09:41:00', '09:42:00', '09:43:00', '09:44:00', '09:45:00', '09:46:00',
				'09:47:00', '09:48:00', '09:49:00', '09:50:00', '09:51:00', '09:52:00', '09:53:00', '09:54:00',
				'09:55:00', '09:56:00', '09:57:00', '09:58:00', '09:59:00', '10:00:00', '10:01:00', '10:02:00',
				'10:03:00', '10:04:00', '10:05:00', '10:06:00', '10:07:00', '10:08:00', '10:09:00', '10:10:00',
				'10:11:00', '10:12:00', '10:13:00', '10:14:00', '10:15:00', '10:16:00', '10:17:00', '10:18:00',
				'10:19:00', '10:20:00', '10:21:00', '10:22:00', '10:23:00', '10:24:00', '10:25:00', '10:26:00',
				'10:27:00', '10:28:00', '10:29:00', '10:30:00', '10:31:00', '10:32:00', '10:33:00', '10:34:00',
				'10:35:00', '10:36:00', '10:37:00', '10:38:00', '10:39:00', '10:40:00', '10:41:00', '10:42:00',
				'10:43:00', '10:44:00', '10:45:00', '10:46:00', '10:47:00', '10:48:00', '10:49:00', '10:50:00',
				'10:51:00', '10:52:00', '10:53:00', '10:54:00', '10:55:00', '10:56:00', '10:57:00', '10:58:00',
				'10:59:00', '11:00:00', '11:01:00', '11:02:00', '11:03:00', '11:04:00', '11:05:00', '11:06:00',
				'11:07:00', '11:08:00', '11:09:00', '11:10:00', '11:11:00', '11:12:00', '11:13:00', '11:14:00',
				'11:15:00', '11:16:00', '11:17:00', '11:18:00', '11:19:00', '11:20:00', '11:21:00', '11:22:00',
				'11:23:00', '11:24:00', '11:25:00', '11:26:00', '11:27:00', '11:28:00', '11:29:00', '11:30:00',
				'13:01:00', '13:02:00', '13:03:00', '13:04:00', '13:05:00', '13:06:00', '13:07:00', '13:08:00',
				'13:09:00', '13:10:00', '13:11:00', '13:12:00', '13:13:00', '13:14:00', '13:15:00', '13:16:00',
				'13:17:00', '13:18:00', '13:19:00', '13:20:00', '13:21:00', '13:22:00', '13:23:00', '13:24:00',
				'13:25:00', '13:26:00', '13:27:00', '13:28:00', '13:29:00', '13:30:00', '13:31:00', '13:32:00',
				'13:33:00', '13:34:00', '13:35:00', '13:36:00', '13:37:00', '13:38:00', '13:39:00', '13:40:00',
				'13:41:00', '13:42:00', '13:43:00', '13:44:00', '13:45:00', '13:46:00', '13:47:00', '13:48:00',
				'13:49:00', '13:50:00', '13:51:00', '13:52:00', '13:53:00', '13:54:00', '13:55:00', '13:56:00',
				'13:57:00', '13:58:00', '13:59:00', '14:00:00', '14:01:00', '14:02:00', '14:03:00', '14:04:00',
				'14:05:00', '14:06:00', '14:07:00', '14:08:00', '14:09:00', '14:10:00', '14:11:00', '14:12:00',
				'14:13:00', '14:14:00', '14:15:00', '14:16:00', '14:17:00', '14:18:00', '14:19:00', '14:20:00',
				'14:21:00', '14:22:00', '14:23:00', '14:24:00', '14:25:00', '14:26:00', '14:27:00', '14:28:00',
				'14:29:00', '14:30:00', '14:31:00', '14:32:00', '14:33:00', '14:34:00', '14:35:00', '14:36:00',
				'14:37:00', '14:38:00', '14:39:00', '14:40:00', '14:41:00', '14:42:00', '14:43:00', '14:44:00',
				'14:45:00', '14:46:00', '14:47:00', '14:48:00', '14:49:00', '14:50:00', '14:51:00', '14:52:00',
				'14:53:00', '14:54:00', '14:55:00', '14:56:00', '14:57:00', '14:58:00', '14:59:00', '15:00:00'],
			'5min': [
						'09:35:00', '09:40:00', '09:45:00', '09:50:00', '09:55:00', '10:00:00', '10:05:00', '10:10:00',
						'10:15:00', '10:20:00', '10:25:00', '10:30:00', '10:35:00', '10:40:00', '10:45:00', '10:50:00',
						'10:55:00', '11:00:00', '11:05:00', '11:10:00', '11:15:00', '11:20:00', '11:25:00', '11:30:00',
						'13:05:00', '13:10:00', '13:15:00', '13:20:00', '13:25:00', '13:30:00', '13:35:00', '13:40:00',
						'13:45:00', '13:50:00', '13:55:00', '14:00:00', '14:05:00', '14:10:00', '14:15:00', '14:20:00',
						'14:25:00', '14:30:00', '14:35:00', '14:40:00', '14:45:00', '14:50:00', '14:55:00', '15:00:00'],
			'15min': [
				'09:45:00', '10:00:00', '10:15:00', '10:30:00', '10:45:00', '11:00:00', '11:15:00', '11:30:00',
				'13:15:00', '13:30:00', '13:45:00', '14:00:00', '14:15:00', '14:30:00', '14:45:00', '15:00:00'],
			'30min': [
				'10:00:00', '10:30:00', '11:00:00', '11:30:00', '13:30:00', '14:00:00', '14:30:00', '15:00:00', '13:00:00']}
		self.allcode_index = [1, 16, 905, 906, 300, 399001, 399006, 399005, 399300]
		configpath = Path.home().joinpath('.qytools')
		if os.path.exists(str(configpath.joinpath('dbname_config.json'))):
			df_config = pd.read_json(str(configpath.joinpath('dbname_config.json')))
			self.config = df_config
			self.file_used = df_config.loc[0, 'file_used']
			self.dbpath = df_config.loc[0, 'dbpath']
			print('配置文件dbname_config.json读取成功')
		else:
			raise FileNotFoundError('配置文件不存在,请执行DBreader.firsttime_setconfig')
		try:
			# ts.set_token('e6e5601134d8d0f15d2192e65e2551998dc2027c29f776834d5cd8f7')
			# ts.set_token(df_config.loc[0, 'tushare_token'])
			try:
				pro = ts.pro_api()
			except:
				print('tushare连接出错，使用配置文件中token重新尝试连接')
				try:
					# ts.set_token(df_config.loc[0, 'tushare_token'])
					pro = ts.pro_api()
				except Exception:
					raise ConnectionError('使用配置文件中token连接tushare失败，请联系管理员')
			try:
				df_opendate = pro.query('trade_cal', start_date='20150101', end_date='20991231')  # 获取交易日
				df_opendate = df_opendate[df_opendate.is_open == 1]['cal_date']
				# 目前正常交易股票代码和名称
				allcode = pro.stock_basic(exchange='', fields='ts_code,list_date').rename(columns={'ts_code': 'code'})
				allcode['code'] = allcode['code'].apply(lambda x: int(x[0:6]))
				allcode['list_date'] = allcode['list_date'].apply(lambda x: f"{x[0:4]}-{x[4:6]}-{x[6:8]}")
				self.allcode = allcode['code'].to_list()
				self.__list_date = allcode
				delcode = pro.stock_basic(exchange='', list_status='D', fields='symbol,list_date,delist_date')
				delcode['symbol'] = delcode['symbol'].apply(lambda x: x.strip('T'))
				delcode['symbol'] = delcode['symbol'].astype(int)
				delcode = delcode.rename(columns={'symbol': 'code'})
				codename = pro.stock_basic(exchange='', list_status='L', fields='symbol,name')
				codename['symbol'] = codename['symbol'].astype(int)
				codename = codename.rename(columns={'symbol': 'code'})
				# 退市股
				self.__delcode = delcode['code'].to_list()
				# 非ST股票
				df_st = pro.namechange(start_date=20140101, fields='ts_code,name,start_date,end_date,change_reason')
				df_st = df_st[df_st['name'].str.contains('\*|ST')]
				df_st['code'] = df_st['ts_code'].apply(lambda x: int(x[0:6]))
				df_st['start_date'] = df_st['start_date'].apply(lambda x: '{0}-{1}-{2}'.format(x[0:4], x[4:6], x[6:]))
				df_st['end_date'] = df_st['end_date'].apply(
					lambda x: '{0}-{1}-{2}'.format(x[0:4], x[4:6], x[6:]) if x is not None else '2099-09-09')
				df_st.sort_values(by='code', inplace=True)
				df_st.reset_index(inplace=True)
				df_st = df_st[['code', 'start_date', 'end_date']]
				self.__stcode = df_st
				# self.__stcode = codename[codename['name'].str.contains('\*|ST')].code.to_list()
				# 交易日历——日
				self.open_date = df_opendate.apply(lambda x: x[0:4] + '-' + x[4:6] + '-' + x[6:])
			except:
				record = pd.read_json(configpath.joinpath('record_api_message.json'))
				self.__delcode = record['delcode'][0]
				# self.__stcode = record['stcode'][0]
				self.__stcode = pd.DataFrame(record['stcode'][0])
				self.open_date = pd.Series(record['open_date'][0]).apply(lambda x: x[0:4] + '-' + x[4:6] + '-' + x[6:])
			# for item in df_config.columns:
			# 	# self.tdx_1min_data = df_config.loc[0, "code_1min_data_tablename"]
			# 	exec('self.' + item + ' = df_config.loc[0, "' + item + '"]')
			# 配置文件文件夹
			self.configpath = str(configpath)
		except Exception as e:
			raise Exception('_init_过程发生错误 ', e)

	@classmethod
	def firsttime_setconfig(cls, dbpath):
		"""
		:param dbpath: 数据库文件目录

		:return: 生成配置文件dbname_config.json.csv
		"""
		home: Path = Path.home()
		dbpath: Path = Path(dbpath)
		if Path.exists(home.joinpath('.qytools')):
			pass
		else:
			Path.mkdir(home.joinpath('.qytools'))
		configpath: Path = home.joinpath('.qytools')
		filelist = os.listdir(str(dbpath))
		dbfiles = [x for x in filelist if x.rfind('.sqlite3') != -1]
		if len(dbfiles) == 0:
			raise Exception('输入的目录没有sqlite3文件，请检查目录是否输入错误')
		dbfiles = pd.DataFrame({'file': dbfiles}, index=range(0, len(dbfiles)))
		dbfiles['name'] = dbfiles['file'].apply(lambda x: x.replace('.sqlite3', ''))
		dbfiles['path'] = dbfiles['file'].apply(lambda x: str(dbpath.joinpath(x)))
		file_used = dbfiles['name'].to_list()
		df_config = dict()
		df_config['dbpath'] = str(dbpath)
		for inx, name in enumerate(dbfiles['name']):
			exec('df_config["dbpath_' + name + '"] = r"' + str(dbfiles.loc[inx, 'path']) + '"')
		df_config['file_used'] = [file_used]
		df_config = pd.DataFrame(df_config)
		df_config.to_json(home.joinpath('.qytools').joinpath('dbname_config.json'), orient='records', indent=1)
		cls.renew_config(configpath=configpath)
		print('配置文件生成成功')

	@classmethod
	def renew_config(cls, configpath):
		"""
		:warnnig:本地目录没有配置文件dbname_config.json时无需运行该函数

		:param configpath: dbname_config.json文件目录,无需输入文件名（定死名字，确保读得到配置文件）,如D:/test/

		:return: 生成配置文件dbname_config.json.csv
		"""
		configpath = Path(configpath)
		if Path.exists(configpath.joinpath('dbname_config.json')):
			pass
		else:
			raise FileNotFoundError('配置文件configpath保存路径不存在！标准格式示例：D:/dir1/dir2/')
		# 读取文件
		df_config = pd.read_json(configpath.joinpath('dbname_config.json'))
		file_used = df_config.loc[0, 'file_used']

		# 连接数据库
		for dbfile in file_used:
			try:
				connect = sqlite3.connect(df_config.loc[0, 'dbpath_' + dbfile])
				table_all = pd.read_sql('select name FROM' + ' sqlite_master WHERE type="table"', con=connect)
				for table in table_all['name']:
					df_tableinfo = pd.read_sql(
						'PRAGMA table_info([' + table + '])', con=connect)
					df_config.loc[0, 'col_' + table] = ','.join(df_tableinfo['name'].to_list())
				connect.close()
			except Exception as e:
				raise Exception('数据库连接异常，请检查配置文件目录是否正确或重新生成配置文件，如问题无法解决请联系qyl', e)

		# 存储json
		df_config.to_json(configpath.joinpath('dbname_config.json'), orient='records', indent=1)
		print('配置文件更新完毕')

	def __new_clean(self, df, start, newdrop):
		if isinstance(newdrop, int):
			pass
		else:
			raise Exception(f'newdrop必须为int，输入值:{newdrop}')
		if newdrop == 0:
			return df
		start = start.replace('"', '')
		df_list_date = \
			self.__list_date[
				self.__list_date['list_date'] >= self.get_opendate(time=start, shift=newdrop)].copy(deep=True)
		df_list_date['list_date'] = \
			df_list_date['list_date'].apply(lambda x: self.get_opendate(time=x, forward=newdrop))
		df_list_date = df_list_date.groupby('code').agg('max').reset_index()
		df = pd.merge(df, df_list_date, on='code', how='left')
		df['list_date'] = df['list_date'].fillna('0')
		df = df[df['list_date'] <= df['date']]
		df.drop(['list_date'], axis=1, inplace=True)
		df.reset_index(drop=True, inplace=True)
		return df

	# 记录api爬取的信息防患于未然（存储位置与配置文件相同）
	def record_api_message(self):
		df = pd.DataFrame(
			{'delcode': [self.__delcode], 'stcode': [self.__stcode], 'open_date': [self.open_date.apply(
				lambda x: x.replace('-', '')).to_list()]})
		df.to_json(self.configpath + 'record_api_message.json', orient='records', indent=1)

	@staticmethod
	def get_tableinfo_cols(dbfile, tablename):
		df_tableinfo = pd.read_sql('PRAGMA table_info([' + tablename + '])', con=sqlite3.connect(dbfile))
		return df_tableinfo['name'].to_list()

	# 处理并检查输入的time选择区间
	@staticmethod
	def __check_mintime(start, end):
		if start is not None:
			assert isinstance(start, str) and len(start) == 8 and start.replace(':', '').isdigit() and start[0: 2] < '24'\
				and start[3: 5] < '60' and start[6: 8] < '60', 'time_start必须为形如09:30:00的字符,且大小符合时间进制'
		if end is not None:
			assert isinstance(end, str) and len(end) == 8 and end.replace(':', '').isdigit() and end[0: 2] < '24' and \
				end[3: 5] < '60' and end[6: 8] < '60', 'time_end必须为形如09:30:00的字符,且大小符合时间进制'
		if start is not None and end is not None:
			str_mintime = ' AND time >= "' + start + '" AND time <= ' + '"' + end + '"'
		elif start is not None and end is None:
			str_mintime = ' AND time >= "' + start + '"'
		elif start is None and end is not None:
			str_mintime = ' AND time <= "' + end + '"'
		else:
			str_mintime = ''
		return str_mintime

	# 处理并检查时间输入，转变为sql语句
	@staticmethod
	def check_time(time):
		if isinstance(time, int):
			if 19000000 < time <= int(datetime.date.today().strftime('%Y%m%d')):
				time = str(time)
				str_time = time[0:4] + '-' + time[4:6] + '-' + time[6:]
			else:
				raise ValueError('数值型start,time必须为8位数int,如20180808,且日期不能超过今日,当前输入:{}'.format(time))
		elif isinstance(time, str):
			if len(time) == 10:
				time = datetime.datetime.strptime(time, '%Y-%m-%d')
			elif len(time) == 8:
				time = datetime.datetime.strptime(time, '%Y%m%d')
			elif len(time) == 19:
				time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
			else:
				raise ValueError('输入str类型时间仅支持"2010-08-08"或"20100808"')
			# # 转str
			# if time.date() > datetime.date.today():
			# 	raise ValueError('输入时间超过了今日，请勿穿越未来')
			# else:
			str_time = time.strftime('%Y-%m-%d')

		elif isinstance(time, datetime.datetime):
			try:
				str_time = time.strftime('%Y-%m-%d')
			except ValueError:
				raise ValueError('datetime型start,time必须符合YYYY-MM-DD hh:mm:ss,如2018-08-08 00:00:00')
		else:
			raise ValueError('时间格式错误:{}'.format(time))
		return str_time

	@staticmethod
	def __check_dbtablename(dbname, tablename):
		assert isinstance(dbname, str), 'dbname必须为str，如tushare_data.sqlite3或tushare_data'
		assert isinstance(tablename, str), 'tablename必须为str如ts_day_data'
		if '.sqlite3' in dbname:
			pass
		else:
			dbname = dbname + '.sqlite3'
		return dbname

	# 确定shift和forward时间
	def __check_timechange(self, start, end, shift, forward, minmode=False):
		if not isinstance(shift, int) or not isinstance(forward, int) or shift < 0 or forward < 0:
			raise ValueError('shift必须为大于0的int')
		else:
			if shift == 0:
				str_start = start
				pass
			else:
				str_start = self.open_date[self.open_date < start].tail(shift).tolist()[0]

			if forward == 0:
				str_end = end
				pass
			else:
				if len(self.open_date[self.open_date > end]) > 0:
					str_end = self.open_date[self.open_date > end].head(forward).tolist()[-1]
				else:
					raise ValueError('forward时间过长,不能穿越到未来！')
			if minmode:
				str_start = '{0}{1}{2}{0}'.format('"', str_start, ' 00:00:00')
				str_end = '{0}{1}{2}{0}'.format('"', str_end, ' 23:00:00')
			else:
				str_start = '{0}{1}{0}'.format('"', str_start)
				str_end = '{0}{1}{0}'.format('"', str_end)
			return str_start, str_end

	# 检查股票代码输入是否正确并生成sql的code查询语句
	# @staticmethod
	def __check_code(self, code, dbname_code, indexmode=False):
		if code is None:
			# str_code = ' '
			if indexmode:
				code = self.allcode_index
			else:
				code = self.allcode
		if isinstance(code, list):
			code = '(' + ','.join(map(lambda x: str(int(x)), code)) + ')'
			str_code = dbname_code + ' in ' + code + ' AND '
		elif isinstance(code, int):
			code = '(' + str(code) + ')'
			str_code = dbname_code + ' in ' + code + ' AND '
		elif isinstance(code, pd.Series):
			code = '(' + ','.join(map(lambda x: str(int(x)), code.to_list())) + ')'
			str_code = dbname_code + ' in ' + code + ' AND '
		else:
			raise ValueError('输入的code为{},请保证code格式为 list 或 int'.format(type(code)))

		return str_code

	# 检查fields是否有效并处理fields格式
	@staticmethod
	def __check_fields(fields, standard_fields):
		# 全选处理
		if fields == '*':
			return fields
		else:
			# str形式处理
			if isinstance(fields, str):
				try:
					fieldslist = fields.split(',')
					errorlist = []
					for column in fieldslist:
						if column in standard_fields:
							pass
						else:
							errorlist.append(column)
					if len(errorlist) == 0:
						return fields
					else:
						raise ValueError('当前查询表内不存在列名：{}'.format(errorlist))
				except:
					raise ValueError('fields输入有误，非合法字符串或字符串list')
			# list形式处理
			if hasattr(fields, "__iter__"):
				errorlist = []
				for column in fields:
					if column in standard_fields:
						pass
					else:
						errorlist.append(column)
				if len(errorlist) == 0:
					str_fields = ','.join(fields)
					return str_fields
				else:
					raise ValueError('当前查询表内不存在列名：{}'.format(errorlist))

	@staticmethod
	def __fields_append(fields, time_start=None, time_end=None, noncode=False):
		fieldsdrop = {'code': 0, 'date': 0, 'time': 0}
		if fields == '*':
			return fieldsdrop, fields
		fieldslist = fields.split(',')
		if 'date' in fieldslist:
			pass
		else:
			fieldsdrop['date'] = 1
			fields = 'date,' + fields
		if 'code' in fieldslist or noncode:
			pass
		else:
			fieldsdrop['code'] = 1
			fields = 'code,' + fields
		if time_start is not None or time_end is not None:
			if 'time' in fieldslist:
				pass
			else:
				fieldsdrop['time'] = 1
				fields = 'time,' + fields
		return fieldsdrop, fields

	@staticmethod
	def __fields_drop(df, fieldsdrop):
		dropfield = [x for x in fieldsdrop.keys() if fieldsdrop[x] == 1]
		if len(dropfield) > 0:
			df.drop(dropfield, axis=1, inplace=True)
		return df

	# 剔除ST股
	def __st_clean(self, df, dbname_code, start, fields, stdrop):
		if not stdrop:
			return df
		start = start.replace('"', '')
		if (dbname_code in fields and 'date' in fields) or fields == '*':
			df_stcode = self.__stcode[self.__stcode['end_date'] >= start]
			df_stcode = df_stcode.sort_values(by=['code', 'start_date'])
			df_stcode.reset_index(inplace=True, drop=True)
			# df_stcode.drop_duplicates(subset=['code'], keep='first', inplace=True)
			df_stcode = df_stcode.groupby('code').agg({'start_date': 'min', 'end_date': 'max'}).reset_index()
			df = pd.merge(df, df_stcode.rename(columns={
				'start_date': 'st_kaishi', 'end_date': 'st_jieshu'}), on='code', how='left')
			df['st_kaishi'] = df['st_kaishi'].fillna('2099-09-09')
			df['st_jieshu'] = df['st_jieshu'].fillna('2099-09-09')
			df = df[~((df['st_kaishi'] <= df['date']) & (df['date'] <= df['st_jieshu']))]
			df.drop(['st_kaishi', 'st_jieshu'], axis=1, inplace=True)
			df.reset_index(drop=True, inplace=True)
		else:
			raise ValueError('stdrop为True时，fields必须为*或包含股票代码，日期字段（code和date）')
		return df

	# 剔除退市股
	def __del_clean(self, df, dbname_code, fields, deldrop):
		if not deldrop:
			return df
		if dbname_code in fields or fields == '*':
			df = df[~df[dbname_code].isin(self.__delcode)]
			df = df.reset_index().drop(['index'], axis=1)
		else:
			raise ValueError('deldrop为True时，fields必须为*或包含股票代码有效字段（code或code）')
		return df

	# 剔除科创板
	@staticmethod
	def __star_clean(stardrop, dbname_code):
		if isinstance(stardrop, bool):
			if stardrop:
				str_stardrop = ' AND ' + dbname_code + '<=650000'
			else:
				str_stardrop = ''
		else:
			raise ValueError('stardrop参数为bool值')
		return str_stardrop

	def get_timesection(self, start, end, shift=0, forward=0, mode='str'):
		"""
		:param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param end: 结束日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int
		:param mode: 时间格式，默认str，支持str datetime int

		:return: dataframe格式数据表.
		"""

		assert isinstance(shift, int) and isinstance(forward, int), 'shift或forward的值必须为≥0的int'
		assert shift >= 0 and forward >= 0, 'shift,forward为非负整数'
		assert mode in ['str', 'datetime', 'int', 'date'], 'mode参数仅可选str，datetime，int,date'
		# time格式检查
		start = self.get_opendate(time=start, shift=shift)
		end = self.get_opendate(time=end, forward=forward)
		if start > end:
			raise ValueError('获取交易日历的开始日期不能大于截止日期')
		timesection = list(self.open_date[(self.open_date >= start) & (self.open_date <= end)])
		# 设定时间格式
		if mode == 'str':
			pass
		elif mode == 'datetime':
			timesection = [datetime.datetime.strptime(x, '%Y-%m-%d') for x in timesection]
		elif mode == 'date':
			timesection = [datetime.datetime.strptime(x, '%Y-%m-%d').date() for x in timesection]
		elif mode == 'int':
			timesection = [int(x.replace('-', '')) for x in timesection]
		else:
			pass
		return timesection

	def get_opendate(self, time, shift=0, forward=0, mode='str'):
		"""
		:param time: 基准日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int
		:param mode: 时间格式，默认str，支持str datetime int

		:return: dataframe格式数据表.
		"""

		assert isinstance(shift, int) and isinstance(forward, int), 'shift或forward的值必须为≥0的int'
		assert shift >= 0 and forward >= 0, 'shift和forward为非负整数'
		assert not (shift > 0 and forward > 0), 'shift或forward只能选一个'
		assert mode in ['str', 'datetime', 'int', 'date'], 'mode参数仅可选str，datetime，int,date'
		if not isinstance(shift, int) or not isinstance(forward, int):
			raise ValueError('shift或forward的值必须为≥0的int')
		if shift > 0 and forward > 0:
			raise ValueError('shift或forward只能选一个')
		# time格式检查
		stime = self.check_time(time=time)
		# shift 确认
		if shift > 0:
			stime = self.open_date[self.open_date < stime].tail(shift).tolist()[0]
		else:
			pass
		# forward 确认
		if forward > 0:
			stime = self.open_date[self.open_date > stime].head(forward).tolist()[-1]
		else:
			pass
		# 设定时间格式
		if mode == 'str':
			return stime
		elif mode == 'datetime':
			return datetime.datetime.strptime(stime, '%Y-%m-%d')
		elif mode == 'date':
			return datetime.datetime.strptime(stime, '%Y-%m-%d').date()
		elif mode == 'int':
			return int(stime.replace('-', ''))

	def read_ts_day_data(
			self, start, end, fields='*', code=None, shift=0, forward=0, newdrop=0,
			stdrop=True, deldrop=False, stardrop=True):
		"""
		:param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param end: 结束日期 ，必选，支持同start
		:param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
		:param code: 代码，默认取所有，支持int如300, list如[1, '300', 399905]列表内可以是数值或str
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int
		:param newdrop: 新股上市多少交易日内不交易，默认0，仅支持int
		:param stdrop: 是否剔除st股，True剔除，默认True
		:param deldrop: 是否剔除退市股，True剔除，默认False
		:param stardrop: 是否剔除科创板股，True剔除，默认True

		:return: dataframe格式数据表.
		"""

		dbname_date = 'date'
		dbname_code = 'code'
		col = self.get_tableinfo_cols(Path(self.config.loc[0, 'dbpath']).joinpath('tushare_data.sqlite3'), 'ts_day_data')
		start_date = self.check_time(time=start)
		end_date = self.check_time(time=end)
		str_start, str_end = self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward)
		str_code = self.__check_code(code=code, dbname_code=dbname_code)
		str_fields = self.__check_fields(fields=fields, standard_fields=col)
		fieldsdrop, str_fields = self.__fields_append(str_fields)

		str_stardrop = self.__star_clean(stardrop=stardrop, dbname_code=dbname_code)
		str_sql = \
			'SELECT ' + str_fields + ' FROM ' + 'ts_day_data' + ' WHERE ' + str_code + '(' \
			+ dbname_date + '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + ')' + str_stardrop
		try:
			connect = sqlite3.connect(Path(self.config.loc[0, 'dbpath']).joinpath('tushare_data.sqlite3'))
			df = pd.read_sql(str_sql, con=connect)
			connect.close()
		except Exception:
			raise ConnectionError('数据库数据获取失败，请确保tushare_data库存在')
		if len(df) > 0:
			df = self.__st_clean(df=df, dbname_code=dbname_code, start=str_start, fields=str_fields, stdrop=stdrop)
			df = self.__new_clean(df=df, start=str_start, newdrop=newdrop)
			df = self.__del_clean(df=df, dbname_code=dbname_code, fields=str_fields, deldrop=deldrop)
			df = self.__fields_drop(df=df, fieldsdrop=fieldsdrop)
		else:
			pass
		return df

	def read_ts_index_daily(
			self, start, end, fields='*', code=None, shift=0, forward=0):
		"""
		:param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 09:00:00'), str('20180908')
		:param end: 结束日期 ，必选，支持同start
		:param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
		:param code: 代码，默认取所有，支持int如300, list如[1, '300', 600012]列表内可以是数值或str
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int

		:return: dataframe格式数据表.
		"""

		dbname_date = 'date'
		dbname_code = 'code'
		col = self.get_tableinfo_cols(
				Path(self.config.loc[0, 'dbpath']).joinpath('tushare_data.sqlite3'), 'ts_index_daily')
		start_date = self.check_time(time=start)
		end_date = self.check_time(time=end)
		str_code = self.__check_code(code=code, dbname_code=dbname_code, indexmode=True)
		str_start, str_end = self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward)
		str_fields = self.__check_fields(fields=fields, standard_fields=col)
		fieldsdrop, str_fields = self.__fields_append(str_fields)

		str_sql = \
			'SELECT ' + str_fields + ' FROM ' + 'ts_index_daily' + \
			' WHERE ' + str_code + '(' + dbname_date \
			+ '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + ')'
		try:
			connect = sqlite3.connect(Path(self.config.loc[0, 'dbpath']).joinpath('tushare_data.sqlite3'))
			df = pd.read_sql(str_sql, con=connect)
			connect.close()
		except Exception:
			raise ConnectionError('数据库数据获取失败，请确保tushare_data库存在')
		df = self.__fields_drop(df=df, fieldsdrop=fieldsdrop)
		return df

	def read_ts_limit_list(
			self, start, end, fields='*', code=None, shift=0, forward=0,
			stdrop=True, deldrop=False, stardrop=True, direction='U'):
		"""
		:param start: 开始日期，必选，支持int(20180808), datetime('2019-08-08 00:00:00'), str('20180808')
		:param end: 结束日期 ，必选，支持同start
		:param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
		:param code: 代码，默认取所有，支持int如300, list如[1, '300', 399905]列表内可以是数值或str
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int
		:param stdrop: 是否剔除st股，True剔除，默认True
		:param deldrop: 是否剔除退市股，True剔除，默认False
		:param stardrop: 是否剔除科创板股，True剔除，默认True
		:param stardrop: 是否剔除科创板股，True剔除，默认True
		:param direction: 输出涨停板还是跌停板，U涨停板，D跌停板，默认U

		:return: dataframe格式数据表.
		"""

		if direction in ['U', 'D']:
			str_direction = ' AND ts_limit="' + direction + '" '
		else:
			raise ValueError('type必须为U或者D')
		dbname_date = 'date'
		dbname_code = 'code'
		col = self.get_tableinfo_cols(
			Path(self.config.loc[0, 'dbpath']).joinpath('tushare_data.sqlite3'), 'ts_limit_list')
		start_date = self.check_time(time=start)
		end_date = self.check_time(time=end)
		str_code = self.__check_code(code=code, dbname_code=dbname_code)
		str_start, str_end = self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward)
		str_fields = self.__check_fields(fields=fields, standard_fields=col)
		fieldsdrop, str_fields = self.__fields_append(str_fields)

		str_stardrop = self.__star_clean(stardrop=stardrop, dbname_code=dbname_code)
		str_pct_chg = ' AND pct_chg < 11 '
		str_sql = \
			'SELECT ' + str_fields + ' FROM ' + 'ts_limit_list' + ' WHERE ' + str_code + '(' + dbname_date \
			+ '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + ')' + str_direction + str_stardrop + str_pct_chg
		try:
			connect = sqlite3.connect(Path(self.config.loc[0, 'dbpath']).joinpath('tushare_data.sqlite3'))
			df = pd.read_sql(str_sql, con=connect)
			connect.close()
		except Exception:
			raise ConnectionError('数据库数据获取失败，请确保tushare_data库存在')
		if len(df) > 0:
			df = self.__st_clean(df=df, dbname_code=dbname_code, start=str_start, fields=str_fields, stdrop=stdrop)
			df = self.__del_clean(df=df, dbname_code=dbname_code, fields=str_fields, deldrop=deldrop)
			df = self.__fields_drop(df=df, fieldsdrop=fieldsdrop)
		else:
			pass
		return df

	def read_ts_top_list(
			self, start, end, fields='*', code=None, shift=0, forward=0,
			stdrop=True, deldrop=False, stardrop=True):
		"""
		:param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20200808')
		:param end: 结束日期 ，必选，支持同start
		:param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
		:param code: 代码，默认取所有，支持int如300, list如[16, '300', 399905]列表内可以是数值或str
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int
		:param stdrop: 是否剔除st股，True剔除，默认True
		:param deldrop: 是否剔除退市股，True剔除，默认False
		:param stardrop: 是否剔除科创板股，True剔除，默认True

		:return: dataframe格式数据表.
		"""

		dbname_date = 'date'
		dbname_code = 'code'
		col = self.get_tableinfo_cols(
			Path(self.config.loc[0, 'dbpath']).joinpath('tushare_data.sqlite3'), 'ts_top_list')
		start_date = self.check_time(time=start)
		end_date = self.check_time(time=end)
		str_code = self.__check_code(code=code, dbname_code=dbname_code)
		str_start, str_end = self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward)
		str_fields = self.__check_fields(fields=fields, standard_fields=col)
		fieldsdrop, str_fields = self.__fields_append(str_fields)

		str_stardrop = self.__star_clean(stardrop=stardrop, dbname_code=dbname_code)
		str_sql = \
			'SELECT ' + str_fields + ' FROM ' + 'ts_top_list' + ' WHERE ' + str_code + '(' + dbname_date \
			+ '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + ')' + str_stardrop
		try:
			connect = sqlite3.connect(Path(self.config.loc[0, 'dbpath']).joinpath('tushare_data.sqlite3'))
			df = pd.read_sql(str_sql, con=connect)
			connect.close()
		except Exception:
			raise ConnectionError('数据库数据获取失败，请确保tushare_data库存在')
		if len(df) > 0:
			df = self.__st_clean(df=df, dbname_code=dbname_code, start=str_start, fields=str_fields, stdrop=stdrop)
			df = self.__del_clean(df=df, dbname_code=dbname_code, fields=str_fields, deldrop=deldrop)
			df = self.__fields_drop(df=df, fieldsdrop=fieldsdrop)
		else:
			pass
		return df

	def read_ts_top_inst(
			self, start, end, fields='*', code=None, shift=0, forward=0,
			combine=False, stdrop=True, deldrop=False, stardrop=True):
		"""
		:param start: 开始日期，必选，支持int(20180809), datetime('2018-08-08 00:00:00'), str('20180808')
		:param end: 结束日期 ，必选，支持同start
		:param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
		:param code: 代码，默认取所有，支持int如300, list如[1, '300', 399905]列表内可以是数值或str
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int
		:param combine: 日内同只股票龙虎榜机构明细数据是否合并为一行，True合并，默认False，参数combie为True时，fields参数必须为*或包含code,sell_rate,buy_rate
		:param stdrop: 是否剔除st股，True剔除，默认True
		:param deldrop: 是否剔除退市股，True剔除，默认False
		:param stardrop: 是否剔除科创板股，True剔除，默认True

		:return: dataframe格式数据表.
		"""

		if not isinstance(combine, bool):
			raise ValueError('combine必须为True 或 False')
		dbname_date = 'date'
		dbname_code = 'code'
		col = self.get_tableinfo_cols(
			Path(self.config.loc[0, 'dbpath']).joinpath('tushare_data.sqlite3'), 'ts_top_inst')
		# if index_col == dbname_code and stdrop:
		# 	raise ValueError('选择index为股票时，不能剔除ST股')
		start_date = self.check_time(time=start)
		end_date = self.check_time(time=end)
		str_code = self.__check_code(code=code, dbname_code=dbname_code)
		str_start, str_end = self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward)
		str_fields = self.__check_fields(fields=fields, standard_fields=col)
		fieldsdrop, str_fields = self.__fields_append(str_fields)

		str_stardrop = self.__star_clean(stardrop=stardrop, dbname_code=dbname_code)
		str_sql = \
			'SELECT ' + str_fields + ' FROM ' + 'ts_top_inst' + ' WHERE ' + str_code + '(' + dbname_date \
			+ '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + ')' + str_stardrop
		if combine and str_fields != '*':
			checkfields = str_fields.split(',')
			lackparanum = [1 for x in [dbname_code, 'sell_rate', 'buy_rate'] if x not in checkfields]
			if sum(lackparanum) >= 1:
				raise ValueError('参数combie为True时，fields参数必须为*或包含code,sell_rate,buy_rate')
		try:
			connect = sqlite3.connect(Path(self.config.loc[0, 'dbpath']).joinpath('tushare_data.sqlite3'))
			df = pd.read_sql(str_sql, con=connect)
			connect.close()
		except Exception:
			raise ConnectionError('数据库数据获取失败，请确保tushare_data库存在')
		if len(df) > 0:
			df = self.__st_clean(df=df, dbname_code=dbname_code, start=str_start, fields=str_fields, stdrop=stdrop)
			df = self.__del_clean(df=df, dbname_code=dbname_code, fields=str_fields, deldrop=deldrop)
		if combine:
			dfgroup = df.groupby(['code', 'date'])
			df = dfgroup.sum().reset_index()
			df = self.__fields_drop(df=df, fieldsdrop=fieldsdrop)
		return df

	def read_ts_moneyflow_hsgt(
			self, start, end, fields='*', shift=0, forward=0):
		"""
		:param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param end: 结束日期 ，必选，支持同start
		:param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
		:param shift: 往前推的时间，默认0，仅支持int
		
		:param forward: 往后推的时间，默认0，仅支持int

		:return: dataframe格式数据表.
		"""

		dbname_date = 'date'
		col = self.get_tableinfo_cols(
			Path(self.config.loc[0, 'dbpath']).joinpath('tushare_data.sqlite3'), 'ts_moneyflow_hsgt')
		start_date = self.check_time(time=start)
		end_date = self.check_time(time=end)
		str_start, str_end = self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward)
		str_fields = self.__check_fields(fields=fields, standard_fields=col)
		fieldsdrop, str_fields = self.__fields_append(str_fields, noncode=True)
		str_sql = \
			'SELECT ' + str_fields + ' FROM ' + 'ts_moneyflow_hsgt' + ' WHERE ' + '(' + dbname_date + '>=' \
			+ str_start + ' AND ' + dbname_date + '<=' + str_end + ')'
		try:
			connect = sqlite3.connect(Path(self.config.loc[0, 'dbpath']).joinpath('tushare_data.sqlite3'))
			df = pd.read_sql(str_sql, con=connect)
			connect.close()
		except Exception:
			raise ConnectionError('数据库数据获取失败，请确保tushare_data库存在')
		df = self.__fields_drop(df=df, fieldsdrop=fieldsdrop)
		return df

	def read_tdx_1min_data(
			self, start, end, fields='*', code=None, shift=0, forward=0,
		time_start=None, time_end=None):
		"""
		:param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param end: 结束日期 ，必选，支持同start
		:param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
		:param code: 代码，默认取所有，支持int如300, list如[1, '300', 399905]列表内可以是数值或str
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int
		:param time_start: 开始时间，默认None，支持str如'09:35:30'
		:param time_end: 结束时间，默认None，支持str如'09:35:30'

		:return: dataframe格式数据表.
		"""

		dbname_date = 'datetime'
		dbname_code = 'code'
		col = self.get_tableinfo_cols(
			Path(self.config.loc[0, 'dbpath']).joinpath('tdx_1min_data.sqlite3'), 'tdx_1min_data')
		start_date = self.check_time(time=start)
		end_date = self.check_time(time=end)
		str_code = self.__check_code(code=code, dbname_code=dbname_code)
		str_start, str_end = \
			self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward, minmode=True)
		str_fields = self.__check_fields(fields=fields, standard_fields=col)
		fieldsdrop, str_fields = self.__fields_append(str_fields)
		str_time = self.__check_mintime(start=time_start, end=time_end)
		str_sql = \
			'SELECT ' + str_fields + ' FROM ' + 'tdx_1min_data' + ' WHERE ' + str_code + ' (' + \
			dbname_date + '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + str_time + ')'
		try:
			connect = sqlite3.connect(Path(self.config.loc[0, 'dbpath']).joinpath('tdx_1min_data.sqlite3'))
			# s = datetime.datetime.now()
			df = pd.read_sql(str_sql, con=connect)
			# ss = datetime.datetime.now()
			# print(ss - s)
			connect.close()
		except Exception:
			raise ConnectionError('数据库数据获取失败，请确保tushare_data库存在')
		df = self.__fields_drop(df=df, fieldsdrop=fieldsdrop)
		return df

	def read_concept_data(
			self, dictcode=False, dictconcept=False, dfcode=False, dfconcept=False, stardrop=True, dropstandard=None,
			aimcode=None, rawconcept=False):
		"""
		:param dictcode: 是否返回字典格式股票代码-所属版块，True返回，默认False（和其余参数4选1）
		:param dictconcept: 是否返回字典格式板块-包含股票，True返回，默认False（和其余参数4选1）
		:param  dfcode: 是否返回dataframe格式股票代码所属版块，True返回，默认False（和其余参数4选1）
		:param dfconcept: 是否返回字典格式板块-包含股票，True返回，默认False（和其余参数4选1）
		:param stardrop: 是否剔除科创板股，True剔除，默认True
		:param dropstandard: 剔除股票数量≥dropstandard的板块，默认None，仅支持int
		:param aimcode: 只选取特定股票的股票板块信息，支持元素为int的list Series array
		:param rawconcept: 是否返回原始一对一无嵌套板块df，默认False，为True时仅返回原始板块
		:return: dataframe格式板块信息
		"""

		assert isinstance(dictconcept, bool), 'dictconcept必须为bool'
		assert isinstance(dictcode, bool), 'dictcode必须为bool'
		assert isinstance(dfcode, bool), 'dfcode必须为bool'
		assert isinstance(dfconcept, bool), 'dfconcept必须为bool'
		assert isinstance(rawconcept, bool), 'rawconcept必须为bool'
		assert dictcode + dfcode + dfconcept + dictconcept < 2, '可选输出参数最多选择一个'
		str_stardrop = self.__star_clean(stardrop=stardrop, dbname_code='code')
		str_sql = 'SELECT concept_name,code' + ' FROM ' + 'dc_concept_data' + ' WHERE code > 0' + str_stardrop
		try:
			connect = sqlite3.connect(Path(self.config.loc[0, 'dbpath']).joinpath('tushare_data.sqlite3'))
			df = pd.read_sql(str_sql, con=connect)
			connect.close()
		except Exception:
			raise ConnectionError('数据库数据获取失败，请确保tushare_data库存在')
		if len(df) > 0:
			pass
		else:
			return df
		df = df[~ df['concept_name'].str.contains('涨停|触板|ST')]  # 剔除昨日涨停板块
		# 剔除股票数量＞=踢出标准的板块
		if not dropstandard:
			pass
		else:
			if isinstance(dropstandard, int) and dropstandard > 0:
				df_concount = df['concept_name'].value_counts()
				df = df[~df['concept_name'].isin(df_concount[df_concount >= dropstandard].index.to_list())]
			else:
				raise ValueError('dropstandard必须是正整数')

		# 剔除特定股票外的股票板块信息
		if isinstance(aimcode, list) or isinstance(aimcode, pd.Series) or isinstance(aimcode, np.ndarray):
			try:
				aimconcept = df[df['code'].isin(aimcode)]['concept_name'].unique()
				df = df[df['concept_name'].isin(aimconcept)]
			except Exception:
				raise ValueError('aimcode必须为list,Array,Series型')

		concept = df['concept_name'].unique()
		if rawconcept:
			return df
		concept = pd.DataFrame({'concept_name': concept}).reset_index().rename(columns={'index': 'concept'})
		concept['concept'] = concept['concept'].apply(lambda x: 'con' + str(x + 1))
		df = pd.merge(df, concept, how='left', on='concept_name')
		if dictcode:
			group_code = df.groupby('code')
			dict_code = {code: group_code.get_group(code)['concept'].tolist() for code in df['code'].unique()}
			return df, dict_code
		elif dictconcept:
			group_concept = df.groupby('concept')
			dict_concept = {con: group_concept.get_group(con)['code'].tolist() for con in concept['concept']}
			return df, dict_concept
		elif dfcode:
			group_code = df.groupby('code')
			dict_code = {code: group_code.get_group(code)['concept'].tolist() for code in df['code'].unique()}
			df_code = pd.DataFrame([dict_code]).T.reset_index().rename(columns={'index': 'code', 0: 'concept'})
			return df, df_code
		elif dfconcept:
			group_concept = df.groupby('concept')
			dict_concept = {con: group_concept.get_group(con)['code'].tolist() for con in concept['concept']}
			df_concept = pd.DataFrame([dict_concept]).T.reset_index().rename(columns={'index': 'concept', 0: 'code'})
			return df, df_concept
		else:
			return df

	def read_aucvol_data(
			self, start, end, fields='*', code=None, shift=0, forward=0,
			stdrop=True, deldrop=False, stardrop=True):
		"""
		:param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param end: 结束日期 ，必选，支持同start
		:param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
		:param code: 代码，默认取所有，支持int如300, list如[1, '300', 399905]列表内可以是数值或str
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int
		:param stdrop: 是否剔除st股，True剔除，默认True
		:param deldrop: 是否剔除退市股，True剔除，默认False
		:param stardrop: 是否剔除科创板股，True剔除，默认True

		:return: dataframe格式数据表.
		"""

		dbname_date = 'date'
		dbname_code = 'code'
		col = self.get_tableinfo_cols(
			Path(self.config.loc[0, 'dbpath']).joinpath('tushare_data.sqlite3'), 'cal_auctionvol_data')
		start_date = self.check_time(time=start)
		end_date = self.check_time(time=end)
		str_code = self.__check_code(code=code, dbname_code=dbname_code)
		str_start, str_end = self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward)
		str_fields = self.__check_fields(fields=fields, standard_fields=col)
		fieldsdrop, str_fields = self.__fields_append(str_fields)
		str_stardrop = self.__star_clean(stardrop=stardrop, dbname_code=dbname_code)
		str_sql = \
			'SELECT ' + str_fields + ' FROM ' + 'cal_auctionvol_data' + ' WHERE ' + str_code + '(' + dbname_date \
			+ '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + ')' + str_stardrop
		try:
			connect = sqlite3.connect(Path(self.config.loc[0, 'dbpath']).joinpath('tushare_data.sqlite3'))
			df = pd.read_sql(str_sql, con=connect)
			connect.close()
		except Exception:
			raise ConnectionError('数据库数据获取失败，请确保tushare_data库存在')
		if len(df) > 0:
			df = self.__st_clean(df=df, dbname_code=dbname_code, start=str_start, fields=str_fields, stdrop=stdrop)
			df = self.__del_clean(df=df, dbname_code=dbname_code, fields=str_fields, deldrop=deldrop)
		df = self.__fields_drop(df=df, fieldsdrop=fieldsdrop)
		return df

	def read_jj_1min_index_data(
			self, start, end, fields='*', code=None, shift=0, forward=0):
		"""
		:param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param end: 结束日期 ，必选，支持同start
		:param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
		:param code: 代码，默认取所有，支持int如300, list如[1, '300', 399905]列表内可以是数值或str
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int

		:return: dataframe格式数据表.
		"""

		dbname_date = 'datetime'
		dbname_code = 'code'
		col = self.get_tableinfo_cols(
			Path(self.config.loc[0, 'dbpath']).joinpath('jj_data.sqlite3'), 'jj_1min_index_data')
		start_date = self.check_time(time=start)
		end_date = self.check_time(time=end)
		str_code = self.__check_code(code=code, dbname_code=dbname_code, indexmode=True)
		str_start, str_end = \
			self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward, minmode=True)
		str_fields = self.__check_fields(fields=fields, standard_fields=col)
		fieldsdrop, str_fields = self.__fields_append(str_fields)

		str_sql = \
			'SELECT ' + str_fields + ' FROM ' + 'jj_1min_index_data' + ' WHERE ' + str_code + ' (' + \
			dbname_date + '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + ')'
		try:
			connect = sqlite3.connect(Path(self.config.loc[0, 'dbpath']).joinpath('jj_data.sqlite3'))
			df = pd.read_sql(str_sql, con=connect)
			connect.close()
		except Exception:
			raise ConnectionError('数据库数据获取失败，请确保jj_data库存在')
		return df

	def read_tdx_5min(
			self, start, end, fields='*', code=None, shift=0, forward=0):
		"""
		:param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param end: 结束日期 ，必选，支持同start
		:param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
		:param code: 代码，默认取所有，支持int如300, list如[1, '300', 399905]列表内可以是数值或str
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int

		:return: dataframe格式数据表.
		"""

		dbname_date = 'datetime'
		dbname_code = 'code'
		col = self.get_tableinfo_cols(
			Path(self.config.loc[0, 'dbpath']).joinpath('tdx_data_5min.sqlite3'), 'tdx_5min_1819')
		start_date = self.check_time(time=start)
		end_date = self.check_time(time=end)
		str_code = self.__check_code(code=code, dbname_code=dbname_code)
		str_start, str_end = self.__check_timechange(
			start=start_date, end=end_date, shift=shift, forward=forward, minmode=True)
		str_fields = self.__check_fields(fields=fields, standard_fields=col)
		fieldsdrop, str_fields = self.__fields_append(str_fields)
		str_sql = \
			'SELECT ' + str_fields + ' FROM ' + 'tdx_data_5min' + ' WHERE ' + str_code + ' (' + \
			dbname_date + '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + ')'
		try:
			connect = sqlite3.connect(Path(self.config.loc[0, 'dbpath']).joinpath('tdx_data_5min.sqlite3'))
			df = pd.read_sql(str_sql, con=connect)
			connect.close()
		except Exception:
			raise ConnectionError('数据库数据获取失败，请确保tdx_data_5min库存在')
		return df

	def read_df_tech_week_qfq(
			self, start, end, fields='*', code=None, shift=0, forward=0,
			stdrop=True, deldrop=False, stardrop=True):
		"""
		:param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param end: 结束日期 ，必选，支持同start
		:param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
		:param code: 代码，默认取所有，支持int如300, list如[1, '300', 399905]列表内可以是数值或str
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int
		:param stdrop: 是否剔除st股，True剔除，默认True
		:param deldrop: 是否剔除退市股，True剔除，默认False
		:param stardrop: 是否剔除科创板股，True剔除，默认True

		:return: dataframe格式数据表.
		"""

		dbname_date = 'date'
		dbname_code = 'code'
		col = self.get_tableinfo_cols(
			Path(self.config.loc[0, 'dbpath']).joinpath('tdx_data_5min.sqlite3'), 'tech_week_qfq')
		start_date = self.check_time(time=start)
		end_date = self.check_time(time=end)
		str_start, str_end = self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward)
		str_code = self.__check_code(code=code, dbname_code=dbname_code)
		str_fields = self.__check_fields(fields=fields, standard_fields=col)
		fieldsdrop, str_fields = self.__fields_append(str_fields)
		str_stardrop = self.__star_clean(stardrop=stardrop, dbname_code=dbname_code)
		str_sql = \
			'SELECT ' + str_fields + ' FROM ' + 'df_tech_week_qfq' + ' WHERE ' + str_code + '(' \
			+ dbname_date + '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + ')' + str_stardrop
		try:
			connect = sqlite3.connect(Path(self.config.loc[0, 'dbpath']).joinpath('tdx_data_5min.sqlite3'))
			df = pd.read_sql(str_sql, con=connect)
			connect.close()
		except Exception:
			raise ConnectionError('数据库数据获取失败，请确保tdx_data_5min库存在')
		if len(df) > 0:
			df = self.__st_clean(df=df, dbname_code=dbname_code, start=str_start, fields=str_fields, stdrop=stdrop)
			df = self.__del_clean(df=df, dbname_code=dbname_code, fields=str_fields, deldrop=deldrop)
			df = self.__fields_drop(df=df, fieldsdrop=fieldsdrop)
		else:
			pass
		return df

	def read_fundamentals(
			self, start, end, fields='*', code=None, shift=0, forward=0,
			stdrop=True, deldrop=False, stardrop=True):
		"""
		:param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param end: 结束日期 ，必选，支持同start
		:param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
		:param code: 代码，默认取所有，支持int如300, list如[1, '300', 399905]列表内可以是数值或str
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int
		:param stdrop: 是否剔除st股，True剔除，默认True
		:param deldrop: 是否剔除退市股，True剔除，默认False
		:param stardrop: 是否剔除科创板股，True剔除，默认True

		:return: dataframe格式数据表.
		"""

		dbname_date = 'date'
		dbname_code = 'code'
		col = self.get_tableinfo_cols(
			Path(self.config.loc[0, 'dbpath']).joinpath('fundamentals.sqlite3'), 'fundamentals')
		start_date = self.check_time(time=start)
		end_date = self.check_time(time=end)
		str_start, str_end = self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward)
		str_code = self.__check_code(code=code, dbname_code=dbname_code)
		str_fields = self.__check_fields(fields=fields, standard_fields=col)
		fieldsdrop, str_fields = self.__fields_append(str_fields)
		str_stardrop = self.__star_clean(stardrop=stardrop, dbname_code=dbname_code)
		str_sql = \
			'SELECT ' + str_fields + ' FROM ' + 'fundamentals' + ' WHERE ' + str_code + '(' \
			+ dbname_date + '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + ')' + str_stardrop
		try:
			connect = sqlite3.connect(Path(self.config.loc[0, 'dbpath']).joinpath('fundamentals.sqlite3'))
			df = pd.read_sql(str_sql, con=connect)
			connect.close()
		except Exception:
			raise ConnectionError('数据库数据获取失败，请确保fundamentals库存在')
		if len(df) > 0:
			df = self.__st_clean(df=df, dbname_code=dbname_code, start=str_start, fields=str_fields, stdrop=stdrop)
			df = self.__del_clean(df=df, dbname_code=dbname_code, fields=str_fields, deldrop=deldrop)
			df = self.__fields_drop(df=df, fieldsdrop=fieldsdrop)
		else:
			pass
		return df

	def read_strategy(
			self, start, end, tablename, fields='*', code=None, shift=0,
			forward=0, stdrop=True, deldrop=False, stardrop=True):
		"""
		:param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param end: 结束日期 ，必选，支持同start
		:param tablename: 策略版本
		:param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
		:param code: 代码，默认取所有，支持int如300, list如[1, '300', 399905]列表内可以是数值或str
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int
		:param stdrop: 是否剔除st股，True剔除，默认True
		:param deldrop: 是否剔除退市股，True剔除，默认False
		:param stardrop: 是否剔除科创板股，True剔除，默认True

		:return: dataframe格式数据表
		"""

		dbname_date = 'date'
		dbname_code = 'code'
		try:
			standard_fields = self.config.loc[0, 'col_' + tablename]
		except Exception as e:
			raise Exception('无法获取数据表的列名，策略库无表{}或未更新配置文件,检查tablename输入或更新配置文件'.format(tablename), e)
		start_date = self.check_time(time=start)
		end_date = self.check_time(time=end)
		str_start, str_end = self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward)
		str_code = self.__check_code(code=code, dbname_code=dbname_code)
		str_fields = self.__check_fields(fields=fields, standard_fields=standard_fields)
		fieldsdrop, str_fields = self.__fields_append(str_fields)

		str_stardrop = self.__star_clean(stardrop=stardrop, dbname_code=dbname_code)
		str_sql = \
			'SELECT ' + str_fields + ' FROM ' + tablename + ' WHERE ' + \
			str_code + '(' + dbname_date + '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + ')' + \
			str_stardrop
		try:
			connect = sqlite3.connect(Path(self.config.loc[0, 'dbpath']).joinpath('strategy_data.sqlite3'))
			df = pd.read_sql(str_sql, con=connect)
			connect.close()
		except Exception:
			raise ConnectionError('数据库数据获取失败，请确保strategy_data库存在')
		if len(df) > 0:
			df = self.__st_clean(df=df, dbname_code=dbname_code, start=str_start, fields=str_fields, stdrop=stdrop)
			df = self.__del_clean(df=df, dbname_code=dbname_code, fields=str_fields, deldrop=deldrop)
			df = self.__fields_drop(df=df, fieldsdrop=fieldsdrop)
		else:
			pass
		return df

	def read_mk_tech_day_data(
			self, start, end, fields='*', code=None, shift=0, forward=0,
			stdrop=True, deldrop=False, stardrop=True):
		"""
		:param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param end: 结束日期 ，必选，支持同start
		:param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
		:param code: 代码，默认取所有，支持int如300, list如[1, '300', 399905]列表内可以是数值或str
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int
		:param stdrop: 是否剔除st股，True剔除，默认True
		:param deldrop: 是否剔除退市股，True剔除，默认False
		:param stardrop: 是否剔除科创板股，True剔除，默认True

		:return: dataframe格式数据表.
		"""

		dbname_date = 'date'
		dbname_code = 'code'
		col = self.get_tableinfo_cols(
			Path(self.config.loc[0, 'dbpath']).joinpath('mk_data.sqlite3'), 'mk_tech_day_data')
		start_date = self.check_time(time=start)
		end_date = self.check_time(time=end)
		str_start, str_end = self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward)
		str_code = self.__check_code(code=code, dbname_code=dbname_code)
		str_fields = self.__check_fields(fields=fields, standard_fields=col)
		fieldsdrop, str_fields = self.__fields_append(str_fields)
		str_stardrop = self.__star_clean(stardrop=stardrop, dbname_code=dbname_code)
		str_sql = \
			'SELECT ' + str_fields + ' FROM ' + 'mk_tech_day_data' + ' WHERE ' + str_code + '(' \
			+ dbname_date + '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + ')' + str_stardrop
		try:
			connect = sqlite3.connect(Path(self.config.loc[0, 'dbpath']).joinpath('mk_data.sqlite3'))
			df = pd.read_sql(str_sql, con=connect)
			connect.close()
		except Exception:
			raise ConnectionError('数据库数据获取失败，请确保mk_data库存在')
		if len(df) > 0:
			df = self.__st_clean(df=df, dbname_code=dbname_code, start=str_start, fields=str_fields, stdrop=stdrop)
			df = self.__del_clean(df=df, dbname_code=dbname_code, fields=str_fields, deldrop=deldrop)
			df = self.__fields_drop(df=df, fieldsdrop=fieldsdrop)
		else:
			pass
		return df

	def read_cal_market_1min_data(
			self, start, end, fields='*', shift=0, forward=0):
		"""
		:param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param end: 结束日期 ，必选，支持同start
		:param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int

		:return: dataframe格式数据表.
		"""

		dbname_date = 'datetime'
		col = self.get_tableinfo_cols(
			Path(self.config.loc[0, 'dbpath']).joinpath('cal_market_data.sqlite3'), 'cal_market_1min_data')
		start_date = self.check_time(time=start)
		end_date = self.check_time(time=end)
		str_start, str_end = \
			self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward, minmode=True)
		str_fields = self.__check_fields(fields=fields, standard_fields=col)
		str_sql = \
			'SELECT ' + str_fields + ' FROM ' + 'cal_market_1min_data' + ' WHERE ' + ' (' + \
			dbname_date + '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + ')'
		try:
			connect = \
				sqlite3.connect(Path(self.config.loc[0, 'dbpath']).joinpath('cal_market_data.sqlite3'))
			df = pd.read_sql(str_sql, con=connect)
			connect.close()
		except Exception:
			raise ConnectionError('数据库数据获取失败，请确保jj_data库存在')
		return df

	def query_stock_day(
			self, start, end, tablename, dbname, fields='*', code=None, shift=0, forward=0, newdrop=0,
			stdrop=True, deldrop=False, stardrop=True):
		"""
		通用型股票日线数据接口，读取索引包含code，date的股票数据库 \n
		:param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param end: 结束日期 ，必选，支持同start
		:param tablename: 查询表名，str类型
		:param dbname: 数据库名，str类型，后缀可加可不加，如test或test.sqlite3均合法
		:param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
		:param code: 代码，默认取所有，支持int如300, list如[1, '300', 399905]列表内可以是数值或str
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int
		:param newdrop: 新股上市多少交易日内不交易，默认0，仅支持int
		:param stdrop: 是否剔除st股，True剔除，默认True
		:param deldrop: 是否剔除退市股，True剔除，默认False
		:param stardrop: 是否剔除科创板股，True剔除，默认True

		:return: dataframe格式数据表.
		"""

		dbname_date = 'date'
		dbname_code = 'code'
		dbname = self.__check_dbtablename(dbname, tablename)
		col = self.get_tableinfo_cols(Path(self.config.loc[0, 'dbpath']).joinpath(dbname), tablename)
		start_date = self.check_time(time=start)
		end_date = self.check_time(time=end)
		str_start, str_end = self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward)
		str_code = self.__check_code(code=code, dbname_code=dbname_code)
		str_fields = self.__check_fields(fields=fields, standard_fields=col)
		fieldsdrop, str_fields = self.__fields_append(str_fields)

		str_stardrop = self.__star_clean(stardrop=stardrop, dbname_code=dbname_code)
		str_sql = \
			'SELECT ' + str_fields + ' FROM ' + tablename + ' WHERE ' + str_code + '(' \
			+ dbname_date + '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + ')' + str_stardrop
		try:
			connect = sqlite3.connect(Path(self.config.loc[0, 'dbpath']).joinpath(dbname))
			df = pd.read_sql(str_sql, con=connect)
			connect.close()
		except Exception:
			raise ConnectionError(f'数据库数据获取失败，请确保{dbname}库以及{tablename}表存在')
		if len(df) > 0:
			df = self.__st_clean(df=df, dbname_code=dbname_code, start=str_start, fields=str_fields, stdrop=stdrop)
			df = self.__new_clean(df=df, start=str_start, newdrop=newdrop)
			df = self.__del_clean(df=df, dbname_code=dbname_code, fields=str_fields, deldrop=deldrop)
			df = self.__fields_drop(df=df, fieldsdrop=fieldsdrop)
		else:
			pass
		return df

	def query_stock_min(
			self, start, end, tablename, dbname, fields='*', code=None, shift=0, forward=0,
		time_start=None, time_end=None):
		"""
		通用型股票分钟数据接口，读取索引包含code，datetime，time的股票数据库 \n
		:param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param end: 结束日期 ，必选，支持同start
		:param tablename: 查询表名，str类型
		:param dbname: 数据库名，str类型，后缀可加可不加，如test或test.sqlite3均合法
		:param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
		:param code: 代码，默认取所有，支持int如300, list如[1, '300', 399905]列表内可以是数值或str
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int
		:param time_start: 开始时间，默认None，支持str如'09:35:30'
		:param time_end: 结束时间，默认None，支持str如'09:35:30'

		:return: dataframe格式数据表.
		"""

		dbname_date = 'datetime'
		dbname_code = 'code'
		dbname = self.__check_dbtablename(dbname, tablename)
		col = self.get_tableinfo_cols(
			Path(self.config.loc[0, 'dbpath']).joinpath(dbname), tablename)
		start_date = self.check_time(time=start)
		end_date = self.check_time(time=end)
		str_code = self.__check_code(code=code, dbname_code=dbname_code)
		str_start, str_end = \
			self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward, minmode=True)
		str_fields = self.__check_fields(fields=fields, standard_fields=col)
		fieldsdrop, str_fields = self.__fields_append(str_fields)
		str_time = self.__check_mintime(start=time_start, end=time_end)
		str_sql = \
			'SELECT ' + str_fields + ' FROM ' + tablename + ' WHERE ' + str_code + ' (' + \
			dbname_date + '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + str_time + ')'
		try:
			connect = sqlite3.connect(Path(self.config.loc[0, 'dbpath']).joinpath(dbname))
			df = pd.read_sql(str_sql, con=connect)
			connect.close()
		except Exception:
			raise ConnectionError(f'数据库数据获取失败，请确保{dbname}库以及{tablename}表存在')
		df = self.__fields_drop(df=df, fieldsdrop=fieldsdrop)
		return df

	def query_index_min(
			self, start, end, tablename, dbname, fields='*', code=None, shift=0, forward=0,
			time_start=None, time_end=None):
		"""
		通用型指数分钟数据接口，读取索引包含code，datetime，time的指数数据库 \n
		:param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param end: 结束日期 ，必选，支持同start
		:param tablename: 查询表名，str类型
		:param dbname: 数据库名，str类型，后缀可加可不加，如test或test.sqlite3均合法
		:param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
		:param code: 代码，默认取所有，支持int如300, list如[1, '300', 399905]列表内可以是数值或str
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int
		:param time_start: 开始时间，默认None，支持str如'09:35:30'
		:param time_end: 结束时间，默认None，支持str如'09:35:30'

		:return: dataframe格式数据表.
		"""

		dbname_date = 'datetime'
		dbname_code = 'code'
		dbname = self.__check_dbtablename(dbname, tablename)
		col = self.get_tableinfo_cols(
			Path(self.config.loc[0, 'dbpath']).joinpath(dbname), tablename)
		start_date = self.check_time(time=start)
		end_date = self.check_time(time=end)
		str_code = self.__check_code(code=code, dbname_code=dbname_code, indexmode=True)
		str_start, str_end = \
			self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward, minmode=True)
		str_fields = self.__check_fields(fields=fields, standard_fields=col)
		fieldsdrop, str_fields = self.__fields_append(str_fields)
		str_time = self.__check_mintime(start=time_start, end=time_end)

		str_sql = \
			'SELECT ' + str_fields + ' FROM ' + tablename + ' WHERE ' + str_code + ' (' + \
			dbname_date + '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + str_time + ')'
		try:
			connect = sqlite3.connect(Path(self.config.loc[0, 'dbpath']).joinpath(dbname))
			df = pd.read_sql(str_sql, con=connect)
			connect.close()
		except Exception:
			raise ConnectionError(f'数据库数据获取失败，请确保{dbname}库以及{tablename}表存在')
		return df

	def query_index_day(
			self, start, end, tablename, dbname, fields='*', code=None, shift=0, forward=0):
		"""
		通用型指数日线数据接口，读取索引包含code，date的指数数据库 \n
		:param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 09:00:00'), str('20180908')
		:param end: 结束日期 ，必选，支持同start
		:param tablename: 查询表名，str类型
		:param dbname: 数据库名，str类型，后缀可加可不加，如test或test.sqlite3均合法
		:param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
		:param code: 代码，默认取所有，支持int如300, list如[1, '300', 600012]列表内可以是数值或str
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int

		:return: dataframe格式数据表.
		"""

		dbname_date = 'date'
		dbname_code = 'code'
		dbname = self.__check_dbtablename(dbname, tablename)
		col = self.get_tableinfo_cols(
				Path(self.config.loc[0, 'dbpath']).joinpath(dbname), tablename)
		start_date = self.check_time(time=start)
		end_date = self.check_time(time=end)
		str_code = self.__check_code(code=code, dbname_code=dbname_code, indexmode=True)
		str_start, str_end = self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward)
		str_fields = self.__check_fields(fields=fields, standard_fields=col)
		fieldsdrop, str_fields = self.__fields_append(str_fields)

		str_sql = \
			'SELECT ' + str_fields + ' FROM ' + tablename + \
			' WHERE ' + str_code + '(' + dbname_date \
			+ '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + ')'
		try:
			connect = sqlite3.connect(Path(self.config.loc[0, 'dbpath']).joinpath(dbname))
			df = pd.read_sql(str_sql, con=connect)
			connect.close()
		except Exception:
			raise ConnectionError(f'数据库数据获取失败，请确保{dbname}库以及{tablename}表存在')
		df = self.__fields_drop(df=df, fieldsdrop=fieldsdrop)
		return df

	def query_market_min(
			self, start, end, tablename, dbname, fields='*', shift=0, forward=0, time_start=None, time_end=None):
		"""
		通用型市场分钟数据接口，读取索引包含datetime，time的市场数据库 \n
		:param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param end: 结束日期 ，必选，支持同start
		:param tablename: 查询表名，str类型
		:param dbname: 数据库名，str类型，后缀可加可不加，如test或test.sqlite3均合法
		:param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int
		:param time_start: 开始时间，默认None，支持str如'09:35:30'
		:param time_end: 结束时间，默认None，支持str如'09:35:30'

		:return: dataframe格式数据表.
		"""

		dbname_date = 'datetime'
		dbname = self.__check_dbtablename(dbname, tablename)
		col = self.get_tableinfo_cols(
			Path(self.config.loc[0, 'dbpath']).joinpath(dbname), tablename)
		start_date = self.check_time(time=start)
		end_date = self.check_time(time=end)
		str_start, str_end = \
			self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward, minmode=True)
		str_fields = self.__check_fields(fields=fields, standard_fields=col)
		str_time = self.__check_mintime(start=time_start, end=time_end)
		str_sql = \
			'SELECT ' + str_fields + ' FROM ' + tablename + ' WHERE ' + ' (' + \
			dbname_date + '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + str_time + ')'
		try:
			connect = \
				sqlite3.connect(Path(self.config.loc[0, 'dbpath']).joinpath(dbname))
			df = pd.read_sql(str_sql, con=connect)
			connect.close()
		except Exception:
			raise ConnectionError(f'数据库数据获取失败，请确保{dbname}库以及{tablename}表存在')
		return df

	def query_market_day(
			self, start, end, tablename, dbname, fields='*', shift=0, forward=0):
		"""
		通用型市场日线数据接口，读取索引包含date的市场数据库 \n 
		:param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param end: 结束日期 ，必选，支持同start
		:param tablename: 查询表名，str类型
		:param dbname: 数据库名，str类型，后缀可加可不加，如test或test.sqlite3均合法
		:param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int

		:return: dataframe格式数据表.
		"""

		dbname_date = 'date'
		dbname = self.__check_dbtablename(dbname, tablename)
		col = self.get_tableinfo_cols(
			Path(self.config.loc[0, 'dbpath']).joinpath(dbname), tablename)
		start_date = self.check_time(time=start)
		end_date = self.check_time(time=end)
		str_start, str_end = \
			self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward)
		str_fields = self.__check_fields(fields=fields, standard_fields=col)
		str_sql = \
			'SELECT ' + str_fields + ' FROM ' + tablename + ' WHERE ' + ' (' + \
			dbname_date + '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + ')'
		try:
			connect = \
				sqlite3.connect(Path(self.config.loc[0, 'dbpath']).joinpath(dbname))
			df = pd.read_sql(str_sql, con=connect)
			connect.close()
		except Exception:
			raise ConnectionError(f'数据库数据获取失败，请确保{dbname}库以及{tablename}表存在')
		return df

	def query_stock_limitday(
			self, date, code, tablename='ts_day_data', dbname='tushare_data', fields='*', shift=0, forward=0):
		"""
		返回单个code的指定天数的日线数据（部分股票停牌，可通过此接口忽略停牌日，取出固定长度数据）
		:param date: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param tablename: 查询表名，str类型
		:param dbname: 数据库名，str类型，后缀可加可不加，如test或test.sqlite3均合法
		:param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
		:param code: 代码，默认取所有，支持int如300, list如[1, '300', 600012]列表内可以是数值或str
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int

		:return: dataframe格式数据表.
		"""

		assert shift == 0 or forward == 0, 'shift，forward参数最多只能选一'
		dbname_date = 'date'
		dbname_code = 'code'
		dbname = self.__check_dbtablename(dbname, tablename)
		col = self.get_tableinfo_cols(Path(self.config.loc[0, 'dbpath']).joinpath(dbname), tablename)
		date = self.check_time(time=date)
		code = self.__check_code(code=code, dbname_code=dbname_code)
		code = code.replace(' ', '').replace('codein(', '').replace(')AND', '').split(',')
		str_fields = self.__check_fields(fields=fields, standard_fields=col)
		if shift == 0:
			str_limit = f'{dbname_date}>={repr(date)} LIMIT {shift + forward}'
		elif forward == 0:
			str_limit = f'{dbname_date}<={repr(date)} LIMIT {shift + forward}'
		else:
			raise Exception('shift,forward参数错误')
		try:
			connect = sqlite3.connect(Path(self.config.loc[0, 'dbpath']).joinpath(dbname))
			df = pd.DataFrame()
			for cod in code:
				str_sql = \
					'SELECT ' + str_fields + ' FROM ' + tablename + ' WHERE code=' + cod + ' AND ' + str_limit
				df_single = pd.read_sql(str_sql, con=connect)
				df = df.append(df_single)
			connect.close()
		except Exception:
			raise ConnectionError(f'数据库数据获取失败，请确保{dbname}库以及{tablename}表存在')
		return df


if __name__ == '__main__':
	# %% 首次执行区（生成/更新配置文件）
	# DBReader.firsttime_setconfig(
	# 	dbpath=r'D:\learn\navicat\data',
	# 	)
	# SetConfig.renew_config(configpath='../test_data/')


	# %% 初始化区---准备执行取数据
	# test = DBReader()
	# t = test.query_stock_limitday(date=20190912,forward=5,code=[1,'16'])
	# test0 = test.query_stock_day(start=20200402, end=20200402,tablename='ts_day_data', dbname='tushare_data')
	# test1 = test.query_stock_min(start=20200402, end=20200402,tablename='tdx_1min_data', dbname='tdx_1min_data')
	# test0 = test.query_index_day(start=20200402, end=20200402, tablename='ts_index_daily', dbname='tushare_data')
	# test1 = test.query_index_min(start=20200402, end=20200402, tablename='jj_1min_index_data', dbname='jj_data')
	# test2 = test.query_market_min(start=20200402, end=20200402, tablename='cal_market_1min_data', dbname='cal_market_data')
	# test3 = test.query_market_day(start=20200402, end=20200402, tablename='cal_market_1min_data', dbname='cal_market_data')
	# tests = test.read_strategy(tablename='factor_b2', start=20190402, end=20200402)
	a=1
	# %% 本地化记录爬虫信息区
	# test.record_api_message()

	# test0 = test.read_strategy(start='2020-04-20', end='2020-04-20', tablename='factor_b2')
	# test00 = test.read_mk_tech_day_data(start='2020-04-20', end=20200420, fields='code,date,ADX')
	#
	# # %% 测试区s
	# test1 = test.get_timesection(start=20200130, end='20200220', shift=1,forward=1,mode='str')
	# test2 = test.get_timesection(start=20200130, end='20200220', shift=1, forward=1, mode='int')
	# test3 = test.get_timesection(start=20200130, end='20200220', shift=1, forward=1, mode='datetime')
	# test4 = test.get_opendate(time=20200130, mode='datetime')
	# test01 = test.read_fundamentals(start=20200201, end='2020-02-05')  # 测试日期输入格式不同
	# test02 = test.read_fundamentals(start=20200130, end='20200220', fields='code,date,total_mv')  # 测试fields参数
	# test03 = test.read_fundamentals(start=20200205, end=20200205, shift=1)  # 测试shift参数
	# test04 = test.read_fundamentals(start=20200205, end=20200205, forward=1)  # 测试forward参数
	# test05 = test.read_fundamentals(start=20200205, end=datetime.datetime.today(), code=[1, '4', 5])  # 测试code参数
	# a = 1
	#
	# test0 = test.read_ts_day_data(
	# 	start='20200313', end=20200313, forward=1, shift=1, newdrop=60)
	# test1 = test.get_timesection(start='20200313', end=20200315, shift=5)
	# a=1
	# test2 = test.read_ts_top_inst(start=20190902, end=20200102, forward=1)
	# test3 = test.read_ts_top_list(start=20200301, end=datetime.datetime.today(), forward=8)
	# test4 = test.read_ts_day_data(
	# 	start=20200304, end=20200304, fields='date,adj_factor')
	# test5 = test.read_ts_index_daily(start=20200301, code=300, end=datetime.datetime.today(), shift=2)
	# test6 = test.read_ts_limit_list(start=20190712, end=20190712, shift=1)
	# test7 = test.read_ts_moneyflow_hsgt(start=20190712, end=20190720, shift=3)
	# test8 = test.read_aucvol_data(start=20200513, end=20200513)
	# test9 = test.read_concept_data()
	# test13,_ = test.read_concept_data(dfconcept=True)
	# test10, test11 = test.read_concept_data(dfcode=True)
	# test12 = test.read_concept_data(rawconcept=True)
	# a = 1

	# %% 参考区
	# test0 = test.read_ts_day_data(
	# 	start=20200313, end=20200313, forward=1, shift=1)
	# test1 = test.read_tdx_1min_data(start=20200420, end=20200420)
	# test2 = test.read_ts_top_inst(start=20190902, end=20200102, forward=1)
	# test3 = test.read_ts_top_list(start=20200301, end=datetime.datetime.today(), forward=8)
	# test4 = test.read_ts_day_data(
	# 	start=20200304, end=20200304, fields='date,adj_factor')
	# test5 = test.read_ts_index_daily(start=20200301, code=300, end=datetime.datetime.today(), shift=2)
	# test6 = test.read_ts_limit_list(start=20190712, end=20190712, shift=1)
	# test7 = test.read_ts_moneyflow_hsgt(start=20190712, end=20190720, shift=3)
	# test8 = test.read_aucvol_data(start=20200212, end=20200220, shift=1, code=600000, forward=1)
	# test9 = test.read_concept_data()
	# test10, test11 = test.read_concept_data(dfcode=True)
	# test12 = test.read_concept_data(rawconcept=True)
	# test13 = test.read_jj_1min_index_data(start=20190712, end=20190712, fields='datetime,code,high')
	# test14 = test.read_ts_limit_list(start=20200325, end=20200325)
	# test15 = test.read_ts_day_data(start=20140327, end=20140327)
	# test16 = test.read_tdx_1min_data(start=20200402, end=20200402)
	# test16 = test.read_tdx_1min_data(start=20200402, end=20200402, time_start='13:00:00', time_end='15:00:00')
	# test17 = test.read_cal_market_1min_data(start=20200402, end=20200402)
	# a = 1


