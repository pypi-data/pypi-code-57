#!/usr/bin/env python
"""
Name: Rio Atmadja
Date: 18 April 2020
Description: This is a test script to perform AWS ec2 essentials
"""
from server_managers.ec2_managers import EC2_Manager
from utils.vpc_managers import VPCManager
from datetime import datetime as dt
from typing import Dict, List

RED: str = "\033[91m"
GREEN: str = "\033[92m"
RESET: str = "\033[0m"

class LaunchInstance(object):

    def __init__(self):
        self.ec2_instance = EC2_Manager()
        self.ec2_vpc = VPCManager()
        self.cidr_block: str = "10.0.0.0/16"


    def create_instance(self) -> List[Dict]:
        """
        This test function will create the following:
        - vpc
        - subnet
        - security group
        - ec2 instance
        :return: a list of dictionary of ec2 attributes
        """
        server_key: Dict = self.ec2_instance.ec2_create_keys()
        vpc: Dict = self.ec2_vpc.ec2_create_vpc(cidr_block=self.cidr_block)
        vpc_id: int = vpc.get('Vpc').get('VpcId')
        subnet: Dict = self.ec2_vpc.ec2_create_client_subnet(cidr_block=self.cidr_block,
                                                             vpc_id=vpc_id)

        security_group: Dict = self.ec2_vpc.ec2_create_security_group(vpc_id=vpc_id, description="Test instances", group_name="launch-test-group")


        ec2_instance: List[Dict] = self.ec2_instance.ec2_create_instances(key_name=server_key.get('KeyName'),
                                               subnet_id=subnet.get("Subnet").get('SubnetId'),
                                               security_group_id=[security_group.get("GroupId")])

        return ec2_instance


    def delete_instance(self) -> Dict:
        """
        This test function will delete all available instances
        :return: a dictionary attribute of the deleted instances
        """

        instances_ids: List[str] = list(map(lambda instance: instance.get('InstanceId'), self.ec2_instance.ec2_get_all_instances()))

        return self.ec2_instance.ec2_delete_instance(instance_ids=instances_ids)

    def delete_vpcs(self) -> List[Dict]:
        """
        This test function will delete all the available vpcs for testing
        :return: a list of dictionary that contains ec2 vpc attributes
        """

        vpcs: Dict = self.ec2_vpc.ec2_get_all_vpcs().get('Vpcs')
        vpc_ids: List[str] = list(map(lambda vpc: vpc.get('VpcId', vpcs), vpcs))

        return [self.ec2_vpc.ec2_delete_vpc(vpc_id=vpc) for vpc in vpc_ids]

    def delete_subnet(self) -> List[Dict]:
        """
        This test function will delete the given subnets
        :return: a list of dictionary of ec2 subnets
        """
        subnets: List[str] = list(map(lambda subnet: subnet.get("SubnetId"), self.ec2_vpc.ec2_get_client_subnets()))
        return [self.ec2_vpc.ec2_delete_client_subnet(subnet_id=subnet_id) for subnet_id in subnets]

    def delete_security_group(self) -> List[Dict]:
        """
        This test function will delete all the security groups
        :return:
        """
        sg: List[Dict] = self.ec2_vpc.ec2_get_secuirty_group()
        security_groups: List[str] = list(map(lambda sg: sg.get("GroupId"), sg))
        return [self.ec2_vpc.ec2_delete_security_group(group_id=group_id) for group_id in security_groups]

if __name__ == "__main__":
    launch_instance = LaunchInstance()
    print(f"[+] Launching Test Instance: {dt.today().isoformat()}")
    # Test: Create instance
    # launch_instance.create_instance()

    print(f"[{GREEN}+{RESET}] INVOKE: DELETE RESOURCES")
    # Test: Delete All subnets
    print(f"[{GREEN}+{RESET}] DELETE SUBNETS:\n {launch_instance.delete_subnet()}")

    # Test: Delete All security groups
    print(f"[{GREEN}+{RESET}] DELETE SECURITY GROUP:\n {launch_instance.delete_security_group()}")

    # Test: Delete all vpcs
    print(f"[{GREEN}+{RESET}] DELETE VPCs:\n {launch_instance.delete_vpcs()}")

    # Test: Delete all instance
    print(f"[{GREEN}+{RESET}] DELETE Instances:\n {launch_instance.delete_instance()}")





