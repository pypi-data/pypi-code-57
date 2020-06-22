"""
tlnetcard_python.system.administration.tcp_ip.tcp_ip
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a ``TcpIp`` object to provide the functionality of TLNET Supervisor -> System
-> Administration -> TCP/IP.
"""

# Standard library.
from typing import Any, Dict
# Required internal classes/functions.
from tlnetcard_python.login import Login

class TcpIp:
    """
    A TLNET Supervisor ``TcpIp`` object. Provides the functionality of the equivalent webpage
    TLNET Supervisor -> System -> Administration -> TCP/IP.

    Basic Usage:

    >>> from tlnetcard_python import Login
    >>> from tlnetcard_python.system.administration import TcpIp
    >>> # As always, a tlnetcard_python.Login object must first be created. Then the Login object
    >>> # can be passed to the tlnetcard_python.system.administration.TcpIp object.
    >>> card = Login(user="admin", passwd="password", host="10.0.0.100")
    >>> card_ip = TcpIp(card)
    >>> # Now that the TcpIp object has been created, functions belonging to the TcpIp class can
    >>> # be used. For example, enabling DHCP for IPv4 on the card:
    >>> card_ip.enable_ipv4_dhcp()
    """
    def __init__(self, login_object: Login) -> None:
        """
        Initializes the ``TcpIp`` object. Returns ``None``.

        :param login_object: A valid ``tlnetcard_python.Login`` object.
        :rtype: ``None``
        """
        self._login_object = login_object
        self._get_url = login_object.get_base_url() + "/en/adm_ipconfig.asp"
        self._post_url = login_object.get_base_url() + "/delta/adm_ipconfig"
    def disable_autonegotiation(self) -> None:
        """
        Disables link autonegotiation. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        ip_data = {
            "SYS_AUTONEG": "0"
        }

        # Uploading TCP/IP configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=ip_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def disable_ipv4_dhcp(self) -> None:
        """
        Disables DHCP for IPv4. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        ip_data = {
            "SYS_DHCP": "0"
        }

        # Uploading TCP/IP configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=ip_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def disable_ipv6_dhcp(self) -> None:
        """
        Disables DHCP for IPv6. Returns ``None``.

        :rtype: ``None``
        """
        ip_data = {
            "SYS_V6DHCP": "0"
        }

        # Uploading TCP/IP configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=ip_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def enable_autonetogiation(self) -> None:
        """
        Enables link speed negotiation. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        ip_data = {
            "SYS_AUTONEG": "1"
        }

        # Uploading TCP/IP configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=ip_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def enable_ipv4_dhcp(self) -> None:
        """
        Enables DHCP for IPv4. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        ip_data = {
            "SYS_DHCP": "1"
        }

        # Uploading TCP/IP configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=ip_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def enable_ipv6_dhcp(self) -> None:
        """
        Enables DHCP for IPv6. Returns ``None``.

        :rtype: ``None``
        """
        ip_data = {
            "SYS_V6DHCP": "1"
        }

        # Uploading TCP/IP configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=ip_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def get_ipv4_info(self) -> Dict[str, str]:
        """
        Returns info on how IPv4 is configured as a dictionary.

        :rtype: ``Dict[str, str]``
        """
        # Generating dictionary of items to search for and initializing out dictionary.
        pretty = {
            "Bootp": "DHCP Status",
            "IP": "IP Address",
            "Mask": "Subnet Mask",
            "Gateway": "Gateway IP",
            "DNS IP": "DNS IP",
            "Domain": "Search Domain"
        }
        out = {}

        # GETing system config.
        system_config = self._login_object.get_system_config()

        # Parsing list for required values.
        for line in system_config:
            if line in pretty:
                out[pretty[line]] = str(system_config[line])
        return out
    def get_ipv6_info(self) -> Dict[str, Any]:
        """
        Returns info on how IPv6 is configured as a dictionary.

        :rtype: ``Dict[str, str]``
        """
        # Generating dictionary of items to search for and initializing out dictionary.
        pretty = {
            "V6 DHCP": "DHCP Status",
            "V6 IP": "IP Address",
            "V6 Gateway": "Gateway IP",
            "V6 DNS": "DNS IP",
        }
        out = {}

        # GETing system config.
        system_config = self._login_object.get_system_config()

        # Parsing list for required values.
        for line in system_config:
            if line in pretty:
                out[pretty[line]] = str(system_config[line])
        out["Prefix Length"] = int(out["IP Address"].split("/")[1])
        out["IP Address"] = out["IP Address"].split("/")[0]
        return out
    def get_system_info(self) -> Dict[str, str]:
        """
        Returns info on the system and its location as a dictionary.

        :rtype: ``Dict[str, str]``
        """
        # Generating dictionary of items to search for and initializing out dictionary.
        pretty = {
            "Name": "Host Name",
            "Contact": "System Contact",
            "Location": "System Location"
        }
        out = {}

        # GETing system config.
        system_config = self._login_object.get_system_config()

        # Parsing list for required values.
        for line in system_config:
            if line in pretty:
                out[pretty[line]] = str(system_config[line])
        return out
    # pylint: disable=too-many-arguments
    def set_ipv4_info(self, ip_addr: str, mask: str = "255.255.255.0", gateway: str = "",
                      dns_ip: str = "", domain: str = "") -> None:
        """
        Sets info on how IPv4 is configured. Returns ``None``.

        :param ip_addr: The IPv4 address to be used.
        :param mask: (optional) The IPv4 subnet mask to be used.
        :param gateway: (optional) The IPv4 gateway to be used.
        :param dns_ip: (optional) The DNS server to be used.
        :param domain: (optional) The domain server to be used.
        :rtype: ``None``
        """
        # Generating payload.
        ip_data = {
            "SYS_DHCP": "0",
            "SYS_IP": ip_addr,
            "SYS_MASK": mask,
            "SYS_GATE": gateway,
            "SYS_DNS": dns_ip,
            "SYS_DOMAIN": domain
        }

        # Uploading TCP/IP configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=ip_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def set_ipv6_info(self, ip_addr: str, prefix_len: int = 64,
                      gateway: str = "::", dns_ip: str = "::") -> None:
        """
        Sets info on how IPv6 is configured. Returns ``None``.

        :param ip_addr: The IPv6 address to be used.
        :param prefix_len: The IPv6 prefix length to be used.
        :param gateway: The IPv6 gateway  to be used.
        :param dns_ip: The domain server to be used.
        :rtype: ``None``
        """
        # Generating payload.
        ip_data = {
            "SYS_V6DHCP": "0",
            "SYS_V6IP": ip_addr,
            "SYS_V6LEN": prefix_len,
            "SYS_V6GW": gateway,
            "SYS_V6DNS": dns_ip,
        }

        # Uploading TCP/IP configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=ip_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def set_system_info(self, name: str = "TLNET", contact: str = "", location: str = "") -> None:
        """
        Sets info on the system and its location. Returns ``None``.

        :param name: (optional) The system hostname to be used.
        :param contact: (optional) The system contact to be used.
        :param location: (optional) The system location to be used.
        :rtype: ``None``
        """
        # Generating payload.
        ip_data = {
            "SYS_NAM": name,
            "SYS_CON": contact,
            "SYS_LOC": location,
        }

        # Uploading TCP/IP configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=ip_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def use_10m_link_speed(self) -> None:
        """
        Sets the link speed to 10M. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        ip_data = {
            "SYS_SPEED": "0"
        }

        # Uploading TCP/IP configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=ip_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def use_100m_link_speed(self) -> None:
        """
        Sets the link speed to 100M. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        ip_data = {
            "SYS_SPEED": "1"
        }

        # Uploading TCP/IP configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=ip_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def use_full_duplex(self) -> None:
        """
        Sets the duplex for the link to full. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        ip_data = {
            "SYS_DUPLEX": "1"
        }

        # Uploading TCP/IP configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=ip_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def use_half_duplex(self) -> None:
        """
        Sets the duplex for the link to half. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        ip_data = {
            "SYS_DUPLEX": "0"
        }

        # Uploading TCP/IP configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=ip_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
