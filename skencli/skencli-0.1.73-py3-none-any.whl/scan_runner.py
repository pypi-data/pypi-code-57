import os
import json
import sys
import time

from .utils import Utils, DockerError, S3Error
from threading import Timer

STATUS_RUNNING = 'RUNNING'
STATUS_ERROR_ETL_BLOCKED = 'ERROR_ETL_BLOCKED'
STATUS_ERROR = 'ERROR'

class ETLError(Exception):
    pass

class ScanRunner(object):
    aws_config = None
    scan_data_items = None
    api_id = None
    app_id = None
    app_number_id = None
    build_dir = None
    etl_retry = False
    timer_delay = 0.01
    max_scanner_running_threshold = None
    ignore_limit = False
    file_count = 0
    line_count = 0

    @classmethod
    def get_scan_data(cls, req):
        print('Getting scan data')
        http = Utils.get_retryable_http()
        try:
            headers = {"Content-Type": "application/json"}
            resp = http.post(Utils.SKEN_SERVER_BASE_URL +
                             '/getScanData', headers=headers, data=json.dumps(req))
            result = resp.json()

            if not result['success']:
                if 'errorMessage' in result and result['errorMessage'] is not None:
                    print('sken.ai is currently unable to scan your project. ' +
                        result['errorMessage'])
                    exit(-1)
                else:
                    print('Failed to get scan data from server: ' +
                        str(result['message']))
                    exit(-1)

            cls.aws_config = result['awsConfig']
            cls.scan_data_items = result['scanDataItems']
            cls.app_number_id = result['appId']
            cls.max_scanner_running_threshold = result['maxScannerRunningThreshold']
        except Exception as e:
            print('Failed to get scan data from server: ' + str(e))
            exit(-1)

    @classmethod
    def _create_etl_request(cls):
        req = {
            'appId': cls.app_id,
            'apiId': cls.api_id,
            'scanDataItems': cls.scan_data_items
        }

        return req

    @classmethod
    def _mark_error_item(cls):
        scan_data = None
        for item in cls.scan_data_items:
            if item['status'] == STATUS_RUNNING:
                scan_data = item
                break
        
        if scan_data is not None:
            scan_data['status'] = STATUS_ERROR
            return True
        else:
            return False

    @classmethod
    def do_etl(cls):
        print('ETL started')
        req = cls._create_etl_request()

        http = Utils.get_retryable_http()
        resp_text = ''

        try:
            headers = {"Content-Type": "application/json"}
            resp = http.post(Utils.SKEN_SERVER_BASE_URL +
                             '/doETL', headers=headers, data=json.dumps(req), timeout=300)
            resp_text = resp.text
            result = resp.json()

            if not result['success']:
                print(result['message'])
                # retry one more time to mark current running item to error
                if not cls.etl_retry and cls._mark_error_item():
                    cls.etl_retry = True
                    Timer(cls.timer_delay, cls.do_etl).start()
                else:
                    cls.etl_retry = False
                    cls._mark_error_item()
                    Timer(cls.timer_delay, cls.run_next_scan).start()
            else:
                cls.etl_retry = False
                cls.scan_data_items = result['scanDataItems']
                Timer(cls.timer_delay, cls.run_next_scan).start()
        except Exception as e:
            print('Failed to trigger ETL: ' + str(e) + ', response: ' + resp_text)
            # retry one more time to mark current running item to error
            if not cls.etl_retry and cls._mark_error_item():
                cls.etl_retry = True
                Timer(cls.timer_delay, cls.do_etl).start()
            else:
                cls.etl_retry = False
                cls._mark_error_item()
                Timer(cls.timer_delay, cls.run_next_scan).start()

    @classmethod
    def run_docker(cls, scan_data):
        # docker login
        client = Utils.docker_login(cls.aws_config)
        scanner = scan_data['scanner']
        parameters = scan_data['parameters']
        # pull image
        docker_image = parameters['dockerImageURI']
        print('Pulling latest image for %s ' % scanner)
        Utils.docker_pull_image(client, docker_image)

        output_file = cls.build_dir + scan_data['outputFile']
        print('Scanning started')
        volumes = {cls.build_dir: {'bind': '/scan', 'mode': 'rw'}}

        if parameters['volumes'] is not None:
           volumes = parameters['volumes']

        command_line = ''
        if parameters['commandLine'] is not None:
           command_line = parameters['commandLine']

        try:
            start_time = Utils.get_timestamp()
            container = client.containers.run(docker_image, command_line, volumes=volumes, detach=True, tty=False, stdout=True, stderr=True)
            # Terminate scans if running > xx minutes
            if not cls.ignore_limit and cls.max_scanner_running_threshold is not None:
                container.stop(timeout=cls.max_scanner_running_threshold*60)
            result = container.wait()
            
            # todo: handle more exit codes, see: https://medium.com/better-programming/understanding-docker-container-exit-codes-5ee79a1d58f6
            if result['StatusCode'] == Utils.container_exit_code_kill:
                end_time = Utils.get_timestamp()
                minutes = int((end_time - start_time)/60)
                Utils.save_stdout(scanner, 'Error: ' + scanner + ' took too long. Time taken so far: ' + str(minutes) + ' minutes.')
                raise DockerError('Error: ' + scanner + ' took too long. Time taken so far: ' + str(minutes) + ' minutes.', 'Running time too long: ' + str(minutes) + ' minutes')
        except Exception as de:
            if isinstance(de, DockerError):
                raise de
            else:
                raise DockerError('Failed to run docker image: ' + str(de), None)

        # write stdout and stderr output
        try:
            Utils.save_stdout(scanner, container.logs(stdout=True, stderr=False).decode('UTF-8'))
            Utils.save_stderr(scanner, container.logs(stdout=False, stderr=True).decode('UTF-8'))
        except Exception as e:
            # ignore this exception
            Utils.noop()

        if os.path.exists(output_file):
            print('Scanning completed. Output file: ' + output_file)
        else:
            print('Scanning completed')

        return output_file
        
    @classmethod
    def run_scan(cls, scan_data):
        # run docker
        try:
            if scan_data['status'] == STATUS_ERROR_ETL_BLOCKED:
                Utils.etl_waiting_countdown()
                scan_data['status'] = STATUS_RUNNING

            start_time = Utils.get_timestamp()
            print(('Launching scanner ' + scan_data['scanner']).ljust(50, ' '))
            output_file = cls.run_docker(scan_data)
            #output_file = cls.build_dir + scan_data['outputFile']
            # upload file
            file_empty = False
            if os.path.exists(output_file):
                file_empty = os.path.getsize(output_file) <= 0
            else:
                file_empty = True
            
            if not file_empty:
                Utils.upload_output(cls.aws_config, str(cls.app_number_id), str(scan_data['scanId']), output_file)
                scan_data['timestamp'] = str(scan_data['scanId'])
                scan_data['fileEmpty'] = False
            else:
                scan_data['fileEmpty'] = True

            scan_data['endTime'] = Utils.get_formated_timestamp_timezone()

            cls.do_etl()
            print(scan_data['scanner'] + ' scan completed. Time taken: ' + Utils.convert_seconds_to_time(Utils.get_timestamp() - start_time) + ', ' + format(cls.file_count, ',d') + ' files, ' + format(cls.line_count, ',d') + ' lines.')
        except DockerError as e:
            print(e.cli_message)
            # docker error found, set the current running data item to ERROR
            scan_data['status'] = STATUS_ERROR

            if e.server_message is not None:
                scan_data['errorMessage'] = e.server_message
            else:
                scan_data['errorMessage'] = e.cli_message

            cls.do_etl()
        except S3Error as e:
            print(str(e))
            # S3 error found, set the current running data item to ERROR
            scan_data['status'] = STATUS_ERROR
            scan_data['errorMessage'] = str(e)

            cls.do_etl()

    @classmethod
    def run_next_scan(cls):
        # pick up the scan data in running status
        scan_data = None
        for item in cls.scan_data_items:
            if item['status'] == STATUS_RUNNING or item['status'] == STATUS_ERROR_ETL_BLOCKED:
                scan_data = item
                break

        if scan_data is None:
            # all completed/error
            # remove skenoutput folder if all scans succeed
            error_occurred = False
            for item in cls.scan_data_items:
                if item['status'] == STATUS_ERROR:
                    error_occurred = True
                    break
            if not error_occurred:
                Utils.delete_skenoutput_folder()

            exit(0)

        cls.run_scan(scan_data)

    @classmethod
    def run(cls, req):
        # get initial scan data items
        cls.app_id = req['appid']
        cls.api_id = req['apiid']
        cls.build_dir = req['buildDir']
        cls.ignore_limit = req['ignoreLimit']
        cls.file_count = req['files']
        cls.line_count = req['linesOfCode']
        Utils.create_skenoutput_folder(cls.build_dir + 'skenoutput')

        cls.get_scan_data(req)
        if len(cls.scan_data_items) == 0:
            print('No scans to run.')
            exit(-1)

        # pick up the scan data in running status
        scan_data = None
        for item in cls.scan_data_items:
            if item['status'] == STATUS_RUNNING or item['status'] == STATUS_ERROR_ETL_BLOCKED:
                scan_data = item
                break

        if scan_data is None:
            print('No running scan found.')
            exit(-1)

        cls.run_scan(scan_data)
