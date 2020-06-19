import pickle
import os

from ..db.model_db import DBSql
from ...util import atm_util as util

class ModelDao(object):
    def __init__(self, run_dir):
        db_file = os.path.join(run_dir, 'atml.sqlite')
        self.sql = DBSql(db_file)

    def insert_trial(self, run_id, exp_id, trial_id, model_key, metric, model, params, exception_msg=None):
        model_pkl = util.to_pickle(model)
        params_pkl = util.to_pickle(params)
        try:
            self.sql.insert_trial(run_id, exp_id, trial_id, model_key, metric, model_pkl, params_pkl, exception_msg)
            self.sql.commit()
        except Exception:
            self.sql.rollback()
            raise

    def retrieve_trials(self, run_id=None):
        if run_id is None:
            result = self.sql.retrieve_all_trials()
        else:
            result = self.sql.retrieve_trial_by_run_id(run_id)

        for row in result:
            yield row[0], row[1], row[2], row[3], row[4], pickle.loads(row[5]), pickle.loads(row[6]), row[7]

    def insert_run_info(self, run_id, exp_ids, log_dirs, raw_input, raw_output, scoring, transform_input=None, x_val=None, y_val=None):
        input_pkl = util.to_pickle(raw_input)
        output_pkl = util.to_pickle(raw_output)
        scoring_pkl = util.to_pickle(scoring)
        transform_pkl = util.to_pickle(transform_input)
        x_val_pkl = util.to_pickle(x_val)
        y_val_pkl = util.to_pickle(y_val)

        try:
            self.sql.insert_run_info(run_id, exp_ids, log_dirs, input_pkl, output_pkl, scoring_pkl, transform_pkl, x_val_pkl, y_val_pkl)
            self.sql.commit()
        except Exception:
            self.sql.rollback()
            raise

    def update_run_info_exp(self, run_id, exp_id, log_dir):
        run_info = self.retrieve_run_info(run_id)
        if run_info is not None:
            exp_ids = exp_id if run_info[1] is None else run_info[1] + ',' + exp_id
            log_dirs = log_dir if run_info[2] is None else run_info[2] + ',' + log_dir
            try:
                self.sql.update_run_info_exp(run_id, exp_ids, log_dirs)
                self.sql.commit()
            except Exception:
                self.sql.rollback()
                raise

    def retrieve_run_info(self, run_id):
        row = self.sql.retrieve_run_info_by_run_id(run_id)

        if row is not None:
            run_id = row[0]
            exp_ids = row[1]
            log_dirs = row[2]
            raw_input = util.from_pickle(row[3])
            raw_output = util.from_pickle(row[4])
            scoring = util.from_pickle(row[5])
            transform_input = util.from_pickle(row[6])
            x_val = util.from_pickle(row[7])
            y_val = util.from_pickle(row[8])

            return run_id, exp_ids, log_dirs, raw_input, raw_output, scoring, transform_input, x_val, y_val

    def insert_search_space(self, run_id, model_full_name, model, search_space):
        model_pkl = pickle.dumps(model)
        search_space_pkl = pickle.dumps(search_space)
        try:
            self.sql.insert_model_space(run_id, model_full_name, model_pkl, search_space_pkl)
            self.sql.commit()
        except Exception:
            self.sql.rollback()
            raise

    def retrieve_search_space(self, run_id):
        result = self.sql.retrieve_model_search_space_by_run_id(run_id)
        for row in result:
            yield row[0], row[1], pickle.loads(row[2]), pickle.loads(row[3])

    def close(self):
        if self.sql is not None:
            self.sql.close()
