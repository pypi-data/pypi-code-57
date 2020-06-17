import os
import yaml


class Config:
    def __init__(self, yml_file_path: str):
        if not os.path.exists(yml_file_path):
            raise FileNotFoundError(f"{yml_file_path} does not exists!")

        self.yaml_file_path = yml_file_path
        with open(self.yaml_file_path) as y:
            self.__yml = yaml.safe_load(y)

    def __getattr__(self, item):
        return self.__yml.get(item)

    def __str__(self):
        output = "Config parameters:\n"
        for key, value in self.__yml.items():
            if isinstance(value, dict):
                output += f"{key}:\n"
                for k, v in value.items():
                    output += f"  {k}: {v}\n"
            else:
                output += f"{key}: {value}\n"

        output += "=" * 50
        return output
