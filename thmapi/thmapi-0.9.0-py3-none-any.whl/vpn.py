from .util import *


class __THMVpn(object):
    def vpn_available_servers(self) -> dict:
        """
        Grabs the list of available VPN servers and the currently selected one

        :return: data
        """

        return http_get(self.session, '/vpn/get-available-vpns')
