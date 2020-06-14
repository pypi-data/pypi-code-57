# -*- coding: utf-8 -*-
""" 容器物件轉換輔助函式 / Value convert function for containers """

from typing import Any, Callable, Optional, List, Dict, Iterable, Mapping

from commonutil_convert.primitive import to_text

import logging
_log = logging.getLogger(__name__)


def to_list(v: Any, element_converter: Callable[[Any], Any], default_value: Optional[Any] = None) -> Optional[List[Any]]:
	"""
	將輸入值轉換為串列，各輸入值透過傳入的轉換函式進行轉換

	Convert given variable into list object with given element convert function.
	Return None or given default value when convert failed or result into empty list.

	Args:
		v: 要轉換的值或物件
		element_converter (callable): 單一個元素的轉換函式，當轉換結果為 None 時此元素會被丟棄
		default_value=None: 預設值

	Returns:
		串列，或是 None 當輸入無法轉換
	"""
	if v is None:
		return default_value
	result = []
	if (not isinstance(v, str)) and (not isinstance(v, bytes)) and (not isinstance(v, Mapping)) and isinstance(v, Iterable):
		for e in v:
			item = element_converter(e)
			if item is not None:
				result.append(item)
	else:
		item = element_converter(v)
		if item is not None:
			result.append(item)
	return result if result else default_value


def to_dict(v: Any,
			element_converter: Callable[[Any], Any],
			key_converter: Optional[Callable[[Any], Any]] = None,
			default_value: Optional[Any] = None) -> Optional[Dict[Any, Any]]:
	"""
	將輸入值轉換為字典，各輸入值透過傳入的轉換函式進行轉換

	Convert given variable into dict object with given key and value convert function.
	Return None or given default value when convert failed or result into empty dict.

	Args:
		v: 要轉換的值或物件
		element_converter (callable): 單一個元素的轉換函式，當轉換結果為 None 時此元素會被丟棄
		key_converter=None (callable): 單一元素對應之鍵值的轉換函式，當轉換結果為 None 時此元素會被丟棄
		default_value=None: 預設值

	Return:
		字典，或是 None 當輸入無法轉換
	"""
	if v is None:
		return default_value
	if key_converter is None:
		key_converter = to_text
	result = {}
	try:
		for k, e in v.items():
			kidx = key_converter(k)
			if kidx is None:
				continue
			item = element_converter(e)
			if item is not None:
				result[kidx] = item
	except Exception as e:
		_log.exception("failed on convert dictionary: %r", e)
	return result if result else default_value
