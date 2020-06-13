#!/usr/bin/env python3.6
"""
Name: Rio Atmadja
Date: 09 April 2020
Description: This class will manage Amazon VPCs
"""
import boto3
from typing import Dict, List
from botocore.exceptions import ClientError, MissingParametersError
import pandas as pd
import numpy as np
from datetime import datetime as dt
from utils.connection_tools import check_connection

class VPCManager(object):

    def __init__(self):
        self.ec2_client = boto3.client('ec2')
        self.date: str = dt.now().strftime('%Y-%m-%d')
        self.description: str = ""

    def ec2_get_all_vpcs(self, vpcs: List[str] = []) -> Dict:
        """
        This function will get all the available vpcs
        :param vpcs: given an optional list of vpcs
        :return: a dictionary object of vpcs
        """

        response: Dict = check_connection(connection=self.ec2_client.describe_vpcs(VpcIds=vpcs),
                                          err_msg=f"Unable to retrieve the following vpcs: {vpcs}")

        return response

    def ec2_get_vpc_attributes(self, vpc_id: str, attribute: str = 'enableDnsSupport' ) -> Dict:
        """
        This function will get all vpc attributes for the given vpn_id
        :param vpc_id: given the vpc_id
        :return: a dictionary object of vpc attribute
        """

        if not vpc_id:
            raise MissingParametersError(object_name="Required parameters", missing="vpc_id")

        response: Dict = check_connection(connection=self.ec2_client.describe_vpc_attribute(Attribute=attribute,
                                                                                     VpcId=vpc_id),
                                          err_msg=f"Unable to retrieve attributes for given vpc_id: {vpc_id}")

        return response

    def ec2_create_vpc(self, cidr_block: str, provided_ipv6_cidr_block: bool = False, dry_run: bool = False, instance_tenancy: str = 'default') -> Dict:
        """
        This function will create vpc for ec2 instanses
        :param cidr_block: given cidr block
        :param provided_ipv6_cidr_block: optional
        :param dry_run: optional
        :param instance_tenancy: optional
        :return: a dictionary of vpc object
        """
        if not cidr_block:
            raise MissingParametersError(object_name="Required paramters", missing="cidr_block")


        response: Dict = check_connection(connection=self.ec2_client.create_vpc(CidrBlock=cidr_block,
                                                                                AmazonProvidedIpv6CidrBlock=provided_ipv6_cidr_block,
                                                                                DryRun=dry_run, InstanceTenancy=instance_tenancy),
                                          err_msg=f"Unable to create vpc with cidr {cidr_block}")
        return response

    def ec2_delete_vpc(self, vpc_id: str, dry_run: bool = False) -> Dict:
        """
        This function will delete the given vpc_id
        :param vpc_id: given the vpc_id
        :param dry_run: optional, emulate delete vpc_id
        :return:
        """
        if not vpc_id:
            raise MissingParametersError(object_name="Required paramters", missing="vpc_id")

        response: Dict = check_connection(connection=self.ec2_client.delete_vpc(VpcId=vpc_id, DryRun=dry_run),
                                          err_msg=f"Unable to delete vpc_id: {vpc_id}")

        return response

    def ec2_get_client_subnets(self, subnet_ids: List[str] = []) -> List[Dict]:
        """
        This function will get all the available subnets
        :param subnet_ids: given a list of string that contains ec2 subnet_ids
        :return: a list of dictionary that contains ec2 subnet attributes
        """

        response: List[Dict] = check_connection(connection=self.ec2_client.describe_subnets(SubnetIds=subnet_ids).get('Subnets'),
                                          err_msg=f"Unable to retrieve subnets {subnet_ids}")

        return response

    def ec2_delete_client_subnet(self, subnet_id: str) -> Dict:
        """
        This function will delete the given subnet_id
        :param subnet_id: given the subnet_id to be deleted
        :return: a dictionary that contains the ec2 subnet attributes
        """

        if not subnet_id:
            raise MissingParametersError(object_name="Required paramters", missing="subnet_id")

        response: Dict = check_connection(connection=self.ec2_client.delete_subnet(SubnetId=subnet_id))

        return response

    def ec2_create_client_subnet(self, cidr_block: str, vpc_id: str) -> Dict:
        """
        This function will create subnet for a given cidr block and vpc_id
        :param cidr_block: given the cidr block
        :param vpc_id: given the vpc_id
        :return: subnet object
        """

        if not cidr_block and not vpc_id:
            raise MissingParametersError(object_name="Required paramters", missing="cidr_block, vpc_id")

        response: Dict = check_connection(connection=self.ec2_client.create_subnet(CidrBlock=cidr_block,
                                                                                   VpcId=vpc_id, DryRun=False),
                                          err_msg=f"Unable to create subnet for VPC Id: {vpc_id}")
        return response

    def ec2_get_secuirty_group(self, group_ids: List[str] = []) -> List[Dict]:
        """
        This function will retrieve all security groups
        :param group_ids: given a list of group ids
        :return: a list of dictionary of ec2 security group
        """

        response: List[Dict] = check_connection(connection=self.ec2_client.describe_security_groups(GroupIds=group_ids).get('SecurityGroups'),
                                          err_msg=f"Unable to retrieve security_group for group_ids {group_ids}")

        return response

    def ec2_create_security_group(self, vpc_id: str, description: str, group_name: str, dry_run: bool = False) -> Dict:
        """
        This function will create security group from the given vpc_id
        :param vpc_id: given the vpc_id required
        :param description: given the description required
        :param group_name: given the group_name required
        :param dry_run: optional
        :return: security configuration group
        """
        if not vpc_id and not description and not group_name:
            raise MissingParametersError(object_name="Required paramters", missing="vpc_id, description, group_name")


        self.description = f"{description} created on {self.date}"
        response: Dict = check_connection(connection=self.ec2_client.create_security_group(Description=self.description,
                                                                                                  GroupName=group_name,
                                                                                                  VpcId=vpc_id,
                                                                                                  DryRun=dry_run),
                                          err_msg=f"Unable to create security group for VpcId: {vpc_id}")
        return response

    def ec2_delete_security_group(self, group_id: str, group_name: str = "", dry_run: bool = False) -> Dict:
        """
        This function will delete security group fro
        :param group_id: given the required parameter group_id
        :param group_name: given the optional parameter group_name
        :return: a dictionary with ec2 security group attribute
        """
        if not group_id and not group_name:
            raise MissingParametersError(object_name="Required paramters", missing="group_id, group_name")

        response: Dict = check_connection(connection=self.ec2_client.delete_security_group(GroupId=group_id,
                                                                                           GroupName=group_name,
                                                                                           DryRun=dry_run),

                                          err_msg=f"Unable to delete security group from the given group_id: {group_id} and group_name: {group_name}")

        return response

    def ec2_list_inbound_rules(self, GroupId: str) -> pd.core.frame.DataFrame:
        """
        This function will list all inbound rules
        :param GroupId: given the group Id
        :return:
        """
        if not GroupId:
            raise MissingParametersError(object_name="Required parameters", missing="GroupId")

        try:
            results = self.ec2.describe_security_groups(GroupIds=[GroupId])
            if not results:
                raise ValueError(f'Unable to fetch the inbound rules for GroupId = {GroupId}.')

            df = pd.DataFrame.from_dict(results.get('SecurityGroups')[0].get('IpPermissions'))
            df.index = np.arange(1, len(df)+1)
            return df

        except ClientError as e:
            raise ClientError('Unable to complete your request.') from e

    def ec2_create_inbound_rules(self, GroupId: str, FromPort: str, ToPort,CIDR:str = "0.0.0.0/0", proto: str='tcp', description: str= '') -> Dict:
        """
        This function will delete a specified inbound rules
        :param GroupId: Given the Security Group Ids
        :param FromPort: Given the from port number
        :param ToPort: Given the to port number
        :param CIDR: Given the CIDR blocks
        :param proto: Given the Internet Protocol (TCP/UDP)
        :return: response from ec2
        """
        if not GroupId or not FromPort or not ToPort:
            raise MissingParametersError(object_name="Required parameters", missing="GroupId, FromPort, ToPort")

        response: Dict = check_connection(
            connection=self.ec2.authorize_security_group_ingress(
                GroupId=GroupId,
                IpPermissions=[
                    {'FromPort': FromPort,
                     'ToPort': ToPort,
                     'IpProtocol': proto,
                     'IpRanges': [
                         {'CidrIp': CIDR,
                          'Description': description
                          }
                     ]}],
                DryRun=False),
            err_msg=f"Unable to create inbound rules Range: {FromPort} - {ToPort}")

        return response

    def ec2_delete_inbound_rules(self, GroupId: str, FromPort: str, ToPort, CIDR:str = "0.0.0.0/0", proto: str='tcp') -> Dict:
        """
        This function will delete a specified inbound rules
        :param GroupId: Given the Security Group Ids
        :param FromPort: Given the from port number
        :param ToPort: Given the to port number
        :param CIDR: Given the CIDR blocks
        :param proto: Given the Internet Protocol (TCP/UDP)
        :return: response from ec2
        """
        if not GroupId or not FromPort or not ToPort:
            raise MissingParametersError(object_name="Required paramters", missing="GroupId, FromPort, ToPort")

        response: Dict = check_connection(
            connection=self.ec2.revoke_security_group_ingress(
                GroupId=GroupId,
                IpPermissions=[
                    {'FromPort': FromPort,
                     'ToPort': ToPort,
                     'IpProtocol': proto,
                     'IpRanges': [
                         {'CidrIp': CIDR}
                     ]}
                ], DryRun=False),
            err_msg=f"Unable to delete inbound rules from port {FromPort} to {ToPort}")

        return response






