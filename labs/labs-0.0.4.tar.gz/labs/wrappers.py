import os


def experiment_path(func):
    """
    Wrapping function of user experiment, by creating inside the worker instance the experiment artifacts path
    """
    def inner(experiment, artifacts_path, metrics):
        if not os.path.exists(artifacts_path):
            os.makedirs(artifacts_path)

        return func(experiment, artifacts_path, metrics)

    return inner
