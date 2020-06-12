"""Separate search for the universe of assets. 
"""
from jamboree.handlers.default.search import BaseSearchHandler
class UniverseMetadata(BaseSearchHandler):
    def __init__(self):
        self.entity = "metadata"
        self.required = {
            "name": str,
            "category": str,
            "metatype": str,
            "submetatype": str,
            "abbreviation": str,
            "subcategories": dict
        }
    
    @property
    def search(self):
        self.reset()
        self['metatype'] = "multi_data_management"
        self['category'] = "universe"
        self["submetatype"] = "price_bag"
        return self
