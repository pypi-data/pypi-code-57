#!/usr/bin/env python
"""
Name: Rio Atmadja
Date: 02 April 2020
Description: This class extends the functionality in Server manager.
             And will manage docker instances.
"""
from server_managers.server_managers import ServerManager
from typing import List, Dict
from botocore.exceptions import ClientError

class DockerManagers(ServerManager):

    def install_docker_ce_ubuntu(self) -> List[str]:
        """
        This function will install docker community edition to the remote ubuntu server
        :return: output from installastion
        """

        # Check OS Version
        os_version = self.detect_os()
        if os_version != 'debian':
            raise EnvironmentError("ERROR: Remote Operation System is not Ubuntu")

        commands = ['apt-get install -y apt-transport-https ca-certificates  curl software-properties-common',
                    'curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - ',
                    'apt-key fingerprint 0EBFCD88',
                    'add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"',
                    'apt-get install docker-ce -y'
                    ]

        try:
            # run the command in batch
            print("[+] Succefully installing  Docker-CE")
            response: List = []
            for cmd in commands:
                response.extend(self.conn.sudo(cmd).stdout.strip().split('\n'))

            return response

        except ClientError as e:
            raise ClientError("ERROR: Unable to install DOCKER-CE ", "X")

    def check_docker_installation(self) -> bool:
        """
        This function will check, if docker has been installed on the remote server.
        :return:
        """

        os_name: str = self.detect_os()
        if os_name == 'debian':
            return len(self.run_cmd("dpkg -l | grep -o docker")) > 0

        if os_name == 'redhat':
            return len(self.run_cmd("rpm -qa | grep -o docker")) > 0

    def deploy_hadoop(self):
        """
        This function will deploy hadoop to ec2 containers.
        NOTE: This function will be implemented in the future versions.
        :return:
        """
        return NotImplemented("This functionality will be implemented in the future version. ")
