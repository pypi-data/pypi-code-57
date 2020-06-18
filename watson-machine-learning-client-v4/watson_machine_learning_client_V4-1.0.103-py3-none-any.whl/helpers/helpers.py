from typing import Union
import json
from configparser import ConfigParser

__all__ = [
    "get_credentials_from_config",
    "pipeline_to_script"
]


def get_credentials_from_config(env_name, credentials_name, config_path="./config.ini"):
    """Load credentials from config file.

        [DEV_LC]

        wml_credentials = { }
        cos_credentials = { }

    :param env_name: the name of [ENV] defined in config file
    :type env_name: str
    :param credentials_name: name of credentials
    :type credentials_name: str
    :param config_path: path to the config file
    :type config_path: str
    :return: dict

    >>> get_credentials_from_config(env_name='DEV_LC', credentials_name='wml_credentials')

    """
    config = ConfigParser()
    config.read(config_path)

    return json.loads(config.get(env_name, credentials_name))


def pipeline_to_script(pipeline) -> Union['str', 'HTML']:
    """
    Create a python script based on a passed pipeline model. (Pythone code representation of pipeline model)


    Parameters
    ----------
    pipeline: Union[Pipeline, TrainedPipeline], required

    Example
    -------
    >>> pipeline_to_script(pipeline=best_pipeline)
    >>>
    """
    from lale.helpers import import_from_sklearn_pipeline
    from sklearn.pipeline import Pipeline
    from watson_machine_learning_client.utils.autoai.utils import is_ipython
    from watson_machine_learning_client.utils import create_download_link
    import os
    script_name = "pipeline_script.py"

    if isinstance(pipeline, Pipeline):
        pipeline = import_from_sklearn_pipeline(pipeline)

    script = pipeline.pretty_print()

    with open(script_name, 'w') as f:
        f.write(script)

    script_location = f"{os.path.abspath('.')}/{script_name}"

    if is_ipython():
        return create_download_link(script_location)
    else:
        return f"Pipeline python script location: {script_location}"


