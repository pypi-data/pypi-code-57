import tushare as ts
import pandas as pd
import time as tm
import os
import sqlite3
import re
import datetime
import logging
from logging import handlers
from qytools.db_read import DBReader
import numpy as np

# 基本工具箱，里面有便于数据库操作的各类函数

# 计时器，可计算代码用时
class Timer:
	def __init__(self):
		self._start = None
		self._name = ''

	def start(self, name=''):
		self._start = datetime.datetime.now()
		self._name = name

	def end(self):
		if self._start is not None:
			print(self._name, '\n', datetime.datetime.now() - self._start)
		else:
			raise Exception('先start才能end')


# 交易日操作类
class TradeDate:
	def __init__(self):
		try:
			pro = ts.pro_api()
		except:
			raise Exception('tushare连接出错，请检查本地是否token设置过后重新尝试连接')
		df_opendate = pro.query('trade_cal', start_date='20150101', end_date='20991231')  # 获取交易日
		df_opendate = df_opendate[df_opendate.is_open == 1]['cal_date']
		self.open_date = df_opendate.apply(lambda x: x[0:4] + '-' + x[4:6] + '-' + x[6:])

	def get_opendate(self, time, shift=0, forward=0, mode='str'):
		"""
		:param time: 基准日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int
		:param mode: 时间格式，默认str，支持str datetime int

		:return: dataframe格式数据表，未来将添加字典嵌套df选项
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
		stime = check_time(time=time)
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

	def get_timesection(self, start, end, shift=0, forward=0, mode='str'):
		"""
		:param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param end: 结束日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
		:param shift: 往前推的时间，默认0，仅支持int
		:param forward: 往后推的时间，默认0，仅支持int
		:param mode: 时间格式，默认str，支持str datetime int

		:return: dataframe格式数据表，未来将添加字典嵌套df选项
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


# 数据库的基本类,读取json文件,计算交易日等
class DbHandle:
	# 进行json文件读取的初始化
	def __init__(self, configpath):

		self.dbpath = None
		self.file_used = None
		today = tm.strftime('%Y%m%d', tm.localtime(tm.time()))
		self.logger = Logger('log/' + today + '.log', level='info')
		self.db_read = DBReader(configpath=r'./')
		self.trade_date = TradeDate()
		self.config_path = configpath
		print('[配置文件dbhandle_config.json读取成功]')
		if os.path.exists(configpath + 'dbhandle_config.json'):
			df_config = pd.read_json(configpath + 'dbhandle_config.json')
			self.config = df_config
			self.file_used = df_config.loc[0, 'file_used']
			self.dbpath = df_config.loc[0, 'dbpath']
			try:
				self.tdx_pathdir = None
				self.dbpath = None
				self.dbname_tushare_data = None
				self.dbname_tdx_1min_data = None
				self.dbname_tdx_5min_data = None
				self.dbname_factor_cal_data = None
				self.tablename_tdx_1min_data = 'tdx_1min_data'
				self.tablename_tdx_5min_data = 'tdx_5min_data'
				self.tablename_factor_b1 = 'factor_b1'
				for item in self.file_used:
					exec('self.dbname_' + item + ' = item')
				self.tdx_pathdir = df_config.loc[0, 'tdx_pathdir']
				self.dbpath = df_config.loc[0, 'dbpath']
				self.sz_1min_pathdir = self.tdx_pathdir + 'sz\\minline'
				self.sh_1min_pathdir = self.tdx_pathdir + 'sh\\minline'
				self.sz_5min_pathdir = self.tdx_pathdir + 'sz\\fzline'
				self.sh_5min_pathdir = self.tdx_pathdir + 'sh\\fzline'
			except:
				raise IndexError('_init_过程发生未知错误，请联系管理员')
		else:
			raise FileNotFoundError('配置文件目录{}不存在,请确认目录是否正确'.format(configpath))

	# 每次访问数据库新建连接，访问数据库结束后关闭连接，防止一些BUG的发生x
	def establish_connection(self, db_name):
		try:
			sqlite3.connect(self.dbpath + db_name + '.sqlite3')
			return sqlite3.connect(self.dbpath + db_name + '.sqlite3')
		except:
			raise ConnectionError('数据库连接失败，请检查数据库是否正常或联系管理员')

	# 存进表的通用接口
	def df_to_db(self, df, db_name, table_name, start=None, end=None):
		# 防止字符串日期无法识别报错
		try:
			if start:
				df = df[(df.date >= start)]
			elif end:
				df = df[(df.date <= end)]
		except:
			if start:
				df = df[(df.date >= datetime.datetime.strptime(start, '%Y-%m-%d'))]
			elif end:
				df = df[(df.date <= datetime.datetime.strptime(end, '%Y-%m-%d'))]
		db_conn = self.establish_connection(db_name=db_name)
		df.to_sql(table_name, con=db_conn, if_exists='append', index=False)
		db_conn.close()

	# 判断表是否存在，防止把表顶掉
	def table_exists(self, db_name, table_name):
		db_conn = self.establish_connection(db_name)
		db_cursor = db_conn.cursor()
		# 这个函数用来判断表是否存在
		sql = "select name from sqlite_master where type='table' order by name"
		db_cursor.execute(sql)
		tables = [db_cursor.fetchall()]
		table_list = re.findall('(\'.*?\')', str(tables))
		table_list = [re.sub("'", '', each) for each in table_list]
		db_conn.close()
		if table_name in table_list:
			return True
		else:
			return False

	# 获取当前更新日期
	def get_update_end_date(self):
		today = datetime.datetime.now()
		today_str = today.strftime("%Y%m%d")
		open_list = self.trade_date.get_timesection(start=today_str, end=today_str)
		if not open_list:
			self.logger.logger.info('[今天非交易日，默认更新至上一个交易日]')
			update_str = self.trade_date.get_opendate(time=today_str, shift=1, mode='str')
		else:
			if today.hour < 17:
				self.logger.logger.info('[未到当日收盘作业时点，默认更新至上一个交易日]')
				update_str = self.trade_date.get_opendate(time=today_str, shift=1, mode='str')
			else:
				self.logger.logger.info('[已到当日收盘作业时点，默认更新至本交易日]')
				update_str = today.strftime('%Y-%m-%d')
		update_datetime = datetime.datetime.strptime(update_str, '%Y-%m-%d')
		return update_datetime


# 记录数操作日志的类
class Logger(object):
	level_relations = {
		'debug': logging.DEBUG,
		'info': logging.INFO,
		'warning': logging.WARNING,
		'error': logging.ERROR,
		'crit': logging.CRITICAL,
	}       # 日志级别关系映射

	def __init__(self, filename, level='info', when='D', back_count=3,
		fmt = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
		self.logger = logging.getLogger(filename)
		format_str = logging.Formatter(fmt)                     # 设置日志格式
		self.logger.setLevel(self.level_relations.get(level))   # 设置日志级别
		sh = logging.StreamHandler()                            # 往屏幕上输出
		sh.setFormatter(format_str)                             # 设置屏幕上显示的格式
		# 往文件里写入
		# 指定间隔时间自动生成文件的处理器
		th = handlers.TimedRotatingFileHandler(
			filename=filename, when=when, backupCount=back_count, encoding='utf-8')
		# 实例化TimedRotatingFileHandler
		# interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，
		# when是间隔的时间单位，单位有以下几种：
		# S 秒
		# M 分
		# H 小时、
		# D 天、
		# W 每星期（interval==0时代表星期一）
		# midnight 每天凌晨
		th.setFormatter(format_str)         # 设置文件里写入的格式
		if not self.logger.handlers:
			self.logger.addHandler(sh)          # 把对象加到logger里
			self.logger.addHandler(th)


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
		# 转str
		if time.date() > datetime.date.today():
			raise ValueError('输入时间超过了今日，请勿穿越未来')
		else:
			str_time = time.strftime('%Y-%m-%d')

	elif isinstance(time, datetime.datetime):
		try:
			str_time = time.strftime('%Y-%m-%d')
		except ValueError:
			raise ValueError('datetime型start,time必须符合YYYY-MM-DD hh:mm:ss,如2018-08-08 00:00:00')
	else:
		raise ValueError('时间格式错误:{}'.format(time))
	return str_time


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


def _mktpye(code):
	# assert isinstance(code, (int, str)), 'code必须为int或者str'
	code = int(code)
	if code < 2000:
		return 2
	elif 2000 <= code < 300000:
		return 4
	elif 300000 <= code < 600000:
		return 3
	elif 600000 <= code < 688000:
		return 1
	elif 688000 <= code < 700000:
		return 5
	else:
		return 0


def mktpye(code):
	if isinstance(code, (int, str)):
		types = _mktpye(code=code)
	elif isinstance(code, (list, pd.Series, np.ndarray)):
		types = []
		for cod in code:
			cod = int(cod)
			types.append(_mktpye(code=cod))
	else:
		raise ValueError('输入的code必须为int，str或Series list array')
	return types


def get_ta_pattern():
	ta_fact = {
		1: [
			'CDLCLOSINGMARUBOZU', 'CDLDOJI', 'CDLDOJISTAR', 'CDLDRAGONFLYDOJI', 'CDLGRAVESTONEDOJI', 'CDLHAMMER',
			'CDLHANGINGMAN', 'CDLINVERTEDHAMMER', 'CDLLONGLEGGEDDOJI', 'CDLLONGLINE', 'CDLMARUBOZU',
			'CDLRICKSHAWMAN', 'CDLSHOOTINGSTAR', 'CDLSHORTLINE', 'CDLSPINNINGTOP', 'CDLTAKURI'],
		2: [
			'CDLBELTHOLD', 'CDLCOUNTERATTACK', 'CDLDARKCLOUDCOVER', 'CDLENGULFING', 'CDLGAPSIDESIDEWHITE',
			'CDLHARAMI', 'CDLHARAMICROSS', 'CDLHOMINGPIGEON', 'CDLINNECK', 'CDLKICKING', 'CDLKICKINGBYLENGTH',
			'CDLMATCHINGLOW', 'CDLONNECK', 'CDLPIERCING', 'CDLSEPARATINGLINES', 'CDLTHRUSTING'],
		3: [
			'CDL2CROWS', 'CDL3BLACKCROWS', 'CDL3INSIDE', 'CDL3OUTSIDE', 'CDL3STARSINSOUTH', 'CDL3WHITESOLDIERS',
			'CDLABANDONEDBABY', 'CDLADVANCEBLOCK', 'CDLEVENINGDOJISTAR', 'CDLEVENINGSTAR', 'CDLHIGHWAVE',
			'CDLHIKKAKE', 'CDLHIKKAKEMOD', 'CDLIDENTICAL3CROWS', 'CDLMORNINGDOJISTAR', 'CDLMORNINGSTAR',
			'CDLTASUKIGAP', 'CDLTRISTAR', 'CDLUNIQUE3RIVER', 'CDLUPSIDEGAP2CROWS', 'CDLSTALLEDPATTERN',
			'CDLSTICKSANDWICH'],
		4: ['CDL3LINESTRIKE', 'CDLCONCEALBABYSWALL'],
		5: ['CDLBREAKAWAY', 'CDLLADDERBOTTOM', 'CDLMATHOLD', 'CDLRISEFALL3METHODS', 'CDLXSIDEGAP3METHODS']}
	return ta_fact


def get_tradetime():
	tradetime = {
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
	return tradetime


class Stock:
	pass


class Market:
	pass


class Concept:
	pass


class Index:
	pass


def check_path(path):
		if len(path) == 0:
			pass
		elif path[-1] == '\\' or path[-1] == '/':
			pass
		else:
			path = path + '/'
		return path
