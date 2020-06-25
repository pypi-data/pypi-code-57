import os
import pickle
import shutil
import subprocess
import sys
import tempfile
from time import sleep, perf_counter

import azureml.dataprep as dprep
from azureml.dataprep.api._loggerfactory import _LoggerFactory, session_id
from azureml.dataprep.fuse._logger_helper import get_trace_with_invocation_id

logger = _LoggerFactory.get_logger('dprep.fuse')


class MountContext(object):
    """Context manager for mounting dataflow.

    .. remarks::

        Upon entering the context manager, the dataflow will be mounted to the mount_point. Upon exit, it will
        remove the mount point and clean up the daemon process used to mount the dataflow.

        An example of how to mount a dataflow is demonstrated below:

        .. code-block:: python

            import azureml.dataprep as dprep
            from azureml.dataprep.fuse.dprepfuse import mount
            import os
            import tempfile

            mount_point = tempfile.mkdtemp()
            dataflow = dprep.Dataflow.get_files('https://dprepdata.blob.core.windows.net/demo/Titanic.csv')
            with mount(dataflow, 'Path', mount_point, foreground=False):
                print(os.listdir(mount_point))

    :param dataflow: The dataflow to be mounted.
    :param files_column: The name of the column that contains the StreamInfo.
    :param mount_point: The directory to mount the dataflow to.
    :param base_path: The base path to resolve the new relative root.
    :param options: Mount options.
    :param invocation_id: The invocation ID to correlate the subprocess and main process.
    :param destination: The destination to write the output to.
    """

    def __init__(self, dataflow, files_column: str, mount_point: str,
                 base_path: str = None, options: 'MountOptions' = None, invocation_id: str = None,
                 destination: tuple = None):
        """Constructor for the context manager.

        :param dataflow: The dataflow to be mounted.
        :param files_column: The name of the column that contains the StreamInfo.
        :param mount_point: The directory to mount the dataflow to.
        :param base_path: The base path to resolve the new relative root.
        :param options: Mount options.
        :param invocation_id: The invocation ID to correlate the subprocess and main process.
        :param destination: The destination to write the output to.
        """
        from azureml.dataprep.fuse.dprepfuse import MountOptions

        self._dataflow = dataflow
        self._files_column = files_column
        self._mount_point = mount_point
        self._base_path = base_path
        self._options = options or MountOptions()
        self._process = None
        self._entered = False
        self._invocation_id = invocation_id
        self._trace = get_trace_with_invocation_id(logger, self._invocation_id)
        self._destination = destination
        self._pickle_path = None

        if not self._options.data_dir:
            self._options.data_dir = tempfile.mkdtemp()

    @property
    def mount_point(self):
        """Get the mount point."""
        return self._mount_point

    def start(self):
        """Mount the file streams.

        This is equivalent to calling the MountContext.__enter__ instance method.
        """
        self.__enter__()

    def stop(self):
        """Unmount the file streams.

        This is equivalent to calling the MountContext.__exit__ instance method.
        """
        self.__exit__()

    def __enter__(self):
        """Mount the file streams.

        :return: The current context manager.
        :rtype: azureml.dataprep.fuse.daemon.MountContext
        """
        if self._entered:
            self._trace('already entered, skipping mounting again.')
        else:
            self._trace('entering MountContext')
            self._mount_using_daemon()
            self._wait_until_mounted()
            self._entered = True
            self._trace('finished mounting')
        return self

    def __exit__(self, *args, **kwargs):
        """Unmount the file streams"""
        if not self._entered:
            self._trace('tried to exit without actually entering.')
            return

        try:
            self._trace('exiting MountContext')
            self._unmount()
            if self._process:
                self._trace('terminating daemon process')
                self._process.terminate()
                self._process = None
            else:
                logger.warning('daemon process not found')
            self._remove_mount()
            self._remove_data_dir()
            self._trace('finished exiting')
        except:
            logger.error('failed to unmount(%s)', self._invocation_id)
        finally:
            self._entered = False

    def _mount_using_daemon(self):
        python_path = sys.executable
        _, dataflow_path = tempfile.mkstemp()
        _, self._pickle_path = tempfile.mkstemp()

        dest = None
        if self._destination:
            dest = (
                dprep.api._datastore_helper._serialize_datastore(self._destination[0]),
                self._destination[1]
            )

        # TODO: Change this to use a mechanism that doesn't involve writing to disk
        with open(self._pickle_path, 'wb') as f:
            pickle.dump({
                'files_column': self._files_column,
                'mount_point': self._mount_point,
                'base_path': self._base_path,
                'options': self._options,
                'invocation_id': self._invocation_id,
                'caller_session_id': session_id,
                'spawn_process_timestamp': perf_counter(),
                'dest': dest
            }, f)
        if self._dataflow:
            self._dataflow.save(dataflow_path)
        self._process = subprocess.Popen(
            [python_path, 'daemon.py', dataflow_path, self._pickle_path],
            cwd=os.path.dirname(__file__)
        )

    def _wait_until_mounted(self):
        attempt = 1
        max_attempt = 15  # total wait time of 60 seconds. 60 = 0.5 * 15 * (15 + 1) / 2
        sleep_time = 0.5  # seconds

        from azureml.dataprep.fuse.dprepfuse import SENTINEL_FILE_NAME

        start = perf_counter()
        while not os.path.exists(self.mount_point) or not os.path.exists(os.path.join(self.mount_point, SENTINEL_FILE_NAME)):
            if attempt > max_attempt:
                error_msg = 'Waiting for mount point to be ready has timed out. Check if fuse device is available on your system.'
                self._remove_pickle()

                try:
                    os_info = os.uname()
                    sysname = os_info.sysname.lower()
                    release = os_info.release.lower()
                    version = os_info.version.lower()

                    if sysname == 'linux' and ('microsoft' in release or 'wsl' in release) and ('microsoft' in version or 'wsl' in version):
                        error_msg += '\nWarning: Fuse only available on Windows subsystem for Linux starting from version 2.\n'
                except:
                    pass

                error_msg += 'Session ID: {}'.format(session_id)
                logger.error(error_msg)
                raise RuntimeError(error_msg)
            sleep(sleep_time * attempt)
            attempt += 1

        elapsed = perf_counter() - start
        self._trace('Launching daemon process took {} seconds'.format(elapsed), {
            'elapsed': elapsed,
            'attempt': attempt
        })
        self._remove_pickle()

    def _remove_pickle(self):
        try:
            if self._pickle_path:
                os.remove(self._pickle_path)
                self._pickle_path = None
        except FileNotFoundError:
            logger.warning('Attempted to remove the pickled path but the path doesn\'t exist.')

    def _unmount(self):
        try:
            self._trace('trying to call umount. In /tmp/? {}'.format(self.mount_point.startswith('/tmp/')))
            subprocess.check_call(['umount', self.mount_point])
        except subprocess.CalledProcessError:
            logger.warning('Non-fatal error: umount failed')

    def _remove_mount(self):
        try:
            self._trace('trying to remove mount point')
            if not os.path.exists(self.mount_point):
                self._trace('mount point does not exist')
                return
            shutil.rmtree(self.mount_point)
            self._trace('successfully removed mount point')
        except:
            logger.warning('Non-fatal error: failed to remove mount point {}.'.format(self.mount_point))

    def _remove_data_dir(self):
        try:
            self._trace('trying to remove data dir')
            if not os.path.exists(self._options.data_dir):
                self._trace('data dir does not exist')
                return
            shutil.rmtree(self._options.data_dir)
            self._trace('successfully removed data dir')
        except:
            logger.warning('Non-fatal error: failed to remove cache directory {}.'.format(self._options.data_dir))


def _main():
    from azureml.dataprep.fuse.dprepfuse import mount
    from azureml.dataprep.api.engineapi.engine import use_multi_thread_channel
    use_multi_thread_channel()

    if len(sys.argv) != 3:
        error_msg = 'Incorrect number of arguments given to mount daemon. Usage: ' \
                    'python daemon.py /path/to/dataflow args_json'
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    dataflow = None
    if os.path.exists(sys.argv[1]):
        with open(sys.argv[1], 'r') as f:
            dataflow_json = f.read()
            if dataflow_json:
                dataflow = dprep.Dataflow.from_json(dataflow_json)

    with open(sys.argv[2], 'rb') as f:
        kwargs = pickle.load(f)

    if kwargs['dest']:
        kwargs['destination'] = (
            dprep.api._datastore_helper._deserialize_datastore(kwargs['dest'][0]),
            kwargs['dest'][1]
        )

    mount(dataflow, **kwargs)


if __name__ == '__main__':
    _main()
