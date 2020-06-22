#  © Copyright IBM Corporation 2020.

import argparse
import configparser
import logging
import sys
import urllib3

from ai_lifecycle_cli.lib.commands import export_command, import_command, asset_command, deployment_command, space_command, deployment_job_command
from ai_lifecycle_cli.lib.utils.LoggingHandler import LoggingHandler


urllib3.disable_warnings()

# Define command parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')
sub_parser_list = list()


# 'export' command parser
export_parser = subparsers.add_parser('export',
                                      help="Exports assets from source environment")
sub_parser_list.append(export_parser)

# 'export' command arguments
export_parser.add_argument('--output_dir', type=str, required=True,
                           help="Directory, where exported content should be saved")
export_parser.add_argument('--export_json_file', type=str, required=True,
                           help="JSON file, specifying which assets to export from which projects/spaces")
export_parser.add_argument('--archive_all', action='store_true',
                           help="Archive all exported content into single ZIP archive")
export_parser.add_argument('--export_version', choices=['2.5', '3.0'], default=None,
                           help="Version of exported environment - if not provided, it'll be auto-detected")
export_parser.add_argument('--export_timeout', type=int, default=600,
                           help="Set timeout for export job in seconds")
export_parser.add_argument('--temp_dir', type=str, default="/var/tmp/ai-lifecycle-cli",
                           help="Directory for temporary files")


# 'import' command parser
import_parser = subparsers.add_parser('import',
                                      help="Import assets to target environment")
sub_parser_list.append(import_parser)

# 'import' command arguments
import_parser.add_argument('--input_file', type=str, required=True,
                           help="Path to exported archive file to be imported")
import_parser.add_argument('--import_version', choices=['3.0'], default='3.0',
                           help="Version of imported environment - if not provided, it'll be auto-detected")
import_parser.add_argument('--import_name', type=str,
                           help="Name of created container (e.g. space) during import")
import_parser.add_argument('--import_desc', type=str,
                           help="Description of created container (e.g. space) during import")
import_parser.add_argument('--import_timeout', type=int, default=600,
                           help="Set timeout for export job in seconds")
import_parser.add_argument('--output_file', type=str, required=False,
                           help="Path where import summary should be saved in JSON format")
import_parser.add_argument('--temp_dir', type=str, default="/var/tmp/ai-lifecycle-cli",
                           help="Directory for temporary files")


# 'asset' command parser
asset_parser = subparsers.add_parser('asset',
                                      help="Provides operations on assets")
asset_subparsers = asset_parser.add_subparsers(dest='asset')

# 'asset list' command parser
asset_list_parser = asset_subparsers.add_parser('list',
                                                help="List assets")
sub_parser_list.append(asset_list_parser)

# 'asset list' command arguments
asset_list_parser.add_argument('--space_id', dest='space_id', type=str, required=True,
                               help="ID of the space")
asset_list_parser.add_argument('--asset_type', dest='asset_type', type=str, required=False,
                               help="List of the asset types separated by comma")
asset_list_parser.add_argument('--id', dest='asset_id', type=str, required=False,
                               help="List of the asset IDs separated by comma")
asset_list_parser.add_argument('--name', dest='asset_name', type=str, required=False,
                               help="List of the asset names separated by comma")


# 'deployment' command parser
deployment_parser = subparsers.add_parser('deployment',
                                      help="Provides operations on deployments")
deployment_subparsers = deployment_parser.add_subparsers(dest='deployment')

# 'deployment create' command parser
deployment_create_parser = deployment_subparsers.add_parser('create',
                                                help="Create new deployment")
sub_parser_list.append(deployment_create_parser)

# 'deployment create' command arguments
deployment_create_parser.add_argument('--space_id', dest='space_id', type=str, required=True,
                                      help="ID of the space")
deployment_create_parser.add_argument('--asset_id', dest='asset_id', type=str, required=True,
                                      help="ID of the asset to deploy")
deployment_create_parser.add_argument('--asset_name', dest='asset_name', type=str, required=False,
                                      help="Name of the asset to deploy")
deployment_create_parser.add_argument('--deployment_name', dest='deployment_name', type=str, required=True,
                                      help="Name of the new deployment")
deployment_create_parser.add_argument('--deployment_type', dest='deployment_type', type=str, required=True,
                                      help="Type of the new deployment")
deployment_create_parser.add_argument('--hardware_spec_name', dest='hardware_spec_name', type=str, required=False,
                                      help="Name of hardware specification")
deployment_create_parser.add_argument('--hardware_spec_num_nodes', dest='hardware_spec_num_nodes', type=int, required=False,
                                      help="Number of nodes applied to a computation")
deployment_create_parser.add_argument('--params', dest='params', type=str, required=False,
                                      help="Params of the new deployment as a JSON string")


# 'deployment delete' command parser
deployment_delete_parser = deployment_subparsers.add_parser('delete',
                                                help="Delete existing deployment")
sub_parser_list.append(deployment_delete_parser)

# 'deployment delete' command arguments
deployment_delete_parser.add_argument('--space_id', dest='space_id', type=str, required=True,
                                      help="ID of the space")
deployment_delete_parser.add_argument('--deployment_id', dest='deployment_id', type=str, required=True,
                                      help="ID of deployment")


# 'deployment list' command parser
deployment_list_parser = deployment_subparsers.add_parser('list',
                                                help="List existing deployments")
sub_parser_list.append(deployment_list_parser)

# 'deployment list' command arguments
deployment_list_parser.add_argument('--space_id', dest='space_id', type=str, required=True,
                                      help="ID of the space")
deployment_list_parser.add_argument('--deployment_type', dest='deployment_type', type=str, required=False,
                                      help="Filter by types of deployment")


# 'space' command parser
space_parser = subparsers.add_parser('space',
                                      help="Provides operations on space")
space_subparsers = space_parser.add_subparsers(dest='space')

# 'space delete' command parser
space_delete_parser = space_subparsers.add_parser('delete',
                                                help="Delete existing space")
sub_parser_list.append(space_delete_parser)

# 'space delete' command arguments
space_delete_parser.add_argument('--space_id', dest='space_id', type=str, required=True,
                                      help="ID of the space to delete")

# 'space list' command parser
space_list_parser = space_subparsers.add_parser('list',
                                                help="List existing spaces")
sub_parser_list.append(space_list_parser)



# 'deployment-job' command parser
deployment_job_parser = subparsers.add_parser('deployment-job',
                                      help="Provides operations on deployment jobs")
deployment_job_subparsers = deployment_job_parser.add_subparsers(dest='deployment_job')

# 'deployment-job create' command parser
deployment_job_create_parser = deployment_job_subparsers.add_parser('create',
                                                help="Create new deployment job")
sub_parser_list.append(deployment_job_create_parser)

# 'deployment-job create' command arguments
deployment_job_create_parser.add_argument('--space_id', dest='space_id', type=str, required=True,
                                      help="ID of the space")
deployment_job_create_parser.add_argument('--job_spec_json', dest='job_spec_json', type=str, required=True,
                                      help="Location of job specification file")


# 'deployment-job cancel' command parser
deployment_job_delete_parser = deployment_job_subparsers.add_parser('cancel',
                                                help="Cancel deployment job")
sub_parser_list.append(deployment_job_delete_parser)

# 'deployment-job cancel' command arguments
deployment_job_delete_parser.add_argument('--space_id', dest='space_id', type=str, required=True,
                                      help="ID of the space")
deployment_job_delete_parser.add_argument('--job_id', dest='job_id', type=str, required=True,
                                      help="ID of the asset to deploy")


# 'deployment-job list' command parser
deployment_job_list_parser = deployment_job_subparsers.add_parser('list',
                                                help="List existing deployment jobs")
sub_parser_list.append(deployment_job_list_parser)

# 'deployment-job list' command arguments
deployment_job_list_parser.add_argument('--space_id', dest='space_id', type=str, required=True,
                                      help="ID of the space")


# Common arguments for all commands - url, user, pass, etc...
for sub_parser in sub_parser_list:
    sub_parser.add_argument('--cpdconfig', dest='cpdconfig', type=str, required=False,
                            help="File with CPD credentials and URL")
    sub_parser.add_argument('--url', dest='cpd_url', type=str, required='--cpdconfig' not in sys.argv,
                                            help="URL to CP4D")
    sub_parser.add_argument('--user', dest='cpd_user', type=str, required='--cpdconfig' not in sys.argv,
                                            help="Username used for CP4D login")
    sub_parser.add_argument('--pass', dest='cpd_pass', type=str, required='--cpdconfig' not in sys.argv,
                                            help="Password used for CP4D login")
    sub_parser.add_argument('--apikey', dest='iam_apikey', type=str,
                               help=argparse.SUPPRESS if True else "IAM API Key used for Cloud IAM authentication")
    sub_parser.add_argument('--token', dest='bearer_token', type=str,
                               help=argparse.SUPPRESS if True else "Bearer token used for authorization (accepted for both CP4D and Cloud)")

def _load_config(path):
    config = configparser.ConfigParser()
    config.read(path)
    flat_config = {}
    for section in config.sections():
        for key in config[section]:
            flat_config[key] = config[section][key]
    return flat_config


def main():
    args = parser.parse_args()

    logger = LoggingHandler()

    if args.command is not None and args.cpdconfig is not None:
        config = _load_config(args.cpdconfig)
        args.cpd_url = config['wml_url']
        args.cpd_user = config['username']
        args.cpd_pass = config['password']


    # Primary command logic
    if args.command == "export":
        logger.log_info("Exporting assets from {url} to {output_dir} directory".format(url=args.cpd_url,
                                                                                       output_dir=args.output_dir))
        export_command.do_export(args)

    if args.command == "import":
        logger.log_info("Importing assets to {url} from {input_file} archive".format(url=args.cpd_url,
                                                                                     input_file=args.input_file))
        import_command.do_import(args)

    if args.command == "asset":
        if args.asset is None:
            asset_parser.print_help()
            return
        asset_command.do_asset(args)

    if args.command == "deployment":
        if args.deployment is None:
            deployment_parser.print_help()
            return
        deployment_command.do_deployment(args)

    if args.command == "deployment-job":
        if args.deployment_job is None:
            deployment_job_parser.print_help()
            return
        deployment_job_command.do_deployment_job(args)

    if args.command == "space":
        if args.space is None:
            space_parser.print_help()
            return
        space_command.do_space(args)


if __name__ == '__main__':
    main()
