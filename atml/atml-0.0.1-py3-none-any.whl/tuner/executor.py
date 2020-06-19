import sys
import traceback
import os

from sklearn.metrics import accuracy_score
import nni
import logzero
from logzero import logger

from .db.model_dao import ModelDao

logzero.logfile(os.path.join(os.path.dirname(__file__), "..", "..", "..", "atml.log"))

class TrialExecution(object):
    def __init__(self, model_key, run_id, run_dir):
        self.model_key = model_key
        self.run_id = run_id
        self.run_dir = run_dir
        self.trial_id = nni.get_trial_id()
        self.exp_id = nni.get_experiment_id()
        self.scoring = accuracy_score

    def _load_data(self, dao):
        logger.info('Retrieving data for run_id: ', self.run_id)
        data = dao.retrieve_run_info(self.run_id)

        x_train = data[3]
        y_train = data[4]
        self.scoring = data[5]
        x_test = data[7]
        y_test = data[8]

        return x_train, x_test, y_train, y_test

    def _get_model(self, model_key, received_params, dao):
        """Get model according to parameters"""

        target_model_instance = None
        for _, model_full_name, model, _ in dao.retrieve_search_space(self.run_id):
            if model_key == model_full_name:
                target_model_instance = model
                break

        logger.info('target_model_instance: {0}'.format(target_model_instance))
        logger.info('PARAMS: {0}'.format(received_params))
        for key in received_params:
            setattr(target_model_instance, key, received_params[key])

        return target_model_instance

    def _run_trial(self, X_train, X_test, y_train, y_test, model, received_params, dao):
        """Train model and predict result"""

        try:
            model.fit(X_train, y_train)
            y_test_pred = model.predict(X_test)
            score = self.scoring(y_test, y_test_pred)
            logger.info('score: %s' % score)
            nni.report_final_result(score)

            dao.insert_trial(self.run_id, self.exp_id, self.trial_id, self.model_key, score, model, received_params)
        except Exception as e:
            dao.insert_trial(self.run_id, self.exp_id, self.trial_id, self.model_key, score, model, received_params,
                             traceback.format_exc())
            raise e

    def execute(self):
        dao = None
        try:
            dao = ModelDao(self.run_dir)
            X_train, X_test, y_train, y_test = self._load_data(dao)

            # get parameters from tuner
            received_params = nni.get_next_parameter()
            logger.debug(received_params)

            model = self._get_model(self.model_key, received_params, dao)

            self._run_trial(X_train, X_test, y_train, y_test, model, received_params, dao)
        except Exception as exception:
            logger.exception(exception)
            raise
        finally:
            if dao is not None:
                dao.close()


if __name__ == '__main__':
    model_key = sys.argv[1]
    run_id = sys.argv[2]
    run_dir = sys.argv[3]

    execution = TrialExecution(model_key, run_id, run_dir)
    execution.execute()
