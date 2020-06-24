import os
import re
import io
import base64
import requests
from configparser import ConfigParser
from os.path import join, dirname, isfile, isdir

import uuid
import torch
from torch.utils import model_zoo

from .loggers import Logger
from .settings import TEMP_DIR, ME_URL, CLIENTS_URL, MODELS_URL, JOBS_URL, SUBMISSIONS_URL, DATA_URL, BASE_URL
from .settings import system_info
from .model_zoo import *  # So loading models does not raise Attribute error

# Load configuration parameters.
# This includes a simple token authentication encoded in base64
config_file = join(dirname(os.path.realpath(__file__)), 'config.ini')  # New .env file
config = ConfigParser()
config.read(config_file)

# Create a Logger
logger = Logger()
logger.info(system_info())


def update_config():
    """Update the configuration file."""
    with open(config_file, 'w') as cf:
        config.write(cf)


def login(username, password):
    """
    Loging in to the FEDBIONET API.
    :param str username: Username to log in. 
    :param password: Password
    :return dict: JSON response. 
    """
    res = requests.get(ME_URL, auth=(username, password))
    if res.status_code == 200:
        "Save token to disk and return user profile data."

        TOKEN = base64.b64encode(f'{username}:{password}'.encode()).decode()
        config['DEFAULT']['TOKEN'] = TOKEN
        update_config()

        return res.json()
    elif res.status_code in range(400, 500):
        "Not authorized code."
        logger.error(f'Login failed: {res.content}')
        return res.json()
    else:
        raise ConnectionError('Connection seems not to be working')


def get_auth():
    TOKEN = config['DEFAULT']['TOKEN']
    return tuple(base64.b64decode(TOKEN.encode()).decode().split(':'))


def logout():
    config.remove_option('DEFAULT', 'TOKEN')
    update_config()


def is_logged_in():
    """ Checks if user data exists"""
    try:
        res = requests.get(ME_URL, auth=get_auth())
        assert res.status_code == 200, 'Login validation failed.'
        return True
    except Exception as e:
        logout()
        return False


def get_uuid_from_url(url):
    """
    Extract the uuid of an object from the URL.
    :param str url: URL where the UUID is contained.
    :return str: UUID as s string.
    """
    return re.findall(r'[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}', url)[0]


def handle_response(res):
    # logger.info(f'Response content: {res.headers}')
    if res.status_code is 204:
        logger.info('Request successful. Status code: 204.')
        return {'detail': 'Request successful. Status code: 204.'}
    elif res.status_code in range(200, 300):
        logger.info('Request successful')
        logger.info(f'Response: {res.json()}')
        return res.json()
    elif res.status_code in range(400, 500):
        logger.error(f'Bad request. Status code: {res.status_code} | Response: {res.content}')
        return res.json()
    else:
        logger.error(f'Bad request. Status code: {res.status_code} | response {res.content}')


def get(url, **kwargs):
    logger.debug(f'Sending GET request to: {url}')
    res = requests.get(url, auth=get_auth(), **kwargs)
    return handle_response(res)


def post(url, **kwargs):
    logger.debug(f'Sending POST request to: {url}')
    res = requests.post(url, auth=get_auth(), **kwargs)
    return handle_response(res)


def put(url, **kwargs):
    logger.debug(f'Sending PUT request to: {url}')
    res = requests.put(url, auth=get_auth(), **kwargs)
    return handle_response(res)


def patch(url, **kwargs):
    logger.debug(f'Sending PATCH request to: {url}')
    res = requests.patch(url, auth=get_auth(), **kwargs)
    return handle_response(res)


def delete(url, **kwargs):
    logger.debug(f'Sending DELETE request to: {url}')
    res = requests.delete(url, auth=get_auth(), **kwargs)
    return handle_response(res)


def model_to_io_file(model):
    """Load model as BytesIO (creates file in RAM)"""
    filename = f'{uuid.uuid4()}.pth'
    model_io = io.BytesIO()
    torch.save(model, model_io)
    return filename, model_io.getvalue()


# ============================================================
# USER DATA
# ============================================================
def me():
    logger.info('Getting profile information...')
    return get(ME_URL)[0]


# ============================================================
# DATA MANAGEMENT
# ============================================================
def get_available_data():
    logger.info(f'Getting available data...')
    return get(DATA_URL)


# ============================================================
# JOBS AND SUBMISSION MANAGEMENT
# ============================================================
def get_jobs(**kwargs):
    logger.info('Getting jobs...')
    return get(JOBS_URL, **kwargs)


def update_job_status(job, status, attach_log=False):
    json = {'status': status}

    # Attach logfile if requested
    if attach_log:
        files = {'log': open(logger.file_path)}
        return patch(job['url'], data=json, files=files)
    else:
        return patch(job['url'], json=json)


def update_job_next_round(job):
    """
    Add up plus 1 in w.r.t. the current round.
    :param dict job: JSON-like object containing job's information.
    :return:
    """
    logger.info('Updating to next round...')

    # Step up in the next round
    json = {'current_round': job['current_round'] + 1}
    return patch(job['url'], json=json)


def upload_trained_model(job, model):
    """Upload train model to job"""
    files = {'trained_model': model_to_io_file(model)}
    return patch(job['url'], files=files)


def get_submissions(job_url=None, current_round=None):
    """
    Gets a list of submissions made by the user requesting the list. Include job_url if you want to
    filter the list of submissions by url.

    :param str job_url: Job URL. This will filter the submissions by Job.
    :param int current_round: Filter by current round 
    :return list: List of dict-like objects containing the submissions associated to the job_url.
    """
    # Filter submissions by job if job URL is provided
    params = {}
    if job_url:
        params['job'] = get_uuid_from_url(job_url)
    if current_round:
        params['round'] = current_round

    # Get list of submissions
    return get(SUBMISSIONS_URL, params=params)


def post_submission(model, job_url, current_round, number_observations):
    """
    Submit a new version of your model.
    :param torch.Module model: Torch model object.
    :param str job_url: Job URL associated to the model trained.
    :param int current_round: Version of the trained model (rounds).
    :param number_observations: Number of observations used to train this model.
    :return:
    """
    logger.info(f'Submitting model...')

    # Append files to upload
    files = {
        'model': model_to_io_file(model),
        'log': open(logger.file_path, 'rb')}

    data = {
        'job': job_url,
        'round': current_round,
        'number_observations': number_observations
    }
    return post(SUBMISSIONS_URL, files=files, data=data)


# ============================================================
# MODEL MANAGEMENT
# ============================================================
def load_model_from_url(model_url):
    """
    Download torch model and load it as a torch Module.
    :param str model_url: Model .pt or .pth URL
    :return torch.Module: Model loaded
    """
    model_dir = join(TEMP_DIR, f'downloaded_models')
    if not isdir(model_dir):
        os.makedirs(model_dir, exist_ok=True)
    cached_models = [join(model_dir, f) for f in os.listdir(model_dir) if f.endswith('pth')]
    for m in cached_models:
        if isfile(m):
            os.remove(m)
    return model_zoo.load_url(model_url, progress=False, model_dir=model_dir)


def load_base_model(job):
    """
    Downloads base torch model.
    :param dict job: JSON-like object containing job's information.
    :return torch.Module: torch model loaded.
    """
    logger.info('Downloading base model...')
    model_file_url = get(job['model'])['model_file']

    # Download file and return model file path
    return load_model_from_url(model_file_url)


def load_trained_model(job):
    """
    Download trained model from job.
    :param dict job: JSON-like object containing job's information.
    :return torch.Module: torch model loaded.
    """
    logger.info('Downloading trained model...')
    trained_model_file_url = get(job['url'])['trained_model']

    return load_model_from_url(trained_model_file_url)


def get_models():
    """Get a list of the currently available models."""
    logger.debug('Getting a list of models.')
    return get(MODELS_URL)
