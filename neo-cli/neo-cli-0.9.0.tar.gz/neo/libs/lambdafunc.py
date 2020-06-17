import os
from neo.libs import utils, image, vm, network


def get_flavor():
    temp = utils.tmp_dir()
    flavor_file = os.path.join(temp, "flavor.yml")
    if os.path.exists(flavor_file):
        flavors = utils.yaml_parser(flavor_file)["data"]
    else:
        flavors = list(
            reversed(sorted([flavor.name for flavor in list(vm.get_flavor())]))
        )
        utils.yaml_create(flavor_file, {"data": flavors})
    return flavors


def get_img():
    temp = utils.tmp_dir()
    img_file = os.path.join(temp, "images.yml")
    if os.path.exists(img_file):
        imgs = utils.yaml_parser(img_file)["data"]
    else:
        imgs = list(reversed([img.name for img in list(image.get_list())]))
        utils.yaml_create(img_file, {"data": imgs})
    return imgs


def get_key():
    return [key.name for key in vm.get_keypairs()]


def get_network():
    return [
        net["name"] for net in network.get_list() if net["name"] != "Public_Network"
    ]
