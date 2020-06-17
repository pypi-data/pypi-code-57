import subprocess
import tempfile
import xml.etree.ElementTree as ET

from ._model import Patch, Product


def _query_zypper():
    return subprocess.check_output([
        'zypper', '--xmlout', '--quiet', '--non-interactive', 'list-patches'
    ], universal_newlines=True)


def _parse_zypper(patches_xml):
    root = ET.fromstring(patches_xml)
    patches = root.iter('update')
    return [
        Patch(patch.attrib.get('category'), patch.attrib.get('severity'))
        for patch in patches
    ]


def get_applicable_patches():
    patches_xml = _query_zypper()
    return _parse_zypper(patches_xml)


def check_needs_reboot():
    result = subprocess.run(
        ['zypper', 'needs-rebooting'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode == 0:
        return False
    elif result.returncode == 102:
        return True
    else:
        return result.check_returncode()


def get_lifecycle_info():
    with tempfile.NamedTemporaryFile() as tmp:
        subprocess.check_call(
            ['zypper', 'lifecycle', '--save', tmp.name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            universal_newlines=True,
        )

        root = ET.fromstring(tmp.read())
        products = root.iter('product')
        return [
            Product(
                product.attrib.get('name'),
                int(product.attrib.get('eol')),
            ) for product in products
        ]


def get_services_needing_restart():
    return {
        line
        for line in subprocess.check_output([
            'zypper', 'ps', '-sss'
        ], universal_newlines=True).splitlines()
        if line  # kill empty lines (e.g. the tailing new-line)
    }
