#  © Copyright IBM Corporation 2020.

from ai_lifecycle_cli.lib.utils.FsHandler import FsHandler
from ai_lifecycle_cli.lib.utils.LoggingHandler import LoggingHandler
from pathlib import Path
import json

logger = LoggingHandler()


def translate_assets(archive_file, archive_version, target_version):
    """
    Translates assets metadata from archive_version to target_version.
    :param archive_file:
    :param archive_version:
    :param target_version:
    :return: path to file with translated assets
    """

    translated_archive = archive_file

    translate_engines = {
        ('2.5', '3.0'): translate_from_v25_to_v30,
        ('3.0', '3.0'): pass_through
    }
    try:
        translate_engine = translate_engines.get((archive_version, target_version))
        if translate_engine is None:
            raise NotImplementedError
        translated_archive = translate_engine(archive_file)
    except NotImplementedError:
        logger.log_error("No translation available between versions {src} to {dest}"
                         .format(src=archive_version, dest=target_version))

    return translated_archive


def pass_through(archive_file):
    """
    Pass-through function for pair of version for with translation is not applicable
    :param archive_file:
    :return: archive_file
    """
    return archive_file


def translate_from_v25_to_v30(archive_file):
    """
    Translate assets from CP4D v2.5 format to v3.0 format
    :param path:
    :return: path
    """
    fs = FsHandler()

    path = fs.get_default_dir()
    fs.unpack_archive(archive_file, path)

    WML_TRANSLATEABLE_ASSET_TYPES = [
        'wml_model',
        'wml_model_definition',
        'wml_function',
        'wml_pipeline',
        'wml_experiment'
    ]

    # Loop through all files in .METADATA catalog
    for filename in fs.list_files(Path(path) / "assets" / ".METADATA"):
        filepath = Path(path) / "assets" / ".METADATA" / filename
        with open(str(filepath), 'r') as fin:
            content = json.load(fin)

            # Skip if asset_type is not translatable
            if "metadata" in content and content['metadata']['asset_type'] not in WML_TRANSLATEABLE_ASSET_TYPES:
                continue

            # Translate entity and metadata of CAMS asset
            logger.log_debug("Translating asset...")

            def _one_to_many_translation(content):
                for training_data_ref in content['entity'].get('training_data_references', []):
                    location_id = training_data_ref['location']['href'].split('/')[-1]
                    content['entity']['data_asset_dependencies'].append(location_id)

                for pipeline_ref in content['entity'].get('document', {}).get('pipelines', []):
                    for node_ref in pipeline_ref.get('nodes', []):
                        training_lib_id = node_ref['parameters']['training_lib_href'].split('/')[-1]
                        content['entity']['training_lib_dependencies'].append(training_lib_id)

                for training_references_ref in content['entity'].get('training_references', []):
                    pipeline_id = training_references_ref['pipeline']['id']
                    content['entity']['pipeline_dependencies'].append(pipeline_id)

                return content

            if 'entity' in content:
                # Remove 'space' from 'entity'
                content['entity'].pop('space', None)
                content['entity'].pop('project', None)
                # Remove 'space_id/project_id` query params from hrefs and move hrefs to ids
                pipeline_key = content['entity'].pop('pipeline', None)
                if pipeline_key is not None:
                    content['entity']['pipeline'] = {
                        "id": pipeline_key['href'].split('/')[-1]
                    }
                training_lib_key = content['entity'].pop('training_lib', None)
                if training_lib_key is not None:
                    content['entity']['training_lib'] = {
                        "id": training_lib_key['href'].split('/')[-1]
                    }
                content = _one_to_many_translation(content)

            # Save translated CAMS asset file
            with open(str(filepath.with_suffix(".new")), 'w') as fout:
                json.dump(content, fout)

        fs.overwrite_file(filepath.with_suffix(".new"), filepath)

    translated_archive = fs.archive_dirs([path], archive_file)

    return translated_archive[0]
