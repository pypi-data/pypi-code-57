#!/usr/bin/env python 
"""
Name: Rio Atmadja 
Date: 02 April 2020 
Description: This class is a wrapper for fabric class
"""
from fabric import Connection
from botocore.exceptions import ClientError 
from typing import Dict, List
from utils.connection_tools import check_connection
from utils.file_and_directory_tools import check_path, get_abs_path, obfuscate_file, validate_file_extension
import os

class ServerManager(object):

    def __init__(self, user: str, host: str, port: int = 22, cmd: str = None, connect_kwargs: Dict = None):
        """
        The followin parameters must be supplied.
        :param user: required
        :param host: required
        :param port: optional
        :param cmd: optional
        :param connect_kwargs: optional
        """
        if not user and host:
            raise ClientError("user and host are required.")

        self.host: str = host
        self.user: str = user
        self.port: int = port
        self.cmd: str = cmd
        self.connect_kwargs: Dict = connect_kwargs
        self.conn: str = None

    def login(self):
        """
        This function will attempt to login to the remote server given the right credentials
        :return:
        """
        err_msg: str = f"Unable to connect to host {self.host}."
        self.conn = check_connection(connection=Connection(user=self.user, host=self.host, port=self.port, connect_kwargs=self.connect_kwargs), err_msg=err_msg)

    def get_previlege(self) -> List[str]:
        """
        This function will lookup current user privilege
        :return: the groups that the users associated with.
        """
        err_msg: str = f"Unable to connect to host {self.host}"
        return check_connection(connection=self.conn.run("groups").stdout.strip().split(" "), err_msg=err_msg)

    def detect_os(self) -> str:
        """
        This function will finger print the remote Operating System by checking the lsb-release for ubuntu/deb versions.
        and redhat-release for centos/redhat versions.
        :return: either debian or centos
        """
        # Check OS Version
        relases = [x for x in self.conn.run('ls -1 /etc/').stdout.strip().split('\n')]

        if 'redhat-release' in relases:
            return 'redhat'

        if 'lsb-release' in relases:
            return 'debian'

    def is_admin(self) -> bool:
        """
        This function will return True if the given user is in either group sudo,wheels
        :return: True if it's an admin
        """

        groups: List[str] = self.get_previlege()
        return list(filter(lambda groups: True if 'wheel' in groups or 'sudo' in groups or 'root' in groups else False, groups)).__len__()  != 0

    def is_root(self) -> bool:
        """
        This function will check if the current user is a root
        :return: True if the user is a root
        """
        return 'root' in self.run_cmd('whoami')

    def run_cmd(self, cmd: str) -> List[str]:
        """
        This function will execute arbitrary commands 
        :param cmd: given the command to be executed 
        :return : List of outputs from the server.
        """
        groups: List[str] = self.get_previlege()
        if 'wheels' in groups or 'sudo' in groups:
            return check_connection(connection=self.conn.sudo(cmd).stdout.strip().split("\n"), err_msg="Unable to connect to the servers")

        return check_connection(connection=self.conn.run(cmd).stdout.strip().split("\n"), err_msg="Unable to connect to the servers")


    def install(self, packages: List[str], os_name: str = 'ubuntu') -> List[str]:
        """
        This function will install, the given packages based on Operating System.
        The default Operating System is Ubuntu 
        :param os_name: given the linux operating system name, default is Ubuntu
        :param packages: given a list of packages to be installed in the remote servers 
        :return : List of outputs from the server.
        """
        if os_name: 
             self.cmd = f"apt-get update && apt-get install -y {' '.join(packages)}"
                
        else: 
            if not self.conn.execute_cmd("ls -1 /etc | grep redhat"):
                raise ClientError(f"Unable to determine the host server.") 
                
            self.cmd = f"yum update -y && yum install -y {' '.join(packages)}"
                
        err_msg: str = f"Unable to install packages {', '.join(packages)}"
        return check_connection(connection=self.conn.sudo(self.cmd).stdout.strip().split("\n"), err_msg=err_msg)


    def upload(self, local_file: str, remote_file: str, ext:str) -> bool:
        """
        This function will upload local file from app to remote server
        :param local_file: Given the local file
        :param remote_file: Given the remote file
        :return: True if successful
        """

        check_path(local_file, ext)
        obfuscated: str = obfuscate_file(local_file)
        err_msg: str = f"ERROR: Unable to upload LOCAL FILE {local_file} to REMOTE {remote_file}"
        check_connection(connection=self.conn.put(obfuscated, remote_file), err_msg=err_msg)

        return True


    def download(self, remote_file: str, local_file: str = "" ) -> bool:
        """
        This function will download file from remote server
        :param remote_file: The given remote file
        :return: True if it's successful
        """

        err_msg: str = f"ERROR: Unable to download file: {remote_file}"
        check_connection(connection=self.conn.get(remote_file, local_file or get_abs_path(os.path.split(remote_file)[-1])), err_msg=err_msg)

        return True


    def close(self):
        """
        Cloce the current connection session.
        :return:
        """
        err_msg: str = "Oops, Something went wrong."
        check_connection(connection=self.conn.close(), err_msg=err_msg)


