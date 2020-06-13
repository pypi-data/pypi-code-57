

import os
import importlib
import imp

plugins = []

class framework:
    def load(self, context, paths):
        global plugins

        for path in paths:
            for root, dirs, files in os.walk(path):
                for f in files:
                    #print('f:', f)
                    if f != "plugin.py":
                        continue
                    fm = os.path.join(root, f)
                    # TODO
                    # current is a simple process for load plugin

                    spec = importlib.util.spec_from_file_location('my_module', fm)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    plugin = module
                    plugins.append(plugin)
                    context.add_plugin(plugin)

                    #plugin = importlib.import_module(fm)

                    if 'extensions' in plugin.config:
                        for ex in plugin.config["extensions"]:
                            context.add_extension(ex['name'], ex['impl'])
                    if 'services' in plugin.config:
                        for ex in plugin.config["services"]:
                            context.add_service(ex['name'], ex['define'])
                    if 'subscribes' in plugin.config:
                        for ex in plugin.config["subscribes"]:
                            context.add_subscribe(ex['name'], ex['define'])
        
        for plugin in plugins:
            plugin.init(context)

def testf(a, b):
    print(a, b)
    return a+b

class CF:
    def test2(self, a, b):
        print("in test2:", a, b)
        return a*b

o1 = CF()

f1 = testf
f2 = o1.test2

print(f1(3,4))
print(f2(3,4))