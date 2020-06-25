# Copyright 2011-2014 Biomedical Imaging Group Rotterdam, Departments of
# Medical Informatics and Radiology, Erasmus MC, Rotterdam, The Netherlands
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import queue
import sys
import threading
import time

from bidict import bidict
import fastr
from fastr import exceptions
from fastr.abc.baseplugin import PluginState

try:
    import drmaa
    load_drmaa = True
except (ImportError, RuntimeError, OSError):
    load_drmaa = False

from fastr.execution.job import JobState
from fastr.plugins.executionplugin import ExecutionPlugin
from fastr.helpers.classproperty import classproperty


class FastrDRMAANotFoundError(exceptions.FastrImportError):
    """
    Indicate the DRMAA module was not found on the system.
    """
    pass


class FastrDRMAANotFunctionalError(exceptions.FastrError):
    """
    Indicate DRMAA is found but creating a session did not work
    """
    pass


class DRMAAExecution(ExecutionPlugin):
    """
    A DRMAA execution plugin to execute Jobs on a Grid Engine cluster. It uses
    a configuration option for selecting the queue to submit to. It uses the
    python ``drmaa`` package.

    .. note::

        To use this plugin, make sure the ``drmaa`` package is installed and
        that the execution is started on an SGE submit host with DRMAA
        libraries installed.

    .. note::

        This plugin is at the moment tailored to SGE, but it should be fairly
        easy to make different subclasses for different DRMAA supporting
        systems.
    """
    if not load_drmaa:
        _status = (PluginState.failed, 'Could not load DRMAA module required for cluster communication')

    # DRMAA Supports cancelling jobs, job dependencies and hold release actions
    SUPPORTS_CANCEL = True
    SUPPORTS_DEPENDENCY = True
    SUPPORTS_HOLD_RELEASE = True
    CANCELS_DEPENDENCIES = False

    GE_NATIVE_SPEC = {
        'WD': '-wd {workdir}',
        'QUEUE': '-q {queue}',
        'WALLTIME': '-l h_rt={walltime}',
        'MEMORY': '-l h_vmem={memory}',
        'NCORES': '-pe smp {ncores:d}',
        'OUTPUTLOG': '-o {outputlog}',
        'ERRORLOG': '-e {errorlog}',
        'DEPENDS': '-hold_jid {hold_list}',
        'DEPENDS_SEP': ',',
        'HOLD': '-h',
    }

    TORQUE_NATIVE_SPEC = {
        'CWD': '',
        'QUEUE': '-q {queue}',
        'WALLTIME': '-l walltime={walltime}',
        'MEMORY': '-l mem={memory}',
        'NCORES': '-l procs={ncores:d}',
        'OUTPUTLOG': '-o {outputlog}',
        'ERRORLOG': '-e {errorlog}',
        'DEPENDS': '-W depend=afterok:{hold_list}',
        'DEPENDS_SEP': ':',
        'HOLD': '-h',
    }

    NATIVE_SPEC = {
        'grid_engine': GE_NATIVE_SPEC,
        'torque': TORQUE_NATIVE_SPEC,
    }

    def __init__(self, finished_callback=None, cancelled_callback=None):
        super(DRMAAExecution, self).__init__(finished_callback, cancelled_callback)

        # Some default
        self.default_queue = fastr.config.drmaa_queue
        self.max_jobs = fastr.config.drmaa_max_jobs
        self.engine = fastr.config.drmaa_engine
        self.regression_check_interval = fastr.config.drmaa_job_check_interval
        self.num_undetermined_to_fail = fastr.config.drmaa_num_undetermined_to_fail

        # Create the DRMAA session
        try:
            self.session = drmaa.Session()
            self.session.initialize()
        except drmaa.errors.DrmaaException as exception:
            raise FastrDRMAANotFunctionalError('Encountered an error when creating DRMAA session: [{}] {}'.format(
                exception.__class__,
                str(exception)
            ))

        fastr.log.debug('A DRMAA session was started successfully')
        response = self.session.contact
        fastr.log.debug('session contact returns: ' + response)

        # Create job translation table
        self.job_lookup_fastr_drmaa = bidict()
        self.job_lookup_lock = threading.Lock()

        # Track jobs of which we cannot determine state and count many times
        # this happened. If only a few times, it might be communications
        # hiccups, but if consistent, the jobs probably died or something.
        self.undetermined_jobs = {}

        # Create even queue lock
        self.submit_queue = queue.Queue()
        self.finished_queue = queue.Queue()

        # Make sure we can regularly check if the threads are still alive
        self.last_thread_check = time.time()
        self.thread_check_lock = threading.Lock()

        # Threads for plugin
        self.collector_thread = None
        self.callback_thread = None
        self.submitter_thread = None
        self.checker_thread = None
        self.ensure_threads()

    def check_threads(self):
        """
        Check if the threads are still alive, but make sure it is only done once per minute
        """
        with self.thread_check_lock:
            # Check only once per minute
            if time.time() - self.last_thread_check < 60:
                return

            self.last_thread_check = time.time()
            self.ensure_threads()

    def ensure_threads(self):
        """
        Start thread if not defined, or restart if they somehow died accidentallyy
        """
        # If plugin is not running, no need for threads
        if not self.running:
            return

        if self.collector_thread is None or not self.collector_thread.is_alive():
            fastr.log.debug('Creating job collector')
            self.collector_thread = threading.Thread(name='DRMAAJobCollector-0', target=self.collect_jobs, args=())
            self.collector_thread.daemon = True
            fastr.log.debug('Starting job collector')
            self.collector_thread.start()

        if self.callback_thread is None or not self.callback_thread.is_alive():
            fastr.log.debug('Creating job callback processor')
            self.callback_thread = threading.Thread(name='DRMAAJobCallback-0', target=self.dispatch_callbacks, args=())
            self.callback_thread.daemon = True
            fastr.log.debug('Starting job callback processor')
            self.callback_thread.start()

        if self.submitter_thread is None or not self.submitter_thread.is_alive():
            fastr.log.debug('Creating job submitter')
            self.submitter_thread = threading.Thread(name='DRMAAJobSubmitter-0', target=self.submit_jobs, args=())
            self.submitter_thread.daemon = True
            fastr.log.debug('Starting job submitter')
            self.submitter_thread.start()

        if self.checker_thread is None or not self.checker_thread.is_alive():
            fastr.log.debug('Creating job regression checker')
            self.checker_thread = threading.Thread(name='DRMAAJobChecker-0', target=self.regression_check, args=())
            self.checker_thread.daemon = True
            fastr.log.debug('Starting job regression checker')
            self.checker_thread.start()

    @classproperty
    def configuration_fields(cls):
        return {
            "drmaa_queue": (str, "week", "The default queue to use for jobs send to the scheduler"),
            "drmaa_max_jobs": (int, 0, "The maximum jobs that can be send to the scheduler"
                                       " at the same time (0 for no limit)"),
            "drmaa_engine": (str, "grid_engine", "The engine to use (options: grid_engine, torque"),
            "drmaa_job_check_interval": (int, 900, "The interval in which the job checker will start"
                                                   " to check for stale jobs"),
            "drmaa_num_undetermined_to_fail": (int, 3, "Number of consecutive times a job state has be"
                                                       " undetermined to be considered to have failed")
        }

    @classmethod
    def test(cls):
        if not load_drmaa:
            raise FastrDRMAANotFoundError('Could not import the required drmaa for this plugin')

    @property
    def spec_fields(self):
        return self.NATIVE_SPEC[self.engine]

    @property
    def n_current_jobs(self):
        return len(self.job_lookup_fastr_drmaa)

    def cleanup(self):
        # Stop submissions and callbacks
        super(DRMAAExecution, self).cleanup()

        # See if there are leftovers in the job translation table that can be cancelled
        while self.n_current_jobs > 0:
            with self.job_lookup_lock:
                fastr_job_id, drmaa_job_id = self.job_lookup_fastr_drmaa.popitem()

            fastr.log.info('Terminating left-over job {}'.format(drmaa_job_id))
            self._terminate_job(drmaa_job_id, retry=0)

        fastr.log.debug('Stopping DRMAA executor')
        # Destroy DRMAA
        try:
            self.session.exit()
            fastr.log.debug('Exiting DRMAA session')
        except drmaa.NoActiveSessionException:
            pass

        if self.collector_thread.is_alive():
            fastr.log.debug('Terminating job collector thread')
            self.collector_thread.join()
        if self.submitter_thread.is_alive():
            fastr.log.debug('Terminating job submitter thread')
            self.submitter_thread.join()
        if self.checker_thread.is_alive():
            fastr.log.debug('Terminating job checker thread')
            self.checker_thread.join()
        if self.callback_thread.is_alive():
            fastr.log.debug('Terminating job callback thread')
            self.callback_thread.join()
        fastr.log.debug('DRMAA executor stopped!')

    def _queue_job(self, job):
        self.submit_queue.put(job, block=True)

    def _terminate_job(self, drmaa_job_id: int, retry=1):
        try:
            self.session.control(drmaa_job_id, drmaa.JobControlAction.TERMINATE)
        except (drmaa.InvalidJobException, drmaa.InternalException) as exception:
            new_status = self._get_job_state(drmaa_job_id)
            if new_status not in [drmaa.JobState.UNDETERMINED,
                                  drmaa.JobState.DONE,
                                  drmaa.JobState.FAILED]:
                if retry > 0:
                    self._terminate_job(drmaa_job_id, retry=retry - 1)
                    return
                else:
                    fastr.log.warning(f'Encountered a DRMAA exception: [{type(exception).__name__}]'
                                      f' {exception}')
        except Exception as exception:
            fastr.log.error(f'Encountered an exception during cancellation of job {drmaa_job_id}: '
                            f'[{type(exception).__name__}] {exception}')

    def _cancel_job(self, job, retry=True):
        with self.job_lookup_lock:
            drmaa_job_id = self.job_lookup_fastr_drmaa.pop(job.id, None)

        if drmaa_job_id is None:
            fastr.log.info('Job {} not found in DRMAA lookup, no longer exists?'.format(job.id))
            return

        fastr.log.debug('Cancelling job {}'.format(drmaa_job_id))
        self._terminate_job(drmaa_job_id)

        # FIXME: Should we call this here or will it called double? should we
        # just call it an make something to avoid double calls?
        self.job_finished(job, errors=[exceptions.FastrError('job cancelled by fastr DRMAA plugin').excerpt()])

    def _hold_job(self, job):
        drmaa_job_id = self.job_lookup_fastr_drmaa.get(job.id, None)
        if drmaa_job_id:
            try:
                self.session.control(drmaa_job_id, drmaa.JobControlAction.HOLD)
            except Exception as exception:
                fastr.log.error(f'Encountered an exception during setting job {drmaa_job_id} to hold: '
                                f'[{type(exception).__name__}] {exception}')
        else:
            fastr.log.error('Cannot hold job {}, cannot find the drmaa id!'.format(job.id))

    def _release_job(self, job):
        drmaa_job_id = self.job_lookup_fastr_drmaa.get(job.id, None)
        if drmaa_job_id:
            try:
                self.session.control(drmaa_job_id, drmaa.JobControlAction.RELEASE)
            except Exception as exception:
                fastr.log.error(f'Encountered an exception during releasing job {drmaa_job_id}: '
                                f'[{type(exception).__name__}] {exception}')
        else:
            fastr.log.error('Cannot release job {}, cannot find the drmaa id!'.format(job.id))

    def _job_finished(self, result):
        pass

    def create_native_spec(self, queue, walltime, memory, ncores, outputLog,
                           errorLog, hold_job, hold, work_dir):
        """
        Create the native spec for the DRMAA scheduler. Needs to be implemented
        in the subclasses

        :param str queue: the queue to submit to
        :param str walltime: walltime specified
        :param str memory: memory requested
        :param int ncores: number of cores requested
        :param str outputLog: the location of the stdout log
        :param str errorLog: the location of stderr log
        :param list hold_job: list of jobs to depend on
        :param bool hold: flag if job should be submitted in hold mode
        :return:
        """
        native_spec = []

        native_spec.append(self.spec_fields['WD'].format(workdir=work_dir))
        native_spec.append(self.spec_fields['QUEUE'].format(queue=queue))

        if walltime is not None:
            native_spec.append(self.spec_fields['WALLTIME'].format(walltime=walltime))

        if memory is not None:
            native_spec.append(self.spec_fields['MEMORY'].format(memory=memory))

        if ncores is not None and ncores > 1:
            native_spec.append(self.spec_fields['NCORES'].format(ncores=ncores))

        if outputLog is not None:
            native_spec.append(self.spec_fields['OUTPUTLOG'].format(outputlog=outputLog))

        if errorLog is not None:
            native_spec.append(self.spec_fields['ERRORLOG'].format(errorlog=errorLog))

        if hold_job is not None:
            if isinstance(hold_job, int):
                native_spec.append(self.spec_fields['DEPENDS'].format(hold_list=hold_job))
            elif isinstance(hold_job, list) or isinstance(hold_job, tuple):
                if len(hold_job) > 0:
                    jid_list = self.spec_fields['DEPENDS_SEP'].join([str(x) for x in hold_job])
                    native_spec.append(self.spec_fields['DEPENDS'].format(hold_list=jid_list))
            else:
                fastr.log.error('Incorrect hold_job type!')

        if hold:
            # Add a user hold to the job
            native_spec.append(self.spec_fields['HOLD'])

        return ' '.join(native_spec)

    # FIXME This needs to be more generic! This is for our SGE cluster only!
    def send_job(self, command, arguments, work_dir, queue=None, resources=None,
                 job_name=None, joinLogFiles=False,
                 outputLog=None, errorLog=None, hold_job=None, hold=False):
        # Create job template
        jt = self.session.createJobTemplate()
        jt.remoteCommand = command

        jt.args = arguments
        jt.joinFiles = joinLogFiles
        env = os.environ
        # Make sure environment modules do not annoy use with bash warnings
        # after the shellshock bug was fixed
        env.pop('BASH_FUNC_module()', None)
        env['PBS_O_INITDIR'] = work_dir
        jt.jobEnvironment = env

        if queue is None:
            queue = self.default_queue

        # Format resource if needed
        if resources.time:
            hours = resources.time // 3600
            minutes = (resources.time % 3600) // 60
            seconds = resources.time % 60

            walltime = '{}:{:02d}:{:02d}'.format(hours, minutes, seconds)
        else:
            walltime = None

        if resources.memory:
            memory = '{}M'.format(resources.memory)
        else:
            memory = None

        # Get native spec from subclass
        native_spec = self.create_native_spec(
            queue=queue,
            walltime=walltime,
            memory=memory,
            ncores=resources.cores,
            outputLog=outputLog,
            errorLog=errorLog,
            hold_job=hold_job,
            hold=hold,
            work_dir=work_dir,
        )

        fastr.log.debug('Setting native spec to: {}'.format(native_spec))
        jt.nativeSpecification = native_spec
        if job_name is None:
            job_name = command
            job_name = job_name.replace(' ', '_')
            job_name = job_name.replace('"', '')
            if len(job_name) > 32:
                job_name = job_name[0:32]

        jt.jobName = job_name

        # Send job to cluster
        job_id = self.session.runJob(jt)

        # Remove job template
        self.session.deleteJobTemplate(jt)

        return job_id

    def submit_jobs(self):
        while self.running:
            try:
                self.check_threads()

                # Max jobs is larger than zero (set) and less/equal than current jobs (full)
                if 0 < self.max_jobs <= self.n_current_jobs:
                    time.sleep(1)
                    continue

                job = self.submit_queue.get(block=True, timeout=2)

                # Get job command and write to file
                command = [sys.executable,
                           os.path.join(fastr.config.executionscript),
                           str(job.commandfile)]
                fastr.log.debug('Command to queue: {}'.format(command))

                # Make sure we do not submit after it stopped running
                if not self.running:
                    break

                fastr.log.debug('Queueing {} [{}] via DRMAA'.format(job.id, job.status))
                work_dir = os.path.abspath(os.path.dirname(job.commandfile))
                # Submit command to scheduler
                cl_job_id = self.send_job(command[0], command[1:], work_dir=work_dir,
                                          job_name='fastr_{}'.format(job.id),
                                          resources=job.resources,
                                          outputLog=job.stdoutfile,
                                          errorLog=job.stderrfile,
                                          hold_job=[self.job_lookup_fastr_drmaa[x] for x in job.hold_jobs if x in self.job_lookup_fastr_drmaa],
                                          hold=job.status == JobState.hold,
                                          )

                # Register job in the translation tables
                with self.job_lookup_lock:
                    self.job_lookup_fastr_drmaa[job.id] = cl_job_id
                self.submit_queue.task_done()
                fastr.log.info('Job {} queued via DRMAA as {}'.format(job.id, cl_job_id))

                # Set the queue lock to indicate there is content in the queue
            except queue.Empty:
                pass

        fastr.log.info('DRMAA submission thread ended!')

    def collect_jobs(self):
        while self.running:
            # Wait for the queue to contain
            try:
                self.check_threads()
                info = self.session.wait(drmaa.Session.JOB_IDS_SESSION_ANY, 2)
            except drmaa.ExitTimeoutException:
                pass  # Nothing there
            except drmaa.InvalidJobException:
                fastr.log.debug('No jobs left (session queue appears to be empty)')
                time.sleep(2)  # Sleep 2 seconds and try again
            except drmaa.NoActiveSessionException:
                self.running = False
                if not self.running:
                    fastr.log.debug('DRMAA session no longer active, quiting collector...')
                else:
                    fastr.log.critical('DRMAA session no longer active, but DRMAA executor not stopped properly! Quitting')
            except drmaa.errors.DrmaaException as exception:
                # Avoid the collector getting completely killed on another DRMAA exception
                fastr.log.warning('Encountered unexpected DRMAA exception: {}'.format(exception))
            except Exception as exception:
                if exceptions.get_message(exception).startswith('code 24:'):
                    # Avoid the collector getting completely killed this specific exception
                    # This is generally a job that got cancelled or something similar
                    fastr.log.warning('Encountered (probably harmless) DRMAA exception: {}'.format(exception))
                else:
                    fastr.log.error('Encountered unexpected exception: {}'.format(exception))
            else:
                self.finished_queue.put(info, block=True)

        fastr.log.info('DRMAA collect jobs thread ended!')

    def dispatch_callbacks(self):
        while self.running:
            try:
                self.check_threads()

                info = self.finished_queue.get(block=True, timeout=2)

                # Make sure we do not submit after it stopped running
                if not self.running:
                    break

                fastr.log.debug('Cluster DRMAA job {} finished'.format(info.jobId))

                # Create a copy of the job that finished and remove from the translation table
                errors = []
                with self.job_lookup_lock:
                    job_id = self.job_lookup_fastr_drmaa.inv.pop(info.jobId, None)
                job = self.job_dict.get(job_id, None)

                if info.hasSignal:
                    errors.append(exceptions.FastrError('Job exited because of a signal, this might indicate it got killed because it attempted to use too much memory (or other resources)').excerpt())

                self.finished_queue.task_done()
                if job is not None:
                    # Send the result to the callback function
                    self.job_finished(job, errors=errors)
                else:
                    fastr.log.warning('Job {} no longer available (got cancelled/processed already?)'.format(info.jobId))
            except queue.Empty:
                pass

        fastr.log.info('DRMAA dispatch callback thread ended!')

    def _get_job_state(self, drmaa_job_id: int) -> "drmaa.JobState":
        try:
            return self.session.jobStatus(drmaa_job_id)
        except drmaa.errors.InvalidJobException:
            # Cannot find job, so status is undetermined
            return drmaa.JobState.UNDETERMINED
        except Exception as exception:
            fastr.log.error(f'Encountered an exception during getting state for job {drmaa_job_id}: '
                            f'[{type(exception).__name__}] {exception}')
            return drmaa.JobState.UNDETERMINED

    def regression_check(self):
        last_update = time.time()

        while self.running:
            self.check_threads()
            if time.time() - last_update < self.regression_check_interval:
                # If it is not time for an extra check, only check undetermined jobs
                # if required, otherwise just sleep
                if self.undetermined_jobs:
                    undetermined_jobs = list(self.undetermined_jobs.keys())

                    for drmaa_job_id in undetermined_jobs:
                        if not self.running:
                            break

                        self._job_regression_check(drmaa_job_id)
                else:
                    time.sleep(1)
                continue

            last_update = time.time()  # Reset timer

            jobs_to_check = list(self.job_lookup_fastr_drmaa.values())
            fastr.log.info(f'Running job regression check, {len(jobs_to_check)} job(s) to be checked')
            fastr.log.info(f'{self.submit_queue.qsize()} waiting to be submitted')
            fastr.log.info(f'{self.finished_queue.qsize()} waiting finished and waiting to be processed')
            fastr.log.info(f'{self.callback_queue.qsize()} waiting waiting for the final callback processing')

            for drmaa_job_id in jobs_to_check:
                if not self.running:
                    break

                self._job_regression_check(drmaa_job_id)

    def _job_regression_check(self, drmaa_job_id: int):
        status = self._get_job_state(drmaa_job_id)

        # Check for undetermined jobs
        if status == drmaa.JobState.UNDETERMINED:
            undetermined_count = self.undetermined_jobs.get(drmaa_job_id, 0) + 1

            # We do not consider the job lost yet, store count and continue
            if undetermined_count < self.num_undetermined_to_fail:
                self.undetermined_jobs[drmaa_job_id] = undetermined_count
                fastr.log.info(f'Job {drmaa_job_id} status could not determined {undetermined_count} times')
                return

        # No undetermined count that is of consequence anymore
        self.undetermined_jobs.pop(drmaa_job_id, 0)

        # Only start cleaning disappeared jobs
        if status not in [drmaa.JobState.DONE,
                          drmaa.JobState.FAILED,
                          drmaa.JobState.UNDETERMINED]:
            return

        fastr.log.info(f'Job {drmaa_job_id} is {status}, calling finished callback')

        # Job failed/done already!
        with self.job_lookup_lock:
            job_id = self.job_lookup_fastr_drmaa.inv.pop(drmaa_job_id, None)
        job = self.job_dict.get(job_id, None)

        # We cannot get the fastr job related to this job, so we cannot continue
        if job is None:
            fastr.log.warning(f'Could not find connected fastr job for {drmaa_job_id}')
            return

        # Send the result to the callback function
        self.job_finished(
            job,
            errors=[exceptions.FastrError(
                "Job collected by the job status checking rather"
                " then getting a callback from DRMAA.").excerpt()])
