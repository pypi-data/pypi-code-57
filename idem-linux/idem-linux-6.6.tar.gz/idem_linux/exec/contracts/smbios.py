# -*- coding: utf-8 -*-
from typing import Any, Dict, List


async def sig_get(hub, string: str, clean: bool = True) -> str:
    pass


async def sig_records(
    hub, rec_type: int = None, fields: str or List[str] = None, clean: bool = True
) -> List[Dict[str, Any]]:
    pass
