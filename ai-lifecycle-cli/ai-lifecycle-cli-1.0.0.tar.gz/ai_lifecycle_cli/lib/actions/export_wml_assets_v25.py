#  © Copyright IBM Corporation 2020.

import json
import datetime

from pathlib import Path
from ai_lifecycle_cli.lib.utils.FsHandler import FsHandler
from ai_lifecycle_cli.lib.utils.LoggingHandler import LoggingHandler
from ai_lifecycle_cli.lib.utils import Constants


logger = LoggingHandler()


def execute(client, sources, timeout):
    """
        Gets all assets from either projects or spaces and save them to temporary directory
        :param client
        :param sources: list of sources of with specified guid and asset_types
        :param timeout
        :return: tuple of files and archived files
    """

    fs = FsHandler()

    files = []
    archived_files = []

    start = datetime.datetime.now()
    elapsed = datetime.datetime.now() - start

    for source_type in list(sources.keys()):
        logger.log_info("Exporting {source_type}s".format(source_type=source_type))
        source_query_string = {
            "space": "?space_id=",
            "project": "?project_id="
        }.get(source_type)

        for source in sources.get(source_type):
            logger.log_info("Exporting {source_type} with ID {source}".format(source_type=source_type, source=source))

            source_guid = source['guid']
            if 'assets' not in source or len(list(source['assets'].keys())) == 0:
                source_asset_types = Constants.EXPORT_SUPPORTED_ASSET_TYPES
            else:
                source_asset_types = list(source['assets'].keys())

            query_string = ""
            for index, asset_type in enumerate(source_asset_types):
                if asset_type not in Constants.EXPORT_SUPPORTED_ASSET_TYPES:
                    logger.log_warning("Asset type {name} is not supported!".format(name=asset_type))
                if index == 0:
                    query_string += "asset.asset_type:" + asset_type
                else:
                    query_string += " OR asset.asset_type:" + asset_type

            assets_path = "/v2/asset_types/asset/search" + source_query_string + source_guid
            search_body = dict(query=query_string)

            assets_res = client.make_request('post', path=assets_path, body=search_body)
            if assets_res.ok:
                search_data = assets_res.json()
                assets = search_data["results"]

                # Create new directory to store serialized files with project guid as folder name
                folder_name = str(source_guid)
                folder_path = Path.joinpath(fs.default_tmp_dir_path, folder_name)
                fs.create_serialize_directory_structure(folder_path, source_asset_types)

                # Iterate over all assets
                for asset in assets:
                    asset_id = ""
                    if "metadata" in asset and "asset_id" in asset["metadata"]:
                        asset_id = asset["metadata"]["asset_id"]
                    asset_type = ""
                    if "metadata" in asset and "asset_type" in asset["metadata"]:
                        asset_type = asset["metadata"]["asset_type"]
                    asset_name = ""
                    if "metadata" in asset and "name" in asset["metadata"]:
                        asset_name = asset["metadata"]["name"]

                    # if "metadata" in asset and \
                    #         "assets" in source and \
                    #         source['assets'][asset_type] != "all" and \
                    #         asset_id not in source['assets'][asset_type]:
                    #     continue

                    # Filter assets in sources:
                    # - skip asset if it is not found in <asset_type> in 'assets' section
                    if "metadata" in asset and \
                            asset_id not in source['assets'][asset_type]:
                        continue

                    # Get assets individually to get attachment details
                    # (no way to get attachment details from search api)
                    asset_href = asset["href"]
                    asset_res = client.make_request('get', path=asset_href)

                    if not asset_res.ok:
                        raise Exception("error retrieving asset details for %s. %s" % asset_name % asset_res.content)

                    asset = asset_res.json()
                    asset_attachments = asset.get("attachments", [])
                    serialized_asset_type = asset["metadata"]["asset_type"]

                    # Try to create directory for asset_type
                    try:
                        asset_type_path = Path.joinpath(
                            folder_path,
                            "assets",
                            serialized_asset_type
                        )
                        fs.setup_dir(asset_type_path)
                    except FileExistsError as ex:
                        logger.log_debug("Directory at {} exists".format(asset_type_path))

                    logger.log_debug(
                        "Processing asset with ID {asset_id} from {source_type} with ID {source_id}".format(
                            asset_id=asset_id,
                            source_type=source_type,
                            source_id=source_guid))
                    asset_path = Path.joinpath(
                        folder_path,
                        "assets",
                        serialized_asset_type,
                        asset_id
                    )

                    asset_metadata_name = serialized_asset_type + "." + asset_id + ".json"
                    asset_metadata_path = Path.joinpath(
                        folder_path,
                        "assets",
                        ".METADATA",
                        asset_metadata_name
                    )

                    # Dump metadata file was here

                    # iterate over all asset attachments
                    for index, attachment in enumerate(asset_attachments):
                        attachment_id = attachment["id"]
                        logger.log_debug(
                            "Processing attachment with ID {attach_id} associated with asset with ID {asset_id} from {source_type} with ID {source_id}".format(
                                attach_id=attachment_id,
                                asset_id=asset_id,
                                source_type=source_type,
                                source_id=source_guid))

                        # get the attachment file using asset-files-api
                        asset_files_key = attachment["handle"]["key"]
                        asset_files_href = "/v2/asset_files/" + asset_files_key + source_query_string + source_guid
                        attachment_res = client.make_request('get', path=asset_files_href)

                        if not attachment_res.ok:
                            raise Exception(
                                "error retrieving attachment files for the asset, %s. %s" % asset_name % attachment_res.content)

                        # If attachment handle key is starting with <asset_type>/...
                        # change attachment path to proper one
                        if asset_files_key.split('/')[0] != asset_type:
                            attachment_suffix = str("." + asset_files_key.split('/')[-1].split('.')[-1]) if len(asset_files_key.split('/')[-1].split('.')) > 1 else ""
                            asset['attachments'][index]["handle"]["key"] = "{}/{}/{}".format(asset_type, asset_id, attachment_id + attachment_suffix)
                            # Create asset directory under asset type with asset_id
                            fs.setup_dir(asset_path)
                            attachment_path = Path.joinpath(asset_path, attachment_id)
                        else:
                            attachment_dir = Path.joinpath(asset_type_path, '/'.join(asset_files_key.split('/')[1:-1]))
                            fs.setup_dir(attachment_dir)
                            attachment_path = Path.joinpath(attachment_dir, asset_files_key.split('/')[-1])
                        # Update object_key or create if does not exist
                        asset['attachments'][index]["object_key"] = asset['attachments'][index]["handle"]["key"]

                        # write the attachment out to file
                        with open(str(attachment_path), 'wb') as f:
                            f.write(attachment_res.content)

                        # Adding attachment paths to the files
                        files.append(attachment_path)

                    # filter out metadata
                    for meta in Constants.ASSET_EXCLUDED_METADATA:
                        asset['metadata'].pop(meta, None)

                    # filter in metadata
                    asset['metadata']['sandbox_id'] = asset['metadata']['space_id']

                    # write the asset json out to file
                    with open(str(asset_metadata_path), 'w') as outfile:
                        json.dump(asset, outfile)

                    # Adding asset json paths to the files
                    files.append(asset_metadata_path)

                # Saving assets and attachments into tmp directory
                # Create manifest json file and use it as flag file
                # Clean up archive content
                now = datetime.datetime.now()
                current_time = now.strftime("%c")
                fs.create_manifest_json(current_time, "1.0", source_type, source_guid, source_guid, folder_path)
                archived_files.append(folder_path)
                fs.cleanup_serialize_directory_structure(folder_path, source_asset_types)
            else:
                # If response code is not ok (200), print the resulting http error code with description
                raise Exception("error retrieving assets %s" % str(assets_res.content))

    return archived_files, files
