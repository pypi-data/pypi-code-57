
import app

config = {
    'plugin_dirs': [],
    'DataNodeRegService::RootNodeKind': 'TestProject',
    'DataService::DefaultService': 'Core::DataService::Config::REG'
}

app.main(config)