
import sys
import os

sys.path.append(os.path.dirname(__file__))
import context
import framework

def main(config):
    #print('config:', config)
    plcontext = context.context()
    pl = framework.framework()
    dirs = [os.path.dirname(__file__) + "\\plugins"]

    plugin_dir = None
    if type(config) == type(''):
        plugin_dir = config
    elif type(config) == type({}):
        if 'plugin_dirs' in config:
            for pdir in config['plugin_dirs']:
                dirs.append(pdir)

    if plugin_dir != None and plugin_dir != '':
        dirs.append(plugin_dir)
    
    pl.load(plcontext, dirs)

    # 配置默认的根数据节点类型
    if 'DataNodeRegService::RootNodeKind' in config:
        #print('config DataNodeRegService::RootNodeKind:', config['DataNodeRegService::RootNodeKind'])
        datanode_service = plcontext.find_service('DataNodeRegService')
        #datanode_service.config('TestProject')
        datanode_service.config(config['DataNodeRegService::RootNodeKind'])

    # 配置默认的DataService
    if 'DataService::DefaultService' in config:
        #print('config DataService::DefaultService:', config['DataService::DefaultService'])
        data_service = plcontext.find_service('DataService')
        #data_service.config('Core::DataService::Config::XML')
        #data_service.config('Core::DataService::Config::REG')
        data_service.config(config['DataService::DefaultService'])

    # 扩展黑名单
    # 通过扩展黑名单禁止部分扩展
    if 'Extension::BackList' in config:
        plcontext.filter_extension(config['Extension::BackList'])

    apps = plcontext.find_extension("PL::APP")
    app = None
    
    for a in apps:
        if a.name() == "MyApp":
            app = a
            break
    if app == None:
        print("PL::APP not match!")
    else:
        app.run(sys.argv)

#print(sys.argv)
#main()