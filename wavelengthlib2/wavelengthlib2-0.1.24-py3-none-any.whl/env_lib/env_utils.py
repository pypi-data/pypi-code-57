import os

WL_PROJECT_ROOT_ENV_VARIABLE = 'WL_PROJECT_ROOT'

def get_env_name():
    wl_project_root = os.environ.get(WL_PROJECT_ROOT_ENV_VARIABLE)
    if wl_project_root:
        env_name = 'DEV'
    else:
        env_name = 'TEST'
    return env_name