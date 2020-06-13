#!/usr/bin/env python3.6 
"""
Name: Rio Atmadja
Date: 5 April 2020

Description: This script is used by systemd to manage docker development pipelines
"""
from argparse import ArgumentParser, ArgumentError
import sys
import os 
import subprocess
from uuid import uuid4
from typing import List
import logging 

LOG = logging.getLogger(__name__)
DIR_PATH: str = "/home/cloud_user/Documents/DEV/server_container/keys"

class DeployTestContainer(object):

    def __init__(self, container_name: str):
        if not container_name: 
            raise ValueError("Must suplly container name.")  

        self.container_name: str = container_name

    def _cmd_(self, cmd: str) -> List[str]: 
        """
        This function will execute system command. 
        
        """
        if not cmd:
            raise ValueError("cmd cannot be empty.")
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.readlines()

    def _set_docker_cmd(self, cmd: str) -> str:
        """
        This function set the docker cmd 
        :param **kwargs: 
        :return : string of docker commane 
        """ 
        if not cmd:
            raise ValueError("command cannot be emtpy.")
        
        return f"/bin/docker ps -a | {cmd}"

    def execute_test_container(self, operation: str) -> List[str]:  
        """
        This function will start the test container 
        """

        if not operation:
            raise ValueError("operation cannot be empty.") 

        if operation == 'start': 
            self.generate_test_key() 

        field: str = "'{print $1}'"
        args:  str = "{}"
        docker_cmd: str = self._set_docker_cmd(f" grep {self.container_name}  | awk {field}  | xargs -I {args} docker {operation} {args}")
        return self._cmd_(docker_cmd)

    def build_container(self) -> List[str]: 
        """
        This function will build the development test server 
        :return : output from the subprocess 
        """

        self.print_output(self.tear_down_containers())
        self.generate_test_key() 

        container_name: str =  f"{self.container_name}_{str(uuid4())}"
        build_query: str = f"docker build -t {container_name} /home/cloud_user/Documents/DEV/server_container"

        self.print_output(self._cmd_(build_query))
        self.print_output(self.tear_down_testing_image())

        run_container: str = "`docker image ls  | sed -n '2p'  | awk '{ print $3 }'  | xargs -I {} echo docker run -d --name " + container_name +  " --mount type=bind,source=/mnt/buckets,target=/root/shares -p 8000:22 {} /usr/sbin/sshd -D`"

        return self._cmd_(run_container)

    def tear_down_containers(self) -> List[str]: 
        """
        This function will remove unused docker images
        :return: a list of executed command
        """
        tear_down_query: str = "docker ps -a  | sed -n '2,$p' | awk '{print $1 }' | xargs -I {} docker rm -f  {}"
        return self._cmd_(tear_down_query)

    def tear_down_testing_image(self) -> List[str]:
        """
        This function will tear down unused testing images
        :return:
        """
        tear_down_query: str = "docker image ls | sed -n '2,$p' | grep testing |  awk '{ print $3 }'  | xargs -I {} echo  docker image rm -f {}"
        return self._cmd_(tear_down_query)

    def check_container_status(self) -> str: 
        """
        This function will check the status of the docker container 
        :return : 
        """
        docker_cmd: str = self._set_docker_cmd(" grep {container_name} | grep Up")
        status: List[str] = [self._cmd_(docker_cmd).__len__() != 0 ] 
        return list(map(lambda x: 'Server Up' if x == False else 'Server Down' , status))[0]

    def generate_test_key(self) -> List[str]: 
        """
        Generate a unique key, everytime the development container is being spun up
        :return : the server keys 
        """

        # remove the old keys 
        old_keys: List[str] = os.listdir(DIR_PATH) 
        if old_keys: 
            build_cmd_query: str = ' '.join( list( map( lambda key : f"{DIR_PATH}/{key}" , os.listdir(DIR_PATH) )) ) 
            self._cmd_(f"rm -v {build_cmd_query}")
        
        return self._cmd_(f"ssh-keygen -t rsa -b 2048 -f {os.path.join(DIR_PATH, str(uuid4()))} -N \"\" ")

    def print_output(self, outputs: List[str]):
        """
        This function will print the output from subprocess
        :param outputs: given the output from subprocess 
        :return :
        """
        for output in outputs:
            print(output.decode('utf-8'))
        
if __name__ == "__main__": 


    parser = ArgumentParser(description="[+] Usage: " + sys.argv[0] + " --name <container_name> ") 
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--start", help='start container', action="store_true")
    parser.add_argument("--stop", help='stop container', action="store_true")
    parser.add_argument("--name", help='container name', action="store")
    parser.add_argument("--generate-key", help='generate server key', action="store_true")
    parser.add_argument("--build", help='build development container', action="store_true")


    args = vars(parser.parse_args()) 
    if not args['name']: 
        # Does not require arguments for systemd 
        test_container = DeployTestContainer('bitbukcet_testing_pipeline') 
        LOG.info("\033[46m [+] Executing command in systemd \033[0m") 
        test_container.print_output(test_container.build_container()) 
        exit() 
        # raise ArgumentError(f"[+] Usage: {sys.argv[0]} --name <container_name>") 

    test_container = DeployTestContainer(args['name']) 

    if args['status']:
        print(test_container.check_container_status()) 
        exit()         

    if args['start']: 
        test_container.print_output(test_container.execute_test_container('start')) 
        exit() 

    if args['stop']: 
        test_container.print_output(test_container.execute_test_container('stop')) 
        exit() 

    if args['generate_key']: 
        test_container.print_output(test_container.generate_test_key()) 
        exit() 

    if args['build']: 
        test_container.print_output(test_container.build_container()) 
        exit() 
