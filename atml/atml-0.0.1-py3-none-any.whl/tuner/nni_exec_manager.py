import json
import os
import subprocess
import time
import shutil
import webbrowser

from logzero import logger
import nnicli as nc

from sklearn.model_selection import train_test_split

from ..util import atm_util as util

class NniExecutionManager(object):
    def __init__(self, run_id, run_dir, model_repo, dao, exec_config):
        self.run_id = run_id
        self.run_dir = run_dir
        self.model_repo = model_repo
        self.dao = dao
        self.current_dir = os.path.dirname(__file__)
        self.exec_config = util.parse_nni_exec_yaml(os.path.join(self.current_dir, 'config', 'default_nni_exec.yml'))
        logger.debug('Default NNI Execution Config: {0}'.format(self.exec_config))
        if exec_config is not None:
            self.exec_config.update(exec_config)

    def execute(self, X, y, scoring, X_val=None, y_val=None):
        if X_val is not None and y_val is not None:
            x_train, x_test, y_train, y_test = X, X_val, y, y_val
        else:
            x_train, x_test, y_train, y_test = train_test_split(X, y, random_state=88, test_size=0.2)

        self.dao.insert_run_info(self.run_id, None, None, x_train, y_train, scoring, None, x_test, y_test)

        for model_key in self.model_repo.repo:
            max_trials = self.model_repo.count_map[model_key]
            self.exec_config['max_trials'] = max_trials

            self._generate_nni_exec_config(model_key)
            self._generate_model_exec_files(model_key)

            config_path = os.path.join(self.run_dir, model_key + "_nni.yaml")
            base_port = self.exec_config['base_port']
            endpoint = "http://localhost:{0}".format(base_port)
            nc.set_endpoint(endpoint)

            try:
                self._stop_nni(model_key, base_port, False)

                logger.info('Starting Hyperparameter Tuning with {0}'.format(model_key))
                self._start_nni(model_key, config_path, base_port)
                webbrowser.open(endpoint)

                exp_id = nc.get_experiment_profile()['id']
                log_dir = nc.get_experiment_profile()['logDir']
                self.dao.update_run_info_exp(self.run_id, exp_id, log_dir)

                succeed_count = 0
                seconds = 1
                while True:
                    time.sleep(1)
                    stats = nc.get_job_statistics()
                    for stat in stats:
                        if stat['trialJobStatus'] == 'SUCCEEDED':
                            succeed_count = stat['trialJobNumber']

                    if seconds % 10 == 0:
                        print('{0} seconds taken. Number of trials succeeded: {1}'.format(seconds, succeed_count))

                    experiment = nc.get_experiment_status()
                    if experiment['status'] == 'DONE':
                        print('Experiment finished. {0} seconds taken. Number of trials succeeded: {1}'.format(seconds, succeed_count))
                        break

                    seconds += 1
            finally:
                self._stop_nni(model_key, base_port)

    def _start_nni(self, model_key, config_path, base_port):
        msg = "for {0} Started".format(model_key)
        self._execute_command(['nnictl', 'create', '--config', config_path, '--port', str(base_port)], base_port, msg)

    def _stop_nni(self, model_key, base_port, log_flag=True):
        msg = "for {0} Stopped".format(model_key)
        self._execute_command(['nnictl', 'stop', '--all'], base_port, msg, log_flag)
        time.sleep(3)

    def _execute_command(self, command, port, msg='', log_flag=True):
        process = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if "ERROR" in str(stdout):
            for line in stdout.splitlines():
                if "ERROR" in str(line):
                    logger.info(line)
        else:
            if log_flag:
                logger.info('http://localhost:{0} {1}'.format(port, msg))


    def _generate_nni_exec_config(self, model_key):
        nni_template = os.path.join(self.current_dir, 'config', 'nni_template.yml')
        out_nni_file = os.path.join(self.run_dir, model_key + '_nni.yaml')

        m = open(nni_template, 'r').read()
        nni_out = open(out_nni_file, 'w')

        m = self._populate_exec_template(m, model_key)

        nni_out.write(m)
        nni_out.close()


    def _populate_exec_template(self, m, model_key):
        m = m.replace("$EXP_NAME", model_key)
        m = m.replace("$CONCURRENCY", self.exec_config['concurrency'])
        m = m.replace("$MAX_DURATION", self.exec_config['max_duration'])
        m = m.replace("$MAX_TRAIL", self.exec_config['max_trials'])
        m = m.replace("$TRAIN_PLATFORM", self.exec_config['training_platform'])
        m = m.replace("$SEARCH_SPACE_PATH", os.path.join(self.run_dir, model_key + '.json'))
        m = m.replace("$TUNER", self.exec_config['tuner'])
        m = m.replace("$MODEL_KEY", model_key)
        m = m.replace("$RUN_ID", self.run_id)
        m = m.replace("$RUN_DIR", self.run_dir)
        m = m.replace("$MAIN_MODULE", 'executor')
        m = m.replace("$CODE_DIR", os.path.join(self.current_dir, '..', '..'))
        m = m.replace("$OPTIMIZE_MODE", self.exec_config['optimize_mode'])

        if shutil.which('python3') is not None:
            m = m.replace("$PYTHON_EXE", 'python3')
        else:
            m = m.replace("$PYTHON_EXE", 'python')

        return m

    def _generate_model_exec_files(self, model_key):
        out_model_file = os.path.join(self.run_dir, model_key + '.json')
        with open(out_model_file, 'w') as outfile:
            json.dump(self.model_repo.repo[model_key], outfile, indent=4, sort_keys=True)