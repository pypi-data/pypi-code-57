import os
import pathlib
import nltk

def install_nltk_data():
  """
  Install required nltk data packages
  """
  def get_env_path():
    return os.environ['VIRTUAL_ENV']

  def create_if_not_exists_env_dir(dir_name):
    env_path = get_env_path()
    dir_path = os.path.join(env_path, dir_name)
    if not os.path.exists(dir_path):
      print("Creating %s..." % dir_path)
      os.mkdir(dir_path)
    return dir_path
  
  nltk_data_path = create_if_not_exists_env_dir('nltk_data/')

  try:
    nltk.data.find('tokenizers/punkt')
  except LookupError:
    nltk.download(info_or_id='punkt', download_dir=nltk_data_path)

  try:
    nltk.data.find('corpora/stopwords')
  except LookupError:
    nltk.download(info_or_id='stopwords', download_dir=nltk_data_path)

  try:
    nltk.data.find('corpora/wordnet')
  except LookupError:
    nltk.download(info_or_id='wordnet', download_dir=nltk_data_path)