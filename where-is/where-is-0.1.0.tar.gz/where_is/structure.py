# where-is is a program/library that helps you find config files
# Copyright (C) <year>  <name of author>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import Dict, Union, List, Any
from where_is import utils
import jsonschema
import pathlib
import json
import os

class Manifest:
    def __init__(self, name: str, manifest_data: Dict[str, Union[str, List]]):
        self.manifest_data = manifest_data
        self.name = name
        with open("./schemas/manifest.json", "r") as schema:
            self.schema_data: Dict[str, Union[str, Any]] = json.load(schema)
        jsonschema.validate(self.manifest_data, schema=self.schema_data)

    @property
    def properties(self) -> str:
        # because mypy's getting triggered
        return self.manifest_data["property-of"]  # type: ignore

    @property
    def location(self) -> List[str]:
        possible_formats: Dict[str, str] = {
            "HOME_FOLDER": str(pathlib.Path.home())
        }

        path: str
        return [path.format(**possible_formats) for path in self.manifest_data["location"] if
                os.path.exists(path.format(**possible_formats))]

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', manifest_data={self.manifest_data})"

class Manifests:
    def __init__(self, config_location: str = utils.config_location()):
        self.config_location = config_location
        self.manifest_location: str = os.path.join(self.config_location, "manifests")
        if not os.path.exists(self.config_location):
            pathlib.Path(self.manifest_location).mkdir(parents=True, exist_ok=True)

    @property
    def manifest_paths(self) -> List[str]:
        return [os.path.join(self.manifest_location, file_path) for file_path in os.listdir(self.manifest_location)]

    @property
    def manifests(self) -> List[Manifest]:
        ret: List[Manifest] = []
        for file_path in self.manifest_paths:
            if os.path.basename(file_path) == "properties.json":
                continue
            try:
                with open(file_path, "r") as manifest:
                    try:
                        ret.append(Manifest(os.path.splitext(os.path.basename(file_path))[0], json.load(manifest)))
                    except jsonschema.exceptions.ValidationError:
                        continue
            except FileNotFoundError:
                continue

        return ret

    def __repr__(self):
        return f"{self.__class__.__name__}(config_location='{self.config_location}')"

class Property:
    def __init__(self, property_: str):
        self.property = property_
        self.manifests: Manifests = Manifests()
        self.properties: Properties = Properties()
        if self.property not in self.properties.all:
            raise ValueError("property doesn't exist")

    @property
    def inherits(self) -> List[Manifest]:
        return [manifest for manifest in self.manifests.manifests if manifest.properties == self.property]

    def __repr__(self):
        return f"{self.__class__.__name__}(property='{self.property}')"

class Properties:
    def __init__(self, manifests: Manifests = Manifests()):
        self.manifests = manifests

    @property
    def all(self) -> List[str]:
        for manifest_path in self.manifests.manifest_paths:
            if os.path.basename(manifest_path) == "properties.json":
                with open(manifest_path, "r") as properties:
                    return json.load(properties)
        else:
            raise FileNotFoundError("properties file not found")

    def __repr__(self):
        return f"{self.__class__.__name__}(manifests={self.manifests})"
