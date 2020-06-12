from abc import ABC
import uuid
"""
    Configuration Abstract
"""

# NOTE: We don't need this. It's more of a code smell. Creating objects using a pipeline instead. 

class Parameter(ABC):
    def __init__(self, *args, **kwargs):
        pass