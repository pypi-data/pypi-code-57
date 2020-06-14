# -*- coding: utf-8 -*-
""" UUID 物件轉換輔助函式 / Value convert function for UUID object """

from typing import Any, Optional
from uuid import UUID


def to_uuid(v: Any, default_value: Optional[UUID] = None) -> Optional[UUID]:
	"""
	將輸入值轉換為 UUID 物件

	Convert given variable into UUID object. Return None or given default value when convert failed.

	Args:
		v: 要轉換的值或物件
		default_value=None: 預設值

	Returns:
		uuid.UUID 物件實體，或是 None 當輸入無法轉換
	"""
	if v is None:
		return default_value
	if isinstance(v, UUID):
		return v
	try:
		aux = UUID(v)
		return aux
	except Exception:
		pass
	return default_value
