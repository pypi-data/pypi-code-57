# -*- coding: utf-8 -*-
"""
tracking client for mlflow
"""

import mlflow
import pandas as pd
from sail_utils.mlflow.config import MAX_RESULTS


class MLFlowClient:
    """
    mlflow client class
    """

    def __init__(self, server: str):
        self._client = mlflow.tracking.MlflowClient(tracking_uri=server)

    def get_experiments(self, experiment_id: int, max_result: int = MAX_RESULTS) -> pd.DataFrame:
        """
        get an experiment's report
        :param experiment_id:
        :param max_result:
        :return:
        """
        runs_info = self._client.search_runs(experiment_ids=experiment_id,
                                             max_results=max_result)

        results = dict()
        column_names = set()
        fields = ['metrics', 'params', 'info', 'tags']
        for i, run in enumerate(runs_info):
            results[i] = dict()
            info = run.to_dictionary()
            results[i]['metrics'] = info['data']['metrics']
            results[i]['params'] = info['data']['params']
            results[i]['info'] = info['info']
            results[i]['tags'] = info['data']['tags']
            for field in fields:
                for name in results[i][field]:
                    column_names.add((field, name))

        report_df = pd.DataFrame(columns=pd.MultiIndex.from_tuples(column_names))
        for field in fields:
            for i, run in results.items():
                for name, value in run[field].items():
                    report_df.loc[i, (field, name)] = value
        return report_df.T.sort_index(level=[0, 1]).T
