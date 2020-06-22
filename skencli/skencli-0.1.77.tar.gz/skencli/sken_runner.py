import os
import argparse
#import http
from .scan_runner import ScanRunner
from .utils import Utils

#http.client.HTTPConnection.debuglevel = 1
LANGUAGES = ['ruby', 'javascript', 'typescript', 'python2', 'python3', 'python', 'php',
             'java', 'license', 'go']
SCANNERS = ['sast', 'dast', 'sca', 'secrets']
BUILD_TOOLS = ['jenkins', 'travis']

def get_build_dir(command_args):
    build_dir = ''
    if command_args.path is not None:
        build_dir = command_args.path
    elif 'WORKSPACE' in os.environ:
        build_dir = os.environ['WORKSPACE']
    elif 'TRAVIS_BUILD_DIR' in os.environ:
        build_dir = os.environ['TRAVIS_BUILD_DIR']
    else:
        build_dir = os.getcwd()

    build_dir = Utils.add_path_separator(build_dir)

    return build_dir

def parse_command_line_params():
    parser = argparse.ArgumentParser(description='Sken Runner.')

    parser.add_argument('--api_id', metavar='API Id', help='API Id.')
    parser.add_argument('--app_id', metavar='Application Id', help='Application Id.')
    parser.add_argument('--scanner', metavar='Scanner', nargs='+', choices=SCANNERS, help='support scanners: ' + ','.join(SCANNERS))
    parser.add_argument('--lang', metavar='Language', nargs='+', choices=LANGUAGES, help='support languages: ' + ','.join(LANGUAGES))
    parser.add_argument('--path', metavar='Project path', help='path of the project to be scanned.')
    parser.add_argument('--build_tool', metavar='Build tool', choices=BUILD_TOOLS, help='Support build tools: ' + ','.join(BUILD_TOOLS))

    parser.add_argument('--var_dast_url', metavar='DAST URL', help='URL to be scanned.')
    parser.add_argument('--var_dast_full_scan', metavar='DAST full scan', choices=['yes', 'no'], help='DAST full scan or quick scan.')
    parser.add_argument('--var_dast_login_url', metavar='DAST login URL', help='DAST login URL.')
    parser.add_argument('--var_dast_login_body', metavar='DAST login body', help='DAST login body.')
    parser.add_argument('--var_dast_username', metavar='DAST login username', help='DAST login username.')
    parser.add_argument('--var_dast_password', metavar='DAST login password', help='DAST login password.')

    parser.add_argument('--var_findsecgubs_exclude_path', metavar='Exclude path of Findsecbugs scanner', help='Exclude path of Findsecbugs scanner.')
    parser.add_argument('--var_nodejsscan_exclude_path', metavar='Exclude path of NodeJsScan scanner', help='Exclude path of NodeJsScan scanner.')
    parser.add_argument('--var_maven_repo_path', metavar='Maven repo path', help='Maven repo path.')
    parser.add_argument('--var_gradle_repo_path', metavar='Gradle repo path', help='Gradle repo path.')
    parser.add_argument('--version', action='store_true', help='View skencli Version.')
    parser.add_argument('--ignore-limit', action='store_true', help='Ignore file and loc limits.')

    command_args = parser.parse_args()

    if command_args.version:
        print('Skencli: ' + version())
        exit(0)

    command_line_params = {
        'buildtool': command_args.build_tool,
        'scanner': command_args.scanner,
        'variables':  {
            'DAST_FULL_SCAN': command_args.var_dast_full_scan == 'yes',
            'DAST_URL': command_args.var_dast_url,
            'DAST_LOGINURL': command_args.var_dast_login_url,
            'DAST_LOGINBODY': command_args.var_dast_login_body,
            'DAST_USERNAME': command_args.var_dast_username,
            'DAST_PASSWORD': command_args.var_dast_password,
            'FINDSECBUGS_EXCLUDE_PATH': command_args.var_findsecgubs_exclude_path,
            'NODEJSSCAN_EXCLUDE_PATH': command_args.var_nodejsscan_exclude_path
        }
    }

    if command_args.scanner is not None:
        command_line_params['scanner'] = ','.join(Utils.remove_duplicated_items_list(command_args.scanner))
    if command_args.lang is not None:
        languages = []
        for language in command_args.lang:
            if language == 'python3':
                language = 'python'

            languages.append(language)

        command_line_params['language'] = Utils.remove_duplicated_items_list(languages)

    return command_line_params, command_args

def get_app_ids(command_args, yaml_config):
    api_id = ''
    app_id = ''

    if 'apiid' in yaml_config and yaml_config['apiid'] is not None:
        api_id = yaml_config['apiid']
    
    if command_args.api_id is not None:
        api_id = command_args.api_id

    if not api_id:
        print('Please specify "apiid" in sken.yaml or use --api_id flag.')
        exit(-1)

    if 'appid' in yaml_config and yaml_config['appid'] is not None:
        app_id = yaml_config['appid']
    
    if command_args.app_id is not None:
        app_id = command_args.app_id

    if not app_id:
        print('Please specify "apiid" in sken.yaml or use --api_id flag.')
        exit(-1)

    return api_id, app_id

def check_language(command_line_params, yaml_config):
    scanners = ''
    if 'scanner' in yaml_config and yaml_config['scanner'] is not None:
        scanners = yaml_config['scanner']
    if 'scanner' in command_line_params and command_line_params['scanner'] is not None:
        scanners = command_line_params['scanner']

    yaml_language = []
    if 'language' in yaml_config and yaml_config['language'] is not None:
        languages = yaml_config['language'].split(',')
        for language in languages:
            if language in LANGUAGES:
                if language == 'python3':
                    language = 'python'

                yaml_language.append(language)
            else:
                print("Scanner for %s hasn't been supported." % language)

    if len(yaml_language) > 0:
        yaml_config['language'] = Utils.remove_duplicated_items_list(yaml_language)
    elif 'language' in yaml_config:
        del yaml_config['language']

    return 'language' in yaml_config or 'language' in command_line_params or (scanners != '' and scanners.find('sast') < 0)

def version():
    return '0.1.77'

def main():
    command_line_params, command_args = parse_command_line_params()
    Utils.assert_docker_alive()
    Utils.assert_docker_version()

    build_dir = get_build_dir(command_args)
    succeed, yaml_config = Utils.read_config(build_dir)
    api_id, app_id = get_app_ids(command_args, yaml_config)

    awsconfig = Utils.get_aws_config(app_id, api_id)
    # count files and loc
    files, lines_of_code = Utils.count_file_code(awsconfig, build_dir)

    if not check_language(command_line_params, yaml_config):
        command_line_params['language'] = Utils.detect_lang(awsconfig, build_dir, LANGUAGES)

    # initial scan data items
    ScanRunner.run({
        'apiid': api_id, 
        'appid': app_id, 
        'buildDir': build_dir,
        'files': files, 
        'linesOfCode': lines_of_code, 
        'commandLine': command_line_params, 
        'yaml': yaml_config,
        'environment_variables': Utils.get_env_variables(command_args, yaml_config),
        'ignoreLimit': command_args.ignore_limit
        })

if __name__ == "__main__":
    main()