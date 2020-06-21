from pathlib import Path
import boto3
import os
from configparser import ConfigParser
from requests_aws4auth import AWS4Auth


class credentialsFile:
    
    def __init__(self, credential_path=None, config_path=None, profile_name=None):
        ''' Establish environment variables for boto3 authentication '''
        if profile_name is None:
            profile_name = 'test'
        if os.getenv(profile_name.upper() + '_AWS_PROFILE') is None:
            print(profile_name.upper())
            self.AWS_SHARED_CREDENTIALS_FILE = str(Path(credential_path).expanduser())
            self.AWS_CONFIG_FILE = str(Path(config_path).expanduser())
            os.environ['AWS_SHARED_CREDENTIALS_FILE'] = self.AWS_SHARED_CREDENTIALS_FILE
            os.environ['AWS_CONFIG_FILE'] = self.AWS_CONFIG_FILE
            self.credentials = ConfigParser()
            self.credentials.read(self.AWS_SHARED_CREDENTIALS_FILE)
            config = ConfigParser()
            config.read(self.AWS_CONFIG_FILE)
            os.environ['AWS_PROFILE'] = profile_name
            os.environ['AWS_ACCESS_KEY_ID'] = self.credentials[profile_name]['aws_access_key_id']
            os.environ['AWS_SECRET_ACCESS_KEY'] = self.credentials[profile_name]['aws_secret_access_key']
            os.environ['AWS_DEFAULT_REGION'] = config['profile ' + profile_name]['region']
        else:
            os.environ['AWS_ACCESS_KEY_ID'] = os.getenv(profile_name.upper() + '_AWS_ACCESS_KEY_ID', 'test')
            os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv(
                profile_name.upper() + '_AWS_SECRET_ACCESS_KEY', 'test')
            os.environ['AWS_DEFAULT_REGION'] = os.getenv(
                profile_name.upper() + '_AWS_DEFAULT_REGION', 'test')


class establishSession(credentialsFile):
    ''' Establish AWS service sessions '''
    
    def __init__(self, credential_path=None, config_path=None, profile_name=None,
                service_name=None):
        super().__init__(credential_path=credential_path, config_path=config_path,
                        profile_name=profile_name)
        self.session = boto3.Session(aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
        self.access_key = self.session.get_credentials().access_key
        self.secret_key = self.session.get_credentials().secret_key
        self.region = self.session.region_name
        self.awsauth = AWS4Auth(self.access_key, self.secret_key,
                                self.region, service_name)


class establishES(establishSession):
    ''' Establish AWS elasticsearch session '''

    def __init__(self, credential_path=None, config_path=None, profile_name=None,
                elastic_path=None, service_name='es'):
        super().__init__(credential_path=credential_path, config_path=config_path,
                        profile_name=profile_name, service_name=service_name)
        self.client = self.session.client(service_name)
        self._test = 'test'
        if elastic_path is not None:
            self.es_config = str(Path(elastic_path).expanduser())
            config = ConfigParser()
            config.read(self.es_config)
            self.es_endpoint = config['elasticsearch-endpoint']['address']
        else:
            self.es_endpoint = os.getenv(profile_name.upper() + "_ENDPOINT")


class establishS3(establishSession):
    ''' Establish connection with AWS S3 '''

    def __init__(self, credential_path=None, config_path=None, profile_name=None, service_name='s3'):
        super().__init__(credential_path=credential_path, config_path=config_path, profile_name=profile_name,
                        service_name=service_name)
        self.resource = self.session.resource(service_name)
        self.client = self.resource.meta.client


class establishQuilt(credentialsFile):
    ''' Create authentication files for quilt3 based on aws_credentials '''

    def __init__(self, credential_path=None, config_path=None, profile_name=None):
        super().__init__(credential_path=credential_path, config_path=config_path, 
                        profile_name=profile_name)
        if profile_name is None:
            profile_name = 'quilt-karrlab'
        if os.getenv(profile_name.upper() + '_AWS_PROFILE') is None:
            os.environ['EXPIRY_TIME'] = '2029-09-30T20:32:07+00:00'
