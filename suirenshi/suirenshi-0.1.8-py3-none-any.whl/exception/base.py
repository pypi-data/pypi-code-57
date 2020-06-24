""" Exceptions """


class CheckpointException(Exception):
    """
    Raised when:
      (1) Checkpoint file not exists.
    """
    pass


class EmptyDatasetException(Exception):
    """ No images found in dataset """
    pass


class GpuUnavailableException(Exception):
    """ GPUs un-available """
    pass


class MissingRequiredFilesException(Exception):
    """
    Raise when:
        (1) Required files in prep.FileLists or FilePatterns missed
    """
    def __init__(self, missing_files, directory):
        error_message = 'Missing required files: %s. (directory=%s)' % (missing_files, directory)
        Exception.__init__(self, error_message)


class SourceModelException(Exception):
    """
    Raised when:
      (1) Source model not found
      (2) Path to source model is not a zip
      (3) Path to source model not exists
    """
    pass


class SubprocessException(Exception):
    """
    Raise when exception occurred in subprocess
    """
    def __init__(self, tag, str_e):
        error_message = 'Unexpected exception in subprocess/%s: %s' % (tag, str_e)
        Exception.__init__(self, error_message)
