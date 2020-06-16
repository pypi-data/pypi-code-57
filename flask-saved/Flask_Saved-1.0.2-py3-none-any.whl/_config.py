from flask import current_app

class ConfigItem:
        
    def __init__(self, name, default=None, required=False):
        self.name = name
        self.default = default
        self.required = required
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self.name not in instance.config and self.required:
            raise RuntimeError("missing config['%s'] in %r" %(self.name, instance))
        return instance.config.get(self.name)
    
    def __set__(self, instance, value):
        instance.config[self.name] = value
