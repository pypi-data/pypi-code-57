from datetime import datetime

from .locations import LocationModel


class ConnectModel:
    def __init__(self, data):
        self.game = "{}:{}".format(
            data["node"]["ip"],
            data["network"]["ports"]["game"]
        )
        self.gotv = "{}:{}".format(
            data["node"]["ip"],
            data["network"]["ports"]["gotv"]
        )


class MapModel:
    def __init__(self, data):
        self.group = data["group"]
        self.id = data["id"]
        self.name = data["name"]
        self.type = data["type"]


class VersionModel:
    def __init__(self, data):
        self.expiry = datetime.utcfromtimestamp(
            data["expiry"]
        )
        self.retrieved = datetime.utcfromtimestamp(
            data["retrieved"]
        )
        self.version = data["version"]


class NodeModel:
    def __init__(self, data):
        self.id = data["id"]
        self.ip = data["ip"]
        self.location = LocationModel(data["location"])
        self.version = VersionModel(data["version"])


class NetworkModel:
    def __init__(self, data):
        self.client = data["client"]
        self.game = data["game"]
        self.gotv = data["gotv"]
        self.rcon = data["rcon"]
        self.steam = data["steam"]


class EacModel:
    def __init__(self, data):
        self.enabled = data["enabled"]
        self.league_id = data["league_id"]
        self.api_key = data["api_key"]


class ServerModel:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.map = MapModel(data["map"])
        self.cost = data["cost"]
        self.created = datetime.utcfromtimestamp(
            data["created"]
        )
        self.node = NodeModel(data["node"])
        self.admins = data["admins"]
        self.charge_period = data["charge_period"]
        self.first_config = data["first_config"]
        self.game_mode = data["game_mode"]
        self.game_type = data["game_type"]
        self.git_url = data["git_url"]
        self.zip_url = data["zip_url"]
        self.hourly_rate = data["hourly_rate"]
        self.last_running = data["last_running"]
        self.maximum_rate = data["maximum_rate"]
        self.mods = data["mods"]
        self.owner = data["owner"]
        self.password = data["password"]
        self.password_value = data["password_value"]
        self.plugins = data["plugins"]
        self.rcon = data["rcon"]
        self.started = datetime.utcfromtimestamp(
            data["started"]
        )
        self.status = data["status"]
        self.tickrate = int(data["tickrate"])
        self.version = data["version"]
        self.ports = NetworkModel(data["network"]["ports"])
        self.disable_default_mods = data["disable_default_mods"]
        self.disable_default_plugins = data["disable_default_plugins"]
        self.eac = data["eac"]
        self.auto_destroy = data["auto_destroy"]
        self.branding = data["branding"]
        self.connect = ConnectModel(data)
