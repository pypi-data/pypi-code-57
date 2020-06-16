from base64 import b64encode, b64decode
from simplejson import dumps, loads, dump
from yaml import safe_dump
from time import time, sleep
from logging import getLogger
from re import findall
from logging.config import fileConfig
from logging.handlers import MemoryHandler
from os import remove
from wthings_gateway.gateway.wt_client import TBClient
from wthings_gateway.gateway.wt_logger import TBLoggerHandler
from wthings_gateway.wt_utility.wt_utility import TBUtility
import traceback

log = getLogger("service")


class RemoteConfigurator:
    def __init__(self, gateway, config):
        self.__gateway = gateway
        self.__new_configuration = None
        self.__old_configuration = None
        self.__apply_timeout = 10
        self.__old_tb_client = None
        self.__old_logs_configuration = self.__get_current_logs_configuration()
        self.__new_logs_configuration = None
        self.__old_connectors_configs = {}
        self.__new_connectors_configs = {}
        self.__old_general_configuration_file = config
        self.__new_general_configuration_file = {}
        self.__old_event_storage = None
        self.__new_event_storage = None
        self.in_process = False

    def process_extend(self, configuration):
        # 最新代码
        # 适配现有服务器网关扩展
        conf = {"wthings": self.__old_general_configuration_file}
        conf["wthings"]["logs"] = b64encode(self.__old_logs_configuration.replace('\n', '}}').encode("UTF-8"))
        # conf = {"wthings": {
        #     "wthings": {
        #         "host": "things.xiaobodata.com",
        #         "port": 1883,
        #         "remoteConfiguration": True,
        #         "security": {
        #             "accessToken": "rknoNpDksmYbMeIt0PRN"
        #         }
        #     },
        #     "storage": {
        #         "type": "memory",
        #         "read_records_count": 100,
        #         "max_records_count": 100000
        #     },
        #     "logs": "W2xvZ2dlcnNdfX1rZXlzPXJvb3QsIHNlcnZpY2UsIGNvbm5lY3RvciwgY29udmVydGVyLCB0Yl9jb25uZWN0aW9uLCBzdG9yYWdlLCBleHRlbnNpb259fVtoYW5kbGVyc119fWtleXM9Y29uc29sZUhhbmRsZXIsIHNlcnZpY2VIYW5kbGVyLCBjb25uZWN0b3JIYW5kbGVyLCBjb252ZXJ0ZXJIYW5kbGVyLCB0Yl9jb25uZWN0aW9uSGFuZGxlciwgc3RvcmFnZUhhbmRsZXIsIGV4dGVuc2lvbkhhbmRsZXJ9fVtmb3JtYXR0ZXJzXX19a2V5cz1Mb2dGb3JtYXR0ZXJ9fVtsb2dnZXJfcm9vdF19fWxldmVsPUVSUk9SfX1oYW5kbGVycz1jb25zb2xlSGFuZGxlcn19W2xvZ2dlcl9jb25uZWN0b3JdfX1sZXZlbD1JTkZPfX1oYW5kbGVycz1jb25uZWN0b3JIYW5kbGVyfX1mb3JtYXR0ZXI9TG9nRm9ybWF0dGVyfX1xdWFsbmFtZT1jb25uZWN0b3J9fVtsb2dnZXJfc3RvcmFnZV19fWxldmVsPUlORk99fWhhbmRsZXJzPXN0b3JhZ2VIYW5kbGVyfX1mb3JtYXR0ZXI9TG9nRm9ybWF0dGVyfX1xdWFsbmFtZT1zdG9yYWdlfX1bbG9nZ2VyX3RiX2Nvbm5lY3Rpb25dfX1sZXZlbD1JTkZPfX1oYW5kbGVycz10Yl9jb25uZWN0aW9uSGFuZGxlcn19Zm9ybWF0dGVyPUxvZ0Zvcm1hdHRlcn19cXVhbG5hbWU9dGJfY29ubmVjdGlvbn19W2xvZ2dlcl9zZXJ2aWNlXX19bGV2ZWw9SU5GT319aGFuZGxlcnM9c2VydmljZUhhbmRsZXJ9fWZvcm1hdHRlcj1Mb2dGb3JtYXR0ZXJ9fXF1YWxuYW1lPXNlcnZpY2V9fVtsb2dnZXJfY29udmVydGVyXX19bGV2ZWw9SU5GT319aGFuZGxlcnM9Y29ubmVjdG9ySGFuZGxlcn19Zm9ybWF0dGVyPUxvZ0Zvcm1hdHRlcn19cXVhbG5hbWU9Y29udmVydGVyfX1bbG9nZ2VyX2V4dGVuc2lvbl19fWxldmVsPUlORk99fWhhbmRsZXJzPWNvbm5lY3RvckhhbmRsZXJ9fWZvcm1hdHRlcj1Mb2dGb3JtYXR0ZXJ9fXF1YWxuYW1lPWV4dGVuc2lvbn19W2hhbmRsZXJfY29uc29sZUhhbmRsZXJdfX1jbGFzcz1TdHJlYW1IYW5kbGVyfX1sZXZlbD1JTkZPfX1mb3JtYXR0ZXI9TG9nRm9ybWF0dGVyfX1hcmdzPShzeXMuc3Rkb3V0LCl9fVtoYW5kbGVyX2Nvbm5lY3RvckhhbmRsZXJdfX1sZXZlbD1JTkZPfX1jbGFzcz1sb2dnaW5nLmhhbmRsZXJzLlRpbWVkUm90YXRpbmdGaWxlSGFuZGxlcn19Zm9ybWF0dGVyPUxvZ0Zvcm1hdHRlcn19YXJncz0oIi4vbG9ncy9jb25uZWN0b3IubG9nIiwgImQiLCAxLCA3LCl9fVtoYW5kbGVyX3N0b3JhZ2VIYW5kbGVyXX19bGV2ZWw9SU5GT319Y2xhc3M9bG9nZ2luZy5oYW5kbGVycy5UaW1lZFJvdGF0aW5nRmlsZUhhbmRsZXJ9fWZvcm1hdHRlcj1Mb2dGb3JtYXR0ZXJ9fWFyZ3M9KCIuL2xvZ3Mvc3RvcmFnZS5sb2ciLCAiZCIsIDEsIDcsKX19W2hhbmRsZXJfc2VydmljZUhhbmRsZXJdfX1sZXZlbD1JTkZPfX1jbGFzcz1sb2dnaW5nLmhhbmRsZXJzLlRpbWVkUm90YXRpbmdGaWxlSGFuZGxlcn19Zm9ybWF0dGVyPUxvZ0Zvcm1hdHRlcn19YXJncz0oIi4vbG9ncy9zZXJ2aWNlLmxvZyIsICJkIiwgMSwgNywpfX1baGFuZGxlcl9jb252ZXJ0ZXJIYW5kbGVyXX19bGV2ZWw9SU5GT319Y2xhc3M9bG9nZ2luZy5oYW5kbGVycy5UaW1lZFJvdGF0aW5nRmlsZUhhbmRsZXJ9fWZvcm1hdHRlcj1Mb2dGb3JtYXR0ZXJ9fWFyZ3M9KCIuL2xvZ3MvY29udmVydGVyLmxvZyIsICJkIiwgMSwgMywpfX1baGFuZGxlcl9leHRlbnNpb25IYW5kbGVyXX19bGV2ZWw9SU5GT319Y2xhc3M9bG9nZ2luZy5oYW5kbGVycy5UaW1lZFJvdGF0aW5nRmlsZUhhbmRsZXJ9fWZvcm1hdHRlcj1Mb2dGb3JtYXR0ZXJ9fWFyZ3M9KCIuL2xvZ3MvZXh0ZW5zaW9uLmxvZyIsICJkIiwgMSwgMywpfX1baGFuZGxlcl90Yl9jb25uZWN0aW9uSGFuZGxlcl19fWxldmVsPUlORk99fWNsYXNzPWxvZ2dpbmcuaGFuZGxlcnMuVGltZWRSb3RhdGluZ0ZpbGVIYW5kbGVyfX1mb3JtYXR0ZXI9TG9nRm9ybWF0dGVyfX1hcmdzPSgiLi9sb2dzL3RiX2Nvbm5lY3Rpb24ubG9nIiwgImQiLCAxLCAzLCl9fVtmb3JtYXR0ZXJfTG9nRm9ybWF0dGVyXX19Zm9ybWF0PSIlKGFzY3RpbWUpcyAtICUobGV2ZWxuYW1lKXMgLSBbJShmaWxlbmFtZSlzXSAtICUobW9kdWxlKXMgLSAlKGxpbmVubylkIC0gJShtZXNzYWdlKXMiIH19ZGF0ZWZtdD0iJVktJW0tJWQgJUg6JU06JVMifX19fX19fX19fX19fX19fX19"
        # }}
        configuration = loads(configuration)
        # configuration = [
        #     {
        #         "type": "OPC DA",
        #         "configuration": {
        #             "servers": [
        #                 {
        #                     "applicationName": "OPC-DA client",
        #                     "applicationOpcServer": "Matrikon.OPC.Simulation",
        #                     "host": "localhost",
        #                     "port": 7766,
        #                     "scanPeriodInSeconds": 10,
        #                     "timeoutInMillis": 5000,
        #                     "mapping": [
        #                         {
        #                             "deviceName": "TEST",
        #                             "devicePath": "Random",
        #                             "attributes": [
        #                                 {
        #                                     "key": "Tag1",
        #                                     "type": "string",
        #                                     "value": "Int4"
        #                                 }
        #                             ],
        #                             "timeseries": []
        #                         }
        #                     ]
        #                 }
        #             ]
        #         },
        #         "id": "TEST"
        #     }
        # ]
        opcuas = []
        modbus = []
        opcdas = []
        connectors = []
        for i, v in enumerate(configuration):
            if v["type"] == "OPC UA":
                for n, m in enumerate(v["configuration"]["servers"]):
                    url = "admin@%s:%s%s" % (m["host"], m["port"], m["applicationUri"])
                    applicationName = m["applicationName"]
                    opcuas.append({
                        "name": applicationName,
                        "config": {
                            "server": {
                                "name": applicationName,
                                "url": url,
                                "scanPeriodInMillis": m["scanPeriodInSeconds"] * 1000,
                                "timeoutInMillis": m["timeoutInMillis"],
                                "security": "Basic128Rsa15",
                                "showMap": False,
                                "identity": {
                                    "type": "anonymous"
                                },
                                "mapping": self.format_mapping(m["mapping"])
                            },
                            "name": applicationName
                        }
                    })
                    connectors.append({
                        "name": applicationName,
                        "type": "opcua",
                        "configuration": "%s.json" % (applicationName, )
                    })
            if v["type"] == "MODBUS":
                for n, m in enumerate(v["configuration"]["servers"]):
                    type = "serial" if m["transport"]["type"] == "rtu" else m["transport"]["type"]
                    name = "modbus_serial_%s" % (n+1,)
                    modbus.append({
                        "name": name,
                        "config": {
                            "server": {
                                "name": "Modbus Default Server",
                                "type": type,
                                "method": m["transport"]["encoding"],
                                "port": m["transport"]["portName"],
                                "baudrate": m["transport"]["baudRate"],
                                "timeout": m["transport"]["timeout"]/1000,
                                "devices": m["devices"]
                            },
                            "name": name
                        }
                    })
                    connectors.append({
                        "name": name,
                        "type": "modbus",
                        "configuration": name+".json"
                    })
            if v["type"] == "OPC DA":
                for n, m in enumerate(v["configuration"]["servers"]):
                    applicationName = m["applicationName"]
                    opcdas.append({
                        "name": applicationName,
                        "config": {
                            "server": {
                                "serverId": n+1,
                                "opcProxyIp": m["host"],
                                "opcProxyPort": m["port"],
                                "opcServer": m["applicationOpcServer"],
                                "collectInterval": m["scanPeriodInSeconds"],
                                "timeout": m["timeoutInMillis"],  #
                                "devices": self.format_mapping(m["mapping"], n+1)
                            },
                            "name": applicationName,
                        }
                    })
                    connectors.append({
                        "name": applicationName,
                        "type": "opcda",
                        "configuration": "%s.json" % (applicationName, )
                    })
        conf["opcua"] = opcuas
        conf["modbus"] = modbus
        conf["opcda"] = opcdas
        conf["wthings"]["connectors"] = connectors
        return conf


    def process_configuration(self, configuration):
        try:
            if not self.in_process:
                self.in_process = True
                # while not self.__gateway._published_events.empty():
                #     log.debug("Waiting for end of the data processing...")
                #     sleep(1)
                # configuration = b64encode(configuration.encode('utf-8'))
                try:
                    decoded_configuration = b64decode(configuration)
                    log.info("process_configuration b64decode")
                    self.__new_configuration = loads(decoded_configuration)
                except Exception  as e:
                    conf = self.process_extend(configuration)
                    log.info("process_configuration extend")
                    self.__new_configuration = conf
                    decoded_configuration = dumps(conf)
                self.__old_connectors_configs = self.__gateway.connectors_configs
                self.__new_general_configuration_file = self.__new_configuration.get("wthings")
                self.__new_logs_configuration = b64decode(self.__new_general_configuration_file.pop("logs")).decode('UTF-8').replace('}}', '\n')
                if self.__old_configuration != decoded_configuration:
                    log.info("Remote configuration received: \n %s", decoded_configuration)
                    result = self.__process_connectors_configuration()
                    self.in_process = False
                    if result:
                        self.__old_configuration = self.__new_configuration
                        return True
                    else:
                        return False
                else:
                    log.info("Remote configuration is the same.")
            else:
                log.error("Remote configuration is already in processing")
                return False
        except Exception as e:
            self.in_process = False
            log.exception(e)

    @staticmethod
    def format_mapping(mapping, n=None):
        for i, v in enumerate(mapping):
            if n:
                v["serverId"] = n
            # 遍历mapping，获取每个设备属性映射
            device_attributes = v["attributes"]
            device_timeseries = v["timeseries"]
            for n, m in enumerate(device_attributes):
                if "type" in m:
                    m.pop("type")
                    m["path"] = m.pop("value")
            for n, m in enumerate(device_timeseries):
                if "type" in m:
                    m.pop("type")
                    m["path"] = m.pop("value")
        return mapping

    def send_current_configuration(self):
        try:
            current_configuration = {}
            for connector in self.__gateway.connectors_configs:
                if current_configuration.get(connector) is None:
                    current_configuration[connector] = []
                for config in self.__gateway.connectors_configs[connector]:
                    for config_file in config['config']:
                        current_configuration[connector].append({'name': config['name'], 'config': config['config'][config_file]})
            current_configuration["wthings"] = self.__old_general_configuration_file
            current_configuration["wthings"]["logs"] = b64encode(self.__old_logs_configuration.replace('\n', '}}').encode("UTF-8"))
            json_current_configuration = dumps(current_configuration)
            encoded_current_configuration = b64encode(json_current_configuration.encode())
            self.__old_configuration = encoded_current_configuration
            self.__gateway.tb_client.client.send_attributes(
                {"current_configuration": encoded_current_configuration.decode("UTF-8")})
            log.info('Current configuration has been sent to WThings: %s', json_current_configuration)
        except Exception as e:
            log.exception(e)

    def __process_connectors_configuration(self):
        log.info("Processing remote connectors configuration...")
        if self.__apply_new_connectors_configuration():
            self.__write_new_configuration_files()
        self.__apply_storage_configuration()
        if self.__safe_apply_connection_configuration():
            log.info("Remote configuration has been applied.")
            with open(self.__gateway._config_dir + "wt_gateway.yaml", "w") as general_configuration_file:
                safe_dump(self.__new_general_configuration_file, general_configuration_file)
            self.__old_connectors_configs = {}
            self.__new_connectors_configs = {}
            self.__old_general_configuration_file = self.__new_general_configuration_file
            self.__old_logs_configuration = self.__new_logs_configuration
            self.__update_logs_configuration()
            self.__new_logs_configuration = None
            self.__new_general_configuration_file = {}
            return True
        else:
            self.__update_logs_configuration()
            self.__old_general_configuration_file.pop("logs")
            with open(self.__gateway._config_dir + "wt_gateway.yaml", "w") as general_configuration_file:
                safe_dump(self.__old_general_configuration_file, general_configuration_file)
            log.error("A remote general configuration applying has been failed.")
            self.__old_connectors_configs = {}
            self.__new_connectors_configs = {}
            self.__new_logs_configuration = None
            self.__new_general_configuration_file = {}
            return False

    def __prepare_connectors_configuration(self, input_connector_config):
        log.debug("input_connector_config=%s" % (input_connector_config))
        try:
            self.__gateway.connectors_configs = {}
            for connector in input_connector_config['wthings']['connectors']:
                for input_connector in input_connector_config[connector['type']]:
                    if input_connector['name'] == connector['name']:
                        if not self.__gateway.connectors_configs.get(connector['type']):
                            self.__gateway.connectors_configs[connector['type']] = []
                        self.__gateway.connectors_configs[connector['type']].append(
                            {"name": connector["name"], "config": {connector['configuration']: input_connector["config"]}})
                        connector_class = TBUtility.check_and_import(connector["type"], self.__gateway._default_connectors.get(connector["type"], connector.get("class")))
                        self.__gateway._implemented_connectors[connector["type"]] = connector_class
        except Exception as e:
            log.exception(e)

    def __apply_new_connectors_configuration(self):
        try:
            self.__prepare_connectors_configuration(self.__new_configuration)
            for connector_name in self.__gateway.available_connectors:
                try:
                    self.__gateway.available_connectors[connector_name].close()
                except Exception as e:
                    log.exception(e)
            self.__gateway._connect_with_connectors()
            log.debug("New connectors configuration has been applied")
            self.__old_connectors_configs = {}
            return True
        except Exception as e:
            self.__gateway.connectors_configs = self.__old_connectors_configs
            for connector_name in self.__gateway.available_connectors:
                self.__gateway.available_connectors[connector_name].close()
            self.__gateway._load_connectors(self.__old_general_configuration_file)
            self.__gateway._connect_with_connectors()
            log.exception(e)
            return False

    def __write_new_configuration_files(self):
        try:
            self.__new_connectors_configs = self.__new_connectors_configs if self.__new_connectors_configs else self.__gateway.connectors_configs
            new_connectors_files = []
            for connector_type in self.__new_connectors_configs:
                for connector_config_section in self.__new_connectors_configs[connector_type]:
                    for connector_file in connector_config_section["config"]:
                        connector_config = connector_config_section["config"][connector_file]
                        with open(self.__gateway._config_dir + connector_file, "w") as config_file:
                            dump(connector_config, config_file, sort_keys=True, indent=2)
                        new_connectors_files.append(connector_file)
                        log.debug("Saving new configuration for \"%s\" connector to file \"%s\"", connector_type,
                                  connector_file)
                        break
            self.__old_general_configuration_file["connectors"] = self.__new_general_configuration_file["connectors"]
            for old_connector_type in self.__old_connectors_configs:
                for old_connector_config_section in self.__old_connectors_configs[old_connector_type]:
                    for old_connector_file in old_connector_config_section["config"]:
                        if old_connector_file not in new_connectors_files:
                            remove(self.__gateway._config_dir + old_connector_file)
                        log.debug("Remove old configuration file \"%s\" for \"%s\" connector ", old_connector_file,
                                  old_connector_type)
        except Exception as e:
            log.exception(e)

    def __safe_apply_connection_configuration(self):
        apply_start = time() * 1000
        self.__old_tb_client = self.__gateway.tb_client
        try:
            self.__old_tb_client.unsubscribe('*')
            self.__old_tb_client.stop()
            self.__old_tb_client.disconnect()
            self.__gateway.tb_client = TBClient(self.__new_general_configuration_file["wthings"])
            self.__gateway.tb_client.connect()
            log.debug("__safe_apply_connection_configuration tb_client connected")
            connection_state = False
            while time() * 1000 - apply_start < self.__apply_timeout * 1000 and not connection_state:
                connection_state = self.__gateway.tb_client.is_connected()
                sleep(.1)
            if not connection_state:
                self.__revert_configuration()
                log.info("The gateway cannot connect to the WThings server with a new configuration.")
                return False
            else:
                self.__old_tb_client.stop()
                self.__gateway.subscribe_to_required_topics()
                return True
        except Exception as e:
            log.exception(e)
            self.__revert_configuration()
            return False

    def __apply_storage_configuration(self):
        if self.__old_general_configuration_file["storage"] != self.__new_general_configuration_file["storage"]:
            self.__old_event_storage = self.__gateway._event_storage
            try:
                self.__gateway._event_storage = self.__gateway._event_storage_types[
                    self.__new_general_configuration_file["storage"]["type"]](
                    self.__new_general_configuration_file["storage"])
                self.__old_event_storage = None
            except Exception as e:
                log.exception(e)
                self.__gateway._event_storage = self.__old_event_storage

    def __revert_configuration(self):
        try:
            log.info("Remote general configuration will be restored.")
            self.__new_general_configuration_file = self.__old_general_configuration_file
            self.__gateway.tb_client.disconnect()
            self.__gateway.tb_client.stop()
            self.__gateway.tb_client = TBClient(self.__old_general_configuration_file["wthings"])
            self.__gateway.tb_client.connect()
            self.__gateway.subscribe_to_required_topics()
            log.debug("%s connection has been restored", str(self.__gateway.tb_client.client._client))
        except Exception as e:
            log.exception("Exception on reverting configuration occurred:")
            log.exception(e)

    def __get_current_logs_configuration(self):
        try:
            with open(self.__gateway._config_dir + 'logs.conf', 'r') as logs:
                current_logs_configuration = logs.read()
            return current_logs_configuration
        except Exception as e:
            log.exception(e)

    def __update_logs_configuration(self):
        try:
            # if self.__old_logs_configuration != self.__new_logs_configuration:
            # global log
            # log = getLogger('service')
            remote_handler_current_state = self.__gateway.remote_handler.activated
            remote_handler_current_level = self.__gateway.remote_handler.current_log_level
            logs_conf_file_path = self.__gateway._config_dir + 'logs.conf'
            new_logging_level = findall(r'level=(.*)', self.__new_logs_configuration.replace("NONE", "NOTSET"))[-1]
            log.debug("__update_logs_configuration new_logging_level=%s" % (new_logging_level))
            with open(logs_conf_file_path, 'w') as logs:
                logs.write(self.__new_logs_configuration.replace("NONE", "NOTSET")+"\r\n")
            # fileConfig(logs_conf_file_path)
            # self.__gateway.main_handler = MemoryHandler(-1)
            self.__gateway.main_handler.setLevel(new_logging_level)
            # self.__gateway.remote_handler = TBLoggerHandler(self.__gateway)
            self.__gateway.main_handler.setTarget(self.__gateway.remote_handler)
            if new_logging_level == "NOTSET":
                self.__gateway.remote_handler.deactivate()
            else:
                self.__gateway.remote_handler.activate(new_logging_level)
            log.debug("Logs configuration has been updated.")
        except Exception as e:
            log.exception(e)

