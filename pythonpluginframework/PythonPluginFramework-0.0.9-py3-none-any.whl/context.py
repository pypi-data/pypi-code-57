
class context:
    plugins = []
    extensions = {}
    services = {}
    subscribes = {}

    def add_plugin(self, plugin):
        self.plugins.append(plugin)
    def get_plugins(self):
        return self.plugins
    
    def add_extension(self, extype, ext):
        if not extype in self.extensions:
            self.extensions[extype] = []
        self.extensions[extype].append(ext)
    def find_extension(self, extype):
        if extype in self.extensions:
            return self.extensions[extype]
        else:
            return []
    
    def add_service(self, name, service):
        self.services[name] = service
    def find_service(self, name):
        if name in self.services:
            return self.services[name]
        else:
            return None

    def add_subscribe(self, name, callback):
        if not name in self.subscribes:
            self.subscribes[name] = []
        self.subscribes[name].append(callback)
    def remove_suscribe(self, name, callback):
        if name in self.subscribes:
            self.subscribes[name].remove(callback)
    def fire(self, name, value1 = None, value2 = None, value3 = None, value4 = None, value5 = None):
        if '*' in self.subscribes:
            for callback in self.subscribes['*']:
                if value2 == None:
                    callback(name, value1)
                elif value3 == None:
                    callback(name, value1, value2)
                elif value4 == None:
                    callback(name, value1, value2, value3)
                elif value5 == None:
                    callback(name, value1, value2, value3, value4)
                else:
                    callback(name, value1, value2, value3, value4, value5)
        if name in self.subscribes:
            for callback in self.subscribes[name]:
                if value2 == None:
                    callback(name, value1)
                elif value3 == None:
                    callback(name, value1, value2)
                elif value4 == None:
                    callback(name, value1, value2, value3)
                elif value5 == None:
                    callback(name, value1, value2, value3, value4)
                else:
                    callback(name, value1, value2, value3, value4, value5)

