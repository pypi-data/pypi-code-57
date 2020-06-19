import sqlite3


class DBSql(object):
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self._create_db()

    def _create_db(self):
        c = self.conn.cursor()

        # Create table
        c.execute('''CREATE TABLE IF NOT EXISTS run_info
                     (run_id text, experiment_ids text, log_dirs text, x blob, y blob, scoring blob, 
                     transform_input blob, x_val blob, y_val blob,
                     CONSTRAINT model_data_pk PRIMARY KEY (run_id))''')

        c.execute('''CREATE TABLE IF NOT EXISTS model_trial
                     (run_id text, experiment_id text, trial_id real, model_key text, metric real, 
                     model blob, params blob, exception text,
                     CONSTRAINT model_trial_pk PRIMARY KEY (run_id, trial_id))''')

        c.execute('''CREATE TABLE IF NOT EXISTS model_search_space
                     (run_id text, model_full_name, instance blob, search_space blob,
                     CONSTRAINT model_sp_pk PRIMARY KEY (run_id, model_full_name))''')

    def insert_trial(self, run_id, exp_id, trial_id, model_key, metric, model_pkl, params_pkl, exception_msg):
        c = self.conn.cursor()
        c.execute("INSERT INTO model_trial VALUES (?,?,?,?,?,?,?,?)", [run_id, exp_id, trial_id, model_key, metric,
                                                                       model_pkl, params_pkl, exception_msg])

    def retrieve_trial_by_run_id(self, run_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM model_trial WHERE run_id = ? ORDER BY metric DESC', [run_id])
        return c.fetchall()

    def retrieve_all_trials(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM model_trial ORDER BY run_id, metric DESC')
        return c.fetchall()

    def delete_trial(self):
        c = self.conn.cursor()
        c.execute("DELETE FROM model_trial")

    def insert_run_info(self, run_id, exp_id, log_dir, raw_input, raw_output, scoring, transform_input, x_val, y_val):
        c = self.conn.cursor()
        c.execute("INSERT INTO run_info VALUES (?,?,?,?,?,?,?,?,?)", [run_id, exp_id, log_dir, raw_input, raw_output,
                                                                      scoring, transform_input, x_val, y_val])
    def update_run_info_exp(self, run_id, exp_ids, log_dirs):
        c = self.conn.cursor()
        c.execute("UPDATE run_info SET experiment_ids = ?, log_dirs = ? WHERE run_id = ?", [exp_ids, log_dirs, run_id])

    def retrieve_run_info_by_run_id(self, run_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM run_info WHERE run_id = ?', [run_id])
        return c.fetchone()

    def delete_run_info(self):
        c = self.conn.cursor()
        c.execute("DELETE FROM run_info")

    def insert_model_space(self, run_id, model_full_name, model_pkl, search_space_pkl):
        c = self.conn.cursor()
        c.execute("INSERT INTO model_search_space VALUES (?,?,?,?)",
                  [run_id, model_full_name, model_pkl, search_space_pkl])

    def retrieve_model_search_space_by_run_id(self, run_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM model_search_space WHERE run_id = ?', [run_id])
        return c.fetchall()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        if self.conn is not None:
            self.conn.close()
