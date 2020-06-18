import os

from testframework.util.assertion import assert_not_null


def get_gcp_project_id():
    project_id = os.environ["GCP_PROJECT_ID"]
    assert_not_null(project_id)
    return project_id


def get_gcp_backup_project_id():
    backup_project_id = os.environ["GCP_BACKUP_PROJECT"]
    assert_not_null(backup_project_id)
    return backup_project_id


def get_bigtable_project_id():
    bigtable_project_id = os.environ["BIGTABLE_PROJECT_ID"]
    assert_not_null(bigtable_project_id)
    return bigtable_project_id


