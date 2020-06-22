# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import logging
from azureml._vendor.azure_cli_core.cloud import AZURE_PUBLIC_CLOUD, \
                                                 _arm_to_cli_mapper, \
                                                 _convert_arm_to_cli, \
                                                 _config_add_cloud, \
                                                 KNOWN_CLOUDS
from azureml._vendor.azure_cli_core._environment import get_az_config_dir

logger = logging.getLogger(__name__)


class _Clouds(object):
    """The cloud class used only for azureml"""

    _clouds = None

    @staticmethod
    def get_cloud_or_default(cloudName):
        """Retrieves the named cloud, or Azure public cloud if the named cloud couldn't be found.

        :param cloudName: The name of the cloud to retrieve. Can be one of AzureCloud, AzureChinaCloud, or AzureUSGovernment.
                          If no cloud is provided, any configured default from the Azure CLI is used. If no default is found,
                          if AzureCloud is found, AzureCloud is used. Otherwise the first cloud is used.
        :type cloudName: str
        :return: The named cloud, any configured default cloud, or the Azure public cloud if the named or default clouds couldn't be found.
        :rtype: azureml._vendor.azure_cli_core.cloud.Cloud
        """
        if not _Clouds._clouds:
            _all_clouds = _Clouds.get_clouds()
            if _all_clouds:
                _Clouds._clouds = {_all_clouds[i].name: _all_clouds[i] for i in range(0, len(_all_clouds), 1)}
            else:
                _Clouds._clouds = {KNOWN_CLOUDS[i].name: KNOWN_CLOUDS[i] for i in range(0, len(KNOWN_CLOUDS), 1)}

        if cloudName in _Clouds._clouds:
            return _Clouds._clouds[cloudName]
        else:
            default_cloud_name = _Clouds.get_default_cloud_name_from_config()
            if default_cloud_name in _Clouds._clouds:
                return _Clouds._clouds[default_cloud_name]
            else:
                return list(_Clouds._clouds.values())[0]


    @staticmethod
    def get_default_cloud_name_from_config():
        """Retrieves the name of the configured default cloud, or the name of the Azure public cloud if a default couldn't be found.

        :return: The name of the configured default cloud, or the name of the Azure public cloud if a default cloud couldn't be found.
        :rtype: str
        """
        config_dir = get_az_config_dir()
        config_path = os.path.join(config_dir, 'config')
        TARGET_CONFIG_SECTION_LITERAL = '[cloud]'
        TARGET_CONFIG_KEY_LITERAL = 'name = '
        cloud = AZURE_PUBLIC_CLOUD.name
        foundCloudSection = False
        try:
            with open(config_path, 'r') as f:
                line = f.readline()
                while line != '':
                    if line.startswith(TARGET_CONFIG_SECTION_LITERAL):
                        foundCloudSection = True

                    if foundCloudSection:
                        if line.startswith(TARGET_CONFIG_KEY_LITERAL):
                            cloud = line[len(TARGET_CONFIG_KEY_LITERAL):].strip()
                            break
                        if line.strip() == '':
                            break

                    line = f.readline()
        except IOError:
            pass

        return cloud

    
    @staticmethod
    def _get_clouds_by_metadata_url(metadata_url):
        """Get all the clouds by the specified metadata url

            :return: list of the clouds
            :rtype: list[azureml._vendor.azure_cli_core.Cloud]
        """
        try:
            import requests
            with requests.get(metadata_url) as meta_response:
                arm_cloud_dict = meta_response.json()
                cli_cloud_dict = _convert_arm_to_cli(arm_cloud_dict)
                if 'AzureCloud' in cli_cloud_dict:
                    # change once active_directory is fixed in ARM for the public cloud
                    cli_cloud_dict['AzureCloud'].endpoints.active_directory = 'https://login.microsoftonline.com'
                return list(cli_cloud_dict.values())
        except Exception as ex:  # pylint: disable=broad-except
            logger.warning('Failed to load cloud metadata from the url specified by {0}'.format(metadata_url))
            pass


    @staticmethod
    def get_clouds():
        """Get all the clouds from metadata url list

            :return: list of the clouds
            :rtype: list[azureml._vendor.azure_cli_core.Cloud]
        """
        metadata_url_list = [
            "https://management.azure.com/metadata/endpoints?api-version=2019-05-01",
            "https://management.azure.eaglex.ic.gov/metadata/endpoints?api-version=2019-05-01"]
        clouds = []
        # Iterate the metadata_url_list, if any one returns non-empty list, return it
        for metadata_url in metadata_url_list:
            all_clouds = _Clouds._get_clouds_by_metadata_url(metadata_url)
            if all_clouds:
                return all_clouds;
