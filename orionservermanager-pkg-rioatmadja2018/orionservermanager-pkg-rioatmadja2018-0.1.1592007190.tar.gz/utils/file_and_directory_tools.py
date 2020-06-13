#!/usr/bin/env python
"""
Name: Rio Atmadja
Date: 02 April 2020
Description: director and files utility tools
"""
import os
from magic import from_file
from uuid import uuid4
from typing import List
from botocore.exceptions import MissingParametersError

def check_path(file_name: str, ext:str) -> bool:
    """
    This function will check if the given path exists
    :param path: given the file to be checked
    :return: boolean
    """
    if not os.path.exists(os.path.join(os.path.abspath('.'), file_name)) \
            and not validate_file_extension(file_name, ext):
        raise FileNotFoundError(f"ERROR: Unable to find the following file: {file_name}")

    return True

def get_abs_path(file_name: str) -> str:
    """
    This function will return the abs path of the file.
    If it exists.
    :param file_name: the full path of the given file
    :return: the absolute path of the file
    """

    abs_path: str = os.path.join(os.getcwd(), file_name)

    return abs_path

def obfuscate_file(file_name: str) -> str:
    """
    This function will obfuscate the given file by adding unique id
    :param file_name: given the file name
    :return:
    """
    return f"{uuid4()}_{file_name}"


def validate_file_extension(file_name: str, ext: str) -> bool:
    """
    This function will validate the given file extension
    :param file_name: given the file name
    :param ext: given the file extension
    :return: boolean
    """

    file_type: str = from_file(file_name, mime=True)
    if ext not in file_type:

        if 'application' in file_type:
            return True
        else:
            return False

    return True

def save_private_key(key_material: List[str], key_location: str, key_name: str) -> str:
    """
    This function will save the key to a default location ~/.ssh/<unique id>.pem, unless the key location and key_name are specified.
    :param key_material: given key_material from boto3 ec2 client key
    :param key_location: optional key_location
    :param key_name: optional key_name
    :return:
    """
    key_path: str = ""

    if not key_material and not key_location and not key_name:
        raise MissingParametersError(object_name="Required parameters", missing="key_material, key_location, key_name")

    if os.path.exists(key_location):
        key_path: str = os.path.join(key_location, key_name)

    try:
        with open(key_path, "w") as f:
            for line in key_material:
                f.write(line)
        f.close()
        return key_path

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Unable to create key_path.") from e






