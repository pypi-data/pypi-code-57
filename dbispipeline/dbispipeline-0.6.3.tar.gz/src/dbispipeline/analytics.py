"""Module containing tools to run result analytics."""
import pandas as pd

from .db import DB
from .db import DbModel
from .utils import load_project_config


def _extract_metric_results(outcome, requested_metric):
    return outcome.apply(
        lambda row: row.apply(lambda value: value[requested_metric]))


def fetch_by_git_commit_id(git_commit_id):
    """Returns a query that is filtered by git commit id.

    Args:
        git_commit_id: the commit id of the returned results.
    """
    session = DB.session()
    return session.query(DbModel).filter(
        DbModel.git_commit_id == git_commit_id)


def fetch_by_row_ids(from_id, to_id=None):
    """Returns a query in the given range of ids.

    Args:
        from_id: the smalles database id included in the results of the query.
        to_id: if specified, this is the biggest database id included in the
            results of the query.
    """
    session = DB.session()
    query = session.query(DbModel).filter(DbModel.id >= from_id)
    if to_id is not None:
        return query.filter(DbModel.id <= to_id)
    return query


def fetch_by_project_name(project=None):
    """Returns a query filtered by project.

    Args:
        project: the name of the project to extract results. If None, the
            project in the dbispipeline.ini is used.
    """
    if project is None:
        project = load_project_config()['project']['name']

    session = DB.session()
    return session.query(DbModel).filter(DbModel.project_name == project)


def get_cv_epoch_evaluator_results(requested_metric=None,
                                   query_function=fetch_by_project_name):
    """Extracts CvEpochEvaluator results from the database.

    Args:
        requested_metric: allows to restrict the results to a single metric.
        query_function: a function returing a SQLAlchemy query when called.

    Returns: A tuple containing the prepared results as first element and the
        whole db entry as the second entry. The prepared results are eighter a
        pandas dataframe if a metric is requested or a dict containing a pandas
        dataframe per metric.
    """
    for run in query_function():
        if run.evaluator['class'] == 'CvEpochEvaluator':
            outcome = pd.DataFrame(run.outcome)

            if requested_metric is None:
                results = {}
                for available_metric in run.evaluator['scoring']:
                    results[available_metric] = _extract_metric_results(
                        outcome,
                        available_metric,
                    )
                yield results, run
            elif requested_metric in run.evaluator['scoring']:
                yield _extract_metric_results(outcome, requested_metric), run
