#!/usr/bin/env python
"""
Name: Rio Atmadja
Date: 10 April 2020
Description: This class will manage ec2 instanses
"""
from typing import Dict, List
import boto3
from botocore.exceptions import MissingParametersError
from utils.connection_tools import check_connection
from utils.file_and_directory_tools import save_private_key
from uuid import uuid4
from utils.constants import AMI_LISTS
import os

class EC2_Manager(object):

    def __init__(self):
        self.ec2_client = boto3.client('ec2')
        self.ec2_resource = boto3.resource('ec2')

    def ec2_create_keys(self, key_location: str = os.path.expanduser("~/.ssh"), key_name: str = str(uuid4())) -> Dict:
        """
        This function will create a ssh key and save to local directory
        :param key_location: given the key location, default location ~/.ssh
        :param key_name: given the key name, default key_name uuid4()
        :return: a dictionary that contains the location of the key
        """
        response: Dict = check_connection(connection=self.ec2_client.create_key_pair(KeyName=key_name),
                                          err_msg=f"Unable to create key: {key_name}")

        key_material: List[str] = response.get("KeyMaterial").split("\n")
        new_key: str = save_private_key(key_material=key_material, key_location=key_location, key_name=f"{key_name}.pem" if "pem" not in key_name else key_name)

        if new_key:
            response['KeyLocation']: str = new_key
            response.pop('KeyMaterial')

        return response

    def ec2_delete_key(self, key_name) -> Dict:
        """
        This function will delete the specified key name
        :param key_name: given the key name to be deleted
        :return: a dictionary that contains the detail about deleted keys
        """

        if not key_name:
            raise MissingParametersError(object_name="Required parameters", missing="key_name")

        response: Dict = check_connection(connection=self.ec2_client.delete_key_pair(KeyName=key_name), err_msf=f"Unable to delete key: {key_name}")

        return response


    def ec2_get_keys(self, key_names: List[str]) -> Dict:
        """
        This function will retrive the given ssh keys and return details about the given keys
        :param key_names: given the key names
        :return: a dictionary that contains the key names deatils
        """
        if not key_names:
            raise MissingParametersError(object_name="Required parameters", missing="key_names")

        response: Dict = check_connection(connection=self.ec2_client.describe_key_pairs(KeyNames=key_names), err_msg=f"Unable to retrieve keys: {key_names}.")

        return response

    def ec2_create_instances(self, key_name: str, subnet_id: str, security_group_id: List[str], max_count: int = 1, min_count: int = 1, instance_type: str = 't2.small', image_id: str = 'ami-085925f297f89fce1') -> List:
        """
        This function will create small ubuntu image
        :param key_name: given the ubuntu image
        :param subnet_id: vpc subnet_id
        :param security_group_id: vpc security id
        :param max_count: optional with default 1
        :param min_count: optional with default 1
        :param instance_type: optional with default small
        :param image_id: optional with default ubuntu image
        :return: List of ec2 instance
        """

        if not key_name and not subnet_id and not security_group_id:
            raise MissingParametersError(object_name="Required parameters", missing="key_names, subnet_id, security_group_id")

        # Default Hardware
        BlockDeviceMappings: List[Dict] = [{'DeviceName': '/dev/sda1',
                                            'Ebs': {'DeleteOnTermination': True}
                                            }]

        InstanceType: str = instance_type
        ImageId: str = image_id
        KeyName: str = key_name

        # Networking
        SubnetId: str = subnet_id
        SecurityGroupIds: List[str] = security_group_id
        NetworkInterfaces: List[Dict] = [{'DeviceIndex': 0,
                              'DeleteOnTermination': True,
                              'SubnetId': SubnetId,
                              'Groups': SecurityGroupIds,
                              'AssociatePublicIpAddress': True}]

        return check_connection(connection=self.ec2_resource.create_instances(BlockDeviceMappings=BlockDeviceMappings,
                                                                          ImageId=ImageId,
                                                                          InstanceType=InstanceType,
                                                                          MaxCount=max_count,
                                                                          MinCount=min_count,
                                                                          KeyName=KeyName,
                                                                          NetworkInterfaces=NetworkInterfaces),
                                err_msg="Unable to create instance.")

    def ec2_delete_instance(self, instance_ids: List[str], dry_run: bool = False) -> Dict:
        """
        This function will delete the given ec2 instance_id
        :param instance_id: given the ec2 to be deleted
        :param dry_run: default is False
        :return: a dictionary of the deleted ec2
        """

        if not instance_ids:
            raise MissingParametersError(object_name="Required parameters", missing="instance_ids")

        return check_connection(connection=self.ec2_client.terminate_instances(InstanceIds=instance_ids,
                                                                               DryRun=dry_run),
                                err_msg=f"Unable to delete instance_id: {instance_ids}")

    def ec2_start_instance(self, instance_ids: List[str], dry_run: bool = False) -> Dict:
        """
        This function will start the given instance ids
        :param instance_ids: given the instance_ids
        :param dry_run: optional default is False
        :return: a dictionary of ec2 instance
        """

        if not instance_ids:
            raise MissingParametersError(object_name="Required parameters", missing="instance_ids")

        return check_connection(connection=self.ec2_client.start_instances(InstanceIds=instance_ids,
                                                                           DryRun=dry_run),
                                err_msg=f"Unable to start instance_ids: {instance_ids}")

    def ec2_stop_instance(self, instance_ids: List[str], dry_run: bool = False, hibernate: bool = False, force: bool = False) -> Dict:
        """
        This function will stop the given instance ids
        :param instance_ids: given the instance_ids
        :param dry_run: optional default False
        :param hibernate: optional default False
        :param force: optional default False
        :return: a dictionary of ec2 instance
        """

        if not instance_ids:
            raise MissingParametersError(object_name="Required parameters", missing="instance_ids")

        return check_connection(connection=self.ec2_client.stop_instances(InstanceIds=instance_ids,
                                                                          Force=force,
                                                                          Hibernate=hibernate,
                                                                          DryRun=dry_run),

                                err_msg=f"Unable to stop instance_ids: {instance_ids}")

    def ec2_get_instance(self, instance_id: str, dry_run: bool = False) -> Dict:
        """
        This function will retrieve a specific ec2 instance based on the given instance_id
        :param instance_id: given the ec2 instance_id
        :param dry_run: optional default False
        :return: a dictionary object of ec2
        """

        if not instance_id:
            raise MissingParametersError(object_name="Required parameters", missing="instance_id")

        return check_connection(connection=self.ec2_client.describe_instances(InstanceIds=[instance_id],
                                                                              DryRun=dry_run),
                                err_msg=f"Unable to retrieve instance_id: {instance_id}")

    def ec2_get_all_instances(self) -> List[Dict]:
        """
        This function will return all the ec2 instances
        :return: all the available ec2 instances
        """

        all_instances: Dict = check_connection(connection=self.ec2_client.describe_instances(),
                                               err_msg="Unable to retrieve ec2 instances.")

        instances: List[Dict] = all_instances.get('Reservations', None)
        if not instances:
            return [{}]

        return [[instance for instance in ec2_instance.get('Instances')][0] for ec2_instance in instances]

    def ec2_get_ami_images(self, **kwargs) -> List[Dict]:
        """
        This function will get AMI attributes from static dictionary
        :param kwargs: given the kwargs that contains image_id and platfrom attributes
        :return: a list of dictionary that contains AMI attributes
        """

        if 'image_id' not in kwargs or 'platform' not in kwargs:
            raise MissingParametersError(object_name="Required parameters", missing="image_id or platform")

        image_id: str = kwargs.get('imageId64', None)
        platform: str = kwargs.get('platform', None)

        return list(filter(lambda ami: ami if ami.get('platform') == platform or ami.get('imageId64') == image_id else None, AMI_LISTS))




