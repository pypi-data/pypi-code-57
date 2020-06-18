from typing import Optional
import numpy as np
import pandas as pd
from pydantic import BaseModel


class MetadataModel(BaseModel):
    # Get the average percentage change of the allocation
    name: Optional[str] = None
    category: Optional[str] = None
    subcategories: Optional[dict] = None
    metatype: Optional[str] = None
    submetatype: Optional[str] = None
    abbreviation: Optional[str] = None
