# coding=utf8
# Copyright 2020 Cognicept Systems
# Author: Jakub Tomasek (jakub@cognicept.systems)
# --> Configuration class handles Cognicept configuration

from dotenv import dotenv_values
from pathlib import Path
import os
import sys
import re


class Configuration:
    config_path = os.path.expanduser("~/.cognicept/")
    env_path = config_path + "runtime.env"
    _regex_key = r"^([_A-Z0-9]+)$"

    def load_config(object, path):
        object.config_path = os.path.expanduser(path)
        object.env_path = object.config_path + "runtime.env"
        file = Path(object.env_path)
        
        if ((not file.exists()) or (file.is_dir())):
            print("Configuration file `" + object.env_path + "` does not exist.")
            return False
        
        object.config = dotenv_values(file)

        if(len(object.config) == 0):
            print("Configuration file `" + object.env_path + "` is empty or could not be parsed.")
            return False

        return True

    def configure(object, args):
        if(not object.load_config(args.path)):
            return
        
        if (not os.access(object.env_path, os.W_OK)):
            print("Error: You don't have writing permissions for `" + object.env_path + "`. Run as `sudo` or change file permissions.")
            return
        if(args.read):
            for key, value in object.config.items():
                print(key + ': "' + value + '"')
        elif(args.add):
            new_key = ""
            while(new_key == ""):
                new_key = input("Config name: ")

                # if empty, exit
                if(new_key == ""):
                    return
                # check if matches key specs
                matches = re.match(object._regex_key, new_key)
                if matches is None:
                    print("Error: Key can be uppercase letters, digits, and the '_'. Try again.")
                    new_key = ""
            
            new_value = ""
            while(new_value == ""):
                new_value = input("Value: ")
                if(new_value == ""):
                    return
                matches = re.match(r"^.*[\"].*$", new_value)
                if matches is not None:
                    print("Error: Value cannot contain '\"'. Try again.")
                    new_value = ""

            object.config[new_key] = new_value
        else:
            for key, value in object.config.items():
                new_value = input(key + "[" + value + "]:")
                matches = re.match(r"^.*[\"].*$", new_value)
                if((new_value != "") and (matches == None)):
                    object.config[key] = new_value
        object.save_config()

    def save_config(object):
        try:
            with open(object.env_path, 'w') as file:
                for key, value in object.config.items():
                    file.write(key + '=' + value + '\n')
        except IOError:
            print("Could not write into `" + object.env_path + "`. Please check write permission or run with `sudo`.")

      