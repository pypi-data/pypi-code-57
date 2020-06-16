from werkzeug.utils import import_string
from flask import current_app
import warnings


class Storage:
    def __init__(self, app=None):
        self.default_provider = None
        self.providers_options = None
        if app is not None:
            self.init_app(app)
      
    @staticmethod       
    def provider(self, name=None):
        _provider = name if name is not None else current_app.config['STORAGE_PROVIDER_DEFAULT']
        if _provider not in current_app.config['STORATE_PROVIDERS_OPTIONS']:
            raise RuntimeError('Storage Provider error')
        _provider_object = import_string(current_app.config['STORATE_PROVIDERS_OPTIONS'][_provider])
        return _provider_object()
    
    def __getattr__(self, key):
        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            current_provider = current_app.config['STORAGE_PROVIDER_DEFAULT']
            providers = current_app.config['STORATE_PROVIDERS_OPTIONS']
            if current_provider not in providers:
                raise RuntimeError('Storage Provider error')
            _provider_object = import_string(providers[current_provider])
            return getattr(_provider_object(), key)

    def init_app(self, app):
        # STORAGE 可用的提供器
        providers_options = app.config.setdefault('STORATE_PROVIDERS_OPTIONS', {
            'local':'flask_saved.providers.local.LocalStorage',
            'oss': 'flask_saved.providers.oss.OssStorage'
        })
        # STORAGE 默认使用的
        default_provider = app.config.setdefault('STORAGE_PROVIDER_DEFAULT', 'local')        
        if default_provider not in providers_options:
            warnings.warn('STORAGE_PROVIDER_DEFAULT set error')  
            
        # STORATE 公共配置
        app.config.setdefault('STORAGE_COMMON_EXTENSIONS', ('jpg', 'jpe', 'jpeg', 'png', 'gif'))
        app.config.setdefault('STORAGE_COMMON_FILE_MAX', 1024 * 1024 * 10)
        
        # LOCAL 提供器配置项
        storage_local_base_path = app.config.setdefault('STORAGE_LOCAL_BASE_PATH', None)
        storage_local_base_url = app.config.setdefault('STORAGE_LOCAL_BASE_URL', None)
         # 使用local提供器 必须设置的配置项
        if default_provider == 'local':
            if storage_local_base_url is None:
                warnings.warn('STORAGE_BASE_URL Suggest setting')
            if storage_local_base_path is None:
                raise ValueError('STORAGE_LOCAL_BASE_PATH must be set')
              
        
        # OSS 提供器配置
        oss_key = app.config.setdefault('STORAGE_OSS_ACCESS_KEY', None)
        oss_secret = app.config.setdefault('STORAGE_OSS_SECRET_KEY', None)
        oss_endpoint = app.config.setdefault('STORAGE_OSS_ENDPOINT', None)
        oss_bucket = app.config.setdefault('STORAGE_OSS_BUCKET', None)
        app.config.setdefault('STORAGE_OSS_CNAME', None)
        app.config.setdefault('STORAGE_OSS_DOMIAN', None)
        app.config.setdefault('STORAGE_OSS_BASE_PATH', None)
        # 使用oss提供器 必须设置的配置项
        if default_provider == 'oss':
            if oss_key is None:
                raise RuntimeError('STORAGE_OSS_ACCESS_KEY must be set')
            if oss_secret is None:
                raise RuntimeError('STORAGE_OSS_SECRET_KEY must be set')
            if oss_endpoint is None:
                raise RuntimeError('STORAGE_OSS_ENDPOINT must be set')
            if oss_bucket is None:
                raise RuntimeError('STORAGE_OSS_BUCKET must be set')

        self.default_provider = default_provider
        self.providers_options = providers_options
        app.extensions['storage'] = self