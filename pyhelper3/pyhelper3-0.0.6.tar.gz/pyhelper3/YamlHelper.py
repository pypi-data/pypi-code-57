# -*- coding: utf-8 -*-
import yaml
class YamlHelper:
    yaml_data = None
    #读取yaml文件
    def __init__(self,yaml_file_path=None):
        if yaml_file_path:
            with open(yaml_file_path,mode='r',encoding='utf-8') as yaml_file_obj:
                self.yaml_data = yaml.safe_load(yaml_file_obj.read())
    def get_data_by_key(self,key=None):
        if key:
            if key in self.yaml_data:
                return self.yaml_data[key]

