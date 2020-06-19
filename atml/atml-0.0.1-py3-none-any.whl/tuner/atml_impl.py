from datetime import datetime
import os

import pandas as pd
from sklearn.metrics import accuracy_score
import logzero
from logzero import logger

from .db.model_dao import ModelDao
from .model_repo_manager import TunerModelManager
from .nni_exec_manager import NniExecutionManager

from ..util import atm_util as util

logzero.logfile(os.path.join(os.path.dirname(__file__), "..", "..", "atml.log"))

class AtmlOrchestrator(object):
    def __init__(self, exec_config=None, with_default=True):

        self.run_id = datetime.now().strftime("%Y%m%d%H%M%S")
        run_dir = os.path.join(util.get_run_dir(), self.run_id)
        os.makedirs(run_dir, exist_ok=True)
        logger.info('run_id: {0}'.format(self.run_id))
        logger.info('run_dir: {0}'.format(run_dir))
        logger.info('with_default: {0}'.format(with_default))

        self.dao = ModelDao(run_dir)
        self.model_manager = TunerModelManager(self.run_id, self.dao, with_default)
        self.nni_executor = NniExecutionManager(self.run_id, run_dir, self.model_manager, self.dao, exec_config)

    def run(self, X, y, scoring=accuracy_score, X_val=None, y_val=None):
        self.nni_executor.execute(X, y, scoring, X_val, y_val)

    def set_exec_config_param(self, key, value):
        self.nni_executor.exec_config[key] = value

    def set_model_search_param(self, instance, attr, value):
        _, _, model_key = util.class_detail(instance)
        m_config = self.model_manager.repo[model_key]
        m_config[attr]['_value'] = value

    def choose_models(self, instances):
        m_config = self.model_manager.repo.copy()
        self.model_manager.repo = {}
        for instance in instances:
            _, _, key = util.class_detail(instance)
            self.model_manager.repo[key] = m_config[key]

    def remove_models(self, instances):
        for instance in instances:
            _, _, key = util.class_detail(instance)
            self.model_manager.repo.pop(key)

    def clear_models(self):
        self.model_manager.repo.clear()

    def get_available_models_and_spaces(self):
        return self.model_manager.repo

    def register_model_search(self, instance, search_space):
        self.model_manager.register(instance, search_space)

    def get_all_trials(self, with_exception=False):
        result = {
            'RUN_ID': [],
            'EXP_ID': [],
            'TRIAL_ID': [],
            'MODEL_KEY': [],
            'METRIC': [],
            'MODEL': [],
            'PARAMS': [],
            'EXCEPTION': [],
        }
        for trial in self.dao.retrieve_trials(self.run_id):
            result['RUN_ID'].append(trial[0])
            result['EXP_ID'].append(trial[1])
            result['TRIAL_ID'].append(trial[2])
            result['MODEL_KEY'].append(trial[3])
            result['METRIC'].append(trial[4])
            result['MODEL'].append(trial[5])
            result['PARAMS'].append(trial[6])
            result['EXCEPTION'].append(trial[7])

        df = pd.DataFrame.from_dict(result)
        if with_exception:
            return df
        else:
            return df[df['EXCEPTION'].isnull()]

    def get_best_model_details(self, instance=None):
        all_trials_df = self.get_all_trials()
        if len(all_trials_df) > 0:
            if instance is None:
                return all_trials_df.iloc[0]
            else:
                model_key = util.class_detail(instance)[2]
                result = all_trials_df[all_trials_df['MODEL_KEY'] == model_key]
                if len(result) > 0:
                    return result.iloc[0]
