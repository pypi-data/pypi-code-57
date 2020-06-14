# -*- coding: utf-8 -*-
""" 基本型態值轉換輔助函式值 / Value convert functions for primitive types """

from typing import Any, Optional
import logging
_log = logging.getLogger(__name__)


def to_text(v: Any, default_value: Optional[str] = None) -> Optional[str]:
	"""
	將輸入值轉換為字串，當輸入值為 None 或空字串或是無法轉換的物件時傳回 None

	Convert given variable into string. Return None or given default value when convert failed.

	Args:
		v: 要轉換的值或物件
		default_value=None: 預設值

	Returns:
		非空字串，或是 None 當輸入是空字串或是無法轉換的物件
	"""
	if v is None:
		return default_value
	r = None
	if isinstance(v, str):
		r = v
	elif isinstance(v, bytes):
		r = str(v, 'utf-8', 'ignore')
	else:
		try:
			r = str(v)
		except Exception:
			_log.info("cannot convert input (%r) to string @[commonutil_convert.primitive.to_text]", v)
			r = None
	if r is not None:
		r = r.strip()
		if r:
			return r
	return default_value


def to_integer(v: Any, default_value: Optional[int] = None) -> Optional[int]:
	"""
	將輸入值轉換為整數，當輸入值為 None 或是無法轉換的物件時傳回 None

	Convert given variable into integer. Return None or given default value when convert failed.

	Args:
		v: 要轉換的值或物件
		default_value=None: 預設值

	Returns:
		整數，或是 None 當輸入是空字串或是無法轉換的物件
	"""
	if v is None:
		return default_value
	try:
		r = int(v)
		return r
	except Exception:
		_log.info("cannot convert input (%r) to integer @[commonutil_convert.primitive.to_integer]", v)
	return default_value


def to_float(v: Any, default_value: Optional[float] = None) -> Optional[float]:
	"""
	將輸入值轉換為浮點數，當輸入值為 None 或是無法轉換的物件時傳回 None

	Convert given variable into float. Return None or given default value when convert failed.

	Args:
		v: 要轉換的值或物件
		default_value=None: 預設值

	Returns:
		非空字串，或是 None 當輸入是空字串或是無法轉換的物件
	"""
	if v is None:
		return default_value
	try:
		r = float(v)
		return r
	except Exception:
		_log.info("cannot convert input (%r) to float @[commonutil_convert.primitive.to_float]", v)
	return default_value


def to_bool(v: Any, default_value: Optional[bool] = None) -> Optional[bool]:
	"""
	將輸入值轉換為布林值，當輸入值為 None 或是無法轉換的物件時傳回 None

	Convert given variable into boolean. Return None or given default value when convert failed.

	Args:
		v: 要轉換的值或物件
		default_value=None: 預設值

	Returns:
		布林值，或是 None 當輸入無法轉換
	"""
	if v is None:
		return default_value
	try:
		if isinstance(v, bool):
			return v
		if isinstance(v, bytes):
			v = str(v, 'utf-8', 'ignore')
		if isinstance(v, str):
			if not v:
				return False
			return (v[0] in ('Y', 'y', 'T', 't', '1', '+'))
		if isinstance(v, (int, float)):
			return (int(v) > 0)
		return bool(v)
	except Exception:
		_log.info("cannot convert input (%r) to boolean @[commonutil_convert.primitive.to_bool]", v)
	return default_value
