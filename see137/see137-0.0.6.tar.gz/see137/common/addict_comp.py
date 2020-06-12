import uuid
import inspect
from loguru import logger
from typing import List, Dict, Tuple, Any
from addict import Dict as ADict
from see137.common import ComponentAbstract


class AddictComponent(ComponentAbstract):
    """
        A component that centers around using dictionaries and addict.
    """
    def __init__(self):
        self.name = self.__class__.__name__
        
        self.within_pipeline = None
        self.required_items:Dict[str, type] = {}
        self.required_settings: Dict[str, type] = {}
        self.settings:ADict = ADict()
        self.is_implemented = False
        
    

    def set_settings(self, **kwargs):
        # self.settings.is_loud = kwargs.get("is_loud", False)
        failed = False
        msg = f"All settings here there for {self.name}"
        if not bool(self.required_settings):
            return failed, "No requirement items to check. Processing ..."

        keys = list(kwargs.keys())
        req_keys = (self.required_settings.keys())
        if len(keys) < len(req_keys):
            self.raise_loud(AttributeError, f"You need ALL of the following keys: {req_keys}. You have: {keys}")
            return True, msg
        try:
            for key, value in self.required_settings.items():
                cap = key.capitalize()
                # ck = key
                current = kwargs[key]
                if key not in keys:
                    raise ValueError(f"{cap} not in the kwargs. ")
                if not isinstance(current, value):
                    raise TypeError(f"{cap} not correct instance type {str(value)}. ")
                self.settings[key] = current
        except KeyError as ke:
            self.raise_loud(KeyError, f"You haven't added the key {str(ke)} to settings")
            return True, str(e)
        except Exception as e:
            self.raise_loud(e, str(e))
            return True, str(e)
        return failed, msg
    

    def check_prev(self, item:ADict):
        """Checks to see if the previous component failed. If it did we skip this task.

        Arguments:
            item {ADict} -- The previous item
        """

        if not bool(item.failed):
            item.failed = False
            item.msg = "Previous item succeeded. Processing here ..."


        if item.failed:
            item.failed = True
            if not bool(item.msg):
                item.msg = f"Previous Component Failed"
            self.raise_loud(ValueError, item.msg)
            
        return item
        
        

    def check_item(self, item:ADict) -> Tuple[bool, str]:
        failed = False
        msg = "All required items pass"
        if not bool(self.required_items):
            return failed, "No items to check."
        
        for key, value in self.required_items.items():
            current = item[key]
            is_valid = bool(current)
            is_bool = isinstance(current, bool)
            if not is_valid and not is_bool:
                failed = True
                msg = f"{key} field not found in the dictionary"
                self.raise_loud(TypeError, msg)
                break
            if value == Any:
                self.settings[key] = value
                continue
            if not isinstance(item[key], value):
                failed = True
                msg = f"{key} field not the correct type"
                self.raise_loud(TypeError, msg)
                break
            self.settings[key] = value
        return failed, msg
    
    def check_all(self, item:ADict):
        item = self.check_prev(item)
        
        if item.failed:
            return item
        failed, msg = self.check_item(item)
        if failed:
            item.failed = failed
            item.msg = msg

        return item
    
    def process(self, item:ADict):
        """Process component using procedure defined here. 

        Arguments:
            item {ADict} -- A modified dictionary with the results inputted in.
        """
        return item


    def raise_loud(self, exc=Exception, msg="General Problem"):
        if self.settings.loud:
            msg = f"{msg}. Error at component {self.name} ... Pipeline: {self.within_pipeline}"
            raise exc(msg)

    def step(self, item:ADict, **kwargs):
        self.settings.loud=kwargs.pop("is_loud", True)
        self.settings.override=kwargs.pop("override", False)
        failed, msg = self.set_settings(**kwargs)
        

        if failed:
            item.failed = failed
            item.msg = msg
            self.raise_loud(Exception, item.msg)

        # self.settings.loud = kwargs.get("is_loud", False)
        item = self.check_all(item)
        if item.failed:
            self.raise_loud(Exception, item.msg)
            return item
        processed = self.process(item)
        return processed

if __name__ == "__main__":
    comp = AddictComponent()
    sample_param = ADict(episode=uuid.uuid4().hex)
    print(comp.step(sample_param, asset=uuid.uuid4().hex))