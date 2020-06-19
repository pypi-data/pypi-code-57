import os

class Config(object):
  """
  Parent configuration class.

  Add all config attributes in the parent class with a default.
  Then override as needed in the environment specific configs
  """
  GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
  PC_MILER_URL = "https://pcmiler.alk.com/apis/rest/v1.0/Service.svc/locations?postcodeFilter={0}&dataset=Current&authToken={1}"
  PC_MILER_KEY = os.getenv('PC_MILER_KEY')
  LOCATION_REDIS_URL = os.getenv('LOCATION_REDIS_URL')
  LOCATION_REDIS_PWD = os.getenv('LOCATION_REDIS_PWD')
  DISTANCE_CACHE_URL = os.getenv('DISTANCE_CACHE_URL')
  DISTANCE_CACHE_PASSWORD = os.getenv('DISTANCE_CACHE_PASSWORD')
  TIMEZONE_CACHE_URL = os.getenv('TIMEZONE_CACHE_URL')
  TIMEZONE_CACHE_PASSWORD = os.getenv('TIMEZONE_CACHE_PASSWORD')
  PC_MILER_HOURLY_LIMIT = 14000
  PC_MILER_MONTHLY_LIMIT = 300000

class LocalConfig(Config):
  """Configurations for running and debugging locally, with a separate local database."""
  LOCATION_REDIS_URL='redis://localhost:6379'
  LOCATION_REDIS_PWD=None
  DISTANCE_CACHE_URL='redis://localhost:6379'
  DISTANCE_CACHE_PASSWORD=None
  TIMEZONE_CACHE_URL='redis://localhost:6379'
  TIMEZONE_CACHE_PASSWORD=None

class DevelopmentConfig(Config):
  """Configurations for running in dev mode, with a remote database."""
  

class ProductionConfig(Config):
  """Configurations for running in dev mode, with a remote database."""
  

config_options = {
    'local': LocalConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}

env_name = os.getenv('APP_SETTINGS')

if not env_name:
  print("warning: No APP_SETTINGS environment variable set, using development")
  env_name = 'development'

app_config = config_options[env_name]
