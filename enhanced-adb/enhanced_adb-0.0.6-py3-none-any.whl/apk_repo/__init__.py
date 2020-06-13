import re

from smb.SMBConnection import SMBConnection
from .. import UserConfig


def connect_to_driver():
    cfg = UserConfig()

    userID = cfg.get('smb_user_ID')
    password = cfg.get('smb_password')
    client_machine_name = cfg.get('smb_client_machine_name')
    server_name = cfg.get('smb_server_name')
    server_ip = cfg.get('smb_server_ip')
    domain_name = cfg.get('smb_domain_name')
    driver = cfg.get('repo_driver')

    conn = SMBConnection(userID, password, client_machine_name, server_name, domain=domain_name, use_ntlm_v2=True,
                         is_direct_tcp=True)

    conn.connect(server_ip, 445)
    shares = conn.listShares()

    driver = next((x for x in shares if x.name == driver), None)

    return conn, driver.name


def recurse_find_file(conn, driver_name, root, re=None):
    lists = conn.listPath(driver_name, root)
    result = []
    for item in lists:
        if item.filename in ['.', '..']:
            continue
        if item.isDirectory:
            result += recurse_find_file(conn, driver_name, root + "/" + item.filename, re)
        else:
            if re:
                if re.match(re, item.filename):
                    result.append((root, item.filename))
            else:
                result.append((root, item.filename))

    return result


class Version:
    re_version = re.compile(r"(\d+).(\d+).(\d+)")

    def __init__(self, major, minor, patch):
        self._major = major
        self._minor = minor
        self._patch = patch

    def __str__(self):
        return "{}.{}.{}".format(self._major, self._minor, self._patch)

    @staticmethod
    def get_version(text):
        r = Version.re_version.search(text)
        if r:
            g = r.groups()
            return Version(g[0], g[1], g[2])
        else:
            return Version(-1, -1, -1)
