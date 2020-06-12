import uuid
import maya

from typing import Optional
from jamboree import Jamboree
from jamboree.base.processors.abstracts import Processor
from jamboree.handlers.default.search import BaseSearchHandler

from loguru import logger

class SearchFacade(object):
    def __init__(self, search_handler:BaseSearchHandler, is_reset=False):
        self.must_have = []
        self.is_reset = is_reset
        
        
        
        # Hidden variables with properties
        self._search:BaseSearchHandler = search_handler
    
    @property
    def processor(self):
        if self._processor is None:
            raise AttributeError("The processor hasn't been set yet.")
        return self._processor

    @processor.setter
    def processor(self, _processor:Processor):
        self._processor = _processor
    
    @property
    def search(self):
        self._search.processor = self.processor
        return self._search
    
    def enable_reset(self):
        self.is_reset = True
    
    def disable_reset(self):
        self.is_reset = False

    def __check_requirements(self, items: dict):
        for _abs in self.must_have:
            if _abs not in items:
                raise NotImplementedError(
                    f"{_abs} has to be added. The absolute required variables are the following: {self.must_have}"
                )

    def __check_other_forced(self, forced: list, items: dict):
        for k in forced:
            if k not in items:
                raise AttributeError(f"{k} not in the arguments")

    def Create(self,
               allow_duplicates=False,
               no_overwrite_reqs=False,
               **kwargs):
        self.search.reset()
        self.__check_requirements(kwargs)

        if no_overwrite_reqs and len(self.must_have) > 0:
            
            _all = self.FForced(**kwargs)
            if len(_all) > 0:
                return _all[0].get("id")

        for k, v in kwargs.items():
            self.search[k] = v

        identity = self.search.insert(allow_duplicates=allow_duplicates)
        return identity

    def UpdateID(self, identity: str, **kwargs):
        """ Updates a record by ID. Gives a warning if you're using a must have variable."""
        self.reset()
        for k, v in kwargs.items():
            self.search.replacement[k] = v
        self.search.update_id(identity)

    def UpdateMany(self, search_dict: dict, force_must=False, **replacements):
        self.reset()
        if not bool(search_dict) or not bool(replacements):
            raise ValueError(
                "You need to have query information AND something to replace it with."
            )
        if force_must:
            self.__check_requirements(search_dict)

        for k, v in search_dict.items():
            self.search[k] = v

        for k, v in replacements.items():
            self.search.replacement[k] = v
        self.search.update()

    def Find(self, general=None,force_must=False, **fields):
        self.reset()
        if general is not None:
            self.general = general
        if not bool(fields):
            if general is not None:
                return self.search.find()
            raise ValueError("You have to search using something")
        if force_must:
            self.__check_requirements(fields)

        for k, v in fields.items():
            self.search[k] = v
        return self.search.find()

    def FindById(self, identity: str):
        self.reset()
        remainder = self.search.pick(identity)
        return remainder
    
    def FindForced(self, **kwargs):
        self.reset()
        self.__check_requirements(kwargs)
        for k in self.must_have:
            self.search[k] = kwargs.get(k)
        _all = self.search.find()
        return _all
    
    def FForced(self, **kwargs):
        for k in self.must_have:
            self.search[k] = kwargs.get(k)
        _all = self.search.find()
        return _all
    

    def Remove(self, **kwargs):
        self.reset()
        for k, v in kwargs.items():
            self.search[k] = v
        self.search.remove()
    
    def RemoveAll(self):
        self.search.reset()
        self.general = "*"
        self.search.remove()
    
    def reset(self):
        if self.is_reset:
            self.search.reset()
    
    def first(self, general=None, force_must=False, **kwargs):
        found = self.Find(general=general, force_must=force_must, **kwargs)
        if len(found) > 0:
            return found[0]
        raise AttributeError("No items matching the given profile was found.")

class PrototypeSearchFeatures(BaseSearchHandler):
    def __init__(self):
        super().__init__()
        self.must_have = []
        # Idea, try using upper case to distinguish from the base application.

    def __check_requirements(self, items: dict):
        for _abs in self.must_have:
            if _abs not in items:
                raise NotImplementedError(
                    f"{_abs} has to be added. The absolute required variables are the following: {self.must_have}"
                )

    def __check_other_forced(self, forced: list, items: dict):
        for k in forced:
            if k not in items:
                raise AttributeError(f"{k} not in the arguments")

    def Create(self,
               allow_duplicates=False,
               no_overwrite_reqs=False,
               **kwargs):
        self.reset()
        self.__check_requirements(kwargs)

        if no_overwrite_reqs and len(self.must_have) > 0:
            
            _all = self.FForced(**kwargs)
            if len(_all) > 0:
                return _all[0].id

        for k, v in kwargs.items():
            self[k] = v

        identity = self.insert(allow_duplicates=allow_duplicates)
        return identity

    def UpdateID(self, identity: str, **kwargs):
        """ Updates a record by ID. Gives a warning if you're using a must have variable."""
        self.reset()
        for k, v in kwargs.items():
            self.replacement[k] = v
        self.update_id(identity)

    def UpdateMany(self, search_dict: dict, force_must=False, **replacements):
        self.reset()
        if not bool(search_dict) or not bool(replacements):
            raise ValueError(
                "You need to have query information AND something to replace it with."
            )
        if force_must:
            self.__check_requirements(search_dict)

        for k, v in search_dict.items():
            self[k] = v

        for k, v in replacements.items():
            self.replacement[k] = v
        self.update()

    def Find(self, general=None,force_must=False, **fields):
        self.reset()
        if general is not None:
            self.general = general
        if not bool(fields):
            if general is not None:
                return self.find()
            raise ValueError("You have to search using something")
        if force_must:
            self.__check_requirements(fields)

        for k, v in fields.items():
            self[k] = v
        return self.find()

    def FindById(self, identity: str):
        self.reset()
        remainder = self.pick(identity)
        return remainder
    
    def FindForced(self, **kwargs):
        self.reset()
        self.__check_requirements(kwargs)
        for k in self.must_have:
            self[k] = kwargs.get(k)
        _all = self.find()
        return _all
    
    def FForced(self, **kwargs):
        for k in self.must_have:
            self[k] = kwargs.get(k)
        _all = self.find()
        return _all

    def Remove(self, **kwargs):
        self.reset()
        for k, v in kwargs.items():
            self[k] = v
        self.remove()
    
