#!/usr/bin/env python
"""
Name: Rio Atmadja
Date: 04 April 2020
Descriptions: This is utility tools to manage firewalld in the following Linux distributions:
              - Redhat/Centos
              - Debian/Ubuntu
"""
from server_managers.server_managers import ServerManager
from typing import List
import logging

LOG = logging.getLogger(__name__)

class FirewallManagers(ServerManager):

    def __init__(self, ip: str = "", port: str = "", service: str = "", ipset: str = "", protocol: str = "", family: str = "", zone: str = "public", rich_rule: str = "", description: str = "", *args, **kwargs):

        self.ip: str = ip
        self.port: str = port
        self.service: str = service
        self.ipset: str = ipset
        self.protocol: str = protocol
        self.family: str = family
        self.zone: str = zone
        self.description: str = description
        self.rich_rule: str = rich_rule
        super(FirewallManagers, self).__init__(*args, **kwargs)

    def create_ipset(self) -> List[str]:
        """
        This function will create an ipset rules on the remote server
        :return:
        """
        if not self.is_root():
            raise PermissionError("You must be a root to run this command.")

        ipset_rule: str = f"""
        firewall-cmd --permanent --new-ipset={self.ipset} --type hash:ip;
        firewall-cmd --permanent --ipset={self.ipset} --add-entry={self.ip};
        firewall-cmd --permanent --zone={self.zone}  --add-source=ipset:{self.ipset};
        firewall-cmd --reload ;
        """
        LOG.info(f"\033[46m DATA: {ipset_rule} \033[0m")

        return self.run_cmd(ipset_rule)

    def delete_ipset(self) -> List[str]:
        """
        This function will delete the given ipset rule
        :return:
        """
        if not self.is_root():
            raise PermissionError("You must be a root to run this command.")

        ipset_rule: str = f"""
        firewall-cmd --permanent --delete-ipset={self.ipset};
        firewall-cmd --reload;
        """
        LOG.info(f"\033[46m DATA: {ipset_rule} \033[0m")
        return self.run_cmd(ipset_rule)

    def get_ipset(self) -> List[str]:
        """
        This function will retrieve the given ipset rule
        :return:
        """
        if not self.is_root():
            raise PermissionError("You must be a root to run this command.")

        ipset_rule: str = f"""
        firewall-cmd --ipset={self.ipset} --get-entries;
        """
        LOG.info(f"\033[46m IPSET: {ipset_rule} \033[0m")
        return self.run_cmd(ipset_rule.strip())

    def create_service(self) -> List[str]:
        """
        This function will create a custom firewalld service on remote machine
        :return:
        """
        if not self.is_root():
            raise PermissionError("You must be a root to run this command.")

        firewall_service: str = f"""
        firewall-cmd --permanent --new-service={self.service};
        firewall-cmd --permanent --service={self.service} --set-description={self.description}; 
        firewall-cmd --permanent --service={self.service} --add-port={self.port}/{self.protocol}; 
        firewall-cmd --permanent --add-service={self.service}; 
        firewall-cmd --reload;
        """
        LOG.info(f"\033[46m [+] Service: {firewall_service} \033[0m")
        return self.run_cmd(firewall_service)

    def delete_service(self) -> List[str]:
        """
        This function will delete a given firewalld service on remote machine
        :return:
        """
        if not self.is_root():
            raise PermissionError("You must be a root to run this command.")

        firewall_service: str = f"""
        firewall-cmd --permanent --delete-service=;
        firewall-cmd --reload; 
        """
        return self.run_cmd(firewall_service)

    def create_rich_rules(self) -> List[str]:
        """
        This function will create firewall-cmd rule from a given rich-rule
        :return:
        """

        if not self.is_root():
            raise PermissionError("You must be a root to run this command.")

        rich_rule: str = f"""
        firewall-cmd --permanent --add-rich-rule={self.rich_rule};
        firewall-cmd --reload;
        """
        return self.run_cmd(rich_rule)

    def delete_rich_rules(self):
        """
        This function will delete firewall-cmd rule from a given rich-rule
        :return:
        """
        if not self.is_root():
            raise PermissionError("You must be a root to run this command.")

        rich_rule: str = f"""
        firewall-cmd --permanent --remove-rich-rule={self.rich_rule};
        firewall-cmd --reload;
        """
        return self.run_cmd(rich_rule)


