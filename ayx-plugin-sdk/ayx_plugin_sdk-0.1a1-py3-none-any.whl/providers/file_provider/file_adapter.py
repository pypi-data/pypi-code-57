# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Converts file provider classes to and from XML and CSV files."""
from pathlib import Path
from typing import Any, Dict, List

from ayx_plugin_sdk.core.field import FieldType
from ayx_plugin_sdk.core.metadata import Metadata
from ayx_plugin_sdk.providers.file_provider.file_provider_input_anchor import (
    FileProviderInputAnchor,
)
from ayx_plugin_sdk.providers.file_provider.file_provider_output_anchor import (
    FileProviderOutputAnchor,
)

import pandas as pd

import xmltodict


class FileAdapter:
    """
    File adapter class definition.

    This class converts input files into file provider objects and
    then also converts file provider objects back into output files.
    """

    def __init__(self, tool_config: Path, workflow_config: Path):
        """
        Instantiate a file adapter.

        Parameters
        ----------
        tool_config
            The path to the XML file that contains the tool configuration.
        workflow_config
            The path to the XML file that contains the anchor configurations.
        """
        config = self.convert_to_dict(tool_config)
        self.tool_config: Dict[str, Any] = config["Configuration"]
        self.workflow_config = self.convert_to_dict(workflow_config)
        tool_info = self.workflow_config["AlteryxJavaScriptPlugin"]["Properties"][
            "MetaInfo"
        ]
        self.name = tool_info["Name"]
        self.description = tool_info["Description"]

    def convert_to_dict(self, xml_file: Path) -> Dict[str, Any]:
        """
        Convert a XML file to a Python dictionary.

        Parameters
        ----------
        xml_file
            The XML file that should be converted to a Python dictionary.

        Returns
        -------
        Dict[str, Any]
            The anchor configuration information.
        """
        with open(xml_file) as fd:
            return dict(xmltodict.parse(fd.read(), strip_whitespace=True))

    def csv_to_dataframe(self, input_file: Path) -> pd.DataFrame:
        """
        Convert a CSV file to a pandas dataframe.

        Parameters
        ----------
        input_file
            The input CSV file that should be converted to a Pandas dataframe.

        Returns
        -------
        pandas.Dataframe
            The pandas dataframe that contains the input records.
        """
        # TODO: Add error handling on read_csv
        return pd.read_csv(input_file)

    def xml_to_metadata(self, xml_file: Path) -> Metadata:
        """
        Convert an xml file to record metadata.

        Parameters
        ----------
        xml_file
            The XML file that should be converted to Metadata.

        Returns
        -------
        Metadata
            The metadata information from the incoming XML file.
        """
        metadata = Metadata()
        metadata_dict = self.convert_to_dict(xml_file)
        # Iterate through each element of the XML called "Field"
        fields = metadata_dict["RecordInfo"]["Field"]
        for field in fields:
            name = field["@name"]
            size = int(field["@size"])
            field_type = FieldType(field["@type"])
            metadata.add_field(name=name, field_type=field_type, size=size)
        return metadata

    # TODO Remove duplicate code in build_input_anchors and build_output_anchors
    def build_input_anchors(self) -> List[FileProviderInputAnchor]:
        """
        Build the input anchors based on anchor configuration settings.

        Returns
        -------
        List[FileProviderInputAnchor]
            The a list of file provider input anchor information.
        """
        anchor_settings = self.workflow_config["AlteryxJavaScriptPlugin"]["GuiSettings"]

        input_anchors = anchor_settings.get("InputConnections")
        if not input_anchors:
            input_anchor_configs = []
        else:
            input_anchor_configs_raw = input_anchors["Connection"]
            if not isinstance(input_anchor_configs_raw, list):
                input_anchor_configs = [input_anchor_configs_raw]
            else:
                input_anchor_configs = input_anchor_configs_raw

        return [
            FileProviderInputAnchor(
                name=config["@Name"],
                allow_multiple=config["@AllowMultiple"].lower() == "true",
                optional=config["@Optional"].lower() == "true",
            )
            for config in input_anchor_configs
        ]

    def build_output_anchors(self) -> List[FileProviderOutputAnchor]:
        """
        Build the output anchors based on tool config settings.

        Returns
        -------
        List[FileProviderOutputAnchor]
            The a list of file provider output anchor information.
        """
        anchor_settings = self.workflow_config["AlteryxJavaScriptPlugin"]["GuiSettings"]

        output_anchors = anchor_settings.get("OutputConnections")

        if not output_anchors:
            output_anchor_configs = []
        else:
            output_anchor_configs_raw = output_anchors["Connection"]
            if not isinstance(output_anchor_configs_raw, list):
                output_anchor_configs = [output_anchor_configs_raw]
            else:
                output_anchor_configs = output_anchor_configs_raw

        return [
            FileProviderOutputAnchor(
                name=config["@Name"],
                allow_multiple=False,
                optional=config["@Optional"].lower() == "true",
            )
            for config in output_anchor_configs
        ]

    def dataframe_to_csv(self, output_file: Path, dataframe: pd.DataFrame) -> None:
        """
        Convert a pandas dataframe to an output CSV file.

        Parameters
        ----------
        output_file
            The path for the output file where the dataframe values should be held.
        dataframe
            The Pandas dataframe that should be converted to a CSV file.
        """
        # TODO Add error handling for to_csv
        # TODO There should be an option here for appending a dataframe to a CSV file that already exists
        dataframe.to_csv(output_file, index=False)

    def metadata_to_xml(self, output_file: Path, metadata: Metadata) -> None:
        """
        Convert record metadata to an XML file.

        Parameters
        ----------
        output_file
            The path for the output file where the metadata information should be held.
        metadata
            The Metadata that should be converted to a XML file.
        """
        # Record each field in record metadata to a different row in an XML file
        field_list = []
        for field in metadata.fields:
            field_dict = {
                "@name": field.name,
                "@size": str(field.size),
                "@type": field.type.value,
            }
            field_list.append(field_dict)
        fields_dict = {"Field": field_list}
        to_xml = {"RecordInfo": fields_dict}

        # Create the output XML file
        xml = xmltodict.unparse(
            input_dict=to_xml, pretty=True, short_empty_elements=True
        )
        with open(output_file, "w") as fd:
            fd.write(xml + "\n")
