import ruamel.yaml
import json
import requests
import glom
from gooey import GooeyParser

API_KEY = "a-yjvfd3-ga2dfjzhv2"
API_TOKEN = "IK3uZDsrV?4vPv)lJ*"

API_KEY = "a-yjvfd3-wgf0kiimqj"
API_TOKEN = "aH_GXHbRI9pmUKDHOm"

ORG_ID = "yjvfd3"
BASE_URL = "https://{org_id}.internetofthings.ibmcloud.com/api/v0002".format(org_id=ORG_ID)

device_type_template = """{
    "id": "",
    "description": "",
    "classId": "",
    "deviceInfo": {
        "serialNumber": "",
    },
    "metadata": {}
}"""


def load_config(config):
    with open(config) as f:
        return ruamel.yaml.safe_load(f)


def main():
    parser = GooeyParser(description="Update server configuration from deployment config")
    parser.add_argument('-c', '--config', widget="FileChooser",
                        help="Configuration file to load device data from")
    parser.add_argument('-p', '--prod',
                        help="Deploy to production database. Only do after confirming dry run without this mode")
    args = parser.parse_args()
    config_data = load_config(args.config)
    update_device_types(config_data)


# resp = requests.get(BASE_URL + "/mgmt/requests", auth=(API_KEY, API_TOKEN))
def create_device_type(device, class_id):
    """
    :param device:
    :param permission_type:
    :return:
    """
    device_type_template = {
        "id": device["device_type"],
        "description": "",
        "classId": class_id,
        "deviceInfo": {"serialNumber": ""},
        "metadata": {}}
    resp = requests.post(BASE_URL + '/device/types', json=device_type_template, auth=(API_KEY, API_TOKEN))
    resp.raise_for_status()


def update_device_types(config):
    resp = requests.get(BASE_URL + '/device/types', auth=(API_KEY, API_TOKEN))
    resp.raise_for_status()
    dev_types = {dev['id']: dev["classId"] for dev in resp.json()['results']}
    for device in config["devices"]:
        if device["device_type"] not in dev_types:
            # Create device type
            create_device_type(device, 'Device')
    if config["gateway"] not in dev_types:
        create_device_type(config["gateway"], 'Gateway')


if __name__ == "__main__":
    main()
