from worker.data.operations import get_data_by_path

parameters = {
    "global": {
        "app-name": "my-app",
        "app-key": "my-app-key",
        "event-type": "scheduler",
        "query-limit": 1000,
    },
}


def get(path, default=None):
    return get_data_by_path(data=parameters, path=path, default=default)


def update(additional_parameters):
    """
    The purpose of this method is to update the existing parameters data
    with the provided additional parameters. Note that the globals will
    be replaced if the additional parameters contains global node.
    :param additional_parameters:
    :return:
    """
    globals = parameters.pop('global')
    additional_globals = additional_parameters.pop('global', {})
    globals.update(additional_globals)
    parameters.update(additional_parameters)
    if globals:
        parameters['global'] = globals
