import docker
import boto3
from botocore.config import Config
import base64
import subprocess
from datetime import datetime
import time
import sys
import os
import json
import ntpath
import shutil
import platform
from xml.dom.minidom import parse
import requests
import yaml
import logging
import math

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class DockerError(Exception):
    def __init__(self, cli_message, server_message):
        self.cli_message = cli_message
        self.server_message = server_message

class S3Error(Exception):
    pass

class Utils(object):
	sken_output_foler = ''
	linguist_image = '621002179714.dkr.ecr.us-east-1.amazonaws.com/linguist:latest'
	cloc_image = '621002179714.dkr.ecr.us-east-1.amazonaws.com/cloc:latest'
	SKEN_SERVER_BASE_URL = 'https://cli.sken.ai/api/cli/v1'
	#SKEN_SERVER_BASE_URL = 'http://localhost:8080/api/cli/v1'
	http = None
	last_time_docker_login = 0
	minutes25 = 60*25
	cloc_file = None
	min_docker_version = 18.03
	# if a scanner for an app id is executed too close in time, skencli must wait for 5 minutes
	etl_waiting_threshold = 300
	# docker container exit code 137: Indicates failure as container received SIGKILL
	container_exit_code_kill = 137
	# retrying upload to s3
	upload_retry = False

	@classmethod
	def get_retryable_http(cls):
		if cls.http is not None:
			return cls.http

		retry_strategy = Retry(
			total=10,
			backoff_factor=2,
			status_forcelist=[429, 500, 502, 503, 504],
			method_whitelist=["HEAD", "GET", "OPTIONS", "POST"]
		)

		adapter = HTTPAdapter(max_retries=retry_strategy)
		cls.http = requests.Session()
		cls.http.mount("https://", adapter)
		cls.http.mount("http://", adapter)

		return cls.http

	@classmethod
	def assert_docker_alive(cls):
		try:
			client = docker.from_env()
			client.ping()
		except Exception as e:
			print('No running docker client found, please ensure the docker client is running.')
			print(str(e))
			exit(-1)
	
	@classmethod
	def assert_docker_version(cls):
		try:
			client = docker.from_env()
			version_info = client.version()
			version_parts = version_info['Version'].split('.')
			version_number = float(version_parts[0] + '.' + version_parts[1])

			if version_number < cls.min_docker_version:
				print("We don't support the docker version you're running, please upgrade to " + str(cls.min_docker_version) + " or higher.")
				exit(-1)
		except Exception as e:
			print('Error occurred when checking the docker version, please contact support.')
			print(str(e))
			exit(-1)

	@classmethod
	def docker_login(cls, scan_info):
		# no need to login again within 30 minutes
		now = cls.get_timestamp()
		if (now - cls.last_time_docker_login) < cls.minutes25:
			return docker.from_env()

		print('Logging in to docker')
		session = boto3.Session(
			aws_access_key_id=scan_info['accessKeyId'], 
			aws_secret_access_key=scan_info['secretAccessKey'], 
			region_name=scan_info['region'])

		ecr_client = session.client('ecr')
		try:
			token = ecr_client.get_authorization_token()
			ecr_username, ecr_password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')
			registry = token['authorizationData'][0]['proxyEndpoint']
		except Exception as e:
			raise DockerError('Login to docker failed while getting ECR authorization token: ' + str(e), None)

		command = ['docker', 'login', '-u', ecr_username, '--password-stdin', registry]
		if sys.version_info < (3, 0):
			command = ['docker login -u ' + ecr_username + ' --password-stdin ' + registry]

		p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, shell=True)
		stdout, stderr = p.communicate(input=ecr_password.encode('utf-8'))
		p.wait()

		if stdout is not None and stdout.decode('utf-8').find('Login Succeeded') >= 0:
			print('Login to docker succeeded.')
		else:
			raise DockerError('Login to docker failed: ' + stdout.decode('utf-8'), None)

		client = docker.from_env()
		cls.last_time_docker_login = cls.get_timestamp()
		"""
		below code doesn't work even it returns 'Login succeeded', see https://github.com/docker/docker-py/issues/2256
		client = docker.from_env()
		try:
			client.login(username=ecr_username, password=ecr_password, registry=registry, reauth=False)
		except Exception as e:
			print('Failed to login to docker: ' + str(e))
			exit(-1)
		"""

		return client

	@classmethod
	def docker_pull_image(cls, docker_client, image):
		"""
		command = ['docker', 'image', 'pull', image]
		if sys.version_info < (3, 0):
			command = ['docker image pull ' + image]
			
		p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
		for line in iter(p.stdout.readline, b''):
			line = line.rstrip().decode('utf8')
			print(line)
		p.stdout.close()
		p.wait()
		"""
		try:
			docker_client.images.pull(image)
		except Exception as e:
			# pull failed, check if the image exists, if true then use the current version, otherwise raise error
			try:
				docker_client.images.get(image)
			except Exception as de:
				raise DockerError('Failed to pull image: ' + str(e), None)

		
	@classmethod
	def get_timestamp(cls):
		now = datetime.now()
		try:
			return round(now.timestamp())
		except Exception as e:
			return int(round(time.mktime(now.timetuple())))

	@classmethod
	def get_formated_timestamp_timezone(cls):
		now = cls.get_timestamp()
		return datetime.strftime(datetime.utcfromtimestamp(now),'%Y-%m-%dT%H:%M:%SZ')

	@classmethod
	def get_formated_timestamp(cls):
		now = cls.get_timestamp()
		return datetime.strftime(datetime.utcfromtimestamp(now),'%Y%m%d%H%M%S')

	@classmethod
	def create_skenoutput_folder(cls, dir):
		cls.sken_output_foler = dir

		if not os.path.exists(dir):
			os.makedirs(dir)
			os.chmod(dir, 0o777)

	@classmethod
	def delete_skenoutput_folder(cls):
		if os.path.exists(cls.sken_output_foler):
			shutil.rmtree(cls.sken_output_foler)

	@classmethod
	def save_stdout(cls, scanner, content):
		if not content:
			return
		if sys.version_info < (3, 0):
			content = content.encode('utf-8')

		with open(cls.sken_output_foler + os.path.sep + scanner + '-stdout.txt', 'w') as f:
			f.write(content)

	@classmethod
	def save_stderr(cls, scanner, content):
		if not content:
			return
		if sys.version_info < (3, 0):
			content = content.encode('utf-8')

		with open(cls.sken_output_foler + os.path.sep + scanner + '-stderr.txt', 'w') as f:
			f.write(content)

	@classmethod
	def detect_lang(cls, scan_info, build_dir, support_languages):
		print('Warning: no "language" specified in sken.yaml and --lang flag. Auto-detecting language...')
		client = cls.docker_login(scan_info)
		cls.docker_pull_image(client, cls.linguist_image)
		container = client.containers.run(cls.linguist_image, volumes={build_dir: {
			'bind': '/scan', 'mode': 'rw'}}, detach=True, tty=False, stdout=True, stderr=True)
		container.wait()
		print(container.logs().decode('UTF-8'))

		lang_file = build_dir + 'sken-lang.json'
		if not os.path.exists(lang_file):
			exit(-1)

		languages = []
		with open(lang_file, 'r') as f:
			data = json.load(f)
			detected_languages = data['languages']
			for language in detected_languages:
				if language.lower() in support_languages:
					languages.append(language.lower())
			
		if len(languages) > 0:
			print('Detected languages: ' + ', '.join(languages))
		else:
			print('No support languages detected.')
			exit(-1)

		if os.path.exists(lang_file):
			os.remove(lang_file)

		return languages

	@classmethod
	def count_file_code(cls, scan_info, build_dir):
		print('Counting files and lines of code')
		files = None
		lines_of_code = None
		try:
			client = cls.docker_login(scan_info)
			cls.docker_pull_image(client, cls.cloc_image)
			command_line = "/scan --json --out /scan/sken-cloc.json  --exclude-dir node_modules,target,dist,build,node,.git,.hg,tests,tmp,temp,docs --skip-archive '(zip|tar|jar|war(.(gz|Z|bz2|xz|7z))?)' --exclude-ext json,xml,svg,md"
			container = client.containers.run(cls.cloc_image, command_line, volumes={build_dir: {
				'bind': '/scan', 'mode': 'rw'}}, detach=True, tty=False, stdout=True, stderr=True)
			container.wait()

			cls.cloc_file = build_dir + 'sken-cloc.json'
			if not os.path.exists(cls.cloc_file):
				return files, lines_of_code

			with open(cls.cloc_file, 'r') as f:
				data = json.load(f)
				if 'SUM' in data:
					files = data['SUM']['nFiles']
					lines_of_code = data['SUM']['code']
		except Exception as e:
			print('Failed to count files and lines of code: ' + str(e))
			
		return files, lines_of_code

	@classmethod
	def _get_m2_from_settings(cls, settings_file):
		try:
			dom = parse(settings_file)
			root = dom.documentElement
			node_list = root.getElementsByTagName('localRepository')

			if node_list.length > 0:
				if node_list[0].childNodes.length > 0:
					return node_list[0].childNodes[0].data
		except Exception as e:
			return ''

	@classmethod
	def _get_maven_home(cls):
		command = ['mvn', '--version']
		if sys.version_info < (3, 0) or platform.system() == 'Linux':
			command = ['mvn --version']

		p = subprocess.Popen(command, stdout=subprocess.PIPE,
							stderr=subprocess.STDOUT, shell=True)

		maven_home = ''
		for line in iter(p.stdout.readline, b''):
			line = line.rstrip().decode('utf8')
			try:
				if line.index('Maven home') == 0:
					maven_home = line.split(': ')[1]
			except ValueError:
				continue
		p.stdout.close()
		p.wait()

		return maven_home

	@classmethod
	def find_m2_location(cls):
		# check if ${user.home}/.m2/settings.xml exists
		m2_location = ''
		user_home = cls.add_path_separator(os.path.expanduser('~'))

		if os.path.exists(user_home + '.m2/settings.xml'):
			m2_location = cls._get_m2_from_settings(user_home + '.m2/settings.xml')

		if m2_location:
			#print('found m2 location from user settings: ' + m2_location)
			return m2_location

		# find maven home
		maven_home = cls._get_maven_home()
		# check ${maven.home}/conf/settings.xml exists
		if maven_home:
			maven_home = cls.add_path_separator(maven_home)
			if os.path.exists(maven_home + 'conf/settings.xml'):
				m2_location = cls._get_m2_from_settings(maven_home + 'conf/settings.xml')

				if m2_location:
					#print('found m2 location from global settings: ' + m2_location)
					return m2_location
				else:
					# use default location
					return user_home + '.m2'

		return ''

	@classmethod
	def find_gradle_location(cls):
		# detect gradle user home
		user_home = cls.add_path_separator(os.path.expanduser('~'))

		gradle_user_home = user_home + '.gradle' + os.path.sep

		if 'GRADLE_USER_HOME' in os.environ and os.environ['GRADLE_USER_HOME'] is not None:
			gradle_user_home = cls.add_path_separator(os.environ['GRADLE_USER_HOME'])

		cache_location = gradle_user_home + 'caches' + os.path.sep + 'modules-2' + os.path.sep + 'files-2.1' + os.path.sep

		if os.path.exists(cache_location):
			return cache_location

		return ''

	@classmethod
	def add_path_separator(cls, path_str):
		if not path_str.endswith(os.path.sep):
			path_str = path_str + os.path.sep
		
		return path_str
	
	"""
	Read config from sken.yaml
	"""
	@classmethod
	def read_config(cls, build_dir):
		sken_config = {}
		succeed = False
		if os.path.exists(build_dir + 'sken.yaml'):
			with open(build_dir + 'sken.yaml', 'r') as stream:
				try:
					sken_config = yaml.safe_load(stream)
					succeed = True
				except yaml.YAMLError as exc:
					print('Read '+(build_dir + 'sken.yaml')+' failed, please check the content.')
					logging.exception(exc)
					exit(-1)
		else:
			print('File not found: %s' % (build_dir + 'sken.yaml'))

		return succeed, sken_config

	@classmethod
	def get_aws_config(cls, app_id, api_id):
		http = cls.get_retryable_http()
		try:
			resp = http.get(cls.SKEN_SERVER_BASE_URL + '/getAwsConfig', params={'appId': app_id, 'apiId': api_id})
			result = resp.json()

			if not result['success']:
				print('Failed to get aws config: ' + result['message'])
				exit(-1)

			return result

		except Exception as x:
			print('Failed to get aws config: ' + str(x))
			exit(-1)

	@classmethod
	def get_env_variables(cls, command_args, yaml_config):
		# home dir of jenkins and travis
		variables = {}
		if 'WORKSPACE' in os.environ:
			variables['jenkins_home_dir'] = os.environ['WORKSPACE']
		if 'TRAVIS_BUILD_DIR' in os.environ:
			variables['travis_home_dir'] = os.environ['TRAVIS_BUILD_DIR']
		
		# repo dir of maven and gradle
		if command_args.var_maven_repo_path is not None:
			variables['maven_repo_path'] = command_args.var_maven_repo_path
		elif 'variables' in yaml_config and 'MAVEN_REPO_PATH' in yaml_config['variables'] and yaml_config['variables']['MAVEN_REPO_PATH'] is not None:
			variables['maven_repo_path'] = yaml_config['variables']['MAVEN_REPO_PATH']
		else:
			variables['maven_repo_path'] = cls.find_m2_location()

		if command_args.var_gradle_repo_path is not None:
			variables['gradle_repo_path'] = command_args.var_gradle_repo_path
		elif 'variables' in yaml_config and 'GRADLE_REPO_PATH' in yaml_config['variables'] and yaml_config['variables']['GRADLE_REPO_PATH'] is not None:
			variables['gradle_repo_path'] = yaml_config['variables']['GRADLE_REPO_PATH']
		else:
			variables['gradle_repo_path'] = cls.find_gradle_location()

		return variables

	@classmethod
	def upload_output(cls, aws_config, app_id, scan_id, output_file):
		print('Uploading output file...')
		file_name = ''
		output_file_handle = None
		cloc_file_handle = None

		try:
			config = Config(
				retries = dict(
					max_attempts = 3
				)
			)

			session = boto3.Session(
				aws_access_key_id=aws_config['accessKeyId'], 
				aws_secret_access_key=aws_config['secretAccessKey'], 
				region_name=aws_config['region'])

			s3 = session.resource('s3', config=config)
			file_name = ntpath.basename(output_file)
			output_file_handle = open(output_file, 'rb')
			s3.Bucket('sken-scanner-output').put_object(Key=app_id + '/' + scan_id + '/' + file_name, Body=output_file_handle)

			# upload cloc file
			try:
				if cls.cloc_file is not None and os.path.exists(cls.cloc_file):
					cloc_file_handle = open(cls.cloc_file, 'rb')
					s3.Bucket('sken-scanner-output').put_object(Key=app_id + '/' + scan_id + '/sken-cloc.json', Body=cloc_file_handle)
			except Exception as ce:
				# ignore
				cls.noop()
		
			print('Output file uploaded')
		except Exception as e:
			# retry one more time
			if not cls.upload_retry:
				print('Failed to upload output file, retrying. ' + str(e))
				cls.upload_retry = True
				return cls.upload_output(aws_config, app_id, scan_id, output_file)
			else:
				cls.upload_retry = False
				raise S3Error('Failed to upload output file: ' + str(e))
		finally:
			try:
				if output_file_handle is not None:
					output_file_handle.close()
				if cloc_file_handle is not None:
					cloc_file_handle.close()
					os.remove(cls.cloc_file)
					cls.cloc_file = None
			except Exception as fe:
				# ignore
				cls.noop()

		return scan_id

	@classmethod
	def remove_duplicated_items_list(cls, list_object):
		if list_object is None:
			return []

		return list(dict.fromkeys(list_object))

	@classmethod
	def etl_waiting_countdown(cls):
		count = cls.etl_waiting_threshold
		while count > 0:
			minute = str(int(math.floor(count/60))).zfill(2)
			seconds = str(count % 60).zfill(2)
			sys.stdout.write('Previous scan ETL is processing, wait for ' + minute + ':' + seconds)
			sys.stdout.write("\r")
			sys.stdout.flush()
			count -= 1
			time.sleep(1)

	@classmethod
	def noop(cls):
		pass

	@classmethod
	def convert_seconds_to_time(cls, seconds):
		m, s = divmod(seconds, 60)
		h, m = divmod(m, 60)
		return '{:d}:{:02d}:{:02d}'.format(h, m, s)
