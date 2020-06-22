#  © Copyright IBM Corporation 2020.
import os

from ai_lifecycle_cli.lib.clients.rest_client import RESTClient
from ai_lifecycle_cli.lib.utils.FsHandler import FsHandler
from ai_lifecycle_cli.lib.utils.LoggingHandler import LoggingHandler
from ai_lifecycle_cli.lib.utils.CPDStatusHandler import CPDStatusHandler
from ai_lifecycle_cli.lib.actions import import_wml_assets, import_wml_assets_v25, translate_assets, preparation
from ai_lifecycle_cli.lib.actions import manage_wml_assets
from pathlib import Path
import json

# 'import' command
def do_import(args):

    # Initialize default dir
    fs = FsHandler()
    fs.setup_dir(args.temp_dir)

    # Define loggers
    logger = LoggingHandler()
    status_logger = CPDStatusHandler(args.temp_dir, "import")

    # Initialize REST Client
    logger.log_debug("Importing assets...")
    client = RESTClient(args.cpd_url, (args.cpd_user, args.cpd_pass))

    # Detect CP4D version of source environment to choose import logic (now only 3.0 supported)
    archive_version, archive_type = preparation.detect_target_archive(args.input_file)
    target_version = preparation.detect_target_environment(client)

    # Translate assets which are pending import to proper version
    translated_archive = translate_assets.translate_assets(args.input_file, archive_version, target_version)
    #translated_archive = args.input_file

    # Prepare name and description for new space
    if args.import_name is None:
        container_name = "{container}-imported-from-{container_id}".format(
            container=archive_type,
            container_id="id")
    else:
        container_name = args.import_name

    if args.import_desc is None:
        container_desc = "{container_u} imported from {container} {container_id} using AI Lifecycle CLI".format(
            container_u=archive_type.capitalize(),
            container=archive_type,
            container_id="id")
    else:
        container_desc = args.import_desc

    # Select import engine
    import_engines = {
        '2.5': import_wml_assets_v25,
        '3.0': import_wml_assets
    }
    status_logger.log_status(msg="Selecting import engine...",
                             percentage=0
                             )
    import_engine = import_engines.get(target_version, import_wml_assets)

    # Create space
    create_container_engines = {
        'space': preparation.create_space,
        'project': preparation.create_project,
    }
    status_logger.log_status(msg="Creating project/space...",
                             percentage=5
                             )
    create_container_engine = create_container_engines.get(archive_type, preparation.create_space)
    logger.log_info("Creating {archive_type} for imported content...".format(archive_type=archive_type))
    container_id = create_container_engine(client=client, name=container_name, desc=container_desc)
    logger.log_info("Created {archive_type} with ID {container_id}...".format(archive_type=archive_type, container_id=container_id))

    # Start import process
    logger.log_info("Uploading assets to {archive_type}...".format(archive_type=archive_type))
    status_logger.log_status(msg="Importing project/space...",
                             percentage=10
                             )
    space_id, files = import_engine.execute(client, container_id, archive_type, translated_archive, args.import_timeout)
    status_logger.log_status(msg="Import is completed...",
                             status="succeeded",
                             percentage=100,
                             completed=True
                             )

    if args.output_file is not None:
        assets = manage_wml_assets.list_assets(client=client, space_id=space_id, asset_types=None, ids=None,
                                  names=None)
        assets['space_id'] = space_id
        output_file_dir = os.path.dirname(args.output_file)
        Path(output_file_dir).mkdir(parents=True, exist_ok=True)
        with open(args.output_file, 'w') as file:
            file.write(json.dumps(assets))

    return space_id, files
