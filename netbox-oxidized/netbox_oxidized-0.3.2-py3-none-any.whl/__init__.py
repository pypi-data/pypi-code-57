from extras.plugins import PluginConfig

class NetboxOxidizedConfig(PluginConfig):
    name = 'netbox_oxidized'
    verbose_name = "Netbox Oxidized"
    description = "Netbox Oxidized Integration Plugin"
    version = '0.3.2'
    author = 'Paul Denning'
    base_url = 'netbox-oxidized'
    required_settings = []
    default_settings = {'oxidized_url': ''}

config = NetboxOxidizedConfig