#  © Copyright IBM Corporation 2020.

import time
import re
import json
import requests
import jmespath
from flatten_dict import flatten
from ai_lifecycle_cli.lib.utils.LoggingHandler import LoggingHandler
from ai_lifecycle_cli.lib.utils.FsHandler import FsHandler
from ai_lifecycle_cli.lib.utils import Constants


logger = LoggingHandler()


def create_project(client, name, desc):
    """
    Create new project with given name
    :param client: RESTClient
    :param project_name: name of the project
    :return: newly created project guid; Exception is raised otherwise
    """
    try:
        create_project_path = "/v4/spaces"
        space_body = dict(
            name=name
        )

        project_creation_res = client.make_request('post', path=create_project_path, body=space_body)

        if not project_creation_res.ok:
            raise Exception("failed to create new project, %s" % project_creation_res.content)

        content = project_creation_res.json()
        return content["metadata"]["guid"]
    except requests.exceptions.RequestException:
        raise Exception("failed to create new project")


def create_space(client, name, desc):
    """
    Creates new space with given name
    :param client: RESTClient
    :param space_name: name of the space
    :param space_desc: description of space
    :param space_tags: list of tags related to the space
    :return: newly created space guid; Exception is raised otherwise
    """
    try:
        create_space_path = "/v4/spaces"
        space_body = dict(
            name=name,
            description=desc
        )

        space_creation_res = client.make_request('post', path=create_space_path, body=space_body)

        if not space_creation_res.ok:
            raise Exception("failed to create new space, %s" % space_creation_res.content)

        content = space_creation_res.json()
        return content["metadata"]["guid"]
    except requests.exceptions.RequestException:
        raise Exception("failed to create new space")


def detect_source_environment(client, source_version=None):
    """
    Detects version of environment, from which assets are exported.
    :param client:
    :return: string with version of source environment
    """
    if client:
        diag_response = client.make_request('get', path="/diag")
        version_res = re.search(r'^\d{1}.\d{1}.\d{1}.\d{1}', diag_response.text).group(0)
        if source_version is None:
            if version_res == '2.5.0.0':
                return '2.5'
            if version_res == '3.0.0.0':
                return '3.0'
            return '3.0'
        else:
            if version_res == '3.0.0.0' and source_version == '3.0':
                return '3.0'
            if version_res == '2.5.0.0' and source_version == '2.5':
                return '2.5'
            else:
                return 'invalid'


def detect_target_environment(client):
    """
    Detects version of environment, to which assets are imported.
    :param client:
    :return: string with version of target environment
    """
    if client:
        diag_response = client.make_request('get', path="/diag")
        version_res = re.search(r'^\d{1}.\d{1}.\d{1}.\d{1}', diag_response.text)
        if version_res == '2.5.0.0':
            raise Exception("Import into CP4D 2.5.0.0 is not supported")
        if version_res == '3.0.0.0':
            return '3.0'
        return '3.0'


def detect_target_archive(archive):
    """
    Detects version and type (project, space) of exported archive based on manifest file.
    :param archive:
    :return: string with version of exported archive and archive type
    """
    fs = FsHandler()
    manifest_path = fs.get_file_from_archive(archive, 'manifest.json')
    try:
        with open(str(manifest_path), 'r') as f:
            manifest = json.load(f)
            if 'container' in manifest and 'type' in manifest['container']:
                return '2.5', manifest['container']['type']
            else:
                return '2.5', 'space'
    except FileNotFoundError as e:
        logger.log_info("No manifest detected - archive is coming from export from CP4D 3.0 cluster")
        return '3.0', 'space'


def get_asset(client, asset_id, source_type, source_guid):
    """
    Retrieve asset
    :param client:
    :param asset_id:
    :param source_type:
    :param source_guid:
    :return: Asset from CAMS
    """
    source_query_string = {
        "space": "?space_id=",
        "project": "?project_id="
    }.get(source_type)
    asset_path = "/v2/assets/{}".format(asset_id) + source_query_string + source_guid
    asset_res = client.make_request('get', path=asset_path)
    if asset_res.ok:
        asset_entity = asset_res.json()['entity']
        asset_metadata = asset_res.json()['metadata']
    else:
        raise Exception("Couldn't retrieve asset with ID {asset_id}.".format(asset_id=asset_id))

    return asset_entity, asset_metadata


def search_asset(client, query, source_type="space", source_guid=None):
    """
    Searches for assets using by providing Lucene query
    :param client:
    :param query:
    :param source_type:
    :param source_guid:
    :return:
    """
    source_query_string = {
        "space": "?space_id=",
        "project": "?project_id="
    }.get(source_type)
    search_body = {
        "query": query
    }
    assets_path = "/v2/asset_types/asset/search" + source_query_string + source_guid
    assets_res = client.make_request('post', path=assets_path, body=search_body)
    if assets_res.ok:
        search_data = assets_res.json()
        assets = search_data["results"]
    else:
        raise Exception("Couldn't find asset.")
    return assets


def get_all_assets(client, asset_type=None, source_type="space", source_guid=None, full_metadata=False):
    """
    Retrieve all assets metadata of given type
    :param client:
    :param asset_type:
    :param source_type:
    :param source_guid:
    :param full_metadata:
    :return: List of str with IDs of assets of given type
    """
    source_query_string = {
        "space": "?space_id=",
        "project": "?project_id="
    }.get(source_type)
    if asset_type is None:
        search_body = {
            "query": "asset.asset_state:available"
        }
    elif isinstance(asset_type, str):
        search_body = {
            "query": "asset.asset_type:" + asset_type
        }
    elif isinstance(asset_type, list) and len(asset_type) > 0:
        search_body = {
            "query": " OR ".join(["asset.asset_type:{}".format(t) for t in asset_type])
        }
    else:
        raise Exception("Incorrect query provided")
    assets_path = "/v2/asset_types/asset/search" + source_query_string + source_guid
    assets_res = client.make_request('post', path=assets_path, body=search_body)
    if assets_res.ok:
        search_data = assets_res.json()
        assets = search_data["results"]
        if full_metadata:
            assets_info = list(map(lambda x: x['metadata'], assets))
        else:
            assets_info = list(map(lambda x: x['metadata']['asset_id'], assets))
    else:
        raise Exception("Couldn't retrieve assets for {asset_type} asset type.".format(asset_type=asset_type))

    return assets_info


def dfs_dependency_search(client, dependency_tree, assets_dict, space_guid):
    for asset_type in assets_dict:
        dependency_tree[asset_type] = {}
        for asset in assets_dict[asset_type]:
            try:
                deps = get_asset_dependencies(client, asset, space_guid)
            except Exception as e:
                if asset_type in ["software_specification"]:
                    deps = []
                else:
                    raise e
            if len(deps) == 0:
                dependency_tree[asset_type][asset] = "END"
            else:
                dependency_tree[asset_type][asset] = {}
                dependency_tree[asset_type][asset] = dfs_dependency_search(client, dependency_tree[asset_type][asset], deps, space_guid)
    return dependency_tree


def get_asset_dependencies(client, asset, space_guid):
    asset_entity, asset_metadata = get_asset(client, asset, 'space', space_guid)
    asset_type = asset_metadata['asset_type']
    deps = dict()
    for path, asset_t in Constants.WML_DEPENDENCY_MAP.get(asset_type, {}).items():
        asset_list = jmespath.search(path, asset_entity[asset_type]) if jmespath.search(path, asset_entity[asset_type]) is not None else []
        if not isinstance(asset_list, list):
            asset_list = [asset_list]
        results = list(map(lambda res: res.split('/')[-1].split('?')[0], asset_list))
        if len(results) > 0:
            deps[asset_t] = results
    return deps


def merge_space_sources(dict1, dict2):
    dict1_space = sorted(dict1.get('space', []), key=lambda x: x['guid'])
    dict2_space = sorted(dict2.get('space', []), key=lambda x: x['guid'])
    for idx, space in enumerate(dict2_space):
        if len(dict1_space) < idx + 1:
            dict1_space.append({
                'guid': space['guid'],
                'assets': {}
            })
        for key, val in dict2_space[idx]['assets'].items():
            if key not in dict1_space[idx]['assets']:
                dict1_space[idx]['assets'][key] = val
            elif len(dict1_space[idx]['assets'][key]) == 0:
                dict1_space[idx]['assets'][key] = val
            else:
                dict1_space[idx]['assets'][key] = list(set(dict1_space[idx]['assets'][key]) | set(val))
    return {
        'space': dict1_space
    }


def resolve_dependencies(client, sources, shallow=False):
    """
    Build complete list of assets to export based on user provided list of assets
    :param client:
    :param sources:
    :return:
    """

    if 'project' in sources:
        logger.log_warning("Project sources are skipped")
        sources.pop('project')

    # Create new reference
    resolved_sources = sources

    # Resolve non-existing 'assets' key and "all" indicator for asset_types
    for ix, space in enumerate(resolved_sources.get('space', [])):
        space_guid = space['guid']
        if 'assets' not in space:
            resolved_sources['space'][ix]['assets'] = {}
            for asset_type in Constants.WML_RESOLVABLE_ASSET_TYPES:
                resolved_sources['space'][ix]['assets'][asset_type] = get_all_assets(client, asset_type, 'space', space_guid)
        else:
            for asset_type in space['assets']:
                if space['assets'][asset_type] == "all":
                    resolved_sources['space'][ix]['assets'][asset_type] = get_all_assets(client, asset_type, 'space', space_guid)

    # Resolve all dependencies
    if not shallow:
        dependence_sources = dict()
        merged_dependence_sources = dict()
        dependence_sources['space'] = []
        # Resolve asset dependencies
        for ix, space in enumerate(resolved_sources.get('space', [])):
            space_guid = space['guid']

            # Perform DFS Search for all dependencies
            dep_assets = dfs_dependency_search(client, {}, space['assets'], space_guid)
            flatten_assets = dict.fromkeys(Constants.WML_RESOLVABLE_ASSET_TYPES)
            for asset_type in flatten_assets:
                flatten_assets[asset_type] = []
            flat_deps = flatten(dep_assets, reducer='path')
            for el in flat_deps:
                paths = el.split('/')
                for i in range(int(len(paths) / 2)):
                    if paths[2 * i] not in flatten_assets:
                        flatten_assets[paths[2 * i]] = [paths[2 * i + 1]]
                    else:
                        flatten_assets[paths[2 * i]].append(paths[2 * i + 1])
            # Merge parent assets with dependencies
            space_spec = {
                "guid": space_guid,
                "assets": flatten_assets
            }
            dependence_sources['space'].append(space_spec)
            merged_dependence_sources = merge_space_sources(merged_dependence_sources, dependence_sources)

        resolved_sources = merge_space_sources(resolved_sources, merged_dependence_sources)

    return resolved_sources
