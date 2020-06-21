from boto3.s3.transfer import TransferConfig
from configparser import ConfigParser
from karr_lab_aws_manager.config import config
from karr_lab_aws_manager.s3 import util as s3_util
from pathlib import Path, PurePath
import botocore
import json
import os
import quilt3
import tempfile


class QuiltUtil(config.establishQuilt):

    def __init__(self, profile_name=None, default_remote_registry=None,
                aws_path=None, cache_dir=None, config_path=None):
        ''' Handle Quilt authentication file creation without having to use quilt3.login()

            Args:
                aws_path (:obj:`str`): directory in which aws credentials file resides
                base_path (:obj:`str`): directory to store quilt3 credentials generated from aws credentials
                profile_name (:obj:`str`): AWS credentials profile name for quilt
                default_remote_registry (:obj:`str`): default remote registry to store quilt package
                cache_dir (:obj:`str`): default directory to store data
                config_path (:obj:`str`): directory in which aws config file resides
        '''
        super().__init__(credential_path=aws_path,
                         config_path=config_path,
                         profile_name=profile_name)
        self.cache_dir = cache_dir
        self.profile_name = profile_name
        base_path_obj = Path(self.cache_dir)
        quilt3.session.AUTH_PATH = base_path_obj / 'auth.json'
        quilt3.session.CREDENTIALS_PATH = base_path_obj / 'credentials.json'
        quilt3.session.AUTH_PATH.touch()
        self.quilt_credentials_path = quilt3.session.CREDENTIALS_PATH

        self.aws_credentials_path = Path(aws_path) 

        dic = {'access_key': os.getenv('AWS_ACCESS_KEY_ID'),
               'secret_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
               'token': None,
               'expiry_time': os.getenv('EXPIRY_TIME')}
        with open(str(self.quilt_credentials_path), 'w') as f:
            json.dump(dic, f)
        self.default_remote_registry = default_remote_registry
        quilt3.config(default_remote_registry=default_remote_registry)
        self.package = quilt3.Package()

    def bucket_obj(self, bucket_uri):
        ''' Create quilt3 bucket object

            Args:
                bucket_uri (:obj:`str`): quilt s3 bucket address

            Returns:
                (:obj:`quilt3.Bucket`): quilt3 bucket object
        '''
        return quilt3.Bucket(bucket_uri)

    def add_to_package(self, package_name, destination=None, source=None, meta=None):
        ''' Add file/directory to an existing package on S3 or build new package
            with name package_name
        
            Args:
                package_name (:obj:`str`): name of package to be modified
                source (:obj:`str`): source to be added to package,
                                    directories must end with '/'
                destination (:obj:`str` ): package to be manipulated,
                                        directories must end with '/'
                meta (:obj:`dict`): package meta

            Returns:

        '''
        suffix = '/'
        s = source
        m = meta
        d = destination
        try:
            p = quilt3.Package.install(package_name)
        except botocore.errorfactory.ClientError:
            p = self.package

        if s.endswith(suffix) != d.endswith(suffix): # when s and d do not share the same suffix
            return '{} and {} must have the same suffix. Operation stopped.'.format(d, s)

        if s.endswith(suffix):
            p.set_dir(d, s, meta=m)
        else:
            p.set(d, s, meta=m)
        p.build(name=package_name)

    def push_to_remote(self, package_name, registry=None, destination=None, message=None) -> str:
        ''' Push local package to remote registry

            Args:
                package_name (:obj:`str`): name of package in "username/packagename" format
                registry (:obj:`str`): S3 URI where package should be pushed
                destination (:obj:`str`): file landing destination in remote registry
                message (:obj:`str`): commit message
        '''
        try:
            p = quilt3.Package.browse(package_name)
        except botocore.errorfactory.ClientError:
            return 'No such package {} on s3'.format(package_name)
        except FileNotFoundError:
            self.package.build(name=package_name)
            p = self.package
        except quilt3.util.QuiltException as e:
            return str(e)
        p.push(package_name, registry=registry, dest=destination, message=message)

    def delete_package(self, package_name, registry=None, delete_from_s3=True):
        """delete a local/remote package from local/remote registry
        
        Args:
            package_name (:obj:`str`): name of the package or name of file
            registry (:obj:`str`, optional): the registry from which the package will be removed. Defaults to None.
            delete_from_s3 (:obj:`bool`): whether to delete the underlying files in s3 bucket.
        """
        try:
            bucket = quilt3.Bucket(registry)
            bucket.delete_dir('.quilt/named_packages/' + package_name + '/')
        except quilt3.util.QuiltException as e:
            return str(e)
        if delete_from_s3:
            bucket.delete_dir(package_name + '/')

    def delete_obj(self, key):
        """delete an object from s3 bucket
        
        Args:
            key (:obj:`str`): key of the object in s3 bucket
        """
        try:
            bucket = quilt3.Bucket(self.default_remote_registry)
            bucket.delete(key)
        except botocore.errorfactory.ClientError:
            return 'No such object {} on s3'.format(key)        

    def build_from_external_bucket(self, package_name, package_dest, bucket_name, key, file_dir,
                                  bucket_credential=None, profile_name=None, meta=None,
                                  bucket_config=None, max_concurrency=10):
        ''' Build package with source from external (non-quilt) s3 buckets

            Args:
                package_name (:obj:`str`): local package name after being built
                package_dest (:obj:`str`): package(s) to be manipulated
                bucket_name (:obj:`str`): s3 bucket name
                key (:obj:`str`): the name of the key in s3 bucket to download from
                file_dir (:obj:`str`): the local path to which the file will be downloaded
                bucket_credential (:obj:`str`): directory in which credential for s3 bucket is stored
                profile_name (:obj:`str`): profile to be used for authentication
                meta (:obj:`dict`): meta information for package file
                bucket_credential (:obj:`str`): directory in which config for s3 bucket is stored
                max_concurrency (:obj:`int`): threads used for downloading
        '''
        settings = TransferConfig(max_concurrency=max_concurrency)
        if bucket_credential is None:
            bucket_credential = str(self.aws_credentials_path.expanduser())
        else:
            bucket_credential = str(Path(bucket_credential).expanduser())

        if bucket_config is None:
            bucket_config = str(self.aws_credentials_path.with_name('aws_config').expanduser())
        else:
            bucket_config = str(Path(bucket_config).expanduser())

        if profile_name is None:
            profile_name = self.profile_name

        s3 = s3_util.S3Util(profile_name=profile_name, credential_path=bucket_credential,
                            config_path=bucket_config)
                            
        file_name_path = Path(file_dir, key).expanduser()
        file_name = str(file_name_path)
        if package_dest.endswith('/'):
            file_name_path.mkdir(parents=True, exist_ok=True)
            s3.download_dir(key, bucket_name, local=file_dir)
        else:
            Path(file_name_path.parent).mkdir(parents=True, exist_ok=True)
            file_name_path.touch(exist_ok=True)        
            s3.client.download_file(bucket_name, key, file_name, Config=settings)
        
        if package_dest.endswith('/'):
            self.package.set_dir(package_dest, file_name, meta=meta)
        else:
            self.package.set(package_dest, file_name, meta=meta)
        return self.package.build(package_name)