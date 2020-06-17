
import app

config = {
    'plugin_dirs': [],
    'DataNodeRegService::RootNodeKind': 'TestProject',
    'DataService::DefaultService': 'Core::DataService::Config::REG',
    #'Extension::BackList': ["PL::Basic::Menu::OpenSave"]
}

app.main(config)