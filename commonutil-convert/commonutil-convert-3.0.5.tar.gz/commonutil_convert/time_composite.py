# -*- coding: utf-8 -*-
""" 日期時間物件轉換輔助函式 / Value convert function for time related object """

from typing import Any, Optional, Sequence
import re
import datetime

from commonutil_convert.primitive import to_integer

import logging
_log = logging.getLogger(__name__)

_DATETIME_REGEX_yyyymmddhhmmss = re.compile(r'([0-9]{4})-?([0-9]{2})-?([0-9]{2})[_T\s\.]?([0-9]{2})?[\:\.\s_]?([0-9]{2})?[\:\.\s_]?([0-9]{2})?')
_DATETIME_REGEX_hhmmoffset = re.compile(r'([-+]?)([0-9]{2})([0-9]{2})?')


def _to_datetime_for_string(v: str) -> Optional[datetime.datetime]:
	v = v.strip()
	if v in (
			"utc-now",
			"UTC-NOW",
			"utcnow",
			"UTCNOW",
			"now",
			"NOW",
	):
		return datetime.datetime.utcnow()
	if v in (
			"local-now",
			"LOCAL-NOW",
			"localnow",
			"LOCALNOW",
	):
		return datetime.datetime.now()
	m = _DATETIME_REGEX_yyyymmddhhmmss.match(v)
	if m is not None:
		year = to_integer(m.group(1), 1970)
		month = to_integer(m.group(2), 1)
		day = to_integer(m.group(3), 1)
		hour = to_integer(m.group(4), 0)
		minute = to_integer(m.group(5), 0)
		second = to_integer(m.group(6), 0)
		return datetime.datetime(year, month, day, hour, minute, second)
	m = _DATETIME_REGEX_hhmmoffset.match(v)
	if m is not None:
		direction = m.group(1)
		hour_offset = to_integer(m.group(2), 0)
		minute_offset = to_integer(m.group(3), 0)
		# when not +/- mode, replace given hour and minute into current time as result
		current_tstamp = datetime.datetime.now()
		if (direction is None) or (direction == ""):
			return current_tstamp.replace(hour=hour_offset, minute=minute_offset, second=0)
		# when not offset to any time point
		if (hour_offset == 0) and (minute_offset == 0):
			return current_tstamp
		# when offset symbol (+/-) is given
		d = datetime.timedelta(hours=hour_offset, minutes=minute_offset)
		return (current_tstamp - d) if (direction == '-') else (current_tstamp + d)
	return None


def _to_datetime_for_sequence(v: Sequence[Any]) -> Optional[datetime.datetime]:
	year = None
	month = 1
	day = 1
	hour = 0
	minute = 0
	second = 0
	if len(v) >= 3:
		year = to_integer(v[0], 1970)
		month = to_integer(v[1], 1)
		day = to_integer(v[2], 1)
	if len(v) >= 4:
		hour = to_integer(v[3], 0)
	if len(v) >= 5:
		minute = to_integer(v[4], 0)
	if len(v) >= 6:
		second = to_integer(v[5], 0)
	# return result if valid
	return None if (year is None) else datetime.datetime(year, month, day, hour, minute, second)


def to_datetime(v: Any, default_value: Optional[datetime.datetime] = None) -> Optional[datetime.datetime]:
	"""
	將輸入值轉換為時間格式，當輸入值為 None 或是無法轉換的物件時傳回 None

	Convert given variable into datetime.datetime object. Return None or given default value when convert failed.

	輸入範例 / Input Examples:
		整數/浮點數 (視為 UNIX time-stamp) / Integer or Float (will treat as UNIT time-stamp):
			1352454146.387523
		字串 / String:
			'2012-11-10 10:10:10', '+01' (加 1 小時), '+0123' (加 1 小時 23 分鐘)
		串列或數對 / List or Tuple):
			(2012, 11, 10, 10, 10, 10, 0, 0, 0,)

	Args:
		v: 要轉換的值或物件
		default_value=None: 預設值

	Returns:
		時間格式，或是 None 當輸入無法轉換
	"""
	if v is None:
		return default_value
	if isinstance(v, datetime.datetime):
		return v
	if isinstance(v, (int, float)):
		return datetime.datetime.fromtimestamp(v)
	r = None
	if isinstance(v, str):
		r = _to_datetime_for_string(v)
	elif isinstance(v, Sequence):
		r = _to_datetime_for_sequence(v)
	if r is not None:
		return r
	_log.info("cannot convert input (%r) to datetime @[commonutil_convert.datetime.to_datetime]", v)
	return default_value
