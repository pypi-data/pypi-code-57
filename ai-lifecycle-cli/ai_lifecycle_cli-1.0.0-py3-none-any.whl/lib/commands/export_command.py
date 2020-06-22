#  © Copyright IBM Corporation 2020.

from ai_lifecycle_cli.lib.clients.rest_client import RESTClient
from ai_lifecycle_cli.lib.utils.FsHandler import FsHandler
from ai_lifecycle_cli.lib.utils.LoggingHandler import LoggingHandler
from ai_lifecycle_cli.lib.utils.CPDStatusHandler import CPDStatusHandler
from ai_lifecycle_cli.lib.actions import export_wml_assets, export_wml_assets_v25, preparation
import json
import os


# 'export' command
def do_export(args):

    # Initialize default dir
    fs = FsHandler()
    fs.setup_dir(args.temp_dir)

    # Create output dir
    fs.setup_dir(os.path.dirname(args.output_dir))

    # Define loggers
    logger = LoggingHandler()
    status_logger = CPDStatusHandler(args.temp_dir, "export")

    # Initialize REST Client
    logger.log_debug("Exporting assets...")
    client = RESTClient(args.cpd_url, (args.cpd_user, args.cpd_pass))

    # Detect CP4D version of source environment to choose export logic
    source_version = args.export_version
    if source_version is None:
        source_version = preparation.detect_source_environment(client)
    else:
        source_version = preparation.detect_source_environment(client, source_version=source_version)
        if source_version == 'invalid':
            logger.log_error("Detected version is not supported or you are providing wrong version as an argument.")
            status_logger.log_status(msg="Module wml-aux does not support WML in CP4D 2.5 cluster...",
                                     status="failed",
                                     percentage=100,
                                     completed=True
                                     )
            return
    logger.log_debug("Detected environment in version {ver}".format(ver=source_version))
    export_engines = {
        '2.5': export_wml_assets_v25,
        '3.0': export_wml_assets
    }
    status_logger.log_status(msg="Selecting export engine...",
                             percentage=0
                             )
    export_engine = export_engines.get(source_version, export_wml_assets)

    # Load export specification and resolve which assets needs to be exported
    with open(str(args.export_json_file), 'r') as source_file:
        sources = json.load(source_file)

    status_logger.log_status(msg="Resolving asset dependencies...",
                             percentage=5
                             )
    is_shallow = source_version in ['3.0']
    resolved_sources = preparation.resolve_dependencies(client, sources, shallow=is_shallow)

    # Start export process
    status_logger.log_status(msg="Exporting project/space...",
                             percentage=10
                             )
    serialized, files = export_engine.execute(client, resolved_sources, args.export_timeout)
    logger.log_info("Finished exporting assets...")

    # Pack exported assets into proper format
    status_logger.log_status(msg="Packaging exported assets...",
                             percentage=95
                             )
    if len(serialized) > 0:
        archive_list = fs.archive_dirs(serialized, args.output_dir)
        logger.log_info("Archived assets to {archives}".format(archives=archive_list))
        if args.archive_all:
            dest = fs.archive_files(archive_list, args.output_dir)
            logger.log_info("Archived all packages to {dest}".format(dest=dest))
    if len(serialized) == 0 and len(files) > 0:
        dest_paths = fs.move_files(files, args.output_dir)
        logger.log_info("Archived assets to {archives}".format(archives=dest_paths))
        if args.archive_all:
            dest = fs.archive_files(dest_paths, args.output_dir)
            logger.log_info("Archived all packages to {dest}".format(dest=dest))
    status_logger.log_status(msg="Export is completed...",
                             status="succeeded",
                             percentage=100,
                             completed=True
                             )
